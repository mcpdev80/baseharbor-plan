# CODEX-REVIEW 0427-165 r11 — PR #1500

ROLLE: REVIEW

URTEIL: APPROVE

## Exakter Kandidat und Lauf

- PR #1500, Branch `0427-165-target-delete-orphanrec`, Kopf `ef1851dc707cf386ccab73b6d1041a673b9f826b`.
- PR-Base `develop`; aktueller `develop` ist `8a2912c62869cc89adc35bd6680b18724c5eac8d`. Dieser Base-Commit ist Vorfahr des Kopfes; es liegen vier lineare Commits darauf und keine Merge-Commits im Bereich.
- Run 42674227560, Attempt 2: `completed/success` auf exakt `ef1851dc707cf386ccab73b6d1041a673b9f826b`.
- Im erfolgreichen Attempt 2 sind `PR · Native destroy retry · docker` und `PR · Native destroy retry · podman` beide erfolgreich. `PR · Validation · go-unit-tests` ist erfolgreich; sein voller Paketlauf meldet `ok github.com/mcpdev80/baseharbor/cmd/baha 494.062s`. `TestUpNameResumesThroughCommandEntrypoint` ist in diesem unveränderten `cmd/baha`-Paket enthalten und hat keinen Skip-Pfad. Attempt 1 war fehlgeschlagen; die erneute native Ausführung in Attempt 2 heilte den Laufwiderspruch.

## Prüfung des Rezept-Kerns

### 1. Linearer Rebase auf develop — BESTANDEN

Der exakte `develop`-Commit `8a2912c62` ist Vorfahr des PR-Kopfes. Der Bereich enthält vier reguläre, lineare Commits und keine Merge-Commits; ein weiterer Rebase ist nicht erforderlich.

### 2. Getrennter Lock- und Orphan-Verweigerungsfall — BESTANDEN

`TestTargetDefinitionDetachBlocksOnSharedTargetWideLock` richtet einen gültigen Target-Zustand ohne collectable Orphans ein, hält den produktiven App-Lifecycle-Lock und ruft `deleteTarget` auf. Die Assertion schließt den Orphan-Fehlercode ausdrücklich aus, sodass allein die Verweigerung am gemeinsamen targetweiten Lock den Test erfüllt.

`TestTargetDefinitionDetachRefusesOwnerlessRecord` ist der separate Produktionspfad-Fall: Er entfernt den Runtime-Owner, seedet einen collectable Orphan und prüft, dass `deleteTarget` die Detach-Änderung mit dem benannten Orphan verweigert und sowohl Target-Konfiguration als auch Record unverändert bleiben. Die beschädigten/abweichenden UUID-Ordner- und Identity-Fälle bleiben davon getrennt; die r11-Änderung ergänzt insbesondere einen gültig benannten Ordner mit abweichender eingebetteter UUID, der nicht als collectable Orphan ausgegeben wird, während die ownerless Detach-Prüfung fail-closed bleibt.

### 3. `TestUpNameResumesThroughCommandEntrypoint` im vollen Lauf — BESTANDEN

Attempt 2 führt den vollständigen `go-unit-tests`-Gate aus. Der Test liegt im `cmd/baha`-Paket; dieses Paket meldet im Lauf `ok` nach 494.062 Sekunden. Der Test selbst enthält keinen Skip-Pfad. Damit ist der frühere exakte-head Rückfall im vollständigen Paketlauf geheilt; ein isolierter Testlauf wird nicht als Ersatz herangezogen.

## Urteil

Die geprüften r11-Kriterien sind auf dem exakten Kandidaten erfüllt. Dies ist ein Review-Urteil; es wurde weder genehmigt noch gemergt.

## Repo-Regel-Konformität

Produkt-Repository und GitHub wurden nur lesend geprüft. Keine Tests, Reruns, Approvals oder Merges ausgeführt. `python3 scripts/plan.py render && python3 scripts/plan.py check` meldet bestehende, nicht durch diese Akte verursachte Validierungsfehler in Planning-Einträgen; diese wurden nicht geändert.

## SOP-Rohbelege

```text
$ git -C baseharbor ls-remote origin refs/pull/1500/head refs/heads/0427-165-target-delete-orphanrec refs/heads/develop
ef1851dc707cf386ccab73b6d1041a673b9f826b\trefs/heads/0427-165-target-delete-orphanrec
8a2912c62869cc89adc35bd6680b18724c5eac8d\trefs/heads/develop
ef1851dc707cf386ccab73b6d1041a673b9f826b\trefs/pull/1500/head

$ gh pr view 1500 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-165-target-delete-orphanrec","headRefOid":"ef1851dc707cf386ccab73b6d1041a673b9f826b","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1500"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-165-target-delete-orphanrec --limit 8
completed\tsuccess\tCI · PR #1500\tCI · Source & Quality\t0427-165-target-delete-orphanrec\tpull_request\t42674227560\t10m21s\t2026-11-09T18:54:27Z
completed\tfailure\tCI · PR #1500\tCI · Source & Quality\t0427-165-target-delete-orphanrec\tpull_request\t42668673003\t8m53s\t2026-11-09T17:51:28Z

$ gh run view 42674227560 --repo mcpdev80/baseharbor --attempt 2 --json headSha,status,conclusion,url,updatedAt
{"conclusion":"success","headSha":"ef1851dc707cf386ccab73b6d1041a673b9f826b","status":"completed","updatedAt":"2026-11-09T19:04:49Z","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42674227560/attempts/2"}

$ gh run view 42674227560 --repo mcpdev80/baseharbor --attempt 2 --json jobs | jq -r '.jobs[] | select(.name|test("go-unit-tests|Native destroy retry|PR Selected Checks")) | [.name,.status,.conclusion] | @tsv'
PR · Native destroy retry · podman\tcompleted\tsuccess
PR · Native destroy retry · docker\tcompleted\tsuccess
PR · Validation · go-unit-tests\tcompleted\tsuccess
PR Selected Checks\tcompleted\tsuccess
```

END_DONE 0427-165-r11-review: APPROVE PR #1500 ef1851dc7; develop-Basis linear, Lock/Orphan-Regression getrennt, voller go-unit-tests-Lauf samt erfolgreichem cmd/baha-Paket, Docker und Podman in Attempt 2 gruen.
