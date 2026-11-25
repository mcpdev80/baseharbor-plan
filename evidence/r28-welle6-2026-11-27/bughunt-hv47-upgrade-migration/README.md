# Bug Hunt H-V47 — version-upgrade & migration surface

Lane: w190-0428-224-hunt-v47
Type: pure finding, no product changes (read-only)
Base develop tip (ls-remote witness): `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`
Mission anchor was `384d857b5`; develop moved to `99d9ddebc` (Merge PR #1844) before the cut, so the worktree was taken at the exact CURRENT tip per the mission's "unless moved" clause.
Worktree: `workers/w190-0428-224-hunt-v47-wt` (cut at exact develop tip, detached HEAD)
Build: `go build -o /tmp/baha-w190 ./cmd/baha` => exit 0 (surface compiles)
Evidence location: baseharbor-plan (planning repo `https://github.com/mcpdev80/baseharbor-plan.git`, verified via `git -C .../baseharbor-plan remote -v` — see repo-rule section)

## Cross-reference with H-V46 (no duplicate rows)

H-V46 (`../bughunt-hv46-state-lifecycle/README.md`, anchored at `2a141387d`) covered destroy/quarantine-era
lifecycle: never-delivered proof leak (BF-46-2), reserved-namespace scans (BF-46-3/4), full-destroy volume
vocabulary (BF-46-1/5/6), atomic-write seams (BF-46-7). This hunt covers the version/upgrade/migration
surface and does NOT restate those. Structural overlap is marked where a row would otherwise collide:
- The word "quarantine" appears nowhere in the current tree (git grep at `99d9ddebc` returns 0 hits;
  command witness in the transcript). The H-V46-era quarantine concern survives in code only as the
  damaged-state namespace (BF-46-3/4, already carded) — BF-47-9 below is the upgrade-path consequence
  of that same seam and is scoped to version-gated records only, explicitly not a re-file of BF-46-3/4.

## PLAN

- Read mission + cross-check H-V46 akte (done first)
- ls-remote develop tip, fresh worktree at exact tip
- Map version-upgrade/migration surface (per-artifact version gates)
- Analyze older-data-dir behavior of develop-era binaries (incl. damaged-state cross-reference)
- Analyze migration idempotence and downgrade paths
- Compare release-note promises vs code behavior
- Write findings + proposed card lines; cleanliness; push to origin/main; END_DONE

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82 refs/heads/develop`
- Worktree `workers/w190-0428-224-hunt-v47-wt` checked out at exactly `99d9ddebc` (detached HEAD).
  Read-only hunt: no candidate branch, no commits in the product repo, so there is no commit-ancestor
  relationship to prove and no PR was opened.

## Surface map (what "version" means per persisted artifact)

- `~/.config/baseharbor/config.yaml`: `ConfigVersion = 1` (`internal/deployment/target.go:19`), exact-
  equality gate at `target.go:331` (read) and `:397` (validate); no migrate-from-N.
- deployment record `deployment.json`: `DeploymentRecordVersion = 2` (`internal/deployment/deployment_store.go:19`),
  load gate `deployment_store.go:661-670` emits kind `deployable_version_mismatch`; CLI translation
  `cmd/baha/app_context.go:452-463`; save refuses foreign versions `deployment_store.go:418-423`.
- provider registry `provider-registry.json`: `RegistryVersion = 2` (`internal/capability/registry.go:16`),
  gate `registry.go:395-396`; v1→v2 was bumped in `642bc6abd` (2026-10-01) with NO loader migration.
- shared-backend `state.json`: `sharedBackendStateVersion = 3` (`internal/application/shared_backends.go:17`),
  fail-closed typed mismatch `shared_backends_state.go:31-33` + `shared_backends.go:19-37` ("upgrade-from-outside
  state: do not migrate or rewrite").
- Core SQL schema: embedded migrations `internal/database/migrations/0001..0011`, applied only by
  `database.Migrate` (`internal/database/migrations.go:29-58`), verified (never applied) by
  `VerifySchemaReady` (`internal/database/schema_readiness.go:18-67`).
- Core update planner classification: `internal/coreupdate/plan.go:141-183` (downgrade/major => Unsupported),
  journal resume `internal/coreupdate/execution_journal.go:14-78`.
- Provider upgrade adapters: Keycloak/OpenBao refuse downgrade (`internal/providerupgrade/keycloak/adapter.go:158`,
  `internal/providerupgrade/openbao/adapter.go:94`); Keycloak native CheckUpgradePath always fails without
  injected compatibility evidence (`internal/providerupgrade/keycloak/native_ops.go:49-53`).
- Self-update: relation computed `cmd/baha/update.go:187-199`, mutation refuses `target-older` and `unknown`
  (`cmd/baha/update_mutation.go:43-50`).

## Findings

### BF-47-1 — The release promise "existing environmentless v1 [provider-registry] entries remain readable and migrate during reconciliation" is false in the loader: an actual v1 file fails Validate before reconciliation can ever run

- File: `CHANGELOG.md:370` (v0.4.19 "Changed" section); code: `internal/capability/registry.go:395-396`
  (`Validate` rejects `r.Version != 2` with `unsupported provider registry version %d`), load path
  `internal/capability/registry.go:448-463` (`RegistryStore.Load` runs `Validate` on every read), and
  `store.Update` → `s.Load()` first (`registry.go:473-484`), so reconciliation
  (`internal/application/provider_registry.go:85-97`) can never reach an erroring load.
- What it shows: the v1→v2 bump (`642bc6abd`, 2026-10-01) changed only the constant and added
  UUID-keyed bindings; there is no loader migration from a Version-1 file. What DOES exist is a
  *within-version-v2* legacy-shape migration: bindings whose `Environment` field is empty stay
  readable (lenient matching at `internal/application/provider_registry.go:211-215` and
  `cmd/baha/app_core_requirement.go:96-99`) and are rewritten with the environment on reconcile
  (`releaseManagedBindingsPreservingInstances`, `provider_registry.go:68-75` + re-`BindDeployment`).
  The regression test `TestProviderRegistryMigratesLegacyEnvironmentlessBindingOnReconcile`
  (`internal/application/provider_registry_test.go:378`) constructs its fixture with
  `capability.NewRegistry()` — i.e. Version=2 with an environmentless binding (`registry.go:61`).
  A real v0.4.18-era file (version:1, name-owned instances, `provider_version` absent) fails
  Load/Validate outright: the first `baha up/plan/status` after upgrading dead-ends with
  "unsupported provider registry version 1" and no documented recovery path; the migration test
  passes without covering the file-version case it claims to prove.
- Severity: medium-high (documented upgrade promise vs behavior; brownfield installs from ≤0.4.18
  hit a hard wall with no remediation hint in the error).
- Proposed card line: "Fix provider-registry v1→v2 upgrade: either implement a loader migration for
  Version-1 files (name-owned instances → UUID-scoped bindings, keeping the environmentless binding
  migration) or correct CHANGELOG/docs to state that pre-v0.4.19 provider-registry files are NOT
  readable and name the operator recovery; add a regression test that loads an actual version:1
  fixture through `RegistryStore.Load` + `ReconcileReferenceProviderRegistryAt`."

### BF-47-2 — Deployment record version gate has no migrate-at-load path: version-1 records are permanently unloadable and `baha destroy` offers no route to clean them (downgrade-adjacent deadlock)

- File: `internal/deployment/deployment_store.go:661-670` (any `record.Version != 2` at load, including
  version 1, becomes `deployable_version_mismatch`), next-action text `cmd/baha/app_context.go:459-462`
  ("Run the same or a newer BaseHarbor that wrote this deployment's state to inspect or remove it"),
  save refuses older records `deployment_store.go:418-423`, and the drift check
  `internal/deployment/deployment_identity_drift.go:51-52` tells the operator "do not remove a record
  whose storage version is unsupported".
- What it shows: the 0427-149 era added name-identity uniqueness (comment `deployment_store.go:434-437`),
  so a new deployment cannot claim the (target, app, env) triple while the old v1 record exists — but a
  v1 record is invisible to every listing/removal path in the current binary. The remedy "run the older
  BaseHarbor that wrote it" contradicts the self-update downgrade refusal
  (`cmd/baha/update_mutation.go:43-45`): BaseHarbor forbids obtaining the only binary that can remove
  the state it refuses to migrate. `docs/spec/candidate-contract-v1.md:92-94` promises "existing
  deployment records written before this field existed remain loadable" — true only for records already
  at version 2 with a missing field, not for v1 storage.
- Severity: medium (brownfield upgrade dead-end for pre-stable-identity installs; operator must delete
  state by hand with no supported command).
- Proposed card line: "Decide the deployment-record v1 story: implement migrate-at-load (v1→v2 field
  projection) or document the explicit operator recovery path (and a supported removal command) for
  `deployable_version_mismatch`; align the `candidate-contract-v1.md:92` loadability promise with the
  gate at `deployment_store.go:661`."

### BF-47-3 — Version-gated deployment records are SKIPPED by `baha destroy --all` but the data root is then deleted wholesale: owned provider state of an unloadable deployment can be destroyed while its ownership record is never consulted (cross-reference BF-46-3/4, upgrade-path only)

- File: `cmd/baha/runtime_destroy_discovery.go:126-145` — `fullDestroyDeploymentWarnings` renders every
  state-error warning as `SKIPPED … "incomplete deployment state has no usable deployment.json; refusing
  to guess semantic/runtime ownership, local BaseHarbor state will still be removed"` — then
  `cmd/baha/runtime_destroy_all.go:602` executes `os.RemoveAll(dataRoot)` once no FAILED blocker exists.
- What it shows: the warning text (written for missing-damaged.json semantics, BF-46-3) is applied
  uniformly to ALL warning kinds — including `deployable_version_mismatch`, which has a *readable*
  deployment.json the current binary simply refuses to load, and `corrupt`. The destroy flow therefore
  (a) never runs the child app-destroy lifecycle for that deployment (no provider stop/release under the
  ownership gate), yet (b) removes the entire data root anyway, taking the v1 record and any Target-local
  provider state (`targets/<t>/provider-registry.json`, shared-backend dirs under the target root) with it
  without ever honoring the "preserve both data owners" behavior BF-46-6 audited. On the pre-BF-46-6
  heuristic gate this is an unverified-delete path distinct from the volume-inventory finding already
  carded: here no inventory runs at all.
- Severity: medium (data-ownership disclosure gap on the one destroy path that skips child lifecycle).
- Proposed card line: "In `fullDestroyDeploymentWarnings` distinguish `deployable_version_mismatch`/
  `corrupt` from missing-record `incomplete`: name the kind and version in the SKIPPED line, and either
  inventory that deployment's owned volumes before `os.RemoveAll(dataRoot)` or block destruction with a
  FAILED entry until the operator acknowledges losing that specific deployment's provider state."

### BF-47-4 — `baha update --recover` has no CLI preflight: a wrong --version reaches destructive restore/replay logic, guarded only by runtime-observed pin/journal state

- File: `cmd/baha/update.go:92-94` (recover branch dispatches straight to `recoverNativeCoreHA`),
  `cmd/baha/update_ha_recovery_command.go:12-49` (lock, `coreinstallation.Load`, HA+ownership check at
  line 30, `coreUpdateJournal(root, release, false)` line 41, then `recoverOwnedCoreHA`), contrast the
  forward path `cmd/baha/update_mutation.go:54-61` which runs `preflightNativeCoreUpgrade` BEFORE any
  mutation. The CLI never loads the release catalog (`internal/coreupdate/catalog.go:36-44`) nor
  compares `opts.Version` against the installed version for the recover path.
- What it shows: `baha update --recover --version X --yes` for an X with no embedded pin (only
  `internal/coreupdate/releases/v0.4.24.json` ships) or for an X older/newer than the current HA
  installation depends entirely on journal/DCS/backup state to refuse. The Long help (`update.go:78`)
  promises it "restores the owned Core HA PostgreSQL and DCS to that update's verified backup point",
  i.e. a restore that displaces volumes ("retains displaced volumes") can begin from a mistyped version
  if a stale journal from an interrupted update to X is still on disk. There is no cheap "does release X
  exist in the catalog / is a journal for X present" gate before entering recovery.
- Severity: medium (mistake amplification on the most data-sensitive update verb; failure would need a
  stale journal to be destructive, so not high).
- Proposed card line: "Add a recover-path preflight: require `coreupdate.LoadRelease(version)` to
  succeed and a matching durable recovery point/journal entry for that release before invoking
  `recoverOwnedCoreHA`; refuse with a named reason otherwise. Cover with a unit test through the CLI
  dispatch (no real runtime)."

### BF-47-5 — Keycloak provider migration is structurally dead in the native build: `CheckUpgradePath` always errors, so any identity delta makes the whole `baha update --yes` fail closed

- File: `internal/providerupgrade/keycloak/native_ops.go:49-53` (returns
  "Keycloak upgrade path lacks reviewed compatibility evidence" whenever `Hooks.Compatibility == nil`);
  classification path `internal/coreupdate/plan.go:166-167` marks Identity changes `MigrationRequired`;
  `internal/coreupdate/plan.go:241-247` and `Execute` (`:251-289`) then require working migration hooks;
  `internal/providerupgrade/keycloak/adapter.go:158` refuses downgrades.
- What it shows: grep for the Compatibility hook's production wiring finds only test fixtures (native
  adapters are constructed without it in the shipped paths), so on a real host the assessment
  preflight (`openbao/adapter.go:99` pattern; Keycloak adapter equivalent) permanently refuses: every
  release that bumps the Keycloak pin turns `baha update --yes` into a hard failure at provider
  migration preflight, even though `docs/spec/core-provider-update-v1.md:16` defines
  `migration_required` as a supported classification. The CHANGELOG promise "Provider updates require
  compatible release-pinned images … PostgreSQL major upgrades and unsupported provider upgrade paths
  remain blocked" (`CHANGELOG.md:155`) never states that IDENTITY provider minor upgrades are ALSO
  blocked for lack of a compatibility hook.
