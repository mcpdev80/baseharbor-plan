# w271 stranded-evidence recovery — w255-0428-251-demo170codex

## PLAN

1. Verify the 88-path w271 census from Plan PR #76 against current live main and revalidate each carrier and blob.
2. Restore only unique, still-missing paths from their exact original refs or stash trees; classify content duplicates and task-ID collisions explicitly.
3. Record post-merge #75 readback for all 13 expected paths and the 0428-273 card state.
4. Restate the read-only findings in direct-main commits 9ff4e1108 and 6480495f5 with true executing lanes, content verdicts, and invalid publication channels; preserve both commits unchanged.
5. Record a row for every restored artifact with path, original carrier, original blob SHA and restored blob SHA; require `git diff --quiet <carrier> HEAD -- <path>` to exit 0.
6. Self-review scope, ancestry, name-only diff, author identity and exact-head Hosted Plan validation; merge only this scoped Plan PR after validation succeeds.
7. Read back every newly restored path from post-merge main, update the lane board and publish the final evidence witness.

## Visible identity and provenance

Card 0428-251 frontmatter owner verbatim from live `origin/main` at runtime (`tasks/t-20261123-demo-digest-consent-adaptation.md`): `owner: Coordinator (merge 1450) / 9b7683b5`. This is the assigned reviewer/recovery lane `w255-0428-251-demo170codex`; following the explicit Owner lane assignment, every commit created by this work uses git user.name `w255-0428-251-demo170codex` and git user.email `w255-0428-251-demo170codex@baseharbor.local`.

Literal planned commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit -m "Restore unique stranded Plan evidence"`.

Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`; also inspect `%cn` and stop on any mismatch.

Planning repository remote verified in the isolated worktree: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. The local shared checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` remains read-only with unrelated modified/untracked work.

Base attestation at branch creation: `7ae6d04bf92217ca70e664542897f42e237dbe89` (the live main tip immediately after PR #75 merge). Before edits, fetched live main advanced to `6480495f518eb83c4b1e01ecbfa3c48defd45fc1`; this branch fast-forwarded to that exact tip before any candidate commit. This preserves the original base attestation and current live ancestry.

## PR #75 post-merge readback

PR #75 merged by squash as `7ae6d04bf92217ca70e664542897f42e237dbe89`; exact-head Hosted `Plan · validate` run `45743596213` succeeded on `56db4052c4153fd4903e489293b295cf13794ade` (`pull_request`, completed success). The PR restored 12 of the 88 paths inventoried by w271 PR #76 (head `97cf9672e11922025e43afd56611df8fca679468`, Hosted validation run `45741218805` success). The post-merge readback was performed after fetching main at `7ae6d04bf92217ca70e664542897f42e237dbe89`; each path passed `git cat-file -e origin/main:<path>` and the first line below is the exact `git show origin/main:<path> | head -1` witness.

| Path | Post-merge `head -1` witness |
| --- | --- |
| `evidence/2026-11-28/w247-0428-285-1820hop.md` | `# w247 — PR-HOP #1820 (card 0428-285) — STOP + STATE, ancestry-gap documentation` |
| `evidence/r28-welle6-2026-11-26/1851-carrier/disposition.md` | `# #1851 carrier disposition` |
| `evidence/r29-welle6-2026-11-28/0428-253/w136-1853-owner-ruling.md` | `# Owner ruling record — card 0428-253 / PR #1853` |
| `evidence/r29-welle6-2026-11-28/0428-284/w136-demo-prgate-availability.md` | `# Demo PR gate availability disposition — #179 and #170` |
| `evidence/2026-11-26/w249-0428-284-gateids/akte.md` | `# w249-0428-284-gateids — Read-only 14-gate id pre-flight audit` |
| `evidence/e6ca7696-b1f8-492d-b226-876b16925fc5/w245-0428-284-1842alt/akte.md` | `# w245-0428-284-1842alt · READ-ONLY routing alternatives for PR #1842` |
| `evidence/r29-welle6-2026-11-26/0428-284-1842alt/routing-alternatives.md` | `# w245-0428-284-1842alt · READ-ONLY routing alternatives for PR #1842` |
| `evidence/w248-0428-284-boardscan/akte.md` | `# w248-0428-284-boardscan — board intake scan akte` |
| `evidence/verify/w253-demo170179-census.md` | `# w253 — Demo PR Census (#170 + #179), read-only` |
| `evidence/r28-welle6-2026-11-26/w252-1833-1835-disposition/disposition.md` | `# Disposition: #1835 and #1833` |
| `evidence/w246-1812diag/w246-1812gatefaildiag.md` | `# w246 — 1812 post-retry gate fail diagnosis` |
| `evidence/w255-0428-251-demo170codex/decision.md` | `# w255-0428-251-demo170codex — demo PR-event route decision` |
| `evidence/w258-1819-preflight/akte.md` | `# w258-0428-273-1819preflight — read-only preflight of PR #1819` |

