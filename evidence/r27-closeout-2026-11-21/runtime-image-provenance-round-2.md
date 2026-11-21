# v0.4.27 runtime image source and attestation reconciliation — round 2

## Exact published artifact

- Current remote `v0.4.27` resolves to source commit `6c40fab4de9a611bc8da2e834417427a83c01ca5` (the remote tag ref is annotated; its dereferenced commit matches).
- Release workflow run [43991839986](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986) is successful, dispatched from workflow source `main@c000c5db2560c471fe84842136e03d6e54d96779`.
- Its reusable `publish-runtime-image / build` job is job `133775188667`, completed successfully on attempt 2.
- The public GHCR OCI index digest is `sha256:5ea2febbab28933588bb87e7b6a0c4edb5a61375c828de0b695952eb7a9c480b`; the raw manifest bytes hash to that exact digest. The index contains amd64 `sha256:a0d2fd23b365268d3848ba305376c9ded9c7ab11ca19a2e1c99feb1ce21c7021` and arm64 `sha256:dd9e1c06cc1b271ecfc0335dd6a0e7df1ce531db6d6d11bf836e07c98c1d896d`, plus one BuildKit attestation manifest for each platform.

## Source binding — what the two attestations prove

- `gh attestation verify oci://ghcr.io/mcpdev80/baseharbor-runtime@sha256:5ea2febbab28933588bb87e7b6a0c4edb5a61375c828de0b695952eb7a9c480b --repo mcpdev80/baseharbor --signer-workflow mcpdev80/baseharbor/.github/workflows/runtime-image.yml --format=json` succeeds with one GitHub SLSA provenance attestation. Its signed subject is exactly the OCI index digest above; its certificate source is `refs/heads/main@c000c5db2560c471fe84842136e03d6e54d96779`, the workflow source that was dispatched.
- Independently fetched each platform's BuildKit provenance statement from its attestation manifest in the same OCI index. Both in-toto layer blobs were SHA-256 checked against their descriptors. Each statement subject equals that platform manifest digest, and each reports `build-arg:COMMIT=6c40fab4de9a611bc8da2e834417427a83c01ca5` and BuildKit `vcs.revision=6c40fab4de9a611bc8da2e834417427a83c01ca5`.
- The release run log also records the input ref/version `v0.4.27`, the checked-out/build commit `6c40fab4de9a611bc8da2e834417427a83c01ca5`, and published digest `sha256:5ea2febbab28933588bb87e7b6a0c4edb5a61375c828de0b695952eb7a9c480b`. The GitHub-signed attestation and BuildKit statements are tied together because the signed subject is the root index whose content-addressed descriptors include those platform attestation manifests.

## Remaining discrepancy — do not certify it away

- The image metadata label `org.opencontainers.image.revision` is `c000c5db2560c471fe84842136e03d6e54d96779`, while the binary, BuildKit `vcs.revision`, and build argument identify packaged source commit `6c40fab4de9a611bc8da2e834417427a83c01ca5`.
- OCI defines `org.opencontainers.image.revision` as the source-control revision identifier for the packaged software ([OCI Image Spec](https://github.com/opencontainers/image-spec/blob/main/annotations.md)). It is therefore a real published metadata mismatch, not the BuildKit source mismatch originally suspected. Do not rewrite the immutable `v0.4.27` image tag. Reconcile this through an explicitly versioned follow-up image/release (or an owner-approved exception) before accepting full artifact metadata verification.
- The artifact and all four version channels are otherwise verified in `tasks/t-20261017-release-0-4-27-verify.md` and its round-1 audit. The v0.4.27 release stages also remain sequenced behind the still-active release-scope card 0427-189; its required CI gate is not green. Card 0427-191 is now accepted, so it is no longer a current blocker.

## Decision

The earlier “signed source is only workflow-dispatch main” wait finding is refined: signed GitHub provenance authenticates the release workflow and exact image index, while the embedded per-platform BuildKit provenance identifies the packaged tag commit. That resolves the source-binding question. Keep 0427-010 waiting because the published OCI revision label is wrong and because its publish predecessor / v0.4.27 release chain still cannot be accepted while 0427-189 remains active.
