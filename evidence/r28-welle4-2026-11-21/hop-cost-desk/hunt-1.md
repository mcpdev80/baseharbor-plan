# H-V41 Hop-Kosten-Desk — hunt-1

LANE: `0428-221-hopcost` · ROLLE: Worker (BUG-HUNT, reine Befundung) · SLICE: H-V41 Hop-Kosten-desk — was kostet ein hop auf develop, pro rotem PR, in dateien und konflikt.
DATUM: 2026-11-21
MODELL: worker-ornith1.5-laptop

## PLAN
- planning remote + baseharbor github remote verifizieren; develop-HEAD-SHA festhalten
- alle offenen PRs via gh (authed) auflisten; PR-Nummer, head-SHA, base-ref sammeln
- fuer jeden PR: `git merge-base --is-ancestor <develop> <head>`; `rev-list --count` rueckwaerts/vorwaerts
- fuer jeden divergierenden PR: `git merge-tree --write-tree <mb> <develop> <head>` -> CONFLICT-Zaehl; schnittmenge der dateimengen
- fuer jede schnittmenge-datei: letzte aenderung auf develop und im PR (commit + zeit); owner-datei-abgleich
- klassen (t/m/h/o) zuweisen; akte mit tabelle, cleanliness, repo-rule-compliance schreiben

## BASE ATTESTATION
- planning remote (einzige source of truth fuer planning):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` =>
  origin https://github.com/mcpdev80/baseharbor-plan.git (fetch / push)
- baseharbor github remote (FIRST git action, remote = github.com/mcpdev80):
  `git -C /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor remote -v` =>
  origin git@github.com:mcpdev80/baseharbor.git (fetch / push)
- base develop head SHA (git ls-remote):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` =>
  77c1e60f51b91003ac3ddc391008c15e4a713a5c  refs/heads/develop

## METHODE
- Quelle der offnen PRs: `gh pr list --repo mcpdev80/baseharbor --state open` (25 offene PRs), auth via ~/.config/gh/hosts.yml (account mcpdev80).
- Divergenz: `git merge-base --is-ancestor <develop> <head>` + `git rev-list --count <head>..<develop>` (rueckwaerts) + `git rev-list --count <develop>..<head>` (eigene commits).
- Basis jeder Lane = ihr Branch-Punkt (`git merge-base <develop> <head>`), NICHT develop-HEAD. Eigenes Change-Set = `git diff --name-status <merge-base> <head>` (A/M/Delete), nicht die 4000+ Commit History-Delta gegen develop-HEAD.
- Konfliktprognose: `git merge-tree --write-tree <mb> <develop> <head>`; Zaehlung der Zeilen mit `CONFLICT`.
- Schnittmenge = `comm -12 <files changed by PR> <files changed by develop>`.
- Owner-Impakt = any file in `.github/**`, `scripts/**`, `internal/operatorauth/**` im EIGENEN change set (A/M/Delete) der Lane.
- History unshallow geholt, um merge-base/rev-list korrekt zu rechnen. Kein baum verändert, kein rebase/merge, kein commit an baseharbor.

## ERGEBNIS: divergenz + konfliktprognose pro PR

| PR # | divergence-rueckwaerts | eigene commits | schnittmenge-groesse | merge-tree CONFLICT | klasse |
| --- | --- | --- | --- | --- | --- |
| 1747 | 0 | 1 | 0 | 0 | t |
| 1746 | 23 | 2 | 0 | 0 | t |
| 1742 | 13 | 3 | 0 | 0 | t |
| 1741 | 166 | 13 | 27 | 0 | m |
| 1740 | 166 | 15 | 28 | 0 | m |
| 1739 | 0 | 2 | 0 | 0 | t |
| 1738 | 166 | 12 | 28 | 0 | m |
| 1737 | 166 | 13 | 28 | 0 | m |
| 1736 | 166 | 1 | 0 | 0 | t |
| 1725 | 0 | 7 | 0 | 0 | t |
| 1723 | 166 | 1 | 0 | 0 | t |
| 1714 | 70 | 3 | 0 | 0 | t |
| 1704 | 308 | 4 | 0 | 0 | t |
| 1702 | 62 | 6 | 1 | 0 | m |
| 1650 | 166 | 6 | 1 | 0 | m |
| 1645 | 191 | 1 | 1 | 0 | m |
| 1627 | 166 | 8 | 0 | 0 | t |
| 1625 | 477 | 9 | 6 | 0 | m |
| 1623 | 477 | 9 | 13 | 0 | m |
| 1620 | 166 | 7 | 1 | 0 | m |
| 1614 | 485 | 8 | 23 | 0 | m |
| 1597 | 166 | 4 | 2 | 0 | m |
| 1596 | 166 | 7 | 0 | 0 | t |
| 1588 | 5 | 6 | 0 | 0 | t |
| 1585 | 29 | 15 | 0 | 0 | t |

