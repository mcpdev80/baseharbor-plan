# 0428-223-testctx — hop-wave akte #3: PR #1750 + PR #1753 onto develop 5ca8420c181

## PLAN

- (done) 1. ls-remote-abgleich: develop 5ca8420c181 (#1714 merged), #1750 head 5d47569f337, #1753 head ce5cf8f3037
- (done) 2. PR #1750: additive hop, pushed candidate f6d3fc5c (parents 5d47569f + 5ca8420c)
- (done) 3. PR #1750: push ohne force; run 44990801974 completed SUCCESS, failed jobs 0
- (done) 4. PR #1750 PFLICHTBELEG: Selected Runtime + Native·matrix STILL SKIPPED (job-ids + plan-rule beigelegt)
- (done) 5. PR #1753: additive hop 50c4bce74d2, push ohne force; run 44990860430 completed SUCCESS, failed jobs 0; idem SKIPPED-befund
- (done) 6. Akte publiceren op plan origin/main + ls-tree-witness (plan commit a15c069e0; zie onder)
- (pending) 7. END post aan 9142ab1f

## publishing witness

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep hop-develop-5ca8420c-w223
evidence/r28-welle5-2026-11-22/base-hop-mechanics/hop-develop-5ca8420c-w223.md
```

## Remote witnesses

- Voor de hops (remote guard `git remote -v` → `origin https://github.com/mcpdev80/baseharbor.git`): develop `5ca8420c1814f25bea6404e55fd054c60746eae5`; #1750 branch=head `5d47569f337`; #1753 branch=head `ce5cf8f3037`.
- Na de pushes: refs/heads/lane-0428-223-testcontext-target = refs/pull/1750/head = `f6d3fc5c23e4a3097d4d36130303338b0ff180bd`; refs/heads/lane-0428-227-footprint-gate-admission = refs/pull/1753/head = `50c4bce74d2d269cd985b3e66ac51fc879e0d627`.
- Planning zone: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## Hopmechanics

- PR #1750: `git merge --no-ff 5ca8420c181` op lane-0428-223-testcontext-target → hop commit `f6d3fc5c`, parents exact `5d47569f` (oude PR head) + `5ca8420c` (develop). Ancestry beide yes; `git log --oneline 5ca8420c181..f6d3fc5c` toont enkel de 5 PR-eigen commits + de hop. Eerlijke kanttekening: een eerdere poging met omgekeerde volgorde gaf een boom die verschilde van de merge-tree-som in `cmd/baha/test_operator_context_test.go` (beide kanten voegen op verschillende plaatsen toe); de gepushte f6d3fc5c bevat beide kanten correct (testIsolatedSelectionContext + develop's wizard-regels). Geen conflict, geen UU; geen rebase/amend/force.
- PR #1753: hop commit `50c4bce74d2`, parents `ce5cf8f3` + `5ca8420c`; push `ce5cf8f3..50c4bce7` zonder force.
- Nothing edited by me in `.github/**` or `scripts/**`; the content arriving via the merges is develop's own.

## Runs (terminals, Eigenes-Run-Pflicht)

- PR #1750 @ f6d3fc5c: run `44990801974` completed **success**, failed jobs **0**.
- PR #1753 @ 50c4bce7: run `44990860430` completed **success**, failed jobs **0**.

## PFLICHTBELEG — Selected Runtime / Native·matrix: nog steeds SKIPPED op beide (bevinding)

- PR #1750: `PR · Selected Runtime` job `137111249509` SKIPPED; `PR · Native · ${{ matrix.id }}` job `137111239451` SKIPPED; validate `137111207599` skipped; `PR Selected Checks` `137112288306` success; `PR · Native gate plan` `137111206801` success (log 46,352 bytes).
- PR #1753: `PR · Selected Runtime` job `137111418122` SKIPPED; `PR · Native · ${{ matrix.id }}` job `137111419930` SKIPPED; validate `137111383309` skipped; `PR Selected Checks` `137112373149` success; `PR · Native gate plan` `137111382518` success (log 46,451 bytes).
- De plan-regel uit beide native-gate-plan-logs: `matrix='{"include":[]}'` via de else-tak van `if git cat-file -e "$BASE_SHA:scripts/pr-native-gate-plan.py"`, met de warning `The PR base ($BASE_REF) does not contain the trusted native gate planner; no native runtime checks can be selected yet.` — de planner wordt uit de PR-base gelezen; de base-ref van beide pull_request-runs was de develop vóór #1714 (checkout-regel `ref: 1ff16925c4e…` in dezelfde log), terwijl develop 5ca8420c de planner en de #1755-toelating wél bevat (`git cat-file -e 5ca8420c:scripts/pr-native-gate-plan.py` → present). Dit is een CI-volgorde-bevinding, niets gewijzigd.

## repo-rule compliance

Geen `.github/**`- of `scripts/**`-bewerking; additieve `--no-ff` hops; geen merge/close/ready; geen GitHub-commentaar; geen lokale test-runs; geen subagenten; posten alleen naar coordinator 9142ab1f.

## cleanliness

cleanliness: nothing started. Docker: één vreemde running container `a0d40c5bcc8e baha-prunit-db-2286133` (niet van deze lane, alleen gemeld); door mij gestart: niets. Hopzones + `/var/tmp/0428-223*` scratch worden opgeruimd; een lokaal binair bijproduct `baha` in mijn wermtree was een restant van deze sessie en is verwijderd.

END 0428-223-testctx PENDING (publiceer hieronder; candidate SHAs #1750=f6d3fc5c23e, #1753=50c4bce74d2)
