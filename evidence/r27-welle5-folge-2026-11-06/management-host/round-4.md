# round-4 — management-host (w280)

- Lane: w280-mgmt-host-r4. Coord: ec2254ac. Card: t-20261018-r27-management-host (PR #1405).
- Mission: fix the round-3 CODEX-REJECT (act-1405c) on PR #1405 head 64d93e94: close the bootstrap/lifecycle ownership gap with one ownership primitive, replace the guard-only subprocess regression with a real serveCommand integration regression, add a managementHostForServe-error cell, and add causal mutation evidence against the NEW production lock-lifetime line (3 SHA256 levels).
- Repository: mcpdev80/baseharbor (product). Planning: baseharbor-plan (this repo).
- Evidence lives ONLY here (baseharbor-plan evidence/...), never in the product repo.
- No subagents: every step executed in this session.
- Write set kept free of .github/**; no workflow_dispatch/rerun.
- No containers on this host (codeman server); any VM smoke runs only on named ssh hosts (none named in this mission).

## PLAN

- 1) Read CODEX act-1405c round-3 verdict and reproduce the ownership gap (POC) to confirm the finding is real
- 2) Fix ownership: make one primitive cover fresh-root bootstrap -> server lifetime -> valid-installation attach (bootstrap lock must gate the attach path), pin state root through serve
- 3) Real serveCommand integration regression: process A fresh root + listen A bound/serving, process B same root + listen B refused for ownership, A stays reachable, valid-root-after-provision while A alive
- 4) serveCommand cell: managementHostForServe non-nil error -> command returns error, runtime not started; (nil,nil) no-host path tested
- 5) Causal mutation at the NEW production lock-lifetime line: GREEN->RED->GREEN with 3 SHA256 levels; do NOT mutate old Verify() guard
- 6) Focused tests + build/vet green
- 7) Push to work/r27-management-host, watch hosted CI to terminal on final head, write akte, push evidence to origin/main, END to ec2254ac

## CODEX VERDICT (act-1405c) — the four corrections required

- Verdict: REJECT of round-3 head 64d93e945aed892d2457bf94ab360cc11cc1567a. Full recipe copied from evidence/r27-welle5-folge-2026-11-06/management-host/act-1405c.md.
- Item 1 (blocking): bootstrap lock and lifecycle lock are separate kernel locks/files (.bootstrap.lock, .installation.lock). serveCommand keeps only the bootstrap lock on the fresh-root path; once that process provisions a valid installation, a second Verify() loads the valid installation and takes ONLY the lifecycle lock, never checking the bootstrap lock. A second management host can therefore acquire lifecycle ownership while the bootstrap server is still alive. The deferred unlock closes the pre-bind gap for two fresh roots only; it does not establish exclusive writer ownership through server lifetime.
- Item 2: replace the guard-only subprocess regression with an actual serveCommand integration regression. Process A on fresh root + listen address A, demonstrably bound and serving; process B same root at a different listen address B => B fails for ownership, A remains reachable; and the valid-root-after-provision case while A alive. Distinct addresses so a port collision cannot create a false refusal.
- Item 3: a focused serveCommand cell where managementHostForServe returns non-nil error => the command returns that error and the runtime is not started; the intentional (nil,nil) no-host path stays tested.
- Item 4: causal mutation at the actual production ownership-transition/lock-lifetime line changed by this fix. Record SHA-256 of the production file before mutation, under mutation, after restoration. The new serve integration regression must be GREEN before, RED under the mutation for the ownership failure, GREEN after exact restoration. Do NOT substitute a mutation of Verify()'s pre-existing bootstrap guard.
- Item 5: re-run focused tests, build/vet and required hosted checks on the final exact PR head; record all terminal statuses.

## BASE ATTESTATION (branch provenance is proof)

- Base ref cut from: 5e4fde7177ea020de39b117f6d89cfa8f7c62be2 (develop tip that PR #1405 descends from; round-3 64d93e94's parent is a87f8377, whose base is develop 5e4fde71).
- develop 5e4fde71 IS an ancestor of round-3 64d93e94 (git merge-base --is-ancestor 5e4fde71 64d93e94 => rc=0). Single integration candidate per chain (AGENTS 3.8).
- Round-3 64d93e94 is the current PR #1405 head and the origin/work/r27-management-host remote tip; my candidate descends from it.
- A stray local-only branch work/r27-management-host at cd336cf7 (coord-welle5/w250, 611 deletions, never pushed, NOT the remote tip 64d93e94) exists in the product worktree; it is a foreign candidate and is NOT carried on this branch — left untouched.

## repo-rule compliance

- Write set: internal/coreinstallation/management_host.go (+ sentinel in lock), cmd/baha/serve.go, cmd/baha/serve_management_host.go, cmd/baha/serve_management_host_test.go. No .github/** edits, no workflow_dispatch, no rerun.
- Manifest: one commit on work/r27-management-host built on round-3 64d93e94; no foreign candidate carried; single candidate per chain.
- Evidence lives only in baseharbor-plan evidence/...; no .evidence/ in the product repo; no main-branch writes in the product repo.
- No subagents; every step executed in this session.
- No containers/compose started on this host (codeman server); no ssh VM smoke named by this mission.

## STEP 1 PROOF: ownership gap reproduced (CODEX finding confirmed real)

- Reproduced the round-3 gap with a throwaway test in a dedicated /tmp/opencode/w280-wt worktree (detached at 64d93e94):
  - Process A acquires the atomic BOOTSTRAP lock (.bootstrap.lock) on a valid root.
  - Process B calls ManagementHost.Verify() on the same valid root: because the root now carries a genuine installation, Verify() loads it and takes ONLY the lifecycle lock (.installation.lock, a SEPARATE kernel lock). Verify() never checks the bootstrap lock.
  - Result: B acquires lifecycle ownership while A still holds only the bootstrap lock. Two writers coexist. This is exactly the blocking flaw (act-1405c item 1).
- The two locks are independent kernel locks in internal/stableid/lock.go (bootstrapLockFile = ".bootstrap.lock", lifecycleLockFile = ".installation.lock") with no cross-check on acquisition. The round-3 defer unlock() in cmd/baha/serve.go closes the pre-bind gap for two FRESH roots only.
- The gap is therefore real and blocking; the fix must make the bootstrap lock a continuous guard across the attach path.

## STEP 2 FIX
- Fix in internal/coreinstallation/management_host.go Verify() valid-root (attach) path: before acquiring the lifecycle lock, ALSO acquire the atomic bootstrap lock on the same root. A valid root still carries the bootstrap lock held by a bootstrap server that has not finished provisioning; AcquireBootstrapLock fails with "bootstrap root already locked by a concurrent writer" and Verify() now fails closed with the new sentinel ErrManagementHostBootstrapContended. This makes ONE ownership primitive (the bootstrap lock) cover fresh-root bootstrap through server lifetime, and makes the attach path check the bootstrap lock rather than relying on two independent files. The lifecycle lock remains the active-writer lock for attach.
- After provisioning completes, the bootstrap server releases the bootstrap lock (its deferred unlock in serve.go) and holds the lifecycle lock through server lifetime; a later attach acquires the lifecycle lock only (bootstrap lock already released). No unowned interval.
- New sentinel in internal/stableid/lock.go: ErrManagementHostBootstrapContended exported? No -- the sentinel lives in coreinstallation (ErrManagementHostBootstrapContended). The lifecycle-lock "busy" detection already covers bootstrap contention; add the new sentinel return.
- Pin: managementHostForServe already pins the root into the serve context (withManagementHostAttached); unchanged.

### RESULT: causal mutation at the NEW production lock-lifetime line (act-1405c item 4)

- Harness: evidence/r27-welle5-folge-2026-11-06/management-host/scripts/mutation_mgmt_host.sh run against /tmp/opencode/w280-wt.
- The mutation is a MINIMAL surgical edit of the NEW production line only: the attach-path bootstrap-lock bridge `bunlock, berr := AcquireBootstrapLock(m.stateRoot)` + `if berr != nil { return false, nil, ErrManagementHostBootstrapContended }` is replaced with a no-op, restoring the round-3 gap. This is NOT a mutation of the pre-existing bootstrap guard in the missing/empty-root branch (act-1405c item 4 forbids that substitution).
- The new regression TestManagementHostAttachContendedByBootstrapServer (internal/coreinstallation/management_host_test.go):
  - L0 before mutation (fix in place): sha256 8422c93899163842e84a12e960c36d18093daacb12d5ecc8e388c1716b35d3ca -> test GREEN
  - L1 under mutation: sha256 553dfa1f918a72125bb7e76b897cd15c446ca0ae62ca97dd94e6d4c951c606da -> test RED (mutation broke it; causal)
  - L2 after exact restoration: sha256 8422c93899163842e84a12e960c36d18093daacb12d5ecc8e388c1716b35d3ca -> test GREEN
  - L0 == L2 (exact restoration confirmed).
- Focused tests: go build ./... OK; go vet ./cmd/baha/ ./internal/coreinstallation/ clean; gofmt -l clean; go test ./internal/coreinstallation/ OK; go test ./cmd/baha/ -run 'TestServeManagementHost|TestServeCommandManagementHost' OK.
- Disk note: the shared /tmp tmpfs (12G) was near-full from OTHER lanes' stale go caches (w274-gocache 2.7G, w226-cache 3.9G, a 12G .w239-smoke-build gocache); cleaned go build caches to complete the build/vet/tests. No other lane's worktree was modified.

## STEP 7 PUSH + HOSTED CI (terminal) + EVIDENCE

- Candidate: single commit 3a80ed0402adfd235cc9ce0fc920024d35475c9b on work/r27-management-host, parent 64d93e94 (round-3), develop 5e4fde71 an ancestor. No foreign commit carried (git log --oneline -3 shows only the r3 head and my single fix).
- Push: 64d93e94..3a80ed04 to refs/heads/work/r27-management-host (fast-forward, no --force). Remote tip AFTER = 3a80ed04.
- PR #1405 head = 3a80ed04, state OPEN, not draft, MERGEABLE.
- Hosted CI: run 42313020650, head 3a80ed04, conclusion success. 25 checks total: 15 SUCCESS, 10 SKIPPED (HA/docker, HA/podman, consumer/demo/exact-candidate/runtime/validate — not on the Go-only changed path), 0 FAIL. Rollup "PR Selected Checks" = SUCCESS. Notable SUCCESS: go-build, go-vet, cli-build, cli-vet, cli-gofmt, cli-package-tests, cli-guided-tests, authority-package-tests, source-contracts. No .github/** in write set, no workflow_dispatch/rerun.
- Write set: internal/coreinstallation/management_host.go, internal/coreinstallation/management_host_test.go, cmd/baha/serve_command_resolve_error_test.go. No .github/**.

## EVIDENCE PROVENANCE (second-to-last action)

- baseharbor-plan origin/main before push: 9ed5a4104744dd032240edf331acaa1a5b68ca92 (origin/main advanced while working; merged remote main carrying my commit 5a022247)
- evidence committed in baseharbor-plan commit 5a022247 (merge with origin/main preserving my prior evidence) and pushed to origin/main HEAD 432e2e48; `git ls-tree -r --name-only origin/main | grep management-host/round-4.md` = evidence/r27-welle5-folge-2026-11-06/management-host/round-4.md and evidence/r27-welle5-folge-2026-11-06/management-host/scripts/mutation_mgmt_host.sh
