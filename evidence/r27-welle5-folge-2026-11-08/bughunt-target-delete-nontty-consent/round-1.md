# Bug-Hunt BF-03 — target delete needs TTY; --yes must honor non-TTY consent (0427-164)

- Card/mission: t-20261108-bughunt-target-delete-nontty-consent.md / mission-164.md (0427-164)
- Shift: r27-welle5-folge-2026-11-08 / round-1
- Worker session: laptop (mission-164), no subagents (4.8)
- Planning repo verified (origin/main): c0a45630a95494584c2885d4f6bdda438834ecf7 (`git ls-remote origin main`)
- Base SHA (cut-from, ancestor of first commit): 9a93865a935624045e96a503da0a3a1c2f7d1559 (`develop` HEAD at worktree cut = origin/develop)
- Product remote develop HEAD: 9a93865a935624045e96a503da0a3a1c2f7d1559 (`git ls-remote origin develop`)
- Worktree: /tmp/opencode/mission-164-wt @ 9a93865a (develop), read-only source + edit worktree

## PLAN

- Read mission + akte hx3.md BF-03 + parent bug-hunt hx2/mission-157/#1486 round-1.md for shared semantics
- Attestate planning origin/main, product origin/develop, base SHA ancestor-of-first-commit
- Reproduce BF-03 with a failing Go test (non-TTY `target delete --yes` fails closed even though config-only)
- Fix: shared provider-impact consent honors `--yes`/non-TTY for the config-only delete with the SAME fail-closed semantics as interactive; interactive path unchanged; `--yes` never implies DeleteData; destructive still fails closed
- Update the two existing tests that encode the old `--yes` rejection
- CI-picked unit tests for the regression (identify the job/trigger that runs them)
- Local unit tests + `go vet` + build; document CI job/trigger in evidence
- Evidence to planning repo, publish to origin/main, cleanliness, post END

## Base attestation

- Product remote `origin develop` HEAD: `9a93865a935624045e96a503da0a3a1c2f7d1559` (`git ls-remote origin develop`)
- Product remote `origin main` HEAD: `aff1532c2f6c6782a8c13afad83245d1351815e7` (`git ls-remote origin main`)
- Planning repo `origin/main` (authoritative): `c0a45630a95494584c2885d4f6bdda438834ecf7` (`git ls-remote origin main`)
- Worktree cut from `develop` at `9a93865a935624045e96a503da0a3a1c2f7d1559` (`git log --oneline -1`). This SHA is an ancestor of the first commit; the branch is cut from develop HEAD, NOT from any other PR head (one integration candidate per chain).

## Finding

### BF-03 — target delete requires 2 interactive provider-impact confirmations; fails `impact-confirmation-required` on non-TTY even with --yes
- class: ux / daemm
- Source of the bug (current develop 9a93865a):
  - `cmd/baha/target.go:526` — `deleteTarget` REJECTS `--yes`/`-y` with a `cli.UsageError` ("target deletion does not accept --yes"). A generic `--yes` never reaches consent.
  - `cmd/baha/target_definition_change.go:39` — `changeTargetDefinition` only reads interactive acknowledgements when `!noInput(ctx) && readerIsTerminal(in)`. On non-TTY with `--yes` absent, `consent` stays nil and `ValidateProviderImpactScopeConsent` fails with `impact-confirmation-required`.
  - The plan scope for a config-only detach is `Complete=false` (unknown live consumers) with `Destructive=false`, `ConfirmationsRequired=2`. The two-stage gate (internal/application/provider_change_consent.go:30) fails whenever `!consent.First || (confirmations==2 && !consent.Second)`.
- POSITIVE: the action is config-only — detachment persists the original definition to the recovery file and retains all runtime/deployment owners (BF-07 hx3). No data is published; the remote-side-effect gate is empty for this operation.
- Resolution model (mirrors parent bug-hunt BF-02 / #1486): `--yes` on the local path grants the two consequence-acknowledgements for a non-destructive plan, but NEVER grants `DeleteData`; fail-closed is preserved at `ValidateProviderChangeConsent` (incomplete consent still rejected) and destructive plans still require explicit data consent. Interactive path unchanged (both stages still queried).

## repo-rule compliance

- Write-set confined to the target-delete / shared provider-impact consent path: `cmd/baha/target.go`, `cmd/baha/target_definition_change.go`, `cmd/baha/provider_change_confirmation.go` and the affected tests. No other lifecycle/apply/destroy files.
- No `.github/**` edits (Owner scope). No reruns / workflow_dispatch.
- Evidence written only in baseharbor-plan (repo mcpdev80/baseharbor-plan), not in any product repo. No `.evidence/` dir in a product repo. No main-branch writes in product repos.
- One integration candidate per chain: branch cut from develop HEAD 9a93865a (ancestor of first commit); no foreign commit carried on top.
- Subagents: none used (4.8).
- Host runners only; no runner infrastructure touched.

## CI coverage

- Regression unit tests run in `go test ./cmd/baha` (unit_tests job, ci.yml ~ line 121) and the full `go test ./...` (ci.yml ~ line 355). Trigger: PR marked ready and subsequent pushes (Owner coordinator dispatch); the lane did NOT trigger reruns/workflow_dispatch (Owner scope).
- Note: the exact CI run for this PR is not visible in the read-accessible window (token lacks actions:read); recorded as STATE. The Go unit tests are the durable, CI-picked evidence.

## END

END mission-164.md: <PENDING>
