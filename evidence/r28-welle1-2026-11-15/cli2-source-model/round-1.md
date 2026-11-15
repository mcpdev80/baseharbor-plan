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
- cmd/baha/workspace_mutation.go: `map` on a local source fails closed with a pointer to the portable path surface.
- cmd/baha/app_workspace_wizard.go: guided "Local directory" source choice.
- cmd/baha/machine_coverage.go + regenerated docs/reference/cli-machine-coverage.md, docs/cli/command-index.md, docs/de/cli/command-index.md (generator-owned; BASEHARBOR_UPDATE_MACHINE_DOCS=1, the mechanism the repo's own CI documentation prescribes).
- cmd/baha/mcp_workspace_mutation.go: jsonschema descriptions updated for the extended model (same field shapes; no registry change).
- Tests: internal/development/source_model_test.go (6 new), cmd/baha/app_workspace_source_model_test.go (8 new).

## Test IDs (declared before implementation per contract)
- Package internal/development: TestSourceModelAllowsOptionalUniqueComponents, TestSourceModelLocalDirectorySource, TestResolveWorkspaceLocalDirectoryWithSubPaths, TestRemoveSourceRejectsLastSourceAndReportsReferences, TestSourceAndComponentUpsertReplaceWithoutDuplicates, TestSaveRemovableSourceDetachesMappingOnly (source_model_test.go).
- Package cmd/baha: TestWorkspaceInitAcceptsLocalDirectorySource, TestWorkspaceInitRejectsArtificialComponents, TestWorkspaceSourceAddAndRemoveDetachSafely, TestWorkspaceComponentAddListRemove, TestWorkspacePathSetsAndShowsSourcePaths, TestWorkspacePathRejectsForeignCheckoutOwnership, TestWorkspaceSourceModelMachineParity, TestWorkspaceGitStatusIncludesLocalGitSources (app_workspace_source_model_test.go).
- Fixtures: t.TempDir manifests + XDG_CONFIG_HOME isolation only; native Git where a checkout is required; no Docker/Podman/TLS/native runtime needed for this slice (domain metadata + CLI only), so unit coverage is the correct durable evidence.

## RESULT
- Focused local runs (TMPDIR off the quota-carrying /tmp):
  - `go test ./internal/development/ ./cmd/baha/ -run 'TestWorkspace|TestSource|TestResolve|TestRemoveSource' -count=1` → both `ok`.
  - `go build ./...`, `go vet ./cmd/baha ./internal/development`, `gofmt -l` clean; `scripts/source-readability-audit.sh` PASS; `scripts/documentation-audit.sh` result recorded below.
- Exact candidate SHA + full-suite and CI results: appended in this file after push (Eigenes-Run-Pflicht, terminal observation).

## Environment caveat (documented, not a candidate defect)
- This host's /tmp is tmpfs with usrquota and ~2.6G free; the pre-existing heavy tests TestStagePinnedGitTreeExportsCommitNotDirtyWorktree / TestPrepareStagedCoreGitCandidatePinsCanonicalApplication (64 MiB writes + native `git archive`) fail here with "disk quota exceeded"/"signal: killed" both WITH and WITHOUT my changes (baseline stash-run reproduced identically). Full-package runs therefore used TMPDIR=/home/marcel/dev/baseharbor-ecosystem/workers/tmp-w059. GitHub CI (ubuntu runners, no such quota) executes the same tests.
- One Go-toolchain quirk found while diagnosing: `exec.Cmd.Wait` after a StdoutPipe EOF can hang past the test timeout when the 60 s command-context cancel raced (goroutine dump in the log; also observed in a standalone reproducer, git 2.53.0). Pre-existing product code path, untouched by this slice; recorded as an observation, no scope taken.

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
```
(result appended after commit)

## Cleanliness
- No containers/compose/networks/volumes started by this lane (domain/CLI unit work only); `docker ps` untouched. Scratch: /tmp/opencode/w059cli-wt (worktree), /tmp/opencode/w059-*.log, /home/marcel/dev/baseharbor-ecosystem/workers/tmp-w059 (test TMPDIR).

## Handoff
- Branch: lane-0428-059-cli2-source-model (from 3a91e2a8). PR: draft, base lane-0428-uid-target (retarget stack per mission; NOT a develop PR).
- Dependencies: uid-app #1579 lands before this stack retargets to develop (coordinator sequencing); nothing in this slice assumes app.id presence.
- Shared-file conflicts: none observed; machine_coverage.go/doc regeneration belongs to whoever integrates the stack — re-run the generator on integration.
- Remaining gaps: none known for the slice acceptance list.