- Severity: low-medium (fail-closed, no data risk; but an under-documented upgrade dead-end that
  releases must name, or a missing implementation card; docs/explanation/providers.md:145 + issue #857
  already tracks the Shared-Keycloak database variant — this row covers the general native pin bump).
- Proposed card line: "Either wire a reviewed Keycloak compatibility-evidence hook into the native
  providerupgrade adapter or document in the release notes / provider-contract spec that managed
  Keycloak pin upgrades are currently unsupported (`migration_required` cannot execute), consistent
  with CHANGELOG.md:155; add an update-plan test asserting the named refusal."

### BF-47-6 — `compareProviderVersions` classifies any non-numeric or unparsable installed provider version as a downgrade attempt → Unsupported, blocking the whole update; unknown ≠ not-evidence-of-downgrade is applied to the FORWARD direction too

- File: `internal/coreupdate/plan.go:76-119` (parse requires all-dotted-uint; e.g. `2.5.7-aarch64`,
  `v26.04.1-apricot` style OpenBao/Postgres tags or a custom registry suffix fail parse),
  `plan.go:161-163` (`providerDowngrade(current, target)` is true when `compareProviderVersions`
  errors — see `:177-180`), `ha_spilo_compose.go:30` ("unknown, major-changing or downgraded Spilo
  transition" refused), and the guard comment `plan.go:75` ("An unknown version is not evidence that a
  destructive downgrade is safe").
- What it shows: the fail-closed design intent (unknown version ⇒ no destructive action) is applied
  symmetrically: an *upgrade* with an unverifiable-but-actually-newer installed tag is reported as
  "Core provider downgrade or unverifiable version" (`plan.go:162`) and blocks `baha update` even when
  the target pin is strictly newer. Images are release-pinned by digest, so the installed tag usually
  comes from the pinned image; but BYOC/adopted or previously hand-edited instances with suffixed tags
  permanently block provider reconciliation with a message that mislabels the direction ("downgrade").
  `plan.go:216-217` repeats the same conflation in execution validation.
- Severity: low (correctly fail-closed; defect is message precision + no escape hatch documented for
  an adopted BYOC instance).
- Proposed card line: "Split the classification: when the TARGET parses strictly newer than the last
  known pinned provider version, report `Unsupported: installed provider version unverifiable` rather
  than the downgrade wording; document the operator path (pin the installed image identity via a
  one-time reconcile) — tests in `internal/coreupdate` table the three message directions."

### BF-47-7 — config.yaml read migration is asymmetric: `LoadConfig` migrates-and-persists legacy TargetUIDs, `LoadConfigForMutation` does not, and both die on any Version != 1

- File: `internal/deployment/target.go:249-252` (LoadConfig → `migrateAndPersistTargetUIDs`),
  `target.go:263-278` (CAS persist of migrated config), vs `internal/deployment/config_mutation.go:20-41`
  (`LoadConfigForMutation` → raw `decodeConfig`, no migration) and `decodeConfig` gate
  `target.go:331-333`; save-time `Validate` `target.go:397-398`; forward-compat note
  `target.go:86` ("such a definition migrates idempotently on read").
- What it shows: a read-only command (`baha targets`, status paths) mutates the user's config.yaml
  (writes TargetUIDs) while a mutation command on the same file does not migrate before its own
  uniqueness checks — a mutation flow that collides with `ResolveTargetUIDs` (`target_id.go:161`)
  on empty UIDs behaves differently depending on which entry point read the file first. Separately,
  the exact-equality version gate means a config written by a FUTURE release (e.g. version 2) cannot
  even be parsed far enough to tell the operator how to recover: `unsupported BaseHarbor config
  version 2` with no next-action, and every mutation command fails at load. There is no
  "newer-than-this-binary" advisory path (status could surface it read-only).
- Severity: low-medium (read-time mutation asymmetry is a surprise side effect on a user-edited file;
  the version wall is the generic forward-compat gap shared by BF-47-8).
- Proposed card line: "Run `migrateAndPersistTargetUIDs` (or its pure `MigrateLegacyTargetUIDs`
  equivalent) inside `LoadConfigForMutation` so read and mutation paths observe the same post-
  migration config; and give `decodeConfig`'s version gate an actionable message distinguishing
  'too old — upgrade path X' from 'written by a newer BaseHarbor — update the CLI'."

