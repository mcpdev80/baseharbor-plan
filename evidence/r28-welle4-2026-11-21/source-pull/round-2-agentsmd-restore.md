# Round 2: restore AGENTS.md + document machine_coverage requirement (card 0428-061, lane w27-pr1627-0428-061-pull)

Lane: `lane-0428-061-sourcepull` (worktree `workers/0428-061-sourcepull-wt`)
Candidate head after this round: `d9124a91` (merge of new develop)
Owner request: sha256 `a933dc9bb0bf` (w27redo) + follow-up sha256 `bd359b318fe0` (w27stop)

## END lane

END w27-pr1627-0428-061-pull: BLOCKED on Owner/CI-owner write-set (machine_coverage.go + generated docs); AGENTS.md restored, candidate d9124a91 on new develop 42da7128, PR #1752 still draft, handed to coordinator. No write occurred in Owner/CI-owner scope this round.

## PLAN

- Reality check: remote develop HEAD, PR #1752 head, origin URL, my commit intact.
- Measure the AGENTS.md defect against develop and merge-base d1acf3f3.
- Restore AGENTS.md from origin/develop, own commit, author == committer.
- Hop to current develop 42da7128 (was 513488ee, moved) via fetch + merge --no-ff.
- Build + targeted local test; confirm the "unclassified command: baha app pull" gate.
- Locate the classification site (classifyCommandCoverage + operation registry) and confirm Owner/CI-owner write-set.
- Locate the generated docs and confirm both regenerate the row once classified.
- Document exact requirement with file:line + pattern for the coordinator.
- Post QUESTION to coordinator to hand off the write to the integration/CI owner.

## Findings against my own candidate

The defect the owner reported is confirmed: my candidate `#1752` deletes the rule-document `AGENTS.md`.

numstat, `git diff --numstat develop..refs/pull/1752/head -- AGENTS.md` (owner-measured phrasing):

- `0  125  AGENTS.md`  (0 insertions, 125 deletions)

Same number measured two ways in my worktree:

- `git diff --numstat origin/develop..HEAD -- AGENTS.md` -> `0  125` (origin/develop is ahead of the old head, so the delta only shows the deletion side)
- `git diff --numstat d1acf3f3..HEAD -- AGENTS.md` -> `0  125` (vs the exact merge-base the owner named)

Content witness:

- `git show HEAD:AGENTS.md` -> `1` line (deleted; only a stale warning line remains)
- `git show origin/develop:AGENTS.md` -> `126` lines
- `git show d1acf3f3:AGENTS.md` -> `125` lines

The deletion is real and is exactly the owner-reported class of defect. Restored in this round (see below), not reproduced.

## Restore of AGENTS.md

Restore command: `git checkout origin/develop -- AGENTS.md` (file now byte-identical to develop).

Identity: `author=0428-061-sourcepull <0428-061@baseharbor.local>` == `committer=0428-061-sourcepull <0428-061@baseharbor.local>` (commit `16c120f1`, reason text: "the earlier candidate #1752 deleted AGENTS.md (0 insertions, 125 deletions vs both origin/develop and merge-base d1acf3f3). Restore the rule-document from origin/develop verbatim; no content change to the source-pull feature.")

Byte-identical check: `git diff --cached origin/develop -- AGENTS.md` -> empty (staged file equals develop exactly).

## Hop to current develop (was 513488ee, moved to 42da7128)

Remote develop HEAD now (git ls-remote origin refs/heads/develop):

- `42da7128e724a533349e93d3742cbd232ea48936  refs/heads/develop`

Steps executed (no rebase, no amend, no filter-branch):

1. `git fetch origin refs/heads/lane-0428-061-sourcepull` -> `FETCH_HEAD = 4bae3194fa71327cdf2a67e64c9a11c91d0f5972` (my original commit), `git merge-base --is-ancestor 4bae3194... FETCH_HEAD` -> YES.
2. `git merge --no-ff origin/develop` -> `d9124a91` (ort strategy; 9 files, +1299/-23, all from develop: app_status_result, orgconfig, perses).
3. `git merge-base --is-ancestor 4bae3194... HEAD` -> YES (original feature commit still an ancestor).
4. `git merge-base --is-ancestor origin/develop HEAD` -> YES (clean single-candidate chain on new develop).

`git log --oneline origin/develop..HEAD` (my own commits + the merge only):

- `d9124a91` Merge remote-tracking branch 'origin/develop' into lane-0428-061-sourcepull
- `16c120f1` restore: bring back AGENTS.md deleted from candidate (reg rule doc)
- `4bae3194` 0428-061 implement guided source pull (baha app pull)

## Local build + targeted test (host constraint: tmpfs full)

Build passed after redirecting Go build temp/cache to the home filesystem (`/tmp` tmpfs = 2.6G free; the coordinator log `/tmp/coord-175-wt/logs/tmp-sweep.log` is 2.6G and is not mine to trim). Env used: `TMPDIR=/home/marcel/.gobuild/tmp GOCACHE=/home/marcel/.gocache go build ./cmd/baha/` -> clean.

Targeted gate (named form per the test-runner rule, bare package test never run on the coordinator host):

- `go test ./cmd/baha/ -count=1 -run TestMachineCoverageCIRealTreeAndJSONClassification -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`
- Result: `FAIL` -> `registration_ci_readiness_test.go:82: unclassified command: baha app pull`

