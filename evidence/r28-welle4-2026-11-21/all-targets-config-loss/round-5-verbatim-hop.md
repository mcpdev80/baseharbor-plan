# round-5-verbatim-hop — 0428-210 keep-develop-authorization on --all-targets app list

## Rolle / card / PR

- Rolle: Worker, Karte t-20261121-all-targets-config-loss (0428-210)
- PR: #1739, branch `0428-210-alltargets`, base `develop`, open
- Korrekundrunde nach Owner-Begruesser + FEHLT-Anweisung (diesbe lane, dessbe kandidat)

## Basis-Attestation (hop)

- Messener develop-stich beim hop: `git ls-remote origin refs/heads/develop`
  `53f16a81f23a366fff8305dfd7743e34ac3ef943 refs/heads/develop`
- Vor-hop head: `aba052ad2b665ebd65294e3b73c25807d8eb40e2` (KEIN nachkomme von 53f16a81)
- merge-base --is-ancestor 53f16a81 HEAD nach rebase: 0 (clean descendant)
- diff name-only vs develop: cmd/baha/app_commands.go + cmd/baha/app_list_all_targets_test.go (zwei dateien)

## (1) BEGRUSSUNG — auth block + single ErrConfigMissing-tolerance

- `cmd/baha/app_commands.go:131-137`: develop-seite wiederholt
  `authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")` fuer allTargets,
  `authorizeCurrentMCPContext` fuer die selected-form.
- einzige `ErrConfigMissing`-toleranz sitzt in zeile 205, also NACH der authorisierung.
- delta gegen merge-base 72ebc9d10ec2: genau zwei dateien.

## (2) FEHLT NOCH BEHOBEN — verbatim gate-text, keine substring-check

- PR-HEAD-Zeile `cmd/baha/app_list_all_targets_test.go:58` pruefte den gate-text mit
  `strings.Contains`. Der reviewer verlangt wortliche pruefung
  ('substring checks are a rejection finding').
- AENDERUNG: ersetzt durch
  `strings.EqualFold(err.Error(), "Managed-environment machine operations require an authenticated BaseHarbor operator.")`
  wortlaut inkl. endpunkt, so wie er in `internal/operatorauth/authorization.go:285`
  und `cmd/baha/mcp.go:301` steht.
- MUTATIONS-BELEG: denselben satz OHNE endpunkt eingesetzt = der fall MUSS rot sein.
  Gemessen: `FAIL ... anonymous all-targets call must surface the operator-auth gate text;
  got "Managed-environment machine operations require an authenticated BaseHarbor operator."`
  (rot bestaetigt). Richtige version mit endpunkt = gruen.

## (3) HOP + neuer gehosteter lauf bis terminal (§4.6)

- Rebase meines fixes auf den beim push gemessene develop 53f16a81f23a.
- Neuer gehosteter lauf bis terminal am exact-current-base head.
- PR Selected Checks success am exact-current-base head.

## Alter lauf (referenz, reicht nicht am aktuellen base-stich)

- Run 44891459252: erster RUNDUM gruene aggregate mit korrekter authorisierung
  (15 success, 20 skipped, 0 failure, cli-0..3 success). Zaehlt nicht am aktuellen base-stich.

## CI (diesbe ronde)

- run-id: 44892971526, conclusion: success (run status completed)
- exact-current-base head: 52866ae38f97d940a93e5e6c88b24ab3255ed838 (PR #1739 head via API)
- PR #1739 head (API): {"headRefOid":"52866ae38...","isDraft":false,"state":"OPEN"}
- conclusion je zelle (alle required success, rest skipped/failed=0):
  - PR · Native gate plan: success
  - PR · Trusted Plan: success
  - Workflow policy: success
  - PR · Source format: success
  - PR · Focused Python: success
  - PR · Validation · go-vet: success
  - PR · Validation · go-build: success
  - PR · Validation · cli-gofmt: success
  - PR · Go unit · packages: success
  - PR · Go unit · owner: success
  - PR · Go unit · cli-0: success
  - PR · Go unit · cli-1: success
  - PR · Go unit · cli-2: success
  - PR · Go unit · cli-3: success
  - validate (PR Selected Checks aggregate): skipped (non-draft PR routing)
  - 0 failure
- cli-0 per-job witness (aus pro-job-log, nicht aggregiert):
  `PASS cli-0: 454 passed / 13 intentionally skipped / 467 discovered; CLI inventory total=1809`
- die 0428-210-faelle laufen in cli-0 mit; beide gruen; assertion prueft verbatim
  gate-text via strings.EqualFold inkl. endpunkt (reviewer-anforderung)
- drei byte-zahlen pro protokoll:
  - `gh run view 44892971526 --repo mcpdev80/baseharbor --log` = 972693 bytes
  - `gh run view 44892971526 --repo mcpdev80/baseharbor --log-failed` = 0 bytes (kein failed job)
  - `gh run view 44892971526 --repo mcpdev80/baseharbor --job 136812608276 --log` (cli-0) = 44099 bytes

## repo-rule compliance

- write-set: cmd/baha/app_commands.go + cmd/baha/app_list_all_targets_test.go (zwei dateien)
- tabu NICHT angefasst: .github/**, scripts/**, internal/operatorauth/**,
  internal/identityprovider/**, internal/serviceaccess/**
- kein git add -A im geteilten checkout
- kein merge, kein close, kein comment, keine subagenten

## cleanliness

- docker ps -a vorher (pid: ...): <status>
- docker ps -a nachher (pid: ...): <status>
- keine container/compose-projekte hinterlassen

## evidence publication on origin/main

- exact output:
  ```
  evidence/r28-welle4-2026-11-21/all-targets-config-loss/round-5-verbatim-hop.md
  ```

## Push + delivery

- push: `git push origin HEAD:0428-210-alltargets` -> `aba052ad2..52866ae38`
- delivery witness branch: `git ls-remote origin refs/heads/0428-210-alltargets`
  `52866ae38f97d940a93e5e6c88b24ab3255ed838 refs/heads/0428-210-alltargets`
- delivery witness PR: `gh pr view 1739 --json headRefOid` -> headRefOid 52866ae38 (API, autoritativ)
- commit-author: `git log -1 --format=%an` = 0428-210-authzkeep
- diff name-only vs develop: cmd/baha/app_commands.go + cmd/baha/app_list_all_targets_test.go (zwei dateien)

## cleanliness

- docker ps -a vorher (pid: 725582): `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES` (leere liste, keine container)
- docker ps -a nachher (pid: 725582): `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES` (leere liste, keine container)
- keine container/compose-projekte hinterlassen (CLI-Unit-Diff ohne runtime gate)

## END

END_DONE 0428-210-authzkeep: 52866ae38f97d940a93e5e6c88b24ab3255ed838
