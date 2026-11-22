# Gate-admission census — round-1 (H-V32)

Lane: `w21-pr1702-0428-142-compat`
Slice: H-V32 `gate-admission-census` (coordinator BUG-HUNT.md, mission sha256 f9c8f075a4d2)
Scope: pure findings over the path->gate mapping for `cmd/baha/ci_integration_*.go` and sibling boundary files in `scripts/pr-gate-plan.py` AND `scripts/pre-release-runtime-impact.json`. develop anchor `6209874428f08dc3e90d6e29a42b30683ce9932a`.
Product boundary: NO product change, NO push to any product branch, NO GitHub comment, NO local test, NO subagent.

## PLAN
- Bullet 1: enumerate every `cmd/baha/ci_integration_*.go` on develop plus sibling boundary/datei.
- Bullet 2: for each, check presence in `scripts/pr-gate-plan.py` (which gate, which line) AND `scripts/pre-release-runtime-impact.json` (which entry, which line).
- Bullet 3: output the list of files that SHOULD map to a required gate but are MISSING from the mapping — per line: file, expected gate, 'feHLT in pr-gate-plan.py' / 'fehlt in pre-release-runtime-impact.json', and the file:line where the line should exist.
- Bullet 4: akte to evidence/r28-welle5-2026-11-22/gate-admission-census/round-1.md, push origin/main, cleanliness line.
- Bullet 5: findings only, no cards from this lane (fund->karte ownership stays with coordinator).

## Method
- `git ls-tree -r --name-only 6209874428f08dc3e90d6e29a42b30683ce9932a cmd/baha | grep ci_integration` => three files.
- `git show <develop>:scripts/pr-gate-plan.py` and `git show <develop>:scripts/pre-release-runtime-impact.json` read read-only; `grep` for each path.
- Traced the resolver branch (`targeted_plan`, pr-gate-plan.py) that classifies an unmapped `cmd/baha/*.go` path.

## Files census (develop 6209874428f)
`cmd/baha/ci_integration_operator_enabled.go`
`cmd/baha/ci_integration_operator_disabled.go`
`cmd/baha/ci_integration_operator_enabled_test.go`
All three: build tag `//go:build baseharbor_ci_operator_testonly`; operator-injection seams (`withCIIntegrationOperator` / `ciIntegrationOperator*`) that supply the synthetic verified CI operator used by the disposable demo atomic gates (DEMO_ATOMIC_GATE). They live in cmd/baha, not in internal/operatorauth.

### Presence check
| File | In pr-gate-plan.py explicit sets | In pre-release-runtime-impact.json core mapping |
| --- | --- | --- |
| cmd/baha/ci_integration_operator_enabled.go | ABSENT (grep count 0) | ABSENT (grep count 0) |
| cmd/baha/ci_integration_operator_disabled.go | ABSENT | ABSENT |
| cmd/baha/ci_integration_operator_enabled_test.go | ABSENT | ABSENT |

### Where the mapping SHOULD exist (file:line to add)
- `scripts/pr-gate-plan.py`: no line references any of the three paths. The explicit-file sets that DO name `cmd/baha/*.go` (WIZARD_COMPONENTS at lines ~150-179, EDIT_SQL_PREVIEW at ~261-333) never list them. There is no `cmd/baha/ci_integration_*` entry anywhere.
- `scripts/pre-release-runtime-impact.json`: the `core` map (lines ~16-57) names lifecycle/guided/data-capabilities-impacting `cmd/baha/*.go` files (e.g. `app_core_requirement.go`, `app_coreless_runtime_test.go`) but never any `ci_integration_*`. No entry exists for any of the three.

### Fallback classification (what the resolver actually does for these paths)
For an unmapped `cmd/baha/*.go` (non-test, non-`_engine.go`), `targeted_plan` reaches `pr-gate-plan.py:1344` `elif path.startswith('cmd/baha/') and path.endswith('.go')` => `area = 'cli-unresolved-runtime-impact'`, requires `CODE_CHECKS` + `CLI_CHECKS`, and appends `CLI runtime impact needs qualified targeted native coverage: <path>`. Net: `broad_required = true` (fail-closed) and NO `atomic/*` native gate selected. So the three seam files are NOT silently skipped by the planner — they force the broad conservative path. That is a real finding only if a required atomic gate should fire for them and currently cannot.

## Findings

