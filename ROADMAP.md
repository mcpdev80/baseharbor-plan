---
kind: roadmap
sources: ["mcpdev80/baseharbor#155"]
---
# BaseHarbor roadmap

Master roadmap, migrated from [baseharbor#155](https://github.com/mcpdev80/baseharbor/issues/155). Detailed scope and acceptance live in the linked release notes; delivered history lives in the product repository's release notes. Live task state: [views/overview.md](views/overview.md).

## Direction

Developer experience first: simple by default, secure by default, explicit when needed. Capabilities, not products. Portable Application Intent stays independent from Docker, Podman, Kubernetes, OpenShift and infrastructure products.

Repository / Application → Inspection → Portable Intent → Environment + Policy → Target and Runtime / Capability / Delivery Providers → Plan / Preflight / Reconcile → Verify → Audit / Evidence.

Runtime, capability, delivery, workload-source adaptation and workspace/Git acquisition remain distinct boundaries. Known failures explain the cause and the safest next action.

**Binding product correction (from #872, 2026-10-11): no migration implementation scope before v1, no developer-supplied Application IDs, no unconditional SQL/Secrets/Identity bundle.** The provider footprint follows requested capabilities and genuine dependencies. Preserve shared consumers, data, recovery and security during lifecycle changes. #810 records historical v0.4.23 behavior and does not define the current product. Later releases consume the accepted foundation and do not silently redefine contracts.

## Release sequence

v0.4.23 (#571), v0.4.24 (#603) and v0.4.25 (#872, closed 2026-10-15) are published/delivered. Their historical evidence does not qualify later candidates.

| Release | Note | Scope and main dependencies |
| --- | --- | --- |
| v0.4.26 | [v0.4.26](releases/v0.4.26.md) · epic [core-888](epics/core-888-development-and-ci.md) | Compact needs-first wizard, CLI/JSON/MCP footprint and developer docs; bounded workflow/CI V1 with small PRs and conservative test selection |
| v0.4.27 | [v0.4.27](releases/v0.4.27.md) | One local/remote workflow, shared installation-owned state and app binding; durable operations, native registry/local-store delivery, independent stage versions/readable release inventory/thin promotion, remote web and developer access/profile portability [core-777](epics/core-777-developer-access-and-profiles.md) |
| v0.4.28 | [v0.4.28](releases/v0.4.28.md) | Web Console management and complete developer journeys |
| v0.4.29 | [v0.4.29](releases/v0.4.29.md) · epic [core-818](epics/core-818-host-platforms.md) | Host portability: core-819…core-823; audit core-817; Darwin prerequisite core-882, Podman Machine core-883, real macOS runtime evidence core-884 |
| v0.4.30 | [v0.4.30](releases/v0.4.30.md) | Native TLS / justified proxies core-902; attack-protection baseline and DDoS/operator boundaries core-903 |
| v0.4.31 | [v0.4.31](releases/v0.4.31.md) | Final semantic acceptance; quality completion core-862 and a no-new-features stability reconciliation before the freeze |
| v0.4.x (unscheduled) | [v0.4.x](releases/v0.4.x.md) | Open v0.4.x items without a patch assignment (#427 parent) |

All belong to milestone **v0.4.x** ([v0.4.x](releases/v0.4.x.md), #427). Release qualification/promotion stays ordered; independent future work may proceed on develop while a candidate is frozen. Quality, safety, ownership, CLI/JSON/MCP parity, bilingual documentation and exact-source evidence are requirements of every release. The formal compatibility freeze is v0.5 (#175), not v0.4.25. Standards-first service bindings/provider catalog (core-390) remain pre-freeze work.

### Host-platform boundary

v0.4.29 is authoritative: Linux and real WSL2 developer local/remote paths; macOS arm64 Dev Local with **both Docker Desktop and Podman Machine**. Native macOS amd64 build/conformance alone does not establish runtime support. VM resource evidence and isolation describe the actual selected runtime. Automatic macOS Keychain trust and macOS Dev Remote (core-886) and Developer ID signing/notarization (core-885) are explicitly unscheduled follow-ups outside v0.4.29; they stay in [backlog](releases/backlog.md) without an invented release.

### Older open work

Released v0.4.23 tasks #805–#808 and #810–#814 are closed with qualification/publication links; earlier bugs #755, #764 and #765 are closed with released references. core-750–core-752 (inspect), core-754 (typed machine preconditions), core-766 (orphan cleanup) and core-815 (remaining all-stack native startup) stay visible until their exact remaining scope has evidence; age or a published version is not proof of completion. core-815's build fixes are delivered; its broader startup requirement is not discarded. core-862 introduces minimal version-pinned static/vulnerability checks and risk-focused coverage early and ratchets them across releases; final completion belongs to v0.4.31. Assessment core-887 is review/backlog material, not release scope.

## Later milestones

| Milestone | Note | Planned children |
| --- | --- | --- |
| v0.5.x | [v0.5.x](releases/v0.5.x.md) (#428, #175) | Formal freeze v0.5.0; state versioning core-297; cross-component contracts core-298; upgrade/recovery/deprecation core-299; portability acceptance core-300 |
| v0.6.x | reserved | Additional compatible availability extensions only; the original HA foundation was delivered before the freeze |
| v0.7.x | [v0.7.x](releases/v0.7.x.md) (#430) | Namespace-first Kubernetes runtime foundation core-102 and core-304…core-310; delegated delivery/GitOps core-325 |
| v0.8.x | [v0.8.x](releases/v0.8.x.md) (#431) | Kubernetes Complete: lifecycle/provider/recovery/observability/DX parity and production acceptance core-313…core-320 |

No pre-v1 migration obligation is introduced by the compatibility/versioning roadmap. Fundamental Application/Provider boundaries are settled before the formal freeze. Unscheduled ecosystem work: core-100 (operator RBAC/JIT), core-181 (air gap/private OCI), core-209 (optional ecosystem) — `status/backlog`; promoting them needs an explicit scope decision.

## Release and issue workflow

- v0.4.25 alone kept its shared PR #881 and earlier procedure. From v0.4.26, core-888 governs small task branches/PRs against develop, conservative targeted CI and separately frozen release candidates. Other contributors need Maintainer (@mcpdev80) approval; the Maintainer's own PRs use the documented solo-maintainer exception with required checks. Preserve others' commits; no force-push over shared work. core-882 is the agreed develop prerequisite exception.
- Release notes own scope, ordering, cross-cutting acceptance and release completion. Focused tasks reference their parent; do not create duplicate roadmaps or turn every heading into a task.
- Planning lives in this repository (see [WORKFLOW.md](WORKFLOW.md)); specs own normative semantics, ADRs rationale and release notes delivered history — all in the product repositories. Source GitHub issues retain discussion/history; [the activation record](migration/cutover-checklist.md) defines the switch.
- A task closes only when its bounded implementation and required evidence are complete. Missing/failed/skipped/unverified acceptance stays open. Reuse green evidence only when the verifier proves unchanged inputs; rerun affected gates.
- Candidate readiness covers BaseHarbor, Demo, Console, Node Connector, CLI/JSON/MCP contracts, EN/DE docs, Pages candidate build/navigation, changelog/release notes, immutable ecosystem pins and release-specific evidence.
- Preparation does not authorize complete pre-release execution, merge, tag, publication or production Pages deployment; those follow separately authorized release steps.

## Roadmap clarifications kept from the source comments

- **v0.4 completion vs v0.5 freeze (2026-09-23):** v0.4.x finishes the missing product/runtime/developer primitives; v0.5.x freezes, versions, hardens and proves the complete contract. v0.5 may finalize/version/harden these semantics; it must not reopen application intent, ownership, provider axes, developer journey, artifact convergence semantics or add a new foundational platform direction. The normal developer model stays `baha app init` + `baha up`. BaseHarbor abstracts operational work but does not hide platform facts: application-relevant capability/provider/runtime versions, compatibility and changes stay observable through concise human output and detailed verbose/JSON/MCP state.
- **Standards-first pre-freeze dependency:** current v0.4.x correctness/DX → core-390 standards-first contract alignment → v0.4.31 semantic acceptance → v0.5.x freeze. core-390 fixes the common contract boundary that provider/capability work consumes; no parallel product-specific contracts; existing v0.4 capability IDs stay compatible until mapping/migration is explicit and tested.
- **Observability (2026-09-24):** when Metrics/Logs are enabled, BaseHarbor automatically collects supported workload and managed-provider signals (including provider audit for PostgreSQL/Valkey/OpenBao/object storage); disabled intent stays disabled. The workload developer contract is OpenMetrics for metrics and stdout/stderr for logs.
- Older sequencing comments (v0.4.15–v0.4.18) are historical and remain in the [source snapshot](migration/source-snapshot/baseharbor/155.json).
