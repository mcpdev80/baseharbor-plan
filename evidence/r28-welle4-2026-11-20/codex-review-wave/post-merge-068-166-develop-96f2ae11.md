# Post-merge review: 0428-068 and 0428-166 at develop 96f2ae11

ROLLE: CODEX-REVIEW
**Verdict 0428-068: BEFUND MIT REZEPT**
**Verdict 0428-166: PASS**

- Session-ID: not exposed by this execution interface; not fabricated.
- Model/backend: GPT-6 agent runtime; more precise backend identity is not exposed in-session.
- Review time: 2026-11-20 12:12 UTC (13:12 Europe/Berlin).
- Product clone/worktree: `/var/tmp/codex-review-wave/baseharbor-develop-96f2`, detached at the requested commit.
- Plan clone: `/var/tmp/codex-review-wave/baseharbor-plan`.
- `develop before review = 96f2ae11a25a508998c44a9854ef17f8fa15c112`
- `develop after review = 96f2ae11a25a508998c44a9854ef17f8fa15c112`

## Scope and independent witnesses

Read-only audit of the merged implementations for `t-20261114-r28-cli2-context-shell` (0428-068) and `t-20261120-r28-signal-id-normalization-collision` (0428-166). No product files, PRs, or card states were changed. `python3 scripts/plan.py show` on fetched plan `origin/main` reported both cards `state: accepted` (not `closed`); this audit does not update planning.

```text
gh api repos/mcpdev80/baseharbor/pulls/1710 --jq '[.head.sha,.merge_commit_sha,.merged_at] | @tsv'
74f5f707b812a1c052e725839c3d8a84d8747557 f1c2c34236f4d932fb01403dcecad1b7a6965716 2026-11-20T11:04:29Z

gh api repos/mcpdev80/baseharbor/pulls/1712 --jq '[.head.sha,.merge_commit_sha,.merged_at] | @tsv'
a83fcc707f814e8d62db2e528d28816196f3e841 96f2ae11a25a508998c44a9854ef17f8fa15c112 2026-11-20T11:33:24Z

git rev-parse refs/review/postmerge/1712^{tree} origin/develop^{tree}
5dbd30e493188a65eb50bd5f7fd9c77258e4e6cf
5dbd30e493188a65eb50bd5f7fd9c77258e4e6cf
git diff --quiet refs/review/postmerge/1712 origin/develop; echo $?
0
```

PR #1712's tree is identical to develop 96f. PR #1710 merged at `f1c2c342…`; the owner follow-up #1713 (`e3b4300f…`) is immediately before that merge in the observed history. The initial product clone's checked-out local `main` was not used: review used a detached worktree pinned to `origin/develop` 96f.

## 0428-068 — BEFUND MIT REZEPT

### B1 — context-use operands

`cmd/baha/completion_setup.go:84-90` calls the executable with the original `"$@"`, then branches on `case "$1:$2"`; successful `context use` evaluates that invocation's output (`:86-90`). Fish does the same with `command baha $_baha_argv` and evaluates the returned snippet (`:66-71`). The Bash end-to-end test begins with `BASEHARBOR_TARGET=docker-dev`, executes `baha context use prod`, and asserts the parent shell sees `prod` (`cmd/baha/context_terminal_test.go:373-407`). **B1 covered.**

### B2 — fish recursion, guards, completion

Fish's internal call is `command baha` (`completion_setup.go:64-67`), bypassing the function wrapper defined at `:78-80`. `TestContextWrapperCallsRealCommandViaCommand` asserts `command baha` in both Bash and fish and rejects the recursive bare call (`context_terminal_test.go:217-230`). `TestCompletionWorksWithHookInstalled` checks generated completion forwarding for Bash/Zsh/Fish (`:233-254`); `TestInteractiveGuardPresent` checks interactive guards (`:302-317`). Production guards are at `completion_setup.go:111-123`.

`TestEndToEndInstalledZshAndFishWrappers` drives those shells only if installed and continues otherwise (`context_terminal_test.go:434-439,491-505`). The hosted success does not prove which optional interpreters were installed, so I do not claim real Fish execution from that test without the runner's binary-presence evidence.

### B3 — persisted-over-default test gap

Production precedence is explicit override (`cmd/baha/context_terminal.go:187-190`), shell environment (`:195-205`), persisted selection (`:206-210`), then configured default (`:211-213`). The behavior is present, but its regression evidence does not establish it through the product command path:

- `TestContextPrecedenceDefaultFallback` writes persisted `docker-dev` and directly calls `effectiveContextOrigin` (`cmd/baha/context_terminal_test.go:122-135`). The fixture also sets `DefaultTarget: "docker-dev"` (`cmd/baha/target_test_helpers_test.go:44-47`); it never verifies `baha context show` output or a distinct persisted target winning over the default.
- `TestContextShowReportsWinningStage` uses `runContextShowCommand` but tests only the configured-default stage (`context_terminal_test.go:156-163`). `TestContextPrecedenceTerminalEnvWinsOverDefault` directly calls the helper (`:109-119`).

