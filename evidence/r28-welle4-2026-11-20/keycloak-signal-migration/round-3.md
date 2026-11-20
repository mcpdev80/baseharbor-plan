# 0428-168 signal-id-migration — round 3 (x-168r3, takeover)

Takeover lane for card t-20261120-r28-keycloak-signal-id-migration-gap,
PR mcpdev80/baseharbor#1709, branch `lane-0428-168-signal-id-migration`.
Reason for the fresh lane: the previous session (x-168r2) ended END_BLOCKED
with the reason "Der Kontext meiner Session erreichte sein Limit" — a context
limit, not a content problem. Its state was not lost: its head was on GitHub.
This lane took over that head and finished the outstanding items.

## PLAN

1. Resolve git remotes (github-only rule), read plan card + r1/r2 archives
2. Fetch refs/pull/1709/head into own worktree, check out the lane branch
3. Verify branch is already on current develop (no rebase needed), witnesses
4. go build, go vet, gofmt, readability audit, ci-fast-check
5. Reality-check the coordinator's handoff warning: the existing
   TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle
6. P1/P2/P4: verify against code, add the coverage the mutation probes proved missing
7. Fix the two concrete CI-surfacing defects (undetected test file; registry.go line limit)
8. Commit, push --force-with-lease, ls-remote witness
9. Evidence round-3.md to planning origin/main
10. Watch ONE pull_request run to terminal (§4.6), END post, cleanup

## remote-pruefung (git remote -v, /tmp/opencode/x-168r3-wt via shared checkout)

In the shared baseharbor checkout (/home/marcel/dev/baseharbor-ecosystem/baseharbor),
`git remote -v` resolved: lane-origin, origin and upstream ALL point to
`https://github.com/mcpdev80/baseharbor.git` (the filesystem-`origin` trap was
NOT present in this checkout right now — but every push/fetch used the
name `lane-origin`, verified github-url-bound, per the remote guard).
Planning repo attestation: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git` — the real
planning repo (workers/baseharbor-plan was never touched).

## base attestation and ancestry

- Remote truth (measured, `git ls-remote lane-origin`):
  - refs/heads/develop = 36d075fad77fa61ac8c153e979855546589b32c2
  - refs/heads/lane-0428-168-signal-id-migration = 85bb4b4a4cb84707cb15eedbe94dfb0b7fadc9a2 (at takeover)
  - refs/pull/1709/head = 85bb4b4a4cb84707cb15eedbe94dfb0b7fadc9a2
  - The coordinator's mission quoted head 4d3494ea7a14; the lane had since
    advanced to 85bb4b4a4 ("style(0428-168): keep registry.go within the
    800-line readability limit"). Taken over from 85bb4b4a4, nothing re-invented.
- Base SHA cut from: develop = 36d075fad77fa61ac8c153e979855546589b32c2.
  The takeover branch already sat directly on that tip
  (`git merge-base --is-ancestor 36d075fad77f HEAD` → YES), so step 3's rebase
  was a verified no-op — the mission's measured base f61ef0f4991c had already
  been hopped by the previous lane.
- Own-commits-only log (`git log --oneline lane-origin/develop..HEAD` after push):
  - 380c66c49 test(0428-168): surface the sort regression, prove the mutation cases, keep registry under the line limit
  - 85bb4b4a4 style(0428-168): keep registry.go within the 800-line readability limit
  - 4d3494ea7 fix(0428-168): re-book legacy keycloak source inside registration, change-aware
  - 48d05ab8d fix(0428-168): re-book legacy keycloak-metrics observability source on ID scoping
  - 9d905cbd1 fix(0428-168): re-book legacy keycloak-metrics observability source on ID scoping
  All five are this card's chain (x-168r1/r2 + this takeover); no foreign commit rides on top.

## the handoff warning resolved (existing shared-postgres test)

The mission ordered checking FIRST whether the reconcile changes ownership/
lifecycle behavior, via the existing develop test
`TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle`.
Measured outcome, word for word, on BOTH the branch and pure develop
36d075fad77f in this worktree's environment:

```
--- FAIL: TestStandaloneSharedPostgresUsesPhysicalOwnerAcrossAppAndRecoveryLifecycle (0.00s)
    shared_postgres_runtime_owner_test.go:75: owned recovery backup: dump postgres instance default: execution selected the logical app environment instead of the physical provider owner
