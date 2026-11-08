# 0427-128 r6 — PR #1452

## Context

CODEX-REVIEW (Rolle: REVIEW) round-5 (PR #1452 head `01f6325d660aa4723a9106d84dbca49faf6e392f`, hosted run `42461735463` terminal success) returned KORREKTUR on two remaining points:

1. The control-plane observation production-path cross-project regression is still absent. The retirement path gained `TestRetireOwnedServicesRejectsForeignPinnedReplica`, but `observeControlPlaneStopRuntime` (seam `cmd/baha/control_plane_stop_observation.go`) gained no regression that calls it with the same pinned native name under a foreign project.
2. Hosted execution of `TestRepositoryComposePinnedWorkloadLifecycleInCI` (`.github/workflows/ci.yml:349`, runtime-integration `-run` selector, `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` gate) is still missing — owner-scope workflow.

Everything else from the r4 stop-points (renderer panic safety, retirement identity, selected-stop postcondition) stays green on the exact head.

## PLAN

- Verify PR #1452 head `01f6325d660aa4723a9106d84dbca49faf6e392f` and develop base `07ae6c3e91b081a189266ca4b162ba705d4aa78f` via `git ls-remote`; confirm develop and r4 head `48814ecc5e8603f16f4849249fffc9b0c8abd7ab` are ancestors of the PR head.
- Cut lane branch `bughunt/0427-128-container-name-replica-r6` from the exact PR #1452 head; record base attestations.
- Locate the seam `observeControlPlaneStopRuntime` and the file that already exercises it; make the provider injectable with an internal helper mirroring the retirement seam.
- Add the focused control-plane cross-project pinned regression: owned planned pinned container + foreign-project row with the exact same native name/service; prove the foreign row is never accepted, selected, or mutated; include a foreign-only inventory and preserve the valid owned case.
- Run `go build`/`go vet`/`go test` locally (cmd/baha + runtime), `gofmt`.
- Drift-merge `develop`, follow-up commit on the PR #1452 branch; run go-unit-tests + affected tests to terminal on the exact head; `git ls-remote` witness.
- Report the ci.yml:349 owner-block for `TestRepositoryComposePinnedWorkloadLifecycleInCI` with the exact diff line and owner-pending note; NO workflow edit, NO green-wash.
- Commit evidence to `origin/main`, verify the evidence path via `git ls-tree` before END; END post to coordinator session.

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1452/head` -> develop `07ae6c3e91b081a189266ca4b162ba705d4aa78f`, PR #1452 `01f6325d660aa4723a9106d84dbca49faf6e392f`.
- `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 01f6325d660aa4723a9106d84dbca49faf6e392f` exits 0 -> develop is an ancestor of the PR head.
- `git merge-base --is-ancestor 48814ecc5e8603f16f4849249fffc9b0c8abd7ab 01f6325d660aa4723a9106d84dbca49faf6e392f` exits 0 -> r4 head is an ancestor of the PR head.
- Lane branch cut from exact PR #1452 head `01f6325d660aa4723a9106d84dbca49faf6e392f`.

## Point 1: control-plane observation cross-project pinned regression — DONE (SHA `213fafa9`)

The seam `observeControlPlaneStopRuntime` (seam `cmd/baha/control_plane_stop_observation.go`) gained an injectable provider via a minimal extraction:

```diff
 func observeControlPlaneStopRuntime(...) error {
 	...
 	provider, err := detectRuntimeForTarget(ctx, target)
 	if err != nil {
 		return nil
 	}
-	resources, err := provider.InspectProjectResources(ctx, p.Project, p.Resources)
-	if err != nil {
-		return runtimeMutationOwnerError()
-	}
+	return observeControlPlaneStopWithProvider(ctx, provider, p)
+}
+
+// observeControlPlaneStopWithProvider exercises the production identity contract
+// against an already-resolved runtime provider. It mirrors the retirement seam's
+// testability: the cross-project pinned native-name contract is verified here so
+// a focused regression can call this seam directly with a pinned provider.
+func observeControlPlaneStopWithProvider(ctx context.Context, provider bhruntime.RuntimeProvider, p *controlPlaneStopPlan) error {
+	p.ObservedProcesses = []coreStopProcessObservation{}
+	p.ObservedResources = []bhruntime.ProjectResource{}
+	p.nativeRevision = "unverified"
+	resources, err := provider.InspectProjectResources(ctx, p.Project, p.Resources)
+	if err != nil {
+		return runtimeMutationOwnerError()
+	}
 	containers, err := provider.ListRuntimeContainers(ctx)
```

New focused regression `cmd/baha/control_plane_stop_observation_foreign_test.go` invokes `observeControlPlaneStopWithProvider` directly with a pinned provider (spiegelbildlich zu `TestRetireOwnedServicesRejectsForeignPinnedReplica`):

- owned planned pinned container (`linkding-web`, project `linkding`, service `web`) — admitted, `RuntimeObserved` true, no canonical-only rejection;
- cross-project: inventory additionally carries a foreign-project row with the exact same native name/service — the foreign row is never accepted, never selected, never included in the observed set; matcher contract `ContainerNameInPlannedSet` still rejects the foreign project row;
- foreign-only inventory: nothing owned is observed (fail-closed), the foreign row does not enter the observed set.

The test was verified as a genuine guard: with the project-scope filter (`if container.Project != p.Project`) disabled it FAILS, with it restored it PASSES. `gofmt` clean.

## Point 2: hosted `TestRepositoryComposePinnedWorkloadLifecycleInCI` at `.github/workflows/ci.yml:349` — OWN-BLOCK (owner-scope, owner-pending, second reviewer pressure)

The test exists and is gated:

- definition: `cmd/baha/app_workload_integration_test.go:338` `func TestRepositoryComposePinnedWorkloadLifecycleInCI`, gate at line 339-340 (`BASEHARBOR_CI_RUNTIME_INTEGRATION != "1"` skip);
- CI selector: `.github/workflows/ci.yml:349` currently lists only `TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI` — `TestRepositoryComposePinnedWorkloadLifecycleInCI` is ABSENT.

Verified present on the exact pushed head `213fafa9` via `gh api .../contents/.github/workflows/ci.yml?ref=213fafa9…`: the pinned-workload test is still not in the selector. On run `42464743849` the native runtime job is `skipped`; the passing Go unit / go-build / go-vet / PR Selected Checks jobs do not prove this native Docker/Podman pinned-lifecycle path.

Exact change required (owner-scope, `.github/**` — NOT edited here):

```diff
-        run: go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI)$' -count=1 -v
+        run: go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposePinnedWorkloadLifecycleInCI|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI)$' -count=1 -v
```

Status: second reviewer / owner pressure; owner-pending. NO workflow edit, NO rerun/dispatch, NO green-wash. This review makes no workflow change.

## Hosted run (observed to terminal by this session, AGENTS 4.6)

- `gh run list --repo mcpdev80/baseharbor --branch bughunt/0427-128-container-name-replica`: run #5175, `42464743849`, headSha `213fafa9cb44644a7c4318bee25d5a7ac182ae66`.
- `gh run view 42464743849 --repo mcpdev80/baseharbor`: `status=completed`, `conclusion=success`.
- Jobs: `go-unit-tests` success, `go-build` success, `go-vet` success, `cli-gofmt` success, `runtime-provider-package-tests` success, `PR Selected Checks` success; `PR · Source format` / `Trusted Plan` / `Workflow policy` success. Native runtime job skipped (owner-block point 2 still open).
- go-unit-tests selects the new `TestObserveControlPlaneStopRejectsForeignPinnedReplica` via normal package discovery.

## Drift-merge develop

`git fetch origin develop` — no new commits since the PR head base. `git log --oneline 01f6325d..origin/develop` empty; develop is fully contained in the PR head. No drift-merge commit needed.

## SHA, scope, and CI witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1452/head` returned `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (develop) and `01f6325d660aa4723a9106d84dbca49faf6e392f` (PR #1452 head, pre-r6).
- Post-r6 head via `git ls-remote`: PR #1452 `213fafa9cb44644a7c4318bee25d5a7ac182ae66`, branch `bughunt/0427-128-container-name-replica` `213fafa9…`.
- `git merge-base --is-ancestor 01f6325d660aa4723a9106d84dbca49faf6e392f 213fafa9cb44644a7c4318bee25d5a7ac182ae66` exits 0; develop is an ancestor of the exact head.
- `git log --oneline 213fafa9..HEAD` lists ONLY my own commit `213fafa9 fix(0427-128 r6): control-plane stop cross-project pinned regression` on top of the PR head; no foreign commit carried.
- Product delta r6: `cmd/baha/control_plane_stop_observation.go` (seam injection only), `cmd/baha/control_plane_stop_observation_foreign_test.go` (new regression). No workflow file changed.

## END

END_DONE 0427-128-r6 — PR #1452 head `213fafa9cb44644a7c4318bee25d5a7ac182ae66`; control-plane cross-project pinned regression `TestObserveControlPlaneStopRejectsForeignPinnedReplica` added + terminal (run `42464743849` success); ci.yml:349 hosted-lifecycle owner-block documented (owner-pending, no workflow edit).
