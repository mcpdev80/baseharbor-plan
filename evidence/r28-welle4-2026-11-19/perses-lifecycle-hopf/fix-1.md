# Perses lifecycle hopf — fix-1 (card 0428-084, PR #1598)

Mission: mission-084-hopf-lean.md (mission tag: 084-perses-lifecycle-hopf)
Date: 2026-11-19
Final candidate head: 3852472aa5281e6f69d38cba07cfb2cd7b9db018
Branch: lane-0428-084-perses-lifecycle (PR #1598, base develop, draft=false, mergeable=MERGEABLE)

## Wrong-zone check (planning repo)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin`
=> https://github.com/mcpdev80/baseharbor-plan.git (this is the planning repo; evidence lives here only).

## Work zone

All product work in /var/tmp/m084-hopf-clone (blob:none clone of
https://github.com/mcpdev80/baseharbor.git). No container/compose project was
started by this lane on this host (docker/podman tests are not part of this
mission; see cleanliness).

## Base attestation and provenance

- PR #1598 head at mission start (git ls-remote origin refs/pull/1598/head):
  e866723746a5c5393aba06cd5da8c8b7800788e7 — exactly the mission's cited head.
- develop at mission time and throughout (git ls-remote origin refs/heads/develop):
  da76c5cf9c963207038d5599bd130b89ecb1e8a4.
- Note: a single combined `git fetch origin develop refs/pull/1598/head` left
  FETCH_HEAD at the develop tip (last line wins); corrected by fetching the PR
  ref last. hopf started at e8667237.
- `git merge-base --is-ancestor` witnesses (all exit 0, monotone hops):
  - e866723746a5c5393aba06cd5da8c8b7800788e7 → 831c2bea ✓
  - 831c2bea8bd9b87aac71588353318e66d582c901 → 2dd8f98c ✓
  - 6e371c99be27cfc423a018fd76458402e39db86b → 3852472a ✓
  - da76c5cf9c963207038d5599bd130b89ecb1e8a4 (develop) → 3852472a ✓
  - final head 3852472a == refs/pull/1598/head == refs/heads/lane-0428-084-perses-lifecycle (ls-remote).
- `git merge-tree --write-tree origin/develop 3852472a` → exit 0, tree
  5ba01b3a20c9596926ea0e8a7d5519587518f9c8, 0 conflict markers → PR is clean.
- `git log origin/develop..HEAD` lists 20 commits; every one is this card chain
  (0428-084 lifecycle work and the 0428-075 seam commits already merged into the
  PR branch by earlier rounds: authors lane-0428-075-perses-seam,
  lane-0428-077-worker, w091-0428-091, worker-flash, lv4-verify) or my own
  fix commits (2dd8f98c, 6e371c99, 3852472a, authored lv4-verify). No foreign
  candidate is carried on top.

## Hopf history (both head states, per coordinator instruction)

1. Candidate 831c2bea8bd9b87aac71588353318e66d582c901 (run 44499778660, FAILURE):
   - documentation-classification failure. Literal job-log lines:
     - `machine_documentation_test.go:48: unclassified product command: baha app perses disable`
     - `registration_ci_readiness_test.go:82: unclassified command: baha app perses disable`
     - `human_documentation_test.go:107: machine documentation drift in docs/cli/command-index.md`
   - the new perses lifecycle commands had no classification in
     `cmd/baha/machine_coverage.go:21` (`currentCommandCoverage`): `gap` rows
     trip the fatal at `cmd/baha/machine_documentation_test.go:47-48`;
     `semantic` requires a real `machine.OperationByID` entry (same file,
     lines 50-53, `internal/machine/contract.go`).
2. Candidate 2dd8f98ca637215ae3378c1809277db6e047f375 (run 44508277727, FAILURE):
   - `PR · Validation · documentation-audit` failed:
     `DE technical integrity: FAIL (9 findings across 168 paired pages)` —
     the new literals were missing from the paired DE pages.
3. Candidate 6e371c99be27cfc423a018fd76458402e39db86b (run 44509535053, FAILURE):
   - golden-record failure: `contracts/machine_control_test.go:41: public
     discovery fixture differs from Core operation/binding registry`,
     package github.com/mcpdev80/baseharbor/contracts (cells `PR · Go unit ·
     packages` + `PR Selected Checks`).
4. Candidate 3852472aa5281e6f69d38cba07cfb2cd7b9db018 (run 44510690944, SUCCESS
   at terminal state, 20 success / 19 skipped / 0 failures, PR stays draft=false).

## Conflict resolution (step 2 of the mission)

`git merge origin/develop` produced exactly the four predicted conflicts:

- internal/application/manifest_render.go: develop-side
  `writeManagementUIYAML(&b, m.Services.ObservabilityManagementUI)` (explicit
  flag, general grammar) kept over the branch's hard-coded `true`; the
  branch-side perses rendering block below the conflict stays intact.
- internal/application/manifest_test.go: both sides kept. The develop-side
  three round-trip cases (WithoutManagementUI fail-closed,
  WithManagementUIStill round-trip, IgnoredWithoutManagementUIAndPerses
  baseline) plus my renamed duplicate set from an earlier edit pass were
  deduplicated to the develop-side set; the branch-side
  `TestManifestPersesSelectionRequiresManagementUI` (fail-closed case) — then a
  duplicate of the develop-side case — collapsed to the single surviving test,
  no function was silenced.
- add/add internal/capability/perses.go: the general form (the surface is
  deliberately NOT an IntegrationDescriptor; no capability kind) with the
  branch's Luna-review history fused in as the special case.
- add/add internal/metrics/perses_contract_test.go: same rule — branch's r2/r4
  review-history narrative plus develop's general statement, fused into one
  comment; test bodies identical.

## Classification decision per command (coordinator fix instruction)

All four commands are `semantic` with a genuine typed operation (the
`app stop`/`destroy` pattern); none needed `excluded`/`presentation`:

- `baha app perses enable` → app.perses.enable, baseharbor.app.perses.enable,
  mutating + ConfirmationRequired (internal/machine/contract.go, next to
  app.stop; registered in cmd/baha/mcp_lifecycle_extra.go; classified in
  cmd/baha/machine_coverage.go cliMachineOperations + cliSemanticModes).
- `baha app perses disable` → app.perses.disable, mutating + ConfirmationRequired.
- `baha app perses status` → app.perses.status, read_only.
- `baha app perses remove` → app.perses.remove, destructive + ConfirmationRequired.
- The `baha app perses` group row stays `presentation` (command group, Run==nil).
- CLI and MCP share one seam (executePersesLifecycle / reportPersesSurfaceStatus
  in cmd/baha/perses_lifecycle.go), so CLI -o json equals the MCP structured
  result. Machine transports converge runtime via the shared apply lifecycle;
  the deferred-to-apply notice is direct-human-CLI presentation only (per the
  existing acceptance tests' manifest-mutation-before-apply semantics).

## Regenerated artifacts (one logical change set)

- docs/reference/cli-machine-coverage.md, docs/cli/command-index.md,
  docs/de/cli/command-index.md, docs/reference/mcp.md — via the test's own
  generator `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run
  TestMachineDocumentationTracksRegistryAndCommandTree` (+ TestHumanCommandIndex).
- docs/de/reference/cli-machine-coverage.md, docs/de/reference/mcp.md — paired
  DE literals added by hand per the pattern of neighbouring rows (the DE
  technical-integrity checker compares inline literals of paired pages).
- contracts/machine/v1/control.golden.json — regenerated with the repository's
  designated generator `go run ./scripts/tools/machine-control-fixtures`
  (precedent commit 35292a67 "contracts: regenerate machine-control golden
  fixtures for secret.reveal"); verified byte-identical to the generator output,
  pure +36-line addition of the four discovery operations, no other record moved.

## Local verification (final head state)

- `go test ./contracts -run TestMachineControlGoldenRecordsMatchCoreDiscovery -count=1 -v` → PASS.
- `go test ./contracts -count=1` → ok (0.44s).
- `go test ./cmd/baha -run "TestMachineDocumentation|TestHumanDocumentation" -count=1 -v` →
  TestHumanCommandIndexTracksExactCommandMetadata PASS,
  TestMachineDocumentationTracksRegistryAndCommandTree PASS,
  TestHumanDocumentationUsesFinalInitializationPath PASS.
- `python3 scripts/check_de_translation_integrity.py` → DE technical integrity: PASS (168 paired pages).
- `bash scripts/source-readability-audit.sh` → Go file size PASS / Function span
  PASS / Regression ratchet PASS (baseline note: internal/providers/runtime/podman/lifecycle.go
  843 lines, ratchet ≤878 — unchanged, not my file).
- `gofmt -l .` → empty. `go build ./...` → OK. `go vet ./...` → OK.
- `go test ./internal/capability ./internal/metrics ./internal/application -run Perses -count=1` →
  all ok.
- `go test ./cmd/baha -count=1` (full package, this host): three failures
  (TestAppEditCommandCompleteProviderEditRunsRealLifecycle,
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication,
  TestRuntimeUpRequiresORASBeforeCoreBootstrap). Control runs prove they are
  host-environment, not candidate: TestPrepareStagedCoreGitCandidate... fails
  identically on plain develop da76c5cf (60s "native Git archive failed:
  signal: killed"), and TestRuntimeUpRequiresORASBeforeCoreBootstrap fails
  identically on plain develop with the same "container runtime orchestration
  not found" (this coordinator host exposes only a nonstandard rootful engine;
  mission rules put native runtime tests on baha-docker/baha-podman only). The
  GitHub exact-head shards for these paths are green (see CI table).

## CI — exact-head run 44510690944 on 3852472a (terminal: SUCCESS)

Executed cells (all success):

| Check | Result | Job |
| --- | --- | --- |
| Workflow policy | pass | 135513868534 |
| PR · Trusted Plan | pass | 135513869031 |
| PR · Source format | pass | 135513869087 |
| PR · Native gate plan | pass | 135513868754 |
| PR · Focused Python | pass | 135514000472 |
| PR · Go unit · cli-0 | pass | 135514000594 |
| PR · Go unit · cli-1 | pass | 135514000514 |
| PR · Go unit · cli-2 | pass | 135514000520 |
| PR · Go unit · cli-3 | pass | 135514000559 |
| PR · Go unit · owner | pass | 135514000552 |
| PR · Go unit · packages | pass | 135514000653 |
| PR · Validation · go-build | pass | 135514000803 |
| PR · Validation · go-vet | pass | 135514000675 |
| PR · Validation · cli-gofmt | pass | 135514000610 |
| PR · Validation · documentation-audit | pass | 135514000788 |
| PR · Validation · mkdocs-en-strict | pass | 135514000677 |
| PR · Validation · mkdocs-de-strict | pass | 135514000668 |
| PR · Validation · pages-candidate-build | pass | 135514000754 |
| PR · Validation · wizard-registration-tests | pass | 135514000743 |
| PR Selected Checks | pass | 135516284738 |

Skipped cells + why (the ordinary develop-targeted cells hang on
`github.event.pull_request.draft == false`; those were satisfied — skips below
come from the OTHER selectors in the same workflow, and from plan-output gating):

| Check | Skip condition (file:line) |
| --- | --- |
| PR · Draft source and routing / Draft Go · shards | `.github/workflows/ci.yml` draft-only cells; PR is draft=false since `gh pr ready 1598`. |
| PR · Main release checks / Main release Go · shards / Main release source / Release Source Preflight | `.github/workflows/ci.yml:554`/`:603`/`:652` gate these on `github.base_ref == 'main'`; this PR targets develop. |
| PR · Native · ids / Native Keycloak/Core · runtimes / Selected Runtime / Selected Core-less / Runner Interface | `.github/workflows/ci.yml:478`/`:956` gate on `needs.pr_plan.outputs.runtime_required == 'true'` / consumer mode; the impact planner (PR · Native gate plan) marked no native-runtime path required for this diff (contracts/docs/CLI classification only). |
| Targeted HA · docker / Targeted HA · podman | HA cells gated on the plan's HA-required outputs; no HA-affecting change in this candidate. |
| PR · Exact Candidate / Exact full Pre-Release / Consumer Pins / Demo Pin / Public Contracts | promotion/pin gates for merge-time and main flows, not PR-synchronize runs (ci.yml same drafting block as above). |
| validate | legacy alias cell, superseded by PR · Validation · matrix. |

`PR Selected Checks` (explicit): pass, job 135516284738 — the aggregation cell
that previously failed on all three earlier heads, green on the final head.

## Earlier runs (recorded per instruction)

- run 44499778660 (head 831c2bea): FAILURE — cli-0/cli-3 + PR Selected Checks
  (documentation classification; lines quoted above).
- run 44508277727 (head 2dd8f98c): FAILURE — documentation-audit + Go unit
  packages + PR Selected Checks (DE technical integrity, 9 findings).
- run 44509535053 (head 6e371c99): FAILURE — Go unit packages + PR Selected
  Checks (contracts/machine_control_test.go:41 golden discovery fixture).
- run 44510690944 (head 3852472a): terminal SUCCESS (20 pass / 19 skipped / 0 fail),
  mergeable=MERGEABLE, draft=false. Watched to terminal by this lane (§4.6).

## Push witnesses

- `git push origin hopf:refs/heads/lane-0428-084-perses-lifecycle` (e8667237..831c2bea, fast-forward, no force)
- `git push origin fixbase:refs/heads/lane-0428-084-perses-lifecycle` (831c2bea..2dd8f98c)
- (6e371c99), (3852472a) same branch, all fast-forwards; final ls-remote:
  3852472aa5281e6f69d38cba07cfb2cd7b9db018 refs/heads/lane-0428-084-perses-lifecycle.

## Cleanliness

- docker ps -a before: 7 pre-existing entries, all foreign (bh-local-shared-*
  stacks of ambient cores), none created by this lane.
- docker ps -a after: same 7 pre-existing foreign entries, 0 hopf/084/perses-owned
  containers, networks or volumes (filtered ls-commands return empty);
  `podman` is not installed on this host (command not found) — podman ps -a n/a.
- No compose project was started on any SSH test host by this mission.
- cleanliness: no test-owned container/network/volume/state left on this host;
  work confined to /var/tmp/m084-hopf-clone and /var/tmp/hopf-base-check.

## Scope fidelity

- No merge performed, no review verdict, no `.github/**` or `scripts/**` edit,
  no rerun/workflow_dispatch, security.go untouched, no new test functions
  (the develop-side perses selection tests entered via the merge, as the
  mission's resolution rule required), no card status change, no subagent,
  only `git add <file>`, everything outside the product repo lives under /var/tmp.
- No .github/** change was needed (the CI-wiring duty of AGENTS 5.3: these
  tests are already executed by the `pr_unit_shards` cells, job definition at
  `.github/workflows/ci.yml:1134`, the if-condition line is `:1137`
  (`... && github.event.pull_request.draft == false && needs.pr_plan.outputs.unit_scope != 'none'`)),
  and the workflow's pull_request trigger is at `:30` (draft == false gate);
  trigger: pull_request to develop/lane- bases.

END_DONE mission-084-hopf-lean.md: hopf complete — PR #1598 head 3852472aa5281e6f69d38cba07cfb2cd7b9db018, exact-head run 44510690944 terminal SUCCESS (20 pass/19 skipped), draft=false, mergeable.
