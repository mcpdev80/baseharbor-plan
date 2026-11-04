# CODEX-WORKER w133 — profile codec round 6

Card: `t-20261018-r27-profile-codec`; PR #1363; existing remote branch `work/r27-profile-codec`; coord f49a3303.

## Candidate and lineage

Final PR head: `ac6a048e290f4c1be5d2657b7aa3baefd384318b`.
The Owner-directed develop base was `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`.
Merge commit `fb48254db383dfea1cead299c652b6830b3f2714` has parents `5cbc4fe1036b20bf649dd8d792b4bb53c605e644` and `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`; it is a normal two-parent merge, not a rebase or force-push. The final short-write log assertion commit is a descendant of that merge.

Witnesses:

- `git merge-base --is-ancestor origin/develop HEAD` exited 0.
- `git merge-base origin/develop HEAD` is `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`.
- `git ls-remote origin refs/heads/work/r27-profile-codec` returned `ac6a048e290f4c1be5d2657b7aa3baefd384318b`, equal to final HEAD.
- PR #1363 remains OPEN and ready, base `develop`, head exactly `ac6a048e290f4c1be5d2657b7aa3baefd384318b`.

## PLAN

1. Refresh PR, develop, branch, existing review and prior evidence; preserve the stale local branch ref and unrelated worktrees.
2. Replace duplicate staging writes with one injectable write attempt; prove actual `n < len(data)`, typed failure and clean rollback.
3. Verify false trust switch, full record round-trip with non-empty export descriptor, canonical ordered golden bytes, additional canary categories, and replacement cleanup failure state.
4. Align EN and DE codec/store rules in parallel; verify the production-consumer boundary read-only.
5. Merge the refreshed develop head normally, run all required local checks on the merged candidate, push only to the existing PR branch, and observe hosted checks to terminal.

## Seven review points

1. **Atomic write / genuine short write.** `Store.atomicCommit` makes one `s.writeStaging(f, data)` call and tests the returned count before Sync or Rename. The unconditional second write is removed. The deterministic seam writes the first half of the actual buffer and captures requested and returned byte counts. `TestRecipe4ShortWriteSeam` asserted one writer call, `0 < n < requested`, `errors.Is(err, ErrPartialWrite)`, no final `.json`, and no `.tmp`. Exact local test log: `recipe 4: staging writer returned n=809 for requested=1619 bytes`.
2. **Trust switch false.** `TestRecipe3TrustSelfConsistencyUnconditional` constructs `ExpectedBindingForTest(rec, false)`, tampers the carried CA fingerprint, imports the tampered container, and requires rejection. The implementation still calls `ValidateTrust` unconditionally.
3. **Full import→export and canonical bytes/order.** `TestRecipe6FullRecordRoundTrip` uses a valid `credential-export` record with a non-empty AES-256-GCM descriptor. It requires one valid JSON document with EOF after the first decode, then compares the complete serialized `RecordWire` bytes against the original, including `export`. `TestRecipe6CanonicalGoldenBytesAndFieldOrder` pins `store.golden.json` SHA-256 `255be16cff43839ca1a0b17cc60bc8acee7c518f4616dd4467ea82023bfd9e34`, checks re-encoding byte equality, and asserts container, record and nested field order against explicit expected sequences.
4. **Canary categories.** `TestRecipe5CanaryPerCategory` independently rejects installation ID, scope, recipient, destination path, nested `storage.class`, export descriptor nonce, and private-key PEM canaries. The helper requires `ErrSecretOnField` for fields scanned by the secret detector and requires no exported container; if a container is returned, it serializes it and asserts the canary is absent before failing. `storage.class` is a closed two-value enum in the schema, so a schema-valid arbitrary canary cannot be made there; the deliberately malformed canary is rejected by the scanner before any export bytes are returned. Export nonce `SECRETAAAAAAAAAA` is a valid 16-character base64url value and reaches the secret scan.
5. **Replacement cleanup failure.** `TestRecipe4ReplaceCleanupFailurePreservesOldRecord` injects a deterministic obsolete-file removal error. Import returns typed `ErrNoWrite`; the exact old JSON bytes remain as the only `.json` file, no `.tmp` remains, and a newly opened store reads the old state cleanly.
6. **EN/DE specification parity.** Both `docs/spec/credential-access-v1.md` and `docs/de/spec/credential-access-v1.md` now state the exact canonical record version on export/import, mandatory non-empty expected recipient prefix, canonical member order including nested records, one-write staging behavior, short-write failure before Sync/Rename, and old-state preservation on replacement cleanup failure.
7. **Write-set / consumer boundary.** `git diff --name-only origin/develop...HEAD` lists exactly ten paths: eight under `contracts/managementaccess/v1` and the two paired specs. No `.github`, `cmd/baha`, or `internal/delivery` path changed. Read-only production import grep for `github.com/mcpdev80/baseharbor/contracts/managementaccess` returned no matches; production call-site grep outside the package for `ExportToContainer`, `ImportWithBindingForTest`, `NewStoreForTest`, and `DecodeContainerForTest` returned no matches. The production consumer remains assigned to `t-20261018-r27-public-surfaces`.

