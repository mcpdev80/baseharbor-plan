# TASK EVIDENCE: t-20261123-wizard-org-default-usageerror (#0428-258)

- lane: w081-pr1802-wizard-org-default-usageerror
- card: 0428-258 · app-new wizard: org-default (H-P1 finding F6)
- PR: #1802 https://github.com/mcpdev80/baseharbor/pull/1802
- base branch: develop
- owner: w081
- real github remote confirmed: origin = https://github.com/mcpdev80/baseharbor.git

## PLAN

1. Read mission m_584_fix.md.g; understand corrected hypothesis: line-level coverage gap for cmd/baha/app_new_wizard_org_default_test.go.
2. Show git diff origin/develop for scripts/pr-gate-coverage.json; compare path match to precedence pattern (id source.cmd_baha_app_new_wizard_<name>_test_go, guided surfaces like #1800).
3. Register the new test source in scripts/pr-gate-coverage.json (append-only vs develop byte-exact, no sorting/regeneration, no .github/**, no consent change).
4. Rebase branch onto current develop so diff-vs-develop is clean; confirm catalog delta is write-set-free vs develop.
5. Build, targeted tests (named -run, skip RunsRealLifecycle), go vet; run gate planner vs base.
6. One PR run to terminal (Trusted Plan + wizard-app-new-tests). END with head + run-id + BASE_SHA + line excerpt.

## FIX (correct, passes locally and in CI)

- File: cmd/baha/app_new_wizard.go, function guidedStackProfile (org-default branch, org-default name present but absent from the effective stack catalog).
- Before: return guidedStackSelection{}, fmt.Errorf("organization default stack %q is not available in the effective stack catalog", name)
- After: return guidedStackSelection{}, usageError("organization default stack %q is not available in the effective stack catalog", "Remove the organization stack default or add the stack to the effective catalog, then re-run app new.")
- Reuse existing usageError helper (cmd/baha/commands.go:261). No consent/fail-closed/github behavior change. No UX/environment change, no new framework.
- Extracted shared guard orgDefaultStackNotInCatalog(name, catalog) so fix + tests share one path.
- Indirect organizationDefaultStack via package var organizationDefaultStackName for test determinism (no on-disk org config needed).
- New tests: cmd/baha/app_new_wizard_org_default_test.go
  - TestGuidedStackProfileOrgDefaultMissingStackUsageError: missing stack yields *cli.UsageError (before fix the same test caught *errors.errorString).
  - TestGuidedStackProfileOrgDefaultPresentStackResolves: present stack resolves to nil error.
  - TestOrgDefaultStackNotInCatalog: pure guard coverage (empty/present not missing; absent missing).

## LOCAL VERIFICATION (head 027fb255a)

- go build ./cmd/baha/ : exit 0
- go vet ./cmd/baha/ : exit 0
- go test ./cmd/baha/ -count=1 -run 'TestGuidedStackProfileOrgDefaultMissingStackUsageError|TestGuidedStackProfileOrgDefaultPresentStackResolves|TestOrgDefaultStackNotInCatalog' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication" : ok (0.027s)
- Gate planner vs base afa064519 (GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop): exit 0, selected_gates = ['atomic/docker/data-capabilities', 'atomic/docker/guided']
- Validator: python3 scripts/validate-pr-gate-coverage.py -> "PR gate coverage catalog is valid"
- diff-vs-develop (origin/develop .. 027fb255a) = only cmd/baha/app_new_wizard.go + cmd/baha/app_new_wizard_org_default_test.go. scripts/pr-gate-coverage.json is a no-op (row now owned by #1803).

## CI (run #7503, head 027fb255a) - RESULT SUCCESS

- Run: https://github.com/mcpdev80/baseharbor/actions/runs/45173006468 (number 7503, terminal: completed / conclusion success)
- PR base sha (BASE_SHA) = afa064519a859fbfa6e171c749a911301b9522b7 (confirmed via gh api pull/1802 .base.sha). This is the catalog the Trusted Plan read; #1803 registered my test row on develop.
- No failed jobs. Key jobs (all success): PR · Trusted Plan, PR · Native gate plan, PR · Source format, PR · Runner Interface, PR · Exact Candidate, PR · Go unit (cli-0..3), PR · Validation · cli-gofmt / cli-vet / cli-build, PR · Validation · wizard-app-new-tests, PR · Validation · source-contracts, PR · Focused Python. Remaining jobs skipped (release-matrix gates not applicable to this focused fix).
- The line-level coverage gap that caused the earlier uncataloged-source failure is resolved: the path cmd/baha/app_new_wizard_org_default_test.go now matches a catalog row on the base.

## BASE ATTESTATION

- git ls-remote origin refs/heads/develop (base for this run): afa064519 (pull base.sha witness above).
- git merge-base --is-ancestor afa064519a859fbfa6e171c749a911301b9522b7 HEAD -> YES (base is an ancestor of head).
- git log --oneline origin/develop..HEAD:
  - 027fb255a fix: rebase 0428-258 wizard fix on trusted coverage
  - 272115423 fix(0428-258): org-default missing-stack returns usageError parity (#0428-258)
  - d361c5337 ci(0428-258): catalog cmd/baha/app_new_wizard_org_default_test.go in pr-gate-coverage (#1802 develop-only)
- PR head ls-remote: 027fb255a4396215760771729d265ebbc6f9020f refs/pull/1802/head.

## CATALOG LINE EXCERPT (base afa064519, my test source)

{"id": "source.cmd_baha_app_new_wizard_org_default_test_go", "path": "cmd/baha/app_new_wizard_org_default_test.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}

## repo-rule compliance

- Fix reuses existing usageError helper; single-area, minimal diff. No consent/fail-closed/github change.
- Catalog registration append-only vs develop byte-exact; no sorting/regeneration; no .github/** edit. The row was landed on develop by the Owner via #1803 (separate ingress PR, Owner scope), so this PR's diff-vs-develop is write-set-free for the catalog.
- No subagents. Every step executed in this session. One PR per card.
- Tests run via named -run with skip (test-runner-rule). No bare go test ./cmd/baha/ on the coordinator host.
- Runners GitHub-hosted shared runners only; no runner/build infrastructure touched. No docker/podman compose started.

## CLEANLINESS

- No docker/podman containers or compose projects started (Go unit work only, per test-runner-rule).
- docker ps -a (my pid run): $(docker ps -a 2>&1 || true)
- No stray files in /home/marcel/dev/baseharbor-ecosystem; helper artifacts under /tmp/opencode.
- Worktree at workers/baseharbor (canonical remote origin = github.com/mcpdev80/baseharbor). Working tree clean after checkout of canonical head 027fb255a.

## END

END_DONE w081-pr1802-wizard-org-default-usageerror: #0428-258 fix + tests correct and green. CI run #7503 on head 027fb255a terminal success (BASE_SHA afa064519); Trusted Plan + wizard-app-new-tests pass, no failed jobs. Catalog line owned by Owner #1803 on develop; this PR diff-vs-develop is only the fix + test (write-set-free).