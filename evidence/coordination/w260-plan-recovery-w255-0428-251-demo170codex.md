# w260 Plan recovery — w255-0428-251-demo170codex

Base attestation: live `origin/main` resolved by `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` to `264e2632319bdab152e7b03b7bd8bd0b3656bce9`; this is the exact commit from which this detached worktree was created before branch creation. `git remote -v` verified the real GitHub remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

Visible author block: source card 0428-253 frontmatter at this base says exactly `owner: w205 (lane w205-0428-253)`; this does not authorize using that identity. The edited existing 0428-273 card frontmatter at this base says exactly `owner: w65-0428-269-batchbaseline`; its owner field is unchanged, and the factual update is an Owner ruling published by this executing lane, not an adoption of the w65 identity. The executing lane identity is `w255-0428-251-demo170codex`, with git user.name `w255-0428-251-demo170codex` and git user.email `w255-0428-251-demo170codex@baseharbor.local`. Planned literal commit invocation: `git -c user.name="w255-0428-251-demo170codex" -c user.email="w255-0428-251-demo170codex@baseharbor.local" commit -m "Restore missing Plan evidence forward-only"`. Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.

## PLAN

1. Verify live Plan `origin/main` equals the attested SHA; inspect mission inventory, each original PR file list and the current task-card state.
2. Fetch original PR heads #44, #51, #57, #58, #61, #62, #65 and #66; restore only genuinely missing mission paths, choosing newest source #58 for #51/#58 duplicates and #61 for #57/#61.
3. Prove each restored blob equals its source PR head and record path, source PR, original blob SHA and restored blob SHA.
4. Record forward-only disposition of the w254/w65-identity and w258 direct-main publications, including content assessment and invalid publication channel; preserve their commits and source evidence unchanged. Record the prior #1819 preflight as sound point-in-time content but unqualified until compliant disposition.
5. Review the exact Plan diff, commit with the executing lane identity, push one branch, open one scoped Plan PR, and wait for Hosted Plan validation SUCCESS on its exact final head.
6. Review #1650 at exact head for content and commit identity, record that its same-head run pair remains incomplete, and analyze w270’s #170/#179 trigger evidence; do not merge or trigger unrelated runs.
7. Merge only after exact-head Plan validation succeeds; verify every restored artifact and the w258 source path on fetched live main, record PR/run/main witnesses, and update the lane board.

## Initial state

Live main witness: `264e2632319bdab152e7b03b7bd8bd0b3656bce9`. No product repository changes or local tests are in scope. The mission requires one ordinary forward-only Plan PR, no force push, no history rewrite, and no direct-main write.

## Artifact verification

Pending.

## Hosted validation and publication

Pending.

## Cleanliness

Before witness (PID `1957824`): `docker ps -a` showed only the table header and no containers. No Docker/Podman stack was started by this lane. Final witness pending.

## Verified source heads and restored blobs

The following original refs were fetched directly from `https://github.com/mcpdev80/baseharbor-plan.git` as `refs/pull/N/head`. GitHub Files API path inventories matched the selected paths. For duplicates, the newer #58 head was selected over #51 and #61 over #57. For every restored file, `git diff --quiet <source-ref> -- <path>` exited 0; original and staged blob IDs are identical.

