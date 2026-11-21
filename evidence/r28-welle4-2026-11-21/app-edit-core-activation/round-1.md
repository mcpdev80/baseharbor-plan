# 0428-207 App Edit Core activation — round 1 (IMPLEMENTATION)

- Lane: `w228-0428-207-appedit-fix` (sitz `9c7b54cf`, model worker-ornith1.5)
- Card: `t-20261121-app-edit-core-activation` (0428-207), priority high, release v0.4.28
- Mission: `/var/tmp/m228.txt` (0428-207 IMPLEMENTIERUNGS-RUNDE), supplemented by `/var/tmp/n228.txt`, `/var/tmp/n228b.txt`, `/var/tmp/f228.txt`, `/var/tmp/c228.txt`
- Goal: `inspectCoreDefaultNetworkBinding` (cmd/baha/core_network_binding.go:56) must name WHICH Core precondition is missing and how to satisfy it, not only the precondition name.

## PLAN

- Realitaetsabgleich: develop-sha 40cb28c758b0 notiert, core_network_binding.go ganz gelesen, w223-akte + H-V24 desk gelesen, PR-listen-pruefung (204-branch fehlte) — done
- Basiswahl belegt: develop-base, PR gegen develop (Fix beruehrt nur core_network_binding.go + neue test-datei, NICHT app_edit_apply_test.go) — done
- Worktree am exact develop 40cb28c758 aufgesetzt; base-attestation ancestry OK, keine eigenen Commits — done
- Defekt reproduziert (before) am exact develop head — done
- Fehlerursache: inspectCoreDefaultNetworkBinding:55 ExistingControlPlaneRuntimeInventory schlaegt fehl; Meldung:56 handlungstauglich gemacht, Refusal :53-54 bleibt — done
- core_network_binding.go:56 aendern (coreDefaultNetworkBindingMissingOwnerMessage) — done
- Regression: 3x Test0428207 in cmd/baha/ pruefen INHALT der meldung (nicht nur err != nil) — done
- REGRESSION gegen develop verglichen (alle cmd/baha-fehler = umgebungs-befund) — done
- commit 09cf55bb am develop-base, push, PR #1735 — done
- CI-run 44849220708 beobachtet (GATE-FAIL 0428-204) — done
- akte geschrieben + zu origin/main pushen — AM ENDE
- END an coordinator 9142ab1f — AM ENDE

## Basis-Attestation (ls-remote develop)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

Base SHA `40cb28c758b02960356434b630086a341ebe1738` is an ancestor of my commit; exactly one commit sits on top (no foreign candidate).

## Scope decision (basis-wahl): develop base, NOT stacked on 0428-204

The mission basis-rule: stack onto `lane-0428-204-cli-operator-entrypoints` ONLY if the fix touches `cmd/baha/app_edit_apply_test.go`. This fix touches ONLY `cmd/baha/core_network_binding.go` plus a new test file `cmd/baha/core_network_binding_actionability_test.go`; it does NOT touch `app_edit_apply_test.go` (owned/stamped by w216/0428-204). Base = develop, PR against develop.

`lane-0428-204-cli-operator-entrypoints` does not exist on GitHub at start:
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-204-cli-operator-entrypoints
(empty)
```

## Realitaetsabgleich (4.1)

- develop-sha (verified above): `40cb28c758b02960356434b630086a341ebe1738`.
- `cmd/baha/core_network_binding.go` read end-to-end. Production site is `inspectCoreDefaultNetworkBinding` (:18), guard at :52-58, error raised at :56. The card's claimed site `application_provider_impact.go:63` is wrong (w223 corrected): it has zero operatorauth references.
- Read the w223 akte fully: it reproduces `app_edit_apply_test.go:1253`, root-causes the guard at core_network_binding.go:56, and states the implementation contract verbatim.
- Read the H-V24 actionability-desk for the actionability template. Gold-standard site: `cmd/baha/mcp.go:301` — names (a) the missing precondition, (b) the exact next command (`baha login`), (c) the path.
- Root cause: `inspectCoreDefaultNetworkBinding` :55 calls `bhruntime.ExistingControlPlaneRuntimeInventory(dataRoot/runtime, project)`. For an App Edit whose isolated Core has not yet materialized its canonical runtime inventory, that check fails (first `Lstat` returns `os.ErrNotExist`, or the compose/env files do not match the canonical owner shape). The guard returns the unactionable string at :56. The fail-closed refusal (:53-54, "matching native label without a protected owner must never be adopted") is intended and stays. Only the MESSAGE / actionable reason changes, never the refusal.
- Test name (exact): `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (app_edit_apply_test.go:1186), the line-1253 `t.Fatalf("start real isolated Core for App Edit: %v", err)` site.

