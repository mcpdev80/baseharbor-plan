# Migration decisions and remaining product work

Planning migration does not require resolving every product task. The Maintainer authorized completing the reviewed migration on 2026-10-15; software/CI claims still require evidence. Open PR/source state was independently re-read; source issue bodies and timestamps remain unchanged from the 87-issue snapshot.

## Resolved interpretations

- Fixed Core bundle: apply the already binding #872 correction. Requested capabilities and genuine dependencies determine footprint; optional management retains real security requirements.
- Shared release branches/two sessions: historical v0.4.25 only. From v0.4.26 use small independent task PRs; source snapshots retain superseded wording as history.
- core-862: introduce and ratchet checks early; final completion belongs to v0.4.31. Preserve `early: true`.
- console-1 and console-2: remaining Console delivery belongs to v0.4.28; future Kubernetes parity follows the later runtime roadmap.
- nc-3: remaining remote/enrollment work belongs to v0.4.27.
- GitHub Projects: the Maintainer supplied project BaseHarbor #4, ID `PVT_kwHOAVfknc4BnGti`, https://github.com/users/mcpdev80/projects/4. Retire only this project after cutover. ai-coding-system #1 is unrelated and must remain untouched. Current live settings cannot be verified with this connector; no new discovery is needed just to establish existence.

## Preserved open work (not migration blockers)

- demo-24 remains in triage: compare its original secure-default acceptance to current implementation before assigning a release. Do not silently defer an existing TLS defect to v0.4.30.
- core-893-interface records the actual observed pair: PR #930 `a239e7a39a64113ebbd52eaf5d991047c92d6ea7` consumes PR #932 `174dc6d56b40dea85f2708b95e71b3a7b3638c4c`. Final agreement/qualification remains with the existing task owner; old references are historical.
- Old Demo PRs #61/#62/#86/#104/#106 and Console #3 / Connector #4 remain open for source/ancestry review. Migration does not authorize declaring their changes integrated or closing them without that review.
- core-909 retains missing per-ref deletion evidence as open work. The known local mirror and earlier 14-deletion log exist in the source discussion; a current low branch count does not prove every deletion. Do not invent the missing second-pass log.
- core-884 retains the Mac runner/runtime/licensing choice as an implementation prerequisite, not a planning-migration prerequisite. Do not assume Docker Desktop is the only permitted runtime.

## Cutover prerequisites

- Reconcile the live source inventory and PR heads immediately before switching; do not reset historical acceptance.
- Prepare coordinated product-repository entry points and preserve running sessions' ownership.
- Execute the real Obsidian/CardBoard/Git UI acceptance. This cannot be claimed from Python tests or a JSON schema check.
- Apply one coordinated cutover under the existing Maintainer instruction; do not request separate approval for each routine step.
