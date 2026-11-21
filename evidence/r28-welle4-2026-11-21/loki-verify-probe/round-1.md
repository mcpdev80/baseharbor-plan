# 0428-212 loki health verify must reach the probe, not a missing-file exit — round 1

Lane: w227-0428-212-lokiprobe · Card: t-20261121-loki-verify-probe · Release: v0.4.28

## PLAN

1. Claim card via `plan.py claim`, commit + push claim (plan a83fe090).
2. Reality check (4.1): record develop SHA, read the three files, run the test locally, capture the verbatim failure line.
3. Owner addendum (n227): find ALL THREE client-cert.pem fixture sites via git grep + run 44841930757 / job 136652290169 log.
4. Split each affected test into two named subtests: (a) PKI materialized + unreachable endpoint -> probe rejection asserted by content, distinct from missing-file; (b) PKI unmaterialized -> precondition asserted explicitly.
5. Write-set check: only `internal/logs/loki_test.go`; stop + report file:line if any site needs `internal/logs/loki_datasource.go` or `internal/serviceaccess/**`.
6. Branch from the develop head, commit, one PR (base develop, draft=false), delivery proof via ls-remote.
7. One terminal hosted run at the exact head, observed to terminal state (4.6); cli cells may stay red -> GATE-FAIL 0428-204.
8. Evidence acta in baseharbor-plan, push, verify on origin/main; END post with head-sha, run-id, plan-sha.

