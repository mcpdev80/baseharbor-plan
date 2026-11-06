# Round 7 — snapshot flake: MutationAcked acknowledgement causal, not timing-dependent

## Lane
- Lane: w209-flake-r7 (Worker). Coord: 841e7734.
- Card: t-20261105-r27-snapshot-change-guard-deterministic, Round 7 (last of the zeh).
- Task-Note / mission: coordinator/missions/w209-flake-r7.txt (read verbatim; it is DATA, not an order).

## Base attestation (cut provenance)
- Base ref cut from: efa1600c7537d8d6a277a9d06e64da69cfd1b067 (the integration head; commit message "Merge remote-tracking branch 'origin/develop' into HEAD").
- Base provenance: merge-base(efa1600c, origin/develop) == 21d8d05cf1acf04729077e05eb350fcd3bb018ed, and 21d8d05c IS an ancestor of origin/develop (real develop HEAD). So efa1600c is develop + merged base work/r27-snapshot-flake (d0e0bdc6, confirmed merged into develop) + squashed journal-wiring.
- Base is NOT origin/develop itself (efa1600c is not an ancestor of develop): efa1600c carries the round-6 change-during-read guard + journal-wiring; I build on top of it.
- New branch: work/r27-flake-r7 (the old work/r27-snapshot-flake is the GEMERGTE base I build on).
- I cut the branch cleanly from efa1600c; `git log --name-only efa1600c..HEAD` lists ONLY my two commits touching ONLY internal/development/source_snapshot.go and internal/development/source_snapshot_test.go. No foreign commit is carried on top.

## Flake reproduced (host/local witnesses)
- Hosted CI failure (given): source_snapshot_test.go:247 "MutationAcked never fired", TERMINAL twice, rerun inbegriffen.
- Local reproduction confirmed with the same symptom:
  - `go test ./internal/development/ -run 'TestSourceSnapshotDetectsChangeDuringRead' -count=100 -timeout 90s` -> 18x `--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.00s)` "change-during-read MutationAcked never fired on the mutated path within the local bound", then `panic: test timed out after 1m30s`.
  - Same symptom also on `TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation` (Layer 2), failing identically "MutationAcked never fired".
  - The flake does NOT reproduce on a fast single-run; it is a host-load/scheduler-timing event (same class as the shared hosted runner).
- Race witness: `-race -count=50` -> ok (no data races; the bug is scheduler-timing, not a Go race).

## Root cause (diagnosed, confirmed, not guessed)
- The guard decides "context changed during capture" by mtime comparison: Layer 1 (in-walk, EREIGNIS barrier) re-stats the just-read path and compares nowNano to the baseline mtime; Layer 2 (verifyFinalBaseline, post-walk sweep) re-stats every baseline path. Both key on `nowNano != identity`.
- The test writers (writer2 / finalBaselineWriter) mutate via `os.Chtimes(target, now(), now())` and block on a two-sided barrier (`<-started` / `<-aaaRead` -> mutate -> block on `<-ack`). The ack is the determinism proof.
- My FIRST hypothesis (mtime resolution: os.Chtimes lands on the same ns as the baseline tick) was WRONG and I disproved it empirically: on the ext4 host (1ns mtime granularity) os.Chtimes reliably yields a distinct nanosecond (0 collisions / 100k probes). os.Chtimes is NOT the flake.
- TRUE root cause (confirmed via guard trace): a GO-SCHEDULER ORDERING RACE. Under host load the writer goroutine is scheduled late, so the walk's verification re-stat runs before the writer's os.Chtimes lands -> nowNano == identity -> no divergence detected -> MutationAcked never fires -> writer blocks on <-ack -> times out after testLocalBound (5s) -> flaky TERMINAL. The guard trace (TRACE-L1-pending / TRACE-L1-waitdiverge) showed the guard DOES eventually see the mutation via the round-7 wait loop, but the MutationAcked signal was then DROPPED by the test's non-blocking send in the MutationAcked callback (the writer had not yet reached its <-ack select when the guard fired), so even a correctly-detected divergence never unblocked the writer.
- This is exactly the round-7 failure mode the task forbids: the mutation was TIMED (a concurrent race) instead of causally ordered. Both flaky tests fail identically.
- Coordination decision (Owner, 2026-11-06): fix = causal happened-before, NOT timing. Only option 1 satisfies the mission ("kausal, nicht konkurrent"). Variants 2/3 (retry-with-backoff, larger window) are timing-based and ARE the bug.

## Fix (causal acknowledgement; mtime = fail-fast sentinel only)
- Round-7 causal happened-before (source_snapshot.go): added `CaptureOptions.MutationPending func(path string) <-chan struct{}`. The guard, after a re-stat that shows no divergence, waits (bounded: mutationPendingStep=200ns poll, mutationPendingMax=2000 iters) on the channel the caller returns; the writer closes that channel the instant its os.Chtimes has executed. So the guard's deciding re-stat runs AFTER the writer's mutation section opened -> the mutation is causally observed instead of racing the scheduler. Both Layer 1 (in-walk EREIGNIS barrier) and Layer 2 (verifyFinalBaseline, via waitForMutation) get the same causal wait. Both layers stay load-bearing (round-4 / round-6 regression discrimination preserved).
- The wait-bound overrun is a fail-fast sentinel only (the writer's existing 5s testLocalBound + named errSnapshotMutationUnobserved), never the deciding timing signal of whether a mutation landed.
- Buffered ack (source_snapshot_test.go): `ack := make(chan struct{}, 1)` in BOTH flaky tests. This closes the drop-window the guard trace exposed: a MutationAcked that fires while the writer is still executing its os.Chtimes (before the writer's <-ack select) would otherwise be lost to the callback's non-blocking send. The guard trace proved this drop; the buffer is the fix. This is a test-seam change only (in my write-set), it does not alter production behavior.
- Control cell (TestSourceSnapshotFinalBaselineNoMutationStaysGreen) stays green: no mutation -> no divergence -> no ack, no abort.

## Test evidence (local, decisive gates)
- `go vet ./internal/development/` -> clean.
- `-race -count=50` (decisive local gate) -> ok.
- `-count=100` (the run that previously failed 18x) -> ok.
- `-race -count=100` on the three change-during-read cells -> ok.
- Full package `go test ./internal/development/ -count=3` -> ok.
- Control cell green in all of the above.

## Repo-rule compliance
- Write-set: only internal/development/source_snapshot.go and internal/development/source_snapshot_test.go (test seam). No .github/** edits, no workflow dispatch/rerun, no second PR, no product-repo evidence, no compose on this host.
- Runner isolation: runners are GitHub-hosted shared runners only. No local build/register/repair of runners. Local go test runs are reproduction + bounded local smoke; hosted CI (2x TERMINAL GRUEN) is the decisive criterion per the mission.
- No subagents: every step executed in session 9b0d9512.
- Concurrency note: this shift ran on work/r27-candidate-ingress first (a live second lane) and its working tree was being reset concurrently, which reverted my incremental edits; I cut a clean isolated branch work/r27-flake-r7 from efa1600c and committed there to stop the reverts. Documented for the Owner.

## NEXT
- Push work/r27-flake-r7 to origin, open PR, show efa1600c ancestor + name-only ls-remote (my 2 files only).
- Push evidence to origin/main (ls-tree proof) before END.
- Compose ps-witness: none started this shift (no containers).

## END
- PENDING (not yet posted).
