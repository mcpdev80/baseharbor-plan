# Coordinator correction: finish the automatic one-gate chain

Owner instruction: 2026-10-27. This is the current corrective direction for the v0.4.27 receipt work. It supersedes contradictory scheduling and manual-pilot instructions in earlier runbooks. Preserve actual claims, source and evidence; do not restart the architecture.

## Outcome, not intermediate green jobs

Keep the approved minimal design: one canonical receipt below 500 bytes, no own PKI/signatures, no payload archive or retention service. GitHub is the live witness; after genuine Owner approval, protected Planning history is the authority. Exactly ONE gate must traverse the complete chain automatically. The explicit Owner approval decision is the only permitted manual action; no human copies run IDs/hashes, downloads patches, edits receipts or publishes evidence.

Observed baseline to refresh before working: #1092 is merged and includes the accepted #1090 implementation; #1090 is closed without a separate merge. A successful Owner approval run and an approved Planning receipt exist. That does NOT prove automatic publication or end-to-end consumption: the approval workflow exports a patch, post-run/shadow jobs are still dormant, and its main-context assertion was overwritten in-shell. Treat those as concrete remaining gaps, not accepted skeleton evidence.

## Three workers, start together

Use three TOTAL worker slots plus the coordinator. Freeze current callable interfaces and assign disjoint files from the same fresh baseline. Preserve ongoing work rather than dispatching replacements for it.

| Worker | Work now | Exclusive writes |
| --- | --- | --- |
| W1 | Real trusted workflow/ref policy, exact discovery/selection, shadow retained consumption and removal of temporary diagnostic policy exceptions | Legacy planner/runner/policy registrations and their tests; receipt-shadow.yml; paired docs |
| W2 | Automatic bounded publication of the receipt/plan/task link with concurrency-safe normal pushes; post-run production wiring | receipt_writer.py, receipt_tasklink.py, their focused tests; receipt-post-run.yml |
| W3 | Genuine Owner approval context, automatic publication of its sole allowed edit, live/offline verification and the three negatives | receipt_verifier.py, verifier/chain tests; receipt-approval.yml |

All prepare and test concurrently; do not wait for another worker's acceptance to work against the frozen existing interface. W2 owns a shared publication interface if needed inside receipt_writer.py; W3 consumes that agreed interface without editing W2's file. No third production publisher, framework or duplicate authority. Coordinator serializes common-branch pushes, Planning metadata and integration. Rebalance by remaining effort; free workers cross-review another package, not their own acceptance.

## Required corrections

1. Remove GITHUB_REF spoofing and other manufactured identity assertions. Check the real GitHub workflow/actor/ref against the explicitly accepted protected source policy. If main is required, run the reviewed workflow from main; if protected develop is deliberately allowed, change that policy honestly and test rejection of untrusted refs. Do not replace a failed protection check with a caller-set boolean or environment string.
2. Activate only the bounded pilot post-run and shadow paths from reviewed trusted code. Privileged jobs must never execute PR-controlled source or give fork jobs Planning write credentials. Derive the tested head/base/integration identity from the existing authenticated trusted-pr-plan; API head_sha alone is insufficient. Check run, attempt, workflow and exact job outcomes.
3. Publish unapproved and approved receipts plus task references automatically. A successful local commit, uploaded patch or summary is not publication. Use a least-privilege Planning credential and ordinary fast-forward/expected-head updates, preserving concurrent edits. No force push; retries must be idempotent. Only the approved field may change once. Check the published exact bytes/history before reporting success.
4. If the scoped cross-repository credential/protected-source configuration is unavailable, prepare everything else, then state the exact setting, required rights and concrete activation action once. Do not simulate access, export a manual patch as the finished solution, or debug the absence through repeated hosted runs. Never print credentials.
5. Remove temporary diagnostics and stale comments that claim activated jobs are dormant. Preserve the legacy required final-check until accepted skeleton proof; shadow verification is informational until the separate PR3 cutover. Do not mix unrelated product fixes into this evidence candidate.

## One coherent candidate, one sufficient hosted qualification

Integrate all three packages into a single reviewable correction candidate on top of the actual merged baseline. Keep documentation and relevant tests in that candidate. Resolve identity, rights, mapping/test discovery and local positive/negative failures BEFORE pushing. Inspect any current CI result first. No one-file push/merge/dispatch loops and no full runtime matrix.

Then demonstrate one ordinary contributor path:
producer -> trusted writer -> published unapproved receipt -> fresh live verification -> real Owner approval -> published approval -> automatic task link -> retained shadow final-check consumption.

Use the production verifier path for the positive and three controlled negatives: wrong candidate SHA, genuinely nonexistent run ID, edited receipt/history. Do not corrupt the real approved receipt or count a network outage as proof of the expected dead-run rejection. The positive retained verification must work with GitHub API access disabled. Preserve exact tested source and outcomes automatically; local fixture success is not hosted acceptance. Another worker/coordinator reviews the integrated result.

Accept the skeleton only when ALL links, the ordinary-contributor/no-manual-evidence behavior and three negatives are demonstrated. Successful approval alone, a manually replayed chain or skipped post-run/shadow jobs are not acceptance. Summary stays at most checked / validly reused / not required with reason; not-required never means PASS. Only then prepare/accept the separate PR3 required-check cutover. No additional gates before that.

## Planning and fixed deadline

Update the existing resolver/pilot/acceptance cards with current PRs, concrete blockers and actual evidence; mark paper-only runbooks historical. Do not close acceptance from this instruction or relabel missing checks as green. Keep three-worker ownership and actual progress visible.

T0 remains 2026-10-26T23:35:50Z; deadline remains 2026-10-29T23:35:50Z. New correction PRs do not reset it. Without accepted skeleton by the deadline, stop infrastructure expansion and route eligible product work through adequate existing trusted legacy checks, publishing the precise remaining blocker. No silent extension or weakening of product requirements.

Use GitHub MCP and normal repository validation. This direction authorizes finishing the agreed chain, not a new evidence platform or release. Report completion only with an accepted automatic chain, or a concrete external configuration blocker requiring Owner action.