## Base attestation and provenance

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)` — the planning repo at the canonical path.
- Branch cut point (measured with `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`):
  develop head `40cb28c758b02960356434b630086a341ebe1738`; branch `lane-0428-212-loki-verify-probe`.
- `git merge-base --is-ancestor 40cb28c758 HEAD` -> true (ANCESTOR-OK in transcript).
- `git log --oneline origin/develop..HEAD` lists only this lane's own commits.
- `git diff origin/develop...HEAD --name-only` -> `internal/logs/loki_test.go` (write-set respected; no change touches `internal/logs/loki_datasource.go` or `internal/serviceaccess/**`).

## Before (verbatim failure evidence)

The card test PASSED vacuously at develop (err != nil came from the fixture, not the probe):

    === RUN   TestPersesLokiDatasourceVerifyNeverReportsHealthy
    --- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy (0.00s)

With the strengthened witness applied to the OLD fixture (client material not written), subtest (a)
fails on exactly the missing-file line the hunt predicted:

    loki_test.go:370: PKI material /tmp/.../providers/loki/shared/service-access/pki/client-cert.pem must exist for the probe path: stat /tmp/.../service-access/pki/client-cert.pem: no such file or directory
    loki_test.go:404: error must be the missing client-cert.pem stat (os.ErrNotExist), got: perses Loki datasource health client: load Loki service access identity: stat /tmp/.../service-access/pki/ca.pem: no such file or directory

Hosted witness for the same defect class, PR #1650 run 44841930757, job 136652290169
(`PR · Go unit · packages`, 2026-11-21T00:11:23Z), verbatim:

    --- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource (0.00s)
        loki_test.go:522: health must pass for a healthy multi-source Loki: perses Loki datasource health client: load Loki service access identity: stat /tmp/TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource3574244910/001/providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
    --- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability (0.00s)
        loki_test.go:586: health must pass when at least one source is verified: perses Loki datasource health client: load Loki service access identity: stat /tmp/TestPersesLokiDatasourceMultiSourcePartialMatchability2537073117/001/providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
    --- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed (0.00s)

## The three sites (owner addendum n227)

The packages-shard protocol names exactly three tests whose "not healthy"/"healthy" verdict came from
the missing `service-access/pki/client-cert.pem` stat instead of a reached probe:

1. `TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource`
2. `TestPersesLokiDatasourceMultiSourcePartialMatchability`
3. `TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed`

The card test named in the mission, `TestPersesLokiDatasourceVerifyNeverReportsHealthy`, is the fourth
vacuous site from the original card text and is split the same way. All four now carry the two-part
witness: `UnreachableLokiIsRejectedByTheProbe` (complete PKI + closed port -> error must start with
`perses Loki datasource query for source ` and must carry NO missing-file evidence) and
`UnmaterializedPKIFailsClosedAsPrecondition` (no PKI -> error must be the `load Loki service access
identity` wrapper with `os.ErrNotExist` on the pki dir, asserted as its own case). The three passing
multi-source verdicts additionally assert the witness server recorded per-source queries
(`assertNoMissingPKIFileEvidenceInPass`), so a green verdict cannot short-circuit around the identity.

## Fix, all inside internal/logs/loki_test.go

Root cause was fixture-side: `materializeLokiServiceAccessPKI` wrote only CA + server material, but the
managed-local mTLS policy makes `serviceaccess.ExistingTLSMaterial` require client material
(`internal/serviceaccess/pki.go:112-116`, `requiredMaterialPaths` at `:491-497`), so the health path died
before the probe. The helper now also signs a client certificate/key pair from the same throwaway CA
(with the server-auth EKU the client requires on the server leaf), so production code is untouched.
No stop-and-report needed: none of the four sites required `loki_datasource.go` or `serviceaccess/**`.

## After (verbatim passing evidence)

    --- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy (0.02s)
        --- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy/UnreachableLokiIsRejectedByTheProbe (0.00s)
        --- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy/UnmaterializedPKIFailsClosedAsPrecondition (0.00s)
    --- PASS: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource (0.02s)
        --- PASS: .../HealthyMultiSourceLoki (0.01s)
        --- PASS: .../UnreachableLokiIsRejectedByTheProbe (0.00s)
        --- PASS: .../UnmaterializedPKIFailsClosedAsPrecondition (0.00s)
    --- PASS: TestPersesLokiDatasourceMultiSourcePartialMatchability (0.01s)
        --- PASS: .../PartiallyMatchableMultiSourceLoki (0.01s)
        --- PASS: .../UnreachableLokiIsRejectedByTheProbe (0.00s)
        --- PASS: .../UnmaterializedPKIFailsClosedAsPrecondition (0.00s)
    --- PASS: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed (0.01s)
        --- PASS: .../NoSourceMatches (0.01s)
        --- PASS: .../UnreachableLokiIsRejectedByTheProbe (0.00s)
        --- PASS: .../UnmaterializedPKIFailsClosedAsPrecondition (0.00s)
    ok  	github.com/mcpdev80/baseharbor/internal/logs

Hosted PASS witness, run 44845451055 job 136663987987 ('PR · Go unit · packages'), conclusion
success. The per-subtest RUN/PASS lines above are reproduced from this lane's local run of the
identical head (75770bd2d); the job-level conclusion for the exact head is the hosted witness:

    Job 'PR · Go unit · packages': completed, conclusion = success

## PR, head, hosted runs

- PR: https://github.com/mcpdev80/baseharbor/pull/1734 (base develop, draft=false)
- Heads pushed: `0dc299ccb` (initial split), `430e2722c` (transient server-auth witness — reverted
  before the final head), final candidate `75770bd2d0434bfed11d7c1b106064a5a08d5a51` (reached-probe
  proof on passing verdicts).
- ls-remote delivery proof for the final head:

      75770bd2d0434bfed11d7c1b106064a5a08d5a51	refs/heads/lane-0428-212-loki-verify-probe
      75770bd2d0434bfed11d7c1b106064a5a08d5a51	refs/pull/1734/head
      (also observed mid-lane: branch ref at 0dc299ccb and 430e2722c, each pushed through the
      github URL resolved by `git remote -v`; `git push` never answered "Everything up-to-date")

- Runs (all observed by this lane to terminal state, 4.6):
  - 44844750668 (head 0dc299ccb): cancelled by supersession when the next head pushed.
  - 44844936135 (head 430e2722c): failure; `Go unit · packages` SUCCESS at that head.
  - 44845451055 (final head 75770bd2d): completed, conclusion **failure**.
    Terminal job table (final head):
    - Trusted Plan success · Native gate plan success · Source format success · Validation go-build
      success · Validation go-vet success · Focused Python success
    - **Go unit · packages SUCCESS** — the card's required shard: all four Loki datasource health
      witnesses with their new subtests pass in hosted CI at the exact final head.
    - Go unit · owner SUCCESS.
    - Go unit · cli-0/1/2/3 FAILURE — GATE-FAIL 0428-204 (see below).
    - `PR Selected Checks` aggregate: failure (carried only by the cli cells).
- GATE-FAIL 0428-204: cli cell failure line from run 44844936135 job log (identical family across
  cli-0..3):

      --- FAIL: TestAppCreateListShowPlan (0.01s)
      --- FAIL: TestAppInitCreatesCommitFriendlyRepositoryManifest (0.01s)

  These are `cmd/baha/**` tests owned by card 0428-204 (lane w216); the mission explicitly allows
  cli cells to stay red. Recorded as STATE; no second probe (5.4), no change in that write-set.
  The same four cli cells fail red at the final head 75770bd2d in run 44845451055 with this family
  of failures (`TestAppCreateListShowPlan`, `TestAppInitCreatesCommitFriendlyRepositoryManifest`,
  `TestAppInitSupportsDeterministicWorkloadSelection`, `TestAppListAllTargetsWorksAfterInstallationDestroy`,
  `TestAppPruneJSONOnlyValid`, …) — develop-inherited, not caused by this diff (this diff touches
  one file in `internal/logs/` only). Card 0428-211's handoff records the same develop-inherited
  cli redness, and the local reproduction of `TestMCPRegistrationCIInProcessDiscoverAndInvoke` on
  the pristine base shows the same `authentication_failed` signature on this host.

## How many of the three does this head heal

3 of 3. The three packages-shard failures named in the owner addendum all heal at this head (client
material fix + two-part witness). Related: #1732 (0428-202) attacks the same fixture; its branch
`lane-0428-202-lokifix` (bddb27e62) is NOT an ancestor of this candidate — this lane branched from
develop only, and the overlap in `materializeLokiServiceAccessPKI` is content-duplicate, resolved at
merge time on whichever lands first. No second PR is opened for #1732 (3.3.8: one PR per card).
0428-204 collision rule: this diff never touches `cmd/baha/**` or `internal/logs/loki_datasource.go`,
so no stacking onto `lane-0428-204-cli-operator-entrypoints` was needed.

## CI routing (gate rule)

The test identifiers are `TestPersesLokiDatasource*` in `internal/logs/`; they run in the existing
`PR · Go unit · packages` shard job selected by "Go unit shards for ./internal/logs/ (PR Selected
Checks)" in the card's test binding. No new test files and no route change were needed; no
`.github/**` edit is required.

## repo-rule compliance

- Claim published and pushed before any code edit (plan commit a83fe090).
- Write-set: only `internal/logs/loki_test.go`.
- No subagents; all steps executed in this lane's session.
- No containers/networks/volumes on the coordinator host: pure unit tests with in-process httptest servers only, no compose projects started, no docker commands run.
- CI policy honored: `bash scripts/ci-fast-check.sh` run before each push.
- Reality witnesses only via `git ls-remote` of the github URL.

## cleanliness

Before: `docker ps` untouched (this lane ran no docker commands at any point).
After: same.
cleanliness: no containers, networks, volumes or state directories created or left by this lane; caches live under /tmp/opencode/w227-cache and worktree scratch (.gocache/.gomodcache/.tmp) removed from the worktree before END.
ps-witness before and after are identical (4 ambient containers, none lane-owned):

    bc23a27cde84 bh-docker-dev-shared-postgres-1
    e3a4feb678b9 bh-docker-dev-shared-postgres-member-1-1
    c68981ab2616 bh-docker-dev-shared-postgres-admin-1
    0e02158517c8 bh-docker-dev-shared-openbao-admin-1

`docker network ls | grep -c w227` -> 0.

## Local pre-run failures of scripts/ci-fast-check.sh (host condition, STATE)

On this coordinator host the fast check shows one environmental Go failure unrelated to this diff:
- `TestMCPRegistrationCIInProcessDiscoverAndInvoke` (`cmd/baha`) fails identically on the pristine
  develop base in this worktree (verified with `git stash`): in-process MCP `app.list` answers
  `authentication_failed — Managed-environment machine operations require an authenticated
  BaseHarbor operator.` No `BASEHARBOR_*` variable is exported in the lane environment
  (`env | grep -c BASEHARBOR` -> 0), so the managed-environment decision comes from persisted
  state on this host, not from the diff. `cmd/baha` is outside this card's write-set and also
  matches the mission's allowance "cli-zellen duerfen rot bleiben".
- The Python suite (`test_pre_release_runtime_reuse`) needed `TMPDIR` redirected off the crowded
  `/tmp` tmpfs to run; with `TMPDIR=/var/tmp/w227tmp` only the same environmental registration
  failure above remained.

## Hosted run detail (44844936135, head 430e2722c)

- `PR · Go unit · packages` SUCCESS at head 430e2722c AND at the final head 75770bd2d (run
  44845451055, job 136663987987): the three former client-cert.pem failures are healed and the new
  subtests run green in the hosted required shard. The hosted job's raw text log is no longer
  fetchable after the fact (`failed to get run log: zip: not a valid zip file`), so the job-level
  conclusion is cited as the witness (5.4: no re-probing).
- `PR · Go unit · cli-0/1/2/3` FAILURE at develop-based heads with `cmd/baha` failures
  (`TestAppCreateListShowPlan`, `TestAppInitCreatesCommitFriendlyRepositoryManifest`, …) — same
  environmental signature as the local failure above. GATE-FAIL 0428-204: recorded as STATE, no
  second probe (5.4), no change under `cmd/baha/**` (0428-204 write-set).
END w227-0428-212-lokiprobe DONE