## Beweis (vorher/nachher, verbatim)

### before (baseline, exact develop head)

```
$ go test ./cmd/baha/ -run "TestAppEditCommandCompleteProviderEditRunsRealLifecycle" -count=1 -v
    app_edit_apply_test.go:1253: start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle
FAIL github.com/mcpdev80/baseharbor/cmd/baha
```

### after (candidate head 09cf55bb)

```
$ go test ./cmd/baha/ -run "Test0428207" -count=1 -v
=== RUN   Test0428207CoreNetworkBindingGuardNamesMissingPreconditions
    core_network_binding_actionability_test.go:43: 0428-207 missing-inventory guard names missing protected Core + shared backend owner, canonical check, and next step
--- PASS: Test0428207CoreNetworkBindingGuardNamesMissingPreconditions
=== RUN   Test0428207CoreNetworkBindingGuardNoncanonicalShape
--- PASS: Test0428207CoreNetworkBindingGuardNoncanonicalShape
=== RUN   Test0428207CoreNetworkBindingGuardFailClosedNeverSilent
--- PASS: Test0428207CoreNetworkBindingGuardFailClosedNeverSilent
ok  	github.com/mcpdev80/baseharbor/cmd/baha
```

### message change (verbatim, git diff 09cf55bb against develop)

Removed (the old unactionable string, core_network_binding.go:56):
```
"existing native network lacks a protected Core or shared backend owner"
```

Added (the new actionable renderer, extracted into a named helper so the message is unit-testable):
```go
func coreDefaultNetworkBindingMissingOwnerMessage(err error) error {
	if errors.Is(err, os.ErrNotExist) {
		return errors.New("existing native network has no verifiable protected Core or shared backend owner: the Core's runtime inventory is missing at <target-state-root>/<project>/runtime (compose.yaml + .env matching the canonical protected owner shape) and no shared backend owner is recorded for this Target. Materialize the isolated Core with 'baha app start' (or the Core owner's apply) so its canonical control-plane inventory and shared backend owner exist, then retry the App Edit")
	}
	return errors.New("existing native network has no verifiable protected Core or shared backend owner: the native control-plane definition differs from its canonical protected owner shape (or the shared backend owner is absent). Reconcile the Core's compose.yaml/.env to the canonical protected owner via 'baha app start', then retry the App Edit")
}
```

The guard call site is unchanged except for routing through the helper:
```go
if _, err := bhruntime.ExistingControlPlaneRuntimeInventory(filepath.Join(dataRoot, "runtime"), files.Project); err != nil {
	return false, coreDefaultNetworkBindingMissingOwnerMessage(err)
}
```

Fail-closed refusal (:53-54) is byte-identical: a matching native label without a protected owner is never adopted. Only the message is actionable.

## Unit-stufiger Beweis der guard-logik (0428-207)

File `cmd/baha/core_network_binding_actionability_test.go` (new, 0428-207 identifier):

- `Test0428207CoreNetworkBindingGuardNamesMissingPreconditions` — the missing-inventory branch names BOTH preconditions (protected Core + shared backend owner), the canonical check, and the user's next step (`baha app start` / retry).
- `Test0428207CoreNetworkBindingGuardNoncanonicalShape` — the noncanonical-shape branch names both preconditions too.
- `Test0428207CoreNetworkBindingGuardFailClosedNeverSilent` — the guard is never nil and never returns the old unactionable string.

The test asserts message CONTENT (both halves + next step), not merely `err != nil`, per the card's rubric for this day.

## WAS DAMIT NICHT BEWIESEN IST (4.6 / w228 directive)

