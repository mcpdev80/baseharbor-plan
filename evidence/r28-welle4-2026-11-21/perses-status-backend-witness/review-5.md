ROLLE: REVIEW

## PLAN

1. Read the current task contract, task note, prior review evidence, and owner-stop state.
2. Verify live develop and PR #1702 refs, candidate SHA, PR metadata, merge-base, changed paths, and commit count.
3. Inspect the exact backend witness implementation for Verification=none and trace its claimed source.
4. Verify required exact-head checks and inspect per-job logs for the relevant backend evidence.
5. Record verdict and actionable finding recipes, then publish only this evidence file.
6. Verify the evidence path is present on planning origin/main and report the exact candidate SHA.

Timestamp: 2026-11-21 12:05 UTC
Backend/model: Codex API, GPT-6

## Verdict

**Verdict: REQUEST CHANGES — exact candidate `2e4a570a769885dc0062b6aadd4923331e0cbfc5`.** The candidate does not produce a genuine negative backend witness: production passes an empty witness, then renders absent Loki/Tempo observations as `unreachable`. Its positive Prometheus `configured` state comes from manifest source presence plus a static host/provider capability resolver, not a source-specific backend observation. This fails the card's backend-witness acceptance and the owner's open (a)/(b) boundary. The current PR also conflicts with current `develop`; this is a separate freshness finding.

The prior verdict SHA `b2f2fd3ac17293949c18223b55936e1018085472` resolves as a GitHub commit object, but it is not an ancestor of the current head: GitHub compare `b2f2fd3...2e4a570` reports `ahead_by=110`, `behind_by=5`, merge base `40cb28c758b02960356434b630086a341ebe1738`. The stale-verdict reachability problem is resolved in the narrow sense that the new candidate has its own exact review target; it does not inherit the old verdict's ancestry. The semantic finding remains present at the new head.

## Task contract, refs, and scope

`python3 scripts/plan.py show t-20261119-r28-perses-status-backend-witness` reports `state: review`. The task note's current acceptance requires a CLI-path test against backend evidence for reached/matched and absent/unavailable states, with matching human and machine output; its hard acceptance requires exact SHA → test ID → mapped gate → trigger → actual passing run. The owner handoff records the 0428-143 rule that `Verification=none` makes no verification assertion and the exporter omits those sources. The task's hard boundary files `internal/capability/perses.go` and `cmd/baha/machine_coverage.go` are absent from this PR diff. No owner stop in the task note prohibits this read-only review.

Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).

My `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1702/head` output:

```text
97b2ba5543f07b820b5c18a688058fd932c4516f refs/heads/develop
2e4a570a769885dc0062b6aadd4923331e0cbfc5 refs/pull/1702/head
```

`gh pr view 1702 --repo mcpdev80/baseharbor` reports `state=OPEN`, `isDraft=false`, `headRefOid=2e4a570a769885dc0062b6aadd4923331e0cbfc5`, `baseRefName=develop`, `mergeable=CONFLICTING`, `mergeStateStatus=DIRTY`. The REST Pull Request view reports base SHA `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef` and the same head SHA.

GitHub compare of the PR base `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef` to the candidate reports `status=ahead`, `ahead_by=6`, `behind_by=0`, merge-base equal to the PR base, and exactly four changed paths:

- `cmd/baha/app_status_result.go`
- `cmd/baha/app_status_result_test.go`
- `cmd/baha/perses_lifecycle.go`
- `cmd/baha/perses_lifecycle_transport_test.go`

All four are within the card's status-result and test scope. No `.github/**`, `internal/capability/perses.go`, or `cmd/baha/machine_coverage.go` path is changed. Against the live `develop` SHA `97b2ba5543f07b820b5c18a688058fd932c4516f`, compare reports `status=diverged`, `ahead_by=6`, `behind_by=65`, merge-base `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef`. Thus live develop is not an ancestor of the PR head; GitHub reports the PR as conflicting. The old exact-head green run is not a current-base integration proof.

## Production source review and decision question

