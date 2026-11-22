# 0428-240 round-1 — broker readiness diagnostics name the dependency

Mission: t-20261122-broker-diagnostics-empty. Gemelde leegte: attempt-3 logs van de data-capabilities-reihe zeggen 'application runtime broker container health is unhealthy; runtime diagnostics:' en dan komt NIETS (docker job 137133647957, podman job 137133625738, regel per app_capability_runtime_test.go:136).

## PLAN

- (done) 1. ls-remote develop = `acc343239681feb235a33cf00c8ea754c537291f`; branch lane-0428-240-broker-diagnostics exact daarop gesneden (werkzone workers/0428-240-brokerdiag-wt, 0 wijzigingen voor de snit).
- (done) 2. Meet-punten afgelezen; oorzakelĳke STRUCTUUT gemeten: de diagnostics-tak in app_broker.go riep DiagnosticsProject aan via een optionele interface-assertion van de concrete compose-provider; het veld kan dus leeg blijven zodra de return geen details produceert. De broker self noemt de dependency allang: server_run.go logt `dependency=openbao` / `dependency=runtime-executor`, en de /readyz body draagt veld `dependency` in server.go writeNotReady (LET OP: writeNotReady zet ALLÉÉN de naam, er is geen body-veld met waardegeheimen).
- (done) 3. Implementatie (CMD/BAHA/APP_BROKER.GO zelve, geen sperren aangeraakt): de diagnostics worden opgebouwd uit container-logtail (`LogsProject` op de brokerdienst) + de laatste /readyz-summary via het AL bestaande probe-kanaal (exec/curl in de package); beide afgekapt (`truncateDiagnosticTail`, bounded bytes op regel-grens), en de /readyz-samenvatting bevat uitsluitend name/status/version, NOOIT waardes. Geen nieuwe interface, geen produktsemantiek behalve deze diagnostiek.
- (done) 4. Test: cmd/baha/app_broker_diagnostics_test.go — `TestRuntimeBrokerReadinessFailureCarriesDependencyDiagnostics` rijgt de ECHTE failure-tak (failRuntimeBrokerReadiness, gedeeld codepad met de product-call): gemelde gezond-heid onhealthy + fixture logt/readyz → fouttekst moet de dependency NAAM noemen. Twee companiontests (probe-falure note, truncation-gedrag).
- (done) 5. build/vet/gofmt ok; source-readability-audit PASS; ci-fast-check 302 tests OK; commit `5d138ce2613169ea55db96478fdc6b14605fc06f`, push zonder force; PR #1763 draft tegen develop; delivery-witness `git ls-remote` (branch + refs/pull/1763/head) = `5d138ce261…`.
- (done) 6. Gehoste run `45005245380` terminal: **completed SUCCESS, failed 0** op de draft-route. CLI-suite uitgevoerd: cli-0 `137155287075`, cli-1 `137155287035`, cli-2 `137155286969`, cli-3 `137155287027`, packages `137155287076` (success). Test-bereikbaarheid = standaard cli-package-shards via `scripts/pr-go-unit-shard.py` (ontdekt in `./cmd/baha`) → de nieuwe test wordt hier uitgevoerd, zonder gate-uitbreiding nodig.
- (pending) 6b. BELEG-GAP (vraag aan coordinator, niet als groen verkopen): native docker EN podman jobs zijn op een DRAFT-skipped (`Native matrix 137155288612`, `Selected Runtime 137155288959`). Ready-schakelen is niet een lane-actie (mission: geen ready flip). Het gevraagde native-zeugnis is dus alleen te leveren na een owner/coordinator flip; in afwachting QUESTION.
- (pending) 7. Akte publiceren op plan origin/main.
- (pending) 8. Cleanliness + END aan coordinator 9142ab1f.

## Meetpunt van de diagnose (waarom: op acc34323968)

```text
cmd/baha/app_broker.go (ensureAndStartRuntimeBrokerWithCore falende tak, lines ~199-206): roept DiagnosticsProject via een optionele interface-assertie; wanneer die afwezig of teruggeeft als empty string blijft 'runtime diagnostics:' leeg, terwijl de afhankelijkheden al genoemd worden door server_run.go logs dependency=openbao/runtime-executor en internal/controlplaneruntime/server.go writeNotReady gezet als JSON 'dependency' naam.
```

