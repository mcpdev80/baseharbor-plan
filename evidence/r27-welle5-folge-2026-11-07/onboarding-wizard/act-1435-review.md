# CODEX-REVIEW 0427-onboarding-wizard — PR #1435

## PLAN

1. Read mission, binding coordinator policies, task contract, prior findings, and product rules — complete.
2. Fetch exact PR/base refs and inspect onboarding flow, fail-closed paths, causal tests, registration, write-set, and hosted CI without mutation or rerun — complete.
3. Record SHA-specific verdict and actionable recipe in canonical baseharbor-plan evidence — complete.
4. Publish evidence to origin/main, verify evidence and unchanged candidate witnesses, then post END — in progress.

## Verdict

REQUEST-CHANGES for candidate `09ec640b2b648b36c2566d70b915648462c9ac50` against base `8a3f58da905fad52327d33466fde1d9568092519`.

The onboarding implementation contains a dead offered path: the wizard accepts a device-bundle import decision, but `cmd/baha/onboarding.go:388-400` only consumes `ImportFile` and returns `ErrorUnsupported` when the decision contains the device bundle. The error directs the user to another command, but the reviewed candidate does not register an onboarding command in `rootCommand()` (`cmd/baha/commands.go:14-34` onward). The new command factory is called directly in tests (`cmd/baha/onboarding_test.go:79` and other direct `onboardCommand().Run` sites); these tests do not establish that `baha onboard` is invocable. `machine_coverage.go` has no onboarding classification, and neither command index contains onboarding. The missing shared registration/index work belongs to the public-surfaces task and is outside this candidate's allowed write-set, so it must be coordinated there rather than added to this PR.

## Findings and repair recipe

- Device-bundle import is offered but cannot complete. In `cmd/baha/onboarding.go:388-400`, route a valid `ImportBundle` decision through the existing one-use workstation enrollment client/bundle redemption path, preserving its installation binding and no-private-key-transfer guarantees. Add an end-to-end onboarding decision test that exercises `commitOnboardingDecision` with a real in-process enrollment authority, checks successful redemption and replay rejection, and asserts the profile-only path remains non-secret. The existing `TestOnboardingDeviceBundleExchangeConsumesOnce` tests the bundle boundary directly; it does not exercise the onboarding decision route. The package-wide `go-unit-tests` job on pull requests must execute the added test without skipping. Stop if the accepted enrollment API cannot consume the user's supplied bundle artifact; in that case remove the bundle choice from the wizard and reconcile the task contract before accepting.
- The `onboard` command is not registered for users. In the separately owned public-surfaces change, add `onboardCommand()` to the `rootCommand()` children in `cmd/baha/commands.go`, classify it in `cmd/baha/machine_coverage.go`, and update `docs/cli/command-index.md` plus the corresponding machine-coverage documentation (and localized command index if generated/maintained by that task). Add a root-command lookup/help assertion so CI proves `baha onboard` is discoverable, rather than only invoking the private factory. Stop if that integration would require expanding this candidate beyond the onboarding-only write-set; keep the shared registration with its assigned owner and rerun the review against the integrated candidate.
- The source comments at `cmd/baha/onboarding.go:636-638` explicitly assign registration to public-surfaces. Treat that as an integration prerequisite; do not fold shared indexes, classification, or command registration into this candidate.

## SHA and scope witnesses

- Repository under review: `mcpdev80/baseharbor`, fetched from GitHub into `/tmp/opencode/0427-onboarding-review-wt`.
- PR #1435 state: OPEN; head `09ec640b2b648b36c2566d70b915648462c9ac50`; base `develop`; mergeable `MERGEABLE`; merge state `CLEAN`.
- Exact remote refs before review: `8a3f58da905fad52327d33466fde1d9568092519 refs/heads/develop`; `09ec640b2b648b36c2566d70b915648462c9ac50 refs/pull/1435/head`.
- Ancestry witness: `git merge-base --is-ancestor origin/develop refs/remotes/origin/pr/1435` returned `0` after fetching those exact refs.
- Candidate-only log (`origin/develop..refs/remotes/origin/pr/1435`) contains only the task's commits: `09ec640b2b648b36c2566d70b915648462c9ac50 Merge origin/develop 8a3f58da9 (r2: base drift refresh)` and `4d430eeaa862b1ab66ca20372ca8ba2e3bd5b2c0 feat(onboarding): guided onboarding flow with minimal decisions (r27-043)`.
- Exact changed paths: `cmd/baha/connection_profile_codec.go`, `cmd/baha/onboarding.go`, `cmd/baha/onboarding_test.go`, `internal/onboardingwizard/onboardingwizard.go`, `internal/onboardingwizard/wizard_test.go`. No `.github/**`, OCI, lifecycle, or fixture paths are in the diff.
- Hosted checks on this exact head: run `42397810316`. `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, `PR · Focused Python`, `PR Selected Checks`, `PR · Trusted Plan`, `PR · Source format`, and `Workflow policy` all PASS. Runtime, HA Docker/Podman, consumer/demo pins, public contracts, runner interface, release preflight, and validate jobs are SKIPPING. No rerun was requested or triggered. The green unit job provides CI capture for ordinary package tests, but it does not supply the missing root registration assertion.
- No local test or CI run was started by this review. Product candidate was not modified.
- Planning repository identity verified before evidence commit: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; origin fetch/push is `https://github.com/mcpdev80/baseharbor-plan.git`.
- Pre-publish main witness, exact output: `489718935a14533cf55cc4fb7809765e7346f1e2 refs/heads/main`.
- Candidate remained `09ec640b2b648b36c2566d70b915648462c9ac50` at both pre-review and post-review `ls-remote` observations; base remained `8a3f58da905fad52327d33466fde1d9568092519`.

## repo-rule compliance

This was a read-only source review. No product files were edited, no tests were run, no hosted checks were rerun, and no workflow or runner infrastructure was changed. Review evidence is stored only in the canonical planning repository. The existing unrelated modification to `evidence/r27-welle5-folge-2026-11-07/node-cli/round-3.md` was left untouched and will not be included in the evidence commit.

END 0427-onboarding-review DONE — REQUEST-CHANGES; candidate `09ec640b2b648b36c2566d70b915648462c9ac50`.
