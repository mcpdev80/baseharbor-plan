# 0428-240 redaction-round-1 — diagnostics: fixed text plus validated names only

Sicherheitbefund (unabhaengige read-only-pruefung, vom coordinator aus dem diff bestaetigt): `'readyz body is not valid JSON: ' + truncateDiagnosticTail(out, 200)` in cmd/baha/app_broker.go schrieb bei einem NICHT-JSON body den ROHEN koerperteil (bis 200 Zeichen) in den fehlertext. Der /readyz-pfad ist aktiv am secure-runtime broker; ein roher koerperteil kann wertetrager enthalten. Genau das verbietet die sicherheitsregel.

## PLAN

- (done) 1. ls-remote + base-abgleich: refs/heads/develop = `8629450ef3c5198bb675331c12f56b2c9377aa1c` (wie in der mission genannt); alter head `5d138ce26` base 52a3c…/acc343… — rueckstand, daher ADDITIV gehopft: `git merge --no-ff 8629450ef3c` -> merge-commit b38838e1c, KEIN rebase/amend/force.
- (done) 2. redaktion: (Zeile der mission) — der fehlertext traegt jetzt NIE einen rohen body oder teil davon: ausgabe nur feste texte plus der NAME der dependency (validated gegen die vertragliche wortliste openbao/runtime-executor/database, sonst 'unknown'), plus version/commit wenn sie eine strenge build-tokenklasse erfuellen; 'body ist kein JSON' meldet nur die KOERPERLAENGE als zahl (`body-length=%d`), nie inhalt. Der container-log-tail-pfad derselben datei wurde auf dasselbe muster geprueft und begrenzt:Zeilenanzahl plus whole-token-Nennung der festen dependency-wortliste (`logMentionsDependency`), keine rohe zeile; der exec-error-pfad gibt nur noch die feste meldung 'readyz probe failed (error detail redacted by security rule)'. `truncateDiagnosticTail` ist mit dem letzten aufrufer entfernt.
- (done) 3. marker-test aktiv: `TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker` in cmd/baha/app_broker_diagnostics_test.go — vier faelle mit ausgedachtem wert-markierer `token=abc123` (non-JSON body, unbekanntes JSON-field, log-stream, hostile dependency value): der markierer darf NICHT in der ausgabe erscheinen, die sichere dependency-NAAM muss es aber; zusaetzlich generic key=value-scan. Kein kommentar, eine echte assertion. Der probe-failure-test assertiert jetzt ebenfalls die abwesenheit des raw-error-details.
- (done) 4. push normal auf lane-0428-240-broker-diagnostics, base develop 8629450ef3c, additiv gehopft; delivery-witness `git ls-remote` branch = refs/pull/1763/head = b38838e1c30d18eabe3fa7e8e64c6c053c576bce.
- (done) 5. Gehoster durchgang 45008350091 terminal: **completed SUCCESS, failed 0** am neuen head. Der alte durchgang 45005245380 zaehlt nicht (nur draft-route; native reihen nie ausgefuehrt).
- (done) 6. Diese akte auf plan origin/main + ls-tree-witness.
- (pending) 7. END post aan 9142ab1f.

## redaktion:

redaktion: roher body/log/exec-fehler wird NIE mehr in den fehlertext geschrieben; ausgabe = feste texte + validierte dependency-NAAM (closed set) + status aus closed set + version/commit nur bei build-tokenklasse + koerperlaenge als zahl im nicht-JSON-fall; container-logtail = zeilenzahl + whole-token dependency-Nennung, kein inhalt.

## Provenance + witnesses

- Remote erster git-action: `git remote -v` -> `https://github.com/mcpdev80/baseharbor.git` (URL, name aufgelöst).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = 8629450ef3c5198bb675331c12f56b2c9377aa1c (FETCH_HEAD exakt, vor dem hop); `git merge-base --is-ancestor 8629450ef3c HEAD` -> yes (am finalen head).
- `git log --oneline develop..HEAD` (gegen 8629450) = 5d138ce26 (round-1), 87fce2a1c (redaktion), b38838e1c (additiver merge-commit) — alle von mir, kein fronder kandidat on top.
- `git diff 8629450ef3c...HEAD --name-only` = `cmd/baha/app_broker.go`, `cmd/baha/app_broker_diagnostics_test.go`; KEIN internal/**, KEIN .github/**, KEIN scripts/** (STOP-Kriterium nicht bertroffen — die redaktion passte vollstaendig in cmd/baha).
- Nach push: `git ls-remote … refs/heads/lane-0428-240-broker-diagnostics refs/pull/1763/head` = beide `b38838e1c30d18eabe3fa7e8e64c6c053c576bce`.

## Gehostete runs

- run 45008350091 (pull_request, head b38838e1c): completed SUCCESS, failed 0; executed jobs: source-and-routing 137164862889, cli-0 137164863124, cli-1 137164863204, cli-2 137164863115, cli-3 137164863161, packages 137164863193. Die neue marker-test liegt in ./cmd/baha und laeuft in den cli-shards (scripts/pr-go-unit-shard.py discover + named run).
- Alter durchgang 45005245380 zaehlt laut mission NICHT (draft-route, 6 success / 27 skipped, native nie ausgefuehrt). Die native docker/podman dependency-zeugnis-req (round-1 punkt 6b) bleibt offen am ready-flip (owner/coordinator hand); diese korrekturronde aendert daran nichts — kein ready-schalten durch die lane.

## Checks lokal (Vorpruefung, kein ersatz fuer hosted)

- go build/vet ok; gofmt 0; named runs `go test ./cmd/baha/ -count=1 -run 'TestRuntimeBrokerReadiness' -skip "RunsRealLifecycle|…"` ok (alle subtests green, marker feld); ci-fast-check.sh rc=0 (302 tests OK) VOR dem push.

## repo-rule compliance

- Write set: cmd/baha/app_broker.go + cmd/baha/app_broker_diagnostics_test.go (dieselben zwei dateien wie round-1). Kein internal/**, kein .github/**, kein scripts/**, kein interface, keine produkt-semantik ausser der diagnostics-ausgabe selbst. Kein merge/close/kommentar, keine subagenten, posten nur an coordinator. PR bleibt DRAFT.

## cleanliness

cleanliness: nothing started. Eigen pid 3461392. `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries. Keine container/netzwerke/volumes; scratch `/var/tmp/0428-240-fastcheck*.txt` (removed at END), GOCACHE=/var/tmp/go-cache-0428-240; worktree workers/0428-240-brokerdiag-wt (Lane-Zone).

## plan-repo remote witness

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (erste zeile):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
```

END 0428-223-testctx DONE (0428-240 redaktion: branch lane-0428-240-broker-diagnostics, head b38838e1c30d18eabe3fa7e8e64c6c053c576bce, base 8629450ef3c (additiv gehopft), PR #1763, run 45008350091 completed SUCCESS failed 0, marker-test aktiv (TestRuntimeBrokerReadinessDiagnosticsNeverEchoesValueMarker, 4 case), cleanliness: nothing started)

## origin/main evidence witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep redaction-round-1`:

```
evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/redaction-round-1.md
```
