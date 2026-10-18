---
id: 2026-10-18-horde-codex-handover-pause
status: accepted
sources: []
---

# Temporary development pause for the Horde/Codex handover test

## Context

Marcel requested a pause on 2026-10-18 to test Horde and Codex against the repositories. This decision records operational authority and the immutable handover snapshot; task notes remain the canonical lifecycle records. The pause is not a release freeze qualification, product acceptance or permission to weaken mandatory checks.

## Decision

- Stop source implementation, merges, native/SSH tests and new runtime/CI dispatches. Only this bounded Planning reconciliation and explicit subsequent Maintainer test assignments are authorized.
- Session 1 previously owns core-921/#998; Session 2 previously owns the #995 bootstrap/cleanup correction. Their claims and work are preserved, writes paused. Do not silently clear or steal ownership. A test worker must read the task, receive an explicit assignment/transfer, publish its claim and preserve all prior commits before changing source.
- Qwen owns native tests only, not source fixes. Its latest #995 run finished with failure and owned-resource cleanup. An owned checkout remains on the authorized test system; no secret/access/local-path details are published. Removing it is a Qwen-only scoped housekeeping step after checkpointing sanitized evidence.
- Review, immutable coverage qualification, actual required CI, Maintainer merge, Planning acceptance and release qualification remain separate decisions. A read-only Horde/Codex evaluation may inspect all public source/evidence; it may not infer implementation or merge authorization.
- Resume only through Marcel's explicit assignment or resumption instruction. This temporary notice should be removed/marked ended as part of that coordinated resumption; do not leave an ambiguous permanent prohibition.

## Verified product snapshot

Current develop: `f2bad5efa27fa2a791e5b357509af92d8861a3f1`. Product main and unrelated repositories are unchanged by this cleanup.

| PR | Exact open head | State / next boundary |
| --- | --- | --- |
| #998 | 756b22dc8967d0daa7393065cd5bc15f262c7050 | Draft, core-921 implementation handed off; full independent source review and immutable coverage still pending. CI 39130075369 reported functional/docs green, final unresolved. |
| #995 | eaf86813f789f62b393ecf9ad287ae04b3ff7561 | Open, prior bounded correction source-reviewed; latest native run FAIL before backup and automatic cleanup fails ownership. Existing canonical correction task blocked. No native recovery acceptance. |
| #993 | b981f3b60bebfaebf6eb7f2f467dfd06142c90fe | Draft, source review positive; formal coverage/current mandatory CI and merge pending. Never use global reset on shared systems. |
| #990 | bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f | Draft, partial fixture fix included in unmerged #995; do not close as accepted recovery. |
| #989 | 78a72ebad0723eefe760090bc34130b55858d8a3 | Open, source/native positive evidence present; formal qualification/current mandatory CI/merge pending. |
| #986 | 7b666773c948fedef0ea337f6212ee982986c88d | Open legacy CI PR; work included in merged #991, administrative supersession still to verify/publish, not a second implementation lane. |
| #985 | 5a3813385af5392a9be3095bd038424a4f9950b7 | Draft, test-only positive content review; current trusted-base Go execution/vet/build and source qualification remain pending. |
| #616 | 875dc5edd5efd56799fd61ba40a75fe69a513e7b | Unrelated historical PR targets main; outside this handover cleanup, untouched. |

Already merged by Manager: #983 -> 980e8db8; #996 -> 29cb0920; #982 -> 85dfcfa3; #997 -> 58efa1a3; #984 -> 8e77b704; #991 -> 9f622e6e; #978 -> f2bad5ef. Each merge has prior independent review and actual green mandatory CI; no self-approval or required-CI bypass. Core-918 and core-751 are accepted; core-921 and recovery tasks are not.

## Latest native failure and restart point

Exact #995 eaf86813, rootless Podman 5.7.0 / Go 1.26.9, user-supplied Qwen run FAIL at 166.76s:

1. Guided Core setup and manager readiness advance past the old second-Bootstrap failure.
2. App apply rejects obsolete fixture service key postgres; parser expects capability names. Backup/Destroy/Restore and SQL/secrets/consumer/identity-regeneration assertions never run.
3. Registered cleanup executes, but authorized destroy refuses unverified Target/deployment ownership. io.Discard hides the structured report; exact failing owner/caller still needs safe diagnosis.
4. Qwen removed only its owned resources; unrelated resources remained untouched. No global reset/helper, source fix or merge.

Resume on existing #995 by first validating its manifest through the real parser without native startup, then diagnosing cleanup with bounded redacted structured output and existing ownership/consent authority. Do not soften guards, invent evidence, print secrets or create another duplicate issue/task. Independent exact-SHA review precedes Qwen's next native retest.

## Consequences and closeout requirement

Canonical task updates and this discoverable handover are published atomically. Generated views are not edited by hand. Before treating the repository handover as synchronized, an executable Planning owner must pull current main, run release-cycle sync where required, regular render/check and all Planning tests, publish all generated changes while preserving concurrent work, and validate the final pushed SHA. Manager execution is offline and HF Jobs connector unavailable in this session; no new executable validation or clean local worktree is claimed.

All public handover records omit private hostnames, IPs, SSH aliases, local checkout/report locations, credentials and secret-bearing diagnostics. Root has no access to the external sessions' local worktrees and cannot certify them clean; each worker must preserve/commit or explicitly report its own outstanding changes, without deleting other work.
