ROLLE: REVIEW — rv1230

## PLAN

0. DONE — Auftrag und bindende Richtlinien gelesen; PLAN hier erfasst. Native TodoWrite ist in dieser Sitzung nicht verfügbar.
1. DONE — Task, Worker-Evidence, Kandidat, Basis und Remote-Checks SHA-genau verifiziert.
2. DONE — Non-PR-Skip, Negativ-Fixtur und Diff-Scope geprüft; Urteil und Rezept dokumentiert.
3. DONE — Dossier für Veröffentlichung vorbereitet; Commit, Push und ls-remote im Transcript bezeugen.

## Verdict: REQUEST_CHANGES

PR #1230 ist offen gegen main e92e20588c5737f566e29d47bbd08a9bcaed19d3, Head 9a5abda0f145beb52c2654cd2c635fa1797d2b85. HTTPS ls-remote bestätigt main und den Kandidatenbranch. Run 41120306664 ist completed/success für diesen Head, aber ausschließlich Workflow policy succeeded; PR Selected Checks und die übrigen PR-Jobs sind skipped. Der Run belegt somit nicht die Ausführung des geänderten Post-Run-Pfads. q260.md auf Planning main enthält END. Task ist review; Abhängigkeit t-20261017-release-0-4-27-updates nicht accepted.

1. **Non-PR nicht clean:** In `.github/workflows/receipt-post-run.yml` überspringt `skip_check` bei `push` den Download-Schritt, aber der folgende `Decode pr-plan and extract candidate_sha`-Schritt hat keine Skip-Bedingung. Er läuft nach erfolgreichem Checkout weiter und öffnet `plan.zip`, das wegen des übersprungenen Downloads nicht existiert. Das Extract-Job scheitert statt neutral/erfolgreich zu enden. Der Publish-Job wird damit zwar nicht ausgeführt, aber das erste Acceptance-Kriterium ist nicht erfüllt.
2. **Kein echter Negativtest:** `scripts/test_receipt_postrun.py`, `F1NegativeNonPRSkip`, liest das YAML und prüft allein das Vorhandensein von Zeichenfolgen und einer Download-Bedingung. Weder ein Fake-Producer-Payload noch die Steps werden ausgeführt; der fehlende Decode-Guard bleibt unentdeckt. Damit ist das geforderte Skip-Verhalten nicht bewiesen.
3. **API-Fehler als Non-PR klassifiziert:** `gh api ... || echo ""` verwandelt einen fehlgeschlagenen Event-Lookup in einen erfolgreichen Skip. Fehlende oder ungültige Evidenz über den Event-Typ ist kein nachgewiesener Non-PR-Fall und darf den PR-Verarbeitungspfad nicht still als Skip ausgeben.

Diff gegen den tatsächlichen PR-Merge-Base von main umfasst ausschließlich `.github/workflows/receipt-post-run.yml` und `scripts/test_receipt_postrun.py`; die Änderungen betreffen den benannten Scope. Kein Produkt-Worktree verändert; keine neuen gehosteten Runs ausgelöst.

## Worker-Rezept

In `.github/workflows/receipt-post-run.yml` alle Schritte, die den geladenen Plan voraussetzen, einschließlich `Decode pr-plan and extract candidate_sha`, an den erfolgreichen PR-Pfad binden; echten Non-PR-Event als erfolgreiche Skip-Ausgabe ohne Artefaktzugriff oder Receipt behandeln. Lookup-Fehler, leeres oder ungültiges Event separat fail-closed behandeln. In `scripts/test_receipt_postrun.py` eine ausführbare Regression mit gefälschtem authentifiziertem `push`-Producer und beobachteten Step-/Job-Ergebnissen ergänzen: exit 0, kein Download/Decode/Receipt; daneben PR-Positivpfad und API-Fehler als Fehler prüfen. Fokussierte Tests und die für den finalen SHA vorgeschriebenen CI-Checks ausführen, dann denselben Review-Kontext erneut vorlegen. Stop bei fortlaufendem Decode, Receipt-Versuch, fehlendem Ereignisnachweis oder nicht bestandenen Gates.

## repo-rule compliance

Unabhängige Lesereview; kein Merge, keine Produktänderung, kein Task-Statuswechsel. Fremde uncommittete Planning-Änderungen bleiben unangetastet. basics-check zeigte fremde Board-/Lane- und Pool-Hinweise, die durch diese Review nicht als erledigt behauptet werden.

Planning check: shared worktree with existing foreign WIP passes (0 errors, 14 warnings); clean remote-main worktree fails in pre-existing Planning metadata (integer PR reference, `short_ref` AttributeError). Foreign WIP was not included in this evidence commit.

END rv1230 REQUEST_CHANGES
