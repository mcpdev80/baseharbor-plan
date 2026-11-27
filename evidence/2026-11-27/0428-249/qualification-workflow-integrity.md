# Qualification evidence workflow integrity — 2026-11-27

## Owner disposition — qualification evidence workflow integrity (2026-11-27)

This is an existing-card disposition for 0428-249, because the decisions below are prerequisites for a trustworthy #1812 qualification. Implementation is by the worker lane on 0428-249, Owner-authorized; `.github` changes are limited exactly to this edit set. This is the named-card exception in coordinator/RUNBOOK.md §4.0, line 251. The Owner's global scope covers every evidence-producing qualification, gate, and acceptance workflow, including the `PR Selected Checks` graph in `ci.yml`.

### Decisions

1. Evidence-producing runs must not be cancelled by a newer event. Set `cancel-in-progress: false` for all qualifying workflows below. A cancelled run cannot be cited as completed qualification evidence.
2. Concurrency identity must include the immutable, verified candidate commit SHA, never the branch/ref name. Include gate/runtime identity and `github.run_id` so independent jobs and distinct evidence events do not evict each other. For an input such as `inputs.ref`, resolve it to a full 40-hex commit before a gate is admitted, assert the checkout's `git rev-parse HEAD` equals that SHA, and use that verified SHA in the gate-level group. Workflow-level expressions cannot read a later job's output: an orchestrator whose input may be a branch/tag must use a unique non-cancelling run group, while each evidence job uses the resolved SHA. A branch-shaped input must not be treated as a verified SHA.
3. A single long Podman job is not independent evidence when it bundles unrelated acceptance assertions. Split the Podman `single_default_native` job into independently named/checkable jobs for (a) single-default SQL/Secrets, (b) Node HTTPS enrollment/remote CLI, (c) install destroy/interrupted retry, and (d) pinned-workload lifecycle/backup. Each job must check out and attest the same immutable candidate SHA, run its own required setup/cleanup, and fail independently. `podman-acceptance.yml:106-175` currently bundles all four; the separate `keycloak_single_native` job at `:62-104` is already distinct and must remain distinct. The configured timeout of `keycloak_single_native` is 22 minutes and `single_default_native` is 65 minutes; the source does not establish an observed 24-minute duration. The required structural correction is the four-way split of the bundled evidence regardless of wall time.

### Exact workflow edit set (current `origin/develop` witnesses)

For evidence jobs, the required group shape is `bh-evidence-${{ <verified-head-sha> }}-${{ <gate/runtime-id> }}-${{ github.run_id }}`; use the actual gate/runtime expression available at that workflow/job. Keep independent matrix jobs separate by gate/runtime. Where a workflow has no current concurrency block, add a **job-level** block after immutable SHA resolution; do not create a static workflow-wide lock.

