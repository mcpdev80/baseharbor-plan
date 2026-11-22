# 0428-231 #1771 target.go provider-fix round-1 — local-docker/local-podman als lokaal in detectRuntimeForTarget

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: de ECHTE code-fix in
`cmd/baha/target.go` (detectRuntimeForTarget, ~:722) op branch
lane-0428-231-static-opauth-fix, na een additive hop naar develop
`484c95fc…`.

## PLAN

1. (done) Realiteit: origin=github URL (remote -v); ls-remote
   develop=`484c95fca938cb96736c4578906e6ea58bf043b8`; pull/1771/head = branch
   head = `ebd01baa…` (round-1 hop state); werktree
   workers/0428-231-opauthfix-wt clean; docker ps -a before=0, eigen pid 2072695.
2. (done) Hop: `git merge --no-ff origin/develop` → merge-commit `02cf8eac`
   (ouders: ebd01baa + 484c95fc), GEEN conflicten, geen force/rebase/amend,
   ANCESTOR-OK.
3. (done) Root meten: de guard was letterlijk
   `if access != "" && access != "local" -> ErrorCapabilityMissing`; de
   registry-/fixturevormen `local-docker`/`local-podman` (cmd/baha/target.go
   create-path, `--access local-docker`) vielen dus als REMOTE door de probe
   VOOR engine ownership, terwijl de sibling grant-path
   (local_workload_authority.go:34 isLocalRuntimeAccessProvider) juist
   `local` + `local-<runtime>` toelaat. Exactly zoals de missie stelde.
4. (done) FIX (alleen target.go): switch over de provider — `''`/`local` als
   voorheen; `local-docker` lokaal ALLEEN met runtime docker en
   `local-podman` lokaal ALLEEN met runtime podman (shared exacte
   provider-vs-runtime vergelijking tegen bhruntime.ProviderDocker/
   ProviderPodman); ALLE andere providers en elke mismatch houden exact
   dezelfde fail-closed machine.ErrorCapabilityMissing. Geen nieuwe
   session-binding en geen auth-contract wijziging — runtime-probe/engine
   ownership beslist daarna onveranderd (GEEN stop-val benodigd).
5. (done) Regression `cmd/baha/target_runtime_access_provider_test.go`
   TestDetectRuntimeForTargetLocalRuntimeAccessProviders: 9 subcases —
   local-docker/docker accepted, local-podman/podman accepted, `local`+`''`
   ongewijzigd accepted, en NEGATIES: baseharbor-node-connector,
   baseharbor-core, unknown, local-docker×podman, local-podman×docker
   allemaal ErrorCapabilityMissing. Lokaal 9/9 PASS in named+skip vorm
   (guard-only tests: start géén containers, host-schoon; de accepted-takken
   vallen door naar de gewone runtime-resolver). CI-home: `cli-package-tests`
   voert ./cmd/baha package tests uit via scripts/pr-check-runner.py:190-204
   (hosted, pull_request→develop); ci-fast-check rc=0. gofmt clean.
6. (done) ONE commit `b9dc3c31221b66038856a92f2c05225e0be53e83` op de hop,
   normal push; ls-remote branch-head en pull/1771/head beide = b9dc3c31.
   PR blijft OPEN/ready. Log origin/develop..HEAD toont alleen EIGEN
   0428-231 commits (de fix + de twee 0428-231 hops + de oorspronkelijke
   fix/hop-history van deze branch — geen vreemde tak).
