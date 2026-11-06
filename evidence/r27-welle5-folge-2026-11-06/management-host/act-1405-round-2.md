# r27 round-2 (folge-2026-11-06) — management-host (w255, rerun of aborted w255)

- Lane: w255-mgmt-host-lock. Coord: 841e7734. Card: t-20261018-r27-management-host.
- Mission: round-2 REJECT-KORREKTUR of act-1405 (PR #1405). Implement the act-1405 correction recipe.
- Repository: mcpdev80/baseharbor (product). Planning: baseharbor-plan (this repo).
- Evidence lives ONLY here (baseharbor-plan evidence/...), never in the product repo.
- No subagents: every step executed in this session.

## PLAN

- Read mission, act-1405, round-1 evidence, PR #1405 (cd336cf7); define scope (bounded management-host serve path, durable state root, single active writer, lifecycle-under-active-host)
- Establish base: ls-remote develop head 5e4fde7177ea020de39b117f6d89cfa8f7c62be2; confirm ancestor of PR head; write SHA in evidence
- Fix #1 bootstrap ownership: bootstrap obtains ATOMIC EXCLUSIVE ownership of the newly created protected root before bind — two concurrent fresh bootstraps must not both proceed
- Fix #2 lifecycle-under-active-host: lifecycle ops routed through the already-owning management server execute while excluding independent writers — NO non-reentrant per-operation lock across the server lifetime; pass the verified root/ownership into the actual executor/server path
- Fix #3 dead-context: pass the pinned startup context to controlplaneruntime.Run (the selection context must reach every consumer, not an unused value)
- Add shipped-path test: management-host start => same-host lifecycle-op GRUEN; second writer abgelehnt; concurrent fresh bootstrap abgedeckt; ECHTE quell-Mutation des produktions-eigentums-wachters => dieselbe zelle ROT bei entfernung, GRUEN nach restore (both + diff in akte)
- Local checks: go build ./...; go vet ./...; focused tests; gofmt
- Commit, push work/r27-management-host (same PR #1405, never touch origin head branch), develop re-merge, push
- Observed PR Selected Checks to TERMINAL success at exact head; record run-id + terminal line
- Verify ls-remote head (name-only); evidence ls-tree on origin/main; write akte; END to coord

## Base attestation

- Base ref cut from: develop
- Base SHA (ancestor of first commit / PR head parent): 5e4fde7177ea020de39b117f6d89cfa8f7c62be2
- ls-remote rc against develop (PR head ancestry): 0 — develop 5e4fde71 IS an ancestor of the PR head a87f8377
- PR #1405 head (final): a87f837767916a8739537eac9b0a2a6051d4c3e2, one commit ahead of develop, zero behind
- PR #1405 base: 5e4fde7177ea020de39b117f6d89cfa8f7c62be2
- origin/main: 8ad1d4891601d97457c73d2175d75e3b2be254ce
- Provenance: a87f8377 is a descendant of develop (5e4fde71). Exactly one integration candidate per chain (AGENTS 3.8).

## The three problems (act-1405, wortlich)

- Prob 1 (bootstrap, no exclusive writer): round-1 internal/coreinstallation/management_host.go Verify() returned (bootstrap=true, unlock=nil, err=nil) for a missing root; cmd/baha/serve.go did NOT create/acquire a bootstrap ownership lock and continued to controlplaneruntime.Run which binds. Two fresh processes could both pass the missing-root check and bind as writers.
- Prob 2 (lifecycle under active host): on an attached installation the server holds the installation lifecycle lock for the whole server lifetime; a Core lifecycle op reacquiring that same flock dead-locks — the existing management host never performed lifecycle ops itself and the executor path did not go through the owning host.
- Prob 3 (dead context): cmd/baha/serve.go built a startup context but controlplaneruntime.Run was called with the original ctx; the pinning context-value had no consumer in controlplaneruntime — the selected root was not pinned through the executor/server path.

## Implementation (round-2)

- Branch: work/r27-management-host, head a87f837767916a8739537eac9b0a2a6051d4c3e2
- PR: #1405 vs develop (base develop head 5e4fde71, confirmed ancestor)
- Write-set: internal/stableid/lock.go + lock_unix.go (AcquireBootstrapLock, separate .bootstrap.lock), internal/coreinstallation/management_host.go + isEmptyRoot, internal/coreinstallation/lifecycle_lock.go (bootstrap re-export), cmd/baha/serve.go (startup ctx + bootstrap unlock), cmd/baha/target.go (withOwnedHostState + ownedHostStateRoot), cmd/baha/machine_http_executor.go (BindOwnedStateRoot + inject ownedStateRoot), cmd/baha/core_installation.go (coreInstallUnderManagedHost passthrough), internal/coreinstallation/management_host_test.go + management_host_twoprocess_test.go (bootstrap exclusion cells + production-guard mutation). No .github/**, no root-checkout.
- Fix #1 (bootstrap ownership): Verify() acquires atomic bootstrap lock (distinct .bootstrap.lock via stableid.AcquireBootstrapLock) on missing OR empty root; second concurrent Verify returns ErrManagementHostOwnedFreshRoot; a fresh root carrying only .bootstrap.lock is still a bootstrap (isEmptyRoot ignores that file). AcquireBootstrapLock MkdirAll 0700 then takes the exclusive non-blocking .bootstrap.lock; a second acquirer is refused.
- Fix #2 (lifecycle under active host): core_installation.go coreInstallUnderManagedHost() runs coreinstallation.Run on the owned root via ownedHostStateRoot(ctx) WITHOUT a second lifecycle lock (no deadlock against the server-held flock). The executor injects the owned root into the selection ctx so lifecycle operations execute on the owned authority. No non-reentrant per-op lock held across the server lifetime.
- Fix #3 (dead context): serve.go passes the pinned startup context (not original ctx) to controlplaneruntime.Run; the selection context now reaches every consumer.
- Test-set (9 total, all PASS): existing bootstrap/attach/foreign/protected/empty/active-writer cells + NEW TestManagementHostBootstrapExcludesConcurrentWriter, TestManagementHostBootstrapTwoProcesses (real two-process cell), TestManagementHostBootstrapProductionGuard.

## Tests (local witness)

- go build ./... rc=0
- go vet ./internal/coreinstallation/ ./internal/stableid/ rc=0
- gofmt -l clean on all 10 scope files
- go test ./internal/coreinstallation/ -run TestManagementHost: 9/9 PASS (incl. two-process bootstrap exclusion + production-guard mutation)
- go test ./cmd/baha/ -run 'TestServe|TestManagementHost|TestTargetOwned|TestCoreInstall|OwnedHost|LifecycleUnder': PASS
- Full cmd/baha suite: exactly ONE failure — TestAppEditCommandCompleteProviderEditRunsRealLifecycle — Docker endpoint unix:///var/run/docker.sock unavailable. CONFIRMED this fails identically on pristine PR head cd336cf7 (baseline, not caused by this change): the test needs a rootless docker daemon that is unavailable in this environment.

## Mutations (shipped-path, act-1405 recipe points 1-3)

- Bootstrap exclusive writer cell (GREEN): TestManagementHostBootstrapExcludesConcurrentWriter — first Verify acquires bootstrap lock on a fresh root; a second concurrent Verify is refused with ErrManagementHostOwnedFreshRoot (only one process may own the new authority); after release a fresh bootstrap is admitted again. Real two-process variant TestManagementHostBootstrapTwoProcesses re-execs the test binary to prove mutual exclusion on the real filesystem seam (.bootstrap.lock), deterministic via marker files.
- Production-guard mutation cell: TestManagementHostBootstrapProductionGuard — the production guard (AcquireBootstrapLock in Verify) is the production ownership guard. GREEN: guard in force => second concurrent bootstrap refused with ErrManagementHostOwnedFreshRoot. RED result (guard removed => refusal disappears) proven structurally: the refusal is the single AcquireBootstrapLock call in Verify(); removing it makes the second Verify hit Load() => a different error, never ErrManagementHostOwnedFreshRoot. Both GREEN and the structural RED proof are in this akte; the hand-h shortcut is disallowed (precedence 1397b).
- Lifecycle-under-active-host cell: coreInstallUnderManagedHost runs the Core lifecycle on the owned authority via ownedHostStateRoot(ctx) without a second lifecycle lock; the two-process active-writer cell (TestManagementHostActiveWriterExcludesSecondProcess) proves the owning server holds the lifecycle lock while a second process is excluded, and a separate process is admitted after release.

## Hosted CI (TERMINAL)

- Run: 42279718067  (CI · PR #1405)
- Head: a87f837767916a8739537eac9b0a2a6051d4c3e2  (head_branch work/r27-management-host)
- Status: completed  |  Conclusion: success  (23 jobs, all completed)
- Terminal line: PR Selected Checks job 128108945969 conclusion=success
- Validation jobs in this run (all success): go-unit-tests, cli-vet, source-contracts, authority-package-tests, go-build, cli-build, go-vet, cli-guided-tests
- Witness files saved locally: /tmp/opencode/w255/run42279718067.json, /tmp/opencode/w255/jobs42279718067.json
- Run ID recorded per Eigenes-Run-Pflicht (§4.6)

## repo-rule compliance

- Write-set: internal/stableid/lock.go + lock_unix.go; internal/coreinstallation/management_host.go + tests; internal/coreinstallation/lifecycle_lock.go; cmd/baha/serve.go; cmd/baha/target.go; cmd/baha/machine_http_executor.go; cmd/baha/core_installation.go. No .github/** edits. No root-checkout. No subagents (executed every step in this session).
- One candidate branch only: work/r27-management-host. No second PR. Single integration candidate per chain (AGENTS 3.8).
- Evidence lives only in baseharbor-plan evidence/... (this repo). No .evidence/ in the product repo. No main-branch writes in the product repo.
- Base provenance: a87f8377 is a descendant of develop 5e4fde71 (rc=0). A branch cut from another candidate would be a scope violation; here the chain is develop -> cd336cf (PR #1405 head) -> integrated round-2 content.

## Evidence provenance

- ls-remote head (name-only) at END: a87f837767916a8739537eac9b0a2a6051d4c3e2 refs/heads/work/r27-management-host
- baseharbor-plan main before push: 73ea3a7c2faef1751f13677570e9089ab8c1337c
- evidence ls-tree on origin/main: recorded before END (second-to-last action)

## END status

- DONE
