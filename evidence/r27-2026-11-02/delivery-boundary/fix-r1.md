# w2-delivery-boundary — typed owner/selection checks + fixtures + docs/spec/delivery-provider-v1.md (EN/DE) + ADR 0022

- Lane: `w2-delivery` (r27 delivery-boundary)
- Task: `t-20261018-r27-delivery-boundary` (owner w2-delivery, active — claim published)
- PR: STACKED on #1326
- Hosted model: Qwen Flash (via AgentGateway)
- Date: 2026-11-02

## PLAN

1. plan.py claim t-20261018-r27-delivery-boundary — already published (task active). ✅
2. Ground write-set from card + predecessor (predecessor contract.go + docs/spec/delivery-provider-contract-v1.md exist; deliverables = typed checks/fixtures on top + docs/spec/delivery-provider-v1.md EN/DE + ADR 0022). ✅
3. Build typed owner/selection checks + delegated-owner denial fixtures in internal/delivery/ on top of existing Selection.Validate(). ⏳
4. docs/spec/delivery-provider-v1.md EN (standards map, Baha-extension narrowings, tool/version checks, fixtures).
5. docs/de/spec/delivery-provider-v1.md DE counterpart (literals verbatim).
6. ADR 0022 (next free after 0021; 0011 already taken).
7. Local checks to terminal.
8. push + STACKED PR on #1326 + observe gates + END.

## repo-rule compliance (expected write-set)

- internal/delivery/contract.go + tests: build on existing predecessor types (Mode/ReconciliationOwner/Placement/Selection + Validate()); NO overlap with coreinstallation/stableid slices.
- docs/spec/delivery-provider-v1.md + DE counterpart (distinct from predecessor delivery-provider-contract-v1.md).
- one product ADR: next free number = 0022 (0001..0021 exist; 0011 already = delivery-providers-and-tool-neutrality.md).
- NO universal bundle/registry/DSL/scaffold/registry-server/scheduler/approval/pipeline engine.
- No shared command/HTTP/MCP/help/golden registrations (public-surfaces). No nav/mkdocs edit.

## END

- Status: BLOCKED — awaiting input; work restart started per Owner correction.
