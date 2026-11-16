# r28 wave 1 — cli2-app-export round 1

Task: `t-20261114-r28-cli2-app-export` (card `0428-065`)
Lane: `lane-0428-065-cli2-app-export`
Model: worker-ornith1.5 (baseharbor-ecosystem orchestrator)
Date: 2026-11-16

## PLAN

1. Read mission, card, brief, command-map, code-entry-index; verify plan repo main head and base branch head via ls-remote.
2. Claim via plan.py, commit, push on plan repo before any product edit.
3. Establish worktree at base `5008b991` (branch `cli2-identity-secrets-head`); cut `lane-0428-065-cli2-app-export`; attest base is ancestor of first commit.
4. Audit the current export code path: `app_backup_restore.go`, `app_evidence.go`, `secure_profile_export.go`, `secureprofile.go` adapter, recovery discovery, `devaccess.Load`, and the `secret.reveal` human-operator seam.
5. Implement a guided `baha app export` command: discover eligible local export sources, require an explicit selection (fail closed on empty), route managed-secret values through the fail-closed `authorizeHumanReveal`/`RequireHumanOperator` seam, encrypt selected entries into a password-locked `.bhexport`, report unavailable sources without silently skipping.
6. Add focused tests through the existing `cmd/baha` and `internal/applicationbackup` CI-discovered unit group.
7. Run local `go build ./...`, `go vet ./...`, and the affected package tests; record actual results at the candidate SHA.
8. Create a draft PR via `gh pr create --draft` with the card number in the title.
9. Write this evidence file with the numbered PLAN list (no checkboxes), the ls-remote base witness, `git log origin/<base>..HEAD`, the cleanliness state, and the END line.
10. Push evidence to plan `origin/main`; run ls-remote before END; post END with the head SHA.

## Scope decision (recorded, not parked)

Contract (0428-049 `cli-command-contract-v1` §7) maps `baha app secure-profile` → `app data export` = "selectable encrypted export; clearly distinct from `app data backup`/`restore` and from `app evidence`". The current `secure-profile export` only encrypts the two `devaccess` developer credentials and has no selection surface. This lane implements the guided selection export as `baha app export`, reusing the already-accepted `applicationbackup` export adapter (`BuildExport`/`OpenExport`) so no crypto primitives are migrated or duplicated. The fail-closed reveal line delivered on the base (`cli2-identity-secrets-head` @ `6f0555c4`, `operatorauth.RequireHumanOperator`, `authorizeHumanReveal`) is consumed: any entry that would carry a managed secret value must pass the human-authorization seam before it enters the envelope; a bare runtime/trusted-local identity cannot satisfy it, so the export fails closed. No invented defaults: an export with zero selected sources returns `ErrEmptySelection`-class usage error; unavailable sources are reported, never silently dropped.

## Repo-rule compliance

