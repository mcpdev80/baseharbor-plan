# 0428-248: catalog fill surfaces (surface-d)

- karte 0428-248, sitz f0f6c8b4. DEP-FREIE KATALOG-LANE. develop b27b2ebe.
- Trusted-Plan guardian aborts PRs fail-loud whose NEW product source is not catalogued in scripts/pr-gate-coverage.json.
- Dispatched census listed: cmd/baha/mcp.go, cmd/baha/core_targets.go(+core_targets_test.go), cmd/baha/app_secrets.go.
- REALITY CHECK on develop b27b2ebe: census paths may be stale. Which actually exist AND are uncataloged?
- ONLY scripts/pr-gate-coverage.json + one planner-unit. NO product code, NO .github, NO footprint/237, NO stage-boundary/ci-operator (other lanes).

## PLAN

1. Establish reality (remote guard, develop b27b2ebe via ls-remote). Cut lane-0428-248-catalog-surface from EXACTLY origin/develop b27b2ebe.
2. grep + ls-tree: which census paths exist on develop b27b2ebe AND are truly NOT source-paths in scripts/pr-gate-coverage.json (else STOP+report). Use resolve_covered_gates to find genuine uncataloged set.
3. Map the genuine uncataloged product source to an existing surface with a valid release-gate owner: cmd/baha/mcp.go -> gate.mcp (atomic/static/mcp). Only scripts/pr-gate-coverage.json. NO product code, NO .github, NO footprint/237.
4. Regression: validate-pr-gate-coverage.py + test_pr_gate_coverage.py + planner-unit show the path mapped, no uncataloged-abort. ci-fast-check.sh fast gates before push.
5. Hosted PR push -> draft->ready -> PR. ls-remote pull/<n>/head witness. PR body lists the path + surface + why census paths excluded. akte. Publish to baseharbor-plan origin/main. END + post.

## BASE ATTESTATION

- develop HEAD (ls-remote, github.com/mcpdev80): b27b2ebedb7da10690fb83c24a9f763ee16d7468
- Used existing clean branch lane-0428-248-catalog-surface (at origin/develop b27b2ebe, unmodified) — coordinator queue commit 1222 had paused this sitz to avoid a competing write.
- branch head: 7d7c81fce2b3cb1700d533d7ccdb07a4908d0c44
- merge-base(origin/develop, HEAD) = b27b2ebe; git log origin/develop..HEAD = only my commit; git diff origin/develop..HEAD --name-only = scripts/pr-gate-coverage.json only.

## Reality (deviation from dispatched census)

The dispatched census paths were partially stale:

- cmd/baha/core_targets.go — NEVER existed on develop (no history; git log --all --diff-filter=D = none).
- cmd/baha/core_targets_test.go — NEVER existed on develop.
- cmd/baha/app_secrets.go — NEVER existed on develop.
- cmd/baha/mcp.go — EXISTS on develop b27b2ebe, was uncataloged (resolve_covered_gates returned it unresolved -> fail-loud guardian aborted PR #1752 / #1738).

Verified: `git ls-tree origin/develop -- cmd/baha/mcp.go cmd/baha/core_targets.go cmd/baha/app_secrets.go` = only mcp.go present. `git log --all --diff-filter=D -- cmd/baha/core_targets.go cmd/baha/app_secrets.go` = empty. So only cmd/baha/mcp.go is a genuine, catalogable product source.

## Surface decision (authoritative, not guessed)

- cmd/baha/mcp.go is the MCP tool-registration entrypoint (registerMCP*Tools in runMCPServer), the machine-interface surface.
- The catalog surface gate.mcp is owned by release gate atomic/static/mcp (selection_scope: focused, in release requirements gates, covers ['capability.profile.machine-interface', 'gate.mcp']).
- Existing census (gap-census-round-1.md) flagged mcp.go as "ambivalent" and did not pin the surface. Authoritative-source mapping: gate.mcp -> atomic/static/mcp. validate() accepts it, resolve_covered_gates(['cmd/baha/mcp.go']) = ['atomic/static/mcp'], guardian still fails for truly-unknown paths.
- No new surface-key invented; no new native_checks row (gate.mcp is static, no native/docker|podman row needed — correct for a static surface).

## Change (catalog JSON only)

- Added component `source.cmd.baha.mcp.go`: {id: "source.cmd.baha.mcp.go", path: "cmd/baha/mcp.go", surfaces: ["gate.mcp"], runtime_specific: true}, inserted after source.cmd.baha.main.go.
- One-commit, one-file, surgical edit. No product, .github, footprint, stage-boundary or ci-operator change.

## Regression

- python3 scripts/validate-pr-gate-coverage.py -> "PR gate coverage catalog is valid"
- resolve_covered_gates(['cmd/baha/mcp.go']) -> (['atomic/static/mcp'], [])  (unresolved: [])
- resolve_covered_gates(['cmd/baha/zz_new_uncataloged.go']) -> ([], ['cmd/baha/zz_new_uncataloged.go'])  (fail-loud intact)
- unittest scripts.test_pr_gate_coverage scripts.test_ci_v0427_gate_catalog scripts.test_pr_required_final scripts.test_pr_ci_fallback scripts.test_pr_diff_base -> 97 tests OK
- scripts.test_pr_gate_plan OK (37 cases), scripts.test_pr_native_gate_plan OK (13), scripts.test_pr_gate_coverage OK (41)
- gofmt: no changed Go files (JSON only); scripts/source-readability-audit.sh PASS; scripts/ci-workflow-policy.sh PASS (20 approved workflow files)
- Hosted CI run 45054068537 @ 7d7c81fce: conclusion success. Selected green: PR · Trusted Plan, PR · Focused Python, PR · Validation · pr-planner-tests, ci-executor-tests, ci-policy, Native gate plan. PR Selected Checks success. Runtime/native gates correctly skipped (mcp.go is a static surface — no native/docker|podman row expected for a catalog-only PR).

## Hosted PR

- PR #1784 https://github.com/mcp80/baseharbor/pull/1784 (base develop, head lane-0428-248-catalog-surface @ 7d7c81fce)
- ls-remote refs/pull/1784/head = 7d7c81fce2b3cb1700d533d7ccdb07a4908d0c44 (matches branch head)
- CI run 45054068537 @ 7d7c81fce: completed/success.
- Class: review = handed off; exact-head CI (run 45054068537) green; Codex review pending.

## repo-rule compliance

- dep-free catalog lane: only scripts/pr-gate-coverage.json changed; no product code, no .github/**, no footprint/237, no stage-boundary/ci-operator.
- one integration candidate, one PR per card; branch from develop b27b2ebe (base attestation shown); only my commit in origin/develop..HEAD.
- no subagents; no merge/comment; no product write; no .github touch.

## END

END_DONE w27-pr1627-0428-061-pull: 0428-248 catalog fill surfaces (surface-d) DONE. Reality deviation from dispatched census: core_targets.go/core_targets_test.go/app_secrets.go NEVER existed on develop b27b2ebe (git history empty); only cmd/baha/mcp.go genuinely exists AND was uncataloged. Mapped cmd/baha/mcp.go -> surface gate.mcp (owned by release gate atomic/static/mcp) via surgical one-file catalog edit; validate() OK, resolve_covered_gates=['atomic/static/mcp'], fail-loud guardian intact, 97 catalog/plan tests OK, hosted CI run 45054068537 @ 7d7c81fce SUCCESS (PR Trusted Plan green), PR #1784 ready (base develop, head 7d7c81fce, ls-remote witness). branch lane-0428-248-catalog-surface, head 7d7c81fce2b3cb1700d533d7ccdb07a4908d0c44. Evidence: evidence/r28-welle5-2026-11-22/gate-catalog-0428-248/surface-d-round-1.md (origin/main). cleanliness: no container/compose project or network started by this sitz (catalog JSON + python/go read-only checks only); baseharbor-plan worktree clean. Waiting on owner/Codex review of PR #1784.