| Workflow and current lines | Current state | Required edit |
| --- | --- | --- |
| `.github/workflows/ci.yml:24-26` | `ci-${{ github.ref }}`; cancel `true`. The same run contains `PR Selected Checks` (`:1552-1577`) and selected jobs. | `group: ci-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`. Keep the aggregator and selected evidence jobs in the same non-cancelling candidate run. |
| `.github/workflows/docker-runtime-acceptance.yml:24-26` | workflow/ref group; cancel `true`; `inputs.ref` may be a ref and is checked out at `:189`. | Run-unique orchestrator group + resolver job. Each evidence job listed in the correction appendix uses the resolver's verified SHA output, a literal job/gate/runtime identity, run ID, and `cancel-in-progress: false`; exact checkout assertion required. |
| `.github/workflows/podman-acceptance.yml:23-25` | workflow/ref group; cancel `true`; `inputs.ref` may be a ref and is checked out at `:191`. | Run-unique orchestrator group + resolver job. Each evidence job, including the four split single-default jobs, uses the resolver's verified SHA output + its own job/gate identity + run ID, and `cancel-in-progress: false`; exact checkout assertion required. |
| `.github/workflows/host-trust-owned-e2e.yml:23-25` | group uses PR number or `github.ref`; cancel `true`. | `group: host-trust-owned-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`; `cancel-in-progress: false`. |
| `.github/workflows/mcp-lifecycle-acceptance.yml:28-30` | workflow group includes ref/input; cancel `true`; Docker/Podman checkout at `:48` and `:91`. | Replace with a run-unique non-cancelling orchestrator group; add `resolve_candidate`, then per-runtime job groups using `needs.resolve_candidate.outputs.candidate_sha` + runtime + run ID, cancel `false`; check out and assert that exact SHA. |
| `.github/workflows/nextjs-greenfield-e2e.yml:13-15` | workflow group uses PR number/ref; cancel `true`; candidate checkout input at `:77`. | Replace with run-unique non-cancelling orchestrator group; `resolve_candidate` emits verified SHA; `nextjs-docker` and each `greenfield-native` matrix job depend on it and use SHA + job/stack/runtime + run ID, cancel `false`; checkout/assert the output SHA. |
| `.github/workflows/observability-acceptance.yml:33-35` | workflow group contains ref/input; cancel `true`; Docker/Podman jobs checkout input at `:59` and `:141`. | Replace with run-unique non-cancelling orchestrator group; add `resolve_candidate`; Docker and Podman jobs depend on it and use resolver SHA + runtime + run ID, cancel `false`; checkout/assert output SHA. |
| `.github/workflows/targeted-integration.yml:51-64` | workflow-level key uses `github.ref` and raw `inputs.ref`; dispatch allows branch/ref input. The resolver output does not exist at workflow-concurrency evaluation time. | Exact resolver/job-level before/after pattern below: use a run-unique non-cancelling workflow group, resolve `inputs.ref || github.sha` to `needs.resolve_candidate.outputs.head_sha`, then key every evidence job by that SHA + gate/runtime + run ID. No raw `inputs.ref` in any concurrency key. |
| `.github/workflows/pre-release.yml:6-8` | cancel already `false`; group is either a run ID in develop mode or one global static `baseharbor-release-qualification` lock. Candidate SHA is resolved in `source_prepare` (checkout `:50`, checks around `:75-91`). | `group: pre-release-orchestrator-${{ github.run_id }}`; keep `cancel-in-progress: false`. Orchestrator is unique per run; each evidence-producing reusable gate call after resolution must key by `${{ needs.source_prepare.outputs.candidate_sha }}-${{ matrix.runtime }}-${{ matrix.gate }}-${{ github.run_id }}`. Never use branch/tag input as the evidence key. |
| `.github/workflows/pre-release-runtime-suite.yml:81-126, 661-705` | The existing step validates and checks out raw `inputs.ref` (`:81-115`) and then records `git rev-parse HEAD` (`:122-126`); the gate job has no resolver-job output or SHA-based concurrency. | Exact resolver-job before/after pattern below: add `resolve_candidate` that emits a full 40-hex `head_sha`; make `gate` depend on it, checkout that output, assert `HEAD == head_sha`, and key by output SHA + runtime + gate + run ID. Never use raw `inputs.ref` in the key. |
| `.github/workflows/targeted-demo-acceptance.yml:48-50` | cancel `false` already; static `baseharbor-release-qualification` lock. Its `resolve` job produces the tested SHA at `:55-62`, so workflow-level concurrency cannot use that output. | `group: targeted-demo-orchestrator-${{ github.run_id }}`; keep cancel `false`. Each downstream evidence job must use `needs.resolve.outputs.ref` + gate/runtime + run ID in its job-level group, after the resolver validates the exact commit. |
| `.github/workflows/runtime-broker.yml:6-20, 25-37, 321-325` | Acceptance/performance jobs accept branch-shaped `inputs.ref`; no resolver or concurrency. | Add resolver job fetching and resolving `inputs.ref` to verified `candidate_sha`; both jobs `need` it, checkout/assert its output, and use `broker-${{ needs.resolve_candidate.outputs.candidate_sha }}-<acceptance-or-performance>-${{ github.run_id }}` with cancel `false`. |
| `.github/workflows/runtime-s3-acceptance.yml:4-23` | Dispatch input defaults to mutable `develop`; no resolver/concurrency; checkout uses raw input. | Add resolver job fetching/resolving input to verified `candidate_sha`; `runtime-s3` needs it, checks out/asserts output SHA, and uses `runtime-s3-${{ needs.resolve_candidate.outputs.candidate_sha }}-${{ github.run_id }}` with cancel `false`. |
| `.github/workflows/supplemental-release-validation.yml:1-8, 36-39` | Push/dispatch evidence workflow; no concurrency block; checkout uses the event commit. | Add job-level `group: supplemental-validation-${{ github.sha }}-${{ github.run_id }}` and `cancel-in-progress: false`; assert checkout HEAD equals `github.sha`. |

