# Bug-Hunt Slice H-V26 — Candidate build / --confirm-candidate consent / runtime-trust fail-open (round 1)

Lane: `w58-0428-267-huntcandgate`
Type: read-only Befundung. REINE BEFUNDUNG — no product change, no commit/push/PR, no hosted run, no local test, no subagent.
Develop anchor: `3ebfb90d` (v0.4.28). Read from `origin/develop` via a detached mirror worktree.
Scope note: CI/CI-adjacent findings (workflow files under `.github/**`, the trusted planner that selects gates) are Owner scope. Per mission they are reported as STATE with file:line and NOT fixed here.

## PLAN

- Set up verified read-only mirror at exactly develop anchor 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd; confirm real GitHub remote.
- Area A: trace `baha-ci-operator-testonly` production end to end — which Job/Step builds it, into which artifact path, and whether every consumer path has it.
- Area B: trace `--confirm-candidate` (record-deployment-before-mutation) — exact develop conditions that require consent, who sets the override legitimately, which runtime-gate calls set vs omit it.
- Area C: trace operator-trust / fail-open in the runtime-actor path (`deploymentApplied`, runtime-actor allow/verify, trusted-local) for real False-Green/False-Red gaps — NOT the already-carded 0428-189..194 consent-flaeche.
- Dedup vs. carded 0428-189..194 and H-V25 F1-F9; mark "wie 0428-1xx, other spot".
- Write this dossier with per-finding file:line, reproducible path, expected vs actual, severity, ref card.
- Persist to baseharbor-plan origin/main, verify with ls-tree, post END.

## Remote witness (baseharbor product repo, per mission)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v`
origin  https://github.com/mcpdev80/baseharbor.git (fetch)
origin  https://github.com/mcpdev80/baseharbor.git (push)
lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin  https://github.com/mcpdev80/baseharbor.git (push)

Develop truth: `git -C baseharbor ls-remote ssh://git@github.com/mcpdev80/baseharbor.git refs/heads/develop`
3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd  refs/heads/develop  (matches anchor)

Mirror worktree used: `/home/marcel/dev/baseharbor-ecosystem/workers/w58-0428-267-huntcandgate-wt` (detached at 3ebfb90da), `git merge-base --is-ancestor origin/develop HEAD` passes; `git diff origin/develop..HEAD --name-only` empty (worktree == develop head, read-only, no commits).

## Method

Pure static code reading (`git show`/`grep`/`sed`/`python3` JSON) plus the pinned demo checkout at `c23bd9ac58919302ffad3a43f43afb1a34bfbc96` (read-only clone, no build). No build, no local test, no VM, no hosted run (this is a read-only hunt, no PR). No containers/volumes created by this lane.

## Findings

### F1 — Release workflow never builds the test-only candidate binary, but release runtime gates require it (STATE, Owner scope)

- File:line: `.github/workflows/pre-release.yml` `release_candidate` job, "Build exact candidate binary" step builds and uploads only `baha` (`pre-release-source-candidate`, lines ~491-501); `.github/workflows/pre-release.yml` never references `baha-ci-operator-testonly` (0 occurrences across the file). The downstream `runtime_candidate` job (lines ~575-636) re-downloads `pre-release-source-candidate`, builds the runtime image, and uploads `pre-release-runtime-candidate` — which therefore contains only `baha`, never the test-only binary.
- Consumer: `.github/workflows/pre-release-runtime-suite.yml` "Run runtime gate" step, `if: ... class == 'runtime'`, run block lines 314-319:
  ```
  testonly="$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly"
  test -s "$testonly"        # line 316, under `set -euo pipefail`
  ```
  Every release runtime gate dispatched with `candidate_artifact: pre-release-runtime-candidate` (guided, lifecycle, policy, connectivity, full-destroy, data-capabilities, observability, identity, security, reconciliation, failure, backup-restore — 12 runtime-class gates in `tests/gate-resources.json`) hits line 316.
