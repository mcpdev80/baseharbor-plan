# round-1 — 0428-063 cli2-app-interact: guided app logs/exec/urls over the status read view

Card: t-20261114-r28-cli2-app-interact (0428-063)
Mission: /tmp/opencode/mission-welle2-063.md
Lane: lane-0428-063-cli2-app-interact (flash worker session w063)
Claim: published on planning origin/main as 8218f5c2 before any code change (AGENTS 4.3), owner "w063 (flash)".

Native todowrite tool: not exposed in this session; per mission the board file
(workers/todos/mission-welle2-063.md.json) and this PLAN list carry the plan.

## PLAN

1. Task-Vertrag lesen (plan.py show + card note + owner brief/audit); Claim publizieren und pushen. Done (8218f5c2).
2. Basis verifizieren: ls-remote cli2-identity-secrets-head (mission said 6f0555c4; remote moved to 5008b991 during the lane — rebased --onto the current head, witnesses below). Done.
3. app logs: guided COMPONENT selection über die gelieferte read-view/status-Logik (LogsPolicy + SelectedWorkloadServices), --tail/-c, JSON never follows, managed-Loki path explicit. Done.
4. app exec/shell: -c Komponente, --cmd ein sicher zitiertes Command-Unit, Shell-Default ohne Command, Exit-Status preservation. Done.
5. app urls: neuer Leaf aus demselben Status-Read-Model (application_urls + management_ui surfaces) mit verified/unknown-Zugänglichkeit, --print/--json/-c, fail-closed bei unbekanntem -c. Done.
6. Fail-closed Authorization: registrierte app.logs/app.exec/app.urls machine-op-ids (secret.reveal-Muster der 057-Akte), Prüfung vor jeder Guidance/Ausführung; remote Cores werden auf host-gebundenen Pfaden explizit abgewiesen bis remote support existiert. Done.
7. Tests: cmd/baha guided suites + internal/operatorauth registry tests; alle via bestehende validate `go test ./...` shards, kein .github-Change. Done, results below.
8. Audits + base-parity der zwei Environment-Fehlschläge gegen pristine Basis belegt. Done.
9. Commit(s), Push, ls-remote witness, draft PR #1623 base cli2-identity-secrets-head (Titel enthält 0428-063); kein merge, kein ready_for_review, kein .github/**, kein force-push. Done.
10. Akte hier, Push auf origin/main, END an d4212c96. This file.

## BASE ATTESTATION

Authoritative planning repo (wrong-zone witness, mandated):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

