# PR #1789 — final-hop op develop b9e69b14 (handoff b90)

Lane 0428-223-testctx, sitz b90e4ba1, handoff van 0847 (desens
#1789-werk is afgerond). Opdracht git-only: PR #1789 (branch
codex/0428-076-promql-ci-capture, head `146ccf6fd67c285a33dbc06a7d061806228550ce`,
open/ready) additief hoppen op develop `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e`
en exact hosted meten.

## PLAN

1. (done) Realiteit: `git remote -v` origin =
   https://github.com/mcpdev80/baseharbor.git; ls-remote develop =
   `b9e69b14…`, refs/pull/1789/head = branch-head = `146ccf6fd…`; PR #1789
   OPEN/ready base develop, titel "test(metrics): drop dead
   promqlparser-tagged perses witness from default build". PR-diff
   (merge-base): `internal/metrics/perses_dashboards_promql_test.go`,
   `internal/metrics/perses_dashboards_test.go`,
   `scripts/pr-gate-coverage.json`, `scripts/test_pr_native_gate_plan.py`.
   Catalog-diff vs merge-base: 6 minus / 0 plus (de PR verwijdert zijn eigen
   promql row). docker ps -a before = 0, eigen pid 3066585.
2. (done) Werktree workers/0428-223-1789-wt (worktree add --detach op
   146ccf6fd, checkout -B codex/0428-076-promql-ci-capture op exact dat
   voorwerp). Geen andere lane-tree geraakt.
3. (done) Hop: `git merge --no-ff origin/develop` → head `46994750`, GEEN
   conflict (develop heeft de rows van #1790 toegevoegd op andere plaatsen
   in het bestand; de PR-verwijdering van de promql row stond los), ouders
   146ccf6fd + b9e69b14 (beide is-ancestor gemeten). Geen force/rebase/
   amend, geen content-edit door deze lane.
4. (done) Catalog PRUEFUNG: `git diff origin/develop HEAD --
   scripts/pr-gate-coverage.json` = EXACT 6 minus / 0 plus en de
   minus-regels zijn precies de perses_dashboards_promql_test.go row
   (hieronder). Census op de merge-file: 217 components, dup ids 0, dup
   paths 0, geen promql row meer. Ingress rows #1790 (
   `cmd.baha.app.env.test.go`, `cmd.baha.target.runtime.access.provider.
   test.go` en derden) present. #1791 is nog OPEN (gemeten), dus de
   app_access rows zijn hier terechtniet expected en afwezig — conform
   missie "(falls schon gemergt: sonst egal)". Validator:
   "PR gate coverage catalog is valid".
5. (done) `bash scripts/ci-fast-check.sh` rc=0 ("No candidate-added
   validation checks. The trusted base plan remains the only merge
   requirement."); push; ls-remote refs/heads/codex/0428-076-promql-ci-capture
   EN refs/pull/1789/head = `469947501944603bd08aab1b3fb02a0474a5f1ec`.
   PR blijft OPEN/ready; GEEN merge.
6. (done) EXACT hosted run **45092733609** @46994750 terminal
   completed/**success** — gate met job-ids:
   - Trusted Plan: GROEN — 137425715839 success (ingress rows + PR-diff
     passeren de base plan; Native gate plan 137425715829 success).
   - Selected Runtime observability: docker 137426163826 EN podman
     137426163801 "Executed … success".
   - Go/static: Source format 137425715638 success; Go unit shards
     cli-0..3 + owner + packages (137425770039/…/137425770127) success;
     Exact Candidate 137425769892 success; Focused Python 137425769913
     success. PR Selected Checks aggregate 137428435195 SUCCESS.
   - **Advisory candidate-added checks: rood (known)** — 137425769881
     failure, precies zoals de missie voorspelde (kaart 0428-253; de
     candidate-added checks rapporteren maar binden deze PR niet).
     Toegift voor latere PRs na merge.
   - Native matrix 137425772366 skipped — structureel: de catalog diff
     raakt geen runtime source rij die native afdwingt.
7. (done) Akte + ls-tree-witness op plan origin/main.
8. (done) Cleanliness + END.

## Provenance en delivery

- base attestation: ls-remote develop = `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e`
  vóór de hop; tweede ouder van `46994750` = precies dat voorwerp; eerste
  ouder = `146ccf6fd` (additief, beide is-ancestor gemeten).
- `git log --oneline origin/develop..HEAD` toont alleen de eigen #1789
  ketening (merge + PR commits); `git diff --name-only
  origin/develop...HEAD` = de vier PR-paden hierboven.
- delivery: ls-remote branch EN pull/1789/head = `46994750…` na push.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## Catalog-diff vs develop (alleen de PR-eigen minus)

```
-    {
-      "id": "source.internal.metrics.perses.dashboards.promql.test.go",
-      "path": "internal/metrics/perses_dashboards_promql_test.go",
-      "surfaces": ["source.gate.atomic.docker.observability", "source.gate.atomic.podman.observability"],
-      "runtime_specific": true
-    },
```

6 minus / 0 plus (gemeten); geen dubbele paden, geen dubbele ids.

## repo-rule compliance

- Alleen de git hop + push (missie). Geen content-edit, GEEN .github touch,
  GEEN merge, PR open/ready gelaten; geen subagenten; geen containers op
  deze host. Advisory-rood niet "groen gerekend" — als known gedocumenteerd.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 3066585), AFTER = 0
entries (pid 3097479). Geen compose/container gestart op deze host. Scratch
(/var/tmp/0428-223-fc1789.log) vóór END verwijderd. Werktree
workers/0428-223-1789-wt houdt de kandidaat (0 delta); deze hop-werktree is
voor deze fanoutklus en mag daarna opgeruimd worden.

END_DONE 0428-223-testctx — PR #1789 final-hop: NIEUWE HEAD
469947501944603bd08aab1b3fb02a0474a5f1ec op branch
codex/0428-076-promql-ci-capture (merge --no-ff, ouders 146ccf6fd +
b9e69b14, beide ancestor gemeten, geen conflict, geen force, content-edit
nul; ls-remote branch + pull/1789/head = 46994750; PR open/ready, GEEN
merge). Catalog: diff vs develop == EXACT 6 minus / 0 plus (alleen de
PR-eigen perses promql row), ingress rows #1790 present, #1791 nog open,
dup id/path 0, validator VALID. EXACT hosted run 45092733609 terminal
completed/SUCCESS — Trusted Plan GROEN (137425715839) + Native gate plan +
Selected Runtime observability docker+podman (137426163826/137426163801) +
Go shards + Exact Candidate + Focused Python + PR Selected Checks
(137428435195) success; Advisory candidate-added 137425769881 rood (known,
kaart 0428-253, bindt deze PR niet); native matrix structureel skipped.
cleanliness: besenrein.
