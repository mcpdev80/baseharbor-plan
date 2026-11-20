# 0428-168 signal-id-migration — round 4 (x-168r3, P1-blocker correction)

Lane x-168r3 continues (same session as round 3). Correction round against the
valid, frozen r3 verdict:
`evidence/r28-welle4-2026-11-20/codex-review-wave/1709-0428-168-r3.md`
(REQUEST CHANGES, one blocking finding = P1 mixed-state; P2 and P4 satisfied,
no rework; r3 scan-error fix validated).

## PLAN

1. Reality check: ls-remote (branch == refs/pull/1709/head == 1fa78df42), read r3 review file, rebuild worktree at frozen head
2. Reproduce the blocker in a test BEFORE fixing it (mutations first)
3. Fix ownerProjectMaps: union derived legacy-owner map with non-empty recorded map; propagate ListAll error; fail-closed before mutation when an owner resolves through no route
4. Scope discipline: no signature changes to RebookLegacySignals/MigrateScopedMany (announce for 0428-166), no .github writes, no cmd/baha writes
5. Local: build, vet, gofmt, targeted tests, mutation proof, ci-fast-check
6. ONE commit, force-with-lease onto the unguarded branch (base decision 2026-11-20-pr-branch-refresh-by-rebase), freeze witnesses
7. Watch run to terminal at exact head; END post

## base attestation

- Base SHA this round cut from: the frozen, verdict-valid head
  `1fa78df421e521ab7aeaec05a58d6cf646ddf971` (measured via
  `git ls-remote lane-origin refs/heads/lane-0428-168-signal-id-migration
  refs/pull/1709/head` — both equal it; refs/pull/1709/head additionally
  fetched before the ancestry test).
- develop (measured): `36d075fad77fa61ac8c153e979855546589b32c2` — unchanged
  since the r3 review, so no rebase hop was required; the new candidate
  489e4e66a keeps develop as a direct ancestor (witness line 2 below).
- `git merge-base --is-ancestor 36d075fad77f 489e4e66a2b1` → exit 0 (YES).
- Own-commits log develop..head shows SEVEN commits, all this card's chain
  (r1/r2/r3/r4 of lane-0428-168), no foreign candidate:
  489e4e66a / 1fa78df42 / 380c66c49 / 85bb4b4a4 / 4d3494ea7 / 48d05ab8d / 9d905cbd1.

## the blocker, reproduced word for word (mutations first)

At the frozen head 1fa78df42, `ownerProjectMaps` returned
`append(maps, recorded)` immediately when the state scan produced a non-empty
map; `legacyLiteralOwners` (the registry-derived recovery) ran only when the
map was COMPLETELY empty. Mixed state — legacy holder appA with NO state
directory, registering appB WITH one: appA's record reached
`ProjectFor`'s last-resort fallback and was re-booked under appB's project.
This is the pre-fix run of the new regression test, verbatim (the r3 code,
union reverted):

```
--- FAIL: TestRegisterKeycloakSignalsRebooksLegacyOwnerWithoutStateDir (0.00s)
    keycloak_legacy_migration_integration_test.go:404: appA's record is not under its own derived identity with its owner verbatim: "keycloak:bh-target-alpha-dev:keycloak-metrics" sources=[{ID:"keycloak:bh-target-bravo-identity-dev" ... OwnerApplication:"bravo" ...}, {ID:"keycloak:bh-target-bravo-identity-dev:keycloak-metrics" ... OwnerApplication:"alpha" ... Target:"runtime://bh-target-bravo-identity-dev/keycloak" ...}]
FAIL	github.com/mcpdev80/baseharbor/internal/identityprovider	0.005s
```

The second source is appA's owner field riding on appB's project identity —
the r3 blocker verbatim.

## the fix (scope: exactly this defect)

`internal/identityprovider/keycloak_realization.go`:
- the derived legacy-owner map now appends ALONGSIDE a non-empty recorded map;
  maps are consulted in order (existing precedence), so a recorded owner keeps
  its state-derived project and an un-recorded legacy holder resolves through
  the grammar. No new error class: the not-exist semantics of
  `ListKeycloakOwnerProjects` (absent state = nil, nil) are reused unchanged;
  the real scan-error path from r3 is UNTOUCHED (mutation proof D still holds).
- `legacyLiteralOwners` propagates the `ListAll` error instead of converting a
  registry read failure into "no legacy owners" (r3 recipe point).
