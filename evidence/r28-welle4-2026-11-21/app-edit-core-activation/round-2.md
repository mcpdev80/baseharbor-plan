# 0428-207 / PR #1735 — exact-head closeout

- Exact PR head: `5617fd4efe9fce887463507d6f34dd2a04ecd625`.
- Exact run: [44890430911](https://github.com/mcpdev80/baseharbor/actions/runs/44890430911), SUCCESS.
- Existing affected test: `cmd/baha.TestAppEditCommandCompleteProviderEditRunsRealLifecycle`.
- Added regression: `cmd/baha.Test0428207CoreActivationFailsBeforeComposeWhenOwnerInventoryMissing`.
- Both test IDs deterministically map to `PR · Go unit · cli-2` (job `136804912887`), SUCCESS. Aggregate `PR Selected Checks` job `136806045895`, SUCCESS.
- The exact run also passed all other Go shards, packages, owner, build/vet, source format, and selected checks.
- PR #1735 merged normally at 2026-11-21T09:43:17Z as `72ebc9d10ec247f24853af579655fd95c387214b`.
- The App Edit activation path now reports the protected Core/shared-backend owner refusal before attempting Compose, preserving operator-auth behavior and the existing real lifecycle test.
