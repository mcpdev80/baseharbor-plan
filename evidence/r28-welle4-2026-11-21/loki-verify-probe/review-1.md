ROLLE: REVIEW

**Verdict: REQUEST CHANGES**

The requested probe/precondition subtests and all three client-certificate fixture repairs are correct. However, two adjacent tests of `VerifyPersesLokiDatasourceHealth` still accept any non-nil error, contrary to the mission's explicit rule that every refusal in this health-test family must verify its error identity. The failure is limited to test precision; production code and this PR's write-set are otherwise correct.

## PLAN

1. Verify the real GitHub remotes, frozen PR #1734 head/base/refs, ancestry, exact commit and changed-file set. Complete.
2. Read card 0428-212 and lane/H-V23 evidence; inspect acceptance and old/new Loki tests. Complete.
3. Search all `client-cert.pem` references in the exact candidate tree; verify the known sites and check for another fixture site. Complete.
4. Compare PR #1734 with superseded #1732; inspect exact-head package/owner and CLI CI states. Complete.
5. Recheck candidate SHA; write verdict, recipe, session/model/time and END. Complete.
6. Publish only this review file to plan main and verify its remote path and plan SHA. In progress.
7. Post final END_DONE to coordinator. Pending.

## Review metadata

- Session ID: not exposed by this interface.
- Model: GPT-6 Codex.
- Backend: not exposed by this interface.
- Review time: 2026-11-21 01:34 UTC.
- Candidate: `mcpdev80/baseharbor#1734`, head `75770bd2d0434bfed11d7c1b106064a5a08d5a51`.
- PR head before review: `75770bd2d0434bfed11d7c1b106064a5a08d5a51` (`refs/pull/1734/head`).
- PR head after review: `75770bd2d0434bfed11d7c1b106064a5a08d5a51` (`refs/pull/1734/head`).
- Base: `develop` at `40cb28c758b02960356434b630086a341ebe1738`; PR base SHA and live `refs/heads/develop` match.

## Candidate and provenance

First Git action / remote guard:

```text
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v
lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)
lane-origin https://github.com/mcpdev80/baseharbor.git (push)
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)
upstream https://github.com/mcpdev80/baseharbor.git (fetch)
upstream https://github.com/mcpdev80/baseharbor.git (push)
```

PR API:

```text
gh api repos/mcpdev80/baseharbor/pulls/1734 --jq '[.head.ref,.head.sha,.base.ref,.base.sha,.state,.draft,.mergeable,.mergeable_state,.updated_at]'
["lane-0428-212-loki-verify-probe","75770bd2d0434bfed11d7c1b106064a5a08d5a51","develop","40cb28c758b02960356434b630086a341ebe1738","open",false,true,"blocked","2026-11-21T00:41:03Z"]
```

Remote refs:

```text
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-212-loki-verify-probe refs/pull/1734/head refs/pull/1732/head
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
75770bd2d0434bfed11d7c1b106064a5a08d5a51 refs/heads/lane-0428-212-loki-verify-probe
75770bd2d0434bfed11d7c1b106064a5a08d5a51 refs/pull/1734/head
bddb27e6251ec6bc76574a1dcdb13fc7ce017f24 refs/pull/1732/head
```

Exact shallow Git fetch at `/tmp/opencode/codex-rev-cli2b-1733-wt/baseharbor` used the real GitHub URL. `git merge-base --is-ancestor origin/develop origin/pr-1734` exited `0`. `git log --oneline origin/develop..origin/pr-1734` listed only the candidate's three commits: `75770bd`, `430e272`, `0dc299c`. `git diff --name-only origin/develop...origin/pr-1734` output:

```text
internal/logs/loki_test.go
```

PR file API independently returned only `internal/logs/loki_test.go`. The write-set is within the card; no change to `internal/serviceaccess/**`, `internal/logs/loki_datasource.go`, or `.github/**`.

## 1. Two named probe/precondition cases

Card `t-20261121-loki-verify-probe` requires a materialized-PKI/unreachable-endpoint probe error and a separate unmaterialized-PKI precondition error, each identified by content or type (`Acceptance criteria` 1-2). The candidate implements both:

