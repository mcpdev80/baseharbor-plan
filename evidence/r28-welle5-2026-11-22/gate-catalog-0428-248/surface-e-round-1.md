# 0428-248: catalog fill surfaces (surface-e)

- karte 0428-248, sitz f0f6c8b4. DEP-FREIE KATALOG-LANE. develop 484c95fca. Pattern = #1784 (CI SUCCESS).
- #1761 (static-auth-helper: ReadGrantingMembershipProvider, WithVerifiedTestOperator, WithVerifiedTestOperatorPrincipalForced) adds 4 NEW uncataloged sources -> PR Trusted Plan fail-loud guardian aborts.
- The 4 (on develop 484c95fca): cmd/baha/app_env_test.go, cmd/baha/app_export_command_test.go, cmd/baha/target_definition_change_test.go, internal/operatorauth/test_operator.go.
- ONLY source->surface mapping rows in JSON. NO product code, NO .github, NO footprint/237.

## PLAN

1. Establish reality (remote guard, develop 484c95fca via ls-remote). Cut lane-0428-248-catalog-surface-e from EXACTLY origin/develop 484c95fca (no force later). Record 484c95fca.
2. grep confirm the 4 paths are NOT in scripts/pr-gate-coverage.json (else STOP+report). Examine existing surface keys to learn the mapping pattern.
3. Map each of the 4 to an existing matching surface. All 4 -> source.gate.atomic.{docker,podman}.data.capabilities (same as sibling test_operator_context_test.go — operator-context helpers exercised through data-capabilities gate). New surface-key only if none matches (following source->native/static pattern). Only scripts/pr-gate-coverage.json. NO product code, NO .github, NO footprint/237. STOP if a source maps to an existing surface but still fails (planner-bug).
4. Regression: planner-unit / census-report shows the 4 paths mapped (no uncataloged-abort). ci-fast-check.sh fast gates before push.
5. Hosted PR push -> draft->ready -> PR. ls-remote pull/<n>/head witness. PR body lists 4 paths + surfaces + unblocks #1761. akte. Publish to baseharbor-plan origin/main. END + post.

## BASE ATTESTATION

- develop HEAD (git ls-remote origin develop, fresh): 484c95fca938cb96736c4578906e6ea58bf043b8
- NOTE: the shared checkout's local origin/develop ref was STALE at b27b2ebe. Fetched fresh (git fetch origin develop) and cut the branch from 484c95fca. Verified 484c95fca IS an ancestor of my HEAD (git merge-base --is-ancestor 484c95fca HEAD = YES).
- branch head: f3f0188bad2caaf10e90fc8f2f1552383f30bd5d
- git log --oneline 484c95fca..HEAD = only my commit f3f0188ba; git diff 484c95fca...HEAD --name-only = scripts/pr-gate-coverage.json only.

## Reality (deviation from dispatched census)

The dispatched surface-e census paths were partially stale:
- core_targets.go, core_targets_test.go, app_secrets.go — NEVER existed on develop 484c95fca (no git history). These were the surface-d/#1784 stale paths.
- On develop 484c95fca only the 4 #1761 sources are genuinely uncataloged (verified programmatically against resolve_covered_gates):
  - cmd/baha/app_env_test.go: catalogued=False, unresolved=YES
  - cmd/baha/app_export_command_test.go: catalogued=False, unresolved=YES
  - cmd/baha/target_definition_change_test.go: catalogued=False, unresolved=YES
  - internal/operatorauth/test_operator.go: catalogued=False, unresolved=YES
  - cmd/baha/installation_destroy_native_test.go: already catalogued (NOT one of the 4)
  - cmd/baha/test_operator_context_test.go: already catalogued (NOT one of the 4)

## Surface decision (authoritative, not guessed)

The catalog's surface system only supports data.capabilities / lifecycle / guided / observability / coreless-lifecycle — NOT per-file static surfaces (no app/env static, app/export, target-definition-change, or operatorauth static-auth surface exists). The authoritative mapping: all 4 files map to source.gate.atomic.{docker,podman}.data.capabilities — the same surface as the sibling cmd/baha/test_operator_context_test.go fixture. These four are operator-context static-auth helpers; the operator-context they provide is exercised through the data-capabilities gate.
- verify: resolve_covered_gates for each -> ['atomic/docker/data-capabilities', 'atomic/podman/data-capabilities'] (unresolved: []). NOT the STOP condition (planner-bug): mapping to an existing surface resolves cleanly.
- No new surface-key invented; no new native_checks row (data.capabilities native gate native/docker|podman/data-capabilities already exists and covers source.gate.atomic.{docker,podman}.data.capabilities).