FAIL	github.com/mcpdev80/baseharbor/internal/application	0.006s
```

Identical failure on develop (checkout of 36d075fad77f measured in the shared
base checkout) and on the takeover branch. The branch's same-package run
(`go test ./internal/application/ -count=1`) passes. So: the test is RED ON
DEVELOP ITSELF in this host environment — an environment/base question, not
content carried by this branch, and NOT the r2 loop's cause. The r2 lane's
234 package runs chased an environment false signal; the branch content does
not touch application ownership/lifecycle at all (diff is confined to
observability/identityprovider). Reported to the coordinator as a STATE finding.
(Also observed: several unrelated packages (accesswizard, availability,
provider registry, r27 private integration) fail locally on develop for the
same environment reasons — "rejecting legacy organization selection: writable
directory /home/marcel/.config is not trusted" etc. The GitHub CI is the
authoritative verdict for those; all four touched/adjacent packages
(observability, identityprovider, logs, application) pass locally.)

## what the previous lane did NOT finish, and this lane's fixes

Measured at takeover (head 85bb4b4a4): 35/35 checks completed, 2 FAILURE =
`PR · Source format` and `PR Selected Checks`. Both had two concrete causes,
neither a P1/P2/P4 behavior gap:

1. `internal/observability/registry.go has 930 lines (limit: 800)` — the
   85bb4b4a4 style commit fixed THAT, but it left the file with a stray
   orphaned comment fragment and a duplicated `RegistryHasSignal` body glued
   into migration.go with a mangled signature line
   (`func RegistryHasSignal(...) {id string, ...) {`). gofmt/go build still
   parsed it because the second copy became the function's body — repaired:
   registry.go now keeps only `SignalKindForSignal`; `RegistryHasSignal`
   lives once, in migration.go, rewritten over `ListAll` (registry.go 795→791
   lines, all files ≤800, `scripts/source-readability-audit.sh` PASS on all
   three checks).
2. `TestReadSignalsForTestSortsStably` lived in `read_signals_test_helper.go`
   — NOT a `_test.go` filename, so Go never compiles it into the test binary
   and no CI job runs it (AGENTS 5.3). Moved into the new
   `internal/observability/read_signals_test.go`; it now runs in
   `PR · Go unit · packages` like every other package test (verified
   `--- PASS` with `-run` locally, and `go test ./internal/observability/`
   counts it).

## P1 / P2 / P4 against the code (r2-verdict closure)

P1 (re-booking survives the next registration): RebookLegacySignals runs
INSIDE the single RegisterProviderSignals mutation, before the (ID, provider)
replacement, and books foreign-owned legacy records under the DERIVED
`<provider>:<project>:<legacy-id>` grammar, which the replacement selector
(`<provider>:<project>`) can never match; the caller's own record converges
onto the caller's canonical registration identity, which the replacement then
REFRESHES (not drops) in the same pass. Coverage added by this lane:
`TestRegisterProviderSignalsRebooksLegacyBeforeReplacement` (both records
coexist, owners verbatim) and
`TestRebookLegacySignalsConvergesCallerOwnRecordToRegistrationID` (the
convergence branch — this was the uncovered path: the r2 mutant "remove
convergence" passed the whole suite before this test existed; see mutation
proofs). The appA/appB production-path integration test
`TestRegisterKeycloakSignalsPreservesLegacySourceForOwner` already covers
metrics-enabled and metrics-disabled; the maintainer field-preservation
acceptance (network, target, descriptor, enabled state) is now proven by
`TestRebookLegacySignalsPreservesEverySourceField`.

P2 (change-aware under the mutate lock): `mutateChanged` takes the SAME
`<registry>.lock` flock (no parallel migration lock) and returns
changed=false without creating or replacing the file when serialization is
byte-equal or nothing was found and nothing produced. r2's coverage was only
byte-comparison; this lane adds the file-REPLACEMENT witness (mtime unchanged
across a no-match migration over an existing file) and the never-create
witness, in `TestMigrateScopedIsIdempotentAndWritesNoByte`. Mutant "always
write" now fails that test (it passed r2's version).

P4 (corpse visible BEFORE the re-booking, not after):
`TestLegacyKeycloakMetricsSourceCorpseProvesTheBug` proves the pre-migration
state per the listing contract: the record EXISTS in the registry file
(RegistryHasSignal true) but is NOT listable for any owner (route-2
environment derivation fails closed on a project-less ID) — that is what
made it an unreachbable corpse. The integration test witnesses the same
pre-state and then asserts the migrated record IS listable and removable by
its derived identity for its original owner. (The r1 verdict's literal
"visible in List before" is unsatisfiable by the environment-derivation
contract itself: a pre-scoping ID carries no environment; the lane documents
and proves the equivalent: present-before, observable-after.)

## mutation proofs (both runs word for word)

Mutant A — convergence branch removed (`migrated = append(migrated, existing)`
instead of booking onto registrationID):

```
--- FAIL: TestRebookLegacySignalsConvergesCallerOwnRecordToRegistrationID (0.00s)
FAIL	github.com/mcpdev80/baseharbor/internal/observability	0.015s
ok  	github/mcpdev80/baseharbor/internal/identityprovider	8.956s
```

Mutant B — change-aware write removed (`if false && bytes.Equal(...)`):

```
--- FAIL: TestMigrateScopedIsIdempotentAndWritesNoByte (0.00s)
FAIL	github.com/mcpdev80/baseharbor/internal/observability	0.025s
ok  	github/mcpdev80/baseharbor/internal/identityprovider	9.219s
```

Mutant C — derived re-book removed entirely (pre-fix behavior: record dropped):

```
--- FAIL: TestRebookLegacySignalsPreservesEverySourceField (0.00s)
--- FAIL: TestRegisterProviderSignalsRebooksLegacyBeforeReplacement (0.00s)
FAIL	github.com/mcpdev80/baseharbor/internal/observability	0.009s
--- FAIL: TestRegisterKeycloakSignalsPreservesLegacySourceForOwner (0.00s)
FAIL	github/mcpdev80/baseharbor/internal/identityprovider	9.004s
```

All mutants reverted; the restored tree passes:

```
ok  	github.com/mcpdev80/baseharbor/internal/observability	0.010s
ok  	github/mcpdev80/baseharbor/internal/identityprovider	9.047s
```

## local checks

- `go build ./...` clean; `go vet` clean on both packages; `gofmt -l internal/` empty
- `bash scripts/ci-fast-check.sh`: gofmt/vet/build/readability PASS, 293 script tests OK,
  "No candidate-added validation checks. The trusted base plan remains the only merge requirement."
- `go test ./internal/observability/ ./internal/identityprovider/ ./internal/logs/ ./internal/application/ -count=1` all ok

## delivery witnesses

`git push --force-with-lease lane-origin HEAD:refs/heads/lane-0428-168-signal-id-migration`:

```
To https://github.com/mcpdev80/baseharbor.git
   85bb4b4a4..380c66c49  HEAD -> lane-0428-168-signal-id-migration
```

`git ls-remote lane-origin refs/heads/lane-0428-168-signal-id-migration refs/pull/1709/head refs/heads/develop` (post-push):

```
36d075fad77fa61ac8c153e979855546589b32c2	refs/heads/develop
380c66c49218a3f8c18d04412536acbc6a2c3a6d	refs/heads/lane-0428-168-signal-id-migration
85bb4b4a4cb84707cb15eedbe94dfb0b7fadc9a2	refs/pull/1709/head
```

(The refs/pull entry lags seconds behind the branch push; the PR-head refresh
and the exact-head CI run are recorded below as the terminal witness.)

Candidate SHA: 1fa78df421e521ab7aeaec05a58d6cf646ddf971 (frozen at coordinator
freeze directive 08:10Z; the earlier 380c66c49 is superseded, no dangling
work: 1fa78df42 sits directly on it, single final commit).

## freeze round (coordinator directive, 2026-11-20 08:10Z)

The coordinator ordered a freeze because a CODEX-REVIEW had been commissioned
while the lane was still pushing (reviewer verdict BLOCKED, "candidate changed
during review" — recorded in
evidence/r28-welle4-2026-11-20/codex-review-wave/1709-0428-168-r2.md; that
file's partial findings P1 largely-addressed / P2 addressed / P4 addressed /
packages-shard executes new tests stand, but it is no verdict). Per the
directive's rule 1, the one needed change still in the tree was landed in a
SINGLE commit, then silence — no further pushes until acceptance is ordered.

The change: the r2 review's provisional blocker, confirmed by this lane on
380c66c49 as still real. `ListKeycloakOwnerProjects` silently omitted an
application directory whose env-listing failed to read, and
`ownerProjectMaps` fell through scan errors to the caller-only map, so a
foreign owner's legacy record could be re-booked under the registering app's
project — an identity whose grammar lacks the owner anchor, failing closed in
listing (unobservable again). Fix:
- internal/identityprovider/keycloak_realization.go:323-347 — per-owner ReadDir
  errors and env-less owner directories now return an error (absent state stays
  (nil,nil): the legacy no-state case, preserved);
- :209-238 ownerProjectMaps propagates the error; a shared placement returns
  early (its records resolve via the sharing boundary, never the project
  grammar);
- :133-151 registerKeycloakSignals aborts BEFORE the registry mutation.
Tests (both deterministic, no sleep loops):
`TestRegisterKeycloakSignalsAbortsOnPartialOwnerStateScan` (aborted
registration leaves registry bytes + legacy record verbatim; the 0o000 seam
skips when the user may read 0o000 dirs — running as the unprivileged uid
1000 here, both subtests executed and passed) and
`TestListKeycloakOwnerProjectsReportsPartialScan`.
Mutation proof D (silent-omission restored verbatim):

```
--- FAIL: TestRegisterKeycloakSignalsAbortsOnPartialOwnerStateScan (0.00s)
--- FAIL: TestListKeycloakOwnerProjectsReportsPartialScan (0.00s)
FAIL	github.com/mcpdev80/baseharbor/internal/identityprovider	8.967s
```

Restored tree: observability/identityprovider/logs packages ok, go build/vet/
gofmt clean, ci-fast-check.sh clean, readability audit PASS.

## freeze witnesses (three lines, word for word)

(a) `git ls-remote lane-origin refs/heads/lane-0428-168-signal-id-migration refs/pull/1709/head`

```
1fa78df421e521ab7aeaec05a58d6cf646ddf971	refs/heads/lane-0428-168-signal-id-migration
1fa78df421e521ab7aeaec05a58d6cf646ddf971	refs/pull/1709/head
```

(b) `git fetch lane-origin refs/pull/1709/head` first (refs/pull already
measured equal to the head), then
`git merge-base --is-ancestor 36d075fad77fa61ac8c153e979855546589b32c2 1fa78df421e521ab7aeaec05a58d6cf646ddf971`

```
ANCESTOR_YES   (exit 0; develop 36d075fad77f is an ancestor of the frozen head)
```

`git log --oneline 36d075fad..1fa78df42` lists ONLY this card's chain:
1fa78df42 / 380c66c49 / 85bb4b4a4 / 4d3494ea7 / 48d05ab8d / 9d905cbd1 — six
own commits, no foreign candidate carried on top.

(c) Last pull_request run on the frozen head: `44700696085` (head
1fa78df421e5, in_progress at the time of writing; the terminal state and
conclusion of every selected check are recorded below under §4.6).

## repo-rule compliance

- No `.github/**` writes; no workflow_dispatch; no reruns (CI policy: this
  PR's tests ride the existing `PR · Go unit · packages` shard — non-CLI
  Go packages, no name filter — so no workflow change was needed).
- No `git add -A`; only the five named files were staged.
- No subagents; every step executed in this session.
- Write-set respected: nothing touched in cmd/baha/app_status_result.go,
  internal/application/perses_datasources*, internal/capability/perses*.go.
- One candidate branch only (lane-0428-168-signal-id-migration); no second
  branch was created or deleted.
- Evidence lives only in baseharbor-plan (this file); product repo untouched.

## CI terminal witness (§4.6, watched by this lane)

Run 44700696085, `pull_request`, exact head 1fa78df421e521ab7aeaec05a58d6cf646ddf971:

```
{"conclusion":"success","headSha":"1fa78df421e521ab7aeaec05a58d6cf646ddf971","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/44700696085"}
```

Check-runs on the exact head (`gh api .../commits/1fa78df42/check-runs?per_page=100`,
total / not-completed / failures):

```
35	0	0
```

Both former failures are closed at this head: `PR · Source format` and
`PR Selected Checks` completed success. Notable executed jobs (from the watched
run log): `PR · Go unit · packages` (includes internal/observability and
internal/identityprovider, no name filter — the new tests run), `PR · Go unit ·
cli-0/cli-2` success, `PR · Selected Runtime (atomic/docker/identity, docker,
identity) / Executed docker · identity` success (candidate SHA resolution,
rootless runtime prep, gate execution, cleanup all ✓), `PR Selected Checks`
success including "Require complete selected Go shard coverage". The 16 skipped
cells (native matrix, Targeted HA, release, draft jobs) are skipped by
selection and are NOT reported as passes.

## cleanup / cleanliness

`docker ps` on this host: no containers started or stopped by this lane (the
daemon is absent from this coordinator host); no compose projects; no test
VMs were part of this mission. Worktree scratch lives under
/tmp/opencode/x-168r3-wt and /tmp/opencode/x-168r3-plan only; the dead
previous-lane stub /tmp/opencode/x-168r2-wt (0 bytes, prunable) was removed
by this lane. Stray test temp dirs are under Go's own cleanup.
cleanliness: this lane leaves the machine as it found it plus the two
/tmp/opencode worktrees and the pushed candidate.

## END

END_DONE x-168r3: takeover complete — r2 blocker fixed, P1/P2/P4 coverage with mutation proofs A-D, FROZEN candidate 1fa78df421e521ab7aeaec05a58d6cf646ddf971 on PR #1709, run 44700696085 completed SUCCESS at exact head (35 checks, 0 open, 0 failure). No further pushes until acceptance is ordered.
