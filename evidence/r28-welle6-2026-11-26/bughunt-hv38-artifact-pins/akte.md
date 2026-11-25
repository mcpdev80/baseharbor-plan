# BUG-HUNT slice H-V38 - artifact pin & digest integrity

Sitz `w169-0428-224-hunt-v38`. H-V38 (pure FINDING, no product changes). READ-ONLY audit of artifact pin & digest integrity across GitHub workflows + `scripts/release-requirements.json`, cross-checked against the 0428-249 registry-artifact context.

## PLAN

- fetch develop (refs/heads/develop via `git ls-remote`), HEAD-sha in akte; NUR lesen (git show/grep/rg/read)
- anchor rule: every image/binary/tool referenced in workflows + release-requirements.json -> tag-only vs SHA/digest-pinned; oras/registry-auth paths; digest verification in release assembly
- per-row file:line findings + proposed card lines in this akte
- cleanliness (nichts geaendert; keine container/volumes); END_DONE with fund count
- NO subagents, NO product edits, NO workflow edits

## Anchor

- develop HEAD: `a87da7d179e08d43e8987885c38ab459ff1d887d` (git ls-remote origin refs/heads/develop; matches mission target a87da7d17-era)
- Worktree cut at EXACT tip: `workers/w169-0428-224-hunt-v38-wt` @ a87da7d1; `git merge-base --is-ancestor origin/develop HEAD` passes; `git log --oneline origin/develop..HEAD` empty; `git diff origin/develop..HEAD --name-only` empty
- planning repo remote: `origin	https://github.com/mcpdev80/baseharbor-plan.git` (fetch)

## Scope read

- `scripts/release-requirements.json`: NOT an image/binary/tool manifest. It is a gate inventory (`baseharbor.pre-release.gate-evidence/v1` + adoption + ha + integration + journey schemas). Zero occurrences of `oras://`, `sha256:`, `digest`, `image:`, `registry`, or auth. Pinning/digest audit therefore lives entirely in `.github/workflows/*.yml` + the `scripts/ci-*.sh`/`*.py` they invoke.

## Findings (per-row)

