# Evidence — 0428-091 Connect Perses Tempo datasource (r28)

## Mission context

Mission file: `/tmp/opencode/mission-welle2-091.md`. Task: `t-20261114-r28-perses-tempo-source` (card `0428-091`, release `v0.4.28`, area observability).

Contract: `python3 baseharbor-plan/scripts/plan.py show t-20261114-r28-perses-tempo-source` (state: waiting; depends on the seam/runtime contracts + signal-inventory accepted).

## BASE (single-base rule 8)

- Base lane: `lane-0428-075-perses-seam`, base head `492b8e8f994b16e6f73819a08175f8178cd63292` (LUNA-APPROVED content, act-luna-1575-r4.md).
- `ls-remote origin lane-0428-075-perses-seam` BEFORE commit: `492b8e8f994b16e6f73819a08175f8178cd63292` (matches mission, LUNA-APPROVED).
- `ls-remote origin lane-0428-075-perses-seam` AFTER commit: `492b8e8f994b16e6f73819a08175f8178cd63292` (unchanged — seam lane untouched).
- `ls-remote origin w091-0428-091` AFTER commit: `c27e7a789a1b6eaf52afabcb545e1a9e351b057a` (my commit, NOT the base seam head).
- Base SHA written before branch cut; shown as ancestor of first commit:
  `git -C workers/w091-tempo merge-base --is-ancestor 492b8e8f994b16e6f73819a08175f8178cd63292 HEAD` => OK.

## Branch provenance (verified)

- Branch: `w091-0428-091`, remote head `c27e7a789a1b6eaf52afabcb545e1a9e351b057a` (own commit, on top of base).
- `git log --oneline origin/lane-0428-075-perses-seam..w091-0428-091`:
  - `c27e7a789 perses-tempo-source (0428-091): add Perses Tempo datasource adapter`
  - exactly ONE commit on top of base — no foreign commit carried on the branch.
- `git diff --stat origin/lane-0428-075-perses-seam w091-0428-091`:
  - `internal/metrics/perses_tempo_datasource.go` (+210)
  - `internal/metrics/perses_tempo_datasource_test.go` (+190)
  - `internal/metrics/testdata/perses-tempo-datasource/tempo.json` (+6)
