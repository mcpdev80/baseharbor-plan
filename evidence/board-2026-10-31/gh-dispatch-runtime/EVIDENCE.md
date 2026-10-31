# EVIDENCE: gh-dispatch-runtime

## Step 0: Plan und Evidence-Verzeichnis erstellt ✓
- Evidence path: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-10-31/gh-dispatch-runtime/
- PLAN.md erstellt

## Step 1: Analyse — runtime-broker.yml
- runs-on: `self-hosted, Linux, X64, baseharbor, docker` → 2 jobs (acceptance, performance)
- Ziel: ubuntu-latest, docker nativ
- Analyse: Workflow ruft `docker` commands direkt auf, erwartet rootless Docker endpoint (`unix:///run/user/1001/docker.sock`)
- Keine `ci-core-rootless-runtime.sh`调用 — war auf self-hosted Runner vorkonfiguriert

## Step 2: Analyse — runtime-s3-acceptance.yml
- runs-on: `self-hosted, Linux, X64, baseharbor, docker` → 1 job
- Ziel: ubuntu-latest, docker nativ
- Analyse: Gleiche Abhängigkeit — `docker` commands, rootless Docker endpoint erwartet

## Step 3: Analyse — docker-runtime-acceptance.yml
- runs-on: `ubuntu-latest` bereits ✅
- Sub-jobs: `ubuntu-24.04` für provider-ha, mcp-edit-native
- Nutzt `scripts/ci-core-rootless-runtime.sh` explizit
- Kein self-hosted

## Step 4: Analyse — targeted-integration.yml
- Dynamic `runs-on: matrix.runtime == 'podman' && 'ubuntu-26.04' || 'ubuntu-latest'`
- Nutzt `ci-core-rootless-runtime.sh`
- Kein self-hosted

## Step 5: Analyse — targeted-demo-acceptance.yml
- runs-on: `ubuntu-latest` / `ubuntu-26.04`
- Kein self-hosted

## Step 6: Migration — runs-on: self-hosted → ubuntu-latest
- runtime-broker.yml: acceptance job → `ubuntu-latest` ✓
- runtime-broker.yml: performance job → `ubuntu-latest` ✓
- runtime-s3-acceptance.yml: runtime-s3 job → `ubuntu-latest` ✓
- Commit: `3735aa3e`
- Branch: `work/gh-dispatch-runtime`
- Pushed to origin

## Step 7: Nachweis — workflow_dispatch Runs

### 7a. runtime-broker.yml (acceptance)
- Run: 41246264824
- Status: **failure**
- Error: `Error: selected Docker endpoint unix:///run/user/1001/docker.sock is unavailable; start its rootless daemon or correct the Target endpoint/context; no fallback to System Docker`
- Ursache: self-hosted Runner hatte rootless Docker vorkonfiguriert; ubuntu-latest hat dies nicht.

### 7b. runtime-s3-acceptance.yml
- Run: 41246264909
- Status: **failure**
- Error: Gleicher rootless Docker endpoint — `unix:///run/user/1001/docker.sock is unavailable`
- Ursache: Wie 7a.

### 7c. docker-runtime-acceptance.yml
- Run: 41246264908
- Status: **in_progress** (75-min timeout, noch nicht terminal)
- Nutzt `scripts/ci-core-rootless-runtime.sh` — dieser Weg ist der korrekte für GH-hosted.

### 7d. targeted-integration.yml
- Run: 41246265123
- Status: **success**
- Gate: `app-backup-restore`
- Läuft auf ubuntu-latest, rootless Docker setup via Skript.

### 7e. targeted-demo-acceptance.yml
- Run: 41246264910
- Status: **failure**
- Ursache: `demo_ref=work/gh-dispatch-runtime` — kein 40-char hex SHA, kein gültiger demo-Ref.
- **Kein Runner-Problem** — workflow_dispatch input issue.

## Step 8: rootless-Interface-Bedarf

**Kritischer Befund:** Die zwei workflows, die bisher ausschließlich auf self-hosted liefen (runtime-broker, runtime-s3-acceptance), setzen `docker` Kommands ohne `ci-core-rootless-runtime.sh` voraus. Der self-hosted Runner hatte das rootless Docker Daemon vorkonfiguriert (`unix:///run/user/1001/docker.sock`).

**Interface-Bedarf an gh-ci-core-Lane:**
- Die Broker- und S3-Acceptance-Workflows brauchen einen `ci-core-rootless-runtime.sh` Aufruf oder äquivalente rootless Docker Setup-Schritte auf ubuntu-latest.
- Alternativ: Die Skripte im broker workflow müssen das system docker Socket erkennen und adaptieren.
- **Keine** Änderung am Skript selbst (gh-ci-core besitzt es). Nur `runs-on` migrieren — aber das Skript hat auf ubuntu-latest ein anderes Interface-Bedarf: rootless Docker muss explizit provisioniert werden.

## Step 9: END post
- candidate SHA: `3735aa3e`
- END_BLOCKED gh-dispatch-runtime: 3735aa3e run_ids=[41246264824(fail,rootless-docker),41246264909(fail,rootless-docker),41246264908(in_progress,docker-runtime),41246265123(success,integration),41246264910(fail,demo-ref-input)] runner-status=[runtime-broker:FAIL, runtime-s3:FAIL, docker-runtime:IN_PROGRESS, targeted-integration:SUCCESS, targeted-demo:FAIL] rootless-interface: broker+s3 workflows need ci-core-rootless-runtime.sh on ubuntu-latest — self-hosted had pre-configured rootless daemon
- END_BLOCKED