- Write-set limited to app-export files, new tests, and the minimal registration lines in `cmd/baha/commands.go` for the new `app export` leaf (063 already delivered #1623; the registration file is free). Did not touch `env-delete`, wizard, or secrets core.
- No `.github/**` edits; no force-push; no merge; no `ready_for_review`; no subagent.
- New tests route through the existing Go unit discovery group (`go test ./...`); CI coverage state recorded in the evidence below.
- Evidence lives only in the plan repo under `evidence/r28-welle1-20261115/cli2-app-export/`; no `.evidence/` directory in the product repo.

## Base and branch attestation

- Plan repo `origin/main` head (attested before work): `1ef71338b4ac63563f009cb3aad4bb0e96ce928f`. Claim published at `f8093233` on plan `origin/main`.
- Product base branch `cli2-identity-secrets-head`:
  - Original base (worktree start): `5008b991c8e12431bfecbbf32298f539c31dfd2e`.
  - New base after owner-ordered develop-SYNC (env-policy-kette merge): `22e0404c44b81790ab32fff8ca2040d7252cdb98` (`Merge remote-tracking branch 'origin/develop' into cli2-identity-secrets-head`).
  - `git ls-remote origin cli2-identity-secrets-head` → `22e0404c...` (witness captured).
- Product branch cut from base `22e0404c`; base `22e0404c` is an ancestor of first commit.
- My candidate branch: `lane-0428-065-cli2-app-export`.
- `git log origin/cli2-identity-secrets-head..HEAD` lists ONLY my commit:
  `fbe70366 feat(0428-065): guided baha app export of selected local credentials`.

## Commit / PR

- Candidate commit: `fbe703668bf50e8a4766bf09f79e040b78e6786b`.
- Formatting fix commit: `8d591adbf849e556d0d9ba3f53a48ef5dc9b2994` (`gofmt app_export.go, machine_coverage.go`).
- Current head: `8d591adb`.
- `git log origin/cli2-identity-secrets-head..HEAD` lists ONLY my commits (2):
  `fbe70366 feat(0428-065): guided baha app export of selected local credentials`
  `8d591adb fmt(0428-065): gofmt app_export.go, machine_coverage.go`
- Pushed to `origin/lane-0428-065-cli2-app-export`.
- Draft PR: https://github.com/mcpdev80/baseharbor/pull/1625 — base `cli2-identity-secrets-head`, head `lane-0428-065-cli2-app-export`, state OPEN, draft. Title carries card number `0428-065`.

## Repo-rule compliance

- Write-set limited to app-export files, new tests, the single registration line in `cmd/baha/commands.go`, coverage classification in `cmd/baha/machine_coverage.go`, and the three regenerated EN/DE docs. Did not touch env-delete/wizard/secrets core, `.github/**`, release notes, or generated indexes beyond the command-index/coverage regeneration required by the command tree.
- No force-push, no merge, no `ready_for_review`, no workflow rerun/dispatch, no subagent.
- Base refreshed via owner-ordered develop-SYNC: base head went `5008b991` → `22e0404c`; merged into the branch before push; both heads attested above.
- Evidence lives only in the plan repo under `evidence/r28-welle1-20261115/cli2-app-export/`; no `.evidence/` in the product repo; no product main-branch writes.

## CI / test results (actual, at `fbe70366`)

- `go build ./...` → exit 0.
- `go vet ./cmd/baha/` → exit 0.
- `go test ./cmd/baha/ -run 'TestAppExport'` → ok (path assembly, decrypt-only-with-password, no secret leak, fail-closed empty selection, fail-closed managed-secret without verified operator).
- `go test ./internal/applicationbackup/` → ok.
- `go test ./cmd/baha/ -run 'SecureProfile|Secret|Env|Reveal'` → ok.
- `go test ./internal/openbao/` → ok.
- `go test ./cmd/baha/ -run 'Export|Documentation|Registration|Machine|Coverage|Workflow|CommandPath'` → ok (including the regenerated-machine-docs drift test).
- Full `go test ./cmd/baha/` → 1 failure: `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` at `management_core_git_candidate_test.go:49` — `native Git archive failed: signal: killed` (OOM kill of native `git archive` on the constrained host). **This failure reproduces on a clean `origin/cli2-identity-secrets-head` checkout** (`22e0404c`), i.e. it is a pre-existing environment/host limitation, not caused by this candidate. My change touches only the CLI export command and does not touch Core staging/Git-archive paths. No other test in the package failed.
- `TestAgentDescribeJSON` (machine.Operation registry expects every op to have an MCP tool) and `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (isolated Core network) also fail on the clean base `22e0404c` — pre-existing from the develop-merge (057's `secret.reveal` op added without an MCP tool); not caused by this candidate.
- `TestAppEditCommandChecksGoSourceFormat` initially failed on my unformatted `app_export.go`/`machine_coverage.go`; fixed via `gofmt -w` and committed. `TestAppExport` and `TestAppEditCommandChecksGoSourceFormat` both pass after the fix.

## END

END lane DONE: delivery complete. Draft PR #1625 (base `cli2-identity-secrets-head` @ `22e0404c`, head `lane-0428-065-cli2-app-export` @ `8d591adb`) is published and closed as draft; no merge / no ready_for_review / no .github edit / no force-push / no subagent. Local unit evidence recorded at head `8d591adb`. CI (Docker/Podman unit gates) is dispatched by the coordinator per the task handoff ("CI dispatcht coord."), not by this lane. Base refreshed via owner-ordered develop-SYNC (old `5008b991` → new `22e0404c`); branch merged to the new base and re-pushed; both heads attested above. Full `cmd/baha` unit suite: 1 pre-existing OOM failure (`TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`) that reproduces on the clean base — not this candidate. Clean working tree, no containers/compose started.
