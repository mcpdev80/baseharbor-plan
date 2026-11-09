# CODEX-REVIEW 0427-175 r7 — PR #1512

ROLLE: REVIEW

URTEIL: KORREKTUR

## Exakter Kandidat und Lauf

- PR #1512, Branch `0427-175-initlock`, Kopf `84f60778ad6f71a8d1f76651e7e184bd2fe81558`.
- `develop` `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` ist im Kandidaten enthalten.
- Run 42661724281 ist `completed/success` auf exakt diesem Kopf; Branch-Liste und `gh run view` bestätigen den terminalen Erfolg.
- Runde-7-Evidence auf origin/main: `evidence/bughunt-concurrent-init-double-registration/round-7.md`, Blob `7c98148c1bab5cf2f4e1efef72e5a780387f1198`.

## Prüfung gegen act-1512-review-r6

### 1. Cobra-CLI-Einstieg — NICHT BESTANDEN

Die neue Poison-Recovery-Zelle `TestRegistryConflictRepairViaRealCLIEntryDeletesSelectedTwinOnlyAndKeepsSibling` ruft `executeApplicationDestroyLifecycle(...)` direkt auf. Das ist ein gemeinsamer Lifecycle-Helfer, kein Aufruf von `appDestroyCommand` beziehungsweise dessen Cobra-`Run`-Pfad. Daher belegt die Zelle nicht die verlangte Ausführung des Cobra-Einstiegs mit `--uuid <id> --full-reset --yes` einschließlich Authorization.

Der zusätzliche Test wird außerdem nur ausgeführt, wenn `BASEHARBOR_APP_FULL_RESET_ACCEPTANCE=1`; die Runde-7-Evidence bestätigt, dass er im beobachteten CI-Lauf standardmäßig SKIP. Damit beweist der exact-head grüne Lauf diesen nativen Entry-Test nicht.

### 2. Guard vor JEDEM destruktiven Effekt und Drift-Test — NICHT BESTANDEN

Der Guard steht nun am Anfang von `removeApplicationState()`, aber der normale Lifecycle ruft vorher `cleanupDevelopmentCanonicalRoutes`, `destroyRuntimeResources` und `cleanupProviderState` auf. Die Guard-Position ist somit weiterhin nach destruktiven Routen-, Runtime- und Provider-Effekten und erfüllt die geforderte Vorbedingung nicht. Der Guard muss an eine gemeinsame Vor-Mutations-Stelle vor diesen Aufrufen oder in gleichwertiger Weise so eingebaut werden, dass jeder destruktive Pfad ihn zuerst durchläuft.

`TestRegistryConflictCLIEntryDriftRefusedBeforeAnyMutation` baut und manipuliert eine Execution (`exec.selection = ...`), verwendet diese manipulierte Execution anschließend aber nicht. Stattdessen startet der Test `executeApplicationDestroyLifecycle` mit einer frischen, regulär selektierten Execution. Das ist kein erzwungener Drift durch denselben CLI-Pfad. Zusätzlich prüft der Test die Deployment-Records, nicht die `.owner`-Bänder; aufgrund der Lifecycle-Reihenfolge könnten Cleanup-Effekte bereits eingetreten sein, obwohl beide Records erhalten bleiben.

### 3. Twin- und Band-Nachweise — TEILWEISE BESTANDEN

Die erfolgreiche Recovery-Zelle seedet `.owner`-Bänder für beide Twins, prüft die vollständige Entfernung des ausgewählten Deployment-Verzeichnisses und vergleicht das Record sowie das Band des Survivors byteweise. Anschließend prüft sie die gesunde Registry mit genau dem überlebenden Record. Dieser Erfolgsnachweis erfüllt den Retentionsteil. Die Drift-Zelle belegt jedoch nicht, dass beide Twins einschließlich Band nach einer tatsächlichen Drift-Verweigerung unberührt bleiben.

### 4. Race-Regression und CI — BESTANDEN

`cmd/baha/app_init_concurrent_race_test.go` ist zwischen r6 und r7 unverändert. Der Lauf 42661724281 ist exakt-head `completed/success`. Das deckt die unveränderte, CI-ausgeführte Race-Regression ab; die native Acceptance-Suite mit dem Cobra-Einstieg wurde laut Evidence in diesem Lauf übersprungen.

## Korrekturrezept und Stop-Kriterien

1. Die Poison-Recovery-Zelle muss den tatsächlichen Cobra-`appDestroyCommand` ausführen (oder den echten durch Cobra gebundenen `Run`-Pfad), mit `--uuid <id> --full-reset --yes`; Resolution, Authorization, Preflight und Mutation müssen dabei im selben Aufruf stattfinden.
2. Den selector-vs-resolved Guard vor Route-, Runtime-, Provider-, App-State-, Provider-Registry- und Deployment-Record-Änderungen ausführen. Die Drift-Regression muss den Drift innerhalb genau des ausgeführten CLI-Pfads injizieren, bevor der Guard entscheidet.
3. Bei Drift-Verweigerung beide vollständigen Twin-Verzeichnisse inklusive `deployment.json` und `.owner` byte-identisch nachweisen und gesunde Registry mit beiden Einträgen prüfen. Beim Erfolgsfall ausgewählten Twin samt Band entfernt und Survivor samt Record+Band byte-identisch sowie Registry gesund belegen.
4. Race-Test und exakten terminalen CI-Nachweis erhalten. Stop review bis Cobra-Entry- und echte Drift-Regression die Kriterien erfüllen.

## Repo-Regel-Konformität

Produkt-Repository und GitHub wurden nur lesend geprüft. Keine Tests, Reruns, Approvals oder Merges ausgeführt. `python3 scripts/plan.py render && python3 scripts/plan.py check` meldet drei bereits bestehende Fehler in `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md`; diese fremde Entscheidung wurde nicht verändert.

## SOP-Rohbelege

```text
$ git -C baseharbor ls-remote origin refs/pull/1512/head refs/heads/0427-175-initlock refs/heads/develop
84f60778ad6f71a8d1f76651e7e184bd2fe81558\trefs/heads/0427-175-initlock
fea92f379e55bbe6e143a095d7c2e6c16e0b3a06\trefs/heads/develop
84f60778ad6f71a8d1f76651e7e184bd2fe81558\trefs/pull/1512/head

$ gh pr view 1512 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-175-initlock","headRefOid":"84f60778ad6f71a8d1f76651e7e184bd2fe81558","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1512"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-175-initlock --limit 5
completed\tsuccess\tCI · PR #1512\tCI · Source & Quality\t0427-175-initlock\tpull_request\t42661724281\t11m53s\t2026-11-09T17:08:45Z

$ gh run view 42661724281 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"84f60778ad6f71a8d1f76651e7e184bd2fe81558","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42661724281"}
```

END_DONE 0427-175-r7-review: KORREKTUR PR #1512 84f60778a; Cobra-Einstieg fehlt, Drift-Test manipuliert eine ungenutzte Execution und Guard kommt nach Route-/Runtime-/Provider-Cleanup. Erfolgsfall-Bands, unveränderte Race-Regression und exact-head CI sind belegt.
