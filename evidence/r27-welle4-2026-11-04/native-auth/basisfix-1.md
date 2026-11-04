# w97-basisfix — base-refresh (merge develop into work/r27-native-auth)

- Task: ABGABE-NACHHOL w97. The remote history had been rewritten by the earlier rebase-style push (w94s base commit c2adcc86 was gone from the branch tip; contents were carried over, good — but no other lane's merged commits were rebased). Two regelfaelle: (1) never rebase other lanes' merged commits, use merge next time; (2) develop f8ef4255 is NOT the ancestor of the earlier candidate 8f4cbd2b.
- Owner decision: full scope (option 3) — callable path + git-helper protocol + stderr redaction already delivered in the candidate; this round only refreshes the base.
- Coord f49a3303. Evidence SHA target: basisfix-1.md (bullets, no markdown checkboxes).
- END: END_DONE w97-basisfix: head=0958107f lsremote=0958107f | PR #1362 CI run 41815956903 terminal gruen; base f8ef4255 als Vorfahr integriert; natives Diff unveraendert.

## PLAN

- Step 1: Fetch origin develop; confirm develop = f8ef4255 (https transport repaired by coord via gh-credential remotes).
- Step 2: Merge origin/develop into work/r27-native-auth (rc=0 expected; END_BLOCKED mit datei:stelle on conflict).
- Step 3: Rebuild + retest (go build/vet/test + gofmt).
- Step 4: Push; ls-remote == new head.
- Step 5: Watch PR #1362 gates terminal green (base-refresh only, no other changes).
- Step 6: Publish evidence + board; post END_DONE.

## What changed (base-refresh only)

- Merge commit 5fee807264a714b965d92595c196769a8934ef07 = "Merge remote-tracking branch 'origin/develop' into work/r27-native-auth". Parents: 8f4cbd2b (w97 candidate) + f8ef4255 (develop). develop f8ef4255 is now a first-parent ancestor of the branch head.
- The develop update carries CI/script changes (.github/workflows/ci.yml, pre-release.yml, targeted-demo-acceptance.yml, scripts/develop-ecosystem-*.py, scripts/pr-stage-boundary.py, scripts/pr-consumer-followup.py, plus their tests). None touch internal/credential/native/.
- w97 native files (broker.go, caller_test.go, gitcredential.go, host.go, native_test.go) are byte-identical to the reviewed candidate 8f4cbd2b (same blob SHAs: 599c3ea6 / db98d7ed / 0c9b48d5 / c8998fc8 / 46b3853b). Native content is unchanged; only the base moved.
- Empty trigger commit 0958107f marks the base-refreshed head and re-fires the pull_request workflow (base-refresh only, no other changes).

## Verify (own run, base-refreshed)

- go build ./... rc=0.
- go vet ./internal/credential/... rc=0.
- gofmt -l internal/credential/ = empty (clean).
- go test ./internal/credential/... -count=1 = ok across credential, credential/native (19 tests incl. real-protocol + broker regressions), credential/openbao.
- ls-remote origin work/r27-native-auth == 0958107fb8be0f60a92d33b5327c1c8e5ef609b2 == local head.

## PR #1362 CI gates (own run 41815956903, terminal)

- Run 41815956903 (workflow "CI · Source & Quality", head 0958107f).
- go-build = success, go-vet = success, go-unit-tests = success, Source format = success, Workflow policy = success, PR Selected Checks = success.
- Product gates (Targeted HA docker/podman, Release Source Preflight, Exact Candidate, Consumer Pins, Selected Runtime, Public Contracts, Demo Pin) correctly SKIPPED — single-scope change to internal/credential/native does not trigger them.

## repo-rule compliance

- Merge, not rebase: other lanes' merged commits are not rewritten (w97 regelfall 1). develop brought in via `merge origin/develop` rc=0.
- Base-pflicht letzter schritt (w97 regelfall 2): develop f8ef4255 now a true ancestor; ls-remote confirms head.
- No product changes: only the base moved; native diff is byte-identical to the reviewed candidate.
- No new lane / no Scheinauftrag. Base-refresh is a maintenance operation on the existing candidate.

## END

END_DONE w97-basisfix: head=0958107f lsremote=0958107f | PR #1362 CI run 41815956903 terminal green (go-build/go-vet/go-unit-tests/Source-format/Policy all success, product gates skipped); develop f8ef4255 merged as ancestor via merge rc=0, native diff unchanged; base-sauberer Kopf fuer Luna.
