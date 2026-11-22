# 0428-241 #1783 app-new admission round-1 — narrow tagged-fixture fix (develop 978a0f90)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: de owner-diagnose landen in
de smallste Fix: het build-tagged test-only fixture `app new` (exact
kanonische args) toelaten onder `gate == "data-capabilities"`, regression
erbij, nieuwe head + exact hosted. Re-hop later apart; niets verder gedaan.

## PLAN

1. (done) Realiteit: origin=github URL (remote -v); ls-remote
   develop=`978a0f90b512e98300ee30b5aa2a1cae5d628b21` — "catalog #1771's
   target.go + target_runtime_access_provider_test.go … (#1786)" (gemerged,
   als voorspeld); branch EN pull/1783/head = `2da7f565…`; werktree
   workers/0428-241-optawt clean; docker ps -a before=0, eigen pid 2227297.
2. (done) Root gemeten in het fixture: `ciIntegrationGuidedAppNew(args)`
   admitted alleen bij `gate == "guided"` (regel ~129), arg-match exact
   `len(args)==2 && args == app,new` (:235-237). Precies als gesteld.
3. (done) Additieve hop naar origin/develop 978a0f90 (merge --no-ff, tweede
   ouder = develop-head, geen force/rebase/amend): merge-commit `c8b8da85`,
   ANCESTOR-OK. (Verdere re-hops volgen separaat, hier NIET gedaan.)
4. (done) NARROW FIX in alleen het tagged fixture-bestand: extra tak
   `gate == "data-capabilities" && ciIntegrationGuidedAppNew(args)` met
   DEZELFDE exact kanonische args-match — geen ruimere match, `app edit`
   blijft guided-only, footprint-show (:135) NIET aangeraakt (ons eigen
   rerun-log toonde géén selected footprint-show consent-fail), GEEN
   productcode, GEEN --confirm-candidate/demo, GEEN 247, GEEN baseharbor-demo.
5. (done) Regression `TestCIIntegrationOperatorDataGateAppNewAdmission`:
   (a) canonical `app new` onder docker+podman data-capabilities -> admitted
   (geen interactive-OIDC fallthrough), (b) noncanonical (`app new --yes`,
   `app new extra`, `app edit`) -> DENIED binnen die gate, (c) andere gates
   (core-capability, lifecycle, observability) -> `app new` blijft DENIED
   (guided unchanged). Geen blanket-allow; product fail-closed intact.
   Seam-suite volledig OK in named+skip vorm; gofmt clean; ci-fast-check rc=0.
   CI-home: ci-integration-operator-seam-tests (ci.yml:1328).
6. (done) ONE commit `8b99bdc3c615f29a788e4800e50a685a8099be9a` bovenop de
   hop (NIEUWE head, niet 2da7f565); normal push; ls-remote branch-head EN
   pull/1783/head = 8b99bdc3; PR blijft OPEN/ready.
7. (done) EXACT hosted run **45061359667** @8b99bdc3 terminal
   completed/failure — maar de TAAKSTEL van deze missie IS aangebracht:
   - Trusted Plan 137327788426, Source format, Native gate plan, Workflow
     policy, Focused Python, Runner Interface, Exact Candidate,
     source-contracts, Demo Pin, cli-vet/build/guided-tests en
     **ci-integration-operator-seam-tests 137327855366 EXECUTED+success**
     (regression draait hosted).
   - Selected docker data-caps cell 137328292265 trace:
     `decision=managed-local-gate command="app new"` op
     atomic-docker-data-capabilities — app new wordt nu ADMITTED (in
     eerdere runs viel dit door en gaf de interactive-auth PTY timeout);
     `app edit` blijft daar correct REJECTED (guided-only). Native broker:
     `[OK] Starting secure runtime broker - done (13.7s)` — de :edge
     broker-stap faalde NIET in deze cel-run (anders dan eerdere rondes).
   - De cel blijft rood door de reeds bekende demo/consent-laag: de
     demo-driver-stap `new-edit-new-sql-cancel` gooit
     `Error: record deployment before mutation: candidate submission
     requires an explicit operator/automation consent
     (--confirm-candidate) …` gevolgd door
     `RuntimeError: new-edit-new-sql-cancel exceeded no-output timeout`.
     Dat is het apply/digest-pad dat buiten deze opdracht blijft (demo-repo,
     apart gemeld); onze `app new`/`app edit`/footprint-admissions zijn hier
     exact zoals de missie ze snijdt.
   - Podman cell + native jobs (137327828176/137327828248) analog rood —
     native :edge = waiting-#1770, niet defect.
   -> 'selected app-new admitted data-caps: JA' (direct uit de
      trace-regel); cel groen: NEIN (demo-consent laag, aparte kaart).
