# r27 shadow-run: harness hardening (lane o227)

## PLAN

1. Read o227.txt, negative-proofs.sh, and the BLOCKER findings in negative-proofs-live.md.
2. Fix the script so the synthetic Case-3 receipt id comes from a non-colliding test-id constant with an optional environment override, and the binders default to the real main chain.
3. Verify the candidate SHA (57a9c4a78b7652fc26025b3e448581222ebb815e), plan (eef674d0b7d9214724417b215495d500cc1c24b2) and the Planning-main receipt (run 40921493079) on the live chain.
4. Run the 3 cases with the corrected script against the live Planning main (read-only), capture setup, command, exit and key stderr for each.
5. Confirm no side effects on planning main (SHA unchanged, working tree clean, Case-3 synthetic workspace isolated and never pushed).
6. Write this evidence file.

## WHY THE PREVIOUS SYNTHETIC ID WAS A BLOCKER

negative-proofs-live.md reported that the earlier script hardcoded the synthetic Case-3 receipt id to 40903927718. That id collides with the REAL receipt evidence/receipts/public-contracts/40903927718-1.json already committed on Planning main. In Case 3 the script does `git add` on the synthetic receipt path; an already-committed file makes `git commit` exit 128, `set -e` aborts the script after commit A, and no Case-3 proof is ever produced. The fix must therefore (a) use a synthetic id that cannot collide with any real main-chain run id and (b) make that id overridable so any other isolated id can be supplied without editing the script.

## SCRIPT FIX

Only evidence/board-2026-10-29/scripts/negative-proofs.sh was edited (evidence path; no product-repo file, no baseharbor-plan file, no git commit/push in either). The script is a new untracked file in this ecosystem repo; its SHA-256 after the fix is a37fdce2a5c67f601e2d6e71a22c62b43e8b6e0977c45fbee5c111a7f4d6d2a0 (219 lines).

The substantive change set is:

- Synthetic Case-3 receipt id now comes from a non-colliding test-id constant with an optional environment override:
  - Before (hardcoded, collides): SYNTH_RUN_ID="40903927718"
  - After (non-colliding + overridable): SYNTH_RUN_ID="${RECEIPT_ID:-99999999999}"
    SYNTH_RECEIPT="evidence/receipts/public-contracts/${SYNTH_RUN_ID}-1.json"
  - The default 99999999999 is a non-colliding test-id range. It never equals a real run id on the chain (not the superseded 40903927718, not the tested 40921493079) and cannot stage an already-committed receipt, so Case 3 commit B introduces a genuinely new path as the verifier's "receipt commit must introduce a new path" rule requires. RECEIPT_ID may override the id for any other isolated value without editing the script.
- Binders now default to the real main chain and are overridable, so the script runs against the authoritative chain without placeholder substitution and fails closed only when an operator truly forgets a binder:
  - RUN_ID="${RUN_ID:-40921493079}"
  - PLAN="${PLAN:-eef674d0b7d9214724417b215495d500cc1c24b2}"
  - PIN_MAIN and CANDIDATE keep their unset/placeholder guards: PIN_MAIN="${PIN_MAIN:-SET_ME_TO_MAIN_HEAD_40HEX}", CANDIDATE="${CANDIDATE:-SET_ME_TO_APPROVED_CANDIDATE_SHA_40HEX}". The script refuses to proceed while either is unset or still at its placeholder value.
- Comment clarification: PIN_MAIN is now documented as the *Planning* main (origin/main of baseharbor-plan) read at runtime from the planning clone, not any product main. The verifier reads receipt blobs and plan fixtures from the Planning clone's Git history; the only git network in the run is the read-only fetch. This disambiguation stops anyone confusing Planning main with a product main. The three Python heredocs that build the Case-3 synthetic receipt (author receipt, clean approval edit, tampering edit) and the Case-3 `git add` / `prove --receipt` all reference the now-variable SYNTH_RECEIPT / SYNTH_RUN_ID, so the override propagates through the whole Case-3 build.

The full diff is reproduced verbatim in the run transcript above this note (script diff captured with `git diff --cached` before the run).

## GUILTIG-ERST-AB

The two earlier case runs reported in negative-proofs-live.md (PIN_MAIN=67359c87 captured from a stale local ref, and a broken script invocation) were already DISCARDED and marked GUILTIG-ERST-AB there; they do not count as evidence and are not repeated here. This run is the first authoritative reproduction of all three negative cases with the hardened script.

## CASE TABLE

Context (first successful chain, run 40921493079): producer run 40921493079, receipt evidence/receipts/public-contracts/40921493079-1.json approved@2026-10-29T17:50:24Z by mcpdev80, receipt_commit ea77ff3faa091ae16e0326200d54906300ed3b6d, candidate 57a9c4a78b7652fc26025b3e448581222ebb815e, plan eef674d0b7d9214724417b215495d500cc1c24b2.

Live Planning main: origin/main HEAD 48860cc360f959217f8553f7091b2c8e628a3d61 (the o224 pin 67359c87 was stale; the chain has since moved). The receipt is committed at 48860cc3, the approval edit ea77ff3 is an ancestor, and the receipt blob carries candidate_sha=57a9c4a78b7652fc26025b3e448581222ebb815e.

