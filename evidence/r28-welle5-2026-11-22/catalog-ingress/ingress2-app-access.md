# INGRESS-2 — catalog rows voor cmd/baha/app_access.go + test

Lane 0428-223-testctx, sitz b90e4ba1, kaart
t-20261123-catalog-ingress-app-access. Muster: het gemergde #1790. Doel: de
trusted-base rows voor de twee bestaande paden, zodat #1620 (en elke future
wijziging aan app_access) de Trusted Plan passeert.

## PLAN

1. (done) Realiteit: origin = github URL (remote -v); ls-remote develop =
   `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e`. Muster-rows uit develop
   gemeten: `source.cmd.baha.app.edit.go` ZONDER runtime_specific (shared
   command source); `cmd.baha.app.env.test.go` EN
   `cmd.baha.target.runtime.access.provider.test.go` MET
   `runtime_specific: true`. Inhoudelijk: `cmd/baha/app_access.go` bevat
   runtime-werk voor beide families ( `detectRuntimeForApplication`,
   `compose.RunProjectFilesEnv` op de resolved provider, en de
   human-reveal/audit routes uit #1620-gebied); `cmd/baha/app_access_test.go`
   is puur parsing/unit (geen docker/podman direct gebruik, gemeten met
   grep). docker ps -a before = 0, eigen pid 3012986.
2. (done) Frische branch `lane-0428-ingress2-app-access` op exact develop
   `b9e69b14` (worktree add -b, ANCESTOR-OK gemeten) in
   workers/0428-223-ingress2-wt. De #1620-branch is niet geraakt.
3. (done) Catalog edit, REINE addition, alleen `scripts/pr-gate-coverage.json`:
   - `{"id": "source.cmd.baha.app.access.go", "path":
     "cmd/baha/app_access.go", surfaces = beide atomic data-capabilities}`
     — BESLUITING regel: gedeelde command source, muster =
     `source.cmd.baha.app.edit.go` (app_edit.go draait dezelfde
     docker+podman workloadroutes zonder vlag). app_access.go is runtime-
     gebonden aan de provider-volgorde uit de resolved target, maar net als
     app_edit.go NIET engine-specifiek geschreven → geen
     runtime_specific vlag.
   - `{"id": "cmd.baha.app.access.test.go", "path":
     "cmd/baha/app_access_test.go", "runtime_specific": true, beide
     data-capabilities surfaces}` — BESLUITING: analog
     `cmd.baha.app.env.test.go` en `cmd.baha.target.runtime.access.provider.
     test.go`: de test dekt de human-reveal/audit paden die aan BEIDE
     runtime-families hangen; runtime_specific true behoudt beide
     engine-siblings in de native matrix (validator-interpretatie:
     validate-pr-gate-coverage.py:105-112 — shared components gebruiken
     docker als representative, runtime_specific behoudt podman erbij).
   - Geen enkele bestaande zeile gewijzigd: diff vs develop = precies deze
     twee blokken; release-veld blijft v0.4.27.
4. (done) PRUEFUNG vóór push: dup ids 0, dup paths 0, components 220;
   `validate-pr-gate-coverage.py` → "PR gate coverage catalog is valid";
   `scripts/test_pr_gate_coverage.py` → OK; `scripts/test_pr_native_gate_plan.py`
   → OK; `pr-gate-plan.py` sim over de twee paden → rc=0, 0 uncataloged,
   selected = `atomic/docker/data-capabilities, atomic/podman/data-capabilities`.
5. (done) `bash scripts/ci-fast-check.sh` rc=0; commit `d3eed85a`; push;
   ls-remote refs/heads/lane-0428-ingress2-app-access EN
   refs/pull/1791/head = `d3eed85ab96040c1f80b2132f8316879f31e1b26`. PR
   **#1791** base develop, ready, body verweist kaart + #1620 +
   #1773-klasse + muster #1790. KEIN merge.
6. (done) EXACT hosted run **45091676596** @d3eed85a terminal
   completed/**success** (failed=0):
   - Trusted Plan: GROEN — 137422407321 success. Plan-artefact in de job-log
     kiest de CI-beheersing-gates (ci-executor-tests, ci-policy,
     pr-planner-tests, receipt-execution-tests) — correct voor een
     catalog-only diff.
   - Native gate plan 137422407115, Source format 137422407208, Focused
     Python 137422472729, Candidate-added checks (advisory) 137422472664:
     success. PR Selected Checks 137423008005: success.
   - Native docker/podman, Go unit shards, Selected Runtime: SKIPPED
     (137422457025/137422475080/137422474314) — structureel: de
     catalog-only diff raakt geen runtime-bron, het trusted base-plan
     selecteert dan geen runtime gates. Niet als groen geteld.
7. (done) Akte + ls-tree-witness op plan origin/main.
8. (done) Cleanliness + END.

## Provenance en delivery

- base attestation: ls-remote develop = `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e`
  vóór het branchen; `git merge-base --is-ancestor origin/develop HEAD` = OK
  op de eerste (en enige) commit `d3eed85a`.
- `git log --oneline origin/develop..HEAD` = alleen d3eed85a (eigen commit).
- `git diff --name-only origin/develop...HEAD` = alleen
  `scripts/pr-gate-coverage.json`.
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` = https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Develop-only ingress, geen product-code edit, GEEN .github touch, GEEN
  merge, geen edit aan de #1620-branch, geen subagenten, geen containers op
  deze host. PR blijft OPEN/ready (handoff = review).

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 3012986), AFTER = 0
entries (pid 3055857). Geen compose/container gestart. Scratch
(/var/tmp tp-log, diff-json, fastcheck-log, pr-body) vóór END verwijderd
(ls-bewijs 0 treffers). Werktree workers/0428-223-ingress2-wt = kandidaat
d3eed85a, 0 delta.

END_DONE 0428-223-testctx — INGRESS-2: PR #1791 (branch
lane-0428-ingress2-app-access, head d3eed85ab96040c1f80b2132f8316879f31e1b26,
ls-remote branch + pull/1791/head bewezen, base develop, ready, geen merge).
Catalog diff = precies 2 additive rows (shared-muster app_edit voor
app_access.go; runtime_specific true analog app_env/target-runtime voor
app_access_test.go), validator + test_pr_gate_coverage +
test_pr_native_gate_plan lokaal groen, dup 0. EXACT hosted run 45091676596
terminal SUCCESS — Trusted Plan GROEN (137422407321), Source format +
Focused Python + Candidate-added advisory + PR Selected Checks
(137423008005) success; runtime gates structureel skipped bij catalog-only
diff. Na merge passeert #1620 de TP base-zijdig. cleanliness: besenrein.

## origin/main witness

Exact: `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep ingress2-app-access` (plan main = 0fe22152c4806e1ec286bd876edf65cd7a2cb333):

```
evidence/r28-welle5-2026-11-22/catalog-ingress/ingress2-app-access.md
```
