---
id: 2026-11-09-r27-local-delta-delivery-and-target-presets
status: accepted
sources: []
---
# Local delta delivery and editable target deployment presets (2026-11-09)

Decision owner: BaseHarbor product owner. This is agreed product direction, **not** implementation acceptance or CI proof.

## User workflow
`baha use docker-dev` selects the existing persistent Target. `baha app apply` submits the **current local working tree**, including suitable dirty and untracked files; no required commit, push, remote Git credentials or Core-side clone. Source fingerprint identifies exact bytes independently of Git revision. A Git SHA/branch may be recorded as provenance, but never substituted for the actual dirty content.

## Standard-first transfer
- Reuse accepted candidate packaging (#0427-019) and ingress (#0427-018), native source/build-context ignore semantics, bounded capture and existing Core authority, consent, deployment ID and journal.
- First source transfer full, later incremental: changed/added/deleted files, mode changes, with content integrity and safe atomic activation. Prefer an established rsync/delta standard where compatible with the existing authenticated HTTPS Core/Connector boundaries. **Do not invent an rsync-compatible transport or silently require SSH**. Integration decision/test must determine exact appropriate tool.
- Do not upload `.git`, credentials, local state, secret files or unsafe links by default. Native ignore semantics are not a security filter alone.
- Existing local OCI images: use accepted #0427-030 transfer selection (native stores, OCI registry/pull/copy or native save/load); digest/architecture verification; avoid transferring existing layers where supported; no automatic build for an existing image. Do not implement a registry or layer protocol.
- Same deployment identity for same Target/Application/Environment; previous last-good snapshot available for recovery; unnecessary restarts avoided.

## Target presets – Best Practice defaults, always editable
| Setting | Development | Test | Staging | Production |
| --- | --- | --- | --- | --- |
| Branches | all | develop, release/* | main, release/* | main |
| Dirty source | allowed | disallowed | disallowed | disallowed |
| Commit required | no | yes | yes | yes |
| Verified remote commit | no | no | recommended | recommended |
| Explicit approval | no | no | optional | recommended |
| Pinned OCI image digest | optional | yes | yes | yes |

These are **wizard starter values**, not enforced global policies. Operator can change *every* field including production dirty behavior. Only selected persisted target rules are enforced by owning Core for CLI/API/MCP. Protected branch, clean-tree and remote-commit claims must be verified through suitable trusted provenance, not blind client assertions. Existing targets are not retroactively restricted by implicit presets. Empty/missing rules keep their documented backward-compatible meaning. Target names never imply policy.

## Runtime boundaries
v0.4.27 integrates Docker/Compose and Podman/Quadlet as already implemented. Source/OCI transport interfaces remain runtime-neutral. Kubernetes/OpenShift runtime implementations are later roadmap work (v0.7.x/v0.8.x). No premature Helm, Argo CD, Flux or native manifest requirement.

## Required acceptance
Independent workstation -> authenticated Core -> Connector -> Docker/Podman READY -> second changed-only apply -> update/destroy, plus dirty and untracked, deletion, no-change, image reuse, source tamper, symlinks/secrets, wrong tenant, consent, policy overrides, and forged metadata cases. Keep #1473 open until exact-head CI and real independent E2E evidence.

This document supersedes Core-side pinned-Git-only acquisition as the mandatory default for remote developer deployments. Clean Git SHA-only releases remain an optional source identity and are not the everyday development flow.
