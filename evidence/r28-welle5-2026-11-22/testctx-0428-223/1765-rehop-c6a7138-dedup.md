# 0428-209/#1765 — re-hop + dedup op develop c6a7138ce

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: PR #1765 (head 90586945a)
re-hoppen op develop `c6a7138ce2bf7de88f45f2a68e5168c835601a16` — de
ingress-PR #1790 is gemerged, de trusted-base row voor
`cmd/baha/control_plane_single_native_ci_test.go` staat NU in de develop
catalog, dus de eigen branch-edit is redundant en mag GEEN dubbele rij
achterlaten.

## PLAN

1. (done) Realiteit: `git remote -v` origin =
   https://github.com/mcpdev80/baseharbor.git; ls-remote develop =
   `c6a7138ce2bf7de88f45f2a68e5168c835601a16`, branch EN pull/1765/head =
   `90586945acb5a0a812b8cf87b3dc82e5a2d07845`; PR #1765 OPEN/ready base
   develop. Base-catalog bevat de trusted row met PUNT-id
   `cmd.baha.control_plane_single_native_ci_test.go` (gemeten). docker ps -a
   before = 0, eigen pid 2879612.
2. (done) Hop: `git merge --no-ff origin/develop` → "Auto-merging
   scripts/pr-gate-coverage.json", rc=0, merge-head `61fb002f`. Geen
   botserende conflict, maar de auto-merge produceerde WEL een dubbele rij
   (base-rij met punt-id + onze rij met underscore-id, dup paths = 1) —
   dus stap 3 trad in werking.
3. (done) Dedup: `git checkout --theirs` gaf in deze merge-situatie de
   develop-versie NIET terug (0 paths bijgewerkt, blob nog gelijk aan onze
   kop); daarom exact volgens de missie-doel (byteidentiek aan develop):
   `git show origin/develop:scripts/pr-gate-coverage.json >
   scripts/pr-gate-coverage.json` + `git add` + amend in de merge-commit →
   definitieve head `c8bbb0f5232b9725d750a1eca9efac238a9e221a` (ouders
   90586945ac + c6a7138ce2, develop-ancestor gemeten).
   PRUEFING gemeten: `git diff origin/develop HEAD -- scripts/pr-gate-coverage.json`
   = 0 regels; blob-hash worktree = develop-blob = `56f567d589743762bda8df67a5a10024fbb28e55`
   (BYTEIDENTIC). Census: 1 rij voor ons pad (punt-id), duplicate ids 0,
   duplicate paths 0, components 218. Validator: "PR gate coverage catalog
   is valid".
4. (done) `bash scripts/ci-fast-check.sh` rc=0 ("No candidate-added
   validation checks. The trusted base plan remains the only merge
   requirement."); push; ls-remote branch-head EN pull/1765/head =
   `c8bbb0f5`; PR blijft OPEN/ready; GEEN merge door deze lane.
5. (done) EXACT hosted run **45087109688** @c8bbb0f5 terminal
   completed/**success** (failed=0). Gates:
   - Trusted Plan: GROEN — 137408145223 success. Uncataloged-source fix:
     JA, base-zijdig (de trusted-base row uit #1790 doet wat deze lane als
     bevinding meldde).
   - Native: 6/6 success — docker data-caps 137408195963, podman
     data-caps 137408195996, coreless docker/podman 137408196051/137408195941,
     guided docker/podman 137408195959/137408196026.
   - Selected Runtime: docker data-caps 137408655821 + podman data-caps
     137408655818, docker guided 137408655841 + podman guided 137408655806,
     alle "Executed ... success".
   - Selected Core-less integrations docker/podman: success (137413362323,
     137412582096 + de matrix-bladen).
   - Go/static: Source format 137408145552 success; Focused Python
     137408210585 success; Go unit shards cli-0..3 (137408210674/598/663/706)
     success.
   - PR Selected Checks aggregate: 137416707967 success. De 68 skipped
     jobs zijn niet-geselecteerde matrix-bladen achter een groen plan — dit
     is geen defect: het aggregate en elke geselecteerde check zijn
     geexecuteerd en success.
6. (done) Akte + ls-tree-witness op plan origin/main.
7. (done) Cleanliness + END.

## Provenance en delivery

- base attestation: ls-remote develop = `c6a7138ce…` vóór de hop; tweede
  ouder van `c8bbb0f5` = precies dat voorwerp (is-ancestor gemeten); eerste
  ouder = `90586945ac` (additief).
- `git log --oneline origin/develop..HEAD` toont alleen eigen werk van deze
  PR-keten (de #1765 lane commits + onze merges); PR-diff omvang t.o.v.
  develop: alleen de twee eigen test-paden
  (`cmd/baha/control_plane_single_native_ci_test.go`,
  `cmd/baha/runtime_integration_test_support_test.go`) — de catalog is
  teruggegeven aan develop 1:1.
- delivery: ls-remote refs/heads/codex/0428-209-native-cell-recut EN
  refs/pull/1765/head = `c8bbb0f5232b9725d750a1eca9efac238a9e221a`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Alleen de named branch gebruikt (geen tweede kandidaat); merge + amend op
  DEZE lane's eigen merge-commit (geen force/rebase op gepushte historie —
  de amend zat vóór de eerste push van deze merge, ls-remote vooraf toonde
  nog 90586945).
- GEEN .github touch, GEEN merge, PR open/ready gelaten; geen subagenten;
  geen containers op deze host.
- STOP-kritieria beoordeeld en NIET voldaan: catalog diff vs develop leeg,
  geen duplicate-id validatorfout na dedup, geen TP-fail op andere source.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 2879612), AFTER = 0
entries (pid 2962449). Geen compose/container gestart. Scratch
(/var/tmp/0428-223-fc.log) vóór END verwijderd; werktree
workers/0428-2xx-fanout-1765-wt = kandidaat c8bbb0f5, 0 delta.

END_DONE 0428-223-testctx — 0428-209/#1765 re-hop + dedup op develop
c6a7138ce: NIEUWE HEAD `c8bbb0f5232b9725d750a1eca9efac238a9e221a` op branch
codex/0428-209-native-cell-recut (ls-remote branch + pull/1765/head bewezen,
PR open/ready, geen merge). Catalog dedup BYTEIDENTIEK aan develop (blob
56f567d5, `git diff origin/develop HEAD -- scripts/pr-gate-coverage.json` ==
leeg, 1 rij, dup id/path 0, validator VALID). EXACT hosted run
**45087109688** terminal completed/SUCCESS failed=0 — Trusted Plan GROEN
(uncataloged-source opgelost, base-zijdig via #1790), native 6/6, selected
data-caps + guided docker/podman, selected coreless integrations, Go unit
shards + Focused Python, PR Selected Checks GROEN. cleanliness: besenrein.

## origin/main witness

Exact: `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 1765-rehop-c6a7138-dedup` (plan main = 9669fbfbda7fe7787db4d7ff08247c779e608ec5):

```
evidence/r28-welle5-2026-11-22/testctx-0428-223/1765-rehop-c6a7138-dedup.md
```
