# PR #1575 Review R2

Review role: CODEX-REVIEW r2
Review date: 2026-11-14
Card: t-20261114-r28-perses-contract-seam (0428-075)
PR: https://github.com/mcpdev80/baseharbor/pull/1575 (OPEN, DRAFT)
Reviewed candidate: dc670bfd4d32baf29afde0e4b021bfdb63f4e0be
Fetched base: 0e9ccb582f5bdcdc74049bbe3996263cdce6500c (develop)

## PLAN

1. Fetch and verify exact candidate, base, branch provenance, and hosted run state. (done)
2. Review diff against r1 recipe, configured versus reachable semantics, docs, tests, and PR #1577 overlap. (done)
3. Record SHA-specific verdict and actionable recipe in planning evidence. (done)
4. Validate and publish evidence to planning origin/main, post END, then hold for the next correction round.

## Candidate and provenance witnesses

Exact `git ls-remote` output from BaseHarbor:

`git ls-remote origin refs/heads/develop refs/pull/1575/head refs/pull/1577/head`
`0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop`
`dc670bfd4d32baf29afde0e4b021bfdb63f4e0be	refs/pull/1575/head`
`79a2bf6ccdcdc0e0423003b75066c725e445658f	refs/pull/1577/head`

The fetched #1575 head and base resolve to the same SHAs. `git merge-base --is-ancestor refs/review/develop refs/review/pr1575-r2` exited 0. The exact base-to-head log is:

`git log --format='%H %an <%ae> %s' refs/review/develop..refs/review/pr1575-r2`
`dc670bfd4d32baf29afde0e4b021bfdb63f4e0be mcpdev80 <dev@pfingstgraef.eu> fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability`
`61f76fa18897d4a0709c09c27ae67e1ded8dba20 lane-0428-075-perses-seam <lane-0428-075-perses-seam@baseharbor.dev> feat(0428-075): define optional Perses provider seam (fail-closed)`

Both commits are on the named task branch `lane-0428-075-perses-seam`; the second is the instructed correction on the existing candidate, not a second PR-head chain. The review did not modify the product branch. The candidate changes 14 files; no `.github/**` paths changed. `git diff --check` is clean.

Planning repository was verified before this evidence commit. Exact command and output:

`git rev-parse --show-toplevel`
`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`

Pre-push remote witness:

`git ls-remote origin main`
`63222b6ab1661166dd05b14dd81a85997d221abf	refs/heads/main`

## Review findings

REJECT for candidate `dc670bfd4d32baf29afde0e4b021bfdb63f4e0be`. Several R1 corrections are present, but the required public CLI tests are not present in substance.

Passed review points:

- `PersesManagementSurfaceNow(selected bool)` now uses the manifest selection and a validated pinned release to set declaration/configuration state. Reachability is a separate field and remains `unverified`; no container or health probe is claimed. `VerifyPersesManagementUIAt` does not assert runtime reachability.
- `docs/spec/provider-management-acceptance-v1.md` classifies Perses HA as unsupported for this configuration-only seam and explicitly says reachability and endpoint continuity are unverified. No supported HA claim remains.
- `internal/application/manifest.go` changed only field alignment between the first candidate and r2. `gofmt -d` on the candidate file produced no output.
- The provider implementation version `0.1.0` remains distinct from Perses product release `v0.55.1`; product version/image remain realization metadata.
- Current PR #1577 head is `79a2bf6ccdcdc0e0423003b75066c725e445658f`. Its English and German release docs now describe unselected Perses as normal/no error, selected-but-absent Perses as unsupported, and keep authentication unsupported pending real provisioning. This addresses the status split, but leaves one wording conflict to resolve before either candidate is accepted: the release note says a runtime-absent surface is “never as configured,” while this candidate defines `Provisioned` as manifest-declared configuration and can therefore set it true with reachability still unverified. Clarify that the declaration/configuration state and runtime provision/reachability are distinct; do not let the boundary text imply the declaration flag proves a running instance or say that declared configuration is absent.

Blocking finding — tests do not execute the CLI command and omit the required unknown-owner case:

