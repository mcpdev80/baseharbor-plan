# w394-0428-249-1812diag — Diagnose terminal FAILURE of PR #1812 on exact head c2dd3ff04 (read-only)

Lane: w394-0428-249-1812diag (worker). Card: 0428-249. Repo: baseharbor, PR #1812, head c2dd3ff04e30c73046b4eeecb56f3cab20e56c92.
Mission: DIAGNOSE only. No push, no merge, no rerun, no workflow_dispatch, no gate/workflow changes. This is NOT a qualification.

## PLAN

- Done: read mission, verified remotes (real GitHub URL only), ls-remote witnesses.
- Done: (a) full check census on the exact head, split terminal vs older-head.
- Done: (b) failed jobs + failed steps of run 45944501306, decisive log lines quoted.
- Done: (c) failure-class classification with file:line evidence.
- Done: (d) ancestry vs origin/develop.
- Done: (e) the two distinct run IDs a qualifying exact-head run would need and why current state fails.
- Done: (f) this akte, published to plan main via plan worktree + PR + squash merge.
- Done: cleanup, END post.

## Remote and reality witnesses

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (first action before any evidence commit):
  `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)/(push)` — real planning repo confirmed (per WRONG-ZONE rule; workers/baseharbor-plan not used).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1812/head refs/pull/1812/merge`:
  - develop = ea5218d72e263f21e79853b679af50074dab8c25
  - refs/pull/1812/head = c2dd3ff04e30c73046b4eeecb56f3cab20e56c92 (mission head confirmed)
  - refs/pull/1812/merge = e614da47788076753358c060fd73f2e68d2fc358
- PR #1812: state OPEN, isDraft=false, base develop, headRefOid c2dd3ff04…, mergeStateStatus=BLOCKED, mergeable=MERGEABLE (rulesets disabled; BLOCKED reflects failing checks only).
- Branch lane-0428-249-runtime-image-fix tip = c2dd3ff04 (ls-remote), identical to PR head.

## (a) Check census — terminal on c2dd3ff04 vs older heads

Only ONE CI run exists on the exact head c2dd3ff04: run 45944501306 (`CI · PR #1812`, event pull_request, run_attempt 1), created 2026-11-27T05:13:23Z, completed/failure (gh api actions/runs + actions/runs?head_sha both confirm a single run row for this SHA).