Deze PR vult die tak door reeds bestaande kanalen als bronnen, zonder interface toe te voegen en zonder de twee gesperrde internal-bestanden of workflows te wijzigen. De diagnose zelf: logtail + /readyz naam, begrensd, geen credentials.

## Test-rigging

- `failRuntimeBrokerReadiness(...)` is exact het code-pad dat in `ensureAndStartRuntimeBrokerWithCore(...)` bij falen terugkeert: het project + `LogsProject` + `ExecProject` op de broker service. De fixture implementeert `runtime.RuntimeProvider` via embedden en beantwoordt de twee kanalen (logtail met `dependency=runtime-executor`, readyz-json met `dependency=runtime-executor`).
- Assertie: fouttekst bevat `dependency=runtime-executor` + beide kanaalkoppen ("broker container log tail:"/"broker /readyz (last):"); probe-falure geval noteert een uitdrukkelĳke melding; truncatie marker en bounded tail asserts.

## CI-toegang (missie: elk nieuwe test door een CI check)

- De nieuwe test heet `TestRuntimeBroker*` in package `./cmd/baha` en wordt daarmede gedekt door de `PR · Draft Go · cli-N` shards (script `scripts/pr-go-unit-shard.py` ontdekt alle testnamen in de package). De cli-shard rij liep en slaagde op de exacte kandidaat, zie job-ids boven.

## Provenance + witnesses

- Remote-URL eerste git-action: `git remote -v` (werkzone checkout URL `https://github.com/mcpdev80/basehar…`) — zie git -C config; de remote is github URL.
- Base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `acc34323968…` (voordat snit); branch is op die SHA; `git merge-base --is-ancestor acc343239681feb235a33cf00c8ea754c537291f HEAD` → yes.
- `git log --oneline acc34323968..HEAD` = precies 1 commit `5d138ce26` (van mij), geen fronder.
- `git diff acc34323968...HEAD --name-only` = `cmd/baha/app_broker.go`, `cmd/baha/app_broker_diagnostics_test.go` (twee pfade, geen SPERR-paden).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-240-broker-diagnostics refs/pull/1763/head` = beide `5d138ce2613169ea55db96478fdc6b14605fc06f`.

## REDELĲKE BEWĲS: native docker- en podman-job

- De missie: "BELEG is een natieve docker-UND-podman-job, whose output toont de dependency-naam (new job ids noemen)." Dit PR kan dit BELEG NIET produceen zonder de ready-flip: alle native/selected-checks zijn draft-skipped. De cli-shards zijn wel groen en voeren de package-unit tests (new testincluded), maar tonen niet de NATIVE runtime log met `dependency=runtime-executor` in de echte CLI error.
- Opties voor de coordinator (geen lane-actie): (a) ready-zetten van #1763 nu implementatie compleet is (review = handoff, ready flip = owner/coordinator-hand); (b) gemichte exception voor native gates op deze draft PR; (c) eenmalige targeted validation dispatch op een aparte workflow (Owner scope). Zonder één van deze kan het native BELEG niet geleverd worden en mag de kaart niet als volledig groen worden afgesloten.

## repo-rule compliance

- Write set: cmd/baha/app_broker.go + cmd/baha/app_broker_diagnostics_test.go. Geen productsemantiek behalve diagnostics, geen interface, geen `.github/**`, geen `scripts/**`; `internal/observability/registry.go` en `internal/capability/perses_selection.go` NIET aangeraakt.
- Geen ready flip, geen merge/close/comment. Geen subagents. Posten alleen aan 9142ab1f.

## cleanliness

cleanliness: nothing started. Eigen pid `3212762` (shell), host zonder daemon `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries (host heeft geen docker daemon; workzone gebruikt geen test-containers). Geen compose/netwerk/volume gestart. Cache onder `/var/tmp/go-cache-0428-240`.

END 0428-223-testctx BLOCKED (0428-240): branch lane-0428-240-broker-diagnostics, head `5d138ce2613169ea55db96478fdc6b14605fc06f`, PR #1763, run `45005245380` terminal completed SUCCESS, failed 0, native jobs `137155288612`/`137155288959` = SKIPPED op draft — BELEG vereist native docker EN podman met dependency-zeugnis, vereist ready-flip of exception (coordinator-hand). cleanliness: nothing started.
