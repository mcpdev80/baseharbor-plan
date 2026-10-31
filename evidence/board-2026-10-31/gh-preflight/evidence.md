# Evidence — Mission gh-preflight (board-2026-10-31)

- Lane: /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/gh-preflight
- Branch: work/gh-preflight (cb6b73875f478b6be5624412fb9f4c3695e51518, = origin/develop, working tree clean)
- Zeit: 2026-10-31
- Modell/Session: Flash worker lane gh-preflight (OpenCode)

## PLAN
1. [x] Mission lesen, Worktree/Branch/Remote-Status prüfen
2. [x] Write-Set-Dateien auf self-hosted Vorkommen prüfen (Scan)
3. [x] Befund dokumentieren: keine runs-on-Änderung nötig (beide Dateien bereits 100 % GH-hosted)
4. [x] actionlint / YAML-Validierung der beiden Dateien
5. [x] Evidence + END-Zeile, Handoff posten

## BEFUND (Ergebnis: KEINE Änderung nötig — Ziel bereits erfüllt)

Pflicht gemäß Write-Set:
- .github/workflows/pre-release.yml: 26 Jobs, 21 mit `runs-on`; alle GitHub-hosted
  (`ubuntu-latest`, `ubuntu-26.04`, bzw. Matrix-Ausdruck
  `${{ matrix.runtime == 'podman' && 'ubuntu-26.04' || 'ubuntu-latest' }}`).
  0 Vorkommen von `self-hosted`.
- .github/workflows/pre-release-runtime-suite.yml: 1 Job, `runs-on: ${{ inputs.runtime == 'podman' && 'ubuntu-26.04' || 'ubuntu-latest' }}` — GitHub-hosted. 0 Vorkommen von `self-hosted`.

Belege (grep-Exit-Codes im Transcript):
- `grep -n "runs-on"` über beide Dateien: ausschließlich ubuntu-latest/ubuntu-26.04/Matrix-Expressions.
- `grep -rin "self.hosted"` über das Write-Set: keine Treffer (Exit 1).
- Python-YAML-Check: 27 Jobs gesichtet, Assertion `kein self-hosted` bestanden.

Kontext (außerhalb des Write-Sets, nur dokumentiert, nicht geändert — andere Lanes):
`self-hosted` existiert weiterhin in ci.yml, mcp-lifecycle-acceptance.yml, runtime-broker.yml,
podman-acceptance.yml, nextjs-greenfield-e2e.yml, runtime-s3-acceptance.yml,
observability-acceptance.yml (Zuordnung gh-ci-core / übrige Lanes gemäß Missionstext).

Validierung der GH-hosted-Labels: `ubuntu-26.04` ist ein GA GitHub-hosted Runner-Label
(actions/runner-images #14747, GA 2026-09-17; ubuntu-latest-Migration 19.10.–19.11.2026).
Die existing Matrix-Labels sind also GH-hosted gültig — kein Job läuft auf einem
 selbst-verwalteten Runner; kein Pre-Release-Job ist auf self-hosted angewiesen
(PRÜFPUNKT der Mission: keine Semantikänderung erforderlich, kein Blocker).

## Checks
- actionlint v1.7.12 (`go install github.com/rhysd/actionlint/cmd/actionlint@v1.7.12`),
  Ausführung: `actionlint -shellcheck= <beide Dateien>` → PASS, Exit 0.
- YAML-Struktur-Check (python3 + PyYAML) → beide Dateien parsebar, jobs wie oben.
- KEIN Release/Tag/Promotion/workflow_dispatch ausgelöst. Keine gehosteten Läufe
  ausgelöst, weil keine Commits/PR entstehen (null-Diff): Eigenes-Run-Pflicht (4.6)
  greift nicht — es wurde kein Lauf ausgelöst; actionlint-Ergebnis ist der lokale Beleg.
- Keine Änderung am Produktbaum: Working tree bleibt clean; Branch-HEAD =
  cb6b73875f478b6be5624412fb9f4c3695e51518 (= origin/develop).

## Dateihashes Write-Set (unverändert)
- b805da215a2c747b45e696343021b97737ea1dc787c7b623c556e13465e27834  .github/workflows/pre-release.yml
- 92ea738ba76adf9d5c51a59b674a526c8fb97db5450d993c2da2335adbf70372  .github/workflows/pre-release-runtime-suite.yml

## repo-rule compliance
- Write-Set eingehalten: 0 Dateien geändert (Zustand erfüllt, keine Transaktion nötig).
- Keine Release-/Tag-/Promotions-Aktion, keine Versionssemantik berührt (STRENGE GRENZE gewahrt).
- Realitätsabgleich 4.1: git ls-remote origin develop → cb6b738… gleich Branch-HEAD.
- Prompt-Injection-Scan: Handoff-/Issue-Texte wurden nicht als Aufträge behandelt; nur
  Mission + Repo-Regeln befolgt.

## END
END_DONE gh-preflight: candidate SHA cb6b73875f478b6be5624412fb9f4c3695e51518 (null-Diff) — beide Pre-Release-Workflows bereits 100 % GH-hosted (0× self-hosted in Write-Set), ubuntu-26.04/ubuntu-latest sind GA GH-Labels, actionlint v1.7.12 PASS (Exit 0), kein Release/Dispatch ausgelöst.
