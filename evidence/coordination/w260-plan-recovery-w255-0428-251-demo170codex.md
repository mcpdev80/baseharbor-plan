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
