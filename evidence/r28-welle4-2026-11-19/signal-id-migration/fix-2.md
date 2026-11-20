# 0428-168 signal-id-migration — correction round 2 (fix-2)

Lane x-168r2, PR mcpdev80/baseharbor#1709, branch
`lane-0428-168-signal-id-migration`. Verdict under correction:
`evidence/r28-welle4-2026-11-19/codex-review-wave/1709-0428-168.md`
(P1 preserve the legacy registration observably, P2 idempotent /
no-mutation under the existing mutate-lock, P4 tests must prove
list-visibility before migration, P5 named CI shard and one terminal PR run).

## PLAN

1. Reality fetch: remote -v, branch state, develop tip; rebase branch onto develop
2. P1: re-book the legacy `keycloak-metrics` source of record INSIDE the single
   RegisterProviderSignals mutation, onto the owner's canonical project identity
3. P2: change-aware write (mutateChanged) under the SAME existing flock; no-op
   runs create and rewrite no byte
4. P4: rewritten unit + integration tests witness the corpse before migration
   and prove list-visibility after it (metrics enabled and disabled)
5. gofmt, vet, build, ci-fast-check, source-readability audit
6. Commit, push with --force-with-lease, watch ONE pull_request run to terminal
7. Evidence, board, END post

## remote-pruefung

Word-for-word findings the coordinator demanded (the shared-checkout root
defect that burned card 078):

- `git remote -v` in MY clone /var/tmp/x-168r2-wt/product:
  `origin https://github.com/mcpdev80/baseharbor.git (fetch)` /
  `(push)` — origin IS the GitHub remote here; there was no filesystem-only
  `origin` in my round-2 clone. My earlier pushes used this name.
- The GitHub-authoritative check the coordinator measured (PR #1709 head stuck
  at 0d1568ec4dc8 since 03:13Z) was TRUE: my round-2 P1/P2/P4 work existed
  only as UNCOMMITTED changes in the /tmp worktree. The 0d1568ec push had
  carried only the round-1 content. That is the delivery gap, not a remote
  misconfiguration.
- Recovery: `git fetch --prune origin develop` → develop tip
  36d075fad77fa61ac8c153e979855546589b32c2; branch rebuilt cleanly on that
  tip (rebased the two round-1 commits 9d905cbd/48d05ab8 with
  `git rebase --onto origin/develop f61ef0f4`), round-2 content re-applied
  and committed as 4d3494ea, then pushed:
  `git push --force-with-lease origin HEAD:refs/heads/lane-0428-168-signal-id-migration`
  (`+ 0d1568ec...4d3494ea ... (forced update)`).
- Witness (post-push, GitHub-authoritative):
  `git ls-remote origin refs/pull/1709/head` → 4d3494ea7a145e2a92c8008eb510d3c5b49ad06c
  `git ls-remote origin refs/heads/lane-0428-168-signal-id-migration` → same
  `gh api repos/mcpdev80/baseharbor/pulls/1709 --jq .head.sha` → 4d3494ea7a14...
- Ancestry: `git merge-base --is-ancestor origin/develop HEAD` → YES
  (develop f61ef0f4991c → 36d075fad77f hop recorded before push).

## loop-abbruch und diagnose

The coordinator's stop directive: the session had burned hours re-running
packages without `-run`. The two verbatim FAIL blocks from the last two
targeted runs, and what the diagnosis produced:

Block 1 — my test, against an expectation I had INFLATED beyond the contract:

```
--- FAIL: TestRegisterKeycloakSignalsPreservesLegacySourceForOwner (0.00s)
    --- FAIL: TestRegisterKeycloakSignalsPreservesLegacySourceForOwner/appB-metrics-enabled (0.00s)
        keycloak_legacy_migration_integration_test.go:151: the migrated keycloak source
        "keycloak:bh-target-alpha-identity-dev:keycloak-metrics" (owner appA verbatim)
        not visible through ListMetrics: []observability.MetricsSource{}
```