This is the exact CI gate class the owner named (hosted run 44955232402, required job `PR Draft Go cli-0`, same test, same line). The host disk limit is a real local boundary; it does not replace the CI gate and does not cause this failure. The failure is the missing machine-coverage classification, which lives in an Owner/CI-owner write-set this round.

## The missing classification: exact requirement for the integration/CI owner

The failing test (`registration_ci_readiness_test.go:82`) requires every command in `currentCommandCoverage()` to carry a non-`gap` classification, and every `semantic` row must have a valid `Operation` with a matching `MCPTool`.

Where classification happens:

- `cmd/baha/machine_coverage.go:58` `classifyCommandCoverage(path, command)`: for a command with `command.Run != nil`, it looks up `cliMachineOperations[path]` (map at line 95) and, if `machine.OperationByID(operationID)` exists, emits a `semantic` row with `Operation`, `MCPTool`, `Reason` from `cliSemanticModes[path]`, and `JSONSurface`.
- `internal/machine/contract.go:166` `Operations()` is the registry the test checks against. No `pull` / `source.pull` operation currently exists.

The command itself:

- `baha app pull` is a real mutating command (`cmd/baha/app_pull.go:29-41`, has `command.Run`, pulls Git source as a strict fast-forward and, with `--up`, invokes the same `app-up` lifecycle as `baha app update`). It is NOT a group, NOT excluded, NOT in `cliMachineOperations`.

Exact change needed (Owner/CI-owner write-set, not mine this round):

1. In `cmd/baha/machine_coverage.go`, add `"baha app pull": "<operation-id>"` to the `cliMachineOperations` map (line 95), mirroring the `baha env destroy` / other CLI2 pattern.
2. Add a matching `Operation{ID, MCPTool, ...}` entry to the registry in `internal/machine/contract.go:166` `Operations()`, with a `MCPTool` value that the registry exposes.
3. Add a human reason to `cliSemanticModes` for the new path so the `Reason` column is populated.
4. Regenerate both contract pages (they must match `currentCommandCoverage()` exactly or the documentation test fails):
   - `docs/reference/cli-machine-coverage.md`
   - `docs/de/reference/cli-machine-coverage.md`
   via the existing generator, e.g. `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run TestMachineDocumentationTracksRegistryAndCommandTree`. Both are generated from the same source; the `baha app pull` row would then appear as `semantic` with the new operation id and an English reason. Do not hand-edit either page.

Note: `internal/machine/contract.go` is the operation registry. Its `MCPTool` field drives `baseharbor.<id>` tool names in `docs/reference/mcp.md` (also generated). The new `pull` operation needs a concrete `MCPTool` value consistent with the naming convention (`baseharbor.<operation-id>`). The coordinator/CI-owner should confirm the intended operation id + MCP tool before writing.

## Write-set verification (this round)

`git diff --name-only origin/develop..HEAD` -> only my two commits touch product files; the restore re-adds `AGENTS.md`. No change under `.github/**`, no change to `machine_coverage.go`, `contract.go`, `commands.go`, or the generated docs by this lane this round.

## Ancestry / single-candidate witnesses

- `git ls-remote origin refs/pull/1752/head` (before hop): `4bae3194fa71327cdf2a67e64c9a11c91d0f5972`
- `git ls-remote origin refs/heads/develop` (current): `42da7128e724a533349e93d3742cbd232ea48936`
- `git merge-base --is-ancestor origin/develop HEAD` -> YES
- `git merge-base --is-ancestor 4bae3194... HEAD` -> YES
- `git log --oneline origin/develop..HEAD` -> only my 2 commits + the merge (no foreign candidate carried).
- git identity: `0428-061-sourcepull <0428-061@baseharbor.local>` (author == committer on `16c120f1`).

## repo-rule compliance

- No `.github/**` touched. No runner infrastructure touched. No subagents. No build/repair of runners.
- No hand-edit of generated docs (left for the registry generator).
- Operational text (lane identity, base-refresh notes) kept out of the product repo; only a restore of an existing file with a factual commit message.
- PR #1752 left DRAFT. No merge, no close.

## cleanliness

- No docker/podman compose projects started this round. `docker ps -a` not applicable (no containers). tmpfs `/tmp` full by the coordinator log, not by my work.

## Handoff to coordinator (post)

QUESTION w27-pr1627-0428-061-pull: AGENTS.md restored (commit 16c120f1) and candidate hopped onto new develop 42da7128 (d9124a91, my feature commit 4bae3194 still an ancestor, single-candidate chain). The CI gate still fails locally with the expected `unclassified command: baha app pull` (registration_ci_readiness_test.go:82). The fix lives in an Owner/CI-owner write-set this round:

- classify `baha app pull` in `cmd/baha/machine_coverage.go:58` via `cliMachineOperations` (line 95) with a new semantic operation registered in `internal/machine/contract.go:166` `Operations()` + a `cliSemanticModes` reason, then regenerate `docs/reference/cli-machine-coverage.md` and `docs/de/reference/cli-machine-coverage.md` with `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run TestMachineDocumentationTracksRegistryAndCommandTree`.

Requesting the integration/CI-owner to write the classification into my branch (candidate d9124a91 / lane-0428-061-sourcepull), then re-run the exact CI job so the mutation proof is RED (44955232402) -> GREEN at the same test. PR #1752 stays draft until the exact-head CI is green. Lane withdrew from the classification write; the AGENTS.md deletion by the original candidate is documented above (numstat 0/125 vs both develop and merge-base d1acf3f3).
