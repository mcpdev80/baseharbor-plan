# PR #1832 — Round 2 state (worker w126-0428-290-pr1832-worker)

Date: 2026-11-24 (host clock)

Verified via `gh` authenticated API (token `gho_*`, scopes `gist,read:org,repo`; anonymous core
rate limit was exhausted and this session switched to `gh`).

## Reality witnesses (verified this round)

- PR #1832 head: `cac4db0095ef93f98693cfa084c485e01ee5b760`, state **open**.
- Candidate branch `lane-0428-290-metrics-discovery`, two new commits above handoff head `7c40e3d`:
  - `7cc823aa7` fix(0428-290): tie metrics exporter path to sole workload module (fail-closed)
  - `cac4db009` ci(0428-290): catalog metrics discovery sources for trusted plan
- Working tree of worktree `/tmp/opencode/w126-pr1832-wt` is clean; no uncommitted drift.
- Base develop is `145b4a20f`; the branch already integrated the later develop tip via normal merge
  commit `07355c3e` (second parent). Do NOT re-integrate develop.

## Exact 8 uncataloged production sources (worker's real change set vs `145b4a20f`)

```
UNCATALOGED cmd/baha/app_init_detection.go
UNCATALOGED cmd/baha/app_init_prompts.go
UNCATALOGED cmd/baha/app_init_selection.go
UNCATALOGED cmd/baha/app_init_summary.go
UNCATALOGED cmd/baha/app_init_wizard.go
UNCATALOGED internal/repositoryinspect/capability_detectors.go
UNCATALOGED internal/repositoryinspect/model.go
UNCATALOGED internal/repositoryinspect/result_helpers.go
CATALOGED   cmd/baha/app_init_wizard_test.go   (already present)
```

The 9th changed source is the test file `cmd/baha/app_init_wizard_test.go`, already cataloged.

## Mapping-association fix (the blocking review finding — exporter→workload association)

`cmd/baha/app_init_detection.go` changed the gate from `if len(metricsPaths) == 1` to:

```go
if len(metricsPaths) == 1 && len(d.WorkloadServices) == 1
```

Fail-closed unless exactly one workload service **and** one proven metrics path exist, so quick init
never maps a proven exporter (Quarkus/Spring) detected in an unrelated module onto a lone sidecar
workload (e.g. Caddy). Regression test `TestGuidedQuickInitDoesNotBindCaddyToQuarkusExporter` added
in `cmd/baha/app_init_wizard_test.go`.

## CI evidence — run 45495987965 on head `cac4db009` (TERMINAL, failure)

- Jobs (32 total). Passing: `Workflow policy`, `PR · Source format`, `PR · Native gate plan`,
  `Native · native/docker/guided`, `Native · native/podman/data-capabilities`,
  `Native · native/podman/guided`, `Native · native/docker/data-capabilities`.
- **Failing: `PR · Trusted Plan`, job `138806508322`, step
  "Resolve exact immutable PR inputs using trusted base policy" — failure.** This is the catalog
  classification failure: the 8 production sources are uncataloged in develop's
  `scripts/pr-gate-coverage.json` (coverage_status=unresolved → fail closed).
- The trusted plan runs from the **develop copy**, so in-PR catalog rows (in `cac4db009`) do not
  qualify this PR. Rows must enter develop first.

## Coordinator decision pending (posted to coordinator 00d66002)

The 8 sources classify as: all surface `source.gate.atomic.docker.observability` +
`source.gate.atomic.podman.observability`, owned by `atomic/docker/observability` +
`atomic/podman/observability`. Row shape per source:

```json
{"id": "<component.id>", "path": "<file>", "surfaces": ["source.gate.atomic.docker.observability", "source.gate.atomic.podman.observability"]}
```

Rows submitted to the coordinator awaiting their call on whether they land in develop via a
separate data-only rows-PR (w124 pattern), after which this head `cac4db009` is rerun (no new head).

## Rows-PR resolved: collective PR #1836

The waiting decision is resolved. The coordinator opened a **collective data-only rows-PR
#1836** ("docs(ci): classify 13 uncataloged source rows in trusted gate catalog
(collective w124/w126/w128)"), head `e3628dd56b4a` — one PR per card discipline. All 8 of my w126
sources are confirmed present in its `scripts/pr-gate-coverage.json` change (the only file it
touches): `cmd/baha/app_init_{detection,prompts,selection,summary,wizard}.go` +
`internal/repositoryinspect/{capability_detectors,model,result_helpers}.go`. Row shape matches
my proposal (`source.gate.atomic.{docker,podman}.data.capabilities` → `atomic/{docker,podman}/data-capabilities`).

- PR #1836 CI is **GREEN** on head `e3628dd5` (run `45499188735` success); also green on
  heads `661559a3`, `c000c5db`, and the develop GC run.
- Per the coordinator's 2026-11-24 22:27Z disposition, Codex (w136, review+merge, slot 1/2) reviews
  and merges #1836 on this exact head. As of this round #1836 is still **open / not merged**.
- The trusted plan reads `scripts/pr-gate-coverage.json` from the **develop copy**, so once #1836
  merges into develop, the 8 sources become cataloged there and my existing head `cac4db009` will
  pass the Trusted Plan gate — no new head needed.

## Status

- **BLOCKED** pending the merge of rows-PR #1836 into develop. No new candidate pushed; candidate
  head `cac4db009` is final for this lane.
- After #1836 merges, rerun existing head `cac4db009` (no new head) to obtain the two exact-head
  run IDs (Docker + rootless Podman) for PR #1832 acceptance.
