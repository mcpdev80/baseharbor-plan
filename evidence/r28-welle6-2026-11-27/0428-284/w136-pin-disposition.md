# #1842 Demo pin target disposition

## PLAN

1. Read the assigned mission, inspect the live todo board, verify the planning remote, and inspect the #1842 gate resolver and runtime checkout semantics.
2. Check the w198 census inbox and compare the supplied Demo commits and branch ancestry.
3. Decide the exact v0.4.28 pin and state the hosted qualification sequence plus release-main limitation.
4. Publish this decision record to baseharbor-plan origin/main and tick the board step.
5. Post the required Codeman completion status.

## Review identity and publication

- Governing card: `t-20261125-0428-284-1812-postretry-gate-failure`; frontmatter `owner` read from fetched plan `origin/main`: `w177-0428-284-demo-pin-1812`.
- Current recovery-transfer direction in that task record assigns future #1842/#1812 candidate commits to `w198-0428-284-demo-parser`; the mission also explicitly requires `%an` to equal that exact string. This governs the candidate pin commit, not this reviewer evidence commit.
- Evidence lane identity: `w136-pr1836-rowsreview`; `git user.name=w136-pr1836-rowsreview`; `git user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Evidence commit invocation: `git -c user.name=w136-pr1836-rowsreview -c user.email=w136-pr1836-rowsreview@baseharbor.local commit -m 'docs(evidence): disposition 1842 demo pin target'`.
- Pre-push author gate: `git show -s --format=%an HEAD` must print `w136-pr1836-rowsreview`.
- Planning remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.
- Isolated worktree base attestation: fetched `origin/main` at `9bfb496aba9190f81d913b9c4b7235b3dd627d1b`; this is the commit from which this evidence worktree was created.

## Decision

Set `docs/releases/v0.4.28.demo-ref` to `5ca92a7cd2f746934890cfd7096a48068bdf218e` (one full lowercase SHA plus newline). Keep the pin-advance candidate limited to that one file. This is the current Demo develop tip and is a descendant of reviewed Demo merge `1a3c055cc0eef3f961722f12d843e33f6c1ca43e` by three commits; it is also six commits ahead of the previous pin `b41127723e523134a1c14ee3c36cf133237162ce`.

Do not target Demo main tip `6381a67f58e067358ef54dce7f4cff2106f8a623`: the comparison says it diverges from `1a3c055`, and it does not contain that reviewed merge. The existing `b4112772` pin is a no-op and does not advance the approved source.

## Gate semantics proof

- `scripts/pr-gate-plan.py:1182-1184` recognizes both `docs/releases/v0.4.27.demo-ref` and `docs/releases/v0.4.28.demo-ref`, selecting `demo-source-pin-validation`; lines 1185-1186 still contain stale `.27` wording.
- The selected validator route is declared in `scripts/pr-gate-plan.py:789-794`.
- `scripts/pr-check-runner.py:383-398` currently hard-codes `docs/releases/v0.4.27.demo-ref`. Therefore a green PR-selected `demo-source-pin-validation` does not itself prove the `.28` file value. Treat that selected check as insufficient exact-file evidence; the separate tag-aware pre-release source validation below must validate `.28`.
- `.github/workflows/pre-release.yml:175-194` loads `docs/releases/${tag}.demo-ref`, validates a full SHA, and requires a supplied `demo_ref` to equal that file. The pin-specific dispatch must use `tag=v0.4.28` and `demo_ref=5ca92a7cd2f746934890cfd7096a48068bdf218e`.
- `.github/workflows/pre-release.yml:726-729` and `755-758` pass the resolved `demo_ref` into both Docker and Podman Light matrices. `.github/workflows/pre-release-runtime-suite.yml:203-216` clones the Demo repository, fetches the supplied full SHA directly, checks it out detached, and asserts exact SHA equality. This is any fetchable repository commit; the Light jobs do not require the SHA to be a branch tip or an ancestor of `main`.
- The exact hosted dispatch must prove each of the 14 required Light gate entries actually executed and passed. Reused-only or skipped entries do not count as execution proof.
- This makes Demo `main` absence non-blocking for hosted gate checkout. It remains a separate release-readiness condition: `docs/internal/pre-release-documentation-audit.md:157-159` requires Demo `main` to contain the intended test implementation before the final BaseHarbor pre-release run. The pin and Hosted qualification do not satisfy that release-audit condition.

## Exact candidate and qualification

- Candidate edit: change only `docs/releases/v0.4.28.demo-ref` to `5ca92a7cd2f746934890cfd7096a48068bdf218e` plus newline. No `.github/**` or product changes are part of this disposition.
- Candidate commit author gate: every new candidate commit must have `.commit.author.name == w198-0428-284-demo-parser`; verify mechanically with `git show -s --format=%an HEAD` before push.
- On the resulting exact candidate SHA, collect two distinct full `pull_request` run IDs, each terminal success with required PR checks executed. A dispatch run is a separate evidence kind and cannot substitute for either PR event.
- Separately run the authorized `pre-release.yml` workflow_dispatch against that same Core candidate SHA, `tag=v0.4.28`, and explicit `demo_ref=5ca92a7cd2f746934890cfd7096a48068bdf218e`. Require terminal success and execution/pass evidence for all 14 Docker/Podman Light gate entries; skipped or reused-only entries are nonqualifying.
- Reconfirm the exact pin file, candidate SHA, candidate author, run event types, run heads, and all gate-level execution outcomes before acceptance.

## Evidence and inbox

- Demo compare `1a3c055...5ca92a7`: status `ahead`, ahead_by 3, behind_by 0, merge base `1a3c055...`.
- Demo compare `b411277...5ca92a7`: status `ahead`, ahead_by 6, behind_by 0, merge base `b411277...`.
- Demo compare `6381a67...5ca92a7`: status `diverged`, ahead_by 13, behind_by 8; this establishes non-ancestry to main, not inability to fetch the exact commit.
- Codeman inbox was empty at review time (`pending=0`, `unseen=0`); no w198 census had arrived. Decision is based on the mission facts and direct workflow/source inspection.
- No product file, workflow file, PR, or remote runtime was modified or triggered by this disposition.

## Result

END w136-pr1836-rowsreview DONE — #1842 target is Demo develop tip `5ca92a7cd2f746934890cfd7096a48068bdf218e`; Hosted gates can fetch it by SHA despite its absence from Demo main. The final release audit still requires intended implementation on Demo main.
