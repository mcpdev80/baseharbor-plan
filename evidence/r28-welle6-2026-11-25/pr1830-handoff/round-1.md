# PR #1830 handoff — Core Demo pin

Date: 2026-11-24
Card: 0428-284 / `t-20261125-0428-284-1812-postretry-gate-failure`
PR: [mcpdev80/baseharbor#1830](https://github.com/mcpdev80/baseharbor/pull/1830)

## Exact candidate and source pin

- Branch: `w115-0428-284-demopin` (the live PR branch; short SHA `3e80fb90`).
- Exact head: `3e80fb90171ce8f45f2efa0f1a50c26b65fd20d2`.
- The branch contains a normal merge of current Core `develop` after #1826 merged. #1826 merge commit and then-develop tip: `145b4a20f35179a0ac6bc0a66666a846c1ae35c0`.
- Resolved the conflict in `docs/releases/v0.4.28.demo-ref` to exactly `b41127723e523134a1c14ee3c36cf133237162ce` (Demo PR #174 develop tip). `git show HEAD:docs/releases/v0.4.28.demo-ref` verified this exact value after the merge.
- The normal push advanced the PR branch from `8658af5e1dfc4f3db09e0f9e92771784e45e981e` to `3e80fb90171ce8f45f2efa0f1a50c26b65fd20d2`. `git diff --name-status origin/develop...HEAD` lists only `M docs/releases/v0.4.28.demo-ref`.
- Last observed PR state: open, mergeable, `CLEAN`; not merged. Last measured `refs/heads/develop` was `145b4a20f35179a0ac6bc0a66666a846c1ae35c0`; refresh both PR and refs before any merge.

## Hosted exact-head evidence

Both qualifying runs below are distinct, hosted, terminal-success runs on the same exact PR head `3e80fb90171ce8f45f2efa0f1a50c26b65fd20d2`:

1. PR-CI [run 45483027348](https://github.com/mcpdev80/baseharbor/actions/runs/45483027348) — `pull_request`, completed `success`; `PR Selected Checks` succeeded, along with the selected source-format, workflow-policy, Go build/vet and unit checks.
2. Required v0.4.28 source/pin validation [run 45484190794](https://github.com/mcpdev80/baseharbor/actions/runs/45484190794) — `workflow_dispatch`, completed `success`; inputs were `tag=v0.4.28`, `ref=3e80fb90171ce8f45f2efa0f1a50c26b65fd20d2`, `demo_ref=b41127723e523134a1c14ee3c36cf133237162ce`, and `only_gates=atomic/static/mcp,atomic/static/ci-fast-check`. The source qualification passed and both `Static · mcp` and `Static · ci-fast-check` executed and passed.

Void run: [45460152741](https://github.com/mcpdev80/baseharbor/actions/runs/45460152741) was canceled on the prior owner hold at old head `8658af5e1dfc4f3db09e0f9e92771784e45e981e`; it is not a witness.

The v0.4.28 validation above is for the source pin's catalog-required static checks. It did not run #1812's separate 14 Docker/Podman Light gates.

## Exact next steps for the receiving worker

1. Refresh PR #1830, `refs/heads/develop`, and the PR branch. Confirm the PR head is still `3e80fb90171ce8f45f2efa0f1a50c26b65fd20d2`, the pin remains exactly `b41127723e523134a1c14ee3c36cf133237162ce`, and both successful run IDs above still qualify on that head. If develop advanced or the PR head changed, follow the owner ordering: integrate current develop by a normal merge, resolve the pin to the same exact Demo SHA, push normally, and collect two fresh green hosted run IDs on the new exact head.
2. Once the two-run exact-head pair and current mergeability are confirmed, merge #1830 under the owner mandate with an expected-head guard. Record the merge commit and `git ls-remote` witnesses for `develop` and the PR branch.
3. After #1830 merges, perform the owner-authorized #170 Leg-B supersession dispatch using `pre-release.yml`: `ref=develop-tip`, omit `demo_ref` so the v0.4.28 pin supplies Demo `b41127723e523134a1c14ee3c36cf133237162ce`, and set `only_gates=atomic,static,config-matrix`. Record the exact source identities, run ID/URL, and whether `config-matrix` actually executed and passed without #170's hunk.
4. Add that run as the supersession witness to `t-20261124-ci-operator-acceptance-nontty.md` and `evidence/r28-welle6-2026-11-25/170-ci-route/close-proposal.md`. A green witness supports a close proposal only; do not silently close #170. The Kanban card needs an owner-visible confirmation line first.
5. Keep #1812's 14 Light-gate qualification explicitly separate; the two #1830 runs above do not claim those Docker/Podman gates passed.

END handoff. No Core source or PR mutation was made after head `3e80fb90`; #1830 remains unmerged in this handoff.

Author note: PR #1830 branch `w115-0428-284-demopin` is green at exact head `3e80fb90171ce8f45f2efa0f1a50c26b65fd20d2`; hosted PR-CI run [45483027348](https://github.com/mcpdev80/baseharbor/actions/runs/45483027348) and required v0.4.28 validation run [45484190794](https://github.com/mcpdev80/baseharbor/actions/runs/45484190794) both completed successfully on that head, with `docs/releases/v0.4.28.demo-ref` pinned to `b41127723e523134a1c14ee3c36cf133237162ce`.
