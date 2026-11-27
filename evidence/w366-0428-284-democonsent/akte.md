# w366-0428-284-democonsent — capture-boundary fix (baseharbor-demo)

- Lane: w366-0428-284-democonsent (session e6ca7696-b1f8-492d-b226-876b16925fc5)
- Card: 0428-284 (t-20261125-0428-284-1812-postretry-gate-failure) — repo baseharbor-demo
- Candidate head: 83c80c917858e719118bd21e0183b4516959ac53 (branch w366-0428-284-democonsent)
- PR: #183 https://github.com/mcpdev80/baseharbor-demo/pull/183 (base develop, ready for review)
- Commit identity: an=w366-0428-284-democonsent cn=w366-0428-284-democonsent (both verified)
- Status: Handled to review with a CI-gate blocker to report (see CI blocker below)

## Approved scope (w267 disposition)

- Owner adjudication akte: baseharbor-plan evidence/2026-11-27/0428-284/pr1866-capture-disposition.md (origin/main b5b88bb04).
- Minimal capture-path correction in baseharbor-demo/tests/guided/drive.py ONLY.
- Preserve fail-closed consent: explicit second `up --confirm-candidate <exact captured digest>` only when documented prompt + digest present in captured first transcript AND no foreign error signature. Missing/partial/ambiguous = Abort. No auto-yes, no consent bypass.
- Not authorized: Core/product code, consent/auth semantics, .github/**, pin changes, parser/retry redesign.

## What was done

- Claim published: plan.py claim 0428-284 (owner w366-0428-284-democonsent, status active), commit 5149cda9f on origin/main.
- Branch cut from demo develop tip 58ac70679efe5f7e95bd47d602841704fb9ffa67 (attested via git ls-remote; merge-base --is-ancestor OK). Rebasing onto the current develop tip after commit.
- Fix (write-set: tests/guided/drive.py):
  - Extracted reconcile_capture_from_log(log_path, capture_buffer, capture_tail) — appends on-disk log bytes the final-drain loop never read back into capture_buffer (the log is authoritative). Returns (updated_buffer, updated_tail) tuple so run_tty can rebind its immutable-string locals.
  - In run_tty capture path (after the final-drain loop), reconciles the on-disk log against capture_buffer. This is a capture-bucket reconciliation; it does NOT assert a specific PTY mechanism (per akte).
  - Fail-closed path (run_guided_consent_flow) unchanged: refuse 588-606, retry 621-648 — untouched.
- Tests (write-set: tests/guided/test_consent_capture.py, +135 lines, no markdown checkboxes):
  - test_21: documented digest + retry hint captured -> second_up (production flow through run_guided_consent_flow).
  - test_22: foreign error still aborts (no retry) after the boundary fix.
  - test_23: absent digest aborts (no retry).
  - test_24: white-box guard on reconcile_capture_from_log — appends unread log bytes; fails on the un-reconciled boundary (verifies the fix is present, fails otherwise).
- Local validation (non-qualifying prechecks only, per CI policy): syntax OK, py_compile OK, git diff --check clean. Full suite 25/25 pass on final HEAD. test_24 confirmed FAIL on un-fixed code (AttributeError: no reconcile_capture_from_log) and PASS on fixed code — genuine regression guard.
- Did NOT run any local test module for CI qualification (CI policy). Prechecks only.

## Evidence

- Demo remote (verified first git action): origin https://github.com/mcpdev80/baseharbor-demo.git
- Branch push (git ls-remote): 83c80c917858e719118bd21e0183b4516959ac53 refs/heads/w366-0428-284-democonsent
- PR #183 headRefOid 83c80c917858e719118bd21e0183b4516959ac53, base develop, isDraft false, state open.
- Base attestation: git ls-remote origin refs/heads/develop -> 58ac70679efe5f7e95bd47d602841704fb9ffa67; git merge-base --is-ancestor 58ac706...HEAD -> YES. git diff origin/develop...HEAD --name-only -> tests/guided/drive.py, tests/guided/test_consent_capture.py.
- Identity gate: git show -s --format='%an' HEAD -> w366-0428-284-democonsent; git show -s --format='%cn' HEAD -> w366-0428-284-democonsent.
- CI run on head: gh run 45923683323 (workflow pr-config-matrix.yml, event push, conclusion failure, 0 jobs, "workflow file issue").

## CI BLOCKER (report file:line — Owner scope, NOT fixed here)

The only demo workflow that covers the changed path tests/guided/** is pr-config-matrix.yml. It fires on pull_request to develop with a paths filter that includes tests/guided/** — but it has NEVER successfully scheduled a job:

- File: .github/workflows/pr-config-matrix.yml (repo baseharbor-demo). Header line 1: "# DRAFT ONLY — owner-scope workflow addition; not committed or run."
- The workflow ran exactly once (run 45923683323, event push) and failed with "This run likely failed because of a workflow file issue"; gh api .../runs/45923683323/jobs -> {"jobs":[]}; total 0 jobs.
- No pull_request run exists on head 83c80c9 (the pull_request CI did not fire the config-matrix workflow on PR #183; check-runs API returns 404).
- Net: my test in tests/guided/ is NOT picked up by any executed GitHub CI job. This is the CI-Aufnahmepflicht gap. The fix to the workflow trigger/coverage is a .github/** change = Owner scope; per mission + CI policy it is reported here as a finding with file:line, NOT edited by this lane.

Suggested Owner fix (finding, not implemented): make pr-config-matrix.yml a live workflow (remove the DRAFT-only status) and confirm its pull_request branches:[develop] + paths:[tests/guided/**] filter actually schedules jobs on a develop-targeted PR; if the "workflow file issue" is a YAML/syntax/trigger defect, repair it. Once the workflow runs on develop PRs, tests/guided/** (including test_21-24) execute under the existing group — no new lane/test registration needed.

## Cleanliness

- Demo repo git status clean (only tests/__pycache__ and .tools/ untracked, build artifacts).
- No container / compose project started on this or any host.
- Plan repo: akte published under baseharbor-plan evidence/w366-0428-284-democonsent/ (pushed to origin/main via isolated worktree; worktree removed).

## END line

END_BLOCKED w366-0428-284-democonsent: minimal drive.py capture-boundary fix + focused regression tests (test_21-24, 25/25 local pass, test_24 is a genuine guard) implemented, committed (83c80c9, canonical identity), pushed, PR #183 against develop. Fail-closed consent semantics unchanged. CI-gate blocker: the only demo workflow covering tests/guided/** (pr-config-matrix.yml, Owner-scope .github/**) schedules 0 jobs on a develop PR — reported as finding file:line, not edited (outside write-set). PR left ready-for-review with Hosted CI gate pending. No product code, no consent/auth change, no .github change, no runner/infra work.
