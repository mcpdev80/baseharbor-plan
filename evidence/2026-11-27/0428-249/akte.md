# w362-0428-249-1812rebase — Evidence (akte, card closure per ruling 2026-11-27T04:24:55Z)

Lane: w362-0428-249-1812rebase · Card 0428-249 · Repo: baseharbor · PR #1812
Branch: lane-0428-249-runtime-image-fix · Candidate head: `0b343af5ea895d23cbe808fda50a66d550552bc6`
(delivered by ONE normal push `6ab5310d1..0b343af5e`, no force; witnesses: ls-remote branch +
refs/pull/1812/head and `gh pr view 1812 --json headRefOid` all = 0b343af5e, 2026-11-27 ~04:22Z)

Full working record (edit-set spec, terminal-log class diagnosis, carrier table, owner-ruling
sequence) lives in `w362-0428-249-1812rebase-editset.md` in this evidence tree; published via plan
PRs #172/#174/#175/#176. This file is the card's canonical akte closure.

## ANSATZ (identity)
- git identity 4-Feld on all candidate commits: `w362-0428-249-1812rebase`
  (`w362-0428-249-1812rebase@baseharbor.local`), verified pre-push via `git show -s --format=%an HEAD`.

## Fresh exact-head run (Eigenes-Run-Pflicht)
- Run **45939271268** (pull_request, head 0b343af5e) — watched to terminal in this session; census
  (per_page=100) and native Docker/Podman gate naming recorded below at terminal.
