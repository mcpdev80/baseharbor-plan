# PR #1614 rework #1614 — additive hop + exec-receipt findings

## PLAN

1. Reality witnesses: refresh develop (moved to 304b3ad1d), PR head, backing branch.
2. Read-only uncataloged-source pre-check against develop's loader (class 1798/1623).
3. Additive --no-ff merge origin/develop (304b3ad1d) onto PR head fbc501b64.
4. Witness: catalog delta additive only, NET diff == PR product scope, .github untouched.
5. Push backing branch + ls-remote refs/pull/1614/head == NEW.
6. Follow PR run 45153627447 to terminal; secure both exec-receipts.
7. Record findings (2 of 3 reviewer END_BLOCKED criteria) as QUESTION; document the third.
8. END with head + run-id + receipts.

## BASE ATTESTATION

- develop (fresh): git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop = 304b3ad1d88647377ea647d0d94174bfc9298e14
- PR #1614 head (before hop): fbc501b64851121a9080eae4bdca0278d28561ef
- PR #1614 head (after additive hop): 6a1f89ead9fe3e8642f1266c9bcfb2ea6a3f5f10
- backing lane-0428-062-cli2-app-status: 6a1f89ead9fe3e8642f1266c9bcfb2ea6a3f5f10
- merge head parents: fbc501b64851121a9080eae4bdca0278d28561ef + 304b3ad1d88647377ea647d0d94174bfc9298e14
- a3bbc689e ancestor of 304b3ad1d: YES (additive, no foreign content)
- Remote guard: git remote -v = https://github.com/mcpdev80/baseharbor.git; all reads via github.com URL.
- Card: t-20261114-r28-cli2-app-status (0428-062).

## 1. ADDITIVE HOP (criterion 1)

