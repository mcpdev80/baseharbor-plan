# v0.4.26 CI integration — session 1

Marcel assigned this session CI implementation, integration and coordination. Session 2 owns native acceptance and consumer freezes; session 3 owns independent review. Their published handoffs at `67bb9ad81fb65a49e495fc2b3e1cd34dbcd22f30` and `33b7e29852a50198ae71b18a40a82185e4b17252` were read and preserved. No product merge, tag, release, deployment, full pre-release or cleanup was performed. v0.4.27 is untouched.

## Exact replacement candidates

| PR | Published head | Tested tree / local checkpoint | Current technical outcome |
| --- | --- | --- | --- |
| [#1064](https://github.com/mcpdev80/baseharbor/pull/1064) | `e7fe45ccb3c2103bb3b57ad3300892b932818934` | tree `ead688ff2e5ebb660c369cd073e1dc268153d6d0`, local `570e16384539fa15dae349699e951a4310ae0474` | [40110621660](https://github.com/mcpdev80/baseharbor/actions/runs/40110621660): mandatory final check and all selected validations PASS. Fresh independent source review remains required; previous verdict applied to `54dfa458`. |
| [#1060](https://github.com/mcpdev80/baseharbor/pull/1060) | `db79f24a39ccc1a6f8f38a13d20dd18ab151abc2` | tree `aaf2be84d53c8b8b320e14d3b73c7260c31b1fe1`, local `4806d2783dafce5800cf159c0f975ec9ebd4013d` | [40110759871](https://github.com/mcpdev80/baseharbor/actions/runs/40110759871): focused Python, planner, policy, executor/verifier and actionlint PASS; final check BLOCKED on exact workflow/executor qualification. This is not acceptance. Fresh source review and accepted target-side record still missing. |

Both are ordinary forward commits on the existing PR branches. Published trees were checked against the locally tested trees before the expected-SHA, non-force ref updates. API-created commits have different commit metadata from local checkpoints; tree identity is established, not guessed. No old-head review is extended to these replacements.

### #1064 correction

- Removed the inherited `bootstrap_eligible` fallback. A real-Git regression first reproduced acceptance of an unreviewed executor through a commit-message/title claim; it now rejects.
- Removed the obsolete hard-coded binding to rejected #1060 source. The existing trusted-target SHA-256 register now accepts exactly two bounded inventories: the three modified CI scripts, or those same scripts plus modified `ci.yml`. The latter always requires workflow syntax validation.
- The record must match authenticated repository/develop, exact statuses, full hashes and mandatory checks; actual diff/integration is independently re-derived. Reviewed source may advance only by exact Git-computed first-parent merges of trusted target history. No candidate-side record becomes authority.
- Reused the original real-Git integrity fixture for both inventories instead of preserving false rejection fixtures. Covered missing/forged integration, wrong hashes/statuses/context, omitted syntax checks, duplicate/weakened records, trusted forwards, untrusted side parents and altered/copied trees. The historical bootstrap positive now demands refusal.
- Python 3.12 / Go 1.26.9: complete planner suite **115 PASS**, existing executor/verifier suites **69 PASS**, focused binding/bootstrap matrix **25 PASS**, workflow policy **PASS (19 existing files)**, diff check PASS. Hosted required CI also PASS.

### #1060 correction

- Added a narrow binding for immutable #1052 source `9f715184af7b89ca3011aa4a0636c45138fe2c6b`: only the two modified bootstrap files qualify, through the actual resolver/integration and clean target-forward proof. Other paths, statuses or unreviewed follow-ups remain blocked. Independent qualification of this actual #1052 source is still a prerequisite to accepting the policy; the reported q123 verdict is not substituted for that review.
- Fixed the unreachable helper and actual workflow route: extract the runner from the trusted base, discover once, execute the exact 21 bootstrap/retry unit tests once and require RUN/PASS for each. Missing, skipped and failed requested families reject. Native opt-in tests remain separate runtime gates.
- Restored exact end-of-name anchoring for the existing core-918 SQL safety tests; replacement-suffixed names reject again.
- Planner/runner/workflow regression selection **125 PASS**; three focused strict-executor/real-Git/actual-shell-route tests PASS. The workflow case was executed against a real temporary trusted Git source and Go package for positive/missing/skipped cases. Process mocking is confined to the deterministic negative-output matrix.
- The actual corrected helper executed **all 21 required tests successfully** against immutable #1052 source `9f715184`. This was package-unit verification, not a Podman or other native receipt. A local real-object target-forward simulation against develop `65aa063e` resolves exactly `source-contracts` and `openbao-package-tests`.
- Actionlint **1.7.12**, workflow policy (19 files) and diff check PASS. Hosted component checks PASS; final coverage refusal remains expected until separately reviewed target qualification is integrated.

## Preserved #1056 preparation

Local-only checkpoint `ad3e4d2f70bf028a0b482abcce9b37d563340ce5` in `/workspace/scratch/754a78dce362/pins-correction` preserves the F1/F2 correction preparation; remote #1056 is unchanged at `b0abe105`.

The preparation reuses canonical `validate_ecosystem_graph`, `resolve_pins` and `source_origin` from trusted-base sibling modules. It verifies the full required gate set, role repositories, workflows, DAG consumes links, gate/ecosystem SHA equality and joint origins; v0.4.26 cannot omit its ecosystem graph. Duplicate JSON keys, noncanonical paths and symlinks reject. Historical v0.4.23 metadata stays checked under its existing format.

Also found a separate executable-path gap: the current workflow had no `pins-data-validation` case. The preparation adds that case, extracts the runner and its two canonical dependencies from the authenticated base into a fresh temporary directory, and proves the real shell route ignores candidate-supplied modules and propagates a graph failure. No workflow is added.

Canonical CLI/path/bootstrap/binding tests passed in bounded selections. An earlier 150-test combined regression selection passed before the final binding/path tightening; do not represent that as complete qualification of the final local checkpoint. This candidate must consume corrected integrated #1060/#1064 first, preserve the OpenBao runner changes and receive fresh checks/review before publication. No speculative qualification record or remote candidate was pushed for it.

## Native dispatch unblocked by the Owner

The connector has no workflow-dispatch mutation, and this host has no `gh` binary or Actions token. Marcel executed the existing authenticated CLI route on his VM, creating [40110974339](https://github.com/mcpdev80/baseharbor/actions/runs/40110974339), attempt 1, `workflow_dispatch`, wrapper develop `65aa063e90767c85af976081c100be1817370e67`.

Completed resolver job `120922437823` explicitly records Core `1861ed07888a1ec22c218ca491d23ee54f48e261`, Demo `f57c8b6e5ff39d0873df62b26272962765e88d6e`, runtime `podman`, gate `backup-restore`. Selected job `120922470036` is the requested bounded gate; the full reference journey is skipped. At this handoff checkpoint the native job is in progress, not PASS. Session 2 must inspect the final runtime and owned-cleanup result/artifacts before any Demo acceptance. No duplicate dispatch or rerun was requested.

## Integration order and remaining triggers

1. Session 3 reviews exact replacement #1064 `e7fe45cc`; mandatory CI is already green. Integrate only after its actual verdict and record the exact accepted source/merge outcome.
2. Review corrected #1060 and the actual #1052 source/test contract. After #1064 lands, bring actual develop into #1060, preserving both test matrices. A local preview found an expected overlap in the appended test section; resolve it explicitly, inspect the final tree and obtain the exact resulting review anchor. Do not manufacture a clean-merge proof for a manually resolved merge.
3. Publish a separate reviewed target-side SHA-256 register entry for that final #1060 four-file anchor; then a genuinely clean target-forward record merge and fresh required PR CI. No bootstrap or Required Check bypass.
4. After #1060: forward-integrate #1052 and run the selected real checks; continue the preserved #1056 correction as the sole planner writer, with a separate exact target record/fresh CI as needed. #1046's source-only approval still needs its current-anchor qualification and mandatory checks after C/D.
5. Session 2 owns final Podman receipt, actual D → U → K freezes and subsequent W1. Core C remains `1861ed07`; no speculative squash pins or v0.4.27 dependency is introduced. In the native handoff the superseded #9 is **Connector #9**, not Console #9; continue Console #9 unless a real later reason requires replacement.
6. #1050, final gate/origin inventories and final release acceptance follow the actual merged consumer graph. No release-readiness claim is made.

The other sessions' task notes, states, evidence and published handoffs are preserved. This session remains owner of the active CI closeout; no unrelated worker/daemon or hygiene operation was started.
