
## REVIEW — PR #1794

- Role: CODEX-REVIEW, independent review of the complete exact-head diff. A separate CODEX-MERGE role follows only because every acceptance check passed.
- Reviewer identity: codex-rev-1747, independent of PR author w078. Session UUID/backend were not exposed in the shell. Model family: GPT-6.
- Review time: 2026-11-23 05:12 UTC.
- Product remote resolution: `origin`, `lane-origin`, and `upstream` resolve to `https://github.com/mcpdev80/baseharbor.git`; only this GitHub URL was used as the remote truth witness.
- Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- `python3 baseharbor-plan/scripts/plan.py show t-20261123-catalog-ingress-develop-prereqs` reports the source catalog-ingress task as accepted. This review follows the exact PR-specific contract in `/tmp/opencode/m_rev_1794.md.g`.

### Candidate and ancestry

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/ingress-0428-078-perses-identity refs/pull/1794/head refs/pull/1650/head` returned:
  - `7880a8f6bcfaabd8fd254ef987522abc1770c52e refs/heads/develop`
  - `3b1fa817abbade86987b854b7ea581d67532fcd2 refs/heads/ingress-0428-078-perses-identity`
  - `3b1fa817abbade86987b854b7ea581d67532fcd2 refs/pull/1794/head`
  - `d3100a1faa304abf71aa52f8bb187a9889b038bf refs/pull/1650/head`
- PR API reports #1794 open, not merged, not draft, mergeable, mergeable state `clean`, exact base `develop` at `7880a8f6bcfaabd8fd254ef987522abc1770c52e`, exact head `3b1fa817abbade86987b854b7ea581d67532fcd2`.
- GitHub compare API reports merge base equal to develop, `ahead_by: 1`, `behind_by: 0`, and one changed file. The sole ahead commit is `3b1fa817abbade86987b854b7ea581d67532fcd2` with message `docs(ci-gate): add two pr-gate-coverage rows for perses identity-witness paths (#1650 ingress)`.
- PR #1650 is still open at `d3100a1faa304abf71aa52f8bb187a9889b038bf`, based on the same develop SHA. Its diff touches both referenced product paths. Both paths currently exist on develop; the contract also explicitly allows forward rows if paths are absent until #1650 lands. This condition is satisfied without depending on #1650 being merged first.

### Diff and catalog validation

- Exact diff: `scripts/pr-gate-coverage.json`, 12 insertions and 0 deletions; no other path changed.
- The two rows added relative to develop are exactly:
  - `source.cmd.baha.app.status.result.test.go` → `cmd/baha/app_status_result_test.go`, `runtime_specific: true`, surfaces `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`.
  - `source.internal.metrics.realization.go` → `internal/metrics/realization.go`, `runtime_specific: true`, surfaces `source.gate.atomic.docker.data.capabilities` and `source.gate.atomic.podman.data.capabilities`.
- Both row shapes match the requested data-capabilities surface pattern. Full-catalog comparison found exactly two added component rows and no removed rows. No duplicate IDs or paths exist in the resulting catalog. Root keys are unchanged and `release` remains `v0.4.27` on both base and candidate.
- No `.github/**`, `go.mod`, product source, or unrelated catalog entries changed.

### Exact-head CI, reviews, and active rules

- Run `45115221208` is `completed/success`, event `pull_request`, exact head `3b1fa817abbade86987b854b7ea581d67532fcd2`.
- The complete check-run census is 32 terminal check runs: 11 success and 21 skipped; none are queued, in progress, or failed. `PR Selected Checks` succeeded for the exact head, and its GitHub Actions app integration id is `15368`, matching the active required-status-check ruleset `25223521`.
- Supporting successful checks include `PR · Trusted Plan`, `PR · Native gate plan`, `PR · Source format`, `Workflow policy`, `PR · Focused Python`, and candidate-added advisory checks. The candidate-added advisory check succeeded. The 21 skipped groups are not counted as passes; they were not selected for this catalog-only diff. The active ruleset requires `PR Selected Checks`, which passed.
- Live ruleset inspection: `25223521` (`develop - required checks`) is active and requires `PR Selected Checks` with integration id `15368`; strict up-to-date is enabled. Ruleset `23754541` (`develop - integration branch`) is disabled, so it is not represented as technically active. Merge will use the ordinary squash path with an expected-head guard and no admin/bypass flag.
- Fresh review inventory: zero existing PR reviews and zero review threads. This evidence is the independent Codex review of the complete candidate; there are no unresolved review threads.

Review verdict: APPROVE. All mission acceptance points pass; proceed to ordinary squash merge guarded by exact head `3b1fa817abbade86987b854b7ea581d67532fcd2`.

## repo-rule compliance

- No product files or workflows were edited. No local product tests or VM/container tests were run; this catalog-only PR was validated by its exact-head hosted checks.
- The shared product checkout contains unrelated existing modifications and untracked paths. They were not changed, staged, reset, or used as remote-state evidence.
- Planning evidence is kept only in this repository under the required `evidence/r28-welle5-2026-11-23/sweep-1650/` path.

## cleanliness

- A Docker baseline was not captured at the start of review. No local container or compose command was run during review.
- Post-merge and pre-publication witness: PID 3889606 ran `docker ps -a --no-trunc`; output was only `CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES`.
- Final pre-publication witness: PID 3890502 ran `docker ps -a --no-trunc`; output was only `CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES`.

## MERGE — CODEX-MERGE

- Review verdict was APPROVE with no open threads. The expected-head squash merge was then performed through the normal GitHub path, without `--admin` or a bypass flag.
- The first CLI invocation without an explicit `--repo` failed locally before contacting GitHub (`failed to run git: fatal: not a git repository`). Retrying as `gh pr merge 1794 --repo mcpdev80/baseharbor --squash --match-head-commit 3b1fa817abbade86987b854b7ea581d67532fcd2` succeeded.
- GitHub PR API confirms merged at `2026-11-23T05:13:42Z`, merge commit `0c1b8ca2ff4a057853432a7a565040be57cade06`. The remote `refs/heads/develop` points to that merge SHA; `refs/pull/1794/head` remains the reviewed SHA. PR #1794 is closed and merged.
- Merge-triggered `Runtime · Docker Core · develop`, run `45116441716`, completed success on merge SHA `0c1b8ca2ff4a057853432a7a565040be57cade06`; its one selected job succeeded and five other jobs were skipped. `Runtime · Podman Core · develop`, run `45116441723`, completed success on the same merge SHA; its one selected job succeeded and three other jobs were skipped. Skipped jobs are not treated as passes. Both runs were observed to terminal success with `gh run watch --repo mcpdev80/baseharbor ...`.
- The merged develop tree contains both intended catalog rows and retains `release: v0.4.27`.

## END codex-rev-1747 DONE

PR #1794 was independently reviewed and normally squash-merged. Merge SHA and current develop head: `0c1b8ca2ff4a057853432a7a565040be57cade06`.

## origin/main evidence-path witness

Exact output from `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle5-2026-11-23/sweep-1650/review-merge-1794.md` was:

```text
evidence/r28-welle5-2026-11-23/sweep-1650/review-merge-1794.md
```