| Path | Original PR | Original blob SHA | Restored blob SHA |
| --- | --- | --- | --- |
| `evidence/2026-11-28/w247-0428-285-1820hop.md` | #44 (`a1af2fe8373894a18346cf7b8e9c58d75de2c536`) | `b0b06ff5aa5f2fe26644982db4a9ceccdf54306b` | `b0b06ff5aa5f2fe26644982db4a9ceccdf54306b` |
| `evidence/r28-welle6-2026-11-26/1851-carrier/disposition.md` | #58 (`8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`) | `1ce4af41f86b30a4e1219b938bcc259b138eb8c3` | `1ce4af41f86b30a4e1219b938bcc259b138eb8c3` |
| `evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md` | #58 (`8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`) | `f7d8f48f00884f3a1daf26cb85f35fa91158f664` | `f7d8f48f00884f3a1daf26cb85f35fa91158f664` |
| `evidence/r29-welle6-2026-11-28/0428-284/w136-demo-prgate-availability.md` | #58 (`8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`) | `b2660bab864e3e1fca5675e1dfa0993d4938b14e` | `b2660bab864e3e1fca5675e1dfa0993d4938b14e` |
| `evidence/2026-11-26/w249-0428-284-gateids/akte.md` | #58 (`8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`) | `0a49b2349f8259818b4fb02e21b554b6293afe6e` | `0a49b2349f8259818b4fb02e21b554b6293afe6e` |
| `evidence/e6ca7696-b1f8-492d-b226-876b16925fc5/w245-0428-284-1842alt/akte.md` | #58 (`8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`) | `def3a593ce6ec8c514968783da41f713ab205ae9` | `def3a593ce6ec8c514968783da41f713ab205ae9` |
| `evidence/r29-welle6-2026-11-26/0428-284-1842alt/routing-alternatives.md` | #58 (`8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`) | `dd56513369d6008c389e92a679becada8e454123` | `dd56513369d6008c389e92a679becada8e454123` |
| `evidence/w248-0428-284-boardscan/akte.md` | #58 (`8b7ad11572e9ccc2cd0db37bf7d2259ab7460666`) | `3d6461e3cc9d4510a0be2545764603bfb4f82870` | `3d6461e3cc9d4510a0be2545764603bfb4f82870` |
| `evidence/verify/w253-demo170179-census.md` | #61 (`ac1a0e9f0c0a9bba840a8fea9c8a1546c869c739`) | `600636e2aff943d54dc7095a6a926a3aef0a2b10` | `600636e2aff943d54dc7095a6a926a3aef0a2b10` |
| `evidence/r28-welle6-2026-11-26/w252-1833-1835-disposition/disposition.md` | #62 (`f6fdecf7060ae612a8df1c3946fd0f3e52a28c52`) | `72a6e6cdc2a8d23a2089fdaca8502c511f3c9d9b` | `72a6e6cdc2a8d23a2089fdaca8502c511f3c9d9b` |
| `evidence/w246-1812diag/w246-1812gatefaildiag.md` | #65 (`868f014feabcc5196540066c254eedb1f8342d02`) | `9781ec653c1650702ab28613fbe3d8fa2dc27eca` | `9781ec653c1650702ab28613fbe3d8fa2dc27eca` |
| `evidence/w255-0428-251-demo170codex/decision.md` | #66 (`1a9317acfa3b04e9925e320bdcb0494c581ec06b`) | `6468d3a7e703db2959b0b9ce8793c547912f08d2` | `6468d3a7e703db2959b0b9ce8793c547912f08d2` |

The additional #51/#58 paths `evidence/r29-welle6-2026-11-28/0428-253/w136-1853-verdict-line.md` and `tasks/t-20261123-planner-deleted-source-advisory.md` were not restored: the former is outside the mission artifact list; the latter already contains the #68 admission note at base `264e263` and was not overwritten. The task-card history since the prior base includes #68 at `264e263` and the earlier reset point `76ab859`; the current owner note is preserved.

## Forward-only provenance disposition

- w254 catalog finding: the content that the #1819/#1820 rows were already present is sound and is corroborated by BaseHarbor #1822 merge `90086a1f938e106171b08c76e9bcbc98d89d1de4`. Direct-main commit `9e9e53cf775699b4ea80bd8e72e776e3bce61ad1` has parent `76ab859144661e7fdabdc10e36b9cee5f3ce99ad`, author and committer `w65-0428-269-batchbaseline`, zero associated PRs, and is an ancestor of current Plan main. The earlier coordinator-identified commit `aea8cb43088280678b53aea42ca07e25d996a5b8` has parent `a68b2af3ca51560f83f69888d6611867eab0faae`, author `w65-0428-269-batchbaseline`, committer `w248-coordinator`, and is not an ancestor of current main after the recorded regression; its object is locally available, while GitHub’s associated-pulls endpoint no longer resolves it. The coordinator identifies it as a direct-main publication with no associated PR. Both are foreign author identity for w254 and do not qualify w254 lane evidence. This akte changes neither commit nor history and restates the factual result through the current Plan PR.
- w258 #1819 preflight: content is sound as a point-in-time assessment of its recorded develop `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`, #1819 head `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`, and #1812 head `0922888af8fd70be4049cec529c69aebc057a356`: non-empty four-file payload, catalog paths resolve to focused runtime gates, seam-C resolves on the #1812-carrying head, merge-tree was clean, and eight foreign carried commits make the #1819 candidate unqualified until cleaned. Its report is not current #1819 qualification. The akte path `evidence/w258-1819-preflight/akte.md` was introduced/updated by direct-main commit `053b2b6d1af11ad0f926949ef39c7fdbf0e400bf`, parent `08b1f66bb733d4c1422135429e5bc29fbd67cd57`, author and committer `w258-0428-273-1819preflight`, with zero associated PRs. That publication channel is invalid for acceptance evidence. Preserve the commit and source file unchanged; this report records the content assessment and invalid channel using the compliant Plan PR.
- Card 0428-273 is updated without changing owner/frontmatter: rows are already present via #1822; #1812's 14-Light-gate qualification remains unproven. PR #1650 is open, currently head `37c4d847ca377d1555163ac4791c8ba08b85de77` on develop `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`. Run `45663047993` succeeded only for older head `1c33e910070a07a6d4105f0d38e3c89988a788a3`; it executed Docker data-capabilities, Docker observability, Podman data-capabilities, and Podman observability selections, not an exact-head #1812 14-gate qualification. It is stale for the current PR and does not qualify merge or #1812 acceptance.