Also retain the already-safe job-level HA groups in `ci.yml:180-182` and `:222-224` (`cancel-in-progress: false`); change their constant group to `targeted-ha-docker-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}` and `targeted-ha-podman-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}` respectively. The workflows are currently push-triggered, so `github.sha` is the pushed candidate; the PR-head expression preserves correct identity if PR events are enabled later. `pre-release.yml:882` and `:934` already use per-gate HA groups but must carry the resolved candidate SHA and unique run ID. The six exclusions and file/line rationale are itemized below; `pages.yml` has a cancelling deployment group, but that is outside the qualification-evidence contract.

### Resolver-job correction requested by independent review (w255, 2026-11-27)

The earlier raw-input group examples are withdrawn for `targeted-integration.yml` and `pre-release-runtime-suite.yml`. Workflow-level concurrency cannot reference `needs` outputs. The orchestration group must therefore be unique per run and non-cancelling; the **gate jobs** use the resolver output. This avoids grouping by a mutable branch name and avoids using an unverified raw input.

#### `targeted-integration.yml:51-64`

Before (current shape):

```yaml
  ref:
    description: Git ref or commit SHA to test
    required: true
    default: develop
    type: string

concurrency:
  group: targeted-integration-${{ github.ref }}-${{ inputs.ref || github.sha }}-${{ inputs.gate || 'default' }}-${{ inputs.runtime || 'default' }}
  cancel-in-progress: ${{ github.ref_name != 'work/v0.4.24-core-ha-updates' && github.ref_name != 'work/v0.4.25-contract-minimal-core' }}
```

After (resolver output plus per-evidence-job concurrency):

```yaml
concurrency:
  group: targeted-integration-orchestrator-${{ github.run_id }}
  cancel-in-progress: false

jobs:
  resolve_candidate:
    runs-on: ubuntu-latest
    outputs:
      head_sha: ${{ steps.resolve.outputs.head_sha }}
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ github.sha }}
          fetch-depth: 0
          persist-credentials: false
      - id: resolve
        shell: bash
        env:
          CANDIDATE_REF: ${{ inputs.ref || github.sha }}
        run: |
          set -euo pipefail
          git fetch --no-tags origin "$CANDIDATE_REF"
          head_sha="$(git rev-parse --verify 'FETCH_HEAD^{commit}')"
          [[ "$head_sha" =~ ^[0-9a-f]{40}$ ]]
          echo "head_sha=$head_sha" >> "$GITHUB_OUTPUT"

  <each evidence job>:
    needs: [resolve_candidate, <existing needs>]
    concurrency:
      group: targeted-${{ needs.resolve_candidate.outputs.head_sha }}-<literal gate/runtime identity>-${{ github.run_id }}
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ needs.resolve_candidate.outputs.head_sha }}
      - name: Assert exact candidate
        env:
          EXPECTED_HEAD_SHA: ${{ needs.resolve_candidate.outputs.head_sha }}
        run: test "$(git rev-parse HEAD)" = "$EXPECTED_HEAD_SHA"
```

Apply the resolver dependency, resolved checkout, and job-level group to every evidence-producing job in this workflow, including the `workflow_dispatch`, `workflow_call`, and push gate paths. Retain each job's existing gate/runtime literals or matrix identity in its group. The resolver is the sole place where a branch/ref becomes a commit SHA; a gate cannot start if fetch, resolution, 40-hex validation, or checkout equality fails.

#### `pre-release-runtime-suite.yml:81-126`

Before (current shape):

```yaml
    - name: Validate candidate ref before checkout
      env:
        CANDIDATE_REF: ${{ inputs.ref }}
      run: <validate branch/tag/ref>
    - name: Checkout BaseHarbor candidate
      uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
      with:
        ref: ${{ inputs.ref }}
    - name: Resolve candidate SHA
      id: candidate
      run: echo "sha=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"
```

