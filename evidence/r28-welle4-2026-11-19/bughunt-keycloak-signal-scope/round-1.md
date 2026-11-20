# Bug Hunt H-V12 — project-wide signal-id embedding of #1707 vs the perses identity neighbors

- Shift: r28-welle4-2026-11-19
- Lane: x-165
- Card: t-20261120-r28-bughunt-keycloak-signal-scope (0428-165)
- Role: hunt-worker (pure finding, no product change, no branch, no PR, no merge, no container/VM)
- Base measured: `b7cbc00f0adfa36945d6f7af8098d88096276c4f` (origin/develop, HEAD = merge #1707)
- Worktree: /tmp/opencode/baseharbor-x165v (fresh git clone against https://github.com/mcpdev80/baseharbor.git)

## Scope

Hunt H-V12 inspects the project-wide signal-id embedding introduced by #1707
(`b7cbc00f0adf`, `internal/identityprovider/keycloak_realization.go`, 5 lines +
`keycloak_signal_registration_test.go`, 73 lines) against the perses identity
neighbors. It answers: which key is built (K1), what the embedding does not
cover (K2), backward-compat read behavior (K3), and whether the merge's test
covers collision or only differentiation (K4). Pure source + local unit test
inspection. No product change, no branch, no PR, no .github change, no
subagent, no container/VM.

## Base attestation

- Planning repo origin/main: `50f346535239e539bba0ef95ceaa5908286c8bda` (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git main`).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `b7cbc00f0adfa36945d6f7af8098d88096276c4f`.
- `git show b7cbc00f0adf --stat` => 2 files (`keycloak_realization.go` +5/-5, `keycloak_signal_registration_test.go` +73/-10), 1 commit.
- `git merge-base --is-ancestor b7cbc00f0adf origin/develop` => YES. The merge is the develop HEAD.

## PLAN (numbered)

- Measure base: `git ls-remote refs/heads/develop` => `b7cbc00f0adf`; `git log -1 --format=%H` confirmed same SHA. go.mod pins `go 1.25.0` / toolchain go1.26.9; host go 1.26.8.
- K1: `git show b7cbc00f0adf -- internal/identityprovider/keycloak_realization.go` to extract the exact key formula; read `keycloakStateIdentity` + `keycloakFiles.go` + `runtime/project_names.go` to trace `r.files.Project`; probe the `projectToken` normalization (`.`->`-`) with a throwaway `internal/runtime/*_test.go` and remove it after.
- K2: grep every `RegisterProviderSignals` / `ID:` builder in `internal/identityprovider`, `internal/capability`, `internal/application`, `internal/traces`, `internal/telemetry`, `internal/logs`, `cmd/baha`.
- K3: read `observability/registry.go` `List` (read path) and `RegisterProviderSignals` (write path) and `Remove`/`PruneOwnedProviderInstances` to determine ID-based lookup semantics; compare old `"keycloak-metrics"` vs new `"keycloak:<project>"`.
- K4: read `keycloak_signal_registration_test.go` at `b7cbc00f0adf`, especially `TestKeycloakSignalRegistrationKeepsProjectsDistinct`, to determine whether it tests same-base-name collision or only distinct-name differentiation.
- Run `go test` for `internal/identityprovider`, `internal/observability`, `internal/runtime`, `internal/telemetry`, `internal/traces`, `internal/logs` plus `go vet` and `go build ./...`; record results; remove the throwaway probe.
- Card: written here as this Akte; owner casts a bug card from the FUND lines.

## Findings

### FUND 1 (K1) — The key is `"keycloak:" + r.files.Project` with a fixed `-` separator; `projectToken` collapses `.` to `-`, so `my.identity` and `my-identity` collide in the perses signal registry.

KEYWORD (vertrag): each Keycloak project must own a unique perses signal ID.
ERWARTET (vertrag): distinct applications map to distinct `"keycloak:"` IDs.

IST (gemessen):
- The merge builds the key as a plain string concat with the literal prefix `"keycloak:"` and NO other separator: `internal/identityprovider/keycloak_realization.go:134` (H-V12 line context) / merge diff: `registrationID := "keycloak:" + r.files.Project`.
- `r.files.Project` for `ScopeApplication` is `bhruntime.ApplicationProjectName(namespace, app.Name+"-identity", app.Environment)` (`internal/identityprovider/keycloak_files.go:156`, derived at `:141`), which formats as `bh-<target>-<app>-identity-<env>` (`internal/runtime/project_names.go:31-38`).
- `projectToken` normalizes lowercase, trims surrounding `-`, replaces every `.` with `-`, and falls back to a token (`internal/runtime/project_names.go:41-49`).
- Consequence: `ApplicationProjectName("cluster","my.identity","prod")` AND `ApplicationProjectName("cluster","my-identity","prod")` both produce the compose project `bh-cluster-my-identity-prod`, and therefore the SAME perses signal ID `keycloak:bh-cluster-my-identity-prod`. Verified with a throwaway `internal/runtime/x165_probe_test.go` (removed afterward): `dot-name project : "bh-cluster-my-identity-prod"`, `dash-name project : "bh-cluster-my-identity-prod"`, `>>> COLLISION`.
- The collision is INHERENT to the existing project-name normalization, not to the new prefix: the prefix `"keycloak:"` is constant and the value is exactly the (already-collapsed) compose project name. Two application names that normalize to the same compose project produce the same ID — same base-name under two spellings — so a second registration overwrites the first in the registry (`registry.go:246-251` removes the prior source with the same `ID`+`Provider` before appending the new one).
- Case-sensitivity: `projectToken` lowercases, so the ID is already case-folded; "can two different-case names collide?" reduces to the same `.`-vs-`-` collapse question and is likewise unguarded.

DATEI:ZEILE: `internal/identityprovider/keycloak_realization.go:134` (`registrationID`), `internal/identityprovider/keycloak_files.go:156,141` (`Project`), `internal/runtime/project_names.go:41-49` (`projectToken`, the `.`->`-` replacement at :43), `:31-38` (`ApplicationProjectName`), `internal/observability/registry.go:246-251` (dedupe-by-ID write that overwrites the prior source).

WIRKUNG auf user-sicht: an application whose name normalizes against another already-registered application loses its own perses metrics source (overwritten); the second registration's ID shadows the first. Non-blocking for the common single-app case, but a real correctness gap for the `.`/`-` normalization boundary.

STUFE: nicht-block.

VERHALTEN — the ID formula itself is correct for distinct normalize-classes; the gap is the unguarded normalization boundary. VERHALTEN KORREKT for distinct projects; the `.`-vs-`-` collapse is a BEFUND (abdeckung fehlt). witness: `TestKeycloakSignalRegistrationKeepsProjectsDistinct` (below) only exercises distinct names and does not cover this boundary.

Reproduce: `go test ./internal/runtime -count=1 -run "TestX165SignalIDCollisionProbe"` (probe, now removed) showed the identical projected project and identical key for `my.identity` vs `my-identity`.

### FUND 2 (K2) — Four providers build their perses identity with the SAME `"provider:"+project` rule; only Keycloak and Tempo get a per-`app.Name` `OwnerApplication`, and Loki/OTel share `ScopeShared` with a single per-target project. No un-prefixed duplicate ID exists.

KEYWORD: the embedding is not the sole place; the rule is uniform.

IST (gemessen) — every `RegisterProviderSignals` ID builder in scope:
- Keycloak: `internal/identityprovider/keycloak_realization.go:164` (merge) `ID: registrationID == "keycloak:" + r.files.Project`; `OwnerApplication: r.app.Name` (`:168`).
- Tempo: `internal/traces/tempo.go:404` `ID: "tempo:" + p.Project` with `p.Project` = `ApplicationProjectName(namespace, m.Name, m.Environment)` (`internal/traces/tempo.go:172`) for `ScopeApplication` / `SharedProjectName(namespace)` for `ScopeShared`; `OwnerApplication: p.OwnerApplication`.
- Loki (logs): `internal/logs/realization.go:233` `ID: "loki:" + placement.Project`.
- OpenTelemetry collector: `internal/telemetry/realization.go:197` `ID: instance.ObservationID == "opentelemetry-collector:" + files.Project` with `files.Project = SharedProjectName(namespace)` (`internal/telemetry/otlp.go:408`); `Scope: capability.ScopeShared`.
- The read path `internal/observability/registry.go:383-442` (`List`) filters by `source.ID` EXACTLY within scope/class filters (no normalization, no prefix-stripping); the write path dedupes by `(ID, Provider)` (`:246-251`). So there is no place that would read back a `"keycloak-metrics"` legacy ID as the new project-scoped ID.
- The only identifier that is NOT project-scoped is the signal NAME declaration `"keycloak-metrics"` in `internal/capability/reference.go:160` — that is the `Descriptor`/signal name (validated against registered signals), not the `ID`. It is correctly constant per descriptor and does not collide across projects.

CONCLUSION (K2): no second place builds the SAME id WITHOUT the project prefix. The four providers are internally consistent; the gap is the normalization collapse in FUND 1, not a missing prefix.

DATEI:ZEILE: `internal/identityprovider/keycloak_realization.go:164`, `internal/traces/tempo.go:404,172`, `internal/logs/realization.go:233`, `internal/telemetry/realization.go:197`, `internal/telemetry/otlp.go:408`, `internal/observability/registry.go:383-442`, `internal/observability/registry.go:246-251`, `internal/capability/reference.go:160`.

STUFE: nicht-block (observation).

### FUND 3 (K3) — Backward-compat: a pre-existing un-prefixed `"keycloak-metrics"` registration is read back as a DIFFERENT id and disappears from perses after #1707.

KEYWORD: existing registrations without project prefix.

ERWARTET (vertrag): existing perses registrations for the provider should remain observable after a deploy that changes the ID rule.

IST (gemessen):
- Before #1707 the Keycloak ID was the literal `"keycloak-metrics"` (merge diff `- ID: "keycloak-metrics"`).
- After #1707 the ID is `"keycloak:" + r.files.Project == "keycloak:bh-<target>-<app>-identity-<env>"` (for `ScopeApplication`).
- `List` (`registry.go:383`) returns sources whose `source.ID` matches the exact registered ID; `Remove` (`:367`) deletes by exact ID. `"keycloak-metrics"` never equals `"keycloak:bh-...-identity-..."`, so an un-prefixed registration left in `observability/signals.json` is neither matched by a post-#1707 read nor removed by the Keycloak destroy path.
- There is NO migration/remediation of the observability signal registry in the merge (`git show b7cbc00f0adf --stat` = only 2 files; no `Remove("keycloak-metrics")`, no `PruneOwnedProviderInstances` call in `keycloak_realization.go`, no id-rewrite in `Destroy`/`Stop`). The OTel destroy does call `observability.Remove("opentelemetry-collector:" + files.Project)` (`internal/telemetry/otlp.go:525`) but there is no analogous keyed cleanup for Keycloak's old ID.

CONCLUSION (K3): this is a read-path break, not a crash. On the next deploy that switches a running install from the old ID to the new project-scoped ID, the old `keycloak-metrics` source lingers in the registry (a "leiche") and the new source coexists under the new ID; the alert-verifier (arte 0428-152) reads by exact ID, so a consumer still keyed on `"keycloak-metrics"` will see it vanish, while a consumer keyed on the new ID sees only the new source. No data loss (the metrics stream is provider-side), but the perses view can show a stale/missing Keycloak metrics source across the cutover.

DATEI:ZEILE: `internal/observability/registry.go:383-442` (`List` exact-ID match), `:367` (`Remove`), `internal/identityprovider/keycloak_realization.go` (merge, new ID), `internal/telemetry/otlp.go:525` (the ONLY keyed Remove witness, for OTel — no Keycloak equivalent).

WIRKUNG auf user-sicht: perses metrics view for Keycloak can show a missing/legacy source across the ID cutover; the alert-verifier keyed on the old ID stops seeing it. STUFE: nicht-block (cutover observation); depends on whether any live install still carries the old ID.

### FUND 4 (K4) — `keycloak_signal_registration_test.go` tests DIFFERENTIATION, not COLLISION. The `.`/`-` normalization collision in FUND 1 is UNCOVERED.

KEYWORD: the merge's test.

IST (gemessen): `TestKeycloakSignalRegistrationKeepsProjectsDistinct` (`internal/identityprovider/keycloak_signal_registration_test.go:120`) registers TWO apps with TWO DIFFERENT project names (`"identity-alpha"`, `"identity-beta"`, `:126`) and asserts the two resulting IDs `keycloakMetricsSignalID("identity-alpha")` and `keycloakMetricsSignalID("identity-beta")` are distinct and each still found after both registrations. It never registers two apps whose names normalize to the SAME project (e.g. `"my.identity"` vs `"my-identity"`), so it proves "two projects, different names stay apart" (differentiation) but not "two projects, same base-name under two spellings do not collide" (collision).

CONCLUSION (K4): the test proves the ID rule distinguishes distinct projects but does NOT prove the rule carries — the exact gap in FUND 1. This is the classic "VERHALTEN KORREKT vs BEFUND: abdeckung fehlt" distinction the mission names. A regression test with a colliding pair (`"my.identity"` vs `"my-identity"` -> same `ApplicationProjectName`) would fail today and is the witness the merge lacks.

DATEI:ZEILE: `internal/identityprovider/keycloak_signal_registration_test.go:120-171` (`TestKeycloakSignalRegistrationKeepsProjectsDistinct`, distinct projects at :126), `internal/runtime/project_names.go:41-49` (the normalization the test does not exercise).

WIRKUNG: the uncovered boundary is exactly the collision class in FUND 1; the existing test would not catch a regression that reintroduces it.

STUFE: nicht-block (coverage gap); directly supports FUND 1.

## Test coverage (mission step 6)

Command 1: `go test ./internal/identityprovider/... -count=1`
Result: `ok github.com/mcpdev80/baseharbor/internal/identityprovider 9.017s` — EXIT 0.

Command 2: `go test ./internal/observability/... ./internal/runtime/... ./internal/telemetry/... ./internal/traces/... ./internal/logs/... -count=1`
Result: all `ok` (identityprovider, observability, runtime + runtime/contract, runtime/model, runtime/remoteprojection, runtime/resolver, runtime/terminal, telemetry, traces, logs) — EXIT 0.

Command 3 (collision probe, throwaway test file created then removed): `go test ./internal/runtime -count=1 -run "TestX165SignalIDCollisionProbe"` — PASS, and printed the identical projected project and identical key for `my.identity` vs `my-identity`, i.e. the collision. Test file removed; repo clean afterward.

`go vet ./internal/identityprovider/ ./internal/observability/ ./internal/runtime/` — VET_EXIT 0.
`go build ./...` — BUILD OK.

No PANIC, no dead-lock, no container/VM started.

## Conclusion

H-V12 found the signal-id embedding is correct for distinct projects and
uniform across the four perses providers (Keycloak/Tempo/Loki/OTel-collector),
but uncovered two real correctness gaps at the normalization boundary:

1. FUND 1 (K1) — the key `"keycloak:" + r.files.Project` shares the
   `projectToken` `.`->`-` collapse, so `my.identity` and `my-identity`
   produce the SAME perses signal ID; a second registration overwrites the
   first (`registry.go:246-251`). DATEI:ZEILE:
   `internal/identityprovider/keycloak_realization.go:134` + `internal/runtime/project_names.go:43`.
2. FUND 3 (K3) — a pre-existing un-prefixed `"keycloak-metrics"` registration
   is read back as a DIFFERENT id after #1707 and vanishes from the exact-ID
   perses read without any registry migration/remediation. DATEI:ZEILE:
   `internal/observability/registry.go:383-442`.
3. FUND 4 (K4) — the merge's test covers differentiation, not collision; the
   FUND 1 boundary is UNCOVERED. DATEI:ZEILE:
   `internal/identityprovider/keycloak_signal_registration_test.go:120`.

No product change made; no PR, branch, merge, .github edit, subagent, container
or VM.

## KARTE: offen (an coordinator) — three findings to cast

- FUND 1: `internal/identityprovider/keycloak_realization.go:134` + `internal/runtime/project_names.go:43` — Keycloak signal-id normalization collision (`.`/`-`).
- FUND 3: `internal/observability/registry.go:383-442` — missing registry migration for legacy un-prefixed Keycloak ID.
- FUND 4: `internal/identityprovider/keycloak_signal_registration_test.go:120` — test covers differentiation, not the collision in FUND 1.

## Cleanliness

- Worktree: /tmp/opencode/baseharbor-x165v (git status clean, 0 modified/untracked; throwaway `internal/runtime/x165_probe_test.go` removed).
- Containers: none started.
- Networks: none created.
- Volumes: none created.
- State directories: none created (unit tests use temp dirs under /tmp via t.TempDir(), auto-removed).
- Before/after list: empty on both sides (pure source/unit-test lane).

## Base attestation

- Base SHA cut from: `b7cbc00f0adfa36945d6f7af8098d88096276c4f` (origin/develop, HEAD = #1707 merge).
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git main` => `50f346535239e539bba0ef95ceaa5908286c8bda`.
- This lane wrote only into baseharbor-plan evidence (this file). No commit, branch, or PR on baseharbor.