## Plan validation and cleanliness preflight

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 10 existing dependency warnings across 776 tasks. Render changed only unrelated generated `tasks/t-20261122-runtime-broker-health-unhealthy.md`; that render-only change was restored in this isolated worktree and is excluded from the candidate. No local tests or product tests were run. The Plan branch contains only mission restorations, the explicitly commissioned 0428-273 factual note, and this recovery report.

## #1650 scoped review observations — w267 owns the final bounded review

Owner clarification assigns the bounded product PR review/merge decision to w267; this Plan akte does not claim a final independent product review and does not merge or trigger anything on BaseHarbor. The following are direct read-only observations for that reviewer and for the commissioned provenance classification.

- Card 0428-078 frontmatter owner at base `264e263` is exactly `w165-0428-078-pr1650-basehop`. On live PR #1650 head `37c4d847ca377d1555163ac4791c8ba08b85de77` (base develop `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`), commits `ed2fb751a45ee437157d5bd991c61cd93f12a6dc` and `f89f506f50c2b5f8b200a7847018bf2353ee3074` have author `w181-0428-doclink-sweep` and committer `w165-0428-078-pr1650-basehop`. The canonical author gate compares `%an`; `w181-0428-doclink-sweep` is a different lane, not a shortened form of the card owner. Classify these two authorships as genuinely foreign; route forward reissue through Coordinator, with no rewrite, force push, or silent amend.
- Run `45734193200` is exact-head `pull_request`, attempt 1, terminal SUCCESS; its 43-job census has successful `PR Selected Checks`, `PR · Trusted Plan`, `PR · Source format`, `PR · Native gate plan`, and all four selected Docker/Podman data-capabilities and observability runtime gates. Distinct second run `45737093207` is exact-head `pull_request`, attempt 1, triggered after mcpdev80 closed at `2026-11-26T01:38:13Z` and reopened at `01:38:15Z`; it was in progress when this observation was recorded. No rerun was requested or started by this lane. The pair is complete only if this second distinct run reaches terminal SUCCESS with required selected jobs executed.
- Card 0428-078 Required checks at `tasks/t-20261114-r28-perses-dashboard-identity.md:69-71` require focused checks, with isolated Docker and rootless Podman only when runtime risk requires them; they explicitly reject a blanket full matrix. `scripts/pr-gate-plan.py:1915-1961` resolves changed paths through the coverage catalog and sets the selected runtime gates; `scripts/pr-gate-coverage.json:1714-1737` maps the status/CLI paths to Docker+Podman observability, and `:2659-2665` maps the witness source to Docker+Podman data-capabilities. Thus skipped HA, generic `PR · Native`, and `PR · Native Keycloak/Core` cells are not independently required for this card's admission; the four selected runtime gates actually executed. This does not cure the content findings below.
- Candidate content has a concrete target-binding mismatch: `internal/metrics/identity_dashboard_witness.go:145-154` derives the expected registry ID as `keycloak:<manifest-name>`, while the producer at `internal/identityprovider/keycloak_realization.go:133-138` registers `keycloak:<KeycloakFiles.Project>`. Application-scope project construction at `internal/identityprovider/keycloak_files.go:411-421` uses `ApplicationProjectName(namespace, app.Name + "-identity", environment)`, not the manifest name. The candidate also adds no direct test of `IdentityDashboardWitnessAt` or the serialized positive/negative status field; the only changed test file adds fixture environment isolation. Finally, the candidate diff does not include a production Perses identity panel provisioning/export consumer, and the card's Owner decision at lines 237-241 expressly holds merge until that 0428-181 delivery consumer exists. These are concrete review inputs for w267; green hosted gates alone do not establish functional acceptance.
- Selector verdict: no blanket skipped-native requirement is imposed by the card for this path; run 457341's four selected runtime jobs satisfy the card's Docker/Podman selection condition. The exact run census and pair status remain separate from content and identity acceptance.

## Demo #170/#179 PR-event route decision

No w270 Plan PR/branch was available in the w270 case checkout or in the Plan PR search at review time. The read-only w270 mission is `coordinator/missions/w270-demo-170179-routespec.txt`; current refs and files were independently checked from the real Demo GitHub remote, with no Demo writes or triggers.

