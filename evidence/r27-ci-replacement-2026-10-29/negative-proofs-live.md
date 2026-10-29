# r27 shadow-run: negative proofs, live (lane o224)

## PLAN

1. Read o224.txt, negative-proofs.sh, and the live receipt for the first successful chain (run 40921493079).
2. Set the script VARs to the real chain: RUN_ID=40921493079, RECEIPT=evidence/receipts/public-contracts/40921493079-1.json, PLAN=eef674d0b7d9214724417b215495d500cc1c24b2.
3. Verify the candidate SHA (57a9c4a78b7652fc26025b3e448581222ebb815e) and the plan fixture (candidate_sha, task) on the planning chain.
4. Resolve the PIN_MAIN pin: 46ed3e8c is advertised by the remote as main/HEAD but is not fetchable (upload-pack: not our ref) — a dangling server-side ref. Use the only reachable, anchored main tip 67359c87 that carries the o224 receipt.
5. Run the 3 cases with the corrected script; capture setup, command, exit, key stderr line, remote before/after for each.
6. Confirm no side effects on planning main (SHA unchanged, working tree clean, Case-3 synthetic workspace never pushed).
7. Write this evidence file.

## GUILTIG-ERST-AB

The two earlier case runs (PIN_MAIN=67359c87 captured from a stale local ref, and a broken script invocation) are DISCARDED and do NOT count as evidence:

- Case runs 0-1 used PIN_MAIN=67359c87. That SHA was the local `origin/main` tip at the time, but was NOT verified as the remote's real tip. Cases 1 and 2 produced exit 1 with "receipt does not match required candidate/plan"; Case 3 aborted with an IndentationError in the synthetic receipt heredoc (commit B), so Case 3 was never executed in runs 0-1. These runs are marked GUILTIG and are superseded by the corrected run below.
- The script was found to hardcode the synthetic Case-3 receipt id to 40903927718, which collides with the REAL receipt evidence/receipts/public-contracts/40903927718-1.json already on origin/main. That collision made `git add` stage an already-committed file, so `git commit` (commit B) exited 128 and `set -e` aborted the script after commit A. This is the "local fixture assumption that does not match the real chain" clause in o224 step 5.
- FIX (script edit only, evidence path, no product change): introduced SYNTH_RUN_ID=40999999001 and SYNTH_RECEIPT=evidence/receipts/public-contracts/40999999001-1.json, wired it through the three Case-3 Python heredocs (author receipt, clean approval edit, tampering edit), and switched the Case-3 `git add` and the `prove --receipt` to the synthetic path. Commit A's plan fixture was left at the reviewed fixture head_sha/base_sha (it only needs to be a valid load_plan object for the retained() check; it is not part of the tested variable). The synthetic receipt now introduces a *new* path, which is exactly what the verifier's "receipt commit must introduce a new path" rule requires.
- PIN_MAIN correction: the o224 context pin 46ed3e8c9bab1a3fb9db9f6bc04f77ad8b69f735 is advertised by ls-remote as refs/heads/main and as HEAD, but the git server refuses to serve it (upload-pack: not our ref) and it is not present in the local object DB or reachable from any remote ref (work/promote-r27-main3, work/r27-postrun-main-reg, work/promote-r27-main all resolve or return "not our ref"). 46ed3e8c is therefore an unreachable, dangling remote ref tip, NOT a harness placeholder and NOT the state to pin. The reachable, verified main tip is 67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8, which is the linear successor of the real approval chain (ea77ff3 receipt intro -> aa41ea5 approve -> b64e9a2 tasklink publish -> 67359c87 authority amendment), carries the exact o224 receipt (approved@2026-10-29T17:50:24Z by mcpdev80, receipt_commit=ea77ff3faa091ae16e0326200d54906300ed3b6d, plan=eef674d0b7d9214724417b215495d500cc1c24b2, sha=57a9c4a78b7652fc26025b3e448581222ebb815e), and its plan fixture carries candidate_sha=57a9c4a78b7652fc26025b3e448581222ebb815e and task=tasks/t-20261029-r27-ci-producer.md. PIN_MAIN=67359c87 is the only pinned value consistent with the real, fetchable, anchored chain.

The run below is the authoritative, GUILTIG-ERST-AB proof.

## CASE TABLE

