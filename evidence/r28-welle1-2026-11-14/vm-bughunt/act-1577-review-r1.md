# PR #1577 Review R1

Review role: CODEX-REVIEW
Review date: 2026-11-14
Card: t-20261114-r28-perses-release-boundary (0428-092)
PR: https://github.com/mcpdev80/baseharbor/pull/1577 (OPEN, DRAFT)
Reviewed candidate: e955f43507de193cb21dee51ce4021248f3bd08f
Fetched base: 0e9ccb582f5bdcdc74049bbe3996263cdce6500c (develop)

## PLAN

1. Fetch and verify PR #1577 head and develop base; record provenance. (done)
2. Review the exact diff, release contract, component table, versioning, provisioning claims, and overlap with PR #1575. (done)
3. Write a SHA-specific verdict and actionable recipe in planning evidence. (done)
4. Validate and publish evidence to planning origin/main, post END, then hold for PR #1575 r2. (done)

## Candidate and repository witnesses

Exact remote output from the BaseHarbor repository:

`git ls-remote origin refs/heads/develop refs/pull/1577/head`
`0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop`
`e955f43507de193cb21dee51ce4021248f3bd08f	refs/pull/1577/head`

Fetched refs resolved to the same full SHAs. `git merge-base --is-ancestor refs/review/develop refs/review/pr1577` exited 0. The exact base-to-head commit list contains one candidate commit:

`git log --oneline refs/review/develop..refs/review/pr1577`
`e955f4350 docs(v0.4.28): set optional Perses release boundary (pin v0.55.1)`

PR #1577 is open and draft, base `develop`, head branch `0428-092-perses-boundary`. The diff contains nine documentation/changelog files; no product code or `.github/**` file changed. `git diff --check` is clean.

Planning repository identity was verified before the first evidence commit. Exact command and output:

`git rev-parse --show-toplevel`
`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`

Pre-push `git ls-remote origin main` output:

`26a6d034314298cf6661affa6d89e1d7f1dec53f	refs/heads/main`

## Findings and verdict

REJECT for candidate `e955f43507de193cb21dee51ce4021248f3bd08f`. The v0.55.1 pin itself is consistent across the changed English/German release documentation and changelog. Upstream's official Perses release page lists v0.55.1 as the latest release dated 2026-11-02: https://github.com/perses/perses/releases. The docs distinguish Perses v0.55.1 from BaseHarbor v0.4.28 and do not claim an instance is currently provisioned. Optional absence is described as a normal, non-error state.

Blocking findings:

- The task is to align active release and audit entry points, but `docs/development/pre-release-readiness.md` still defines the active scope specifically as v0.4.27 (Core and Demo; archived Console/Node Connector excluded only from that release). `docs/internal/pre-release-documentation-audit.md` likewise says the archived repositories are excluded from v0.4.27 and does not state the v0.4.28 component scope or Perses's optional/not-configured status. The PR changes release notes and indexes but leaves these live readiness/audit entry points stale for the current release.
- The new docs say BaseHarbor reports the observability management surface as unsupported when Perses is not provisioned. The independently reviewed, still-current PR #1575 head is `61f76fa18897d4a0709c09c27ae67e1ded8dba20`; its `internal/capability/perses.go` `PersesManagementSurfaceNow` marks `Provisioned=true` solely because the compile-time default version/image validates, without runtime provisioning evidence. The default authentication class remains unsupported, but the internal provisioned state conflicts with the release text's promise about runtime state. Keep the user-facing statement conditional on Perses being selected but absent, and hold a current-behavior claim until PR #1575 r2 makes the seam fail closed on actual provisioning state.
- The German additions need correction before publication: `docs/de/releases/v0.4.28.md` contains the truncated `Verschlüsselungsschl` and misspelled `Visualisierungsoberfolge`; `docs/de/reference/releases.md` contains `Normalzust` where `Normalzustand` is intended.

PR #1575 overlap witness at review time:

`git ls-remote origin refs/pull/1575/head refs/heads/develop`
`0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop`
`61f76fa18897d4a0709c09c27ae67e1ded8dba20	refs/pull/1575/head`

## Correction recipe and stop criteria

1. Update `docs/development/pre-release-readiness.md` and `docs/internal/pre-release-documentation-audit.md` so v0.4.28's active scope names Core, Demo, delivered CLI, and optional Perses; explicitly exclude archived public Console and Node Connector without weakening genuine release, test, provenance, or runtime gates. State that an unselected Perses surface is `not configured` with no error/readiness failure. Do not say Perses is implemented or provisioned.
2. In `docs/releases/v0.4.28.md`, `docs/reference/releases.md`, and matching German pages, describe `unsupported` only for the selected Perses surface when it is absent. Keep the ordinary unselected state non-error. Reconcile the wording with the final PR #1575 r2 behavior before making an actual-behavior claim.
3. Correct the German release text: `Verschlüsselungsschlüssel`, `Visualisierungsoberfläche`, and `Normalzustand`. Keep the v0.55.1 product pin distinct from BaseHarbor's own release/provider version.
4. Stop review acceptance until the readiness/audit entry points are current, the EN/DE statements agree, and the final PR #1575 candidate no longer marks Perses provisioned from a pin alone. Stop if PR #1575's final candidate changes after its review; refresh and review that exact SHA.

## Planning validation

`python3 scripts/plan.py check`: 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors, 10 existing warnings. `git diff --check` produced no output.

## CI and scope

GitHub Actions run `43640753778` on the reviewed draft PR candidate. `PR · Draft source and routing` and all five `PR · Draft Go` jobs (`cli-0` through `cli-3`, `packages`) succeeded. `PR Selected Checks`, source-format, release, and native runtime jobs were skipped under draft selection. No checks were rerun or dispatched, and no workflows were changed.

## repo-rule compliance

- Read-only review of the product candidate; no product files, PR state, or CI state were changed.
- Evidence is in the actual planning repository, `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, not the workers bookkeeping checkout.
- No subagents used and no secrets included.
- Verdict is bound to the fetched candidate/base above.

END act-1577-review-r1 DONE — REJECT; candidate e955f43507de193cb21dee51ce4021248f3bd08f.
