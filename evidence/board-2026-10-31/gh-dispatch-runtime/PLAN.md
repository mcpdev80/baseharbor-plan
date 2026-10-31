# PLAN: gh-dispatch-runtime

## Step 0: Plan und Evidence-Verzeichnis erstellt ✓

## Step 1: YAML-Workflows analysieren
- File: `.github/workflows/runtime-broker.yml` (self-hosted docker ~Z27,~Z233)
- File: `.github/workflows/runtime-s3-acceptance.yml` (self-hosted docker ~Z15)
- File: `.github/workflows/docker-runtime-acceptance.yml` (uses ci-core-rootless-runtime.sh)
- File: `.github/workflows/targeted-integration.yml` (uses rootless-skript)
- File: `.github/workflows/targeted-demo-acceptance.yml` (uses rootless-skript)

## Step 2: runs-on: self-hosted → ubuntu-latest migrieren
- docker nativ auf GH-hosted ausführen
- Skripte aus gh-ci-core-Lane NICHT ändern

## Step 3: workflow_dispatch-Jobs nachweisen
- `gh workflow run <file> -R mcpdev80/baseharbor --ref <branch>` bis terminal
- Eigenes-Run-Pflicht: Run-ID, Status, Fehlerzeilen dokumentieren

## Step 4: Self-hosted-Abhängigkeiten entfernen
- Erst nach grünem GH-hosted-Ersatz

## Step 5: END post
- SHA + Run-IDs + Runner-Status je Workflow + rootless-Interface-Bedarf
