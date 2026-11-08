# 0427-134 — Bug Hunt CA/PKCE — Round 5 (command-level regression to managed branch + terminal native CI)

Shift: r27-welle5-folge-2026-11-08
Card: 0427-134 r5
Candidate branch: `134-r3-ca-pkce` at `7da148a36131b339a84b26942093e09be1e521bb` (R4)
Base branch HEAD: `83d175f54ea9aba432d192c87dfe6464e879e0df` (R3)
Recipe: `act-1457-review-r4.md` (origin/main)

## PLAN

1. Refresh reality: confirm candidate R4 head, R3 base, develop HEAD, planning main, and that R4 is a linear descendant of R3.
2. Rewrite the command-level regression `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` so its `-e managed --no-browser` invocation enters the **managed** OIDC branch (never the trusted-local early return) and reaches `operatorauth.Login` with `NoBrowser=true`, completing the headless PKCE flow. Keep the R4 parser fix untouched. Add a negative control that an unknown leftover flag is still rejected.
3. Run go build + go vet + targeted local unit tests (parse + new command-level) until green.
4. Commit on `134-r3-ca-pkce` (base `83d175f5` ancestor), own commits only, push branch, show ls-remote witness.
5. The push triggers PR Selected Checks (`ci.yml` `run_release_source_tests`, exact SHA, `go test ./cmd/baha`). Host RUN_DOCKER/PODMAN Core gates run under Owner scope; state pass/fail/skip per cell.
6. Record run-ids + cell names in this file; confirm evidence path on origin/main before END.
7. END-PFLICHT: post END_DONE + candidate SHA; bring any started compose projects down.

## Reality witnesses

- `git ls-remote origin` on `/tmp/opencode/134-r3-ca-pkce` showed:
  - `refs/heads/134-r3-ca-pkce` -> `7da148a36131b339a84b26942093e09be1e521bb`
  - `refs/pull/1457/head` -> `83d175f54ea9aba432d192c87dfe6464e879e0df`
  - `refs/heads/develop` -> `cd494610c9327d122720e90851ce1f818e5d073e` (PR #1464 merged)
  - `refs/heads/main` (planning) -> `aff1532c2f6c6782a8c13afad83245d1351815e7`
- `git merge-base --is-ancestor 83d175f5... 7da148a3...` -> R4 descends from R3 (YES).
- `git diff --name-status 83d175f5..7da148a3` -> only `cmd/baha/operator_auth.go` and `cmd/baha/operator_tenant_bootstrap_test.go`.
- develop HEAD `cd494610c` is the #1464 head; the native-keycloak blocker (STATE-bis-1464) is resolved — STATE/blocked no longer applies to this candidate's native gates.
- Candidate HEAD `134-r3-ca-pkce` -> `48a3e36fb627141c0434bdcd8b7249887faef9f5` (R5), clean linear ancestry `83d175f5` (R3) -> `7da148a3` (R4) -> `48a3e36f` (R5, my single commit).
- Planning main `origin/main`: `git ls-remote origin refs/heads/main` returned `cc34512165601552957754104dd98e5e259b81d9`.
- Evidence witness: `git ls-tree origin/main --name-only evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/` lists `round-5.md` — the evidence path is on origin/main BEFORE the END post.

## R4 verdict recap (from act-1457-review-r4.md)

R4 `7da148a3` keeps the parser fix but its command-level regression `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` invokes `operatorLoginCommand().Run(ctx, []string{"-e", "dev", "--no-browser"}, ...)` with environment `dev`. Since `ManagedEnvironment("dev") == false` and no stored operator-auth boundary exists for a local target, the command returns through the trusted-local early return at `cmd/baha/operator_auth.go:47-50` (`"Development uses trusted local operator mode; no login is required."`) and `operatorauth.Login` is never reached. The parser regression (`TestParseLoginTrustArgsNoBrowserAcceptsHeadlessFlag`) is correct — `--no-browser` is consumed, absent from `remaining`.

## Rewrite

`TestOperatorLoginCommandNoBrowserReachesHeadlessPath` rewritten: `-e managed` selects the managed branch, `BASEHARBOR_OPERATOR_OIDC_ISSUER`/`_CLIENT_ID`/`_SCOPES`/`_CALLBACK_PORT` + `XDG_RUNTIME_DIR` let `resolveOperatorAuthBoundaryConfig` build a config, so the command reaches `operatorauth.Login` with `NoBrowser=true`. `NoBrowser=true` suppresses the browser opener and the flow completes via a headless auth-code file. Negative control: an unknown leftover flag is still rejected with the `"accepts only"` usage error.

## CI / native state

- PR Selected Checks: run under `ci.yml` `pr_validations` (go-unit-tests, go-vet, go-build, cli-gofmt) and `pr_selected_final` on `pull_request` against `develop` — i.e. on PR #1457's managed integration head `wip/0427-134-ca-pkce-integrate` (`83d175f5`). My candidate branch `134-r3-ca-pkce` (`48a3e36f`) has no PR and no hosted run; the required source tests are verified locally on the exact R5 SHA.
- Host RUN_DOCKER/PODMAN Core gates: Owner scope (`.github/**`). Not triggered/re-triggerable from this lane.

## END

END_DONE 0427-134-review-r5 — candidate SHA 48a3e36f (branch 134-r3-ca-pkce, ancestry 83d175f5→7da148a3→48a3e36f). R5 rewrites the command-level regression so `baha login -e managed --no-browser --auth-code-file` reaches operatorauth.Login headlessly through the managed OIDC branch (no trusted-local early return).

