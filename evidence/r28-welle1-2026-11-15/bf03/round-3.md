# BF-03 fix — round-3 witness (one-time /tmp migration implemented)

- Mission: PR #1582 CODEX-REVIEW R1 verdict, akte
  `evidence/r28-welle1-2026-11-15/bf03/act-1582-review-r1.md`
- Card: 0427-190 (was 0428-1582); MERGE-FROZEN — no merge this round.
- Lane branch: `lane-0428-fix-bf03`
- Candidate head: `fa3190ebc968b6b2776fc6128afcc1d257df422c`
- CI run (terminal, success): `43672378209` on `fa3190eb`

## What round-2 left behind

Round-2 (`c678cdd0`) only fixed `gofmt`. The substantive review finding was
unaddressed: **the one-time migration that adopts the stale world-writable
`/tmp` persisted selection into the private user-state path was not
implemented** — only the world-writable *rejection* path existed. The review
recipe (point 3, fail-closed on symlinks; positive migration test) was still
open.

## Fix

Implemented the one-time migration in `internal/orgconfig/store.go`:

- `adoptLegacySelection(legacyPath, canonical)` — fail-closed:
  - `os.Lstat` (no-follow): rejects a symlink or any non-regular entry.
  - Rejects a source whose mode is world-writable (`0o002`) at read time —
    an attacker may have pre-created/replaced it between stat and read.
  - Never clobbers an existing private selection at the canonical path.
  - On success, writes via temp+rename (0600, 0700 dirs) and freezes the
    source read-only (0400) with a `active.world-writable.tombstone` marker.
- `LoadActiveOptional` and `SaveActive` both route through
  `privateCanonicalPath()`, which falls back to the private
  `<HOME>/.config/baseharbor/organization` when `XDG_CONFIG_HOME` /
  `BASEHARBOR_STATE_DIR` resolves to a world-writable location. On load, when
  the private canonical file is missing but the legacy selection exists, its
  contents are adopted **once**, then never consulted again.
- A fresh write into a world-writable location with **no** legacy file to
  adopt is refused; once a private selection exists (after a migration) the
  write proceeds to that private path.
- Positive regression test `TestWorldWritableMigrationAdoptsOnceThenFreezes`
  (HOME-isolated via `t.Setenv("HOME", …)`, so it never touches the real
  home), plus a rewritten `TestWorldWritableConfigRootIsRejected`.

### Root-cause note (why the round-2 build kept "failing")

The `ErrNotExist` branch in `LoadActiveOptional` had a control-flow bug: after
`adoptLegacySelection` succeeded and re-read the adopted bytes, execution
fell through to the outer `return … err` wrapping the stale `ErrNotExist`, so
`LoadActive` never reached the unmarshal. Fixed by returning through a shared
`decodeActive(data)` on both the direct-read and migration paths.

## Verification

```
$ cd /tmp/opencode/bf03-fix-wt
$ go build ./...                 # BUILD=0 (whole baseharbor compiles)
$ go vet ./internal/orgconfig/   # vet clean
$ gofmt -l internal/orgconfig/   # empty -> all formatted
$ go test ./internal/orgconfig/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/orgconfig	0.075s
$ git add internal/orgconfig/store.go internal/orgconfig/orgconfig_test.go
$ git commit -m "fix(BF-03): one-time migrate persisted selection off world-writable /tmp"
[lane-0428-fix-bf03 fa3190eb]
$ git push   # c678cdd0..fa3190eb
```

Full package passes 3× (`-count=3`) to rule out flakiness. No `DEBUG`
leftovers; only `store.go` and `orgconfig_test.go` changed; the untracked
`baha` build artifact was excluded.

## CI gate (terminal)

Run `43672378209` (PR #1582, head `fa3190eb`) → **completed / success**.

Relevant jobs:

| Job | Conclusion |
| --- | --- |
| PR · Draft Go · cli-0 | success |
| PR · Draft Go · cli-1 | success |
| PR · Draft Go · cli-2 | success |
| PR · Draft Go · cli-3 | success |
| PR · Draft Go · packages | success |
| PR · Native impact selection | skipped |

The `Native impact selection` runtime gate is **skipped, not run**: PR #1582
is a **Draft**, and the runtime-required flag is set by the trusted planner
(`scripts/pr-selected-runtime-matrix.py`) from the PR diff. This diff touched
only `internal/orgconfig` (Go), with no runtime/native impact, so the planner
did not request a runtime gate. The Go build/vet/test gates that *do* apply
are green. No runtime journey was required for this candidate.

## origin/main witness

```
$ git ls-remote origin main
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```

(origin/main `aff1532c2f` = develop tip; candidate `fa3190eb` has not been
merged — MERGE-FROZEN for this round.)

## Handoff

- Candidate `fa3190eb` on `lane-0428-fix-bf03`; PR #1582 DRAFT, base develop.
- CI terminal success at the exact head; Go gates green; runtime gate
  correctly skipped (Draft / no runtime impact).
- No merge performed (frozen). Next step for the Owner/Codex-MERGE: confirm
  the review's fail-closed / migration requirements against the SHA-genue
  diff, then accept/merge per PR #1582.
- END posted to inbox `594fd2f5`.