- Trigger: a release run of `pre-release.yml` -> `runtime_candidate` -> any `release_light_gates_{docker,podman}` / `release_heavy_gates_*` with a runtime-class gate.
- Expected: the exact candidate binary consumed by the gate (`$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly`) exists and matches `CANDIDATE_SHA` (the same `version | grep $GITHUB_SHA` integrity the CI `pr_candidate` job enforces at `ci.yml` lines 1145-1147).
- Actual: the release `runtime_candidate` artifact ships only `baha`; `test -s "$testonly"` at pre-release-runtime-suite.yml:316 fails the job under `set -e` for every runtime-class gate when `reuse_from` is empty (no reused evidence). Only a prior successful run providing `reuse_from` (and its evidence artifact, which carries the test-only binary) would skip the build.
- Note the contrast: the CI path builds it correctly once per PR head in `pr_candidate` (ci.yml lines 1141-1153, "Prepare candidate binary and image independently of Docs", `CGO_ENABLED=0 go build ... -tags=baseharbor_ci_operator_testonly -o "$out/baha-ci-operator-testonly"`). So the test-only binary is produced for PR runtime gates but NOT for release runtime gates.
- Severity: high for release (release runtime gates cannot complete on the current release workflow); Owner scope — fix is in `.github/**`, reported here as STATE.
- Ref card: none yet (Fund->Karte-pflicht at Coordinator). Duplicate marker: not 0428-189..194 (consent-flaeche) and not H-V25 F1-F9 (Perses observability); distinct gap in the release candidate artifact vs the CI candidate artifact.

### F2 — `--confirm-candidate` is only required for repository-owned applies, not for managed/other sources; and the fail-closed gate is a single choke point that every apply path must share (STATE, no fix)

- File:line: `cmd/baha/deployment_record.go` `recordDeploymentBeforeMutation`, the candidate choke point at lines 520-521 (`if record.Source.Kind == "repository" && state == "applying"`) and the finalize/fail-closed leaf at lines 528-573. `finalizeCandidateConsent` (cmd/baha/app_candidate_consent.go:180-206) returns nil consent for an empty confirm -> `missingCandidateConsentError` (app_candidate_consent.go:152-160) fails closed before any state write.
- Under which develop conditions consent is required: a deployment record whose `Source.Kind == "repository"` AND the mutation is an applying-state (`state == "applying"`). The `configured` pending state used by init/restore planning (deployment_record.go:357 `recordPendingDeployment(... "configured" "")`) is NOT a candidate submission and carries no consent requirement.
- Who sets the override legitimately (all routed through the same context leaf `candidateConsentOverride`, app_candidate_consent.go:63-67):
  - Local CLI `baha app apply` / `baha up` parse `--confirm-candidate <digest>` into `runtimeUpOptions.CandidateConsent` (cmd/baha/runtime.go:137-139) and push it via `withRuntimeUpCandidateConsent` (app_candidate_consent.go:50-52); remote management re-passes it as a CLI arg (cmd/baha/app_input_resolver.go:572-573).
  - MCP `apply` sets it via `withCandidateConsentDigest(ctx, input.ConfirmCandidate)` (cmd/baha/mcp_tools.go:486).
  - The digest is never trusted raw: `finalizeCandidateConsent` recomputes the canonical content-hash of the exact submission and compares in constant time (app_candidate_consent.go:190-197); a mismatch -> `errCandidateConsentDigestMismatch` -> `staleCandidateConsentError` (deployment_record.go:369-376).
- Which runtime-gate calls set vs omit it (without touching consent validation): `recordDeploymentBeforeMutation` is invoked with the context value at cmd/baha/app_apply.go:202 (local apply), cmd/baha/app_remote_lifecycle.go:163 (remote apply, after `promptConfirmCandidateSubmission` at :162), cmd/baha/deployment_record.go:359 (`recordPendingDeployment`, configured state -> ""). The tagged CI test-only operator (cmd/baha/ci_integration_operator_enabled.go) exercises these under `DEMO_ATOMIC_GATE=1` but never supplies a confirm digest, so it must drive commands that are NOT repository-owned candidate submissions, or the apply fails closed.
- Expected: every repository-owned apply enforces the same fail-closed consent gate.
- Actual: the gate is a single choke point and IS enforced for repository source; managed-app create uses a local source path (`record.Source.Kind` != repository) and is correctly excluded (by design). No consent-validation change is needed.
- Severity: info — the consent mechanism is internally consistent; documented here so the Coordinator can judge whether the repository-vs-managed carve-out should be a card.
- Ref card: none. Duplicate marker: NOT the already-carded 0428-189..194 consent-flaeche — this F2 describes the repository-source carve-out and the context-routing, a different spot.

### F3 — `ManagedEnvironment()` hard-codes the managed branch to always-true, so the trusted-local fail-open seam in `authorizeMachineOperation` is unreachable via production callers (STATE, medium)

