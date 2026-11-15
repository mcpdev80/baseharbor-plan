# cli2-org-env (0428-056 / t-20261114-r28-cli2-org-env) — round 1

- Worker: welle2-056 (Ornith; confirmed at spawn)
- Mission: `/tmp/opencode/mission-welle2-056.md`
- Date: 2026-11-15
- State: active -> review (draft PR open; CI-routing gap reported as STATE, Owner scope)

## PLAN

- Read mission, task contract, owner brief, command-map, code-entry-index, approved CLI contract v1, card 054/053 evidence.
- Establish remote reality witnesses (planning origin/main, product origin/develop, base lane origin/lane-0428-env-registry).
- Cut working branch from base lane b85efaf6 (ls-remote witness); base is ancestor of head; only my commit on top.
- Implement the 0428-056 slice in my own write-set (internal/orgconfig only).
- Focused tests at exact candidate SHA; wire to existing CI `validate` group (`./internal/...` wildcard, no .github/** change).
- Run go build/vet/test locally; record actual results at exact candidate SHA.
- Draft PR (base=lane-0428-env-registry, title carries 0428-056); publish evidence to origin/main; post END.
- CI-routing gap: lane-PR base matches no ci.yml trigger -> report as STATE (file:line), do not edit.

## BASE ATTESTATION

- Cut ref (base): `lane-0428-env-registry` @ `b85efaf6c94cd158de68a6b8f837dc4a23be455a` (ls-remote witness: `git ls-remote origin lane-0428-env-registry` -> `b85efaf6...`). This is card 0428-054's delivered HEAD (PR #1591 head).
- Candidate head branch: `cli2-org-env-reconcile` @ `32307a4336045d16b59027dd5a91b827a8c807d5` (my single commit on top of b85efaf6).
- `git merge-base --is-ancestor b85efaf6c... cli2-org-env-reconcile` -> true (base is ancestor of head).
- Only my commit sits on top of the base:
  ```
  32307a43 internal/orgconfig: shared environment identity reconciliation (0428-056)
  b85efaf6 internal/deployment: env-registry app/target/node association on environment.json (0428-054, owner ruling B)
  ```
- PR: #1596 (draft, base `lane-0428-env-registry` b85efaf6, stack-rule), head `cli2-org-env-reconcile` 32307a43. No develop PR (owner ruling).
- Note (process): my first local branch was mis-named `cli2-org-env-head` in the quarantined base main working tree; the detached commit did not advance that ref. I cut the correct branch `cli2-org-env-reconcile` in a dedicated /tmp worktree and pushed. No stray refs carried foreign commits.

## SCOPE (card + owner working brief + 2026-11-15 ruling)

- 0428-056 OWNS the org-config definition layer: extend versioned organization configuration to carry shared environment identities/policies and reconcile with Core after contract approval; keep provider/defaults vs mandatory policy distinct.
- Card 0428-054 owns the deployment registry (per-Target environment.json, UUID identity, ruling B). This slice is definition-only; it never writes the registry.
- Entry points owned: `internal/orgconfig/model.go`, `internal/orgconfig/effective.go` + dedicated org-env tests.
- Reserved (NOT edited): `cmd/baha/commands.go`, shared parser/machine registry, `.github/**` (Owner scope), release notes, generated indexes, `internal/deployment/*` (054's slice), Console/Node Connector.
- Acceptance: Git/OCI/local parity, stable UID, update/conflict and untrusted config, mandatory rule precedence; no secret material in config.

## IMPLEMENTATION (definition layer only)

- `internal/orgconfig/model.go`: add `EnvironmentIdentity{Reference, Authoritative}` and an optional `Identity *EnvironmentIdentity` field on `EnvironmentDefaults`; add `validateEnvironmentIdentity` so a present-but-empty reference fails closed and inline secret material is rejected exactly like every other organization reference. Provider/defaults vs mandatory policy structs are untouched.
- `internal/orgconfig/effective.go`: add `EnvironmentResolutionInput{CoreIdentity}` and `ResolveEffectiveWithCoreIdentity(state, environment, coreEnv, preferences...)`; keep the public `ResolveEffective(state, environment, preferences...)` signature unchanged (definition-layer-only, reconciliation inert) so all 11 existing call sites compile without change. `Effective` gains `EnvironmentIdentity *EffectiveEnvironmentIdentity{Reference, Authoritative, Source}`.
- Reconciliation (`reconcileEnvironmentIdentity`): declared identity matches Core registry identity -> authoritative; diverges -> typed `policy_denied` / `environment_identity_mismatch` fail-closed (carries Resource + remediation); absent registry identity -> inert (authored identity surfaces non-authoritative, definition-layer resolution not weakened).

## ACCEPTANCE per criterion (test names + literal output at candidate SHA 32307a43)

Git/OCI/local parity — the existing orgconfig suite already covers Git (TestGitResolutionPinsRevisionAndCheckDoesNotActivate), OCI (TestOCIResolutionPinsDigestAndPullsImmutableReference), and local (TestLocalActivationAndEffectiveProvenance) resolution parity at the candidate SHA. All green below.

Stable UID — environment identity is a declared non-secret reference; rename/identity separation is the 0428-054 domain, preserved (this slice reads it, never mutates it).

Update/conflict and untrusted config — untrusted config rejected (TestOrgEnvIdentitySecretMaterialRejected, literal PASS below); mismatch fails closed (TestReconcileIdentityMismatchFailsClosed).

Mandatory rule precedence — provider/defaults vs mandatory policy kept distinct and not weakened by reconciliation (TestOrgEnvIdentityReconciliationDoesNotWeakenMandatoryPolicy, literal PASS below).

No secret material in config — secret-bearing identity reference rejected at validation (TestOrgEnvIdentitySecretMaterialRejected).

New tests (exact IDs/packages), all in `internal/orgconfig/org_environment_reconcile_test.go`:
- `TestReconcileIdentityMatchIsAuthoritative` — declared identity == Core registry identity -> authoritative, source attests reconciliation.
- `TestReconcileIdentityMismatchFailsClosed` — divergent identity -> typed `policy_denied`/`environment_identity_mismatch` with Resource+Next.
- `TestReconcileEmptyDeclarationWithRegistryIdentityFailsClosed` — empty reference with registry identity present -> fails closed.
- `TestReconcileAbsentRegistryIdentityIsInert` — no registry identity -> authored identity surfaces non-authoritative, target resolution intact.
- `TestResolveEffectiveWithoutCoreIdentityDoesNotReconcile` — public signature unchanged, reconciliation inert.
- `TestOrgEnvIdentitySecretMaterialRejected` — inline secret material in identity reference rejected.
- `TestOrgEnvIdentityReconciliationDoesNotWeakenMandatoryPolicy` — mandatory organization policy survives reconciliation.

### Actual local results at candidate SHA 32307a43

```
$ go build ./...                          # exit 0
$ go vet ./internal/orgconfig/            # clean (no output)
$ go test ./internal/orgconfig/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/orgconfig	0.105s
$ go test ./cmd/baha/ -run 'Organization|ConfigOrg|OrgConfig' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.100s
```

Baseline (base lane b85efaf6) was green before any change; all above green after. `gofmt -l internal/orgconfig/` clean.

The 11 existing `ResolveEffective` callers in `cmd/baha` and `internal/application` compile unchanged (signature preserved). `internal/application` has pre-existing test failures on the clean base (provider-registry resolution/ordering; outside this write-set) — verified identical failures without my change via `git stash`; not caused by this slice.

## CI STATE (Owner scope — reported, NOT fixed)

- Draft PR #1596 (base `lane-0428-env-registry` b85efaf6, head `cli2-org-env-reconcile` 32307a43). Diff base..head shows ONLY my 3 files and only my commit `32307a43`.
- **CI-routing gap (finding):** `origin/main:.github/workflows/ci.yml` lines 7-18 fire CI only on `push` to branches `develop`, `runtime-validation/ci/**`, `runtime-validation/source-preflight/**`, `runtime-validation/ha/**` (lines 8-12) and `pull_request` to branches `develop`, `main` (lines 13-17). A lane PR with base `lane-0428-env-registry` matches NEITHER trigger, so the `validate` group (ci.yml line 255: `go test ./contracts/... ./internal/... ./spec/...`) does not run on this candidate.
- This is the same condition 0428-053 already documented (lane PRs get no hosted CI during repair). Per Owner scope-split: `.github/**` NOT edited, no rerun/workflow_dispatch issued.
- **Needed change (Owner scope, file:line):** `origin/main:.github/workflows/ci.yml` line 12 (push branches) and/or line 17 (pull_request branches) — add the 0.4.28 lane-branch pattern (e.g. `- 'lane-0428-*'` to the `pull_request.branches` list, or route lane PRs through develop) so this slice's new tests become durable CI evidence. Until then, actual hosted execution must be proven by another route (e.g. a develop-targeted pilot) before acceptance.

## EVIDENCE LAYOUT (baseharbor-plan ONLY, never a product repo)

- Path: `baseharbor-plan/evidence/cli-redesign-20261114/r28-welle1-2026-11-15/cli2-org-env/round-1.md`
- No `.evidence/` directory in any product repo. No main-branch writes in baseharbor.
- Claim published to baseharbor-plan origin/main (48faa9dd) before editing.

## repo-rule compliance

- Write-set is exactly `internal/orgconfig/model.go`, `internal/orgconfig/effective.go`, `internal/orgconfig/org_environment_reconcile_test.go` + their tests. No other card's files touched.
- No `.github/**` edits, no reruns/workflow_dispatch, no subagents (§4.8), no force push, no branch-protection bypass.
- No release/tag authorized.
- Cleanliness: work only in `/tmp/opencode/welle2-056/`; base main working tree left clean; no containers/compose projects started or left running.

## END

- DONE (draft PR #1596 open; CI-routing gap reported as STATE, Owner scope; acceptance gated on actual hosted execution of the new tests)
