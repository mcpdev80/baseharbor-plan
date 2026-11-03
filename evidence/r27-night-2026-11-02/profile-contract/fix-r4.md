# Fix r4 — PR #1324 (task t-20261018-r27-profile-contract)

**Lane:** l6-profile-r4 · **Coord:** f49a3303 · **Basis:** head `78b851d9` · **PR:** #1324
**Status in progress — lane DONE | BLOCKED line updated with END.**

## PLAN

1. Read mission + review-1324d.md; create own worktree from `work/r27-profile-contract` (head 78b851d9).
2. Punkt 1 SCHEMA-LÜCKE: make schema-if/then for each of the three classes (management-profile, device-enrollment, credential-export) complete; add schema Golden Positive + Negative per class, running through the real validator.
3. Punkt 2 ENROLL-BINDUNG: change `EnrollDevice` signature to require profile + installation ID + pinned CA (via `Enforcer.ResolveFingerprint`, previously uncalled) + recipient + expiry and validate ALL before `enforcer.Enroll` runs; reorder to validate-then-enroll. Add positive + negative (foreign CA, expired, recipient mismatch) tests through the real path, asserting no effect on failure.
4. Punkt 3 DOKU: make docs EN/DE contradiction-free — either code satisfies the bound-anchor claim (keep it) or docs are set to implementation state (pre-consumption verification only for what 1+2 really do). deferred section stays honest.
5. Punkt 4 GOLDEN one-use: enrollment reuse (one-use) via one real path as Negative-Golden.
6. Tests: `TMPDIR=/tmp go test ./contracts/managementaccess/v1` + `go build ./...` + `go vet`.
7. Push (fast-forward), `ls-remote` as proof, no foreign run-logs, then END to f49a3303.

## Progress

- [x] Step 1: worktree
- [ ] Step 2: schema
- [ ] Step 3: enroll binding
- [ ] Step 4: docs
- [ ] Step 5: golden one-use
- [ ] Step 6: tests
- [ ] Step 7: push + END

## repo-rule compliance

(document here after changes)
