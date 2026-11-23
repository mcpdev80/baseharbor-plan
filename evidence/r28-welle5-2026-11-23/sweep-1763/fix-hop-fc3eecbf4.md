# 0428-240 / #1763 FIX+HOP: build-identity mismatch diagnostic + additive re-hop onto develop b3df96348

- karte 0428-240 / t-20261122-broker-diagnostics-empty, PR #1763, sitz f0f6c8b4. PR-SWEEP #1763 FIX+HOP.
- Mission m_f0f_1763fix.md.g: develop zog zweimal weiter (jetzt b3df96348), der review-befund sitzt im head d1ee8ade. EIN push: fetch+rev-parse origin/develop verifizieren, merge --no-ff auf den branch (kein rebase/force). FIX cmd/baha/app_broker.go verifyRuntimeBrokerBuildIdentity (~:660). TARGETED REGRESSION in den diagnostics-tests. BELEG: katalog-diff LEER (228 comps byteidentisch), .github untouched, files == broker + diagnostics-test. push + ls-remote refs/pull/1763/head == NEU + PR-triggerter run bis terminal. Kein merge, kein cancel. akte sweep-1763/fix-hop-fc3eecbf4.md. 9142ab1f, keine subagenten, keine lokalen suites.
- #1763 sweep #1 done (re-hop onto develop 7880a8f6b, 27a482429). #1763 RUHE-HOP done (re-hop onto develop 0c1b8ca2f, d1ee8ade1, CI 45119822711). Prior fix attempt 74f7c2d25 failed CI on uncataloged app_broker_compat_test.go fail-loud.

## PLAN

1. read m_f0f_1763fix.md.g. FIRST ACTION before git. plan in board + evidence (numbered, no checkboxes). git remote guard (origin = github.com/mcpdev80).
2. fetch origin develop; rev-parse verifizieren. develop advanced f50b118f2 -> b3df96348 (concurrent merges).
3. FIX cmd/baha/app_broker.go verifyRuntimeBrokerBuildIdentity (~:660): mismatch branch reported expectedVersion twice (requires + got), hiding the observed runtime version. Restore actualVersion so diagnostic reports the TRUE observed version + CLI's expected version distinctly.
4. TARGETED REGRESSION in diagnostics-tests (cataloged app_broker_diagnostics_test.go): mismatch-fall asserts the TRUE observed value appears once, not duplicated from expected.
5. BELEG: katalog-diff LEER (228 comps byteidentisch). .github untouched. files == app_broker.go + app_broker_diagnostics_test.go only. gofmt + build + named regression tests.
6. additive git merge --no-ff origin/develop (re-hop onto newest develop). push + ls-remote refs/pull/1763/head witness; KEIN merge. PR-triggerter EXAKTER hosted run bis terminal. akte + cleanliness. POST 9142ab1f.

## BASE ATTESTATION

- develop HEAD (git ls-remote origin develop): b3df96348a9c56de00d67a060c9a5f0ddf6593d5 (advanced from cd9cc4836a -> 7880a8f6b -> 0c1b8ca2f -> f50b118f2 -> b3df96348; concurrent merges by other sessions).
- pre-fix prior #1763 branch tip: 74f7c2d25b9d6695cdf25390eacd6023a341a8f7 (failed CI on uncataloged compat test).
- post-fix head: 60844a770a67dd6c4a86e85ed2292933e64a88da (branch lane-0428-240-broker-diagnostics).
- merge parents (git log -1 %P) of 60844a770: c62808054... b3df96348... (additive merge --no-ff, KEIN force/rebase/amend).
- merge-base(60844a770, develop) == b3df96348 (purely additive; develop is an ancestor).
- ls-remote refs/heads/lane-0428-240-broker-diagnostics = 60844a770. ls-remote refs/pull/1763/head = 60844a770 (ref refetches on next CI).
- merge-base --is-ancestor origin/develop HEAD: YES.

## THE BUG (review-befund, fix verified by negative regression)

- verifyRuntimeBrokerBuildIdentity(actualVersion, actualCommit) mismatch branch (line ~663):
  - BUGGY (develop f50b118f2): `fmt.Errorf("%w: CLI version %s requires runtime version %s, got %s", errRuntimeBrokerIncompatible, expectedVersion, actualVersion, actualVersion)` — the 2nd and 3rd %s are BOTH actualVersion, so the diagnostic reports the observed runtime value in BOTH the "requires runtime version" and "got" slots while the CLI's expected version only appears once; a fix-loud that should name what the runtime actually is collapses to a duplicated observed value. Semantic mismatch: the message claims the CLI requires a version but never surfaces the CLI's expected version as distinct.
  - FIXED: `fmt.Errorf("%w: runtime version %s incompatible with CLI version %s", errRuntimeBrokerIncompatible, actualVersion, expectedVersion)` — reports the TRUE observed runtime version (actualVersion) first, the CLI's expected version (expectedVersion) distinctly. No value duplicated; the diagnostic is truthful.
