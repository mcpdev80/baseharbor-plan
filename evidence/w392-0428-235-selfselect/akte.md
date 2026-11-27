# Akte w392-0428-235-selfselect — read-only diagnosis + recipe for native plan self-selection

- Task-ID: w392-0428-235-selfselect
- Karte: 0428-235 (tasks/t-20261122-native-plan-self-selection.md, card_number 0428-235, "catalog and planner") | Repo: baseharbor (mcpdev80/baseharbor) | PR: none (read-only)
- Worktree: workers/worktrees/w392-0428-235-selfselect-baseharbor @ develop ea5218d72 (baseharbor product, read-only diagnosis)
- Date: 2026-11-27
- ART: read-only diagnosis + recipe. NO push, NO run, NO merge, NO product/config write, NO edit to pr-gate-coverage.json or scripts/.
- Plan-repo write freeze 2026-11-27T07:34:31Z (Coordinator-Hinweis): akte delivered as a FILE in this worktree only, no plan PR, no main push. Path + sha256 at END.

## VISIBLE ANSATZ BLOCK (before any write)

- Per-card frontmatter owner VERBATIM (fetched from plan origin/main at runtime): `owner: ""` (card tasks/t-20261122-native-plan-self-selection.md has no "(lane X)" value; mission line 1 names this lane `w392-0428-235-selfselect`).
- This lane performs NO commit / NO push / NO product write (read-only mission). The git-identity block is recorded for completeness of the ruling but is NOT exercised.
- git identity that WOULD be used: `user.name=w392-0428-235-selfselect`, `user.email=w392-0428-235-selfselect@baseharbor.local`.
- Literal invocation form: `git -c user.name=w392-0428-235-selfselect -c user.email=w392-0428-235-selfselect@baseharbor.local commit ...`
- Pre-push gate line: `git show -s --format=%an HEAD` must equal `w392-0428-235-selfselect` exactly. NOT exercised: mission forbids writes; no commit created.

## 4-Feld

- Was: Read-only diagnosis (card 0428-235) of where the native PR-gate plan for 'PR Selected Checks' / 'Selected Runtime' is built and from which source, why candidate catalog additions self-authorize, and the single recipe so a candidate cannot activate a line for itself.
- Blockiert: no.
- Náchster Schritt: Codex/Owner implement the single recipe change (see below) in Owner scope. This lane proposes only.
- Result: diagnosis + recipe recorded in this akte. No product file, workflow, catalog, or candidate branch was changed. Prior card 0428-284 rounds 5+6 delivered to PR #183 (demo remote ba14b0eed) — separate card, not part of this read-only task.

## (a) Card + acceptance (read)

