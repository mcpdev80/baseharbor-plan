---
id: t-20261124-0428-277-reveal-fail-authorizationresult-allow
card_number: "0428-277"
card_short_title: "reveal fail allow"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w86-0428-277-1823test
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-277 · reveal fail allow
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1823]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1823"]
---

- [x] t-20261124-0428-277-reveal-fail-authorizationresult-allow · Bug-Hunt H-V27 intake: reveal failure records AuthorizationResult=allow #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** w86-0428-277-1823test · **Priority:** low  
    **PR:** [baseharbor#1823](https://github.com/mcpdev80/baseharbor/pull/1823)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1823)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w86-0428-277-1823test  
**Priority:** low  
**PRs:** [baseharbor#1823](https://github.com/mcpdev80/baseharbor/pull/1823)  
**Source:** 
<!-- /generated:links -->

## Problem (audit-precision nuance, non-blocker)

- Where: `cmd/baha/environment_operations.go`, Z. 39-44: a failed `inspectApplicationEnvironment` (e.g. `os.Stat(files.ApplicationEnv)` missing at Z. 39) calls `recordRevealFailed`, which reads the stored `AuthorizationDecision` and sets `AuthorizationResult=allow` (the human reveal was authorized) while `Outcome=failed`.
- Expected: an audit event that carries both a consistent authorization-result and outcome.
- Actual: the event records `outcome=failed` (the material fact is correct) but `AuthorizationResult=allow` because the human-operator + secret.reveal decision was already granted upstream (`authorizeHumanReveal`, `cmd/baha/secret_operations.go`, Z. 111-130). The `outcome` field correctly signals the failure; only the authorization-result sub-field is arguably inconsistent with a failed release.
- Severity: Low. Non-blocker; the reveal success path is recorded only after a genuine successful read (`cmd/baha/environment_operations.go`, Z. 52-55) and the H-V14 secret-reveal-paths evidence already validated the reveal seams.
- Ref: H-V14 / 0428-171, finding source `bughunt-hv27 F2` dossier.

## Regression

- A failed reveal must NOT record `AuthorizationResult=allow` for a failed release (fail-closed) or must explicitly record the discrepancy. Either the failing `recordRevealFailed` derives `AuthorizationResult` from the actual reveal outcome (deny on `outcome=failed`), or it records a distinct `AuthorizationResult`/discrepancy value flagging that authorization was granted upstream but the release failed.

## Acceptance

- A failed reveal no longer records an inconsistent `AuthorizationResult=allow` paired with `Outcome=failed`.
- A regression test asserts that a failed reveal records the fail-closed authorization-result (deny) or a clearly-marked discrepancy, and never a spurious `allow` for a failed release.

Failed reveal must not record AuthorizationResult=allow with Outcome=failed (fail-closed or discrepancy marker). Conflict-free write-set.

END_BLOCKED at CI: stray cmd/baha/app_context.go change (gofmt-only, OUTSIDE write-set) forced a 7th pr-gate-coverage row (owner scope). Correction: revert app_context.go, ensure fix is in environment_operations.go/secret_operations.go (card files), rerun. NOT an owner catalog decision unless an in-write-set file still needs a row.

Reverted stray app_context.go; diff = secret_operations.go + secret_audit_test.go only (in-write-set), head 9afd3e6a terminal-green 19 PASS/0 FAIL MERGEABLE. Handed to CODEX-REVIEW (review-only; MERGE deferred so develop is not advanced while #1812 validation run 45385372243 is in flight).

CODEX-REVIEW CHANGES RC1: regression used context.Background() (passes under bug). Fix: seed an ALLOWED AuthorizationDecision (operatorauth.WithAuthorizationDecision) then recordRevealFailed -> assert Outcome=failed + AuthorizationResult=deny; must fail if reverted. Production unchanged. w68 correction.

CODEX verdict RC: regression seeds upstream allow + asserts Subject only; must ALSO seed+assert Assurance and Methods (cmd/baha/secret_audit_test.go:329-373), production unchanged. w86 doing test-only repair on lane-0428-277-revealallow; current head f072dcb not mergeable.

w86 test-only repair DONE: expanded TestAuthorizeHumanRevealFailedRecordsRevealAudit to seed Assurance=loa2 + Methods=[password,webauthn] and assert all three preserved. Production recordRevealForTarget already preserves all three -> NO prod change. Head abec98ea on PR #1823 (OPEN). CI run 45407605826 terminal SUCCESS (PR Selected Checks = integration 15368). Evidence: evidence/r28-welle6-2026-11-25/w86-0428-277-1823test.md. Merge deferred to CODEX after re-review.

MERGED (owner-authorized after green). Rebased exact head 1a2c0d893effca92927d4000722b08f49f89db64, Hosted CI run 45412966378 SUCCESS (incl Docker data-capabilities + PR Selected Checks), PR CLEAN/not-draft/no-open-threads. Squash merge f14fb87c8f5afd91168e4f174d620c9f00e6341e @14:44:38Z. develop=f14fb87c8 (CODEX/owner merge + ls-remote witness). RC (Assurance+Methods assertions) satisfied. #1823 is independent, NOT counted in the #1812->#1819->#1820 chain.
