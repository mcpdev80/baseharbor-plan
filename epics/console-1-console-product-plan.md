---
id: console-1
title: Console product architecture and implementation plan
status: open
release: v0.4.28
parent: ""
sources: ["mcpdev80/baseharbor-console#1"]
---
# console-1 · Console product architecture and implementation plan

Source: [baseharbor-console#1](https://github.com/mcpdev80/baseharbor-console/issues/1). Remaining delivery is assigned to [v0.4.28](../releases/v0.4.28.md); future Kubernetes parity remains subject to the later runtime roadmap. Child task: [console-2](../tasks/console-2-live-core-adapter-workflow-proofs.md).

The completed checklists of the source (Phase 0 foundation, UI/wizard/UX checkpoints of 2026-10-02/03, contract alignment) are history; see the [snapshot](../migration/source-snapshot/baseharbor-console/1.json). This note keeps the product rules and the open items.

## Product definition

The Console is the complete visual operations surface for BaseHarbor: every workflow plus deep runtime visibility, while BaseHarbor stays the single source of truth. CLI / JSON / MCP / HTTP / Console all use the same BaseHarbor Core.

## Rules

- Runtime resources are provider-neutral (Docker/Podman now, Kubernetes/OpenShift later): Application → Deployment → Component/Provider → Runtime realization → Runtime resource. Ownership is authoritative, never guessed from names: `managed | external | unmanaged | platform`.
- The Console never calls a Node Connector or runtime API directly: Console → BaseHarbor HTTP → Core → Target Access Provider. Kubernetes/OpenShift normally use native APIs.
- Security: shared Machine Operator Authorization, no Console-local RBAC; HTTPS only for Console/API/streams; no duplicate secret store; no raw secret reveal by default; safety class/policy/confirmation/ownership enforced server-side; terminal/exec explicit and auditable, never a hidden host shell.
- `docs/UX-DESIGN-SYSTEM.md` in the Console repository is the authoritative UX/UI specification; complex workflows use its wizard system (no oversized modals or one-shot forms for dependent decisions).
- Non-goals: second orchestration engine, duplicate deployment state, Git hosting, browser IDE, direct browser-to-runtime APIs, Console-to-Node-Connector path, Console-local secret store or authorization model.
- Do not fake contract-bound features in the Console; bind to Core contracts.
- **Deployment topology:** one installation/security boundary → one authoritative Core → optional Console for that installation. Console state is presentation/client state only; no federation of Dev/Test/Prod, no proxying one installation through another, no Baha-to-Baha traffic; same-origin or tightly bound trusted origin by default. A future multi-Core selector is client-side only and connects directly to the chosen Core.

## Phases still open

- Phase 1–3 live binding (read-only BaseHarbor, workflow parity, runtime operations) through Core — continued in console-2.
- Phase 4 remote Targets through the Target Access Provider contract (#769).
- Phase 5 AI assistance (explain/diagnose/plan/guarded actions through the same machine operations; no shell, no secrets in AI context by default) — the pre-freeze decision belongs to v0.4.28.
- Phase 6 Kubernetes/OpenShift after BaseHarbor's runtime contracts exist; no separate OpenShift Console clone.

## Acceptance

- Every supported human-facing BaseHarbor operation has a Console representation.
- repository → inspect → init → plan → apply works through the GUI.
- Runtime resources are visible from Application and Target context.
- Logs/terminal/metrics/events work through BaseHarbor streams.
- managed/external/unmanaged/platform ownership is visible.
- The Console can evolve from Docker/Podman to Kubernetes/OpenShift without replacing its core architecture.
- Default Console deployment is documented as belonging to one BaseHarbor installation/Core/security boundary.
- Console live mode has exactly one selected authoritative Core at a time.
- No Console-local or central cross-installation deployment/authorization database exists.
- Same-origin/tightly bound trusted-origin browser deployment is the preferred default.
- Independent Dev/Prod installations remain independent when the Console is enabled.
- Any future multi-Core selector is client-side only and preserves direct Core authority.

## Remaining contract-bound items (from the source's 2026-10-03 checkpoint)

These waited for Core #767/#768/#769/#770, which are now closed foundations; the live binding is tracked in console-2:
bind the adapter to protected HTTP discovery/results; operation submission/progress/problems; actor/session/authorization; live runtime ownership/capability inventory; remote Target Access; live logs/events/terminal; replace fixture-preview data with live Core projections.