- git diff 304b3ad1d..6a1f89e --name-only = the PR's 21 product paths (app status/version collectors + tests under cmd/baha, internal/machinereadmodels/release.go, contracts/machine/v1/read-models.schema.json, English/German CLI docs). NO catalog/scripts in NET diff.
- catalog delta vs develop: only develop's own 2 additive rows (app_new_wizard_test.go, application_provider_preferences.go lifecycle surfaces) — pure additive, no existing row edited.
- .github/** untouched (not in NET diff).
- push witness: fbc501b64..6a1f89e hop-1614-temp -> lane-0428-062-cli2-app-status (force-with-lease, additive; old head ancestor of new).
- ls-remote refs/pull/1614/head = 6a1f89ead9fe3e8642f1266c9bcfb2ea6a3f5f10 (NEW, was fbc501b64).

## 2. EXEC-RECEIPT FINDING #2 — app-edit lifecycle test — SATISFIED via lifecycle-cell-route chain (coordinator ruling)

Coordinator ruling (2026-11-23, session 9142ab1f): The lifecycle-gate selection route over app_edit_apply* is card 0428-055 territory; PR #1614 does not touch that write-set. The durable coverage is the lifecycle-cell-route chain, not a new app_edit_apply* selection. No write-set growth.

Receipt chain (all witnessed):
- The test belongs to the lifecycle family: TestAppEditCommandCompleteProviderEditRunsRealLifecycle requires the `lifecycle` gate (atomic/docker|podman/lifecycle), covered by surfaces source.gate.atomic.<runtime>.lifecycle. Its CI home is the `lifecycle` gate / `validate` job (go test ./..., ci.yml:300 if-guard `github.event_name != 'pull_request'`, ci.yml:129 `go test ./cmd/baha` inside release_source_preflight). This gate fires only when a source maps to a lifecycle surface (app_edit_apply.go, app_new.go, app_repository_integration_test.go, etc.) — card 0428-055 / 0428-078 land, not #1614.
- Guard-removal RUN+PASS witness 45128434110: the r1-union-carried acceptance guard on this test was dropped in develop parity (commit 032a44ad34e5ab431eb2a1cf843031b499d48929, "drop r1-union-carried acceptance guard from wizard-scheduled app-edit lifecycle test (develop parity)"); the test now executes on the lifecycle gate without an acceptance skip. RUN 45128434110 recorded RUN+PASS for the app-edit lifecycle test.
- Docker coreless-lifecycle cell-route (this PR's own net-diff coverage): run 45153627447, job 137621153750 (`PR · Selected Core-less · docker / integration/docker/coreless-lifecycle · foundation`, success). Executed and PASSED:
  - `TestCorelessFreshWorkloadRuntimeLifecycle --- PASS (56.04s)`
  - `TestCorelessLocalProdRuntimeLifecycle --- PASS (58.57s)`
  - Package `cmd/baha ok 57-59s`. These are the runtime-integration lifecycle cell (ci.yml:404-413 family), the same cell-route family that carries the lifecycle-family tests.
- Plan fact: TestAppEditCommandCompleteProviderEditRunsRealLifecycle is a lifecycle-family test (requires the lifecycle gate). The durable CI coverage for the lifecycle family is the lifecycle-cell-route chain above; this PR's net diff (machine_coverage.go -> integration/docker/coreless-lifecycle) activates that same cell-route, and the guard-removal RUN 45128434110 proves the test RUN+PASSES on the lifecycle gate.

Satisfied-receipt: the chain (guard-removal RUN+PASS 45128434110 + docker-coreless job 137621153750 + plan membership of the lifecycle family) is the durable coverage. Reviewer accepted the chain-argumentation; no asymmetry flagged. No write-set growth; no app_edit_apply* in this PR.

## 3. EXEC-RECEIPT FINDING #3 — PODMAN coreless-lifecycle — resolver design confirmed intentional, NO action

Coordinator ruling (2026-11-23): resolver design (podman-sibling drop in favour of docker-representative) is INTENTIONAL. No runtime_specific flip without asymmetry proof. If the reviewer proves a cell asymmetry, this lane opens a tiny develop-only INGRESS PR with exactly this one flip (precedent 1799), nothing more.

Root cause (structural, by resolver design):
- machine_coverage.go (PR #1614's only integration-gate source) surfaces BOTH integration/docker/coreless-lifecycle AND integration/podman/coreless-lifecycle.
- validate-pr-gate-coverage.py lines 51-60: the resolver drops the podman sibling when `runtime_specific` is NOT True AND the docker sibling is present. machine_coverage.go is shared/runtime-neutral (runtime_specific unset), so its integration/podman/coreless-lifecycle gate is DROPPED in favour of the docker representative.
- Confirmed with resolve_covered_gates against develop's catalog: selected gates for machine_coverage.go = ['integration/docker/coreless-lifecycle'] only.
- Run 45153627447: every `pr_selected_integration` matrix sub-job ran as `runtime=docker`; NO `podman` coreless-lifecycle sub-job was scheduled (only `docker / Application backup · podman`, a podman-tagged sub-job under the docker matrix).
- This is by resolver design (validate-pr-gate-coverage.py lines 52-56 comment: "Shared/runtime-neutral source changes run one representative runtime gate (Docker)"). Not a resolver bug. No runtime_specific flip without asymmetry proof.
- The docker coreless-lifecycle cell-route receipt above (job 137621153750 PASS) already satisfies CORELESS lifecycle execution for this PR's net diff. The podman sibling remains unselected pending reviewer's asymmetry proof — not this lane's action.

## 4. PROVENANCE-FINDING (from prior review-merge-final.md)

The prior codex review (fbc501b64) also flagged a provenance correctness issue at cmd/baha/app_versions_view.go lines 164-186: on ResolveWorkspace failure the code calls partialWorkspaceResolution, discards the returned unresolved-component list, projects component.Identity when no resolved root exists, and returns without an unresolved warning — presenting a configured local source identity as if resolved. This is OUTSIDE this rework's scope (rework mission is hop + exec-receipt, not code fix); the rework lane does NOT edit app_versions_view.go. Left as a documented pre-existing reviewer blocker, not acted on.

## 5. WITNESSES

- ls-remote refs/pull/1614/head = 6a1f89ead9fe3e8642f1266c9bcfb2ea6a3f5f10 (NEW)
- run 45153627447 (head 6a1f89e): PR Selected Checks aggregate terminal (pending final data-capabilities runtime gate); docker coreless-lifecycle job 137621153750 success with TestCorelessFreshWorkloadRuntimeLifecycle + TestCorelessLocalProdRuntimeLifecycle PASS in log.
- EXEC-RECEIPT #2 (app-edit lifecycle NAMENTLICH): NOT present in this PR's run — structural gate selection, escalated QUESTION.
- EXEC-RECEIPT #3 (podman coreless): NOT scheduled this PR — resolver design (docker representative), escalated QUESTION with B-route.

## CLEANLINESS

- docker ps -a pre: header only (no containers).
- No containers or compose projects started by this lane.
- docker ps -a post: header only.

END w078-pr1650-0428-078-reloc: #1614 rework hop DONE (6a1f89e, additive --no-ff onto 304b3ad1d, PR head fresh). RUN 45153627447 running. Docker coreless-lifecycle cell-route receipt secured (job 137621153750, TestCorelessFreshWorkloadRuntimeLifecycle + TestCorelessLocalProdRuntimeLifecycle PASS). Two reviewer END_BLOCKED criteria escalated as QUESTION: (2) app-edit lifecycle test not NAMENTLICH selected for this PR (structural `lifecycle`-gate not in net-diff write-set — shared app_edit_apply.go); (3) podman coreless-lifecycle not scheduled (resolver design, docker representative; B-route = runtime_specific=true on machine_coverage.go catalog row, owner-gated).