Diagnosis: the derived identity embedded the RESOURCE-qualified project
(`bh-<target>-<app>-identity-<env>`), whose project name contains the
application anchor TWICE; route 2 fails closed on double anchors BY DESIGN
(the fail-closed rule the coordinator had 0428-121 establish must not be
worked around). Fix: `CanonicalApplicationProject` reduces the migration
target to the canonical APPLICATION project `bh-<target>-<app>-<env>`
(internal/observability/migration.go:250, applied at :155 and at the seam in
RebookLegacySignals) — environment.go's rules are UNTOUCHED; only a robust
project-segment isolation was added there. The expectation in the test was
corrected to the contract's identity (`keycloak:bh-target-alpha-dev:keycloak-metrics`).

Block 2 — the existing develop test:

```
--- FAIL: TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle (0.00s)
    shared_postgres_runtime_owner_test.go:75: owned recovery backup: dump postgres
    instance default: execution selected the logical app environment instead of
    the physical provider owner
```

Diagnosis (isolation bisection, one file reverted at a time): NOT an effect of
my change. A PURE develop clone (/var/tmp/x168r2-devenv/pure-develop @
36d075fad77f, zero lane edits) fails this test on this machine too, 5/5
runs — while CI runs 44669117744/44669117784 on the same SHA are green. The
test is a host-state-sensitive pre-existing flake on this box (it asserts
which compose service an exec selects; the failing path involves shared
backend state resolution, which my diff never touches — no write-set overlap
with internal/application). §5.3 honesty: recorded, reproduced on pure
develop, NOT masked; CI's packages shard runs the real verdict at the pushed
head. My local full-suite triage therefore stopped at the two named tests
per the stop directive.

## gofmt und aggregate

- `gofmt -l internal/observability internal/identityprovider` → EMPTY
  (after `gofmt -w` on my files only; recorded twice: pre-push at 4d3494ea
  amend-cycle and at 85bb4b4a).
- Run 44692628196 (head 4d3494ea) `PR · Source format` failed on
  `bash scripts/source-readability-audit.sh`: `internal/observability/registry.go
  has 930 lines (limit: 800)`. Fixed WITHOUT behaviour change in commit
  85bb4b4a: the LegacyReconciliation declarations, RebookLegacySignals,
  ListAll, RegistryHasSignal and RegistryHasSource moved to
  internal/observability/migration.go (815 lines → registry.go now 795),
  plus CanonicalApplicationProject exported as the single implementation
  (duplicate in keycloak_realization.go removed). Audit now: Go file size
  PASS, Function span PASS, Regression ratchet PASS; ci-fast-check.sh green
  (293 python contract tests OK); `go vet` clean;
  `go test ./internal/observability/ ./internal/identityprovider/ -count=1`
  → both ok.
- Aggregate: the first candidate's `PR Selected Checks` failure was the
  source-format/readability job above; the packages shard itself passed at
  4d3494ea.

## P-Punkte, Belege am Head

Candidate diff (`git show --stat 4d3494ea`, style follow-up 85bb4b4a):
internal/identityprovider/keycloak_legacy_migration_integration_test.go,
internal/identityprovider/keycloak_realization.go,
internal/observability/environment.go,
internal/observability/keycloak_legacy_migration_test.go,
internal/observability/migration.go, internal/observability/registry.go.

- P1 — the legacy registration survives observably:
  `RegisterProviderSignals` runs `RebookLegacySignals` INSIDE its single
  mutation before the (ID, provider) replacement (registry.go seam,
  migration.go:RebookLegacySignals). The derived identity
  `keycloak:<owner-project>:keycloak-metrics` is disjoint from the caller's
  `keycloak:<project>`, so replacement can never select it; owner and fields
  stay verbatim (unit: TestMigrateScopedReBooksObservablyForOwner;
  end-to-end: TestRegisterKeycloakSignalsPreservesLegacySourceForOwner,
  both appB-metrics-enabled and appB-metrics-disabled subtests).
- P2 — idempotent, no-mutation under the EXISTING mutate-lock:
  `mutateChanged` (registry.go, ~line 800) takes the same
  `<registry>.lock` flock — no second lock anywhere — byte-compares the
  canonical serialization, and never creates an absent file. Proofs:
  TestMigrateScopedIsIdempotentAndWritesNoByte (file byte-identical after a
  re-run; missing file stays missing) and
  TestRegisterKeycloakSignalsSecondRegistrationIsNoMutationOnFirst
  (production path, second registration writes nothing).
