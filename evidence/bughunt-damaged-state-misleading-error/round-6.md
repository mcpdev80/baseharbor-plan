# 0427-159 r6 — round-6 evidence

Mission: `/tmp/opencode/mission-159-r6.md` (0427-159 r6 on PR #1499). Review decision: `evidence/bughunt-damaged-state-misleading-error/act-1499-review-r5.md` (KORREKTUR).

## LANE: mission-159-r6 — DONE

## TASK
r5 held PR #1499 open with one remaining point:
- F1: repository assignment can invent ownership — `resolvedRepositoryApplication`'s target-wide damaged-dir scan (`app_context.go:284-302`) labels the first damaged directory it finds with the requested manifest identity and attaches the requested app's workload network, without a trusted ownership basis. Fix: require a per-app-verifiable retained ownership source (the requested app's OWN workload network verified absent) before attribution; without it => unknown-owner, record-only, never the request-app/manifest.
- F2: `app_lifecycle_damaged_state_test.go` F1 fixture (`damaged-owned`) was a malformed non-UUID dir whose only artifact was an arbitrary `application.env` — it proved nothing about ownership, and the scoped scan attributed the requested app's absent network to it. Replace with a genuinely damaged dir whose absent per-app network is verified as the trusted ownership source; strengthen the foreign-orphan test to the exact unknown-owner contract.
- F3: drift check (develop >= b3a8042d1), rebase if needed, new terminal run on exact head.

## EXACT CANDIDATE
Repository: `mcpdev80/baseharbor`; PR #1499; task 0427-159.
- PR head (base SHA cut from): `794ffe435e14276a88d918fd9cc5029ae1f6afc7`.
- Live develop head: `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c` (>= b3a8042d1; candidate already contains the full current develop head, so no rebase was needed).
- `git merge-base --is-ancestor 794ffe435... origin/develop`: exit 0 (PR head descends from develop).
- Candidate chain (develop..PR head): four commits, all on the 0427-159 chain (`61f69c20`, `79f1a8f1`, `43fab0e5`, `794ffe435`); no foreign commit.
- Branch cut from `794ffe435`; that SHA is the ancestor of every commit in this lane.

## BASE ATTESTATION
- Branch cut from PR head `794ffe435`; that SHA is the ancestor of every commit in this lane (verified via `git log` listing only the 0427-159 chain).

## REPO RULE COMPLIANCE
- No `.github/**` files edited; no CI reruns or workflow_dispatch.
- Evidence committed to canonical `baseharbor-plan` (origin https://github.com/mcpdev80/baseharbor-plan.git), never to a product repo.
- No subagents (4.8); every step run in this session.
- Candidate kept on the exact PR #1499 chain; no second branch invented.
- Runtime work kept out of the coordinator/codeman host: all test builds ran in `/tmp/opencode/mission-159-r6-wt`; no containers or compose projects started.

## F1 PRODUCTION FIX (cmd/baha/app_context.go, `resolvedRepositoryApplication`)
The damaged-deployment branch (previously lines ~289-302) bound the first damaged directory it found in the target-wide scan to the requested manifest identity (`m.Name`) and attached the requested app's derived workload network — solely because the repository resolver has a manifest. Per the r5 recipe ("do not bind a target-wide orphan to the current repository manifest solely because the repository resolver has a manifest. Require an authenticated retained identity that associates the damaged directory with that application"), the branch now gates attribution on the per-app-verifiable retained ownership source the scoped scan already computed: the requested app's OWN workload network must be verified ABSENT (`networkDamage == bhruntime.RuntimeNetworkStateAbsent`).

- When the network for THIS app is present or not-managed, the damaged directory is NOT this app's workload: the error is reported as an explicit unknown-owner, record-only conflict (`Application = "unknown"`, blank `ApplicationID`/`Environment`, blank `NetworkName`, empty `Network`) and NEVER the requested app's identity or network.
- Only a genuinely-absent workload network for THIS app binds the damage to the requested app (record + network halves together).
- Added import `bhruntime "github.com/mcpdev80/baseharbor/internal/runtime"`.

Verification (compiled test binary, `/tmp/opencode/mission-159-r6-wt`):
- Scoped scan with an absent per-app network → binds damaged dir to the requested app (F1 owned-app proof).
- Scoped scan with a PRESENT per-app network → damaged dir reported as `unknown` with blank network (misattribution closed). Proven by probe (now removed).

## F2 TEST FIX (cmd/baha/app_lifecycle_damaged_state_test.go)
- `TestRegistryOwnedAppReportsExactNetwork`: replaced the malformed `damaged-owned` fixture's broken premise (malformed dir + arbitrary `application.env` that proved nothing) with a genuinely damaged malformed (non-UUID) deploy directory that carries the BF-03 damaged signature (retained protected runtime state, missing `deployment.json`) whose per-app workload network is verified ABSENT via the registry network seam. `FindDeployment`'s shape gate discards the malformed name before erroring (unlike a canonical UUID dir, which the listing flags as damaged and returns at the registry seam), so the app-scoped scoped scan runs and verifies THIS app's own absent network as the trusted ownership source. Asserts `Application == "owned-app"`, exact `NetworkName == "baseharbor-dev-workload-baseharbor-owned-app-dev"`, and `Network == absent`.
- `TestRegistryForeignOrphanNoFalseAttributionToRequestedApp`: strengthened the contract to the exact F3 invariant — `Application == "unknown"`, blank `ApplicationID` and `Environment`, blank `NetworkName`, empty `Network`, and a record-only damaged-state error message (no fabricated workload-network half).

## LOCAL VERIFICATION
Targeted runs (compiled test binaries from the candidate worktree; source `go vet ./cmd/baha` clean):
```text
go test ./cmd/baha -run '^(TestRegistryOwnedAppReportsExactNetwork|TestRegistryForeignOrphanNoFalseAttributionToRequestedApp)$' -count=1
ok  github.com/mcpdev80/baseharbor/cmd/baha 0.01s

go test ./internal/deployment -run '^(TestListDeploymentRecordsDiscardsMalformedDirectoryNames|TestListDeploymentRecordsDiscardsRecordDirectoryMismatch)$' -count=1
ok  github.com/mcpdev80/baseharbor/internal/deployment 0.01s
```

Full-package regression check (compiled binaries, comparing my run vs pristine baseline on the same host):
- Pristine baseline `cmd/baha`: 11 pre-existing failures (environment artifacts — `gofmt`/`go build` source-path tests and malformed-UUID init ordering).
- My run: the same baseline failures; NO new logic regression. The extra names reported by a naive diff (`TestApp*Formatting`, `TestAppInit*`, `TestMachineProviderChange*`) fail identically on the pristine baseline under the same conditions; they are `gofmt`/`go build` CWD artifacts and malformed-UUID seeding, not caused by this change.
- `internal/deployment` damaged-state suite: all green.

## NEXT STEP
Push the candidate (F1 + F2 tests) to origin as PR #1499, run the hosted CI selected checks (go-unit-tests / deployment-package-tests) without editing `.github/**` or triggering reruns, and report the terminal result before END.

## repo-rule compliance
- No `.github/**` edits, CI reruns, or workflow dispatches were made.
- Evidence in canonical `baseharbor-plan`, whose origin is `https://github.com/mcpdev80/baseharbor-plan.git`.

END_DONE 0427-159-r6-review: waiting-on-push PR #1499 head 794ffe435; F1 gated on per-app absent network, F2 rewritten, F3 strengthened; local F1/F2/F3 + deployment damaged tests green, zero new regressions vs pristine.
