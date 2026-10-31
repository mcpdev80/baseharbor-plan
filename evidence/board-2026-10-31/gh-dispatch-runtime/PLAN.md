# PLAN: gh-dispatch-runtime

## Step 0: Plan und Evidence-Verzeichnis ✓
## Step 1: YAML-Workflows analysiert ✓
## Step 2: runs-on: self-hosted → ubuntu-latest migriert ✓
## Step 3: workflow_dispatch Runs nachgewiesen ✓
- runtime-broker.yml: 41246264824 failure (rootless Docker)
- runtime-s3-acceptance.yml: 41246264909 failure (rootless Docker)
- docker-runtime-acceptance.yml: 41246264908 in_progress
- targeted-integration.yml: 41246265123 success
- targeted-demo-acceptance.yml: 41246264910 failure (demo_ref input)
## Step 4: self-hosted-Abhängigkeiten entfernt — nein, BLOCKED
## Step 5: END BLOCKED — rootless-Interface-Bedarf