- Prior-run ledger (all non-current, per owner): 45915629291 VOID (rerun-attempt pair, not evidence);
  45930995254 + 45931118156 proof runs terminal FAILURE with class-by-class diagnosis in the editset
  akte (static classes 1-4 carriers = now-pushed 8c83c7091+0b343af5e; class 5 'Selected runtime'
  consent-refusal booked as #283/#284 prerequisite — NOT repaired on #1812); 45918769472 REJECT
  (validation-workflow dispatch, demo pin INPUT_DEMO_REF).
- Carrier ancestry at push head: ea5218d72 → … → 6ab5310d1 (remote; ruling content: cancel:false,
  SHA-keyed groups, Podman single-default split) → 8c83c7091 (targeted-integration expression fixes
  + targeted-demo + supplemental groups) → 0b343af5e (narrow test-only fixtures, positive+negative
  coverage retained). `git merge origin/develop` (ea5218d72) was "Already up to date" — no conflict.

## Third-file authorization executed (coordinator disposition 04:29:07Z)
- `scripts/test_ci_single_default_route.py` (assertion region around :98 ONLY, +19/−1): per-workflow
  positives — docker keeps its `  single_default_native:` positive; podman enumerates the five split
  jobs (`keycloak_single_native`, `single_default_native_sql_secrets`, `single_default_native_node_https`,
  `single_default_native_install_destroy`, `single_default_native_pinned_workload`) AND gains the
  negative `assertNotIn("  single_default_native:\n")` on the retired monolithic job name. Static
  verification (assertion logic only, NOT a test run): all positives pass on both candidate workflow
  files, and the negative provably fails on the pre-split form (ea5218d72) — coverage did not shrink.
  No other file touched; no product/workflow edit; ci.yml untouched.
- develop advance check: ls-remote develop = ea5218d72 (unchanged, candidate already contains it via
  709a9b1be) → no merge needed per condition (3).
- ONE forward commit `d95e46de9` (4-Feld w362 verified: an=ae=cn=ce=w362-0428-249-1812rebase); ONE
  normal push `0b343af5e..d95e46de9`. Witnesses: ls-remote branch + refs/pull/1812/head =
  `d95e46de9df009055399938bcd8a2f472c1fa32e`; `gh pr view 1812 --json headRefOid` identical.
- Fresh exact-head run **45940327574** on d95e46de9 — watched to terminal in this session (Watcher
  sh_21b4545a5001rv1vUMlrfyTVCb); per_page=100 census with BOTH native Docker and Podman gates and
  error classes recorded below at terminal. Run 45939271268 (head 0b343af5e) is superseded by the
  authorized third-file fix and remains in the ledger as the MELD-evidence run.

## Terminal census — run 45940327574 (head d95e46de9) = completed/failure (terminal ~05:00Z)
- 138 jobs (per_page=100 census): 60 success, 10 failure, 68 skipped.
- **Both native gates GREEN (namentlich):** `PR · Native · native/docker/data-capabilities`
  (140312972801) and `PR · Native · native/podman/data-capabilities` (140312972722) = success.
  All static classes green: `Workflow policy`, `Trusted Plan`, `Native gate plan`, `Source format`,
  `Exact Candidate`, `Demo Pin`, `Runner Interface`, `Candidate-added checks (advisory)`,
  `Validation · ci-actionlint` + `ci-executor-tests` + `go-build` + `go-vet`, all Go unit shards.
- Failure class A (FOURTH fixture file — outside every issued authorization; MELD, not fixed):
  `PR · Focused Python` (140313019507), exactly ONE subtest: `test_pr_runtime_workflow_shape.py:18`
  `test_exactly_one_unconditional_reusable_gate_job`, `AssertionError: Lists differ: ['gate'] !=
  ['resolve_candidate', 'gate']` — the 0428-249 edit set added the `resolve_candidate` job to
  `.github/workflows/pre-release-runtime-suite.yml` (witness: `git show 6ab5310d1:…` has
  `resolve_candidate:` at line 10 + `gate:` at 31; base ea5218d72 has only `gate:`), and this
  shape-fixture pins the job-name list. Fix would belong to the same narrow test-only family
  (positives on both jobs, e.g. assertIn `  resolve_candidate:` + gate-unconditional assertions
  retained), but requires an explicit authorization like the 04:29:07Z third-file disposition.
- Failure class B (KNOWN, #283/#284 prerequisite, unchanged signature): eight
  `PR · Selected Runtime` gates (docker/podman × connectivity/policy/reconciliation/full-destroy,
  140313783746/140313816781/140313821165/140313836179/140313883992/140313942543/140313958453/
  140313993651) + downstream `PR Selected Checks` (140322747354). Identical consent-refusal line:
  `Error: record deployment before mutation: candidate submission requires an explicit
  operator/automation consent (--confirm-candidate); refusing to record deployment state`
  (demo run_consented path). Not attributable to the edit set; no waiver, no repair here.
- Class-A fix from run 45939271268 (test_ci_single_default_route.py) CONFIRMED green at this head —
  its subtest no longer appears among failures.

## Terminal census — run 45939271268 (head 0b343af5e) = completed/failure (terminal ~04:33Z)
- **Both native gates GREEN (namentlich):** `PR · Native · native/docker/data-capabilities`
  (job 140309633126) = success; `PR · Native · native/podman/data-capabilities` (job 140309633103)
  = success. Also success: `Workflow policy`, `PR · Trusted Plan`, `PR · Native gate plan`,
  `PR · Source format`, `PR · Exact Candidate`, `PR · Demo Pin`, `PR · Runner Interface`,
  `PR · Candidate-added checks (advisory)`, `PR · Validation · ci-actionlint`,
  `ci-executor-tests`, `go-build`, `go-vet`, all `PR · Go unit` shards.
  → Classes 1-4 (actionlint ×2, check_routes fixture, executor-tests fixture) are FIXED at this head.
- Failure class A (fixed by the authorized third-file d95e46de9): `PR · Focused Python`
  (140309641868), exactly one subtest — `test_both_existing_runners_gate_develop_push_by_selector
  (workflow='...podman-acceptance.yml')` (test_ci_single_default_route.py:98).
- Failure class B (KNOWN, booked #283/#284 prerequisite, NOT repaired on #1812): the eight
  `PR · Selected Runtime` gates (docker+podman × connectivity/policy/reconciliation/full-destroy,
  jobs 140310098645/140310099076/140310102122/140310137371/140310137642/140310140189/140310153741/
  140310173791) + downstream `PR Selected Checks` (140320611239). Exact log signature identical to
  the 6ab5310d1/860d41572 proof runs: `Error: record deployment before mutation: candidate
  submission requires an explicit operator/automation consent (--confirm-candidate); refusing to
  record deployment state` (demo run_consented path, tests/.../run.sh:36 family) with transient
  per-job-registry `blob unknown` retries. Standalone-pair consistency: same class as the consent
  line the owner booked for #283/#284 — no waiver, no repair here.

## Hosted CI gate census (run 45939271268, early)
- In-progress census at ~04:24Z (per_page=100, 104 jobs): GREEN so far — `Workflow policy`,
  `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Source format`, `PR · Exact Candidate`,
  `PR · Demo Pin`, `PR · Runner Interface`, `PR · Candidate-added checks (advisory)`, all
  `PR · Validation · ci-actionlint/ci-executor-tests/go-build/go-vet`, all `PR · Go unit` shards.
  Classes 1-4 (actionlint ×2, Focused Python carriers, ci-executor-tests) are FIXED by the push
  (they were the failure carriers on 45931118156/45930995254).
- Native gates: `PR · Native · native/docker/data-capabilities` and
  `PR · Native · native/podman/data-capabilities` BOTH started (in_progress) — the pair evidence.
- One failure at early census: `PR · Focused Python` (job 140309641868) — exactly ONE failing
  subtest: `test_both_existing_runners_gate_develop_push_by_selector
  (workflow='.github/workflows/podman-acceptance.yml')` in
  `scripts/test_ci_single_default_route.py:98`. It asserts the OLD un-split job name
  `  single_default_native:`, which the accepted edit set (6ab5310d1) split into five jobs
  (`single_default_native_sql_secrets`, `single_default_native_node_https`,
  `single_default_native_install_destroy`, `single_default_native_pinned_workload`,
  `keycloak_single_native`); the docker-side subtest of the same case still passes (docker keeps its
  un-split `  single_default_native:` job). Carrier status: this third file is NOT covered by the
  w267 two-file authorization (rule 2 lists only test_ci_check_routes.py +
  test_pr_selected_runtime_matrix.py), and rule 3 makes any further-file repair a MELD case, not a
  self-fix. Reported as MELD — no self-initiated fix, no retry, no further push.
(pending terminal for final census + remaining native gate conclusions)

## Sequencing (owner ruling 04:24:55Z)
- #1812 chain stays serial behind demo #183: merge only after #183 green+merged and the PR demo pin
  (repo variable BASEHARBOR_PR_DEMO_SOURCE_SHA) advances. No further push, no self-initiated retry
  by this lane.
- Correction of record: develop (ea5218d72) does NOT carry the runner-health ruling; only this
  candidate does (booked as coordinator's own error, owner 04:24:55Z). The fresh exact-head run is
  the develop-green witness for this merge base.

## PR #1812 handoff comment
Posted at https://github.com/mcpdev80/baseharbor/pull/1812#issuecomment-7210342591 with the full
run ledger and ls-remote witnesses (branch + refs/pull/1812/head = d95e46de9df009055399938bcd8a2f472c1fa32e;
develop ea5218d72).

## Final per-job evidence harvest (run 45940327574, head d95e46de9) — owner request 05:05:43Z
10 failed jobs, each with log line + carrier and class attribution:
1. `PR · Focused Python` (140313019507) — log: `FAIL: test_exactly_one_unconditional_reusable_gate_job
   ( … )`, `File "…/scripts/test_pr_runtime_workflow_shape.py", line 18`, `AssertionError: Lists
   differ: ['gate'] != ['resolve_candidate', 'gate']`. Class: **stale-shape assertion (FOURTH-file
   family)** — the edit set added `resolve_candidate:` to `.github/workflows/pre-release-runtime-suite.yml`
   (witness: `git show 6ab5310d1:…` job list) while the fixture pins the old single-job list.
   NOT in any issued authorization → **MELD with witness, not repaired** (rule: scope-exceeding class
   = report, per 04:29:07Z-style disposition needed). The already-authorized third-file fix
   (test_ci_single_default_route.py) is confirmed GREEN at this head (no FAIL from that file).
2-9. Eight `PR · Selected Runtime` gates (docker/podman × connectivity/policy/reconciliation/full-destroy;
   jobs 140313816781/140313883992 = demo-connectivity FAIL, 140313821165/140313958453 = demo-policy
   FAIL, 140313993651/140313942543 = demo-reconciliation FAIL, 140313836179/140313783746 =
   demo-full-destroy FAIL). Log line on all eight: `Error: record deployment before mutation:
   candidate submission requires an explicit operator/automation consent (--confirm-candidate);
   refusing to record deployment state` + `demo-<gate> FAIL — …/run.sh:36 assertion command failed`.
   Policy/full-destroy sub-lines mention keycloak/server-key only inside the demo journey (same
   refusal root; no distinct Keycloak server.key failure class observed at this head). Class:
   **known #283/#284 prerequisite (operator targets / --confirm-candidate consent)** — unchanged
   signature on all four heads 860d41572/6ab5310d1/0b343af5e/d95e46de9; NOT repaired on #1812.
10. `PR Selected Checks` (140322747354) — downstream aggregator of 2-9. Same known class.
Native pair at this head: **both GREEN** (`native/docker/data-capabilities` 140312972801,
`native/podman/data-capabilities` 140312972722). No #183-capture class and no matrix-ref class
failures remain (both fixed by the pushed carriers).

## END line
END (no push, no retry, no cancel, no merge — #1812 stays serial behind demo #183): head
`d95e46de9` delivered (ls-remote branch + refs/pull/1812/head + headRefOid all =
d95e46de9df009055399938bcd8a2f472c1fa32e); exact-head run 45940327574 terminal FAILURE with
classes [native-pair GREEN; stale-shape FOURTH-file `test_pr_runtime_workflow_shape.py:18` —
MELDED, out of scope; 8× Selected Runtime + aggregator = known #283/#284 consent class].
Vorlauf 45939271268 (0b343af5e) terminal FAILURE, classes [third-file single_default_native —
fixed by d95e46de9; same known consent class]. Ledger commented on PR #1812.
