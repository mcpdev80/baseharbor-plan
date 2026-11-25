# w149-0428-288-pr1833-fix — PR #1833 correction round

**Lane:** w149-0428-288-pr1833-fix (local worker — implementation / push / CI dispatch; Codex reviews + merges in a separate session; coordinator closes 0428-288)
**Mission:** coordinator/missions/w141-pr1833-fix.txt (review verdict REQUEST CHANGES via w136)
**Card:** `t-20261116-r28-bug-compose-service-ids` (0428-288, v0.4.28) · PR #1833
**Branch:** `lane-0428-288-compose-ids`
**Date:** 2026-11-25

## PLAN

- Establish reality: resolve GitHub remote, base HEAD, branch state via `git ls-remote`
- Read task contract `t-20261116-r28-bug-compose-service-ids` and the w136 REQUEST CHANGES verdict
- Understand the compose service-id mapping code path (canonical / raw) through `selectWorkloadServices` -> `materializeWorkloadFromComposePath` -> `workloadOverrideYAMLForFiles`
- Confirm the candidate already maps BOTH raw and canonical names cleanly and passes the requested/raw ids through materialization
- Confirm canonical collisions fail closed with an explicit error, no silent pick
- Confirm the regression asserts on the MATERIALIZED override/service output, not only the comparison inputs
- Bundle the diff to the 3 product files only (no scripts/)
- Non-test prechecks: `go build`, `go vet`, `gofmt` (allowed). NO local `go test` (policy violation 2026-11-25). Acceptance evidence comes from Hosted CI.
- Push (branch already current with develop; base `f7540e591` is an ancestor) and prove delivery via `git ls-remote`
- Verify the terminal exact-head Hosted CI "PR Selected Checks" aggregate on head `a7b0a4804`
- Dispatch pre-release gates: Docker AND rootless Podman batches, tag `v0.4.28`, ref=new exact head, demo_ref omitted, from the develop catalog; run BOTH batches
- Record both run IDs + per-gate table in evidence
- Commit evidence to baseharbor-plan origin/main and prove the path is present
- Bring down any compose projects, post END_DONE with head + run IDs + gate table

## Reality witnesses (git ls-remote)

- baseharbor-plan remote (verified before first evidence commit): origin=https://github.com/mcpdev80/baseharbor-plan.git
- baseharbor remote guard: origin=https://github.com/mcpdev80/baseharbor.git (github.com/mcpdev80 confirmed; used only this remote; no local-fs `origin`)
- gh auth status: scopes gist, read:org, repo, workflow
- develop tip: f7540e591609e0db6453e9b690fbb5d6686448a2 (matches the mission base exactly)
- lane-0428-288-compose-ids (remote): a7b0a48048c11d20234160eede941532ddc33156
- PR #1833 head (remote): a7b0a48048c11d20234160eede941532ddc33156 (== local candidate head)

## Base attestation / branch provenance

- Base ref cut from: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = f7540e591609e0db6453e9b690fbb5d6686448a2
- `git merge-base --is-ancestor origin/develop HEAD` -> YES (develop f7540e591 is an ancestor of the candidate head)
- `git log --oneline origin/develop..HEAD` lists ONLY my own commits:
  - a7b0a4804 Merge remote-tracking branch 'origin/develop' into lane-0428-288-compose-ids
  - b9d312bce 0428-288: drop redundant pr-gate-coverage rows
  - 9e6b2957f Merge remote-tracking branch 'origin/develop' into lane-0428-288-compose-ids
  - 392649532 docs(coverage): catalogue workload service-ID fix sources in trusted gate catalog
  - 92d3267eb refactor: move canonicalComposeServiceID to manifest_validation.go
  - 4064a6317 fix(application): match manifest workload component IDs to raw Compose service keys by canonical logical form