The post-merge task readback at `tasks/t-20261124-gate-catalog-baseline-1819.md` records that the requested #1819 catalog rows already exist exactly once through BaseHarbor PR #1822, merged at `90086a1f938e106171b08c76e9bcbc98d89d1de4`; no further catalog edit or dispatch is needed. It also says #1812's 14-gate preflight is not qualified by #1650's stale run and remains unqualified pending exact-head evidence.

## Census disposition

Source is w271's read-only census in Plan PR #76, exact head `97cf9672e11922025e43afd56611df8fca679468`, validation run `45741218805`; it measured 88 missing evidence/task paths totalling 632,946 bytes at its census point. The w271 result is not altered by the two later direct-main evidence publications described below. PR #75 restored 12; this follow-up evaluates the 76 additional census rows against current main.

Three paths are omitted as content duplicates, not silently lost: `evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/w194-0428-224-intake.md` has the exact same blob `2157b2f48472e9dc76ada6e5a15e52185eae61ea` as existing root path `w194-0428-224-intake.md`; `evidence/w246-0428-284-1812diag/w246-1812gatefaildiag.md` has the exact same blob `9781ec653c1650702ab28613fbe3d8fa2dc27eca` as the canonical path restored by #75, `evidence/w246-1812diag/w246-1812gatefaildiag.md`; and `tasks/t-20261124-r28-alert-applied-face-stale-runtime.md` (0428-268) is superseded by the current accepted 0428-268 evaluator/live-health task delivered by #1831. The source blob and matching or superseding current path were checked before exclusion.

Six Hunt47 task files are not duplicates: their card IDs 0428-341 through 0428-346 are occupied on current main by unrelated Hunt48 task files. Park them for Coordinator reissue under unique IDs; do not change their contents or publish an ID collision. The mappings are in the table below. The four remaining Hunt47 task IDs 0428-347 through 0428-350 are free and restored verbatim, along with unique tasks 0428-155, 0428-175, and the rcptlink task. All other still-missing census evidence paths are restored verbatim. Therefore 67 unique paths are restored in this PR, 3 are duplicate-content exclusions, and 6 card-ID conflicts are parked for reissue; no unique source artifact in this selected set was unavailable.

| Parked source task | Source card ID | Current main occupant |
| --- | --- | --- |
| `tasks/t-20261125-hunt47-provider-registry-v1-migration.md` | 0428-341 | `tasks/t-20261128-hunt48-workstation-bootstrap-contract.md` |
| `tasks/t-20261125-hunt47-deployment-record-v1-wall.md` | 0428-342 | `tasks/t-20261128-hunt48-metrics-endpoint-docs.md` |
| `tasks/t-20261125-hunt47-destroystep-v1-warning-kind.md` | 0428-343 | `tasks/t-20261128-hunt48-unify-runtime-error-envelope.md` |
| `tasks/t-20261125-hunt47-recover-preflight-and-flag-route.md` | 0428-344 | `tasks/t-20261128-hunt48-runtime-pagination-contract.md` |
| `tasks/t-20261125-hunt47-version-gate-error-surface.md` | 0428-345 | `tasks/t-20261128-hunt48-refresh-public-api-ownership-map.md` |
| `tasks/t-20261125-hunt47-keycloak-migration-docs.md` | 0428-346 | `tasks/t-20261128-hunt48-source-transfers-contract.md` |

## Invalid publication-channel dispositions

The following original commits and files remain untouched in history. Their reports are restated here through the scoped forward-only Plan PR path; neither commit is accepted as qualified lane publication evidence.

