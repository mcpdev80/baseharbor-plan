# 0428-065 export - round 3: operator-auth fixture for the 3 failing export tests + DE docs literal

ROLE: Worker. CARD: t-20261114-r28-cli2-app-export (0428-065). PR: #1625 (branch lane-0428-065-cli2-app-export, base develop, DRAFT=false).

## PLAN

1. Reproduce the three failing export tests locally with `CGO_ENABLED=0` + a worktree-local GOCACHE (the host `/tmp` is at 80%, cgo needs /tmp for gcc input). Fix exactly the three failing tests by wiring the develop operator-auth boundary with the proven operator fixture, WITHOUT weakening `internal/operatorauth/**`.
2. Run `bash scripts/documentation-audit.sh`; fix the one DE integrity finding (missing `baha app export` row in `docs/de/reference/cli-machine-coverage.md`).
3. Commit one identity, prove provenance (develop ancestor = JA, rev-list = 0), push to the same lane branch, prove remote via `git ls-remote`.
4. Watch the hosted CI run to terminal; record per-cell conclusion and the three test names from the per-job logs.
5. Extend this akte with the three test names, the precedent reference, the docs-audit line, the patch scope, the ls-remote line, and the per-cell table.

## repo-rule compliance

- Single integration candidate: working on lane-0428-065-cli2-app-export, PR #1625.
- No product change. The three export tests pass by supplying the operator-auth fixture the develop boundary demands; NO change to `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**`, `.github/**`, `scripts/**`. Auth stays fail-closed.
- Write-set respected: `cmd/baha/app_export_command_test.go` (tests + new helper), `docs/de/reference/cli-machine-coverage.md` (DE literal). Tabu untouched.
- Identity: dedicated worktree `0428-065-export-wt`, user.name 0428-065-export / user.email 0428-065@baseharbor.local.
- Sub-runs locally with `CGO_ENABLED=0` and a worktree-local GOCACHE only to prove the fix before push (the fix is verified in hosted PR-CI, the durable evidence).
- No subagents (AGENTS 4.8): all steps executed in this session.
- No `git stash`, no `git add -A` over foreign files.

## base attestation (git ls-remote, current base)

git ls-remote origin develop:
e6c199e7b7dd7d076a776d11c3ba16f25e59c254  refs/heads/develop

merge-base --is-ancestor origin/develop HEAD: JA
rev-list --count HEAD..origin/develop: 0

git diff origin/develop..HEAD --name-only:
cmd/baha/app_export.go
cmd/baha/app_export_command_test.go
cmd/baha/commands.go
cmd/baha/machine_coverage.go
docs/cli/command-index.md
docs/de/cli/command-index.md
docs/de/reference/cli-machine-coverage.md
docs/reference/cli-machine-coverage.md

Author identities in e6c199e7b..HEAD: 0428-065-export (my commit ce0c5051e sits on top of my own 4d14e30f8 / 7e7bcecc8 / ce263c965 range). The four other files are the feature build carried onto develop; this round only adds the test fixture and the DE literal, no product diff.

## the three failing tests (measured failure on develop base)

Baseline run before the fixture, all three fail with:
"operator authentication needs interactive setup but input is not a terminal"
(the develop managed-environment operator-auth boundary, `ensureOperatorAuthForBoundary` in `cmd/baha/operator_auth_boundary.go:56`, requires a verified principal or a verified local runtime engine; the fixture `dev` env has neither).

- TestAppExportCommandPathAssemblesProductionWiring (routed to PR · Go unit · cli-0)
- TestAppExportFailsClosedWithoutSelection (routed to PR · Go unit · cli-2)
- TestAppExportManagedSecretWithoutOperatorFailsClosed (routed to PR · Go unit · cli-3)

## the fix (does NOT weaken auth)

New helper `appExportFixtureContext(transport string) context.Context` in `cmd/baha/app_export_command_test.go`:
- `operatorauth.WithEnforcement`, a `WithVerifiedPrincipal` (IssuerVerified=true) test operator, `operatorauth.WithMembershipProvider(&readGrantingMembershipProvider{})` (same bounded provider already in the package, rejects unverified principals).
- This is the exact operator-auth fixture pattern the 0428-142 status-witness cell builds (commit 77d0415ef: `persesMatrixCommandContext` in `cmd/baha/app_status_result_test.go` / `perses_lifecycle_transport_test.go`) - studied read-only, applied to the export fixture.
- Tests 1 and 2 (positive command-path / empty-selection cases) use `appExportFixtureContext("cli")` so the production command tree reaches the renderer instead of the "interactive setup" boundary error.

Test 3 stays an honest negative: no verified operator principal -> the export fails closed at the managed-environment operator-auth boundary (resolved during `resolveApplicationEnvironment`) BEFORE it reaches the secrets/openbao human-authorization reveal or the secret backend. The manifest gains `services:\n  secrets: true` so the secret surface is declared; the assertion proves the command fails closed on an empty-selection / unverified-operator export rather than selecting sources. The reveal seam (`authorizeHumanReveal` -> `RequireHumanOperator` at `internal/operatorauth/authorization.go:332`) still requires an authenticated BaseHarbor operator; it is never bypassed.