7. (done) EXACT hosted rerun **45057170560** @b9dc3c31 terminal
   completed/failure. Job-statements:
   - Source format / Workflow policy / Native gate plan: EXECUTED success.
   - `PR · Trusted Plan` (137314858474) **failure — maar NIET door de
     provider-fix**: uncataloged-abort voor de TWEE bronnen die DEZE wijziging
     zelf in de PR-diff brengt: cmd/baha/target.go en
     cmd/baha/target_runtime_access_provider_test.go. Beide zijn op develop NOOIT
     cataloged geweest (gemeten: target.go state niet in de catalog). Het
     toevoegen van catalog entries is in deze opdracht VERBODEN
     ("KEIN catalog"), dus dit is een Coordinator-action buiten deze write-set
     (shared planner catalog): de twee paden (met dezelfde data-capabilities
     surfaces als de #1768/#1777 muster) moeten in scripts/pr-gate-coverage.json
     voordat welk gehopte #1771-draait dan ook groen kan worden. Gemeld.
   - native data-capabilities jobs (docker 137314894493, podman 137314894310)
     failure: TestApplicationCapabilityLifecycleExistingCore/secrets vraagt
     `--confirm-candidate 86c62ede…` — DEZELFDE candidate-consent grens als bij
     de Option-A/#1783 en #1771-hop metingen; géén 'has no authenticated live
     runtime binding' / ErrorCapabilityMissing regel meer in de cel-log
     (grep: provider-reject tekst = afwezig; de grant loopt nu door tot de
     consent-grens). Selected Runtime jobs worden door GitHub gemengd; de
     cell-logs (indien bereikbaar) zijn via de native parents beoordeeld.
   -> 'local-docker/local-podman grant accepted im probe: ja' (de grant
      passeert de provider-guard en botst ná de probe op de consent-grens;
      de provider-reject text is uit de cellen verdwenen) — definitief
      aantoonbaar zodra Trusted Plan (catalog entries) weer sluit.
   -> 'remote/unknown fail-closed: ja' (9/9 unit asserts + gelijke guard in
      beide runs).
8. (done) Akte + ls-tree-witness op plan origin/main.
9. (done) Cleanliness + END.

## Provenance

- base attestation: ls-remote develop = `484c95fca938cb96736c4578906e6ea58bf043b8`
  gemeten vóór de hop; merge `02cf8eac` heeft het als tweede ouder; de
  fix-commit `b9dc3c31` is ANCESTOR-OK van/bovenop die hop.
- `git log --oneline origin/develop..HEAD` na de push = 1771-tak commits
  (172fb251 fix, 965c1135 hop, dc775235 chore-hop, ebd01baa hop-both,
  02cf8eac deze hop, b9dc3c31 deze fix) — alle 0428-231 work van deze
  card-chain (de eerdere hops zijn door de vorige missie bevolen), geen
  vreemde kandidaten.
- `git diff origin/develop...HEAD --name-only` = local_workload_authority
  (origionele #1771 fix + test), main.go, target.go + de nieuwe test — alle
  binnen de 0428-231 contracts.
- delivery: ls-remote refs/heads/lane-0428-231-static-opauth-fix en
  refs/pull/1771/head = `b9dc3c31221b66038856a92f2c05225e0be53e83`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Write-set: alleen cmd/baha/target.go + zijn regression test, en de bevolen
  additive hop. GEEN .github, GEEN 237, GEEN #1783/#1761/#1770 content, GEEN
  catalog-json. Geen product contract-wijziging buiten de provider-kwestie
  (punt 4); geen stop-val benodigd. Geen merge/kommentaar door deze lane; PR
  state OPEN/ready gelaten. Geen subagenten. Geen containers op deze host
  (guard-only tests; named+skip vorm gebruikt).

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 2072695), AFTER = 0 entries
(pid 2140721). Geen compose/container gestart op deze host. Onbedoelde `baha`
build-resten verwijderd; scratch /var/tmp/0428-223-fc-tg.log, -tp1771b.log,
-np1771b.log vóór END verwijderd. Werktree 0 delta na commit.

END 0428-223-testctx DONE — 0428-231 target.go provider-fix round-1 op #1771: NIEUWE HEAD b9dc3c31221b66038856a92f2c05225e0be53e83 (additive hop 02cf8eac op exact develop 484c95fc + fix-commit, ls-remote branch+pull bewezen), exact hosted rerun 45057170560 terminal; 'local-docker/local-podman grant accepted im probe: ja' (provider-reject tekst verdwenen uit de cellen; cel stopt nu bij de candidate-consent grens), 'remote/unknown fail-closed: ja' (9/9 asserts); Trusted Plan faalt uitsluitend omdat cmd/baha/target.go + de nieuwe test NIET in scripts/pr-gate-coverage.json staan en catalog-json hier verboden was — Coordinator-action buiten deze write-set (met data-capabilities muster). native :edge/#1770 en demo-consent/#1783 blijven gescheiden, alleen status gemeld. cleanliness: besenrein

## origin/main witness

Exacte uitvoer van `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 1771-target-go-provider` (plan main = 70ed50d7a65715aeb833bf8e2232506601e3aea9):

```
evidence/r28-welle5-2026-11-22/static-cells-operator-auth-0428-231/1771-target-go-provider-round-1.md
```
