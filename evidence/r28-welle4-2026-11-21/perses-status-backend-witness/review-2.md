ROLLE: REVIEW

# CODEX-REVIEW — PR #1702 / Karte 0428-142

**Verdict: REQUEST CHANGES**

## PLAN

1. Read the mission and record the numbered plan before Git.
2. Read required coordinator authorization and inspect repository remotes; use only verified GitHub URLs.
3. Verify frozen PR #1702 head/base, refs, ancestry, exact changed paths, and historical comparison heads.
4. Read the card contract, prior review and hop evidence; inspect exact candidate behavior and production reachability.
5. Verify hosted CI and cleanliness chronology; classify inherited CLI failures.
6. Recheck candidate immutability and finalize verdict/follow-up evidence.
7. Publish only this review file on baseharbor-plan main and verify its remote path and commit SHA.
8. Complete the end handoff without posting to other sessions, as the mission requires.

## Review metadata

Session ID: not exposed by this interface.
Model: GPT-6 Codex; exact serving variant is not exposed.
Backend: not exposed by this interface.
Review time: 2026-11-21 03:11 UTC.

Candidate: mcpdev80/baseharbor PR #1702, head `e21b5c528923ddd610b8c5e709ff0d61294c211e`, base develop `40cb28c758b02960356434b630086a341ebe1738`.

## Candidate and diff witnesses

The PR API reported head `e21b5c528923ddd610b8c5e709ff0d61294c211e`, base.ref=develop, base.sha=`40cb28c758b02960356434b630086a341ebe1738`, open, draft=false, merged=false, mergeable_state=blocked. PR files:

```text
modified cmd/baha/app_status_result.go +145/-1
added cmd/baha/app_status_result_test.go +267/-0
modified cmd/baha/perses_lifecycle.go +26/-3
```

Remote witness before review:

```text
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
e21b5c528923ddd610b8c5e709ff0d61294c211e refs/heads/lane-0428-142-statuswitness
e21b5c528923ddd610b8c5e709ff0d61294c211e refs/pull/1702/head
```

The fresh GitHub clone used remote `origin https://github.com/mcpdev80/baseharbor.git`. `git merge-base --is-ancestor origin/develop origin/pr-1702` exited 0. `git diff --name-status origin/develop...origin/pr-1702` listed exactly the three PR files above. `git log --oneline origin/develop..origin/pr-1702` listed:

```text
e21b5c52 hop(0428-142): carry card r1 BackendWitness field on persesStatusResult for new develop
67658ef8 fix(0428-142 r2): emit real unreachable backend-witness from resolved signal (CODEX-REVIEW r2)
```

No owner-owned path was changed: the diff is empty for `internal/operatorauth/**`, `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identityprovider/**`, `internal/serviceaccess/**`, `cmd/baha/main.go`, and the #1615 `cmd/baha/app_status_collect.go` stack.

## P1 — The hop does not carry the human-output behavior from 3f7600d

I compared the prior candidate `3f7600ded0d98902ec689543fa29ad4fdc0d3e6e` against the new head and read the prior review `evidence/r28-welle4-2026-11-20/perses-status-backend-witness/review-1.md`. The test file blob is byte-identical at both heads. The source blobs are not. Most materially, the old candidate called `renderPersesBackendWitness(out, result.BackendWitness)` after printing the state; the new candidate's `cmd/baha/perses_lifecycle.go:85-94` prints only `Perses state` and returns. The helper remains at :314-317 but has no production caller in the status command. The unchanged `TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends` at `cmd/baha/app_status_result_test.go:245-265` requires the human output to contain every backend name. That test's required behavior is absent at the exact head.

The direct tree comparison also shows the app-status comment changing `configured` to `configured_unverified` and the lifecycle help text reverting to that vocabulary. Those strings follow the current base's text, but the dropped renderer is behavior, not a base-comment difference. The hop akte's claim that card content was carried unchanged is therefore not supported for the human status face.

Recipe: in `cmd/baha/perses_lifecycle.go`, render `result.BackendWitness` in the human `perses status` branch after the state line. Keep `TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends` as an end-to-end command test and make sure it fails with the call removed and passes with the call present. Stop until that test is executed in a required CI shard on the exact candidate and verifies the backend names and source IDs in human output.

## P2 — Production paths pass no Loki/Tempo evidence