## Change (catalog JSON only)

Added 4 components, each runtime_specific: true, surfaces [source.gate.atomic.docker.data.capabilities, source.gate.atomic.podman.data.capabilities]:
- cmd.baha.app.env.test.go -> cmd/baha/app_env_test.go
- cmd.baha.app.export.command.test.go -> cmd/baha/app_export_command_test.go
- cmd.baha.target.definition.change.test.go -> cmd/baha/target_definition_change_test.go
- internal.operatorauth.test.operator.go -> internal/operatorauth/test_operator.go
Surgical one-file edit, inserted after the sibling test_operator_context_test.go component.

## Regression

- python3 scripts/validate-pr-gate-coverage.py -> "PR gate coverage catalog is valid"
- resolve_covered_gates for all 4 -> (['atomic/docker/data-capabilities','atomic/podman/data-capabilities'], []) (unresolved: [])
- fail-loud guard intact: resolve_covered_gates(['cmd/baha/zz_new_uncataloged.go']) -> ([], ['cmd/baha/zz_new_uncataloged.go'])
- unittest: test_pr_gate_coverage 41 OK; test_ci_v0427_gate_catalog 7 OK; test_pr_native_gate_plan 13 OK; test_pr_ci_fallback/test_pr_diff_base/test_targeted_gate_ref/etc 82 OK
- ci-fast-check.sh fast gates (read-only/policy subset) OK; no Go files changed (JSON only)
- Hosted CI run 45057444858 @ f3f0188ba: conclusion success. Selected green: PR · Trusted Plan, PR · Focused Python, PR · Validation · pr-planner-tests, ci-executor-tests, ci-policy, Native gate plan, PR Selected Checks success. Runtime/native gates correctly skipped (catalog-only PR, no product change).

## Hosted PR

- PR #1785 https://github.com/mcpdev80/baseharbor/pull/1785 (base develop, head lane-0428-248-catalog-surface-e @ f3f0188ba)
- ls-remote refs/pull/1785/head = f3f0188bad2caaf10e90fc8f2f1552383f30bd5d (matches branch head)
- CI run 45057444858 @ f3f0188ba: completed/success.
- Class: review = handed off; exact-head CI (run 45057444858) green; Codex review pending.

## repo-rule compliance

- dep-free catalog lane: only scripts/pr-gate-coverage.json changed; no product code, no .github/**, no footprint/237, no stage-boundary/ci-operator.
- one integration candidate, one PR per card; branch from develop 484c95fca (base attestation shown with ancestor proof); only my commit in 484c95fca..HEAD.
- no subagents; no merge/comment; no product write; no .github touch.

## END

END_DONE w27-pr1627-0428-061-pull: 0428-248 catalog fill surface-e DONE. Reality deviation: dispatched census paths core_targets.go/core_targets_test.go/app_secrets.go NEVER existed on develop 484c95fca; only the 4 #1761 sources (app_env_test.go, app_export_command_test.go, target_definition_change_test.go, internal/operatorauth/test_operator.go) genuinely uncataloged. Mapped all 4 to source.gate.atomic.{docker,podman}.data.capabilities (same surface as sibling test_operator_context_test.go) — NOT the STOP condition; resolves cleanly to atomic/{docker,podman}/data-capabilities. validate() OK, fail-loud guard intact, 41+7+13+82 catalog tests OK, hosted CI run 45057444858 @ f3f0188ba SUCCESS (PR Trusted Plan green), PR #1785 ready (base develop, head f3f0188ba, ls-remote witness). branch lane-0428-248-catalog-surface-e, head f3f0188bad2caaf10e90fc8f2f1552383f30bd5d. Evidence: evidence/r28-welle5-2026-11-22/gate-catalog-0428-248/surface-e-round-1.md (origin/main). cleanliness: no container/compose project or network started by this sitz (catalog JSON + read-only python/go checks only); baseharbor-plan worktree clean. Waiting on owner/Codex review of PR #1785.