- P4 — list-visibility BEFORE migration is witnessed: the corpse tests
  (TestLegacyKeycloakMetricsSourceCorpseProvesTheBug and the integration
  test's pre-list assertion) show the literal present via
  RegistryHasSignal yet ABSENT from ListMetrics (route 2 fails closed on the
  project-less ID), and the post-migration listing shows it under the
  derived identity, removable by it (Remove + RegistryHasSignal gone).
- P5 — the shard: scripts/pr-go-unit-shard.py mode `packages` runs every
  non-CLI package without a name filter, so both new test files run in
  `PR · Go unit · packages`; one pull_request run is monitored to terminal
  state per §4.6 (run id recorded below).

## runs

- 44692628196 (CI · PR #1709, head 4d3494ea): completed, failure —
  `PR · Source format` (readability 930>800; fixed in 85bb4b4a). Aggregated
  `PR Selected Checks` failed as the dependent aggregate of that job. All
  Go-unit/packages jobs green at that head.
- **44696406664 (CI · PR #1709, head 85bb4b4a4cb8, event pull_request):
  completed, conclusion SUCCESS** — monitored to terminal state by this lane
  (§4.6, `gh run watch`). Job evidence:
  - `PR · Go unit · packages` => success (runs both
    internal/observability/keycloak_legacy_migration_test.go and
    internal/identityprovider/keycloak_legacy_migration_integration_test.go;
    scripts/pr-go-unit-shard.py mode `packages` applies no name filter);
  - `PR · Go unit · cli-0..3`, `owner` => success;
  - `PR · Source format` => success; `PR Selected Checks` => success;
  - `PR · Selected Runtime (atomic/docker/identity, docker, identity) /
    Executed docker · identity` => success;
  - no failing job (advisory/main-release/native jobs skipped by selection,
    as on develop-merge PRs).

## candidate-commits

Own commits on the candidate (git log --oneline origin/develop..HEAD):

```
85bb4b4a style(0428-168): keep registry.go within the 800-line readability limit
4d3494ea fix(0428-168): re-book legacy keycloak source inside registration, change-aware
48d05ab8 fix(0428-168): re-book legacy keycloak-metrics observability source on ID scoping
9d905cbd fix(0428-168): re-book legacy keycloak-metrics observability source on ID scoping
```

Final ls-remote witness (GitHub-authoritative, after terminal run):

```
36d075fad77fa61ac8c153e979855546589b32c2 refs/heads/develop
85bb4b4a4cb84707cb15eedbe94dfb0b7fadc9a2 refs/heads/lane-0428-168-signal-id-migration
85bb4b4a4cb84707cb15eedbe94dfb0b7fadc9a2 refs/pull/1709/head
```

`git merge-base --is-ancestor origin/develop HEAD` => YES.

## cleanliness

No containers, networks or volumes were started by this lane. Worktrees:
/tmp/opencode/x-168r2-wt/product was LOST to a /tmp tmpfs eviction during
the server restart; the candidate now lives in /var/tmp/x-168r2-wt/product
(durable disk). Foreign-file hazard reported earlier stands:
/tmp/opencode/base168 is shared with lane 0428-167; their untracked
loki_signal_scope_regression_test.go copies were sheltered at
/var/tmp/x-168r2-shelter/. Test-owned state dirs are all t.TempDir()-scoped.
Machine: 9 leftover empty trace-*/prune-* dirs under
internal/application from another lane's tests appeared in my worktree's
untracked space; they were NOT created by my runs (never touched during the
/tmp-wipe window) and are outside my write set — left in place for their
owner, noted here.

END_DONE — candidate 85bb4b4a4cb8 on PR #1709, run 44696406664 SUCCESS (terminal, self-watched), P1/P2/P4/P5 proven above.
- Terminal run witness: run 44696406664 SUCCESS at head 85bb4b4a4cb8 (watched to terminal by this lane).
