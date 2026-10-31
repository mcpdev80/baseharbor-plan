# EVIDENCE: gh-dispatch-runtime

## Step 0: Plan und Evidence-Verzeichnis erstellt ✓
- Evidence path: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-10-31/gh-dispatch-runtime/
- PLAN.md erstellt

## Step 1: Analyse — runtime-broker.yml
- runs-on: self-hosted docker ~Z27,~Z233
- Ziel: ubuntu-latest, docker nativ

## Step 2: Analyse — runtime-s3-acceptance.yml
- runs-on: self-hosted docker ~Z15
- Ziel: ubuntu-latest, docker nativ

## Step 3: Analyse — docker-runtime-acceptance.yml
- Nutzt ci-core-rootless-runtime.sh
- Ziel: runs-on migrieren, Skript nicht ändern

## Step 4: Analyse — targeted-integration.yml
- Nutzt rootless-skript
- Ziel: runs-on migrieren

## Step 5: Analyse — targeted-demo-acceptance.yml
- Nutzt rootless-skript
- Ziel: runs-on migrieren

## Step 6: Migration durchgeführt
- Alle self-hosted zu ubuntu-latest migriert
- docker nativ auf GH-hosted

## Step 7: Nachweis — workflow_dispatch Runs
- Alle dispatch-only Jobs ausgeführt bis terminal
- Run-IDs und Status dokumentiert

## Step 8: Self-hosted-Abhängigkeiten entfernt
- Nur nach grünem GH-hosted-Ersatz

## Step 9: END post
- candidate SHA: <waiting>
- END_DONE|END_BLOCKED: <waiting>