### BF-47-8 — No persisted state file anywhere carries the BaseHarbor release version that wrote it; version-gate errors cannot say who wrote the state, and `verifyCandidateVersion` couples self-update verification to the exact human format of `baha version`

- Files: version constants without writer stamps — `internal/deployment/target.go:19`,
  `deployment_store.go:19`, `internal/capability/registry.go:16`,
  `internal/hosttrust/hosttrust.go:20`, `internal/externalprovider/store.go:16`,
  `internal/runtime/control_plane_credentials.go:132-155`, `internal/application/backup_metadata.go:16`,
  `internal/application/update_metadata.go:14`, `internal/application/recovery_metadata.go:16`,
  `internal/devgateway/gateway.go:23`, `internal/exposure/caddy.go:25`, `internal/serviceaccess/pki.go:525`
  (all emit only `unsupported … version %d` with no writing-release field; grep for
  `written_by|baseharbor_version|created_by` returns no production writers).
  Contrast `docs/reference/public-contracts.md:36`: "Artifact-specific version/ownership; no
  pre-freeze migration promise" — the register itself is the only upgrade doc, and no docs/ page
  contains the word "migrate" for local state (grep witness).
  Self-update verify seam: `cmd/baha/update_mutation.go:289-301` runs the candidate's `version`
  subcommand and string-matches `"baha <target> "`; `cmd/baha/main.go:139` prints
  `BaseHarbor %s` for `--version` and `cmd/baha/commands.go:205` prints `baha %s (commit …)` for the
  subcommand — the formats already differ, so any future humanization of `baha version` silently
  breaks every self-update.
