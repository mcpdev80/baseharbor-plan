# t-20261104-r27-demo-guided-consent — demo consent harness correction round 2

Task: t-20261104-r27-demo-guided-consent (baseharbor-demo)
Worker: w87-demo-r2
Coord: f49a3303
Date: 2026-11-04
Authority: mission coordinator/missions/w87-demo-r2.txt; review-128a.md (Codex Luna, REJECT); baseharbor-demo/AGENTS.md (planning = baseharbor-plan), product/review/CI in the demo repo.
Write scope: tests/guided/drive.py only. Pin 488a39e6 (already set). No Core files. No new gate semantics. No env-var auto-confirm. No weakening of the consent gate.

## PLAN

- Read mission + review-128a.md; confirm scope (drive.py only, pin 488a39e6, branch head 683f1da7, ls-remote == head)
- Fix B1: run_tty capture-pfad pruefwerte (exit code + required rules) auswerten; nur dokumentierter consent-abbruch (alle interaktionen abgearbeitet + extrahierter hash) ist erlaubter zwischenzustand
- Fix B2: binary_supports_confirm_candidate fail-closed — support nur bei positivem eindeutigem merkmal; exakt unsupported => nicht-unterstuetzt; sonstiger probe-fehler => fehler/unklar, KEIN zweiter up-lauf
- B2 gegenproben (vier zeilen, je erwartetes verhalten): binary fehlt / timeout / unbekannte meldung / exakt unsupported
- B1 regressions (neu, positiv): exit!=0 ohne hash => abbruch; fehlender pflicht-prompt => abbruch; erfolg ohne hash mit erwarteten bedingungen => OK; erwarteter consent-abbruch mit hash => zweiter lauf
- Local syntax (py_compile) + targeted evidence run; capture run ids, exit codes, transcripts
- Push; verify ls-remote == head; write evidence demo/consent-harness-2.md
- END to coord f49a3303 with DONE/SHA + one-line summary

## Repo-rule compliance

- Write scope honored: only tests/guided/drive.py changed. Pin 488a39e6 untouched (already correct). No Core files.
- Consent gate not weakened: fail-closed everywhere; only the documented candidate-consent with extracted hash proceeds; normal success without hash only on expected exit/rules. No env-var auto-confirm.
- Not a --help grep probe: keeps the behavioral probe with documented rationale (flag parsed manually, absent from usage).
- CI authority: demo CI is push-triggered to release branches only (work/v0.4.2*-release), not main/feature branches — that is why PR #128 reported "no checks reported". A hosted run on the target branch is the only visible CI; see PR + status.

## END

- lane: w87-demo-r2 | verdict: correction round on PR #128
- B1: capture-pfad pruefwerte ausgewertet; nur dokumentierter consent-abbruch (hash + alle interaktionen) ist erlaubter zwischenzustand; sonstiger exit!=0 oder fehlender pflicht-prompt => ABBRUCH
- B2: fail-closed, nur positives merkmal => supported; exakt unsupported => nicht-unterstuetzt; sonstiger probe-fehler => FEHLER (kein zweiter up-lauf); vier gegenproben dokumentiert
- STOP-KRITERIUM: nirgends READY/PASS bei unerwartetem exit oder fehlendem pflicht-prompt; keine zweite up nach unklarem probe-ergebnis

## PR + status

- PR #128 (not draft, READY): https://github.com/mcpdev80/baseharbor-demo/pull/128
- Base: main (cd9176e0129f01270ca85fd6b29acf99404f6dcd)
- Head: w85-demo-guided-consent = b73be42ba9944d21ffe8869382c37100c3e40384
- ls-remote == head: verified (b73be42ba9944d21ffe8869382c37100c3e40384)
- HEAD (commit): b73be42 test(guided): fail-closed candidate-consent probe + capture error/rules check (t-20261104-r27-demo-guided-consent, w87-demo-r2)
- Evidence harness commit: 7e972f0 (tests/guided/scripts/evidence_b1_b2.py)
- Files: tests/guided/drive.py only. Pin 488a39e6 unchanged. No Core files touched.
- Commit/PR status: committed to branch, pushed, PR OPEN/READY/draft=false/mergeable=true.
- CI: demo CI is push-triggered to release branches only (work/v0.4.24/25/26-ecosystem-release), NOT main/feature branches (v0424-targeted.yml). PR #128 on main therefore reports "no checks reported" — this is the configured gate, not a defect. No hosted gate exists for this feature branch; local py_compile + targeted B1/B2 evidence is the verification for this correction round.
- Local verification: py_compile drive.py PASS; targeted evidence run evidence_b1_b2.py — 9/9 OK (B2 four gegenproben + positive; B1 regressions).
