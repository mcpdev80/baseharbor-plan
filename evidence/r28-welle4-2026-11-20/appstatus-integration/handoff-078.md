# handoff 0428-078 (r8 → owner)

Card `0428-078` / PR #1650 is handed off to the owner for final completion at the frozen head
`9add5e8a2122c5555c2403d5ea04073cfb2dc842` (PR #1650, single commit on develop `96f2ae11a25`).
Branch head == PR #1650 head (same SHA). Owner r8 review at that head = REQUEST CHANGES (akten
`r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r8.md`, `pr-sweep/review-1650-2026-11-20.md`).

## (a) DONE (what this worker considers settled, write-set on the frozen head)
- Verify-only identity-dashboard eligibility: `perses_status != nil && *perses_status == verified` gates both
  the local and the remote-target status faces; `not_configured` / `configured_unverified` fail closed.
- Verified-only decision extracted into `identityDashboardBackendEligible`, called by both returns (`app_status_result.go:165-177`, `:300-317`).
- Catalog `perses_identity_dashboards.go` (+ test + testdata) REMOVED — zero production consumers; `IdentitySelectionWitnessAt` stays (single consumer `app_status_result.go:343`).
- P3 target-isolation both directions: `TestIdentityWitnessIsolatedToConcreteTarget` goes RED when the target-filter is removed; foreign target, same sharing boundary → no positive witness.
- P5 two isolated mutations, distinct red outputs: witness `perses_selection.go:110 -> false` and predicate `verified-only -> configured_unverified` form.
- gofmt clean, `go build`/`go vet` clean; CI run `44737589479` `CI · PR #1650` success at this exact head; akte `round-8.md` published on origin/main (`3a712db6`).

## (b) Reviewer gaps still open (owner's r8 REQUEST CHANGES)
1. Positive status-JSON page not proven through the public `baha status --json` output.
2. Witness isolation by concrete target / tenant / state-root not yet evidenced.
3. No dashboard delivery path in the diff.

## (c) Two things a successor must NOT read differently
- `internal/capability/perses_selection.go` is LOCKED by owner directive — no lane edits.
- `internal/application/perses_runtime.go` is being written by #1684 (0428-083) — do not touch; the catalog delivery belongs there, sequenced after #1684.

Worker's account on this card is closed; the branch is NOT being rebased or re-pushed from here.