After:

```yaml
jobs:
  resolve_candidate:
    runs-on: ubuntu-latest
    outputs:
      head_sha: ${{ steps.resolve.outputs.head_sha }}
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ github.sha }}
          fetch-depth: 0
          persist-credentials: false
      - id: resolve
        shell: bash
        env:
          CANDIDATE_REF: ${{ inputs.ref }}
        run: |
          set -euo pipefail
          git fetch --no-tags origin "$CANDIDATE_REF"
          head_sha="$(git rev-parse --verify 'FETCH_HEAD^{commit}')"
          [[ "$head_sha" =~ ^[0-9a-f]{40}$ ]]
          echo "head_sha=$head_sha" >> "$GITHUB_OUTPUT"

  gate:
    needs: resolve_candidate
    concurrency:
      group: atomic-${{ needs.resolve_candidate.outputs.head_sha }}-${{ inputs.runtime }}-${{ inputs.gate }}-${{ github.run_id }}
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ needs.resolve_candidate.outputs.head_sha }}
      - name: Assert exact candidate
        env:
          EXPECTED_HEAD_SHA: ${{ needs.resolve_candidate.outputs.head_sha }}
        run: test "$(git rev-parse HEAD)" = "$EXPECTED_HEAD_SHA"
```

Carry existing `gate` job steps after this checkout/assert sequence, preserving the existing pinned action SHAs and behavior. Change every subsequent candidate reference/manifest field to the resolver output, not raw `inputs.ref`; ensure the resolver job's SHA is the `candidate_sha` written into evidence. For `targeted-integration.yml`, add `resolve_candidate` to every evidence job's existing `needs` (append, do not replace): `compose_isolation_exact`, `registered_otlp_handoff`, `up_dispatch_source`, `application_full_reset`, `core_stop`, `standalone_retirement`, `observability_consumers`, `installation_destroy`, `shared_network`, `coreless_runtime`, `shared_provider_contracts`, `focused`, `app_backup_restore_podman`, `core_bootstrap`, `core_ha_recovery`, `provider_topology`, `application_provider_topology`, `core_provider_versions`, `core_ha_openbao_versions`, `v0421_ha`, `adoption`, `bug_hunt_templates`, `rootless_engine_isolation`, `identity_trust`, `final_bug_acceptance`, `provider_observation`, `external_provider_handoff`, `pr_selected_coreless_lifecycle_shards`, and `pr_selected_coreless_lifecycle`. Each gets its own group literal or current `matrix.gate`/`matrix.runtime` so no gate identity is lost.

#### `ci.yml:180-182` and `:222-224`

Before: both `group: baseharbor-release-qualification`; `cancel-in-progress: false`.

After for Docker and Podman respectively (retain `cancel-in-progress: false`):

```yaml
group: targeted-ha-docker-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}
```

```yaml
group: targeted-ha-podman-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}
```

This prevents the two runtime jobs and separate candidate heads from sharing the constant release lock while keeping the candidate identity tied to the PR head SHA when the event has one.

### Correction round 2 — w255 CHANGES (2026-11-27, Plan main `fee501fef`)

The earlier table's remaining raw-ref group proposals are superseded by these patterns. Every resolver must fetch the supplied branch/ref, resolve `FETCH_HEAD^{commit}`, validate exactly 40 lowercase hex characters, export the resulting `candidate_sha`, and fail before any gate if that fails. Every consumer must `needs: resolve_candidate`, check out the output SHA, and assert `git rev-parse HEAD` equals it. Workflow-level groups cannot use job outputs, so they are per-run orchestrator groups with cancellation disabled; only evidence jobs use resolver-output SHA groups.

#### Reusable resolver block

Add this `resolve_candidate` job to each workflow below; set `CANDIDATE_REF` to the noted input or event SHA. Preserve the pinned `actions/checkout` version already present in that file.

