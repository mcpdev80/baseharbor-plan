# BF-03 fix — round-7 witness (PR #1582 review R4 corrections)

- Mission: `/tmp/opencode/mission-bf03-fix.md` (card `t-20261115-bughunt-d28-tmp-selection` = 0427-187)
- Review: PR #1582 CODEX-REVIEW R4, akte `evidence/r28-welle1-2026-11-15/1582-init-migration/act-1582-review-r4.md`
- Card: 0427-190; MERGE-FROZEN — no merge this round.
- Lane branch: `lane-0428-fix-bf03`
- Candidate head: `756b2be7eb2ee2e0671de6cf2e7862395e3881fc`
  - `312933dc` = round 6 (cmd/baha package isolation + R3 edge cases).
  - `756b2be7` = new source-and-target-both-removed regression test (this round).
- CI run (terminal, success): `43683234849` on `756b2be7` (event `pull_request`, workflow "CI · PR #1582").
- origin/main witness (`git ls-remote origin main`): `aff1532c2f6c6782a8c13afad83245d1351815e7`.

## What R4 required (one narrow point)

Verdict REJECT at `312933dc` for one missing acceptance regression:

- The tombstone/missing-active-file behavior is fixed and asserted (findings 1, 3, 4 already satisfied).
- The requested source-and-target-removal regression is **not actually present**. `TestWorldWritableMigrationFrozenWhenSourceAndTargetRemoved` retains `legacyPath` and only removes `canon` — no test removes the legacy source in the missing-target regression.
- Recipe: keep the retained-source assertion, and add a **distinct** case that removes **both** `legacyPath` and canonical `canon` while preserving the private marker, then calls `LoadActive` and asserts `errors.Is(err, ErrNotConfigured)` with **no decode error**.
- Scope: add exactly this one test, change nothing else. Covered by the existing `PR · Draft Go · packages` job; no workflow edit needed.

## Fix (candidate `756b2be7`)

`internal/orgconfig/orgconfig_test.go` only — one new test:

`TestWorldWritableMigrationFrozenWhenSourceAndTargetBothRemoved`:
1. Seeds a world-writable legacy selection, adopts it (`LoadActive` → `mig-1`).
2. Asserts the durable marker `active.frozen.tombstone` is present.
3. Removes **both** the canonical `active.json` **and** the frozen legacy source, leaving only the private marker.
4. Asserts `LoadActive` returns `ErrNotConfigured` with no decode/EOF error and no successful return.

This is a distinct case from `TestWorldWritableMigrationFrozenWhenSourceAndTargetRemoved` (retained source), which proves the marker blocks re-adoption even with a live source present. The both-removed case locks in that a deleted legacy source is never resurrected by a second migration.

## Meaningfulness (positively tested)

Neutralizing `canonicalMigrationFrozen` (returning false) to prove the assertion:
- `TestWorldWritableMigrationFrozenWhenSourceAndTargetRemoved` (retained source) → **FAILS** (marker is what blocks re-adoption with a live source).
- `TestWorldWritableMigrationFrozenWhenSourceAndTargetBothRemoved` (both deleted) → still passes even neutralized, because with both files gone `adoptLegacySelection` finds no source and returns `(false, nil)`. This is expected: the both-removed case passes trivially without the marker, which is why it is a **contract lock** ("both deleted → not-configured") rather than the stronger behavioral proof. The retained-source test remains the marker-semantics proof; the both-removed test is the exact case R4 demanded.

## Verification

```
$ go build ./internal/orgconfig/          # BUILD=0
$ go vet ./internal/orgconfig/            # clean
$ gofmt -l internal/orgconfig/            # empty -> all formatted
$ go test ./internal/orgconfig/ -run 'TestWorldWritableMigrationFrozenWhenSourceAndTarget' -v
    --- PASS: TestWorldWritableMigrationFrozenWhenSourceAndTargetRemoved
    --- PASS: TestWorldWritableMigrationFrozenWhenSourceAndTargetBothRemoved
$ go test ./internal/orgconfig/ -count=3   # ok (stable, no flake)
```

Full branch vs base `fa3190eb` changes only three files: `internal/orgconfig/store.go`, `internal/orgconfig/orgconfig_test.go`, and `cmd/baha/runtime_integration_test_support_test.go`. The R4 delta (`312933dc..756b2be7`) changes **only** `internal/orgconfig/orgconfig_test.go` (+81 insertions). Working tree clean.

## CI gate (terminal, exact head `756b2be7`)

Run `43683234849` (PR #1582, event `pull_request`, head `756b2be7`) → **completed / success**.

| Job | Conclusion |
| --- | --- |
| PR · Draft Go · cli-0 | success |
| PR · Draft Go · cli-1 | success |
| PR · Draft Go · cli-2 | success |
| PR · Draft Go · cli-3 | success |
| PR · Draft Go · packages | success |
| PR · Draft source and routing | success |
| validate | skipped (PR-excluded by design) |

`internal/orgconfig` (including both source/target-removal tests) is covered by `PR · Draft Go · packages`, which is green. No workflow edit was made; the new test falls under the existing `packages` job as R4 noted.

## origin/main witness

```
$ git ls-remote origin main
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```

(origin/main `aff1532c` = develop tip; candidate `756b2be7` has not been merged — MERGE-FROZEN for this round.)

## Handoff

- Candidate `756b2be7` on `lane-0428-fix-bf03`; PR #1582 DRAFT, base develop.
  - `234f8306` R3-scoped `internal/orgconfig` fix (not-configured marker path + retained-source regression).
  - `312933dc` `cmd/baha` package config/data isolation (round 6 coordinator-reject fix).
  - `756b2be7` the distinct source-and-target-both-removed regression R4 required (one test, no other change).
- `internal/orgconfig`: build/vet/gofmt clean; the two source/target-removal regression tests green; package stable across `-count=3`. Terminal CI success on the exact head (`packages` Go gate green).
- No merge performed (frozen). Next step for the Owner/Codex-MERGE: confirm the SHA-accurate delta against `act-1582-review-r4.md` (the one added test is exactly the requested source-and-target-removal regression; nothing else changed), then accept/merge per PR #1582.
- END posted to inbox `594fd2f5`.