**Follow-up recipe:** add a regression in `cmd/baha/context_terminal_test.go` with configured default A and persisted target B; invoke actual `baha context show` using `runContextShowCommand` and assert B plus the persisted-origin label. It must fail when persisted/default resolution order is reversed and be included in a successful CLI Go-unit shard. **Stop criterion:** do not treat precedence acceptance evidence as complete until that command-path test is CI-executed and the order mutation makes it fail.

### B4 — mutation independence

Current source comments map three separate mutations to three separate tests (`context_terminal_test.go:329-351`): remove shell export → `TestEndToEndBashInteractiveContextUseAndClear`; remove interactive guard → `TestInteractiveGuardPresent`; remove completion forwarding → `TestCompletionWorksWithHookInstalled`. Thus current A/B/C targets are distinct (the old A/C overlap no longer describes the merged source). These comments record prior individual mutation runs; this post-merge audit did not rerun them. Fish recursion has a structural assertion at `:217-230`; no separate fish-only recursion mutation transcript was found. The optional-interpreter caveat is recorded under B2.

### 068 CI

Run `44723710049` for final #1710 head `74f5f707…` completed successfully; `PR · Go unit · cli-2` and `cli-3` succeeded. The precedence tests are selected in cli-2; `TestEndToEndInstalledZshAndFishWrappers` is selected in cli-3. The later #1712 run `44727442216` also ran cli-2/cli-3 successfully on a tree identical to develop 96f. The post-merge develop push runs were Docker/Podman runtime jobs; I do not claim a Go-unit job ran on the merge push itself.

## 0428-166 — PASS

### P2 — legacy rebook persists before collision rejection

`internal/observability/provider_registration.go:97-100` calls `RebookLegacySignals` inside the `mutate` callback. The collision guard records `registrationErr` and returns the rebooked `sources` with nil callback error (`:109-118`); after `mutate` completes, it returns `registrationErr` (`:129-133`).

The callback uses the existing shared lock: `internal/observability/registry.go:598-600` delegates to `mutateChanged`; that function takes exclusive flock on `<registry>.lock` (`:615-627`), runs the callback (`:637-640`), and writes changed data (`:647-667`). Returning a callback error here would discard callback edits, so nil is essential to persist the unrelated successful rebook.

`TestRegisterKeycloakSignalsCommitsLegacyRebookBeforeRejectingCollision` verifies rejected collision, retained foreign owner, and independently rebooked source visible/removable (`internal/identityprovider/keycloak_legacy_migration_integration_test.go:432-533`). `TestRegisterKeycloakSignalsPreservesCanonicalLegacyOwnerOnCollision` covers a legacy record whose canonical destination is already foreign-owned (`:540-610`). This closes the prior P2 ordering concern.

### Backward-compatible `keycloak:` IDs

`TestKeycloakSignalIDGoldenSingleTokenStable` pins literal IDs `keycloak:bh-cluster-alpha-prod` and `keycloak:bh-cluster-beta-prod` (`internal/identityprovider/keycloak_signal_golden_test.go:18-39`), registers both and checks both owners remain listed (`:45-78`). Expected values are literals, not calculated by the production formula. The collision-boundary regression is `TestKeycloakSignalIDCollisionOnNormalizationBoundary` (`internal/identityprovider/keycloak_signal_collision_test.go:24-85`).

### 166 CI inclusion

PR run `44727442216` completed successfully on head `a83fcc707f814e8d62db2e528d28816196f3e841`, with a tree identical to develop 96f. The queried jobs were:

```text
PR · Validation · identity-provider-package-tests  success
PR · Go unit · packages                              success
PR · Go unit · cli-2                                 success
PR · Go unit · cli-3                                 success
```

The package job logs reported `ok github.com/mcpdev80/baseharbor/internal/identityprovider` and `ok github.com/mcpdev80/baseharbor/internal/observability`; the targeted identity-provider job matched `./internal/identityprovider`. These are executed, not skipped. The post-merge `develop` runs at 96f were `44728572807` Runtime Docker Core and `44728573148` Runtime Podman Core, both success; no Go-unit job was in that push run. Unit evidence above is the successful PR run on identical source bytes.

## Outcome

- 0428-068: **BEFUND MIT REZEPT** — B1/B2 and distinct current A/B/C mutation target mappings are evidenced; B3 lacks a persisted-over-default assertion through the actual `baha context show` path. Follow-up recipe is above; no implementation was made.
- 0428-166: **PASS** — collision handling persists successful rebook under the existing lock; the legacy `keycloak:` golden schema and relevant executed CI packages are evidenced.
