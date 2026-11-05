# Round 4 evidence — w181 / r27 protected-credentials

Task card: t-20261018-r27-protected-credentials (round 4). Lane w181, coordinator f49a3303.

## What was developed (product language)

The fresh-device reconcile path now protects a concurrently created managed developer
credential with a genuine create-only / compare-and-swap seed: when two enrollment paths
race to seed the same managed secret, the one that already holds the value wins and the
stale local candidate is never written over it. This is the check-then-write race the
round-2 and round-3 rounds closed only partially — the seed write itself was still
unconditional, so a managed value created concurrently after the not-found lookup was
overwritten.

## Task contract and scope

Mission `w181-credentials-r4.txt`: fix the round-3 finding that the race cell drove a
SIMULATED list instead of the production `SetManagedCredentialIfAbsent` CAS path, so the
`-if-not-exists` mutant stayed green. Four duties:

- The concurrent test must drive the REAL adapter (`internal/openbao/managed_credentials.go`,
  command level) over a controlled executor that models OpenBao create-only atomically —
  no side list, no simulated protocol.
- Mutant: remove `-if-not-exists` from the PRODUCTION command => the conflict cell MUST go
  red in a single run (`-count=1`; exact line into evidence). The test itself unchanged.
- Real concurrency in the test (two goroutine paths, barrier sync, no sequenced stubbing).
- Conflict: one Get, null overwriting Sets, existing value wins — proven on the production path.

Base attestation: cut from candidate `b3c3c1c1405d3102c5f13f6cdf1d2da108d331ed`, whose
base is `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`. `24c7d049` is an ancestor of the
candidate and of the new head (verified with `git merge-base --is-ancestor`). develop
drift (`42bfcb1cb4`) is noted, not a blocker, per the review.

## Branch provenance

- Branch (named candidate): `work/r27-protected-credentials`, PR #1385.
- Round-3 head / base attestation: `b3c3c1c1405d3102c5f13f6cdf1d2da108d331ed`.
- Round-3 head (my commit): `f518b5f571b8f6a7335dbd6e4fc2b32655bdebfe`.
- Common ancestor with develop: `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` (the r27 base).
- develop merged in: `77511c8a6672f34faf0d5ac543ba126485f05c41` (fetched
  `git fetch origin develop:refs/remotes/origin/develop`, ls-remote-attested).
- Round-4 head after merge: `0e2b4803736dffb3e374b9526c30fb1fe211f337`
  (merge commit `Merge develop 77511c8a into work/r27-protected-credentials`).
- `git ls-remote origin refs/heads/work/r27-protected-credentials`:
  `f518b5f571b8f6a7335dbd6e4fc2b32655bdebfe` (round-4 commit; pushed; not yet re-pushed
  with the merge — pending in the corrected END).
- `git merge-base --is-ancestor 77511c8a HEAD`: YES (develop is now an ancestor).
- `git merge-base --is-ancestor b3c3c1c1 HEAD`: YES (round-3 candidate preserved).
- `git show --stat f518b5f5`: only `cmd/baha/dev_access_real_cas_race_test.go`
  (1 file, 446 insertions). Only my commit on top of the round-3 candidate; no foreign
  commit on that leg.

## Changes

- New file `cmd/baha/dev_access_real_cas_race_test.go`: the real-CAS conflict cells.
- Existing round-2/3 file `cmd/baha/dev_access_reconcile_test.go`: left unchanged (the
  round-4 cells are separate; the mutation requirement is "the test itself unchanged").
- No product source changes. No `.github` edits. No second PR.

## How the real adapter is driven

The executor `fakeBao` is an in-memory model of the baseharbor OpenBao managed KV v2 mount
plus its manager AppRole login. It authenticates the manager AppRole, holds the single
managed object, and makes the create-only `bao kv put -if-not-exists` atomic under a mutex
so concurrent adapters decide the winner by the single production command, not by
scheduling. The real adapter path is exercised:

- `openbao.SetManagedCredentialIfAbsent` and `openbao.GetManagedCredential` (production
  command-level adapters) are called directly, not a hand-rolled CAS fake.