Tool: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/negative-proofs.sh (hardened for o227: SYNTH_RUN_ID/SYNTH_RECEIPT now ${RECEIPT_ID:-99999999999}, RUN_ID/RCEIPT/PLAN defaulted to the real chain, PIN_MAIN clarified as Planning main read at runtime; no product-repo file edited).
Verifier: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/receipt_verifier.py mode "retained" (offline: reads blobs/paths from the Planning clone's Git history, no network, no push; every push in the real approval chain goes through the single receipt_writer in-process auth, never here).
VARs: PIN_MAIN=48860cc360f959217f8553f7091b2c8e628a3d61, CANDIDATE=57a9c4a78b7652fc26025b3e448581222ebb815e, PLAN=eef674d0b7d9214724417b215495d500cc1c24b2, RUN_ID=40921493079.
Synthetic Case-3 id: 99999999999 (default; not present on origin/main, verified: ls-remote count 0). No remote touched.

| Case | Setup | Command (abbrev) | exit | key stderr line | Planning origin/main before | after |
|------|-------|------------------|------|-----------------|------------------------------|-------|
| 1 wrong candidate | live Planning clone, wrong candidate sha vs real receipt | python3 receipt_verifier.py retained --planning baseharbor-plan --revision 48860cc3 --receipt .../40921493079-1.json --candidate deadbeef...(40) --plan eef674d0 | 1 | receipt blocked: receipt does not match required candidate/plan | 48860cc360f959217f8553f7091b2c8e628a3d61 | 48860cc360f959217f8553f7091b2c8e628a3d61 |
| 2 wrong plan rev | live Planning clone, plan revision never holds the receipt | python3 receipt_verifier.py retained --planning baseharbor-plan --revision 48860cc3 --receipt .../40921493079-1.json --candidate 57a9c4a7...(CANDIDATE) --plan deadbeef...(40) | 1 | receipt blocked: receipt does not match required candidate/plan | 48860cc360f959217f8553f7091b2c8e628a3d61 | 48860cc360f959217f8553f7091b2c8e628a3d61 |
| 3 edited approval | synthetic workspace /home/marcel/tmp-ops/o224/proof-edited (fresh git clone of Planning, 4 local commits A/B/C/D, never pushed); Case-3 receipt is synthetic 99999999999-1.json (new path, not on main) | python3 receipt_verifier.py retained --planning proof-edited --revision <EDIT_HEAD> --receipt evidence/receipts/public-contracts/99999999999-1.json --candidate 57a9c4a7...(CANDIDATE) --plan <P1> | 1 | receipt blocked: original receipt was edited (canonical fails on the tampered approval edit) | 48860cc360f959217f8553f7091b2c8e628a3d61 | 48860cc360f959217f8553f7091b2c8e628a3d61 |

Script-level result: EXIT=0, all three bounded negative cases behaved as intended.

Per-case exit expectation: block => exit 1 in all three. Result: PASS wrong candidate (exit 1), PASS wrong plan revision (exit 1), PASS edited receipt (exit 1).

RECEIPT_ID override spot-check: RECEIPT_ID=88888888888 produced a fresh synthetic workspace whose Case-3 receipt was 88888888888-1.json and Case 3 still PASS (exit 1), script EXIT=0 — the override path works and stays isolated.

## SUPERSEDED

The receipt evidence/receipts/public-contracts/40903927718-1.json (status pass, approved:null, plan 17ca27b74d8fa5871beb04260619180b968b59ec, sha bb42a2fa727711dc42f8b48e8c9f4375db1a649a) is SUPERSEDED by evidence/receipts/public-contracts/40921493079-1.json (status pass, approved@2026-10-29T17:50:24Z by mcpdev80, receipt_commit ea77ff3faa091ae16e0326200d54906300ed3b6d, plan eef674d0b7d9214724417b215495d500cc1c24b2, sha 57a9c4a78b7652fc26025b3e448581222ebb815e). Nothing is deleted: 40903927718-1.json remains committed on Planning main; this note only records the supersession. The old hardcoded synthetic id 40903927718 in the pre-fix script collided with exactly this real receipt and is the defect o227 fixes.

## repo-rule compliance

- Write-set: only evidence/board-2026-10-29/scripts/negative-proofs.sh was edited (evidence path). No product-repo file edited. No baseharbor-plan file edited; no git commit/push in baseharbor-plan. The script is a new untracked file in the ecosystem repo; it was staged only to capture the diff, then unstaged (git status shows no new staged file).
- Planning main untouched: origin/main HEAD 48860cc360f959217f8553f7091b2c8e628a3d61 unchanged BEFORE vs AFTER every case; local working tree clean except one pre-existing unrelated untracked evidence file (evidence/r27-ci-replacement-2026-10-29/shadow-run-final.md from a prior lane, not authored here).
- Case 3 isolation: synthetic workspace is a local clone under /home/marcel/tmp-ops/o224/proof-edited; `git remote -v` shows only the local planning path as origin, never pushed; no workflow_dispatch, no variables/ruleset changes. The synthetic receipt 99999999999-1.json was a new path (ls-remote count on origin/main = 0). The workspace was deleted after the run.
- No network/hosted dispatch: receipt_verifier.py mode "retained" reads blobs/paths from the Planning clone history; the only git network in the run is the read-only fetch that surfaced the current main HEAD. No push credentials used. No gh run rerun.
- No self-approval / no CI / no release/tag/deploy.

## END

Negative proofs, hardened for o227: the synthetic Case-3 receipt id defaults to the non-colliding test id 99999999999 (overridable via RECEIPT_ID) so it cannot collide with a real main-chain run id including the superseded 40903927718; the binders default to the real chain and PIN_MAIN is documented as the Planning main read at runtime. All three bounded negative cases fail closed (exit 1) as intended, fail-closed verified individually, script EXIT=0, no side effects on Planning main (48860cc3 before == after), synthetic Case-3 workspace isolated and never pushed, RECEIPT_ID override spot-checked. The superseded receipt 40903927718-1.json (approved:null) is documented as superseded by 40921493079-1.json; nothing deleted.

o227-DONE
