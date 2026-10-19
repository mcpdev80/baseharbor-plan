---
id: t-20261019-ci-evidence-stabilization
type: maintenance
areas: [ci]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Codex (Maintainer CI/evidence stabilization coordinator)"
priority: critical
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261019-ci-evidence-stabilization · Restore exact integration, retained evidence and reviewed-candidate completion #task #release/v0-4-26 #status/active #view/active #area/ci #kind/maintenance
    <!-- generated:card -->
    **Owner:** Codex (Maintainer CI/evidence stabilization coordinator) · **Priority:** critical  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (Maintainer CI/evidence stabilization coordinator)  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Restore the actual PR-head/integration/trusted-plan/executor/evidence/coverage/required-check/merge production path without weakening source or runtime safety.

## Scope

- Coordinate the existing six PRs #998/#995/#993/#990/#989/#985 and accepted #999/#1000 retention fix; do not reimplement the accepted GC correction.
- Own bounded CI/evidence infrastructure corrections, executable Git regression tests, independent source qualification records for already reviewed non-core921 candidates, and current-input integration repairs. This assignment does not take over Codeman product claims.
- Preserve paused worker o1's unpublished core-921 binding and its two local uncommitted files. Do not create a competing CORE_921 implementation. Any other shared planner changes must remain distinct and be documented for later normal integration of o1's preserved work.
- No Codeman workers, unauthorized native tests, force push, generic path exemptions, fake approvals or full release matrix.

## Acceptance

- Demonstrate and repair integration_sha_mismatch on actual immutable event inputs; keep exact parent ordering and merge-tree proof.
- Test stale target, wrong/reversed/extra parents, modified integration tree and clean target integration using real temporary Git repositories.
- Audit GC plus all proof-bearing artifact retentions; protect provenance and compatible evidence reuse.
- Independently reviewed sources are qualified only by exact source commit plus complete changed-status set, compatible clean trusted merges and mandatory real test families.
- At least one previously blocked PR reaches actual green mandatory CI and regular protected Maintainer merge; other PRs finish or retain concrete verified external blockers and owners.
- Final Planning main rendered/checked/tested and published. Codeman remains paused until separately authorized.

## Required checks

Smallest existing Python/contract checks, real Git fixtures, current GitHub required CI; native execution only on verified authorized lanes when indispensable. HF Jobs where available; record unavailable tooling instead of claiming execution.

## Dependencies and file ownership

- Separate infrastructure assignment explicitly authorized by Marcel, 2026-10-19. Existing product claims remain with paused Codeman.
- Core-921 binding owned by existing t-20261019-core921-coverage-binding; preserved, not reassigned.
- Planning validator may emit exact generator output on failure to support normal remote-only render reconciliation; generated files remain produced by scripts/plan.py.

## Handoff

### 2026-10-19 — Initial verified diagnosis and claim

- Remote Planning main at intake eaf0e0490ba2b20bfb06284b47649fc95287f288; develop 6d5a9e1be5c887c28b20c4960acca78586aced7f includes accepted #1000/#999.
- Codeman PAUSED per explicit user instruction. evidence/COORDINATOR-STATUS.md, evidence/board-2026-10-19 and local worker worktrees are not present in published Planning/product trees and no local executor is connected; preserve them and record inability to inspect, never reconstruct or overwrite local ownership evidence.
- Actual #995 run 39180948409 logs BASE=d54ac358, HEAD=d359af83, INTEGRATION=a3848e74. Commit a384 parents are e678cc92,d359af83. Actual #985 run 39180000961 BASE=d54ac358, HEAD=e1c797bb, INTEGRATION=60a7795e; parents f2bad5ef,e1c797bb. Verifier correctly rejects mismatched base, not reversed parents or deleted evidence.
- Both trusted-pr-plan artifacts actually exist, unexpired, expiring 2026-10-21. #985 e1c797bb message describes a merge but its sole parent is 5a381338; copied trusted changes do not establish normal integration ancestry. Source test delta itself is gofmt alignment only.
- ci.yml retains trusted-pr-plan and several exact-candidate/runner/consumer proof artifacts for only 2 days despite 30-day ci-evidence. GC ci.yml-run protection exists; do not repeat its implementation.
- HF identity authenticated but hf_jobs endpoint returns UNAVAILABLE; local execution unavailable. Use real existing GitHub execution when necessary, no invented local/HF successes.