### F1 (blocker-class, the known reference case) — `cmd/baha/ci_integration_operator_enabled.go` has NO atomic-gate admission
- File: `cmd/baha/ci_integration_operator_enabled.go`
- Expected gate: an `atomic/docker/*` / `atomic/podman/*` demo gate (the seam feeds `DEMO_ATOMIC_GATE` acceptance — the in-process operator grant for enrolled remote Core Targets).
- 'feHLT in pr-gate-plan.py': no line anywhere references the path (explicit sets at ~150-179, ~261-333 never list it).
- 'fehlt in pre-release-runtime-impact.json': not in the `core` map (lines ~16-57).
- Consequence: a change to this seam (or the sibling seam files) triggers only the broad `cli-unresolved-runtime-impact` conservative path (pr-gate-plan.py:1344) — no `atomic/*` native gate is selected for it. If a required atomic gate belongs here, it is silently unmapped.
- Benchmark corroboration: same unmapped behavior caused `atomic/docker/data-capabilities` to SKIP in PR-run 44966211481 while the run stayed green (the reference case the hunt was calibrated on).

### F2 (same class) — `cmd/baha/ci_integration_operator_disabled.go` has NO atomic-gate admission
- File: `cmd/baha/ci_integration_operator_disabled.go`
- Expected gate: an `atomic/docker/*` / `atomic/podman/*` demo gate.
- 'feHLT in pr-gate-plan.py': no reference (explicit sets ~150-179, ~261-333).
- 'fehlt in pre-release-runtime-impact.json': not in `core` (~16-57).
- Consequence: broad `cli-unresolved-runtime-impact` fallback (pr-gate-plan.py:1344); no atomic gate selected.

### F3 (same class) — `cmd/baha/ci_integration_operator_enabled_test.go` has NO atomic-gate admission
- File: `cmd/baha/ci_integration_operator_enabled_test.go`
- Expected gate: an `atomic/docker/*` / `atomic/podman/*` demo gate (test seam for the above).
- 'feHLT in pr-gate-plan.py': no reference; falls to `cli-unresolved-runtime-impact` (pr-gate-plan.py:1344), not the `_test.go` package path (1336) which needs a `cmd/baha/` explicit set the file is absent from.
- 'fehlt in pre-release-runtime-impact.json': not in `core`.
- Consequence: broad conservative path; no atomic gate selected for the test seam.

### F4 (observation, not a defect) — broad fallback keeps these fail-closed
- The planner does not silently drop these files: an unmapped `cmd/baha/*.go` forces `broad_required = true` and the conservative `CODE_CHECKS` + `CLI_CHECKS` run (pr-gate-plan.py:1344-1347). So F1-F3 are admission gaps for a POSSIBLY-required `atomic/*` native gate, not a silent CI skip. The risk is that a required native gate is never SELECTED for the seam even though the broad path runs — the mapping should name the seam and attach the intended atomic gate explicitly rather than relying on the conservative fallback.

## Not decided (explicitly, no verdict)
- Whether each of F1-F3 should bind to a specific existing `atomic/*` gate (the correct gate is an owner decision; this lane only reports).
- Whether the `baseharbor_ci_operator_testonly` build tag means these files are already intentionally outside the declarative mapping (then F1-F3 are expected and the broad fallback is correct) — an owner/authoritative-source question.

## Boundaries
- Read-only: `git ls-tree`, `git show`, `grep`, `awk`, `python3` against fetched develop refs only. No `git apply` to a product branch, no commit, no push on any product ref, no GitHub comment, no merge/close.
- No local `go test`/`go vet`/compile (owner sha256 d65b09b8ffed). No `.github/**`/`scripts/**` change. No subagents (AGENTS 4.8).
- Findings only; card gossing stays with the coordinator (fund->karte-pflicht).

## END
END_DONE w21-pr1702-0428-142-compat: H-V32 gate-admission-census round-1 done (findings only). `dateien ohne zulassung: 3` — cmd/baha/ci_integration_operator_enabled.go, ci_integration_operator_disabled.go, ci_integration_operator_enabled_test.go (build tag baseharbor_ci_operator_testonly) absent from both scripts/pr-gate-plan.py explicit sets AND scripts/pre-release-runtime-impact.json core map; fall through to cli-unresolved-runtime-impact (pr-gate-plan.py:1344) requiring CODE+CLI checks but no atomic/* native gate + flagged unresolved. F1-F3 admission gap; F4 note: broad fallback keeps fail-closed so no silent CI skip. Evidence: evidence/r28-welle5-2026-11-22/gate-admission-census/round-1.md (origin/main). cleanliness: container/netzwerke/volumes unveraendert, nichts hinterlassen (read-only read of fetched develop refs; no container/compose project started by this sitz). Waiting on owner push to cli2-env-delete for 0428-226 (round-2) — run-ids of the two coreless-lifecycle jobs to terminal pending. Lane head 7d4351c6d645353b6b96c8d320b4c832d55f9047 (base develop 6209874428f08dc3e90d6e29a42b30683ce9932a, no foreign commits).
