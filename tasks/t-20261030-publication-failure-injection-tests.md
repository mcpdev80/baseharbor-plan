---
id: t-20261030-publication-failure-injection-tests
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: ""
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261030-publication-failure-injection-tests · Publication Failure-Injection Tests (Nachlauf PR 1213) #task #release/v0-4-27 #status/planned #view/waiting #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** t-20261017-release-0-4-27-updates  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** t-20261017-release-0-4-27-updates  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Jeder Stage des Publikationspfads (fetch, compare, commit, push, readback, restore) hat einen Test, der den Fehlerfall durch den ECHAUTEN receipt_verifier-Pfad gegen ein bare remote injiziert und HEAD/index/worktree/remote-Zustand assertiert.

## Scope

- In scope: scripts/test_receipt_tasklink.py, scripts/test_receipt_verifier.py (Injektionstests), ggf. minimale Test-Helfer in scripts/.
- Out of scope: Produktcode-Verhalten (in #1213 gemergt), andere Receipt-Komponenten.

## Acceptance

- Sieben Faelle gemaess rv1213f..j-Katalog: fetch-fail, stale-ref, commit-without-push-retry, commit-fail, push-fail, readback-mismatch, restore-blob-reconstruction.
- Jeder Fall laeuft uber den Produktionswrapper, nicht gegen interne Helfer.
- receipt-suite.sh exit0; bisherige Akzeptanz-Matrix bleibt gruen.

## Required checks

- scripts/receipt-suite.sh (5 Suiten) exit0
- CI receipt-execution-tests gruen

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Entstanden aus Owner-Konvergenzentscheid Option 1, baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/konvergenz-entscheid-o246.md (2026-10-30).
- Bezugskandidat: PR #1213, develop 5fc601fe (rv1213j-Dossiers f..j in evidence/board-2026-10-29/codex-rv1213*-merge.md).
