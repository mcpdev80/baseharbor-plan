# PR #1752 independent exact-head review — a4adc29a5844

## PLAN

1. Refresh remote PR #1752 and develop refs; verify exact requested head, base, ancestry, diff paths and commits.
2. Inspect F1-F4 corrections and compile-fix/test semantics at the exact candidate without running tests locally.
3. Verify golden fixture and CI routing for the changed tests.
4. Observe exact hosted run 44971782040 until terminal; skipped/queued required checks are not a pass.
5. Publish exact-head verdict/evidence only after terminal CI. Do not modify product branch, merge, close or comment; preserve #1753 hold.

## Review scope and witnesses

- Product remote: `https://github.com/mcpdev80/baseharbor.git`, resolved from `git remote -v` in the product worktree.
- PR #1752 is OPEN and draft; branch `lane-0428-061-sourcepull`; exact head `a4adc29a5844266cf4009bb12b9b68ae26a4a99a`.
- Base `develop`: `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Live refs observed: `a4adc29a5844266cf4009bb12b9b68ae26a4a99a refs/pull/1752/head`; `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop`.
- `git merge-base --is-ancestor develop-6209874428 pr1752-a4adc29a`: exit 0.
- Full diff against develop: 18 paths, 1,412 insertions, no deletions: `cmd/baha/app_pull.go`, `cmd/baha/app_pull_options_test.go`, `cmd/baha/app_pull_render.go`, `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go`, `cmd/baha/mcp.go`, `cmd/baha/mcp_lifecycle_extra.go`, `contracts/machine/v1/control.golden.json`, `docs/cli/command-index.md`, `docs/de/cli/command-index.md`, `docs/de/reference/cli-machine-coverage.md`, `docs/de/reference/mcp.md`, `docs/reference/cli-machine-coverage.md`, `docs/reference/mcp.md`, `internal/development/source.go`, `internal/development/source_pull.go`, `internal/development/source_pull_test.go`, `internal/machine/contract.go`.
- The candidate adds commits `719242df` (F1/F2/F3 fixes) and `a4adc29a` (compile-fix attempt) atop the previously reviewed same-chain commits. The observed commit identity remains `0428-061-sourcepull`; no foreign commit was found.
- Product diff check and ancestry were read-only. No product edits, local tests, merge, close or PR comment were performed.

## Findings

### F1 — REQUEST CHANGES: JSON plus `--up` still emits two top-level documents

At `cmd/baha/app_pull.go:157-172`, `runAppPull` first writes `result` as JSON, then after successful `--up` writes the composite document to the same writer. The helper itself emits one valid JSON value, but the pull JSON already written remains in the stream. `baha app pull --output json --up` therefore does not produce one valid JSON document. The MCP handler subsequently calls `json.Unmarshal` on this combined buffer, so pull and app-up can mutate successfully and then the MCP tool reports a decoding error. No changed test covers JSON failure exit status or JSON-plus-`--up` composite output.

Repair: for JSON plus `--up`, emit only the composite object; do not write the standalone pull value first. Add CI-routed tests asserting one decodable JSON document with `pull` and `up`, and a failed-pull nonzero exit with structured failure output.

### F2 — Addressed in implementation

`machineApplicationPullInput` has `components` and `up` fields, and the MCP handler passes both into the shared pull coordinator. Component filtering is wired through `machinePullComponents` and the shared source filter. The previously missing MCP component/up fields are present.

### F3 — Runtime behavior documented; regression test still fails due incorrect snapshot

The implementation documents sequential fast-forwards and no cross-repository rollback; it reports the changed and failed repositories and keeps aggregate success false, preventing `--up`. The apply-time test deliberately creates local drift after preflight so the second repository's fast-forward fails after the first repository advances.

The compile-fix commit leaves `webBefore := gitRev(t, localB)` at `source_pull_test.go:264`, before it creates the local drift commit at line 265. The later assertion at line 308 expects the failed repository to remain at this pre-drift revision. Correct behavior leaves the intentional drift commit in place. Hosted CI confirms the bad expectation: `source_pull_test.go:308: web-source was mutated by the failed pull: before=173f6b07a81d159d3acea68859a43fb7a04a04f2 after=97ea58f76ad81144a9f32591f7fc50337046812f`.

Repair: retain a separate pre-drift revision only for verifying the fixture mutation, then snapshot the post-drift revision before calling `ApplySourcePull` and compare the failed repo against that post-drift snapshot. This is a regression-test assertion error; the recorded result shows no additional mutation during the failed fast-forward.

### F4 — Approval gate implemented; dedicated regression remains absent

`machineApplicationPullInput` now contains `Approval`, and `cmd/baha/mcp_lifecycle_extra.go:96-98` calls `applicationlifecycle.RequireApproval("app.pull", input.Approval)` before invoking the source-pull coordinator. The registry and golden continue to declare `ConfirmationRequired: true` and `PolicyRequired: true`. Static inspection confirms the missing explicit gate from the earlier head is implemented. The current diff still adds no MCP app.pull approval test; changed test paths are only `app_pull_options_test.go` and `source_pull_test.go`. Add direct coverage for rejection without approval before Git operations and acceptance with explicit approval.

## Machine golden and source semantics

The golden change remains an additive `app.pull` record: mutating safety, confirmation and policy required, contract version v1, MCP tool `baseharbor.app.pull`. Its public registry surface agrees with the enforced approval code.

Source selection, strict fast-forward, dirty/ahead/diverged/missing-upstream fail-closed handling, and `--up` gating remain as previously reviewed. The documented runtime behavior is sequential and non-atomic across independent repositories; partial results remain unsuccessful and never start `--up`.

## Hosted CI state

- Run `44971782040` is terminal `failure`, event `pull_request`, exact head `a4adc29a5844266cf4009bb12b9b68ae26a4a99a`.
- `PR · Draft Go · packages` job `137052952860` failed on the new partial-failure test. Exact line: `source_pull_test.go:308: web-source was mutated by the failed pull: before=173f6b07a81d159d3acea68859a43fb7a04a04f2 after=97ea58f76ad81144a9f32591f7fc50337046812f`.
- `PR · Draft Go · cli-3` job `137052952179` failed during `TestEndToEndInstalledZshAndFishWrappers`. Exact environment/setup line: `context_terminal_test.go:467: zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh": executable file not found in $PATH`. This is a runner prerequisite/setup failure, not evidence of an app.pull assertion failure. Workflow files remain owner scope; no rerun or workflow edit was attempted.
- `PR · Draft Go · cli-0` `137052952244`, `cli-1` `137052952191`, and `cli-2` `137052952200` succeeded.
- `PR · Draft source and routing` `137052952001` succeeded.
- `PR · Trusted Plan` `137052953767` and `PR Selected Checks` `137052954250` were skipped. Skipped is not a pass; there is no successful required aggregate for this head.

