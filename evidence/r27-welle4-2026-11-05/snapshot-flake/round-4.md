# Snapshot change-during-read guard — defense in depth (w189, round-4)

Task: `t-20261105-r27-snapshot-change-guard-deterministic` (r27 wave 4).
Lane: `w189` (Worker, model Ornith). Coordinator: `f49a3303`.
Branch: `work/r27-snapshot-flake` (PR #1387), head `d21badc6f4a202b5ff81022e0039adc095e079e3`.
Evidence: this file + `scripts/mutant-proof-r4.txt`.

## Base attestation (Owner requirement)

- Round-3 head (pre-this-round): `e2d87906a5103db132e0d86e935387680426245b`.
- Develop merged: `origin/develop` = `10e8d646f0136c62fde0f7b84968a42ae572ba68`.
- Attestation: `git merge-base --is-ancestor e2d87906 HEAD` → rc=0 (round-3 head is an ancestor of my head).
- Attestation: `git merge-base --is-ancestor 10e8d646 HEAD` → rc=0 (develop is an ancestor of my head).
- FINAL ls-remote witness: `work/r27-snapshot-flake` -> `d21badc6f4a202b5ff81022e0039adc095e079e3` (== my head).
- My code commits stack exactly on top of `e2d87906`: `03dbff5e` (barrier fix + final sweep) + `c87c5fb1` (regression test) + `d21badc6` (deterministic regression), with one trigger commit `33ae6df9` to start the hosted gate. All four commits are mine; no foreign candidate carried.

## Goal (in product language)

The source-snapshot capture must prove it saw a change during the read AND defend the baseline paths after the walk. Round-3 rebuilt the guard on EREIGNIS semantics (a per-file identity barrier inside the walk) but the per-file comparison was dead code (`entry.Info()` returns the walk's own mtime, which can never diverge), so it flaked, and the prior post-walk final sweep was gone. Review-1387c REJECTed that. Round-4: fix the barrier to a real `os.Lstat` mid-walk re-stat (deterministic witness), restore the post-walk final baseline-path verification as a second independent layer, and pin the late-mutation gap with a regression.

## The change (round-4 only, write-set = 2 card files)

- `internal/development/source_snapshot.go`:
  - Layer 1 (event-barrier) FIX: the per-file barrier now re-stats each path after reading it with a fresh `os.Lstat` (not `entry.Info()`, which returns the walk's own mtime and could never diverge). This makes the deterministic EREIGNIS witness actually fire on a real mid-walk divergence — the root cause of the round-3 flake.
  - Layer 2 (final baseline-path verification): `verifyFinalBaseline` re-checks every recorded baseline path after the walk and aborts on any divergence (defense in depth: a writer modifying an already-visited path while later files are captured). Extracted into its own function so `CaptureSource` stays within the readability function-span limit (was 217 → 201 lines).
- `internal/development/source_snapshot_test.go`:
  - `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation`: mutates the already-visited `first.bin` while the filler files (`filler/00.dat` … `filler/39.dat`, lexical order after `first.bin`) are still being walked, and asserts the capture aborts. Deterministic via a background writer that keeps `first.bin`'s mtime advancing (a past-mtime offset, distinct every iteration), so the baseline sampled inside `CaptureSource` and the post-walk sweep each see a different mtime with no wall-clock race (100/100 local).

## Hosted (the acceptance criterion)

- Run `42083071514` (https://github.com/mcpdev80/baseharbor/actions/runs/42083071514) completed **success** at the exact reviewed head `d21badc6`. `PR Selected Checks` = success. All green: `PR · Source format`, `PR · Trusted Plan`, `Workflow policy`, `PR · Focused Python`, `PR · Validation · go-build`, `go-vet`, `go-unit-tests`. Runtime/HA gates skipped by the selected-checks mapping (the unit-tests gate is the acceptance criterion this round).
- The round-3 head `e2d87906` hosted run (`42077184597`) failed `go-unit-tests` (`TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation (0.01s)` — capture returned success). The flake was the barrier's `entry.Info()` identity check; the fixed `os.Lstat` barrier + deterministic regression pass here.

## Mutant proof (fail-fast, named, wörtlich)

- Hook-disabled mutant (barrier `if hadBaseline && nowNano != identity` neutralized): `TestSourceSnapshotDetectsChangeDuringRead` fails fast 3x with the named sentinel `change-during-read hook never fired within the local bound` at the 5.01s test-local bound — NOT the generic 10-minute timeout. Proves the barrier is a real deterministic witness (round-3 dead `entry.Info()` would have passed by luck).
- Final-sweep-disabled mutant: `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation` fails — the late mutation of an already-visited path is no longer caught. Proves the restored final sweep is a real guard.
- Race-50 named + quiet-20 quiet: terminal green. Full witness in `scripts/mutant-proof-r4.txt`.

## Required checks

- `gofmt -l internal/development/` → empty (formatted).
- `go build ./internal/development/` → clean (rc=0). Whole module `go build ./...` → clean.
- `go vet ./...` (whole module) → clean.
- `gofmt -l` + `bash scripts/source-readability-audit.sh` → PASS (Go file size, function span ≤ 200, regression ratchet).
- `-race -count=50` on the two named tests → `ok`.
- `-race -count=20` on `TestSourceSnapshotNoGuardAbortWhenQuiet` → `ok` (quiet leader).
- `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation` → 100/100 green.
- Whole package `go test ./internal/development/` → `ok`.

## Repo-rule compliance

- Write-set: only the two card Go files. No `.github/` edits, no workflow triggers, no reruns beyond the single required trigger commit.
- One working branch `work/r27-snapshot-flake` (PR #1387); single integration candidate per chain. No second branch invented.
- No subagents. All runs executed in this session. Hosted run watched to terminal myself (§4.6).
- Base attestation shown (ancestor rc=0 for both `e2d87906` and develop); ls-remote real == head verbatim.
- No secrets/tokens logged. Workspace layout respected (worktree under /tmp/opencode; mutant worktrees removed; no scratch under the ecosystem root).
- No markdown checkboxes in evidence (plain bullets only).

## Status

Round-4 candidate ACCEPT-ready: EREIGNIS barrier fixed to a real mid-walk `os.Lstat` (root-cause of the flake), final baseline-path verification restored as a second independent layer, late-mutation regression pinned deterministically. Hosted run `42083071514` terminal SUCCESS at `d21badc6`; local race-50 / quiet-20 / mutant proofs all as required.

## CI

- Hosted run `42083071514` → terminal SUCCESS @ `d21badc6` (go-unit-tests / go-vet / go-build / PR Selected Checks / Source format / Trusted Plan / Workflow policy / Focused Python all success; runtime/HA gates skipped by selected-checks mapping).
- Before: run `42077184597` @ `c87c5fb1` → `go-unit-tests` FAILURE `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation (0.01s)`.

## END

END w189-snapshot-flake-r4: head=d21badc6f4 endcheck=final-sweep restored (verifyFinalBaseline) + EREIGNIS barrier fixed to real os.Lstat (dead entry.Info() was the flake root cause) barre=unveraendert witness race50=gruen quiet20=gruen mutante=hook-disabled 3x rot named sentinel @5s; endcheck-entfernt mutante rot (regression fängt) hosted=42083071514 TERMINAL SUCCESS PR-Selected-Checks gruen lsremote=d21badc6f4 | ancestor e2d87906+develop rc=0, ein kandidat pro kette, nur 2 karten-dateien
