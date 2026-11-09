# CODEX-REVIEW 0427-178 r2 — PR #1511

ROLLE: REVIEW
URTEIL: KORREKTUR

## PLAN

1. PR-Head, develop-Basis, ancestry und terminale Hosted-Checks sha-genau verifizieren.
2. Den Batch-/Classification-Delta gegenüber dem zuvor approbierten #1509-Stand prüfen.
3. Die #174-Fail-closed- und truthful-classification-Pfade sowie Testabdeckung im neuen Batch-Aufruf prüfen.
4. Urteil und gezieltes Korrekturrezept veröffentlichen.

## Verifizierter Stand

- PR #1511 head `97c0f1ed95698524ffe2a0f8edca89efc4b90711`; base `develop` = `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`; merge-base entspricht develop, kein Drift.
- Exakter Run `42590834498`: `completed/success` auf genau diesem Head. `PR Selected Checks` vom GitHub Actions integration 15368 ist grün. `deployment-package-tests`, `cli-guided-tests`, build, vet und source-contracts sind ausgeführt und grün. Die nativ ausgewiesenen Jobs sowie weitere Matrix-Jobs sind `skipped`; sie sind nicht als grün gezählt.
- Live-PR ist offen und `MERGEABLE/CLEAN`; es wurde kein Merge ausgeführt.
- Gegenüber dem aktuellen develop-Diff fügt der PR `deployment_list_owner_batch.go` und `deployment_list_owner_scale_test.go` hinzu und ändert `deployment_owner_loan.go`. Er ändert `deployment_list.go` und `deployment_store.go` nicht. Die #174-Dateien sind daher aktueller Base-Inhalt; der PR-Batch muss ihre Semantik übernehmen.

## Befund zum Delta

Der Batch zählt den einmaligen Owner-Load und wendet danach pro Deployment erneut `verifyDeploymentOwnerAgainstInstallation` an (`internal/deployment/deployment_list_owner_batch.go:77-85,110-143`). Damit wird der per-Deployment-Ordner-/Target-Check nicht blind aus dem Cache übernommen. Der genehmigte Skalierungsansatz bleibt erkennbar: nur der Target-Owner-State wird gebündelt.

Die neue Batch-Owner-Ladeverzweigung erhält aber die #174-Klassifikation nicht: `internal/deployment/deployment_list_owner_batch.go:101-105` behandelt jeden Fehler außer `os.ErrNotExist` als `ErrDeploymentOwnerForeign`. Dadurch wird ein tatsächlicher Permission-/Filesystem-Lesefehler beim Laden von `installation.json` als fremder Owner klassifiziert. Bei best-effort list wird dieser Fehler anschließend in `classifyOwnerFailure` als `foreign` ausgegeben (`deployment_list_owner_batch.go:153-163,191-200`); beim normalen List bleibt der falsche Sentinel ebenfalls erhalten. Der bestehende #174-Einzelpfad in `internal/deployment/deployment_store.go:159-180` unterscheidet Access-Denied, malformed state und echte positive Foreign-Identität. Der neue Batch lädt unabhängig und ruft diese Klassifikation nicht auf.

Die neue `TestBatchedListClassifiesAccessForeignMissing` deckt diesen Fall nicht ab: ihr `access`-Untertest injiziert einen Fehler aus `TenantOwnerResolver` (`deployment_list_owner_scale_test.go:240-267`), bevor ein Owner-Datei-Load fehlschlägt. Er beweist daher nicht, dass `os.ErrPermission` oder ein anderer tatsächlicher Load-Fehler `access` statt `foreign` wird. Die r2-Regression `TestDeploymentOwnerLoanRecheckPropagatesReadError` testet den separaten Loan-Recheck-Pfad, nicht `ownerBatch.loadOwner`. Ich sehe im Kandidaten keine Abschwächung bestehender Tests, aber eine fehlende Regression für den neuen Batch-Ladepfad.

## Korrekturrezept

- Datei: `internal/deployment/deployment_list_owner_batch.go`, besonders `ownerBatch.loadOwner` Zeilen 101-105.
- Änderung: dieselbe zentrale Owner-Load-Klassifikation wie `VerifyDeploymentOwner` verwenden. `os.ErrNotExist` bleibt Missing; Permission/sonstige nicht lesbare Installation muss als access-denied weitergereicht werden; malformed bleibt eigener fail-closed Zustand; `foreign` darf nur aus einer positiv geladenen, tatsächlich abweichenden Identität entstehen.
- Testanforderung: ergänze eine Best-effort und/oder normale Batch-List-Regression, die `resolveInstallationLoad` für den Target-Owner deterministisch mit `os.ErrPermission` fehlschlagen lässt. Best-effort muss `Kind == "access"` und `errors.Is(err, ErrDeploymentOwnerAccessDenied)` erhalten; normaler List-Aufruf darf weder `ErrDeploymentOwnerForeign` noch ein erfolgreich gelistetes Record liefern. Behalte die vorhandenen missing-, positive-foreign-, tenant-grant- und per-record-bound-Tests. Die Regression muss im Hosted `deployment-package-tests` Job laufen.
- Stop-Kriterium: echte Owner-Datei-Lesefehler werden im neuen Batch-Pfad nie als foreign oder missing ausgegeben; positiver foreign identity mismatch bleibt weiterhin fail-closed; exakter korrigierter Head hat terminal erfolgreiche erforderliche Checks.

Status: nicht mergefähig bis diese #174-Klassifikation im Batched Owner-Load erhalten und CI-erfasst ist.

END 0427-178 REVIEW: KORREKTUR — PR #1511 `97c0f1ed95698524ffe2a0f8edca89efc4b90711`; Batched Owner Load faltet echte Load-Fehler in `foreign`.
