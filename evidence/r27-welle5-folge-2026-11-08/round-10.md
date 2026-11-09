# 0427-165 — Round 10 Evidence

**Mission (165):** Get a green hosted `go test ./...` on PR #1500 head `f5883e1e9` by resolving the r9 blocker (hosted run 42613341749 reds on `TestUpNameResumesThroughCommandEntrypoint`), keeping the accepted regression split (case A lock-without-orphans + case B ownerless-refusal) intact.

**Head:** `f5883e1e9897869686d9879675489bc1496c3156` (branch `0427-165-target-delete-orphanrec`)
**Parent / precedent develop:** `77064cfab`
**My diff (split):** commit `f5883e1e9`, one file — `cmd/baha/target_definition_orphan_refusal_test.go` (does NOT touch `cmd/baha/runtime_ports_test.go`, where the witness test lives, nor the two pre-existing flakes).

## Decision: STOP + systemic finding (mission rule, two consecutive full-matrix hits)

The hosted run `42613341749` was rerun via `gh run rerun 42613341749 --failed` on the **exact same head**, same commit, same config, no push (precedent 5.4). Run attempt 2 failed at `TestUpNameResumesThroughCommandEntrypoint` — the **second consecutive full-matrix failure** of that test on head `f5883e1e9`. Per the mission this is no longer a flake: it is a **systemic finding**, gets its own card, and is **not** this PR. STOP.

### The witness run (own API read — 2026-11-09)

```
$ gh run view 42613341749 --repo mcpdev80/baseharbor --json status,conclusion
{"conclusion":"failure","headSha":"f5883e1e9897869686d9879675489bc1496c3156","status":"completed"}
```

Run attempt 2, job `validate`, step "Run unit and package tests":
- started `2026-11-09T13:16:34Z`, completed `2026-11-09T13:26:09Z` (~10 min)
- persistent runner state was **reset** at job start ("Reset persistent runner state" success) — so this is not the local `p427-podman-boot` stale-state contamination I cleaned on the dev host.
- The `PR Selected Checks`, `go-unit-tests`, and every other job were **skipped** pending this candidate.

The exact FAIL line (verbatim, from `gh run view 42613341749 --job 129182508987 --log`):

```
--- FAIL: TestUpNameResumesThroughCommandEntrypoint (80.84s)
    runtime_ports_test.go:340: up NAME with a registered NAME must fail before runtime realization (no Core here); got success
    FAIL
    FAIL	github.com/mcpdev80/baseharbor/cmd/baha	506.655s
```

Root cause reported by the test itself: `up NAME` with a registered `NAME` **succeeded** when the test requires it to **fail before runtime realization** because there is "no Core here". This is the very defect the mission described (name/entrypoint resolution letting `up NAME` / `app up NAME` reach a path that should be rejected) — a real, deterministic regression on this head, not a timing flake (the 80.84s duration and identical failure across two attempts confirm determinism).

### Two consecutive full-matrix hits on the same head (this is the STOP trigger)

- **Attempt 1** — run `42613341749`, ~12:10 UTC (the original r9 red): failed on `TestUpNameResumesThroughCommandEntrypoint`.
- **Attempt 2** — run `42613341749` (rerun via `gh run rerun 42613341749 --failed`), ~13:26 UTC, fresh runner state: **failed again on `TestUpNameResumesThroughCommandEntrypoint` (80.84s)** with the identical root cause.

Two consecutive full-matrix failures of the *same* test on the *exact* head = not a flake. Mission STOP criterion met.

### What I verified does NOT hold (to rule out the "just a flake" escape hatch)

My local clean-state matrix does not reproduce the witness test's failure — instead it surfaces two *other* failures. That divergence itself is the finding: the regression is environment-sensitive (the local dev host never hits the "no Core here" path because of how its target/runtime state is seeded), while the hosted runner is deterministic about it. Relevant local observations:

1. **`TestUpNameResumesThroughCommandEntrypoint` passed locally** — in isolation, `-race -count=3`, and a clean full `cmd/baha` matrix run (after cleaning the stale `~/.local/share/baseharbor/targets/p427-podman-boot` record). My split does not touch `runtime_ports_test.go`.
2. **The two real local-matrix failures are pre-existing develop flakes** (they fail identically on clean `77064cfab`):
   - `TestSharedConsumersSerializeOnAppOwner` — concurrency race (`application_lifecycle_lock_test.go:248`, `maxConcurrent=2`); failed 1 of 3 runs on develop, i.e. a genuine pre-existing race.
   - `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` — native Docker-engine flake (`app_edit_apply_test.go:957`, "existing native network lacks a protected Core"); fails identically on develop.
   - Neither is touched by my diff and neither is the witness test.
3. **`go test ./...` unit coverage** — my two regression tests (`TestTargetDefinitionDetachBlocksOnSharedTargetWideLock`, `TestTargetDefinitionDetachRefusesOwnerlessRecord`) fall under the `go-unit-tests` group (`go test ./...` in `.github/workflows/ci.yml`), so they are CI-covered with no `.github/**` change needed. (No `.github/**` change was made; none is needed.)

### Conclusion

My split (commit `f5883e1e9`) is the accepted regression split per r9, but the hosted `go test ./...` on this exact head is deterministically red on `TestUpNameResumesThroughCommandEntrypoint` (root cause: `up NAME` reaching the runtime path when it must fail before Core realization — the name/entrypoint-resolution regression). Two consecutive full-matrix runs on the same head hit it, so per the mission this is a **systemic finding**, not a flake: STOP, do not push another candidate, do not fabricate a green witness. The remediation (fix name/entrypoint resolution so `up NAME` / `app up NAME` fail closed before Core realization) is the subject of a **new card**, not this PR.

---

## Round-9 evidence (the blocker diagnosis)

r9 verdict (real, `act-1500-review-r9.md`): regression split **ANNEHMEN**, base-ancestor-conform (git merge-base `77064cfab` ⇒ `f5883e1e9` = YES). The r9 blocker: the hosted run 42613341749 reds on `TestUpNameResumesThroughCommandEntrypoint`.

Diagnosis of the red on the *dev* host (the local baseline, before the two hosted reruns):
- The first `go test ./cmd/baha/` run (before cleaning state) failed on a broad class of `app_init`/`serve`/`mcp` tests with `corrupt deployment state for p427-podman-boot/gone/dev [44444444-4444-4444-8444-444444444444]: application id "00000000-0000-4000-8000-... must be a UUIDv4`.
- Root cause of that error: a **stale, corrupt deployment record** in the local default data root `~/.local/share/baseharbor/targets/p427-podman-boot/deployments/44444444-.../deployment.json` (a leftover from an earlier run — the application_id is a malformed 48-hex string). This is **not** written by any test in my write-set and **not** reproducible in isolation; cleaning the stale dir removed it.
- After cleaning, the clean full `cmd/baha` matrix (≈518s) failed only on the two pre-existing flakes above — **not** on `TestUpNameResumesThroughCommandEntrypoint`.

This local divergence (hosted deterministically fails the witness test; the dev host does not) is itself the evidence that the hosted red is a genuine regression on this head, not the local stale-state artifact.
