ROLLE: REVIEW
**Verdict: APPROVE CONTENT — PR Selected Checks remain failed on unrelated 0428-210 test**

# PR #1740 — 0428-209 native cell operator seam

## PLAN

1. Read the mission and add this plan plus the live board plan before Git inspection.
2. Verify the exact PR head, base refs, ancestry, and stable-head condition.
3. Review the two-file diff and trace the native test's runWithIO authorization through the shared test seam.
4. Inspect exact-head CI, native-cell results, cli-0 failure, logs, and the relationship to PR #1739.
5. Verify the complete changed-file list against the allowed write-set and owner-stack exclusions.
6. Publish this evidence file only and verify the Planning path and final PR head.

## Candidate and session

- Card: t-20261121-native-cell-operator-seam / 0428-209.
- PR: mcpdev80/baseharbor#1740, branch lane-0428-209-native-cell-operator-seam.
- PR head before review: 0ffe093357d9f7fb52f5e7542f4ade41e48fab1b.
- PR base: lane-0428-198-cli-shard-operator-env at e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- Session: Codex review session; session identifier is not exposed in this interface.
- Model/backend: GPT-6.2, Codex API session.
- Review time: 2026-11-21 05:19 UTC.
- Planning remote witness from git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v:
  origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
  origin https://github.com/mcpdev80/baseharbor-plan.git (push)
- Product remote witness from isolated review clone: origin https://github.com/mcpdev80/baseharbor.git (fetch/push).
- PR API reports exact head 0ffe093357d9f7fb52f5e7542f4ade41e48fab1b, base ref lane-0428-198-cli-shard-operator-env, base SHA e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4, open, draft false, not merged.
- ls-remote confirms base branch e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 and both candidate branch and refs/pull/1740/head at 0ffe093357d9f7fb52f5e7542f4ade41e48fab1b.
- git merge-base --is-ancestor e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 PR-head exited 0.
- Exact diff against base: cmd/baha/control_plane_single_native_ci_test.go; cmd/baha/runtime_integration_test_support_test.go.

## P1 — shared operator seam is used; production enforcement is unchanged

The candidate's cmd/baha/runtime_integration_test_support_test.go:930-938 clears BASEHARBOR_TARGET, calls runWithIO(ctx, args, out, out) for target create, and selects the new target only after registration. The native acceptance test reaches ensureRuntimeIntegrationTrustPlane at cmd/baha/control_plane_single_native_ci_test.go:28-30.

The shared runWithIO path in cmd/baha/main.go:149-164 applies operatorauth.WithEnforcement, then routes eligible test-binary calls through testOperatorContext. cmd/baha/operator_test_fixture_test.go:25-29 binds that to operatorAuthFixtureContext; lines 61-72 add a verified principal and membership provider. internal/operatorauth/context.go:54-57 confirms WithVerifiedPrincipal itself initializes enforcement before setting the principal. This is the shared test-only seam, not a private stamp in this card. Production enforcement is untouched because the PR changes only two _test.go files.

The exact run reports PR · Native Keycloak/Core · docker (job 136738825463) and podman (job 136738825465) as success. The task's exact-head test-to-gate mapping identifies TestControlPlaneSingleDefaultNativeRuntimeInCI in both jobs and records PASS lines. Direct gh run view --job ... --log retrieval for these jobs returned 0 bytes during this review; I rely on the exact-run job conclusions and the published test-to-gate mapping, not a claim that I independently read the PASS lines.

## P2 — cli-0 failure is a distinct 0428-210 issue, not operator-auth inheritance

Run 44868911131 is terminal failure, pull_request event, exact head 0ffe093357d9f7fb52f5e7542f4ade41e48fab1b. PR Selected Checks is failure. Go unit cli-0 failed; cli-1, cli-2, cli-3 succeeded. Both Native Keycloak/Core cells succeeded.

For this run, gh run view 44868911131 --repo mcpdev80/baseharbor --log returned 900721 bytes. Counting unique first-level --- FAIL: Test lines gives exactly one: TestAppListAllTargetsWorksAfterInstallationDestroy. The gate-text count for requires an authenticated BaseHarbor operator is zero. --log-failed returned 8594 bytes; cli-0 job 136738825446 returned 45757 bytes. The failure line is:

app_list_all_targets_test.go:26: all-targets inventory depended on deleted Target config "docker-dev": BaseHarbor config root is configured but the config.yaml is missing: /tmp/TestAppListAllTargetsWorksAfterInstallationDestroy3183043325/001/config/config.yaml

It is followed by --- FAIL: TestAppListAllTargetsWorksAfterInstallationDestroy (0.01s).

I independently checked PR #1739: head 79d962a063be8339a071a681afde4bb35ef4688c, title fix(cmd/baha): tolerate missing config for --all-targets inventory after destroy, changed file cmd/baha/app_commands.go. This is the separate 0428-210 failure. It is absent from #1740's diff and is not an inherited operator-auth failure. State: the overall required aggregate remains red due to the separate card; #1740 is not merge-ready until the stacked required checks resolve and a valid exact-head aggregate succeeds.

## P3 — exact allowed write-set

The diff changes exactly cmd/baha/control_plane_single_native_ci_test.go and cmd/baha/runtime_integration_test_support_test.go, both explicitly allowed. No other cmd/baha file, .github/**, internal/operatorauth/**, internal/serviceaccess/**, internal/identityprovider/**, internal/observability/registry.go, or internal/capability/perses_selection.go is changed. The owner-stack exclusions hold.

## P4 — base movement and candidate stability

The owner reports that the base lane moved five times today, most recently to e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4. I independently confirmed this current base from the PR object and ls-remote, and confirmed it is an ancestor of the exact PR head. I did not reconstruct all five intermediate transitions. The candidate branch and refs/pull/1740/head matched before review.

## Verdict and merge state

**Verdict: APPROVE CONTENT — PR Selected Checks remain failed on unrelated 0428-210 test**

The card's two-file change uses the shared test-only runWithIO operator seam, preserves the valid authorization order, and leaves production enforcement untouched. Its specified Docker and Podman native cells are successful on the exact candidate. The overall PR Selected Checks aggregate is not green because cli-0 fails in the separate #1739/0428-210 test; do not merge until that stacked required-check failure is resolved. No correction recipe is issued against #1740 for that unrelated failure.

## Head stability

- PR head before review: 0ffe093357d9f7fb52f5e7542f4ade41e48fab1b.
- PR head after review: pending final remote recheck before publication.

END_DONE: review complete; content verdict recorded; no candidate, PR, workflow, or test changes made.
