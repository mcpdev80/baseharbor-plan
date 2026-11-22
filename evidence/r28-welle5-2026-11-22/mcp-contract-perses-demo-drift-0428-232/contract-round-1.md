# 0428-232 perses MCP contract demo drift - contract-round-1 akte

Sitz `w21-pr1702-0428-232-perses`. Karte 0428-232, owner-order stufe 2.
BELEG: static-mcp job 137190621450 im vollen Pre-Release 45015912507 failt mit 'unexpected baseharbor.app.perses.disable/enable/remove/status' - die vier Perses-MCP-tools sind im gepinnten DEMO-vertrag NICHT (korrekt) gefuehrt.
Auftrag: im REPO baseharbor-demo (Demo-vertrag), NICHT baseharbor produkt, NICHT gate-json, NICHT broker/runtime.

## PLAN

- plan in board-file + ## PLAN in akte
- realitaetsabgleich: develop + gepinnten demo-rev (docs/releases pin) fetchen; pruefen WO der demo-vertrag die erlaubten MCP-tools deklariert (datei:zeile)
- die VIER tools baseharbor.app.perses.disable/.enable/.remove/.status in den gepinnten demo-vertrag aufnehmen; minimaler zusatz, keine tool-semantik aendern
- minimaler laufzeitstatus im demo-repo: kleinste demo-seitige fixture/status-ergaenzung, wenn der gate einen laufenden zustand erwartet
- addiver commit + normaler push; git diff <base>...HEAD --name-only + merge-base --is-ancestor in akte
- beweislog: zeigen dass die vier tools jetzt im vertrag stehen (gate- oder local-zeugnis)

## tools:

- baseharbor.app.perses.disable
- baseharbor.app.perses.enable
- baseharbor.app.perses.remove
- baseharbor.app.perses.status

## pin:

- docs/releases pin im baseharbor-demo repo (noch nicht gelesen)
- gepinnten demo-rev + develop fetchen, dann WO MCP-tools deklariert

## zeugnis:

- (noch nicht erzeugt) gate- oder local-zeugnis, dass die vier tools jetzt als EXPECTED gelten

## SPERREN:

KEIN baseharbor produkt-code, KEIN broker/runtime, KEIN pr-gate-coverage.json (das ist 0428-242), KEIN .github, keine subagenten, kein merge/kommentar. Nur baseharbor-demo Demo-vertrag.

## run:

- (noch nicht laufen gelassen) static-mcp job 137190621450 / pre-release 45015912507

## cleanliness:

(no containers/networks/volumes/compose started; demo worktree)

## END w21-pr1702-0428-232-perses BLOCKED

(to be updated: END_DONE if static-mcp gate green, END_BLOCKED if blocked by pin/permissions)