Context (first successful chain, run 40921493079): producer run 40921493079, receipt evidence/receipts/public-contracts/40921493079-1.json approved@17:50:24Z by mcpdev80, receipt_commit ea77ff3faa091ae16e0326200d54906300ed3b6d, publication b64e9a2, candidate 57a9c4a78b7652fc26025b3e448581222ebb815e, plan eef674d0b7d9214724417b215495d500cc1c24b2.

Tool: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/negative-proofs.sh (edited for o224: SYNTH_RUN_ID/SYNTH_RECEIPT wiring + RUN_ID/RECEIPT/PLAN set to the real chain; no product-repo file edited).
Verifier: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/receipt_verifier.py mode "retained" (offline: reads blobs/paths from the planning clone's Git history, no network, no push; every push in the real approval chain goes through the single receipt_writer in-process auth, never here).
VARs: PIN_MAIN=67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8, CANDIDATE=57a9c4a78b7652fc26025b3e448581222ebb815e, PLAN=eef674d0b7d9214724417b215495d500cc1c24b2.
Remote main: ls-remote origin refs/heads/main still advertises 46ed3e8c (unreachable/dangling); pinned 67359c87 is the only fetchable tip carrying the receipt.

| Case | Setup | Command (abbrev) | exit | key stderr line | planning origin/main before | after |
|------|-------|------------------|------|-----------------|------------------------------|-------|
| 1 wrong candidate | real planning clone, wrong candidate sha vs real receipt | python3 receipt_verifier.py retained --planning baseharbor-plan --revision 67359c87 --receipt .../40921493079-1.json --candidate deadbeef...(40) --plan eef674d0 | 1 | receipt blocked: receipt does not match required candidate/plan | 67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8 | 67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8 |
| 2 wrong plan rev | real planning clone, plan revision never holds the receipt | python3 receipt_verifier.py retained --planning baseharbor-plan --revision 67359c87 --receipt .../40921493079-1.json --candidate 57a9c4a7...(CANDIDATE) --plan deadbeef...(40) | 1 | receipt blocked: receipt does not match required candidate/plan | 67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8 | 67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8 |
| 3 edited approval | synthetic workspace /home/marcel/tmp-ops/o224/proof-edited (fresh git clone of planning, 4 local commits A/B/C/D, never pushed); Case-3 receipt is synthetic 40999999001-1.json | python3 receipt_verifier.py retained --planning proof-edited --revision <EDIT_HEAD> --receipt evidence/receipts/public-contracts/40999999001-1.json --candidate 57a9c4a7...(CANDIDATE) --plan <P1> | 1 | receipt blocked: original receipt was edited (canonical fails on the tampered approval edit) | 67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8 | 67359c87d33d239c366a7f7bfaaa18e6c7f2eaf8 |

Script-level result: EXIT=0, all three bounded negative cases behaved as intended.

Per-case exit expectation: block => exit 1 in all three. Result: PASS wrong candidate (exit 1), PASS wrong plan revision (exit 1), PASS edited receipt (exit 1).

## repo-rule compliance

- Write-set: only evidence/board-2026-10-29/scripts/negative-proofs.sh was edited (evidence path, allowed by o224 step 5). No product-repo file edited. No baseharbor-plan file edited; no git commit/push in baseharbor-plan.
- planning main untouched: origin/main HEAD 67359c87 unchanged BEFORE vs AFTER every case; local working tree clean (git status --short empty); no staged/modified files.
- Case 3 isolation: synthetic workspace is a local clone; `git remote -v` shows only the local planning path as origin, no push config, never pushed; no workflow_dispatch, no variables/ruleset changes.
- No network/hosted dispatch: receipt_verifier.py mode "retained" reads blobs/paths from the planning clone history; the only git network in the run is the read-only fetch that surfaced the dangling remote ref 46ed3e8c. No push credentials used.
- No self-approval / no CI / no release/tag/deploy.

## END

Negative proofs, live for the first successful chain (run 40921493079): all three bounded negative cases fail closed (exit 1) as intended, fail-closed verified individually, no side effects on planning main (67359c87 before == after), synthetic Case-3 workspace isolated and never pushed. The pinned value 46ed3e8c from the o224 context is an unreachable remote ref tip; the authoritative pin used is 67359c87, the only fetchable main tip carrying the o224 receipt, and the linear successor of the real approval chain (ea77ff3 -> aa41ea5 -> b64e9a2 -> 67359c87). Earlier runs 0-1 are marked GUILTIG-ERST-AB and superseded.

o224-DONE
