# CODEX-REVIEW: PR #1756 exact-head review

Session marker: 1450c201
Review role: CODEX-REVIEW, read-only
Candidate: `6cec31ff6737d1b409e9c9e3b1f3597fa0cb686b`
Base develop: `1ff16925c4e141d732459a34ddf0b7f49128a214`

## PLAN

1. Read the #1756 mission and record the numbered plan.
2. Refresh exact PR/head/base, current develop, gate catalog and CI run state.
3. Inspect the six requested routing, executor, assertion, and runtime-selection points at exact SHAs.
4. Verify exact-head CI job IDs, terminal status, and selected native gate IDs.
5. Write the SHA-specific review verdict and evidence in baseharbor-plan.
6. Publish evidence, verify its origin/main path, update the board, and post lane END.

## Verdict

REQUEST CHANGES

## Findings

1. Coverage: the requested source groups are represented in the candidate catalog: the eight #1750 Go test sources, three `ci_integration_operator_*` sources, environment destroy, service stop, and five legacy coreless runtime test sources. The candidate has 190 component rows, 15 native check rows, and 60 `native_checks` to `source_components` pairs. The new data-capabilities, guided, coreless-lifecycle, environment-destroy, and service-stop rows name the corresponding source component IDs.
2. Gate tuples: the candidate assignments match the base `scripts/pr-gate-plan.py` wizard map. Operator context and lifecycle lock select data-capabilities for both runtimes; init, wizard, repository-up-init, and both Perses dashboard tests select data-capabilities plus guided; shared runtime support selects data-capabilities, guided, and coreless-lifecycle.
3. Resolver: 28 catalog components declare `runtime_specific: true`. For a runtime-specific component, the resolver retains both Docker and Podman sibling checks when both are declared. For shared components it keeps the Docker representative, with set-based aggregation deduplicating repeated checks across components.
4. Executor: `ci-native-pr-gate.sh` has executable branches for `data-capabilities`, `guided`, `coreless-lifecycle`, `environment-destroy`, and Podman `service-stop`. These match the catalog IDs. Its fallback prints `REJECT: unsupported native PR gate` and exits 2.
5. Pairing assertions: NOT MET. The additions to `test_pr_gate_coverage.py` exercise selected examples, and `test_pre_release_runtime_reuse.py` checks that each path in `NATIVE_TEST_GATE_COMPONENTS` has a component and some native owner. They do not enforce the requested global pairing invariant across the intended native-admission source set in both directions. The validator rejects unknown component IDs, but does not catch a newly added relevant component that has no native check, nor verify reverse completeness against the admitted source set. Extend the shared assertion to compare the complete expected source-component and native-check pairs, so omission on either side fails in hosted CI.
6. Exact-head CI: run `44989283191` completed SUCCESS on exact head `6cec31ff6737d1b409e9c9e3b1f3597fa0cb686b`. `PR · Native gate plan` job `137106614785` completed SUCCESS; its output matrix was `{"include":[]}`. `PR Selected Checks` job `137106988634` completed SUCCESS. The native executor matrix job `137106648654` and selected-runtime job `137106653647` were skipped, and no gate IDs were selected. Per the correction received in `fix1756run.md.g`, this PR changes only `scripts/**`, so this empty exact-head matrix is expected and is not a defect in this candidate. PRs #1750 and #1753 are still open at heads `5d47569f3372f76078b040490c261d43233e1d92` and `ce5cf8f30373e13c0d08092d84b24232e93a356a`; their post-merge hopped-head runs do not yet exist. Do not use cancelled run `44989154812` (stale head `de141fe9fa13508f56136f96e6d2e70f8a3f29b4`) as acceptance evidence.

## CI evidence

- Exact PR head from `git ls-remote`: `6cec31ff6737d1b409e9c9e3b1f3597fa0cb686b` at `refs/pull/1756/head`.
- Exact develop base: `1ff16925c4e141d732459a34ddf0b7f49128a214` at `refs/heads/develop`.
- Run `44989283191`: completed SUCCESS on the exact candidate.
- Required aggregate `PR Selected Checks`: job `137106988634`, completed SUCCESS.
- Native plan job `137106614785`: completed SUCCESS with empty matrix; no selected gate IDs. This is expected for this scripts-only PR under the correction.
- Run `44989154812`: CANCELLED on stale head `de141fe9fa13508f56136f96e6d2e70f8a3f29b4`; excluded from verdict evidence.

## Repo-rule compliance

Read-only review. No product files changed, no local tests run, no workflow edited or dispatched, and no PR comment, merge, or close performed. Planning evidence only is published to the verified `baseharbor-plan` repository (`origin` URL `https://github.com/mcpdev80/baseharbor-plan.git`). BaseHarbor remote `lane-origin` resolves to `https://github.com/mcpdev80/baseharbor.git`.

## Cleanliness

Before review: PID `2462090`; `docker ps -a` returned only the header and no containers. No container or compose project was started.

After review: pending final witness.

## END codex-rev2-1736 BLOCKED

REQUEST CHANGES: pairing assertions do not establish the requested global two-way admission invariant. Candidate SHA `6cec31ff6737d1b409e9c9e3b1f3597fa0cb686b`.
