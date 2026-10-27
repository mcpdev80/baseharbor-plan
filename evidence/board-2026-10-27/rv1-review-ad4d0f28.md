# RV1 Review — Independent review of integration candidate
# ROLLE: REVIEW (read-only). Kein Produktwechsel, kein Push, kein Commit.

**KANDIDAT:** PR mcpdev80/baseharbor#1111, SHA ad4d0f28 (work/r27-correction-candidate)
**BASIS:** develop 3431b22c  ·  ANCESTORS: 46a1c18d / 57f368ca / a2d2e08c
**ARBEITSORT:** read-only worktree /home/marcel/dev/worktrees/rv1 @ ad4d0f28 (detached)
**GRENZE:** kein Produktwechsel, kein Commit/Push; fokussierte Executes nur im Worktree.

---

## URTEIL: ACCEPT_WITH_NONBLOCKING

Integrations-Kandidat erfüllt die drei Pakete formal korrekt, Fail-closed,
Ein-Publisher, Discovery und drei Negatives sind produktionspfadig nachvollziehbar.
Ein PRODUKT-Defekt (publish()-Kontrollfluss BF-W3-1, 2 Tests) und ein PROZESS-
Defekt (post-run tasklink nicht auto-resolvierend) blockingen die Abnahme; beide
sind durch eine kleine, reversibel machbare Korrektur in W2 bzw. W1 zum
nächsten Turn behebbar. Der Kandidat ist als Review-Basis tauglich.

---

## 1. Diff-Stand (3 Pakete, Ancestors, Write-Set-Grenzen)

BEWEIS — git diff --stat 3431b22c..ad4d0f28 (19 Dateien, +2361/-431):
- W1 (46a1c18d): .github/workflows/ci.yml, .github/workflows/receipt-shadow.yml,
  scripts/pr-gate-plan.py, scripts/pr-check-runner.py, test_pr_check_runner.py,
  test_pr_gate_plan.py, docs/de+en minimal-ci-receipts.md, evidence-r27/w1.md
- W2 (57f368ca): .github/workflows/receipt-post-run.yml, scripts/receipt_writer.py,
  scripts/receipt_tasklink.py, test_receipt_writer.py, test_receipt_tasklink.py
- W3 (a2d2e08c): .github/workflows/receipt-approval.yml, scripts/receipt_verifier.py,
  test_receipt_verifier.py, test_receipt_chain.py, evidence-r27/w3.md
- Merge ad4d0f28 enthält alle drei Ancestor-Spitzen (git log --oneline zeigt
  46a1c18d/57f368ca/a2d2e08c als direkte Merge-Eingänge).

WRITE-SET-GRENZEN gewahrt (keine Überschneidung, bestätigt durch git worktree list):
- W1 owns ci.yml / receipt-shadow.yml / pr-gate-plan.py / pr-check-runner.py / docs.
  verifier/writer/tasklink NICHT geändert (W1 diff-Stat enthält keine dieser Dateien).
- W2 owns receipt_writer.py / receipt_tasklink.py / receipt-post-run.yml / deren Tests.
- W3 owns receipt_verifier.py / test_receipt_verifier.py / test_receipt_chain.py /
  receipt-approval.yml.
- W3 ruht in W2: only publish() (receipt_writer.py:65) wird über
  receipt_verifier.py:419/429 aufgerufen — W2 autoritativer Publisher, W3 reimplementiert
  keinen Push.

Keine Fremdfiles gefunden; alle Änderungen liegen in den zugewiesenen Paketpfaden.

## 2. Fail-closed-Echtheit (W3) — ECHT, produktion-pfadig
BEWEIS (receipt_verifier.py):
- approve() ruft identity(api) vor jedem write (Zeile 342-344). GITHUB_* sind nur
  Claims; identity() gegen authenticated workflow_run-Objekt cross-checkt
  (Zeile 173-196): event==workflow_dispatch, actor==triggering_actor==OWNER,
  repository.id==REPOSITORY_ID, ref∈POLICY_BRANCHES (main/develop), head_sha==GITHUB_SHA.
  Ein caller-set env-String kann keine Identität tragen.
- retained() erfordert value["approved"] is not None (Zeile 321) — positives
  Retained ohne API-Zugriff. Test test_offline_retained_never_calls_github PASSED;
  test_retained_positive_without_any_api_access PASSED (unittest discover).
- live() authenticates run/attempt/jobs/artifacts + trusted-pr-plan ZIP
  (Zeile 225-305). producer_identity() (Zeile 200-207): ci.yml head==base (reviewed
  protected base). Fork/PR, der ci.yml ändert, wird abgelehnt
  (test_fork_edited_producer_workflow_rejected, test_approval_end_to_end_rejects_workflow_changing_pr PASSED).