- `unresolvedLegacyOwners` (new, realization-local) aborts registration
  fail-closed BEFORE `RegisterProviderSignals` when an app-scoped legacy
  record's owner resolves through NEITHER map NOR the record's own
  scoped-ID/runtime:// anchor. The anchor route is the exact one `ProjectFor`
  walks, so the abort is precise and never fires on records that resolve
  (no false-positive risk for the no-legacy normal path).
- `internal/observability/migration.go`: `ScopedIDProject` exported as the
  single implementation of the scoped-ID anchor read; `scopedProjectOf`
  delegates. No signature changes anywhere else:
  `RebookLegacySignals(r, sources, registrationID) []SignalSource` and
  `MigrateScopedMany(project, sourceProjects...) (bool, error)` stand
  unchanged.

## tests (both green at the candidate; (a) red without the fix)

- `TestRegisterKeycloakSignalsRebooksLegacyOwnerWithoutStateDir` — appA legacy
  literal with NO state dir + appB state dir; appB registers through the real
  production path; asserts: literal gone, appA's record under appA's own
  derived identity (`keycloak:bh-target-alpha-dev:keycloak-metrics`) with
  owner verbatim, list-visible for appA through `ListMetrics`, removable by
  that identity. Fails red on the pre-fix code (block above); green after:

```
--- PASS: TestRegisterKeycloakSignalsRebooksLegacyOwnerWithoutStateDir (0.00s)
```

- `TestRegisterKeycloakSignalsAbortsOnUnreadableLegacyRegistry` — corrupt
  registry bytes + appB state: registration aborts with the bytes untouched.

```
--- PASS: TestRegisterKeycloakSignalsAbortsOnUnreadableLegacyRegistry (0.00s)
```

## mutation proofs this round

- Mutant E (union reverted to the r3 early-return, code above): blocker test
  RED, fix-candidate GREEN. Word-for-word RED block in the section above.
- Mutant D (silent owner omission, from r3): unchanged code path, untouched
  by this round — `TestRegisterKeycloakSignalsAbortsOnPartialOwnerStateScan`
  and `TestListKeycloakOwnerProjectsReportsPartialScan` still pass at
  489e4e66a.

## regression coverage (same commands, restored code)

```
ok  	github.com/mcpdev80/baseharbor/internal/observability	0.010s
ok  	github.com/mcpdev80/baseharbor/internal/identityprovider	8.998s
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.048s
```

`go build ./...` clean, `go vet` clean, `gofmt -l internal/` empty,
`scripts/source-readability-audit.sh` PASS (biggest files: registry.go 791,
migration.go 413, keycloak_realization.go 629 — all ≤800),
`bash scripts/ci-fast-check.sh` OK (293 script tests, no candidate-added
checks).

## CI-surfacing (§5.3)

Both new tests are ordinary Go package tests in
`internal/identityprovider` — executed by `PR · Go unit · packages`
(non-CLI packages, no name filter) and `PR · Validation ·
identity-provider-package-tests`, same as the r3 tests. No `.github/**`
change was needed.

## freeze witnesses (three lines, word for word)

1. `git ls-remote lane-origin refs/heads/lane-0428-168-signal-id-migration refs/pull/1709/head` (post-push):

```
489e4e66a2b11f32bad63719adc2a3b885579db7	refs/heads/lane-0428-168-signal-id-migration
489e4e66a2b11f32bad63719adc2a3b885579db7	refs/pull/1709/head
```

2. `git fetch lane-origin refs/pull/1709/head` first, then
   `git merge-base --is-ancestor 36d075fad77fa61ac8c153e979855546589b32c2 489e4e66a2b11f32bad63719adc2a3b885579db7` →
   exit 0, `ANCESTOR_YES` (develop unchanged at 36d075fad since the r3 review;
   no rebase hop required this round).

3. pull_request run at the EXACT head: `44704834012` — status and conclusion
   recorded below once terminal (§4.6, this lane watches it).

Candidate SHA (frozen): `489e4e66a2b11f32bad63719adc2a3b885579db7`
(push witness: `1fa78df42..489e4e66a` via
`git push --force-with-lease=refs/heads/lane-0428-168-signal-id-migration:1fa78df42...`;
no force-push over unseen work: the frozen head was ancestry-verified and
develop was unchanged).

