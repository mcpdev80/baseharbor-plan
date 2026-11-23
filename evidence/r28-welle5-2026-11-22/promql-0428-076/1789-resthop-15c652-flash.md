# 0428-076 / PR #1789 — REST-HOP onto develop 15c652136 (git-only)

Lane: w076-0428-076-1789rest (restored flash session, handoff from b90e; single writer on
branch `codex/0428-076-promql-ci-capture`, worktree `/home/marcel/dev/baseharbor-ecosystem/workers/0428-223-1789-wt`).
Mission: /tmp/opencode/m_9b7_1789re.md.g — rest-hop, no content edits, no merge.

## PLAN

1. Resolve remotes and locate the existing #1789 worktree/branch.
2. `git fetch origin develop`; `git merge --no-ff origin/develop` into the candidate branch (no force/rebase/amend, no new branch).
3. Katalog-check: `git diff origin/develop HEAD -- scripts/pr-gate-coverage.json` == delete-only promql entry (6 minus / 0 plus), no `.github` touch.
4. Push and take `ls-remote refs/pull/1789/head` witness.
5. Watch the exact hosted CI run to terminal; record head + run-id + gates; classify the advisory candidate-added result.
6. Write this evidence, publish to baseharbor-plan origin/main, post END.

## Remote resolution (REMOTE GUARD)

`git remote -v` in the worktree (first git action):

```
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```

All fetch/push/ls-remote used only this github.com/mcpdev80 URL.

## BASE ATTESTATION

- Branch cut base (previous hop): `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e` (merge-base of HEAD and develop before this hop).
- New develop head fetched: `git ls-remote origin refs/heads/develop` →
  `15c652136b0fce19dd0ae286b341b38cac3f7854 refs/heads/develop`
- Pre-hop PR/branch head (`git ls-remote origin refs/pull/1789/head refs/heads/codex/0428-076-promql-ci-capture`):
  both `469947501944603bd08aab1b3fb02a0474a5f1ec` (matches mission handoff).
- Merge: `git merge --no-ff --no-edit origin/develop` → auto-merged `scripts/pr-gate-coverage.json`
  (ort strategy), merge commit `2be1136606d5c881badf317bd001f0024da1ea46`. No conflicts, no force,
  no rebase, no amend, same branch only.
- Ancestry witness: `git merge-base --is-ancestor origin/develop HEAD` → exit 0 (develop 15c652136
  is an ancestor of the merge commit).

## Branch content proof

