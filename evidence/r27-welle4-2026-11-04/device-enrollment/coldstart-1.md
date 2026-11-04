# w146-enroll-r5 — R27 device enrollment, ROUND 5 (work evidence)

Lane: `workers/w146-enroll-r5` · Coord: `f49a3303` · Card: `t-20261018-r27-device-enrollment`
Repo: baseharbor · Branch (candidate): `work/w96-production-wiring-f8ef4255` · PR #1371 · head `f4ec625f8014`
Review: `review-1371c.md` = REJECT, three findings R1/R2/R3 (read fully before coding).

## PLAN

- Read mission + review-1371c fully before coding
- R1 fix station policy resolver for first bootstrap + coldstart tests (i-v)
- R2 rollback test reads artifacts from chosen stage .down.sql + 0008/0009 swap mutation probe
- R3 remove AGENTS.md from product diff
- Local checks: go test ./internal/database, workstationenrollment, cmd/baha, build, vet, gofmt
- Hosted runs to terminal (Run-ID + status, self-run)
- Evidence: name-only diff, log line, ls-remote, merge-base; write coldstart-1.md
- Post END to f49a3303
- Update PR with provenance

## Mission scope summary

- R1 (coldstart): first workstation bootstrap dead-cycles. Policy resolver only authorizes when a
  row already exists in `workstation_enrollment_registry`, but that row is written only after a
  successful enrollment. Fix per existing schema: resolver must accept BOTH an existing registry row
  AND a valid, not-yet-consumed assignment in `workstation_enrollment_grants` (the one-use bootstrap
  authorization, per migration 0009). Keep fail-closed for unassigned/foreign; membership from verified
  identity stays mandatory. Prove cases (i)-(v). If grant source (b) is unworkable: STOP + report file:line.
- R2 (rollback artifacts): rollback test picks latest stage but hard-codes workstation-table assertions.
  Read owned artifacts from the chosen stage's `.down.sql` (0009 => the two workstation tables). Prove
  exact set missing after rollback, earlier stages intact. Swap 0008/0009 prefixes => test must stay green.
- R3 (AGENTS.md): remove the lane-identity AGENTS.md from the product diff (`git checkout develop -- AGENTS.md`).
  If a second non-field path appears: STOP + report.

## Evidence (filled during work)

### name-only diff (git diff origin/develop...HEAD)

- (to be recorded; must contain ONLY enrollment/database/wiring field, NO AGENTS.md)

### log line (git log --oneline origin/develop..HEAD)

- (to be recorded; must list ONLY my own commits)

### ls-remote

- (to be recorded; must equal candidate head verbatim)

### merge-base

- (to be recorded; `git merge-base --is-ancestor origin/develop HEAD` => rc=0)

## END

- lane DONE / BLOCKED line (see below)