```yaml
  resolve_candidate:
    runs-on: ubuntu-latest
    outputs:
      candidate_sha: ${{ steps.resolve.outputs.candidate_sha }}
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ github.sha }}
          fetch-depth: 0
          persist-credentials: false
      - id: resolve
        shell: bash
        env:
          CANDIDATE_REF: <workflow input or github.sha>
        run: |
          set -euo pipefail
          git fetch --no-tags origin "$CANDIDATE_REF"
          candidate_sha="$(git rev-parse --verify 'FETCH_HEAD^{commit}')"
          [[ "$candidate_sha" =~ ^[0-9a-f]{40}$ ]]
          echo "candidate_sha=$candidate_sha" >> "$GITHUB_OUTPUT"
```

Every evidence job then uses:

```yaml
    needs: [resolve_candidate, <all existing needs>]
    concurrency:
      group: <workflow>-${{ needs.resolve_candidate.outputs.candidate_sha }}-<literal gate/runtime or matrix gate/runtime>-${{ github.run_id }}
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          ref: ${{ needs.resolve_candidate.outputs.candidate_sha }}
      - name: Assert exact candidate
        env:
          EXPECTED_CANDIDATE_SHA: ${{ needs.resolve_candidate.outputs.candidate_sha }}
        run: test "$(git rev-parse HEAD)" = "$EXPECTED_CANDIDATE_SHA"
```

#### Workflow-specific resolver consumers

| Workflow | Before | After: resolver input, orchestrator and consuming job group |
| --- | --- | --- |
| `mcp-lifecycle-acceptance.yml:28-30,35-120` | Workflow group contains mutable `github.ref` and raw `inputs.ref`; Docker and Podman check out raw input at `:48, :91`. | Orchestrator `group: mcp-orchestrator-${{ github.run_id }}`, cancel false. Resolver input `inputs.ref || github.sha`. Docker job: `needs: resolve_candidate`, `group: mcp-${{ needs.resolve_candidate.outputs.candidate_sha }}-docker-${{ github.run_id }}`. Podman job: same with `-podman-`. Both checkout/assert resolver output. |
| `nextjs-greenfield-e2e.yml:13-15,18-90` | Workflow group contains PR number/ref; greenfield matrix checks out raw `inputs.candidate_ref` at `:77`. | Orchestrator `group: greenfield-orchestrator-${{ github.run_id }}`, cancel false. Resolver input `inputs.candidate_ref || github.sha`. `nextjs-docker` and `greenfield-native` depend on resolver; groups use output SHA + `nextjs-docker`, or `${{ matrix.stack }}-${{ matrix.runtime }}`, plus run ID. Both checkout/assert output SHA. |
| `observability-acceptance.yml:33-35,40-160` | Workflow group contains `github.ref` and raw `inputs.ref`; jobs check it out at `:59, :141`. | Orchestrator `group: observability-orchestrator-${{ github.run_id }}`, cancel false. Resolver input `inputs.ref || github.sha`. Docker and Podman depend on resolver; groups use output SHA + literal runtime + run ID. Both checkout/assert output SHA. |
| `docker-runtime-acceptance.yml:24-26` | Workflow concurrency uses branch ref; candidate is raw `inputs.ref` at `:189`. | Orchestrator `group: docker-runtime-orchestrator-${{ github.run_id }}`, cancel false. Resolver input `inputs.ref || github.event.pull_request.head.sha || github.sha`. Add resolver dependency and a per-job output-SHA group plus each job's ID/matrix runtime to `select_develop`, `keycloak_single_native`, `single_default_native`, `docker-runtime`, `provider-ha`, and `mcp-edit-native`; replace candidate checkout with output SHA and assert equality. |
| `podman-acceptance.yml:23-25` | Workflow concurrency uses branch ref; candidate is raw `inputs.ref` at `:191`. | Orchestrator `group: podman-runtime-orchestrator-${{ github.run_id }}`, cancel false. Resolver input `inputs.ref || github.event.pull_request.head.sha || github.sha`. Add resolver dependency and per-job output-SHA group + job ID to `select_develop`, `keycloak_single_native`, and `podman-quadlet`; the four split `single_default_native` children each get their own output-SHA/job-ID group. Replace checkout with output SHA and assert equality. |
| `runtime-broker.yml:6-20,25-37,321-325` | `inputs.ref` accepts a branch/ref and both evidence jobs directly check it out; no resolver/concurrency. | Resolver input `inputs.ref`; `acceptance` and `performance` both depend on it and use `broker-${{ needs.resolve_candidate.outputs.candidate_sha }}-acceptance-${{ github.run_id }}` / `...-performance-...`, cancel false, checkout/assert output SHA. |
| `runtime-s3-acceptance.yml:4-23` | Dispatch defaults to mutable `develop`; runtime-s3 directly checks out raw input; no resolver/concurrency. | Resolver input `inputs.ref || github.sha`; `runtime-s3` depends on it and uses `runtime-s3-${{ needs.resolve_candidate.outputs.candidate_sha }}-${{ github.run_id }}`, cancel false, checkout/assert output SHA. |
| `targeted-integration.yml:51-64` | Corrected in round 1: workflow uses per-run orchestration; evidence jobs depend on resolver output. | Retain the resolver and all evidence-job dependencies/groups from round 1. No raw `inputs.ref` in a concurrency key. |
| `pre-release-runtime-suite.yml:81-126` | Corrected in round 1: resolver job emits full SHA; `gate` consumes it. | Retain resolver-output group and checkout equality assertion from round 1. No raw `inputs.ref` in a concurrency key. |