- `cmd/baha/app_perses_cli_test.go:22-47` is named as a CLI status test, but it calls `recordAppliedDeployment`, `application.ApplicationManagementUISurfaces`, and `capability.PersesManagementSurfaceNow` directly. It never executes `appStatusCommand`, `appDoctorCommand`, a Cobra command, or the `baha` process. The temporary fixture does not make those helper calls a genuine CLI entry-point test.
- `cmd/baha/app_perses_cli_test.go:71-76`, `TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer`, is a no-op: it only calls `filepath.Abs(".")` and constructs an unused context. It does not create/use a temporary root or invoke a command.
- `cmd/baha/app_perses_cli_test.go:83-107` checks unsupported authentication by calling `ApplicationManagementUISurfaces` directly. The added tests contain no unknown-owner scenario and no command-level assertion that unknown ownership or missing authorization fails closed. The existing hosted shard script discovers `Test*` names with `go test ./cmd/baha -list .` and distributes them over `cli-0` through `cli-3`; the changed `cmd/baha` path selected the CLI group. Thus CI picked up the test file, but passing the test functions does not satisfy the missing command-level assertions. The round-2 handoff's claim that test (5) covers unknown ownership/missing-auth through the genuine CLI is therefore not supported by the candidate diff.

## Hosted run witness

Exact run query result: `gh run view 43642055022 --repo mcpdev80/baseharbor --json databaseId,headSha,status,conclusion,workflowName,event,displayTitle,jobs` reported `headSha=dc670bfd4d32baf29afde0e4b021bfdb63f4e0be`, `status=completed`, `conclusion=success`, `event=pull_request`, workflow `CI · Source & Quality`. The hosted run is terminal on the reviewed candidate. Job log `PR · Draft Go · cli-2` showed the `scripts/pr-go-unit-shard.py --mode cli-2` path and the passing result `PASS cli-2: 407 passed / 19 intentionally skipped / 426 discovered; CLI inventory total=1674`; the other CLI shard jobs were also successful.

Observed job results:

- `PR · Draft source and routing`: success.
- `PR · Draft Go · cli-0`: success.
- `PR · Draft Go · cli-1`: success.
- `PR · Draft Go · cli-2`: success.
- `PR · Draft Go · cli-3`: success.
- `PR · Draft Go · packages`: success.
- `Workflow policy` and `PR Selected Checks`: skipped under draft selection. No check failed. No rerun or workflow_dispatch was initiated.

## Correction recipe and stop criteria

1. Replace the faux CLI tests with tests that execute the actual public `baha status` or `baha doctor` command path using an isolated temporary root and injected dependencies, as required by the owner direction in round-2. Assert the surfaced configuration and unverified reachability fields, without starting containers or probing a nonexistent Perses service.
2. Add command-level cases for unknown ownership and missing/unsupported authorization. Assert each fails closed and never reports authorized/configured access. Keep the tests in `cmd/baha` so the existing draft Go CI selection executes them; do not change `.github/**`. Remove the no-op test or make it perform the real command invocation.
3. Reconcile boundary wording in `docs/releases/v0.4.28.md`, `docs/reference/releases.md`, and matching German counterparts with the agreed axes: manifest-selected/configured-by-declaration versus runtime provision/reachability. State that a selected but unavailable Perses surface has unsupported auth and unverified reachability; absence when not selected remains a normal non-error state. Avoid saying “never configured” for a manifest-selected declaration that this candidate exposes as configured.
4. Stop acceptance until the CLI command is genuinely executed for all required negative cases, the resulting tests are covered by the existing hosted group, and the documentation no longer conflates declared configuration with runtime reachability. Any changed candidate invalidates this review and requires fresh SHA/run evidence.

## Planning validation and repo-rule compliance

`python3 scripts/plan.py check`: 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors, 10 warnings. `git diff --check` is clean.

- Read-only product review; no product files, PR state, CI workflows, or run state changed.
- Evidence is stored only in the actual planning repository `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, never the workers bookkeeping checkout.
- No subagents used, no secrets included, and no containers started.
- Verdict is bound to the exact fetched candidate and base above.

END act-1575-review-r2 DONE — REJECT; candidate dc670bfd4d32baf29afde0e4b021bfdb63f4e0be.