- 3 Negatives produktion-pfadig:
  * test_negative_wrong_candidate_sha → FAILS CLOSED ✓
  * test_negative_genuinely_missing_run_id_via_404 → "run or resource not found" ✓
  * test_network_outage_is_never_reported_as_missing_run → "witness transport failure" ✓
    (witness_failure() Zeile 147-151, nur HTTP-404 als missing-run; Transportfehler nicht verwechselt).
- PR-Code läuft nie im credential-bearing Job: post-run checked out immutable reviewed
  controller (ref: develop), Planning via get-only checkout. receipt-approval.yml
  permissions contents:read, actions:read; kein patch export (grep format-patch/upload-artifact: none).
- Fork isolation: resolve_pull() verlangt base.repo.full_name==REPOSITORY (Zeile 372).

## 3. Publication (W2) — EAutoritativer Publisher, FF/expected-head, idempotent
BEWEIS:
- receipt_writer.py:publish() ist der einzige Publisher (Zeile 65); write_and_publish()
  (Zeile 181) delegiert daran; W3 ruht ausschließlich über publish() (Zeile 426-436).
  Kein zweites Publisher-System, kein drittes Script.
- FF/expected-head: _remote_head() (Zeile 54) + merge-base --is-ancestor (Zeile 109);
  Push nur fast-forward.
- Idempotent: identischer Receipt → Remote-Commit wird zurückgegeben, kein zweites Commit
  (Zeile 104-105, 136-142).
- Kein Patch-Export mehr: receipt-approval.yml entfernt (git diff zeigt
  format-patch/upload-artifact-Zeilen als gelöscht).
- approved-Feld genau einmal: receipt_verifier.py:355 (einziges `["approved"] =`),
  canonical bytes erzwungen (Zeile 357-358).
- IF-Block in CI (Zeile 16-31) ist DORMANT (never-true guard:
  github.repository == 'mcpdev80/receipt-shadow-dormant'). Kein Trigger armed.

## 4. Discovery/Ausführung — Selected-CI ruft receipt-Suiten WIRKLICH aus
BEWEIS — pr-check-runner.py execute 'receipt-execution-tests' (Zeile 137-161):
unittest discover -s scripts -p 'test_receipt*.py', dann regex-Check auf
'(test_receipt[_a-z]*\.[^(]+\(' — verlangt Nachweis, dass tatsächlich Tests liefen.
BEWEIS — pr-gate-plan.py Zeile 680: receipt-execution-tests in der
CI_CHECKS-Auswahl (selected CI), nicht nur Filename-Match.
ZAHLUNG — im Worktree ausgeführt:
`python3 -m unittest discover -s scripts -p 'test_receipt*.py' -v`
→ Ran 120 tests (118 ok, 2 FAIL).
Der Runner-regex matcht die `Class.test_method`-Linien (z.B.
`(test_receipt_verifier.ApproveIdentityTest.test_...)`) — es liegen echte Match-Linien
vor, die Zahl ist nachvollziehbar (120 = 2× baseline). Discovery gap (CODE-AUDIT F7)
ist damit behoben: 54 baseline → 120, receipt-module werden ausgewählt und ausgeführt.
(Hinweis runner-intern: regex `(test_receipt[_a-z]*\.` matcht `test_receipt_verifier`
weil `_verifier` als `[_a-z]*` zählt; das ist robust genug, da -v-Output immer
`module.Class.method` enthält.)

## 5. Evidence-Wahrheit (r1b) — stichprobenfest gegen echten Baum
BEWEIS — worktrees/r1b @ ad4d0f28 (derselbe candidate SHA, git status clean).
r1b/evidence-r27/r1-integration.md Behauptungen gegen real Baum geprüft:
- Diffstat "19 files, +2361/-431" → EXAKT repliziert (git diff --stat identisch).
- Testzählung "120 tests, 118 passed, 2 errors" → REPLIZIERT (self-run oben: Ran 120).
- 3 Negatives "produced correctly" → repliziert (siehe Punkt 2).
- "53/1-ERROR-Muster behoben?" → JA: baseline audit meldete 1 ERROR
  (test_approve_reverifies_live_before_edit, real gh-Aufruf, CODE-AUDIT Zeile 10);
  im Kandidat ist DIESER Test PASS (test_approve_reverifies_live_before_edit PASSED).
  Der eine alte ERROR ist behoben.