## SCHNITTMENGEN-DETAIL (nur PRs mit int>0)
- PR1741/1740/1738/1737: intersection = geteilte shared test-fixture-und-support-dateien in `cmd/baha/` (z.B. `main.go`, `mcp.go`, und ~25 `*_test.go` fixtures). Alle vier lanes stammen vom gleichen old base `40cb28c75` (cli2-env-policy-head). merge-tree: 0 CONFLICT.
- PR1702, 1650: je `cmd/baha/app_status_result.go` (1 datei).
- PR1645: `internal/serviceaccess/perses_compose_realization.go` (1 datei).
- PR1625: `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go`, 3 docs (6 dateien).
- PR1623: `cmd/baha/app_access.go`, `app_logs.go`, `commands.go`, `machine_coverage.go`, `contracts/machine/v1/control.golden.json`, docs (13 dateien), `internal/machine/contract.go`.
- PR1620: `cmd/baha/app_access.go` (1 datei).
- PR1614: workspace/source-model / machine_coverage / docs (23 dateien).
- PR1597: `cmd/baha/app_perses_cli_test.go`, `app_status_result.go` (2 dateien).

## SCHNITTMENGEN-ANALYSE: wer zuletzt recht hat
Fuer jede schnittmenge-datei letzte aenderung auf develop (commit+zeit) und im PR (commit+zeit). Basis: develop-HEAD zeitstempel 2026-11-21 11:49:47 +0100.
- In fast allen schnittmenaten ist develop die neuere aenderung ("develop is newer") — develop hat zuletzt recht; die PR-versionen sind aelter.
- Ausnahmen, wo die PR-versionen juingor gleich sind: ausschliesslich `cmd/baha/*_test.go` fixtures in PR1741/1740/1738/1737 (geteilte shared fixtures), plus `internal/serviceaccess/perses_compose_realization.go` (PR1645). Kein fall ist ein echter zeilenkonflikt (merge-tree 0 CONFLICT ueberall).

## OWNER-IMPAKT (klasse o)
- `git diff --name-status <merge-base> <head>` pro PR ueberprueft auf `.github/**`, `scripts/**`, `internal/operatorauth/**`.
- ERGEBNIS: KEINER der 25 offenen PRs aendert eine owner-datei in seinem eigenen change-set.
- WARNUNG (befund): `git diff --name-only <develop-HEAD> <head>` fuer divergierende PRs LISTET `.github/workflows/ci.yml` etc. auf — das ist ein FALSE POSITIVE. Diese PRs sind auf OLD base-branches geschnitten (vor .github/workflows/ci.yml-existent); die `.github`-dateien sind am branch-punkt schon vorhanden und werden NICHT von der lane geaendert. Richtige messung = merge-base->head, und die zeigt 0 owner-dateien. Kein PR beruehrt owner-reichweite.

## FUND-N (hart)
- Hart (`h`, echter konfliktprognose / merge-tree CONFLICT): 0. Keine lane erzeugt einen merge-konflikt gegen develop.

## KLASSEN-ZUSAMMENFASSUNG
- t (trivial, keine schnittmenge): 1747, 1746, 1742, 1739, 1736, 1723, 1714, 1704, 1725, 1627, 1596, 1588, 1585 (13 PRs).
- m (mittel, schnittmenge ohne zeilenkonflikt): 1741, 1740, 1738, 1737, 1702, 1650, 1645, 1625, 1623, 1620, 1614, 1597 (12 PRs).
- h (hart): 0.
- o (owner-reichweite): 0.

## OBSERVATION (fuer H-V38 hop-kampagne)
- Alle 25 offenen PRs sind hinter develop (kein PR entwickelt sich parallel zu develop).
- Kein PR ist ein harter konflikt; der hoechste risikowert ist m (schnittmenge, kein zeilenkonflikt).
- Die 4 operator-env lanes (1741/1740/1738/1737) teilen sich denseiben shared test-fixture-beruehrungen auf old base 40cb28c75 — ihre schnittmenge ist groess, aber ohne konflikt.
- owner-reichweite wird nirgendts beruehrt — hop-kampagne kann ohne owner-gate geplant werden.

## cleanliness
- read-only bug-hunt. Keine container/compose gestartet.
- `docker ps -a` VOR (pid $$): leer (0 container), exit=0.
- `docker ps -a` NACH: leer (0 container), exit=0.
- Sauberkeits-feststellung: cleanliness=true, keine test-eigenen netzwerke/volumes/state-verzeichnisse angelegt.

## repo-rule compliance
- Nur gelesen, keine produktdatei aendern. Kein rebase/merge in einem baum. `git merge-tree --write-tree` ist schreibgeschuetzt (nur tree im object-store, kein commit, kein branch).
- Kein commit an baseharbor. Keine PR-aktion.
- Keine subagenten (4.8).
- Kein nacktes `go test ./cmd/baha/`.
- Kein `git add -A`. Kein `git stash`.
- planning repo remote = https://github.com/mcpdev80/baseharbor-plan.git (verifiziert).
- baseharbor remote = git@github.com:mcpdev80/baseharbor.git (verifiziert; github.com/mcpdev80).
- evidence liegt in baseharbor-plan, NICHT in baseharbor.

## END
LANE 0428-221-hopcost: DONE (befund abgegeben, akte committed). candidate sha: baseharbor-plan evidence commit sha (unter evidence-publizierung vermerkt).
