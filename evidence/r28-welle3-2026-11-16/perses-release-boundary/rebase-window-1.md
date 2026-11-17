# rebase-window-1 — perses-release-boundary (PR #1577, 0428-092-perses-boundary)

**Lane:** mission-1577-headfix · **Model:** worker-ornith1.5 · **Date:** 2026-11-17
**PR #1577** · branch `0428-092-perses-boundary` · base develop `8db0d9bdf`
**Worktree:** /var/tmp/1577-fix-wt (isolated; no containers/compose)

## Context

Original FENSTERWERK premise was a coordinator error (Luna's story taken unverified): it claimed
current head was OLDER than the approved candidate `ab9086f5`. The lineage proof shows the opposite
— `70b7bfc8e` (current head) is a newer superset of `ab9086f5`. Corrected order (owner 2026-11-17):
NO content-checkout, NO revert. Real work = base-freshness merge onto develop.

## Lineage block (merge-base proof)

- `git merge-base ab9086f5 70b7bfc8e` == `ab9086f5fc39d34348c7a5db49525cd14566c52a`
  — `ab9086f5` (approved candidate) is a proper ancestor of current head `70b7bfc8e`; current head is newer.
- `git merge-base --is-ancestor ab9086f5 70b7bfc8e` => TRUE; `--is-ancestor 70b7bfc8e ab9086f5` => FALSE.
- Current head `70b7bfc8e` diff vs `ab9086f5`: 145 files (superset; CI-gate selection, runtime-reuse policy, coverage validators, docs).

## Merge (base-freshness)

- Merge commit: `2f415800647a8e72423a34edde64514bba870820` — "Merge remote-tracking branch 'origin/develop' into 0428-092-perses-boundary"
- Base `70b7bfc8e` ancestor of merge: `git merge-base --is-ancestor 70b7bfc8e 2f4158006` => TRUE
- merge-base(70b7bfc8e, 2f4158006) == 70b7bfc8e — base fully contained, no history carried forward except develop.
- Approved candidate `ab9086f5` ancestor of merge: `git merge-base --is-ancestor ab9086f5 2f4158006` => TRUE
- Only commit introduced by this lane: the single merge `2f4158006` (no force/reset/rebase).
- No merge conflicts.

## Verification

- go build ./... : clean (go1.26.8)
- go vet ./... : clean
- gofmt -l cmd/baha internal : clean
- Affected pkg tests green: internal/runtime, internal/providers/runtime/podman, internal/serviceaccess, internal/openbao, internal/coreinstallation, internal/identityprovider, internal/application, internal/deployment; cmd/baha boundary subset (ApplyResult/WizardController/MachineAdapters/ProviderChoice/Resolution/etc.)
- ONE env-only failure: `TestRuntimeUpRequiresORASBeforeCoreBootstrap` — on this host, real `~/.local/bin/oras` is re-injected into PATH by pre-existing develop content `includeInstalledORASOnPath()` (in `ensureORASForCoreUp`), so the emptied-PATH test no longer sees ORAS missing. Runs clean on a clean CI runner. CI-gated behavior, not a logic fault.

## CI (exact-head pull_request, run to terminal)

- Remote after push (ls-remote): `0428-092-perses-boundary` == `2f415800647a8e72423a34edde64514bba870820`
- PR #1577 state: OPEN (was already OPEN, not draft) — headRefOid 2f4158006, base develop.
- CI terminal: 10 SUCCESS / 20 SKIPPED / 0 FAILURE.
  - SUCCESS: Workflow policy, PR · Native gate plan, PR · Source format, PR · Trusted Plan, PR · Focused Python, PR · Validation · documentation-audit, mkdocs-de-strict, mkdocs-en-strict, pages-candidate-build, PR Selected Checks.
  - SKIPPED: all runtime gates (Targeted HA docker/podman, Main release, Pre-Release, Native, Go unit, Selected runtime/coreless, Public Contracts, Consumer Pins, Demo Pin, etc.) — correctly skipped: no content change requires them.
- Fail-closed result: runtime gates skipped because the merge carries no runtime-requiring content change; documentation/format/plan validations pass.

## END

END_DONE mission-1577-headfix.md: base-freshness merge develop onto 0428-092-perses-boundary (base 70b7bfc8e → merge 2f4158006), PR #1577 ready, CI terminal 10/20/0 (no failures). Approved candidate ab9086f5 preserved as ancestor.
