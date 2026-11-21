# CODEX-REVIEW — PR #1749 / card 0428-222 / exact head ed9741b93c0395ec6d577d19f6531dc8cc964846

## PLAN

1. Pin review to exact head `ed9741b93c0395ec6d577d19f6531dc8cc964846`; verify live refs, PR metadata, ancestry/back count, author, and exact hosted run `44961731917`.
2. Inspect `internal/testsupport/envpin/pin.go` and direct tests for inherited `ETCDCTL_INSECURE_SKIP_TLS_VERIFY`, `ETCDCTL_USERNAME`, and `ETCDCTL_PASSWORD` filtering while preserving ordinary environment values.
3. Trace child process starts in `internal/coreupdate/dcs_boot_probe.go`, `internal/corebackup/etcd/etcdctl.go`, and `internal/corebackup/etcd/etcdutl.go`; determine whether any route bypasses envpin.
4. Compare `23feeefee58...ed9741b93c0` to distinguish additive develop merge content from the already reviewed security fix at `10c7c64140b`.
5. Issue exact-head APPROVE or REQUEST CHANGES with terminal run evidence and an actionable recipe if changes are required.
6. Publish this evidence to Planning origin/main; no merge or close.


## Review result

Decision: **APPROVE** for exact head `ed9741b93c0395ec6d577d19f6531dc8cc964846`. Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git` returned that exact `refs/pull/1749/head` and develop `42da7128e724a533349e93d3742cbd232ea48936`. PR #1749 is OPEN, non-draft, based on develop, author `0428-222-childenv`, mergeable `MERGEABLE`, merge state `CLEAN`. The exact pull_request run `44961731917` for this head completed `success`; `PR Selected Checks` completed success and there were zero failed jobs. No merge or close was performed.

`internal/testsupport/envpin/pin.go:45-63` drops inherited keys with prefix `ETCDCTL_` (lines 52-57), drops inherited copies of explicitly pinned non-prefix keys (58-60), preserves other inherited entries (61), then appends the requested pins (63). This removes inherited `ETCDCTL_INSECURE_SKIP_TLS_VERIFY`, `ETCDCTL_USERNAME`, and `ETCDCTL_PASSWORD` while allowing explicit controlled values such as API, endpoints, CA, certificate, and key pins to be appended. `internal/testsupport/envpin/unpinned_etcdctl_test.go:32-110` has the subprocess regression checking all three unpinned names absent, expected pins present, and ordinary `NORMAL_EXPORTED_VAR=keep-me` preserved; `:132-177` directly tests the three inherited values plus ordinary environment preservation. The filter also preserves non-ETCDCTL inherited variables by construction at `pin.go:58-63`.

At the exact candidate, all production `exec.CommandContext` paths under the named packages are routed through envpin: `internal/coreupdate/dcs_boot_probe.go:59-66`; `internal/corebackup/etcd/etcdctl.go:98-103` for snapshot save, `:122-123` for snapshot verify, and `:164-171` for endpoint status; `internal/corebackup/etcd/etcdutl.go:95-100` for restore. A repository grep for process starts under `internal/coreupdate` and `internal/corebackup/etcd` found no second production path bypassing the filter. Remaining direct starts in `runtime_integration_test.go` are test harness etcd/etcdctl instances, not these production child paths.

Hop proof: exact head `ed9741b...` is a merge commit with parents security-fix head `10c7c64140bc3a5fa673e786f15a950f5b70aa17` and develop `42da7128e724a533349e93d3742cbd232ea48936`; the fix head `10c7...` is parent 1 of the hop. The named security-fix change from prior reviewed head `23feeefee58c5438ccd37fe5c0edc674c5d0a79b` to `10c7...` changes only `internal/testsupport/envpin/pin.go` and `internal/testsupport/envpin/unpinned_etcdctl_test.go` (32 lines plus 221-line regression). The merge adds develop content only relative to the fix parent; no additional modification to the security fix.

The previous REQUEST CHANGES at `9d3393e426bb` concerned old head `23feeefee58` and is superseded for this candidate.

Planning repository verified: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

## repo-rule compliance

Reviewer-only. No product edits, local test execution, workflow actions, PR comments, merge, or close.

## cleanliness

Read-only source review; no containers or compose projects started.

END_DONE codex-rev-1747: #1749 APPROVE for exact head ed9741b93c0395ec6d577d19f6531dc8cc964846/run 44961731917 terminal success; envpin covers all named production child starts and removes inherited unpinned ETCDCTL_ values.
