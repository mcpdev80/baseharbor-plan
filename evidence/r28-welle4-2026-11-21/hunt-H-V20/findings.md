# BUG-HUNT slice H-V20 - three 'gereichte Aenderungen' on develop 513488eeb6d

ROLE: Worker. CARD: t-20261114-r28-cli2-app-export (0428-065). SLICE: H-V20 (BUG-HUNT fill, AGENTS 3.3.5). MISSION: /var/tmp/hunt20.g.md.
BASE: develop 513488eeb6d788f0e5eec054be89807505f05e08 (measured, real github origin via `git ls-remote`).
MODE: read-only findings, no commit / no push / no PR / no comment in baseharbor.

## PLAN

1. ls-remote (double-write protection) on real github origin; confirm develop = 513488eeb6d, worktree head = 6585feaa. Read-only; no git changes to product worktree.
2. Slice 1 (#1585 target-isolation per state root): can `baha --state-root A` use a target from B via an env var or cache entry? Trace the selection chain, ordering, file:line.
3. Slice 2 (#1596 orgconfig-redaction): are redacted keys reused where the unredacted key serves as index (`_lookup_` / `_map-key_`)? file:line.
4. Slice 3 (#1702 perses per-signal backend witness): mixed case (one signal reachable, one not) - does the command emit unreachable / ok / mixed, and does it match the akte?
5. Write findings.md (own plan-worktree), publish to origin/main.

## Double-write protection (before any read)

git remote -v (REMOTE GUARD):
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)

git ls-remote BEFORE work:
513488eeb6d788f0e5eec054be89807505f05e08 refs/heads/develop
worktree HEAD 6585feaac37c8d634f6de6be1079a17caf89d107 (card 0428-065 head, unrelated to slice)

Worktree git status after read-only investigation: clean (no staged/unstaged changes to product files).

## Findings

### Finding 1 - Slice 1 (#1585) target-isolation per state root: NO HIJACK (severity: nicht-blockierend)

Question: with `--state-root A` (operator-set, via `BASEHARBOR_STATE_DIR=A`), can an env var or cache entry let the CLI use a target from a foreign installation B?

Expected: fail-closed - root A's selection resolves only from A's own state; B's target / org default / cache never enters.

Actual: isolation holds. Selection chain traced:

- `effectiveTarget` (cmd/baha/target.go:88) branches on `deployment.StateRootSelected()` (= `BASEHARBOR_STATE_DIR` set, `internal/deployment/target.go:134-146`). With `--state-root A` the dedicated chain `resolveTargetBelowStateRoot` (cmd/baha/target_state_layout.go:32) runs.
- Ordering in `resolveTargetBelowStateRoot` (cmd/baha/target_state_layout.go:32-76), checked in order:
  1. `explicit` (--state-root target flag) -> `cfg.ResolveTarget` (line 33-35).
  2. `selected` (populated from env `BASEHARBOR_TARGET` at target.go:94) -> only accepted if `cfg.Targets[selected]` is a registration of THIS root or `local` (line 36-40). A foreign name fails membership and does not resolve.
  3. persisted activation below the root (line 41-55): a persisted name with no registration of this root fails closed (line 52-54), never falls through to an org default.
  4. organization default ONLY if `orgconfig.StateRootOwnsOrganizationState(state)` (line 62): the default is read from this root's own state.
  5. else fail-closed (line 68-73), never a foreign default / builtin `local` fallback.
- The env var `BASEHARBOR_TARGET` (cmd/baha/target.go:94) is a legitimate per-command target override, NOT an installation-identity hijack: it is still validated against this root's `cfg.Targets` membership before it resolves anything, and it cannot cross a state-root boundary to B's registration.
- Cache-path angle (`internal/orgconfig/store.go:402-443`): `StateRootOwnsOrganizationState` requires the active-state source location OR cache path to be inside the selected root; `selectsWithin` (store.go:432-443) admits a path only when `path == root || strings.HasPrefix(path, root+sep)`, and any source outside the root falls through to `false` (store.go:443). A foreign cache entry from B is therefore treated as foreign organization state and never resolves a target for A.
- `resolveTargetBelowStateRootFallback` (cmd/baha/target_state_layout.go:78-103) fails closed on ambiguous multi-registration and only admits a single root-local registration (line 86-92). No foreign path.

Reproduction: read-only trace only (no container, no second installation on this host). Source lines above are the witnesses.

Conclusion: with `--state-root A`, an env var or a cache entry set for installation B does NOT let A use B's target. The state-root boundary (BF-01) holds. No fix required.

### Finding 2 - Slice 2 (#1596) orgconfig-redaction: NO REDACTED-KEY-AS-INDEX LEAK (severity: nicht-blockierend)

Question: are redacted keys reused at a place where the unredacted key serves as the index (`_lookup_` / `_map-key_`)?

Expected: all maps are keyed by identity/name/field, never by a secret value; redaction only sanitizes surfaced error text; no map key is a redacted secret that leaks when re-read.

Actual: no leak. Structural evidence:

- orgconfig stores REFERENCES ONLY, never secret material (internal/orgconfig/model.go:44-46 Reference struct; validation rejects inline secrets model.go:126-127, 146-147, 172-173, 271-272, 291-292). `PreferenceDigest` (internal/orgconfig/scope.go:126) hashes the (non-secret) `EnvironmentDefaults` struct; its maps (`EnvironmentDefaults.Target/Stack/Providers/Trust/Policies`, model.go:79-85) are keyed by target name / provider name / trust name, not values.
- Profile lookup keyed by identity, not value: `ProfileKey(name, target)` (internal/orgconfig/profiles.go:265) = `name=|target=`. `Manager.GetByKey(name, target)` / `Manager.Get(name)` key by name/target (profiles.go:552, 564). `ProfileMap` keys by `ProfileKey` (profiles.go:603). No secret value is ever a map key.
- Resolver maps keyed by definition Name, secrets excluded by construction: `PersistableValues` (internal/applicationinput/resolver.go:118-127) drops secret values entirely; `SecretValues` (resolver.go:129-138) keys by the definition `Name`, never by the secret value. `Value.String()` renders `"<redacted>"` but the value is never used as a key.
- The only "redaction" in orgconfig is error stderr sanitization, not value-as-key: source.go:217 ("redacting %v wrappers so the classifier still recognises the fail-closed path"), source_oci.go:156-168 (redacted error class), app_maintenance_client.go:655-657 (`redactMaintenanceInput`), application_registry_source.go:288/650 (`exitStatusError` redacts stderr to a fixed class). None of these map a redacted string to a secret as an index.

Reproduction: read-only structural trace only. No container. Source lines above are the witnesses.

Conclusion: there is no place where a redacted key is reused where the unredacted key serves as index. The `_lookup_`/`_map-key_` pattern is keyed by identity/name, never by secret value. No fix required.

### Finding 3 - Slice 3 (#1702) perses per-signal backend witness: MIXED CASE HANDLED, MATCHES AKE (severity: nicht-blockierend)

Question: mixed case (one observability signal reachable, one not) - does `baha app perses status` emit unreachable / ok / mixed, and does it match the akte?

Expected: each backend (Prometheus/Loki/Tempo) reports its OWN three-state witness (not-configured / configured / unreachable) from its OWN resolved signal; a mixed case emits mixed per-backend verdicts; identical witness on the human `perses status` face and the machine `app status` host-containers JSON (no drift).

Actual: holds. `persesBackendSignalWitnessFromManifest` (cmd/baha/app_status_result.go:110-202) emits one verdict per backend from that backend's own signal:
- Prometheus (app_status_result.go:124-146): `configured` when `HasMetricsSources && resolvedHostSignalStatus==ObservabilitySupported && witness.PrometheusProven`, else `unreachable` (line 132-139), else `not-configured` (line 140-146).
- Loki (app_status_result.go:150-173): same shape with `witness.LokiProven`.
- Tempo (app_status_result.go:177-200): same shape with `witness.TempoProven`.
- Mixed case: e.g. `witness.PersesBackendSignalWitness{PrometheusProven: true, LokiProven: false}` with all declared yields `prometheus: configured` + `loki: unreachable` (each line carries its own source-id: `metrics.sources` / `logs.collect`). The command never returns a single blended "ok"; it returns one independent verdict per backend.
- Shared witness across faces: `renderPersesBackendWitness` (cmd/baha/perses_lifecycle.go:315) and the machine `app status` JSON (app_status_result.go:313, 417) call the same `persesBackendSignalWitnessFromManifest`, so the human `perses status` face (perses_lifecycle.go:235) and the machine face never drift.
- Three-state constants (cmd/baha/app_status_result.go:70-75): `not-configured`, `configured`, `unreachable` - never "ok"/"verified"/"healthy".

Akte match: card 0428-142 mandates real `unreachable` emitted from a resolved (declared-but-unreachable) signal, per-backend source-id bound, no drift between the two faces. The existing tests pin it: `TestPersesStatusWitnessConfiguredWhenResolved` (cmd/baha/app_status_result_test.go:134, all `Proven:true` -> all `configured`) and `TestPersesStatusWitnessUnreachableWhenDeclaredNotResolved` (:178, empty witness -> all `unreachable`). The mixed outcome is the union of these two independent per-backend branches.

Reproduction: read-only trace + the two existing unit tests above (no container). Source lines are the witnesses.

Conclusion: the mixed case is correctly mixed (one backend `configured`, the other `unreachable`), derived from each backend's own resolved signal, matching the akte. No drift between human and machine faces. No fix required.

## repo-rule compliance

- Read-only findings only: NO commit, NO push, NO PR, NO comment in baseharbor (mission rule).
- No subagents (AGENTS 4.8). No .github/** / scripts/** change.
- No merge/close of card 0428-065 (its verdict is at acceptance).
- Evidence written only in the own plan-worktree (baseharbor-plan, tooling #29); never in the product checkout.
- No containers or compose projects started (worktree-only investigation).

## cleanliness

- docker ps -a BEFORE: 8 containers (all pre-existing, Exited, names bh-itest-* from other lanes).
- docker ps -a AFTER: 8 containers (unchanged; no containers/compose started this hunt).
- No new networks / volumes / state directories created.
- ambient-core / fremder-carrier images: unangetastet.
- worktree git status: clean (no product changes).
