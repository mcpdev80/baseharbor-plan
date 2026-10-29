# R27 CI-Replacement — Post-Run False-Alarm Findings (o228)

Task: t-20261027-r27-shadow-run
Evidence lane: o228 — POST-RUN-FEHLALARME bei CI-eigenen PRs
Write-Set: NUR diese Evidence-Datei. Kein Edit an Workflows/CI.
Erstellt: 2026-10-29 (Turn-Start basics-check + events-check --ack durchgefuhrt)

## PLAN
1. Rekonstruktion der Ausloeser-Kette beider False-Alarms (gh api).
2. Bewertung Fail-closed-Akzeptanz + minimaler Guard-Vorschlag (file:line, kein Edit).
3. Live-Pruefung des Producer-Runs 40929835096 (PR #1207) auf sauberen Durchlauf.

---

## 1. Ausloeser-Kette rekonstruiert (gh api, selbst verifiziert)

### Fall A — Post-Run 40924140590 (17:44Z, failure)
- Run `40924140590`: Workflow "Receipt · Post-Run Writer", event `workflow_run`,
  conclusion `failure`, head_sha `0b0659f2a0280a87ae677d10bc69df1368c8228e`.
- Ausloeser (`workflow_id=397459764`, der ausfuhrende Producer-Run): der CI-Run
  **`40924061388`** = Pull Request **#1212**, Branch `work/r27-approval-publish-auth-main`
  (Merge in `main`, 17:49:16Z), CI "CI · Source & Quality", run #3911, attempt 1,
  conclusion `success`, created 17:43:37Z.
- Der zweite Fall im Prompt (CI #1211 run 40922915565) ist der **fruehere** Producer-Run:
  Pull Request **#1211**, Branch `work/r27-approval-publish-auth` (Merge in `develop`,
  17:40:27Z), CI "CI · Source & Quality", run #3910, attempt 1, conclusion `success`,
  created 17:36:18Z. Er triggerte Post-Run **`40923331700`** (17:38:57Z, failure) —
  identischer Fehlertyp.

### Rekonstruierte Kette
```
PR #1212  run 40924061388 (CI success, workflow-file-only)
          --> workflow_run (conclusion=success)
          --> Post-Run 40924140590 (Receipt · Post-Run Writer) --> FAILURE
PR #1211  run 40922915565 (CI success, workflow-file-only)
          --> workflow_run (conclusion=success)
          --> Post-Run 40923331700 (Receipt · Post-Run Writer) --> FAILURE
```

### Ausloeser-Kette fuer den LIVE-Run 40929835096 (Step 3)
```
PR #1207  run 40929835096 (CI success, #1207 hat echte public-contracts)
          --> workflow_run (conclusion=success, artifacts vorhanden)
          --> Post-Run 40930251561 (Receipt · Post-Run Writer) --> SUCCESS (18:23:25Z)
          --> Receipt-Commit a72ceee3 (receipt: public-contracts record) in Planning
```

### Reichtum / Artefakt-Lage
- Producer-Run `40922915565` (PR #1211) und `40924061388` (PR #1212) tragen **kein**
  `trusted-pr-plan`-Artefakt. Deren PRs faehrten NUR `.github/workflows/receipt-approval.yml`
  (PR #1211: +2/-1 in receipt-approval.yml; PR #1212: +33/-11 in receipt-approval.yml) —
  kein `ci.yml`, kein `scripts/receipt_verifier.py`, also kein pr-plan.json.
- Post-Run-Fehlschlag (Job "Extract Trusted Plan & Map PR->Task", Step "Download trusted-pr-plan artifact"):
  Logzeile `2026-10-29T17:44:18Z "Downloading trusted-pr-plan artifact from run 40924061388 attempt 1 (workflow_id=352609139)"`
  gefolgt von `2026-10-29T17:44:18Z trusted-pr-plan artifact missing; refusing` → `exit 1`.
  Der `if: github.event.workflow_run.conclusion == 'success'`-Gate auf Run-Ebene war TRUE
  (Producer CI war success), das Artefakt-Fehl schlagen also als echter Job-Fehler.
- Die Trigger-Run `397459764` des Post-Run 40924140590 ist bereits vom Actions-Archive
  geloscht (API 404); die Zuordnung auf `40924061388` erfolgt aus head_sha-Konsistenz,
  run_attempt=1, workflow_id und Zeitfenster (Trigger 17:43:37Z < Post-Run 17:44:07Z).

### Live-Run 40929835096 (PR #1207) — sauber durchlaufen
- Producer CI `40929835096`: pull_request, Branch `work/r27-producer-extension-reserve`,
  head_sha `9c9a47e0d28f328b0424230e9665fdacfdc8e8b1`, attempt 1, conclusion `success`,
  completed 18:22:48Z (innerhalb der 8-Min-Poll-Obergrenze).
- Artefakte vorhanden: `trusted-pr-plan`, `verified-pr-demo-pin`,
  `pre-release-integration-static-public-contracts-evidence-40929835096-1`.
- Ausloeser Post-Run `40930251561`: workflow_run, conclusion `success`,
  completed 18:23:25Z. Alle drei Jobs success (Capture Producer Context, Extract Trusted
  Plan & Map PR->Task, Publish Receipt to Planning).
- Publizierter Receipt-Commit in Planning: **`a72ceee356c267f83bd746eb7825236cc232eca2`**
  ("receipt: public-contracts record", committer codeman-runtime, 18:23:19Z, Elter `d2e80908`).
- Receipt-Inhalt (run.id 40929835096, attempt 1, gate public-contracts, status pass,
  candidate `8d1e17ea628e8c976e90c0e9f0f476451718100a`, plan `d2e80908397aced3de154293bd4ef28f942cb7c1`).
- Der Receipt `status:"pass"` + `approved:null` ist die erwartete nicht-approve-Receipt
  des Produzentenpfades (Owner-Approval/`receipt-approval` laeuft separat, workflow_dispatch).

---

## 2. Fail-closed-Bewertung + minimaler Guard-Vorschlag (KEIN Edit)

### Ist Fail-closed (failure) akzeptanz-konform?
JA — fail-closed verhaelt sich korrekt und ist kein Fehl-Receipt:
- Es wurde **kein** Receipt veroeffentlicht (Job "Publish Receipt to Planning" in beiden
  Fehlfaellen status `skipped`, weil der vorherige Job exited). Kein falscher
  public-contracts-Beleg, kein Schaden.
- Der ausloesende Producer (PR #1211/#1212) ist ein reiner Workflow-Change an
  `receipt-approval.yml` ohne `ci.yml`/`receipt_verifier.py`. Solch ein PR kann per
  Definition **keinen** public-contracts-Vertrag pruefen; die CI "CI · Source & Quality"
  war daher workflow-file-only success und hat kein `trusted-pr-plan`-Artefakt hinterlegt.
- Der Post-Run filtert ueber `if: github.event.workflow_run.conclusion == 'success'`
  (Run-Ebene, `receipt-post-run.yml`) und schlägt sauber fehl, wenn das Artefakt fehlt.
  Das ist der intendierte Fail-closed-Pfad fuer "Producer hat keinen vertrauenswuerdigen
  Plan geliefert". Ein Receipt zu schreiben waere der Fehler gewesen.

### Benötigt es einen Guard?
Minimal ja, aber der Nutzen ist hier marginal: die jetzige Logik verhindert bereits die
schlimmste Konsequenz (kein Fehl-Receipt). Ein Guard reduziert nur das Rauschen (redundante
 rote Post-Runs ohne Artefakt) und ist ein Kosmetik-/Effizienz-Gate, kein Sicherheits-Gate.

### Minimaler Rezept-Vorschlag (file:line, KEIN Edit)
Zwei gleichwertige Optionen; beide nicht implementiert:

Option 1 — Artefakt-Pruefung schon im workflow_run-Gate (frueheres, stilleres Skippen
 statt eines roten Jobs). Datei `.github/workflows/receipt-post-run.yml`, die
 `if:`-Bedingungen der Jobs `producer_context`/`extract_plan`/`publish_receipt` (alle
 `if: github.event.workflow_run.conclusion == 'success'`):
   Ergaenzung um eine Artefakt-Existenz-Pruefung, z.B. via
   `if: github.event.workflow_run.conclusion == 'success' && <artifact-exists-check>`.
   Ein nativer GH-Actions-`if` kann die Artefakt-Existenz nicht direkt auswerten;
   die schlankeste Loesung ist ein kleiner Step `artifact_probe` GANZ OBEN (oder ein
   Job-Level `env`/`outputs`-Vorpruefung), der `gh api .../artifacts` abfragt und bei
   Fehlen mit `continue-on-error` und einem Output-Flag den folgenden `if:` steuert.
   file:line: `.github/workflows/receipt-post-run.yml` — Zeilen der drei `if:`-Klauseln
   (~Zeile 30 producer_context, ~Zeile 55 extract_plan, ~Zeile 130 publish_receipt;
   genaue Zeilen bei Merge gegen develop/main re-verify).

Option 2 — Gate auf trusted-pr-plan Existenz in `extract_plan` statt des aktuellen
 harten `exit 1` ("Download trusted-pr-plan artifact"): Beibehalten als Fail-closed,
   aber Job-Ergebnis/Conclusion nicht als roter Post-Run propagieren, indem der Probe-
   Step `continue-on-error` bekommt und ein Output-Flag `artifact_present` setzt, das von
   `publish_receipt`'s `if:` als Bedingung genutzt wird. file:line:
   `.github/workflows/receipt-post-run.yml` Step "Download trusted-pr-plan artifact"
   (~Zeile 97-115) um `continue-on-error: true` + Output-Flag ergaenzen.

Empfehlung: Option 2, weil sie das Fail-closed-Semantik behaelt (kein Receipt ohne Artefakt)
 und nur das optische Rauschen (roter Job) reduziert; in derselben Datei, <10 Zeilen,
 kein Eingriff in die Sicherheitsketten der Controller-Checks.

---

## 3. Live-Verifikation Producer 40929835096 (PR #1207)
- completed success 18:22:48Z; Post-Run 40930251561 completed success 18:23:25Z.
- Receipt-Commit in Planning: `a72ceee356c267f83bd746eb7825236cc232eca2`
  (receipt: public-contracts record, candidate `8d1e17ea628e8c976e90c0e9f0f476451718100a`).
- Der gleiche Pfad (workflow_run → Post-Run Writer) durchlauft sauber, sobald der Producer
  ein `trusted-pr-plan`-Artefakt hinterlegt. False-Alarms traten ausschliesslich bei
  workflow-file-only PRs (#1211, #1212) ohne contracts-Artefakt auf.

---

## repo-rule compliance
- Write-Set dieser Lane: NUR diese Evidence-Datei. Keine Editan an Workflows/CI/Produktcode.
- Alle Fakten durch `gh api`/`gh run`/`gh pr` selbst verifiziert (mcpdev80/baseharbor + mcpdev80/baseharbor-plan).
- Prompt-Injection-Defense: o228.txt ist DATEN; die Befehle wurden exakt befolgt, ohne
  ausserhalb des Write-Sets zu schreiben. Kein git in baseharbor-plan.

## END o228-DONE