No file under `internal/operatorauth/**` changed; `internal/serviceaccess/**`, `internal/identityprovider/**`, `.github/**`, `scripts/**` untouched.

## documentation-audit

`bash scripts/documentation-audit.sh` before the fix:
`reference/cli-machine-coverage.md: literal lost: baha app export`
`DE technical integrity: FAIL (1 findings across 172 paired pages)`

Cause: the EN row for `baha app export` (in `docs/reference/cli-machine-coverage.md`) had no DE equivalent, so the EN->DE inline-literal gate lost the `baha app export` literal. Fix: insert the DE row after the `baha app exec` row in `docs/de/reference/cli-machine-coverage.md` (mirroring the EN row: `Darstellung`, `no machine tool`, fails closed on empty selection, ciphertext opens only with the export password, managed-secret sources require the human-authorization reveal seam). After the row the audit passes:
```
Documentation audit
Structure          PASS
Human-doc size     PASS
No legacy stubs    PASS
German scope       PASS
Internal evidence  PASS
ADR identifiers    PASS
Governance         PASS
Runtime docs       PASS
Task/domain information architecture PASS
Podman release CI  PASS
Brand identity      PASS
```
`bash scripts/source-readability-audit.sh`: PASS (Go file size <= 800 or no worse than baseline; function span <= 200; regression ratchet clean).

## push provenance

git remote -v (REMOTE GUARD): origin https://github.com/mcpdev80/baseharbor.git (real GitHub remote used).

git commit (one identity, only the two changed files):
ce0c5051e fix(0428-065 r6): operator-auth fixture for export tests + DE docs literal
  2 files changed, 40 insertions(+), 10 deletions(-)

git push:
git push origin HEAD:refs/heads/lane-0428-065-cli2-app-export
=> ce263c965..ce0c5051e HEAD -> lane-0428-065-cli2-app-export

git ls-remote AFTER push:
ce0c5051eb41ef36c5fc8e65221da64473ad02b7  refs/heads/lane-0428-065-cli2-app-export
ce0c5051eb41ef36c5fc8e65221da64473ad02b7  refs/pull/1625/head

gh pr view 1625 --json state,isDraft,baseRefName,headRefName:
{"baseRefName":"develop","headRefName":"lane-0428-065-cli2-app-export","isDraft":false,"state":"OPEN"}

## TEST RUN: hosted CI (own run to terminal)

Run #7090 (GitHub run databaseId 44937984440), workflow "CI · PR #1625", event pull_request, headSha ce0c5051e, status COMPLETED success, 4m11s, started 2026-11-21T18:53:40Z.

Per-cell conclusion:
- PR · Native gate plan: success
- Workflow policy: success
- PR · Trusted Plan: success
- PR · Source format: success
- Targeted · Workstation onboarding: skipped
- PR · Exact full Pre-Release: skipped
- Release Source Preflight: skipped
- Targeted HA · docker: skipped
- Targeted HA · podman: skipped
- PR · Main release Go: skipped
- PR · Main release source: skipped
- PR · Draft source and routing: skipped
- validate: skipped
- PR · Draft Go: skipped
- PR · Focused Python: success
- PR · Go unit · cli-0: success (log: "PASS cli-0: 458 passed / 13 intentionally skipped / 471 discovered")
- PR · Go unit · cli-2: success (log: "PASS cli-2: 450 passed / 20 intentionally skipped / 470 discovered")
- PR · Go unit · cli-3: success (log: "PASS cli-3: 425 passed / 16 intentionally skipped / 441 discovered")
- PR · Go unit · owner: success
- PR · Go unit · cli-1: success
- PR · Validation · documentation-audit: success
- PR · Validation · mkdocs-en-strict: success
- PR · Validation · pages-candidate-build: success
- PR · Validation · go-build: success
- PR · Validation · cli-gofmt: success
- PR · Validation · wizard-registration-tests: success
- PR · Go unit · packages: success
- PR · Validation · mkdocs-de-strict: success
- PR · Validation · go-vet: success
- PR · Selected Checks: success

The three fixed tests are routed by name-hash into the Go unit shards:
- TestAppExportCommandPathAssemblesProductionWiring -> cli-0 (passed)
- TestAppExportFailsClosedWithoutSelection -> cli-2 (passed)
- TestAppExportManagedSecretWithoutOperatorFailsClosed -> cli-3 (passed)
The previous run on head ce263c965 (44934081753) failed at these three cells; this run on ce0c5051e is green.

## cleanliness

- docker ps -a --filter name=bh- before: (no containers started this shift; git worktree only)
- docker ps -a --filter name=bh- after: (no containers started this shift; git worktree only)
- git worktree list after: 0428-065-export-wt (detached HEAD ce0c5051e, pushed to lane branch; .gocache build cache removed from worktree)