### F1 - GitHub composite actions: SHA-pinned (OK)
- All `uses:` are commit-SHA pinned (40 hex), not mutable tags. Evidence:
  - `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` (# v7.0.1) - every workflow
  - `actions/setup-go@b7ad1dad31e06c5925ef5d2fc7ad053ef454303e` (# v7)
  - `actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97`
  - `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065` (# v5)
  - `actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02` (# v4.6.2) and `@b7c566a772e6b6bfb58ed0dc250532a479d7789f` (# v6)
  - `actions/download-artifact@d3f86a106a0bac45b974a628896c90dbdf5c8093` (# v4.3.0) and `@018cc2cf5baa6db3ef3c5f8a56943fffe632ef53`
  - `actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6` (# v4)
  - `actions/setup-node@v6` - 3x in pre-release.yml:1503,1720,1937 -> TAG-pinned, not SHA. See F5.
  - `docker/*-action`, `goreleaser/goreleaser-action@f06c13b6b1a9625abc9e6e439d9c05a8f2190e94`, `renovatebot/github-action@6d26fcf0275dc65624cbc3d51fe78bc773f98321` (# v46.3.6)
- Verdict: composite-action pinning is SHA-faithful. No finding.

### F2 - Runtime image base layers: SHA-digest pinned (OK)
- `deploy/control-plane/Dockerfile:1` `FROM golang:1.27-alpine AS build` - tag.
- `deploy/control-plane/Dockerfile:13` `FROM alpine:3.24@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6` - digest-pinned (OK).
- `deploy/control-plane/Dockerfile.binary:1` `FROM debian:trixie-slim@sha256:a72b4433de1cf7d6bae0c4cee74d0547f58601a643b3375f070c51600d63b6b2` - digest-pinned (OK).
- Verdict: the release-built runtime image layers on digest-pinned bases. The `golang:1.27-alpine` build-stage base is tag-only (F4), but it is a build-only layer that does not enter the pushed artifact.

### F3 - Release image publication (OK)
- `.github/workflows/runtime-image.yml` job `build` (lines 23-140): `docker/login-action@ghcr` (line 99-104) -> `docker/metadata-action` (106-118) tags `edge` + `sha-${short_commit}` + version/minor + `latest=false`; `docker/build-push-action` `push: true` (120-133); `actions/attest` `subject-digest: ${{ steps.build.outputs.digest }}` to-registry (135-140).
- Release assembly `release.yml`: `checks` -> `pre-release.yml` (63-72); `runtime-image` -> `runtime-image.yml` (73-87); `release` job checks out the exact tag SHA (96-106), runs GoReleaser (107-116) and `actions/attest` on `dist/baseharbor_linux_*.tar.gz` + `dist/checksums.txt` (131-140).
- Verdict: released image + binaries are attested by digest/checksum. No finding.

### F4 - build-stage base image tag-only (INFO, non-blocking)
- `deploy/control-plane/Dockerfile:1` build FROM `golang:1.27-alpine` is tag-only. The run-stage `alpine:3.24@sha256:...` (Dockerfile:13) is digest-pinned. Because the build stage is ephemeral (builder image discarded), the mutable golang tag does not affect the published artifact.
- Proposed card: "Digest-pine the build-stage Go base: change `deploy/control-plane/Dockerfile:1` `FROM golang:1.27-alpine` to `@sha256:<digest>` of the pinned Go image; scope: single-line dep change, no release-gate change."
- Note: editing `deploy/control-plane/Dockerfile` is outside the hunt write-set (would need a card); this is recorded as a proposed card line, not applied.

### F5 - actions/setup-node: tag pinned, not SHA (INFO, non-blocking)
- `pre-release.yml:1503,1720,1937` use `actions/setup-node@v6` (tag ref, no SHA). Composite-action tag pins are version-bumped by renovate; not a release-artifact integrity risk.
- Proposed card: "SHA-pin `actions/setup-node@v6` (3 occurrences, pre-release.yml:1503/1720/1937) to a commit SHA. Scope: workflow policy file, Owner scope (`.github/**`) - report as file:line, do not edit."

### F6 - ORAS CLI install: tag pinned + checksum-verified (OK, with note)
- `scripts/ci-install-oras.sh` (used by ~15 workflow cells: ci.yml:289,552; docker-runtime-acceptance.yml:127,221; pre-release.yml:894,946,1018,1083,1249,1286,1327,1387; targeted-integration.yml:1478; nextjs-greenfield-e2e.yml:86; runtime-broker.yml; observability-acceptance.yml:71,153; podman-acceptance.yml:128).
- `version=1.3.6` (line 7, tag) + `oras_project` asset downloaded from GitHub release (14) + `oras_1.3.6_linux_<arch>.tar.gz` + `checksums.txt` fetched (18) -> `sha256sum --check --status` against the release-supplied manifest (19-21). Tool is checksum-verified at install.
- Verdict: oras is the verified OCI resolution tool; its own release is tag-pinned + checksum-verified. No integrity gap. Note: the oras *release version* is a mutable tag (1.3.6); a supply-chain hardening card could pin it by digest, but this is a CI tool, not a release artifact.

### F7 - Local OCI registry publish + ORAS resolve (OK)
- `scripts/ci-local-oci-registry.sh publish` (lines 24-67): validates `localhost:5000/*:*` target (27), `image inspect` source (31), runs `docker.io/library/registry:2.8.3` container (41), pushes (55-60), then `oras resolve --plain-http` validates the published digest matches `^sha256:[0-9a-f]{64}$` (61-65) or fails.
- `insecure = true` is set ONLY for the podman localhost:5000 registry config (32-39) - scoped to the isolated local registry, not ghcr. Intentional and narrow.
- Verdict: the published pre-release/core-bootstrap/coreless/browser runtime image is digest-verified via ORAS before consumption. No finding. This is the same mechanism the 0428-249 context characterized (registry-artefakt vs operator-auth distinction).

### F8 - Release assembly digest verification (OK)
- `pre-release.yml` `source_prepare` resolves the candidate SHA; every gate checks out `ref: candidate_sha` (e.g. 277,330,369,391,448,483). `source` job (1507-1537 in targeted-integration) checks out exact candidate and verifies `git rev-parse HEAD == EXPECTED_SHA` (1456-1465).
- `targeted-integration.yml` podman build path (777-785): `--pull` + `--iidfile`, inspects image Id + revision label + runs `sha256sum` of in-image baha, cross-checked in Python (787+).
- `docker-runtime-acceptance.yml` (594-627): `docker build --pull` + `image inspect` verifies `revision == source` + `image_id matches sha256:` + host-binary digest == runtime-binary digest (621-624) - byte-exact binary-to-image proof.
- Verdict: release assembly verifies the exact candidate SHA and, where a runtime image is built, byte-exact binary<->image digest. No finding.

### F9 - `docker build --pull` semantics (OK)
- Every CI image build uses `docker/podman build --pull` (ci.yml:1149; docker-runtime-acceptance.yml:271,594; observability-acceptance.yml:80,162; pre-release.yml:1256,1293,1341,1401; runtime-broker.yml:60,352; runtime-s3-acceptance.yml:37; targeted-demo-acceptance.yml:301; targeted-integration.yml: many). `--pull` forces a fresh base-layer fetch (no stale cache), so the pinned base digest (F2) is actually pulled and verified by the runtime, not taken from a cached layer.
- Public-image cache `ci-public-image-cache.py` (read-only forwarder to `public.ecr.aws` / `ghcr.io`): admits only a fixed namespace allow-list (library/... plus openbao/openbao, chrislusf/seaweedfs, valkey/valkey) and re-verifies manifest body against `sha256` (53-59) with `Docker-Content-Digest` (114-124). No finding.
- Verdict: base layers are pulled fresh and digest-verified. No finding.

### F10 - consumer source pins (OK)
- `scripts/consumer_source_pins.py` (1-50): validates console/connector `repository` + 40-hex `commit` + `workflow` == `.github/workflows/release-integration.yml`, rejects symlinks/loose perms (35-44), schema `baseharbor.private-evidence-pins/v1`. `pre-release.yml` checks out exact demo (1492-1498), connector (1470-1476), console (1477-1483), candidate (1485-1491) refs, all 40-hex.
- `docs/releases/*.demo-ref` files: every tag v0.4.17-v0.4.28 has a 40-hex demo commit pin (verified: v0.4.28 = b41127723e523134a1c14ee3c36cf133237162ce).
- Verdict: consumer refs are SHA-pinned and validated. No finding.

### F11 - release-requirements.json itself (OK)
- No image/binary/tool references, no oras, no digest. It gates release readiness by gate-id, not by artifact pin. No finding for this file's scope.

## Cross-check vs 0428-249

- 0428-249 (r28-welle5-2026-11-22, develop 3cbb2bac) characterized a *runtime*: `localhost:5000/baseharbor-runtime:pre-release` ORAS `local registry blob/manifest unknown` = a registry-PUSH/BLOB gap in `ci-local-oci-registry.sh publish` / `pre-release-runtime-suite.yml`, NOT operator-auth.
- H-V38 confirms the SAME publish-or-resolve path (F7) is now digest-verified: `ci-local-oci-registry.sh:61-65` rejects a non-sha256 digest. The 0428-249 fix (verify-or-fail on resolve) is present in the current tree. No new gap of that class.

## Propose card lines

1. F4: "Release runtime image build-stage Go base (`golang:1.27-alpine`, deploy/control-plane/Dockerfile:1) is tag-only while run-stage base is SHA-digest-pinned; pin the build stage by digest. Single-line, non-release-gate."
2. F5: "SHA-pin `actions/setup-node@v6` (pre-release.yml:1503/1720/1937) to a commit SHA. Owner-scope workflow file - file:line finding."
3. Optional F6 hardening: "Pin oras CI tool release (scripts/ci-install-oras.sh:7 `version=1.3.6`) by release digest. CI-tool supply-chain hardening, optional."

## Fund count

- Real (buildable card): F4 (1).
- INFO, non-blocking, no card required: F1, F3, F7, F8, F9, F10, F11.
- Owner-scope workflow file finding (report only): F5.
- Optional hardening: F6.

Total proposed cards: 2 (F4 real, F5 Owner-scope report). No product edits made. No workflow edits made.

## Cleanliness

- docker ps -a before: none started (read-only audit, no compose/container launched).
- docker ps -a after: none.
- No volumes, networks, state directories created. ambient-core/ images untouched.
- cleanliness: clean.

## END

END_DONE w169-0428-224-hunt-v38: H-V38 artifact pin & digest integrity audit complete; 2 proposed cards (F4 real build, F5 Owner-scope workflow pin), rest confirmed OK; no product/workflow edits.
