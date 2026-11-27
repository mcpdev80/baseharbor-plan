# Independent review: qualification workflow integrity

## Verdict

CHANGES on the edit set in `evidence/2026-11-27/0428-249/qualification-workflow-integrity.md` at Plan main `2f388b6bf6cce52da3e7308ec77c405c361e72b3` (which extends `d7cd3f20dffd5b46c28d937f24f9df33893488bf`). Review target: BaseHarbor develop `6d237ccdf3a5db19c5814ad5b76d01be6c38c35c`.

The three Owner decisions are sound in principle: evidence runs must not be cancelled; evidence concurrency must bind a verified full candidate SHA plus gate/runtime identity and run ID; and Podman's bundled `single_default_native` assertions must be split into four independently reported jobs. The inventory names all 14 proposed evidence workflows and all six exclusions. The 65-minute timeout is the configured value at `podman-acceptance.yml:111`; workflow source does not establish a 24-minute observed duration, and the akte correctly makes the split independent of wall-clock duration.

Commit/identity record: card owner verbatim is `w362-0428-249-1812rebase` (card 0428-249 frontmatter). Review author and committer are `w255-0428-251-demo170codex`; executing reviewer lane is `w255-0428-251-demo170codex`. Planned invocation: `git -c user.name="w255-0428-251-demo170codex" -c user.email="w255-0428-251-demo170codex@baseharbor.local" commit -m "review(0428-249): workflow integrity disposition"`. Pre-push identity gate: `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`.

The apparent `.github/**` ownership conflict is resolved by commit `2f388b6bf`: RUNBOOK §4.0 permits the dispatched WORKER to implement the exact workflow/test preparation explicitly approved for a named card. Here that is worker `w362` on existing card 0428-249, limited to the edit set below. It does not authorize this reviewer lane or a broader trigger change.

## Findings for worker w362

### Finding 1 — concurrency keys use raw refs instead of resolver outputs

The required full-SHA resolution output does not yet exist in the relevant current graphs. In `.github/workflows/targeted-integration.yml:51-64`, `inputs.ref` is expressly a “Git ref or commit SHA” and the workflow-level group is computed before jobs; there is no resolver job output. In `.github/workflows/pre-release-runtime-suite.yml:81-126`, ref validation, checkout, and `git rev-parse HEAD` output all occur as steps within the `gate` job; a job's concurrency expression cannot consume a later step output, and the proposed `inputs.ref` group is still the unverified caller string. The same raw-input pattern in the proposed groups must be corrected in `docker-runtime-acceptance.yml`, `podman-acceptance.yml`, `mcp-lifecycle-acceptance.yml`, `nextjs-greenfield-e2e.yml`, `observability-acceptance.yml`, `runtime-broker.yml`, and `runtime-s3-acceptance.yml`.

Before: gate concurrency is based on `inputs.ref`/`inputs.candidate_ref`, which may be a branch or tag; later steps separately inspect or check out that value. After: add a resolver job that resolves the supplied ref to a full 40-hex commit SHA, exports `outputs.candidate_sha`, and fails closed if resolution fails; make each evidence job `needs: resolve`, check out `needs.resolve.outputs.candidate_sha`, assert `git rev-parse HEAD == needs.resolve.outputs.candidate_sha`, and set its job-level group to `bh-evidence-${{ needs.resolve.outputs.candidate_sha }}-${{ <gate/runtime identity> }}-${{ github.run_id }}` with `cancel-in-progress: false`. For an input that is already contractually a full SHA, still validate that object and export the validated SHA from the resolver before the gate job. Use existing resolver outputs in `targeted-demo-acceptance.yml:53-62` and `pre-release.yml:source_prepare` rather than raw inputs; workflow-level orchestration groups remain unique per `github.run_id` and non-cancelling.

### Finding 2 — CI HA group proposal keys PR work by the synthetic merge SHA

The akte proposes `github.sha` for the existing HA job groups at `.github/workflows/ci.yml:180-182,222-224`. For `pull_request`, that is the synthetic merge commit; the candidate head is `github.event.pull_request.head.sha`. The workflow-level proposal at `ci.yml:24-26` already uses the correct PR-head fallback, but the job-level HA proposal must use the same candidate identity.

Before: `ha-${{ github.sha }}-${{ matrix.group }}-${{ matrix.runtime }}-${{ github.run_id }}`. After: `ha-${{ github.event.pull_request.head.sha || github.sha }}-${{ matrix.group }}-${{ matrix.runtime }}-${{ github.run_id }}`, retaining `cancel-in-progress: false`. Keep the selected graph inside that same protected run: runtime selection at `ci.yml:1479-1496`, selected integration at `1498-1513`, owner-native jobs at `1515-1550`, and the `PR Selected Checks` dependency/result checks at `1552-1605`. No candidate-added job should enter the required aggregator beyond the base-plan graph.

