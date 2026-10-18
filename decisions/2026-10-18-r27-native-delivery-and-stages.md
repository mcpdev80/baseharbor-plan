---
id: 2026-10-18-r27-native-delivery-and-stages
status: proposed
sources: []
---
# Native delivery, artifacts and independent stage versions

Maintainer clarification on 2026-10-18 replaces the earlier video-oriented/custom-platform interpretation. Planning direction only; product specs/ADRs and independently reviewed implementation establish actual support. Preserve all existing core-777 acceptance and task IDs.

## Product boundary

BaseHarbor connects application needs to selected providers, binds credentials safely, coordinates ownership/consequence consent and verifies native results. It is not a CI platform, registry server, build farm, pipeline engine or replacement Kubernetes controller. Same everyday init -> select destination -> up -> status flow for local/remote and solo/team. Ask only unresolved information, show readable names/versions by default, expose digests/details/JSON for exact identity. No login/server or fixed SQL/Secrets/Identity bundle for ordinary local use.

## Reuse map

| Concern | Adopted source/function | Baha responsibility |
| --- | --- | --- |
| Image identity/content/platform | OCI Image/Distribution and image-layout; native Docker/Podman stores | Select/resolve/verify actual artifacts; distinguish manifest/index/config digests |
| Human version/source metadata | OCI image.version, image.source, image.revision, image.title; existing release manifests | Readable component inventory; claim/verified/unknown distinctions; no fabricated provenance |
| Multi-container release input | Existing Compose files/OCI artifacts, Quadlet units; later native Helm/Kustomize/Kubernetes inputs | Bind selected exact native input to app/target/stage, no compulsory custom release format |
| Build | Existing Docker/Compose, Podman, configured native builder; existing CI | Invoke only for explicit source-build; no rebuild of an existing release/promote |
| Image transfer | Native pull/push/save/load or established OCI-copy tools/libraries | Scope auth/trust, ensure availability, verify exact supported transport identity |
| Registry | Existing enterprise endpoint; optional existing OCI Distribution implementation | Native credentials/CA, explicit opt-in local setup, owned storage/cleanup, no always-on requirement |
| Runtime lifecycle | Compose; Quadlet/systemd; later K8s/OpenShift native controllers/APIs | Apply supported native resources and observe; do not invent atomicity/canary/zero downtime |
| CI | Existing GitHub Actions/GitLab CI or equivalent | Headless CLI/JSON/API consumption with personal/machine scope and result correlation |
| GitOps | Existing Argo CD/Git/Helm/Kustomize/native tracking | Delegated ownership guards, desired-change preview/handoff and honest observed status |

These are open standards and established ecosystem mechanisms, not a claim that all formats/tools are interchangeable or that every backend/version is supported. Pin/test actual versions and feature-detect before implementation. Compose OCI publication has a documented minimum version; do not blindly require latest tooling or introduce it as a mandatory distribution path.

## State, stages and ownership

The management instance owns Baha installation/deployment/binding metadata and locks. Runtime state is observed natively. In delegated delivery, external Git/config is desired-state authority for those resources; Baha cannot imperatively overwrite it or run a second reconcile loop. One owner per resource, not one duplicated global database. Local cache and a copied profile grant no rights.

Stage != Target != application version. Each deployment retains desired, applied and observed component refs plus its configuration/secret/provider scope. Dev v1.5, Test v1.4 and Prod v1.3 may run simultaneously. Multiple environments on one target require distinct native project/resource/data owners; reuse across environments is explicit and authorized. Independent installations remain independent; equal aliases or dev names confer no trust. Native image availability does not imply data or security isolation.

## Thin promotion and version inspection

A release may contain several differently versioned components and no Git checkout. Use existing artifact/source metadata; annotations are claims unless evidence verifies them. Missing Git revision/build provenance stays unknown. Show release, components, Git/contract revision, intended/applied/observed version, running resources and observation time; exact image identifiers remain available in details/JSON.

Promote means the user selects exact artifact refs and destination, then existing target-specific plan/preflight/apply/verify runs. No automatic stage ordering, test approval, CI gating judgement, automatic database copying or rebuilding. Destination settings/secrets/provider bindings remain destination-owned. Across authorities the client can carry permitted artifact refs, not provider/admin/secret state; no federation required. A native copy unable to preserve required identity/signatures cannot silently pass. For delegated delivery, return an explicit change preview for the existing Git/CI process; never directly mutate the cluster or claim synced/healthy from mere submission. No automatic Git push/merge.

Database schema migration is the application's responsibility using its existing tools/jobs. Baha enforces only its verified ownership/permissions/declared preconditions and explicit recovery choices. A backup is not proof of schema compatibility; image rollback is not database rollback. Unsupported/unknown migration capability is reported, not guessed.

## Release boundaries and evidence

v0.4.27 implements qualified Docker/Podman direct operation and reusable client/artifact/stage interfaces, with deterministic CI/GitOps boundary examples. Live Kubernetes/OpenShift and delegated GitOps runtime acceptance stay in existing core-325/v0.7/v0.8 plans. Full air-gap mirrors remain core-181; advanced governance remains core-100. Do not move those implementations forward to satisfy a video.

The old video-proof card is now real stage/artifact/promotion acceptance; filming is optional. BaseHarbor's own release-promotion lifecycle cards are unrelated to user-app promotion. New implementation remains startup/CI-predecessor dependent, unassigned and separately reviewed. Cheap tests first; native evidence only for actual uncovered behavior; verifier-valid green reuse and separate complete pre-release authorization remain unchanged.

## Primary references checked on 2026-10-18

- [OCI annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md), [OCI image layout](https://github.com/opencontainers/image-spec/blob/main/image-layout.md).
- [Compose OCI artifact distribution](https://docs.docker.com/compose/how-tos/oci-artifact/), [Compose build](https://docs.docker.com/reference/compose-file/build/), [Compose production](https://docs.docker.com/compose/how-tos/production/).
- [Podman Quadlet/systemd](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html), [native image transfer](https://docs.podman.io/en/latest/markdown/podman-image-scp.1.html), [Skopeo copy](https://github.com/podman-container-tools/skopeo/blob/main/docs/skopeo-copy.1.md).
- [GitHub Actions image publishing](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images), [GitLab image build/push](https://docs.gitlab.com/user/packages/container_registry/build_and_push_images/).
- [Argo CD automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/), [tracking strategies](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/).
