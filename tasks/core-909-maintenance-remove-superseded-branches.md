---
id: core-909
areas: [maintenance]
type: maintenance
release: maintenance
version: ""
parent: ""
owner: mcpdev80 (core-909 local Qwen maintenance)
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#909"]
source_updated: "2026-10-15T16:47:13Z"
labels: [kind/maintenance]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-909 · Maintenance: safely remove superseded branches #task #release/maintenance #status/active #view/active #area/maintenance #kind/maintenance
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-909 local Qwen maintenance) · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [maintenance](../releases/maintenance.md)  
**Depends on:** none  
**Owner:** mcpdev80 (core-909 local Qwen maintenance)  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#909](https://github.com/mcpdev80/baseharbor/issues/909)
<!-- /generated:links -->

## Goal

Remove verified-superfluous branches; every remaining branch has a justified owner, work or evidence purpose. Not a product feature or release blocker.

## Scope

- Maintainer decision (2026-10-15): remove all archived remaining branches except `main`, `develop`, `feature/kubernetes-runtime-foundation`, `test/kubernetes-adoption-contract-demo` and any macOS/Darwin work. A complete mirror backup including the original branch refs is held by the Maintainer locally (path recorded in the source snapshot). 14 branches had already been removed per the local deletion log; 37 further refs were planned for archive-backed removal. This is deliberate archive cleanup, not proof that every historical change is in develop; open bugs stay open and their old sources remain in the mirror. Release tags and Actions evidence are not deleted.
- Rules before each removal: each branch exists in the mirror at exactly the current remote SHA; new/changed branches, new open PRs and new macOS/Kubernetes work are kept; historical candidate/evidence refs leave the remote inventory but keep their Git states in the mirror; keep the mirror safe for later verification.
- Already done (per source): draft #861 closed (selective integration via #837); Renovate PRs #724/#779/#782 and single updates #725/#778 closed (the pending host-trust checkout/Alpine update is **not** delivered and stays visible in the dependency dashboard, see [external tooling](../migration/external-tooling.md)); duplicate dashboard #17 closed; #616 kept open (real Kubernetes pre-freeze proof); core-750/751/752 and core-754/766/815 kept open.
- The 55-branch inventory with audit SHAs (develop `33b7ca94b42cc45e908c0d964cfbe0cc8349f231`, main `54acc4b66715681213788fdba395a569ddc95a1b`) is in the [source snapshot](../migration/source-snapshot/baseharbor/909.json).

## Acceptance

- Re-check branch heads, open PRs, new commits and active sessions before execution; never delete an old audit SHA blindly.
- Preserve main lines, open #616 pre-work and active task branches; do not merge branches merely to get rid of them.
- Remove only confirmed candidates individually at their unchanged SHA; no wildcard deletion or force-push.
- Afterwards re-read the remote inventory and document every actually removed ref with its original SHA and reason.
- No claim "branches cleaned up" while only the inventory exists. No new product/release CI runs for this hygiene task.

## Required checks

- Remote branch inventory before and after; mirror presence per SHA.

## Dependencies and file ownership

- No task dependencies. Needs authenticated GitHub access for ref deletion.

## Autonomous local execution

- Preferred assignment: local Qwen with authenticated `gh` and access to the Maintainer's existing mirror backup. Verify the repository path, `gh` identity and mirror availability before execution. A cloud-only connector without ref-deletion/mirror access is not an adequate execution environment for this task.
- Own only this task's planning handoff, local audit/deletion record and individually qualified obsolete remote refs. No product source, CI/workflow, live ruleset, planning config or active implementation branch edits.
- Re-read open PRs and current planning claims directly. Protect every new/current task branch, both main lines, #616 and Kubernetes/macOS work. Do not rely on the historical eight-branch inventory as the current state.
- Complete the inventory, exact-SHA mirror checks, authorized safe removals where still needed and per-ref audit before/after as one task. If cleanup was already executed, recover the real existing deletion log instead of pretending to delete refs again. No new product CI is required. Publish render/check-validated planning closeout through the normal Maintainer acceptance boundary.
- Independent of wizard CI readiness and the pilot cost report; it may run alongside both. Do not remove their active refs or evidence origins.