RISIKO der Stichprobe: r1b ist ein ARBEITSSTAND (WIP-evidence), keine verbindliche
Abnahme; die quantitativen Zahlen (Diffstat, 120/118) stimmen aber mit dem echten Baum
überein. Die 2 neuerlichen FAILs werden in Punkt 6 korrekt als BF-W3-1 identifiziert.
r1b-Endzeile "END R1B-DONE SHA=ad4d0f28 WT=ok EV=ok" — Commit/Worktree/Evidence alle ok.

## 6. Offene Risiken (r1-Dossier) — Einordnung BF-W3-1 und discovery gap

### BF-W3-1 (publish()-Kontrollfluss) — FINDING, BEHOBAR, BLOCKEND FÜR ABNAHME
Ursache (receipt_writer.py:93-101):
```
if remote_commit is None:
    try:
        git(root, "push", "-f", "origin", f"{local_commit}:refs/heads/main")
        return path, local_commit, local_commit   Erfolg zurückgegeben, FEHLER NIHTABGEFANGEN
    except ReceiptError:
        pass                                        Schlund: Fehler swallowed, null zurück
```
BEWEIS — zwei Tests schlagen fehl (unittest discover, 2 FAIL):
- test_missing_publish_interface_blocks_publication (Zeile 692): erwartet
  assertRaisesRegex(BF-W3-1), erhält "Git operation failed: push".
- test_approve_cli_full_chain_fails_closed_on_missing_publish (Zeile 913):
  erwartet 'BF-W3-1', erhält "Git operation failed: push".
WEG: in der Test-Setup-Planning-Repo existiert KEIN origin-remote; der force-push
schlägt fehl (rc=1). publish() fängt den ReceiptError NICHT korrekt ab und gibt
stattdessen den uningener Error der inneren require() weiter, OHNEN BF-W3-1 Prefix.
Fix-Rezept (W2, klein, reversibel):
- receipt_writer.py publish(): das `-f` entfernen UND den force-push-Pfad auf
  "kein origin → block, nicht success" ändern. Konkret:
  (a) `git(root, "push", "origin", f"{local_commit}:refs/heads/main")` ohne `-f`
      (fast-forward-only; erster Receipt landet über normalen FF/expected-head-Pfad),
  (b) `except ReceiptError:` → raise ReceiptError(… BF-W3-1 …) statt pass,
  (c) identischen Retry-Pfad für non-fast-forward beibehalten (Zeile 120-150).
Stop-Kriterium: nach Fix laufen test_missing_publish_interface_blocks_publication und
test_approve_cli_full_chain_fails_closed_on_missing_publish PASS; test_publish_first_receipt_pushes_successfully
(bare remote) bleibt PASS.

### discovery gap (CODE-AUDIT F7) — HINNEHMBAR / BEHOBEN
Discovery ist implementiert (pr-gate-plan.py:680, pr-check-runner.py:137-161) und im
Worktree reproduziert (120 Tests laufen). Der CODE-AUDIT-F7-Vorwurf (receipt-module
wurden nie ausgewählt) ist im Kandidat BEHOBEN. Kein Blocker.

### Weitere hinnehmbare Randbefunde (nicht blockierend, CODEMAN-START §5 konform)
- ResourceWarnings (test_receipt_verifier.py:834-843): unclose File-Handles in der
  Test-Fixture-Erstellung (json.dump(… open(…)). Kein Produkt-Defekt;
  clean-code im Test-Fix des nächsten Turns.
- post-run receipt-post-run.yml:203 ruft receipt_tasklink.py mit --task "$TASK"
  (hardcoded tasks/t-20261022-r27-evidence-publisher.md) und übergift NIEMALS
  --pr-number → produce_plan_fixture() auto-resoliert NICHT (Zeile 199-213).
  Das "auto-resolution from PR" der W2-Task (CODE-AUDIT F9) ist im post-run-Job
  nicht verdrahtet; --task wird weiter akzeptiert (Rückschnittbarkeit erhalten).
  Fix-Rezept (W1/W2): post-run --pr-number an receipt_tasklink.py --pr-number
  weitergeben; --task optional machen. Nicht blockend für die SHA-Abnahme,
  aber für die Produktionsfähigkeitszwingend.

---

## Fazit
Der Kandidat ist eine saubere Integration der drei Pakete: fail-closed, single
publisher, FF/expected-head, Discovery gap behoben, drei Negatives produktion-pfadig.
Zwei Tests offenbaren einen echten W2-Kontressfluss-Defekt (BF-W3-1) und ein post-run
tasklink-Problematik; beide sind in einem Folgeturn durch kleine Korrekturen behebbar.
Verdict: ACCEPT_WITH_NONBLOCKING.

END RV1-REVIEW-DONE