### Finding 3 — exclusion classifications need source-line witnesses

The six exclusions are plausible, but the akte lists no file:line anchors for them, so its completeness claim is not independently auditable. Add an exclusion row per path with the trigger/job behavior that makes it non-qualification scope and state whether it has any cancelling concurrency: `runtime-image.yml:1-20,22-45` (release image/provenance build), `release.yml:1-35` (release publication), `pages.yml:3-20` (Pages deployment; its deploy concurrency is not qualification evidence), `receipt-post-run.yml:1-27` (post-merge receipt writer), `artifact-gc.yml:4-35` (workflow maintenance and PR-scoped mocked tests), and `renovate.yml:3-20` (dependency automation). For any excluded workflow that can emit a check, explicitly say why that check is outside the qualification evidence contract; do not imply that it has no tests or jobs.

## Podman split — approved shape and source mapping

In `.github/workflows/podman-acceptance.yml`, the current `single_default_native` job at `:106-175` bundles four blocks: SQL/Secrets at `:129-146`; Node HTTPS enrollment/remote CLI at `:147-149`; install destroy/interrupted retry at `:150-152`; and pinned-workload lifecycle/backup at `:153-172`. Before: these share one job and one final status. After: extract those four blocks into four named jobs, each with its own setup, exact-candidate checkout/verification, cleanup and independently failing result. Preserve `keycloak_single_native` at `:62-104` as a separate job. Keep the configured 65-minute timeout unless the worker has a scoped reason to adjust it; the current evidence does not support an observed 24-minute duration.

## Coverage and evidence

The akte covers these 14 evidence workflows: `ci.yml`, `docker-runtime-acceptance.yml`, `podman-acceptance.yml`, `host-trust-owned-e2e.yml`, `mcp-lifecycle-acceptance.yml`, `nextjs-greenfield-e2e.yml`, `observability-acceptance.yml`, `targeted-integration.yml`, `pre-release.yml`, `pre-release-runtime-suite.yml`, `targeted-demo-acceptance.yml`, `runtime-broker.yml`, `runtime-s3-acceptance.yml`, and `supplemental-release-validation.yml`. The six exclusions above complete the current develop workflow inventory. Current develop line witnesses were read at `6d237ccdf3a5db19c5814ad5b76d01be6c38c35c`; exact anchors are included above for all findings and the named exclusion rows.

## PLAN

1. Record the exact develop workflow revision and compare each workflow line anchor with the published edit-set table.
2. Check the three owner decisions, source inventory, exclusion rationale, and worker-scope exception.
3. Publish the independent CHANGES disposition with concrete worker edits; leave workflow implementation to w362.

## Base and delivery attestation

Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.

Plan main base: `2f388b6bf6cce52da3e7308ec77c405c361e72b3` (confirmed by `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` before creating this review commit). The review commit must be a direct child of this exact tip; verify `git merge-base --is-ancestor 2f388b6bf6cce52da3e7308ec77c405c361e72b3 HEAD` before publication. The review changes no task, workflow, or product file.

## Fresh re-review — Plan main 70aead9a9, 2026-11-27

Plan main advanced through `70aead9a9da6c6c576ed8d73ab91006810d4e6d5` (`evidence(0428-249): resolve candidate SHA before gating`) and `175fac3cd3de7a6ee9ba7463fb6898bda30dd100` (unrelated evidence update). BaseHarbor develop remains `6d237ccdf3a5db19c5814ad5b76d01be6c38c35c` at this review. Verdict remains CHANGES, but the update resolves two earlier findings:

1. ACCEPTED: `targeted-integration.yml` now has a per-run non-cancelling workflow group, `resolve_candidate.outputs.head_sha`, and exact-SHA gate checkouts/assertions (`qualification-workflow-integrity.md:40-100`). `pre-release-runtime-suite.yml` now follows the same resolver-output pattern (`:102-160`). The original source has no such resolver job outputs: `targeted-integration.yml:51-64` only declares a ref input and workflow-level concurrency, while `pre-release-runtime-suite.yml:81-126` resolves within the gate job. The proposed split is the appropriate correction.
2. ACCEPTED: the CI HA key correction now uses `${{ github.event.pull_request.head.sha || github.sha }}` with distinct Docker/Podman identities and `github.run_id` (`:162-176`); this fixes the earlier synthetic-merge-SHA concern. It preserves the `PR Selected Checks` graph at develop `ci.yml:1479-1513,1552-1605`.
3. ACCEPTED: the named-card authority is explicit in 2f388b6bf and the edit set still limits implementation to worker w362 on card 0428-249 under RUNBOOK §4.0. The four Podman source blocks are mapped below.