Check-run census on commit c2dd3ff04 (paginate of `/commits/c2dd3ff04/check-runs`): 61 success, 9 failure, 68 skipped (138 check runs; mission's earlier census 61/9/68 reproduced).

- Terminal FAILURE (9) — all belong to run 45944501306 on this exact head:
  1. PR Selected Checks (aggregate) — fail
  2. PR · Selected Runtime (atomic/docker/connectivity) / Executed docker · connectivity — fail
  3. PR · Selected Runtime (atomic/docker/full-destroy) / Executed docker · full-destroy — fail
  4. PR · Selected Runtime (atomic/docker/policy) / Executed docker · policy — fail
  5. PR · Selected Runtime (atomic/docker/reconciliation) / Executed docker · reconciliation — fail
  6. PR · Selected Runtime (atomic/podman/connectivity) / Executed podman · connectivity — fail
  7. PR · Selected Runtime (atomic/podman/full-destroy) / Executed podman · full-destroy — fail
  8. PR · Selected Runtime (atomic/podman/policy) / Executed podman · policy — fail
  9. PR · Selected Runtime (atomic/podman/reconciliation) / Executed podman · reconciliation — fail
- Green on this head includes: both Native data-capabilities gates, Focused Python, all Go-unit shards, Validation (go-vet/go-build/ci-*), Trusted Plan, Native gate plan, Workflow policy, Exact Candidate, Demo Pin, Runner Interface, Source format, the 8 non-failing Selected Runtime gates (docker+podman × guided/lifecycle/failure/data-capabilities), and both coreless-lifecycle aggregations.
- `gh pr checks 1812 --required` returns only `PR Selected Checks` (fail). required-count=0 in statusCheckRollup → rulesets are disabled (matches the standing note), so the single "required" display is the rollup placeholder, not an active ruleset.
- Older-head (superseded) pull_request runs on branch lane-0428-249-runtime-image-fix: 45940327574 @ d95e46de9d (failure), 45939271268 @ 0b343af5ea (failure), 45931118156 @ 6ab5310d17 (failure), 45930995254 @ 860d41572a (failure), 45915629291 @ 05cb3fd95b attempt 2 (cancelled; both attempts excluded by the coordinator note of 01:22:41Z), and older. Commit 8c83c70914 has NO run row at all (gh api actions/runs?head_sha=8c83c7… and `gh run list --commit` both empty) — the push CI for it never materialized. None of these are terminal evidence for c2dd3ff04.

## (b) Failed jobs and decisive lines (run 45944501306)

Every failing Executed job failed in the single step "Run runtime gate"; the aggregate failed in step "Require normal selected job results". Decisive lines (from job logs via `gh api actions/jobs/<id>/logs`; identical class in all 8):

- docker · policy (job 140326537573, log line 1505; podman twin 140326573644 line 1405):
  - `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state…` (line 1505)
  - `demo-policy FAIL — …/baseharbor-demo-atomic/tests/policy/run.sh:30: assertion command failed (exit 1): return\ 1` (line 1777 podman / summary)
  - `RESULT FAIL` (line 2096)
- docker · connectivity (140326489447; podman 140326525870): same Error at line 1505; `demo-connectivity FAIL — tests/connectivity/run.sh:36 … run_consented "$BAHA" up --yes …` (line 1882); `RESULT FAIL`.
- docker · reconciliation (140326533408; podman 140326484294): same Error; `demo-reconciliation FAIL — tests/reconciliation/run.sh:22 … run_consented "$BAHA" app apply …` (line 2089); `RESULT FAIL`.
- docker · full-destroy (140326484459; podman 140326577053): same Error at 1505; `demo-full-destroy FAIL — tests/full-destroy/run.sh:16: … tee "$ARTIFACT_DIR/full-destroy-after.txt"` (line 1875); plus a cleanup-phase diagnostic `Managed-environment machine operations require an authenticated BaseHarbor operator.` at the post-failure diagnostics — in THIS exact-head run that operator-auth line is cleanup-adjacent only (its scope-result.json shows `"errors": []`, docker-full-destroy.log lines 1934/1943); the PRIMARY error is the identical candidate-consent refusal above. (On the older head 7e42c1e686 the same class WAS the primary error with `operator_not_authenticated`, per the w322 ledger comment 2026-11-26T12:24:10Z.)
- PR Selected Checks (140335189160): step `Require normal selected job results` fail; aggregate reflects the 8 red Executed jobs.

Sub-checks that DID pass inside each failed job prove the gates ran real mutations; only the guided-atomic consent handshake ended red. The guided demo path itself is `tests/guided/run.sh:5` ("Fail-closed guided candidate-consent suite"), :53 (`if ! run_consented "$BAHA" up --yes …`) at demo pin 1a3c055.

Guided-path detail (decisive for classification): the guided atomic bootstrap drives the main app through the PTY driver; the first non-JSON `up --yes` refuses (docker-connectivity job log line 1505, confirm-hash 908778252c3a…), the driver re-runs and reaches READY (`[phase] guided up: READY reached; returning to acceptance gate`). Then the test-body `run_consented` (tests/lib.sh:198 → tests/fixture-consent.py) acknowledges the companion-app refusal exactly once (`isolated-demo-fixture: acknowledge the exact current application source candidate`, docker-connectivity line 1862 / podman-reconciliation 1950+1980, docker-reconciliation 2034+2056), after which the acceptance flow terminates with the same fail-closed message (`Error: record deployment before mutation …`, docker-connectivity final Error at offset after the ack; RESULT FAIL at line 1882/2125 region). In policy and full-destroy the Executed job never reaches a fixture ack at all (`isolated-demo-fixture` count 0 in docker-policy.log / docker-full-destroy.log for the app path; full-destroy only logs the provider-plan ack in cleanup), so the refusal reproduces identically at line 1505 and in the summary at line 2096/2117. The carrier changes no consent logic: measured on `gh pr diff 1812`, `grep -c consent` = 0 and `grep '^diff --git' | grep -i consent` returns no match (19 changed files, listed above).

## (c) Failure classes

All 8 Executed failures + the aggregate are ONE identical signature: fail-closed candidate-consent refusal on `baha up --yes` / `baha app apply` even when the documented `--confirm-candidate <digest>` flag is propagated (ci-operator trace proves the flag reached Core). Classification:

- (iii) Real test-fixture fault in the consumed Demo pin (class "(ii)/(iii) boundary", booked as #283/#284 prerequisite): the PR-gate consumes Demo `1a3c055cc0eef…` (repo variable `BASEHARBOR_PR_DEMO_SOURCE_SHA`, set 2026-11-27T00:24:18Z, artifact `verified-pr-demo-pin` of run 45944501306 = 1a3c055…; job log line 38 `demo_ref: 1a3c055cc0eef3f961722f12d843e33f6c1ca43e`). `tests/fixture-consent.py` at that pin (candidate_confirmation() lines 33–56; main() retry loop lines 161–205, JSON parse at 184, digest extract at 188) acknowledges a current refusal exactly once (`isolated-demo-fixture: acknowledge the exact current application source candidate`, set at 192) and never loops on a second identical refusal; in the guided-atomic bootstrap path the CI operator trace shows the flow as `up`, `up --confirm-candidate` (empty value) then `up --confirm-candidate <digest>` (e.g. docker-connectivity ci-operator.log lines for target atomic-docker-connectivity) — and Core fails closed again with the identical `Error: record deployment before mutation: … (--confirm-candidate)` text, so the fixture exits 1 and run.sh:36/:22/:30/:16 aborts. The product fail-closed boundary itself is `internal/operatorauth/authorization.go:281` (cited verbatim in this PR's own comment at cmd/baha/ci_integration_operator_enabled.go, diff hunk line 1580). This is the exact regression demo PR #183 (OPEN, head ba14b0eed4, "reconcile PTY final-drain capture boundary for candidate-consent digest (0428-284)") targets; #183 changes only tests/guided/drive.py + test_consent_capture.py — the atomic run.sh path consumes the same documented-message contract, and the booked ledger (PR comments of w362, 05:05Z and 05:45Z) already classifies this as the #283/#284 consent-capture prerequisite, unchanged signature across heads 0b343af5e → d95e46de9 → c2dd3ff04.
- (i) trusted-plan/catalog: NOT a factor. `PR · Trusted Plan`, `Native gate plan`, `Workflow policy`, `Demo Pin`, `Focused Python` and all planner tests are GREEN on this exact head; scripts/release-requirements.json on develop contains no demo SHA pins at all (verified by parsing the file: `contains 1a3c055/5ca92a7/58ac706: False`). The 14-light-gate catalog rows (#1837, merged) executed the gates; nothing was skipped.
- (ii) demo-pin / #183: the PRESENT cause route to green. Demo develop already carries 58ac7067 (#182 merged 11:59Z "documented consent flag in new application apply path") and main 2618b396; the docs release pin `docs/releases/v0.4.28.demo-ref` on develop = 5ca92a7cd2 (predates #182; per w255 review note it does NOT carry the fix either — it is "behind" develop by the #182 merge, ahead of 1a3c055 by 0). PR-gate demo source currently = variable 1a3c055cc0; #183 is still OPEN (head ba14b0eed4). So no consumed pin demonstrably fixes the guided-path refusal.
- (iv) infra/runner: NOT a factor for these 9 — jobs ran to completion on GitHub-hosted runners, executed real containers, produced full diagnostics; the earlier runner-health class is fixed by this PR's own concurrency edit set (`.github/workflows/ci.yml` +5-3: cancel-in-progress false, SHA-keyed groups) and no cancellation appears on this head. The only runner-visible oddity: head 8c83c70914 has no pull_request run row at all (4 s gap between the 6ab5310d17 pushes; superseded by 0b343af5ea run) — informational, no gate impact.
- Product side note (file:line): Core behavior itself is fail-closed and correct (`operatorauth/authorization.go:281` boundary, referenced by `cmd/baha/ci_integration_operator_enabled.go` diff comments); this PR's product delta (ci_integration_operator_enabled.go +34: full-destroy `destroy --all --yes --json` / `destroy --all --json` synthetic-operator forms) works — the full-destroy Executed job now passes its destroy step (see resources REMORED, `"destroyed":true` in scope-result) and only the later cleanup diagnostic shows the untouched operator-auth path. Consent/auth logic untouched, as required.

## (d) Ancestry vs origin/develop

Fetched develop = ea5218d72e263f21e79853b679af50074dab8c25 (ls-remote witness above; also git merge-base origin/develop HEAD == ea5218d72).

- `git rev-list --count c2dd3ff04..origin/develop` = 0 → the carrier contains ALL current develop content (no missing develop commits; develop is an ancestor of the head).
- `git rev-list --count origin/develop..c2dd3ff04` = 21 → 21 lane commits on top; `git log --oneline origin/develop..HEAD` lists exclusively w362/w322/w255-lane 0428-249 commits and develop-absorption merges (author witness: `git show -s --format=%an HEAD` = w362-0428-249-1812rebase for the head commit).
- Diff base check: `git diff --name-only origin/develop...c2dd3ff04` = 19 files, byte-identical set to `gh pr diff 1812 --name-only` (19). No foreign content rides on the carrier.

## (e) What a qualifying exact-head run would need (NO qualification claimed)

Per the coordinator acceptance note (PR #1812 comment 2026-11-27T01:22:41Z) and the pair doctrine, qualification on the EXACT head c2dd3ff04 would need TWO distinct executed run IDs on that same SHA:

1. A fresh `pull_request` "CI · PR #1812" run on c2dd3ff04 with the `PR Selected Checks` aggregate SUCCESS (terminal, not skipped/queued) — the authorized second-trigger route is close+reopen (or any real second event), NEVER a rerun (rerun raises run_attempt on the SAME id and is void as pair evidence).
2. The separate 14-gate `Release · Pre-Release Validation` run (pre-release.yml, workflow_dispatch on a ref whose resolved candidate = c2dd3ff04) on the same exact candidate, with its gate rows green.

Why the current state does not meet either:
- Requirement 1: the only pull_request run on c2dd3ff04 is 45944501306 = completed/FAILURE (9 failed checks, run_attempt 1, no sibling). A second distinct executed ID on this SHA does not exist.
- Requirement 2: the dispatch would resolve candidate = ref head = c2dd3ff04 and demo from `docs/releases/v0.4.28.demo-ref` = 5ca92a7cd2 (pre-release-runtime-suite resolve step reads the docs pin; run 45918769472 REJECTED earlier dispatch precisely on a pin mismatch class), and that pin — like every current published Demo ref (develop 58ac70679e, main 2618b39623) — contains the SAME run_consented/fixture-consent code as 1a3c055 (verified byte-identical for tests/connectivity/run.sh and tests/fixture-consent.py across those refs), i.e. the guided-atomic consent-capture defect demo #183 is still fixing. So a second distinct pull_request run on THIS head reproduces the identical 8-gate failure signature; the pair requirement cannot be satisfied by this head alone while the prerequisite stands.
- Unblocking route (stated as diagnosis, not instruction): merge demo #183 → advance the PR-gate demo source (owner-set repo variable and/or the docs pin) to a head carrying the reconciled consent capture → push a content-carrying commit to #1812 (or use the authorized close+reopen) → obtain the two distinct green run IDs on that new exact head. Until then #1812 remains correctly parked per the owner's serial-behind-#183 ruling.

## Findings (for coordinator/Codex, no action taken by this lane)

- F1: Demo #183 (OPEN) must merge before any second exact-head run of #1812 can pass the 8 Selected Runtime gates; every currently published Demo ref (5ca92a7, 58ac706, 2618b396, 1a3c055) carries the identical failing consent path (byte-compare of tests/connectivity/run.sh + tests/fixture-consent.py).
- F2: `docs/releases/v0.4.28.demo-ref` (5ca92a7cd2) predates demo #182; the w255 pin-decision comment (2026-11-26T12:57:35Z) says this docs pin must not be claimed as the tested source when the repo variable overrides it. When #183 lands, both the variable AND (per release policy) the docs pin path need a consistent, recorded decision.
- F3: informational — head 8c83c70914 has zero CI run rows (race with the 6ab5310d17 force-adjacent pushes); no evidence value, excluded from the ledger.

## w394-0428-249-1812diag (4 fields)

- LANE: w394-0428-249-1812diag — read-only DIAGNOSE, no push/merge/rerun/dispatch/gate change performed.
- RESULT: run 45944501306 (the only run on exact head c2dd3ff04) = completed/failure; 9 terminal failures = 8x PR · Selected Runtime Executed gates + PR Selected Checks aggregate; census 61/9/68 reproduced.
- CAUSE: known demo consent-capture class (#283/#284 prerequisite, fix route demo #183, OPEN); carrier is current-develop-complete (0 behind), contains no consent-logic delta, all other PR-gate checks green on this head.
- NEXT: coordinator/Codex disposition of findings F1–F3; qualification NOT asserted by this lane; two distinct exact-head run IDs (fresh pull_request aggregate-green + separate 14-gate Pre-Release Validation) remain required and are currently impossible on this head.

## ledger (4-field)

- What: Read-only diagnosis of the terminal failure of run 45944501306 (exact head c2dd3ff04, PR #1812).
- Evidence: this akte on plan main + run/job/check census commands listed above (gh api endpoints quoted).
- Blockers: none for this lane; PR #1812 itself is blocked on demo #183 (class (ii)/(iii)) per F1.
- Next: coordinator/Codex dispositions F1–F3; no re-run, push, merge or gate change by this lane.

## cleanliness

- No containers/compose started by this lane (read-only API/log work only). `docker ps` not needed on this host (no daemon use here per rules); no VM access.
- Scratch: /tmp/opencode/w394-logs/*.log (job logs), /tmp/opencode/*.py|*.sh (Demo file fetches for byte-compare), all in /tmp/opencode per fixed workspace layout.

END_BLOCKED w394-0428-249-1812diag: diagnosis complete — run 45944501306 on exact head c2dd3ff04 fails only on the known demo consent-capture class (#183/#283/#284 prerequisite); carrier is current-develop-complete (0 behind); qualification NOT asserted; PR stays blocked serial behind demo #183.
