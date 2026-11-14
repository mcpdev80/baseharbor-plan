# 0428-052 uid-target — round 1 evidence

**Card:** `t-20261114-r28-cli2-uid-target` (0428-052) · **Release:** v0.4.28
**Lane:** `lane-0428-uid-target` · **Owner:** lane-0428-uid-target
**Base (verified):** `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (`origin/develop`)
**Candidate SHA (pushed, origin/HEAD):** `ebeafa56a2d14d962603cbc649e4764628104417` (`git ls-remote origin lane-0428-uid-target` witness)
**Draft PR:** [#1580](https://github.com/mcpdev80/baseharbor/pull/1580) — base `develop`, head `lane-0428-uid-target`, DRAFT, OPEN
**Planning repo root (verified):** `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (origin/main `24ef397d`)
**Evidence path (only in planning repo):** `evidence/r28-welle1-2026-11-14/cli2-uid-target/round-1.md` — present on origin/main (verified via `git show origin/main:evidence/...`)

## Plan checklist

- Read task card + owner contract (cli-command-contract-v1.md) + brief + command-map + code-entry-index — DONE
- Claim task (active) + verify remote base 0e9ccb582 + cut lane branch — DONE
- Map current target identity (tenant-id, ResolvedTarget, config schema, recovery) — DONE
- Design + implement stable target UID resolution + safe migration — DONE round 1
- Dedicated tests (unit + real-CLI-entry-point) — DONE
- gofmt + go vet + targeted test run — DONE
- Push candidate branch + open draft PR (MERGE-FROST: draft only) — pending this round

## Scope decision (Owner 2026-11-14)

Owner clarified the exact destination:

- The stable Target UID is a **Core-side uid**. It is NOT the ownership binding: `TenantID`/ownership path stays unchanged in meaning (card: "ohne laufzeit-eigentumschaft zu aendern").
- Cross-ref contract §6: the three distinct roles must NOT be conflated — Core-side uid, workstation-alias, deployment-ids. Verified the UID is distinct from all three.
- The **name stays addressable**; the name→UID migration is **idempotent + collision-fail-closed**, and produces **no data movement on disk** (directories stay keyed by name; only resolution gains the UID).
- If any code bound the UID to ownership: HOLD + QUESTION with file:line. (None found — UID threads only through `ResolvedTarget.UID` and the config field; ownership stays `TenantID`.)

## What was implemented (round 1)

- `internal/deployment/target_id.go` (new): `NewTargetUID`, `ValidateTargetUID`, `MigrateTargetUID` (idempotent, fails-closed on malformed), `ApplyTargetUID`, `ResolveTargetUIDs` (uniqueness-enforcing), `CheckTargetUIDCollision`, `validateTargetUIDUniqueness`.
- `internal/deployment/target.go`: added `TargetDefinition.TargetUID` (yaml `target-uid`, json `target_uid`); `ResolvedTarget.UID`; `ResolveTarget` threads UID; `Validate` checks UID format + cross-Target uniqueness.
- `internal/deployment/config_target_recovery.go`: recovery carries the UID (recovery struct already embeds `TargetDefinition`).
- `cmd/baha/target_mutation.go`: `createTargetDefinition` generates/validates a fresh UID, rejects a collision against another Target's UID, and persists it — `TenantID` left as the ownership path untouched.
- `cmd/baha/target.go`: `target list -o json` exposes `uid`; `targetListItem.UID`.
- `internal/deployment/target_id_test.go` (new, 8 tests, all pass): idempotent migration, explicit-UID preserved, malformed fails closed, collision fail-closed, collision-by-name, UID threads through ResolveTarget, owner TenantID not conflated, config validate accept/reject, recovery preserves UID.
- `cmd/baha/target_uid_cli_test.go` (new, 3 tests, all pass): real CLI entry point persists UID, idempotent retry, collision rejected by CLI with no partial definition left behind.

## Verification (candidate SHA = branch HEAD, unpushed)

- `gofmt -l cmd internal spec contracts` — CLEAN (formatted all touched files).
- `go vet ./internal/deployment/... ./cmd/baha/` — PASS.
- `go test ./internal/deployment/...` — PASS (0.785s).
- `go test ./internal/coreinstallation/...` — PASS (0.433s).
- `go test ./cmd/baha/ -run 'Target|UID|Uid|uid'` — PASS (107.6s, EXIT=0).
- `go test ./cmd/baha/ -run 'TestCreateTarget'` — PASS.
- End-to-end manual run: `baha target create docker-prod ...` persists `target-uid` (UUIDv4); `target list -o json` exposes `uid`; read round is idempotent (UID unchanged across `target list` invocations).

## CI routing (no .github/** change needed)

- New tests live in `internal/deployment/` and `cmd/baha/`, both auto-run by CI job "release-source tests" (`.github/workflows/ci.yml:122` `go test ./internal/... ./spec/...` and `:123` `go test ./cmd/baha`). No workflow edit requested — `.github/**` is Owner scope.

## MERGE-FROST compliance

- No merge on develop; PR to be opened DRAFT (base develop). No release/tag.

## Push + PR witnesses (END)

- `git ls-remote origin lane-0428-uid-target` -> `ebeafa56a2d14d962603cbc649e4764628104417` (matches local HEAD).
- `git merge-base --is-ancestor 0e9ccb582 HEAD` -> PASS; `git log origin/develop..HEAD` -> only `ebeafa56a feat(r28): stable target UID without runtime-ownership change (0428-052)`.
- `git diff --name-only 0e9ccb582 HEAD` -> 7 files, all this lane's slice (target.go, target_mutation.go, target_uid_cli_test.go, config_target_recovery.go, target.go, target_id.go, target_id_test.go).
- Draft PR #1580 OPEN, base develop, head lane-0428-uid-target, isDraft=true.
- Evidence on origin/main: `git show origin/main:evidence/r28-welle1-2026-11-14/cli2-uid-target/round-1.md` -> present.

## END status

ROUND-1 DONE: implementation + dedicated tests + local verification complete. Branch `lane-0428-uid-target` pushed to origin (SHA ebeafa56a2); draft PR #1580 opened (base develop). Ready for CODEX-REVIEW against the contract.
