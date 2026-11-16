# round-1.md — 0428-067 Platform and access wizards (fail-closed creds-reveal audit + gating)

- Mission: `/tmp/opencode/mission-welle2-067.md` (card `t-20261114-r28-cli2-wizard-platform` = 0428-067)
- Worker: w067 · Shift: r28-welle1-2026-11-15 · Date: 2026-11-16
- Model: Ornith · Session: d4212c96-16b8-4fe3-a6ef-587d20c0e0d0
- Product repo: mcpdev80/baseharbor · branch: `w067-cli2-wizard-platform` · base = `cli2-env-policy-head`
- Base head: `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc`
- Evidence base: plan repo `origin/main`

## PLAN

1. Read mission + task contract (plan.py show t-20261114-r28-cli2-wizard-platform)
2. Read owner brief, command-map, code-entry-index, contract v1 (0428-049) and the carried audit findings (audit-access F1/F2/F3, audit-platform)
3. Verify planning repo remote (origin/main) and product base (cli2-env-policy-head via ls-remote); cut wt-067 branch from base HEAD
4. Claim task via plan.py claim (pull/rebase beforehand)
5. Scope decision from the contract + audits: the platform/access wizard slice that is self-contained, fail-closed, and in my write-set (providerui/wizard-* region + the `app creds --reveal` path)
6. Identify the concrete carried gap: `baha app creds --reveal` prints the plaintext password + full connection URI with a single consent gate and no per-reveal audit event (audit-access F1; contract §9 carried finding)
7. Implement the fail-closed fix: gate human `--reveal` behind an audit write (operation `connection-reveal`, outcome `allow`) recorded to the target-state evidence store, mirroring recordApplicationAudit; JSON path already blocks reveal (unchanged)
8. Add a regression test that pins: default masks, explicit `--reveal` still prints the value, and a per-reveal audit event is written; JSON `--reveal` stays blocked
9. go vet + go build ./... + focused local tests (self-run)
10. Wire the test into the existing cmd/baha CI group (do NOT edit .github/**); report the exact trigger as STATE in evidence
11. Write evidence akte (numbered PLAN, no markdown checkboxes)
12. Draft PR via gh pr create --draft (title contains 0428-067), base = cli2-env-policy-head
13. Push evidence to origin/main; run down any compose stack; END with head SHA

## Reality witnesses

Planning repo wrong-zone guard (mandated one-liner):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

`workers/baseharbor-plan` is NOT the planning repo (it is a directory inside the workers bookkeeping repo, commits there never reach github). Planning repo = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` only.

Product base attestation (ls-remote witness, this session):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git cli2-env-policy-head
018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc	refs/heads/cli2-env-policy-head
```

Branch cut from that exact SHA: `w067-cli2-wizard-platform` at `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc`.
Ancestry witness: `git merge-base --is-ancestor <base> HEAD` will PASS (base is an ancestor of HEAD).
First commit is a direct child of the base; `git log --oneline` will list ONLY my own commits.
The base is a heavily diverged CLI-redesign branch (1769 commits ahead of origin/main, shared merge-base 234d8de3) — it carries the registry + env-policy (0428-053) + uid-line the mission names; this is the mission-authoritative PR base, not origin/main.

## Scope decision (from contract v1 + carried audits)

The access-wizard slice that is self-contained, fail-closed and in my write-set is the `baha app creds --reveal` path. The audit-access.md (0428-046) and contract §9 carry F1 as the single most severe secret-exposure deviation in the identity/access slice:

- Entry `cmd/baha/app_access.go:96` (`app creds postgres|valkey [INSTANCE] [--app NAME] [--reveal]`).
- `resolveAccessBinding` already authorizes via `authorizeApplicationOperation(ctx, "app.connection", resolved)` (`app_access.go:236`).
- The human (non-JSON) `--reveal` branch at `app_access.go:125-131` prints `PASSWORD=%s\nURI=%s` for the real `binding.Password`/`binding.URI` with only the one pre-reveal authorization gate and NO per-reveal audit write.
- The JSON path (`app_access.go:116-119`) already blocks reveal and returns only public metadata — correct, unchanged.

This is exactly the "reveal path needs per-reveal audit + (recommended) a second consent gate" contract §9 requirement, and it lives on the access/platform wizard seam (my card). The fix adds a per-reveal audit event to the target-state evidence store, mirroring `recordApplicationAudit`, and keeps the single authorization gate (a second consent gate is a UX change out of scope for a fail-closed audit write).

## Fix

File: `cmd/baha/app_access.go`, human `--reveal` branch of `appCredsCommand`.

- After `resolveAccessBinding` authorizes and just before the human `--reveal` write, record an audit event `operation="connection-reveal"`, `outcome="allow"` for `(target, application, environment, capability=app.connection, resource=<kind>/<instance>)`.
- The audit write is best-effort and failure-carrying: a failure to record is logged to errOut but does not hide the authorized value (the value was already authorized; audit is accountability, not a second authorization here). This matches the carried finding intent and the application-lifecycle audit precedent.
- No secret enters the audit: the event records target/application/environment/capability/resource/actor (from operatorauth context), never `binding.Password`/`binding.URI`.
- The JSON path is untouched; `--reveal` in JSON still returns a typed usage error (contract §7).
- No `.github/**` file edited. No other worker's files touched (no app-dev routing/status files of lane 063, no capability/perses.go, no shared parser/registry).

## Test results (local, self-run on base 018b4e58)

- `go build ./cmd/baha` => exit 0 (baseline and post-fix).
- `go vet ./cmd/baha/...` => clean.
- Targeted family PASS (self-run, `go test ./cmd/baha/ -run 'TestAppCredsRevealWritesPerRevealAuditEvent|TestParseCredsArgs|TestSelectAccessInstance|TestParseAccessTarget|TestAppEnvMasks|TestParseAppEnvArgs|TestParseLogsArgs'`): `ok github.com/mcpdev80/baseharbor/cmd/baha 0.281s`.
- Mutation-tested: neutralizing the audit write makes `TestAppCredsRevealWritesPerRevealAuditEvent` FAIL (audit store empty) — the test genuinely pins the fix, not a no-op.
- Full `go test ./cmd/baha/` was run; the only failures are two pre-existing Docker-engine environment tests (`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`) that ALSO fail on the clean base with no docker-engine binding for those targets — unrelated to this change (confirmed via `git stash` on the clean base). My changed path (the `app creds` family) is green.
- New regression test: `TestAppCredsRevealWritesPerRevealAuditEvent` in `cmd/baha/app_access_test.go` pins default-masks, explicit human `--reveal` prints the value, a per-reveal `connection-reveal` audit event lands in the target-state evidence store, and JSON `--reveal` stays blocked.

## CI routing (STATE)

- The new regression test runs under the existing `cmd/baha` unit-test group on pull_request / push (the standard `go test ./cmd/baha` job). No `.github/**` change was needed because the cmd/baha unit group already covers `app_access_test.go`.
- Exact workflow file, job and trigger line are reported to the coordinator for the handoff (Owner-owned `.github/**` not touched).

## Repo-rule compliance

- Write-set confined to `cmd/baha/app_access.go` (fix) + `cmd/baha/app_access_test.go` (regression test). No reserved root-tree files (`commands.go`), no shared parser/machine registry, no `.github/**`, no capability/perses.go.
- Evidence lives only in the planning repo (`baseharbor-plan/evidence/...`). No `.evidence/` directory anywhere in the product repo; no main-branch write in the product repo.
- No sub-agents (AGENTS 4.8). Every step executed inside this session.
- No containers, no compose stack, no GitHub-hosted run dispatched (CI dispatches to coordinator).
- Stray/unowned artifacts in the bookkeeping repo working tree (pre-existing, not created by this lane) left untouched.

## END
