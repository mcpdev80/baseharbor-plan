
## Review scope and remote state

- Task: `t-20261120-workload-port-flag-ignored-locally` / card `0428-199`.
- PR #1752 exact head: `34feb493480ec3b2703681bf576ce41e3904995b`; current live `develop`: `1ff16925c4e141d732459a34ddf0b7f49128a214`.
- PR state: OPEN, DRAFT. GitHub pull-request metadata reported base SHA `82825e95a6f6083702d0ba5401d97f356085c722`; the exact head compare against live develop reports merge base `1ff16925c4e141d732459a34ddf0b7f49128a214`, `behind_by=0`, 15 commits ahead. Run 44987053069 is exact-head terminal success; its Draft Go job logs fetched base SHA `82825e95a6f6083702d0ba5401d97f356085c722`. The run's `PR Selected Checks` aggregate was skipped because this PR is Draft, so this is Draft Go proof, not full merge-gate proof.
- GitHub compare of current develop `1ff16925c4e141d732459a34ddf0b7f49128a214` to candidate and prior feature base `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7` to old candidate `0045bdcc743854164f54adecf0cb2c17e3e49c8d` returned the same 19 changed paths. For every path, additions/deletions matched and the API patch text was identical. No missing or extra source-pull files were found relative to the prior feature candidate.
- Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

## Findings

- F1 — REQUEST CHANGES: the task contract asks for the workload-port flag to be evaluated locally, but that behavior is absent from this candidate's diff. The current diff is the guided `baha app pull` feature across 19 files; `cmd/baha/app_pull.go:34-35` lists its supported options (`-c`, `--up`, `--check`, `--manifest`, and JSON output), with no workload-port option, and no changed file adds or evaluates a workload-port flag. The candidate therefore does not demonstrate the task's core local workload-port behavior or a regression for it. Recipe: route this card to the candidate that implements local workload-port evaluation, or have the implementation owner supply a candidate whose diff includes the local evaluation and hosted regression. Stop criterion: the exact task candidate contains the local workload-port decision and a hosted job visibly executes its regression. This is a scope/contract mismatch; the source-pull changes below were reviewed independently and have no remaining F1-F4 code finding.

## Source-pull regression review

- F1 failure propagation and JSON shape: `cmd/baha/app_pull.go:153-183` returns `ErrSourcePullBlocked` when the aggregate result is unsuccessful and does not proceed to `--up`; the successful JSON `--up` path emits one composite result (`:160-183`, `:186-205`). `cmd/baha/app_pull_options_test.go:67-108` requires one decodable JSON object with `schema_version`, `pull`, and `up`.
- F2 MCP contract: `cmd/baha/mcp.go:100-107` exposes `components`, `up`, and `approval`; `cmd/baha/mcp_lifecycle_extra.go:89-113` authorizes `app.pull`, calls `applicationlifecycle.RequireApproval`, routes options into shared `runAppPull`, and returns structured JSON.
- F3 partial apply: `internal/development/source_pull.go:136-193` performs fast-forwards sequentially, marks individual failure details, leaves already-advanced sources advanced, and sets the aggregate unsuccessful if any source failed. CLI `--up` remains after the aggregate-success check. `internal/development/source_pull_test.go:206-321` exercises an earlier successful fast-forward followed by a real later divergence and asserts no rollback of either source.
- F4 explicit MCP approval: the handler enforces approval at `cmd/baha/mcp_lifecycle_extra.go:91-106`; `cmd/baha/app_pull_mcp_approval_regression_test.go:26-76` drives the registered MCP tool and checks refusal for `approval=false` and passage past the approval gate for `approval=true`.
- The control golden fixture and generated command/MCP reference changes are in the same 19-file diff as the old feature candidate, with byte-identical API patches per file; no additional fixture drift appeared in the current-base comparison.

## Hosted Draft proof

- Exact run `44987053069`: terminal `completed / success`, head `34feb493480ec3b2703681bf576ce41e3904995b`.
- `PR · Draft source and routing`: job `137099809829`, success.
- `PR · Draft Go · packages`: job `137099809947`, success; log includes `ok github.com/mcpdev80/baseharbor/internal/development 3.670s`.
- `PR · Draft Go · cli-0`: job `137099809960`, success; `PASS cli-0: 464 passed / 13 intentionally skipped / 477 discovered`.
- `PR · Draft Go · cli-1`: job `137099810267`, success.
- `PR · Draft Go · cli-2`: job `137099810028`, success.
- `PR · Draft Go · cli-3`: job `137099810021`, success. The log installs both shells (`zsh: /usr/bin/zsh`, `fish: /usr/bin/fish`), runs `go test ./cmd/baha -run TestEndToEndInstalledZshAndFishWrappers -count=1 -v`, and records `--- PASS: TestEndToEndInstalledZshAndFishWrappers (7.60s)` plus `PASS cli-3: 428 passed / 16 intentionally skipped / 444 discovered`.
- `PR Selected Checks` job `137099812604` was skipped. No claim is made that full required CI passed or that the PR is merge-ready.

## Authorship

The identity mixture remains in the exact current head's 15-commit compare list. Eleven commits use `0428-061-sourcepull <0428-061@baseharbor.local>`; the final hop uses `Marcel Pfingstgräf <22537373+mcpdev80@users.noreply.github.com>`. Three commits still use the placeholder identity `BaseHarbor Worker <worker@example.invalid>`: `b010dabcb...`, `e7df5ab4a6c3219404de26846198d4f6e1b8fed0`, and `7b3c658800aff87ce8298fe370c5bcd448942f83`. This is an owner identity follow-up, not a code finding; the mixture did not disappear.

## Verdict

REQUEST CHANGES because F1 shows the exact candidate does not implement or test the task's local workload-port behavior. The source-pull F1-F4 findings are resolved in the reviewed feature diff. The Draft Go proof is green for the exact head, but `PR Selected Checks` is skipped and cannot establish merge readiness. Owner attention: the three placeholder-author commits listed above remain.

## repo-rule compliance

- Read-only review. No local tests, product changes, GitHub comments/reviews, workflow reruns, PR state changes, merges, or container operations were performed.

## cleanliness

- Before review, PID `2413388`: `docker ps -a` showed only pre-existing container `baha-prunit-db-2286133` (`a0d40c5bcc8e`), Postgres 18, Up; it was not started or changed by this review.
- After review, PID `2416562`: `docker ps -a` showed the same pre-existing container `baha-prunit-db-2286133` (`a0d40c5bcc8e`) Up; no container was created, stopped, or modified.

## END codex-rev-1747 BLOCKED

Verdict REQUEST CHANGES for candidate `34feb493480ec3b2703681bf576ce41e3904995b`; Draft run `44987053069` terminal success. The core workload-port behavior is absent from this source-pull diff. Author identity mixture remains: `b010dabcb...`, `e7df5ab4a6c3219404de26846198d4f6e1b8fed0`, `7b3c658800aff87ce8298fe370c5bcd448942f83` are by `BaseHarbor Worker <worker@example.invalid>`.
