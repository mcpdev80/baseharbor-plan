# 0428-075 seam round-3 (mission-seam-r3.md) — source-readability split + Perses contract test alignment

ROLLE: WORKER (flash lane, 0428-075 r3 correction, mission-seam-r3.md)

Namenshinweis: dies ist die r3-KORREKTURRUNDE der Mission (Base cb4367f347). Die Datei `evidence/r28-welle1-2026-11-14/perses-contract-seam/round-3.md` (head c195a9a20) ist eine ÄLTERE Runde auf früherem Base — nicht verwechseln; dieser Akt schreibt den PR-Head auf 293e0e05a fort.

## PLAN

1. Verify candidate head via ls-remote (lane-0428-075-perses-seam = cb4367f347) and use the dedicated worktree at that head.
2. Bring internal/application/manifest_parse.go under the 800-line limit by a behaviour-identical extraction (no comment/whitespace tricks).
3. Rewrite internal/metrics/perses_contract_test.go:52 (TestPersesIsNotAnApplicationCapability) against the NEW r2 contract state: Perses = management surface (valid IntegrationDescriptor bound to the observability owner), NOT an application capability; intent preserved, assert rewritten, not deleted.
4. Run go build ./..., go vet, gofmt, targeted Perses tests and the manifest-grammar test group; record outputs literally.
5. Prove extraction equivalence head-vs-base with a temporary comparison harness (not committed).
6. Commit + push on lane-0428-075-perses-seam; write this evidence; publish to planning origin/main; post END with the new head.

## Reality witnesses (measured via ls-remote)

- Before work: `git ls-remote origin lane-0428-075-perses-seam` →
  `cb4367f347ed587cb84c67a14b47ffaa3505a5dd  refs/heads/lane-0428-075-perses-seam`
- Worktree: /tmp/opencode/lane-0428-075-perses-seam-wt, HEAD == origin head cb4367f347, clean.
- After push: `git ls-remote origin lane-0428-075-perses-seam` →
  `293e0e05ac04716e441a72679704cbfcc38d6e0e  refs/heads/lane-0428-075-perses-seam`
- Commit 293e0e05a "fix(0428-075): split manifest service grammar below 800 lines; align Perses contract test with r2 descriptor (r3)" — parent cb4367f34 (verified via git log). 3 files changed, +137/−99.

## Fix 1 — manifest_parse.go under 800 lines

- Failing check (run 43766612514): "internal/application/manifest_parse.go has 821 lines (limit: 800)".
- Extraction: `parseServiceField` (the services-section field grammar, the code path that carries the Perses `perses: true|false` seam keys and the management-ui/enabled switches) moved verbatim from manifest_parse.go into the new file internal/application/manifest_parse_services.go, same package.
- Sizes after: manifest_parse.go = 729 lines, manifest_parse_services.go = 103 lines. `bash scripts/source-readability-audit.sh` → all PASS (file size / function span / regression ratchet).
- Behaviour-identical proof (not a claim, a measurement): a temporary harness walked every *.yml under testdata/ and internal/application/ through ParseYAML and ran three grammar cases (services round trip incl. `perses: true` + sql instances; `perses` under sql rejected), executed identically on the base head cb4367f347 and on the r3 tree. `diff` of both outputs → EQUIV-IDENTICAL:
  - `scanned=4 parsed=0 rejected=4 other=0`
  - `rt perses=true obsui=true sql=true sqlinst=map[primary:{}]`
  - `bad-rejected: line 7: perses is only valid under observability`
- The harness file was kept outside the product branch (/tmp/opencode/equiv/main.go) and removed from the worktree immediately; `git status` clean before commit.

## Fix 2 — internal/metrics/perses_contract_test.go:52

- Old assertion (pre-r2 state): `len(desc.Capabilities) == 0` and `desc.Validate()` must FAIL. After r2, PersesManagement is a valid IntegrationDescriptor bound to the observability owner (Metrics + MetricsV1.ID), so the old expectation fails on the candidate — exactly the red of run 43766612514.
- New assertion, same INTENT (Perses = management surface, NOT an application capability), rewritten not deleted:
  1. `desc.Validate()` PASSES at its intended boundary (the r2-rezept positive against-test);
  2. it binds exactly one capability kind, the observability owner `capability.Metrics`, and exactly the versioned `capability.MetricsV1.ID` — no fake metrics/logs/traces application capability;
  3. `EffectiveServices()` yields exactly `[observability]` — never an application service surface;
  4. fail-closed catalog membership: `capability.PersesProviderKind` never appears in `capability.ReferenceIntegrations()`.

## Verification outputs (literal, from this worktree on the exact r3 tree)

- `go build ./...` → exit=0 (no output).
- `go vet ./internal/application/... ./internal/metrics/... ./internal/capability/...` → exit=0 (no output).
- `gofmt -l internal/application internal/metrics internal/capability` → no output.
- `go test ./internal/metrics/... ./internal/capability/... -run Perses -v` → all PASS:
  - metrics: TestPersesReleaseIsPinnedAndCurrent, TestPersesManagementSurfaceFailClosedWhenUnprovisioned, TestPersesReleaseVersionIsRealizationMetadataNotProviderVersion, TestPersesIsNotAnApplicationCapability (the rewritten one) — `ok github.com/mcpdev80/baseharbor/internal/metrics 0.006s`
  - capability: TestValidatePersesReleaseFailClosedWithoutPin, TestValidatePersesReleaseRejectsUnknownAuthClass, TestPersesDefaultReleaseValidates, TestPersesIsManagementSurfaceNotApplicationCapability, TestPersesManagementIsAValidIntegrationDescriptor, TestPersesManagementNotRegisteredAsCapabilityProvider — `ok github.com/mcpdev80/baseharbor/internal/capability 0.003s`
- `go test ./internal/application/... -run 'Manifest|YAML|Parse' -v` → 29 tests PASS, `ok github.com/mcpdev80/baseharbor/internal/application`.
- `go test ./internal/application/ -run Perses -v` → TestManifestPersesManagementUIRoundTripFailsClosedWithoutMetrics, TestManifestPersesSelectionRequiresPinnedRelease PASS.
- `bash scripts/source-readability-audit.sh` → Go file size PASS / Function span PASS / Regression ratchet PASS.
- Note: `go test ./internal/application/...` (full package) shows three FAILs (TestSharedBackend* / TestStandaloneSharedPostgres*) that reproduce IDENTICALLY on the untouched base head cb4367f347 (verified by stash/compare in this worktree) — base-side, outside this mission's two candidate-side points; documented as a finding, not masked.

## Repo-rule compliance

- Write set: internal/application/manifest_parse.go, new internal/application/manifest_parse_services.go (same package, per mission), internal/metrics/perses_contract_test.go. Nothing else.
- No .github/** edits, no merge, no ready_for_review, no subagent (§4.8). Own execution and own-run watching per §4.6.
- No features/docs changed; Perses reachability stays unverified; behaviour identical (proven above).
- Cleanliness: no containers, networks, volumes or state dirs created (pure compile/test work); before/after: this host's ambient containers untouched; worktree left clean at pushed head 293e0e05a, temp harness removed.

## Hosted CI (own-run watch, §4.6)

- Push triggered PR run "CI · Source & Quality" run-id 43768376429 on 293e0e05a — in progress at the time of writing this file; terminal outcome and test names are appended below in the follow-up section of this act (or the END post if the run completes first).

## END

- New candidate head: 293e0e05ac04716e441a72679704cbfcc38d6e0e (ls-remote verified above).