Decision: use only the existing `.github/workflows/pr-config-matrix.yml` `pull_request` route, with `branches: [develop]` retained. On live develop, the workflow has `pull_request` at lines 4-6 and `tests/config-matrix/**` at line 14. That path already matches #170's only changed file `tests/config-matrix/run.sh`, so the path filter alone does not explain #170's missing PR run; do not assert an unproven cause. #179's four changed test paths are absent from develop's filter but already appear on main's equivalent filter.

Owner-scope minimal patch for the Demo workflow, not applied by this lane:

```diff
 on:
   pull_request:
+    types: [opened, synchronize, reopened, ready_for_review]
     branches: [develop]
     paths:
       - .github/workflows/pr-config-matrix.yml
       - baseharbor-core.ref
       - compose.yaml
       - scripts/acceptance.sh
       - scripts/failure-runtime-diagnostics.sh
       - scripts/install-baseharbor.sh
       - tests/config-matrix/**
+      - tests/connectivity/run.sh
+      - tests/full-destroy/run.sh
+      - tests/policy/operator-test-certificate.sh
+      - tests/reconciliation/run.sh
       - tests/fixture-consent.py
       - tests/lib.sh
```

The explicit activity list preserves the current default `opened`, `synchronize`, and `reopened` events and adds `ready_for_review`; it keeps the base branch and existing path filters, adds only #179's four missing paths, and introduces no push duplicate, permission, secret, or behavior change for unrelated paths.

Qualification order and owner event authority: #170 first (OPEN, non-draft, head `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`); after the Owner workflow patch is on develop, require two distinct executed `pull_request` run IDs on that exact head, with the second produced by the Owner-authorized close+reopen event. #170's previous run `45663390190` is `push`, failed with `jobs=[]`; it is a dispatch failure, not a test failure. The #170 existing path match means the trigger cause remains unproven until a real PR event executes. #179 is OPEN/DRAFT at `cda6aa70e80bec1a1db06d85decdd8833cb63994`; leave it draft until its owner authorizes readiness, then require a `ready_for_review` run and a second distinct same-head `pull_request` run by Owner-authorized close+reopen. Its previous run `45688177820` is `push`, failed with `jobs=[]`, not a test failure. Record both run IDs, event, head, attempt, and per-page-100 job name/status/conclusion census when qualification occurs.

Exact live Demo refs checked: develop `5ca92a7cd2f746934890cfd7096a48068bdf218e`, main `2618b3962330509add5bf265522995da2a9034ce`, #170 `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`, #179 `cda6aa70e80bec1a1db06d85decdd8833cb63994`. #170 changed only `tests/config-matrix/run.sh`; #179 changed `tests/connectivity/run.sh`, `tests/full-destroy/run.sh`, `tests/policy/operator-test-certificate.sh`, and `tests/reconciliation/run.sh`. The restored `evidence/w255-0428-251-demo170codex/decision.md` already contains this route decision, and this recovery akte restates it; that decision is included in this same recovery PR.

## Demo-route correction after Plan PR #72

Plan main advanced after the initial route census. PR #72 (`b3ffd617c58026c905c484ba37c1da181aa1fec8`) published `evidence/w269-0428-251-179pre/akte.md`; I read it from the fetched main tree and independently checked the current Demo refs. It provides the missing historical workflow-availability fact: `.github/workflows/pr-config-matrix.yml` was absent from Demo default branch `main` when the old #170/#179 heads were pushed and reached `main` only via Demo PR #180 at merge `2618b3962330509add5bf265522995da2a9034ce`. That explains why no PR workflow was available at the earlier events. The default-branch availability condition is now met because the file exists on current main.

Current branch-copy state: Demo main's workflow already has the four #179 test paths at lines 14-17; its pull_request types do not include `ready_for_review`. Demo develop's workflow keeps `tests/config-matrix/**` at line 14 for #170 but lacks the four #179 paths and lacks explicit `types`. Therefore the minimal durable Owner change is to converge the existing workflow copies for `main` and `develop`: add `types: [opened, synchronize, reopened, ready_for_review]` in each copy; keep `branches: [develop]`; add the four #179 paths only to the develop copy (they are already in main). Do not add a second workflow, a push trigger, permissions, or secrets. The workflow owner must apply/synchronize this because `.github/**` is Owner scope.

The corrected #170 assessment is: its file path matched the develop filter, but at the original event time the workflow did not yet exist on default main, so there could be no PR-event run. The filter is not the historical cause. Now that the default-branch workflow exists, an Owner-authorized reopened event on #170's exact head can produce the first real PR run; the second distinct run must follow via the Owner-authorized close+reopen sequence. #179 remains draft and needs the explicit `ready_for_review` activity plus its four develop path entries before its readiness event can select this workflow. Keep both PRs on their exact current heads and record two distinct run IDs, each `event=pull_request`, terminal SUCCESS, with executed jobs and per-page-100 job census including attempts.

