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

## STOP DIRECTIVE RECEIVED (2nd unconfirmed-close incident, owner 2026-11-09)

- Witness (own `ls-remote`, first line of this file):
  - `refs/pull/1500/head` = `f966505cda93aa35da60ad65afee5e885e4886c9` — UNCHANGED, exactly the head named in the r6 CODEX-REVIEW verdict
  - `refs/heads/develop` = `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06`
- No candidate was pushed to `origin/pr1500`; the PR head remains the verdict's head. The r7 correction stays on the local branch `0427-165-r7-orphan-refusal` (worktree `/tmp/opencode/0427-165-r7-wt`), unpushed.
- Per owner directive: NO further pushes or END posts for 165. The r7 correction will be completed by the coordinator commissioning a fresh lane against the real head. No other lane (incl. 178) touched this shift.
- Corrective actions taken: removed stray `baha` binary from the worktree; branch left uncommitted/unpushed for a later honest lane.

## Compose / runtime hygiene

- No docker/podman compose projects were started this shift; nothing to tear down.
