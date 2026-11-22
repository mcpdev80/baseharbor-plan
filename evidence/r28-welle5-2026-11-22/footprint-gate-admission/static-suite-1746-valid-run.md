# 0428-223-testctx — PR #1746 static-suite: the valid run is 44987381250 (ref=lane branch)

ungueltig: 44986797647 (ref=develop, gates skipped) — this run used develop's workflow file, six static matrix gates SKIPPED there, cli-3 died on 'zsh: executable file not found'. It must not appear as proof in any akte or PR evidence.

gueltig: 44987381250 — workflow_dispatch of 'Release · Pre-Release Validation' with workflow ref `lane-0428-208-static-release-gate`, exact head `eb2e471a8fdff3233254043782fd805698d9a798` (= refs/heads/lane-0428-208-static-release-gate, observed equal to refs/pull/1746/head).

## PLAN

- (done) 1. ls-remote + run witnesses: branch head = kandidaat eb2e471a8fd; run 44987381250 headSha exact
- (done) 2. Run 44987381250 gevolgd tot terminal: completed FAILURE
- (done) 3. Job-tabel met alle 6 statische gates; GEEN enkele SKIPPED (2 success, 4 failure) — overige skipped jobs zijn niet-uitgekozen runtime-matrix, niet de statische suite
- (done) 4. cli-3 in deze suite: job success, shells stap success; per-test 'ok'-regel wordt door de shard-runner niet geprint (file:line hieronder)
- (done) 5. Akte + verwijzing dat de PR-beschrijving uitsluitend 44987381250 noemt (edit is Owner-hand)
- (done) 6. Publiceren op plan origin/main + ls-tree-witness
- (pending) 7. END post aan 9142ab1f

