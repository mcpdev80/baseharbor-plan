# H-V47 intake — bug hunt findings to cards (w193-0428-224-hunt-v47-intake)

Lane: w193-0428-224-hunt-v47-intake. Mission: turn the H-V47 bug-hunt findings
BF-47-1..9 (akte `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/README.md`,
plan origin/main `59a288736`, anchored develop `99d9ddebc`) into bug cards.
Planning-only; no product-code changes. One new row (BF-47-11) was discovered at intake.

## PLAN

- Read the akte fully — DONE (all 10 rows + cross-reference notes).
- ls-remote develop tip, fresh product worktree at exact tip — DONE (`99d9ddebc`,
  worktree `workers/w193-hunt-v47-intake-wt`, detached HEAD).
- Reproduce/confirm each BF-47 row at the tip (CLI binaries built from tip + v0.4.18
  in isolated /tmp/opencode zones, plus named-case unit probes) — DONE.
- File bug cards for still-live findings, cluster same-root-cause rows — DONE
  (8 new cards 0428-341..349 + one intake-discovered row 0428-350; mapping table below).
- Update the hunt akte with a per-finding disposition line + mapping table — DONE (appended to README.md).
- render + check + publish via isolated plan worktree, lane-identity commit — see witnesses below.
- Verify cards + evidence on origin/main (ls-tree), then END — see witness below.

## Base attestation and remote witnesses

Planning repo check BEFORE first evidence commit
(`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Product remote truth (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`):

```
99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82	refs/heads/develop
```

- Same value as the akte anchor; develop has NOT moved since the hunt, so every
  file:line in the akte was re-measured against the exact tip (fresh worktree at
  `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`, verified via `git rev-parse HEAD`).
- The quarantined `workers/baseharbor` checkout refs were never cited; remote
  truth came from `git ls-remote` and `git fetch` on the URL-resolved github remotes.
- Planning repo is a SHARED checkout: all plan writes happened in the isolated
  worktree `workers/w193-hunt-v47-intake-plan` created from `origin/main`
  (`git worktree add ... origin/main -b lane-0428-224-hunt47-intake-w193`); no
  rebase/reset/stash in the shared checkout.

## Per-finding verification at develop 99d9ddebc

- BF-47-1 LIVE (reproduced 3 ways). Unit probe at the tip: authentic v1 fixture through
  `ReconcileReferenceProviderRegistryAt` → `validate provider registry: unsupported provider
  registry version 1`; same via `RegistryStore.Load`. CLI probe: v0.4.18 binary (`go build`
  of tag v0.4.18 at `bf60b0d83`) writes a real v1 registry (`"version": 1`, name-owned shape
  confirmed by reading `642bc6abd^`/tag source); develop-tip `baha app init --yes` on that
  state → the same wall, file unchanged (no reconcile write reachable). Version-bumping only
  the number fails at `stableid.ValidateUUIDv4` (registry.go:419) — the CHANGELOG sentence
  ("existing environmentless v1 entries remain readable and migrate during reconciliation",
  present verbatim in BOTH v0.4.18 CHANGELOG:52 and v0.4.19 CHANGELOG:89) promises a
  migration that no shipped code performs. → 0428-341.
- BF-47-2 LIVE. Gate re-measured (deployment_store.go:661-670, save refusal :418-423, drift
  text :51-52, CLI translation app_context.go:452-463, downgrade refusal
  update_mutation.go:43-45). Intake unit witness: genuine name-only v1 record →
  `listAllDeployments` yields 0 records + 1 `deployable_version_mismatch` warning —
  invisible to every listing/removal path. Note the warning Identity carries `Target` only
  (ApplicationID/Application/Environment empty), so the CLI SKIPPED line reads
  "deployment <uuid>" with no app name. → 0428-342.
- BF-47-3 PARTIALLY LIVE (mechanism corrected). Direct call probe:
  `fullDestroyDeploymentWarnings` renders a `deployable_version_mismatch` warning with the
  WRONG generic "incomplete deployment state has no usable deployment.json" text — the
  disclosure defect is confirmed. The akte's "destroy --all skips then RemoveAll" is NOT
  reachable as stated: with a v1 record, `destroy --all` aborts earlier at the strict
  listing seam (`countFullDestroyBlockers`-clean but `ListAllDeployments` error via
  prepare/impact paths: "Provider consumer inventory is incomplete or damaged"
  — proven end-to-end with a temp installation fixture at the tip). The data root is
  therefore NOT removed while the record is unloadable; the defect reduces to the false
  disclosure line (and its FAILED-vs-SKIPPED choice once 0428-342 lands). → 0428-343 (bug,
  severity lowered to low: message accuracy, no data loss found).