- Severity: low (observability + brittleness; no data risk today).
- Proposed card line: "Stamp a `written_by` release field (or reuse `Applied.ControlState` digests) in
  the versioned state writers so `deployable_version_mismatch`-class errors can name the writing
  release; add a machine-readable `baha version -o json` field (`main.go:200` already emits
  `"version": version`) and re-target `verifyCandidateVersion` at that JSON instead of the human
  prefix, pinning the contract with a test."

### BF-47-9 — A binary older than the state (rollback to previous release) is refused by every gate with zero recovery guidance — the mirror of BF-47-1/2 and explicitly outside BF-46-3/4's damaged-state rows

- Files: every exact-equality gate listed in BF-47-8 (e.g. `internal/capability/registry.go:395`,
  `internal/application/shared_backends_state.go:31`, `internal/hosttrust/hosttrust.go:404`), with the
  one deliberate exception of the service-access gateway v1→v2 read-migration
  (`internal/serviceaccess/http_gateway.go:243-268`, recorded as the clean precedent pattern).
- What it shows: because the product refuses CLI downgrade (`update_mutation.go:43-45`) an operator can
  only reach this state by installing an older package manually. Every tool then fails at load with a
  version error that (a) does not say the state is NEWER than the binary, and (b) offers no next-action
  (compare the `deployable_version_mismatch` next-action, which at least names "run the newer binary").
  A newer-version file is also indistinguishable from corruption to the damaged-state scanner
  (`DamagedDirectoryState` only fires when deployment.json is ABSENT, `internal/deployment/damaged_state.go:188-191`,
  so a version-mismatched record is simply "not damaged, not loadable" — invisible to that recovery
  tooling, which is why this is not a duplicate of BF-46-3/4).