`git log --oneline origin/develop..HEAD` (lists ONLY this chain's own commits + merge commits, no foreign candidates):

```
2be11366 Merge remote-tracking branch 'origin/develop' into codex/0428-076-promql-ci-capture
46994750 Merge origin/develop b9e69b14 into codex/0428-076-promql-ci-capture (#1789 final hop: inherits #1790/#1791 ingress rows)
146ccf6f test(metrics): clean English in promqlparser-witness comments
b9af4ec9 test(metrics): reword two stale comments on removed promqlparser witness
2ba09ce3 Merge remote-tracking branch 'origin/develop' into HEAD
bc3a8d7f Merge remote-tracking branch 'origin/develop' into HEAD
2edc7570 Merge remote-tracking branch 'origin/develop' into codex/0428-076-promql-ci-capture
d7c109dc Merge remote-tracking branch 'origin/develop' into codex/0428-076-promql-ci-capture
1d67c567 test(metrics): drop dead promqlparser-tagged perses witness from default build
```

`git diff origin/develop...HEAD --name-only`:

```
internal/metrics/perses_dashboards_promql_test.go
internal/metrics/perses_dashboards_test.go
scripts/pr-gate-coverage.json
scripts/test_pr_native_gate_plan.py
```

## Katalog-check (step 2)

`git diff origin/develop HEAD -- scripts/pr-gate-coverage.json` is exactly one hunk,
**6 deleted lines / 0 added lines** — the removal of the single `promql` catalog row
(id `source.internal.metrics.perses.dashboards.promql.test.go`), i.e. delete-only #1768.
Verified counts: develop JSON has 1 promql row, HEAD JSON has 0; id-level diff removes only
that one id. All base rows retained, including `app_access` rows (JSON lines 217/225).
No `.github/**` file is touched by the branch (`git diff origin/develop HEAD --name-only -- .github/` → empty).

## Push + delivery witness (step 3)

`git push origin HEAD:refs/heads/codex/0428-076-promql-ci-capture` →
`46994750..2be11366  HEAD -> codex/0428-076-promql-ci-capture`.

Post-push `git ls-remote origin refs/pull/1789/head refs/heads/codex/0428-076-promql-ci-capture`:

```
2be1136606d5c881badf317bd001f0024da1ea46	refs/heads/codex/0428-076-promql-ci-capture
2be1136606d5c881badf317bd001f0024da1ea46	refs/pull/1789/head
```

No merge performed by this lane (mission: KEIN merge; the old run 45092733609 on b9e69 is obsolete).

## Hosted CI (step 4, Eigenes-Run-Pflicht)

- Run: `CI · Source & Quality` — run-id **45094339280**, event pull_request, headSha
  `2be1136606d5c881badf317bd001f0024da1ea46`, url https://github.com/mcpdev80/baseharbor/actions/runs/45094339280
- Watched by this session to terminal: `status=completed conclusion=success`
  (created 2026-11-23T01:23:54Z, updated 2026-11-23T01:34:25Z).
- Required/selected gates (executed, terminal states):
  - PR Selected Checks — success
  - PR · Trusted Plan — success; PR · Native gate plan — success
  - PR · Workflow policy / Source format / Runner Interface — success
  - PR · Go unit · cli-0/cli-1/cli-2/cli-3/packages/owner — success
  - PR · Focused Python — success; PR · Exact Candidate — success; PR · Demo Pin — success
  - PR · Validation · ci-executor-tests / ci-policy / go-build / go-vet / pr-planner-tests /
    receipt-execution-tests — success
  - PR · Selected Runtime docker · observability — success
  - PR · Selected Runtime podman · observability — success
  - Release matrix / HA / draft / consumer-pin / pre-release jobs — skipped by plan (not applicable to this diff)
- Advisory status: `PR · Candidate-added checks (advisory)` — **failure (red)**. Failing log line:
  `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared
  runtime gate owner: internal/metrics/perses_dashboards_promql_test.go (id
  source.internal_metrics_perses_dashboards_promql_test_go): add this source with its surfaces to
  scripts/pr-gate-coverage.json ...` with the job's own note `Candidate planner: FAIL (the required
  base plan is unaffected).`
  This is the known, documented card **0428-253** advisory case (candidate-added route for the
  deleted promql test file). Per CI policy it cannot block this PR; documentation only, no action taken here.

## Local checks before push

`bash scripts/ci-fast-check.sh` (before the push): Go file size / function span / regression
ratchet PASS, Workflow policy PASS (20 approved files), 41 + 303 python tests OK,
"No candidate-added validation checks. The trusted base plan remains the only merge requirement." Exit 0.
JSON validity of `scripts/pr-gate-coverage.json` verified with python3 json.load.

## cleanliness

- No containers, compose projects, networks or volumes were started or touched by this lane
  (git-only hop; docker/podman tests run only on the named SSH hosts).
- `docker ps -a` (host pid 3174895) before/after: header only, zero containers, ambient stack untouched.

## Evidence-on-origin/main verification (second-to-last actions)

```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 1789-resthop-15c652-flash
evidence/r28-welle5-2026-11-22/promql-0428-076/1789-resthop-15c652-flash.md
```
(commit f8041e1eb on origin/main; planning repo remote verified: https://github.com/mcpdev80/baseharbor-plan.git)

END_DONE w076-0428-076-1789rest: rest-hop merged develop 15c652136 into #1789 (no conflicts), new head 2be11366 pushed and witnessed, katalog diff delete-only promql row (6-/0+), run 45094339280 completed/success on exact head; sole red is advisory Candidate-added checks (known 0428-253, non-blocking).
