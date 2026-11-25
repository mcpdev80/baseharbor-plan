# 0428-288: demo PR#170 qualification (w170-quali)

- Lane `w201-0428-288-demo-170-quali`. Mission `coordinator/missions/w170-quali.txt`. Card 0428-288 context 0428-250. This mission performs NO card edits and NO product/fixture edits: duties are (1) read PR diff + card akte, (2) transition PR#170 from DRAFT to READY (one-way), (3) watch Hosted CI to terminal and record run databaseId + job receipts, (4) if it fails report STATE and STOP, (5) report head + run ID to the w136/w200 review queue. NO merges, NO plan commits (freeze), NO new cards.

## visible ansatz block

- Card 0428-250 governing frontmatter owner: fetched from origin/main at runtime (see below; akte-context read from evidence/r28-welle5-2026-11-22/ci-operator-allowlist-0428-250/).
- git author identity for any candidate commit (none needed this lane, no commit): `git -c user.name=w201-0428-288-demo-170-quali -c user.email=w201-0428-288-demo-170-quali@baseharbor.local commit ...`
- pre-push gate (for any candidate): `git show -s --format=%an HEAD` must equal the lane name `w201-0428-288-demo-170-quali`.
- This lane makes no commit and no push to the product repo: the PR#170 candidate already exists; the only write is `gh pr ready 170` on the remote.

## PLAN

1. Read mission file (done first, before git).
2. Establish reality witnesses: planning repo `remote -v`, PR#170 head via ls-remote, governing card akte from origin/main.
3. Read PR#170 diff + card 0428-250 akte context; confirm the in-scope demo fix; confirm PR is OPEN+DRAFT.
4. Transition PR#170 to READY per READY-TOGGLE doctrine (one-way `gh pr ready 170`); verify `.draft==false` via `gh api`.
5. Watch Hosted CI (pull_request event) to terminal; record run databaseId + per-job receipts (executed, not skipped; per_page=100).
6. On failure: report STATE (job + failing log line) and STOP — no fixture edits beyond run.sh's own row.
7. Report head + run ID to coordinator; clean down any compose stack; publish evidence to baseharbor-plan origin/main; post END.

## base attestation

- Planning repo (real): `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch) / (`push`). Verified with `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` before any evidence commit.
- demo PR#170 head (git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/pull/170/head): `0249c9f73c21f46ba532fddc94a764e772f69acf`.
- demo branch default (git ls-remote refs/heads/main): `f10216f717810111502cd160fd6ab104f9fd7d35`.
- PR#170 base ref: `develop`; merge-base origin/develop..HEAD: to be confirmed post-fetch during watch (PR base is develop).
- gh auth: logged in as mcpdev80 (github.com), active account.

## PR #170 diff (read-only)

- One file: `baseharbor-demo/tests/config-matrix/run.sh` (+11/-12).
- Change: the config-matrix core-up temp root is now named `baseharbor-core-bootstrap.XXXXXX` (was `.config-matrix.XXXXXX`), `bootstrap_root="$matrix_root"` (the extra `control-plane` subdir dropped), and `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root"` is exported around the `baha up --yes` call (matching tests/core-bootstrap.sh so the demo operator allow-list admits the up). The `doctor`/`^READY` gate stays after the subshell.
- This is the same in-scope demo fix implemented in prior session w21 (evidence r28 akte). It touches ONLY the demo test script; NO baseharbor product code, NO .github, NO allow-list widening, NO guard.
- PR#170 current state: `state=OPEN`, `isDraft=true`, `mergeStateStatus=CLEAN`, base `develop`, head `0249c9f73`.

## card 0428-250 akte context (origin/main)

- Evidence akte `demo-fix.md` + `fix-round-1.md` under evidence/r28-welle5-2026-11-22/ci-operator-allowlist-0428-250/ on origin/main.
- Round-1 (H-V30): baseharbor synthetic-operator allow-list (cmd/baha/ci_integration_operator_enabled.go:24-119, :304-352) is NARROW AND CORRECT. The static gates fail because the demo harness runs `baha up --yes` from a fixture root not named `baseharbor-core-bootstrap.*` and not setting `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT`.
- Fix (demo-side, w21): name the config-matrix temp root `baseharbor-core-bootstrap.*` and export the env var around core-up -> ciIntegrationLocalCoreBootstrap admits the up -> operator stamped. This is the content of PR#170.

## PR -> READY transition (step 4) — DONE

