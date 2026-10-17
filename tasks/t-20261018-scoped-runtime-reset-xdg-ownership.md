---
id: t-20261018-scoped-runtime-reset-xdg-ownership
type: bug
areas: [ci]
release: v0.4.26
parent: v0.4.26
owner: "mcpdev80 (scoped XDG reset review)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#992"]
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-scoped-runtime-reset-xdg-ownership · Scoped runtime reset must retain unrelated XDG state #task #release/v0-4-26 #status/active #view/active #area/ci #kind/bug

## Goal

Fix [baseharbor#992](https://github.com/mcpdev80/baseharbor/issues/992) before v0.4.26 readiness. A resource-scoped `scripts/ci-runtime-reset.sh` call must never recursively delete shared or ownership-unknown BaseHarbor XDG state.

## Ownership and scope

- Product files: `scripts/ci-runtime-reset.sh` and one dedicated sandbox regression script. No changes to #991 or CI policy/executor.
- Preserve scoped resource filtering; never infer state ownership from an arbitrary substring scope.
- Ambiguous/shared XDG state is retained or blocked. Only explicitly proven isolated state may be removed when scoped.
- Preserve existing intentionally authorized full reset of the dedicated runner; never expand it to arbitrary environments.
- Shell fixtures use disposable HOME/XDG roots, a stub container engine and harmless systemctl. Test selected/foreign containers, networks, volumes, Quadlets, selected/foreign XDG state, unknown scope, isolated roots and dedicated full reset.
- No real containers, SSH, native hosts, credentials or private paths. Minimal appropriate CI; batch edits and independently review before merge.

## Handoff

- 2026-10-18: Claim published before product implementation. Review issue #992 and product repository rules; state cleanup must fail closed for shared XDG roots. Release prepare depends on this task.
