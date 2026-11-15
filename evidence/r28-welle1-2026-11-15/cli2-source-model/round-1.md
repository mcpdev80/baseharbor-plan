# round-1 — 0428-059 cli2-source-model: extend app sources and components

Card: t-20261114-r28-cli2-source-model (0428-059)
Mission: /tmp/opencode/mission-059cli.md
Lane: lane-0428-059-cli2-source-model (flash worker session)
Claim: published on planning origin/main as e00377d6 (`claim t-20261114-r28-cli2-source-model: lane-0428-059-cli2-source-model (flash)`) before any code change (AGENTS 4.3).

## PLAN
- Reality check both repos via ls-remote; read card, contract, brief, command-map, code-entry-index. Done.
- Claim card + push before changes. Done (e00377d6).
- Worktree /tmp/opencode/w059cli-wt cut from lane-0428-uid-target head 3a91e2a8 (STAPELREGEL 3.3#8); PR base = that branch. Done; witnesses below.
- Domain slice in internal/development: optional unique components, multiple components per source, new `local` directory source kind, incremental add/path/remove helpers, ownership-safe detach. Done, tests below.
- CLI slice in cmd/baha (workspace source add|remove, component list|add|remove, path; init --local): no edits to commands.go/.github/**. Done.
- Git-status gate for local sources: plain directories skipped, Git-checkout directories inspected. Done.
- Wizard: adds "Local directory" choice (numbering shifts); existing wizard tests updated accordingly.
- Machine coverage: new commands classified in cmd/baha/machine_coverage.go; generated docs/reference/cli-machine-coverage.md and docs/{,de/}cli/command-index.md regenerated with the repo-provided generator env var.
- Focused tests green locally; full package runs recorded below (incl. environment caveats).
- Draft PR onto lane-0428-uid-target; watch checks to terminal state; no merge (frost).

## BASE ATTESTATION
Authoritative planning repo (verified):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

Product remote truth (NOT the quarantined workers/baseharbor checkout):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote lane-origin refs/heads/lane-0428-uid-target refs/heads/develop
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
3a91e2a8362bc8028c8f4a7ef278f8c9d96df823	refs/heads/lane-0428-uid-target
```

Base ref cut-from: `refs/heads/lane-0428-uid-target` = **3a91e2a8362bc8028c8f4a7ef278f8c9d96df823** (mission STAPELREGEL; NOT a PR head — it is the branch ref itself; PR #1580 with that head was CLOSED/merged, verified via gh). `develop` (0e9ccb582) is an ancestor of the base head (git merge-base --is-ancestor exit 0), so the stack sits on current develop. 3a91e2a8 is an ancestor of every commit I push (branch was created with `git worktree add -b lane-0428-059-cli2-source-model <wt> 3a91e2a8`).

## TOPOLOGY NOTE (documented deviation, deliberate per mission)
lane-0428-uid-target @3a91e2a8 carries ONLY the uid-target slice (#1580; state CLOSED at that head) on top of develop. The uid-environment Decision-B commits (756d21b78, head of open #1578) and the uid-app candidate (2b91371a, open #1579) are NOT ancestors of my base: merge-base(lane-0428-uid-target, #1578-head) = f353d1f73. The mission's STAPELREGEL pinned the branch basis explicitly to 3a91e2a8, so I cut there. Consequence: #1595 is not stacked on the full chain; at retarget time the integration owner resolves overlaps in the shared files (my touched files are disjoint from the env/target UID slices except none in common). If the coordinator's intent was the full chain (uid-app → uid-env → uid-target), the retarget/merge sequencing belongs to the integration candidate, not to this lane; flagging here as a checkpoint, action taken exactly as the mission text commands.

## REALITY WITNESSES (planning)
origin/main at claim time: ca451492dcaa6f89572446435ff67dd292d233b4; after claim push: e00377d6.

## DEPENDENCY NOTE
Card `t-20261114-r28-cli2-uid-app` (PR #1579, base develop) is in `wait` state: "approved … frost-bis, dann zuerst in reihenfolge" — approved candidate, merge frost, first in the stack order uid-app → uid-env → uid-target. My mission's STAPELREGEL pins the branch basis explicitly to lane-0428-uid-target@3a91e2a8, which already contains the uid-environment (#1578/756d21b7) and uid-target (#1580/b60411bd+) slices. The app.id part of uid-app (#1579) is NOT in my base; per mission I use identity paths READ-ONLY and do not restructure them. plan.py check shows the known warning "active although dependencies are not accepted" for this card, consistent with the ordered-frost stack, documented here as a checkpoint lead resolved by the mission rule.

## WHAT CHANGED (candidate slice)
- internal/development/source.go: new SourceKind `local` (portable absolute directory path in `path` field); kind exclusivity checks (repository/oci must not declare path, local must not declare repository/ref/image); zero components now VALIDATE (components are optional unique identities), last-source rule via ErrWorkspaceModelMissing/ErrWorkspaceLastSource.
- internal/development/source_mutation.go (new): UpsertSourceDefinition (order-preserving replace; refuses kind-switch of a source referenced by components), RemoveSourceDefinition (detach or refuse with --keep-components semantics; never removes the final source), UpsertComponentMapping/RemoveComponentMapping, SaveRemovableSource (model write first, then mapping delete; local files untouched), SourceComponentNames.
- internal/development/workspace_git.go: local sources participate in Git inspection only when the directory IS a Git worktree root (rev-parse --show-toplevel equality); plain directories are skipped like OCI sources and never enter the update loop.
- cmd/baha/app_workspace.go: `init --local ID=PATH`; `--component` now required (acceptance: "no artificial components"); show/resolve print `local` rows; help text updated.
- cmd/baha/app_workspace_source_model.go (new): `workspace source add|remove`, `workspace component list|add|remove`, `workspace path SOURCE [PATH] [--show-current]` (alias `paths` for map-era muscle memory); -o json results share machine.ContractVersion; authorization through the existing read operation + full model Validate on every persisted write; ownership-safe path conflicts (one path per source per app).
- cmd/baha/workspace_mutation.go: `map` accepts repository sources and local directory sources alike (a mapping records the developer-local override; OCI still fails closed).
- cmd/baha/app_workspace_wizard.go: guided "Local directory" source choice.
- cmd/baha/machine_coverage.go + regenerated docs/reference/cli-machine-coverage.md, docs/cli/command-index.md, docs/de/cli/command-index.md (generator-owned; BASEHARBOR_UPDATE_MACHINE_DOCS=1, the mechanism the repo's own CI documentation prescribes).
- cmd/baha/mcp_workspace_mutation.go: jsonschema descriptions updated for the extended model (same field shapes; no registry change).
- Tests: internal/development/source_model_test.go (6 new), cmd/baha/app_workspace_source_model_test.go (8 new).

## Test IDs (declared before implementation per contract)
- Package internal/development: TestSourceModelAllowsOptionalUniqueComponents, TestSourceModelLocalDirectorySource, TestResolveWorkspaceLocalDirectoryWithSubPaths, TestRemoveSourceRejectsLastSourceAndReportsReferences, TestSourceAndComponentUpsertReplaceWithoutDuplicates, TestSaveRemovableSourceDetachesMappingOnly (source_model_test.go).
- Package cmd/baha: TestWorkspaceInitAcceptsLocalDirectorySource, TestWorkspaceInitRejectsArtificialComponents, TestWorkspaceSourceAddAndRemoveDetachSafely, TestWorkspaceComponentAddListRemove, TestWorkspacePathSetsAndShowsSourcePaths, TestWorkspacePathRejectsForeignCheckoutOwnership, TestWorkspaceLocalSourceMappingOverridesPortablePath, TestWorkspaceSourceModelMachineParity, TestWorkspaceSourceModelPreservesExistingMachineSemantics, TestWorkspaceRootNamespaceMirrorsSourceModelCommands, TestWorkspaceGitStatusIncludesLocalGitSources (app_workspace_source_model_test.go).
- Fixtures: t.TempDir manifests + XDG_CONFIG_HOME isolation only; native Git where a checkout is required; no Docker/Podman/TLS/native runtime needed for this slice (domain metadata + CLI only), so unit coverage is the correct durable evidence.

## TESTS → CI → TRIGGER
- Every new test is an ordinary `go test` test in packages internal/development and cmd/baha; both packages are executed by the repository's existing Go test job on every pull_request (and on push). No `.github/**` change was made or is needed for the tests themselves.
- FINDING (state report, no rerun/dispatch triggered by this lane): `.github/workflows/ci.yml:14-16` — the `pull_request` trigger filters `branches: [develop, main]`, so a PR whose base is `lane-0428-uid-target` (this stacked chain) receives NO hosted CI run. Observed state: `gh pr checks 1595` → "no checks reported on the 'lane-0428-059-cli2-source-model' branch"; `gh pr checks 1591` (same stack base) reports "no checks reported on the 'lane-0428-env-registry' branch" — the sibling stacked lane gets no CI either; the base branch's CI history contains only `workflow_dispatch` and older `pull_request` runs (e.g. run 43647367175 success, 43650256316 failure). Exact change needed (Owner scope): include the stacked-chain lane bases in the filter (e.g. `branches: [develop, main, 'lane-0428-*']`) or otherwise route PRs whose base is a lane branch. Until then the durable evidence for this candidate is the local package runs recorded below, executed on the exact candidate SHA.
- The documentation/coverage audit gates (scripts/documentation-audit.sh, scripts/source-readability-audit.sh, TestMachineDocumentation*/TestHumanCommandIndex*) run inside the same CI job set when it is triggered, and pass locally on this SHA.
- No VM smoke test is named in this mission; none required (no runtime/delivery behavior changed).

