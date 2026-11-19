# Fix 0428-073 / PR #1613 — lift w073-perses-alerts back onto develop (hopf-dirty)

- Mission: mission-073-hopf-dirty.md — candidate 470735c1d on refs/heads/w073-perses-alerts was "dirty" against develop (GitHub merge-conflict), stuck in review. Task: lift the candidate monotonically onto develop and make it checkable.
- Scope: ONLY lift the candidate onto develop via `git merge origin/develop`; resolve the 4 conflict files content-preserving. NO merge into develop, NO review, NO .github/scripts edit, NO security.go, NO subagent, no `-A` in worktree (only `git add <file>`), tmp under /var/tmp, host cleanup before END.
- Scope-blocked files (0428-121a, internal/observability/registry.go, internal/metrics/{prometheus_files.go,prometheus_verify.go}, cmd/baha/app_logs.go): not touched. None appeared in the conflict set.

## Base attestation / reality witnesses

- Planning repo root: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (git remote origin = https://github.com/mcpdev80/baseharbor-plan.git, HEAD main). `git ls-remote origin main` -> 3cac9ed71f219749d817f5cc5810fa6acf255609 refs/heads/main.
- Candidate fetched from baseharbor origin: `git fetch origin refs/heads/w073-perses-alerts` -> 470735c1d187d8a680ae3b0539d75f592c945110.
- Merge-base develop..candidate: 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95.
- Ancestry (before): `git merge-base --is-ancestor origin/develop 470735c1d` -> NO (dirty).
- Chain proven: candidate range origin/develop..470735c1d is a merge-commit chain (53300858e "Merge ... into w073-perses-alerts", 66ff93d1c "Merge ... into lane-0428-075-perses-seam") — NOT a rebase. `git log --merges origin/develop..w073-perses-alerts` lists exactly those two merge commits. Rebase was correctly rejected by the mission (branch already carries develop merges; rebase would replay integrated history and re-boil the manifest.go conflict storm).

## Manifest file layout check (pre-conflict)

- develop manifest files: internal/application/manifest.go, manifest_parse.go, manifest_parse_services.go, manifest_render.go, manifest_test.go, manifest_validation.go.
- candidate manifest files: identical set (same basenames, no added/renamed).
- `git diff --name-only 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95 w073-perses-alerts | grep manifest*.go` -> only manifest.go (edited, not added). No rename conflict path. Perses alert files (perses_prometheus_alerts.go) are candidate-only and absent from develop -> merge cleanly.

## Conflict list (4 files) + resolution + justification

1. internal/application/manifest_render.go (content)
   - Context: inside `if m.Services.ObservabilityManagementUI { b.WriteString("  observability:\n") ... }`.
   - HEAD side: `writeManagementUIYAML(&b, true)` (hardcoded).
   - develop side: `writeManagementUIYAML(&b, m.Services.ObservabilityManagementUI)`.
   - Resolution: keep develop side. Rationale: the manifest schema passes the per-surface `ObservabilityManagementUI` field through; hardcoding `true` would (a) ignore the declared field and (b) be inconsistent with all other management-UI renders in this file that pass the field. The develop value is the correct, data-driven choice. Function preserved on both sides.
2. internal/application/manifest_test.go (add/add)
   - HEAD side: empty block.
   - develop side: 3 new perses-selection round-trip tests (TestManifestPersesSelectionRoundTripWithoutManagementUI, ...WithManagementUIStill, ...IgnoredWithoutManagementUIAndPerses).
   - Resolution: keep develop side (add the 3 tests). These tests assert the same fail-closed perses-selection contract the candidate already carries; they are additive and belong on the candidate. Function preserved; nothing removed.
3. internal/capability/perses.go (add/add, comment block)
   - HEAD side: richer r2->r4 rationale (references act-luna-1575-r1.md, PR #1575, Luna REQUEST_CHANGES).
   - develop side: concise rationale for the same point.
   - Resolution: keep HEAD side (richer, authoritative rationale; both are true and complementary). Comment-only, no behavior change.
4. internal/metrics/perses_contract_test.go (add/add, comment block)
   - HEAD side: richer r2->r4 rationale (r2 wrongly moved onto IntegrationDescriptor; r4 replaced with management-tool/surface contract).
   - develop side: concise rationale.
   - Resolution: keep HEAD side (richer, authoritative). Comment-only, no behavior change.

## Local checks (in worktree /var/tmp/w073-wt, head d8838f622b551cdc8a7f8e8320c3f122b2ae5783)

- gofmt -l . -> empty (all 4 files formatted).
- go build ./... -> BUILD_EXIT=0.
- go vet ./... -> VET_EXIT=0.
- go test ./internal/application/ -> ok 5.719s (APP_EXIT=0).
- go test ./internal/metrics/ -> ok 0.210s (METRICS_EXIT=0).
- go test ./internal/application/ ./internal/metrics/ -run 'Manifest|Perses|ManifestParse|ManifestRound|ManifestObserv|ManifestPers' -> ok; all perses_alerts fail-closed evaluator/health tests + manifest round-trip tests PASS (full output above in akte via test runs).

### cmd/baha package failures (pre-existing, NOT introduced by this change)

- go test ./cmd/baha/ -> FAIL 564s. Three FAIL markers:
  - TestAppEditCommandCompleteProviderEditRunsRealLifecycle (app_edit_apply_test.go:1253): needs a real Docker engine / protected Core backend owner — unavailable in this host.
  - TestPrepareStagedCoreGitCandidatePinsCanonicalApplication (management_core_git_candidate_test.go:49): "native Git archive failed: signal: killed" — Git-archive OOM in host.
  - TestRuntimeUpRequiresORASBeforeCoreBootstrap (oras_setup_test.go:80): ORAS not installed ("container runtime orchestration not found").
- These 3 are environment/runtime failures. Proven pre-existing: on clean origin/develop baseline worktree (/var/tmp/w073-baseline, HEAD da76c5cf9), the same three FAIL identically (TestAppEditCommandCompleteProviderEditRunsRealLifecycle 31.5s, TestPrepareStagedCoreGitCandidatePinsCanonicalApplication killed at 60s, TestRuntimeUpRequiresORASBeforeCoreBootstrap ORAS-not-found). None of the three touch the 4 edited files (manifest_*, perses.go, perses_contract_test.go). The only failing test that references a touched file (perses.go) is TestAppEditCommand... and it fails on engine-owner, not on perses.go. My edited files compile (go build/vet clean) and their packages pass.

## Ancestry witness after merge (in worktree)

- git merge-base --is-ancestor 470735c1d d8838f622 -> YES.
- git merge-base --is-ancestor origin/develop d8838f622 -> YES (monotonic).
- git log --oneline origin/develop..d8838f622 lists ONLY the w073 merge-commit chain + the new merge commit d8838f622 (no foreign candidate commit carried on top).

## Push witness

- git push origin refs/heads/w073-perses-alerts (no force) -> 470735c1d..d8838f622  w073-perses-alerts -> w073-perses-alerts, PUSH_EXIT=0.
- git ls-remote origin refs/heads/w073-perses-alerts -> d8838f622b551cdc8a7f8e8320c3f122b2ae5783 (CONFIRMED on remote).

## CI

- Run ID 44491028219 (commit d8838f622b551cdc8a7f8e8320c3f122b2ae5783, PR #1613, branch w073-perses-alerts, base develop da76c5cf9).
- gh api .../check-runs: total 30 check runs. All "PR · Draft Go" jobs terminal SUCCESS (5/5): cli-0, cli-1, cli-2, cli-3, packages. No failure.
- The other 25 runs are release/pre-release/targeted gates (skipped, not applicable to a Draft Go PR) — not relevant to this hopf-dirty fix.
- Terminal SUCCESS witness captured via gh api check-runs (all in_progress resolved to conclusion=success; 0 failed).

## Host hygiene

- docker ps -a / podman ps -a: no containers started by this lane (no runtime test run). cleanliness: PASS.
- Worktrees: /var/tmp/w073-baseline removed after baseline comparison; /var/tmp/w073-wt retained for END.

## revision-labels

- hopf-dirty fix, w073-perses-alerts, 0428-073, PR #1613.
