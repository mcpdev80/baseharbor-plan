# Evidence — Mission gh-acc-suite

**Mission:** Acceptance-Suiten auf GitHub-hosted migrieren (100% GitHub-hosted, KEINE self-hosted Runner)
**Working tree:** `/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/gh-acc-suite` (branch `work/gh-acc-suite`)
**Write-set (exklusiv):**
- `.github/workflows/podman-acceptance.yml`
- `.github/workflows/mcp-lifecycle-acceptance.yml`
- `.github/workflows/observability-acceptance.yml`
**Evidence dir:** `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-10-31/gh-acc-suite/`
**Lane / Codeman session:** `8c0f41e1-21b3-4d3e-9537-ec733a3c2d60`

## PLAN (checklist)

1. Analyse der drei Ziel-Workflows: `runs-on: [self-hosted,...]`-Stellen kartieren, Write-Set gegen Mission verifizieren.
2. `podman-acceptance.yml` (1 Job, podman): `runs-on` -> `ubuntu-latest`, rootless-podman Setup im Job-Setup einfügen.
3. `mcp-lifecycle-acceptance.yml` (docker + podman, 2 Jobs): beide -> `ubuntu-latest`, docker nativ, podman rootless-Setup.
4. `observability-acceptance.yml` (docker + podman, 2 Jobs): beide -> `ubuntu-latest`, docker nativ, podman rootless-Setup.
5. KEIN künstliches PASS/SKIP; Assertions/Tests unverändert; nur Runner + nötiges In-Job-Setup.
6. `scripts/ci-core-rootless-runtime.sh` NICHT selbst ändern (Lane gh-ci-core). Bei Skript-Bedarf als Interface-Bedarf melden.
7. Lokale Validierung: actionlint (Workflow-Syntax), `git diff` gegen Write-Set, Repo-Regelkonformität.
8. Branch pushen; für push/call einen PR oder `gh workflow run --ref <branch>` fahren; Run bis terminal beobachten (Eigenes-Run-Pflicht). runner-status je Workflow dokumentieren.
9. Planning-Abschluss (nur bei gültigem Merge / Owner-Auftrag) + Planning-Publishing.

## repo-rule compliance
- Repo-Regel: AGENTS.md baseharbor + Mission gh-acc-suite. Exklusives Write-Set auf 3 Workflow-Dateien beschränkt.
- `ci-core-rootless-runtime.sh` bleibt unverändert (Interface-Bedarf an Lane gh-ci-core, siehe unten).

## END
<lane> gh-acc-suite: <status> | <candidate SHA>
