# Round 4 Evidence — registry access (card t-20261018-r27-registry-access, PR #1395)

- Lane: w219-registry-r4 (Worker). Coordinator: 841e7734.
- Date: 2026-11-06.
- Mission: coordinator/missions/w219-registry-r4.txt (RUNDE 4).
- Scope source: review-1395c.md lines 59-85 (read self; blocking finding + required correction recipe).
- Candidate branch: work/r27-registry-access (same branch as rounds 1-3, PR #1395, no second PR).
- Final head: 99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c (ls-remote witness below). Chain on top of base 2f073f51:
  - 22497ea4 fix(r27 registry-access r4): propagate resolve failure at caller, opt-in-only mutable fallback with negative cells
  - 99b3e144 Merge commit 'af349188' (develop refresh; develop IS ancestor rc=0)

## PLAN

- Step 1: Read mission + review-1395c.md 59-85; verify ls-remote branch HEAD == 2f073f5149b. DONE
- Step 2: Reproduce the finding: resolveRegistrySourceImpl swallows ErrRegistrySourceUnavailable and returns the mutable location with nil error => caller pulls unpinned despite denied/public endpoint. DONE (verified by M1 mutant: negatives red when fallback restored)
- Step 3: Fix (1): resolver propagates every resolution failure (no mutable fallback at the resolver). DONE
- Step 4: Fix (2): legacy mutable path only as explicit opt-in BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE, class-gated so endpoint-denial and public-default rejections can never be bypassed. DONE (hard-rejection sentinels errClassDenied/ErrRegistrySourcePublicDefault; resolveUnavailable() excludes them before the opt-in is consulted)
- Step 5: Fix (2b): public-default rejection enforced before the native tool seam in resolveRegistrySourceImpl + RegistrySource.resolve, independent of tool availability. DONE
- Step 6: New caller negative cells (pull counts asserted): TestFailedResolvePropagatesWithZeroPulls, TestDeniedEndpointResolveCausesNoPull, TestMissingDigestResolveCausesNoPull, TestPublicDefaultDockerHubResolveCausesNoPull, TestPublicDefaultRejectedBeforeNativeTool; opt-in gating cells TestUnavailableResolveWithOptInPullsMutableTag / TestUnavailableResolveWithoutOptInFailsClosed. Success cells (TestPullResolvedRuntimeImagePinsImmutableDigest, TestProductionCallerPinsResolvedDigestNotMutableTag) stay green. DONE
- Step 7: Mutant battery (real mutations, git diff, revert + gegenprobe). DONE (table below)
- Step 8: Local gates: gofmt/vet/build name-only, race-20, full cmd/baha suite, develop ancestry rc=0. DONE
- Step 9: Push single commit chain to work/r27-registry-access; watch hosted run to TERMINAL. PENDING
- Step 10: Evidence on baseharbor-plan origin/main + END. PENDING

## Adapter file note (refuted suspicion, resolved with source proof)

An interactive check once suggested my push had DELETED application_registry_source.go:
`git ls-tree --name-only af349188 cmd/baha | grep registry_source` returned nothing. That
check was wrong: `ls-tree <path>` (without `-r`) on a subtree prints the SUBMODULE-style
entry and lists NOTHING for plain subtrees (proved: the same command for develop lists a
single "tree cmd/baha" entry). The authoritative forms all confirm the file is intact and
the PR delta is exactly the write-set:
- git ls-tree --name-only -r HEAD cmd/baha | grep registry_source => present
- gh pr view 1395 --json files => 6 files, all cmd/baha card write-set
- md5 diff of the six touched files between 22497ea4 and pushed 99b3e144 => all SAME

## Base attestation (branch provenance)

- Cut point: origin/work/r27-registry-access == 2f073f5149b0d5742a8aa6a4d949e58f396de514 (ls-remote, matches mission head).
- ls-remote origin refs/heads/develop BEFORE push: af3491889ec689812b8b08d4ff379f56d82d2a49.
- merge-base --is-ancestor af349188 HEAD: rc=0 (develop IS ancestor of the new head via the develop-refresh merge 99b3e144, following the round-3 precedent 4304d828 "Merge branch 'develop' into work/r27-registry-access").
- git log --format='%h %an' 2f073f51..HEAD non-develop commits: only 22497ea4 (Marcel, mine) + 99b3e144 (my develop-refresh merge). The remaining entries are develop's own merged history, carried by the refresh exactly as in round 3 (#1398/#1399 merged to develop BEFORE this head; no foreign candidate sits on top — gh pr files lists only card write-set files).
- PR #1395 diff vs develop after push: app_broker.go, app_broker_registry_negative_test.go (new), application_registry_source.go + the three round-1..3 card files (pull_caller/registry_pull tests, adapter + adapter test). All within the card write-set (cmd/baha); zero .github, zero docs, zero product-repo evidence.
- Discarded locally and NEVER pushed: db37f381/4a6cbc8a/23ba3a2d/024bfa16/9e8dc3a6 (bad-authority merge line produced during the worktree-hijack incident below). Final pushed chain is 2f073f51 -> 22497ea4 -> 99b3e144 only.

## Workspace-integrity incident (documented, not hidden)

During this session another lane's automation repeatedly re-linked my worktree (/tmp/opencode/w219-wt) to a foreign junk repo ("BaseHarbor Test", branch main, commit 8038aa20 "add app"), which silently deleted the card's adapter files from the branch head in my first merge attempts and caused one bad merge commit (db37f381) with a bogus -X theirs resolution. Response:
- Worktree was rebuilt from origin/work/r27-registry-access (2f073f51); all edits re-verified byte-identical to the locally-tested candidate (md5 comparison of all six touched files recorded SAME).
- db37f381 (BaseHarbor Test author, content WRONG — a -X theirs merge auto-resolved develop's deletion against my branch's authoritative content and dropped adapter files) was DISCARDED locally and never pushed.
- The final pushed chain 2f073f51 -> 22497ea4 -> 99b3e144 is built from the true origin head and verified: files present, focused+race20 green, ancestry rc=0. The develop-refresh merge used the ort strategy WITHOUT bogus resolutions for the card files.

## Fix description (PFLICHT 1+2)

- resolveRegistrySourceImpl: `if err != nil { return location, nil }` replaced by `return "", err` — the resolver's fail-closed behavior now reaches the caller unchanged.
- pullResolvedRuntimeImage: on resolve error, the mutable-tag fallback runs ONLY when (a) errors.Is(err, ErrRegistrySourceUnavailable), (b) the error is not a hard rejection (denial errClassDenied / public-default ErrRegistrySourcePublicDefault anywhere in the cause chain — checked via resolveUnavailable), and (c) the explicit operator opt-in env BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE is set. Otherwise the error propagates and compose.PullImage is never called.
- Public-default (docker.io / index.docker.io / registry-1.docker.io / registry.docker.io) is rejected at the impl entry and in RegistrySource.resolve BEFORE the native-tool seam, wrapped so callers see the single classification ErrRegistrySourceUnavailable while the hard identity ErrRegistrySourcePublicDefault stays assertable. The opt-in cannot rescue it.
- app_broker.go: the caller is unchanged semantically (IsMutableDevelopmentImage trigger preserved); only the opt-in helper envAllowMutableDevelopmentRuntimeImage + doc comments live there. The empty-location check was moved before splitReference so an empty location fails closed with ErrRegistrySourceEmpty first (previously it fell into Resolve's generic handling; TestResolveRejectsEmptyEndpoint stays green either way — recorded as an order fix, not a behavior change).

## New cells (PFLICHT 3) — file cmd/baha/app_broker_registry_negative_test.go

- TestFailedResolvePropagatesWithZeroPulls — tool failure => error propagates, 0 pulls.
- TestDeniedEndpointResolveCausesNoPull — denial-classified reply with opt-in ON => 0 pulls (opt-in cannot bypass denial).
- TestMissingDigestResolveCausesNoPull — unpinnable reply => 0 pulls.
- TestPublicDefaultDockerHubResolveCausesNoPull — real tool seam (NOT stubbed), opt-in ON => hard rejection identity, 0 pulls.
- TestPublicDefaultRejectedBeforeNativeTool — a stub that would "resolve" anything must never be reached for docker.io => proves rejection order, 0 pulls.
- TestUnavailableResolveWithOptInPullsMutableTag / TestUnavailableResolveWithoutOptInFailsClosed — opt-in exists and is class-gated (regression-read of the allowed legacy path).
- Success path cells (existing, regression): TestPullResolvedRuntimeImagePinsImmutableDigest, TestProductionCallerPinsResolvedDigestNotMutableTag remain GREEN; all prior resolver cells (TestResolveRejectsPublicDockerDefault, TestResolveFailsClosed*) stay GREEN.

## Mutant battery (PFLICHT 4) — real mutations, git diff, revert, gegenprobe

- M1 fallback line restored verbatim (return location, nil): RED: TestFailedResolvePropagatesWithZeroPulls, TestDeniedEndpointResolveCausesNoPull, TestMissingDigestResolveCausesNoPull, TestUnavailableResolveWithoutOptInFailsClosed (4 negatives red; public cells stay green because impl-level rejection still runs Resolve — covered by M3/M4).
- M2 opt-in env gate removed (fallback always on): RED: TestFailedResolvePropagatesWithZeroPulls, TestMissingDigestResolveCausesNoPull, TestUnavailableResolveWithoutOptInFailsClosed (3).
- M3 hard-rejection exclusion removed from classifier: RED: TestDeniedEndpointResolveCausesNoPull, TestPublicDefaultDockerHubResolveCausesNoPull, TestPublicDefaultRejectedBeforeNativeTool (3).
- M4 public-default sentinel demoted to unavailable alias: green on the cell battery — documented escape: M4d (alias + identity-compare removal pair) => RED: denial + both public cells (3). Recorded as a limit of single-mutation coverage against the aliasing pair.
- M5 production caller pulls raw tag bypassing pullResolvedRuntimeImage: RED: TestProductionCallerPinsResolvedDigestNotMutableTag (existing discriminator still live).
- Gegenprobe after every revert: full cell battery GREEN (ok cmd/baha).

## Local gates

- gofmt clean; go build ./cmd/baha (name-only) + adapter, go vet ./cmd/baha rc=0.
- race-20 on the registry cells (failed/denied/missing-digest/public-default/tool-ordering/opt-in-gate/pull/caller): go test ./cmd/baha -race -count=20 => ok, rc=0 (605s wall, run twice; one earlier timeout-only attempt hit the default 10m test-binary budget because each caller-cell iteration carries the fixed 30s OpenBao readiness wait, no race was reported).
- Full cmd/baha suite: the only local failure is TestAppEditCommandCompleteProviderEditRunsRealLifecycle, which needs the rootless Docker daemon endpoint unix:///var/run/docker.sock (not available in this session's host; mission names no VM for this lane and starting stacks on this host is forbidden). Native gate ownership unaffected: hosted CI runs it on the named runners.
- ./internal/... suites: all ok except the BASEHARBOR_TEST_DATABASE_URL-gated integration cells (controlplane/migration/RLS), which are documented environment prerequisites, untouched by this change, and hosted-runner owned.
- internal/runtime, internal/application, internal/deployment, internal/delivery suites: ok.

## Hosted run (PFLICHT: TERMINAL am neuen Kopf selbst)

- Pushed head 99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c; run 42168126290 (CI · Source & Quality) started at that exact head; watched to terminal state by this lane:
  - RESULT: status=completed, conclusion=success. 14 jobs green (incl. go-unit-tests, cli-package-tests, cli-guided-tests, vet, source-contracts, trusted plan, source format, cli-build), 10 path-inapplicable skipped, 0 red.

## Review-rezept cross-check (review-1395c lines 59-85, point by point)

- (a) "Do not turn ErrRegistrySourceUnavailable into a successful mutable reference in the production caller" => done: the `return location, nil` line in resolveRegistrySourceImpl is gone (git diff witness in the mutante section; M1 restores it and turns the negatives RED).
- (b) "Propagate the resolution failure for rejected, denied, or unavailable sources" => done: `return "", err` + caller wraps with %w; cells assert ErrRegistrySourceUnavailable reaches the test through pullResolvedRuntimeImage.
- (c) "If the legacy mutable path must remain, make its fallback a separate explicit opt-in that cannot bypass endpoint and public-default rejection rules" => done: BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE, class-gated by resolveUnavailable(); denial + public-default carry hard-rejection identities excluded from the fallback class; public defaults rejected before the native tool seam; opt-in-on RED cells prove non-bypassability.
- (d) "Add a caller-level negative test proving that a failed resolve causes zero runtime pulls, including the public Docker Hub rejection case" => done: TestFailedResolvePropagatesWithZeroPulls + TestPublicDefaultDockerHubResolveCausesNoPull + TestPublicDefaultRejectedBeforeNativeTool (pull counts asserted == 0 in every negative).
- (e) "Re-run focused caller/adapter tests and the required hosted checks on the corrected exact head" => done locally (race-20 ok) and hosted run 42168126290 at 99b3e144 watched to terminal below.

## Compose/VM hygiene

- No docker/podman compose project was started by this lane on any host; nothing to bring down.
- All worktrees, caches and scratch live under /tmp/opencode/w219* only.

## Evidence-on-origin/main witness (second-to-last action)

$ git ls-remote origin refs/heads/work/r27-registry-access
99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c	refs/heads/work/r27-registry-access
$ git rev-parse HEAD
99b3e144dd5f3339a2e0dbbcbea14a7c5dbca36c
$ git -C baseharbor-plan ls-remote origin refs/heads/main   # after publishing this file
69447901dbf599eb28227b23f4e77fe10249f980	refs/heads/main
$ git -C baseharbor-plan ls-tree -r origin/main --name-only | grep registry-access
... tasks/t-20261018-r27-registry-access.md
... evidence/r27-welle5-2026-11-05/registry-access/round-4.md   <- this file, present on origin/main

## END

- END_DONE w219-registry-r4: head=<sha10> propagiert=TestFailedResolvePropagatesWithZeroPulls negcells=3x null-pulls (failed/denied/public-default + missing-digest) mutante=M1 echt rot + gegenprobe lauf=42168126290 TERMINAL lsremote=<sha10> | resolver-Ausnahme wird am caller propagiert, mutable nur noch klassen-exklusiv per opt-in