- Negative regression proof: TestRuntimeBrokerBuildIdentityMismatchReportsTrueRuntimeVersion FAILS on the buggy code (`"CLI version 0.4.15 requires runtime version 0.4.14, got 0.4.14"` — observed value 0.4.14 duplicated) and PASSES on the fixed code.

## THE REGRESSION TEST

- Added TestRuntimeBrokerBuildIdentityMismatchReportsTrueRuntimeVersion to cataloged cmd/baha/app_broker_diagnostics_test.go (the file's ghost catalog row exists on develop: source.cmd.baha.app.broker.diagnostics.test.go, runtime_specific). Keeps catalog byte-identical develop.
- Assertions: the true observed runtime version (0.4.14) appears in the message; the CLI's expected version (0.4.15) also appears distinctly; the observed version appears exactly once (not duplicated from expected).

## DIFF vs develop b3df96348 (the mission's gates)

- catalog-diff origin/develop..HEAD -- scripts/pr-gate-coverage.json == LEER (0 lines). byteidentical. 228 components.
- scripts/ changed: 0 files. .github/ changed: 0 files.
- scope (git diff --name-only origin/develop HEAD): exactly 2 files:
  - cmd/baha/app_broker.go — the mismatch fix (line ~663), plus the sweep-1 refactor functions that were part of the #1763 fix (failRuntimeBrokerReadiness / runtimeBrokerReadinessDiagnostics wiring).
  - cmd/baha/app_broker_diagnostics_test.go — regression test appended (cataloged ghost row, no new row needed).
- git tree hashes: candidate 60844a770 vs develop b3df96348 (differ only in the 2 files).

## CI — EXAKTER hosted run 45131580969 @ 60844a770

- conclusion = SUCCESS. PR Selected Checks = success. ZERO failure jobs.
- Required jobs all success: PR · Trusted Plan = success, PR · Native gate plan = success, all Native docker-podman data-capabilities + coreless-lifecycle = success, all Go unit/build/vet/gofmt = success, PR · Focused Python = success.
- The prior fail-loud atomic/static/mcp (runs 45038621419/45033686480) and the 74f7c2d25 uncataloged-compat-test fail-loud are both RESOLVED — mcp.go base-cataloged on current develop, and the compat-test modification dropped from the diff.
- Regression guard confirmed in the hosted run: the new regression test executes in the Go unit CI group and passes on 60844a770 (FAILS on the buggy version, per local negative proof).
- KEIN merge (owner/codex after CODEX-REVIEW per policy 0.4.28+). PR #1763 is OPEN, not draft, base develop.

## repo-rule compliance

- catalog byte-identical develop (228 comps), 0 scripts, 0 .github. scope == app_broker.go + app_broker_diagnostics_test.go only.
- additive merge --no-ff, no force/rebase/amend. push + ls-remote witness (refs/pull/1763/head = 60844a770).
- no subagents. no local test suites (only go build, gofmt, and NAMED regression tests — never bare `go test ./cmd/baha/`).
- regression test wired into the existing Go unit CI group (no .github change needed; the file's catalog row already routes it).

## cleanliness

- docker ps -a: clean (header only, 0 containers).
- podman ps -a: only ambient shared infra (baseharbor-pre-release-registry, bh-p427 podman boot pods) — not mine, untouched.
- No test-owned containers/networks/volumes/state left behind by this lane.

## END

END_DONE w27-pr1627-0428-061-pull: #1763 FIX+HOP done. branch lane-0428-240-broker-diagnostics head 60844a770 (additive git merge --no-ff onto newest develop b3df96348; merge-base b3df96348 — KEIN force/rebase/amend). catalog-diff origin/develop..HEAD == LEER (byteidentical develop, 228 comps). scripts/ untouched (0). .github/ untouched (0). scope == app_broker.go (mismatch fix: report actualVersion, not duplicated) + app_broker_diagnostics_test.go (regression test). push 60844a770 + ls-remote witness refs/pull/1763/head=60844a770. PR #1763 not draft, base develop, KEIN merge. EXAKTER hosted run 45131580969 @ 60844a770 = FULL SUCCESS (PR Selected Checks = success, ZERO failures; fail-louds atomic/static/mcp + uncataloged compat test RESOLVED). regression guard FAILS-on-buggy / PASSES-on-fixed proven locally. akte published to baseharbor-plan origin/main. docker ps -a clean.
