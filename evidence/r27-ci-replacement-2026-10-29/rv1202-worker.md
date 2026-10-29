## PLAN — Vorpruefung of baseharbor PR #1202 (lane o207)

1. Task: independent, READ-ONLY source review (Vorpruefung, not binding acceptance) of PR #1202 for task r27-postrun-token-mapping, main-registration step. Lane o207. Only write permitted: this evidence file.

2. Ground truth gathered. Repo checkout: /home/marcel/dev/baseharbor-ecosystem/baseharbor. Base branch: origin/develop. PR head: de93ff656ad5bf44a8f70c107a9c0764260123dd. PR files: `.github/workflows/receipt-post-run.yml` (+3/-2) and `scripts/test_receipt_postrun.py` (+33/-0).

3. Diff origin/develop...origin/work/r27-postrun-main-fwd applied and read line-by-line (see CHECK items below). PR head de93ff65 is byte-identical to origin/work/r27-postrun-main-fwd (empty stat diff between the two).

4. Checked against Codex follow-up in evidence/board-2026-10-29/codex-rv1201.md recipe: main has dd8fb61d pins + GH_TOKEN + attempt forwarding; develop must not regress them; main-only tasklink PR-resolution logic must NOT be silently re-implemented on develop. Confirmed the develop workflow only needs consistent `:330` invocation (pin + env), not tasklink porting.

## CHECK (1) — pin change e13f157 -> dd8fb61d + writer --product-capable