Current Demo source witnesses remain: main `2618b3962330509add5bf265522995da2a9034ce`, develop `5ca92a7cd2f746934890cfd7096a48068bdf218e`, #170 `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`, #179 `cda6aa70e80bec1a1db06d85decdd8833cb63994`. Prior push runs `45663390190` and `45688177820` remain `jobs=[]` dispatch failures, not test evidence.

## Recovery branch base integration

The recovery branch was cut from exact live Plan main `264e2632319bdab152e7b03b7bd8bd0b3656bce9`. Before PR creation, live main advanced to `b3ffd617c58026c905c484ba37c1da181aa1fec8` through PR #72, whose only changed path is `evidence/w269-0428-251-179pre/akte.md`. I integrated that exact current main into this branch with ordinary merge commit `33ee934e896dd818a9c1eac320acca2571d2a08c`; no conflict or rebase occurred. This main tip is now an ancestor of the candidate.

## Owner demo-route witnesses and pending w274 mechanism finding

The coordinator supplied API witnesses read at approximately 01:5xZ: workflow `.github/workflows/pr-config-matrix.yml` is active on Demo default `main` (workflow ID 430588588); that default-branch copy's `paths` include #170's `tests/config-matrix/run.sh` and all four #179 changed test files (`tests/connectivity/run.sh`, `tests/full-destroy/run.sh`, `tests/policy/operator-test-certificate.sh`, `tests/reconciliation/run.sh`). Check-runs on #170 head `b086cf58b` and #179 head `cda6aa70e` are zero, with no `pull_request` runs. Instead, the cited approximately eight workflow runs are `push` events with conclusion `FAILURE` and empty jobs: 45726589547, 45726404672, 45688177820, 45663390190, 45661078349, 45660181295 (including develop tip 5ca92a7cd). The develop workflow copy contains the banner `# DRAFT ONLY - owner-scope workflow addition; not committed or run.` and differs from main; the coordinator reports main..develop diverged 13 ahead / 10 behind.

These witnesses falsify the prior path-only explanation for the absent runs and show that merely noting #179 draft status is incomplete. They do not yet establish which binding/definition mechanism caused zero PR jobs or the minimum corrective action. w274 has been commissioned to identify that mechanism and the smallest action that makes a check appear on these exact heads. Final route verdict is therefore held pending that akte; this lane makes no `.github/**` edit and triggers no Demo event. Once w274's Plan PR is available, review its evidence and choose among an Owner main-side workflow change, develop-side normalization, or a fresh PR event plus `ready_for_review`, then record the exact file:line prescription and #170-first qualification sequence here.

Recovery publication state: Plan PR #75 is open as draft at candidate `adc78b1fe785bb8c6bb2e3ad16dd0e5b356ac5d0`; Hosted Plan validation run 45739887273 (`pull_request`) was in progress when captured. This candidate is subject to a follow-up evidence commit for the owner witnesses and must receive Hosted validation on its final exact head before merge.

## Additional bounded reviews

### #1650 exact-head pair update

Run `45737093207` is now terminal SUCCESS on exact head `37c4d847ca377d1555163ac4791c8ba08b85de77`, event `pull_request`, attempt 1. Its four selected runtime jobs all completed SUCCESS: Docker data-capabilities, Docker observability, Podman data-capabilities, and Podman observability. Together with distinct run `45734193200` (same exact head, same event, attempt 1, terminal SUCCESS with the same four executed jobs), the required two-distinct-run condition is satisfied. This establishes only the CI pair, not content/identity admission. Verdict remains content HOLD; commits `ed2fb751` and `f89f506f` have genuinely foreign author `w181-0428-doclink-sweep` for card owner `w165-0428-078-pr1650-basehop`. A Coordinator-led forward reissue is required for that provenance, and the card's 0428-181 delivery-consumer hold remains unmet. The lane does not merge product PRs or trigger runs; w267 owns the bounded review/merge route.

### #1842 relocation and selector failure classification

Reviewed run `45739171543`, event `pull_request`, attempt 1, exact head `4f570ff966cd5e8d3043e8bd6363e1ea4e87d0d6`; it is terminal FAILURE, so #1842 must not merge on this head. The Owner ruling is relocation of the v0.4.27 registration/pin selection to v0.4.28 without removing criteria; fail-closed unknown/non-cataloged behavior, broad checks, and runtime coverage stay intact.

