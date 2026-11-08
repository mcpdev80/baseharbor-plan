# Round 1 — bughunt count=2 confirm-deadlock (card t-20261108-bughunt-0427-count2-confirm-deadlock)

Lane 0427-135, owner `lane-w135-count2`. Mission: reproduce the reported
`go test ./cmd/baha -count=2` hang (alleged pipe-holding goroutine in
`recordDeploymentBeforeMutation`, consent==nil path) on a clean host; fix
minimally with a CI-run regression, or deliver a documented negative /
attributed finding.

## PLAN

- Wirklichkeitsabgleich: origin/develop = `07ae6c3e91b081a189266ca4b162ba705d4aa78f`
  (ls-remote), Karte + Fundquelle round-9.md „Open (handed to owner / blocked) F1"
  gelesen; Claim aktiv (lane-w135-count2).
- Base-Attestation: Worktree `/tmp/opencode/0427-135-wt`, Branch
  `task/0427-135-count2-confirm-deadlock` geschnitten von 07ae6c3e9 — **null Commits,
  kein Produktzweig, kein PR** (develop nicht betroffen, siehe Befund).
- IST-Reproduktion auf develop-Baum (Zelle + lokale Proben + SIGQUIT-Dumps): Haenger
  NICHT reproduzierbar.
- Owner-Antwort (QUESTION): Urfall war auf WIP-Head `e291fba9a`
  (`task/r27-compose-host-isolation-wip`), nicht develop → Gegenprobe auf genau diesem Head.
- WIP-head count=2-Zellen auf sauberem Host baha-docker-2 (vm-lock lane-w135-count2):
  wip3 terminiert sauber PASS; wip5 terminiert uber go-test-Alarm (500s) mit vollem
  Goroutine-Dump — KEIN exit-block-Haenger, KEIN io.Pipe-Rahimen im Dump.
- Einordnung: 2b Dreifach-Negativ (develop negativ, WIP-Head negativ,
  Urzeugnis /tmp/c2-matrix.out nicht mehr vorhanden; Erklaerung unten).
- Evidence hier, Push nach baseharbor-plan origin/main, Host-Aufraeumen, vm-lock release, END.

## Befund: count=2-Haenger nicht reproduzierbar (negativer Dreifach-Beweis)

### 1. develop @ 07ae6c3e9 (Base-Attestation)

- Sigle-Zellen mit `consent==nil`-Weg (`TestMissingCandidateConsent*`, count=2):
  `ok ... 0.017s` — terminieren sofort, kein exit-block.
- Vollstaendige count=2-Versuche auf diesem Rechner: der Prozess endet normal;
  ein exit-blockender Pipe-Warater existed nicht, weil auf diesem Host fd0 der
  Test-Binaeren `/dev/null` ist (kein Pipe-Ende). Ein eigens gebauter Leak-Probe
  (os.Pipe als os.Stdin, apply-Lifecycle mit consent==nil) meldete
  `goroutines 2->2 pipeWaiters=0`.
- Produktsuche: die einzigen `io.Pipe()` in Nicht-Test-Quellen sind
  `internal/targetsession/stream.go:70` und `internal/runtime/compose_command.go:107`,
  beide mit Close-Disziplin (`CloseWithError` auf allen Aesten). In `cmd/baha`
  gibt es kein `io.Pipe()`. `recordDeploymentBeforeMutation`
  (`cmd/baha/deployment_record.go` ~:393, consent==nil →
  `errConsentRequiredForCandidateSubmission` ~:522) oeffnet bei der Verweigerung
  keinerlei Stream/Pipe und startet keinen Warter-Goroutine.
- SIGQUIT-Dumps der blockierten Daemone zeigen nur den normalen
  `os/exec`-Waiter-Kanal — keine Pipe haltende Goroutine.

### 2. WIP-head e291fba9a (Gegenprobe gemaess Owner-Antwort)

Host baha-docker-2 (rootless docker), Claim lane-w135-count2, Ambient-Check vor jeder
Zelle (fremde `bh-w169-ci-bootstrap-*` Container unangetastet gelassen).

- Zelle wip3 (`TestRepositoryWorkflowRealLifecycle -test.count=2`, korrekte Launch-Semantik):
  Iteration 1 PASS (195.40s), Iteration 2 PASS (39.03s), `PASS`, Prozess exit clean,
  `cell_end=wip3 2026-11-08T07:11:34Z`, `HANG=no`.
