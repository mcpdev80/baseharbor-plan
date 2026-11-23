# TASK EVIDENCE: t-20261123-wizard-org-default-usageerror (correction round)

- lane: w081-pr1802-wizard-org-default-usageerror-correction
- card: 0428-258 · app-new wizard: org-default (correction round, reviewer fecb post-merge)
- PR: #1804 https://github.com/mcpdev80/baseharbor/pull/1804 (fresh branch off develop; #1802 already merged)
- owner: w081
- real github remote confirmed: origin = https://github.com/mcpdev80/baseharbor.git

## PLAN

1. Read mission m_584_q.md.g: correction round. Bug: org-default missing-stack usageError prints LITERAL %q instead of expanded stack name at cmd/baha/app_new_wizard.go ~508. usageError() takes a plain string (no format expansion); precedent callers use fmt.Sprintf("...%q...", val).
2. Reproduce literal %q: extend cmd/baha/app_new_wizard_org_default_test.go with substring assertion (message must contain the quoted stack name and never contain literal %q). Confirmed FAIL against merged code: message was "organization default stack %q is not available...".
3. Smallest fix: expand format verb via fmt.Sprintf before passing to usageError (existing helper style, no UX/env change).
4. Fresh branch from current develop tip ff4cdf509 (old PR branch lane-0428-wizard-org-default-usageerror merged, no longer usable). Build, go vet, targeted named -run tests (skip RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication). bash scripts/ci-fast-check.sh.
5. One push, one pull_request-run to terminal (wizard-app-new-tests by name + PR Trusted Plan). No merge, no catalog/.github change (row exists develop-side via #1803). END with head + run-id + BASE_SHA + test witness.

## FIX

- File: cmd/baha/app_new_wizard.go, guidedStackProfile org-default branch (line ~508).
- Root cause: usageError() signature is `func usageError(message, hint string) error` — it stores the message verbatim. The message was passed as the literal format string "organization default stack %q is not available in the effective stack catalog" with no expansion, so the user saw the literal `%q`.
- Before: return guidedStackSelection{}, usageError("organization default stack %q is not available in the effective stack catalog", "...")
- After: return guidedStackSelection{}, usageError(fmt.Sprintf("organization default stack %q is not available in the effective stack catalog", name), "...")
- Matches precedent callers: cmd/baha/app_init_prompts.go:399 usageError(fmt.Sprintf("expected yes or no, got %q", line), ...), cmd/baha/app_prune.go:299 usageError(fmt.Sprintf("app prune accepts exactly one name, got %d", len(args)), ...).
- No UX/env/framework change. Minimal single-site diff.

## LOCAL VERIFICATION (head 854c7ceff, base ff4cdf509)

- Reproduction (before fix): go test -run TestGuidedStackProfileOrgDefaultMissingStackUsageError -> FAIL: message was "organization default stack %q is not available in the effective stack catalog" (literal %q).
- go build ./cmd/baha/ : exit 0
- go vet ./cmd/baha/ : exit 0
- go test ./cmd/baha/ -count=1 -run 'TestGuidedStackProfileOrgDefaultMissingStackUsageError|TestGuidedStackProfileOrgDefaultPresentStackResolves|TestOrgDefaultStackNotInCatalog' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication" : ok (0.049s)
- The new regression assertion now passes: usageError message contains the quoted stack name "\"ghost\"" and contains no literal %q.
- bash scripts/ci-fast-check.sh : OK (41 tests + 308 tests, workflow policy PASS 20 approved files, source readability PASS).

## CI (run #7507, head 854c7ceff) - RESULT SUCCESS

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/45180964447 (number 7507, terminal: completed / conclusion success)
- PR base sha (BASE_SHA) = ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb (gh api pull/1804 .base.sha; also origin/develop).
- No failed jobs (all non-success are skipped release-matrix gates).
- Key jobs (all success): PR · Trusted Plan, PR · Validation · wizard-app-new-tests (by name, as required), PR · Native gate plan, PR · Source format, PR · Go unit (cli-0, cli-1, cli-2, cli-3).

## BASE ATTESTATION

- git ls-remote origin refs/heads/develop (base): ff4cdf509dd00df81f90ecd0eb0bff17696ca9bb
- git merge-base --is-ancestor origin/develop HEAD -> YES (base ff4cdf509 is an ancestor of head 854c7ceff).
- git log --oneline origin/develop..HEAD (ONLY my commit):
  - 854c7ceff fix(0428-258): expand org-default usageError format verb (#0428-258 correction)
- git diff --name-only origin/develop HEAD (write-set-free, no catalog/.github):
  - cmd/baha/app_new_wizard.go
  - cmd/baha/app_new_wizard_org_default_test.go
- PR head ls-remote witness: 854c7cefff1e4483b2885026b91354944312522f refs/heads/w081-pr1802-wizard-org-default-usageerror-correction (refs/pull/1804/head = 854c7ceff).

## repo-rule compliance

- Smallest possible fix; reuses existing usageError helper and precedent fmt.Sprintf style. No consent/fail-closed/github change.
- New regression assertion wired into the same PR (wizard-app-new-tests CI job picks it up; durable evidence, not just local).
- Fresh branch cut from current develop tip ff4cdf509 (old branch was merged, not usable). One PR per card (#1804). No merge.
- No subagents; every step executed in this session.
- Tests via named -run with skip (test-runner-rule). No bare go test ./cmd/baha/ on the coordinator host.
- Runners GitHub-hosted shared runners only; no runner/build infrastructure touched. No docker/podman compose started.

## CLEANLINESS

- No docker/podman containers or compose projects started (Go unit work only, per test-runner-rule).
- docker ps -a (my pid run): $(docker ps -a 2>&1 || true)
- No stray files in /home/marcel/dev/baseharbor-ecosystem; temp PR files under /tmp.
- Worktree at workers/baseharbor (canonical remote origin = github.com/mcpdev80/baseharbor). Branch w081-pr1802-wizard-org-default-usageerror-correction at 854c7ceff.

## END

END_DONE w081-pr1802-wizard-org-default-usageerror-correction: #0428-258 correction round fixed. Literal %q in org-default usageError now expanded via fmt.Sprintf (matches precedent usageError callers). CI run #7507 on head 854c7ceff terminal success (BASE_SHA ff4cdf509): PR Trusted Plan + wizard-app-new-tests + Go unit all pass, zero failed jobs. Fresh branch off develop ff4cdf509; PR #1804 diff-vs-develop = fix + test only (no catalog/.github). Evidence on origin/main; END posted.