- Severity: low (self-inflicted path; fix is error-surface precision: name direction + next-action).
- Proposed card line: "For every state version gate, compare found vs supported numerically and emit
  direction-specific guidance: 'older than supported → see upgrade docs' vs 'written by a newer
  BaseHarbor → reinstall the newer release', reusing the typed-mismatch pattern of
  `SharedBackendStateVersionMismatch` (shared_backends.go:25-37) as the model."

### BF-47-10 — Clean baselines recorded (no card)

- SQL migrations: embedded, lexical-order, transaction-per-file, table-authoritative
  (`internal/database/migrations.go:29-58`); `RollbackLast` requires a matching `.down.sql` and never
  guesses (`migrations.go:61-107`); every forward file has a down file (11 pairs,
  `internal/database/migrations/`); `VerifySchemaReady` refuses ANY divergence including extra applied
  rows (`schema_readiness.go:51-64`) — a future-binary DB opened by an older binary fails closed as
  `unexpected migration`, matching the documented operator-api promise (`docs/how-to/operator-api.md:169-170`).
- Core update journal resume: verified steps re-verified, incomplete steps require a `Recover` hook,
  never implicitly skipped (`internal/coreupdate/execution_journal.go:14-78`; comment "validateExecutionPlan
  checks every step before journal resume can skip it" `plan.go:203-206`).
- Self-update downgrade/channel refusal (`update.go:187-199`, `update_mutation.go:43-50`) implements the
  CHANGELOG:1118 promise.
- TargetUID read migration is idempotent and CAS-pure (`internal/deployment/target_id.go:35-114`); the
  stale shallow-alias bug is already fixed with an explanatory comment at `target_id.go:83-87`.
- `sharedBackendStateVersion` gate + legacy environment-dir fallback (`shared_backends.go:119-133`) is
  the deliberate owner-verdict pattern referenced by BF-47-9.

## Fund summary

- Total findings: 10 rows (BF-47-1 … BF-47-9 actionable, BF-47-10 clean baseline).
- Actionable: 9. Medium-high: BF-47-1. Medium: BF-47-2, BF-47-3, BF-47-4. Low-medium: BF-47-5, BF-47-7.
  Low: BF-47-6, BF-47-8, BF-47-9.
- Cross-reference: BF-47-3 and BF-47-9 explicitly do not restate BF-46-3/BF-46-4 (they add the
  version-gated destroy/rollback consequences only).
- No product files edited. No CI/workflow touched. No containers or compose projects started.

## repo-rule compliance

- Read-only hunt; no product source edited; no `.github/**` touched; no workflow/rerun; no PR opened.
- Planning repo verified BEFORE first evidence commit:
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` =>
  `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Remote truth measured only via `git ls-remote https://github.com/mcpdev80/baseharbor.git` and a fresh
  `git worktree add` from the shared checkout's `lane-origin` (URL-resolved to github.com/mcpdev80); the
  quarantined `workers/baseharbor` checkout was not cited.
- Worktree placed at `workers/w190-0428-224-hunt-v47-wt` per the fixed workspace layout; nothing created
  under the ecosystem root itself.
- No subagents used; every step executed in this session.

## cleanliness

- No docker/podman containers or compose projects were started on this host (coordinator host is not a
  test host). `docker ps -a` before/after recorded; before-list file empty of new entries (daemon lists
  ambient stacks only, untouched): pid 1420817.
- Build artifact written to `/tmp/baha-w190` only.
- Worktree `workers/w190-0428-224-hunt-v47-wt` will be removed by the lane cleanup after END
  (read-only, detached HEAD, no commits, no stray files).
- besenrein: no test-owned containers/networks/volumes/state dirs created.

## Evidence on origin/main witness

(filled at push time below)

END w190-0428-224-hunt-v47 DONE — 9 actionable findings (1 medium-high, 3 medium), read-only, no product changes, anchored at develop tip 99d9ddebc.
