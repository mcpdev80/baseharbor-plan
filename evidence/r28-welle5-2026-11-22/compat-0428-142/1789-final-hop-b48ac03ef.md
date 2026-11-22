# 0428-076 / #1789 FINAL hop onto develop b48ac03ef — DONE

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 follow-up — additive hop of existing PR #1789 onto the newest develop head b48ac03ef (#1771 merged)
candidate: 2edc757079e27617f44e24fc02daf4e37db1e58a (hop merge of d7c109dc1 onto develop b48ac03ef)
base develop SHA: b48ac03ef75165c4e50a4a29d5ef0197af3444da
PR #1789: https://github.com/mcpdev80/baseharbor/pull/1789 (draft, base develop, head codex/0428-076-promql-ci-capture)
hosted CI run: 45078492469 (head 2edc7570, conclusion success)
status: END_DONE

## PLAN

1. Read mission m_0847_1789final.md.g; verify real remote, develop head, PR #1789 head, hop branch.
2. Fetch origin/develop b48ac03ef; merge --no-ff origin/develop into hop branch (HEAD d7c109dc1). No force/rebase/amend of existing commits.
3. Verify after merge: git diff origin/develop HEAD -- scripts/pr-gate-coverage.json shows STILL ONLY my 6 promql-deletion lines (0 plus). Foreign rows (mcp.go/target.go/operatorauth) intact. JSON valid, catalog regression OK, no dangling ref, metrics builds + selector/malformed test passes in default build.
4. Push new head + ls-remote refs/pull/1789/head witness. Keep PR draft. No merge.
5. Watch hosted CI on new head to terminal (self-run duty). Record run-id + status.
6. Publish akte to baseharbor-plan origin/main, verify path present, then post END_DONE to 9142ab1f.

## Realität / base attestation

- Real remote: `origin` = https://github.com/mcpdev80/baseharbor.git, `lane-origin` = same (both github.com/mcpdev80, per REMOTE GUARD). Confirmed first git action.
- develop head (ls-remote): b48ac03ef75165c4e50a4a29d5ef0197af3444da. This SHA is the ancestor of hop head 2edc7570 (verified: `git merge-base --is-ancestor b48ac03ef... HEAD` => YES).
- PR #1789 head was d7c109dc1 (prior hop). This hop is git-only (no new content); d7c109dc1's content is preserved under the no-ff merge.
- `git diff --name-only origin/develop HEAD` lists ONLY: internal/metrics/perses_dashboards_promql_test.go, scripts/pr-gate-coverage.json, scripts/test_pr_native_gate_plan.py — plus #1771's cmd/baha/* files (expected from develop). No foreign candidate content carried on top beyond develop's own.
- #1771 (develop b48ac03ef vs prior develop 78f75c907) touches ONLY cmd/baha/* files — NO catalog, NO internal/metrics. Verified: promql diff stays isolated, no conflict expected/found.

## The hop (git-only, no new content)

Work done in a dedicated worktree /tmp/opencode/1789-hop-wt (existing worktree /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 left clean and untouched).

1. Fetched origin/develop (b48ac03ef).
2. Reset hop branch codex/0428-076-promql-ci-capture to the remote head d7c109dc1 (local only — no force-push).
3. `git merge --no-ff origin/develop` — NO conflict. develop contributed #1771's cmd/baha/* changes only (local_workload_authority.go, local_workload_authority_test.go, main.go, target.go, target_runtime_access_provider_test.go).
4. New hop head: 2edc7570 (d7c109dc1 merged --no-ff onto develop b48ac03ef; existing commit 1d67c5676 preserved via no-ff).