- One-way per mission: `gh pr ready 170 --repo mcpdev80/baseharbor-demo`. Retried several times against transient GitHub GraphQL "Something went wrong" + one 502 Bad Gateway; succeeded on the last attempt.
- Verify: `gh api repos/mcpdev80/baseharbor-demo/pulls/170` → `.draft == false`, `state == open`. Confirmed draft=false.
- PR#170 confirmed: base `develop`, head `lane-0428-250-demo-operator-root@0249c9f73c21`, draft=false, state=open, mergeStateStatus=CLEAN.

## CI watch + receipts (step 5) — STATE / NON-QUALIFYING TRIGGER

- Watch run databaseId via `gh api repos/mcpdev80/baseharbor-demo/actions/runs?per_page=100`, filtered to head `0249c9f73`, plus the pull_request check-runs endpoint. Result: NO workflow run exists for head `0249c9f73` under ANY event (pull_request or workflow_dispatch). PR status-check rollup is `null` (terminal view after ~3 min of polling).
- Root cause (base/trigger config, Owner scope `.github/**`): the only PR-triggered workflow is `.github/workflows/pr-guided-consent.yml`, whose trigger is `on: pull_request: branches: [main]`. PR#170's base is `develop`, so the `pull_request` event from the READY transition matches NO branch and fires nothing. The other workflow `v0424-targeted.yml` triggers only on `push` to `work/v0.4.2*` release branches — irrelevant here.
- This is NOT a candidate content defect: the run never starts because of the base/trigger mismatch, not because the head fails. The head SHA `0249c9f73` itself has not been executed by any required job. Per the proof rule, success requires an actually-executed required job on the exact head — that has not occurred.
- STATE (non-qualifying trigger, not a red job): no run was started; the pull_request event is scoped to `main`-based PRs only. No failing log line exists (no job ran). No fixture edit to `tests/config-matrix/run.sh` (in scope) is warranted — the gap is the workflow trigger base, which is Owner scope.
- Exact file:line (the STATE finding): `.github/workflows/pr-guided-consent.yml`, the `on: pull_request:` block lists `branches: [main]` only (confirmed via `gh api repos/mcpdev80/baseharbor-demo/contents/.github/workflows/pr-guided-consent.yml?ref=main` → decoded YAML: `on:\n  pull_request:\n    branches: [main]\n  workflow_dispatch:`). PR#170's base is `develop` → the `pull_request` event matches no branch → fires nothing.
- Fired-but-empty event evidence (terminal):
  - `gh api repos/mcpdev80/baseharbor-demo/pulls/170 --jq '{base, head, head_sha, draft, state}'` → `{"base":"develop","draft":false,"head":"lane-0428-250-demo-operator-root","head_sha":"0249c9f73c21","state":"open"}` (ready, not a failed step).
  - `gh api repos/mcpdev80/baseharbor-demo/actions/runs?per_page=100` filtered to `.head_sha|startswith("0249c9f73")` → empty (no run for this head under any event).
  - `gh api repos/mcpdev80/baseharbor-demo/pulls/170 --jq '.statusCheckRollup'` → `null` (no checks produced).
  - Newest repo workflow_runs: run #93 (head `6371ca5542c4`) completed `success` at 2026-11-25T15:47Z — BEFORE my READY (~17:00Z); nothing newer for `0249c9f73`.

## Scope note

- Per the scope split (Owner clarification 2026-11-04), `.github/**` belongs to the Owner. The required change — adding `develop` to the `pr-guided-consent.yml` pull_request trigger (or otherwise qualifying develop-based PRs) — is an Owner action. I report it as a finding with file:line and STOP, per the mission's "report a failing check as STATE ... and stop there." I do NOT edit the workflow and do NOT trigger workflow_dispatch.
- This lane makes no commit and no push to the product repo: the PR#170 candidate already exists; the only write is the remote `gh pr ready` (already done).

## END w201-0428-288-demo-170-quali

END_DONE (STATE at non-qualifying trigger; Owner ruling 2026-11-25: stop, leave #170 in current ready state, trigger change is an Owner decision item).
- head: `0249c9f73c21f46ba532fddc94a764e772f69acf` (PR#170 head, branch `lane-0428-250-demo-operator-root`, base `develop`)
- run databaseId: NONE (no run started; base=develop triggers nothing)
- STATE (file:line): `.github/workflows/pr-guided-consent.yml` `on: pull_request: branches: [main]` vs PR#170 base `develop` — event fires nothing. No red job, no log line (no job ran).
- Candidate content: NOT tested — the run never starts. No product/fixture edit made; PR#170 head unchanged.
- Trigger change (add develop to the pull_request trigger, or otherwise qualify develop-based PRs) is an OWNER decision item — Owner scope `.github/**`.
- No commit, no push, no re-toggle, no workflow_dispatch, no .github touch. PR#170 left in its CURRENT ready state.
- No compose stack started (no containers to clean).
