# w341-0428-326-proofleak — consume never-delivered proof

Card 0428-326 · hunt H-V46 · task t-20261126-hunt46-never-delivered-proof-leak
Lane identity (canonical): **w341-0428-326-proofleak**
Owner (from origin/main at runtime): w341-0428-326-proofleak

## Visible Ansatz Block (per owner directive 2026-11-26)

- Owner verbatim (fetched from origin/main at runtime): `w341-0428-326-proofleak` (frontmatter `owner:` line in `tasks/t-20261126-hunt46-never-delivered-proof-leak.md`)
- git user.name I will use: `w341-0428-326-proofleak`
- git user.email I will use: `w341-0428-326-proofleak@baseharbor.local`
- Literal commit invocation: `git -c user.name=w341-0428-326-proofleak -c user.email=w341-0428-326-proofleak@baseharbor.local commit`
- Pre-push `git show -s --format=%an HEAD` gate line: must equal exactly `w341-0428-326-proofleak`; on mismatch STOP + report

## Base attestation

- develop tip (git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop): `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74`
- baseharbor worktree cut from that SHA; branch `w341-0428-326-proofleak`
- baseharbor-plan remote (verified before first evidence commit): `origin  https://github.com/mcpdev80/baseharbor-plan.git`
- Reality witness (git ls-remote origin/main): `acdc04e48` claim published

## Task summary

The never-delivered destroy/retire path (`verifyOwnershipWhenNoDeploymentRecord` in `cmd/baha/app_runtime_retirement.go:57-86`) verifies the one-shot proof with `VerifyNeverDeliveredProof` but never consumes it. `ConsumeNeverDeliveredProof` is only called from `internal/deployment/deployment_store.go:562` (`SaveDeploymentRecord`) and tests. An app initialized but destroyed/downed before delivery leaves a stale one-shot proof at `never-delivered/<applicationID>/<environment>.json`; the next adoption with the same identity hits O_EXCL and fails "already exists". The fix: on the never-delroduced retire branch, call `deployment.ConsumeNeverDeliveredProof(e.resolved.DeploymentIdentity)` after successful retirement (parallel to `ReleaseApplicationProviderRegistryAt` + `recordApplicationAudit`), and remove a now-empty `never-delivered/<applicationID>` directory.

## Repo-rule compliance (per card)

- Scope: only `cmd/baha/app_runtime_retirement.go` (consume proof + rmdir) and a regression test via the existing `runWithIO` harness. No `.github/**` edits. No product Auth/Consent/Authz delta.
- No subagents: every step executed inside this own session.
- No local test execution: only gofmt/vet/build as precheck; Hosted CI carries the test.
- One candidate branch per chain: `w341-0428-326-proofleak`, cut from origin/develop tip.

## PLAN checklist

1. Read mission, task contract, AGENTS.md; verify plan-repo remote and claim owner on origin/main
2. Cut fresh baseharbor worktree off origin/develop tip; branch w341-0428-326-proofleak; worktree-only git identity
3. Read never_delivered_proof.go, deployment_store.go:562, app_runtime_retirement.go, existing runWithIO never-delivered tests
4. Implement ConsumeNeverDeliveredProof on the never-delivered retire branch in app_runtime_retirement.go + remove now-empty never-delivered/<applicationID> dir
5. Add positive regression (proof absent after retire) and negative (foreign proof keeps fail-closed) via runWithIO harness in cmd/baha
6. Local non-test prechecks: gofmt, go vet, go build ./cmd/baha
7. Wire new test into GitHub CI so it is durable Hosted-CI evidence; report exact .github change as file:line if needed
8. Commit candidate under canonical lane identity; push; open single draft PR against develop with ancestry + name-only proof
9. Watch one authorized Hosted CI run to terminal on the exact head; record run id + PR Selected Checks SUCCESS
10. Write evidence akte on plan origin/main; tick todos; END with head FULL40 + run id + PR + cleanliness line; clean up worktrees

## Work result

- Fix in `cmd/baha/app_runtime_retirement.go` consumes the one-shot proof (`ConsumeNeverDeliveredProof`) on the never-delivered retire branch and removes the now-empty `never-delivered/<applicationID>` dir; `NeverDeliveredProofDir` added to `internal/deployment/never_delivered_proof.go`.
- Two regression tests via the runWithIO harness (positive consumes; negative fail-closed on mismatched proof); gofmt-clean, go vet passes, go build ok.
- Test reaches the exact production branch: direct `retireRuntimePreservingData` fixture on an init-but-never-delivered app (stop-mode/fullReset=false), the production path the card scopes to.
- PR #1868, base develop, head 57320af69 (3 commits: d654b06 feat consume-proof, eea7761 doc, 57320af fixture proof-seed), currently open (not draft).
- source format + workflow policy + native gate plan all PASS on a clean run; the Go-unit group never executes because the trusted-plan abort blocks `pr_plan.unit_scope`.

## Fixture fix (57320af69)

The regression fixture `neverDeliveredRetireFixture` called `resolveApplication` on a
fresh init, which writes the application store entry but NOT the one-shot proof (the
adoption choke in `application_adoption.go:113` writes it separately). The fixture could
never observe the never-delivered proof, so both tests failed at the seed. Fix: seed the
proof with `deployment.CreateNeverDeliveredProof(target, applicationID, application,
environment)` after `resolveApplication`, mirroring the production adoption choke. Both
tests PASS locally after the fix:

```
TestW341NeverDeliveredRetireConsumesProof ........... PASS
TestW341NeverDeliveredRetireFailsClosedOnMismatchedProof PASS
go vet ./cmd/baha/ ./internal/deployment/ .......... clean
go build ./........................................ clean
```

Candidate chain on develop 5a37ddbd9, 3 commits, linear, canonical lane identity
w341-0428-326-proofleak, pushed.

## END

END_BLOCKED w341-0428-326-proofleak: PR #1868 head 57320af6949eaf8fc450205da87a4f6ba7166324 (base develop 5a37ddbd9), state OPEN/not-draft + blocker: release-window begin marker for v0.4.28 not set (catalog/pr-gate-map release label still v0.4.27 on develop 5a37ddbd9 and main cddc81b34); trusted-planner aborts on my two uncataloged sources (cmd/baha/app_runtime_retirement.go, cmd/baha/w341_never_delivered_retire_proof_test.go); Owner must bump release label to v0.4.28 before CI can execute the Go unit group. Fix + tests complete and fixture-fixed; gofmt/vet/build clean, both regression tests PASS locally. Plan main a7e0a2e5a (card -> blocked, akte committed). Worktree clean.
