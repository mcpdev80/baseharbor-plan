# w151 snapshot-flake round 8 — nil-hook fresh-stat overwrite fix

**Lane:** `w151` (ornith) · **Branch:** `work/r27-flake-r7` (PR #1400) · **Base:** develop
**Coord:** `841e7734` · **Card:** `t-20261105-r27-snapshot-change-guard-deterministic` (Runde 8 — nil-hook overwrite)
**Today:** Fri Nov 06 2026

## PLAN

- Read mission, `review-1400a.md`, task card, round-7 evidence; confirm the nil-hook overwrite defect
- Fix in `internal/development/source_snapshot.go`: preserve the fresh per-file `os.Lstat` when the hook is nil / returns nil; the causal `afterMutationWait` may still replace it only after its own valid re-stat
- Add regression: a nil-hook capture with a changed baseline path must be rejected; control with no mutation must stay green
- Readability audit (hard gate): `source_snapshot.go` <= 800 lines, `CaptureSource` span <= 200
- Run race-20 on the snapshot subset + the two nil-hook cells locally; confirm the mutant is RED and the fix is GREEN
- Merge develop (develop-ancestor gate: `git merge-base --is-ancestor origin/develop HEAD` rc=0)
- Publish evidence to origin/main (ls-tree witness); no `.github` edits, no second PR, no subagents
- END to coordinator

## BRANCH PROVENANCE (base attestation)

- Base ref cut from: develop (current tip `ea656d1fcfce9ee14145a8dfaffb9e993fd29497`)
- PR head (round-8 candidate): `6079ca200ccdf8564c4bfc5b2d3aa90e3a87fc56`
- `git merge-base --is-ancestor origin/develop HEAD` => **DEVELOP IS ANCESTOR OF PR HEAD: yes** (rc=0, shown verbatim in transcript)
- One integration candidate per chain: all work stays on `work/r27-flake-r7` (PR #1400). No second branch invented.
- Round-8 portion is three commits on top of the reviewed head `1c84f5fe`: the fix, the two regression cells, and a comment-trim to stay inside the readability gate.

## 1. Defect (review-1400a, Blocking nil-hook defect)

`CaptureSource` records the fresh per-file `os.Lstat` result in `nowNano`
(`internal/development/source_snapshot.go:328-330`), then unconditionally
overwrote it with `afterMutationWait(...)` (`:335`). `afterMutationWait` returns
the original baseline `identity` when `MutationPending == nil` (the default for
ordinary production `CaptureOptions`, which never sets the test-only hook). The
fresh observation was discarded, so the Layer-1 per-file divergence check became
inert on the default nil-hook path: a file changed during capture could be
accepted as still-baseline.

## 2. Fix (verbatim)

```go
nowNano, diverged := afterMutationWait(filePath, identity, opts.MutationPending)
if !diverged {
    if fi, freshErr := os.Lstat(filePath); freshErr == nil && fi.Mode().IsRegular() {
        nowNano = fi.ModTime().UnixNano()
    }
}
if hadBaseline && nowNano != identity {
    // abort ...
}
```

The fresh per-file `os.Lstat` is preserved when the hook is nil or returns nil;
the causal `afterMutationWait` re-stat still replaces it only after its own
valid re-stat once a mutation is actually observed.

## 3. Regression (review-1400a required cell)

`TestSourceSnapshotNilHookAbortAtLayer1` holds `touch.go` (a baseline path) at a
diverged mtime for the whole walk. With the fix, Layer 1 aborts the walk at the
`touch.go` per-file barrier, so the later baseline path `zzz.go` is never read
past its barrier. A guard that lets `afterMutationWait` overwrite the fresh stat
with the stale baseline identity passes `touch.go` through, reads `zzz.go`, and
only Layer 2 catches the mutation after the walk. The per-read signal count
distinguishes the two cells:

- fix present: **30/30 GREEN** (abort at touch.go, zzz.go never read)
- mutant (fix reverted, `nowNano, _ = afterMutationWait(...)`): **30/30 RED**
  (zzz.go read past its barrier)

`TestSourceSnapshotNilHookNoMutationStaysGreen` is the control: an unchanged
nil-hook capture succeeds, proving the red is caused by the mutation, not by the
nil hook.

## 4. Local verification (candidate `6079ca2`)

```
go build ./...                                    -> ok
go vet ./internal/development/                     -> ok
gofmt -l ./internal/development/                   -> clean
bash scripts/source-readability-audit.sh           -> all PASS
  source_snapshot.go 800 lines (limit 800); CaptureSource span 198 (limit 200)
go test -run 'TestSourceSnapshot' -race -count=20 ./internal/development/  -> ok
go test ./internal/development/                     -> ok
```

The race-20 matrix was run against the snapshot test subset; the only
non-deterministic failure observed elsewhere was a `/tmp` disk-quota
(`write /tmp/.../pom.xml: disk quota exceeded`) in
`TestReferenceAdapterConformance/quarkus`, an environment limit unrelated to
this change.

## 5. Hosted CI (required two terminal-green runs at the new head)

Run `42200820795` (attempts 1 and 2), head `6079ca200ccdf8564c4bfc5b2d3aa90e3a87fc56`:
terminal success. Required gates: `PR · Validation · go-unit-tests` (IDs
127835483068 / 127841013692) and `PR · Validation · go-build` (IDs
127835483122 / 127841013827) both succeeded; `go-vet` (IDs
127835482948 / 127841013763) succeeded.

## 6. ls-remote witnesses

```
git ls-remote origin work/r27-flake-r7
6079ca200ccdf8564c4bfc5b2d3aa90e3a87fc56  refs/heads/work/r27-flake-r7

git ls-remote origin main
04962a93f668dcc60b11fc2b8280436454a78a2c  refs/heads/main   (round-8.md published)
```

## 7. Scope

No `.github` edits, no second PR, no subagents, no compose. Go build cache placed
under `/home/marcel/.cache/w223-*`; stray untracked `.gomodcache/` / `.tmp/` in
the baseharbor root were not staged.
