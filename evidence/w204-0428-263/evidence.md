# w204-0428-263 · t-20261124-r28-perses-backend-status-real-probe

## END_DONE w204-0428-263

## Card
- id: t-20261124-r28-perses-backend-status-real-probe
- card_number: 0428-263
- title: status probe not the verifier
- type: bug
- owner: w204-0428-263 (claimed via scripts/plan.py claim)
- depends_on: t-20261120-r28-perses-status-never-verified (accepted)

## Visible Ansatz block (pre-commit)
- Frontmatter owner of t-20261124-r28-perses-backend-status-real-probe at runtime (fetched from origin/main): owner unassigned
- git user.name: w204-0428-263
- git user.email: w204-0428-263@baseharbor.local
- literal commit invocation: git -c user.name=w204-0428-263 -c user.email=w204-0428-263@baseharbor.local commit ...
- pre-push identity gate: git show -s --format=%an HEAD -> w204-0428-263 (verified, matches)

## Base attestation
- product remote: origin https://github.com/mcpdev80/baseharbor.git
- cut from SHA (git ls-remote origin/develop): 99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82
- ancestor test: git merge-base --is-ancestor 99d9ddeb... HEAD -> YES
- log line (git log --oneline origin/develop..HEAD): only own commit fdb3bcea4

## Plan repo remote (verified before first evidence commit)
- git -C baseharbor-plan remote -v: origin https://github.com/mcpdev80/baseharbor-plan.git

## Work
- candidate commit: fdb3bcea465e83b4bb97e3933581e5f13e7199f5 (branch lane-0428-263-status-probe)
- PR: #1845 (draft), base main, head fdb3bcea4
- delivery witness (git ls-remote): refs/pull/1845/head = fdb3bcea4, refs/heads/lane-0428-263-status-probe = fdb3bcea4
- diff --name-only (origin/develop..HEAD): cmd/baha/app_status_result.go, internal/metrics/perses_backend_status.go

## What changed
- Card 0428-263: two coexisting "real HTTP probe" definitions for the same perses.status three-state surface. internal/metrics/perses_backend_status.go documented BuildPersesInfraDashboardWithProbe as the per-target instrument while cmd/baha/app_status_result.go named VerifyPersesInfraDashboard as the sole verifier.
- This is a comment/alignment fix only. Both comment sites now name the one documented verifier path: BuildPersesInfraDashboardWithProbe answers every panel's own series query over the materialized Prometheus endpoint and fails closed on any missing datasource/endpoint/authorization — the same VerifyPersesInfraDashboard contract. No behavioral change.
- Boundary respected: internal/capability/perses_selection.go verified-only predicate untouched. No auth/consent behavior change.

## Acceptance
1. One probe definition: both comment sites now name the single build-with-probe path (BuildPersesInfraDashboardWithProbe / VerifyPersesInfraDashboard). No third definition in the codebase.
2. One executable regression in the package owning the status entry point (internal/metrics): scripted probe denied endpoint/config -> configured_unverified, never verified; answering backend -> verified. Existing perses_backend_status_test.go covers these through persesBackendAnswersStatusWithProbe and the production entry PersesBackendAnswersStatusNow.
3. Evidence names the CI job/trigger: PR Go unit `packages` shard (runs go test ./... on all non-CLI packages including internal/metrics).

## Prechecks (local, on candidate fdb3bcea4)
- gofmt -l: clean
- go build ./...: OK
- go vet ./internal/metrics/ ./cmd/baha/: OK
- go test ./internal/metrics/ -run PersesBackendAnswersStatus (named form, skip RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication): 6/6 PASS
- go test ./internal/metrics/ (full, skip RunsRealLifecycle|...): ok 0.975s
- bash scripts/ci-fast-check.sh: OK (Go file size PASS, Function span PASS, Regression ratchet PASS, Workflow policy PASS, 45 + 320 tests OK)

## CI handoff
- PR #1845 is a DRAFT. Moved to review only at handoff.
- Required gate for this card: PR Go unit `packages` shard on exact head fdb3bcea4. Not yet run in Hosted CI — pending Codex review / exact-head Hosted run.
- ci.yml not edited (Owner scope). Work is comment-only in the product write-set; no workflow trigger change needed.

## Cleanup
- baseharbor worktree workers/w204-0428-263-wt (branch lane-0428-263-status-probe) kept for handoff
- plan evidence at /tmp/opencode/w204-plan-wt (isolated, outside plan repo) — moved out of the plan repo on owner housekeeping flag to stop the 1586 globbed-checkbox false errors
- No docker/podman compose projects started; no containers to bring down.
