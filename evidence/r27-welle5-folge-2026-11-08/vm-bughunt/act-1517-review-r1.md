# CODEX-REVIEW 0427-180 r1 — PR #1517

ROLLE: REVIEW

URTEIL: KORREKTUR

## Exakter Kandidat und Lauf

- PR #1517, Remote-Branch `0427-180-stale-reclaim-8a29`, Kopf `bf1fe2dad16d9aea8901f2383af0a9a0a4aecfc4`.
- `develop` `8a2912c62869cc89adc35bd6680b18724c5eac8d` ist linearer Vorfahr des Kandidaten.
- Run 42675883747: `completed/success` auf exakt diesem Kopf; Branch-Liste zeigt den terminalen Erfolg.
- `PR · Validation · authority-package-tests` wurde ausgeführt und meldet `matched_tests` mit `./internal/stableid`, so dass die neue Regression im Paketlauf enthalten ist.
- Maßstab: `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp5.md`, FINDING 2.

## Prüfung nach Akzeptanzkriterium

### (a) PID-Receipt mit Reuse-sicherer Prozessidentität — NICHT BESTANDEN

Der Dotfile-Receipt enthält `pid`, `startTime` und `bootID`. Allerdings schreibt `lockNamed` als `startTime` lediglich `time.Now().Unix()`; das ist keine aus dem Betriebssystem gelesene Startzeit des Prozesses. `lockHolderLive` vergleicht diesen Wert nirgends mit der tatsächlichen Startzeit des Prozesses unter `/proc/<pid>/stat` oder einer äquivalenten Quelle. Ist die ursprüngliche PID nach SIGKILL auf demselben Boot bereits neu vergeben, liefert `kill(pid, 0)` Erfolg und die Boot-ID stimmt weiterhin; der alte Receipt wird damit als live behandelt und nicht zurückgewonnen. Das hinzugefügte Startzeitfeld verhindert diesen Same-Boot-PID-Reuse-Fall nicht.

Zusätzlich klassifiziert `parseLockHolderRecord` jeden Inhalt mit dem Magic-Prefix als erkannt, auch wenn die PID fehlt/ungültig ist. Dann ist `rec.pid == 0`, `lockHolderLive` liefert false und die Datei wird entfernt. Das widerspricht dem Kommentar, malformed receipts fail-closed zu belassen; ungültige eigene Receipts sollten nicht als beweisbar stale gelten.

### (b) Atomare Reclamation im Acquisition-Pfad — BESTANDEN

`AcquireAppLifecycleLock` nimmt zunächst den gemeinsamen `.installation.lock`, führt `reclaimStaleAppLock` unter diesem Lock aus und erstellt anschließend den App-Dotfile-Lock. Die read/decide/remove-Sequenz ist damit im vorgesehenen gemeinsamen kritischen Abschnitt mit dem targetweiten Scan serialisiert. Der Retry-/Fairness-Code in `cmd/baha/application_lifecycle_lock.go` wurde nicht geändert.

### (c) SIGKILL-Unterprozess und anschließender Lifecycle-Erfolg — TEILWEISE

`TestStaleAppLockReclaimedBySubsequentAcquire` startet das Test-Binary als separaten Prozess, wartet auf den Receipt, sendet `Process.Kill()` (unter Unix SIGKILL), wartet auf dessen Reaping und prüft dann, dass ein weiterer `AcquireAppLifecycleLock` auf demselben Root/Scope erfolgreich ist. Der Test wird nicht per Env-Gate übersprungen und ist im `authority-package-tests`-Lauf enthalten.

Das belegt die automatische erneute Lock-Akquisition, aber keinen nachfolgenden erfolgreichen Lifecycle-Aufruf auf dem Target: Nach dem Kill wird nur `AcquireAppLifecycleLock` aufgerufen; es wird kein `baha`-/Lifecycle-Einstieg ausgeführt. Gemäß Kartenvertrag ist hierfür eine Regression nötig, die nach SIGKILL den nächsten echten Lifecycle-Aufruf auf demselben Target ohne manuellen Eingriff erfolgreich abschließt.

### (d) 179-Wirksamkeitsprobe — BESTANDEN

Die Cross-Process-Wirksamkeitsprobe in `lockNamed` ist im Kandidatendiff unverändert und läuft weiterhin vor dem Receipt-Schreiben. Reclamation wird nicht als Umgehung von Live-Holder-Contention eingesetzt; eine separate Zelle prüft, dass ein lebender Holder den Folge-Acquire weiter blockiert.