The new helper `persesBackendSignalWitnessFromManifest` at `cmd/baha/app_status_result.go:100-180` consumes manifest declarations and a `PersesBackendSignalWitness`. Its Loki and Tempo false branches emit `unreachable` at `:142-148` and `:169-174`. The production callers supply `metricsprovider.PersesBackendSignalWitness{}` at `cmd/baha/perses_lifecycle.go:235` and `cmd/baha/app_status_result.go:296,399`; these zero values contain no HTTP response, container state, or source-specific observation. Therefore a declared Loki or Tempo source is printed as `unreachable` solely because no witness was supplied. That is an unobserved/unknown input, not a genuine negative backend witness.

The positive Prometheus branch at `cmd/baha/app_status_result.go:116-129` checks `application.HasMetricsSources(m)` and `resolvedHostSignalStatus == capability.ObservabilitySupported`. The resolver `internal/capability/perses.go:343-368` is explicitly read-only, performs no backend probe, and checks manifest selection, Perses pin validity, and the static reference provider catalog. `HasMetricsSources` is only `len(m.Metrics.Sources) > 0` in `internal/application/manifest.go:390`. The candidate does not correlate that manifest source with its effective scrape target or its source-specific `Verification` policy. It can therefore label a declared source `configured` without proving that source has a current backend observation or effective target. This is the positive-without-source risk in the mission's (a)/(b) question; the current code does not inspect `Verification=none` to prevent that assertion.

The positive helper test `TestPersesStatusWitnessConfiguredWhenResolved` manually passes `ObservabilitySupported` and `LokiProven: true, TempoProven: true` at `cmd/baha/app_status_result_test.go:114-125`. It verifies helper behavior with synthetic inputs, not that production obtains those values. The CLI human-face test asserts `configured` for Prometheus and `unreachable` for Loki/Tempo at `:317-330`, reproducing the unsupported states rather than validating backend observations. The human/machine parity test compares backend names, not source provenance or equivalent backend evidence.

Direct answer to the owner question: the candidate does **not** produce a genuine negative witness from a real backend source. It can emit a positive `configured` field based on a manifest declaration and unrelated static capability resolution, without checking source-specific verification/effective-target evidence. The state labels are therefore not safely grounded in the evidence required by this card.

The patch contains no idle-driven file deletion or cleanup branch. The mission's idle-plus-mutation condition is not applicable to this diff. Existing M1/M2 mutation notes in `round-6-authfixture.md` only prove renderer reachability and that changing a derived label makes witness assertions fail; they do not prove production source provenance, and do not close this finding.

## Exact-head hosted checks and per-job evidence

Run `44886438604` is `pull_request`, completed with `conclusion=success` on the exact head `2e4a570a769885dc0062b6aadd4923331e0cbfc5`. `PR Selected Checks`, `PR · Trusted Plan`, `Workflow policy`, and the required Go unit cells passed. Skipped jobs are not counted as passes.

I retrieved individual job log payloads via `gh api repos/mcpdev80/baseharbor/actions/jobs/<job-id>/logs`, rather than relying on the aggregate. Each relevant log reports its own successful execution:

- `PR · Go unit · cli-0`, job `136792667844`, 22,164 bytes; terminal line: `PASS cli-0: 453 passed / 13 intentionally skipped / 466 discovered; CLI inventory total=1812`.
- `PR · Go unit · cli-1`, job `136792667836`, 22,242 bytes; terminal line: `PASS cli-1: 434 passed / 10 intentionally skipped / 444 discovered; CLI inventory total=1812`.
- `PR · Go unit · cli-2`, job `136792667876`, 22,249 bytes; terminal line: `PASS cli-2: 442 passed / 19 intentionally skipped / 461 discovered; CLI inventory total=1812`.
- `PR · Go unit · cli-3`, job `136792667866`, 22,250 bytes; terminal line: `PASS cli-3: 425 passed / 16 intentionally skipped / 441 discovered; CLI inventory total=1812`.
- `PR · Go unit · packages`, job `136792667899`, 33,408 bytes; terminal line: `PASS all non-CLI Go package tests`.
- `PR · Trusted Plan`, job `136792625758`, success; `Workflow policy`, job `136792625589`, success; `PR Selected Checks`, job `136793845118`, success.

