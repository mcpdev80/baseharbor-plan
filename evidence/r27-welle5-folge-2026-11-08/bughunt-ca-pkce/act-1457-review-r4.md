# CODEX-REVIEW — 0427-134 R4 / PR #1457

## PLAN

1. Refresh and verify the exact R4 candidate branch, current PR head, develop, and relevant hosted CI state.
2. Review only `83d175f5..7da148a3`, checking the no-browser parser consumption and command-level proof.
3. Verify the exact file scope and linear ancestry from the reviewed R3 head.
4. Classify the native CI state against the 0427-137 rule and the #1464 integration without treating unrelated green checks as proof for this candidate.
5. Publish the SHA-specific verdict and correction recipe in this planning evidence file.

## Verdict

**ROLLE: REVIEW**
**URTEIL: KORREKTUR (REQUEST-CHANGES)**
**Reviewed candidate branch:** `134-r3-ca-pkce` at `7da148a36131b339a84b26942093e09be1e521bb`
**Reviewed baseline:** `83d175f54ea9aba432d192c87dfe6464e879e0df`
**Current PR #1457 head:** `83d175f54ea9aba432d192c87dfe6464e879e0df` (R4 is not yet on the PR)

### 1. Parser fix: pass; command-path regression: insufficient

The one-commit R4 delta changes exactly two files. In `cmd/baha/operator_auth.go`, `parseLoginTrustArgs` now captures `--no-browser` into `noBrowser` and consumes it instead of appending it to `remaining`. The command passes that value to `operatorauth.Login` in `TrustOptions.NoBrowser` at lines 61–65. The updated parser regression correctly asserts that `--no-browser` is absent from the remaining generic arguments. This repairs the parser behavior identified in R3.

The new `TestOperatorLoginCommandNoBrowserReachesHeadlessPath` in `cmd/baha/operator_tenant_bootstrap_test.go` does not prove the claimed production login path. It clears issuer, client-ID, and scopes, invokes `operatorLoginCommand` with environment `dev`, then expects the trusted-local no-login message. Production `operatorLoginCommand` returns at `cmd/baha/operator_auth.go:42–50` when no stored operator-auth boundary exists; `operatorauth.Login` at lines 61–65 is never called. The test does prove that the generic parser no longer rejects the option and that an unrelated unknown flag still fails, but not that the CLI forwards `NoBrowser=true` into headless OIDC login.

**Correction recipe:** keep the parser fix. Replace or extend the command-level regression so its command invocation enters the managed OIDC branch and reaches `operatorauth.Login` with `NoBrowser=true`. Use a deterministic local TLS OIDC fixture with the managed/test CA and auth-code file, or an equivalent narrow injection seam that observes the actual `TrustOptions` passed by the command. Assert that the authorization URL is emitted, the headless code-file flow completes, and no browser opener is invoked. Keep a negative control showing unknown leftover arguments remain rejected.

**Stop criterion:** the test must fail if the CLI returns through trusted-local mode before calling Login, if `--no-browser` is not forwarded, or if the browser path is opened; it must pass only after the command-entry headless login flow completes.

### 2. Scope and provenance

`git diff --name-status 83d175f54ea9aba432d192c87dfe6464e879e0df..7da148a36131b339a84b26942093e09be1e521bb` lists only:

- `cmd/baha/operator_auth.go`
- `cmd/baha/operator_tenant_bootstrap_test.go`

The branch head is one commit above R3, with `83d175f5` as its direct parent. The branch head is `7da148a3…` on the remote. No unrelated files or commits are in this delta.

### 3. Native CI state and 0427-137 / #1464 classification

The CI state must remain **STATE / not PASS for R4**. At review time the live PR still points to R3 (`83d175f5`), while R4 (`7da148a3`) has no hosted run. The last run on PR #1457's R3 head, `42467172096`, terminated with failures in `PR · Native Keycloak/Core · docker`, `PR · Native Keycloak/Core · podman`, `PR · Native destroy retry · docker`, `PR · Native destroy retry · podman`, and `PR Selected Checks`. No rerun or workflow dispatch was requested or performed.

The current 0427-137 task note requires relevant native tests on GitHub-hosted Docker and Podman runners, says missing/skipped/failed acceptance is not PASS, and assigns selector/workflow changes exclusively to the CI owner. PR #1464 is now merged as `cd494610c9327d122720e90851ce1f818e5d073e`; its exact-head run `42474092741` passes `PR · Native destroy retry · docker`, `PR · Native destroy retry · podman`, and `PR Selected Checks`. In that run, `PR · Native Keycloak/Core` is skipped. Therefore #1464 validates the repaired destroy-retry selector/fixture path but does not provide native Keycloak/Core or headless operator-login proof for #1457 R4. The #1464 green run is not transferable to the unpushed R4 candidate.

**CI-owner action / recipe:** after the command-level regression is corrected and R4 is advanced to the PR, observe the exact candidate's selected checks. The relevant hosted Docker and Podman acceptance must execute where required by the task/selector and pass; a skipped or missing relevant acceptance remains STATE, not PASS. Any selector or workflow change belongs to the CI owner under `.github/**`; this review changes no workflow and triggers no run.

### Stop criterion

Do not approve or advance R4 to the PR until the command-level regression demonstrably reaches and completes `operatorauth.Login` in headless mode. Then obtain exact-candidate hosted CI evidence; do not infer R4 status from R3 or #1464. If relevant native acceptance is skipped or missing after the CI-owner routing is resolved, keep the review open and report the missing gate by name.

## Evidence witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git` showed branch `134-r3-ca-pkce` at `7da148a36131b339a84b26942093e09be1e521bb`, develop at `cd494610c9327d122720e90851ce1f818e5d073e`, and PR #1457 head at `83d175f54ea9aba432d192c87dfe6464e879e0df`.
- `gh pr view 1457` reported open, base `develop`, head `83d175f54ea9aba432d192c87dfe6464e879e0df`, mergeable, with merge state unstable.
- The R4 source comparison is exactly `83d175f54ea9aba432d192c87dfe6464e879e0df..7da148a36131b339a84b26942093e09be1e521bb`; `git diff --check` passed.
- `gh run list --commit 7da148a36131b339a84b26942093e09be1e521bb` returned no run for R4.
- `gh pr checks 1457` showed the R3 run `42467172096` with the four named native failures and failed `PR Selected Checks`.
- `gh pr checks 1464` showed run `42474092741` with native destroy retry Docker/Podman and `PR Selected Checks` passing; Native Keycloak/Core skipped. PR #1464 is merged as `cd494610c9327d122720e90851ce1f818e5d073e`.
- Planning remote is `https://github.com/mcpdev80/baseharbor-plan.git`; the pre-publication `git ls-remote origin refs/heads/main` returned `7ae9c3c196aaa10e7a26f2932609358b7a0af6fe`.
- This was a read-only product review. No product files, PR refs, or `.github/**` files were changed; no tests, reruns, or workflow dispatches were performed.

## END

END_DONE 0427-134-review-r4 — KORREKTUR: parser fix and two-file scope pass, but the command-level regression takes the trusted-local early return and never reaches `operatorauth.Login`; R4 has no hosted run. #1464's green destroy checks do not establish R4 headless-login acceptance.
