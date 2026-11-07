# Evidence: 0427-onboarding-wizard (t-20261018-r27-onboarding-wizard), Round 1

Lane: 0427-onboarding-wizard (flash worker). Card: r27-onboarding-wizard.
Repository: mcpdev80/baseharbor. Branch: lane/0427-onboarding-wizard.
PR: https://github.com/mcpdev80/baseharbor/pull/1435 (base develop).

## PLAN

- Read task contract, card body, baseharbor AGENTS.md and DEVELOPMENT_GUIDELINES.md.
- Confirm claim (card already active, owner lane-0427-onboarding-wizard via kanban commit 0960b679).
- Create isolated worktree, branch from origin/develop; keep base drift-free through the final push.
- Explore onboarding-relevant code and accepted predecessors (management connection, profile-codec, workstation enrollment, client commands).
- Write red-first tests for the guided flow in CI-discovered packages (cmd/baha, internal/onboardingwizard).
- Implement internal/onboardingwizard plus cmd/baha production bindings, disjoint from access-wizard/node-cli/116/118 write-sets.
- Run targeted local checks plus repository audits.
- Commit one coherent candidate, push, open exactly one PR against develop.
- Watch hosted CI on the final SHA to a terminal state and record it here.
- Publish this evidence file to baseharbor-plan origin/main and END the lane.

## Base attestation

- Cut base: origin/develop 812c99c88.
- Drift: develop moved to 06e4b1eaa (owner merged PR #1431); merged forward into the lane as a fast-forward.
- Ancestor witness: `git merge-base --is-ancestor origin/develop HEAD` returned rc0 (printed ANCESTOR_RC0) at 06e4b1eaa; re-verified immediately before the final push.
- Candidate commits on top of develop: `git log --oneline origin/develop..HEAD` lists exactly one commit: 4d430eeaa "feat(onboarding): guided onboarding flow with minimal decisions (r27-043)".
- Push witness (ls-remote): `4d430eeaa862b1ab66ca20372ca8ba2e3bd5b2c0 refs/heads/lane/0427-onboarding-wizard`.

## Write-set

Added files only (all inside the bounded onboarding write-set):
- cmd/baha/onboarding.go
- cmd/baha/connection_profile_codec.go
- cmd/baha/onboarding_test.go
- internal/onboardingwizard/onboardingwizard.go
- internal/onboardingwizard/wizard_test.go

Forbidden paths untouched: cmd/baha/commands.go, .github/**, accesswizard/**, node.go/node_cli_behaviors, app_remote_lifecycle.go/remote_pureclient_*, app_maintenance_*, broker/source_oci, the runtime integration fixtures.

## Design

- Four distinct intents: bootstrap, attach, import (device bundle XOR non-secret team profile), remove (local-only; never revokes remotely; core-777 separation of onboarding and bootstrap).
- The wizard is a presentation controller with zero mutation: discovery injects facts (installation presence/identity, declared Targets, existing application registration, valid reusable connection) and the wizard is forbidden to ask for any of them. A single explicit `--target` skips the questionnaire and executes the verified effect path (verify-then-persist); a repeat run with a valid stored connection fact continues silently with zero questions.
- Effects commit exactly once after review; cancel/EOF/review-deny never mutate; conflicts (existing-app claim without registration, profile duplicate/foreign binding, unverified connection) fail closed.
- Reuses accepted seams only: coreinstallation.Load/ResolverForTargetSelection (management connection), the profile-codec store (contracts/managementaccess/v1, conflict-reject + expected binding), the workstation-enrollment one-use exchange, application.HasRepositoryApplication for registration discovery.

## Findings (reported to coordinator)

- Command registration: `baha onboard` is NOT added to rootCommand() because cmd/baha/commands.go belongs to t-20261018-r27-public-surfaces. The factory + classification/index integration is the shared gap both this PR and access-wizard #1430 leave to public-surfaces. Fence tests (TestMachineCoverageCIRealTree, TestHumanCommandIndex, TestMachineDocumentation) pass on this head because no unclassified command is introduced.
- No file collision with access-wizard #1430 (its write-set: access_wizard_command.go + internal/accesswizard + commands.go edit; mine touches none of these).

## Local verification

- `go test ./internal/onboardingwizard ./cmd/baha -run TestOnboarding -count=1`: PASS (both packages).
- Full `go test ./cmd/baha -count=1`: failure set identical to the base (stash-compare on the same machine): 13 pre-existing environment-dependent failures (real-isolated-Core / p427-podman-boot deployment-state fixtures); no new failure attributable to this change.
- `go vet ./...`: clean. `gofmt -l`: clean. `go build -o /tmp/baha-0427 ./cmd/baha`: OK.
- `bash scripts/source-readability-audit.sh`: all PASS.
- No VM compose projects were started by this lane (nothing to tear down).

## Hosted CI

- PR: #1435, head SHA 4d430eeaa862b1ab66ca20372ca8ba2e3bd5b2c0.
- (run ids and terminal statuses appended below by this lane after watching to terminal.)
