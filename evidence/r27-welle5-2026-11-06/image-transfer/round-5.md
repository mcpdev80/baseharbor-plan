# Image transfer adapter fix — round 5

- Role: CODEX-WORKER; coordinator: `841e7734`.
- Mission: `coordinator/missions/codex-worker-1402-adapterfix.txt`.
- Candidate: PR #1402, branch `work/r27-image-transfer`, initial head `c8272e9f3d04654fb711fbc5a716eb538bdba6dd`.
- Scope: correct the existing native image inspect adapter for Docker and Podman 5.7, integrate current `develop`, run focused and locked host checks, publish the evidence.

## PLAN

1. Confirm exact PR branch/head, task contract, previous runtime transcripts, and current VM lock owners.
2. Reproduce the Podman 5.7 inspect failure against the initial candidate; retain Docker's passing behavior as a countercheck.
3. Make the smallest runtime-aware adapter and test change; ensure exact executable names and format strings are exercised.
4. Merge the latest `origin/develop` into this same PR branch, run focused local checks, and push normally.
5. Run Podman and Docker host smokes one at a time under `vm-lock`; record image/container cleanup.
6. Observe the hosted run for the final SHA through terminal status and complete this evidence before handoff.

## Initial state

- PR #1402 is open and mergeable at `c8272e9f3d04654fb711fbc5a716eb538bdba6dd`; prior hosted run 42213910864 succeeded at that old head.
- `origin/develop` is `78e78e66c5a809ad17482d015539dcf3940d5f9b`; the candidate does not yet contain that head.
- `vm-lock.sh status` at mission start: `baha-docker` held by `w237`; `baha-podman` held by `w243`. No host operation was attempted.
- At 2026-11-06T13:44Z, both `w237-devenv-smoke` and `w243-remote-control-r2` were still busy. Separate `vm-lock.sh claim` attempts returned `BUSY` / exit 3 for Podman (owned by w243) and Docker (owned by w237); no SSH or other VM command was run. A QUESTION asking the coordinator to signal the first released host was posted to 841e7734.

## Change

At `1c024d11bd6d0c82062902b7066305bf1d582be5`, `RuntimeImageTransferSource` now requires an explicit Docker or Podman runtime. The adapter selects the native executable and digest format for that runtime, and uses the common top-level `{{.Architecture}}|{{.Os}}` platform format. Target verification selects from `RuntimeProvider.Kind()` and rejects unsupported runtimes. Tests cover the source and target adapter command lines for Docker and Podman 5.7 and fail-closed unsupported-runtime behavior. Only `cmd/baha/application_image_transfer.go` and its matching test changed.

## Red-first and local checks

- Before the correction, `TestPodman57ImageInspectTemplatesResolve` failed against the original image-transfer source from c827 (unchanged at the develop-integration checkpoint): the executed command was `podman image inspect --format {{.RepoDigests[0]}} ...`; the test's Podman 5.7 contract rejected that unsupported template. Round-3 host evidence independently records Podman 5.7 rejecting the same exact old format.
- After the correction, focused adapter tests passed:
  `go test ./cmd/baha -run '^(TestPodman57ImageInspectTemplatesResolve|TestDockerImageInspectTemplatesResolve|TestImageTransferRejectsUnsupportedRuntime|TestRuntimeImageTransferTargetUsesNativeInspectFormats|TestImageTransfer.*|TestSplitDigestReference)$' -count=1 -timeout=60s` → `ok`.
- CLI build succeeded with `go build -buildvcs=false -o /home/marcel/dev/baseharbor-ecosystem/workers/w245-cache/baha ./cmd/baha`.
- A full `go test ./cmd/baha -count=1 -timeout=120s` did not complete: it timed out in unrelated `TestAppEditApplyReview918RealLifecycleReturnsAfterFacts` while waiting in `recordDeploymentBeforeMutation` (`cmd/baha/deployment_record.go:209`). No rerun was made.
- The first Go build attempt failed because `/tmp` returned `disk quota exceeded`; GOCACHE and GOTMPDIR were moved to workspace rootfs `workers/w245-cache`, with GOMODCACHE retained at `/tmp/opencode/w245-gomodcache`.
- Hosted run 42226452453 completed `success` at the exact final head `1c024d11bd6d0c82062902b7066305bf1d582be5`. `PR Selected Checks` succeeded (job 127925327338); `go-unit-tests` succeeded (job 127921170653); CLI package tests, CLI build, go build, go vet, source contracts, formatting and focused Python checks succeeded. Targeted HA Docker and Podman jobs were skipped, so they do not substitute for the locked host smokes.

## Locked Podman 5.7 adapter smoke

