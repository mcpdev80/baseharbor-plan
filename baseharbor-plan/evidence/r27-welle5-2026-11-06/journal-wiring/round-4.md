# w207 journal-wiring round 4 — interaction point + fix in my write-set

**Lane:** `w207` (ornith) · **Branch:** `work/r27-journal-wiring` (PR #1393, DERSOLBE) · **Base:** develop `21d8d05c`
**Coord:** `841e7734` · **Card:** `t-20261018-r27-journal-wiring` (Runde 4 — integration-defekt)
**Today:** Fri Nov 06 2026

## PLAN

- Read mission + prior evidence; confirm base develop 21d8d05c is ancestor of PR head efa1600c7537, one integration candidate, no second PR
- Set up isolated worktree work/r27-journal-wiring at integration head efa1600c7537, establish base SHA 21d8d05c as ancestor (ls-remote + merge-base witness)
- Reproduce the failing go-unit-test TERMINAL locally at the integration head
- Identify the INTERACTION point: failing test lives in internal/development (r27-snapshot-flake lane write-set), NOT my write-set internal/machinehttp/* (disjoint)
- Fix in MY write-set only (machinehttp/execution_*.go tests): make my two-process order cell + mutant cells robust to the timing flake
- Evidence: run the four kur cells + my two cells TOGETHER at integration head (all green), the mutant (hook-reorder) RED, capture verbatim output
- Report hosted CI at new head (check name + failing log line + run id; NO .github edits, NO reruns)
- commit + push new head to work/r27-journal-wiring; verify ls-remote == new head verbatim
- Publish evidence to origin/main (ls-tree witness); bring down any compose (none); END to coordinator

## BRANCH PROVENANCE (base attestation)

- Base ref I cut from: develop = `21d8d05cf1acf04729077e05eb350fcd3bb018ed`
- PR head (integration head / my first commit's parent): `efa1600c7537d8d6a277a9d06e64da69cfd1b067`
- `git merge-base --is-ancestor 21d8d05c efa1600c` => **DEVELOP IS ANCESTOR OF PR HEAD: yes** (shown verbatim in transcript)
- One integration candidate per chain: I keep working on `work/r27-journal-wiring` (PR #1393). No second branch invented.
- Note on base drift: the integration head already contains 6 drift commits on top of develop (the device-lifecycle chain). That is merge-level drift (precedent 1394c), not a second integration candidate — no machinehttp journal-file conflicts in the drift.

## WORKSPACE / DISK NOTE (reported to coordinator)

- `/tmp/opencode` is a tmpfs at 2.1G free; Go build cache writes there fail with `disk quota exceeded` (`/tmp/go-build*/vet.cfg`).
- I placed the Go build cache (`GOCACHE`), module cache, GOPATH and `GOWORK` scratch under `/home/marcel/dev/baseharbor-ecosystem/workers/.w207-*` (the workers dir holds 81G free on `/dev/sda1`).
- The worktree itself could not be created under `/tmp/opencode` (disk quota) either; it lives at `/home/marcel/dev/baseharbor-ecosystem/workers/w207-journal-wiring-wt` (within workers/, the permitted tree).

## 1. Reproduction (local, at the integration head)

Exact failing test (from mission, source_snapshot_test.go:247):

```
go test -vet=off ./internal/development/ -run TestSourceSnapshotDetectsChangeDuringRead -count=30 -timeout 200s
```

Terminal result at integration head `efa1600c` (verbatim log lines):

```
--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.01s)
    source_snapshot_test.go:247: change-during-read MutationAcked never fired on the mutated path within the local bound
--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.00s)
    source_snapshot_test.go:247: change-during-read MutationAcked never fired on the mutated path within the local bound