## Local verification on final source

- `GOCACHE=/tmp/w133-codec-r6-gocache go test ./contracts/managementaccess/v1 -count=1` — PASS (`ok ... 0.192s`). The focused short-write probe also passed with `n=809`, `requested=1619`.
- `GOCACHE=/tmp/w133-codec-r6-gocache go build -buildvcs=false ./...` — PASS.
- `GOCACHE=/tmp/w133-codec-r6-gocache go vet ./...` — PASS.
- `gofmt -l contracts/managementaccess/v1` — no output; PASS.
- `git diff --check` — PASS.
- Plain `go build ./...` was attempted and failed only while Go queried VCS status in this temporary worktree (`error obtaining VCS status: exit status 128`); full build with VCS stamping disabled passed. No build/test source was altered to hide this environment limitation.

## Hosted checks to terminal

The first run on the develop-merged candidate, `41885222570`, reached `completed/success` for head `fb48254db383dfea1cead299c652b6830b3f2714`; documentation audit, EN/DE strict MkDocs, source contracts, source format, focused Python, Workflow policy and PR Selected Checks passed. A one-line test-log follow-up was then pushed so the short-write witness records the actual returned count.

Final-head run `41885528132` for `ac6a048e290f4c1be5d2657b7aa3baefd384318b` reached terminal `completed/success` (watch exit 0). Terminal passes: source format, trusted plan, Workflow policy, focused Python, documentation audit, EN strict MkDocs, DE strict MkDocs, pages candidate build, source contracts, and PR Selected Checks. Impact-selection jobs for consumer/runtime/release/HA were skipped by the workflow selector; no required selected check was skipped. No rerun or workflow dispatch was issued.

## repo-rule compliance

One existing PR and remote branch only; normal merge of `origin/develop`; normal fast-forward push; no force-push, no `.github` changes, no merge of the PR, no status change, no removed tests, no subagents. All implementation work stayed inside the allowed contract directory and paired EN/DE spec files. The isolated worktree lived under `/tmp/w133-profile-codec-r6`; unrelated local changes and worktrees were preserved. This evidence has no Markdown checklist checkboxes.

## END

END_DONE w133-codec-r6: head=ac6a048e29 einzelschreib=belegt kurzschreib=n=809<1619 bewiesen vertrauen=unbedingt rundlauf=vollstaendig+golden canary=je_kategorie aufräumen=typisiert spec=EN=DE lsremote=ac6a048e29 | Develop 2ea2c6f1 ist Vorfahr des gemergten Kandidaten; PR #1363 Hosted Run 41885528132 terminal erfolgreich.
