# PR #1881 / 0428-310 — heal round 1 (candidate unchanged; catalog-lift unlock PR #1885 created)

Lane: w402-0428-310-1881heal · Card: t-20261125-hunt40-migration-marker-last (0428-310) · Repo: mcpdev80/baseharbor · PR: #1881
Mission: coordinator/missions/w402-0428-310-1881heal.txt (re-issued after the interim #1884 read-only report leg)
Note: an earlier coordinator stop ("dein bisheriger Auftrag ist durch Owner-Anweisung UNGUELTIG") voided the first dispatch; the identical mission file was then re-issued at 13:08 — this round executes it. Between the two I performed the requested read-only #1884 report only, with zero product writes.

## PLAN

- Verify remote truth via ls-remote (first git action was `git remote -v`; only github.com/mcpdev80 URLs used) — DONE
- Own worktree /tmp/opencode/w402-310... heal-wt at the named candidate head; the branch ref itself stays locked by the inactive w399 worktree, so I work on same-SHA local branch `w402-0428-310-1881heal` and push refspec-only into the named candidate branch — DONE
- `git fetch origin` + `git merge-base --is-ancestor origin/develop HEAD` -> rc=0, develop IS already an ancestor: NO merge/hop commit needed (mission step 2 conditional not triggered) — DONE
- Pre-push non-test checks only: gofmt clean, `go vet ./internal/orgconfig/` OK, `go build ./...` OK, `python3 -m py_compile scripts/pr-gate-plan.py scripts/validate-pr-gate-coverage.py` OK; NO tests executed locally — DONE
- Push candidate + ls-remote delivery proof — DONE (no-op: remote already identical, see step-3 analysis)
- Root-cause all 4 red Trusted-Plan failures on head 2e81d55fd0 (runs 46098935150 + 46099522933): class-A trusted-BASE catalog freeze, not candidate content — DONE
- Build the minimal route per GATE RULE: catalog-only unlock PR #1885 (own branch lane-0428-310-1881heal-cataloglift; NOT a second branch for card #1881 — a separate trusted-base prerequisite; card-disposition decision left to Codex, flagged here as finding, not implemented) — DONE
- Report the required correction rounds for #1881 and #1884 (remove self-declared rows after merge; close+reopen pair) — coordinator/Codex action — REPORTED
- END_DONE to coordinator — LAST action (this file is on origin/main before that post)

## VISIBLE ANSATZ BLOCK

- Card frontmatter owner VERBATIM from origin/main (`git -C baseharbor-plan show origin/main:tasks/t-20261125-hunt40-migration-marker-last.md | grep '^owner:'`): `owner: w399-0428-289-providers`. No "(lane X)" marker present, so the candidate-admission identity would be that full value — but this heal adds NO new candidate commits (step-3 proof below); every commit I create this round uses my own lane identity.
- Lane identity for all commits created by me: git user.name `w402-0428-310-1881heal`, git user.email `w402-0428-310-1881heal@baseharbor.local`
- Literal invocation used: `git -c user.name=w402-0428-310-1881heal -c user.email=w402-0428-310-1881heal@baseharbor.local commit -q -m "ci(0428-310): catalog trusted base rows for the frozen class-A sources (orgconfig trio + #1884 quartet)" -- scripts/pr-gate-coverage.json`
- Pre-push gate executed before every push: `git show -s --format=%an HEAD` -> must equal `w402-0428-310-1881heal` (output witness below).

## Step 1-2 witnesses (product remote)

- First git action `git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor: origin/lane-origin/upstream all `https://github.com/mcpdev80/baseharbor.git` (push URLs verified; the `workers/baseharbor` quarantine zone was NOT used for any witness).
- ls-remote: `refs/heads/lane-0428-310-migration-marker` = 2e81d55fd019c54fecc79875f21b1ba5c6fdfc33; `refs/heads/develop` = 6944e8761af6f07b801f55e39bb9a5409226c10b (identical to dispatch-time base — no base drift).
- `git merge-base --is-ancestor origin/develop HEAD` in /tmp/opencode/w402-0428-310-1881heal-wt -> rc=0 (develop IS ancestor; merge skipped per mission step 2 condition).
- `git log --oneline origin/develop..HEAD` (candidate, pre-existing chain): 2e81d55fd0 (w404-0428-310-markerfix), 1cd5029f71 merge (w403-0428-310-syncdirfix), 772ebc3999, d7d1ea2db7 (w403), 640f53a6e8, 6fb13d012c, fc510d73d5 (w399-0428-289-providers = card owner). All are the established #1881 chain history already content-reviewed (R6 PASS, w267); this heal created NONE of them, so the own-commits-only rule applies to my new commits only (none on the candidate branch).

## Step 3 analysis — why no candidate push could heal the checks

- My push attempt `git push origin refs/heads/w402-0428-310-1881heal:refs/heads/lane-0428-310-migration-marker` returned "Everything up-to-date"; ls-remote proof: `2e81d55fd019c54fecc79875f21b1ba5c6fdfc33 refs/heads/lane-0428-310-migration-marker` and `2e81d55fd019c54fecc79875f21b1ba5c6fdfc33 refs/pull/1881/head` — the remote head equals my local head; no content of mine ever failed to leave the machine because NO content change is admissible: develop is already an ancestor, and the red checks are not content-caused (below).
- A forced commit (e.g., re-merging develop) would re-run the same failing Trusted Plan identically; reruns do not raise run_attempt on the existing IDs as pair evidence and are banned as analysis substitute (mission step 4/5, owner lesson 2026-11-25).

## Step 4/5 — red-check diagnosis on exact head 2e81d55fd0

- Runs on the head (both `pull_request`, FAILURE, terminal): 46098935150 and 46099522933 (workflow "CI · Source & Quality"; run numbering shows 46099522933 is run_attempt 2 of the same run 517639282 — a rerun, VOID as pair evidence).
- Failing jobs in each run (2 per run = the "4 rote Checks"): "PR · Trusted Plan" (steps: success checkout, success detect-owner-diff, FAILURE "Resolve exact immutable PR inputs using trusted base policy") and "PR Selected Checks" (FAILURE "Require complete selected Go shard coverage").
- Verbatim error line (identical in both runs; job logs 140838555483 / 140837698126): `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/orgconfig/migration.go …; internal/orgconfig/migration_marker_test.go …; internal/orgconfig/store.go …` (pr-gate-plan.py:1952 `raise ValueError`).
- Downstream verbatim (PR Selected Checks): `UNIT_SCOPE:` (empty) → `REJECT: Go test selection missing or invalid`; every test-bearing job (Go unit shards, native docker/podman, validation) is SKIPPED — no executed test receipt exists on this head, so greenness is NOT computable and not claimed.
- Classification: UMGEBUNG/PLAN-KATALOG — the Trusted Plan resolves the catalog from the TRUSTED BASE (`git show <base>:scripts/pr-gate-coverage.json`, pr-gate-plan.py `_base_catalog_document` ~:1881-1895) and the orgconfig rows do NOT exist on develop (verified: `git show origin/develop:scripts/pr-gate-coverage.json | grep internal/orgconfig` -> empty). The candidate already ships correct rows in its own catalog (HEAD lines 2865/2873/2881) — candidate-side content is NOT the cause. NOT base drift (develop is ancestor), NOT product behavior.
- No `.github/**` change is needed (finding: none); the unlock lives entirely in scripts/pr-gate-coverage.json — mission step 6 stop-criteria not triggered.

## Step 6 — unlock route executed: PR #1885 (catalog-only, draft)

- Branch: lane-0428-310-1881heal-cataloglift @ af6cd4e3d2bd8a5e4a52e2a33bcfc613204b3da0, cut from develop 6944e8761a (ANCESTRY_OK; `git log --oneline origin/develop..HEAD` = exactly my 1 commit; `git diff origin/develop...HEAD --name-only` = scripts/pr-gate-coverage.json).
- Delivery proof: `git ls-remote origin refs/heads/lane-0428-310-1881heal-cataloglift` = af6cd4e3d2bd8a5e4a52e2a33bcfc613204b3da0. Pre-push identity: `af6cd4e3d2 an=w402-0428-310-1881heal cn=w402-0428-310-1881heal`.
- Rows added (7): orgconfig trio (store.go, migration.go, migration_marker_test.go) + #1884 quartet (cmd/baha/app_candidate_consent_interactive.go, app_candidate_consent_test.go, app_remote_lifecycle.go, core_installation.go) — surfaces docker/podman data.capabilities, matching the planner's own suggested remedy verbatim. Static validator: `python3 scripts/validate-pr-gate-coverage.py` -> "PR gate coverage catalog is valid".
- FINDING (card disposition, Codex decision, NOT implemented here): per codex-disposition-136, catalog edits belong in a catalog-only product PR outside any feature card's write-set (that precedent explicitly refuses adding them to a feature card). This heal had no admissible action under its write-set otherwise (pushing the identical head is empty; committing catalog rows into the #1881 branch would duplicate the fan-in pattern the prior disposition rejected). If Codex instead decides the rows belong on the candidate branch itself, the single commit af6cd4e3d2 cherry-references into lane-0428-310-migration-marker without content loss.
- Correction rounds required AFTER #1885 merges into develop (coordinator dispatch): #1881 remove its duplicate self-declared rows from scripts/pr-gate-coverage.json delta (then normal push = new exact head), #1884 likewise (its core_installation.go row was missing even in-PR — now covered by #1885). Each then needs a terminal exact-head pull_request PAIR via authorized close+reopen; a rerun is void.

## Hosted CI observation (own-run duty)

- PR #1885 (draft, catalog-only): runs watched to terminal — recorded in the appended section below.
- PR #1881: NO new run triggerable by me without forbidden ops (push was a no-op; close+reopen is not authorized for this PR by my mission; a pair on the unchanged red head reproduces the class-A failure anyway). STATE as observed: 2 failed runs on exact head (IDs above).

## cleanliness

- `docker ps -a` before/after (this host): empty output, 0 containers; own pid recorded: 819488 (bash) / pushes ran as child PIDs of this session. No compose projects started, none to tear down.
- Worktrees: /tmp/opencode/w402-0428-310-1881heal-wt (kept for corrections), /tmp/opencode/w402-cataloglift-wt (kept for #1885 corrections), /tmp/opencode/w402-attest and /tmp/opencode/w402-sim (neutral clones; removed at END — see appended line). No scratch in the ecosystem root; no extension of foreign paths (the w405-collision finding was reported last leg).

## END

END_DONE w402-0428-310-1881heal: #1881 heal round 1 — candidate head 2e81d55fd0 unchanged (develop 6944e8761a already ancestor; red checks are class-A trusted-BASE catalog freeze, not candidate content; push was content-empty by necessity, ls-remote proof above); unlock route built in this PR per GATE RULE: catalog-only draft PR #1885 at af6cd4e3d2 (7 class-A rows, validator green); post-merge correction rounds for #1881/#1884 + close+reopen pair are coordinator dispatch. head=2e81d55fd0 basis=6944e8761a gates=0 pass/4 fail (2 runs x Trusted Plan + Selected Checks) runs=46098935150,46099522933 unlock=1885@af6cd4e3d2.

## Appended witnesses (final)

- PR #1885 hosted observation (my own triggered candidate, watched to terminal): run 46145618061, event pull_request, exact head af6cd4e3d2, workflow CI · Source & Quality, conclusion SUCCESS (draft PR ⇒ the draft path ran; Trusted Plan selection on catalog-only path succeeded — the added rows are parse- and schema-valid under the real planner).
- Quarantine-rule correction (honest note): the remote-truth command in the first git action block was executed in the shared checkout /home/marcel/dev/baseharbor-ecosystem/baseharbor; the identical refs were then re-verified from /tmp/opencode clones and via `git ls-remote <url>` direct calls; all cited SHAs were additionally cross-checked with `gh` API (GitHub source of truth). No conclusion rests on the quarantined workers/baseharbor refs.
- Scratch cleanup: /tmp/opencode/w402-attest and /tmp/opencode/w402-sim removed.

## Final origin/main verification (second-to-last action, exact output)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle9-2026-11-28/0428-310-1881/heal-round-1.md`
- (output appended after merge)
- Exact output: `evidence/r28-welle9-2026-11-28/0428-310-1881/heal-round-1.md` (present on origin/main; plan main advanced efe488381..a98a853d0 via squash merge of plan PR #270, Plan · validate SUCCESS on exact head 1c7e39f86).
