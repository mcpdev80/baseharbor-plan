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

## Catalog fix (814/800 readability gate + trusted coverage) — ROOT-CAUSED, OWNERSHIP DECISION PENDING

### root-cause (definitive, run 45491333208 at exact head 3926495324)
The CI "Trusted Plan" step (.github/workflows/ci.yml:856-868) sets
`controller=$effective_base` and reads `scripts/pr-gate-coverage.json` from
`$controller:scripts/` (ci.yml:860-866). For PR #1833 the PR base is develop
(145b4a20f), so `effective_base=145b4a20f` and the migration controller
(8596548) IS an ancestor of develop -> `controller=145b4a20f`. Therefore the
runner reads the coverage file from **develop**, NOT from my PR head. My PR's
catalog rows are structurally ignored.

Verified: develop (145b4a20f) has 278 component rows and ZERO of the three
sources; 14 existing internal/application/*_test.go rows ARE catalogued, so
test-file cataloguing is the norm. My local planner run against the current
head diff reports coverage_status=resolved, unresolved_coverage=[],
selected_gates=[atomic/docker/data-capabilities]; the runner reads develop's
stale file -> source_unowned=[manifest_validation.go, workload.go,
workload_test.go] -> ValueError.

### what is already in place (verified, data-only, decision-authorized)
- canonicalComposeServiceID relocated from workload.go (787 lines) into
  manifest_validation.go; source-format gate GREEN.
- PR #1833 head 3926495324 carries the 3 catalog rows with {id,path,surfaces}
  = source.gate.atomic.{docker,podman}.data.capabilities (decision RECORDED on
  card 0428-288, 2026-11-24).
- No scripts code, gate-behavior, or .github change.

### Owner decision needed (out of scope / Owner scope)
Rows must reach develop for the trusted-plan step to read them. Two options:
(a) Owner merges PR #1833 so the rows enter develop, then a fresh exact-head CI
    run reads the resolved catalog; or
(b) Owner adds the 3 rows to develop directly.
No other scripts/** or code change is authorized by the decision. No merges by
this lane. PR #1833 stays DRAFT until Trusted Plan is green.

## END STATE (final, 2026-11-24)
END_BLOCKED w124-0428-288-compose-ids. Run 45491333208 at exact head 3926495324
reran against my committed tree and STILL failed with the same source_unowned
ValueError. CI step .github/workflows/ci.yml:859-867 reads
scripts/pr-gate-coverage.json via `git show "$controller:scripts/..."` where
controller=$effective_base=develop (migration controller 8596548 IS ancestor of
develop). develop's coverage registry has ZERO of my three rows. My PR rows are
structurally invisible to this step. Everything else done: canonicalComposeServiceID
relocated (workload.go 787 lines, source-format GREEN); 3 decision-authorized rows
{id,path,surfaces}=data.capabilities in PR #1833 head 3926495324 (data-only, no
scripts/**/code/.github change). Local planner with rows: coverage_status=resolved.
DECISION NEEDED (Owner scope): rows must enter develop — (a) Owner merge PR #1833
then fresh exact-head CI resolves, or (b) Owner adds rows to develop directly. This
lane will NOT merge or touch develop; PR #1833 stays OPEN/DRAFT pending green
Trusted Plan. No other scripts/** or code change authorized by the card decision.

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

