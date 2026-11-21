ROLLE: REVIEW
**Verdict: REQUEST CHANGES**

# PR #1738 — 0428-214 destroy authority stamp

## PLAN

1. Read the mission and record the numbered plan in the live board and this evidence before Git inspection.
2. Verify PR head, base refs, merge ref, ancestry, and whether the candidate stayed frozen.
3. Inspect the authority-stamp correction and trace the test through the real installation.destroy authorization boundary.
4. Inspect exact-head CI, byte counts, failing test names, and the earlier red-first evidence.
5. Check the allowed write-set, owner-stack exclusions, and recorded cleanliness evidence.
6. Publish only this review file and verify its origin/main path and the PR head again.

## Candidate and session

- Card: t-20261121-destroy-authority-stamp / 0428-214.
- PR: mcpdev80/baseharbor#1738, branch lane-0428-214-destroystamp.
- PR head before review: bdc3fcb63912a7a9be69be7bc10149deef07b5cf.
- PR base ref: lane-0428-198-cli-shard-operator-env.
- PR object base SHA: 80dc4987993b6855314c0112ad2c8645c15a4562.
- Current base branch ref: e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- Session: Codex review session; session identifier is not exposed in this interface.
- Model/backend: GPT-6.2, Codex API session.
- Review time: 2026-11-21 05:37 UTC.
- Planning remote witness from git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v:
  origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
  origin https://github.com/mcpdev80/baseharbor-plan.git (push)
- Product remote witness from the isolated read-only review clone: origin https://github.com/mcpdev80/baseharbor.git (fetch/push).
- PR API and ls-remote agree on candidate head bdc3fcb63912a7a9be69be7bc10149deef07b5cf. The PR base SHA is 80dc4987993b6855314c0112ad2c8645c15a4562, while the current remote base branch is e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4.
- GitHub commit API reports the candidate's sole parent as c2f9f2f32fd6bd27c0b0b4e269ad02fde6d643b5, the reported rebase point.
- Exact diff name list: cmd/baha/core_installation_runtime_test.go only.

## P1 — the synthetic authority stamp is still on the assertion path

The claimed withdrawal of the self-stamp is not present in this candidate. In cmd/baha/core_installation_runtime_test.go:294-306, coreBootstrapFixtureCleanupContext constructs a synthetic principal with issuer https://fixture.invalid, subject core-bootstrap-cleanup, IssuerVerified true, and editor group at :298-301, then attaches it with operatorauth.WithVerifiedPrincipal at :302 and a synthetic membership provider at :303-305. The test confirms that principal at :315.

The new assertion at :332-346 does call the production boundary and records the resulting mode, but it passes the same already-stamped context. At cmd/baha/operator_auth_boundary.go:55-60, ensureOperatorAuthForBoundary returns nil as soon as PrincipalFromContext succeeds. internal/operatorauth/context.go:54-57 shows WithVerifiedPrincipal also initializes enforcement. Then cmd/baha/mcp.go:292-302 bypasses the local-grant lookup when that principal exists and enters the boundary with the synthetic identity. internal/operatorauth/authorization.go:235-268 resolves the synthetic membership and records mode authenticated. The test explicitly accepts that mode at :341 and therefore accepts the fixture's own stamp as proof. The actual unauthenticated failure branch at authorization.go:283-292 is not shown to be reachable by this test.

This does not meet the card's proof contract: authenticated must represent a session, or local-runtime must represent the verified local grant. The current authenticated result is produced by the test-built issuer and membership, not a session. Calling the production boundary does not cure the test setup that short-circuits it.

Recipe: in cmd/baha/core_installation_runtime_test.go:274-306 and :309-346, separate the teardown-only fixture context from the authority assertion. Do not pass the helper's synthetic principal/membership context to the positive installation.destroy boundary assertion. Exercise the boundary with a real test session seam that represents the authenticated path, or with the verified local-runtime grant, and assert the exact admitting mode plus its source. Keep the remote-target and unrelated-principal denial cases genuinely unstamped. Add a negative regression that proves the unauthenticated installation.destroy path returns the exact gate denial before runtime access. Before accepting the correction, record a red-first run on the sick behavior: reintroducing the synthetic fixture stamp or removing the real authority input must make this test fail in its selected Go unit shard. Stop criterion: CI shows the unstamped denial at the production boundary, and the positive witness reports only a real session or verified local-runtime grant; a synthetic issuer must not pass as authenticated.

## P2 — exact run, shard outcomes, and red-first evidence

Run 44867319394 is completed/failure, pull_request event, candidate head bdc3fcb63912a7a9be69be7bc10149deef07b5cf. The overall PR Selected Checks is failure. The run log ref is refs/pull/1738/merge at 85ae2615014528e2c3610a7db06fa2a6c607d080, whose parents show “Merge bdc3fcb63912a7a9be69be7bc10149deef07b5cf into 80dc4987993b6855314c0112ad2c8645c15a4562”. Thus this run tested the candidate merged with 80dc, not the current base branch e454.

