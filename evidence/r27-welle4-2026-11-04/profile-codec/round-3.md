# ROUND 3 — r27 profile-codec (PR #1363 / card t-20261018-r27-profile-codec)

- Lane: w123-codec-r3 (Worker). Coordinator: f49a3303.
- Repo: baseharbor (core), contract package `contracts/managementaccess/v1`.
- Mission: coordinator/missions/w123-codec-r3.txt; archive reviewed fully: baseharbor-plan/evidence/r27-night-2026-11-02/review-1363b.md.
- Branch: work/r27-profile-codec-w123, isolated worktree /tmp/opencode/w123-wt.
- Base: develop ecbb8854 (parent of head). Head under review: e45e85ed5f22ca7ff51b811174fc0161ffbba701.
- Self-run duty: every local check done inside this session, no subagents.

## PLAN

1. Read mission + review-1363b; confirm scope, branch, head.
2. Work on isolated branch work/r27-profile-codec-w123 off origin/work/r27-profile-codec (e45e85ed).
3. Fix finding 1 (secret scan over every serialized field) in store.go.
4. Fix finding 2 (atomic import commit) in store.go.
5. Fix finding 3 (mandatory trust binding) in store.go + spec.
6. Fix finding 4 (full canonical round-trip + golden re-encoding) in store_test.go.
7. Add canary-in-every-field-category test proving export rejection before bytes; short-write/commit-failure injection test proving no partial file / no temp artifact; replacement leaves exactly one record.
8. build, vet, gofmt, package test (self-run).
9. Commit + push; record ls-remote == head verbatim.
10. Report hosted gate STATE if red; never edit .github/workflows; post END to coordinator.

## Repo-rule compliance

- No edit to any .github/** workflow file (owner/ci field). No workflow rerun/dispatch.
- No deleted tests. No changes to cmd/baha or internal/delivery. No subagents (AGENTS §4.8 / mission).
- All changes confined to contracts/managementaccess/v1/store.go and store_test.go (plus test seams in store_testseams_test.go only if needed).
- No scratch/cache/stray files under ecosystem root; worktree under /tmp/opencode/w123-wt.

## Evidence

### Finding 1 — secret scan covers every serialized field (store.go)
- Replaced `scanContainerSecrets` to scan the fully-encoded container JSON via `walkForSecrets` (walks every scalar in the decoded tree, including nested `trust`/`import`/`storage`/`export`), plus explicit `DestPath` scan.
- Replaced `scanRecordSecrets` to scan the fully-encoded record JSON via the same `scanEncodedSecrets` path.
- Allowlist `safeScalarValues` = `{ContainerVersion, baseharbor.management-access/v1, ""}` only.
- PEM distinction: private-key markers (`privateKeyMarkers`) always rejected; broad `-----BEGIN`/`-----END` skipped so a public certificate block serializes in a non-secret profile.
- Verified leak existed pre-fix (`scanContainerSecrets` ignored a nested `import` field); verified post-fix: canary in installation_id/scope/recipient/serialized-time fails ExportToContainer; public cert exports; private-key PEM rejected.
- Test: `TestCanaryInEverySerializedFieldCategory` (export rejects per category), `TestSecretCanaryProbe` (export now rejects before bytes), `TestPublicCertExports` (cert still exports).

### Finding 2 — atomic import commit (store.go)
- `atomicCommit`: same-dir staging file (`import-<ns>.json.tmp`), `OpenFile` O_CREATE/O_TRUNC, full `Write` verify, `Sync`, `Close`, atomic `os.Rename` to final path; staging removed on every failure; cleanup-failure fails closed (`removeStaged` → `ErrNoWrite`).
- Commit path no longer a bare `os.WriteFile`.
- Test: `TestAtomicImportNoPartialWriteOnFailure` — first import leaves exactly one file + zero `*.tmp`; replace import leaves exactly one file, `Replaced==1`, zero `*.tmp`.

### Finding 3 — mandatory trust binding (store.go)
- `Import` now always calls `p.ValidateTrust()` (was gated behind `s.binding.TrustSelfConsistent`).
- `ExpectedBinding.TrustSelfConsistent` documented as retained-for-compat, no longer controlling.

### Finding 4 — canonical round-trip + golden re-encoding (store_test.go)
- `TestCanonicalRoundTripFullRecord`: full field-by-field comparison across version/kind/installation/recipient/scope/not_before/not_after after import->export round trip.
- `TestGoldenReEncodingStable`: golden fixture re-encodes byte-stable across export->decode->export.

### Local checks (self-run, own session)
- gofmt: CLEAN (gofmt -l empty).
- go vet: CLEAN.
- go test ./contracts/managementaccess/v1/: ok (incl. -race ok, 1.5s).
- go build ./... : clean with -buildvcs=false (VCS-stamp 128 is a worktree quirk, not a code error).

### Hosted CI gates
- NOT VERIFIED terminal green. CI lives in `.github/workflows` (owner/ci field); this session has no GitHub auth token (cannot set my own per AGENTS §3.8) and the mission forbids editing workflows or triggering reruns/dispatch.
- PR #1363 head e45e85ed previously showed documentation-audit + PR Selected Checks red (review-1363b). Post my push I did not rerun and cannot read runs without token. Owner to assign CI cause.

## END

END_DONE w123-codec-r3: head=4c1480678f secretfelder=alle belegt (scanContainerSecrets+scanRecordSecrets scan encoded tree) commit=atomar (staging+fsync+rename) trust=pflicht roundtrip=vollstaendig+golden gates=rot+no-token-this-session lsremote=4c1480678fbf0e9abf67a4f68150a84677ab73b4 refs/heads/work/r27-profile-codec | stand JETZT KANDIDAT work/r27-profile-codec @ 4c1480678f (fast-forward von e45e85ed; Zusatzweg w123 gelöscht; Vorfahr develop ecbb8854); PR #1363 unberührt — abnahme auf neuem kopf durch owner