8. (done) Akte + ls-tree-witness op plan origin/main.
9. (done) Cleanliness + END.

## Provenance

- base attestation: ls-remote develop = `978a0f90b512e98300ee30b5aa2a1cae5d628b21`
  vóór de hop; merge `c8b8da85` heeft het als tweede ouder; fix-commit
  `8b99bdc3` daarboven — ANCESTOR-OK naar beide.
- `git log --oneline origin/develop..HEAD` na de push = alleen ONZE 0428-241
  chain commits (8f84fcbd, 2da7f565, hop c8b8da85, fix 8b99bdc3) — geen
  vreemde kandidaten.
- `git diff origin/develop...HEAD --name-only` = alleen de twee tagged-
  fixture-bestanden.
- delivery: ls-remote refs/heads/lane-0428-241-optionA-operator-allowlist en
  refs/pull/1783/head = `8b99bdc3c615f29a788e4800e50a685a8099be9a`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Write-set: alleen het tagged fixture + zijn test (missie). GEEN
  productcode/consent-boundary, GEEN --confirm-candidate/demo, GEEN
  baseharbor-demo, GEEN 247, GEEN .github, GEEN catalog; footprint-show
  niet aangeraakt (criterium gecontroleerd op ons eigen rerun-log). Geen
  merge/kommentaar door deze lane; PR status ongewijzigd (bestaand, ready).
  Geen subagenten; geen containers op deze host; named+skip testvorm.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 2227297), AFTER = 0 entries
(pid 2278802). Geen compose/container gestart op deze host. Onbedoelde
`baha` build-resten verwijderd; scratch /var/tmp/0428-223-fc-an.log en
-sel-dk.log vóór END verwijderd. Werktree workers/0428-241-optawt 0 delta.

END 0428-223-testctx DONE — 0428-241 #1783 app-new narrow admission round-1: branch lane-0428-241-optionA-operator-allowlist NIEUWE HEAD 8b99bdc3c615f29a788e4800e50a685a8099be9a (additive hop c8b8da85 op exact develop 978a0f90 + fix-commit; ls-remote branch+pull/1783 bewezen; niet 2da7f565), EXACT hosted run 45061359667 terminal; 'selected app-new admitted data-caps: JA' — trace `decision=managed-local-gate command="app new"` in de selected docker cell, app edit blijft correct denied, broker [OK] (13.7s), seam-tests 137327855366 hosted success incl. TestCIIntegrationOperatorDataGateAppNewAdmission; cel wordt nog rood door de aparte demo-consent laag (new-edit-new-sql-cancel --confirm-candidate, buiten deze opdracht, reeds gemeld); native :edge = waiting-#1770 niet defect; 'remote/other-gates fail-closed: ja'. cleanliness: besenrein

## origin/main witness

Exact: `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 1783-appnew-admission` (plan main = 4f82ebe889556fb37235ad493d43e80136a8df1b):

```
evidence/r28-welle5-2026-11-22/guided-fixture-footprint-contract-divergence-0428-241/1783-appnew-admission-round-1.md
```
