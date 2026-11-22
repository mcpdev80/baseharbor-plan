# Why `PR · Selected Runtime` is still skipped after PR #1755 merged - measured

Develop `1ff16925c4e141d732459a34ddf0b7f49128a214`. Candidates: PR #1750 head `5d47569f3372f76078b040490c261d43233e1d92`
(hopped by lane 0428-223-testctx, run 44986337450) and PR #1753 head `ce5cf8f30373e13c0d08092d84b24232e93a356a`
(re-cut by the Owner, run 44986388874). Both still show `PR · Native · ${{ matrix.id }}` and
`PR · Selected Runtime` = skipped, which is why CODEX-REVIEW issued REQUEST CHANGES for the merged #1755.

## The mechanism, read from the trusted base

`.github/workflows/ci.yml` step "Select exact PR native impact" (near line 491) does not call
`scripts/pr-gate-plan.py`. It takes `scripts/pr-native-gate-plan.py`, `scripts/pr-gate-coverage.json`,
`scripts/validate-pr-gate-coverage.py` and `scripts/release-requirements.json` **from `$BASE_SHA`** and runs:

    pr-native-gate-plan.py --changed-paths-file <paths> --coverage pr-gate-coverage.json \
                           --requirements release-requirements.json

`pr-native-gate-plan.py:24-33` delegates to `validate-pr-gate-coverage.resolve_native_checks`
(`scripts/validate-pr-gate-coverage.py:66-88`), which selects a check only when **both** hold:

1. a row in `coverage["components"]` whose `path` equals a changed path, and
2. a row in `coverage["native_checks"]` (all six rows today) whose `source_components` names that component id.

## Measured gap

* `native_checks` has exactly 6 rows, all `selection_scope: "focused"`, ids such as
  `native/docker/perses-runtime-smoke`. Referenced component ids: 10.
* None of the paths that matter here has a `components` row: `cmd/baha/test_operator_context_test.go`,
  `cmd/baha/application_lifecycle_lock_test.go`, `cmd/baha/runtime_integration_test_support_test.go`,
  `cmd/baha/app_init_wizard_test.go`, `cmd/baha/repository_up_init_test.go`,
  `cmd/baha/ci_integration_operator_enabled.go`, `cmd/baha/ci_integration_operator_enabled_test.go`,
  `cmd/baha/ci_integration_operator_disabled.go` - all False (54 `cmd/baha` components exist, none of them these).

So `changed_ids` is empty for these PRs, `resolve_native_checks` returns `[]`, the planner emits
`{"include":[]}`, `required=false`, and both runtime jobs skip. PR #1755 correctly extended the wizard-style map in
`scripts/pr-gate-plan.py` and added the direct execution branch in `ci.yml`, but neither is consulted by this
selector. That is the whole remaining admission gap; nothing about the candidate code is at fault.

## Recipe (card 0428-234)

1. Add `components` rows following the existing shape (`{"id": "source.cmd.baha.test_operator_context_test",
   "path": "cmd/baha/test_operator_context_test.go", "surfaces": [...]}`) for the eight PR #1750 test sources and the
   three `ci_integration_operator_*` sources.
2. Add `native_checks` rows whose `source_components` name those ids and whose ids are gate ids the runtime matrix
   can actually build - `native/docker/*` plus the podman sibling, mirroring the gate tuples already chosen in
   `scripts/pr-gate-plan.py` (data-capabilities for the operator context and the lifecycle lock; + guided for the
   init/wizard/repository-up/Perses dashboards; + coreless-lifecycle for the shared runtime support file).
3. Keep `scripts/pr-gate-plan.py` and `pre-release-runtime-impact.json` as they are, and extend the pairing test in
   `scripts/test_pre_release_runtime_reuse.py` so a `components` row without a `native_checks` row (the exact defect
   class measured here) fails in CI instead of silently selecting nothing.
4. Proof is hosted, at the hopped heads of #1750 and #1753: `PR · Native · <id>` and `PR · Selected Runtime` executed
   (not skipped), job ids recorded.

## Separate finding, same sweep

The lane for PR #1746 stopped correctly: `.github/workflows/pre-release-runtime-suite.yml` has only a
`workflow_call` trigger (near line 633) and no `workflow_dispatch`, and the static cells are reached only through
`.github/workflows/pre-release.yml` "Release Validation" (near lines 672-687, `runtime: static`), which itself needs a
release tag from the orchestrator. A lane must not dispatch that chain, so the current-head static proof for #1746
needs either an Owner-added dispatch entry or a tag-gated release validation run.
