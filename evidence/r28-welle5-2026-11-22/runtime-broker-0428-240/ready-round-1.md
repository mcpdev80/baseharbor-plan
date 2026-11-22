# 0428-240 ready-round-1 — ready-flip on owner instruction; native/selected gates still not executed

Owner-anweisung (ready1763.md.g): der draft-stand von PR #1763 soll fallen, damit die nativen und policy-/validierungs-gates wirklich laufen. Reihenfolge wie befohlen.

## PLAN

1. (done) ls-remote + PR-state-afgelĳk vóór de aktie: head/branch = `b38838e1c30d18eabe3fa7e8e64c6c053c576bce`, develop = `8629450ef3c5…`, draft=true, state=OPEN, mergeStateStatus=CLEAN. Geen lokale aenderungen; docker ps -a BEFORE = 0 (pid 3568594).
2. (done) `gh pr ready 1763 --repo mcpdev80/baseharbor` ausgefuehrt — die einzige staat-aktie dieser mission ("is marked as ready for review"). Kein merge, kein close, kein kommentar, kein label.
3. (done) PR-state gegengelezen: `state=OPEN, isDraft=false, mergeStateStatus` = BLOCKED direkt na de flip, later CLEAN. Delivery-witness `git ls-remote`: refs/pull/1763/head = refs/heads/lane-0428-240-broker-diagnostics (toen b38838e1c, nu c698d1310).
4. (done) Eerste doorloop na de flip: run `45009251403` (head b38838e1c) terminal completed SUCCESS, failed 0. De vier reihen: nativ docker = NIET EXECUTED (rij `PR · Native · ${{ matrix.id }}` job 137167703522 = SKIPPED, keine docker-/podman-cellen), nativ podman idem, selected docker (`PR · Selected Runtime` 137167725468 = SKIPPED), selected podman (`PR · Selected Core-less` 137167725023 = SKIPPED). Policy-/validierungs-gates liepen wél: Workflow policy, Source format, Trusted Plan, Native gate plan 137167667713 success, Validation go-vet/go-build/cli-gofmt success, Go-unit cli-0..3 + packages + owner success, PR Selected Checks 137168689277 success.
5. (done) Oorzaak gemeten, nicht behaupten: `PR · Native gate plan` SUCCESS but its plan output is `matrix='{"include":[]}'` — empty selection, therefore the native matrix jobs are skipped (skipped ist kein beleg). Local replay against the trusted catalog: my changed paths `cmd/baha/app_broker.go` + `cmd/baha/app_broker_diagnostics_test.go` have NO component rows in scripts/pr-gate-coverage.json (resolve by exact path; the 190-component catalog lists the data-capabilities gate's source_components as `source.cmd.baha.app.*` files + `cmd.baha.*_test` — not app_broker). This is the same catalog-gap finding shape as 0428-230/235 (empty native matrix because the touched paths map nothing). Needed change (Owner scope, file:line): add component rows for path `cmd/baha/app_broker.go` (and the new test file) with surfaces `source.gate.atomic.docker.data.capabilities` + `source.gate.atomic.podman.data.capabilities` in `scripts/pr-gate-coverage.json` (component list), and reference them from `native_checks` rows `native/docker/data-capabilities` / `native/podman/data-capabilities` (source_components arrays). Until then NO PR that edits only app_broker can ever execute the native data-capabilities jobs, so the dependency-name receipt cannot be produced from this lane alone.
6. (done) Second candidate on the same branch: while the flip exposed the gap I found and fixed a redaction edge the round-1 tests did not cover — a NON-JSON /readyz body previously reported only `body-length=<zahl>` with NO status signal at all. New variant reports `status=unknown` alongside the length (fixed phrase; number only), and the marker-test gained the case "body IS the marker" (5 cases now, all pass locally; run for the old head does not count as the receipt of the new head). Commit `c698d1310` ADDITIV (kein rebase/amend/force), ci-fast-check rc=0 (302 tests OK), push ohne force.
7. (done) Tweede doorloop: run `45011815553` (head c698d1310) terminal completed SUCCESS, failed 0. De vier reihen opnieuw: nativ docker 137175608612 SKIPPED, nativ podman (zelfde rij, geen cellen) SKIPPED, selected docker 137175634681 SKIPPED, selected podman-coreless 137175634905 SKIPPED; Native gate plan 137175578131 success met weer lege matrix; PR Selected Checks 137176892351 success.
8. (done) dependency-fund: GEEN native data-capabilities-regel beschikbaar op deze kandidaten — de rijen zijn nooit ausgefuehrt (lege native-matrix door catalog-gap, punt 5). De eenige uitvoerbare bewĳzen zijn de unit-shards, en daar bewijst de marker-test dat de dependency-NAAM in de fouttekst staat en raw body/log/exec-INHOUD niet. Dit is een resultat (de mission zegt: 'blijft het bij body-length, dat is een resultat'), geen verborgen falen.
9. (done) Akte + publicatie op plan origin/main met ls-tree-witness (checklist-regel: deze akte gebruikt genummerde lijsten, geen checkbox-zeilen).
10. (pending) END post aan 9142ab1f.

## Zeilen (plichtformaat)

- PR state: OPEN, isDraft=false, mergeStateStatus=CLEAN (tegengelezen na flip en na tweede push).
- neuer head: `c698d1310ed5a2d5178affb956ba8af2051d0a5b` (b38838e1c + additieve correctie c698d131; hop naar develop was al binnen b38838e1c, develop staat nog op 8629450ef3c).
- run-id: 45011815553 — terminalstatus: completed SUCCESS — failed-zahl: 0.
- vier job-ids/reihen: nativ docker/podman = `PR · Native · ${{ matrix.id }}` 137175608612 (skipped, matrix leeg); nativ keycloak/core 137175634276 (skipped); selected docker = `PR · Selected Runtime` 137175634681 (skipped); selected podman = `PR · Selected Core-less · ${{ matrix.runtime }}` 137175634905 (skipped). Eerste doorloop idem: 137167703522 / 137167724542 / 137167725468 / 137167725023.
- dependency-fund: in de unit-shards (run 45011815553, Go-unit cli-shards) faalt `TestRuntimeBrokerReadinessFailureCarriesDependencyDiagnostics` als de naam verdwijnt en faalt `…NeverEchoesValueMarker` als `token=abc123` terugkeert — beide success; de NATIVE data-capabilities-regel die de woordelijke CLI-fouttekst zou tonen is nooit ausgefuehrt (catalog-gap, punt 5) en wordt hier NIET als groen verkocht.

## benodigde owner-aktie (file:line)

- `scripts/pr-gate-coverage.json`: component-rij voor `cmd/baha/app_broker.go` toevoegen (path + surfaces atomic.{docker,podman}.data.capabilities, runtime_specific true) en diens id opnemen in `native_checks[native/docker/data-capabilities].source_components` en `native/podman/…`; idem voor `cmd/baha/app_broker_diagnostics_test.go`. scripts/** is Owner-scope; de lane heeft niets geaendert en meldt dit als finding, niet als omweg.

## Provenance + witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1763/head refs/heads/lane-0428-240-broker-diagnostics` → develop 8629450ef3c / pull-head c698d1310 / branch c698d1310 (laatst gemeten, in akte).
- `git merge-base --is-ancestor 8629450ef3c HEAD` → yes (base-behind=0).
- `git log --oneline develop..HEAD` → 5d138ce26, 87fce2a1c, b38838e1c (merge), c698d131 — alle van deze lane, geen vreemde kandidaat.
- `git diff 8629450ef3c...HEAD --name-only` → `cmd/baha/app_broker.go`, `cmd/baha/app_broker_diagnostics_test.go` (alleen deze twee; scripts/** en .github/** NIET geraakt).

## repo-rule compliance

- Write set: alleen de twee cmd/baha-bestanden. De flip zelf was de enige staat-aktie die de missie toestond. Geen merge/close/kommentar/label, geen subagenten, geen workflow-wijzigingen. Gepost alleen aan coordinator 9142ab1f.

## cleanliness

cleanliness: nothing started. Eigen pid 3568594. `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries. Geen container/netwerk/volume; scratch `/var/tmp/0428-240-fastcheck*.txt` + nativeplan-logs verwijderd voor END; GOCACHE=/var/tmp/go-cache-0428-240; worktree workers/0428-240-brokerdiag-wt (Lane-Zone).

END 0428-223-testctx DONE (0428-240 ready-flip: PR #1763 isDraft=false, head c698d1310ed5a2d5178affb956ba8af2051d0a5b, run 45011815553 completed SUCCESS failed 0; native docker/podman + selected docker/podman = SKIPPED (lege native-matrix door catalog-gap, file:line in akte); dependency-fund via unit-shards (marker-test geactiveerd, 5 case); cleanliness: nothing started)

## origin/main evidence witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep runtime-broker-0428-240`:

```
evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/ready-round-1.md
evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/redaction-round-1.md
evidence/r28-welle5-2026-11-22/runtime-broker-0428-240/review-1763-headb38838e1c30.md
```
