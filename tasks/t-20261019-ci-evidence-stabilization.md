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
prs: ["mcpdev80/baseharbor#1001", "mcpdev80/baseharbor#1002", "mcpdev80/baseharbor#1003"]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1001", "https://github.com/mcpdev80/baseharbor/pull/1002", "https://github.com/mcpdev80/baseharbor/pull/1003", "https://github.com/mcpdev80/baseharbor/actions/runs/39185230474", "https://github.com/mcpdev80/baseharbor/actions/runs/39185400529", "https://github.com/mcpdev80/baseharbor/actions/runs/39185646028"]
---

- [x] t-20261019-ci-evidence-stabilization · Restore exact integration, retained evidence and reviewed-candidate completion #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/ci #kind/maintenance
    <!-- generated:card -->
    **Owner:** Codex (Maintainer CI/evidence stabilization coordinator) · **Priority:** critical  
    **PR:** [baseharbor#1001](https://github.com/mcpdev80/baseharbor/pull/1001), [baseharbor#1002](https://github.com/mcpdev80/baseharbor/pull/1002), [baseharbor#1003](https://github.com/mcpdev80/baseharbor/pull/1003)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1001), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1002), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1003), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/39185230474), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/39185400529), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/39185646028)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (Maintainer CI/evidence stabilization coordinator)  
**Priority:** critical  
**PRs:** [baseharbor#1001](https://github.com/mcpdev80/baseharbor/pull/1001), [baseharbor#1002](https://github.com/mcpdev80/baseharbor/pull/1002), [baseharbor#1003](https://github.com/mcpdev80/baseharbor/pull/1003)  
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

### 2026-10-19 — Production integration repaired; independent infrastructure review

- #995 now 2ff6846c3b4d246d1291ae2c90d09d231c4214bc: genuine two-parent develop integration, original four source blobs unchanged. Run 39183081916 accepts integration; focused build/vet/guided/source gates pass. Four source paths remain unresolved: no full native recovery/re-review evidence has been fabricated. Paused product owner remains responsible for missing native success and source issues.
- #985 now e2cfc95ff400b56a980c7d95903bcd393cc9a375: genuine two-parent integration, original exact test blob retained. Run 39183103814 executes both required MCP families successfully plus build/vet/gofmt; final blocks only source qualification. Independent source review 5565951329 anchors e1c797bb.
- Infrastructure #1001 initially 1baa4beaa7fb0a8497be2e423a7feb311ffebf85: real stale-base/reversed-parent/extra-parent Git regressions; finite reviewed source/status records for #993/#989/#985; actual five/eight utility tests are required when those candidates are integrated. CI 39183452084 entirely green. Separate read-only Codex reviewer positive; no Codeman worker or claim takeover. Utility suites absent on this infrastructure branch were honestly skipped, not claimed executed there.
- Additional retention audit #1002 exactly 2e3325e142995aedd3d69a2e5569452127cbc58f: four PR proof uploads 2→30 days; direct Docker/Podman evidence 1→30 days; preserve the two actual native-evidence origin workflows in existing GC. Existing #999/#1000 behavior unchanged. Actual read-only GC run 39183759516 executed all seven tests PASS; mutating jobs skipped. Separate independent review positive.
- Final #1001 candidate 667e3806ee03140435825c69bc1b7c45f431ffc9 additionally binds exact #1002 five-file status inventory and requires all seven GC regression methods in mandatory planner tests. New exact review/CI in progress; not merged or self-approved.
- #998 remains blocked on unpublished paused o1 work and regular claim release/resumption; no competing binding created. #990 full-recovery acceptance remains dependent on actual #995 native success, not its narrower fixture checks.

### 2026-10-19 — Real production-path results and fresh review anchors

- #1001 merged 5c5f8a18583d1ade0c71f152bbd56fd2861b28b0 after independent review5565992741 and fully green CI39184026379. #1002 merged57216ba951933dbbc562f0445662b4cf7494584a after independent review5565993909 and green CI39184233759; required planner job117843190047 actually ran all seven GC tests PASS. PyYAML available in actual required execution, no skip exception.
- Actual #985 CI39184450141 proves both MCP families/build/vet/gofmt, but correctly rejects inherited qualification over older explicit tree-resolution history. New independent exact source review5566030344 approves3dfac93c against57216ba9 (single added117-line file, original blob unchanged). #993 freshreview5566047336 approves e6616b45 (two unchanged blobs), actual five sandbox/sevenGC PASS39184711511. #989 freshreview5566047870 approves c3809b12 (same helper/tests, workflow only inherited accepted retention30d); original Qwen native evidence remains78a72eba only.
- Separate #1003 d2e81b4f1c183622b21139931291e0f72f85d0e3 re-anchors only these independently reviewed resolved candidates. New real Git fixture proves copied target contents do not establish history; explicit resolution needs fresh exact review, and later genuine clean trusted merges remain acceptable. No Git verification weakening. CI/review in progress.
- Complete current #995 independent review found concrete diagnostic identity disclosure; review5566018799 CHANGES REQUIRED. Paused Flash product claim owns bounded correction; actual native full Recovery/Cleanup remains missing and belongs to authorized Qwen/native lane. #990 retains dependency. #998 protected unpublished o1 work unchanged. Current Codeman hold persisted in AGENTS/current decision83a425ec; no automatic resumption.

### 2026-10-19 — Maintainer stabilization acceptance; real production completion

The bounded infrastructure assignment is accepted: the representative blocked candidates traversed actual trusted production CI and regular protected merges, and all remaining candidates have verified specific external/source blockers with preserved owners. This is not release authorization or Codeman resumption.

| PR | Final head / merge | Actual CI and result |
| --- | --- | --- |
| #1001 | 667e3806 → 5c5f8a18583d1ade0c71f152bbd56fd2861b28b0 | 39184026379 SUCCESS; independent review5565992741 |
| #1002 | ee751691 → 57216ba951933dbbc562f0445662b4cf7494584a | 39184233759 SUCCESS; independent review5565993909; required seven GC tests actually PASS |
| #1003 | d2e81b4f → f08a55a67f5d0a462c7b2c5a345f029bbe6161a6 | 39185004898 SUCCESS; independent review5566058332; strict copied-tree/conflict-resolution real Git regression |
| #985 | 4954f0b1 → 6c3c936028e1e12c0f198518253cc9f1f42387a8 | 39185230474 SUCCESS; fresh source review5566030344; both actual MCP families/build/vet/gofmt |
| #993 | dbf3ef7a → cf63ccfc822796b2c9e8fe0214026bfe06ebb3f3 | 39185400529 SUCCESS; fresh review5566047336; actual five sandbox/seven GC tests |
| #989 | 07d55619 → 7827e6491a7715e0ffffb1e7938764f6788cc30b | 39185646028 SUCCESS; fresh review5566047870; 59 planner tests without skips, eight consent/seven GC/five reset tests |

- All merges used existing protected squash PR flow and exact expected heads. Required PR Selected Checks were green; no required-check bypass, forged approval or source author pretending independent review. Separate read-only Codex technical reviewer performed all infrastructure/fresh-source reviews; no Codeman worker started.
- Root causes: stale consumed BASE versus actual correctly ordered GitHub integration parents; separately copied trusted trees without ancestry/resolved transitions cannot inherit old review. Genuine current-target integrations repaired inputs; fresh independent exact source/status anchors repaired historical qualification. Existing Git parent/tree/ancestry verification remained strict. Real tests reject stale bases, reversed/extra parents, malformed trees and unseen modifications; clean later target merges preserve qualified source.
- Accepted #999/#1000 were audited, not reimplemented. Additional four PR provenance uploads now30days; native Docker/Podman proof30days and both origin workflows protected from aggressive run deletion. Actual new trusted plans are unexpired until2026-11-18, including #985 and #995. Existing older uploads retain their original expiry (retention is prospective); expired old proof is never inferred valid. #990/#998 need fresh current CI when their real blockers are released. Ephemeral build inputs remain bounded; authoritative archived/atomic proof already30days or longer. Actual final verifiers retrieve current plan and authenticated job evidence; existing executor/verifier/API transport regressions pass.
- #995 now02b4cd5f48e449085bc58df625ef6af8fa7bbd73 against develop7827e649. All four worker blobs preserved. CI39185883757 passes Trusted Plan, policy, Focused Python, guided, build/vet/source; final117848399067 only coverage-unresolved4paths, no integration mismatch. Review5566018799 CHANGES REQUIRED for raw diagnostic owner/deployment identity. Final handoff5566105009. Owner paused Flash/Codeman must correct bounded source then obtain independent re-review; Qwen/authorized native lane must prove full recovery and owned cleanup. No native proof or coverage fabricated.
- #990 unchangedbc6bb47a is the narrower fixture input already in #995; full acceptance/supersession waits for corrected native recovery, so it remains blocked. #998 unchanged756b22dc remains blocked by protected unpublished o1 binding and explicit owner continuation/release. Binding task published blob2d035878b17ba191fc15a6ad7faf720ea4d99b1c unchanged. No competing CORE_921 implementation. Original worker files/worktrees could not be inspected in disconnected local environment; none was accessed or mutated.
- Current product develop7827e6491a7715e0ffffb1e7938764f6788cc30b. Product main unchanged. HF Jobs was unavailable at intake and local executor disconnected; all new executable success claims above come from real GitHub CI. No full matrix, native/SSH run, global reset or unrelated resources touched.
- Final Planning canonical acceptance and external blockers published; regular generator output and exact-main47tests/check must be validated below before reporting final synchronization. Codeman remains PAUSED under the current AGENTS/decision until separate explicit Maintainer authorization. Its eventual o1 integration must preserve accepted finite profiles/test wrappers from#1001/#1003.

### 2026-10-19 — Final Planning validation confirmed

- Actual regular generator output published at17aaf3d506048ce1c5fcb59e2790edf18a970efd. Exact-SHA [Planning CI39186227988](https://github.com/mcpdev80/baseharbor-plan/actions/runs/39186227988) SUCCESS:47/47 planning tests,301tasks,7epics,13releases,11decisions; plan.py check0errors/0warnings. The repository-vault validation verifies no stale generated cards/views; no manual generated-block editing.
- Final acceptance/core-754/#993/#989 closures, #995/#990/core-921 external blockers and unchanged claims are all published. This evidence-only append changes no task metadata or generator output; its own current-main validation still runs before coordinator final report. Codeman stays PAUSED until separately authorized, regardless of the accepted stabilization task.
