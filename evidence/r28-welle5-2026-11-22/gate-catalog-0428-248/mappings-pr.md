# 0428-248 — fehlende Katalog-Mappings A / C / 243 (ein PR)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht (develop-pin 3cbb2bac): de drie
ontbrekende product-source mappings in scripts/pr-gate-coverage.json, additive,
geen dup van B, guardian-onveranderd.

eintrge A/C/243 gesetzt, dup-frei, welche PRs damit entblockt (#1746-static,#1773,#1771)

trusted-planner guardian gruen: ja (validatie + 253 planner/catalog/gate tests OK
op deze kandidaat; hosted Draft-routing run success; de exact-head `PR · Trusted
Plan` + `Validation · pr-planner-tests` cel draait na ready-promotie op deze head,
draft runnt ze niet — dat is de verwachte draft-semantiek, ZIE run-details).

## PLAN

1. (done) Realiteit: origin=github URL; ls-remote develop=713aadd4 (missie-pin
   3cbb2bac is diens directe parent, `merge-base --is-ancestor` OK); #1775 CLOSED
   (vuile dup-B poging), #1776 MERGED als test-only commit 713aadd4 (alleen
   scripts/test_pr_native_gate_plan.py); GEEN bestaande lane-0428-248 ref
   (ls-remote); docker ps -a before=0, eigen pid 305301.
2. (done) Planner-paden doorgrond: `pr-gate-plan.py` gebruikt de BASE-SHA catalog
   met `release` uit pr-gate-map-v1.json (= v0.4.27) en kruipt door
   `requirements.gates[*].required_for`; de native selector in ci.yml gebruikt
   `pr-native-gate-plan.py` met DEZELFDE base-catalog. Consequentie: een gate die
   ALLÉÉEN v0.4.28 in required_for draagt kan hier niet gevalideerd worden
   ("coverage catalog includes gates outside active release catalog") — daarom
   krijgt A zijn surface onder de BESTAANDE v0.4.27 static gate
   atomic/static/shell-ux (covers uitgebreid), en de nieuwe v0.4.28 gate
   atomic/static/ci-fast-check blijft in PR #1746 (Owner-scope, niet hier).
