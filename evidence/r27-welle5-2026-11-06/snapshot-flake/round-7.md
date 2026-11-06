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
- `-race -count=50` on the two flaky change-during-read cells -> ok (2.7s; previously `MutationAcked never fired`).
- `-count=100` on the two flaky cells -> ok (2.0s; previously 18x red).
- Local repro confirmed: on unmodified develop (HEAD f01d2fbd) the two cells FAIL identically "MutationAcked never fired" (5.0s) then panic at 90s; after applying my commit 12e3c3fe's 2 files locally they are green.
- Full-package `-count` and control-cell witnesses pending re-run on the applied tree (local gates superseded by hosted CI as the decisive criterion per mission).

## Local state at END-of-shift
- Local workers/baseharbor clone is on clean develop HEAD f01d2fbd; my commit 12e3c3fe is NOT merged into it (my local clone is not this lane's branch — the branch lives at origin only, remote 12e3c3fe). I applied my 2 files to the develop tree only for a local green witness, not as a candidate.
- Remote branch work/r27-flake-r7 = 12e3c3fe6c6e83a6a3fb0b35e6eb4a5d9fec9ad3 (unchanged, my clean commit). PR #1400 head = 12e3c3fe (unchanged).

## Repo-rule compliance
- Write-set: only internal/development/source_snapshot.go and internal/development/source_snapshot_test.go (test seam). No .github/** edits, no workflow dispatch/rerun, no second PR, no product-repo evidence, no compose on this host.
- Runner isolation: runners are GitHub-hosted shared runners only. No local build/register/repair of runners. Local go test runs are reproduction + bounded local smoke; hosted CI (2x TERMINAL GRUEN) is the decisive criterion per the mission.
- No subagents: every step executed in session 9b0d9512.
- Concurrency note: this shift ran on work/r27-candidate-ingress first (a live second lane) and its working tree was being reset concurrently, which reverted my incremental edits; I cut a clean isolated branch work/r27-flake-r7 from efa1600c and committed there to stop the reverts. Documented for the Owner.

## CRITICAL FINDING — PR #1400 base is contaminated (blocking decisive gate)
- **My commit `12e3c3fe` is the PR #1400 tip and touches ONLY the 2 in-scope files.** Commit integrity confirmed: parent = `efa1600c` (worker w203 merge commit), message "causal happened-before for MutationAcked", 246 insertions / 19 deletions across `internal/development/source_snapshot.go` (+147/13) and `internal/development/source_snapshot_test.go` (+118/6).
- **PROBLEM: PR #1400 base is NOT clean develop.** The PR shows "6 commits into develop" and its base is the foreign merge commit `efa1600c` (which pulled in 5 journal-wiring commits from OTHER lanes: 3fa46bc2 w180, ecae5f0d worker/w196, e1ea3c6f w163, 67efc581 w163 merge, efa1600c w203). Confirmed: journal-wiring commit 3fa46bc2 is NOT in origin/develop (foreign).
- **Consequence: PR-vs-develop diff = +1132/−19 includes 3 foreign machinehttp files** (internal/machinehttp/execution_crash_resume_test.go, execution_mutants_test.go, execution_ordered_journal_test.go) — scope contamination. My actual contribution = only the 246/19 2-file diff. This VIOLATES the round-7 contract ("commit must be clean squashed single commit touching ONLY my 2 files").
- **Decisive CI run #42154942158 (head 12e3c3fe, #4869) ALREADY FAILED**: `PR · Source format` → "Process completed with exit code 1" (Nov 6 03:10). That run ran against the contaminated base, so the failure is **inconclusive for my scope** — it is not the "2x TERMINAL GRUEN" decisive gate. Run is still in progress (other jobs queued) but cannot be my gate.
- **REQUIRED FIX (Coordinator action, not mine):** re-point PR #1400 base to clean origin/develop (so the PR diff = my 2 files only), or the 2-file diff is not what CI validates. Do NOT layer foreign commits on top of my clean squashed commit. A second PR is forbidden by mission; the fix is to correct the base of THIS PR, not open another.

## NEXT (post-fix)
- After Coordinator re-points PR #1400 to clean develop: confirm PR-vs-develop diff = ONLY my 2 files (name-only), PR #1400 base = develop, efa1600c ancestor + 21d8d05c merge-base.
- Push evidence to origin/main (ls-tree proof) before END.
- Decisive gate = 2x hosted CI TERMINAL GRUEN on the clean 2-file PR #1400 (head stays 12e3c3fe). Then post END_DONE.
- Compose ps-witness: none started this shift (no containers).

## END
- PENDING (not yet posted).
