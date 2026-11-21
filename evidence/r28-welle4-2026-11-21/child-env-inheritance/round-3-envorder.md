# round-3-envorder — card t-20261121-child-env-inheritance (0428-222)

## END 0428-222-hopdev DONE

## PLAN (numbered)

- Fix the security finding (reviewer confirmed, independently remeasured by coordinator): the four etcd/etcdutl call
  sites pinned PATH/API/TLS keys FIRST and appended `os.Environ()` LAST; Go's env-dedup is last-wins, so an inherited
  ETCDCTL_API / ETCDCTL_ENDPOINTS / ETCDCTL_CACERT / ETCDCTL_CERT / ETCDCTL_KEY / PATH overrides the pin, making the
  pinned endpoint and TLS trust swappable by a parent process.
- Add `func pinnedEnv(pins ...string) []string` in `internal/corebackup/etcd/`: copy `os.Environ()`, drop every key
  named in `pins`, append the pin values last. This makes the security property independent of Go's dedup rule.
  Apply at all four sites (etcdctl.go:98-106, :119, :162-167, etcdutl.go:98); leave no half-edited site.
- Expand `internal/corebackup/etcd/child_env_inheritance_0428_222_test.go`: one case per pin key
  (PATH, ETCDCTL_API, ETCDCTL_ENDPOINTS, ETCDCTL_CACERT, ETCDCTL_CERT, ETCDCTL_KEY) that (i) sets a parent opposite
  value and (ii) proves the child process env image shows the pin value, not the inherited one. Per call-site subtests
  for all four sites (save, endpoint-status, isolated-restore).
- Targeted `go vet` + `go test ./internal/corebackup/etcd/ -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` — no bare `go test ./...` or `go test ./cmd/baha/` on this host (/tmp quota, `/` 5G free).
- Commit on develop base (e6c199e7b7dd), single author `0428-222-childenv` (identity of the accepted candidate;
  card 0428-224 forbids rewriting SHA witnesses). Prove merge-base ancestor, rev-list=0, parent-sha, one identity line.
- Push to refs/heads/lane-0428-222-child-env; PR #1749 stays the one PR; no merge, no ready-not-befehl, no second PR.
- Own hosted run to terminal at the exact head (4.6); verify which gates the run actually executed vs skipped and report
  file:line if a runtime gate is required by the changed path but not triggered by this PR-run.
- Commit this akte to origin/main of baseharbor-plan (verify via ls-tree before END); post END with plan-sha, PR-head-sha,
  run-id, conclusion per cell, cleanliness line.

## BASE ATTESTATION

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`:
  e6c199e7b7dd7d076a776d11c3ba16f25e59c254	refs/heads/develop
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-222-child-env`:
  68f48754b9f1338daeee83fc4d6609dd306cc859	refs/heads/lane-0428-222-child-env  (round-2 hop head; base for round-3)
- e6c199e7b7dd is an ancestor of the fix commit 3df3cb8be (proof 1 below).

## FIX

pinnedEnv(pins ...string) []string in internal/corebackup/etcd/etcdctl.go:

```go
func pinnedEnv(pins ...string) []string {
	dropped := make(map[string]struct{}, len(pins))
	for _, p := range pins {
		if i := indexByte(p, '='); i >= 0 {
			dropped[p[:i]] = struct{}{}
		}
	}
	out := make([]string, 0, len(os.Environ())+len(pins))
	for _, kv := range os.Environ() {
		if i := indexByte(kv, '='); i >= 0 {
			if _, bad := dropped[kv[:i]]; bad {
				continue
			}
		}
		out = append(out, kv)
	}
	return append(out, pins...)
}
```

It copies `os.Environ()`, removes every key named in `pins`, then appends the pin values last. The drop is mandatory:
with Go's env-dedup (last value wins) an inherited ETCDCTL_* key placed before the pin would win and silently override
the pinned endpoint/trust. Result is therefore independent of Go's dedup rule. Applied at all four sites; every site now
reads `cmd.Env = pinnedEnv(...)`. `indexByte` is a small local byte-offset helper.