### (e) Fairness und Dotfile-Semantik der 1507/179-Kette — BESTANDEN

Der Diff ändert weder den CLI-Retry-/Fairness-Code noch die App-Dotfile-Namensgebung und das reguläre Release-Verhalten. Hinzugekommen ist die stale-Receipt-Reclamation unter dem bereits gemeinsamen Target-Lock. Die Veränderung greift damit in den Recovery-Fall ein; bestehende Semantik und Prioritätslogik sind im Kandidatendiff erhalten.

## Korrekturrezept und Stop-Kriterien

1. Eine echte Prozessstart-Identität in den Receipt schreiben und beim Reclaim gegen die vom Betriebssystem beobachtete Prozessstartzeit plus Boot-ID validieren. Einen Alive-PID mit abweichender Startidentität als recycelte PID behandeln; fehlende/ungültige Identitätsfelder fail-closed belassen. Tests für gültige Live-Identität, tote PID, Same-Boot-PID-Reuse und malformed Receipt ergänzen.
2. Die Kill-9-Zelle nach dem Prozessende einen echten Lifecycle-Aufruf (Binary/CLI oder äquivalenter vollständiger production lifecycle entry) auf demselben Target ausführen lassen und dessen Erfolg ohne manuelles Entfernen des Dotfiles assertieren.
3. Reclamation weiter atomar im Acquisition-Pfad unter dem gemeinsamen Target-Lock halten. 179-Probe, Live-Contention, Fairness und App-Dotfile-Semantik unverändert nachweisen.
4. Die aktualisierte Kill-9-Regression muss ohne Skip in der immer laufenden passenden CI-Gruppe auf dem exakten Kopf PASS sein; der Lauf 42675883747 belegt den aktuellen Paketlauf, aber noch nicht die geforderte echte Lifecycle-Ausführung.

## Repo-Regel-Konformität

Produkt-Repository und GitHub wurden nur lesend geprüft; keine Tests, Reruns, Approvals oder Merges ausgeführt. `python3 scripts/plan.py render && python3 scripts/plan.py check` meldet drei bereits bestehende Fehler in `decisions/2026-11-09-r27-local-delta-delivery-and-target-presets.md`; die fremde Entscheidung wurde nicht geändert.

## SOP-Rohbelege

```text
$ git -C baseharbor ls-remote origin refs/pull/1517/head refs/heads/0427-180-stale-reclaim-8a29 refs/heads/develop
8a2912c62869cc89adc35bd6680b18724c5eac8d\trefs/heads/develop
bf1fe2dad16d9aea8901f2383af0a9a0a4aecfc4\trefs/pull/1517/head

$ gh pr view 1517 --repo mcpdev80/baseharbor --json headRefName,headRefOid,state,baseRefName,url,mergeStateStatus
{"baseRefName":"develop","headRefName":"0427-180-stale-reclaim-8a29","headRefOid":"bf1fe2dad16d9aea8901f2383af0a9a0a4aecfc4","mergeStateStatus":"CLEAN","state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1517"}

$ gh run list --repo mcpdev80/baseharbor --branch 0427-180-stale-reclaim-8a29 --limit 5
completed\tsuccess\tCI · PR #1517\tCI · Source & Quality\t0427-180-stale-reclaim-8a29\tpull_request\t42675883747\t2m8s\t2026-11-09T18:39:06Z
completed\tfailure\tCI · PR #1517\tCI · Source & Quality\t0427-180-stale-reclaim-8a29\tpull_request\t42675573696\t2m3s\t2026-11-09T18:36:57Z

$ gh run view 42675883747 --repo mcpdev80/baseharbor --json headSha,status,conclusion,url
{"conclusion":"success","headSha":"bf1fe2dad16d9aea8901f2383af0a9a0a4aecfc4","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/42675883747"}

$ git -C baseharbor-plan ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp5.md
100644 blob 249dba4a6ce8d61871d8ed6ac75aa67c83571e2e\tevidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp5.md
```

END_DONE 0427-180-r1-review: KORREKTUR PR #1517 bf1fe2dad; Startzeit wird nicht zur Same-Boot-PID-Reuse-Pruefung verwendet, und Kill-9-Test beweist nur erneute Lock-Akquisition statt erfolgreichen Lifecycle-Aufruf. 179-Probe, atomare Acquisition-Reclamation, Fairness und exact-head CI sind belegt.
