# Owner review of the automatic-chain state — 2026-10-27 (authoritative)

Marcel independently re-checked PR #1111 and the newer integration 38771771. This review supersedes rv1's verdict `ACCEPT_WITH_NONBLOCKING` for those trees (rv1's document stays as preserved history, not acceptance). No architecture redesign is requested; close exactly these gaps before merge and activation.

## Confirmed gaps
- G1 post-run broken: invalid YAML (actionlint confirms), still wrong run-ID/plan-revision passing, still overwritten GITHUB_* values.
- G2 test execution faulty: the new discovery check rejects correct unittest success output; the claimed workflow-policy test suite is not executed by the file pattern in use.
- G3 publisher violates the order: a `git push -f` remains; the promised bounded re-apply of own changes under parallel independent edits is missing.
- G4 task link still absent: writer and verifier use different mapping rules; no actual automatic evidence update of a card is implemented.
- G5 approval→shadow not connected: shadow stays disabled; the approval workflow does not invoke it; the allowed approval source was unilaterally widened to main and develop.
- G6 review/report integrity: ACCEPT_WITH_NONBLOCKING contradicts its own named blockers; the later integration report called the real YAML error a false alarm.

## Independently verified by the Owner
- 120 receipt tests, 118 passed, 2 failed; #1111 CI failed. main (= published 0.4.26) unchanged; the Owner changed and started nothing during this check.

## Standing instruction
Keep three parallel lanes on the disjoint packages, close G1-G6 concretely, then re-qualify ONE updated candidate through legacy CI before any merge or activation.

## END OWNER-REVIEW-2026-10-27
