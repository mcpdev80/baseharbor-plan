# Independent review of newer #183 findings

## PLAN

1. Read the mission and record the numbered plan in the live board and this evidence file; then verify current Plan main and exact card owner before the first commit.
2. Inspect all PR #183 comments, reviews, and review threads newer than the round-8 evidence.
3. Compare every finding with exact PR #183 head `50eeafac4` and its permitted code/test delta; classify each as fixed, open, or unhelpful.
4. If a blocking finding remains, send the responsible lane a file/line/test recipe and hold the PR; otherwise verify stable exact head, two distinct terminal run IDs, and executed successful required checks.
5. Merge PR #183 normally only if all independent review and exact-head gates pass; otherwise record HOLD and the repair recipe.
6. Publish this evidence through an isolated Plan PR with successful exact-head Plan validation; verify this evidence path on final origin/main and report findings.

## Visible commit identity block

- Exact card owner, verbatim from current Plan origin/main: `owner: w267-0428-284-pridentity`, fetched verbatim from Plan `origin/main` `2305a1b4f4b2fa952f29cb4ca20b04aa67b7417b`.
- Reviewer lane / Git `user.name`: `w267-0428-284-pridentity`.
- Git `user.email`: `w267-0428-284-pridentity@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
- Pre-push author gate: `git show -s --format=%an HEAD` must equal `w267-0428-284-pridentity`.

## Mission-supplied candidate witnesses

- Product PR: https://github.com/mcpdev80/baseharbor-demo/pull/183
- Claimed exact candidate head: `50eeafac4` (full SHA to verify from current remote).
- Prior exact-head qualifier run: `45983229441`, reported completed/success on `50eeafac4`.
- Prior evidence: `evidence/2026-11-27/0428-284/round-8-50eeafac4.md`, reported SHA-256 prefix `9286d6a91` and present on Plan main.
- Claimed predecessor `dc041ca12` is not by itself review evidence; current GitHub findings and exact PR state must be checked independently.

## Planning base attestation

- Planning repository remote line verified before the first evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Exact ref SHA intended for the evidence branch: `2305a1b4f4b2fa952f29cb4ca20b04aa67b7417b` (`git ls-remote origin refs/heads/main`).
- Current task frontmatter owner is `owner: w267-0428-284-pridentity`; this is the canonical identity required for the evidence commit.

## Independent review observations

- Inspection time: 2026-11-27. PR #183 remains OPEN, non-draft, mergeable, base `develop`; current base SHA is `58ac70679efe5f7e95bd47d602841704fb9ffa67`. The exact PR head is `50eeafac4c31d8cf3a2d0533a54ee67637b3327c`, branch `w366-0428-284-democonsent`.
- Fresh stable remote samples before and after source/review inspection both returned the same values:
  - `58ac70679efe5f7e95bd47d602841704fb9ffa67 refs/heads/develop`
  - `50eeafac4c31d8cf3a2d0533a54ee67637b3327c refs/pull/183/head`
- Changed files are only `tests/guided/drive.py` (+98) and `tests/guided/test_consent_capture.py` (+394). No product auth/consent code or workflow files are changed.
- Issue comments on #183: `7209163708` (2026-11-27T03:39:15Z) and `7213692529` (2026-11-27T08:35:00Z), both by `mcpdev80`. The first asked for an independently sourced log tail, a tracked accounted prefix, flush-before-reread, and a deterministic `run_tty` boundary regression while preserving tests 22/23 fail-closed. The second clarified that offset >=4096 and AST shape do not establish final-drain membership because multiple select/read iterations may occur before `proc.poll`; it requested deterministic ordering, an assertion the digest is actually in the final-drain chunk exactly once, and fail-closed controls.
- Both submitted review records (`6083136758`, `6083141278`) refer to older head `83c80c917858e719118bd21e0183b4516959ac53`; the latter is a correction/hold. Neither is an approval for the current head. The PR review-comments endpoint reports 0 inline comments. No review-thread comments are present in the pull review-comment endpoint. There are no newer issue comments than the two listed above.

### Finding 7209163708 — OPEN, blocking

- The helper at `tests/guided/drive.py:285-306` reads the on-disk log from `already_read` and appends the suffix. The `run_tty` main read path at `tests/guided/drive.py:371-385` writes each PTY chunk to the log and appends the same chunk to `capture_buffer`; the final-drain path at `:437-448` does likewise. `bytes_read` advances for those same chunks. The flush/fsync and helper call at `:480-484` are present.
- This implementation has no demonstrated independent writer/source that can put bytes in this log without the same `run_tty` read path also appending those bytes to memory. The helper test (`tests/guided/test_consent_capture.py:744-786`) uses a prewritten file and manually chosen offset; it proves helper suffix/idempotency behavior, not the missing-source runtime condition. Thus the requested source/premise remains unestablished. The current change partially implements the requested helper behavior but does not establish why a production-path log tail could be absent from the capture buffer.
- Disposition: OPEN. It blocks acceptance until a concrete, supported log-only source and a regression that exercises that source are shown, or the finding is independently demonstrated to be inapplicable.

### Finding 7213692529 — OPEN, blocking

- Current `test_25` (`tests/guided/test_consent_capture.py:788-983`) calls `run_capture` twice at `:860-865`. It sets `drive._test_final_drain_hook` only at `:936-937`, after both runs have completed. The production hook read is `drive.py:455-457` and refers to `_run_tty_final_drain_hook`, so the test writes a different variable and too late to observe either run.
- The test never asserts `drained["chunks"]`, nor that a digest-bearing chunk reached final-drain. It asserts digest presence/count and transcript/log equality (`:939-970`), offset, and AST shape (`:945-979`). Those assertions are compatible with the documented main-loop path; the test's own observations at `:799-803` and `:900-909` say the one-run digest is consumed by normal select reads. Therefore the test does not prove the required final-drain branch membership or its exact-once behavior at that boundary.
- Disposition: OPEN. It blocks acceptance.

## Exact-head CI and review gate

- `gh run view 45983229441 --repo mcpdev80/baseharbor-demo --json ...` returned event `workflow_dispatch`, completed/success, exact head `50eeafac4c31d8cf3a2d0533a54ee67637b3327c`. Its executed job `140452168545`, “Guided consent · production-path regressions”, completed/success; setup, checkout, pinned-Core check, test step, post-checkout, and completion all completed successfully.
- The exact-head run census contains only one executed successful run: `45983229441`. Run `45982811090` is a push event on the same SHA but failed with no jobs; it is not a second executed successful run. Earlier failure `45973828049` was on the predecessor head `dc041ca...` and does not qualify. The two-distinct-successful-run condition is NO.
- No workflow was dispatched, rerun, or edited during this review. PR #183 is held OPEN and was not merged because both findings remain blocking and the exact-head two-run condition is not met.

## Repair recipe sent to responsible lane

At 2026-11-27, sent the responsible active implementation lane `w392-0428-284-demo183fix5` the following focused recipe; this review session made no product changes:

- `tests/guided/drive.py`: identify and document a real supported source that can add bytes to the authoritative log without those bytes being consumed into `capture_buffer`; if no such source exists on the supported path, remove the unsupported reconciliation premise rather than asserting a fictional PTY race. Keep flush-before-reread and byte-offset semantics only if the source is real.
- `tests/guided/test_consent_capture.py::test_25_run_tty_final_drain_appends_missing_log_bytes_once`: install the exact production hook variable before the relevant `run_capture`, drive deterministic process/read/poll ordering so the digest is delivered by final-drain, assert the recorded final-drain chunk contains the digest exactly once, and assert no reconciliation duplicate. Ensure the test fails if the final-drain append/accounted-prefix behavior is removed. Preserve tests 22/23 fail-closed.
- Keep changes within the authorized test-only files. Do not edit `.github/**`; the existing Guided consent workflow job must continue to execute this test on its configured trigger. Requalify the resulting exact head in Hosted CI before requesting review again.

## Dispositions

- Finding 7209163708: OPEN, blocking; requested evidence is only partially present.
- Finding 7213692529: OPEN, blocking; current test hook and assertions do not prove branch membership.
- Earlier `ACCEPT` record 6083136758: not applicable to current head; it was superseded by `CHANGES` record 6083141278 on the same old head, then later comments documented corrections still not proven by this candidate.
- Exact-head test run: PASS for one ID (`45983229441`); two successful run IDs: NO.
- Stable remote head: YES, observed unchanged twice at `50eeafac4c31d8cf3a2d0533a54ee67637b3327c`.
- Merge eligibility: NO. No product merge performed.

## Repo-rule compliance

- Read-only product review; no product files edited and no tests run locally.
- No `.github/**` files edited and no workflow_dispatch/rerun triggered by this review.
- Review recipe was routed to the responsible implementation lane; this session did not implement the correction.
- Evidence is confined to the Plan repository.

## END BLOCKED

END BLOCKED w267-0428-284-pridentity: PR #183 held at exact head 50eeafac4; both lead findings remain open and only one successful executed exact-head run exists.
- GraphQL `reviewThreads(first:100)` returned an empty node list. The separate pull review-comments REST endpoint also returned 0.
- Run `45982811090` is `push` / `completed` / `failure` on the exact SHA, workflow `.github/workflows/pr-config-matrix.yml`, with `jobs: []`; it is not a successful second qualifying run.

## Planning validation and provenance

- Isolated Plan worktree branch: `w267-0428-284-demo183-reviewleads`, created from Plan `origin/main` SHA `2305a1b4f4b2fa952f29cb4ca20b04aa67b7417b`.
- Fresh `git fetch origin main` kept `origin/main` at `2305a1b4f4b2fa952f29cb4ca20b04aa67b7417b`; `git merge-base --is-ancestor origin/main HEAD` exited 0 before commit.
- `python3 scripts/plan.py render` completed. `python3 scripts/plan.py check` reported `784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings`. Warnings are the existing accepted-dependency warnings shown by the command.
- No test command was run locally. The product verification source is Hosted run `45983229441` only; it is insufficient for merge as recorded above.

## Commit identity witnesses

- First evidence commit identity line, captured before the next commit: `79bb2d0 an=w267-0428-284-pridentity cn=w267-0428-284-pridentity`.
- Mechanical check for first evidence commit: `git show -s --format=%H%n%an%n%cn HEAD` returned `79bb2d0692fa51d3e066cb059bdef999b22e8ea1`, author `w267-0428-284-pridentity`, committer `w267-0428-284-pridentity`.

- Before publication, Plan `origin/main` advanced from the branch-cut SHA to `f77e9c5ab6bd1e196ba246f92d0c4b20b7f76c70`. This is a normal fast-forward update of Plan main, not a product candidate; I rebased only my two unpublished evidence commits onto that fetched current Plan main. Current-base ancestry and the one-path diff are recorded after rebase below.
- Current Plan base verification: `git merge-base --is-ancestor origin/main HEAD` exited 0; `git diff origin/main...HEAD --name-only` returned only `evidence/2026-11-27/0428-284/demo183-reviewleads.md`; `git log --oneline origin/main..HEAD` returned only `fd4beaf79 docs: add Plan commit identity witness` and `58424ab57 docs: record independent review of demo PR 183` before this final evidence amendment.

## Plan PR publication

- Evidence PR: https://github.com/mcpdev80/baseharbor-plan/pull/230
- Initial Plan validation run `46005287338` completed successfully on evidence PR head `cb4da0cded903abec7d3ca23788e64a0ac25cf35`; the evidence update below will trigger a fresh validation for the updated exact head before the Plan PR is merged.
- Remote branch delivery witness after push: `cb4da0cded903abec7d3ca23788e64a0ac25cf35 refs/heads/w267-0428-284-demo183-reviewleads`.