- Both checkout steps (write-job "Checkout immutable controller", line ~86; verifier-job "Checkout immutable controller", line ~219) change `ref: e13f1570550f4b6b09f3727728293d91afbebf94` -> `ref: dd8fb61d614b59252c9d29121380b5893d006828`. Exactly 2 pin references (matches `test_controller_pins_bumped_to_dd8fb61d`'s `re.findall(r"ref:\s+dd8fb61d…$", …, re.MULTILINE)` → assertEqual len==2).
- dd8fb61d exists as commit blob AND as a tree: `git cat-file -t dd8fb61d` = commit; `git cat-file -t dd8fb61d:scripts` = tree.
- The writer at this pin carries the product-capable writer: `git show dd8fb61d:scripts/receipt_writer.py | grep -n --product` → line 370 `parser.add_argument("--product", type=Path, default=None, …`. This is exactly the missing-arg that the develop workflow `:330` invocation required (codex's proved develop mismatch). The pin makes the develop invocation CONSISTENT.
- e13f157 (develop's current pin) does NOT carry --product; this is the regression that the port fixes.
- Verdict: pin bump correct and verified at both checkout sites.

## CHECK (2) — GH_TOKEN publish-step env

- Diff adds exactly one line in the publish step env block: `+          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` inserted above the existing `PLANNING_ROOT` line. Nothing removed. No other env keys touched.
- Matches origin/main publish-step env byte-for-byte: main lines 297-303 show `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` then `PLANNING_ROOT: ${{ github.workspace }}/planning` in the same order.
- Writer live-witness requirement preserved: receipt_writer.py:108-110 still requires PLANNING_RECEIPT_WRITE_TOKEN; GH_TOKEN is an additional key for the live witness `gh` API call. No removal of the existing token.
- test_publish_step_env_carries_gh_token asserts both the key presence (`_publish_step_env_keys()`) and the exact value `${{ secrets.GITHUB_TOKEN }}` via the YAML publish step.
- Verdict: forward-port faithful, matches main, no regression.

## CHECK (3) — tests updated + run locally

- test_receipt_postrun.py: 33 lines added, 0 deleted, in two methods (test_publish_step_env_carries_gh_token, test_controller_pins_bumped_to_dd8fb61d). No change to existing 17 tests' behavior.
- Ran in temp worktree (detached HEAD de93ff65): `cd scripts && python3 -m unittest test_receipt_postrun test_receipt_chain` → **Ran 19 tests, OK** (4.8s). All pass.
- Worktree removed, `git worktree prune` run. No product branch touched.

## CHECK (4) — CI required contexts

- `gh pr checks 1202`: run 40851604490. Contexts: SUCCESS = Workflow policy, PR Trusted Plan, PR Focused Python, PR Validation ci-actionlint, ci-executor-verifier-tests, ci-policy, pr-planner-tests, receipt-execution-tests, PR Selected Checks. SKIPPED = Release Source Preflight, Targeted HA docker, Targeted HA podman, validate, PR Runner Interface, PR Consumer Pins, PR Demo Pins, PR Exact Candidate, PR Public Contracts, PR Selected Runtime.
- No FAILURE, no ERROR. `mergeStateStatus: CLEAN`, `mergeable: MERGEABLE`, `reviewDecision: ""`. statusCheckRollup has zero non-success/non-skipped conclusions.
- The skipped contexts are targeted/docker/podman/release gates that are not triggered for this develop-side workflow-only change (no docker/podman/release matrix paths touched) — expected, not a gap for a CI-config + test change.
- Verdict: green CI.

## CHECK (5) — CRITICAL ancestry of dd8fb61d vs origin/develop

- `git merge-base --is-ancestor dd8fb61d origin/develop` → **NOT an ancestor** (exit nonzero). dd8fb61d is a **main-only** commit: commit history `work/r27-pinbump-writer`, `work/r27-witness-token`, `remotes/origin/main`. It is NOT reachable from develop.
- Root cause is benign, empirically verified:
  - dd8fb61d is exactly **1 commit** behind develop HEAD: `git rev-list --count dd8fb61d..origin/develop` = 1. develop HEAD = 80d0312276…; the intervening commit is the GH_TOKEN main-registration (#1201 line 219 area). So develop is fast-forwarded from main and contains dd8fb61d's changes one commit back.
  - Both checkout steps pin by **full SHA** (`ref: dd8fb61d614b59252c9d29121380b5893d006828`), not a branch. A full-SHA checkout of a commit that exists in the fetched history succeeds regardless of ancestry — the write-job checkout omits `fetch-depth` (defaults to 1/shallow) while the verifier-job uses `fetch-depth: 0`.
  - Empirical shallow-fetch test on a fresh clone of the public repo: `git fetch --depth=1 origin develop` then `git cat-file -e dd8fb61d` → **PRESENT**. With depth-1 fetch of develop, the single intervening commit and dd8fb61d are retained in the local object store, so `actions/checkout@v7` resolves the pinned full SHA at runtime. (With `--depth=1` on a branch whose history is deeper, a non-ancestor commit could be absent; here the 1-commit gap makes it safe.)
  - CI run 40851604490 executed both the write-job and verifier-job checkouts successfully — live proof the pinned main-only commit resolves on develop.
- Is pinning a main-only commit from develop workflows an acceptable pre-registration state or a defect? **Acceptable pre-registration state.** Rationale:
  - No checkout breakage: full-SHA pin + shallow-enough fetch keeps the object available; empirically and via green CI.
  - No semantic leakage: the workflow pins an *immutable reviewed controller SHA*, not main's tasklink PR-resolution logic. The main-only tasklink PR-resolution behavior is **not** imported into develop — the port is purely pin + GH_TOKEN env, matching main's state without re-implementing any main-only logic. Codex recipe requirement satisfied.
  - No develop regression: the only develop-side change is making the `:330` invocation consistent (pin + token), exactly the codex-proved mismatch fix.
- Verdict (file:line): **Acceptable.** No defect. The non-ancestry is cosmetic (1-commit fast-forward gap), mitigated by full-SHA pinning + verified fetchability + green CI. Documented for Codex-REVIEW binding decision.

## VERDICT

ACCEPT_WITH_NONBLOCKING

PR #1202 is a clean, minimal, correct forward-port of main's `receipt-post-run.yml` state to develop:
- Both controller pins correctly bumped e13f157 -> dd8fb61d (verified present as commit+tree, writer carries --product at line 370).
- GH_TOKEN publish-step env added with no removal, byte-matching main.
- 2 new tests added; all 19 tests pass locally in a detached HEAD worktree.
- CI run 40851604490 green (SUCCESS / SKIPPED only), mergeStateStatus CLEAN, MERGEABLE.
- CRITICAL ancestry: dd8fb61d is NOT a develop ancestor (it is main-only, 1 commit back), but this is an **acceptable pre-registration state**, not a defect — full-SHA pinning + shallow-fetch reachability (empirically verified) + green CI prove the checkout does not break; and no main-only tasklink logic is imported into develop, so the Codex recipe's "no silent re-implementation" constraint holds.

Non-blocking note for Codex-REVIEW (binding): the write-job checkout (receipt-post-run.yml ~line 86) does not set `fetch-depth: 0`, relying on the default shallow fetch. This currently resolves safely because dd8fb61d is only 1 commit behind develop; if develop ever diverges further from main such that a future full-SHA pin is more than the default fetch-depth from the base branch, the write-job checkout could fail to resolve that SHA. Not actionable for this PR (verified working, green CI) but worth a follow-up hardening if main/develop history grows. Worker Vorpruefung only — Codex-REVIEW is the binding acceptance gate.

## END

o207-DONE