- Zelle wip5 (3 Lifecycle-Tests, count=2, start 07:13:15Z): Exit rc=2 nach
  `-test.timeout=500s`-Alarm mit vollem SIGQUIT-Dump. 5 von 6 Iterationen PASS
  (u.a. `TestRepositoryWorkflowRealLifecycle` Iteration 2 mit 37.41s,
  `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` Iteration 2 86.97s).
  Die haengende Iteration war `TestRepositoryComposeWorkloadOnlyLifecycleInCI`
  Iteration 2, steckend in `docker compose stop` (Wartezeit des compose-CLI auf
  einem durch 19-35 ambient Container anderer Lanes belasteten Host). Dump-Rahmen:
  `os/exec ... pidfdWait` in
  `internal/runtime/compose_files.go:384` (`outputProjectFilesInputEnv`,
  `cmd.Stdin = bytes.NewReader(input)` — eine fertige byte.Reader, keine Pipe,
  kein Warter-Leak moeglich) via `compose_files.go:182` ← `service_stop.go:93` ←
  `app_workload.go:659`. **Kein einziger io.Pipe-/consent-Rahmen im Dump.**
  Alarm-Panik ist ein Test-Zeitueberschreitungs-Tod, kein Prozess-exit-block —
  genau der Unterschied, den die Karte pruefen wollte. Im gesamten Dump gibt es
  0 `io.Pipe`-/`targetsession`-Rahmen (6 Goroutines insgesamt).
- Der Diff `07ae6c3e9..e291fba9a` betrifft in `cmd/baha` nur
  deployment_record.go (+41), target.go (+52) und Test-Support-Dateien;
  `internal/runtime` wird vom WIP-Delta ueberhaupt nicht geaendert.

### 3. Gegenueberstellung mit dem Urzeugnis

- Der im Transcript zitierte Beleg `/tmp/c2-matrix.out` existiert auf diesem Rechner
  nicht mehr (Datei fehlt; Verifikation des Original-Zeugnisses damit nicht mehr
  moeglich — keine Widerlegung, aber auch keine Bestaetigung).
- Meine eigenen ersten WIP-Zellen (`wipcount2`, `wip2`) hatten einen
  Launch-Defekt (fifo-Oeffner starb vor dem exec; `run.log` nie angelegt,
  Test-Binaere lief nie). Ihre `HANG=yes`-Zeugen sind **invalidiert** und
  wurden nicht als Reproduktion gewertet; wip3/wip5 sind die gueltigen Zellen.
  plausibelste Erklaerung des Urhangs: ein Lauf unter shared-host Ambient-Last
  (compose-CLI-Warten), nicht ein
  Pipe-Leak im confirm-Pfad. Auf develop und auf dem WIP-Head selbst ist der
  confirm-Pfad (consent==nil → sofortige Verweigerung ohne Eroffnung von
  Streams) count=2-harmonisch.

## Ergebnis

- **Kein Produktfix, kein PR** (Develop nicht betroffen; WIP-head-Gegenprobe
  terminiert ebenfalls — Dreifach-Negativ, Karte als bughunt-Befund schliessbar).
- Kandidat-Ast: Branch `task/0427-135-count2-confirm-deadlock` existiert nur
  lokal mit 0 Commits auf 07ae6c3e9; kein Remote-Branch, keine PR.

## Zeugen (Auszug)

```
wip3 witness.txt (baha-docker-2:~/lanes/135/wip3):
cell=wip3 host=baha-runner-docker-2 start=2026-11-08T07:07:36Z count=2 bin=baha-wip.test binmd5=3386e3b5aa885b8977b3c7864669f314
containers_running_before=19
test_pid=4166784
--- PASS: TestRepositoryWorkflowRealLifecycle (195.40s)
--- PASS: TestRepositoryWorkflowRealLifecycle (39.03s)
PASS
EXITED rc=0 ... / HANG=no / cell_end=wip3 2026-11-08T07:11:34Z

wip5 witness.txt (baha-docker-2:~/lanes/135/wip5):
cell=wip5 start=2026-11-08T07:13:15Z count=2 binmd5=3386e3b5aa885b8977b3c7864669f314
containers_running_before=27
--- PASS x5, panic: test timed out after 8m20s (Iteration 2 OnlyLifecycleInCI, docker compose stop)
EXITED rc=2 after 500s / HANG=no / cell_end=wip5 2026-11-08T07:21:38Z
```

## Sauberkeit / OWN-BLOCK

- Eigene compose-Projekte je Zelle down (`cell3.sh`-Cleanup); fremde
  `bh-w169-ci-bootstrap-*` (19-35 Container) nie angefasst.
- vm-lock: `lane-w135-count2` auf baha-docker-2 am Ende released.
- Keine Schreibgriff in `internal/orgconfig/profiles.go`,
  `internal/runtime` service_stop/retirement-Dateien oder `.github/**`.
- OWN-BLOCK (fuer Routing, keine Editierung): die InCI-Tests laufen in CI nur
  unter dem `BASEHARBOR_CI_RUNTIME_INTEGRATION`-Gate ihrer Workflows; ein
  Timeout-Haertung (`-test.timeout` vs. compose-Stop-Last) waere `.github/**`-
  bzw. Test-Support-Eigentum anderer Lanes — hier nur dokumentiert.