The selected CLI test route is present in `.github/workflows/ci.yml` at `pr_unit_shards` (candidate line 1190 selects non-draft develop/lane PRs with unit scope) and `scripts/pr-go-unit-shard.py` discovers tests and selects each `cli-N` by the first eight SHA-256 bytes modulo four. Applying that checked-in selector to the candidate's ten witness test IDs maps `TestPersesStatusWitnessUnauthenticatedDenied` to cli-0; `TestPersesStatusWitnessConfiguredWhenResolved`, `TestPersesStatusWitnessNotConfiguredWithoutObservabilityBackend`, `TestPersesStatusWitnessNeverClaimsHealthyFromManifestFlag`, and `TestPersesStatusWitnessHumanFaceRendersBackendWitness` to cli-1; `TestPersesStatusWitnessUnreachableWhenDeclaredNotResolved`, `TestPersesStatusWitnessUnreachableIsNotTheManifestFlag`, `TestPersesStatusWitnessLogsAbsentMarksLokiNotConfigured`, and `TestPersesStatusWitnessRendersBackendWitnessDirectly` to cli-2; and `TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends` to cli-3. These actual selected shard jobs passed. Their passing status does not resolve the source-provenance defect.

No local package test was run. No workflow was edited or dispatched. No product file, PR, or branch was changed.

## Findings and recipes

### Finding 1 — `unreachable` is derived from an empty witness, not a negative backend observation

File: `cmd/baha/app_status_result.go:142-148,169-174`, with production call sites `cmd/baha/perses_lifecycle.go:235` and `cmd/baha/app_status_result.go:296,399`.

Change: supply source-specific backend evidence to both the human `perses status` path and local/remote machine `app status` paths. A missing observation must remain unknown/unverified; emit `unreachable` only when a concrete source reports a negative result. If the upstream contract cannot supply the required provenance within this card, record the precise contract gap for the coordinator instead of synthesizing a negative state.

Test requirement: exercise the registered human and machine commands with a real-source fixture that produces a positive observation and an actual negative observation. Add a mutation that removes the production source-to-witness wiring; the command-level test must fail. Preserve the unauthenticated denial path.

Stop criterion: every emitted `unreachable` value is backed by a named negative source observation, and removing that source wiring makes the command test fail; otherwise no backend health/reachability label is emitted.

### Finding 2 — `configured` is not tied to the named source's verification/effective-target evidence

File: `cmd/baha/app_status_result.go:116-129,287-296,399`, `internal/capability/perses.go:343-368`, and `internal/application/manifest.go:383-390`.

Change: derive a positive state from the named source's own resolved backend evidence and effective-target result, not merely a non-empty manifest source list plus a static host/provider catalog capability. Respect the `Verification=none` rule: it is not evidence that a backend was verified or reached.

Test requirement: add a command-level case where the declared source has `Verification=none` and is omitted from effective scrape targets; assert that no positive reachability/configured witness is emitted. Add the paired source-backed positive case and a mutation that bypasses source-specific verification/effective-target evidence; the mutation must turn the command assertion red.

Stop criterion: a positive field cannot be produced from declaration/static catalog data alone, and the exact source's verified/effective-target evidence is present in both output faces.

### Finding 3 — PR head is stale against live develop and currently conflicts

File: branch base state, not a product file. Live develop is `97b2ba5543f07b820b5c18a688058fd932c4516f`; PR base is `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef`; current comparison is 6 ahead / 65 behind and PR metadata is `mergeable=CONFLICTING`, `mergeStateStatus=DIRTY`.

Change: hop the same PR branch to then-current develop and resolve only conflicts within the card write-set. Do not alter protected paths or use a second candidate branch.

Test requirement: rerun the card's selected Go shards, Trusted Plan, Workflow policy, and `PR Selected Checks` on the exact hopped head; skipped or queued required checks do not count as success.

Stop criterion: then-current develop is an ancestor of the candidate, the PR is conflict-free, and the exact-head required aggregate and card tests pass.

## Repo-rule compliance

Read-only review of GitHub refs, API source, and the planning task/evidence. No product changes, PR mutation, merge, workflow rerun, local Go test, container, or subagent. The only publication from this review is this file in the verified planning repository. This file contains no Markdown checkbox lines.

END REVIEW DONE