### Remaining changes required before worker implementation is fully specified

#### A. Other ref-accepting evidence jobs still key on raw input rather than a resolver output

For `mcp-lifecycle-acceptance.yml:28-30`, the proposed group is workflow-level and contains raw `inputs.ref`; a workflow-level group cannot consume the later resolver output. For `nextjs-greenfield-e2e.yml:13-15`, the proposed workflow-level group contains raw `inputs.candidate_ref`, and `:77` checks out that value. For `observability-acceptance.yml:33-35`, the proposed per-job group still contains raw `inputs.ref` despite the resolver/assertion requirement. None of these rows specifies a resolver job output consumed by gate concurrency.

Before: workflow-level groups use `inputs.ref`/`inputs.candidate_ref`, or a gate group uses those raw strings. After: use run-unique, non-cancelling orchestrator groups; add a resolver job that fetches the supplied ref and exports a verified 40-hex SHA; make evidence jobs depend on it, check out and assert that output, then use `needs.resolve_candidate.outputs.head_sha` plus runtime/gate identity and `github.run_id` in each job-level group. Apply this to `mcp-lifecycle-acceptance.yml`, `nextjs-greenfield-e2e.yml`, and `observability-acceptance.yml`.

#### B. Strict-SHA rows need to state the pre-gate resolution/verification contract

The `docker-runtime-acceptance.yml`, `podman-acceptance.yml`, `runtime-broker.yml`, and `runtime-s3-acceptance.yml` rows constrain evidence inputs to full SHA values and require checkout equality, which is safer than refs. To meet the stated “verified SHA in the gate-level group” rule unambiguously, specify that the supplied SHA is fetched/verified as a commit before the evidence job is admitted and that the evidence job uses the resolver output in its concurrency group. In particular, `runtime-broker.yml:6-20` describes a Git ref input, and `runtime-s3-acceptance.yml:6-9,20-23` defaults to `develop`; a syntax-only full-SHA guard plus a later assertion does not resolve those current branch-shaped inputs.

Before: input may be a ref, and proposed group is `inputs.ref` plus run ID. After: resolve and export a commit SHA in a prerequisite job, or remove branch/ref inputs from the evidence interface and verify the supplied full SHA before acceptance steps; group by that verified SHA, gate/runtime identity, and run ID. Preserve a unique, non-cancelling orchestrator group.

#### C. Add source anchors to every exclusion row

The evidence-workflow table has file-and-line anchors, but the exclusion sentence still has no per-path source anchors. Add these to the edit-set table: `runtime-image.yml:1-20,22-45` (release image/provenance production); `release.yml:1-8,18-35` (publishing); `pages.yml:3-20` (deployment, not qualification); `receipt-post-run.yml:1-27` (post-merge receipt writer); `artifact-gc.yml:4-35` (maintenance workflow with PR-scoped mocked tests); and `renovate.yml:3-20` (dependency automation). For any excluded workflow that emits a check, state why that check is outside the qualification evidence contract; do not imply that it has no tests or jobs.

## Podman split source mapping

The `podman-acceptance.yml:106-175` four-way split is accepted. Before, one job wraps SQL/Secrets `:129-146`, Node HTTPS enrollment/remote CLI `:147-149`, install destroy/interrupted retry `:150-152`, and pinned-workload lifecycle/backup `:153-172`, with shared preparation `:116-128` and cleanup `:173-175`. After, create four named jobs, each with its own verified candidate checkout, preparation, cleanup, and independently failing check result; retain `keycloak_single_native` at `:62-104`. The 65-minute configured timeout at `:111` does not establish an observed 24-minute runtime; the structural split stands without that claim.

## Current disposition

CHANGES remains the worker handoff verdict until remaining changes A, B, and C are carried into the edit set. No workflow or product files were changed by this review. Workflow implementation remains assigned only to worker w362 under the named-card exception.

Delivery correction: the first local review commit was based on `2f388b6bf6cce52da3e7308ec77c405c361e72b3`. Before publishing this updated verdict, the review branch incorporated current Plan main `175fac3cd3de7a6ee9ba7463fb6898bda30dd100` by an ordinary merge commit under this lane identity; no rebase or force-push was used. The final verdict is this forward addendum, which supersedes the initial CHANGES scope above while preserving its audit trail.