| Source akte path | Invalid main commit | True executing lane | Content verdict |
| --- | --- | --- | --- |
| `evidence/w275-0428-251-runaudit/w275-0428-251-runaudit.md` | `9ff4e1108675f18350974a7757c420568a89f692` | `w198` (per akte and commit author; committer was coordinator) | Read-only mechanism finding is usable with a corrected chronology: default-branch `pr-config-matrix.yml` landed at `d512653aa2e5e69e734caf9b64b5043f409ade42` 00:06:55Z, about 2 minutes before #170's 00:09:09/10Z reopen events, not 57 minutes after. Current route is a fresh PR event; no workflow edit. The develop-copy path list lacks #179's four changed files and must be reviewed as part of its event preflight. |
| `evidence/w276-0428-284-1812fire/w276-0428-284-1812fire.md` | `6480495f518eb83c4b1e01ecbfa3c48defd45fc1` | `w276-0428-284-1812fire` (per akte; author/committer were coordinator) | Point-in-time read-only hop and source-coverage findings are useful, but its “14 gate” accounting is internally inconsistent with its 17/18-name enumeration, and the b411277 demo-pin statement is stale under the Owner ruling to target `5ca92a7cd2f746934890cfd7096a48068bdf218e`. Treat it as historical analysis, not current qualification. |

Both direct-main commits are one-parent commits with zero associated Plan PRs. The w275 report had author `w198 <w198@users.noreply.github.com>` and committer `coordinator <coordinator@baseharbor.local>`; w276 had author and committer `coordinator <coordinator@baseharbor.local>`. No force, rewrite, or revert was performed. Neither path was part of w271's already-verified 88-path inventory, so the original census count is unchanged.

## Demo PR-event route decision

The w275 audit's root-cause class is workflow-set resolution on the default branch: `pr-config-matrix.yml` landed on Demo main at `d512653aa2e5e69e734caf9b64b5043f409ade42` at 00:06:55Z, about two minutes before #170's close/reopen events at 00:09:09/10Z. The earlier wording that it landed 57 minutes after those events was a time arithmetic error. The paths filter was not the cause for #170: its changed `tests/config-matrix/run.sh` matched the main-copy allowlist. The control `pr-guided-consent.yml` produced `pull_request` run `45726412673` SUCCESS for a base=main event. The appropriate next action is a fresh pull_request event; this lane makes no workflow change and triggers no event.

Coordinator ruling: commission a fresh close+reopen for #170 now (OPEN, non-draft, base `develop`, head `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`). Commission #179 after it is made ready, also by fresh close+reopen (OPEN, currently draft, base `develop`, head `cda6aa70e80bec1a1db06d85decdd8833cb63994`). The main/default-branch workflow copy covers all four #179 changed files, so the develop-copy omission is copy drift to record, not a prerequisite to this event; no workflow change is needed. Do not commission #181 yet: it is based on `main` while this workflow selects `develop`; it needs a develop-side base=develop event with an applicable changed allowlisted path first.

The pair bar remains two distinct `pull_request` SUCCESS run IDs on the same exact head, each with executed check jobs. One close+reopen yields at most one new qualifying run; only after its terminal success on the exact head should the Coordinator commission the second distinct run with another close+reopen. Push runs, skipped/queued jobs, and empty job sets do not qualify.

## Artifact equality table

Pending restoration and exact per-path comparison. For a ref locator, restore with `git checkout <full-carrier-commit> -- <path>`. For stash-only rows where the file is stored in the stash's untracked third parent, restore with `git checkout <full-stash-commit>^3 -- <path>`; the stash index was resolved to its full SHA before use and no stash is consumed. For every row, compare `git rev-parse <carrier-tree>:<path>` with the staged/restored blob and require `git diff --quiet <carrier-tree> -- <path>` to exit 0.

