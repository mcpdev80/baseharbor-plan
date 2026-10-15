---
kind: external-tooling
sources: ["mcpdev80/baseharbor#889"]
---
# External tooling that stays on GitHub

Some open GitHub issues are maintained by bots, not by people. They stay where they are and are **not** planning authorities. Each has an entry here so the inventory is complete.

| Source | Tool | Purpose | Tracking location | Planning link |
| --- | --- | --- | --- | --- |
| [baseharbor#889](https://github.com/mcpdev80/baseharbor/issues/889) "Dependency Dashboard" | Renovate | Lists pending and detected dependency updates; checkboxes there trigger Renovate, not planning | The issue itself and Renovate PRs in `mcpdev80/baseharbor` | Dependency work that needs a decision becomes a task here; routine Renovate PRs are reviewed as normal product PRs |

State at the snapshot (2026-10-15): one grouped update `renovate/all-dependencies` awaiting schedule (GitHub Actions, Go toolchain and modules, container images); Renovate lookup warnings for the placeholder images `example/api` and `example/worker` in `testdata/adoption-parity/` (expected test fixtures). The pending host-trust checkout/Alpine update noted in [core-909](../tasks/core-909-maintenance-remove-superseded-branches.md) is **not** delivered and stays visible there.

Do not copy dashboard checkboxes into this vault: they would become CardBoard cards and duplicate Renovate's own state.