Self-verification note: an intermediate working-tree draft had the
fail-closed seam as `if err != nil || len(unresolved) > 0 { return nil, err }`
— which returns a NIL error on the unresolved path (a silent no-abort). That
draft was NOT committed: `git show HEAD:...keycloak_realization.go` (lines
260-269) carries the correct explicit form (`if err != nil { return nil, err }`
then `if len(unresolved) > 0 { return nil, fmt.Errorf(...) }`). The
commit-content check is this note's witness; no push was needed for it.

## announcement for 0428-166 (interface planning only)

As directed: the production callback `RebookLegacySignals(LegacyReconciliation,
[]SignalSource, string) []SignalSource` (internal/observability/migration.go)
and the standalone `LegacySource.MigrateScopedMany(project string,
sourceProjects ...map[string]string) (migrated bool, err error)` are exposed
at this head UNCHANGED by round 4. THIS AKTE ANNOUNCES: after candidate
489e4e66a the lane changes NEITHER signature — 0428-166 may plan against them;
the r3 verdict approves nothing downstream and 166 holds any signature change
firmly after this head.

## repo-rule compliance

- No `.github/**` writes, no workflow_dispatch, no reruns, no merge.
- No subagents (§4.8): every step ran in this session.
- Targeted `git add` of exactly three files; no `git add -A`.
- Write-set: internal/identityprovider/keycloak_realization.go,
  internal/identityprovider/keycloak_legacy_migration_integration_test.go,
  internal/observability/migration.go. Nothing in cmd/baha/
  app_status_result.go (card 078), nothing in perses paths (083/174/091).
- One candidate branch (lane-0428-168-signal-id-migration); no extra branch
  created or deleted.
- No pushes between the verdict and this single commit (freeze rule held:
  the correction was developed locally, one commit, then silence).
- Evidence lives only in baseharbor-plan (this file), never in a product repo.
- The shared `/home/marcel/dev/baseharbor-ecosystem/baseharbor` checkout was
  used only for `git remote -v`/`ls-remote`/`fetch` witnesses, never as
  evidence of remote state; all refs came from `git ls-remote lane-origin`
  (URL https://github.com/mcpdev80/baseharbor.git).

## cleanliness

Before: `docker ps` on this host — no daemon (coordinator machine); no
containers, networks, volumes or state dirs created by this lane; worktree
/tmp/opencode/x-168r3-wt rebuilt from 1fa78df42 (the r3 worktree had been
pruned at the r3 END).
After: same state; the lane owns /tmp/opencode/x-168r3-wt,
/var/tmp/x-168r3-plan (planning clone) and the /tmp/opencode Go temp test
dirs Go already cleaned. No compose projects were started on any VM
(VMs are not part of this mission; all gates are GitHub-hosted).
cleanliness: besenrein except the two named lane worktrees.

## CI terminal witness (§4.6, watched by this lane)

Run `44704834012`, event `pull_request`, exact head
`489e4e66a2b11f32bad63719adc2a3b885579db7`, this lane watched it to terminal:

```
{"conclusion":"success","headSha":"489e4e66a2b11f32bad63719adc2a3b885579db7","status":"completed","updatedAt":"2026-11-20T08:51:22Z"}
```

Check-runs at the exact head (`gh api .../commits/489e4e66a/check-runs`,
total / not-completed / failures):

```
35	0	0
```

`PR · Source format` and `PR Selected Checks` success; `PR · Go unit ·
packages` executes both new r4 tests plus the r3 suite (no name filter); the
selected `PR · Selected Runtime (atomic/docker/identity, docker, identity) /
Executed docker · identity` job completed success (its only annotation is the
hosted-runner Node.js-20 deprecation notice, a runner-environment warning, not
a check failure). Skipped cells (native matrix, Targeted HA, release, draft)
remain skipped-by-selection and are not counted as passes.

## END

END_DONE x-168r3: r4 correction complete — P1 mixed-state blocker fixed (union + propagated read error + fail-closed abort), mutation proof E recorded, FROZEN candidate 489e4e66a2b11f32bad63719adc2a3b885579db7 on PR #1709 (branch == refs/pull/1709/head, develop 36d075fad ancestor), run 44700696085→44704834012 watched to terminal: completed SUCCESS at exact head, 35/35 checks, 0 failures. Branch quiet until acceptance; signatures for 0428-166 announced frozen in this akte.
