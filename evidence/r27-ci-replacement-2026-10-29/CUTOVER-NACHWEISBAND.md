# CUTOVER-NACHWEISBAND v0.4.27 (Stand 2026-10-30 ~09:5xZ UTC, alle Angaben erneut gegen Remote geprüft)

## 1. Produkt-Kettenläufe (automatisch, kein Handstep)
- Producer CI 41021394575 (PR #1217 head, pull_request) — success; Public Contracts + Trusted Plan uploads.
- Post-Run Writer 41021632333 — success → Fixture 34b4c06? NEIN: fixtures/records s. unten; Receipt-Record auf planning main.
- Approval-Run 41022064363 (--ref main, pr_number=1217) — success: approve-Commit + Publication + Shadow-Job 'PR · Receipt Shadow Consumption' success.
- Erste komplett automatische Kette zuvor: Runs 41011847920 → 41012128029 → approve 41017075912? NEIN — korrekt: approve success erst 41020139627 (Receipt 41014633723 era) und 41022064363 (final #1217). Historie der Einzelbeweise: tasklink-yamlfix.md + chain-cycle-1207.md.

## 2. Planning-Zeugen (origin/main baseharbor-plan)
- Receipt final: evidence/receipts/public-contracts/41021394575-1.json, approved.by mcpdev80 at 2026-10-30, receipt_commit d4eb0ee-Pendant für finalen Lauf (approved-Feld), status pass.
- Karten-Publication: tasks/t-20261029-r27-ci-producer.md evidence-Feld = EIN gültiger YAML-Block mit https-URL (content-addressed ref auf den approve-Commit) — plan.py check 0 errors.
- Retained: 'checked: public-contracts' (Verifiers retained-Subcommand, finaler Stand, rev 9163cb5/PLANREV 13935a54).

## 3. Negative (fail-closed) — HEUTIGER REPLAY am finalen Pin
- CASE 1 wrong candidate → exit 2 PASS
- CASE 2 wrong plan revision → exit 2 PASS
- CASE 3 edited receipt object → exit 2 PASS
(Kommando + PIN_MAIN=planning 9163cb5; ältere Serie am Pin 46ed3e8c in negative-proofs-replay.md.)

## 4. Approval-Kette Historie (Feuerwehren, alle gemergt)
- PyYAML #1209/#1210 (676edc0a/0b0659f2) · persist-credentials #1211/#1212 (e0de0117/46ed3e8c) · Tasklink-YAML #1213 (develop 5fc601fe, main 5ba82862 via #1214) · Post-Run Eligibility-Gate #1219 (offen, root cause #1218-Röte).

## 5. Regeln & Autorität
- Ruleset develop 25223521 enforcement=active; 25223521-Rollback-JSON bereit.
- Pin BASEHARBOR_RECEIPT_TRUSTED_SOURCE=5ba82862 (Bytes-Regel geprüft: approval-yml + receipt_verifier.py bytegleich auf main e92e2058, Pin darf bleiben, dokumentiert 14:4xZ).
- GITHUB_AUTHORITY Amendment-Draft wartet auf Owner (Datei unangetastet).

## 6. Vorfälle (vollständig, inkl. Coordinator-Fehler)
- o248/#1207 force-push orphan (Lane) → re-chain #1215.
- Coordinator-Kettenbefehl drückte master-HEAD auf reserve-Branch → #1215/#1216 auto-closes → Re-chain #1217, unique heads seitdem.
- Root-Repo zwischenzeitlich auf develop ausgecheckt (Lane-Aktion) → master zurueck, Coord-Skripte wieder da.
- r390 git-add-A rollte 766er Claim in fremden Commit (gezielter add jetzt Vorgabe).
