# Snapshot change-guard determinism — defense-in-depth proof (w192, round-5)

Task: `t-20261105-r27-snapshot-change-guard-deterministic` (r27 wave 4).
Lane: `w192` (Worker, model Ornith-Laptop). Coordinator: `841e7734`.
Branch: `work/r27-snapshot-flake` (PR #1387), final tip `0298871895c19ed2844751ac9a4a141c7250d2a3`.
Evidence: this file + the two mutant worktrees removed at end.

## Base attestation (Owner requirement)

- Round-4 head (this chain, pre-this-round): `d21badc6f4a202b5ff81022e0039adc095e079e3`.
- Attestation: `git merge-base --is-ancestor d21badc6 HEAD` -> rc=0.
- Develop (today, three times lapsed): `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`.
- Attestation: `git merge-base --is-ancestor 3d8fc207 HEAD` -> rc=0. **This closes the END-abwiesung gap (1): develop is now a real ancestor of the branch tip.**
- Final ls-remote witness: `work/r27-snapshot-flake` -> `0298871895c19ed2844751ac9a4a141c7250d2a3` (real push).
- Lineary ancestry chain (single parent each, so the PR source-parent check passes): `3d8fc207` (develop) -> `288c130c` (round-5) -> `0ffe96bf` (round-5.1, span trim) -> `02988718` (round-5.2, span trim).
- Write-set across the whole round-5 chain: `internal/development/source_snapshot.go`, `internal/development/source_snapshot_test.go` only. No `.github/`, no subagents, no second PR.

## Goal (in product language)

The source-snapshot capture must *prove* it saw a change during the read (a real mid-walk event, not a timing gamble) AND defend the baseline paths after the walk. Round-4 built two layers (an in-walk per-file identity barrier that fires a `ChangeHook` on divergence, and a post-walk final-sweep that re-checks every baseline path). Round-4's late-mutation regression mutated an already-visited file from the very start, so the in-walk barrier could catch it too — the test never proved the post-walk sweep (Layer 2) was load-bearing: removing Layer 2 left the test green. Round-5 makes the regression isolate Layer 2 deterministically.

## The change (round-5 only, write-set = 2 card files)

- `internal/development/source_snapshot.go`:
  - The production `ChangeHook` seam fires a second, named sentinel `__path_read_<rel>` exactly once per baseline path the walk reads past its per-file barrier (tracked via a per-`CaptureSource` `consumedPaths` map, emitted through the `signalConsumedPath` helper). This tells a caller a path is already visited — the in-walk barrier can no longer see a mutation of it, so only the post-walk final sweep can catch it. A single extra map lookup per consumed baseline path; no new stat.
  - `baselineReadSignal(relSlash)` returns the `__path_read_<rel>` event name.
  - `ChangeHook` field doc documents both events. Layer 1 (in-walk EREIGNIS barrier) and Layer 2 (post-walk `verifyFinalBaseline` sweep) are unchanged in behaviour; only the test-isolation seam was added.
  - Round-5.1/5.2 trimmed `CaptureSource` from 216 lines back to 191 (CI readability limit 200, baseline ratchet 0) by extracting `signalConsumedPath` and compressing in-walk comments.
- `internal/development/source_snapshot_test.go`:
  - `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation`: rewritten. Two files — `aaa.bin` (read first, lexically before the `filler/` directory) and 40 filler files. The writer waits for the `__path_read_aaa.bin` hook signal, then continuously retouches `aaa.bin` while the filler files are still captured. Because `aaa.bin` was already read past its per-file barrier, the in-walk barrier cannot see the mutation; only Layer 2 aborts. A `sawRead` atomic flag (the writer consumes the `firstRead` channel, so the channel can't be inspected post-hoc) proves the walk reported `aaa.bin` read. A missing-signal mutant fails fast with the named sentinel, not a generic timeout.

## Mutant proofs (fail-fast, named, wörtlich)

- **Layer 2 removed** (`verifyFinalBaseline` neutralized with `if false`, isolated mutant worktree, removed after the run): `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation` goes RED:
  - `source_snapshot_test.go: expected final baseline-path verification to abort the capture on a late mutation of an already-visited file`
  - This is the required named-red proof: the in-walk barrier alone does not catch a mutation of an already-visited path, so the test is red only when Layer 2 is present. Proves Layer 2 is load-bearing.
- **ChangeHook disabled** (mutant: the in-walk barrier's `opts.ChangeHook(relSlash)` call removed, isolated mutant worktree, removed after the run): `TestSourceSnapshotDetectsChangeDuringRead` goes RED:
  - `source_snapshot_test.go:249: change-during-read hook never fired within the local bound` at the 5.01s test-local bound — NOT the generic 10-minute timeout. Proves the barrier is a real deterministic witness (a bare mtime-delta proof would have passed by luck).

## Required checks (all green)

- `gofmt -l` on both card files -> empty (formatted).
- `go vet ./...` (whole module) -> clean (rc=0).
- `go build ./...` (whole module) -> clean (rc=0).
- `bash scripts/source-readability-audit.sh` -> PASS (Go file size <= 800 lines / no worse than baseline; function span <= 200; regression ratchet). Production file `CaptureSource` trimmed back to 191 lines to fit.
- `-race -count=50` on the two named tests -> `ok` (stable across repeated runs).
- Full package `-race` -> `ok`.

## Round-5.2 — END-abwiesung gap (2): own-run to terminal

- The earlier hosted run `42097684121` at my old head `d21badc6` was still IN_PROGRESS when the first END was filed; it has since completed FAILURE. The failure is the pre-existing, Docker-runtime-dependent `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` in `cmd/baha` (`Docker endpoint unix:///var/run/docker.sock is unavailable`), verified by running that test against develop `3d8fc207` locally — it fails identically. That test is outside my card (`internal/development/`) and unrelated to my change.
- After the develop merge I watched the NEW hosted run against the current tip to terminal (§4.6): run **`42106254196`** (https://github.com/mcpdev80/baseharbor/actions/runs/42106254196) -> overall **completed / success**.
  - `PR · Source format` -> success (failed on the merge-commit tip and once more on the first linear tip because `CaptureSource` spanned 216/207 lines vs the 200 limit; trimmed to 191 by the round-5.1/5.2 work; readability audit now PASSES).
  - `PR · Validation · go-unit-tests` -> success — my card's `internal/development` package: `ok github.com/mcpdev80/baseharbor/internal/development`.
  - `PR · Validation · go-build` -> success, `PR · Validation · go-vet` -> success, `PR Selected Checks` -> success.
- The acceptance gate `go-unit-tests` is this lane's run to own; it was watched to its terminal SUCCESS here.

## Scope split / repo-rule compliance

- Scope split (Owner 2026-11-04): `.github/**` belongs to the Owner. This task never touched workflow files, never triggered `workflow_dispatch` or reruns. All checks ran locally or on the existing PR; no CI gate was re-triggered by me.
- Branch provenance: `d21badc6` (mission head / round-4 head) is shown as an ancestor of my head `07108f08` (rc=0). A single integration candidate per chain: the one branch `work/r27-snapshot-flake` (PR #1387). No second branch invented.
- Evidence lives only in baseharbor-plan (this file). No `.evidence/` directory, no main-branch writes, no operational text in a product repo.
- No docker/compose started on this host (pure Go unit-test task; the docker test host is `baha-docker` via SSH, not this session host). No `bh-*` containers on this host.
- No subagents: every run, mutant, check, and the push were executed in this session.
- No secrets/tokens logged.

## CI

- Hosted run **`42106254196`** -> terminal SUCCESS @ tip `02988718`. `go-unit-tests` (acceptance gate) success; `go-build`, `go-vet`, `PR Selected Checks`, `PR · Source format` all success; runtime/HA gates skipped by the selected-checks mapping.
- Before: run `42099175294` @ linear tip `288c130c` -> `go-unit-tests` success but `PR · Source format` FAILURE (`CaptureSource spans 207 lines (limit: 200)`); and the merge-commit tip `f8cabb73` also failed `PR · Source format` for the same span reason on the linear-ancestry heuristic. Both resolved by trimming the function span to 191.
- The `PR · Source format` / `PR Selected Checks` checks are the Owner's workflow heuristic; this lane records the failing STATE and does not rerun them (scope split). The acceptance gate `go-unit-tests` is this lane's to own and it passed.

## END

END w192-snapshot-flake-r5: head=0298871895 endcheckmutante=ROT wörtlich "expected final baseline-path verification to abort the capture on a late mutation of an already-visited file" hookmutante=ROT wörtlich "change-during-read hook never fired within the local bound" @5.01s race50=gruen quiet20=gruen hosted=42106254196 TERMINAL SUCCESS go-unit-tests+go-vet+go-build+PR-Selected-Checks+Source-format gruen lsremote=0298871895c develop-3d8fc207 ancestor rc=0 (gap1 geschlossen), lauf42106254196 bis terminal beobachtet (gap2 geschlossen), ein kandidat pro kette nur 2 karten-dateien kein compose
