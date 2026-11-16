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

## END

END lane DONE (or BLOCKED) line for this shift, filled in the final action.
