# Historical pull-request cleanup — 2026-10-18

Administrative source review requested by the Maintainer. Planning remains authoritative in this repository; closing historical proposals does not accept product tasks or qualify a release.

## Closed as superseded

Reviewed Demo main: `a92347900ed4d1015d9bcde3d265cf9326664a40`. The old heads diverge from main; these are source-level supersession decisions, not claims of Git ancestry or merges. Original PR descriptions and source branches are preserved.

| Demo PR | Preserved head | Reason |
| --- | --- | --- |
| [#61](https://github.com/mcpdev80/baseharbor-demo/pull/61) | `17104fc959bb9857ac54e92f13865609d1bfc715` | Superseded by the current suite registry and acceptance runner, prebuilt-binary/runtime-image source checks, and config-matrix/MCP/agent gates. The suite layout has since evolved; this old normal/operations proposal must not be merged over it. |
| [#62](https://github.com/mcpdev80/baseharbor-demo/pull/62) | `cb3554a2ebefb0cc53435d18388fafa641f8400d` | The current PR file comparison is empty (zero changed files). The maintained suite implementation already lives on main; this duplicate proposal has no remaining patch. |
| [#86](https://github.com/mcpdev80/baseharbor-demo/pull/86) | `2f90fe281119b06ce2f78cc29813833d0068d644` | Superseded by the maintained static shell-ux gate: tests/gate-resources.json declares class static, shell-interface profile and no capabilities; tests/shell-ux/run.sh uses isolated XDG directories and an explicit shell-ux-static Target. |
| [#104](https://github.com/mcpdev80/baseharbor-demo/pull/104) | `c7fa3fce9535c7749a166a900d09781bd99d42fc` | Superseded by the current recovery HTTPS exposure contract, bounded identity capability/check readiness, and canonical gateway security checks. The old aggregate .ready polling is not the current status contract and is not being ported back. This closure does not assert that every old polling loop was merged. |
| [#106](https://github.com/mcpdev80/baseharbor-demo/pull/106) | `fb11ab5cd9613dfa6269a134150e5fd4db866ad8` | Superseded by the explicit HTTPS exposure contract in tests/backup-restore/run.sh. This older patch declares HTTP and must not replace the maintained HTTPS contract. |

## Retained implementation PRs

| PR | Preserved head | Planning authority | Disposition |
| --- | --- | --- | --- |
| [Console #3](https://github.com/mcpdev80/baseharbor-console/pull/3) | `fd2cfe7530c9e8ba62481f31efed2c70ee5dc8df` | [console-2](../tasks/console-2-live-core-adapter-workflow-proofs.md), v0.4.28 | Keep open: live adapter/browser integration is not incorporated into main; comparison reports 64 head-only commits. Reconcile with current contracts and qualify the eventual candidate before acceptance. |
| [Node Connector #4](https://github.com/mcpdev80/baseharbor-node-connector/pull/4) | `365094890c091fbf627c9d71c94e44751018e6e9` | [nc-3](../tasks/nc-3-core-enrollment-remote-runtime-acceptance.md), v0.4.27 | Keep open: enrollment/mTLS/remote lifecycle implementation is not incorporated into main; comparison reports 60 head-only commits. Reconcile and qualify the eventual candidate before acceptance. |

Consumer main comparisons used Console `4724d9962486de5c9f4d226a8a27edcaf8da2fcc` and Connector `813f08a307f2357f2e16ae9307ea247186ea7dda`. Historical qualification links in these PRs retain their original exact-source scope; this review does not establish compatibility with current BaseHarbor.

## Boundaries

- Current v0.4.26 implementation PRs and Kubernetes draft BaseHarbor #616 remain open and unchanged by this cleanup.
- No source branch, commit, ecosystem pin, task claim, task status or acceptance evidence was removed or changed.
- No merge, product test run, tag, release or publication was started.
- Verification is read-only source/diff comparison plus post-write PR-state checks, not new runtime qualification.