## Witnesses (metingen)

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-208-static-release-gate refs/pull/1746/head refs/heads/develop` (05:55Z): branch = PR head = `eb2e471a8fdff3233254043782fd805698d9a798`; develop = `1ff16925c4e141d732459a34ddf0b7f49128a214` (gemeld: branch-head is dezelfde commit als de kandidaat — klopt gemeten).
- `gh run view 44987381250` → name "Pre-Release · v0.4.28", workflow "Release · Pre-Release Validation", event workflow_dispatch, headSha `eb2e471a8fd…`, **completed failure**.
- Ongeldige run getuige: `gh run view 44986797647` → headSha `1ff16925c4e…` (develop), statische jobs: 1 skipped-groep gemeten — ref=develop verklaart de skipped gates.
- Planning repo zone: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## De zes statische matrix-gates (GEEN skipped — allemaal uitgevoerd)

- Static · agent / Executed static · agent — job `137102052113` — **success**
- Static · ci-fast-check / Executed static · ci-fast-check — job `137102089845` — **success**
- Static · init / Executed static · init — job `137102052110` — **failure** (stap 18 'Run static gate'; log-lijn: "Managed-environment machine operations require an authenticated BaseHarbor operator." / Resolution "authenticate the BaseHarbor operator", Affected init-source-fixture/dev)
- Static · config-matrix / Executed static · config-matrix — job `137102052148` — **failure** (zelfde authenticated-operator foutboodschap in JSON-vorm, job-log 59,760 bytes)
- Static · mcp / Executed static · mcp — job `137102052168` — **failure** — `RuntimeError: MCP contract mismatch: missing=[] unexpected=['baseharbor.app.perses.disable', 'baseharbor.app.perses.enable', 'baseharbor.app.perses.remove', 'baseharbor.app.perses.status']`
- Static · shell-ux / Executed static · shell-ux — job `137102052189` — **failure** (operator-authentificatie-keer, idem)

De statische gate-stap is `pre-release-runtime-suite.yml` 'Run static gate' (regel ~257-287 van het branch-workflowbestand) en runt de demo-suite `tests/init|config-matrix|mcp/...`; de vier falen op operator-authenticatie in de gate-cel of op de perses MCP-contractdiff — dat zijn omgeving-/contractbeelden, geen SKIPPED-gates.

## Overige jobs (volledigheid, uit dezelfde run)

Source · Candidate and Gate Plan 137100834532 success; Release · Candidate Artifact 137100936451 success; Source · Go Tests cli-0/1/2/packages 137100936476/514/18/513 success; **Source · Go Tests · cli-3 137100936494 success**; Source · Go Vet 137100936481 success; Docs · Workflow and Release Validation 137100936477 success; Source · Format and Readability 137100936520 success; Release · Snapshot Build 137100936537 success; Source · Qualified 137102037340 success; HA groups · All runtime results 137102052412 success; runtime heavy/light aggregators success; alle overige Integration/HA/Heavy/Light/Greenfield/Reference-Journey/Adoption/Candidate-Image jobs = skipped (deze dispatch kiesde ze niet — geen statische matrix-gate). Pre-Release Checks 137102500035 failure (aggregator boven de vier statische falen). Failed-job-totaal: 5.

## cli-3 in DEZE suite

- Job `Source · Go Tests · cli-3` = `137100936494`, **completed success**.
- Stap `Install shells for the shell-wrapper test path` = **success**; log-getuigenis: `zsh: /usr/bin/zsh` en `fish: /usr/bin/fish` (apt-inst of both in de job, `pre-release.yml:338` definieert deze stap op de branch).
- De uiteindelijke shard-ontvangst: `PASS cli-3: 426 passed / 16 intentionally skipped / 442 discovered; CLI inventory total=1843`.
- Nuance, explicaat gemeld: de shard-runner (`scripts/pr-go-unit-shard.py`, cli() regels ~75-115 op de kandidaat-ref) print GEEN per-test `ok`-regel; hij faalt gesloten zodra `TestEndToEndInstalledZshAndFishWrappers` niet in de 426 passed zit of in de 16 intentional skips verdwijnt (executed/passed/skipped-verplichtingen, 'CLI shard incomplete'). De 0-byte `TestEndToEndInstalledZshAndFishWrappers`-regel die de eerdere run liet vallen, is hier afwezig en het job-result is success met shells stap success — dat IS de beleg, binnen de print-stijl van deze suite. Er is geen aparte, door mij te noemen ok-regel.

## PR-beschrijving

De PR-beschrijvingstext van #1746 mag uitsluitend run `44987381250` noemen; `44986797647` is ongeldig en mag in geen enkele akte of PR-nachweis als beleg staan. De beschrijving bewerkt de Owner, niet deze lane.

## repo-rule compliance

Leeg in deze dispatch: geen productwijziging, geen push op een product-ref, geen merge/close/ready-schakelaar, geen PR-beschrijvings-edit, geen GitHub-commentaar, geen `.github/**`- of `scripts/**`-wijziging, geen lokale test-runs (alleen gh-api/log- en git-show-lezingen), geen subagenten. Posten uitsluitend naar coordinator 9142ab1f.

## cleanliness

cleanliness: nothing started. Eigen pid 2407437. BEFORE `docker ps -a` = 1 entry (`a0d40c5bcc8e baha-prunit-db-2286133`, running ~40 min, gestart door een andere lane — niet van mij, niet aangeraakt); AFTER idem. Geen containers/netwerken/volumes van deze dispatch; scratch onder `/var/tmp/0428-223` wordt voor END verwijderd.

END 0428-223-testctx DONE (geldig: run 44987381250 completed FAILURE; zes statische gates uitgevoerd, geen skipped: agent 137102052113 success, ci-fast-check 137102089845 success, init 137102052110 failure, config-matrix 137102052148 failure, mcp 137102052168 failure, shell-ux 137102052189 failure; cli-3 137100936494 success met shells-stap success)

## publishing witness

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep footprint-gate-admission/static-suite-1746-valid-run
evidence/r28-welle5-2026-11-22/footprint-gate-admission/static-suite-1746-valid-run.md
```
