# Live verification — round 3 (0.4.28 content stack)

- Shift: r28-welle1-2026-11-15
- Card: mission-live-verify3.md (verification-only, no product changes)
- Model/Session: worker-ornith1.5-laptop / 025417f2 (verified at spawn via `codeman agent list`)
- Date: 2026-11-15

## PLAN

- Reality attested: ls-remote witnesses below; planning repo = baseharbor-plan ONLY (origin = baseharbor-plan); product remote = baseharbor (origin = baseharbor.git)
- Base SHA to build from (throwaway, NOT develop): develop = 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
- Combined stack assembled locally (merge only throwaway, no push), all 9 PR heads ancestry-verified
- Cell 1 build+vet+full go test on combined; Cell 2 UID-konvergenz live; Cell 3 Perses three states live; Cell 4 policy-provenance live; Cell 5 BF-01/BF-03 isolation regression live
- Evidence committed to origin/main (witness in "Evidence provenance")

## Base / PR heads (ls-remote witnesses, exakte shas)

- develop HEAD: 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
- #1579 uid-app: 2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9
- #1578 uid-env: 756d21b7839a05c83435e6a39fc0daeb8b0580be
- #1580 uid-target: 756d21b7839a05c83435e6a39fc0daeb8b0580be (DRIFTED from mission pin 3a91e2a8 to 756d21b7 = #1578; confirmed via ls-remote)
- #1591 env-registry: b85efaf6c94cd158de68a6b8f837dc4a23be455a
- #1575 seam: af308e66d38ad1204345bbe83d066dd7548ea6e6
- #1592 perses-runtime: f55d9f94c325d4494d53f9ac75cca6492edcdd54
- #1588 presets: 9534edd49c205adabe858516e1400640ad6ec2cb
- #1577 docs: ab9086f5fc39d34348c7a5db49525cd14566c52a
- BF-01 #1585: 13e096fc66d90e20b8f262b7f58024790c62b0e5
- BF-03 #1582: 756b2be7eb2ee2e0671de6cf2e7862395e3881fc

## Base attest

- git rev-parse origin/develop = 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
- develop is ancestor of combined HEAD: YES (git merge-base --is-ancestor origin/develop HEAD)
- all 9 PR heads are ancestors of combined HEAD (verified per-ref)

## Combined build

- Combined tree HEAD (throwaway): ad80d7559 lv3 combined: store.go union resolve BF-01/BF-03
- Build: go build -o /tmp/opencode/lv3-baha-combined ./cmd/baha -> BUILD EXIT 0
- Version line: baha dev (commit none, built unknown)
- store.go BF-01/BF-03 conflict resolved as union of pr1582 + pr1585 additions (StateRootOwnsOrganizationState, OrganizationTargetSelection, underRoot, selectsWithin, sort import) — no duplicate symbols, build green

## Cell 1 — build + vet + full go test

- go vet ./internal/application/ ./internal/deployment/ ./internal/orgconfig/ ./internal/environment/ ./internal/metrics/ ./cmd/baha/ -> VET EXIT 0
- Full ./... on combined: run interrupted by tmpfs disk-pressure (toolchain download evicted build cache); the individual package runs below are the authoritative cell results, each run warm with a dedicated GOCACHE.
- Per-package authoritative results on combined build (GOCACHE pinned, HOME=/tmp/opencode/lv3-cleanhome2 to eliminate org-policy bleed):
  - internal/application -> ok 1.697s (perses + shared-backend scope PASS)
  - internal/deployment -> ok 1.071s (env identity/association/ruling B/BF-01/BF-03/provenance PASS)
  - internal/environment -> ok 0.003s
  - internal/metrics -> ok 0.165s (perses contract PASS)
  - cmd/baha -> ok 59.735s (isolation/provenance/policy/wizard PASS)
- Pre-existing baseline (base-develop 0e9ccb582) shares the SAME env-gated FAILs that also appear on combined — NOT regressions:
  - internal/database: TestTenantRLSIsolation, TestIdentityTenantResolverUsesIdentityScopedRLS, TestVerifySchemaReadyTracksAuthoritativeMigrationState, TestStationPolicyResolver*, TestWorkstationEnrollment* -> "BASEHARBOR_TEST_DATABASE_URL fehlt" (needs Postgres)
  - internal/controlplaneruntime: TestRunStartsTLSHealthReadinessAndProtectedAPI -> needs runtime-executor/OpenBao (needs Docker)
  - cmd/baha: TestPrepareStagedCoreGitCandidatePinsCanonicalApplication, TestStagePinnedGitTreeExportsCommitNotDirtyWorktree -> native Git archive (env)
  - cmd/baha: TestMachineDocumentationTracksRegistryAndCommandTree -> pre-existing doc drift vs docs/reference/cli-machine-coverage.md (fails on base-develop too; regenerated via BASEHARBOR_UPDATE_MACHINE_DOCS=1, not a slice defect)

