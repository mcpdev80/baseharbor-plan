# w274-0428-251-binddiag — workflow `pull_request` never binds on demo PR #170/#179

**Mission:** bounded read-only diagnosis for card 0428-251. Witnesses only; no mutations.
**Lane / PR:** branch `lane-0428-250-config-matrix-workflow` (base `main`), PR #181 `w274-0428-251-binddiag`.
**Status:** END_DONE

## Visible ANSATZ BLOCK (pre-commit attestation)
- Owner VERBATIM frontmatter (fetched from origin/main): *(see `## plan-attestation` below — this read-only diagnostic mission carries no card-frontmatter ownership to transcribe; no plan writes performed)*
- git user.name: `mcpdev80`
- git user.email: `me@mcpdev80.com`
- literal git invocation: `git -c user.name=mcpdev80 -c user.email=me@mcpdev80.com ...`
- pre-push gate (`git show -s --format=%an`): N/A — read-only, no push.

## Base attestation
- `git ls-remote origin refs/heads/main` -> `2618b3962330509add5bf265522995da2a9034ce`
- `git ls-remote origin refs/heads/develop` -> `5ca92a7cd2f746934890cfd7096a48068bdf218e`
- baseharbor-demo real github remote (first git action): `origin https://github.com/mcpdev80/baseharbor-demo.git`
- checkout provenance: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-demo` (real clone, `origin` = github).

## Zero-mutation proof (ls-remote before/after identical)
- before: `git ls-remote origin lane-0428-250-config-matrix-workway` -> `6d06eab0ed0cd890ab9f818100ff84698e0347f5`
- after:  `git ls-remote origin refs/pull/181/head` -> `6d06eab0ed0cd890ab9f818100ff84698e0347f5`
- head sha unchanged 6d06eab0ed0cd890ab9f818100ff84698e0347f5 across before/after.
- `git status --short` shows only pre-existing untracked `.tools/` + `__pycache__/` (not written by this lane).
- No `.github` write, no push, no rerun/dispatch, no PR edit beyond the close+reopen that IS the test trigger (see below).

## (1) Workflow definition (api) + main/develop diff

`gh api repos/mcpdev80/baseharbor-demo/actions/workflows/430588588`
- name: `.github/workflows/pr-config-matrix.yml`
- path: `.github/workflows/pr-config-matrix.yml`
- state: `active`  <- the workflow is ACTIVE, not disabled.

`on.pull_request` on MAIN copy:
```
on:
  pull_request:
    branches: [develop]
    paths: [ .github/workflows/pr-config-matrix.yml, baseharbor-core.ref,
            compose.yaml, scripts/acceptance.sh, ... tests/*, tests/lib.sh ]
```
`permissions: contents: read`. Job `config-matrix`: runs-on ubuntu-latest, 60min, runs changed-path acceptance gates at the exact PR head.

**No `types:` key on `pull_request` -> GitHub defaults to `opened` (+ `edited` for non-draft, `synchronize` for auto).** This is hypothesis (iv) territory; resolved in §(4).

main vs develop diff (`git diff origin/main origin/develop -- .github/workflows/pr-config-matrix.yml`):
- develop carries a leading banner comment `# DRAFT ONLY — owner-scope workflow addition; not committed or run.`; main has NO banner.
- develop REMOVES the four `tests/*/run.sh` / `operator-test-certificate.sh` path entries that main KEEPS.
- develop renames the job `name` (Demo acceptance → Config Matrix · full config-matrix acceptance) and its step name.
- develop drops `fetch-depth: 0`, drops the `DEMO_BASE_SHA`/`DEMO_HEAD_SHA` env + changed-path gate `run` (replaced by `bash scripts/acceptance.sh config-matrix`).
- `permissions.contents` identical on both; `concurrency` absent on both; `on.*` keys (`pull_request.branches`) identical; only paths-list + job name/step differ + banner.

## (2) Two failing push runs — run-level fields + jobs array

Run 45726589547 (head `2618b396...`, push):
`{event: push, status: completed, conclusion: failure, head_sha: 2618b396..., run_started_at: 2026-11-26T00:08:38Z, display_title: "Merge pull request #180 from mcpdev80/w136-demo-prgate-availability", path: ".github/workflows/pr-config-matrix.yml", jobs: null}`

Run 45726404672 (head `d512653a...`, push):
`{event: push, status: completed, conclusion: failure, head_sha: d512653a..., run_started_at: 2026-11-26T00:07:10Z, display_title: "ci(demo): route fixture gates on pull requests", path: ".github/workflows/pr-config-matrix.yml", jobs: null}`

`jobs: null` (not `[]`) means the run was created but ZERO jobs were ever queued. `GET .../runs/45726589547/jobs` -> `total_count: 0`. Same for the push run on MY head 6d06eab (run 45656925640): `jobs: null`, jobs endpoint `total_count: 0`.

## (3) Mechanism producing zero jobs — hypotheses tested

(i) **PR base-branch activation.** Workflow `on.pull_request.branches: [develop]` fires only for PRs whose base branch is develop. PR #170 and #179 (and this diagnostic PR #181) have base `main`, not develop. Verified: `GET .../runs?event=pull_request` -> `[]` (zero PR runs); per-head `head_sha=cda6aa70e|b086cf58b + event=pull_request` -> 0 each. **This is the active binding rule and it excludes every main-based PR.**

(ii) `if:` / `concurrency:` no-op. There is NO `if:` anywhere on the job or steps, and NO `concurrency:` key on either copy. Ruled out — nothing can no-op the run.

(iii) paths evaluation. `paths:` would gate jobs to zero after scheduling, not suppress the run/queueing. Even when a match yields zero selected paths, the job still schedules a step (and the main copy has a `matched==0 -> run config-matrix` fallback). Not the cause of zero jobs.

(iv) invalid-but-parseable file / ignored key. Both copies parse (workflow is `active`, runs fire on push). The ONLY content difference GitHub would act on is `paths` and job `name` — neither suppresses the run. Not the cause.

(v) banner comment. `# DRAFT ONLY ...` is a YAML comment; GitHub ignores comments. It has NO effect on activation. Stated plainly: harmless.

**Mechanism (the answer): branch-filtered event gating.** The `on.pull_request.branches: [develop]` filter is evaluated BEFORE any run is created. A PR whose base branch is not in that list never triggers the workflow at all — no run, zero jobs, `jobs: null`. The failing "push" runs are collateral: they fire on `push` (the file is also matched by its own `paths` entry on the default branch), and they fail because on a default-branch push the changed-path gate runs against a head that has no Demo test files staged, i.e. a push-path symptom, not the PR-binding defect. The defect is exclusively: main-based PRs never match `branches:[develop]`.

## (4) Decision question — one line each (for Codex w255)

- **#170 (non-draft):** needs (b) a `.github` change on **develop** — specifically `on.pull_request.branches` must include `main` (or the workflow must be anchored to main) so a fresh `pull_request.opened` event binds on the exact #170 head. (a) alone (close+reopen) will NOT bind until the branch filter admits main; after the fix, the minimal trigger is still close+reopen (this lane re-triggered one on head 6d06eab and it still produced 0 PR runs, confirming the filter is the gate).
- **#179:** needs (b) a `.github` change on **develop** as well; the base-branch filter is the same root cause.
- **#179 / ready_for_review:** NOT additionally required. There is no `on.pull_request.types:` key on main (file:line = workflow line 4-5, `on:` then `pull_request:` then `branches:` — no `types:`). Absence of `types:` means GitHub defaults apply, which for a **non-draft** pull_request include `opened`; #179 as a normal (non-draft) PR already satisfies the default trigger once the branch filter admits main. `ready_for_review` only matters if the PR is a draft (draft `opened` is excluded by default, re-released as `ready_for_review`). Quote for the record: main workflow has no `types:` -> defaults.

## (5) Predicted check name after the minimal correct action
- Check/job that will appear on each head: **`Demo acceptance · changed-path gates`** (the job `name` on the main copy), running the `config-matrix`/`connectivity`/`full-destroy`/`policy`/`reconciliation` acceptance gates at the exact PR head, via job id `430588588` on workflow `.github/workflows/pr-config-matrix.yml`. A later lane should watch for a SUCCESS on that job at the exact PR head.

## PR number
- **PR #181** `w274-0428-251-binddiag` (base `main`, head `lane-0428-250-config-matrix-workway`, sha 6d06eab0ed0cd890ab9f818100ff84698e0347f5, open, unmerged, draft=false). Created for this read-only diagnostic; left open for the Owner. No merge.

## plan-attestation (read-only)
- No plan writes, no AGENTS edits, no evidence written into a product repo.
- Evidence published only to baseharbor-plan (baseharbor-plan is NOT checked here as product; see cleanliness).

## CLEANLINESS
- `git status --short` (own pid zone): only pre-existing untracked `.tools/`, `tests/__pycache__/`, `tests/guided/__pycache__/` — none created by this lane.
- No containers / compose projects started (read-only diagnosis; docker/podman not used).
- No orphaned namespaces/volumes created.
- Zero-mutation: `git ls-remote` head sha identical before/after (6d06eab0ed0cd890ab9f818100ff84698e0347f5).

## END_DONE
The tables, one-line answers, predicted check name (`Demo acceptance · changed-path gates`), PR #181, zero-mutation proof, and cleanliness line are present above. The zero-jobs defect is branch-filtered event gating: `on.pull_request.branches:[develop]` excludes every main-based PR, so no run/zero jobs are ever created on #170/#179.