## Cleanliness and repository rules

- Docker before/after snapshot, PID 1582451: the same seven pre-existing exited `bh-itest-*` containers were listed both times; zero running. This review started no containers or compose projects and ran no local tests.
- Product worktree has pre-existing untracked `0428-183-hopdev-plan/`; it remains untouched.
- Evidence is stored only in the real Planning repository, whose verified remote is `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push). Concurrent unrelated Planning edits were left untouched; only this evidence file was staged.
- #1753 hold/review state is unchanged.

## VERDICT

REQUEST CHANGES for exact head `a4adc29a5844266cf4009bb12b9b68ae26a4a99a`. F1 remains a product behavior defect: JSON plus `--up` writes two top-level documents. F3's newly compiling regression test fails because it compares against the pre-drift revision. The `cli-3` failure is a hosted-runner setup failure due missing `zsh`; report it as state for the owning CI cell. `PR Selected Checks` and Trusted Plan are skipped, so the run is not a passing required-gate receipt. F2 and F4 are implemented in code; direct approval regression coverage is still missing. No product branch changes, merge, close or comment.

END codex-rev-1747 DONE — REQUEST CHANGES for exact head a4adc29a5844266cf4009bb12b9b68ae26a4a99a
- First evidence push delivery witness: `db962b0df194eb8a0030476fe114b9be582b0ed6 refs/heads/main`.
