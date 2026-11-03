# PR #1324 — Merge-Gate 775f7a23

ROLLE: MERGE. Ergebnis: **END_BLOCKED**, kein Merge ausgeführt.

Vorher-Nachweis: `gh pr view` meldete OPEN, MERGEABLE, CLEAN und Head `775f7a2355fbddd56a196b704f021e635e223228`; `git ls-remote origin refs/heads/develop refs/pull/1324/head` bestätigte develop `01784c388666cea9d656b5a383bf594c45c86ff7` und denselben PR-Head. `PR Selected Checks` war auf diesem Head erfolgreich, App-ID 15368, Run 41588070331; Review-Threads: keine. Das in `review-1324n.md` dokumentierte Ergebnis ist ACCEPT-WITH-DEFERRAL; die dort benannte Folgearbeit bleibt offen.

Blocker: Die Live-API `repos/mcpdev80/baseharbor/rulesets` meldet sowohl `develop - integration branch` (23754541) als auch `develop - required checks` (25223521) als `disabled`; `rules/branches/develop` liefert `[]`. Damit sind die in der bindenden GitHub-Authority vorausgesetzten aktiven Schutzregeln derzeit nicht vorhanden. Zusätzlich fordert die Mission anhand der Historie einen Merge-Commit und den PR-Head als Vorfahren; die GitHub-Authority fordert ausdrücklich einen Squash-Merge mit Expected-HEAD-Guard. Ein Squash erfüllt diesen Vorfahrennachweis nicht. Die konkrete Regelkollision muss autoritativ geklärt und der Schutzstatus geklärt werden; keine Schutzregel wurde geändert oder umgangen.

Nachtrag: Coordinator-Klärung löst den Merge-Stil-Konflikt zugunsten Squash und ersetzt den Ancestry-Nachweis durch einen Inhaltsvergleich. Erneute Live-Abfrage: Head und develop unverändert, PR OPEN/CLEAN, beide develop-Rulesets weiterhin `disabled`. Der Schutzstatus bleibt ungeklärt; kein Merge ausgeführt.

## Abschluss nach Klärung 2

ROLLE: MERGE. Coordinator stellt fest, dass die deaktivierten Rulesets nichts erzwingen, und autorisiert ausdrücklich den Squash-Merge. Unmittelbar davor bestätigten `gh pr view` OPEN/CLEAN und Head `775f7a2355fbddd56a196b704f021e635e223228`, `ls-remote` denselben Head und develop `01784c388666cea9d656b5a383bf594c45c86ff7`; `PR Selected Checks` SUCCESS, App 15368. `gh pr merge 1324 --squash --match-head-commit 775f7a2355fbddd56a196b704f021e635e223228` erfolgreich ohne Admin.

GitHub meldet MERGED, mergedAt `2026-11-03T06:18:11Z`, Merge-Commit `9a57107f8b2b71011b66025efbb73b39ab1ff12f`; `git ls-remote origin refs/heads/develop` liefert dieselbe SHA. Fetch per HTTPS bestätigt FETCH_HEAD; der `git diff --exit-code 775f7a2355fbddd56a196b704f021e635e223228 FETCH_HEAD -- contracts/managementaccess/v1 docs/spec/credential-access-v1.md docs/de/spec/credential-access-v1.md` war leer (Exit 0). Der zunächst versuchte SSH-Fetch scheiterte an lokaler SSH-Konfiguration; HTTPS erfolgreich. Die in `review-1324n.md` dokumentierten Deferrals bleiben bestehen.