The legacy active-release fixtures are relocation fixtures, not selector-contract regressions: `scripts/test_ci_v0427_gate_catalog.py:39` asserts that the active candidate release remains v0.4.27 while the candidate requirements now identify v0.4.28; move that registration assertion/test to v0.4.28. `scripts/test_pr_ci_fallback.py:176` tests a v0.4.27 demo-ref while its helper uses the active v0.4.28 mapping; relocate that active-release case to v0.4.28. If v0.4.27 compatibility is separately intended, set the fixture mapping to v0.4.27 explicitly rather than treating it as active. The planner-test output also includes the focused-Python copies of the same stale v0.4.27 demo-pin fixture.

The remaining planner failures are real coverage/selector-contract regressions, not release-name fixtures: assertions that broad Go checks and selected runtime gates remain covered fail in `scripts/test_pr_ci_fallback.py:95,145,156`; invalid, uncataloged, unknown-product/source and lone-deleted-source paths fail to reject in `scripts/test_pr_ci_fallback.py:124,195,210,287`; cataloged runtime and Podman routing assertions fail in `scripts/test_pr_gate_coverage.py:354,549,570,604,618,633,714`; runtime-hint, unknown-source, unreviewed-runtime-file, and uncataloged-source rejection assertions fail in `scripts/test_pr_gate_coverage.py:648,665,679,727`. These contradict the explicit no-criteria-removed and fail-closed/runtime-coverage rulings. `scripts/test_pr_gate_plan.py:3265` is the aggregate guardian failure (`0 != 11`) reflecting those nested coverage failures, not an additional independent defect. This lane makes no product edits and does not rerun CI.

Decision to w268: yes, relocate the active v0.4.27 registration and active demo-ref fixture to v0.4.28; preserve the historic v0.4.27 case only with an explicit v0.4.27 fixture mapping. Fix the genuine selector/fail-closed/runtime-coverage failures listed above before treating run 45739171543 as resolved. No Owner criteria are removed.

Owner ruling for #1842 (already-authorized relocation, not an open question): “Resolve the v0.4.27 release-registration test from the already-recorded Owner ruling: remove its active requirement placement from v0.4.27 and carry the same requirement under v0.4.28, preserving all criteria and fail-closed/fallback behavior.” Thus the v0.4.27 active-registration assertion at `scripts/test_ci_v0427_gate_catalog.py:39` is stale for this candidate; move the identical requirement placement and active assertion to v0.4.28. The active v0.4.27 pin fixture at `scripts/test_pr_ci_fallback.py:176` also needs to reflect the current active release, or explicitly define a historical v0.4.27 fixture. Preserve all failure behavior and selection criteria. Any genuinely separate scope remains a finding with exact file:line and does not hold this authorized relocation.

## Forward-only census expansion and current-head disposition

Census source: w271 Plan PR #76, head `97cf9672e...`, Plan validation run `45741218805` GREEN. Its table identifies 76 paths beyond the 12 artifacts in this PR. Disposition: create one second scoped Plan PR after #75 is merged and fetch the then-current `origin/main`; do not overload this already-reviewed 12-artifact recovery PR with a separate 76-path census scope.

