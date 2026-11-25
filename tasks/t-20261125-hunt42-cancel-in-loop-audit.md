---
id: t-20261125-hunt42-cancel-in-loop-audit
card_number: "0428-314"
card_short_title: "cancel-not-deferred loop"
type: task
areas: [runtime, testing]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: Audit the reported per-attempt contexts for a real cancellation leak.
kanban_title: 0428-314 · cancel-not-deferred loop
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/telemetry/otlp.go", "https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/runtimeobservability/observer.go", "https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/targetsession/session.go", "https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/logs/query.go"]
---

- [x] t-20261125-hunt42-cancel-in-loop-audit · 0428 hunt H-V42: cancel()-not-deferred loop contexts (leak class) in telemetry/observer/session #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/runtime #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/telemetry/otlp.go), [proof 2](https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/runtimeobservability/observer.go), [proof 3](https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/targetsession/session.go), [proof 4](https://github.com/mcpdev80/baseharbor/blob/99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82/internal/logs/query.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Audit the reported per-attempt contexts for a real cancellation leak.

## Disposition

DROP (2026-11-25). No implementation or regression test is warranted: the reported per-attempt contexts are explicitly canceled. Deferring cancellation inside these loops would retain resources until the enclosing function returns and make the alleged leak worse. The terminal context is session-scoped, not a retry-loop context.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Source finding

H-V42 proposed replacing explicit per-attempt cancellation with deferred cancellation. Audit of BaseHarbor source at `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82` found the cancellation calls already present in telemetry, observer, target-session, and log-query paths. The cited machine terminal context is long-lived and is canceled on its exit/error paths. No reproducible leak was established.
