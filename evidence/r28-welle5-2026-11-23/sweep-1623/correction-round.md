# PR-SWEEP #1623 — CORRECTION ROUND: failing Draft Go CLI tests FIXED

- lane: w21-pr1702-0428-142-compat
- card: 0428-063 (PR #1623, draft)
- candidate head: d3f56709cc553279e6b4e3164da05590fe08a041 (hop onto latest develop 826d498fc = b3df96348)
- CI: synchronize run 45137189611 on d3f56709c — Draft Go shards cli-0..cli-3 + packages ALL pass; required aggregate checks (Trusted Plan / PR Selected Checks) SKIPPED because PR is draft and GitHub exposes no API to clear draft state
- END lane: DONE (primary objective met; draft-state required-check run blocked — see BLOCKED note)

## PLAN

1. Read mission m_084_1623fix.md.g: classify the 3 failing Draft Go CLI shards + minimal fix in authorized write-set, hop onto develop, push, EXACT hosted run.
2. Attest latest develop = b3df96348 (git ls-remote). #1623 branch = 900be2612 (parents 4cbf9296 + develop e8acf7405).
3. Fetched failed run 45102088584 logs — captured exact failing test lines + job-ids (cli-1 137455015115, cli-2 137455014783, cli-3 137455015204).
4. Classify each failing test individually against the #1623 diff.
5. Apply minimal fix in authorized write-set (cmd/baha, internal/operatorauth, docs). Re-run the failing tests locally with the sanctioned named form — PASS. Full cmd/baha suite PASS. Docs audit PASS.
6. Hop --no-ff onto latest develop (catalog byte-identical, .github untouched), resolve the single merge conflict (app_access.go), regenerate docs from command tree, commit, push.
7. Run EXACT hosted CI to terminal; capture per-shard pass/fail.
8. Publish akte. Report draft-state blocker.

## BASE ATTESTATION

- develop head at hop: 826d498fc1ae9524112d07477a8809798d8272a7 (= b3df96348, git rev-parse origin/develop, git fetch origin develop)
- HEAD parents: d3f56709c -> 804199430 (my fix) + 826d498fc (develop)
- 826d498fc IS ancestor of HEAD (git merge-base --is-ancestor origin/develop HEAD)
- #1623 base e8acf7405 IS ancestor of develop (git merge-base --is-ancestor e8acf7405 origin/develop)

## BRANCH PROVENANCE

git log --oneline origin/develop..HEAD (own commits + hop merge, no foreign candidate carried):
- d3f56709c Merge remote-tracking branch 'origin/develop' into HEAD
- 804199430 fix(0428-063): usage validation before operator-auth gate for guided logs/exec
- 900be2612 Merge remote-tracking branch 'origin/develop' into HEAD
- 4cbf92960 Reject component filters without a workload contract
- accd46da1 Fix CLI application interaction behavior
- 8014d71ea ci: trigger qualifying pull_request run — card t-20261114-r28-cli2-app-interact
- e9c313c5a Merge remote-tracking branch 'origin/cli2-identity-secrets-head' into lane-0428-063-cli2-app-interact
- 4463ac617 Merge branch 'cli2-identity-secrets-head' into lane-0428-063-cli2-app-interact (base-heal r2)
- 7ee9c8808 Merge remote-tracking branch 'origin/cli2-identity-secrets-head' into heal-063
- 1004ecd5f Merge remote-tracking branch 'origin/develop' into lane-0428-063-cli2-app-interact
- beb2ee585 cmd/baha: exit-status preservation keeps a plain runtime error identity (0428-063 refinement)
- 78e8257eb cmd/baha: guided app logs/exec/urls over the status read view (0428-063)

## ROOT-CAUSE CLASSIFICATION (all (a) PRODUCT REGRESSION from #1623 change window)

The 4 cmd/baha failures share ONE root cause. The #1623 guided logs/exec commands resolve the application through selectWorkloadComponentsForCommand -> resolveApplication -> resolveApplicationEnvironment. That resolution fires ensureOperatorAuthForBoundary DURING resolution, BEFORE the command's own usage validation (--follow/--json conflict, invalid component "nosuch", ambiguous exec selection). Because the CLI runWithIO path resets NonInteractive=false (extractGlobalOutputOptions), noInput(ctx)=false, so operator-auth hits the "operator authentication needs interactive setup but input is not a terminal" path (operator_auth_boundary.go:117) instead of the intended usage error.

Per-fail classification:
- TestGuidedLogsJSONNeverFollowsAndFailsClosedNoninteractive (:198): expects "--follow cannot be combined with JSON output"; got operator-auth. (a)
- TestGuidedLogsDerivesUniqueComponentNoninteractive (:228): expects single-component derivation/guided; got operator-auth. (a)
- TestGuidedLogsValidationHappensBeforeAnyRuntimeCall (:241): expects "not selected by the application contract" for "app logs nosuch"; got operator-auth. (a)
- TestGuidedExecNonInteractiveAmbiguityFailsClosed (:359): expects "requires a workload component"; got operator-auth. (a)
- TestHumanCommandIndexTracksExactCommandMetadata (human_documentation_test.go:107) + TestMachineDocumentationTracksRegistryAndCommandTree (machine_documentation_test.go:37): command-index.md / mcp.md drift. (a) stale command-index/mcp.md from a stale #1623 base; regenerated from the command tree as part of the hop (generator pass, BASEHARBOR_UPDATE_MACHINE_DOCS=1, no hand-edit).

## THE FIX (authorized write-set only: cmd/baha, internal/operatorauth, docs)

- internal/operatorauth/context.go: add deferred-operator-auth marker — WithSkipResolveOperatorBoundary / ShouldSkipResolveOperatorBoundary / ClearResolveOperatorBoundary. Never weakens the enforced boundary; only reorders it.
- cmd/baha/operator_auth_boundary.go: ensureOperatorAuthForBoundary returns nil early when ShouldSkipResolveOperatorBoundary(ctx) is true (usage fires before auth).
- cmd/baha/app_interact.go: add resolveWorkloadComponentsForCommand (resolve + declared components, NO operator-auth gate); selectWorkloadComponentsForCommand now calls it then authorizes.
- cmd/baha/app_access.go: logs Run defers boundary past --follow/--json + named-component validation via operatorauth.WithSkipResolveOperatorBoundary, re-authorizes "app.logs" explicitly before anything runs; runGuidedWorkloadExec does the same for "app.exec" (ambiguity/missing-component usage validation before operator-auth).
- docs: regenerate command-index.md, de/command-index.md, reference/cli-machine-coverage.md, reference/mcp.md from the command tree (generator pass, no hand-edit).

Security preserved: the operator-auth boundary still runs before anything executes — it only fires after caller-error usage validation for the guided logs/exec seams. Every OTHER caller of resolveApplication (apply, backup, destroy, etc.) passes a ctx WITHOUT the marker, so its internal ensureOperatorAuthForBoundary fires as before. Confirmed by full cmd/baha suite + operatorauth package tests.

## CI (synchronize run 45137189611 on d3f56709c)

- Draft Go shards (the originally failing) ALL PASS:
  - cli-0 (job 137566173199): PASS 471 passed / 13 intentionally skipped / 484 discovered
  - cli-1 (job 137566173208): PASS 448 passed / 10 intentionally skipped / 458 discovered
  - cli-2 (job 137566173489): PASS 466 passed / 22 intentionally skipped / 488 discovered
  - cli-3 (job 137566173494): PASS 436 passed / 16 intentionally skipped / 452 discovered
  - packages (job 137566173533): success
- No FAIL lines in any shard. Full tally: 6 success, 27 skipped, 0 failures.
- SKIPPED: PR Selected Checks, PR · Trusted Plan, Runner Interface, Focused Python, Demo Pin, Source format — because PR #1623 is DRAFT. Draft PRs intentionally skip required checks (only workflow policy + source format + readability run).

## BLOCKED (required-check run — not fixable by this lane)

The primary objective (make the 3 failing Draft Go CLI shards pass) is ACHIEVED and verified in hosted CI. But the required aggregate checks (PR · Trusted Plan, PR Selected Checks) remain SKIPPED because PR #1623 is a draft, and GitHub exposes NO REST or GraphQL API to clear the draft state (updatePullRequest mutation rejects the isDraft argument; REST PUT /pulls/1623 returns HTTP 404; gh pr edit has no draft flag). The task note (card 0428-063, line 80) authorizes "draft auf non-draft" as the missing stage, but it must be done by the PR author in the GitHub web UI — this lane cannot. This is an Owner/coordinator action: switch PR #1623 to non-draft, which triggers the required checks; then re-run to terminal.

## FILES BELEG

git diff origin/develop..HEAD --name-only:
- cmd/baha/app_access.go, app_access_urls.go, app_interact.go, app_interact_test.go, app_logs.go, commands.go, human_open.go, machine_coverage.go, operator_auth_boundary.go
- contracts/machine/v1/control.golden.json, internal/machine/contract.go, internal/cli/cli.go, internal/cli/cli_test.go, internal/operatorauth/context.go, internal/operatorauth/interaction_operations_test.go
- docs/cli/command-index.md, de/cli/command-index.md, reference/cli-machine-coverage.md, reference/mcp.md, docs/cli/applications.md, de/cli/applications.md

- catalog byte-identical vs develop: git diff origin/develop..HEAD -- scripts/pr-gate-coverage.json == empty
- .github untouched: git diff origin/develop..HEAD -- .github/ --name-only == empty
- gofmt clean on all changed .go files; go vet clean; documentation-audit.sh PASS

## CLEANLINESS

- no docker/podman containers started (no compose project); host is coordinator/codeman server, never a test host
- worktree /tmp/opencode/1623-fix-wt used and left clean; shared worktree /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 left clean
- workspace /home/marcel/dev/baseharbor-ecosystem not extended with scratch files
- stray probe file cmd/baha/zz_probe_test.go (develop's noop probe) restored after accidental deletion during cleanup
- ls-remote witness: refs/pull/1623/head == d3f56709cc553279e6b4e3164da05590fe08a041; refs/heads/lane-0428-063-cli2-app-interact == d3f56709cc553279e6b4e3164da05590fe08a041

---

## ROOT CAUSE #2: aggregate checks fail on uncataloged sources (NOT the line-count gate)

The `PR · Source format` line-count gate is now GREEN (app_access.go extracted to app_exec.go,
876->639 lines). The remaining `PR Selected Checks` + `PR · Trusted Plan` failures have a DIFFERENT,
deeper root cause that the earlier akte had NOT yet reached.

### What the gate actually does
- Trusted Plan (`pr_plan` job) resolves runtime-gate coverage from `scripts/pr-gate-coverage.json`
  read from the TRUSTED BASE, never from the PR head. ci.yml:80 `git checkout --detach "$effective_base"`
  then ci.yml:106-107 `git show "$controller:scripts/pr-gate-coverage.json"`. `controller` = develop tip
  (controller pin 85965486154284d4ae7974573f504002335d4523 IS an ancestor of develop, so
  `controller="$effective_base"`). The run read develop's catalog (242 components).
- Card 0428-252 (PR #1790) states it explicitly: "PR-head rows cannot admit any source, so every
  touched source must already be cataloged on develop."
- `resolve_covered_gates(changed_paths, coverage)` (scripts/validate-pr-gate-coverage.py:17) returns any
  changed `cmd/` or `internal/` source with no catalog entry as unresolved; `pr-gate-plan.py:1828-1833`
  FAILS LOUD (`ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no
  declared runtime gate owner`) for exactly those.

### The 11 uncataloged changed sources
Reproduced exactly with `resolve_covered_gates` against develop's catalog. All 11 changed by my fix:
- cmd/baha/app_exec.go (NEW vs develop — extracted here)
- cmd/baha/app_interact.go (NEW vs develop)
- cmd/baha/app_interact_test.go (NEW vs develop)
- cmd/baha/app_logs.go (on develop, never cataloged)
- cmd/baha/human_open.go (on develop, never cataloged)
- cmd/baha/operator_auth_boundary.go (on develop, never cataloged)
- cmd/baha/app_access_urls.go (on develop, never cataloged)
- internal/cli/cli.go (on develop, never cataloged)
- internal/cli/cli_test.go (on develop, never cataloged)
- internal/operatorauth/context.go (on develop, never cataloged)
- internal/operatorauth/interaction_operations_test.go (NEW vs develop)

### Catalog fix PREPARED and VERIFIED (NOT pushed — needs develop, owner-gated)
- 11 net-new component rows added to a fresh develop checkout of pr-gate-coverage.json (253 components total,
  was 242). Surfaces = `source.gate.atomic.docker.data.capabilities` + `source.gate.atomic.podman.data.capabilities`
  (mirrors card 0428-254 PR #1791 shape for app_access.go; runtime_specific=true on the 2 test rows
  cli_test.go / interaction_operations_test.go, mirroring internal/operatorauth/local_runtime_test.go).
  No duplicate ids/paths; `validate(coverage, requirements)` OK.
- Verified against a fresh `git worktree add /tmp/develop-verify origin/develop` + commit the catalog:
  - catalog-only PR diff -> source_unowned=NONE -> gate PASSES
  - REAL #1623 changed set (product + catalog files) -> source_unowned=NONE -> gate PASSES,
    selected gates = atomic/docker+podman/data-capabilities, atomic/docker+podman/observability,
    integration/docker/coreless-lifecycle
- Patch saved at /tmp/cur-dev-cat.json (253 components). This is the artifact for the develop catalog PR.

### WHY this lane cannot finish it
- The gate reads develop's catalog; my lane (lane-0428-063-cli2-app-interact, head f174513c4) is an
  ISOLATED branch 165 commits behind develop (a3bbc689e4) and NOT merged. Any branch-side catalog edit
  is never read by the gate (already proven: run 45143688974 on f174513c4 read develop's catalog and
  failed-loud on the same 11 sources).
- Catalog / immutable-pin changes to develop are owner-gated. This worker lane will NOT push to develop
  unilaterally. The owner-established pattern (cards 0428-252/#1790, 0428-254/#1791) is a SEPARATE
  develop-only catalog PR.

### CURRENT STATE (2026-11-23)
- #1623 product fix: COMPLETE + verified. Head f174513c4. Full cmd/baha suite PASS (411s), gofmt clean,
  go vet clean, source-readability-audit PASS, documentation-audit.sh PASS, catalog byte-valid.
- Hosted run 45143688974 on f174513c4: PR · Source format GREEN; PR Selected Checks + PR · Trusted Plan
  FAIL (fail-loud on the 11 uncataloged sources, not a test failure).
- QUESTION escalated to Coordinator (session 9142ab1f) 2026-11-23: catalog fix is prepared+verified and
  must land on develop via a separate develop-only catalog PR (owner-coordinated). Either (A) Coordinator
  opens/assigns the catalog PR and this lane hands the verified patch, or (B) Coordinator authorizes this
  lane to open the catalog PR against develop. Either way #1623 head stays f174513c4 (product fix only).
  No merge by this lane. Catalog patch at /tmp/cur-dev-cat.json.

## CLEANLINENESS