The production call sites pass an empty `metricsprovider.PersesBackendSignalWitness{}`: `cmd/baha/app_status_result.go:296,399` (remote and local status) and `cmd/baha/perses_lifecycle.go:234`. The helper's positive Loki/Tempo branches require `witness.LokiProven` and `witness.TempoProven` at `app_status_result.go:134-148,161-175`; given those empty inputs, every declared Loki/Tempo source is always reported unreachable. The positive helper test at :71-82 injects synthetic true fields directly and does not exercise a production source. The existing type documentation at `internal/metrics/perses_dashboards_hosts.go:529-555` says these bits represent each backend's own registered signal and explicitly notes wiring that witness from the runtime registry was not done. Prometheus uses `ResolveHostDashboardSignalStatus`; its implementation at `internal/capability/perses.go:328-368` checks a reference integration descriptor and does not run a target/backend query.

This leaves the central card goal unmet: CLI status still cannot show a real reached/matched Loki or Tempo source, and the tests' synthetic positive helper call cannot establish that production can emit that state.

Recipe: wire authoritative per-backend provenance from the existing resolved runtime/registry into both local and remote `app status` results and the `perses status` result; do not derive it from manifest flags. Add end-to-end tests where a real source is present and matched, where it is absent/unmatched, and where resolution fails, asserting the exact source ID and state through both output faces. Stop if the existing runtime/registry has no permitted source for this information; resolve the card's read/write boundary before claiming backend evidence.

## P3 — Scope and write-set

The candidate diff contains only the three declared CLI files. The restricted-path diff command exited 0 for all owner-owned paths listed above. No scope finding.

## P4 — Cleanliness chronology

The hop akte's `## Cleanliness` records removal of the four `bh-docker-dev-shared-*` containers, gives the container IDs and a post-removal empty `docker ps`/compose witness, and records that this changed local container counts. This is a host-local chronology issue only. It does not invalidate GitHub-hosted run evidence; I did not query or alter Docker/Podman during this review.

## P5 — Exact-head CI state and inherited-failure classification

Run `44850246247` is event=pull_request, head `e21b5c528923ddd610b8c5e709ff0d61294c211e`, completed/failure at 2026-11-21T01:31:27Z. Its `PR Selected Checks` is failure; `PR · Go unit · packages` and `PR · Go unit · cli-0` through `cli-3` are each completed/failure. The `owner`, go-build, go-vet, cli-gofmt and focused Python jobs succeeded. Skipped optional jobs are not passes.

Run `44854729670` for owner PR #1615 is a different head (`7fae3a288f4a7639728a10b047bda9a36e35604a`), not evidence that #1702 passed. Its packages and cli-0..3 jobs are success, while that run's overall conclusion is failure. I cannot label all #1702 failures inherited: this candidate itself has the missing human renderer while its unchanged test explicitly demands that output. The annotations available for #1702 report only the selected Go command's exit code, not the failing test name; I therefore do not attribute the packages failure to a specific test. The aggregate remains red and acceptance is not complete.

The source-level human-output defect is an actionable candidate finding. The separate #1615 success may provide a later base on which a new #1702 run can be evaluated, but it does not replace an exact-head passing required aggregate.

## Verdict and actionable recipes

**REQUEST CHANGES.** The candidate does not preserve the human witness output present in 3f7600d, and all production paths supply empty Loki/Tempo witnesses, so the positive backend-witness tests only prove helper behavior. The exact-head required aggregate is failure.

Required work:
- Restore the production human renderer in `cmd/baha/perses_lifecycle.go`; the end-to-end parity test must fail without it and pass with it.
- Supply actual per-backend provenance at the production call sites in `cmd/baha/app_status_result.go` and `cmd/baha/perses_lifecycle.go`; tests must exercise reached/matched, unmatched, and unreachable through command output, including local and remote status where supported.
- After those corrections and any agreed base integration, obtain a terminal `PR Selected Checks` success on the exact new head with required packages and CLI shards executed. Stop if the aggregate remains red or any required shard is skipped.

No product files, PR metadata, workflows, or containers were changed by this review.

## Planning repository witness and publication

Verified planning remote:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Before final publication, `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main` and the required path lookup returned:

```text
evidence/r28-welle4-2026-11-21/perses-status-backend-witness/review-2.md
```

The mission explicitly says no post to other sessions; no Codeman post was sent.

## Final identity check

```text
PR head before review = e21b5c528923ddd610b8c5e709ff0d61294c211e
PR head after review = e21b5c528923ddd610b8c5e709ff0d61294c211e
```

END_DONE codex-rev-cli2b: REQUEST CHANGES for PR #1702; exact candidate e21b5c528923ddd610b8c5e709ff0d61294c211e.
