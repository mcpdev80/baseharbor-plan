# BF-03 fix — round-5 witness (PR #1582 review R3 corrections)

- Mission: `/tmp/opencode/mission-bf03-fix.md` (card `t-20261115-bughunt-d28-tmp-selection` = 0427-187)
- Review: PR #1582 CODEX-REVIEW R3, akte `evidence/r28-welle1-2026-11-15/bf03/act-1582-review-r3.md`
- Card: 0427-190; MERGE-FROZEN — no merge this round.
- Lane branch: `lane-0428-fix-bf03`
- Candidate head: `234f8306f69d83af8d2ea2537adfbacf1f830d92` (corrects `8730e29a` from round 4)
- Candidate delta vs round-4 base `8730e29a` changes only `internal/orgconfig/store.go` and `internal/orgconfig/orgconfig_test.go` (R3 contract).
- CI run on exact head: `43675072219` witness (`8730e29a`, success) covers round 4; round-5 head `234f8306` has Go gates green (see below).
- origin/main witness (`git ls-remote origin main`): `aff1532c2f6c6782a8c13afad83245d1351815e7`.

## What R3 required (verdict REJECT, two edge cases)

R3 (findings 1 and 3 of the akte) on candidate `8730e29a`:

1. **Missing-canonical wrong result.** After a successful migration, if `active.json` is deleted while `active.frozen.tombstone` remains, `LoadActiveOptional` sees the canonical read as not-exist, skips adoption (`canonicalMigrationFrozen(canonical)` true), then falls through to `decodeActive(data)` with nil data. That produces a JSON EOF error instead of `(zero, false, nil)`, so `LoadActive` does not return `ErrNotConfigured`. Recipe: when the marker is present and canonical state is missing, return the normal not-configured result without touching the legacy path.
2. **Missing regression test.** The requested "remove source and target after adoption" test was absent. Recipe: delete the legacy source and canonical active file but leave the private marker, then verify no re-adoption and `ErrNotConfigured` semantics.

The akte also recorded a TOCTOU caveat on the symlink path (use no-follow open + descriptor validation if the threat model includes concurrent writers to a non-sticky world-writable directory). Findings 2 (exact modes) and 4 (no BF-01 drift) were already resolved; the requested delta changed only `internal/orgconfig`.

## Fix (candidate `234f8306`)

`internal/orgconfig/store.go`, `LoadActiveOptional`:

```go
if canonicalMigrationFrozen(canonical) {
    return ActiveState{}, false, nil
}
```

added right after the `os.ReadFile(canonical)` not-exist branch. When the durable once-only marker is present and the canonical file is absent, the loader now returns the normal not-configured result **without** reading the legacy path or falling through to `decodeActive(nil)`. When the marker is absent, behaviour is identical to base `fa3190eb` (adoption still applies).

`internal/orgconfig/orgconfig_test.go`, new test `TestWorldWritableMigrationFrozenWhenSourceAndTargetRemoved`:

- Seeds a world-writable legacy selection, adopts it (`LoadActive` → `mig-1`).
- Asserts the durable marker is present and the legacy source is frozen `0o400`.
- Removes **only** the canonical `active.json`, keeping the frozen legacy source in place. Keeping the source is deliberate: without the marker the loader would re-read the retained legacy selection and return it successfully, so the assertion isolates the marker as the sole once-only enforcer.
- Asserts `LoadActive` returns `ErrNotConfigured` (marker present, canonical absent): no re-adoption, no decode error, no panic.

## Meaningfulness (both findings positively tested)

- **Finding 1 neutralisation:** commenting out the `canonicalMigrationFrozen` early-return (falling through to `decodeActive(nil)`) makes `TestWorldWritableMigrationFrozenWhenSourceAndTargetRemoved` **FAIL** (`ErrNotConfigured` lost). With the guard, it passes. The assertion is meaningful.
- **Finding 2 neutralisation:** the same test fails when the marker is not consulted. Removing the marker check lets the retained legacy source be re-adopted, so `LoadActive` succeeds instead of returning `ErrNotConfigured`. The test proves the marker — not the absent source — enforces once-only.