- Acquired only `baha-podman` with `vm-lock.sh claim baha-podman w245-codex` at 13:47:34Z; Docker remained owned by w237. Podman reported hostname `baha-runner-podman`, Podman Engine 5.7.0, linux/amd64. The image `quay.io/libpod/alpine:latest` was absent before this lane's pull; `podman ps -aq` was empty.
- The candidate adapter itself was called by temporary harness `scripts/host_smoke_test.go`, copied temporarily to `cmd/baha/application_image_transfer_host_smoke_test.go`: `RuntimeImageTransferSource.Resolve` ran the native Podman inspect commands over SSH, `RuntimeImageTransferTarget.Copy` pulled the immutable digest, and `Verify` inspected the transferred identity. Command: `BH_IMAGE_TRANSFER_SMOKE_HOST=baha-podman BH_IMAGE_TRANSFER_SMOKE_RUNTIME=podman go test ./cmd/baha -run '^TestRuntimeImageTransferRemoteHostSmoke$' -count=1 -v -timeout=4m`.
- Result: `PASS`; source `quay.io/libpod/alpine:latest`; immutable target `quay.io/libpod/alpine@sha256:634a8f35b5f16dcf4aaa0822adc0b1964bb786fca12f6831de8ddc45e5986a00`; digest matched; platform `amd64/linux`; containers before/after empty.
- Teardown: `podman image rm quay.io/libpod/alpine:latest` returned `Untagged`; subsequent inspect returned `image not known`; subsequent `podman ps -aq` remained empty. Released `baha-podman` lock at 13:50Z. The temporary test copy in the product worktree was removed; its script remains in this evidence directory.

## Locked Docker adapter smoke

- After w237 became idle and its Docker lock was free, acquired only `baha-docker` with `vm-lock.sh claim baha-docker w245-codex` at 13:52:55Z. Hostname `baha-runner-docker`; Docker 29.8.1. `quay.io/libpod/alpine:latest` was absent and `docker ps -aq` was empty before the smoke.
- Called the same candidate adapter harness (copied temporarily to `cmd/baha/application_image_transfer_host_smoke_test.go`) with `BH_IMAGE_TRANSFER_SMOKE_HOST=baha-docker BH_IMAGE_TRANSFER_SMOKE_RUNTIME=docker go test ./cmd/baha -run '^TestRuntimeImageTransferRemoteHostSmoke$' -count=1 -v -timeout=4m`. Resolve, immutable digest pull, and Verify all ran through the production adapter over SSH.
- Result: `PASS`; resolved target `quay.io/libpod/alpine@sha256:fa93b01658e3a5a1686dc3ae55f170d8de487006fb53a28efcd12ab0710a2e5f`; digest matched; platform `amd64/linux`; container list stayed empty.
- Teardown: `docker image rm quay.io/libpod/alpine:latest` removed the tag and digest image; subsequent inspect reported `No such image`; subsequent `docker ps -aq` remained empty. Released the Docker lock at 13:54Z. Removed the temporary product-worktree test copy; the harness remains in this evidence directory.
- Podman and Docker pulled the mutable `latest` tag at different times and resolved different digests. Each independent smoke then copied and verified its own immutable digest on the same host; this is not a cross-host content-equality claim.

## Five-head checkpoints

| Checkpoint | Exact head | Result |
|---|---|---|
| Initial PR candidate | `c8272e9f3d04654fb711fbc5a716eb538bdba6dd` | Podman 5.7 red-first reproduced |
| Latest develop integrated | `f42e9da83ffa40a60db3e265193513d4f39a8649` | Conflict-free merge of `78e78e66c5a809ad17482d015539dcf3940d5f9b` |
| Adapter correction committed | `1c024d11bd6d0c82062902b7066305bf1d582be5` | Focused Docker/Podman source and target tests green |
| Remote PR branch | `1c024d11bd6d0c82062902b7066305bf1d582be5` | Normal fast-forward push; no second PR |
| Hosted final candidate | `1c024d11bd6d0c82062902b7066305bf1d582be5` | Run 42226452453 terminal success; PR Selected Checks success |

## Five-head evidence table

| Stage | Candidate head | Podman 5.7 | Docker | Evidence |
|---|---|---|---|---|
| Before fix | `c8272e9f3d04654fb711fbc5a716eb538bdba6dd` | red-first test reproduced old template rejection | prior round-3 host command passed manually | pre-fix test output above |
| After adapter fix | `1c024d11bd6d0c82062902b7066305bf1d582be5` | local and Podman 5.7 host adapter cells green | local adapter cell green | focused Go test and Podman transcript above |
| After develop integration | `f42e9da83ffa40a60db3e265193513d4f39a8649` | no smoke at intermediate merge-only head | no smoke at intermediate merge-only head | merge commit recorded |
| Final pushed candidate | `1c024d11bd6d0c82062902b7066305bf1d582be5` | real Podman 5.7 adapter smoke green | real Docker 29.8.1 adapter smoke green | branch ls-remote confirmed |
| Hosted terminal result | `1c024d11bd6d0c82062902b7066305bf1d582be5` | n/a | n/a | run 42226452453 terminal success; PR Selected Checks success |

## Mutation / discrimination evidence

Mutation witness: replacing the Podman repo-digest format with the previous `{{.RepoDigests[0]}}` makes `TestPodman57ImageInspectTemplatesResolve` fail before the digest can be parsed; restoring the native `{{(index .RepoDigests 0)}}` makes that same positive cell pass. The old source failure and corrected test output are recorded above. The Docker cell separately requires executable `docker` and the Docker format.

## Repository rule compliance

No VM work without an acquired `vm-lock`; no foreign lock was released. Changes stay on the existing PR branch. No workflow files or additional PRs are in scope. Podman and Docker locks were acquired and released separately. The latest lock check shows only `baha-podman` held by w242; this lane performed no operation on that host after releasing it.

## Publication witness

Pending `origin/main` `ls-tree` witness.
