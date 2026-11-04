# CODEX-REVIEW — PR #1363 profile codec, round 6

- Candidate: `ac6a048e290f4c1be5d2657b7aa3baefd384318b` (PR #1363 head and remote `work/r27-profile-codec`).
- Base: `develop` `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`; live PR metadata agrees, and this base is an ancestor of the candidate.
- Evidence reviewed: `evidence/r27-welle4-2026-11-04/profile-codec/round-6.md`; its claims were checked against source, tests, local runs and live GitHub state.
- Verdict: **ACCEPT**. Review only; no approval or merge performed.

## Seven review points

1. **Exactly one staging write and real short write — PASS.** `contracts/managementaccess/v1/store.go:923-957` calls `s.writeStaging(f, data)` exactly once, rejects either a write error or a returned count other than `len(data)` before Sync/Rename, removes the staging file, and wraps the failure with `ErrPartialWrite`. There is no unconditional second `Write`. `store_round5_test.go:120-160` injects a genuine prefix through the same seam and asserts the recorded `written` value is nonzero and less than `requested`, exactly one seam call, typed error, no final JSON and no `.tmp`. Exact-SHA local test output logged `n=809` for `requested=1619`.

2. **Trust self-consistency cannot be disabled — PASS.** `store.go:818-835` calls `p.ValidateTrust()` unconditionally during import; `ExpectedBinding.TrustSelfConsistent` is documented as retained but ignored at `store.go:123-126`. `store_round5_test.go:99-114` supplies `ExpectedBindingForTest(rec, false)`, tampers the carried fingerprint and requires rejection.

3. **Complete round trip and canonical golden bytes — PASS.** `store_round5_test.go:306-375` imports and re-exports a credential-export record with a nonempty AES-256-GCM descriptor, checks the committed artifact is one valid JSON document with EOF after decode, then compares the complete serialized `RecordWire` against the original. This includes every record field and `export`. `store_round6_test.go:15-59` pins the golden file SHA-256, compares re-encoded bytes, and checks container, record and nested member order including `export`.

4. **Canary categories, including path, nested value and export text — PASS.** `store_round5_test.go:261-300` checks installation ID, scope, recipient, destination path, nested `storage.class`, export nonce and private-key PEM. The helper requires an `ErrSecretOnField` rejection and no returned container; the nonce canary is schema-valid base64url text. `storage.class` is a closed enum, so an arbitrary canary is necessarily an invalid enum value; the test still verifies the encoded-field scanner rejects that nested value before returning a container. The scanner covers the fully encoded container at `store.go:507-530`, including nested and export fields.

5. **Replacement cleanup failure — PASS.** `store_round5_test.go:163-203` injects obsolete-file removal failure and asserts `errors.Is(err, ErrNoWrite)`, that only the exact old JSON remains byte-for-byte, that no staging artifact remains, and that reopening the store sees a clean state. The rollback behavior is implemented at `store.go:904-918`.

6. **English/German specification parity — PASS.** The paired serialization sections in `docs/spec/credential-access-v1.md:214-220` and `docs/de/spec/credential-access-v1.md:214-220` state matching requirements: canonical record version independent of caller input, nonempty recipient binding, canonical container/record/nested field order, exactly one staging write, short-write failure before Sync/Rename, no retry, and old-state preservation with typed failure when obsolete cleanup fails. The prose is translated rather than literally identical; the normative requirements and values match.

7. **Write set, local checks, gates and evidence — PASS.** The exact base-to-head changed paths are the eight listed `contracts/managementaccess/v1` files and the two paired specs; no path falls outside the mission's allowed set. Independent local verification at the exact candidate: `GOCACHE=/tmp/r1363e-gocache go test ./contracts/managementaccess/v1 -count=1` — PASS; `GOCACHE=/tmp/r1363e-gocache go build -buildvcs=false ./...` — PASS; `GOCACHE=/tmp/r1363e-gocache go vet ./...` — PASS; `gofmt -l contracts/managementaccess/v1` — empty; `git diff --check` — PASS. Live PR is OPEN, non-draft/READY, base `develop`, head exact. `git ls-remote` reports develop `2ea2c6f1...` and branch `ac6a048e...`. Hosted run `41885528132` for the exact head is terminal `completed/success`; required `PR Selected Checks` is success. Workflow policy, source format, trusted plan, EN/DE strict docs, documentation audit, pages candidate, source contracts and focused Python are success. Selector-excluded impact jobs are skipped; no required selected check is skipped. The round-6 evidence file was present and its claims were independently checked.

## Review boundary and END

Reviewed exact candidate `ac6a048e290f4c1be5d2657b7aa3baefd384318b` in a detached worktree. No candidate source or workflow files were changed. No merge performed. Only this Planning evidence file is being published.

`END_DONE codex-r1363e: verdict=ACCEPT open=none | Single-write and real-short-write assertions, trust=false, full export round trip/golden bytes, category canaries, typed cleanup, EN/DE parity, write-set and terminal hosted gates verified at ac6a048e290.`