- gh run view 44867319394 --repo mcpdev80/baseharbor --log returned 903158 bytes.
- gh run view 44867319394 --repo mcpdev80/baseharbor --log-failed returned 16321 bytes.
- First-level FAIL lines: exactly three. The exact gate text “Managed-environment machine operations require an authenticated BaseHarbor operator” occurred zero times.
- Go unit cli-0 failed TestAppListAllTargetsWorksAfterInstallationDestroy and TestSecureProfileExportCommandPathAssemblesProductionWiring. cli-3 failed TestTargetInspectionProjectsBuiltInAccessCapabilities. cli-1 and cli-2 succeeded.

The logged failure lines are:

app_list_all_targets_test.go:26: all-targets inventory depended on deleted Target config "docker-dev": BaseHarbor config root is configured but the config.yaml is missing: /tmp/TestAppListAllTargetsWorksAfterInstallationDestroy2464468138/001/config/config.yaml

secure_profile_export_command_test.go:125: baha app secure-profile export through the command tree failed: operator authentication needs interactive setup but input is not a terminal (stderr: )

target_hotfix_test.go:201: target "edge-a" is not configured

These are not to be booked as a generic inherited gate class: the exact gate text is absent. The first test belongs to the separate 0428-210 / PR #1739 change in cmd/baha/app_commands.go. The secure-profile test belongs to the 0428-204 base-lane change; commit e45430f2 is titled “test(0428-204): authenticate secure export command path” and changes that test file. The target-inspection test is a 0428-198 base-lane fixture issue; commit 46017060 is titled “test(0428-198): register target before selecting it” and changes target_hotfix_test.go. Both latter fixes are beyond 80dc in the current e454 base, explaining why this old PR merge ref still fails them.

The test under review hashes to cli-0 under scripts/pr-go-unit-shard.py's four-way name assignment. It is absent from the exact run's failure list, so that run does not demonstrate the required red condition. The prior run 44862425216 was on ebc6ac9c3a3032a65256d285aeb510341820e218; gh run view --log returned 0 bytes, --log-failed returned 0 bytes, and the cli-0 job log returned 0 bytes. The lane's round-1 note says the test had no FAIL line there, but I could not independently retrieve those logs. No checkable red-first receipt on the referenced sick behavior (5fa43643 / 838aec5b) is available in the reviewed evidence. The current diff also leaves the synthetic stamp in place, so absence of a failure is not sufficient proof.

State: PR Selected Checks is failed on the three tests above, while the 0428-214 test is not shown failing. A new integration run on the current base is needed after the test correction; this review does not request a rerun or dispatch.

## P3 — write-set and protected files

The candidate changes only cmd/baha/core_installation_runtime_test.go, exactly the allowed write-set. No file from the owner stack PRs #1615, #1625, #1623, #1650, #1606, #1614, #1731, or #1704 is changed. No .github/**, internal/operatorauth/**, internal/identityprovider/**, or internal/serviceaccess/** path is changed.

## P4 — current base, PR merge ref, and cleanliness record

The owner reports five base movements today and that the lane has now been quiet at e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4. I confirmed the current remote base branch is e454. The PR API still reports base SHA 80dc, and refs/pull/1738/merge is 85ae, merging bdc into 80dc. The current base is not an ancestor of bdc: git merge-base --is-ancestor e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4 refs/review/pr1738 exited 1. Therefore the run's PR merge is stale relative to the current stacked base. The chainrebase act reports the rebase point c2f and lists the base-lane advances; the exact current base and exact run merge SHA are recorded above.

The lane's round-1 ## cleanliness section records one already-exited container in before/after docker ps -a output, with no lane-created running container or compose project. The same exited container name appears in the final witness, though the recorded container ID differs from the first before/after pair. This is evidence of no running container left by the lane, not evidence that docker ps -a was empty. I did not start or stop containers.

## Verdict and recipe

**Verdict: REQUEST CHANGES**

P1 remains open: the authorization assertion still consumes a synthetic principal stamped by the fixture, so the reported authenticated mode is not a session witness and the fail-closed denial is not tested. There is also no verifiable red-first proof for the sick behavior. The exact-run aggregate is red and its merge ref predates the current base; the unrelated failing tests are attributed above rather than blamed on this candidate.

Required correction: remove the synthetic identity from the authority-proof path in cmd/baha/core_installation_runtime_test.go, prove the real session or verified local-runtime path, retain the unstamped denial regression, and publish red-first evidence for the test in its selected cli-0 shard. Then rebase/hop to current base e454 and obtain a terminal exact-merge PR Selected Checks result before merge. Stop when the test denies the unstamped path before runtime and accepts only a real session or local-runtime grant, with CI recording the regression as executed.

## Head stability

- PR head before review: bdc3fcb63912a7a9be69be7bc10149deef07b5cf.
- PR head after review: pending final remote recheck before publication.

END_DONE: review completed; REQUEST CHANGES recorded; no candidate or PR mutation performed.
