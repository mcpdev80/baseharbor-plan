# round-2 — 0427-131 (r2) logs top-level: drift fix + pre-existing proof + green Validation

- Card: t-20261108-bughunt-0427-logs-command-gap (0427-131)
- Mission: mission-131-r2.md (recipe act-1456-review.md, points 1-3; point 4 DE-coverage OK)
- Shift/round: r27-welle5-folge-2026-11-08 / round-2
- Worker session: flash lane (.models/flash)
- Repo: mcpdev80/baseharbor (product)
- Write-set (unchanged): cmd/baha root wiring + cmd/baha regression test + docs command-index/machine-coverage (EN + DE)
- PR: #1456, branch work/w131-logs-command-gap, base develop

## Planning repo attestation (WRONG-ZONE check)

Command: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin`
Output: `https://github.com/mcpdev80/baseharbor-plan.git`
This is the planning repo (NOT workers/baseharbor-plan). Evidence committed here only.

## PLAN

1. Verify reality: ls-remote PR #1456 head (27ef9044) + develop (07ae6c3e9), gh pr view (CONFLICTING/DIRTY), planning repo origin/main (3b5246f4).
2. Set up worktree in my persistent zone (workers/.models/flash/wt) on the named candidate branch, fetch develop + pr-1456 refs.
3. DRIFT: merge current develop 07ae6c3e9 into the candidate branch; resolve the single conflict in cmd/baha/machine_coverage.go.
4. Prove ancestry: develop HEAD is-ancestor of candidate; log line lists only my own commits.
5. Push updated candidate branch (PR #1456 becomes conflict-free; develop MERGEABLE/CLEAN).
6. Pre-existing proof on baha-docker: run the exact ci.yml integration selection on candidate AND clean develop with BASEHARBOR_CI_RUNTIME_INTEGRATION=1, same-fixture compare.
7. Observe the PR-triggered run to terminal and record run-id + per-job results.
8. If comparison showed a real new failure in my alias path, minimal-fix in write-set + regression.
9. Bring down my VM compose projects before END (ps-witness).
10. Write this evidence, commit + push to baseharbor-plan origin/main, verify path present.
11. END post to coordinator with candidate SHA.

## Base attestation and ancestry proof

- develop HEAD (base I merged onto): 07ae6c3e91b081a189266ca4b162ba705d4aa78f (`git ls-remote origin develop`)
- candidate head before r2 (old, conflicting): 27ef90449be7ad53a4d6011ad90ff83b36c...  (round-1 head, cut from stale base 8bda98c1)
- new candidate head after r2 merge: 0920086920f8f88949c91c712237d3e47bd9854e (the single integration candidate; same branch, no second branch)
- Merge commit: 092008692 (Merge remote-tracking branch 'refs/remotes/lane-origin/develop' into work/w131-logs-command-gap)
- merge-base(candidate, develop) after merge = 07ae6c3e9 == develop HEAD (clean, conflict-free)
- Ancestor witness: `git merge-base --is-ancestor refs/remotes/lane-origin/develop HEAD` -> exit 0 (develop 07ae6c3e9 IS an ancestor of 092008692)
- `git log --oneline refs/remotes/lane-origin/develop..HEAD` lists EXACTLY my own commits (no foreign candidate carried on top):
  - 092008692 Merge develop into work/w131-logs-command-gap
  - 27ef90449 docs(de): normalize trailing whitespace in command-index
  - cd0d7e3ef docs(de): add baha logs row to machine-coverage for DE parity
  - 8e93b08bd fix(cmd/baha): add top-level 'baha logs' shorthand to app logs
- Net diff vs develop (`git diff --name-only origin/develop..HEAD`) is confined to the write-set only (no .github/**):
  - cmd/baha/commands.go
  - cmd/baha/human_cli_canonical_contract_test.go
  - cmd/baha/machine_coverage.go
  - docs/cli/command-index.md
  - docs/de/cli/command-index.md
  - docs/reference/cli-machine-coverage.md
  - docs/de/reference/cli-machine-coverage.md

## Point 1 — DRIFT resolution (real conflict fix)

GitHub reported the old head 27ef9044 as mergeable=CONFLICTING / mergeStateStatus=DIRTY against develop 07ae6c3e9.
Merging origin/develop 07ae6c3e9 into the candidate produced exactly one content conflict:
- cmd/baha/machine_coverage.go, `cliExcludedCommands` map. The develop side added two rows
  ("baha access assign", "baha access offboard") with wider gofmt key alignment; my side added the "baha logs"
  shorthand row with the previous alignment. I resolved to the union — develop's two new rows plus my single
  "baha logs" row — under develop's wider alignment, and confirmed `gofmt -l` reports the file clean
  (gofmt owns the column alignment). All other touched files (commands.go, the four docs files) auto-merged;
  my "baha logs" rows survived in all four docs files.
- Verification before commit: `go build ./cmd/baha` = 0; `go vet ./cmd/baha` = 0; targeted CLI-surface tests
  (TestCanonicalLogsCommandIsDiscoverable, TestMachineCoverageCIRealTreeAndJSONClassification,
  TestHumanCommandIndexTracksExactCommandMetadata, TestMachineDocumentationTracksRegistryAndCommandTree) = PASS.

After push, `gh pr view 1456` reports mergeable=MERGEABLE, mergeStateStatus=CLEAN on head 092008692.

## Point 2 — Pre-existing comparison (corrected, same-fixture, gate=1)

Method (faithfully mirrors .github/workflows/ci.yml:342-349): on the named host baha-docker (docker 29.8.1,
go1.26.8, tmpfs TMPDIR, -mod=mod), with BASEHARBOR_CI_RUNTIME_INTEGRATION=1 and BASEHARBOR_TEST_RUNTIME=docker,
run the exact selection:
  go test -p 1 ./cmd/baha -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI)$' -count=1 -v
Two independent git worktrees from neutral production paths: clean develop 07ae6c3e9, and candidate 092008692.

Per-test outcomes (identical on both sides):

| Test | clean develop 07ae6c3e9 | candidate 092008692 |
| --- | --- | --- |
| TestRepositoryWorkflowRealLifecycle | FAIL — `app_repository_integration_test.go:48: unknown option repo-e2e` | FAIL — same `unknown option repo-e2e` |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | FAIL — `app_workload_integration_test.go:105: ... deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable` | FAIL — same line (:105) |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | FAIL — `:245` no authoritative installation owner | FAIL — `:245` same |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | FAIL — `:405` no authoritative installation owner | FAIL — `:405` same |
| TestMultiInstanceComposeLifecycleInCI | no PASS/FAIL/SKIP line emitted (suite aborts at the earlier tests) | no PASS/FAIL/SKIP line emitted (same) |

Both sides: `FAIL github.com/mcpdev80/baseharbor/cmd/baha` (develop 120.1s, candidate 154.7s). The failure
signatures are IDENTICAL between candidate and clean develop. Therefore:
- The runtime-integration failure is NOT introduced by the "baha logs" path. Under the recipe rule (fix point 2:
  "only when develop is red despite everything is it pre-existing"), clean develop IS red under the same gate ->
  pre-existing / environmental, so there is no candidate-caused failure to fix.
- The cause is a shared trust-plane prerequisite: `ensureRuntimeIntegrationTrustPlane` cannot establish an
  authoritative installation owner on this VM, so the repository-workload applies fail closed on deployment
  state, and the repo-e2e workflow driver is unknown to this baha build. Neither lives in this card's write-set
  (cmd/baha root command wiring + docs only). Point 4 (minimal-fix in the alias path) is therefore a no-op:
  the comparison surfaced no new error in my path.

Contrast with the old hosted workflow_dispatch failure (round-1): that old candidate 27ef9044 (based on the stale
8bda98c1) failed with a `--confirm-candidate` consent error. The new merged candidate 092008692 inherits develop's
consent-retry fixture (runRepositoryFixtureApply auto-rebinds the printed confirm digest), so that consent error no
longer appears; both the new candidate and clean develop now fail at the same, later installation-owner/trust-plane
prerequisite. The old consent error was an artifact of the pre-merge stale base, not of the "baha logs" change.

## Point 3 — PR-triggered Validation green on the exact new head

The push to work/w131-logs-command-gap fired a genuine `pull_request` event run (no manual dispatch, no rerun).
- Run id: 42463334690; event: pull_request; headSha: 0920086920f8f88949c91c712237d3e47bd9854e (exact candidate);
  status: completed; conclusion: success. Observed to terminal by this lane (AGENTS 4.6).
- `gh pr checks 1456` on head 092008692:
  - PASS: PR · Source format; PR · Trusted Plan; PR · Focused Python; PR Selected Checks;
    PR · Validation · documentation-audit; PR · Validation · cli-gofmt; PR · Validation · mkdocs-en-strict;
    PR · Validation · mkdocs-de-strict; PR · Validation · go-build; PR · Validation · go-vet;
    PR · Validation · go-unit-tests; PR · Validation · pages-candidate-build;
    PR · Validation · wizard-registration-tests.
  - skipping (not scheduled for this diff): validate; PR · Exact Candidate; PR · Demo Pin; PR · Consumer Pins;
    PR · Public Contracts; PR · Runner Interface; PR · Selected Runtime; PR · Native Keycloak/Core;
    Targeted HA · docker; Targeted HA · podman; Release Source Preflight.
  - The heavyweight `validate` runtime-integration job and the native/HA matrix are skipped because my net diff
    touches only cmd/baha root command wiring + docs — no runtime path (CI execution discipline: select checks
    from actual impact; no runtime-path change, so the shared-runner runtime-integration gate is not triggered).

## Repo-rule compliance

- Write-set unchanged and minimal: cmd/baha root-command wiring + cmd/baha regression test + EN/DE command-index
  and machine-coverage docs only. The single DRIFT conflict was resolved inside that write-set (machine_coverage.go).
- No .github/** edit, no rerun, no workflow_dispatch, no manual trigger. The green result came from the normal
  push-triggered pull_request run 42463334690. (Consistency note vs round-1: round-1's repo-rule text said "no
  workflow_dispatch" while a workflow_dispatch run had in fact been triggered; round-2 has no dispatch at all.)
- Docker integration comparison runs only on the named SSH host baha-docker, never on this coordinator/session
  host. No container or compose project was started on the session host.
- VM compose hygiene: the four compose projects created by the comparison bootstrap on baha-docker
  (bh-w169-ci-bootstrap-59c51d74-core-shared, bh-w169-ci-bootstrap-59c51d74-shared,
  bh-w169-ci-bootstrap-d2864ad1-core-shared, bh-w169-ci-bootstrap-d2864ad1-shared) were brought DOWN with
  `docker compose -p <name> down -v --remove-orphans` before END. ps-witness: `docker ps -a | grep -iE
  'w169|w131|ci-bootstrap'` = 0; `docker compose ls` shows no bh-w169 projects.
- One integration candidate per chain: continued the named branch work/w131-logs-command-gap (PR #1456). No second
  branch was created; no force-push. ls-remote shows refs/heads/work/w131-logs-command-gap == refs/pull/1456/head
  == 0920086920f8f88949c91c712237d3e47bd9854e.
- No subagents (directive 4.8): every step executed in this session.
- Evidence lives only in baseharbor-plan; no .evidence/ in the product repo, no main-branch product writes.
- Base attestation + ancestry (merge-base --is-ancestor develop HEAD = 0; log line lists only my own commits)
  recorded above.

## END

END_DONE mission-131-r2.md — PR #1456 candidate head 0920086920f8f88949c91c712237d3e47bd9854e: DRIFT resolved
(develop 07ae6c3e9 merged, ancestry-clean, PR MERGEABLE/CLEAN), runtime-integration failure proven pre-existing
by the same-fixture baha-docker comparison (clean develop red identically), PR · Validation green on the exact
head (run 42463334690, event pull_request, conclusion success). Point 4 no-op (no new error in my alias path).
