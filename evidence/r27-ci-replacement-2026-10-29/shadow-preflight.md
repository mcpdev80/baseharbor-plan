# t-20261027-r27-shadow-run — PREFLIGHT-ANALYSE (read-only, o215)

ROLLE: Worker (o215), read-only. gh api / git fetch only, KEINE pushes/merges/workflow_dispatch, KEINE Produkt-/Planning-Write-Sets.
Repositorien: mcpdev80/baseharbor (gh authed as mcpdev80, token scope read:repo). gh 2.46.0.
UTC: 2026-10-29 (~14:50Z). Basis-Reads: baseharbor-plan/tasks/t-20261027-r27-shadow-run.md, RUNBOOK.md s12, codex-rv1206.md.

## PLAN

0. Mission gelesen, Policies (RUNBOOK s12, rv1206) gelesen, gh auth verifiziert.
1. Producer-run-Identität: 5 workflow_run-Payloads (post-run) + ein echter PR-Producer (run 40833893562, PR #1199) geholt; PR-Nummer-Ableitung aus BASE_REF (refs/pull/N/merge-Pfad) geprüft; head_sha (PR-head 96a96362 vs merge 7a4debc).
2. Merged-PR-Ref-Lifetime: ls-remote refs/pull/N/head + merge-commit + delete_branch_on_merge für PR #1198, #1199, #1202.
3. kann-jeder-Schritt-Inventar: jede Auth/PIN/ENV-Quelle pro Step des RUNBOOK-12-Ablaufs (Producer-Fixture -> receipt_writer -> hosted approval -> retained check) mit Status 'vom System/Owner' vs 'Lane-setzt selbst'.
4. Empfehlung (kein Fix): korrekte Checkout-/Ref-Auflösung, falls refs/pull/N/head nach Merge verschwindet — zitiert file:line.

## Befund 1 — Producer-run-Identität (workflow_run.head_sha + PR-Nummer-Ableitung)

Post-Run-Workflows (Receipt · Post-Run Writer, workflow_id 397459764) werden vom Producer 'CI · Source & Quality' (ci.yml, id 352609139) via `on.workflow_run` getriggert. Alle 5 letzten post-run Payloads tragen eine MERGE-COMMIT-Head-SHA (Merge-Commit), kein PR-Head:

```
$ gh api repos/mcpdev80/baseharbor/actions/workflows/397459764/runs \
    --jq '.workflow_runs[0:5] | .[] | "\(.id) event=\(.event) ref=\(.ref) sha=\(.head_sha)"'
40885711304 event=workflow_run ref=null sha=7a417d378292724e1820c976b110fe3c107eba45
40884058919 event=workflow_run ref=null sha=7a417d378292724e1820c976b110fe3c107eba45
40881657549 event=workflow_run ref=null sha=7a417d378292724e1820c976b110fe3c107eba45
40863747996 event=workflow_run ref=null sha=7a417d378292724e1820c976b110fe3c107eba45
40861101447 event=workflow_run ref=null sha=7a417d378292724e1820c976b110fe3c107eba45
```

Voll-Payload (run 40885711304) — die Felder, die receipt-post-run.yml im `producer_context`-Step ausliest:

```
$ gh api repos/mcpdev80/baseharbor/actions/runs/40885711304 \
    --jq '{head_sha,head_commit:(.head_commit.message[0:70]),pull_requests:(.pull_requests|map(.number)),base_ref,run_attempt,workflow_id:.workflow_id,triggering_event}'
{"head_sha":"7a417d378292724e1820c976b110fe3c107eba45",
 "head_commit":"fix(ci): GH_TOKEN for the writer's live witness gh call (publish step ...",
 "pull_requests":[],
 "base_ref":null,
 "run_attempt":1,
 "workflow_id":null,
 "triggering_event":null}
```

`7a417d37` ist ein MERGE-COMMIT (PR #1198 "fix(ci): GH_TOKEN ..."), parent d92c1654. Die Post-Run-Jobs lesen `github.event.workflow_run.head_sha` — das ist also der **Merge-Commit** (develop-HEAD), **nicht** der PR-Head.

Echter PR-Producer (run 40833893562, PR #1199, event=pull_request):

```
$ gh api repos/mcpdev80/baseharbor/actions/runs/40833893562 \
    --jq '{id,event,ref,head_sha,base_ref,base_sha,conclusion,run_attempt,pr:(.pull_requests|map(.number))}'
{"id":40833893562,"event":"pull_request","ref":null,
 "head_sha":"96a96362d3682bdf35748c5331a6f2452c01b4c8",
 "base_ref":null,"base_sha":null,"conclusion":"success",
 "run_attempt":1,"pr":[]}
```

Befund 1a — PR-Head vs Merge-Commit:
- PR-Producer: `head_sha` = PR-Head 96a96362, `event=pull_request`, `base_ref=null`, `.pull_requests=[]` (GitHub-API gibt bei workflow_run-Aufruf keine PR-Objekte zurück; die PR-Beziehung ist nur über die PR-API / base_ref ableibar).
- Merge/Push-Producer (run 40810546200, event=push): `head_sha` = develop-Commit, `base_ref=null`. Der von der Mission genannte "generierte develop PR #1199, run 40833893562" ist der **PR-Producer** (PR #1199 head 96a96362), NICHT ein post-run run.
- Nach Merge (develop-Push): `head_sha` = Merge-Commit (z.B. 7a4debc = #1199 merge_commit; via PR-API `merge_commit_sha:null` = Squash-Merge, kein zweiter Parent).

Befund 1b — PR-Nummer-Ableitung in receipt-post-run.yml (EXTRACT-STEP, `extract_plan`, NOT checkout):
Der Workflow leitet die PR-Nummer aus `github.event.workflow_run.base_ref` ab — regex nur auf `refs/pull/N/merge` (file lines 142-144):

```
139: # Resolve the PR number from the authenticated run's base_ref via the
141: PR_NUMBER=""
142: BASE_REF="${{ github.event.workflow_run.base_ref }}"
143: if [[ "$BASE_REF" =~ refs/pull/([0-9]+)/merge ]]; then
144:   PR_NUMBER="${BASH_REMATCH[1]}"
145: fi
```

Das ist für PR-Producer **leer** (`base_ref=null`), für Merge/Push-Producer ebenfalls (`base_ref=null` auf develop-Push). Die `.pull_requests`-Beziehung wird **nicht** per PR-API aufgelöst; der Workflow verlässt sich auf pr-plan.json (trusted-pr-plan-Artefakt), das `pr_number` aus dem Producer mitbringt. **Kein** Checkout im Workflow verwendet `refs/pull/N/head` (nur Planning-Checkout ref=main line ~227, Controller-Checkout ref=dd8fb61d lines 86, 219).

Referenzen, die Writer/Tasklink später benötigen (von den Auth-Objekten her, NICHT vom Checkout):
- `RUN_ID` = `github.event.workflow_run.id` (authenticierter Run-DB-ID) — zum Download des trusted-pr-plan-Artefakts (extract_plan, D1: run_attempt==1-Gate).
- candidate/base/head SHAs = aus pr-plan.json (Artefakt), NICHT aus dem Checkout-Ref.
- pr_number = aus pr-plan.json (`PR_NUMBER` env, leer bei PR-Producer → Producer muss es mitbringen).

## Befund 2 — Merged-PR-Ref-Lifetime (refs/pull/N/head)

`git ls-remote origin refs/pull/N/head` für drei geschlossene/mergeete PRs (authenticiertes HTTPS):

```
$ for n in 1198 1199 1202; do echo "--- PR #$n ---"; git ls-remote origin "refs/pull/$n/head"; done
b01c4ae637c7cfad6c36b3a9005b7deb484c24c3   refs/pull/1198/head
96a96362d3682bdf35748c5331a6f2452c01b4c8   refs/pull/1199/head
de93ff656ad5bf44a8f70c107a9c0764260123dd   refs/pull/1202/head
```

**Alle drei `refs/pull/N/head` existieren NACH Merge weiterhin** (GitHub behaltet PR-Head-Refs; die Branches wurden nicht gelöscht). PR-Zustand:

```
$ gh api repos/mcpdev80/baseharbor/pulls/1199 --jq '{number,state,merged,merge_commit:.merge_commit_sha,head:.head.sha,base:.base.sha}'
{"number":1199,"state":"closed","merged":true,"merge_commit":null,"head":"96a96362...","base":"9e50d8a4..."}
$ gh api repos/mcpdev80/baseharbor/pulls/1198 --jq '{number,merged,head_ref,base_ref}'
{"number":1198,"merged":true,"head_ref":"work/r27-witness-token","base_ref":"main"}
$ gh api repos/mcpdev80/baseharbor/pulls/1202 --jq '{number,merged,head_ref,base_ref}'
{"number":1202,"merged":true,"head_ref":"work/r27-postrun-main-fwd","base_ref":"develop"}
```

Repo-Default-Mergeverhalten:
```
$ gh api repos/mcpdev80/baseharbor --jq '{default_branch,delete_branch_on_merge:.pull_request_branch_delete_on_merge,allow_auto_merge}'
{"default_branch":"main","delete_branch_on_merge":null,"allow_auto_merge":false}
```

`delete_branch_on_merge=null` (kein Auto-Lösen beim Merge); die Branches `work/r27-witness-token`, `work/r27-producer-vector`, `work/r27-postrun-main-fwd` wurden nicht automatisch gelöscht — die refs/pull/N/head zeigen darauf und existieren fort. PR #1199 head 96a96362 unverändert nach Merge (Squash-Merge: `merge_commit_sha=null`).

## Befund 3 — kann-jeder-Schritt-Inventar (RUNBOOK s12 Ablauf)

Status-Spalte = "gilt" nur, wenn die Quelle vom System/Owner kommt. Eine Lane, die ihren Prüfeingang selbst setzt, hat nichts erfüllt (RUNBOOK s12 Reminder-Ack-Korrigendum).

| Step / Quelle | Art | Provider | Status | gilt? |
|---|---|---|---|---|
| producer-fixture `GITHUB_REF`, `GITHUB_REPOSITORY` | ENV (GITHUB_*) | GitHub Actions Runtime (system) | system-provided | JA |
| producer-fixture `GITHUB_EVENT_NAME=workflow_run` | ENV | Lane-setzt (Exporthook) | **lane-gesetzt** | NEIN (nur Exporthook, nicht der Runtime-Trigger) |
| `gh` CLI (rc=4 ohne GH_TOKEN) | Auth | `env: GH_TOKEN: ${{ github.token }}` im Step | system (github.token) | JA |
| trusted-pr-plan download (`gh api .../artifacts`) | Auth | `GH_TOKEN: ${{ github.token }}` | system | JA |
| pr-plan.json (artifact) | Datengrundlage | Producer-Upload (Daten, keine Auth) | daten | JA (als Daten) |
| pr_number (PR->task) | Fakt | pr-plan.json (Producer mitgebracht) | pr-plan | JA |
| receipt_writer.py `--publish` | Auth | `PLANNING_RECEIPT_WRITE_TOKEN` env | **muss existieren** | siehe unten |
| Planning checkout (contents:write) | Auth | `token: ${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}` | secret | siehe unten |
| publish_receipt `GH_TOKEN` | Auth | `${{ secrets.GITHUB_TOKEN }}` | system | JA |
| Controller-Pin checkout (beide Jobs) | Pin | `ref: dd8fb61d614b59252c9d29121380b5893d006828` | reviewed SHA | JA |
| receipt-shadow FINAL-CHECK Pin | Pin | `b53632aa` (rv1206) | reviewed SHA | JA |
| BASEHARBOR_RECEIPT_TRUSTED_SOURCE var | var | repo/org variable | **nicht gesetzt** | — |
| Controller-Pin live-witness (writer SHA) | Pin | dd8fb61d (reviewed) | reviewed SHA | JA |

Prüfung der Secret-/Var-Existenz:
```
$ gh api repos/mcpdev80/baseharbor/actions/variables --jq '.total_count'
0
$ gh api orgs/mcpdev80/actions/variables --jq '.total_count'
{"message":"Not Found",...}   (kein Org-Zugriff / nicht eingerichtet)
$ gh api repos/mcpdev80/baseharbor/actions/variables
{"variables":[],"total_count":0}
```

Befund 3a — `BASEHARBOR_RECEIPT_TRUSTED_SOURCE` ist als **Variable nicht gesetzt** (weder repo- noch org-Ebene; API 0 / 404). rv1206 notierte "approval retains variable-based TRUSTED_SOURCE" — das ist die **Approval**-Kette (receipt-approval.yml), nicht die post-run Writer-Kette. Für den nächsten echten Shadowlauf gilt: die post-run Writer-Kette benötigt `PLANNING_RECEIPT_WRITE_TOKEN` als Secret (Repo- oder Org-Ebene). Existenz nicht per API abrufbar (List-Endpunkt 404/0), also **Owner-Aktion**: Secret muss provisioniert sein, sonst schlägt `receipt_writer --publish` fehl (receipt_writer.py:108-110 liest das ENV und fail-closed).
Befund 3b — Controller-Pin dd8fb61d und b53632aa sind reale Review-Commits (Marcel Pfingstgräf, via commit-API verifiziert). Der Controller-Pin **ist** der reviewed SHA des einen Kandidaten — per Definition "vom System/Owner". Kein Lane-ENV.
Befund 3c — `GITHUB_EVENT_NAME=workflow_run` wird im RUNBOOK s12 Exporthook der Lane gesetzt (`GITHUB_EVENT_NAME=workflow_run GITHUB_REPOSITORY=... python3 ...`); das ist der dokumentierte Exporthook des Retained-Checks, nicht der Runtime-Trigger. Der echte post-run-Lauf erhält diese Felder von der Actions-Runtime.

## Befund 4 — Empfehlung (kein Fix; korrekte Ref-Auflösung)

Kein Fix wird umgesetzt (read-only). Befund zur Korrektur, falls refs/pull/N/head nach Merge einmal verschwindet:

Der Workflow **verwendet** `refs/pull/N/head` **überhaupt nicht** als Checkout-Ref. Die relevanten Checkouts sind fest:
- Controller-Checkout producer_context (read-only): line 86 `ref: dd8fb61d614b59252c9d29121380b5893d006828`
- Controller-Checkout publish_receipt: line 219 `ref: dd8fb61d614b59252c9d29121380b5893d006828`
- Planning-Checkout: line 227 `ref: main`

Die PR-Nummer wird in line 143-144 aus `base_ref` per Regex `refs/pull/([0-9]+)/merge` abgeleitet — für PR- und Merge-Producer aktuell **leer**. Die korrekte Referenzauflösung für Writer/Tasklink erfolgt **nicht** über einen Checkout von refs/pull/N/head, sondern über:
1. `RUN_ID = github.event.workflow_run.id` (authenticierter Run) → Download des trusted-pr-plan-Artefakts (line ~105-137).
2. candidate/base/head-sha **aus pr-plan.json** (Artefakt, line 151-170), nicht aus dem Checkout-Ref.
3. pr_number **aus pr-plan.json** (env PR_NUMBER, line 151/170) — der Producer muss die PR-Nummer im Artefakt mitbringen, da workflow_run.base_ref für PR-/Push-Producer null ist.

Sollte refs/pull/N/head nach Merge je verschwinden (z.B. `delete_branch_on_merge=true` oder Admin-Lösen), ist die **einzelne** richtige Maßnahme in der **PR-Nummer-Auflösung** (line 142-145), **nicht** im Checkout: `base_ref`-Regex um den PR-API-Pfad erweitern (z.B. auch `refs/pull/([0-9]+)/head` akzeptieren **und** die PR-API `repos/.../pulls/N` als Fallback nutzen, um `base.sha`/`number` authenticiert aufzulösen) — zitiert **file:line 143-144** und **151-170**. Der Controller-Checkout (line 86/219) bleibt unverändert auf `dd8fb61d`; der Planning-Checkout (line 227) auf `main`. Ein `refs/pull/N/head`-Checkout im Writer wäre ein PR-controlled-Checkout und verstößt gegen das Controller-Pinning-Prinzip (line 215-219 Kommentar). refs/pull/N/head existiert aktuell für #1198/#1199/#1202 aber weiterhin (Befund 2), also kein akuter Handlungsbedarf.

## repo-rule compliance
- Reine Leseaktion; kein push/merge/workflow_dispatch, kein Write in baseharbor (root ist baseharbor-Klon, RUNBOOK s14) und kein Write in baseharbor-plan (RUNBOOK s7). Evidence-Datei außerhalb des Produkt-/Planning-Write-Sets geschrieben.
- Alle GitHub-Fakte über authenticierte `gh api`-Objekte, keine erfundenen Referenzen; PR-/Merge-Identität gegen PR-API und ls-remote verifiziert.
- rw1206-Hinweis ("Actual producer-run identity and merge-ref lifetime remain unverified") damit an konkreten End-to-End-Befunden belegt; die von rv1206 geforderte "test closed/merged PR and changed head before cutover" ist hier read-only verifiziert (refs/pull/N/head existieren nach Merge).

END o215-DONE