- File:line: `internal/operatorauth/config.go:89-91` `ManagedEnvironment` -> `ManagedEnvironmentWithPolicy(environment, false)` -> `!trustedLocal` == `true` for every environment name. The policy-aware form `ManagedEnvironmentWithPolicy` (config.go:108-110) takes an explicit `trustedLocal bool`; no production caller passes `true`.
- The fail-open decision lives at `internal/operatorauth/authorization.go:279-282`:
  ```
  if !ManagedEnvironment(decision.Context.Environment) && !ok {
      decision.Allowed = true
      decision.Actor = ... Mode: "trusted-local", Subject: "trusted-local"
  }
  ```
  With `ManagedEnvironment()` always true, `!ManagedEnvironment(...)` is always false, so this trusted-local branch is dead for every caller using the unversioned function.
- `verifiedLocalWorkloadAuthority` (cmd/baha/local_workload_authority.go:49-157) is the real host-local trust seam; it returns the local-runtime grant (the `local-runtime` fail-open at authorization.go:274-278, reached via `AuthorizeMachineOperationWithLocalGrant`) rather than the trusted-local path, and it is the only place a no-OIDC local operator is actually authorized. The `trusted-local` mode in `authorizeMachineOperation` (authorization.go:279) appears to be a legacy/defensive branch that the current config can no longer reach.
- Trigger: any machine operation on a host-local Target in an unmanaged environment where `trustedLocal` should be true but no local-runtime grant exists.
- Expected: `trusted-local` is the documented fallback for trusted host-local operators in unmanaged environments (config.go comment lines 93-100).
- Actual: the only managed/trusted decision is driven by the explicit `trustedLocal` policy parameter, which production never sets true; `ManagedEnvironment()` therefore reports "managed" for dev/development/prod/arbitrary and the trusted-local fail-open branch is never taken. If the intent was a working trusted-local path for unmanaged environments, it is currently unreachable.
- Severity: medium (an unreachable fail-open seam; either a latent dead branch or a missing policy wiring — both worth a card).
- Ref card: none. Duplicate marker: 0428-189..194 is the consent-flaeche; this is the managed/trusted environment policy wiring, a different spot.

### F4 — `verifyRuntimeBrokerBuildIdentity` deliberately ignores commit SHAs; runtime image provenance is version-only (STATE, low/medium)

- File:line: `cmd/baha/app_broker.go:652-672` `verifyRuntimeBrokerBuildIdentity(actualVersion, actualCommit string)`. The function fails closed on empty version (658-660), enforces version match except the `dev`/`edge` development pair (661-666), then drops commit SHA entirely: `_ = expectedCommit` / `_ = actualCommit` (668-669) with the comment "Commit SHAs are build provenance, not a runtime compatibility contract."
- Trigger: readiness probe at cmd/baha/app_broker.go:641 (`verifyRuntimeBrokerBuildIdentity(ready.Version, ready.Commit)`) during `verifyRuntimeBrokerRunning` (app_broker.go:192) in the apply/verify lifecycle.
- Expected: the applied runtime image is the exact candidate image (the CI path pins `BASEHARBOR_SOURCE_REF=$CANDIDATE_SHA` and builds the image from that SHA), so a version match but different commit should ideally be surfaced.
- Actual: only the version contract is enforced; a runtime image at a different commit (same semver) is accepted. Version-only identity cannot catch an applied runtime that drifted from the exact candidate commit.
- Severity: low/medium (documented by design; a provenance-strength question, not a crash or false-green in the normal path).
- Ref card: none.

### F5 — CI runtime-gate selection does not escalate to a native runtime gate for changes to the trusted-local / runtime-authority seam (STATE, Owner scope)

