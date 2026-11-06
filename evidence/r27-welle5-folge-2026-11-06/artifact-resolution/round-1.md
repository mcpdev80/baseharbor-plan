# round-1 — artifact resolution (card t-20261018-r27-artifact-resolution)

- Lane: w258 · Coordinator session: ec2254ac (coord 841e7734) · Model: worker-flash
- Card: t-20261018-r27-artifact-resolution (claimed by w258, state active)
- Repo: mcpdev80/baseharbor · PR #1406 against develop · head 746afe6d89dfd40811d801409140414047d56059
- Source issue: baseharbor#777 · Release: v0.4.27

## PLAN

- Read mission, card, release plan, baseharbor/AGENTS.md; claim card via plan.py (claim already on plan main).
- Fetch develop; record ls-remote witness; cut work/r27-artifact-resolution from exact develop head 5e4fde7177ea020de39b117f6d89cfa8f7c62be2; prove ancestry.
- Implement artifact resolution in card scope: bounded builder/artifact realization adapter plus apply-path wiring (a standalone unused adapter is not complete).
- Write focused positive/negative regression cells; run them and the full affected package; record transcripts.
- Push exactly one candidate branch; open one PR against develop; watch the hosted selected checks on the final head to TERMINAL (ownes Run, no reruns).
- Write this akte, commit+push baseharbor-plan origin/main, post END to ec2254ac.

## Worktree wipe and recovery (git-log witnesses)

The first implementation session worked in /tmp/opencode/w258-wt/repo, which an orchestrator tmp-sweep deleted before its first commit; the loss was detected mid-session and the coordinator directed a persistent-zone rewrite. Recovery audit, this host's baseharbor object database:

- No earlier candidate existed anywhere: `git ls-remote origin` showed no `*artifact*` branch before the push (grep count 0); both local `work/r2*artifact*` branches pointed at pristine develop 5e4fde71; `git stash list` empty; `git fsck --lost-found` → 41 dangling commits, none containing `application_artifact_resolution` (`git ls-tree -r` sweep); the two dangling blobs for that path (`de8d7ead` adapter, `14bc7932` tests) are reachable from exactly one commit — `746afe6d`, this push (`git log --all --find-object` on both blobs) — and their SHA-1 digests match the files under HEAD byte-for-byte (`git cat-file blob | sha1sum` == `sha1sum`), so they are this commit's own objects, not survivor content. The rewritten files therefore contain zero recovered bytes; they were written from session context plus a live read of the reused authorities (`resolveRegistrySource`, `registrySourceExec`, `runTransfer`, `imageTransferCLIFor`, `splitDigestReference`, `pullRuntimeImage`, `parseRepositoryBuildDefinition`).
- New persistent worktree: /home/marcel/dev/baseharbor-ecosystem/workers/w263-wt/repo (branch-local name `work/r27-artifact-resolution-new` because the root checkout holds the card branch name; pushed under the card name; caches under /home/marcel/dev/baseharbor-ecosystem/workers/w263-wt).

## Base attestation

    $ git ls-remote origin refs/heads/develop   (before push)
    5e4fde7177ea020de39b117f6d89cfa8f7c62be2	refs/heads/develop

    $ git ls-remote origin | grep -c artifact   (before push)
    0

Branch cut from exactly that SHA; ancestry proof:

    $ git merge-base --is-ancestor 5e4fde7177ea020de39b117f6d89cfa8f7c62be2 HEAD && echo ANCESTOR-OK
    ANCESTOR-OK

Own commits only (`git log --oneline origin/develop..HEAD` at push time):

    746afe6d feat(cmd/baha): r27 artifact resolution — resolve source/version to one concrete immutable artifact

## Candidate and CI

