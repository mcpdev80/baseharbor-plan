# ROLLE: REVIEW — PR #1820 preflight

Read-only disposition, 2026-11-27. No product edit, rerun, PR comment, or merge was performed.

## Exact refs and latest Hosted run

- PR #1820 is OPEN, non-draft, base `develop`, head `8f6b2444bdc9baabf4f492e930533c7c36406979` (`fix/broker-build-identity`), `MERGEABLE` but `BEHIND`. The live `develop` tip read was `ea5218d72e263f21e79853b679af50074dab8c25`; compare reports 36 behind / 18 ahead. The full PR ref matched the API head.
- Latest Hosted pull_request run on this exact head is `45710380590`, completed SUCCESS. `PR · Trusted Plan`, Go unit packages/CLI shards, `PR Selected Checks`, and the selected Docker data-capabilities runtime job succeeded. The selected Native job and Targeted HA Podman job were skipped; this run is not evidence that both Docker and Podman gates executed.
- Therefore the latest run is **not Trusted Plan-blocked**: its Trusted Plan job succeeded. The PR is nevertheless **chain-blocked and stale-base**, because #1819 has not landed and #1820 is behind current develop. In addition, the current tree fails the 0428-271 content contract below, so the green aggregate is not candidate qualification.

## Contract and current write-set

Card 0428-271 requires `verifyRuntimeBrokerBuildIdentity` to reject a same-version runtime reporting a different concrete commit, with regressions for matching commits, differing commits, and the permitted `dev`/`edge` case with an empty commit. The card's intended write-set is `cmd/baha/app_broker.go` and `cmd/baha/app_broker_compat_test.go` (plus the already separately handled trusted catalog row).

The current `develop...#1820` diff has only four files, all from the Perses export consumer: `.github/workflows/pre-release-runtime-suite.yml`, `internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go`, and `internal/metrics/perses_dashboard_provision_test.go`. It has no net change to either broker file. At the current head `verifyRuntimeBrokerBuildIdentity` still discards `expectedCommit` and `actualCommit`; the current compatibility test still expects a wrong commit to be accepted. Thus the candidate's visible write-set does not implement the card's required behavior and includes the other card's 0428-181 payload. This is a content/scope blocker in addition to sequencing.

## Forward-only route

The card already calls for a clean fresh cut after #1819 merges. Follow that: wait for #1812 to land first, then #1819; verify both landings from GitHub and fetch the resulting live `develop`. Create a fresh 0428-271 branch from that exact tip under the assigned canonical 0428-271 lane identity. Reapply only the broker identity implementation and its tests; do not carry the 0428-181 Perses files or their foreign commits into the fresh diff. Preserve the separate 0428-274 catalog prerequisite: its row for `source.cmd_baha_app_broker_compat_test_go` must already be in trusted `develop`; do not add a candidate-side substitute. Required tests must prove same version/same commit succeeds, same version/different concrete commit fails, and the allowed `dev`/`edge` empty-commit case succeeds. Then obtain fresh exact-head Hosted qualification, including Trusted Plan, required Go/unit checks, and all card-required runtime gates on the final head. Skips do not count as executions; follow the current distinct exact-head run rule before review. Stop and report any new conflict rather than dropping either card's scope.

## Card and PR fields

Card 0428-271 is `wait`, links PR #1820, and names `w69-0428-271-brokerid2`; that is the historical lane recorded for the card, while the wait reason says it has been released. The PR branch name is `fix/broker-build-identity`; this is not by itself evidence of a current active owner. `depends_on` correctly names the 0428-274 catalog baseline but omits the separately mandated #1819 merge gate. The wait reason does say “clean fresh cut only after #1819 merge,” so prose and dependency metadata disagree. Record #1819 as a formal prerequisite before the next lifecycle transition; do not alter the card in this preflight.

The 0428-274 baseline card is `wait` with no owner or PR recorded. Its prior record states that the broker compatibility-test source row was included in the authorized catalog batch. Verify that row remains on live `develop` when preparing the fresh candidate; the prerequisite is a landed trusted-base row, not a row embedded in #1820.