| Path | Original carrier tree | Original blob SHA | Restored blob SHA |
| --- | --- | --- | --- |
| `evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-1.md` | `e3f77c4a93f90a1650183538f02b6137b94f1c66` (locator `stash@{48}`) | `afe8ceb520e6fc38f863ca3338e37e740fa13ec7` | `afe8ceb520e6fc38f863ca3338e37e740fa13ec7` |
| `evidence/r29-welle6-2026-11-25/w205-0428-253-planner-deleted-source/akte.md` | `cc9c96409a65be9a939e471e931f0f4621dfa355` (locator `ref:cc9c96409`) | `7ef45a1f7d9895fbec6f3b07c88141fd94b00f26` | `7ef45a1f7d9895fbec6f3b07c88141fd94b00f26` |
| `evidence/w228-0428-216-huntv59/akte.md` | `5ba20ff3e34d5de8b50542f0fbbeeae636729e6f` (locator `ref:5ba20ff3e`) | `ad302f2a24f4a8d1e4ba1a1e0d0916acc6e7d395` | `ad302f2a24f4a8d1e4ba1a1e0d0916acc6e7d395` |
| `evidence/2026-11/w242-0428-285-1820census/akte.md` | `5ba20ff3e34d5de8b50542f0fbbeeae636729e6f` (locator `ref:5ba20ff3e`) | `3d728a53fc81105b1349b2619589e21ad70601ed` | `3d728a53fc81105b1349b2619589e21ad70601ed` |
| `evidence/r28-welle6-2026-11-27/bughunt-hv47-upgrade-migration/intake-1.md` | `a47da84b82f2fd10294c934944566d4d935c61a1` (locator `ref:a47da84b8`) | `1c7776c497bca61c6287a961151a1a717c6a29fa` | `1c7776c497bca61c6287a961151a1a717c6a29fa` |
| `evidence/r28-welle6-2026-11-26/1842-review/review.md` | `5ba20ff3e34d5de8b50542f0fbbeeae636729e6f` (locator `ref:5ba20ff3e`) | `67c8c04077c5dec492bc6bdd4f096fd4f9aa43d0` | `67c8c04077c5dec492bc6bdd4f096fd4f9aa43d0` |
| `evidence/r28-welle6-2026-11-25/0428-284-1842-hop/round-1.md` | `25262d41c41912aafeb0fead9590043560b955e1` (locator `ref:25262d41c`) | `9ca0ab57ea5f407952a12b887d211278a09b6501` | `9ca0ab57ea5f407952a12b887d211278a09b6501` |
| `evidence/r28-welle6-2026-11-27/bughunt-hv54-config-defaults/w209-0428-224-hunt-v54.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `48f2e6cd25584669ea0397fb0cff2aed06092d95` | `48f2e6cd25584669ea0397fb0cff2aed06092d95` |
| `evidence/r28-welle6-2026-11-25/w237-0428-283-1818reset2/round-1.md` | `5ba20ff3e34d5de8b50542f0fbbeeae636729e6f` (locator `ref:5ba20ff3e`) | `40b457f731530244a78739dae3fd18e424cae033` | `40b457f731530244a78739dae3fd18e424cae033` |
| `evidence/r28-welle5-2026-11-23/hunt39-v55/catalog-lifecycle-hunt.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `6ee929ee0fbfa7a3680f64950152d501fa3c5370` | `6ee929ee0fbfa7a3680f64950152d501fa3c5370` |
| `evidence/r28-welle6-2026-11-25/w222-0428-307-1852-secondrun/secondrun-gate-akte.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `5ffbe8726aa5bc7716ae3fd64af50810e3c21d8c` | `5ffbe8726aa5bc7716ae3fd64af50810e3c21d8c` |
| `evidence/r29-welle6-2026-11-28/0428-287/w136-1835-redundancy.md` | `34b33010b401229a60c50f7a2acef7d3ed316c45` (locator `ref:34b33010b`) | `fc815666babc137a4021840061f17eb0e1732b83` | `fc815666babc137a4021840061f17eb0e1732b83` |
| `evidence/r28-welle6-2026-11-25/w218-0428-181-0428-285-1819hop/1819-pr-hop-akte.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `a415abfb3b9e5fb138d6cd93ebcd90cf841e4f88` | `a415abfb3b9e5fb138d6cd93ebcd90cf841e4f88` |
| `evidence/2026-11-shift/0428-263/w200-1846-review.md` | `cc9c96409a65be9a939e471e931f0f4621dfa355` (locator `ref:cc9c96409`) | `909162bbab79fc98efa2ee59679b2229d51dd27f` | `909162bbab79fc98efa2ee59679b2229d51dd27f` |
| `evidence/r28-welle4-20261114/0428-065/round-rebase-1615.md` | `b8bb8b7b199b9fd17233be0571c94a688dd1f0a3` (locator `ref:b8bb8b7b1`) | `41ce287917b1cb7d92357de33b0f436c0a8b5a82` | `41ce287917b1cb7d92357de33b0f436c0a8b5a82` |
| `evidence/r28-welle5-2026-11-22/sourcepull-0428-223/review-1750-head17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99.md` | `b4286199e29c14436f849a1d900e2c7dde805a03^3` (locator `stash@{41}`) | `cd2edbe0ef18029d23d1cd2bc0d880b05622a7fc` | `cd2edbe0ef18029d23d1cd2bc0d880b05622a7fc` |
| `evidence/r28-welle6-2026-11-25/w226-0428-307-0428-283-1818reset.md` | `37320b0b8b1d8c9effcf198138b612b88d1b6dd3` (locator `ref:37320b0b8`) | `a8246229ff83539a02b0aa761038826813f87f46` | `a8246229ff83539a02b0aa761038826813f87f46` |
| `evidence/r28-welle6-2026-11-27/w198-0428-284-demo-parser/w198-dispatch-wave-48bac372.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `28fdbbbde81f49326305e9d99e74752d84c1028b` | `28fdbbbde81f49326305e9d99e74752d84c1028b` |
| `evidence/r28-welle6-2026-11-25/w213-0428-287-1835-refresh/evidence.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `06ec6a5dc4927e4214f9df83bd6fce87dad466a3` | `06ec6a5dc4927e4214f9df83bd6fce87dad466a3` |
| `evidence/r29-welle6-2026-11-28/0428-253/w243-1853-rundown.md` | `5ba20ff3e34d5de8b50542f0fbbeeae636729e6f` (locator `ref:5ba20ff3e`) | `e5736dfa23a769a6e86845584601d6e32b057bd3` | `e5736dfa23a769a6e86845584601d6e32b057bd3` |
| `evidence/r29-welle6-2026-11-28/plan-akte-collision/akte-recovery.md` | `5ba20ff3e34d5de8b50542f0fbbeeae636729e6f` (locator `ref:5ba20ff3e`) | `b9f7fa0075c2966140314ece639796c02c93dbec` | `b9f7fa0075c2966140314ece639796c02c93dbec` |
| `evidence/r28-welle6-2026-11-25/w198-0428-284-demo-parser/round-0.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `d76fd6c7e13fa83582cfd18692797a8083eea36e` | `d76fd6c7e13fa83582cfd18692797a8083eea36e` |
| `evidence/2026-11-shift/0428-284/w241-0428-284-1812prehop.md` | `5ba20ff3e34d5de8b50542f0fbbeeae636729e6f` (locator `ref:5ba20ff3e`) | `a1414ed6f369c878552206acd68b3aeed53a7ab2` | `a1414ed6f369c878552206acd68b3aeed53a7ab2` |
| `evidence/r28-welle5-2026-11-22/oras-0428-229/review-1750-head4bd779b1.md` | `11454a71bc79e2dcb4a636e6f2e960388b8928ca^3` (locator `stash@{44}`) | `c1a6ed4df0bf066e08e7f92e9339bb5298f45f8c` | `c1a6ed4df0bf066e08e7f92e9339bb5298f45f8c` |
| `evidence/r28-welle4-2026-11-24/w55-0428-078-probehop-hold.md` | `19c45593daf6a5a2d53bf452a2e64b2cbb63981b^3` (locator `stash@{11}`) | `dfbe752d6eff00f06708307b2e327312ce2028a1` | `dfbe752d6eff00f06708307b2e327312ce2028a1` |
| `evidence/r28-welle6-2026-11-27/0428-284/w136-pin-disposition.md` | `37320b0b8b1d8c9effcf198138b612b88d1b6dd3` (locator `ref:37320b0b8`) | `c1ea42a005541f52cda34d33b314b577f55fa40f` | `c1ea42a005541f52cda34d33b314b577f55fa40f` |
| `evidence/r29-welle6-2026-11-28/0428-253/w136-pr1853-admission-ruling.md` | `34b33010b401229a60c50f7a2acef7d3ed316c45` (locator `ref:34b33010b`) | `0c7f786d892d71abdbba7a0c3e790d09892a64a6` | `0c7f786d892d71abdbba7a0c3e790d09892a64a6` |
| `evidence/w221-0428-253-1853fix/akte.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `bc11616c571fffa941996b830bf9fd8704b9213a` | `bc11616c571fffa941996b830bf9fd8704b9213a` |
| `evidence/2026-11-shift/0428-284/w200-1812-review.md` | `e78e07c0ca105dcad0a0a5ddc241d5e17ddd75d0` (locator `ref:e78e07c0c`) | `d177a7f32deba9e07c2b6903a429f9dbebadad0c` | `d177a7f32deba9e07c2b6903a429f9dbebadad0c` |
| `evidence/2026-11-shift/huntV55/w200-huntV55-disposition.md` | `1a0b786f4eff2e29106d4474c16b698618d6d4b1` (locator `ref:1a0b786f4`) | `262d3759b86703e157fe67a29b664073ce620540` | `262d3759b86703e157fe67a29b664073ce620540` |
| `evidence/2026-11-25/w234-0428-307-1842run2.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `a95e742ad0e24a6b75cf916e2fe10787e85f8895` | `a95e742ad0e24a6b75cf916e2fe10787e85f8895` |
| `evidence/2026-11-25/w200-outstanding-two/decisions.md` | `cc9c96409a65be9a939e471e931f0f4621dfa355` (locator `ref:cc9c96409`) | `4b67411f43684d92a35652b61e80f0120f910671` | `4b67411f43684d92a35652b61e80f0120f910671` |
| `tasks/t-20261119-coord-tooling-defects.md` | `12781be59c561ef1497a5c37c4b2de61090d5e06` (locator `ref:12781be59`) | `cdf21458a1ff28f513934667aa51588aa4201f4a` | `cdf21458a1ff28f513934667aa51588aa4201f4a` |
| `evidence/shifts/2026-11/0428-288/w203-0428-288-diag-165-impl-170/akte.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `d447eca27356c9e3739082acb650096ee2a2d1f6` | `d447eca27356c9e3739082acb650096ee2a2d1f6` |
| `evidence/2026-11-25/w200-1650-review-merge/review.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `bd2beed9432cd479afa112d45ee40aee31829ae9` | `bd2beed9432cd479afa112d45ee40aee31829ae9` |
| `evidence/2026-11-25/w200-1851-carrier/disposition.md` | `cc9c96409a65be9a939e471e931f0f4621dfa355` (locator `ref:cc9c96409`) | `a4be784ed3c1455f3d413ddbba3be882db64b7c1` | `a4be784ed3c1455f3d413ddbba3be882db64b7c1` |
| `evidence/r28-welle5-2026-11-22/0428-227/review-1753-head71deb610.md` | `11454a71bc79e2dcb4a636e6f2e960388b8928ca^3` (locator `stash@{44}`) | `9f9ae08ca37e7da827adfa3b0a367afaa152ad07` | `9f9ae08ca37e7da827adfa3b0a367afaa152ad07` |
| `evidence/2026-11-shift/0428-263/w210-0428-263-pr1846-hop.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `4d77184054754c0c30ffc1141c8fbe4a9571ec09` | `4d77184054754c0c30ffc1141c8fbe4a9571ec09` |
| `evidence/2026-11-shift/1812-runtime-routing/w200-1812-runtime-routing.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `09a3285667a979c63c8b198543c60b350dcce0ae` | `09a3285667a979c63c8b198543c60b350dcce0ae` |
| `evidence/2026-11-25/w214-0428-284-1812-hop.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `54403cc278db9d1fbf1c65f5096858a31d757d8c` | `54403cc278db9d1fbf1c65f5096858a31d757d8c` |
| `evidence/2026-11-shift/cancelgroup/w200-cancelgroup-befund.md` | `cc9c96409a65be9a939e471e931f0f4621dfa355` (locator `ref:cc9c96409`) | `6362ffcbbf95369559194f8071bc0b675ab90499` | `6362ffcbbf95369559194f8071bc0b675ab90499` |
| `tasks/t-20261125-hunt47-write-stamp-json-version.md` | `a47da84b82f2fd10294c934944566d4d935c61a1` (locator `ref:a47da84b8`) | `870c317cd74dc40a977eebcd572d568a4b75e81e` | `870c317cd74dc40a977eebcd572d568a4b75e81e` |
| `tasks/t-20261125-hunt47-deleted-deployment-dangling-binding.md` | `a47da84b82f2fd10294c934944566d4d935c61a1` (locator `ref:a47da84b8`) | `ca54d0c1e6e35d6d7af1433feff93f1a543a71a1` | `ca54d0c1e6e35d6d7af1433feff93f1a543a71a1` |
| `evidence/w186/0428-186-hop.md` | `adfb6c7b921b04e7ef073045b0cb6bbb210caee0^3` (locator `stash@{30}`) | `b1540def552cad23e6bb0997ce9f93762527a679` | `b1540def552cad23e6bb0997ce9f93762527a679` |
| `evidence/2026-11-25/w213-0428-287-1835-refresh.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `41fe11aa6af3d30b67f8834c3a61dcc1ab9e2495` | `41fe11aa6af3d30b67f8834c3a61dcc1ab9e2495` |
| `tasks/t-20261125-hunt47-core-plan-version-message.md` | `a47da84b82f2fd10294c934944566d4d935c61a1` (locator `ref:a47da84b8`) | `f3873478549766942ebdbbf7077e84076e6c057c` | `f3873478549766942ebdbbf7077e84076e6c057c` |
| `tasks/t-20261125-hunt47-config-mutation-migration-parity.md` | `a47da84b82f2fd10294c934944566d4d935c61a1` (locator `ref:a47da84b8`) | `edaa444b01f077dc2df8fe79b69517bee638fd99` | `edaa444b01f077dc2df8fe79b69517bee638fd99` |
| `tasks/t-20261120-coord-publish-integrity-gaps.md` | `12781be59c561ef1497a5c37c4b2de61090d5e06` (locator `ref:12781be59`) | `c9e3e67ea6905d3285e65ea3fc69dfa817675404` | `c9e3e67ea6905d3285e65ea3fc69dfa817675404` |
| `evidence/r28-welle6-2026-11-25/w211-0428-307-fallback.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `90f69b1fa1ea4b9e5d150caf53fe3c84a9f762ce` | `90f69b1fa1ea4b9e5d150caf53fe3c84a9f762ce` |
| `evidence/recovery-2026-11-23/0428-058/round-1.md` | `1069cbc211eac839344c9e06a65397865ecf0a87^3` (locator `stash@{38}`) | `4878ac9a0396ef7bb1a9c75f2a343678d8a14457` | `4878ac9a0396ef7bb1a9c75f2a343678d8a14457` |
| `evidence/w216-1852-hop/EVIDENCE.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `bfe4fd4423389930cec8905ae673430fcd4ef06d` | `bfe4fd4423389930cec8905ae673430fcd4ef06d` |
| `tasks/t-20261102-rcptlink-task.md` | `9b80d8344adb818193c0db285e6ea18b551d6846` (locator `ref:9b80d8344`) | `4febd322811bf803c8a2316e6628dcf9fbf5ee39` | `4febd322811bf803c8a2316e6628dcf9fbf5ee39` |
| `evidence/r28-welle4-2026-11-24/w55-0428-078-probehop-stop.md` | `f40c6ffda83e699a2d6b82a616ce53450aaf3adf^3` (locator `stash@{24}`) | `9da24d6237e692b04c3a38ce5138a324620146fe` | `9da24d6237e692b04c3a38ce5138a324620146fe` |
| `evidence/r28-welle4-2026-11-18/codex-welle3-review/1686.md` | `fbce6e639342065daa0210ffef61f8d78f06cffc` (locator `ref:fbce6e639`) | `09d6b4d748327890c92e3041c5889ecf7471973e` | `09d6b4d748327890c92e3041c5889ecf7471973e` |
| `evidence/2026-11-25/w234-0428-307-1850run2.md` | `e3877cd55e6d2f2e7e68905094c4c82c85c87b31^3` (locator `stash@{1}`) | `58ffb11b93bcdd635dfad3fe7f2458a1461be9cd` | `58ffb11b93bcdd635dfad3fe7f2458a1461be9cd` |
| `evidence/r29-welle6-2026-11-28/0428-307/w136-1852-owner-admission-pr.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `749e2d18bbacc080f97013d5d557238ddf396902` | `749e2d18bbacc080f97013d5d557238ddf396902` |
| `evidence/r28-welle4-2026-11-18/codex-welle3-review/1592-r2.md` | `fbce6e639342065daa0210ffef61f8d78f06cffc` (locator `ref:fbce6e639`) | `907c7f0e6b5ba889a07e5bb19f9e30c2f282bf7f` | `907c7f0e6b5ba889a07e5bb19f9e30c2f282bf7f` |
| `evidence/r28-welle6-2026-11-25/0428-078/pr1847-review-merge.md` | `37320b0b8b1d8c9effcf198138b612b88d1b6dd3` (locator `ref:37320b0b8`) | `247b908ff979f592b37face431baae792723e202` | `247b908ff979f592b37face431baae792723e202` |
| `evidence/board-2026-11-24/w68-0428-277-revealallow.md` | `1c649705a4b4cde684d6afc5d73278549ba1fa88^3` (locator `stash@{9}`) | `960135cddceae7bfae2657a837b9c2fa2968fed3` | `960135cddceae7bfae2657a837b9c2fa2968fed3` |
| `evidence/w266-0428-285-1820pre/PLAN.md` | `8b46c5c20da3e8abaaa5210b80b7044576480067` (locator `ref:8b46c5c20`) | `e41b0dac261342505f5c8b550e51f3ef40dbcb39` | `e41b0dac261342505f5c8b550e51f3ef40dbcb39` |
| `evidence/r29-welle6-2026-11-28/0428-1819/w136-1819-review.md` | `34b33010b401229a60c50f7a2acef7d3ed316c45` (locator `ref:34b33010b`) | `e63d2d387c110767c27752ebdee10e183a94c9ce` | `e63d2d387c110767c27752ebdee10e183a94c9ce` |
| `evidence/r29-welle6-2026-11-28/0428-307/w136-1852-requal-review.md` | `34b33010b401229a60c50f7a2acef7d3ed316c45` (locator `ref:34b33010b`) | `6c9e3b3dd81c3a66f088e485be56f33c1c24f663` | `6c9e3b3dd81c3a66f088e485be56f33c1c24f663` |
| `evidence/r28-welle5-2026-11-22/rev1756f/review.md` | `8110a053d9b7fa7f338fd82e8a91e90221fe3847^3` (locator `stash@{40}`) | `626c319ae0ed9c4dd0cd8acfc6abae0b50807943` | `626c319ae0ed9c4dd0cd8acfc6abae0b50807943` |
| `evidence/r28-welle6-2026-11-24/broker-build-identity-w69/evidence.md` | `585ee38f3aac29cd30a9ae68c44b612c96dc7c87^3` (locator `stash@{7}`) | `32704078b7a98681307520f6bbf1e1f514719ed6` | `32704078b7a98681307520f6bbf1e1f514719ed6` |
| `evidence/r28-welle5-2026-11-22/redir1756/review.md` | `8110a053d9b7fa7f338fd82e8a91e90221fe3847^3` (locator `stash@{40}`) | `6ae5a236ebac553b4c3c39c22bda89767215e1dd` | `6ae5a236ebac553b4c3c39c22bda89767215e1dd` |
| `evidence/r28-welle5-2026-11-22/publishB/review.md` | `8110a053d9b7fa7f338fd82e8a91e90221fe3847^3` (locator `stash@{40}`) | `7fb0a78d309a11ec1b1b91184e0479be8378a3cb` | `7fb0a78d309a11ec1b1b91184e0479be8378a3cb` |
| `evidence/2026-11-25/w219-0428-271-0428-286-1820hop.md` | `541a07965d7d7f19e46a263ccc6145024fce2d37` (locator `ref:541a07965`) | `43bda27f6721e40af3e5d7d9ee135f2583c2a801` | `43bda27f6721e40af3e5d7d9ee135f2583c2a801` |

