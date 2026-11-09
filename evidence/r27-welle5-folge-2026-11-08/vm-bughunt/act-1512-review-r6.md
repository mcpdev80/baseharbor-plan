# CODEX-REVIEW 0427-175 r6 — PR #1512

ROLLE: REVIEW

URTEIL: KORREKTUR

## Exakter Kandidat und Lauf

- PR #1512, Branch `0427-175-initlock`, Kopf `f4b26ecf2cc956fb2d16ed05f717a1ee95967adf`.
- `develop` `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` ist im Kandidaten enthalten.
- Run 42648335154 ist `completed/success` auf genau diesem Kopf; der Branch-Lauf-Eintrag bestätigt den terminalen Erfolg.
- Planning-Evidence: `evidence/bughunt-concurrent-init-double-registration/round-6.md`, origin/main Blob `7d43dc8e78eff72bf572eca6baeacce3f7557c87` (der angegebene Präfix `edbc87b1` stimmt nicht mit dem Blob auf origin/main überein).

## Prüfung gegen act-1512-review-r5

### 1. Echter Destroy-CLI-Pfad — NICHT BESTANDEN

`TestRegistryConflictRepairViaRealCLIDeletesSelectedDirAndBand` ruft nicht `appDestroyCommand` und auch nicht `executeApplicationDestroyLifecycle` auf. Es baut mit `newApplicationDestroyResolvedForRepair` eine Execution, ruft `runPreflight` und danach direkt `removeApplicationState`. Damit laufen CLI-Dispatch und `authorizeApplicationDestruction` nicht durch den Test. Das ist derselbe wesentliche Seam-Umweg, den r5 beanstandete; der Test belegt nicht die geforderte vollständige Folge aus Resolution, Authorization, Preflight und Mutation für `--uuid <id> --full-reset --yes`.

### 2. Identitätsvergleich vor jeder destruktiven Änderung — NICHT BESTANDEN

Der neue Vergleich in `removeApplicationState` steht zwar vor `deployment.DeleteDeploymentRecord`, aber erst nachdem `Store.Delete` bereits den App-Zustand gelöscht hat und `ReleaseApplicationProviderRegistryAt` die Provider-Registrierung verändert hat. Im echten Lifecycle können davor außerdem Routen-, Runtime- und Provider-Bereinigungen laufen. Der Guard steht somit nicht vor jeder destruktiven Änderung.

`TestRegistryConflictIdentityDriftRefusedWithoutDeletingEitherTwin` ruft ebenfalls direkt `removeApplicationState` auf und prüft nur die beiden Deployment-Verzeichnisse. Sein `poisonTwinFixture` legt keine `.owner`-Bands an. Es belegt daher weder den Drift-Stopp vor allen Mutationseffekten noch, dass beide Twins samt Retained Bands unverändert bleiben.

### 3. Retained-Band- und Recovery-Assertions — TEILWEISE

Die erfolgreiche Recovery-Zelle seedet `.owner`-Dateien für beide Records und prüft, dass das ausgewählte Verzeichnis samt Band entfernt wird. Sie prüft anschließend die gesunde Registry mit genau dem überlebenden Sibling. Es fehlt jedoch der geforderte Byte-identisch-Nachweis für den gesamten anderen Twin einschließlich Band; ein Registry-Eintrag allein beweist die Unverändertheit seiner Dateien nicht.

### 4. Race-Regression — BESTANDEN

`cmd/baha/app_init_concurrent_race_test.go` hat im R6-Kandidaten gegenüber seinem Elternstand keinen Diff. Damit bleibt die vorher geprüfte Prozess-Seam-/Contention-Regression unverändert. Der Lauf 42648335154 ist auf exakt R6 terminal erfolgreich und enthält laut Runde-6-Evidence den `go-unit-tests` Job.

## Korrekturrezept und Stop-Kriterien

1. Die Poison-Recovery-Regression muss `appDestroyCommand` mit `--uuid <id> --full-reset --yes` ausführen und die vollständige Produktionssequenz einschließlich Authorization erreichen. Ein direkter Aufruf von Execution-/Lifecycle-Seams genügt nicht.
2. Selector-vs-resolved-Identität muss vor jedem destruktiven Effekt geprüft werden, einschließlich App-State-Löschung, Provider-Registry-Freigabe, Runtime-/Routen-/Provider-Cleanup. Eine Drift-Regression muss über denselben CLI-Pfad laufen und belegen, dass beide Twins sowie alle zugehörigen Zustände vor der Verweigerung unverändert bleiben.
3. Beide Twins samt `.owner`-Band seedieren. Nach erfolgreicher Auswahl muss der ausgewählte Twin vollständig verschwunden sein; der andere Twin einschließlich Record und Band muss byte-identisch sein; danach Registry-Gesundheit belegen.
4. Race-Regression und exakten terminalen CI-Lauf erhalten.

## Repo-Regel-Konformität

Produkt-Repository und GitHub wurden nur lesend geprüft. Keine Tests, Reruns, Approvals oder Merges ausgeführt. Das Planning-Board-Checkskript meldet weiterhin drei bereits bestehende Fehler in `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md`; die fremde Entscheidung wurde nicht verändert.

## SOP-Rohbelege

```text
$ git -C baseharbor ls-remote origin refs/pull/1512/head refs/heads/0427-175-initlock refs/heads/develop
f4b26ecf2cc956fb2d16ed05f717a1ee95967adf	refs/heads/0427-175-initlock
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06	refs/heads/develop
f4b26ecf2cc956fb2d16ed05f717a1ee95967adf	refs/pull/1512/head

$ gh pr view 1512 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-175-initlock","headRefOid":"f4b26ecf2cc956fb2d16ed05f717a1ee95967adf","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1512"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-175-initlock --limit 5
completed\tsuccess\tCI · PR #1512\tCI · Source & Quality\t0427-175-initlock\tpull_request\t42648335154\t11m19s\t2026-11-09T15:48:19Z

$ gh run view 42648335154 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"f4b26ecf2cc956fb2d16ed05f717a1ee95967adf","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42648335154"}
```

END_DONE 0427-175-r6-review: KORREKTUR PR #1512 f4b26ecf2; echter CLI-/Authorization-Pfad fehlt, der Guard liegt nach frueheren Mutationen, und Drift plus Sibling-Byte-Identitaet samt Bands sind nicht ausreichend belegt.