The workflow input may remain a branch/ref where that is an existing interface, but no gate is admitted until resolver fetch succeeds and the resolved commit SHA is exported. A syntax-only SHA check, an unverified raw `inputs.ref` group, or a checkout that is not compared with the resolver output does not satisfy the requirement.

#### Exclusion inventory — source anchors and out-of-contract reason

| Excluded workflow | Source anchor and observed role | Why its check is outside qualification evidence |
| --- | --- | --- |
| `.github/workflows/runtime-image.yml` | `:1-20,22-45`; reusable/manual runtime image build and provenance/attestation permissions. | Produces release artifacts and provenance; it is not a candidate test/acceptance qualification check. Its build result remains release-artifact evidence under the release workflow. |
| `.github/workflows/release.yml` | `:1-8,18-42`; validates release tag ancestry and schedules publication jobs. | Publishes a release after authorization; publication status is not a candidate qualification gate. |
| `.github/workflows/pages.yml` | `:3-20`; Pages build/deploy workflow; concurrency at `:14-16` cancels prior deployment. | Docs deployment is intentionally latest-wins; deployment output is not Core runtime or PR qualification evidence. Do not remove its deployment cancellation under this decision. |
| `.github/workflows/receipt-post-run.yml` | `:1-27`; protected-default-branch receipt writer; checks out trusted source and writes a post-run receipt. | Records a completed event after qualification; receipt generation is downstream bookkeeping, not a gate proving the candidate. |
| `.github/workflows/artifact-gc.yml` | `:4-37`; maintenance trigger and PR-scoped mocked GC tests. | The PR check validates GC workflow/tool behavior, not product runtime/acceptance; its scheduled artifact deletion is maintenance. |
| `.github/workflows/renovate.yml` | `:3-20`; dependency-update automation; fixed concurrency group, cancel false. | Automation creates dependency updates; it is not a qualification or acceptance check. |

These are six scope exclusions, not claims that the workflows have no jobs or checks. `pages.yml` and `renovate.yml` do use concurrency; their behavior is excluded because it serves deployment/automation, not evidence qualification.

### Card mapping and #1812 order

All three decisions are recorded under existing card 0428-249: (1) non-cancellation and (2) checked-SHA identity are shared qualification prerequisites directly consumed by #1812; (3) the Podman split makes each required runtime assertion independently visible to the same qualification chain. 0428-209 is closed and its native-cell contract does not own global workflow scheduling; 0428-321 is an H-V45 CLI documentation/coverage contract, not workflow ownership. No new card is proposed.

Before #1812 can qualify: the Owner must land the approved workflow changes on `develop`; then #1812's owning lane must absorb that `develop` tip by an ordinary forward merge, publish a new exact head, and obtain fresh Hosted evidence on that head. The final census must show every required Docker and Podman gate executed and successful, with no required gate cancelled or skipped; old-head runs do not transfer. `PR Selected Checks` must complete successfully on that same head. This disposition does not qualify #1812 or authorize any workflow edit by this lane.