- Push witness: `git ls-remote origin refs/heads/work/r27-artifact-resolution` → 746afe6d89dfd40811d801409140414047d56059.
- PR #1406 against develop, opened draft, marked ready (single candidate; no other branch pushed). Diff: 1507 additions, 0 deletions, 4 files (git diff --shortstat vs base 5e4fde71).
- Run 42293297231 "CI · Source & Quality", pull_request, head 746afe6d — TERMINAL success (9m46s). Selected checks: 14 pass, 0 fail, 11 skipping (runtime/HA/release lanes not selected for this diff). Canonical: https://github.com/mcpdev80/baseharbor/actions/runs/42293297231
- Run 42293285254 (10s earlier, same head, event pull_request): cancelled by GitHub's same-PR duplicate-workflow suppression when the ready event re-triggered the run — no rerun was dispatched by the lane (AGENTS: "Resolve queue/concurrency blockers before launching replacement runs"); the surviving run is the sole qualification record.

## Local verification

Commands (worktree /home/marcel/dev/baseharbor-ecosystem/workers/w263-wt/repo, go1.26.8 linux/amd64):

    $ gofmt -l cmd/baha            → (empty)
    $ go vet ./cmd/baha            → VET-OK
    $ go test ./cmd/baha -run '<focused artifact selectors>' -count=1 -v
    → 55 PASS cells, ok github.com/mcpdev80/baseharbor/cmd/baha 0.064s

Focused selectors: TestArtifactResolution, TestResolveRenderedWorkloadArtifacts, TestResolveLocalRegistryArtifact, TestLocalArtifactAvailable, TestSplitArtifactResolutionPin, TestNativeArtifactImageTool, TestResolveWorkloadArtifact, TestResolveAndPull, TestRepositoryWorkloadArtifactState, TestLoadRepositoryWorkloadArtifactState, TestValidateWorkloadArtifact, TestResolveArtifactServiceDecision, TestPrepareRepositoryWorkloadArtifactResolution, TestRebuildChangedServices.

Cell transcripts (name → what it proves):

- TestArtifactResolutionSourceLocation (6 table rows): image reference → repository/requested-channel/digest-pin decomposition incl. tag@digest combined form.
- TestSplitArtifactResolutionPin / TestNativeArtifactImageTool: digest-reference split; docker vs podman inspect templates; unsupported runtime fails closed.
- TestResolveArtifactServiceDecisionMatrix (8 cells): pure selection core — existing mode requires an immutable digest and rejects a checkout-build fallthrough; checkout mode routes declared builds, prefers resolved images, rejects imageless/buildless; unknown mode is ambiguous.
- TestResolveLocalRegistryArtifact (3 cells): native inspect reply carries the immutable identity; missing image and mutable-tag reply fail closed.
- TestLocalArtifactAvailable (4 cells): two-call probe (`image exists` then repo-digest `image inspect`); absent is quiet absence; conflicting digests are ErrArtifactResolutionAmbiguous; exists-but-uninspectable is absent, not guessed.
- TestResolveRenderedWorkloadArtifactsExistingMode (7 cells): registry-first with zero local calls; local store wins over declared build; neither-source fail-closed; endpoint denial never papered over by the store; docker.io public default rejected; checkout build rejected in existing mode; service missing from the rendered model is ambiguous.
- TestResolveRenderedWorkloadArtifactsAmbiguousLocalStore (2 modes): conflicted store fails closed in every mode, no arbitrary winner.
- TestResolveRenderedWorkloadArtifactsCheckoutMode (5 cells): pure build routes native; available artifact beats build; unavailable artifact with build routes native; bare local name probes the store without the registry (no false public-default trip); imageless/buildless ambiguous.
- TestResolveWorkloadArtifact (2 cells) / TestResolveAndPullWorkloadArtifact (4 cells): callable seam returns digest-only identity; resolve failure means zero pulls; the BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE opt-in stays class-gated (unavailable class only, denial pulls nothing).
- TestPrepareRepositoryWorkloadArtifactResolution (4 cells): buildless model needs no plan (pure-image apply unchanged); checkout plan routes and proves the context; imagined build context fails closed; broken Compose file set fails closed.
- TestValidateWorkloadArtifactBuildContext (5 assertions) / TestValidateWorkloadArtifactComposeFiles (4 assertions): build must be real and inside the repository; file set must exist and start at the workload Compose file.
- TestRepositoryWorkloadArtifactStatePersistence / TestLoadRepositoryWorkloadArtifactStateAbsentFile: state is 0600, holds only repository@digest/action/requested-channel provenance, never the secret-bearing source-identity field; absent file loads empty.
- TestRebuildChangedServicesArtifactGate: apply-path wiring proof — a fingerprint-changed service whose plan says use-existing never reaches compose build; only the native-build service rebuilds and is recorded in buildChanged. TestRebuildChangedServicesWithoutPlanIsUnchanged: no plan means byte-identical pre-adapter behavior.