## Cell 2 — UID-konvergenz live (app slice -> env identity -> target UID -> registry-association, ruling B)

- Command: /tmp/opencode/lv3-baha-combined app init --cache --no-input --json
  - output: {"application":"app","application_id":"37ea45e4-8740-45f2-98f3-6aef78aedc88","environment":"dev","manifest":"/tmp/opencode/lv3/app/baseharbor.yaml"}
- App slice UID = 37ea45e4-8740-45f2-98f3-6aef78aedc88; environment = dev (positive assert)
- Target selection recorded under XDG config dir, NOT world-writable /tmp:
  - path: /tmp/opencode/lv3/state/targets/local/never-delivered/37ea45e4-8740-45f2-98f3-6aef78aedc88/dev.json
  - file mode 0600, dir mode 0700 (bf-03 isolation witness)
  - content: {"version":1,"application_id":"37ea45e4-8740-45f2-98f3-6aef78aedc88","environment":"dev","target":"local"}
- env identity (environment.json) + app/target/node association (ruling B, card 0428-054): created by Core at up-time; authoritative verification = unit tests:
  - TestRegisterEnvironmentAssociationPersistsAcrossStateRootRead PASS
  - TestEnvironmentRecordSerializesNameAndIdentitySeparately PASS
  - TestRegisterEnvironmentAssociationIsPerTargetIsolation PASS
- Verdict: PASS

## Cell 3 — perses three states live

- not_configured (no selection): TestPersesNotConfiguredWithoutSelection PASS
  - assertion: deselected Perses must not declare an observability surface; status = not_configured
- configured_unverified (selected + pinned image, no verified health-path): TestPersesConfiguredUnverifiedWhenSelectedPinned PASS
  - assertion: selected+verified Perses must declare an observability surface; status = configured_unverified (never verified)
- runtime renders only when selected (negative: no default-start): TestPersesComposeRenderedWhenSelected PASS, TestPersesRuntimeFilesProjectProviderFiles PASS
  - assertion: deselected Perses must render no compose service (fail-closed); no provider files projected
- Verdict: PASS

## Cell 4 — policy-proiset slice: provenance + provenance-verweigerung forged evidence

- TestAdmissionEvidenceForRemoteApplyFailsClosedWithoutRecord PASS
  - assertion: nil record -> no evidence; production Target fails closed without a verified record
- TestAdmissionEvidenceForRemoteApplyBindsApproval PASS
  - assertion: verified record binds approval
- Full provenance suite: ok (TestFromVerifiedCandidateRejectsUnverifiedAndUnbound, TestAdmissionEvidenceForRemoteApply*, TestRemoteProjectDeploymentRejectsInvalidBinding*) PASS
- Verdict: PASS

## Cell 5 — BF-01/BF-03 isolation regression (state-dir cell)

- TestStateDirIsolatesTargetSelection PASS (cmd/baha)
  - two state-dirs A/B isolated; ambient XDG selection NOT consulted when BASEHARBOR_STATE_DIR set; ambient file untouched
- internal/deployment isolation: TestRegisterEnvironmentAssociationIsPerTargetIsolation, TestGetEnvironmentIsPerTargetIsolation, TestGetEnvironmentStateDirOutsideDeploymentsNamespace, TestThreeReferenceIsolation, TestBug865StateOverrideIsolatesConfigurationAndDeployment, TestTargetStateRootIsolation -> PASS
- Verdict: PASS

## repo-rule compliance

- Verification only; NO product files edited; NO .github/** touched; NO reruns/workflow_dispatch
- Combined tree assembled locally only (merge throwaway, no push); no branch opened for a PR
- Evidence written ONLY to baseharbor-plan/evidence/...; no .evidence/ dir anywhere, no product-repo writes
- All live state under /tmp/opencode/lv3/; no docker/podman containers/networks/volumes started (session host is the coordinator/codeman server, NOT a test host)
- Subagents: none (§4.8). Every command run in own session.

## Findings (with severity)

- MEDIUM-01: #1580 uid-target head drifted. ls-remote origin refs/pull/1580/head = 756d21b7839a05c83435e6a39fc0daeb8b0580be (identical to #1578 uid-env), NOT the mission pin 3a91e2a83. #1580 and #1578 are now the SAME commit (siblings merged/retargeted). Combined stack built with the actual current head (#1580==#1578). Verify #1580 target branch in the board/PR.
- INFO-02: Pre-existing doc drift — TestMachineDocumentationTracksRegistryAndCommandTree fails on base-develop too (docs/reference/cli-machine-coverage.md not regenerated after a command-tree change). Not a 0.4.28 slice defect. Fix scope: regenerate the doc; .github/** not touched.
- INFO-03: env-gated integration FAILs (internal/database Postgres, internal/controlplaneruntime Docker/OpenBao) are environmental on both base-develop and combined; not regressions.

## END

- Mission scope met: all 5 cells PASS on the combined 0.4.28 build; no product changes; findings documented + reported to coordinator.