- File:line: `scripts/pr-gate-plan.py` lines 1643-1646: a PR touching `internal/operatorauth/local_runtime.go` (listed in `OPERATORAUTH_POLICY_FILES`, lines 85-93) resolves to `area = 'operatorauth-explicit-policy'` and calls `require(AUTHORITY_PACKAGE_CHECKS + CODE_CHECKS)` only — i.e. package-level Go tests plus `go test ./internal/application/... ./contracts/...`. No `atomic/{docker,podman}/<gate>` is added, so `pr-selected-runtime-matrix.py` reports `runtime_required=false` and the `pr_candidate` job (which builds the test-only binary) is never dispatched.
- Trigger: a PR that modifies the fail-open runtime-authority code (`internal/operatorauth/local_runtime.go`, `authorization.go`).
- Expected: a change to the local-runtime/trusted-local trust seam qualifies via a native runtime gate (the exact seam F3/F4 operate in), so a fail-open regression is caught by real candidate acceptance, not only unit tests.
- Actual: the planner routes the seam to pure package checks; a fail-open regression in `verifiedLocalWorkloadAuthority` (cmd/baha/local_workload_authority.go:49-157, the engine-owner + grant boundary) would pass CI with unit coverage alone and no native runtime acceptance.
- Severity: medium (trust seam qualified only by unit tests; native acceptance absent).
- Note: the executable mapping lives in `scripts/pr-gate-plan.py` (Owner-adjacent: a `scripts/` change binds only later PRs per CI policy, and any workflow/trigger change is Owner scope). Reported here as STATE with file:line; not fixed.
- Ref card: none.

## Fundbilanz

- Echte Dekte (product defect): 0 requiring a product fix inside this card's write-set.
- STATE / Owner-scope (reported, not fixed): F1 (release workflow never builds the test-only candidate binary; release runtime gates fail `test -s`), F3 (managed/trusted policy wiring makes the trusted-local fail-open seam unreachable), F4 (runtime image provenance version-only), F5 (runtime-gate selection does not escalate the runtime-authority seam to a native gate).
- Info / by-design, for Coordinator card judgment: F2 (--confirm-candidate repository-source carve-out + context routing).
- Dedup: none of F1-F5 are the carded 0428-189..194 consent-flaeche nor H-V25 F1-F9 (Perses observability). F2/F3 explicitly mark "other spot".
- Total findings: 5.

## cleanliness

- Read-only hunt. No `docker`/`podman` container, network, volume, or state directory created by this lane.
- `docker ps -a` before: empty (no rows). `podman ps -a` before: one ambient `baseharbor-pre-release-registry` container (registry:2.8.3, Exited) — NOT this lane's, left untouched (ambient-core of other lanes).
- No worktree commits; mirror worktree `/home/marcel/dev/baseharbor-ecosystem/workers/w58-0428-267-huntcandgate-wt` has no commits (read-only).
- No scratch/cache written under the ecosystem root beyond the read-only mirror worktree and the pinned demo read-only clone under `/tmp/demo-probe`.

## END w58-0428-267-huntcandgate DONE

- develop HEAD (witness): `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd` (git ls-remote origin refs/heads/develop)
- 5 findings; read-only desk audit; NO edit/commit/push/subagent/hosted run
- F1 (STATE/high, Owner): `.github/workflows/pre-release.yml` release_candidate never builds `baha-ci-operator-testonly` (0 hits in file); `pre-release-runtime-suite.yml` runtime gate does `test -s "$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly"` under `set -e` (line 316) -> every release runtime-class gate (12 in gate-resources.json) fails when reuse_from empty. CI path builds it in pr_candidate (ci.yml:1141-1153); release path does not.
- F2 (info, by-design): `--confirm-candidate` required only for `record.Source.Kind == "repository" && state == "applying"` (deployment_record.go:520-521, fail-closed at :528-573 via finalizeCandidateConsent app_candidate_consent.go:180-206); routed through candidateConsentOverride from CLI/up/remote/MCP; remote apply at app_remote_lifecycle.go:163 after promptConfirmCandidateSubmission at :162; managed-app create uses local source -> excluded.
- F3 (STATE/medium): `ManagedEnvironment()` config.go:89-91 hard-codes managed=true for every env name; trusted-local fail-open at internal/operatorauth/authorization.go:279-282 unreachable via production callers; real seam is verifiedLocalWorkloadAuthority (cmd/baha/local_workload_authority.go:49) -> local-runtime grant.
- F4 (STATE/low-medium): verifyRuntimeBrokerBuildIdentity app_broker.go:652-672 enforces version only, drops commit SHA (`_ = expectedCommit` at :668); runtime provenance version-only.
- F5 (STATE/medium, Owner): scripts/pr-gate-plan.py:1643-1646 routes operatorauth local_runtime.go to AUTHORITY_PACKAGE_CHECKS + CODE_CHECKS only, no native runtime gate -> runtime-authority seam not qualified by candidate acceptance.
- 0 product fixes; all findings STATE/Owner-scope or by-design; dedup vs 0428-189..194 and H-V25 F1-F9 noted per finding
- cleanliness: no containers/volumes/state created; ambient baseharbor-pre-release-registry podman container left untouched; no worktree commits