- `internal/logs/loki_test.go:403-410` names `UnreachableLokiIsRejectedByTheProbe` and `UnmaterializedPKIFailsClosedAsPrecondition`.
- The probe case at `:417-440` materializes the fixture, checks all five CA/server/client PEM files exist (`:420-425`), closes its listening server before querying (`:427-430`), requires a non-nil error (`:433-436`), then requires the probe-specific `perses Loki datasource query for source ` prefix and rejects missing-PKI signatures (`:437-440`). This cannot pass on the `load Loki service access identity` / `os.ErrNotExist` fixture error.
- The precondition case at `:447-463` first asserts `ca.pem` is absent with `errors.Is(err, os.ErrNotExist)` (`:450-453`), calls the health verifier, then requires the identity-load prefix, `os.ErrNotExist`, and the PKI path (`:454-463`).
- `TestPersesLokiDatasourceVerifyNeverReportsHealthy` calls both at `:359-370`.

The lane evidence records the pre-fix red at `loki_test.go:370/404` and the prior hosted failures naming missing `client-cert.pem` at old lines 522 and 586 (`round-1.md:33-46`). It records the two-part passing subtests and `ok github.com/mcpdev80/baseharbor/internal/logs` (`:75-92`) at the final candidate. The final hosted run independently executes and passes this package, detailed below.

## 2. Three fixture sites and whole-tree search

The three owner-addendum cases are present at the candidate's `TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` (`loki_test.go:648`, probe/precondition subtests `:702-705`), `TestPersesLokiDatasourceMultiSourcePartialMatchability` (`:715`, subtests `:766-769`), and `TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` (`:778`, subtests `:828-831`). Each fixture calls the shared `materializeLokiServiceAccessPKI` helper (`:656`, `:723`, `:786`); that helper writes the signed client keypair at `:623-632`. Thus all three identified tests now materialize the client material they require. Their prior line references in the lane evidence are 671, 751, and 813; those are the corresponding updated call/test sections after the diff reshaped the tests.

The requested `git grep -n "client-cert.pem" -- internal` was independently checked against the exact candidate tree by streaming the GitHub tarball at the frozen SHA through grep (no checkout files written). Relevant output:

```text
mcpdev80-baseharbor-75770bd/internal/logs/loki_test.go:358:... missing service-access PKI client-cert.pem stat.
mcpdev80-baseharbor-75770bd/internal/logs/loki_test.go:401:... non-existent client-cert.pem ...
mcpdev80-baseharbor-75770bd/internal/logs/loki_test.go:421:... "client-cert.pem" ...
mcpdev80-baseharbor-75770bd/internal/logs/loki_test.go:632:... WriteFile(..."client-cert.pem"...)
mcpdev80-baseharbor-75770bd/internal/logs/render.go:105:... loki-access/client-cert.pem ...
mcpdev80-baseharbor-75770bd/internal/serviceaccess/pki.go:485:... filepath.Join(dir, "client-cert.pem") ...
```

Other matches are unrelated application, runtime-executor, OpenBao, telemetry, or generic service-access fixtures. Within the Loki test file, the only deliberately unmaterialized PKI health case is the explicit precondition test; `TestPersesLokiDatasourceVerifyBindsServiceAccessClient` also intentionally leaves it absent. No fourth missing-client-material fixture for a purported reached-probe case was found.

## 3. Error-identity rubric — blocker

The newly split card cases and the updated no-match case are content/type-bound. In particular, the no-source-match refusal checks the exact `no authorized Loki source produced a matching stream` text at `loki_test.go:802-811`; it is not a bare error check.

Two existing refusals in the same Loki health-verification family still pass on any error:

- `TestPersesLokiDatasourceVerifyFailsClosedWithoutProbe`, `internal/logs/loki_test.go:343-350`, only asserts `err != nil` at `:348-350`. The manifest has the management UI and Perses unselected. The production verifier has a specific error for this precondition at `internal/logs/loki_datasource.go:364-365`: `perses Loki datasource requires the observability management UI and Perses selected in the manifest`.
- `TestPersesLokiDatasourceVerifyBindsServiceAccessClient`, `internal/logs/loki_test.go:466-481`, leaves service-access PKI absent but only asserts `err != nil` at `:478-481`. The production path wraps the specific material-load error as `load Loki service access identity` at `internal/logs/loki_datasource.go:399-401`.

The new explicit subtest covers the same missing-PKI identity more rigorously, but these two health-verification refusals remain green on unrelated errors. The mission's rule says any such case is REQUEST CHANGES. This does not identify a defect in the new unreachable-probe witness; it is a test-precision gap in the candidate's same-file health-test family.

