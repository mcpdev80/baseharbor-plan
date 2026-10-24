# Native acceptance and consumer freeze — 2026-10-24

## Verdict and authority

**BLOCKED: no current native acceptance or consumer freeze is claimed.** All independently executable source, lineage, workflow-route and historical-receipt checks below are complete. A fresh, exact-input Podman receipt is still missing; final consumer merges/pins and W1 journeys remain pending.

Marcel explicitly assigned session 2 (`d48643e22049`) this bounded scope and lifted the old stop only for it. Session 1 owns shared CI implementation, develop integration and every product merge. Session 3 owns independent review and evidence checks. No merge, tag, release, deploy, complete pre-release, worker or daemon was started here. No product file, shared Core CI file or v0.4.27 file was changed. Planning claim: [`e12951018409925818b5b3f1300090402f6fdb41`](https://github.com/mcpdev80/baseharbor-plan/commit/e12951018409925818b5b3f1300090402f6fdb41).

Read: current planning and product AGENTS/development/contribution guidelines, core-923, release preparation, v0.4.26 release note and the Codeman [handoff](../codeman-2026-10-24/HANDOFF.md). Planning confirms core-921, core-922 and core-900 accepted. The operational prerequisite is the unfinished freeze/CI chain, not a missing implementation of those accepted predecessors.

Local Ops files f53/f54, q116 and CX-DEMO121R4 were not available: `/home/marcel/dev/baseharbor-ecosystem` is absent in this environment and the published planning tree contains none of those files. Their reported contents are leads from HANDOFF, not independently inspected evidence. Foreign worktrees and existing changes were preserved.

## Immutable candidate inventory

| Surface | Current candidate | Actual pins | Existing CI and review boundary | Next integration trigger |
| --- | --- | --- | --- | --- |
| Core develop | `65aa063e90767c85af976081c100be1817370e67` | W1 anchor remains **`1861ed07888a1ec22c218ca491d23ee54f48e261`** | Shared CI/integration belongs to session 1 | Final accepted CI chain and C/D/U/K graph integrated; do not silently replace C with develop |
| [Demo #121](https://github.com/mcpdev80/baseharbor-demo/pull/121) | `f57c8b6e5ff39d0873df62b26272962765e88d6e` | Core C | No Actions run found for this head. Historical green run below is not input-equivalent. Independent receipt review by session 3 remains required | Exact Podman run succeeds including cleanup; coordinator may then integrate and record actual merged D |
| [Console #9](https://github.com/mcpdev80/baseharbor-console/pull/9) | `6017de2845fa3e4e408c69038a0a5bdd7e82cad9` | C; historical Demo `25c319697fd3d89d894943e0f44cd3d5dde8b198` | [Run 40078839364](https://github.com/mcpdev80/baseharbor-console/actions/runs/40078839364), attempt 1; [source-quality job 120827948192](https://github.com/mcpdev80/baseharbor-console/actions/runs/40078839364/job/120827948192) success; actual browser/Keycloak/Core HTTP job `120827949192` **skipped** | Only after actual D: repin Demo to D, qualify new candidate, independent review; coordinator integrates to actual U |
| [Connector #10](https://github.com/mcpdev80/baseharbor-node-connector/pull/10) | `e832d5651752121dea9484e18422d3e6459f9a72` | C; historical Demo `25c319697fd3d89d894943e0f44cd3d5dde8b198`; historical Console `69d1d14007fa43dc0c0457c3347280be7f802818` | [Run 40081652928](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40081652928), attempt 1; [source job 120836283698](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40081652928/job/120836283698) success; enrollment `120836284408` and encrypted transport `120836304169` **skipped** | Only after D and U: repin both, qualify new candidate, independent review; coordinator integrates to actual K |

Console #9 and Connector #10 each compare as **ahead 1 / behind 0** against current main, with exactly one changed file, `integration-candidate.json`. No current lineage or source reason requires replacing Console #9. Continue it after D unless the coordinator identifies a new ownership/conflict constraint; a replacement would need explicit rationale and the same verified D. The superseded #9 described by Connector #10 is **Connector #9**, not Console #9. No PR was closed here.

After K, session 1 reconciles [Core #1050](https://github.com/mcpdev80/baseharbor/pull/1050) against the actual immutable D/U/K blobs using `scripts/ecosystem_release_pins.py`. Verify required ancestry and all graph cross-links; never precompute a prospective squash SHA. Existing source-only successes do not qualify future repins or skipped native/browser jobs. No final pin was written here.

## Podman route and exact missing access

Existing `targeted-demo-acceptance.yml` supports `workflow_dispatch` with independent exact Core/Demo refs, runtime and gate. Its reusable `pre-release-runtime-suite.yml` uses **ubuntu-26.04 for Podman** and prepares the verified rootless runtime. The two workflow blobs are byte-identical between C and current develop:

| Workflow | Blob |
| --- | --- |
| `.github/workflows/targeted-demo-acceptance.yml` | `67485c03b01eb26ce2d2f878676144a4563d0434` |
| `.github/workflows/pre-release-runtime-suite.yml` | `5251afcb31478b71dea81d91a255a1df9b03e10c` |

Use [demo121-podman-dispatch.json](demo121-podman-dispatch.json) at `POST /repos/mcpdev80/baseharbor/actions/workflows/targeted-demo-acceptance.yml/dispatches`. `ref: develop` selects the verified workflow wrapper; the input `ref` fixes the tested Core to C. Re-read wrapper source and concurrency before dispatch if develop has moved. This is a single existing gate, not a complete pre-release. Backup/restore is necessary here because the missing claim is real recovery plus final owned cleanup; cheaper source checks cannot prove either on rootless Podman.

The missing access is an **authenticated GitHub Actions workflow-dispatch operation for this repository**. The current GitHub MCP tool catalog exposes GET/run/artifact/log reads and rerunning existing jobs, but no dispatch operation. This environment has no Docker/Podman binary/socket, no configured SSH host or local Ops checkout. Runner administration is not exposed by the connector; a rejected runners-endpoint read is not evidence that runners are offline. Existing workflow source and historical runner execution establish the hosted route.

A browser fallback reached a signed-out GitHub page; secure authentication was declined. Marcel subsequently explicitly requested GitHub MCP. No further browser action or login retry follows. Do not reuse/rerun the old job and relabel it as #121: reruns keep its original inputs. No new CI workflow, branch-trigger workaround or gate weakening was introduced.

Coordinator request with exact input payload: [core-923 comment 6386350458](https://github.com/mcpdev80/baseharbor/issues/923#issuecomment-6386350458). Receipt audit: [Demo #121 comment 6386427876](https://github.com/mcpdev80/baseharbor-demo/pull/121#issuecomment-6386427876). Freeze ordering/review coordination: [Core #1050 comment 6386436562](https://github.com/mcpdev80/baseharbor/pull/1050#issuecomment-6386436562). An existing authenticated coordinator route can unblock execution without asking Marcel to relay task status.

## Historical proof: authentic, incompatible with current candidate

[Demo run 39990941852](https://github.com/mcpdev80/baseharbor-demo/actions/runs/39990941852), attempt 1, genuinely executed:

- [Podman job 120542211968](https://github.com/mcpdev80/baseharbor-demo/actions/runs/39990941852/job/120542211968): native recovery and cleanup success.
- [Docker job 120542212240](https://github.com/mcpdev80/baseharbor-demo/actions/runs/39990941852/job/120542212240): native recovery and cleanup success.

Podman artifact `12518384969` was downloaded through GitHub MCP. Local SHA256 equals the GitHub artifact digest: `302be6ce6984d1cb2bac80cb5604161dd1ae47facfa9f992dc790904dc7f76e4`. Its `recovery-qualified.json` binds Core C and Demo **`25c319697fd3d89d894943e0f44cd3d5dde8b198`**, retained recovery mode, run/attempt 39990941852/1, success and cleanup success, `pre_release_ready: false`. Its cleanup-preparation scope receipt records `--unpause-owned`, success, empty accounted/errors. All recovery verification fields are true. Those facts qualify that historical execution only.

[input-comparison.json](input-comparison.json) compares complete immutable tree inventories directly, avoiding a misleading three-dot diff on diverged histories: **87 blobs versus 87**, none removed, exactly two changed:

- `scripts/failure-runtime-diagnostics.sh`: historical Podman total/per-call budgets **90s/60s**; candidate #121 **60s/20s**. This changes real cleanup execution inputs.
- `.github/workflows/v0424-targeted.yml`: artifact set differs; current workflow replaces the cleanup scope receipt upload with the runtime image-cache log.

Podman cleanup preparation ran from `17:25:40.1577219Z` to `17:26:11.7272407Z` on 2026-10-23 (31.57s aggregate). That does not prove each subprocess fit the new 20s ceiling. Equal Core pin and remaining source files are insufficient for input-equivalence. No canonical verifier acceptance exists for the changed helper; **reuse is rejected**. Docker's effective helper budgets remain 60s/20s, but byte-identical verified inputs were not established for the complete gate, so no fresh Docker PASS is inferred either.

## Bounded source checks actually executed

At exact Demo #121 source, existing tests only:

| Existing test family | Result | What it proves |
| --- | --- | --- |
| `tests/guided/*helpers_test.py` | 4 tests, PASS | Picker/consent/state helper behavior |
| `tests/data-capabilities/*helpers_test.py` | 7 tests, PASS | SQL/sentinel ownership helper behavior |
| `scripts/test_owned_runtime_diagnostics.py` | 20 tests, PASS, 84.710s | Existing bounded cleanup, foreign ownership, cancellation and error-preservation regressions |

These **31 source regression successes are not native runtime evidence**. No new tests were added, no full matrix was run, no product source was changed. Console and Connector CI results were inspected rather than redundantly rerun. Planning render/check passed with 0 errors and 5 existing warnings; all 47 existing planning tests passed. No v0.4.27 canonical note or product input was changed. Final publication is re-read and checked against the exact remote source.

## W1 execution and acceptance checklist

Start only after the CI chain and actual consumer pins are integrated and independently checked. Keep Core C fixed. Use actual final D; do not substitute the earlier Demo branch or a future unmerged candidate. Existing targeted gates provide the required coverage:

| Gate | Runtimes | Existing source and observable proof |
| --- | --- | --- |
| `guided` | Docker, rootless Podman | `tests/guided/new_edit.py`: real PTY New with zero needs, Edit, No/Cancel/EOF preservation and CLI JSON/MCP footprint parity |
| `data-capabilities` | Docker, rootless Podman | `tests/data-capabilities/new_edit.py`: New SQL, remove/re-add, provider switch to shared/back, persisted SQL markers and sibling/shared provider preservation |
| Acceptance EXIT cleanup | Both, part of those gates | `scripts/acceptance.sh`: owned-resource preparation, bounded destroy, foreign sentinel checked after actual Core teardown and only then removed by its exact owner |

Collect run ID/attempt, workflow source, exact C/D and final U/K graph, runtime setup/rootless proof, actual selected step result, gate manifest, `new-edit-zero.json`, `new-edit-sql.json` where applicable, footprint parity output, foreign-check/removal outcomes, and cleanup evidence. Inspect downloaded immutable artifacts; require actual execution, truthful exit/outcome and zero unexplained residuals. A green overall run with skipped requested work does not pass. Use the existing release evidence verifier against the actual origins and input fingerprints before reuse. Do not run a reference/full journey or complete matrix merely to replace these bounded gates.

Current W1 state: **not executed for the final graph**. Native New/Edit, SQL/provider changes, negative consent, data/shared preservation and cleanup remain open until those gates actually run. Session 3 must independently review receipts and compatibility; this report is the implementation owner's evidence audit, not independent approval.

## Resume triggers

1. Authenticated Actions dispatch becomes available (or coordinator posts the exact requested run): observe to completion through GitHub MCP, download/verify receipt, diagnose only actual failures, hand exact verdict to session 3 and coordinator.
2. After actual Demo merge D: repin Console; qualify and hand off candidate SHA/CI/review to coordinator. No speculative pin write before D.
3. After actual Console merge U: repin Connector with D/U; qualify and hand off. After K, coordinator integrates final pins and CI chain.
4. After final graph integration: execute only the necessary Docker/rootless-Podman W1 gates, verify artifacts, publish full native acceptance result. Until then core-923 remains blocked, never accepted/closed.

END NATIVE-ACCEPTANCE-HANDOFF-2026-10-24
