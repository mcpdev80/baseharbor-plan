# PR #1575 Round 2 — Perses descriptor correction

ROLLE: WORKER (0428-075 r2 correction)

## PLAN

- Read mission-seam-r2.md, Luna act-luna-1575-r1.md, and task note; verify base develop and planning origin/main via ls-remote.
- Inspect candidate head 219a0a24d, sync worktree, confirm build + existing Perses tests pass.
- Fix internal/capability/perses.go: give PersesManagement a valid versioned capability spec + provider capability kind so IntegrationDescriptor.Validate passes, tied to the observability owner, no fake metrics/logs/traces.
- Update internal/capability/perses_test.go to assert the descriptor passes Validate at its boundary and is not falsely registered as an application capability provider.
- Run gofmt, go vet, focused capability + cmd/baha Perses tests locally.
- Commit on lane-0428-075-perses-seam, push (draft PR#1575 follows), record exact new head via ls-remote.
- Write this evidence file; confirm evidence on origin/main; post END_DONE.

## Reality witnesses (measured via ls-remote)

- Planning origin/main @ b14a483e:
  `88e114ef4329aadba6937b9e81f01096bde332de  refs/heads/main`
- baseharbor origin develop:
  `0e9ccb582f5bdcdc74049bbe3996263cdce6500c  refs/heads/develop`
- baseharbor origin lane-0428-075-perses-seam (candidate head):
  `219a0a24d5687552556b094223e5e4bcfa2eebc4  refs/heads/lane-0428-075-perses-seam`
- Base-to-head diff: 19 files, 1041 insertions, 21 deletions. `git diff --check` clean.

## Luna finding (blocking, from act-luna-1575-r1.md)

- PersesManagement is exported as an IntegrationDescriptor but supplies no provider capability kinds and no versioned capability specifications. IntegrationDescriptor.Validate rejects it (integration_contract.go:145, 148). It cannot serve as the concrete provider-owned management-tool representation; it is an invalid descriptor.
- Change recipe: replace the invalid IntegrationDescriptor value with a purpose-specific management-tool/surface contract tied to the existing observability owner and its optional management-ui interface (or define a genuinely valid versioned provider contract). Keep Perses out of application capability declarations. Do not add a fake metrics/logs/traces capability.
- Test requirement: focused internal/capability tests showing the chosen Perses representation is accepted at its intended boundary, is not falsely registered as an application capability provider, and preserves the existing provider catalog validation behavior.
- Stop criterion: the exported Perses representation has a valid and explicit catalog/registry status, the optional observability management interface and ownership are represented without fake capabilities, and the focused tests plus their existing CI route pass on the new exact head.

## Repo-rule compliance

- Write set limited to internal/capability/perses.go and internal/capability/perses_test.go — seam/capability files only, per the recipe.
- No .github/** touched (Owner scope). No merge, no ready_for_review, no subagent.
- Branch provenance: branch cut from base develop 0e9ccb582; candidate head 219a0a24d is an ancestor of every new commit.
- No product-repo evidence written. Evidence lives only in baseharbor-plan.
- Cleanliness: no containers/compose/volumes/networks started; no VM. Pure Go compile/test work.

## End state

- New candidate head (via ls-remote): `cb4367f347ed587cb84c67a14b47ffaa3505a5dd`
  `refs/heads/lane-0428-075-perses-seam`
- Base `219a0a24d5687552556b094223e5e4bcfa2eebc4` is an ancestor of the new head (confirmed).
- Only my commit `cb4367f34` sits above base; no foreign commit carried on the branch.

## END

DONE
