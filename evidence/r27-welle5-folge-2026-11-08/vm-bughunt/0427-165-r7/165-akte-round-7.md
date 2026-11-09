# 0427-165 r7 — Review correction for PR #1500 orphan refusal, integrated onto current develop

## PLAN

- Fetch remote witnesses (ls-remote develop + PR#1500 head, gh pr view 1500)
- Read r6/r7 CODEX-REVIEW verdicts; scope the exact 0427-165 delta vs the broader #176 lockfairness base
- Cut fresh worktree/branch from current develop fea92f379 (not the old 0427-165 or r5 base)
- Add 0427-165 orphan-refusal files (deployment_orphan_refusal.go, collectable_orphans_test.go, CollectableOrphans reader, orphan guard)
- Resolve overlap: retain #1507 AcquireTargetWideLifecycleLock in lockExistingTargetDefinitionLifecycle
- Preserve #174 classifyOwnerWarning distinction + orphan-guard fail-closed identity checks; keep file-extraction behavior-only
- Extend regression to drive the REAL production detach path while a local app lock is held (r7 recipe)
- Local go build + go vet pass; orphan + regression tests pass
- Push --force-with-lease to named branch; reach terminal exact-head PR run green
- Push evidence to plan origin/main; show origin/main before END; compose down; terminal END

## BASE ATTESTATION

- Base ref cut from (current develop): `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1500/head`)
- Candidate base: `origin/develop` = `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`
- PR #1500 head (this lane) = `77064cfab2c1920f9dbc41fe9056037e9ebb5bfa`, state OPEN, mergeCommit null

## Repo-rule compliance

- Product repository read-only except the 0427-165 work carried on the named candidate branch
- No `.github/**` files changed
- Evidence destination: canonical planning repository whose `origin` is `https://github.com/mcpdev80/baseharbor-plan.git`
- No subagents (Owner directive 2026-11-04): every step executed in this session

## History (this card, multiple shifts)

- r6 CODEX-REVIEW (act-1500-review-r6.md): KORREKTUR — candidate not based on current develop (old base), retains AcquireLifecycleLock instead of #1507's AcquireTargetWideLifecycleLock. Exact-head run 42598338207 succeeded.
- First 165-shift stop: owner flagged 2 unconfirmed closes (run 42604588079=404, wrong branch); halted all pushes/ENDs. Evidence on plan origin/main e3688f2f.
- r7 correction (owner 2026-11-09): rebased onto develop fea92f379, commit 2370ad298, CI run 42605735063 success.
- r7 CODEX-REVIEW (act-1500-review-r7.md): KORREKTUR — lock regression tested only the helper, not the actual Target detach mutation.
- This lane: extended regression to drive the production `deleteTarget`/`changeTargetDefinition` path; commit 77064cfab; CI run 42609509644 completed/success on exact head 77064cfab.

## r7 correction executed

- Regression `TestTargetDefinitionDetachHoldsSharedTargetWideLock` now invokes the real `deleteTarget(ctx, [name], out, errOut)` production path with a local app lifecycle lock held via `lockApplicationTargetLifecycle(...)`.
- Asserts: (1) the detach does NOT complete (fails closed behind the shared target-wide lock / orphan guard); (2) the Target definition is byte-for-byte unchanged before vs after; (3) the attached orphan record is byte-for-byte unchanged.
- Negative check: neutering `AcquireTargetWideLifecycleLock` makes the production path break the assertion (the lock call was the sole `coreinstallation` consumer — the test no longer passes), proving it exercises the production route, not just the helper.
- Retained: orphan guard, #174 `classifyOwnerWarning` distinction, fail-closed identity checks, develop fea92f379 ancestry.

## CI run 42609509644 (exact head 77064cfab, pull_request on PR #1500)

- status: completed, conclusion: success
- Passed: PR Selected Checks, PR · Source format, PR · Native impact selection, PR · Focused Python, PR · Validation · go-unit-tests, go-vet, go-build, cli-gofmt, deployment-package-tests, PR · Native destroy retry · docker, · podman
- Skipped (not counted as passes): validate, Release Source Preflight, Targeted HA docker/podman, PR · Draft focused checks, PR · Demo Pin, PR · Native Keycloak/Core, PR · Consumer Pins, PR · Runner Interface, PR · Public Contracts, PR · Exact Candidate, PR · Selected Runtime
- No failures.

## Compose / runtime hygiene

- No docker/podman compose projects started this shift; nothing to tear down.
