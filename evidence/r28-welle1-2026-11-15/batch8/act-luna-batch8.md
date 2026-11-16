# CODEX-REVIEW — Luna batch 8

**ROLLE: REVIEW**
Review date: 2026-11-16. All candidates and `pull_request` run witnesses were refreshed from GitHub. No merge performed.

| PR / task | Exact head | Exact-head run | Verdict | Finding / next step |
| --- | --- | --- | --- | --- |
| #1613 `t-20261114-r28-perses-alerts` | `470735c1d187d8a680ae3b0539d75f592c945110` | `43830872570` COMPLETED SUCCESS | APPROVE CONTENT (fail-closed unavailable state) | Keep real evaluator/recipient gate false; only enable with Owner-approved real contract. See `perses-alerts/act-luna-r4.md`. |
| #1594 `t-20261114-r28-cli2-env-policy` | `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3` | `43829123791` COMPLETED SUCCESS | APPROVE CONTENT (continuity) | Explicit policy semantics satisfy prior recipe; registry r2 content remains continuous from base. See `cli2-env-policy/act-luna-r2-continuity.md`. |
| #1578 `t-20261114-r28-cli2-uid-environment` | `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283` | `43831549541` COMPLETED SUCCESS (independently verified) | REQUEST CHANGES | Destination can be clobbered if created between precheck and locked rename; domain-only diff still adds unregistered CLI file. See `cli2-uid-environment/act-1578-review-r5.md`. |

Exact-head status, PR metadata, base refs and run timestamps were read from the live API. `git diff --check` was clean for each review diff. Product tests were not run; review was read-only. No merge, approval mutation, or Planning task-state change performed.