Of the 76 census paths, restore 68 unique artifacts forward-only, each from its original carrier ref or a freshly verified, non-consuming stash locator. Classify two as content duplicates and do not publish another copy: (1) `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` has the same blob `9781ec653c...` as the canonical `evidence/w246-1812diag/w246-1812gatefaildiag.md` restored in this PR; (2) `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` is superseded by the current accepted 0428-268 task `tasks/t-20261124-r28-alert-evaluator-live-health-wiring.md` (#1831). Do not restore six Hunt47 task files with IDs 0428-341 through 0428-346: those IDs are already occupied on current main by six different tasks, so they are conflicts requiring coordinator reissue under unique IDs, not content duplicates. Restore the four other Hunt47 task files 0428-347 through 0428-350, plus unique 0428-155, 0428-175, and the broad rcptlink task; the remaining unique evidence files are included in the 68.

Per-artifact proof in the follow-up akte: fetch and identify the exact source carrier (PR ref preferred; if a stash is the only carrier, record its content hash and verify the same stash entry remains present before and after without pop/drop); restore only the named path with `git checkout <carrier> -- <path>`; record source blob SHA and restored blob SHA from `git rev-parse`; require `git diff --quiet <carrier> HEAD -- <path>` to exit 0. Include a row for every restored artifact. No force push, history rewrite, direct-main write, stash consumption, or reconstruction from memory.

The six card-ID conflicts are specifically `tasks/t-20261124-hunt47-provider-registry-migration.md` (0428-341), `tasks/t-20261124-hunt47-deployment-v1-record-wall.md` (0428-342), `tasks/t-20261124-hunt47-destroy-warning-kind.md` (0428-343), `tasks/t-20261124-hunt47-gate-recover-preflight-flag-route.md` (0428-344), `tasks/t-20261124-hunt47-version-gate-error-surface.md` (0428-345), and `tasks/t-20261124-hunt47-keycloak-migration-docs.md` (0428-346). Their current main occupants have distinct subjects; the exact files and conflicting card IDs are recorded here for coordinator reissue. No unique census artifact is presently identified as unrecoverable.

## w274 route finding correction

The w274 akte is present in current main at `dd851feb4`, but its publication was a one-parent direct-main commit by `coordinator` with no associated Plan PR; preserve it in history and do not count its channel as compliant lane evidence. The diagnosis that `branches: [develop]` excluded #170/#179 is factually wrong: both Demo PRs target `develop` (GitHub PR API `baseRefName=develop`). Current copies on Demo main and develop both select `branches: [develop]`. Historical absence of PR runs is explained by the workflow not yet existing on Demo default main at the original events; PR #180 later brought it to main at `2618b3962330509add5bf265522995da2a9034ce`.

Current route prescription, based on the coordinator's recorded run/path witnesses: do not change the base-branch filter. The default-branch main copy covers #170 and #179 paths, but no PR runs/check-runs appeared; develop's copy covers #170 but misses the four #179 files, and both copies lack explicit `ready_for_review` activity. Owner-scope workflow normalization is needed: make main/develop copies agree on `types: [opened, synchronize, reopened, ready_for_review]`, and add `tests/connectivity/run.sh`, `tests/full-destroy/run.sh`, `tests/policy/operator-test-certificate.sh`, and `tests/reconciliation/run.sh` to the develop copy. Then trigger #170 first on its exact head via Owner-authorized PR event; for #179, Owner moves it out of draft after the change. Each requires two distinct `pull_request` SUCCESS run IDs on the same exact head, each with executed check jobs; use Owner-authorized close+reopen for the second run. Prior push runs with `jobs=[]` are not qualification. No workflow file was edited and no product event was triggered here.

## Updated #1842 selector ruling

Releases v0.4.24, v0.4.25, and v0.4.26 have no `.demo-ref`; these are valid no-pin releases. Never fabricate pins for them. Releases that do have a `.demo-ref` resolve against their own release tag. The active registration/pin requirement relocates from v0.4.27 to v0.4.28 with identical criteria under the Owner ruling; fail-closed unknown/non-cataloged behavior, conservative fallback, broad checks, and runtime coverage remain unchanged. The live v0.4.28 `.demo-ref` value `b41127723e523134a1c14ee3c36cf133237162ce` is stale; replace it within #1842 with the immutable validation target `5ca92a7cd2f746934890cfd7096a48068bdf218e`. The v0.4.24–26 parameter fixtures that demand a pin are fixture defects, not selector regressions; the genuine fail-closed/runtime failures and stale active v0.4.27 fixtures are classified in the preceding #1842 section.

## Latest base integration and publication state

The verified real remote is `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. Latest fetched live main before this addendum was `4d7ef2aa50c36a41ef274dd1e30d421aee1d1d6a`; the branch integrates it with ordinary merge commit `20a38727bf210fac447b9c3f19e55e1651e159ea`. PR #75 still points at the earlier published head; the local candidate above is not yet pushed or Hosted-validated. Final status and run IDs will be appended after publication.

PR provenance check at latest integration: `git merge-base --is-ancestor origin/main HEAD` exited 0 for base `4d7ef2aa50c36a41ef274dd1e30d421aee1d1d6a` and candidate `20a38727bf210fac447b9c3f19e55e1651e159ea`. `git diff origin/main...HEAD --name-only` output at this checkpoint:

```text
evidence/2026-11-26/w249-0428-284-gateids/akte.md
evidence/2026-11-28/w247-0428-285-1820hop.md
evidence/coordination/w260-plan-recovery-w255-0428-251-demo170codex.md
evidence/e6ca7696-b1f8-492d-b226-876b16925fc5/w245-0428-284-1842alt/akte.md
evidence/r28-welle6-2026-11-26/1851-carrier/disposition.md
evidence/r28-welle6-2026-11-26/w252-1833-1835-disposition/disposition.md
evidence/r29-welle6-2026-11-26/0428-284-1842alt/routing-alternatives.md
evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md
evidence/r29-welle6-2026-11-28/0428-284/w136-demo-prgate-availability.md
evidence/verify/w253-demo170179-census.md
evidence/w246-1812diag/w246-1812gatefaildiag.md
evidence/w248-0428-284-boardscan/akte.md
evidence/w255-0428-251-demo170codex/decision.md
tasks/t-20261124-gate-catalog-baseline-1819.md
```

## Identity-block disposition and refreshed PR provenance

Before discarding local-only merge `97283409e25e65ad2b2567bec6685164361c86c6`, I verified the published PR #75 still pointed at `f6b7b608b1a1110d805418f9ae26b8af66a6d704`, `git ls-remote origin` advertised no ref at the offending SHA, and GitHub's commit API returned `No commit found for SHA: 97283409e25e65ad2b2567bec6685164361c86c6` (HTTP 422). It had never been pushed. I discarded that local-only commit and recreated the base absorption with `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local merge --no-edit origin/main`.

The replacement merge is `ab57e84d1`; `git show -s --format='%an %cn %s' HEAD` prints `w255-0428-251-demo170codex w255-0428-251-demo170codex Merge remote-tracking branch 'origin/main' into w255-w260-plan-recovery`. At this refreshed checkpoint, base `origin/main` is `3a9bfea66796e2c36795b9c3794cc24654743030` and `git merge-base --is-ancestor origin/main HEAD` exits 0. `git diff origin/main...HEAD --name-only` output remains the same 14 paths listed in the previous provenance section. `git log --oneline origin/main..HEAD` contains only this lane's candidate commits; author and committer verification for every listed commit returns `w255-0428-251-demo170codex <w255-0428-251-demo170codex@baseharbor.local>`. No PR push occurred while the invalid-identity merge was present.

The PR scope restores 12 of the 88 paths counted by w271's census (PR #76 head `97cf9672e...`, Hosted Plan validation run `45741218805` GREEN). This PR records the forward-only disposition for the remaining paths; their 68 unique restorations, two duplicate exclusions, and six card-ID conflict reissues belong to one follow-up PR after this recovery PR is merged.


## PLAN — provenance exception and identity follow-up

1. Check the live Plan ignore rule, tracked worker-root contents, and validator checkbox exceptions.
2. Record the owner's disposition for the two parked paths without changing validator behavior.
3. Record the narrowly scoped 0428-253 same-lane identity admission in the existing task note and quote the implemented start-message rule.
4. Publish the two-file Plan change through an owned branch and PR; require Hosted `Plan · validate` on its exact final head.

## Closing disposition — ignored lane-local worker scratch paths

Owner disposition (choice **i**): these two paths stay permanently excluded from Plan `main` as lane-local scratch, exactly as parked by w255:

- `workers/w186/0428-186-hop.md`
- `workers/w266-0428-285-1820pre/PLAN.md`

They are not restored byte-for-byte and are not relocated to `evidence/`. The live Plan `.gitignore:33` ignores `/workers`; the only existing tracked entry under that root is the specific forced-added `workers/0427-compose-native-acceptance/todos.json`, not a general scratch exception. The Owner-confirmed TOP_CHECKBOX lines in the two parked Markdown files would fail `scripts/plan.py`'s `check_stray_checkboxes` at lines 563–570: only `tasks/`, `roadmap/cards.md`, and `templates/` are exempt. Moving the same bytes under `evidence/` would still fail. No validator allowlist, Plan tooling change, or `.github/**` edit is authorized or needed. These two paths remain parked; w255 continues the other 65 scoped restores.

This is a provenance exception only: it does not remove or weaken the CardBoard checkbox guard and does not classify either scratch file as lost recoverable evidence.

## Commit identity rule recorded for the 0428-253 ruling

The implemented start-message paragraph is `coordinator/scripts/dispatch-lane.sh:44`:

```text
COMMIT IDENTITY (Owner ruling 2026-11-26, generalises the w205/w254 findings): EVERY commit you create, AND EVERY merge commit you create (e.g. absorbing develop), must carry YOUR OWN lane's FULL canonical name in both author and committer, set per-command: git -c user.name=<your-lane-name> -c user.email=<your-lane-name>@baseharbor.local commit/merge ... . Use the complete name wNNN-<card>-<title> exactly as your session is registered: shortened forms (bare 'w205') are AMBIGUOUS and rejected, foreign lane names and the card owner's name are IMPERSONATION, and 'coordinator' is never a commit author (I write no code and you must not launder my name into yours). Before every push print git log --format='%h an=%an cn=%cn' -1 and put that line in your evidence; a mismatched identity blocks acceptance even when CI is green. The only admitted exception is historical: the first two w205 commits count as the same-lane shortened identity w205 = w205-0428-253 (owner ruling, no rewrite, scoped to those two commits and recorded on card 0428-253).
```

The 0428-253 task note names the two first chronological historical commits and admits only their shortened same-lane author formatting. No commit is rewritten; new commits use the full canonical lane identity, and foreign-lane rejection is unchanged.