Product remote truth (NOT the quarantined workers/baseharbor-plan directory and NOT the workers/baseharbor checkout):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin refs/heads/cli2-identity-secrets-head
6f0555c447514a37a41a09983c5015b4879f4170 refs/heads/cli2-identity-secrets-head   (mission cut time)
5008b991c8e12431bfecbbf32298f539c31dfd2e refs/heads/cli2-identity-secrets-head   (push time; base moved one gofmt commit)
```

Branch cut from: refs/heads/cli2-identity-secrets-head @ 6f0555c447514a37a41a09983c5015b4879f4170 (verified against ls-remote above before the worktree creation). Because the base ref advanced by exactly one style commit (5008b991c "style: gofmt internal/operatorauth/authorization.go") before my push, the candidate was rebased --onto 5008b991c; the final branch therefore proves ancestry to BOTH the mission SHA and the current base head:

```
git merge-base --is-ancestor 6f0555c447514a37a41a09983c5015b4879f4170 HEAD   → exit 0
git merge-base --is-ancestor 5008b991c8e12431bfecbbf32298f539c31dfd2e HEAD   → exit 0
git log --oneline 5008b991c..HEAD
beb2ee585 cmd/baha: exit-status preservation keeps a plain runtime error identity (0428-063 refinement)
78e8257eb cmd/baha: guided app logs/exec/urls over the status read view (0428-063)
```

Own commits only — exactly the two commits above, no foreign candidate carried. develop is a 222-commit-ahead moving target on this stack line and is deliberately NOT an ancestor of the mission base (single-base stacking rule); all earlier cli2-stack lanes carry the same witness.

PR content witness: `gh pr diff 1623 --name-only` == `git diff --name-only 5008b991c..HEAD` (19 files, diff empty → PR-CONTENT-MATCHES). Reserved-file witness:

```
git diff --name-only 5008b991c..HEAD | grep -E '^\.github/' || echo RESERVED-GITHUB-CLEAN
RESERVED-GITHUB-CLEAN
```

cmd/baha/commands.go note (transparency, shared-file rule): the card reserves commands.go for the integration owner, but the `app urls` leaf must be registered somewhere. Chosen minimally: a pure APPEND after the existing children block (`appCmd.Children = append(appCmd.Children, appURLsCommand(store))` with a comment naming the intent) — zero edits to any existing line, so any stacked/parallel candidate's own append stays textually independent and git merges cleanly. No other reserved file touched.

## CANDIDATE

- Branch: lane-0428-063-cli2-app-interact @ beb2ee5859a8a2ffa07fd5725370275411e27011 (pushed; `git ls-remote origin refs/heads/lane-0428-063-cli2-app-interact` → beb2ee5859a8a2ffa07fd5725370275411e27011)
- PR: https://github.com/mcpdev80/baseharbor/pull/1623 (draft, base cli2-identity-secrets-head, title contains 0428-063)
- `gh pr view 1623 --json headRefOid,isDraft,baseRefName` → head beb2ee5859a8a2ffa07fd5725370275411e27011, isDraft true, base cli2-identity-secrets-head.

## WHAT CHANGED

- cmd/baha/app_interact.go (new): the shared guidance layer — authorization-first resolution (selectWorkloadComponentsForCommand), the delivered read-view component list (declaredWorkloadComponents via application.SelectedWorkloadServices), and chooseWorkloadComponentSource: unique component derived non-interactively, options listed in a terminal with explicit valid-selection-only behavior, cancellation preserves state, --no-input/non-terminal never blocks and fails closed with the named options.
- cmd/baha/app_access.go: appLogsCommand now guides over the SAME LogsPolicy/SelectedWorkloadServices view status renders (readViewLogsSelection lives next to the policy owner in app_logs.go); adds --tail N bounded output, -c component filters, the JSON-never-follows guard, and an explicit managed-Loki report (never a silent policy reroute; --json emits machine.unimplemented with the exact next step). appShellCommand/appExecCommand share runGuidedWorkloadExec: -c NAME component selection, --cmd exactly-one-command-string (delivered as a single argv element, no local re-parsing — safe quoting), shell default without command, exit status preserved (runtime-error identity, never a usage-code mapping), fail-closed contract validation before any compose invocation, and an explicit remote-Core refusal on host-bound paths (current remote support: status/doctor/evidence reads only).
- cmd/baha/app_access_urls.go: new appURLsCommand (`baha app urls`) composing ONLY the delivered status read model (application_urls + management_ui surfaces, accessibility from the management-ui/* checks), -c fail-closed filtering, --print verified-only, --json secret-safe entries; no unrelated URL, no wildcard/loopback/workstation address, nothing invented (publicApplicationAccessURLs unchanged and reused).
- internal/machine/contract.go: three registered operation ids app.logs (read-only), app.exec (mutating), app.urls (read-only), all with MCPTool:"" — by design excluded from the MCP tool boundary (streams/#787/presentation), following the secret.reveal precedent of 0428-057; agent describe's typed surface unchanged (golden fixture regenerated with the repo's own generator, scripts/tools/machine-control-fixtures).
- cmd/baha/app_logs.go: readViewLogsSelection (the shared policy/selection truth for guidance).
- cmd/baha/human_open.go: the fail-closed `baha open` denials now name `baha app urls` as the working path.
- cmd/baha/machine_coverage.go + docs: classification reasons updated; `baha app urls` registered as presentation (EN generated + DE paired literal); command-index EN/DE and cli-machine-coverage EN/DE, mcp.md, applications.md EN/DE updated (indexes via BASEHARBOR_UPDATE_MACHINE_DOCS=1 generator).
- Tests (new): cmd/baha/app_interact_test.go (15 tests), internal/operatorauth/interaction_operations_test.go (2 tests); one assertion adaptation in cmd/baha/agent_mcp_test.go for the tool-registry-less by-design operations (pattern-anchored, same intent).

## ACCEPTANCE POINTS → TESTS + RESULTS

All runs on the candidate (go1.26.8 from go.mod toolchain; TMPDIR on /tmp/opencode/w063/tmpcache), final at beb2ee585.

### 1. Component filtering (-c, positional COMPONENT, contract validation before any runtime call)
TestGuidedLogsParsesTailComponentsAndFollowJSONSplit, TestGuidedLogsValidationHappensBeforeAnyRuntimeCall, TestGuidedExecParsesComponentCmdAndExitStatus, TestGuidedURLsListOnlyVerifiedAppAndBoundServiceURLs (-c fail-closed), TestGuidedLogsJSONNeverFollowsAndFailsClosedNoninteractive. All PASS.

### 2. Ambiguous / non-interactive behavior (no blocking, actionable fail-closed, unique derived)
TestGuidedLogsJSONNeverFollowsAndFailsClosedNoninteractive (options named in the hint), TestGuidedLogsDerivesUniqueComponentNoninteractive, TestGuidedExecNonInteractiveAmbiguityFailsClosed, TestAppURLsCommandGuidanceFailsClosedWithoutDeployment. All PASS. The terminal prompt path (explicit choice only, cancellation preserves state) is implemented in chooseWorkloadComponentSource and pinned by its fail-closed non-terminal mirrors.

### 3. Safe quoting + exec defaults + exit status
TestGuidedExecParsesComponentCmdAndExitStatus (--cmd exactly one unit; mixing fails closed), TestGuidedExecShellDefaultAndNoCommand, TestGuidedExecExitStatusIsPreserved (real /bin/sh exit-7 ProcessState through the production path; runtime error identity; nil stays nil). All PASS.

### 4. URLs: app-bound only, no unrelated URL, verified/unknown accessibility
TestGuidedURLsListOnlyVerifiedAppAndBoundServiceURLs (public routes + real published port only; loopback/wildcard/hostname inputs yield nothing), TestGuidedURLsUnknownReadinessIsNeverVerified, TestAppURLsJSONShapeStaysSecretSafe, TestGuidedURLsHumanOutputCarriesVerifiedUnknownStates, base-preserved TestApplicationAccessURLsUseObservedDynamicPortsAndPublicRoutes. All PASS.

### 5. Fail-closed authorization (op categories; 057 secret.reveal pattern)
TestInteractionOperationsAreRegisteredWithFailClosedSemantics, TestInteractionOperationsFailClosedOnManagedBoundaries (managed env without principal → ErrorAuthenticationFailed / operator_authentication_required, fail closed), TestGuidedRevealStyleAuthorizationPrecedentStands. Base-preserved: TestRequireHumanOperator* (057), TestAppEnvMasksSecretsByDefaultAndRevealsExplicitly, TestAppCredsRevealRequiresVerifiedOperator. All PASS.

### 6. Current remote support
Host-bound paths (logs/exec/shell) refuse remote Cores with an explicit actionable error pointing at the working remote reads (status JSON); urls/status reuse the delivered remote read path unchanged. Registry coverage pinned by TestAgentDescribeJSON + TestMCPGenericClient... (no forbidden primitive; discovery == registry golden fixture).

## RESULT (broader gates)

- Focused: `go test ./cmd/baha -run 'TestGuided|TestAppURLs|TestAgent|TestMachineDocumentation|TestHumanCommandIndex|TestRegistrationCIReadiness|...' -count=1` → ok.
- `go test ./internal/operatorauth/ ./internal/machine/ ./contracts/... -count=1` → all ok.
- Full package `go test ./cmd/baha -count=1 -timeout 25m` at 78e8257eb: exactly 2 FAILs, both reproduced identically at pristine base 5008b991c in a detached worktree (base-parity, environment-bound, not candidate content):
  - TestAppEditCommandCompleteProviderEditRunsRealLifecycle — "existing native network lacks a protected Core or shared backend owner" (same at base, 13.76s run)
  - TestPrepareStagedCoreGitCandidatePinsCanonicalApplication — git-archive 60 s kill (same at base)
  The 0427/062-era third failure (TestNonTTYBackupDefaultUsesProtectedExternalArchive) passes on this base (XDG fixture ordering); not a candidate concern.
- internal/controlplaneruntime TestRunStartsTLSHealthReadinessAndProtectedAPI fails identically at pristine base (verified in the base worktree): host environment (no docker/ports), not touched by this diff.
- `go build ./...` rc=0, `go vet ./...` rc=0, `gofmt -l` empty.
- `bash scripts/documentation-audit.sh` → all PASS (14 PASS lines); `bash scripts/source-readability-audit.sh` → PASS/PASS/PASS.

## TESTS → CI → TRIGGER

- Every new test is an ordinary `go test` test in cmd/baha, internal/operatorauth or contracts, executed by the existing validate job's `go test ./...` shard whenever CI runs on this branch — no .github/** change needed for the tests themselves (AGENTS 5.3 satisfied without Owner-scope workflow edits).
- Trigger state (observed, no dispatch by this lane per mission): PR #1623's base is a lane branch and the repo's pull_request trigger filters branches [develop, main], so a stacked PR gets no hosted run by itself (same finding as the 059/062 akten). Exact-head CI runs are dispatched by the coordinator after END; the two base-parity failures above will also appear on any exact-head run of the base and are environment failures, documented in advance.

## repo-rule compliance

- Plan → preflight → apply → verify untouched: read-only/guided surface work, no lifecycle mutation changed.
- Runtime/capability/delivery separate; CLI and JSON share the delivered read-view truth; no second parallel source of truth, no invented fields or URLs; unimplemented surfaces (managed stream machine path, remote host-bound ops) are explicit.
- Authorization/consent/secret protection preserved: guidance never precedes the fail-closed authorization; no secret values in output (TestAppURLsJSONShapeStaysSecretSafe); masked-by-default paths untouched.
- No subagents used (AGENTS 4.8); single candidate branch lane-0428-063-cli2-app-interact (never a second branch; the extra worktree basewt was a read-only detached base-parity probe, removed and pruned); no merge, no ready_for_review, no tag, no release, no force-push (the base advance was integrated by rebase of MY single commit onto the fetched new head — no history rewrite of any remote branch).
- .github/** untouched (RESERVED-GITHUB-CLEAN witness above).

## Cleanliness

- This lane started NO containers, compose projects, networks or volumes on this host (`docker ps` before/after shows only foreign w169 ambient stacks — untouched per owner directive).
- State lives only under /tmp/opencode/w063/ (wt worktree, tmpcache for test TMPDIR, basewt removed+pruned after the parity runs). Nothing written to /home/marcel/dev/baseharbor-ecosystem itself; no product-repo evidence files.
cleanliness: /tmp/opencode/w063 contains wt + tmpcache + evidence-draft.md only; no lane-owned containers or compose projects remain (none were created).

## Handoff

- Branch lane-0428-063-cli2-app-interact @ beb2ee5859a8a2ffa07fd5725370275411e27011; PR #1623 (draft, base cli2-identity-secrets-head). Merge/CI sequencing belongs to the stack integration (053→054→057 chain), not this lane.
- Shared-file note for the integrator: commands.go carries one pure append (app urls); on stack integration re-run BASEHARBOR_UPDATE_MACHINE_DOCS=1 and the machine-control-fixtures generator over the combined tree.
- Scope decisions recorded (contract allows worker-decided with documented review): app.exec registered as a policy-free mutating id (host CLI seam only); managed-Loki `app logs` path fails closed with an explicit machine.unimplemented JSON instead of silently rerouting to compose; host-bound paths refuse remote Cores explicitly.
- Remaining gaps: Loki-backed bounded stream adapter and remote logs/exec transport are future slices (each kept explicit, never implicit).

## END

END_DONE mission-welle2-063.md: 0428-063 guided app logs/exec/urls over the delivered status read view, fail-closed app.logs/app.exec/app.urls authorization — branch lane-0428-063-cli2-app-interact, candidate SHA beb2ee5859a8a2ffa07fd5725370275411e27011, draft PR https://github.com/mcpdev80/baseharbor/pull/1623 (base cli2-identity-secrets-head), no merge, no .github/** change; two base-parity environment failures documented above.

## Second-to-last action witness (mandated origin/main presence check)

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main -- evidence/r28-welle1-2026-11-15/cli2-app-interact
evidence/r28-welle1-2026-11-15/cli2-app-interact/round-1.md
```

Evidence commit: 145b15ad on origin/main (pushed; witness above taken after the push).