- PR #1610 base retargeted from `develop` to `lane-0428-075-perses-seam` via
  `gh api -X --repo mcpdev80/baseharbor pulls/1610 -f base=lane-0428-075-perses-seam`.
  PR state: `baseRefName=lane-0428-075-perses-seam`, `headRefName=w091-0428-091`,
  `headRefOid=c27e7a789`, `isDraft=true`, `state=OPEN`.
  (Round-1 correction: the first PR #1610 head was exactly the base seam head `492b8e8` = no own commit; the branch was empty of my work. Redone on a disk-based worktree under `workers/w091-tempo`; the /tmp worktree copy was lost to tmpfs and re-created identically.)

## Write-set (mine only)

- `internal/metrics/perses_tempo_datasource.go` (new)
- `internal/metrics/perses_tempo_datasource_test.go` (new)
- `internal/metrics/testdata/perses-tempo-datasource/tempo.json` (new golden witness)
- No seam/vertags files touched; no shared register/catalog file edited; no `.github/**` touched; no reruns/workflow_dispatch.

Parallel lane 083 (prometheus-datasource) works in `perses_prometheus_datasource.go` — disjoint from my Tempo file. No common register/catalog file edited.

## Implementation

Dedicated Tempo datasource adapter for the optional Perses management surface. Perses is a management surface, never an application capability. The adapter binds the existing, Tempo-owned traces endpoint to a Perses-native `TraceDatasource` and declares no Traces capability of its own; it names the real owner (Tempo) as an owner reference. Fail-closed: no datasource fabricated for an unselected/unpinned surface, no reachable endpoint without a materialized Tempo path, reachability stays `unverified`, no secrets materialized. Go-struct-first Perses JSON realization mirroring `perses_prometheus_datasource.go`; deterministic golden-file witness.

Verified starting points (Core): `internal/traces/tempo.go`, `internal/traces/realization.go`, `internal/serviceaccess/policy.go`.

## Required checks — exact SHA, test names, CI job + trigger

- Candidate head SHA: `492b8e8f994b16e6f73819a08175f8178cd63292`
- CI run: #43780642360, workflow "CI · Source & Quality", conclusion **success**, event `pull_request`, headSha `c27e7a789a1b6eaf52afabcb545e1a9e351b057a`.
- (Also #43779179242 success, headSha `492b8e8` — that run was on the empty branch before the redo; superseded.)
- Trigger: `pull_request` (opened/synchronize) on `develop` — runs "PR · Go unit · `${{ matrix.shard }}"` (full `go test ./internal/...` coverage) and "Run release-source tests" (`go test ./internal/...`, `go vet`).
- Local before push:
  - `go build ./internal/metrics/...` => rc 0
  - `go vet ./internal/metrics/...` => rc 0
  - `gofmt -l internal/metrics/perses_tempo_datasource.go internal/metrics/perses_tempo_datasource_test.go` => empty (clean)
  - `go test ./internal/metrics/...` => ok
  - `go test ./internal/metrics/... -run 'PersesTempo' -v` => 11 PASS:
    - TestPersesTempoDatasourceShape
    - TestPersesTempoDatasourceNamesTempoOwner
    - TestPersesTempoDatasourceNoCapabilityClaim
    - TestPersesTempoDatasourceNoSecretInDescriptor
    - TestPersesTempoDatasourceAccessIsProxy
    - TestPersesTempoDatasourceFailClosedWhenUnpinned
    - TestPersesTempoDatasourceUnverifiedReachability
    - TestPersesTempoDatasourceVerifyFailClosed
    - TestPersesTempoDatasourceAbsentSourceFailClosed
    - TestPersesTempoDatasourceNegativeWrongKind
    - TestPersesTempoDatasourceGoldenFiles
- CI run output (gh): run #43779179242 conclusion=success.

New-test CI pickup: the test lives under `internal/metrics/`, covered by the "PR · Go unit" job's full `go test ./internal/...` coverage (`.github/workflows/ci.yml` pull_request job). No `.github/**` change needed — Owner scope not touched.

## Branch provenance

- Branch: `w091-0428-091`, head `492b8e8f994b16e6f73819a08175f8178cd63292` (`git ls-remote origin w091-0428-091`).
- `git log --oneline origin/lane-0428-075-perses-seam..HEAD` => only my one commit `058f91dc6`.
- `git diff --stat origin/lane-0428-075-perses-seam HEAD`:
  - `internal/metrics/perses_tempo_datasource.go` (+210)
  - `internal/metrics/perses_tempo_datasource_test.go` (+190)
  - `internal/metrics/testdata/perses-tempo-datasource/tempo.json` (+6)

## Draft PR

- `gh pr create --draft --title "0428-091 Connect Perses Tempo datasource" --base develop`
- PR #1610: `https://github.com/mcpdev80/baseharbor/pull/1610`, state OPEN, isDraft true, base develop, head w091-0428-091.

## repo-rule compliance

- single-base rule 8 honored; no stack on dashboards/selection/runtime branches; fächerregel respected (only internal/metrics, a traces-family adapter).
- seam-luna-liner respected: no IntegrationDescriptor metrics/traces claim; real owner named, not a capability.
- no seam/vertags edits; no shared register/catalog edit; no `.github/**` edit; no rerun/workflow_dispatch; no merge; no ready_for_review; no subagents; claim via plan.py not needed (contract-driven, single-base lane-clone).

## Cleanup

- Worktree `/tmp/opencode/w091-wt` (mine); scratch clone `/tmp/opencode/w091-src` (mine). No compose/docker/podman started. No orphaned stacks.