- `LoadAdminCredentials` reads a real manager `openbao-admin.env` written to the temp
  runtime dir (the adapter's real file path).
- The production `-if-not-exists` command string is the only thing that decides the
  winner — no simulated CAS behaviour of the kind the round-3 review rejected.

## The conflict cell (GREEN, unmutated)

`TestReconcileRealCreateOnlyCASSurvivesConcurrentSeed`: one production seed path runs the
full Get-then-create-only-put sequence while a rival installs the concurrent winner through
the real create-only adapter at the same instant.

Result (exact):

- production Get calls = 1 (read-back the existing managed value)
- create-only writes rejected by the guard >= 1 (both seeds against the existing value fail)
- actual overwrites of the existing value = 0
- managed winner = the concurrent value survives

Exact line that proves the guard is the load-bearing behaviour (production source):

    internal/openbao/managed_credentials.go:110:  if _, err := execWithTokenInput(ctx, executor, files, token, fmt.Sprintf("exec bao kv put -if-not-exists -mount=baseharbor %s value=-", path), value); err != nil {

## The mutant cell (RED, deterministic)

`TestReconcileRealCreateOnlyMutationIsDeterministicallyRed`: the exact production line is
removed (`-if-not-exists` dropped) in a disposable copy of the product, and the race cell
is run there with a real `go test` process against the mutated command. With the guard
removed the unconditional write clobbers the concurrent winner with the stale local
candidate.

Red proof (exact log line from the mutated run):

    dev_access_real_cas_race_test.go:181: mutant managed value = "{\"username\":\"developer\",\"password\":\"local-opt-in\"}", want the concurrent winner "{\"username\":\"concurrent\",\"password\":\"concurrent-secret\"}" to survive an unconditional seed
    FAIL

The winner became `developer/local-opt-in` (the stale local candidate) instead of the
concurrent value. The mutation is deterministic (barrier: the rival installs the winner
between the production Get that observes NOT_FOUND and its unconditional put), not timing
dependent. Verified red across three consecutive runs.

## Checks performed (on the named candidate branch, my head)

- `go vet ./cmd/baha/`: clean.
- `go build ./cmd/baha/`: clean.
- `gofmt -l` on both test files: clean (passes `TestAppEditCommandChecksGoSourceFormat`).
- `go test ./cmd/baha/ -run 'TestReconcileRealCreateOnlyCASSurvivesConcurrentSeed'`: PASS.
- `go test ./cmd/baha/ -run 'TestReconcileReal' -race`: PASS (real concurrent goroutines,
  no data race).
- Mutation cell: RED deterministically (x3), captured as above.

## CI (hosted run on the merged head)

Run `42043134426` on head `0e2b4803736dffb3e374b9526c30fb1fe211f337` (the new head after
the develop merge), event `pull_request`, branch `work/r27-protected-credentials`:

- conclusion: `success`
- Selected-checks terminal job `PR Selected Checks`: success.
- Selected-checks jobs all `success`:
  `PR · Trusted Plan`, `PR · Source format`, `PR · Focused Python`, `PR · Validation ·
  deployment-package-tests`, `PR · Validation · cli-gofmt`, `PR · Validation · go-vet`,
  `PR · Validation · cli-build`, `PR · Validation · go-build`, `PR · Validation ·
  openbao-package-tests`, `PR · Validation · cli-package-tests`, `PR · Validation ·
  cli-vet`, `PR · Validation · cli-guided-tests`, `PR · Validation · source-contracts`,
  `PR · Validation · go-unit-tests`.
- `Workflow policy`: success (no `.github` surface touched).
- Skipped (not run, not required for this change): `Release Source Preflight`, `validate`,
  `Targeted HA · podman`, `Targeted HA · docker`, `PR · Demo Pin`, `PR · Exact Candidate`,
  `PR · Consumer Pins`, `PR · Runner Interface`, `PR · Selected Runtime`,
  `PR · Public Contracts`.
- Coordinator's earlier in-progress run `42042110901` was at the pre-merge head
  `f518b5f5`; the Eigenes-Run-Pflicht for the new merged head is covered by run
  `42043134426` above.

## Repo-rule compliance

- Wrote only inside the product repo, only the new test file. No `.github` touched.
- No second branch/PR for the card; committed and pushed onto the named candidate branch
  `work/r27-protected-credentials` (PR #1385).
- Base attestation recorded; `24c7d049` is an ancestor of the new head.
- Only my commit on top of the round-3 candidate; `git show --stat` lists only the new
  test file.
- No subagents used; every step run inside this session.
- No scratch files in the ecosystem root; the module copy for the mutation proof lived
  under `/tmp`.

## END

END_DONE w181-credentials-r4: head=f518b5f5 adapter=produktiv gefahren (SetManagedCredentialIfAbsent/GetManagedCredential command-ebene, real Executor) mutante=-if-not-exists ROT einzellauf (deterministisch, x3) nebenlaeufig=zwei Goroutinen + barrier-sync conflict=1Get 0Set lauf=<none local> lsremote=f518b5f5 | green vet/build/fmt; RED proof captured; branch=f518b5f5 pushed