## 4. Superseded PR #1732 comparison

PR #1732 is `CLOSED`, `mergedAt=null`, and its only file is `internal/logs/loki_test.go` (+32/-0). Its patch signs and writes `client-cert.pem` plus `client-key.pem` in `materializeLokiServiceAccessPKI`. PR #1734's only file is the same test file; its helper now calls `materializeLokiServiceAccessPKIWithClient(..., true)` and signs/writes that same client pair (`loki_test.go:534-635`), while the separate unmaterialized test bypasses the helper deliberately. PR #1734 therefore supersedes #1732's fixture content and adds the focused witnesses; it is a content successor, not an ancestry/branch claim. The package cell at this exact head confirms the coverage is now green.

## 5. Exact-head CI and GATE-FAIL state

Run `44845451055`: event `pull_request`, head SHA `75770bd2d0434bfed11d7c1b106064a5a08d5a51`, terminal `completed/failure` at `2026-11-21T00:48:15Z`.

- `PR · Go unit · packages`: completed/success; raw job output says `ok github.com/mcpdev80/baseharbor/internal/logs 0.194s` and `PASS all non-CLI Go package tests`. This is the card's required `./internal/logs` shard and it executed at the exact candidate.
- `PR · Go unit · owner`: success.
- `PR · Go unit · cli-0..3`: failure; `PR Selected Checks`: failure. Example final-run line from `cli-0`: `main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.` These are `cmd/baha` failures, outside this PR's write-set.
- The lane evidence itself has a `GATE-FAIL 0428-204` section (`round-1.md:123-139`, and again at `:195-206`); the classification is in the akte, not merely the END message. The card-required packages cell is successful, but the aggregate remains red due to 0428-204. No rerun or workflow dispatch was initiated.

## Recipe and stop criterion

In `internal/logs/loki_test.go:346-350`, assert that the no-probe refusal contains the specific manifest-selection error from `internal/logs/loki_datasource.go:364-365`. In `internal/logs/loki_test.go:470-481`, assert `errors.Is(err, os.ErrNotExist)` and the `load Loki service access identity` prefix for the deliberately absent PKI. Keep both fixes in the card's allowed test file; do not change production code or service-access ownership.

Test requirement: run `go test ./internal/logs -run 'TestPersesLokiDatasourceVerify(FailsClosedWithoutProbe|BindsServiceAccessClient)$' -count=1` and confirm an unrelated error cannot satisfy either assertion; the existing `PR · Go unit · packages` route must run these tests in the same candidate. Stop when both refusals identify their intended preconditions and the packages cell is green; stop and report if that requires production or forbidden-file changes.

Separate CI state: resolve GATE-FAIL 0428-204 in its owning work before merge; the red CLI cells are not a 0428-212 content finding, but the failed `PR Selected Checks` aggregate remains a merge blocker.

## Evidence publication

Planning evidence belongs to `baseharbor-plan` only. The isolated plan clone remote was verified as `origin https://github.com/mcpdev80/baseharbor-plan.git`. `git fetch origin main` advanced its remote-tracking ref to `debcfe60b02a1b18c697485fe80e519b79e8e1fd`; `git log --oneline origin/main -5` showed the current five entries. `git rebase origin/main` was attempted but refused because this shallow `--no-checkout` clone represents absent tracked worktree files as local deletions; no local commit exists to replay. The remote `ls-remote` and GitHub API both confirmed main at `debcfe60...`. To avoid touching the shared checkout or materializing the full plan worktree under the disk quota, this single review file will be committed on current plan `main` through the GitHub Contents API; no force update is used.

## END

END_DONE codex-rev-cli2b: REQUEST CHANGES; two Loki verifier refusal tests remain error-only; candidate 75770bd2d0434bfed11d7c1b106064a5a08d5a51.

Remote evidence-path witness from the GitHub tree API (mode/type/blob/path, equivalent to the requested `ls-tree` line):

```text
100644 blob 65c50beb7d9417d8b84088e4d75360b35e655d5b	evidence/r28-welle4-2026-11-21/loki-verify-probe/review-1.md
```

The file was present on plan `main` at blob `65c50beb7d9417d8b84088e4d75360b35e655d5b`; initial evidence commit: `cb2bf7fe6afc21ff40e7f8d0493d1d7da65cba98`.