Full package run (`go test ./cmd/baha -count=1`): one FAIL, environment-only:

    --- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle
        application preflight failed: selected Docker endpoint unix:///var/run/docker.sock is unavailable; start its rootless daemon or correct the Target endpoint/context; no fallback to System Docker

Proven pre-existing: the same test fails identically on a pristine 5e4fde71 worktree (workers/w263-wt/base) with none of this card's files present. No VMs were started; no compose projects were brought up by this lane (nothing to tear down).

## Design mapped to acceptance

- Use existing OCI images/releases first when selected: registry endpoint via the accepted resolveRegistrySource authority (registry-access/native-auth predecessors), then the local store via native `docker/podman image exists/inspect` (image-transfer predecessor's tooling); a verifiably available artifact wins even over a declared build.
- Current-checkout mode only invokes existing Docker/Compose or Podman build machinery: the adapter never builds — it routes native-build actions and proves the rendered build context/Dockerfile exists inside the repository first; the actual build stays in compose.BuildProjectFilesSelectedProgress (app_workload_apply.go), gated by the artifact plan.
- Fail-closed ambiguity: distinct sentinels ErrArtifactResolutionAmbiguous / ErrArtifactResolutionUnavailable; conflicting local digests, contradictory resolver replies, missing rendered services, imagined build contexts, unsupported modes all realize nothing.
- Release/promote cannot silently build/replace/use a mutable tag: existing mode structurally rejects build fallthrough and any digestless identity; pulls take only repository@digest; denial and public-default classes bypass nothing, also behind the dev opt-in.
- Retain only owner/provenance metadata: workload-artifact-resolutions.json (0600) records action + repository@digest + requested channel; endpoints, tool output and the source-identity Requested field are never persisted.
- Standalone-unused rule honored: wired into prepareRepositoryWorkloadExecution + rebuildChangedServices; report-registry-file overlap with landed #1401 checked — none needed (no orgconfig or registry-file edits).

## repo-rule compliance

- Exactly one candidate branch and one PR; no .github edits; no workflow or CI-config changes; no second push after the qualification run; no reruns or dispatches; no subagents; no work in the root checkout (isolated worktree under the persistent workers zone per coordinator directive); caches under the lane worktree; nothing started in compose/VMs.
- Card write-set honored: cmd/baha/app_workload_build.go untouched (its parseRepositoryBuildDefinition authority reused); bounded adapter + tests new (application_artifact_resolution.go / _test.go); minimal reuse additions in application_image_transfer.go (2 helpers, 0 deletions) and apply-path wiring in app_workload_apply.go.
- Standards boundary: native tools only, no private registry/build/pipeline framework, no new mandatory registry; least-privilege state files 0600.
- Evidence lives only in baseharbor-plan; commits carry no AI trailer (repo rule).

## Status

END_DONE w258-artifact-resolution: head=746afe6d89 pr=1406 lauf=42293297231 TERMINAL success lsremote=746afe6d89 akte=evidence/r27-welle5-folge-2026-11-06/artifact-resolution/round-1.md main | Artifact-Resolution ist implementiert und verdrahtet: Quell-/Versionsauswahl loest sich in ein konkretes unveraenderliches Artefakt, Mehrdeutigkeit fail-closed, 55 grune Zellen, hosted CI successful on final head.

## Evidence push witness

    $ git push origin main   (baseharbor-plan)
    To https://github.com/mcpdev80/baseharbor-plan.git
       09caf2f6..d752d31e  main -> main
