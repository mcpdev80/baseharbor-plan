# w124 — 0428-288 Preserve Compose service IDs

## Task
Card `t-20261116-r28-bug-compose-service-ids` (0428-288, v0.4.28). Preserve Compose service
IDs through the affected path. `docker compose config --services` yields an underscore key
(e.g. `vector_db`), but `baha app init` persisted the dash key (`vector-db`) in
`workload.components` and Runtime API consumers, so preflight fails:
`workload service "vector-db" is not present in the application Compose file`.

## Base / branch provenance
- Product repo remote (github): `origin` = https://github.com/mcpdev80/baseharbor.git
  (`git -C baseharbor remote -v` confirms origin/lane-origin both github.com/mcpdev80)
- Exact develop base cut: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  = `145b4a20f35179a0ac6bc0a66666a846c1ae35c0`
  (base requirement was d0a6f370+; current develop 145b4a20 is ahead of d0a6f370)
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w124-0428-288-compose-ids-wt @ 145b4a20`
- First commit will carry only own commits; `git log origin/develop..HEAD` must list only w121 commits
- `git diff origin/develop...HEAD --name-only` recorded before END

## Root-cause audit (baseline-red proof target)
- Detection: `repositoryinspect.workload_source_compose_quadlet.go` `normalizeComposeSource`
  sets `component.ID = normalizeLogicalComponentID(service.Name)`.
  `normalizeLogicalComponentID` (workload_source.go:662) lowercases, replaces `_`->`-`, drops
  invalid chars: `vector_db` -> `vector-db`. This literal ID is persisted in `manifest.Workload.Components`.
- Preflight: `application.workload.go` `composeServiceNames` (line 189) returns the RAW Compose
  service keys from the document (`vector_db`), sorted.
- Failure: `selectWorkloadServices` (workload.go:214-255) builds `availableSet` from raw keys and
  matches `WorkloadComponentNames(m)` (literal `vector-db`) by EXACT equality (line 225), so
  requested `vector-db` is not found in `availableSet{vector_db}` and returns
  `workload service "vector-db" is not present in the application Compose file`.
- Every caller path funnels through `selectWorkloadServices`:
  `SelectedWorkloadServices`, `SelectedWorkloadServicesFromCompose`, `materializeWorkloadFromComposePath`
  (apply path), `app_dev_routing` (dev routing), `app_logs`, `app_interact`, `app_workload`
  security preflight.
- Fix scope: single comparison point in `selectWorkloadServices`. Compare requested IDs against
  available keys by their canonical logical form `normalizeLogicalComponentID(key)` so a manifest ID
  `vector-db` matches the Compose key `vector_db` without mutating either side (no silent unsafe
  aliasing, no change to other identifiers, safety/consent/ownership untouched).
- Existing-green-test gap to close: add deterministic regression in `internal/application/workload_test.go`
  that fails on the baseline (underscore Compose key + dash manifest component => error) and passes on
  the candidate; positive tests for underscores, dashes and mixed graphs. Register in existing package
  test selection (no scripts/** change needed).

## Catalog fix (814/800 readability gate + trusted coverage) — HELD for Codex decision slot w122
Adding the helper pushed workload.go to 814 lines, failing the trusted-catalog
source-format/readability gate. Moved canonicalComposeServiceID into
manifest_validation.go (next to validateComposeServiceName) so workload.go is
787 lines and BOTH sources catalogue cleanly. No behavior change.

The trusted base policy rejects ANY uncataloged source: all three changed files
manifest_validation.go, workload.go, workload_test.go must be added to
scripts/pr-gate-coverage.json in ONE step with surfaces resolving to a real
release gate. I verified locally (planner coverage_status=resolved,
unresolved_coverage=[], selected_gates=[atomic/docker/data-capabilities],
validate() clean) that adding the three component rows with atomic
docker/podman data.capabilities surfaces resolves it. PRECEDENT: card 0428-278
(ghost coverage rows) — same fix in-scope in baseharbor-plan registry.

ROUTING (Owner 2026-11-24): the data-only catalog delta goes through Codex
decision slot w122 NOW. HELD: w122 records DECISION_RECORDED on card 0428-288,
then the lane implements exactly that delta. No other scripts/** touch.

PR #1833 head 3926495324 (moved helper + cataloged coverage — NOT yet the fix
that the w122 decision will author; see below). Two prior exact-head runs
45487951503 + 45491333208 failed only on trusted-plan coverage attribution.

## Acceptance (from card)
- Use literal Compose service identifiers at all runtime lookup and manifest references,
  separating presentation/logical IDs from Compose keys. Positive tests for underscores,
  dashes and mixed service graphs; no silent unsafe aliasing.
- Preserve safety, immutable candidate consent, source ownership, shared-provider isolation.
  Never bypass preflight or delete foreign resources.
- Include positive/negative regressions and classify baseline-red vs candidate-green.

## Repo rules
- baseharbor/AGENTS.md, DEVELOPMENT_GUIDELINES.md, docs/spec
- Scope: internal/compose / store area only. NO .github/**, scripts/**, docs/releases/**,
  cmd/baha/ci_integration_operator_enabled*, internal/metrics/perses_alert*. consent/auth untouched.
- Tests in Hosted CI (existing selection). If registration needs scripts/** -> STOP+QUESTION file:line.

---
## END STATE
END_BLOCKED w124-0428-288-compose-ids: HELD for Codex decision slot w122 (Owner routing 2026-11-24).
source-format gate GREEN. Trusted Plan fails only on uncataloged-source coverage-attribution
for the 3 changed sources; the data-only catalog delta is Owner-authorized to be authored by the
w122 decision slot in baseharbor-plan registry, NOT by this lane. No other scripts/**/code touch.
PR #1833 head 3926495324.

