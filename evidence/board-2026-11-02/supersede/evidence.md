# supersede — Parkdeck-Tabelle (Coord-Analyse, read-only, 2026-11-02)

## PLAN
  - Dateien-Listen aller 7 PRs vs #1258-Schreibset + develop
  - Baum-Vergleiche pro Datei (head-vs-1258, head-vs-develop)
  - Empfehlung je PR
  - Nach #1258-Merge: finale Einzel-Probe 'git diff <pr-head> develop' -> Close-Nachweis

## Tabelle (Stand 735acd95 / develop 9a93865a)

| PR | Dateien (Kern) | Befund | Empfehlung |
|----|----------------|--------|------------|
| #1244 | ci.yml, scripts/ci-podman-gh-runtime.sh | Baum-inhalte == #1258-Kopf; develop-Zeilenvergleich 0; ein Hunk-Wurzel-Podman-Skript in develop noch NICHT nachweisbar | BLOCKED-BIS-1258, danach SUPERSEDED-Prüfung |
| #1239 | ci.yml, nextjs-e2e.yml, rootless-skript, py-test | alle Dateien == #1258-Fassungen | SUPERSEDED-vorbehaltlich-1258 |
| #1238 | 3 Akzeptanz-Workflows | == #1258 | SUPERSEDED-vorbehaltlich-1258 |
| #1247 | 3 Workflows + Podman-Skript | == #1258 | SUPERSEDED-vorbehaltlich-1258 |
| #1248 | ci.yml, pr-check-runner.py, gate-plan, test | == #1258 (gate-plan-Bindung anderswo nachgezogen) | SUPERSEDED-vorbehaltlich-1258 |
| #1249 | ci.yml | == #1258 | SUPERSEDED-vorbehaltlich-1258 |
| #1257 | targeted-integration.yml | == #1258-Fassung; eigener Probe-Lauf NOT WENDEL — Inhalt kommt mit #1258 in develop | nach #1258: SUPERSEDED, kein separater Merge |
| #1243 | broker+s3 Workflows | == #1258 (2 Dateien) | SUPERSEDED bei #1258-Merge |

## Entscheidungsregel nach #1258-Merge
git diff <pr-head> origin/develop -- <jede PR-Datei>: leer => Close 'superseded by #1258' mit Diff-Null-Nachweis;
nicht leer => Rest-Wert prüfen (rebase+nativ ODER totes-Eis mit Begründung).