## Handoff

- Observed 2026-10-15T20:35Z during this migration: the remote has 8 branches (`develop`, `main`, `feature/kubernetes-runtime-foundation`, `test/kubernetes-adoption-contract-demo` and active task branches `task/895-review-protection`, `work/v0.4.26-893-pr-check-enforcement`, `work/v0.4.26-896-isolated-pr-runners`, `work/v0.4.26-910-read-context`). The removal therefore appears executed; **the per-ref deletion record (original SHA + reason) is not yet documented** — record it here to accept this task.

### Execution record (core-909 local Qwen maintenance, 2026-10-16)

- Environment verified before any action: working checkout `/home/marcel/dev/projects/baseharbor` (product repo, remote `mcpdev80/baseharbor`, authenticated `gh` as `mcpdev80`); planning repository edits made only in `mcpdev80/baseharbor-plan`; mirror present at `/home/marcel/baseharbor-branch-backups/20261015-183126/` (`repository.git` bare mirror, 55 `refs/heads` entries, `branches.json` remote snapshot, `deleted.json`, `deleted-second-pass.json`, `pull-requests.json`).
- **No branch was deleted during this session.** The authorized removal had already been executed on 2026-10-15T18:32Z/18:35Z (two logged passes, 14 + 37 refs). This session recovered and verified that real deletion log instead of re-deleting anything; nothing was simulated.
- Current remote inventory (2026-10-16T~10:20Z, `git ls-remote --heads origin`, 17 refs): main lines `main` `54acc4b6…`, `develop` `9766dcb8…`; protected kept refs `feature/kubernetes-runtime-foundation` `a7c6371a…`, `test/kubernetes-adoption-contract-demo` `875dc5ed…` (both still at their audit SHAs); new refs created after the 2026-10-15 decision/mirror: `docs/ci-minimum-sufficient-verification` (open PR #957), `pilot/core-752-953-policy-proof` and `runtime-validation/ci/core-752-policy-proof` (core-752 evidence, commit today), `pilot/core-893-trusted-base` `a867f3c9…`, `pilot/core-893-validation-only` `bf887413…` and `pilot/core-893-unresolved-negative` `6eaae0d2…` (exact PR #943/#944 evidence heads recorded in core-893 notes), `pilot/core-893-public-owner-base`/`-contract`, `pilot/core-893-event-refresh-base`, `pilot/core-893-policy-exact-verification`, `pilot/core-895-green-review`, `pilot/core-895-missing-check` (active sessions today; `pilot/core-895-missing-check` updated `860e83f1..2b45015a` during this fetch), `pilot/pr-impact-924`. Open PRs: #616 (draft, Kubernetes pre-freeze, kept), #957 (wizard CI readiness), #958 (pilot cost evidence) — all heads kept per task rules. The four 2026-10-15 active task branches above are now gone because their PRs #930/#932/#933/#934/#935/#953/#955 merged (normal merge-flow pruning, verified via `git fetch --prune`); no unversioned local files were touched.
- New-post-decision refs are **not** part of the 2026-10-15 authorized set; under the standing rules (new/changed branches, new open PRs and new Kubernetes/macOS work kept; no wildcard deletion) none qualified for removal today. No macOS/Darwin branch exists on the remote.
- Evidence verification performed three-way, all 51 logged refs: (1) each original SHA exists as a commit object in the mirror and the mirror's `refs/heads/<branch>` equals that SHA — 51/51 exact, zero mismatches; (2) each SHA matches the remote snapshot `branches.json` taken immediately before deletion — 51/51; (3) each SHA matches the audit table in source issue #909 — 51/51, and the 55-row inventory reconciles completely as 51 deleted + 4 kept, with no inventory branch left undeleted on the remote. Release tags untouched (59 tags on remote).
- Per-ref deletion record (original SHA + reason) recovered from the Maintainer's local deletion logs at the mirror path above. First pass (2026-10-15T18:32Z, `deleted.json`, 14 refs, per-ref reasons from the log, translated to English here):

| Branch | Original remote SHA | Reason (deletion log) |
| --- | --- | --- |
| `fix/v0.4.21-source-preflight-16a7e166` | `16a7e16636b91c9d7fb657da272a299c2148f3ee` | Commit history already contained in a kept line |
| `release-publish/v0.4.21` | `d8957641ac3bfd1ccf6758c1298777418f0c11df` | Commit history already contained in a kept line |
| `renovate/actions-checkout-6.x` | `47e352c396ca213bb208e61628b2230db153146a` | Closed partial PR, documented as superseded |
| `renovate/actions-configure-pages-6.x` | `386b1846437ad965b1e7fb0196fd075b32a08210` | Closed partial PR, documented as superseded |
| `renovate/actions-deploy-pages-5.x` | `54a33886c424e24c4785f469362e39553058874b` | Closed partial PR, documented as superseded |
| `renovate/docker.io-library-alpine-3.x` | `99ef034636399532c6d0e0e9150816bf48257b82` | Closed partial PR, documented as superseded |
| `renovate/pin-dependencies` | `4103a31230d93fe08f2dd8f3740b89978d896cba` | Closed partial PR, documented as superseded |
| `work/v0.4.24-bugfixes-852-855` | `b6dbb4cf8e6e096650db27a4820bbdc1bb6e1b77` | Closed partial PR, documented as superseded |
| `work/v0.4.24-bugfixes-858-860` | `3ad3de4138eedc64fd3e49ac12c2f6a11c834214` | Closed partial PR, documented as superseded |
| `work/v0.4.24-cli-node-integration` | `4da797e1c792624bbd09c6950c686516d7a703f6` | Closed partial PR, documented as superseded |
| `work/v0.4.24-cli-target-tui` | `ad9ad5a4fb2a52c6ee66f451c08eee9cf21e9005` | Closed partial PR, documented as superseded |
| `work/v0.4.24-openbao-keycloak-upgrades` | `53df05ca93596247f102a9aee9faff44dd80289d` | Closed partial PR, documented as superseded |
| `work/v0.4.24-provider-bindings-1c` | `91eb8af49b624a64a2cc6389be0e8288c4f02105` | Closed partial PR, documented as superseded |
| `work/v0.4.25-contract-minimal-core` | `3c9c1ed8ffbd0cc3578b2726dd5f378fe0808de3` | Commit history already contained in a kept line |

- Archive-backed pass (2026-10-15T18:35Z, `deleted-second-pass.json`, 37 refs). Shared reason: deliberate Maintainer archive-cleanup decision of 2026-10-15 (issue #909) — archived remaining branch outside the kept main lines and Kubernetes/macOS work; each ref individually deleted at its unchanged current remote SHA after exact-SHA mirror verification.

| Branch | Original remote SHA |
| --- | --- |
| `approved-candidates/v0.4.23` | `d71a440a27a1d08c50b1148ac2affa31536e9334` |
| `feature/claude-support` | `5f11cf5a5da1dc85d9ed09c2ce2a2cb5f52d6b22` |
| `feature/549-memory-preflight` | `da10f8ee1707c22f89e404495b9c272818fec5cc` |
| `feature/605-durable-key-value` | `4c7eb0290c83726c50abb1b852d1c9e65fe5c1a1` |
| `feature/606-document-contract` | `58ae53a6fcc9b9f1c4a9175cc7c5244d8b4d0904` |
| `fix/v0419-guided-exposure-detection` | `c987fab50720e9230dd497efdfc00791e1ac2b7e` |
| `fix/v0419-identity-workload-env` | `a22d9f3ecf0de7866030b3417d79e66737a939ba` |
| `fix/v0419-podman-control-plane-security-lookup` | `e1daff435c86526c7f9741a9545510e9cc0ff7fe` |
| `fix/v0419-podman-restart-target` | `aee9d5cccfdf0b025389779cdd466b11053c9265` |
| `fix/v0419-podman-security-quadlet-lookup` | `f93774f8fe68b7b22ca8ab8fa541fe698b18f836` |
| `fix/v0419-readability-ratchet` | `7bf3e51b3497a822fb3fb93566499d9eb340136b` |
| `fix/v0419-restore-ignore-incomplete-deployment-records` | `2933e4152d8b99480a8d04d437c5b6008f499d9c` |
| `fix/v0419-restore-metadata-stable-deployment-r2` | `d89f08b64df2e29e3ae6397aabf3d19cfd513067` |
| `fix/v0419-restore-pending-deployment` | `624638c089a437fff9478dbf60f14e1822130f01` |
| `fix/v0419-restore-persist-pending-first` | `579dfa6d5b58ec9728f85aa8226f994abbd6e90d` |
| `fix/v0419-restore-runtime-init` | `101261a97a0568ef61f01e78dd60d886431fe313` |
| `fix/v0419-restore-stable-deployment-record` | `318775704b1b9138b68769664aea65831aa052dc` |
| `fix/v0419-workload-failure-state` | `d96c77b661f7d3886798bdbc74b01ebfc84a798a` |
| `fix/750-source-neutral-inspect-summary` | `4c810c9f749eaaba9f755c628df22770826c3e05` |
| `fix/750-source-neutral-inspect-summary-v0421-r2` | `e73bc60595a9426242ec1cd1e0883377cf91ab91` |
| `fix/750-source-neutral-inspect-summary-v0421` | `7ffe2417587d0cab80f04808e64187d72b3b0668` |
| `fix/751-capability-import-noise-v0421` | `aabd82ff6cb7f6a55f33001638e51e53dfc7f2a8` |
| `fix/752-default-instance-reconcile-v0421` | `70292f0cd436fdeb170652e26e6c5e228da23c1d` |
| `qualification/v0.4.24-evidence-863-38015430253` | `45aae6ca59688e05461e22eabf190be8122ddd5f` |
| `release/v0.4.19-final-prep` | `8ed294b40ce2c2bd40074945de8ce39da288f25a` |
| `release/v0.4.19-final-prep-r2` | `4103c8e37423cabd5a029d2a3c74b169cca363b0` |
| `release/v0.4.21` | `b39a8b2c6eeda93470ba3b8ffe3b8eb3f01f5ba6` |
| `release/v0.4.25` | `1ed6a057bc9e58c2d98277287aa723109318a8f6` |
| `release-candidate/v0.4.25-final-f325b93c` | `f325b93c589d8b807f44dd0086636aabe83fcd65` |
| `supplemental-validation/v0.4.21-2c56942` | `2c56942b0c3ad1b92d69b5c69113f03004b16def` |
| `test/v0419-deployment-cleanup` | `7857b8e7552179c4dffeb2df0e6b903775e862f2` |
| `test/v0419-shared-backend-destroy-regression` | `3da62e8b7e2b469e763ca0951d678083b1a5f7b3` |
| `validation/evidence/v0.4.25-api-recovery` | `f43dec68246912d8ecba41ad671314c2f8f4cc62` |
| `work/v0.4.24-etcd-dcs-recovery` | `c06cbd6de53c828ee407e970548452ed55c92837` |
| `work/v0.4.24-integrations-docs` | `73cb37a8310522925654c3543bf73e799a807333` |
| `work/v0.4.24-parallel-integration-qa` | `8cf91e25cf80c8831acb833500cf0bbcc27ae64b` |
| `work/v0.4.24-provider-runtime-session2` | `62ea7e887e4ab55ff6e852dddaf9a1adec011dc6` |

- Checks: this is a hygiene task only — no product code, CI/workflow, ruleset, tag or release changes; no product/runtime test runs started; no force-push. Planning render/check executed before this publication.
- Handoff to Maintainer acceptance: authorized cleanup is complete and evidenced; every remaining remote ref has a protected purpose (main line, kept Kubernetes work, open PR head, or active-session/evidence origin). Retain the mirror safely for later verification.
- Status note: the card remains `#status/active` because the planning validator requires at least one PR for `#status/review` and this hygiene task legitimately has none (no product PR exists or should be fabricated). All execution work and the per-ref evidence above are complete and ready for Maintainer acceptance.
