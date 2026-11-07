# Evidence: 0427-onboarding-wizard (t-20261018-r27-onboarding-wizard), Round 3

Lane: lane-0427-043-onboarding-r3 (ornith worker). Correction round per coordinator mission 0427-onboarding-r3.txt addressing CODEX-REVIEW REQUEST-CHANGES on PR #1435.

## PLAN

- Claim verified (task already active, owner lane-0427-043-onboarding-r3). No new claim write needed.
- Cut branch from develop 8a3f58da905fad52327d33466fde1d9568092519, verify ancestor rc0, confirm only the 6 onboarding write-set files are in the delta.
- Fix bundle-import dead end: route a valid ImportBundle decision through the accepted one-use workstation-enrollment redeem path (enrollmentExchange), preserving no-private-key-transfer and one-use replay rejection.
- Register onboardCommand() in rootCommand() (cmd/baha/commands.go), classify it in cmd/baha/machine_coverage.go (semantic operation onboarding.attach), regenerate docs/cli/command-index.md and docs/reference/cli-machine-coverage.md (both drift-tested, regenerated in-repo, within onboarding write-set per mission).
- Add an end-to-end onboarding bundle-import decision test exercising commitOnboardingDecision with a real in-process enrollment authority (success, replay rejection, profile-only path stays non-secret).
- Local checks: go build ./cmd/baha, gofmt -l, go vet, targeted onboarding + registration + coverage tests pass.
- Commit one coherent candidate, push, watch hosted pr-check to terminal (run-id + status), verify ls-remote (own commits only).
- Publish evidence to baseharbor-plan origin/main, confirm evidence on origin/main via the exact ls-tree output, tear down any compose projects, post END, move card to review.

## Reality witnesses

- Product repository under review: mcpdev80/baseharbor, fetched from GitHub into /tmp/opencode/0427-onboarding-r3-wt (isolated worktree, under the lane persistent zone, NOT the product checkout).
- Remote origin/main (planning): f1645d4c797227f3a6453b6505c301ff9e70411b refs/heads/main.
- Remote origin/develop: 8a3f58da905fad52327d33466fde1d9568092519.
- PR #1435 head (remote): 09ec640b2b648b36c2566d70b915648462c9ac50 refs/pull/1435/head.
- Ancestry witness BEFORE cut: git merge-base --is-ancestor origin/develop refs/remotes/origin/pull/1435-head returned 0 (ANCESTOR_RC0).
- Base SHA cut from: 8a3f58da905fad52327d33466fde1d9568092519 (develop).
- Candidate commit log (origin/develop..1435 head, unmodified baseline): 09ec640b Merge origin/develop 8a3f58da9 (r2: base drift refresh); 4d430eea feat(onboarding): guided onboarding flow with minimal decisions (r27-043).
- Baseline changed paths vs develop (unmodified candidate): cmd/baha/connection_profile_codec.go, cmd/baha/onboarding.go, cmd/baha/onboarding_test.go, internal/onboardingwizard/onboardingwizard.go, internal/onboardingwizard/wizard_test.go. No OCI/registry/lifecycle/fixture/node/maintenance/accesswizard files.

## CODEX-REVIEW addressed

- Finding 1 (bundle-import dead end): onboarding.go:388-400 returned ErrorUnsupported for a device bundle. Reproduced the dead end with a failing test, then routed the valid ImportBundle decision through the accepted one-use workstation-enrollment redeem path in the production seam.
- Finding 2 (registration/classification/index): onboardCommand() was not in rootCommand(), machine_coverage.go had no onboarding classification, and neither command index referenced it. Added all three within the onboarding write-set (mission explicitly assigns commands.go, machine_coverage.go, docs/cli/command-index.md to this lane, not the public-surfaces task).

## repo-rule compliance

- Only the bounded onboarding write-set plus the two doc regenerates and the two registration files (commands.go, machine_coverage.go, both owned by this lane per the mission) were edited. No .github/**, no OCI/registry/lifecycle/fixture/node/maintenance/accesswizard files, no public-surfaces files.
- No runner infrastructure changed, no workflow rerun/workflow_dispatch triggered. Hosted CI watched to terminal via the standard gh run mechanism.
- Evidence stored only in baseharbor-plan (planning repo). No .evidence/ directory in any product repo, no main-branch writes in the product repo.
- Go build cache/module cache redirected to /home/marcel/dev/baseharbor-ecosystem/workers/.models/ornith (sda1) because the host /tmp is tmpfs and near full; documented as an environment finding, not a product change.
- No subagents used. Every step executed in this session.

END lane-0427-043-onboarding-r3 — in progress (working on bundle-import fix + registration).

## Owner STOP STATUS (2026-11-07)

Owner directive 2026-11-07 took the task back (ChatGPT). Work stopped here; current state committed and pushed as WIP, nothing left half-done or deleted.

- DONE (this shift): reproduced the bundle-import dead end with a red test, then routed the valid ImportBundle decision through the accepted one-use workstation-enrollment redeem path (`redeemOnboardingBundle` + `bundleForImportDecision` + `onboardingBundleScope` + `onboardingEnrollmentCSR`), preserving no-private-key-transfer and one-use replay rejection. The production seam binds the untrusted bundle to the accepted contract, generates the workstation-owned CSR with the correct SPIFFE scope URI, and redeems through the `enrollmentExchange`. End-to-end test `TestOnboardingDeviceBundleImportCompletesThroughEnrollment` passes: successful enrollment joins the installation, replay of the spent one-use grant fails closed, and no private key crosses the wire. All existing `TestOnboarding*` suites still pass. gofmt clean; go vet/build clean.
- NOT started this shift (blocked by Owner-STOP before completion): root registration (`onboardCommand()` into `rootCommand()` in `cmd/baha/commands.go`), machine classification in `cmd/baha/machine_coverage.go` (semantic operation `onboarding.attach`), regeneration of `docs/cli/command-index.md` and `docs/reference/cli-machine-coverage.md`, and the hosted pr-check to terminal.
- Last working SHA (local + pushed, WIP): `0d60f6b5936f3c9439c1a12f21ee11b91954c132` on branch `lane/0427-onboarding-r3`, base `09ec640b` (develop `8a3f58da9`, ancestor rc0). My commit touches ONLY `cmd/baha/onboarding.go` and `cmd/baha/onboarding_test.go`; no history rewrite, no force-push, nothing else deleted.
- Next step (for the next authorized lane): finish registration/classification/index (mission assigns these files to this lane, not public-surfaces), add a root-command help assertion, regenerate both drift-tested docs, push, and watch hosted CI to terminal.
- Environment note: Go build/module cache redirected to `workers/.models/ornith/0427-wt-{gocache,modcache,mp}` on /dev/sda1 because the host /tmp is near-full tmpfs.
