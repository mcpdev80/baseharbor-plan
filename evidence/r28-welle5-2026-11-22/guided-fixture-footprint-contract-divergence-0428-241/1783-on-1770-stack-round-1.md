# 0428-241 stack ronde-1 — #1783 op #1770 gestapeld: alle drie poorten GROEN (develop c928a627)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht (owner-geautoriseerd,
git-only): de #1770 branch tip IN de #1783 branch mergen zodat #1783 den
native pin letterlijk draegt, PR-base omzetten naar de #1770 branch, en op
het combined head exact hosted aantonen dat de stack BEIDE blockers breekt.

## PLAN

1. (done) Realiteit: origin=github URL (remote -v); ls-remote
   develop=`c928a627389c9284ac1187bb46f06d8c0596f40a`; #1783 head
   `668388076bb39e81d98795358085b618a2e4e365` (branch
   lane-0428-241-optionA-operator-allowlist, OPEN ready, base develop);
   #1770 head = branch tip `0da4a571e35b07b4ac4eece646043ba7b25a78a1` van
   `codex/0428-237-exact-native-runtime` (OPEN, base develop). Write-sets
   gemeten: #1783 = cmd/baha/ci_integration_operator_enabled{,_test}.go,
   #1770 = scripts/ci-native-pr-gate.sh — DISJUNKT. docker ps -a before=0,
   eigen pid 2376950. Werktree workers/0428-241-optawt op 66838807 gezet
   (ff-only vanaf origin; lokale 8b99bdc3 was al ancestor — opmerking: de
   lokaal gemelde ronde-3 chain was in 66838807 opgenomen, geen verlies).
2. (done) Stack-merge: `git merge --no-ff
   origin/codex/0428-237-exact-native-runtime` → combined
   head `62f4ab0d673757c0fc258f35dfb85d87e1fa467a`; GEEN conflicten
   (disjunkt); additief (66838807 EN 0da4a571 zijn beide ancestor, gemeten);
   geen force/rebase/amend; geen content-edit. ci-fast-check rc=0; push;
   ls-remote branch-head EN pull/1783/head = 62f4ab0d.
3. (done) PR base verzet: gh pr edit via PATCH API →
   `baseRefName = codex/0428-237-exact-native-runtime`, head 62f4ab0d,
   state open (gh pr view + ls-remote witness). De CLI-edit-print toonde
   alleen de projects-classic deprecated-waarschuwing; API-getuige is
   leidend. GEEN merge door deze lane (Codex/Owner merged pas bij alle
   drie groen — en die zijn nu groen).
4. (done) EXACT hosted run **45068985009** @62f4ab0d terminal
   completed/**success**, failed=0, skipped=16 (niet-gerelateerde cellen).
   De drie bewijs-poorten:
   - **Trusted Plan GROEN: ja** — job 137351956516 EXECUTED+success (#1786
     catalog via de #1770/c928a627-ancestry).
   - **native GREEN: ja** — native/docker/data-capabilities 137351989582 EN
     native/podman/data-capabilities 137351989526 beide EXECUTED+success
     (exact runtime pin uit #1770, niet meer :edge-waiting).
   - **selected GREEN: ja** — Selected Runtime docker 137352342329 EN
     podman 137352342084 beide EXECUTED+success (fixture app-new :137,
     app-edit :140, footprint-show :151).
   - PR Selected Checks 137357917308 success; Runner Interface, Exact
     Candidate, Focused Python, seam-tests, pr-planner-tests, ci-executor,
     ci-policy, receipt-execution, source-contracts, cli-build/vet/guided,
     Demo Pin, Source format, Native gate plan, Workflow policy: success.
   Dit is de Nachweis dat de stack beide tegen-seitige blockers breekt.
5. (done) Akte + ls-tree-witness op plan origin/main.
6. (done) Cleanliness + END.

## Provenance

- bases: ls-remote develop = `c928a627389c9283…` (gemeten); #1770 tip
  `0da4a571…` en #1783 top `66838807…` zijn BEIDE ouders/ancestors van
  combined head `62f4ab0d` (twee is-ancestor-metingen OK).
- delivery: ls-remote refs/heads/lane-0428-241-optionA-operator-allowlist en
  refs/pull/1783/head = `62f4ab0d673757c0fc258f35dfb85d87e1fa467a`;
  gh pr view baseRefName = `codex/0428-237-exact-native-runtime`.
- git-only ronde: geen content-commit door deze lane; alleen de merge.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Alleen de bevolen git-only stapvolgorde: merge --no-ff (additief), push,
  base-omzetting (PR-beheer zoals expliciet bevolen), hosted waarnemen.
  GEEN content-edit, GEEN .github/product touch, GEEN force, GEEN merge,
  GEEN commentaar; geen subagenten; geen containers op deze host.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 2376950), AFTER = 0 entries
(pid 2438069). Geen compose/container gestart op deze host. Scratch
`/var/tmp/0428-223-fc-st.log` vóór END verwijderd. Werktree
workers/0428-241-optawt 0 delta na de merge-push.

END 0428-223-testctx DONE — 0428-241 stack ronde-1: combined #1783 head 62f4ab0d673757c0fc258f35dfb85d87e1fa467a (additieve merge --no-ff van #1770 tip 0da4a571 op branch lane-0428-241-optionA-operator-allowlist, beide ancestors gemeten, geen conflict/force), PR #1783 base = codex/0428-237-exact-native-runtime (gh API + view bewezen), EXACT hosted run 45068985009 completed/success failed=0: Trusted Plan GREEN: ja (137351956516), native GREEN: ja (docker 137351989582 + podman 137351989526), selected GREEN: ja (docker 137352342329 + podman 137352342084), PR Selected Checks 137357917308 success. Merge blijft bij Codex/Owner. cleanliness: besenrein
