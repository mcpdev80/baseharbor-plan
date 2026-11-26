# w279-0428-078-1650rei — Reissue 0428-078 (PR #1650 lineage)

MISSION: `coordinator/missions/w279-0428-078-1650reissue.txt`. Clean single-lane reissue of the SAME reviewed content from old head `37c4d847ca377d1555163ac4791c8ba08b85de77` onto a fresh single-lane branch. No history rewrite, no force-push, no cherry-pick of foreign commits.

## Visible Ansatz Block (before first commit)

- Canonical owner VERBATIM (fetched from origin/main at runtime): `w165-0428-078-pr1650-basehop`
- git user.name I will use: `w165-0428-078-pr1650-basehop`
- git user.email I will use: `w165-0428-078-pr1650-basehop@baseharbor.local`
- Literal git commit invocation: `git -c user.name=w165-0428-078-pr1650-basehop -c user.email=w165-0428-078-pr1650-basehop@baseharbor.local commit`
- Pre-push gate line: `git log --format='%h %an %cn %s' origin/develop..HEAD` shows ONLY that identity

## Base attestation

- Planning remote (verified first): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin  https://github.com/mcpdev80/baseharbor-plan.git`
- develop SHA (ls-remote, real GitHub https://github.com/mcpdev80/baseharbor.git): `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (matches mission candidate)
- Old contaminated head (audit-only, stays): `37c4d847ca377d1555163ac4791c8ba08b85de77`

## Reviewed write-set (from `git diff --name-status origin/develop...37c4d847c`)

- M cmd/baha/app_perses_cli_test.go
- M cmd/baha/app_status_result.go
- A internal/metrics/identity_dashboard_witness.go
- M scripts/pr-gate-coverage.json

## Steps taken

1. `git fetch origin` on baseharbor (shared checkout, `origin` = https://github.com/mcpdev80/baseharbor.git — resolved via `git remote -v`, NOT a local path).
2. ls-remote witness of develop: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`.
3. `git switch -c w279-0428-078-pr1650-reissue origin/develop` from develop.
4. Enumerated reviewed write-set via `git diff --name-status origin/develop...37c4d847c`.
5. Re-applied exact reviewed write-set per file: `git checkout 37c4d847c -- cmd/baha/app_perses_cli_test.go cmd/baha/app_status_result.go internal/metrics/identity_dashboard_witness.go scripts/pr-gate-coverage.json`.
6. Committed with canonical owner identity (single commit).
7. PAYLOAD GUARD passed (file-for-file equal to reviewed write-set).
8. Pre-checks (NO local test execution): gofmt clean on Go files, `go vet` exit 0, `go build ./cmd/baha` exit 0.
9. Pushed branch via origin (GitHub). Proved delivery via ls-remote (SHA 43326cf57).
10. Opened PR #1855 against develop with old-PR reference, payload guard, identity proof. Did NOT close #1650.

## PAYLOAD GUARD (`git diff origin/develop...HEAD --name-status`)

```
M cmd/baha/app_perses_cli_test.go
M cmd/baha/app_status_result.go
A internal/metrics/identity_dashboard_witness.go
M scripts/pr-gate-coverage.json
```

File-for-file equal to reviewed write-set: YES. HEAD content identical to reviewed old head 37c4d847c: YES. `merge-base --is-ancestor origin/develop HEAD`: YES.

## IDENTITY PROOF (`git log --format='%h %an %cn %s' origin/develop..HEAD`)

```
43326cf57 w165-0428-078-pr1650-basehop w165-0428-078-pr1650-basehop 0428-078: reissue reviewed Perses identity dashboard content on single-lane branch
```

Single commit, single identity. No foreign commits carried.

## PR #1855

- URL: https://github.com/mcpdev80/baseharbor/pull/1855
- state=OPEN, draft=false, mergeable=MERGEABLE, head=43326cf57 (untouched after creation), base=develop ac7c970fe, reviewDecision=none (handoff to w267 for review).

## Run observed (Eigenes-Run-Pflicht): run 45743494737

- Run URL: https://github.com/mcpdev80/baseharbor/actions/runs/45743494737
- Event: pull_request, attempt=1, created 2026-11-26T02:35:59Z, terminal 2026-11-26T02:56:15Z
- Status: completed / SUCCESS on exact head 43326cf57 (base develop ac7c970fe)
- Census (per_page=100): total 43, executed success 27, failure 0, skipped 16, running 0.

### Executed jobs (27, all success)

- PR Selected Checks
- PR · Selected Runtime (atomic/podman/data-capabilities) / Executed podman · data-capabilities
- PR · Selected Runtime (atomic/docker/data-capabilities) / Executed docker · data-capabilities
- PR · Selected Runtime (atomic/podman/observability) / Executed podman · observability
- PR · Selected Runtime (atomic/docker/observability) / Executed docker · observability
- PR · Validation · ci-policy
- PR · Go unit · owner
- PR · Go unit · packages
- PR · Validation · cli-gofmt
- PR · Validation · pr-planner-tests
- PR · Validation · go-build
- PR · Validation · ci-executor-tests
- PR · Validation · receipt-execution-tests
- PR · Validation · go-vet
- PR · Go unit · cli-0
- PR · Go unit · cli-1
- PR · Go unit · cli-2
- PR · Go unit · cli-3
- PR · Demo Pin
- PR · Runner Interface
- PR · Exact Candidate
- PR · Focused Python
- PR · Candidate-added checks (advisory)
- PR · Native gate plan
- PR · Trusted Plan
- PR · Source format
- Workflow policy

### Skipped jobs (16) — release/core/HA gates not selected by this diff

- PR · Main release checks, PR · Public Contracts, PR · Selected Core-less, PR · Native Keycloak/Core, PR · Consumer Pins, PR · Native · ${{ matrix.id }}, PR · Main release Go · ${{ matrix.shard }}, Targeted · Workstation onboarding, validate, PR · Draft source and routing, PR · Exact full Pre-Release, Targeted HA · podman, PR · Draft Go · ${{ matrix.shard }}, Release Source Preflight, PR · Main release source, Targeted HA · docker

### Native gate behaviour proof (log lines)

- Native gate plan job `Select exact PR native impact` step = success. Run log shows checkout `ref: ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (exact develop base), `repository: mcpdev80/baseharbor`, on GitHub-hosted shared runner (Azure centralus, ubuntu-26.04).
- Trusted Plan job steps all success: `Detect owner/node changes from the exact PR source diff`, `Resolve exact immutable PR inputs using trusted base policy`, `Route only required Go tests into mandatory parallel shards`.
- Source format = success.
- All 4 selected runtime gates (docker/podman data-capabilities + observability) = success, confirming the diff selected and executed the native runtime gates rather than skipping them.

## Second distinct trigger — HANDLED BY w267 (coordinator hold)

The second distinct pull_request run on the exact head is created by CODEX (w267) via close+reopen. w267 continues the pair + review. I did NOT self-trigger, did NOT rerun, did NOT merge or close #1650.

## Old PR #1650 disposition

#1650 remains OPEN, base=develop, head=`lane-0428-078-perses-identity-on-resolver` (contaminated-lineage audit). NOT closed by me — closure is a Codex/Owner action.

## Scope compliance

NO merges, NO cards, NO .github writes, NO plan-main pushes, NO workflow_dispatch. PR written via gh pr create on the product repo; akte published on own plan branch + plan PR. Nothing beyond the reissued write-set.

## Cleanliness

- No containers/compose projects started (no docker/podman run).
- Temporary files removed: baseharbor/.w279-payload-guard.txt, /tmp/baseharbor-baha-w279, /tmp/w279-pr-body.md, /tmp/w279-checks1.json.
- Working tree clean: `git status` shows no untracked/modified files beyond the committed write-set.

## END_DONE

- New head SHA: `43326cf57f1a3a8d73f2b9289e8c5ad00b74782a`
- Base develop SHA (absorbed): `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`
- Identity proof: single commit authored by `w165-0428-078-pr1650-basehop` (see IDENTITY PROOF above).
- Observed run: 45743494737 (pull_request attempt=1) SUCCESS on exact head 43326cf57 — 27 executed, 0 failure, 16 skipped; native gate plan/Trusted Plan/Source format + all 4 selected runtime gates executed.
- Second distinct run: pending, created by w267 (coordinator-authorized close+reopen).
- New PR: #1855 (OPEN, MERGEABLE, draft=false).
- Plan PR: pending (own plan branch published; plan PR open by coordinator).