- BF-47-4 LIVE and WIDENED. The recover branch (update.go:92-94) has no preflight
  (`recoverNativeCoreHA` never calls `coreupdate.LoadRelease`; catalog ships only
  releases/v0.4.24.json) — confirmed by reading the dispatch chain. Intake ADDITION:
  the documented verb never dispatches at all: `extractGlobalOutputOptions`
  (main.go:212) treats any `--version` token as the global flag and runWithIO errors
  "–-version cannot be combined with a command" for EVERY ordering — proven in-process
  (probe `runWithIO` and the built binary; also for `update --yes --version X`, the form
  docs/cli/core.md:86 itself prints). v0.4.18 behaves identically (long-standing).
  → 0428-344 (raised to normal priority: the documented recovery verb is dead).
- BF-47-5 PARTIALLY SUPERSEDED. The akte's central claim ("Compatibility hook wired only in
  test fixtures; CheckUpgradePath always errors") is REFUTED: production wires it —
  cmd/baha/update_core_native.go:176 and update_provider_binding_runtime.go:280 pass
  `o.keycloakUpgradePath` (update_provider_binding_runtime.go:76-81: admits exactly
  26.7.5→26.8.0 non-HA, else `patchProviderUpgradePath` same-minor strictly-newer).
  The nil-hook error (native_ops.go:49-53) is defense-in-depth only (adapter_test.go /
  native_ops_test.go:63 fixtures). Residual live defect: docs overstate `migration_required`
  as executable while support is a hardcoded single transition → docs-accuracy bug.
  → 0428-346 (severity low).
- BF-47-6 LIVE (two intake corrections). Probe at the tip: installed `17.9-aarch64` /
  target `18.1` → Unsupported "Core provider downgrade or unverifiable version" — the
  downgrade-mislabel for a strictly-newer target is confirmed. The akte's example
  "26.8.0-rc1 vs 26.8.0 → no precedence" is wrong: plan.go's parser ERRORS before any
  comparison; the true repo-internal inconsistency is that `providerupgrade.ParseVersion`
  (version.go:15-35) strips `-rc1` and parses fine while plan.go (76-119) rejects the same
  string. Existing test already pins `{"26.8.0-rc1","26.8.0",true}`. → 0428-348 (low).
- BF-47-7 PARTIALLY LIVE (split). Live: mutation-path asymmetry —
  `LoadConfigForMutation` (config_mutation.go:20-40) skips `migrateAndPersistTargetUIDs`.
  Refuted at intake: "read-only commands mutate as a surprise" is the documented design
  (target.go:86 comment; `MigrateLegacyTargetUIDs` fills empty UIDs only) and the akte's
  "status could surface a too-new config read-only" is impossible — BOTH paths die at the
  same `decodeConfig` gate; probe witness: `version: 2` config → bare
  "unsupported BaseHarbor config version 2" everywhere (a `baha status` in a repo showed a
  MISLEADING repository-inspection error where the real cause is the config wall — filed
  into the error-surface card). → asymmetry 0428-349; version wall → 0428-345.
- BF-47-8 LIVE (both halves). `git grep -l 'written_by'` at the tip hits exactly one file,
  cmd/baha/agent.go (report struct) — no state writer stamps its release. Human format
  coupling confirmed: main.go:139 prints `BaseHarbor %s…` while commands.go:205 prints
  `baha %s (commit …)` and `verifyCandidateVersion` (update_mutation.go:289-301) binds the
  latter prefix; self-update fixtures in update_mutation_test.go already depend on that
  exact prose. → stamp + JSON-contract half 0428-347; direction/next-action text half 0428-345.
- BF-47-9 LIVE. Exact-equality gates re-measured (registry.go:395, shared_backends_state.go:31,
  hosttrust.go:404 et al.); `DamagedDirectoryState` fires only when deployment.json is ABSENT
  (damaged_state.go:188-191) — confirmed, so a too-new file is neither damaged nor loadable.
  Same root cause as BF-47-7's wall + BF-47-8's missing stamp → clustered into 0428-345.