Stop-criteria checked (mission §3):
- (a) Trusted Plan fail-loud on uncatalogued own source: NO uncatalogued source — only promql deletions. Verified.
- (b) .github/** touched: NO. Verified.
- (c) diff vs develop shows unintended removal of foreign rows: NO. Verified.

## Catalog diff vs develop (mission §2 — must show ONLY my 6 promql-deletion lines)

git diff origin/develop HEAD -- scripts/pr-gate-coverage.json scripts/test_pr_native_gate_plan.py:

- scripts/pr-gate-coverage.json: removed source.internal.metrics.perses.dashboards.promql.test.go / internal/metrics/perses_dashboards_promql_test.go (6 minus lines, 0 plus).
- scripts/test_pr_native_gate_plan.py: removed 'internal/metrics/perses_dashboards_promql_test.go' from the native-gate path tuple (1 minus line).
- NO #1771/#1784/#1785/#1786 rows removed. Verified intact on new head: mcp.go=2, target.go=4, operatorauth=2.

JSON still valid (214 components); catalog python regression test passes; no dangling promql path.

Selector-validity + malformed-query rejection remain covered by the default-build assertValidPromQL heuristic / TestPersesInvalidTrailingMatcherIsRejected (existing deps). Verified on new head:
- go build ./internal/metrics/ (default build) => BUILD OK
- go test ./internal/metrics/ -run '^TestPersesInvalidTrailingMatcherIsRejected$' -count=1 => ok 0.005s

## CI-Aufnahmepflicht proof — hosted CI

- Run 45078492469 (head 2edc7570, conclusion success, https://github.com/mcpdev80/baseharbor/actions/runs/45078492469).
- Job "PR · Draft Go · packages" (id 137381018090, conclusion success).
- Job log: `go test -p 1 "${owned[@]}" -count=1` ran in the DEFAULT build (grep -c "promqlparser" in job log = 0; the dead tagged path ran nowhere).
- internal/metrics compiled and passed: "ok github.com/mcpdev80/baseharbor/internal/metrics 1.242s".
- Selector-validity + malformed rejection executed+passed in the default-build Go unit packages job. CI-Aufnahmepflicht satisfied on the new head.
- All non-skipped jobs on run 45078492469: PR · Draft source and routing -> success; PR · Draft Go · cli-0/1/2/3 -> success; PR · Draft Go · packages -> success. PR · Native gate plan / Native / Native Keycloak/Core -> skipped (expected: the catalog rows the native data-caps referenced are the deleted promql rows; no uncatalogued own source remains).
- gofmt clean on changed Go files; scripts/source-readability-audit.sh PASS; scripts/ci-workflow-policy.sh PASS (20 approved workflow files).

## Evidence witnesses

- ls-remote refs/heads/codex/0428-076-promql-ci-capture = 2edc757079e27617f44e24fc02daf4e37db1e58a
- ls-remote refs/pull/1789/head = 2edc757079e27617f44e24fc02daf4e37db1e58a (= branch head; PR head snapshot refreshed on push)
- CI run 45078492469 databaseId=45078492469, head_sha 2edc75707, conclusion success, status completed.
- CI job-log fetched via gh api to /tmp/opencode/pkg-logs3.txt (temporary, outside ecosystem root).

## END lane

END_DONE — #1789 FINAL hop onto develop b48ac03ef is complete. Hop head 2edc7570 = d7c109dc1 merged --no-ff onto develop b48ac03ef; git-only, no new content, existing commit preserved. diff vs develop = only my 3 files + #1771 cmd/baha/* (from develop). Catalog diff shows ONLY my 6 promql-deletion lines, 0 plus; foreign rows (mcp.go/target.go/operatorauth) intact, no #1771/#1784/#1785/#1786 rows lost. JSON valid, catalog regression passes, metrics builds + selector/malformed test passes in default build. Hosted CI run 45078492469 (head 2edc7570) SUCCESS: Go unit packages ran internal/metrics in the default build (no -tags promqlparser), internal/metrics ok 1.242s, 0 promqlparser hits; all other non-skipped jobs success; native gates correctly skipped. gofmt/readability/workflow-policy pass. No .github touch, no merge (owner/Codex review pending). PR #1789 stays draft.

## cleanliness

- Hop worktree: /tmp/opencode/1789-hop-wt (dedicated worktree under /tmp/opencode, outside ecosystem root). The existing dedicated worktree /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 left clean (git status -s empty) and untouched.
- No stray baha binary, no go.mod/go.sum/product/.github change (scoped to the git-only hop; *_test.go + scripts/** on top of develop).
- No docker/podman compose projects started (git/gh read-only verification of hosted CI; no containers on the coordinator host).
- git ps -a witness: none started (no docker/podman daemon contact).
- Temporary log files: /tmp/opencode/pkg-logs3.txt (outside ecosystem root).