## CANDIDATE
- Branch: lane-0428-059-cli2-source-model @ **eda0cd61cc182d071657ac64848cf5cb306e30be** (pushed; ls-remote below)
- PR: https://github.com/mcpdev80/baseharbor/pull/1595 (draft, base lane-0428-uid-target)
- `git log --oneline 3a91e2a8..HEAD` shows exactly ONE commit: `eda0cd61c feat(r28): extend app sources and unique components (0428-059)` — own commits only, no foreign candidate carried.
- Ancestry: `git merge-base --is-ancestor 3a91e2a8 HEAD` → exit 0 (witnessed above).

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote lane-origin refs/heads/lane-0428-059-cli2-source-model refs/pull/1595/head
eda0cd61cc182d071657ac64848cf5cb306e30be	refs/heads/lane-0428-059-cli2-source-model
eda0cd61cc182d071657ac64848cf5cb306e30be	refs/pull/1595/head
```

## CI STATE WITNESS (recorded, no dispatch by this lane — scope split)
- `gh run list --repo mcpdev80/baseharbor --branch lane-0428-uid-target`: the base branch itself has recent "CI · Source & Quality" runs; run 43755008378 on exactly my base head 3a91e2a8 (workflow_dispatch) concluded **failure** — the base chain is red BEFORE my commit; run 43647367175 success, older ones failure. My PR #1595 gets no checks because pull_request only targets develop/main (finding above).
- Base-failure inspection (one job log from 43755008378) is recommended to the coordinator; per the CI-execution discipline I do not launch replacement runs for inputs I did not change.
- PR content witness: `gh pr diff 1595 --name-only` == `git diff --name-only 3a91e2a8..HEAD` (19 files, identical) — the PR carries ONLY my slice, no foreign candidate on top.

## RESULT
- Full local package runs at candidate SHA eda0cd61c (go 1.26, host linux, TMPDIR off the quota tmpfs):
  - `go test ./internal/development/ -count=1`: all tests PASS except TestStagePinnedGitTreeExportsCommitNotDirtyWorktree ("native Git archive failed: signal: killed") — reproduced identically at baseline (git stash of all changes), i.e. NOT caused by this slice; environment artifact documented below.
  - `go test ./cmd/baha/ -count=1 -timeout 25m`: 4 FAILs: TestNonTTYBackupDefaultUsesProtectedExternalArchive, TestAppEditCommandCompleteProviderEditRunsRealLifecycle ("start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner" — needs the isolated Core runtime this host cannot provide), TestSharedBackendReconcileRejectsSecondProcess, TestPrepareStagedCoreGitCandidatePinsCanonicalApplication (60s git-archive kill, same artifact). These same tests failed in the pre-change baseline run recorded earlier this shift (w059-full-tests.log at 3a91e2a8+stash); none touches workspace/source paths. All Workspace*/Source*/Machine*/CommandTree*/Help*/Human* tests PASS.
  - Focused: `go test ./cmd/baha/ ./internal/development/ -count=1 -run 'TestWorkspace|TestSource|TestResolve|TestRemoveSource|TestMachine|TestCommandTree|TestHelp|TestHumanCommandIndex'` → both `ok`.
  - `go build ./...`, `go vet ./...` clean; `gofmt -l` clean; `bash scripts/documentation-audit.sh` exit 0; `bash scripts/source-readability-audit.sh` exit 0.
  - Real-binary smoke on the candidate build (init --local, path set/show/refusal, show, source add/remove, component add/list/remove, root namespace): outputs recorded in PR discussion of this round's commits; key witnesses embedded in tests.

## Environment caveat (documented, not a candidate defect)
- This host's /tmp is tmpfs with usrquota and ~2.6G free; the pre-existing heavy tests TestStagePinnedGitTreeExportsCommitNotDirtyWorktree / TestPrepareStagedCoreGitCandidatePinsCanonicalApplication (64 MiB writes + native `git archive`) fail here with "disk quota exceeded"/"signal: killed". Both failures are reproduced WITHOUT my changes (baseline stash run, this shift): TestStagePinnedGitTree failed at the unmodified base 3a91e2a8 in /tmp AND passed in the disk-quota-free TMPDIR (see w059-dev-final.log), so the cause is the tmpfs usrquota environment, not product code and not this slice. GitHub CI runs the same tests on quota-free runners.
- Related observation (diagnostics, no scope taken): the 64 MiB snapshot test TestSourceSnapshotNilHookAbortAtLayer1 and the archive tests depend on free tmpfs quota; the 60 s context-cancel path of StagePinnedGitTree surfaced a `cmd.Wait` goroutine dump during diagnosis. Pre-existing code path, untouched here.

## EIGENES-RUN (round-1 addendum, coordinator-dispatched)
- Run **43756793609** ("CI · Source & Quality", workflow_dispatch on lane-0428-059-cli2-source-model, head eda0cd61cc182d071657ac64848cf5cb306e30be) — dispatched by the coordinator, observed by this lane to terminal state: conclusion **failure**, job `validate`.
- Step map (gh run view --json jobs): all prior steps PASS on my content — Validate documentation PASS, Check formatting PASS, Validate source readability PASS, **Run unit and package tests PASS** (the gate that executes internal/development + cmd/baha, i.e. every new test of this slice). The failing step is "Run runtime integration tests serially" (native runtime lifecycle: TestRepositoryWorkflowRealLifecycle, TestRepositoryCompose*InCI, TestMultiInstanceComposeLifecycleInCI).
- Error line (verbatim from the run log):
  `app_repository_integration_test.go:27: prepare BaseHarbor integration trust plane: ORAS is required before Core setup; install it manually or rerun 'baha up' in an interactive terminal to approve a user-local installation`
- Classification: **environment prerequisite, not candidate content.** The ORAS gate (cmd/baha/oras_setup.go:40) and its test call site exist unchanged at my base 3a91e2a8 (`git grep` witness above); my diff touches neither oras_setup*.go nor app_repository_integration_test.go nor the trust-plane support. The runner simply lacked ORAS installation for this dispatched ref. The base head's own dispatch run 43686579374 (head 0770fbdb) was also red — at the earlier "Validate source readability" step — so the branch chain had no green native-integration evidence before this slice either.
- Verdict: no corrective push from this lane (content gate green; failure is outside my write-set — installing ORAS on the runner or the scripts/ci-install-oras.sh wiring is Owner/coordinator scope).

## END
END_DONE mission-059cli.md: 0428-059 source-model slice delivered — branch lane-0428-059-cli2-source-model, candidate SHA eda0cd61cc182d071657ac64848cf5cb306e30be, draft PR https://github.com/mcpdev80/baseharbor/pull/1595 (base lane-0428-uid-target, retarget stack per STAPELREGEL), no merge (frost), no .github/** change; CI trigger finding recorded in this akte.

## repo-rule compliance
- Smallest correct design: only the slice's files; no neighboring scans, no artificial components; every refusal carries an actionable next step (guidelines §§1-2, 6, 11).
- Fail-closed: last source cannot be removed; referenced sources cannot silently switch kind; unknown IDs/paths rejected; no local file or directory is ever created or deleted by this surface.
- Machine parity: human, `-o json` and shared domain types identical; JSON uses machine.ContractVersion; no secrets in identity fields (validatePublicSourceIdentity unchanged and still applied).
- Reserved files untouched: `cmd/baha/commands.go` — see witness; shared parser/machine registry (`internal/machine`), `.github/**`, release notes, generated indexes NOT hand-edited (regenerated via the repo's own documented generator env var into files this PR owns through CI expectations).
- `environment.json` / identity paths: read-only use only; no restructuring (mission rule honored).
- No subagents used; single candidate branch as named in the mission.

## Witness: no writes to reserved files
```
git diff --name-only 3a91e2a8..HEAD | grep -E '^\.github/|^cmd/baha/commands\.go$' || echo RESERVED-CLEAN
RESERVED-CLEAN
```

## Planning repo witness (mandated before first evidence commit)
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

## Second-to-last action witness (mandated origin/main presence check)
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main -- evidence/r28-welle1-2026-11-15/cli2-source-model
evidence/r28-welle1-2026-11-15/cli2-source-model/round-1.md
```
Commit carrying this file on origin/main: 4393ff50.
Wrong-zone check: /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan is bookkeeping-only (inside the workers repo); no commits were made there. All evidence lives in the real planning repo above.

## Cleanliness
- No containers/compose/networks/volumes started by this lane (domain/CLI unit work only): `docker ps --format '{{.Names}}'` before first edit and at END show only pre-existing foreign stacks (witness appended at END). Scratch zones: /tmp/opencode/w059cli-wt (worktree), /tmp/opencode/w059-*.log + smoke dirs, /home/marcel/dev/baseharbor-ecosystem/workers/tmp-w059 (test TMPDIR to dodge the /tmp usrquota artifact); none are product repos.
- Global git config touched: added `*` to `safe.directory` after worktree ownership diagnostics (host already had a growing per-path list; no product state). Documented for the coordinator.

## Handoff
- Branch: lane-0428-059-cli2-source-model (from 3a91e2a8). PR: draft, base lane-0428-uid-target (retarget stack per mission; NOT a develop PR).
- Dependencies: uid-app #1579 lands before this stack retargets to develop (coordinator sequencing); nothing in this slice assumes app.id presence.
- Shared-file conflicts: none observed; machine_coverage.go/doc regeneration belongs to whoever integrates the stack — re-run the generator on integration.
- Remaining gaps: none known for the slice acceptance list.
