# CODEX-REVIEW — PR #1604

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-dashboard-valkey`  
**Candidate:** `bf58a9cf7254f6f5ebc3d9b7f9c8679e13f54ce8`  
**Exact-head CI:** run `43794644565`, COMPLETED SUCCESS, exact SHA; `./internal/metrics` passed.  
**Scope:** based on selection head `e6f5e650d048c28004cdc59608e9205c648bb509`; 3 authored files; `git diff --check` clean.

## Verdict: APPROVE CONTENT

This candidate explicitly returns UNAVAILABLE because the required Valkey signal/adapter is absent. It does not invent an exporter or emit a misleading Perses dashboard. The reason and stable dashboard key are tested; the output is an unavailable-state document rather than a purported native dashboard object.

## Recipe / future gate

- **File/change:** no correction required for the current unavailable-only scope.
- **Checks:** retain the exact-head package CI. Before changing this result to available, add the authorized adapter/signal contract and validate emitted dashboard schema and queries against pinned Perses/Prometheus.
- **Stop:** keep UNAVAILABLE while no verified signal exists; do not convert catalog presence into runtime availability.

Read-only review; no merge performed.
