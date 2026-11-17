## PLAN - hopf-3 boundary sync (mission-1577-hopf3)

- Reality-sync: ls-remote + branch, verify rev-parse == remote HEAD 2f4158006 (first action)
- git merge origin/develop (normal merge-commit, no force; conflict = STOP+rezept)
- build + vet + gofmt + affected boundary tests
- refspec-push + ls-remote witness, PR READY, run exact head CI to terminal (self-run duty)
- append rebase-window-1.md (hopf-3), post END, tick GUI todos

## BASE ATTESTATION

- Candidate branch: 0428-092-perses-boundary
- Cut from SHA (base): 2f415800647a8e72423a34edde64514bba870820 (remote branch HEAD at task start; mission stated head == this)
- Remote branch head (ls-remote origin 0428-092-perses-boundary at start): 2f415800647a8e72423a34edde64514bba870820 == mission stated head 2f4158006
- Remote develop at start: bcae1e8c1261c9e44db03fe285a5d090c532dfcd (mission stated 2581000b = STALE, superseded; verified via ls-remote)
- merge-base(0428-092 remote tip, origin/develop at start): 8db0d9bdf (fix BF-05, #1666)
- The remote branch carried prior lane work (Perses 0428-092 + 0428-077 docs + uid-app metrics, commit 2f4158006) above that merge-base.

## EVIDENCE PATH

- Evidence file lives in planning repo ONLY: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/mission-1577-hopf3.md
- Planning repo verified via ls-remote: e6ebc365f1bd97ebccc7cebc1950cd5df17afc1e  HEAD (https://github.com/mcpdev80/baseharbor-plan.git)
- .evidence/ directory NOT used (would leak into product repo)

## REBASE-WINDOW-1 (hopf-3)

- The task's stated base develop SHA (2581000b) was stale at dispatch: remote develop was already bcae1e8c1. Verified via ls-remote before first work.
- The candidate branch HEAD (2f4158006) was NOT a docs-only boundary tip as the mission implied: another lane had accumulated Perses 0428-077 + 0428-092 docs and uid-app metrics work (PR #1579 identity-stability slice) on it. The branch's own tip was already a develop merge (2f4158006).
- ACTION: reset worktree to the true remote HEAD 2f4158006 (not the stale local detached HEAD), then git merge --no-ff origin/develop. No conflict, no force.
- Foreign untracked files from earlier lanes (second_target_conflict_*.go, shared_core_conflict*.go, scripts/ci-native-installation-destroy.sh) blocked the first merge attempt; moved them out of the baseharbor checkout to /var/tmp/hopf3-safekeep before merging. They are NOT part of this candidate.
- Build tree: /var/tmp/hopf3-wt (worktree of 0428-092-perses-boundary). GOFLAGS=-mod=mod, CGO_ENABLED=0, GOCACHE=/var/tmp/hopf3-wt/.gocache, TMPDIR=/var/tmp/hopf3-wt/.gotmp (system /tmp at quota).

## REVENUE / VERDICT

- Candidate merge SHA: 11f640a2bee57895d5f9ef973cc9de9041935ab2
  - first parent = 2f415800647a8e72423a34edde64514bba870820 (remote branch HEAD / base attestation) ✓ is-ancestor
  - second parent = origin/develop (70b7bfc8e at the moment of merge) ✓ is-ancestor
  - commits on HEAD not on develop: only the merge commit 11f640a2b plus the branch's own prior work (2f4158006 and earlier lane commits) — no foreign candidate carried on top.
- Local: go build ./... OK; go vet ./... OK; gofmt -l cmd internal clean.
- Tests: boundary (cmd/baha Boundary) OK; internal/metrics WorkloadOnly/Prometheus OK; 4 uid-app slice tests (TestUIDAppSliceFirstCreateThenCheckoutReuseIdentityNoAuthoredLeak, ...LegacyImportReusesExistingCanonicalIdentity, ...ConcurrentFirstCreateConvergesOnOneOwner, ...NoIDLeakIntoNormalMachineOutput) all PASS.
- Push: refspec-push origin refs/heads/0428-092-perses-boundary:refs/heads/0428-092-perses-boundary OK; 2f4158006..11f640a2b.
- ls-remote witness after push: 11f640a2bee57895d5f9ef973cc9de9041935ab2  refs/heads/0428-092-perses-boundary
- PR #1577 (title: "0428-051 (docs): set optional Perses release boundary — three-state, pin v0.55.1"): state=open, draft=false, base=develop, head=0428-092-perses-boundary, head_sha=11f640a2b.
- CI (self-run, GitHub-hosted runners): check_suite 119176487333 (GitHub Actions) terminal = completed / success. 30 runs: 24 success, 6 skipped, 0 failures. Focused Python, documentation-audit, pages-candidate-build, mkdocs-en/de-strict, Selected Checks all success; Go unit/CI/HA gates skipped (shard selection, docs/metrics change).

## repo-rule compliance

- No .github/** edit, no force-push, no merge of foreign candidate, no subagent. Worktree under /var/tmp, caches under same tree. Evidence only in baseharbor-plan. One integration candidate per chain (0428-092-perses-boundary).

## END

END_DONE mission-1577-hopf3.md: boundary sync PR #1577 ready + CI green on 11f640a2b