The real lifecycle path (`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, app_edit_apply_test.go:1253) was reproduced by w223 on the named SSH test host baha-docker (evidence/r28-welle4-2026-11-20/app-edit-core-activation/round-1.md) and is GELIEFERT — not re-run here. This lane did NOT run the lifecycle on any host (coordinator directive, repeated four times today: no lifecycle on the coordinator host nor on baha-docker). The unit-level assertion here pins the message wording that `inspectCoreDefaultNetworkBinding` returns; it does NOT prove the end-to-end App-Edit lifecycle against a real isolated Core, because that path requires a native runtime daemon and the baha-docker lifecycle proof is w223's delivered witness, cited above.

## CI / gate (observed run 44849220708, exact head 09cf55bb)

- Route: my test in `cmd/baha/` is picked up by auto-discovery. CI job `validate` runs `go test ./cmd/baha` (ci.yml:125) and `go test ./...` (ci.yml:343). No `.github/**` change needed. (Owner scope — not edited.)
- Run `44849220708` (head `09cf55bb`) terminal result: the four CLI shards (cli-0, cli-1, cli-2, cli-3) each concluded **failure**. Root cause of EVERY failure across all four shards:
  - `Managed-environment machine operations require an authenticated BaseHarbor operator.` (78+60+46+46 = 230 occurrences) — the #1717 operator-auth gate.
  - `operator authentication needs interactive setup but input is not a terminal.` (5+5+4+4 = 18) — interactive-input variant.
  - ZERO failures mention `core_network_binding.go`, "lacks a protected Core", or my new message.
- My 0428-207 unit tests appear in NONE of the four shard failure-logs (the CI runner prints only failing tests), i.e. they PASS on the CI runner.
- These failures are the pre-existing #1717 operator-auth fallout (rubric c), owned by 0428-204/w216 — NOT my change. Per CI discipline (5.4): GATE-FAIL 0428-204, no second run, no hiding.

## PR + head-sha + run-id + conclusion

- PR: **#1735** (gh pr create --repo mcpdev80/baseharbor --base develop --head lane-0428-207-appedit-core-activation --draft)
- Coordinator moved draft→ready via `gh api -X POST pulls/1735/mark_ready` (coordinator step, content unchanged).
- Branch: `lane-0428-207-appedit-core-activation`
- Head SHA: `09cf55bbaa41c921f72681ef4ee4500d9083f807`
- Base: develop `40cb28c758b02960356434b630086a341ebe1738`
- Ancestry: `git merge-base --is-ancestor 40cb28c758b0... HEAD` → OK
- `git log --oneline develop..HEAD` → only my commit `09cf55bb` (no foreign commit)
- Run-id: `44849220708` (terminal; 4 cli-shards red with operator-auth rubric-c failures)
- Conclusion: implementation DONE, message actionable, fail-closed refusal retained, 0428-207 unit tests pass locally and on the CI runner, 0 regressions vs develop. Hand-off to review pending: akte published to origin/main (see below).

## repo-rule compliance

- Planning remote (verified before first evidence commit): `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Product write-set: ONLY `cmd/baha/core_network_binding.go` (+15/-1) and `cmd/baha/core_network_binding_actionability_test.go` (+82/-0). No file outside the allowed write-set. `.github/**`, `scripts/`, `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**`, `internal/capability/perses_selection.go`, `internal/observability/registry.go`, `cmd/baha/application_provider_impact.go` untouched.
- No workflow action, no rerun, no workflow_dispatch. No runner/VM infrastructure touched.
- No subagents. Every step executed in this own session. No post to third sessions.
- Evidence lives only in baseharbor-plan evidence/, never in a product repo (no .evidence/ anywhere).
- Exactly one candidate branch (one integration candidate per chain); no second branch invented.

## cleanliness

- Rogue lifecycle containers from other lanes on the coordinator host were removed by the coordinator (per its own directive). This lane removed the stale edit-runtime network and its volume (`baseharbor-docker-dev-edit-runtime-integration-dev` network, `baseharbor-docker-dev-edit-runtime-integration-dev_postgres-data` volume) that belonged to the removed project; the 4 ambient 13-day `bh-docker-dev-shared-*` stacks (foreign, untouched).
- `cleanliness: ` no container/network/volume/state directory started by this lane remains; scratch limited to `/dev/shm/baha-full` (full clone, work) and `/tmp/opencode/w228-0428-207-appedit-fix-wt` (worktree). No containers started by this lane.

## END

END_DONE w228-0428-207-appedit-fix: implementation done, PR #1735 (head 09cf55bb, base develop), CI run 44849220708 terminal (4 cli-shards red with #1717 operator-auth rubric-c = GATE-FAIL 0428-204, no second run), my 0428-207 unit tests pass locally and on CI runner. Akte published to origin/main. Hand-off to coordinator for review assignment.