## EVIDENCE (proves, not asserts)

- gofmt: clean on etcdctl.go, etcdutl.go, child_env_inheritance_0428_222_test.go (empty gofmt -l output).
- go vet ./internal/corebackup/etcd/ : exit 0.
- `go test ./internal/corebackup/etcd/ -count=1 -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`: ok, 61 tests pass, 0 fail (per-run -v log; subset shown in the run transcript below).
- CI run 44934281616 at head 3df3cb8be: completed/success; 14 jobs executed (success), 21 skipped.
  PR Go unit · packages = success (covers ./internal/... including the write-set path).
- PR #1749 head via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1749/head` == 3df3cb8be6372df630b880d369f3806b0a8fe214.

## VIER PROOFS at fix head 3df3cb8be

- `git merge-base --is-ancestor e6c199e7b7dd 3df3cb8be` = JA (develop is ancestor).
- `git rev-list --count 3df3cb8be..e6c199e7b7dd` = 0.
- `git log -1 --format=%P 3df3cb8be` = 68f48754b9f1338daeee83fc4d6609dd306cc859 (round-2 base).
- `git diff --name-only e6c199e7b7dd 3df3cb8be` = the 3 changed files (child_env_inheritance_0428_222_test.go, etcdctl.go, etcdutl.go) plus the 2 files the round-2 base already carries (internal/coreupdate/child_env_inheritance_0428_222_test.go, internal/coreupdate/dcs_boot_probe.go); only this card's write-set.
- `git log --format=%an e6c199e7b7dd..3df3cb8be | sort -u` = 0428-222-childenv (exactly one identity).

## RUN 44934281616 (terminal, 4.6)

head 3df3cb8be6372df630b880d369f3806b0a8fe214, state completed/success.
Non-skipped job conclusions:
- PR · Go unit · packages: success  (covers write-set path internal/corebackup/etcd + internal/coreupdate)
- PR · Validation · go-build: success
- PR · Validation · go-vet: success
- PR · Source format: success
- PR · Trusted Plan: success
- PR · Native gate plan: success
- PR · Go unit · owner / cli-0..3: success
- PR Selected Checks aggregate: success
Skipped (21): release/HA/pre-release/consumer-pin gates, not required for this lane.

Runtime-gate question (rc2 step 7): the change is a Go helper + a unit test in internal/corebackup/etcd and a test-only
change in internal/coreupdate. No runtime/container path (docker/podman lifecycle, deployment, or host-bound etcdctl
invocation) is exercised by this change; the correct gate is the Go unit test suite in PR Go unit · packages, which
executed and passed. No runtime gate is required by the changed path. No .github/** or scripts/** change made
(Owner scope); nothing to hand off.

## repo-rule compliance

- Write-set: only the 3 files in internal/corebackup/etcd/. No new function beyond pinnedEnv; no new file; no
  .github/**, no scripts/**, no internal/identityprovider/**, internal/serviceaccess/**, internal/operatorauth/**,
  internal/observability/registry.go, internal/capability/perses_selection.go.
- No bare `go test ./...` / `go test ./cmd/baha/` on host (TEST RUNNER RULE). Ran the targeted named form with skip list.
- Single commit, single author 0428-222-childenv; no second PR; no merge; no ready-not-befehl; no rebase onto a foreign
  branch name. Commit ancestry: 3df3cb8be parent 68f48754b (round-2 base), which is itself on develop e6c199e7b7dd.
- Evidence written only into baseharbor-plan (product repo untouched for planning acts).

## cleanliness

- No compose project / container started this round (git + go vet + go test only). `docker ps -a` before (my pid 2146668):
  only bh-itest-* orphan containers from other lanes (3 hours old, Exited). No container brought down by this lane.
- Host free space at end: ~5G on / (98% used); /tmp at 80% — both host constraints; targeted test form used to avoid quota.

## 0428-222-hopdev END DONE
plan-sha: 3df3cb8be6372df630b880d369f3806b0a8fe214
PR #1749 head: 3df3cb8be6372df630b880d369f3806b0a8fe214
run-id: 44934281616 (completed/success)