Equality review: every row above was checked with `git rev-parse <carrier-tree>:<path>` against the staged blob and `git diff --quiet <carrier-tree> -- <path>` exited 0. Stash-only files were found in the stash third-parent tree; no stash was applied, popped or dropped. All 67 paths were absent at their exact path on fetched `origin/main` before restoration.

## CardBoard scanner scope correction

The coordinator authorized the minimal scanner fix in this same scoped forward-only PR. The original evidence bytes stay unchanged and retain exact source/restored blob equality. Census rows `evidence/w186/0428-186-hop.md` (original blob `b1540def552cad23e6bb0997ce9f93762527a679`; source lines 31-34) and `evidence/w266-0428-285-1820pre/PLAN.md` (original blob `e41b0dac261342505f5c8b550e51f3ef40dbcb39`; source lines 7-13) contain lane-plan checkboxes. The prior scanner treated those evidence notes as board cards, contrary to the Plan rule that CardBoard cards come from `tasks/`. `scripts/plan.py` now excludes `evidence/**` and `workers/**` from the stray-card scan while retaining task note validation and stray-card rejection elsewhere. `scripts/tests/test_plan.py` keeps the task-note extra-checkbox rejection and adds a regression proving the same checkbox in evidence and workers notes does not fail. Both are reached by the existing Hosted `Plan · validate` job's `Unit tests` step and subsequent `Validate vault and generated files` step on `pull_request`; no workflow change is needed. No evidence artifact bytes were changed.

## Refreshed #75 presence readback on current main

After the coordinator requested a fresh read, `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` and `git rev-parse origin/main` both returned `1f3e0673fa9f2265805c1291f794531c3876a9de`. All 13 #75 paths again passed `git cat-file -e origin/main:<path>`; `git show origin/main:<path> | head -1` returned the same witnesses recorded in the preceding PR #75 table. The 0428-273 card also exists on this tip and still states the #1822 exact-once catalog result and that #1812's 14-gate preflight remains unqualified; `git cat-file -e origin/main:tasks/t-20261124-gate-catalog-baseline-1819.md` exited 0.

Current fetched base for this follow-up candidate is `1f3e0673fa9f2265805c1291f794531c3876a9de`; `git merge-base --is-ancestor origin/main HEAD` exits 0 before candidate commits. This is a forward-only Plan PR based on the current main.