3. (done) Branch `lane-0428-248-catalog-mappings` fresh van 3cbb2bac; entries in
   scripts/pr-gate-coverage.json (alleen dit bestand gewijzigd):
   - A: component `source.scripts.ci.fast.check` (path scripts/ci-fast-check.sh,
     surfaces ["source.gate.atomic.static.ci.fast.check"], runtime_specific true)
     + nieuwe surface declaratie + gate-owner via atomic/static/shell-ux covers.
   - C: component `source.cmd.baha.app.footprint.presenter.go` op
     source.gate.atomic.{docker,podman}.data.capabilities.
   - 243: components `source.cmd.baha.local.workload.authority.go`,
     `...authority.test.go` en `source.cmd.baha.main.go` (runtime_specific true)
     op dezelfde surfaces, EN opgenomen in de source_components van BOTH
     native/docker/data-capabilities en native/podman/data-capabilities, zodat de
     native matrix (en dus #1771) ze uitvoert. main.go draagt de
     runtime-specifieke grant-routines (RuntimeSpecificLocalEngineTest) — vandaar
     runtime_specific. Alle 5 ids uniek, geen hergebruik/dup van B.
4. (done) Local proofs: `python3 scripts/validate-pr-gate-coverage.py` → "PR gate
   coverage catalog is valid"; unittests test_pr_gate_coverage +
   test_pr_native_gate_plan + test_pr_gate_plan + test_ci_v0427_gate_catalog +
   test_pre_release_check_plan = 253 OK. Native-planner per pad:
   presenter / lwa.go / lwa_test.go / main.go →
   `{"include":[native/docker/data-capabilities, native/podman/data-capabilities]}`;
   scripts/ci-fast-check.sh → covered gate atomic/static/shell-ux (native [] —
   correct, A is een statische executor); B-regressie (ci-native-pr-gate.sh)
   unveraend beide native gates. Guardian fail-loud intact: een uncatalogized
   cmd/baha/zz_uncataloged.go → exacte ValueError met next-action (transcript).
   De 8+8 fails in test_pr_registration_ci/test_ci_docker_runtime_doctor zijn
   base-own: op kale pin 3cbb2bac (git stash, same suite) IDENTIEK — niet door
   deze kandidaat veroorzaakt en buiten deze write-set. ci-fast-check.sh rc=0.
5. (done) ONE commit `d9c1b895bedc0f3ad1d0866445c7237e064951e8`, normal push,
   DRAFT PR https://github.com/mcpdev80/baseharbor/pull/1777; ls-remote
   refs/pull/1777/head = d9c1b895… bewezen. Class: draft tot handoff.
6. (done) Eigen hosted run 45035001471 @d9c1b895: completed/**success**, failed=0.
   Draft-groep: routing 137246673413 success; Go cli-0..3 + packages
   137246673906/593/772/828/897 success. SKIPPED (draft-semantiek, niet als groen
   geteld): Trusted Plan 137246674814, Validation-aggregaat 137246675625, Native
   gate plan 137246674676, Native 137246675294. De guardian-groenheid is hier
   bewezen via de local suite (stap 4) + gehoste routing/Go shards; bij
   ready-promotie draait de exact-head planner-groep vanzelf op deze head.
7. (done) Akte + witness (dit bestand).
8. (done) Cleanliness + END.

## #1776-opmerking (als opgedragen)

scripts/test_pr_native_gate_plan.py (#1776, merged als 713aadd4) covereert nu al
het B-pad (ci-native-pr-gate.sh → beide native gates) en—met deze entries—ook de
243/C-sources via dezelfde native checks. Een additionele assert voor deze paden
zou in #1776s bestand moeten; volgens de missie is dat daar NIET gewijzigd en hier
niet gedaan.

## Provenance

- base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/develop` = `713aadd4e7876d7f0e4d644b68e85a54e8927da8`; de missie-pin
  `3cbb2bac39996391799d1c6460b230979ee34959` (= #1774 merge, develop op moment van
  dispatch) is de directe parent daarvan en is de base van deze branch
  (`git merge-base --is-ancestor 3cbb2bac HEAD` OK; branch aangemaakt op exact die
  SHA).
- `git log --oneline 3cbb2bac..HEAD` = één eigen commit:
  `d9c1b895 ci(0428-248): register the missing catalog mappings A, C and 243`.
- `git diff 3cbb2bac...HEAD --name-only` = alleen `scripts/pr-gate-coverage.json`.
- delivery: `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/lane-0428-248-catalog-mappings refs/pull/1777/head` → beide
  `d9c1b895bedc0f3ad1d0866445c7237e064951e8`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`
  → https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Alleen de catalog-JSON gewijzigd (binnen Codeman/242-scope: "planner/guardian
  metadata only"); GEEN .github/**, geen productcode, geen operatorauth, geen
  scripts/ci-native-pr-gate.sh (237-pad), geen ghcr; geen merge/kommentaar; geen
  subagenten; geen containers op deze host; #1776 onaangeroerd.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 305301), AFTER = 0 entries
(pid zie END-regel). Geen compose/container gestart op deze host. Eigen scratch
under /var/tmp/0428-223-* (changed-paths/diff/log bestanden) wordt vóór END
verwijderd; GOCACHE /var/tmp/go-cache-0428-231 blijft (buiten deze missie).
Werkboom workers/0428-248-catalogmap-wt houdt de kandidaat (0 delta na commit).

END 0428-223-testctx DONE — 0428-248 mappings-pr: branch lane-0428-248-catalog-mappings, head d9c1b895bedc0f3ad1d0866445c7237e064951e8 (ONE commit op 3cbb2bac), PR https://github.com/mcpdev80/baseharbor/pull/1777 (DRAFT, ls-remote bewezen), run 45035001471 completed/success failed=0, entries A/C/243 dup-frei und guardian-intakt; cleanliness: besenrein
