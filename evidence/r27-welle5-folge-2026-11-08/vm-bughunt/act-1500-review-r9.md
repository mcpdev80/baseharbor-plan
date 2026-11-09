# CODEX-REVIEW 0427-165 r9 — PR #1500

ROLLE: REVIEW

URTEIL: KORREKTUR

## Kandidat und Nachweise

- PR #1500, Branch `0427-165-target-delete-orphanrec`, exakter Head `f5883e1e9897869686d9879675489bc1496c3156`, offen, Base `develop`.
- `origin/develop` ist `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` und Vorfahr des Kandidaten; `develop...head` = `0 3`. Kein Rebase wegen Drift erforderlich.
- Lauf 42613341749: `completed/failure` auf exakt `f5883e1e9897869686d9879675489bc1496c3156`.
- PR-Lauf 42613302851 ist ebenfalls fehlgeschlagen. Der Dispatch-Lauf benennt die unten stehende Entrypoint-Regression.

## Prüfung gegen vollständiges Rezept

Der r9-Diff von `cmd/baha/target_definition_orphan_refusal_test.go` erfüllt den geforderten Split:

- `TestTargetDefinitionDetachBlocksOnSharedTargetWideLock` ruft den echten `deleteTarget`-Pfad bei null collectable orphans auf, hält den App-Lifecycle-Lock und akzeptiert `target_definition_collectable_orphans` ausdrücklich nicht als Lock-Erfolg. Zieldefinition bleibt unverändert.
- `TestTargetDefinitionDetachRefusesOwnerlessRecord` ist der separate produktionsnahe Verweigerungsfall und prüft den Fehlercode, die genannte Orphan-ID sowie den unveränderten Record und Target.
- Der aktuelle `develop`-Stand ist bereits Vorfahr; der verlangte lineare Rebase ist bei diesem Head nicht nötig.

**Blockierender Befund:** Das exakte Run 42613341749 scheitert in `go test ./...` mit `TestUpNameResumesThroughCommandEntrypoint` (`cmd/baha`). Diese Entrypoint-/Base-Rückfall-Regression muss als eigener #1500-Befund behandelt werden, nicht als fremder STATE. Das Testziel ist ausdrücklich, dass ein registrierter Name über `up NAME` und `app up NAME` aufgelöst wird und ein unbekannter Name fail-closed bleibt. Ein fehlgeschlagener exakter Lauf kann die Kandidatenabnahme nicht tragen.

## Korrekturrezept und Stop-Kriterium

- `cmd/baha`-Entrypoint-/Name-Auflösung untersuchen und `TestUpNameResumesThroughCommandEntrypoint` auf dem Kandidaten korrigieren; `up NAME` und `app up NAME` müssen den registrierten Namen bis zur Deployment-Auflösung führen, während unbekannte Namen weiterhin fail-closed bleiben.
- Rebase-Basis vor der Änderung erneut prüfen; solange `fea92f379` Vorfahr ist, ist kein Base-Update nötig.
- Die beiden getrennten Regressionen für Lock ohne Orphans und Orphan-Verweigerung erhalten und sicherstellen, dass die betroffenen Tests vom erforderlichen CI-Check erfasst werden.
- Stop review erst, wenn ein terminaler Lauf auf dem exakten neuen Head `TestUpNameResumesThroughCommandEntrypoint` bestanden zeigt und die erforderlichen Checks ohne Fehler abgeschlossen sind.

## Repo-Regelkonformität

Nur lesendes Produktreview und ein Handoff mit dem Korrekturrezept. Keine Produktdateien, Läufe, PR-Status oder Branches verändert; keine Tests ausgeführt, keine Freigabe oder Merge.

## SOP-Rohbelege

```text
$ git ls-remote origin refs/pull/1500/head refs/heads/0427-165-target-delete-orphanrec refs/heads/develop
f5883e1e9897869686d9879675489bc1496c3156	refs/heads/0427-165-target-delete-orphanrec
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
f5883e1e9897869686d9879675489bc1496c3156	refs/pull/1500/head

$ gh pr view 1500 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-165-target-delete-orphanrec","headRefOid":"f5883e1e9897869686d9879675489bc1496c3156","mergeStateStatus":"UNSTABLE","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1500"}

$ gh run view 42613341749 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"failure","headSha":"f5883e1e9897869686d9879675489bc1496c3156","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42613341749"}
```

END_DONE 0427-165-r9-review: KORREKTUR PR #1500 f5883e1e9; lock/orphan test split is now specific, but exact-head run fails TestUpNameResumesThroughCommandEntrypoint and must be corrected before review can pass.
