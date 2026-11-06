# round-2 — artifact resolution registry-priority fix (card t-20261018-r27-artifact-resolution)

- Lane: w270 · Coordinator session: ec2254ac · Model: worker-flash
- Card: t-20261018-r27-artifact-resolution (RUNDE 2, PR #1406, urteil act-1406a REJECT)
- Repo: mcpdev80/baseharbor · branch work/r27-artifact-resolution (one candidate, no second branch)
- Prior head: 746afe6d89dfd40811d801409140414047d56059 · New head: 9ee857387c333131ec9e1c0f42839736314bab4b

## PLAN

- Read mission + act-1406a.md verdict + round-1 akte before acting (done; akte was found locally under evidence/r27-welle5-folge-2026-11-06/artifact-resolution/act-1406a.md).
- Cut an isolated worktree (workers zone /tmp/opencode/w270-wt/repo) from the exact remote branch head 746afe6d89d; attest bases.
- Merge develop 8bda98c1cd3 into the candidate branch (no second PR, one candidate per chain).
- Red-first cell for exactly the blocker case: registry-ok + declared build => artifact=registry (use-existing); capture RED transcript.
- Fix the production resolver line; re-run cell GREEN.
- Causal mutant at the real production resolver line in an isolated copy: RED+GREEN transcripts + file hashes.
- Re-run all round-1 green focused cells at the new head + full cmd/baha package; prove the one env failure pre-exists.
- Push to the named branch only (ls-remote before/after), watch hosted run to TERMINAL (no reruns, .github untouched).
- Commit fix to baseharbor, akte to baseharbor-plan origin/main, post END to ec2254ac.

## Base attestation

Branch/worktree cut point (existing candidate head, the only branch this round continues — AGENTS 3.8 one-candidate rule):

    $ git ls-remote origin refs/heads/work/r27-artifact-resolution   (before push)
    746afe6d89dfd40811d801409140414047d56059	refs/heads/work/r27-artifact-resolution

    $ git ls-remote origin refs/heads/develop
    8bda98c1cd34a984810a0a0ee2d9fe4085b3933a	refs/heads/develop

Ancestry proofs at the final head 9ee857387c3:

    $ git merge-base --is-ancestor 746afe6d89dfd40811d801409140414047d56059 HEAD && echo OLDHEAD-ANCESTOR-OK
    OLDHEAD-ANCESTOR-OK
    $ git merge-base --is-ancestor 8bda98c1cd34a984810a0a0ee2d9fe4085b3933a HEAD && echo DEVELOP-ANCESTOR-OK
    DEVELOP-ANCESTOR-OK

Own commits (`git log --oneline origin/develop..HEAD` at push time — ONLY this card's commits, no foreign candidate carried):

    9ee85738 fix(cmd/baha): r27 artifact resolution round 2 — resolved registry artifact takes priority over a declared build
    9ab3885d Merge develop 8bda98c1cd3 into work/r27-artifact-resolution (round 2 base refresh)
    746afe6d feat(cmd/baha): r27 artifact resolution — resolve source/version to one concrete immutable artifact

The merge commit 9ab3885d brings develop (#1397 landed) into the chain; the first-parent list contains nothing else foreign.

## Blocker and correction (mission w270, act-1406a finding 1)

Blocker verbatim: "registry_success plus declared build selects native-build" — when the registry artifact resolves successfully but the manifest additionally declares a build, the resolver chose native-build instead of the registry artifact. Root cause: in resolveRenderedWorkloadArtifacts the registry-success branch stored the resolved identity but left hasBuild true, and resolveArtifactServiceDecision(CheckoutBuild, true, resolved) returns native-build before considering the resolved artifact.

Correction (production line, cmd/baha/application_artifact_resolution.go, registry-success branch): set hasBuild = false when the registry resolver succeeds, so a verifiable resolved immutable artifact takes priority; the declared build remains the route only when no existing artifact is usable (registry-unavailable + store-absent). The local-store branch already cleared hasBuild; resolution order is now registry first, then local store, checkout-build only explicitly and only when neither source is available. Hard denials, public-default rejection, digest validation and store ambiguity stay fail-closed (unchanged branches verified by the re-run cells below).

## Red-first cell

New cell TestResolveRenderedWorkloadArtifactsCheckoutMode/successfully_resolved_registry_artifact_wins_over_declared_build: registry resolver returns artifactRepo@digestB for an image-plus-build service; asserts Action=use-existing, exact digest identity, and that no native image-tool call happens. Written and run BEFORE the fix:

    $ go test ./cmd/baha -run '^TestResolveRenderedWorkloadArtifactsCheckoutMode$/^successfully_resolved_registry_artifact_wins_over_declared_build$' -count=1 -v
    === RUN   TestResolveRenderedWorkloadArtifactsCheckoutMode/successfully_resolved_registry_artifact_wins_over_declared_build
        application_artifact_resolution_test.go:502: a successfully resolved registry artifact must win over the checkout build: {Service:api Action:native-build Identity:{Repository:registry.example.invalid/org/app Digest:sha256:23456789abcdef...01 Requested:stable} Requested:stable}
    --- FAIL: TestResolveRenderedWorkloadArtifactsCheckoutMode/successfully_resolved_registry_artifact_wins_over_declared_build (0.00s)
    FAIL

After the production fix at the same head:

    --- PASS: TestResolveRenderedWorkloadArtifactsCheckoutMode/successfully_resolved_registry_artifact_wins_over_declared_build (0.00s)
    PASS

## Causal mutant (production resolver line, isolated copy)

Isolated copy: /tmp/opencode/w270-wt/repo (worktree zone per mission; caches /tmp/opencode/w270-wt). Mutant = the fix line `hasBuild = false` in the registry-success branch of the real production resolver function resolveRenderedWorkloadArtifacts reverted (i.e. mutant = pre-fix production behavior at the changed line). No test-side changes in the mutant run. The full ordered sequence ran on the isolated copy; the file is byte-identical to the pushed candidate afterwards (`git status --porcelain` empty).

    SOURCE_ORIGINAL cmd/baha/application_artifact_resolution.go sha1=a70aa9bce5fe910c423bde95adc796b08bce9cff
    $ go test ./cmd/baha -run '^TestResolveRenderedWorkloadArtifactsCheckoutMode$/^successfully_resolved_registry_artifact_wins_over_declared_build$' -count=1 -v
    --- PASS   (GREEN on the fixed production source)

    SOURCE_MUTANT  cmd/baha/application_artifact_resolution.go sha1=65809f4fb2b2a4d9ae1c3a0efd892c8798aa6734
    $ go test ./cmd/baha -run '^TestResolveRenderedWorkloadArtifactsCheckoutMode$/^successfully_resolved_registry_artifact_wins_over_declared_build$' -count=1 -v
    === RUN   TestResolveRenderedWorkloadArtifactsCheckoutMode/successfully_resolved_registry_artifact_wins_over_declared_build
        application_artifact_resolution_test.go:502: a successfully resolved registry artifact must win over the checkout build: {Service:api Action:native-build Identity:{Repository:registry.example.invalid/org/app Digest:sha256:23456789abcdef...01 Requested:stable} Requested:stable}
    --- FAIL: TestResolveRenderedWorkloadArtifactsCheckoutMode/successfully_resolved_registry_artifact_wins_over_declared_build (0.00s)
    FAIL        (RED on mutant, production line causal)

    SOURCE_RESTORED cmd/baha/application_artifact_resolution.go sha1=a70aa9bce5fe910c423bde95adc796b08bce9cff
    $ go test ./cmd/baha -run '^TestResolveRenderedWorkloadArtifactsCheckoutMode$/^successfully_resolved_registry_artifact_wins_over_declared_build$' -count=1 -v
    --- PASS: TestResolveRenderedWorkloadArtifactsCheckoutMode/successfully_resolved_registry_artifact_wins_over_declared_build (0.00s)
    PASS        (GREEN restored; committed source hash a70aa9bc == SOURCE_RESTORED)

Hash pair: 65809f4fb2b2a4d9ae1c3a0efd892c8798aa6734 (mutant, RED) / a70aa9bce5fe910c423bde95adc796b08bce9cff (production, GREEN).

Mutated production line (resolveRenderedWorkloadArtifacts, registry-success branch — the line the fix touches, shown as committed):

```go
			endpoint, err := resolveRegistrySource(ctx, location, requested)
			if err == nil {
				repository, digest := splitDigestReference(endpoint)
				if !validImageDigest(digest) {
					return nil, fmt.Errorf("%w: service %q: resolver returned %q without an immutable digest", ErrArtifactResolutionAmbiguous, service, endpoint)
				}
				resolved.Repository, resolved.Digest = repository, digest
				// A successfully resolved registry artifact is the existing
				// artifact the card puts first: a declared build must never
				// override it into native-build (act-1406a blocker).
				hasBuild = false
				break
			}
```

The mutant removes only `hasBuild = false` (plus its comment); `git show HEAD:cmd/baha/application_artifact_resolution.go | sha1sum` reproduces a70aa9bc, so the hashes are of the committed candidate, not a scratch copy.

## Round-1 green cells re-run at the new head (SHA change => mandatory re-check)

    $ gofmt -l cmd/baha            → (empty)
    $ go vet ./cmd/baha            → VET-OK
    $ go test ./cmd/baha -run 'TestArtifactResolution|TestResolveRenderedWorkloadArtifacts|TestResolveLocalRegistryArtifact|TestLocalArtifactAvailable|TestSplitArtifactResolutionPin|TestNativeArtifactImageTool|TestResolveWorkloadArtifact|TestResolveAndPull|TestRepositoryWorkloadArtifactState|TestLoadRepositoryWorkloadArtifactState|TestValidateWorkloadArtifact|TestResolveArtifactServiceDecision|TestPrepareRepositoryWorkloadArtifactResolution|TestRebuildChangedServices' -count=1 -v
    → 56 PASS cells, 0 FAIL, 0 SKIP (round-1's 55 plus this round's new priority cell)

Full package (`go test ./cmd/baha -count=1` at 9ee85738): one FAIL, environment-only:

    --- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle
        app_edit_apply_test.go:947: application preflight failed: selected Docker endpoint unix:///var/run/docker.sock is unavailable; ... no fallback to System Docker

Proven pre-existing: `application_artifact_resolution.go` exists in no develop revision (`git show origin/develop:cmd/baha/application_artifact_resolution.go` → "exists on disk, but not in 'origin/develop'"), and the same test fails identically in the untouched round-1 base worktree at 5e4fde71 (workers/w263-wt/base, an ancestor of develop) with none of this card's files present (`ls: cannot access cmd/baha/application_artifact_resolution.go`). Same failure signature as round-1 akte. Docker daemon tests were NOT run from this host (owner directive); no VMs named by this mission; nothing compose-related started => nothing to tear down.

## Candidate and hosted CI

- Push witness (before/after, single push, named branch only):

    $ git ls-remote origin refs/heads/work/r27-artifact-resolution
    746afe6d89dfd40811d801409140414047d56059	refs/heads/work/r27-artifact-resolution
    To https://github.com/mcpdev80/baseharbor.git
       746afe6d..9ee85738  HEAD -> work/r27-artifact-resolution
    $ git ls-remote origin refs/heads/work/r27-artifact-resolution
    9ee857387c333131ec9e1c0f42839736314bab4b	refs/heads/work/r27-artifact-resolution

- No second branch was pushed. ls-remote sweep before and after the push shows exactly one remote candidate:

    $ git ls-remote origin | grep -c artifact
    1

- The local branch name work/r27-artifact-resolution-new from round 1 exists only in this host's root checkout as another worktree's checked-out name; it was never pushed, touched or extended by this lane (remote sweep above proves count 1).
- Diff vs develop (git diff --shortstat origin/develop...HEAD): 4 files changed, 1533 insertions, 0 deletions — the same 4 files as round 1 (act-1406a finding 4 confirmed the write-set).
- Run 42297344340 "CI · PR #1406", pull_request, head 9ee857387c333131ec9e1c0f42839736314bab4b — TERMINAL completed/success. Canonical: https://github.com/mcpdev80/baseharbor/actions/runs/42297344340- `gh pr checks 1406`: `PR Selected Checks` pass (job 128170168872); remaining lanes pass or skipping (runtime/HA/release lanes not selected for this diff); 0 failing. PR OPEN, MERGEABLE at head 9ee857387c3. No reruns or dispatches were triggered by this lane.

## repo-rule compliance

- Exactly one candidate branch and one PR; the mission's named branch work/r27-artifact-resolution is the only push target; no .github/** edits; no reruns, no workflow_dispatch, no CI-config changes; no subagents; no work in the root checkout (the root's stale local branch copy is another lane's worktree — untouched); worktree + caches under /tmp/opencode/w270-wt (mission zone); evidence only in baseharbor-plan; commits carry no AI trailer.
- Write-set honored: only cmd/baha/application_artifact_resolution.go (+4 prod lines) and cmd/baha/application_artifact_resolution_test.go (+22 test lines); no other files.
- Docker/podman: no containers or compose projects started on this host; only scripted in-process test fakes.
- Fail-closed semantics preserved: ambiguity sentinels and digest validation untouched; mutant evidence shows the causal line; genuine multi-source ambiguity (no registry, no store) still routes per round-1 cells which all passed at the new head.

## Status

END_DONE w270-artifact-registry-prio: head=9ee857387c prio_zelle=ROT->GRUEN mutante=65809f4f/a70aa9bc lauf=42297344340 TERMINAL lsremote=9ee857387c akte=evidence/r27-welle5-folge-2026-11-06/artifact-resolution/round-2.md main | Registry-artefakt hat Prio vor der Build-Deklaration; echte Mehrdeutigkeit bleibt fail-closed; develop 8bda98c1cd3 gemerged; 56 gruene Zellen am neuen Kopf.

## Evidence push witness

    $ git push origin main   (baseharbor-plan)
    To https://github.com/mcpdev80/baseharbor-plan.git
       4bf6a084..a244e2b0  main -> main

    $ git ls-tree origin/main --name-only evidence/r27-welle5-folge-2026-11-06/artifact-resolution/
    evidence/r27-welle5-folge-2026-11-06/artifact-resolution/round-2.md

## VM/compose hygiene

No VMs named by this mission; no docker/podman/compose projects started anywhere by this lane (scripted in-process fakes only) => nothing to bring down. ps-witness at END:

    $ docker ps -q | wc -l
    0
    (PS-WITNESS: 0 containers on this host; lane started none)