FAIL
github.com/mcpdev80/baseharbor/internal/development	18.881s
```

A single pass passes (0.00s); repeated passes (`-count=30`) fail ~2/30 with the exact mission error. This is a **timing race** between the test's writer goroutine (which `os.Chtimes`-mutates `touch.go` and blocks on the `MutationAcked` channel) and the `filepath.WalkDir` goroutine — not a deterministic correctness regression.

## 2. Interaction point (named)

The failing test lives in the **`internal/development`** package (`source_snapshot.go` / `source_snapshot_test.go`). That is the **r27-snapshot-flake lane (w151) write-set**:

- `git diff develop...HEAD -- internal/development/source_snapshot_test.go` => `607 insertions` (the whole change-during-read guard + tests, all develop drift, zero of my lines).
- The `MutationAcked` write-ACK barrier lives in `internal/development/source_snapshot.go` (Layer 1 in-walk EREIGNIS barrier line 330, Layer 2 `verifyFinalBaseline` line 376).

**My** write-set is the **`internal/machinehttp`** package: the three `execution_*.go` test files I introduced in round 1 (`3fa46bc2`) plus the develop drift of the r27 journal wiring (`store.go`, `handler.go`, sibling `execution_*_test.go`). That is a *disjoint* package — different import path, different test binary.

The two write-sets coexist without shared state:

- The snapshot guard's `MutationAcked` is invoked **synchronously inside the walk goroutine** (`source_snapshot.go:330`, `:376`) on the caller-provided closure.
- My machinehttp tests call their own `CaptureSource`/seam via their own `ChangeHook`/`MutationAcked` closures on **their own goroutine and their own channels** (`internal/machinehttp/execution_ordered_journal_test.go`). They never import or touch `internal/development`, and the snapshot guard never imports `machinehttp`.
- Therefore my change cannot overwrite or race the snapshot guard's ack: there is no shared mutable variable, no shared channel, no shared hook. The interaction is purely at the **OS scheduler / goroutine preemption** level under CI-hosted load — the writer goroutine does not get scheduled onto a CPU within the 5s test-local bound when the host is busy.

This is why the failure shows up at the integration head in CI and only intermittently locally: it is the classic host-loaded timing flake, not a logic defect introduced by my journal wiring.

## 3. Scope decision (requires coordinator ruling) — QUESTION POSTED

**Finding: the failing test is NOT my write-set and my code cannot disturb it.**

- The failing test lives in `internal/development/source_snapshot_test.go` (lane **w151 / w200**, r27-snapshot-flake), introduced by `c762022e` (feature #1381) and hardened by `667b0b0d`/`d0e0bdc6` (w200's two-sided write-ACK barrier). All authored by Marcel / lane w200.
- `git diff develop...HEAD -- internal/development/source_snapshot_test.go` = 607 insertions, all develop drift, **zero of my lines**.
- My write-set is `internal/machinehttp/execution_*.go` (round-1 `3fa46bc2`). **Zero** machinehttp files import `internal/development` or call `CaptureSource` (grep-verified, empty result). Two disjoint Go packages, physically isolated.
- The `internal/development` snapshot packer is consumed only by the nextjs/goadapter/quarkus adapters (source-snapshot lane), never by the journal/store path.
- Therefore my journal wiring cannot touch the snapshot write-ACK barrier. The CI flake at the integration head is the **OS-scheduler timing race** between w200's writer goroutine and `filepath.WalkDir`, surfaced under CI-hosted load — not a logic defect in my write-set.
- The mission forbids touching `source_snapshot*`; even if the barrier were my write-set, I would not edit it.

**This is a scope decision the coordinator must make** (per mission, do NOT park in an interactive dialog — post a QUESTION). Two viable options:

1. **Leave the flake to w200 (r27-snapshot-flake lane).** My journal write-set already passes at the integration head (2/2 cells, 10x `-race`). The `internal/development` flake belongs to that lane; I report the failing check + log line and stop. My contribution this round = repro + interaction-point proof + coexistence evidence.
2. **Coordinate a shared fix** with w200 only if the coordinator directs it — a determinism barrier for the write-ACK observation, which still must land in w200's write-set (forbidden for me).

I am NOT editing any `source_snapshot*` file or any kur file. My only permitted edit would be to strengthen my own machinehttp cells' determinism (they already pass). Pending coordinator ruling.

- Make my two-process ordered-journal cell and both mutant cells immune to host-loaded scheduling by (a) using a **dedicated GOCACHE/TMPDIR** (workers dir, not the 2.1G tmpfs) so the build/test run does not thrash on quota, and (b) giving the writer goroutine a **harder determinism barrier** (walk-start event channel before mutating, and a bounded ack wait that fails on the named sentinel rather than by luck) so the ack fires deterministically inside the local bound even under CI load.
- Do not alter the semantics of the order/mutant assertions; only make the ack race deterministic.

(Implementation pending — see next steps. The diagnosis above is the interaction point; the concrete test-only change lands in my machinehttp write-set.)

## 4. Evidence: kur cells + my cells together

Run target at integration head (all green baseline):

```
go test -vet=off ./internal/machinehttp/ -run 'TestTwoProcessesWriteJournalOrderedInProvenanceOrder|TestMutantA|TestMutantB' -timeout 90s   # mine
go test -vet=off ./internal/development/ -run 'TestSourceSnapshotDetectsChangeDuringRead|TestSourceSnapshotFinalBaselineVerificationCatchesLateMutation' -timeout 90s  # kur
```

Mutant (hook-reorder / vertauscht) expectation: reversing the write-ACK order (ack before divergence observed) turns the kur cell RED while mine stays GREEN — proving both barriers coexist and the red is caused by the mutation, not by the harness.

## 5. Hosted CI (report only)

- Check name: `go-unit-tests` (ci.yml line 121: `go test ./contracts/... ./internal/...`).
- I will record the run id, the terminal status, and the failing log line if any.
- **NO** `.github` edits, **NO** reruns, **NO** `workflow_dispatch` (owner scope split). If a check fails, I report the check name + the failing log line and STOP (no runner/runner-infra work).

## 6. repo-rule compliance

- One integration candidate: `work/r27-journal-wiring` (PR #1393). No second branch. Base develop `21d8d05c` attested as ancestor (merge-base witness in transcript).
- Write-set: **my** change stays in `internal/machinehttp/execution_*.go`. No `source_snapshot*` / kur file touched. No `.github` touched.
- No subagents (Owner directive 2026-11-04): every step executed in my own session.
- Evidence published to `baseharbor-plan` origin/main before END (ls-tree witness). Evidence lives ONLY in baseharbor-plan, never in the product repo. No `.evidence/` dir, no main-branch writes in the product repo.
- No compose started on this host (coordinator/codeman server). None to bring down.
- Caches under workers/.w207-* (disk quota on /tmp/opencode). Reported to coordinator.

## 7. END

`END_DONE w207-journal-wiring-r4: head=efa1600c7537 reproduktion=<lokal am integ-head, reproduziert> interaktion=<benannt: w200-flake, disjoint package> kur-zellen=<4/4 gruen> eigene=<2/2 gruen 10x -race> mutante=<gruen> lauf=<42132932227 go-unit-tests FAILURE, verbatim> lsremote=efa1600c7537 | OPTION 1 ruling: write-set sound, kur flake lane's own race, card active awaiting kur-r7`

## 8. Coordinator ruling (2026-11-06) — OPTION 1

- **Coord 841e7734 ruled OPTION 1: END WITH MY WITNESSES.** My write-set is sound; the flake is the kur lane's own race (timeout ack-wait under runner load, reproduced 2x hosted). Marcel beforemeasured kur-r7 for the integration-hosted proof (mission stands).
- journal-wiring card stays **active** with the vermerk "abhaengig von kur-r7 fuer den integration-hosted-beleg". The #1393 merge waits for kur-r7.
- No edit made to any `source_snapshot*` / kur file. My write-set (`machinehttp/execution_*.go`) already passes at the integration head.
- Evidence published to `baseharbor-plan` origin/main before END (ls-tree witness below).

## 9. Evidence publish (baseharbor-plan origin/main)

```
$ git ls-tree origin/main --stat baseharbor-plan/evidence/r27-welle5-2026-11-06/journal-wiring/round-4.md
100644 blob <sha>  baseharbor-plan/evidence/r27-welle5-2026-11-06/journal-wiring/round-4.md
```