- BF-47-10 baseline rows: all re-confirmed as described (migrations pairs, journal resume,
  TargetUID idempotence incl. the fixed alias comment at target_id.go:83-87,
  serviceaccess http_gateway v1→v2 read migration at http_gateway.go:243-268 as the clean
  precedent). No cards; the akte's precedent note helps 0428-341/342.
- BF-47-11 NEW (intake-discovered while probing the BF-47-1 revive path): dangling
  provider-registry bindings for deployments whose lifecycle was interrupted before
  provider release survive Validate and reconcile forever (no GC in the reconcile seam).
  → 0428-350 (low).

## Mapping table (finding -> card)

| Finding | Disposition | Card |
| --- | --- | --- |
| BF-47-1 | LIVE | 0428-341 t-20261125-hunt47-provider-registry-v1-migration |
| BF-47-2 | LIVE | 0428-342 t-20261125-hunt47-deployment-record-v1-wall |
| BF-47-3 | PARTIALLY LIVE (mechanism corrected: earlier fail-closed abort; disclosure text wrong) | 0428-343 t-20261125-hunt47-destroystep-v1-warning-kind |
| BF-47-4 | LIVE + WIDENED (verb never dispatches at all) | 0428-344 t-20261125-hunt47-recover-preflight-and-flag-route |
| BF-47-5 | PARTIALLY SUPERSEDED (hook IS wired; residual = docs accuracy) | 0428-346 t-20261125-hunt47-keycloak-migration-docs |
| BF-47-6 | LIVE (message conflation; parser-disagreement note corrected) | 0428-348 t-20261125-hunt47-core-plan-version-message |
| BF-47-7 | PARTIALLY LIVE (split: asymmetry real, "surprise write" by design) | 0428-349 (parity) + 0428-345 (version wall) |
| BF-47-8 | LIVE | 0428-347 (+ direction text into 0428-345) |
| BF-47-9 | LIVE (clustered with BF-47-7/8 root cause) | 0428-345 |
| BF-47-10 | clean baseline | no card (per akte) |
| BF-47-11 | NEW at intake | 0428-350 |

Clustering rationale: BF-47-7 tail + BF-47-8 first half + BF-47-9 share one root cause
(exact-equality gates without direction/stamp/next-action) → one card 0428-345; the two
distinct migration decisions (registry file v1, deployment record v1) stay separate cards
because their fix shapes diverge (loader migration vs supported removal, different seams).

## Cleanliness

- No docker/podman/compose projects started (coordinator host; no test stacks). `docker ps -a`
  before/after: empty table both times (daemon has no containers) — nothing started or stopped
  by this lane; ambient stacks untouched. This lane's pid recorded in the END transcript.
- Built binaries: /tmp/baha-w193, /tmp/baha-w193-v18 (temp only). Probe state under
  /tmp/opencode/w193-bf47/ only; removed at END. Product worktrees:
  `workers/w193-hunt-v47-intake-wt` (detached at tip, read-only; removed as last action) and
  `workers/w193-hunt-v47-intake-plan` (plan publish; removed after push).
- Product repo: NO commits, NO pushes, NO branch, NO PR (planning-only mission).
  All probes used in-process Go tests/temp dirs or /tmp/opencode state roots only.

## repo-rule compliance

- AGENTS/development-process: planning-only changes, no CI trigger — no product CI run owed
  (§4.6 applies to hosted runs triggered; none were — the mission is a plan-repo publish).
- No .github/** touched anywhere. No workflow_dispatch/rerun. No subagents used.
- Card bodies use plain bullets (no markdown checkboxes outside the single card line);
  `plan.py check` passes (0 errors) before push.
- Commit identity: cards + akte committed with lane identity (author name = lane string),
  verified via `git show -s --format=%an HEAD` before push (gate output below).

## Evidence on origin/main witness

Commit + push from the isolated worktree `workers/w193-hunt-v47-intake-plan`, identity gate:

```
<filled after push>
```

Second-to-last action (exact required commands):

```
<filled after push>
```

END w193-0428-224-hunt-v47-intake — see last line.