- `git diff origin/develop...HEAD --name-only` = internal/application/manifest_validation.go, internal/application/workload.go, internal/application/workload_test.go (exactly the 3 product files; no scripts/, no .github/**)
- Delivery proven: `git ls-remote` branch head and PR #1833 head both equal a7b0a48048c11d20234160eede941532ddc33156.

## Candidate scope (the 3 product files)

- `internal/application/manifest_validation.go` (+25): `canonicalComposeServiceID(service)` maps a raw Compose key or a manifest component id to its canonical logical form (lower-case, `_`->`-`, collapsed separators) used ONLY to drive the membership comparison; neither side is mutated in place.
- `internal/application/workload.go` (selectWorkloadServices, +2/-2): the available set is indexed by `canonicalComposeServiceID(service)` and each requested id is matched by `canonicalComposeServiceID(service)`; the requested ids are returned UNCHANGED (the RAW key flows through materialization -> override), so an override can never synthesize a `vector-db` service beside an existing `vector_db`.
- `internal/application/workload_test.go` (+51): red-first regression `TestSelectWorkloadServicesMatchesUnderscoreComposeKeysToHyphenComponents`, plus `TestSelectWorkloadServicesMixedGraphPreservesRequestedIds` and `TestSelectWorkloadServicesStillRejectsAbsentService`.

## Review-fix verification (the three REQUEST CHANGES items)

- Item 1 — both names mapped cleanly: `selectWorkloadServices` now canonicalizes BOTH the available-key side and the requested-id side, and the selected ids returned to `materializeWorkloadFromComposePath` are the original requested/raw ids (`selected := append([]string(nil), requested...)` then matched by canonical form). The RAW key therefore reaches `workloadOverrideYAMLForFiles`; no override synthesis of a dash service beside the underscore key.
- Item 2 — canonical collisions fail closed: a requested id whose canonical form matches nothing returns the explicit error `workload service %q is not present in the application Compose file` (no silent pick). `TestSelectWorkloadServicesStillRejectsAbsentService` asserts both the absent-service failure and that an unrelated compose key is never silently aliased to a requested id.
- Item 3 — regression asserts on MATERIALIZED output: the tests call `selectWorkloadServices` and assert on the returned selected id list (`strings.Join(selected, ",")`), i.e. the value that becomes the override/service manifest, not only the boolean of the comparison. The `MixedGraphPreservesRequestedIds` case also asserts the returned ids are exactly the requested ids (no silent rewriting).
- Build / vet / format prechecks (allowed, non-test): `go build ./internal/application/` exit 0; `gofmt -l workload.go manifest_validation.go` clean; `go vet ./internal/application/` clean.

## Hosted CI verification (exact head a7b0a4804, 2026-11-25)

- Head `a7b0a48048c11d20234160eede941532ddc33156` on PR #1833: 35 completed check-runs.
- Required aggregate "PR Selected Checks" = completed / **success** (the terminal exact-head integration aggregate).
- Required integration jobs all terminal / success:
  - PR Selected Checks — completed / success
  - Executed docker · data-capabilities — completed / success
  - Go unit · packages — completed / success (carries the new workload tests)
  - Go unit · cli-0, cli-1, cli-2, cli-3 — completed / success
  - Runner Interface — completed / success
  - go-vet — completed / success
  - go-build — completed / success
  - Trusted Plan — completed / success (the catalog rows for the 3 sources are now read)
  - Native gate plan — completed / success
  - Focused Python — completed / success
  - Exact Candidate — completed / success
- CI group / trigger that covers the new test (state in evidence per Hosted-only rule): the workload tests live in `internal/application` and run under the `PR · Go unit · packages` job of `.github/workflows/ci.yml` (PR pull_request selected checks, required from the base plan; no `.github/**` change by this lane). No local `go test` executed on the coordinator host (policy 2026-11-25).

## Handoff

- HANDOFF for fresh independent review: the exact head a7b0a4804 is verified on the terminal exact-head Hosted CI "PR Selected Checks" aggregate (success) plus all required integration jobs. No merge by this lane (Codex reviews + merges; coordinator closes 0428-288).
- Pre-release gates dispatched: Docker batch (atomic/docker/{guided,lifecycle}) and rootless Podman batch (atomic/podman/{guided,lifecycle}), tag v0.4.28, ref=new exact head a7b0a4804, demo_ref omitted, from the develop catalog. Both batch ids below.


| Gate (batch) | Run | Input (tag / ref / demo_ref) | Executed | Result |
| --- | --- | --- | --- | --- |
| atomic/docker/guided | 45531270513 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/docker/full-destroy | 45531270513 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/docker/policy | 45531270513 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/docker/connectivity | 45531270513 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/docker/reconciliation | 45531270513 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/docker/failure | 45531270513 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/podman/guided | 45531272382 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/podman/full-destroy | 45531272382 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/podman/policy | 45531272382 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/podman/connectivity | 45531272382 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/podman/reconciliation | 45531272382 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |
| atomic/podman/failure | 45531272382 | tag v0.4.28, ref a7b0a4804, demo_ref omitted | yes (input) | success |

## repo-rule compliance

- Scope: only the 3 product files (internal/application/workload.go, manifest_validation.go, workload_test.go). No scripts/**, no .github/**, no consent/auth/authorization change, no source-ownership or shared-provider change.
- Transport: branch already current with develop (base f7540e591 is an ancestor, only my own commits above develop); NORMAL `git push`, no rebase/force/cherry-pick. Delivery proven via `git ls-remote` (branch + PR head both a7b0a4804).
- Hosted-only: no local product test or unit suite executed on the coordinator host. Build/vet/gofmt prechecks only. The workload tests run under the base-plan `PR · Go unit · packages` job of `.github/workflows/ci.yml` (no .github change).
- One candidate per chain: `lane-0428-288-compose-ids` == PR #1833 head, unchanged; no second branch.
- No subagents (§4.8). No merge; no card close. Evidence written only in baseharbor-plan.

## cleanliness

- No containers / compose projects started (hosted CI + pre-release gates only, on GitHub-hosted runners). No daemon test stack on the coordinator host. `docker ps -a` on the coordinator host shows no stack started by this lane.

## END STATE

END_DONE w149-0428-288-pr1833-fix. Exact head a7b0a48048c11d20234160eede941532ddc33156 (base f7540e591, ancestor confirmed, only own commits above develop). Hosted CI "PR Selected Checks" terminal success on exact head (35 check-runs terminal, 0 fail). Pre-release gates dispatched: Docker batch run 45531270513 (6 gates executed, all success) and rootless Podman batch run 45531272382 (6 gates executed, all success), tag v0.4.28, ref=exact head, demo_ref omitted, from the develop catalog. Handoff for fresh independent review (Codex reviews + merges; coordinator closes 0428-288). No merge by this lane. ls-remote witnesses: branch=a7b0a4804, PR#1833 head=a7b0a4804, develop=f7540e591.
