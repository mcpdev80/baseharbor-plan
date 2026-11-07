# Evidence: 0427-onboarding-wizard (t-20261018-r27-onboarding-wizard), Round 2

Lane: 0427-onboarding-wizard (flash worker). Correction round per coordinator
mission 0427-onboarding-wizard-r2.txt on candidate PR #1435.
Repository: mcpdev80/baseharbor. Branch: lane/0427-onboarding-wizard.

## PLAN

- Fetch origin/develop and merge forward to 8a3f58da9; re-verify ancestor rc0 and delta.
- Check the alleged #119 file collision against the actual PR diff; neutralize by checkout of origin/develop copies if any were present.
- Re-run local checks (build, gofmt, vet, onboarding suites, registration/fence tests).
- Push one coherent r2 candidate, watch hosted pr-check on the final SHA to terminal, record run-id and status.
- Publish this round-2 evidence to baseharbor-plan origin/main and END the lane.

## (a) Drift fix

- origin/develop at r2 start: 8a3f58da905fad52327d33466fde1d9568092519 (was not an ancestor of round-1 head 4d430eeaa; mission flag correct).
- Merge commit 09ec640b2 "Merge origin/develop 8a3f58da9 (r2: base drift refresh)"; delta carried only this lane's five files.
- Ancestor witness: `git merge-base --is-ancestor origin/develop HEAD` rc0 (printed ANCESTOR_RC0) at 09ec640b2.

## (b) #119 collision — verified and answered

- Actual diff witness: `gh pr diff 1435 | grep "^diff --git"` listed exactly five files: cmd/baha/connection_profile_codec.go, cmd/baha/onboarding.go, cmd/baha/onboarding_test.go, internal/onboardingwizard/onboardingwizard.go, internal/onboardingwizard/wizard_test.go.
- `git diff --name-only origin/develop...HEAD` on the round-1 head showed the same five files. The three #119-owned files (cmd/baha/application_registry_source.go, internal/orgconfig/source_oci.go, cmd/baha/application_registry_pull_error_test.go) were NOT in this lane's write-set: their content at 4d430eeaa came solely from the base 06e4b1eaa, while #119 changed them on develop between 06e4b1eaa and 8a3f58da9. They appeared as "touched" only because round 1 lagged behind develop.
- After the r2 merge, all three files equal origin/develop byte-for-byte (merge took the #119 versions; `git diff --name-only origin/develop...HEAD` lists only the five onboarding files). No checkout override was needed; no parallel write occurred.
- The onboarding flow requires no OCI-pull or registry-source error path, so no sequencing QUESTION is needed.

## Candidate and hosted CI

- r2 candidate: 09ec640b2b648b36c2566d70b915648462c9ac50 (PR #1435 head, OPEN).
- Push witness (ls-remote): `09ec640b2b648b36c2566d70b915648462c9ac50 refs/heads/lane/0427-onboarding-wizard`.
- Hosted run watched to terminal by this lane: https://github.com/mcpdev80/baseharbor/actions/runs/42397810316 — status completed, conclusion success. All selected checks pass (Workflow policy, Source format, Trusted Plan, Focused Python, go-vet, go-build, cli-gofmt, go-unit-tests including the TestOnboarding* regressions); runtime/HA/consumer jobs report skipping per CI selection.
- Registration/fence tests locally green on the merged head (TestMachineCoverageCIRealTree, TestHumanCommandIndex, TestMachineDocumentation, classification/registration suite): the command stays unregistered in commands.go per the public-surfaces ownership finding of round 1.

## Local verification on the merged head

- `go build ./cmd/baha`: OK. `gofmt -l`: clean. `go vet ./cmd/baha ./internal/onboardingwizard`: clean.
- `go test ./internal/onboardingwizard ./cmd/baha -run TestOnboarding -count=1`: PASS both packages.
- No VM compose projects were started by this lane (nothing to tear down).

## Handoff

- Candidate PR #1435 (base develop, head 09ec640b2) is drift-free and collision-free; review/merge follows the standard protocol (CODEX-REVIEW / CODEX-MERGE).
- Open shared gap (unchanged, documented round 1): `baha onboard` registration into rootCommand(), machine classification and generated indexes belongs to t-20261018-r27-public-surfaces.
- Card may move to review with this evidence; no further lane work pending unless review requests changes.
