# 0427-165 r7 — Review correction for PR #1500 orphan refusal integrated onto current develop

## PLAN

- Fetch remote witnesses (ls-remote develop + PR#1500 head, gh pr view 1500)
- Read r6 CODEX-REVIEW verdict; scope the exact 0427-165 delta vs the broader #176 lockfairness base
- Cut fresh worktree/branch from current develop fea92f379 (not the old 0427-165 or r5 base)
- Add 0427-165 orphan-refusal files (deployment_orphan_refusal.go, collectable_orphans_test.go, CollectableOrphans reader, orphan guard)
- Resolve overlap: retain #1507 AcquireTargetWideLifecycleLock in lockExistingTargetDefinitionLifecycle
- Preserve #174 classifyOwnerWarning distinction + orphan-guard fail-closed identity checks; keep file-extraction behavior-only
- Add/retain production-path regression: held local app lock blocks target-wide detach without changing Target config or orphan records
- Local go build + go test for affected packages
- Push branch; reach terminal exact-head PR run green (PR Selected Checks + source format + unit + deployment-package)
- Push evidence to plan origin/main; show origin/main before END; compose down; terminal END

## BASE ATTESTATION

- Base ref I cut from (current develop): `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1500/head`)
- Candidate base: `origin/develop` = `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (the exact develop head, current as of this lane)
- PR #1500 head = `f966505cda93aa35da60ad65afee5e885e4886c9`, state OPEN, mergeCommit null

## Repo-rule compliance

- Product repository read-only except the 0427-165 work carried on the named candidate branch
- No `.github/**` files changed
- Evidence destination: canonical planning repository whose `origin` is `https://github.com/mcpdev80/baseharbor-plan.git`
- No subagents (Owner directive 2026-11-04): every step executed in this session

## r7 correction (halt lifted, owner 2026-11-09)

- Rebased the 0427-165 orphan-refusal correction linearly onto develop `fea92f379` (#1507 landed).
- Branch: `0427-165-target-delete-orphanrec`, single commit `2370ad2984d8cc86e9a235db71952b0b429fa0a2`.
- develop `fea92f379` IS an ancestor; branch contains only my own commit (no foreign commit).
- #1507 `AcquireTargetWideLifecycleLock` retained in `lockExistingTargetDefinitionLifecycle`; orphan-guard fail-closed identity checks + #174 `classifyOwnerWarning` preserved; file-extraction behavior-only.
- Push: `git push origin HEAD:refs/heads/0427-165-target-delete-orphanrec --force-with-lease` -> `+ f966505cd...2370ad298`.
- CI run `42605735063` (status completed/success, headSha 2370ad298, pull_request on PR #1500 branch):
  PR Selected Checks ✓, PR · Source format ✓, PR · Native impact selection ✓, PR · Focused Python ✓,
  PR · Native destroy retry · docker ✓, · podman ✓, PR · Validation · go-unit-tests ✓, go-vet ✓, go-build ✓, cli-gofmt ✓,
  PR · Validation · deployment-package-tests ✓. Skipped (not counted): validate, Release Source Preflight,
  Targeted HA docker/podman, Draft focused checks, Keycloak/Core, Consumer Pins, Runner Interface, Demo Pin,
  Exact Candidate, Public Contracts. No failures.