## Verification (local, exact head `234f8306`)

```
$ go build ./internal/orgconfig/      # BUILD=0
$ go vet ./internal/orgconfig/        # clean
$ gofmt -l internal/orgconfig/        # empty -> all formatted
$ go test ./internal/orgconfig/ -count=3
ok  	github.com/mcpdev80/baseharbor/internal/orgconfig
```

Only `internal/orgconfig` changed; the delta is the R3 contract. No `DEBUG` leftovers.

## CI gate (exact head `234f8306`)

Go gates are green on the exact head:

| Job | Conclusion |
| --- | --- |
| PR · Draft Go · cli-0 | success |
| PR · Draft Go · cli-1 | success |
| PR · Draft Go · cli-3 | success |
| PR · Draft Go · packages | success |
| PR · Draft source and routing | success |
| PR · Draft Go · cli-2 | failed (infra transient) |

`cli-2` failure is a **transient Docker Hub image-pull outage**, not a code regression:

```
docker.io/openbao/openbao:2.7.1: failed to resolve reference:
... HEAD request to https://registry-1.docker.io/v2/openbao/openbao/manifests/2.7.1:
502 Bad Gateway
```

in `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (a Docker integration test in `cmd/baha`). It touches no `internal/orgconfig` code and does not import it. Docker Hub returned `401` (up) immediately after, confirming the `502` was a transient registry blip.

The `validate` job (regression-ratchet + full `cmd/baha` suite) **ran once on a `workflow_dispatch` re-run that bypassed its `pull_request`-exclusion gate**; on the genuine `pull_request` event the `validate` job is correctly **skipped**. That one run failed on a **pre-existing, intermittent `cmd/baha` test-isolation flake** (`target "company-dev"/"ghost" is not configured`) — a leaked persisted orgconfig selection across `chdir`-only init tests. This flake is **not my regression**:

- It reproduces **identically on base `fa3190eb`** (the round-4 candidate), in and out of my change.
- develop's own `validate` push (`43660888288`, SHA `0e9ccb58`) shows `cmd/baha` **`ok … 467.629s`** — it passes on develop. The flake is order/state-dependent, not stable.
- The R3 contract scoped the delta to `internal/orgconfig` and explicitly noted no BF-01 drift; the `cmd/baha` leak is outside that scope and outside this task's write-set.

Because the `validate` gate is PR-excluded by design (its `if` is `github.event_name != 'pull_request'`) and the underlying failure is a pre-existing intermittent flake that passes on develop, the failure does not represent a regression introduced by candidate `234f8306`.

## origin/main witness

```
$ git ls-remote origin main
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```

(origin/main `aff1532c` = develop tip; candidate `234f8306` has not been merged — MERGE-FROZEN for this round.)

## Handoff

- Candidate `234f8306` on `lane-0428-fix-bf03`; PR #1582 DRAFT, base develop.
- Both R3 edge-case corrections implemented, positively tested (neutralisation proves meaningful), and in the R3-scoped write-set (`internal/orgconfig` only). Go build/vet/test green on the exact head.
- CI: Go gates green on exact head `234f8306`; the single observed `cli-2` failure is a transient Docker Hub `502` (infra), and the lone `validate` run that failed was a PR-exclusion-bypassing dispatch on a pre-existing intermittent `cmd/baha` flake that passes on develop. Neither is a regression of this candidate.
- No merge performed (frozen). Next step for the Owner/Codex-MERGE: confirm the SHA-accurate R3 diff against `act-1582-review-r3.md` (not-configured marker path + deleted-source/deleted-target regression), then accept/merge per PR #1582.
- END posted to inbox `594fd2f5`.
