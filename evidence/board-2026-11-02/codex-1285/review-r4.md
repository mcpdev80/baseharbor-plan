# #1285 Union-Tree — unabhängiges Review

ROLLE: REVIEW
Urteil: REJECT
Promotable: no
Reviewer: OpenAI Codex, unabhängige Session; Session-ID und genaue Modellkennung nicht verfügbar, kein Horde-Task zugewiesen.
Zeit: 2026-11-02; exakte Remote-Refs bei Review: main e92e20588c5737f566e29d47bbd08a9bcaed19d3, develop b8b56bbc7aba7203ea077a965b8a1e4942f9cf53, PR-Head 20bef715e0180eddd71e2172c3bfb021ae76109f. ls-remote vor/nach Prüfung kontrolliert. Candidate/Integration nur gelesen.

## Bestätigt

- `git cat-file -p` in /tmp/integ1285-wt2: M2 3fbe8f08099b286764193aed7baba638ab5acce0 hat Tree dfe249ba5ff28e273258a6d8a3d20b0036e4e8de und Eltern S c18b07a88df15bc3afc8a62e53bb3288adf79e37 und main e92e2058. S hat denselben Tree und Elternteil **9a93865a935624045e96a503da0a3a1c2f7d1559**, nicht das aktuelle develop b8b56bbc.
- `git merge-tree --write-tree e92e2058 3fbe8f08` endet 0, Tree dfe249ba. Das ist wegen main als direktem M2-Elternteil ein Ancestry-Nachweis, für sich allein kein Nachweis inhaltlich korrekter Konfliktlösung.
- `git ls-tree` bestätigt für receipt_verifier.py und alle drei Testdateien identische Blob-IDs zwischen M2 und PR-Head. Die plan-getriebene Kandidatenlogik ist somit enthalten.

## Blockierende Gegenbeweise

1. `git diff main..M2 -- internal/runtime/openbao_runtime_prepare.go` entfernt `sslmode=verify-full` und ersetzt es durch `sslmode=verify-ca` (M2 Zeile 178). Dies entfernt die serverseitige Hostnamenprüfung; CA-Prüfung allein ist keine gleichwertige Beibehaltung dieser Defense. Der Verweis auf einen develop-Baseline-Commit beweist keine explizite Owner-Autorisierung, die main-seitige Prüfung aufzugeben. Die Behauptung „keine Defense-Minus-Zeilen“ ist daher nicht belegt und im Wortsinn widerlegt. Zusätzlich entfernt der Diff in `scripts/receipt_verifier.py` die unbedingte Public-Contracts-Prüfung und ergänzt einen No-op-Rücksprung vor Plan-Schema-/Head-/Integration-Prüfung; dies erfordert eine gesonderte vertragliche Bewertung der Ausnahme statt der pauschalen Behauptung, jede main-Pflichtprüfung bleibe erhalten.
2. Der aktuelle develop-Tipp b8b56bbc ist kein Vorfahr von M2 (`merge-base --is-ancestor` exit 1); das S-Elternteil ist der ältere develop-Stand 9a93865a. Die aktuelle PR ist BEHIND. Der vorgelegte Tree belegt keine Integration oder Erhaltung der zwischenzeitlichen develop-Änderungen und kann nicht unverändert als Simulation auf aktuellem develop gelten.
3. GitHub `gh run list --commit 3fbe8f08099b286764193aed7baba638ab5acce0` liefert `[]`; die Evidence belegt nur lokale Builds/Tests, keinen Hosted-Lauf für M2 oder eine nachweislich gleichwertige aktuelle Integration. Hosted-Qualifizierbarkeit und benötigte grüne Gates sind nicht nachgewiesen.

## Rezept und Stop

Worker/Coordinator: aktuellen develop-Tipp in einen neuen, SHA-fixierten Integrationskandidaten einbeziehen; in `internal/runtime/openbao_runtime_prepare.go` die main-seitige Hostnamenprüfung erhalten oder konkrete autoritative Ausnahme samt gleichwertigem Sicherheitsnachweis vorlegen. In `scripts/receipt_verifier.py` No-op und Plan-Authentifizierung gegen den geltenden Receipt-Vertrag einzeln prüfen und entsprechende Negativtests belegen. Konflikte und sämtliche Defense-Änderungen einzeln dokumentieren; neuen S/M2-Tree mit current develop/main rekonstruieren, Diff und merge-tree erneut prüfen und die tatsächlich erforderlichen Hosted-Gates auf der aktuellen Integration bis zum terminalen Ergebnis beobachten. Stop bei fehlender Owner-Entscheidung zu einer bewussten Defense-Abschwächung oder fehlendem Hosted-Nachweis. Kein Merge in dieser Mission.
