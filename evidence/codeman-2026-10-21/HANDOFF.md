# Codeman handoff — BaseHarbor v0.4.26

Recorded 2026-10-21 UTC. **OWNER REQUESTED STOP.** This document and its patches are a handoff, not authorization to resume or publish. No product merge, product change or new CI run was started after that stop. Coordinate resumption with the Owner. Do not publish a pre-release, tag, promotion or Pages site.

**PRE-RELEASE READY: NO.** Component integrations and real native evidence exist, but three follow-up product corrections, final documentation, immutable consumers and complete final-candidate acceptance remain outstanding.

## Verified remote state at stop

- Product: `mcpdev80/baseharbor`, `develop` = **`30e112431b04a7e24e7e7e9ea76a3600e439a988`**.
- Planning before this handoff publication: `mcpdev80/baseharbor-plan`, `main` = `6a875f302e0107349f8ce643c7ce51a8aba4db9c`. The handoff publication will be a descendant; obtain its exact SHA from `main`.
- Open, **green but deliberately UNMERGED**: [#1030](https://github.com/mcpdev80/baseharbor/pull/1030), head **`446e0e82b965551df24446360f31440880ed7cae`**, base30e11243. [CI39630020500](https://github.com/mcpdev80/baseharbor/actions/runs/39630020500), attempt1: actual Workflow policy, Trusted Plan, Focused Python, planner, policy, executor and final `PR Selected Checks` all completed/success. Unneeded jobs are skipped, not qualified as PASS.
- No additional runtime was dispatched for the latest Demo fixtures. No final ecosystem matrix was frozen. No release/Pages publication occurred.

## Accepted integrations

| Work | Accepted PR / merge | Real CI / scope |
| --- | --- | --- |
| Core921 CLI/MCP registration | [#1026](https://github.com/mcpdev80/baseharbor/pull/1026), `fe2d0c4a8c1df2d15058e338abb78adeb4cc9b83` | [39621449266](https://github.com/mcpdev80/baseharbor/actions/runs/39621449266):17 required validations plus final; component/registration acceptance |
| Complete isolated Podman recovery | [#1027](https://github.com/mcpdev80/baseharbor/pull/1027), `213c15e43ac9f3c333ad5eabed202475eefb501f` | [39623691937](https://github.com/mcpdev80/baseharbor/actions/runs/39623691937):9 required validations plus final; genuine native recovery below |
| Independent exact Docker qualification | [#1028](https://github.com/mcpdev80/baseharbor/pull/1028), `00882c3c35dc1b1822095bec286cb5519fed53bc` | [39625993397 attempt2](https://github.com/mcpdev80/baseharbor/actions/runs/39625993397/attempts/2) |
| Exact native-proven Docker integration | [#1029](https://github.com/mcpdev80/baseharbor/pull/1029), `30e112431b04a7e24e7e7e9ea76a3600e439a988` | [39627285799 attempt2](https://github.com/mcpdev80/baseharbor/actions/runs/39627285799/attempts/2):9 required validations plus final |

Original **#998, #995 and #990 are CLOSED as superseded**, with original descriptions, source ancestry and prior failed evidence retained. Earlier CI recovery #1012/#1013/#1015/#1016 and ecosystem/Automatic fixes #1017–#1025 are already integrated. Original #1007/#1011/#1014 are closed as superseded. #616 is unrelated future Kubernetes architecture; do not silently make it a v0.4.26 native gate.

Trusted-base activation now functions. Do not reimplement the original missing planner logic or retry the old85e05 candidate unchanged. The generic strict repository/target/source/inventory/SHA-256/clean-merge verifier remains intact. Candidate self-qualification is not permitted.

## Real native evidence — keep scopes distinct

### Complete Docker eight-family acceptance

- Source **`c1337192e06e63f8210ace9e5687d8dc8f70f6d2`**, integrated through #1029 after independent policy acceptance.
- [Run39619782116](https://github.com/mcpdev80/baseharbor/actions/runs/39619782116), job119290584209: Repository109.43s, Backend73.78s, WorkloadOnly60.02s, Build90.45s, Multi4.88s, ControlPlaneRecoveryHA255.63s, Loki49.25s, Tempo20.39s. Eight tests/five packages PASS, zero skip/fail, one complete source/run.
- Rootless UID1001, Go1.26.9, exact source/image/binary equality, Doctor/reset/cleanup verified.
- Artifact12355416509; ZIP SHA256 **`dbec35c8fcc0101e3b9cfae79030061bb8346ffe77832cf93764887e5015d5a4`**. Independently downloaded/verified: `/workspace/scratch/2edf243f0f92/docker-c133-evidence.zip`.
- The Docker task explicitly requires the named repository test on the **final develop head**. Its implementation is integrated; final-head acceptance remains open. Earlier cancelled/partial runs are not replacements.

### Complete rootless Podman disaster recovery

- Source **`77eb9a120f46b42281198fcee1de788c9779be18`**, accepted through #1027; exact17 paths, independent full source review and clean target integration.
- [Run39605258769](https://github.com/mcpdev80/baseharbor/actions/runs/39605258769), job119239688725,230.76s, native test/package PASS without skips.
- Real SQL marker and secret restored; READY consumer; regenerated token/client certificate; owned cleanup; foreign volume ID/CreatedAt/labels unchanged, then separately removed by its owner.
- Artifact12348242787, SHA256 **`98db0dd357326383ddf88855748114330e4a5674d21e51d9cb0552db4c763a77`**.
- All three Podman planning slices are accepted. Old Qwen-only/native-missing handoffs are historical, not current blockers.

### Fresh public MCP bootstrap — candidate, NOT integrated

- Source **`f762f4480a2eb6b29ceebb35ae4032cb2ce7288c`**, tree `60a8ce186a573fb7277fc56f3ebdde55f4c86ad4`.
- [Run39626844187](https://github.com/mcpdev80/baseharbor/actions/runs/39626844187), **job119314164799 completed/success**,71.07s; test/package PASS, zero skip/fail; image, real SQL add, coreless execution, wrong/stale refusal and cleanup all pass. Some overall API run metadata was temporarily nonterminal; do not infer its conclusion from steps.
- Initial public Propose omits revision; Apply echoes the returned `proposal.Desired`. No private revision bootstrap. Explicit stale revision and Apply consent remain strict.
- Artifact12357012289, ZIP SHA256 **`a1c4270ffa109484a94064614cf4f62cffe493497c33db261fd7082f58c9ed12`**, independently downloaded and checked: `/workspace/scratch/2edf243f0f92/mcp-public-bootstrap-39626844187.zip`.
- Earlier native b31/39605072620 proves actual execution after private test bootstrap; it does not substitute for this new public-entry proof.

## Ready source candidates behind #1030

#1030 contains only76 added lines in planner/tests, binding these independently reviewed frozen sources. Its generic verifier and unrelated records are unchanged. Local policy checkpoint `815dfdba102c209ad7122e72afba88ae27f9b014`, tree `5c81ddca0c8bcc4a9597924f94708306e066c09d`; remote head446e is authoritative.

| Source | Exact scope | Existing mandatory checks |
| --- | --- | ---: |
| `f762f4480a2eb6b29ceebb35ae4032cb2ce7288c` |4M: app_machine_adapters.go, app_mcp_provider_edit_native_test.go, app_registration_921.go, registration_921_test.go |7, including machine-adapter and Core921 runner |
| `99901ff2e787157ffb5e8d7d5206cf21272bd6c3` |2M: application_provider_preferences.go, app_new_wizard_test.go; terminal Name delegation preserves cancellable reader |6, including actual app-new PTY runner |
| `c6dfb988bb4f1fd295b6beb950980bb257e3699a` |2M: app_edit_apply.go, app_edit_apply_test.go; truthful refusal before Execute, actual partial receipts retained |5, including mandatory Guided regression wrapper |

The earlier Edit source `2f32556c...` lacks the wrapper and receives **no exemption**: its original two atomic runtime requirements remain. Do not qualify that old head. The generic `wizard-app-edit-tests` includes an unconditional real Docker test; do not call that profile a lightweight unit-only test. The frozen c6df wrapper executes refusal, partial-result and destructive/shared guards via existing `cli-guided-tests`.

Local validations: planner94, utility20, executor69, genuine positive/negative Git proofs for all eight records, policy19/Actionlint. MCP Core5+bootstrap9+SDK14, New14, EditGuided7 events pass. Terminal actual CLI single No/Cancel/EOF preserves source/state; this is process evidence, not native Docker/Podman evidence.

After authorized resumption: accept #1030 only while exact head/checks remain valid, then **separate normal clean integrations** of the three source candidates into the actual accepted target, each with its expected SHA and selected CI. Do not publish the combined private preview as an eight-file shortcut; exact source inventories are separate.

## Unpublished documentation and private combined Core preview

- `baseharbor-docs-213c`: clean local commit **`0c8a26c8e9c9be6952f3d5864a99d2dfed9d8e2b`**, tree `58379c9a4d88f8deaf859407aab018691f6c0ded`, parent213c. Exactly16 docs paths: README/CHANGELOG, EN/DE applications/needs/tutorial/index/release notes, both MkDocs configs.
- Strict EN/DE, audit158 language pairs/17,749 references and all three generated reference/coverage checks PASS. Unreleased stays empty; v0.4.26 candidate is not described as published; v0.4.25 remains public baseline. Recovery preferences remain persisted; only detached retirement projection is empty.
- Use `docs-16-paths-unpublished.patch` from this handoff, SHA256 in inventory. **Do not import obsolete61d6 ancestry.** Merge docs normally after actual product corrections; verify final references/Pages candidate, no deployment.
- Private `baseharbor-final-product-preview`: **`041c274febc10d6a3b0170db3e07c9f1cbc0b083`**, tree `b90a89c15dede6e9e8d65b0f1c4df2e1fed36012`, combines30+three corrections+16docs for local composition checks only. Not remotely integrated or final candidate.
- Combined focused Go checks PASS2.718s. Binary `/workspace/scratch/2edf243f0f92/baha-product-docs-preview` built with genuine VCS revision041c and `vcs.modified=false`; actual Demo CLI No/Cancel/EOF/EditCancel and static MCP/Footprint parity pass against it. No native claim.

## Demo handoff — review corrections still pending

Remote base was `a92347900ed4d1015d9bcde3d265cf9326664a40`. No final Demo/Core pin has been written or published.

- Local native fixture checkpoint **`56661ac9372ce0c5aa296f247e5ebb2f48ce54e2`**, followup **`e28acf20842a1393588793637ed40c856fad8869`**, worktree `baseharbor-demo-new-edit`.
- Existing light guided gate gains zero-needs New and real No/Cancel/EOF; heavy data-capabilities gains SQL New, remove/re-add, genuine shared-provider switch/back, retained provider markers, sibling HTTP SQL and foreign paused sentinel. Common actual MCP transport reused. No fabricated registry/provider IDs.
- e28 fixes both reviewed defects: native Podman removes only XDG_CONFIG_HOME/DATA_HOME to retain actual host storage; Baha retains isolated fixture XDG. Ambient No/Cancel oracle uses ID/name/state metadata, not full foreign inspect/config/env.
- Cleanup checkpoints **`bb9eb8925c8a82bbdb918f57b0dc4014a8fba858`** + **`e6ba5b458707c003e1c0a97aea2e1b25abb6bc6a`**, `baseharbor-demo-owned-cleanup`: exact read-only Core destroy inventory, matching native ownership before inspect/log/unpause, bounded process groups/redaction, truthful failure status, original EXIT/INT/TERM. Actual teardown → foreign check → separate exact-owner removal. Independent review CLEAR;17 cleanup tests,2 redactor tests and4 consent tests pass.
- Root combined `baseharbor-demo-integrated`: HEAD **`2adc744d9a5f6e568bce6dde8c44e9381080f8c2`**, includes566+e6+e28. Three tracked UNCOMMITTED files: README.md, .github/workflows/v0424-targeted.yml, tests/mcp/run.sh. The last adds strict tool-list/Edit/Footprint parity and invokes the actual static MCP test; do not lose it.
- **Remaining SQL fixture blocker:** image-basename-only PostgreSQL classification includes Core postgres-admin/postgres-init helpers, making its one-server guard fail. The separate worker has an **UNCOMMITTED**29-line/43-line correction in `baseharbor-demo-new-edit`: `is_postgres_server` checks canonical server role, actual persistent data mount and required environment keys, with tests. Seven heavy/four guided cases reportedly passed, but final independent review/commit/native validation were not completed before STOP. Preserve and review `demo-sql-classification-uncommitted.patch`; it is NOT in the root combined checkpoint.
- Claims must stay precise: UUID markers prove dedicated/shared **provider admin-database retention**; sibling HTTPS SQL proves actual sibling consumer data. New application's restricted SQL consumer data path is not independently probed after switch. Do not claim that proof. Public `baha app env --path` exposes protected host connection material, but container-local execution is a different network context; no guessed DB/role or new client framework was added.
- There is **no verified max11 container limit** in current catalogs. Do not carry that earlier unsupported estimate as a blocker. Real additional workload/SQL/paused sentinel resources must fit the actual runner and8-minute runtime step; evaluate before dispatch.
- No guided/data Docker or rootless Podman native run has qualified these new fixtures. `native_runtime_qualified=false` on local process receipts remains true.

## Consumer and final acceptance gaps

- Console candidate worktree `baseharbor-console-candidate`, local9c337731; Connector `baseharbor-connector-candidate`, local1116c009. Pending-only patches are retained here. They are not complete consumer freezes.
- After final Core implementation/docs: freeze exact Core SHA in develop → Demo core.ref and qualified normal merge → Demo SHA → Console six contract files/source-lock SHA256 plus candidate manifest and **both workflow pins** → Console SHA → Connector canonical `work/v0.4.26-integrations-docs` branch/manifest with exact Core/Demo/Console → exact Connector SHA. That canonical Connector branch was not yet present. Preserve concurrent main changes.
- Console CI pin d5417bde and release-integration pin c359 are still old; do not forget one. Connector v26 workflow routing draft exists; its manifest still says0.4.25 until legitimate freeze. Do not accidentally publish governance/instruction changes from old consumer ancestry.
- Final necessary atomic catalogue remains65 gates:5static,36runtime atomic,4adoption,8HA,2journey,10integration. Reuse complete authenticated joint Console/Connector native/browser receipt instead of duplicate three consumer journeys.
- Existing selected push format: `validation/pre-release/selected/gates/<comma-separated exact gate IDs>`. Bare selected labels need an absent selected-gates file. Do not start full orchestration with unfinished docs/pins/fixtures. No old-run reuse is required for a fresh complete candidate bundle.
- Final Docker named eight-family test, final Podman/recovery applicability, actual CLI New/Edit/NoCancel/provider/data/shared paths, Console/Connector, EN/DE/Pages candidate, release-source-preflight and final integrated SHA verification remain outstanding.
- K3s scope must come from actual release gates; existing Kubernetes adoption corpus acceptance is not native K3s execution. Do not invent a native K3s PASS or unrelated full matrix.

## CI transport limitation and working rules

- #1028 attempt1 ci-policy119311347853 and #1029 attempt1 cli-vet119315801387 remained `in_progress/null` in authenticated API lists despite complete logs/steps, even much later. Final45s bounded verifier correctly blocked. Those attempts are NOT accepted receipts.
- Targeted affected-job reruns yielded actual successful authenticated attempt2, used for the merges. No inference from logs/steps, no verifier weakening. The tool may also rerun dependent jobs; inspect results before another action.
- Cache cause is unproven; query variations did not fix it. Do not blindly increase timeout or add a cachebuster and claim resolution. Direct individual-job fallback is only a proposed unimplemented design, requiring authenticated full identity/status proof. Generic github_fetch blocks that individual endpoint with400; do not circumvent tool controls.
- Batch complete implementation and local checks before push. Evaluate current CI before another candidate. Keep required check, source, runtime and acceptance proof separate; preserve failed evidence.
- Tool auto-review previously rejected publishing a planning AGENTS.md governance rewrite. It was NOT committed; AGENTS remains unchanged. Do not retry/reword/indirectly publish that rejected change. Dated canonical handoffs and Owner instructions carry the current state.
- Local Go1.26.9: `/workspace/scratch/2edf243f0f92/toolchains/go/bin/go`; Actionlint1.7.12 under toolchains/validation-bin. MkDocs via `PYTHONPATH=/workspace/scratch/2edf243f0f92/docs-python`.
- Shared Git worktrees: preserve other sessions' dirty files/claims. Real Go builds may need explicit correct GIT_DIR/GIT_WORK_TREE for VCS stamping. **Unset both for tests**: inherited values corrupt fixture Git resolution and cause a false missing CODEOWNERS failure. Never use `-buildvcs=false` to disguise provenance.

## Planning and suggested resumption order

The former7 ACTIVE cards were stale closeouts/dependent WIP. Before stop:2 ACTIVE (docs/full audit),1 Docker REVIEW; Core921/binding and three Podman slices accepted. This stop handoff moves the remaining Codex ACTIVE cards to BLOCKED with the explicit Owner stop as their blocker, never to accepted. No documentation PR is invented to satisfy a review status. Existing claims/history remain; core923 still waits for real docs and final journeys.

When the Owner authorizes resumption:

1. Read current product/planning mains and actual #1030 head/CI; preserve checkpoint patches and latest external changes.
2. Accept #1030 if still qualified; integrate the three exact sources separately with current mandatory checks.
3. Review/finalize the SQL server-classification dirty patch; integrate complete Demo preparation including e28, e6 and MCP run wiring. Keep evidence claims precise; execute only after coherent candidate/runner review.
4. Integrate docs16 normally, validate final EN/DE/Pages/reference candidate, then freeze four exact consumers in the noncircular order above.
5. Run targeted missing New/Edit guided/data gates on Docker/rootless Podman, required ecosystem/journeys/HA/backup gates, final develop native checks and source preflight; correct actual failures without weakening guards.
6. Publish validated planning/evidence and a final readiness decision. Only say YES with complete exact final-matrix proof; stop before publication.

## Portable checkpoint contents

`patch-inventory.json` records SHA256, byte size, source worktree/head and explicit unaccepted status for every patch. Patches are preserved as **handoff evidence**, not applied product code:

- `demo-combined-unpublished.patch`: apply to Demoa923; includes tracked combined tree and three pending files, excludes the dirty SQL correction.
- `demo-sql-classification-uncommitted.patch`: review/apply separately after the combined Demo patch; unfinished source, not accepted.
- `docs-16-paths-unpublished.patch`: only16 docs paths against213c; integrate current target normally.
- `console-pending-unpublished.patch` and `connector-pending-unpublished.patch`: pending deltas only against their recorded local heads; not complete ancestry/pins or acceptance.

All worktree paths above are under `/workspace/scratch/2edf243f0f92/`. Local commits are not assumed remotely available. This handoff deliberately preserves unapplied differences rather than forcing code publication after the Owner's stop.