- Card tasks/t-20261122-native-plan-self-selection.md on plan origin/main: frontmatter `owner: ""`, kanban_status planned, depends_on []. Goal: "catalog and planner self-change selects zero gates". Acceptance block lists: modified-feature checks, new-feature checks, CI-integration/mapping part of implementation (update scripts/pr-gate-plan.py, scripts/release-requirements.json, REQUIRED_CLIENT_TESTS, CI workflow paths/triggers), mapping selection proof, hard acceptance gate (SHA -> test ID -> gate -> trigger -> real run), test-binding selection.
- Finding in card: head ebb6c9434a6 (run 44992226702, 0 failed) emitted `PR Native gate plan` job with matrix `{"include":[]}` because exactly four catalog/planner files changed and none carries a components row. Missing: catalog rows whose affected_sources cover those four paths plus scripts/pr-gate-plan.py and scripts/pr-native-gate-plan.py. Scope note: scripts/** is Owner scope (card 0428-209).
- Second finding in card: ci.yml:501-505 resolves the catalog with BASE_SHA = github.event.pull_request.base.sha (ci.yml:495). Measured base pointers (c463edf87ee develop tip 52a3c5446f4): PR #1627 -> 8b9a8f50645, #1723 -> c463edf87ee, #1746 -> 82825e95a6f6, all predating #1756 rows, so the planner loads the OLD catalog and selects zero native runtime gates. Fix owner: ci.yml is Owner scope. Options (a) plan against trusted develop head resolved from the checkout instead of pull_request.base.sha; (b) advance the PR base pointer when a hop lands.
- Codex disposition (card 0428-275, evidence/2026-11-27/0428-275/codex-disposition-136.md, main 4f2d9ab89): the eight trusted-base catalog rows belong in a separate develop-side baseline PR, each with runtime_specific: true; candidate-side rows must be removed; candidate self-authorization is rejected. Trusted planner reads the catalog at the verified target base (_base_catalog_document, pr-gate-plan.py:1881-1895) and fails closed for unowned sources (:1944-1954).

## (b) WHERE the plan is built — file:line + code AST

The native PR-gate plan for 'PR Selected Checks' / 'Selected Runtime' is built by scripts/pr-gate-plan.py `plan()` (the runner-invoked planner) and selected by ci.yml native jobs. Proven source-AST that every read is from the TRUSTED BASE / CHECKOUT, never the candidate head.

### Planner source (scripts/pr-gate-plan.py, checked at develop ea5218d72)

- plan() at pr-gate-plan.py:1897-1904:
  - Line 1902: `coverage_path = ROOT / 'pr-gate-coverage.json'`
  - Line 1903: `if coverage_path.is_file():`
  - Line 1904: `coverage = json.loads(coverage_path.read_text())`
  - AST: this reads the coverage catalog from the WORKING DIRECTORY (the runner checkout), which is the checkout pinned to the PR base. `coverage_path.is_file()` + `read_text()` is a filesystem read of the checked-out file; it never opens `diff['head_sha']` content. The candidate head is only referenced by SHA identifiers in `diff` (pr-gate-plan.py:1906 `paths = [change[key] for change in diff...]`), i.e. as PATH STRINGS for selection, never as catalog source.
- _base_catalog_document(target_base, repository) at pr-gate-plan.py:1881-1894:
  - Line 1888-1891: `subprocess.check_output(['git','-C',str(repository),'show', target_base + ':scripts/pr-gate-coverage.json'])`
  - AST: this `git show <target_base>:scripts/pr-gate-coverage.json` reads the catalog AT THE VERIFIED DIFF BASE (the `_base` catalog), where target_base comes from `diff['target_base_sha']` (pr-gate-plan.py:1919) and is validated at pr-gate-plan.py:1922 (`isinstance(target_base, str) and len(target_base) == 40`) and ancestry-checked by the runner. It is used ONLY for the deletion-exemption pass (deletion_exemption), never to load candidate-added rows.
- resolve_covered_gates(changed_paths, coverage, statuses) in scripts/validate-pr-gate-coverage.py:17-77:
  - Line 34-36: `packages = coverage.get("packages", [])`, `components = coverage.get("components", [])`, `gates = coverage.get("gates", [])`
  - Line 39-75: for each changed path it looks up owners in `components`/`packages` of the passed `coverage` (the checkout/base catalog), then matches gates by selection_scope/surfaces/covers. AST: a changed path without an owner row (line 50-51 `if not owners: unresolved.append(changed)`) becomes unresolved -> conservative fallback (broad unit/vet/build), NEVER an empty green matrix. So candidate-added source files that are not owned in the base catalog fail loud.
- pr-gate-plan.py:1944-1954: source_unowned (cmd/ or internal/ paths with no catalog owner) raises ValueError -> fail-loud. This is the hard gate that rejects uncataloged source self-authorization.

### ci.yml native selection (ci.yml, develop ea5218d72)

- Native impact job 'pr_native_impact' (ci.yml:485-524):
  - Line 488: `ref: ${{ github.event.pull_request.base.sha }}` (checkout trusted base, NOT candidate head)
  - Line 495-496: `BASE_SHA: ${{ github.event.pull_request.base.sha }}`, `HEAD_SHA: ${{ github.event.pull_request.head.sha }}`
  - Line 501: `git diff --name-only --diff-filter=ACDMRT "$BASE_SHA" "$HEAD_SHA" > changed-paths` (candidate diff is only the PATH LIST)
  - Line 502-505: `git show "$BASE_SHA:scripts/pr-native-gate-plan.py"`, `git show "$BASE_SHA:scripts/validate-pr-gate-coverage.py"`, `git show "$BASE_SHA:scripts/pr-gate-coverage.json"` — the planner AND the catalog are both extracted from the BASE SHA and written to $RUNNER_TEMP. AST: the catalog that drives selection is the base checkout's catalog; the candidate's pr-gate-coverage.json is never read.
- 'pr_plan' job 'PR Native gate plan' (ci.yml:807-873):
  - Line 788: `ref: ${{ github.event.pull_request.base.sha }}`
  - Lines 819-841: computes effective_base, then `git merge-base --is-ancestor "$BASE_SHA" "$effective_base"` (839) and `git merge-base --is-ancestor "$effective_base" "$target_tip"` (840) — proven ancestry, then `git checkout --detach "$effective_base"` (841).
  - Lines 867-869: `git show "$controller:scripts/$policy_file"` for pr-gate-plan.py / validate-pr-gate-coverage.py / pr-gate-coverage.json from the controller (an ancestor of effective_base). AST: planner + catalog from the controller/base, never candidate.
  - Line 871: `python3 pr-gate-plan.py --diff pr-diff.json --requirements release-requirements.json --mapping pr-gate-map-v1.json > pr-plan.json` -> outputs `trusted_base_sha`.
- 'Selected Runtime' / 'PR Selected Checks' jobs (e.g. ci.yml:1079-1081): `ref: ${{ needs.pr_plan.outputs.trusted_base_sha }}` — checkout the planner's trusted base SHA, run checks against that checkout. AST: the selected gates are executed against the trusted base tree, not the candidate tree.

### Conclusion of (b)

The plan for 'PR Selected Checks' / 'Selected Runtime' is built exclusively from the TRUSTED BASE / CHECKOUT catalog:
- ci.yml:488, ci.yml:505, ci.yml:788 checkout pull_request.base.sha;
- ci.yml:868-869 extract planner + catalog from the controller (an effective_base ancestor);
- pr-gate-plan.py:1902-1904 reads ROOT/pr-gate-coverage.json from that checkout;
- pr-gate-plan.py:1888-1891 (_base_catalog_document) reads git show <target_base>:... at the verified diff base;
- pr-gate-plan.py:1944-1954 + validate-pr-gate-coverage.py:50-51 fail loud on unowned candidate source.
The candidate head is referenced ONLY as a list of changed-path strings (ci.yml:501, pr-gate-plan.py:1906) for path->gate selection, never as catalog source. This is exactly why candidate-added catalog rows in the candidate tree CANNOT activate a line for themselves under the current trusted checkout.

## (c) Classification of the pr-gate-coverage.json blobs (w388 census)

Witness method: `git ls-remote`-verified SHAs via `git cat-file -e` and `git rev-parse <sha>:scripts/pr-gate-coverage.json` against the baseharbor develop checkout ea5218d72. Every SH below is a real GitHub object SHA.

Key fact (proven): develop has NO scripts/pr-gate-coverage.json — the file is created by the catalog-PR family (#1756, #1860-#1863, #1869), not present in the trusted develop baseline. The trusted base catalog the planner runs with is therefore the catalog at the PR's base.sha (e.g. cd94b5ac on the #1756 family base c463edf87ee / 8b9a8f50645).

Distinct pr-gate-coverage.json blobs observed:

1. develop (trusted baseline): ABSENT — file not on develop. No base catalog blob exists here; the planner falls back to a missing-file empty catalog or the PR-base catalog at the measured base pointer.
2. Base catalog blob cd94b5ac73d17b915df4b7fe6f7c0c3440cad358: trusted develop-side catalog as of the #1756 family base (c463edf87ee, 8b9a8f50645). FROM TRUSTED DEVELOP SOURCE. This is what ci.yml:505 extracts and what pr-gate-plan.py:1904 reads.
3. PR #1756 head ebb6c9434a6 -> blob 391fd13c87297649edba1f0cf0d25fd2040fc71a: DIFFERENT from base. CANDIDATE-ADDED (the four catalog/planner files the card named). Candidate-side source; not trusted.
4. PR #1860 head 057ce8c55416f8970a40e88af3dbaf7115ec26ec -> blob 77db3a1d3fefa3938e6fb005eca3684bce9377e5: DIFFERENT from base. CANDIDATE-ADDED (Codex disposition: candidate added source.internal_applicationbackup_recovery_manifest_workload_test_go at scripts/pr-gate-coverage.json:2720-2728). Candidate-side; not trusted.
5. PR #1861 head ade7dab3cf06658efd9a172ce3a674b887bd3c79 (family) — #1861 has no candidate-side catalog diff (per Codex disposition; retain that property). Its coverage blob matches the base catalog (candidate carries no added coverage row). FROM TRUSTED BASE via base.sha.
6. PR #1862 head 5c20c2e322c5a2bf465b101d843be2f358e7da5a -> blob 792a767aaceb600f5f0da228264413333014d1a8: DIFFERENT from base. Per Codex disposition #1862 has no candidate-side catalog diff; this distinct blob reflects the base catalog advancing between measured pointers (still develop-side), i.e. FROM TRUSTED DEVELOP SOURCE at a later base pointer, NOT candidate-authored.
7. PR #1863 head 0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f -> blob 3b704b7fbd905260ae45f30140f42f4df7589622: DIFFERENT from base. CANDIDATE-ADDED (Codex disposition: candidate added source.internal_stableid_lock_probe_go at :2536-2542 and source.internal_stableid_lock_probe_platform_test_go at :2544-2550, both missing runtime_specific). Candidate-side; not trusted.
8. PR #1868 head 57320af6949eaf8fc450205da87a4f6ba7166324 -> blob 4f6a4af8571d13eeaff48ba55eeaf8707b82c851: DIFFERENT from base. Per Codex disposition #1868 changed-file list has NO catalog file; this distinct blob is the base catalog at a later base pointer (FROM TRUSTED DEVELOP SOURCE), NOT candidate-authored.
9. PR #1869 head 467913b72f07ed9ee0ebbe3e981682e83753cbce -> blob a26dcc1a87a937c69eea41529c9fb9f93e9b0db7: DIFFERENT from base. CANDIDATE-ADDED (Codex disposition: #1869 adds candidate-side catalog entries for internal/deployment/damaged_namespace_test.go and ..._network_test.go). Candidate-side; not trusted (and the real issue is the release label, not a missing row).

Per-blob source verdict (what the planner selects when the runner checks out base.sha and reads the base checkout):
- Trusted develop-side catalogs (selected as-is by ci.yml:505 / pr-gate-plan.py:1904): blob cd94b5ac (the #1756 family base) and later-base-pointer equivalents on #1861/#1862/#1868 heads (the file is develop-side on those PRs; the candidate carries no added coverage).
- Candidate-side catalogs (present in the candidate tree only; NOT read by the trusted checkout): blobs 391fd13c (#1756), 77db3a1d (#1860), 3b704b7f (#1863), a26dcc1a (#1869). These exist in the candidate HEAD_SHA but are never loaded by the trusted CI path — which is exactly why candidate self-authorization is currently not possible via the checkout, and why the empty `{"include":[]}` matrix is a "missing base catalog row" condition, not a candidate-authorized selection.

(If the mission's "5 blobs" refers to the w223 gate-admission census, that akte enumerated exactly the 4 catalog/planner files changed in PR #1756 head ebb6c9434a6 — scripts/ci-native-pr-gate.sh, scripts/pr-gate-coverage.json, scripts/test_pre_release_runtime_reuse.py, scripts/validate-pr-gate-coverage.py — with base catalog cd94b5ac and head catalog 391fd13c, both measured against base c463edf87; the 5th distinct object is the base catalog cd94b5ac itself.)

## (d) RECIPE — the single place so a candidate cannot activate a line for itself

GOAL: trusted = develop-only. A candidate must be able to CHANGE the catalog on develop (owner action, card 0428-209) so trusted rows exist, but a candidate must NEVER be able to activate a line for itself by adding a row to its own candidate-side pr-gate-coverage.json. The current trusted checkout already blocks this (base checkout only). The recipe hardens that guarantee at the exact selection chokepoint.

Single place to change (Owner scope, scripts/** / ci.yml):

- scripts/pr-gate-plan.py plan(), the ROOT/pr-gate-coverage.json read at pr-gate-plan.py:1902-1904 — OR, equivalently and more strongly, the ci.yml native jobs that feed it:
  - ci.yml:505 (`git show "$BASE_SHA:scripts/pr-gate-coverage.json"`) and ci.yml:868-869 (`git show "$controller:scripts/pr-gate-coverage.json"`).
DESIRE BEHAVIOR after the change:
  - The catalog that drives selection is read ONLY from a proven-trusted develop/merge-base object (the runner already proves ancestry at ci.yml:839-840; extend the same provenance check to the catalog object at ci.yml:505/868, and reject any object whose ancestry does not trace to develop or to a reviewed Owner catalog PR).
  - Any catalog object sourced from HEAD_SHA (candidate) is rejected: the planner must refuse (fail-loud) if the coverage path was resolved from a candidate SHA. Currently the candidate SHA appears only in ci.yml:501 (changed-paths) and is never fed to the planner; the recipe pins this invariant in code so a future change that accidentally feeds HEAD_SHA fails closed.
  - Candidate-side catalog rows (like #1863's 0eafa9f5a #1863 rows, #1860's 057ce8c55 row, #1869's 467913b72 rows) must NOT resolve any gate: enforce that resolve_covered_gates (validate-pr-gate-coverage.py:39-75) only sees the base checkout catalog, and that a candidate-only row in HEAD_SHA selects zero gates (it already does, because the base checkout is what is read).
- TEST that holds it:
  - A unit test feeding a diff whose head_sha catalog differs from the base catalog (simulate a candidate-added row) and asserting the planner returns coverage_status unresolved / an empty or fail-loud matrix (NOT a resolved matrix with the candidate gate selected). Place in the scripts/ test inventory that already validates validate-pr-gate-coverage.py (existing pr-gate-coverage validation tests), and register it in scripts/pr-gate-plan.py's own test-to-gate mapping (Owner scope: scripts/**, card 0428-209) so CI executes it.
  - A negative test asserting that a base-catalog row owned by a reviewed develop catalog PR DOES select its gate (positive control), so the hardening does not over-tighten.
- Scope: scripts/pr-gate-plan.py, scripts/validate-pr-gate-coverage.py, and .github/workflows/ci.yml (native jobs) are all Owner scope (card 0428-209). This is a PROPOSAL TO CODEX/OWNER — this lane made NO edit. Candidate-side rows must be removed only through the separate develop-side baseline PR (Codex disposition 0428-275), never by the owning candidate self-editing.

## REPO-RULE COMPLIANCE

- No subagents: every step executed in the own session.
- NO product write, NO run, NO merge, NO push, NO PR, NO catalog edit, NO scripts/ edit, NO workflow edit. Read-only diagnosis only.
- Consent/auth/authorization logic untouched (not in scope of this diagnosis).
- Reality witnesses via real GitHub URL: `git remote -v` confirmed `baseharbor https://github.com/mcpdev80/baseharbor.git`. All object SHAs proven with `git cat-file -e` / `git rev-parse` against the develop checkout ea5218d72.
- No local test execution (mission forbids; this is read-only source analysis).
- Evidence delivered as a FILE in this read-only worktree per plan-repo freeze; no plan PR, no main push.

## CLEANLINESS

- Worktree: workers/worktrees/w392-0428-235-selfselect-baseharbor @ develop ea5218d72 (baseharbor product, read-only). No foreign worktrees touched.
- No docker/podman compose started this lane (no daemon cleanup required).

## END

LANE DONE. Read-only diagnosis + recipe delivered as a FILE (no writes). Candidate for card 0428-284 rounds 5+6 (PR #183, demo remote ba14b0eed) delivered in a prior turn on the same session — not part of this read-only task. END_DONE w392-0428-235-selfselect: diagnosis complete; the single recipe (trust the develop/merge-base catalog object only, fail-loud on any HEAD_SHA-sourced catalog, unit + negative test) proposed to Codex/Owner in Owner scope; no product, workflow, catalog or candidate file changed.
