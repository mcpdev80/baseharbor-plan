---
id: 2026-10-22-r27-parallel-execution
status: accepted
date: 2026-10-22
title: v0.4.27 parallel execution and evidence-first launch
---

# v0.4.27 parallel execution and evidence-first launch

## Hard start sequence
1. Complete v0.4.26 and release cleanup. Do not touch Codeman's active product branches.
2. Integrate release-start dependency updates and freeze actual baseline SHAs.
3. Evidence contract accepted; publisher and resolver developed in parallel by different owners.
4. Trusted verifier and independent human/agent/fork acceptance; ordinary PR generates and archives evidence automatically, including planning linkage. Archive errors fail closed where required.
5. Authority, access, delivery and runtime CI gates each require evidence acceptance and their relevant contract. The four gates may proceed concurrently with disjoint files; central trusted CI writer integration is serialized.
6. Dispatch product tasks when their own contracts, accepted CI lane and exact interfaces are available. Never wait for an unrelated domain gate. Integration surfaces have one writer.
7. End-to-end proof, docs, cross-domain CI integration, pre-release preparation and separately authorized release qualification.

## Open work pool
The work pool is shared by Codeman (coordinator + four workers), independent ChatGPT/Codex sessions, humans and external contributors. It is not four fixed slots. The coordinator selects the highest-value ready tasks on the critical path, not a fixed model-specific owner; assign work by capability, file conflicts and actual runner access.

Before claiming: re-read current main and task frontmatter, accepted dependency SHAs, existing PRs and reserved files. Claim one task with owner, exact baseline, branch/PR, scope/write set, evidence/check plan and reviewer. Publish claim through normal planning PR/integration; if another owner already holds it, choose another task. Claims expire or are handed back explicitly; abandoned tasks are re-claimable after preserving unmerged work. Multiple nonoverlapping claims can run in parallel.

Before implementation: ensure real CI coverage is accepted for changed paths; do not create new files that escape trusted planner coverage. Keep source contract/API changes ahead of consumers. Small atomic PRs; no overlapping shared writer files. Keep Docker/Podman/K3s tests isolated; use cheapest applicable gate; avoid redundant reruns and full release matrix until final candidate.

At handoff: run targeted checks, publish exact source and integration SHA, PR, test identity, evidence archive manifest, open findings and independent reviewer. Automatic CI owns evidence creation and task linking for both humans and agents; no manual evidence documents required. Review and trust-policy changes cannot self-qualify. Integrate accepted PRs in dependency order, refresh consumers on new baseline, and reopen invalidated checks only.

## Work streams and single-writer seams
- Authority/state: authority contract -> state owner -> locks/journal -> application binding and management host.
- Access: profile contract -> codec/enrollment/auth -> user/team access -> onboarding.
- Delivery: delivery/candidate contracts -> registry/pack/versioning -> promotion and delegated GitOps.
- Runtime: node service/trust/streams -> native Docker and Podman -> remote rollout.
- Shared integration: central CLI/JSON/MCP/HTTP registration, trusted CI planner/executor/finalcheck and release finalcheck are single-writer merge points; prepare integration fixtures before the last task lands.

Work stealing is allowed: any free worker/contributor takes the next ready unclaimed task, never one blocked by an unaccepted interface. Do not mark a task accepted merely because its PR CI is green; final evidence must bind to actual candidate and independent review.

## Evidence durability limits
baseharbor-plan/evidence is an automatically populated, bounded, redacted and content-hashed archive. GitHub repository protection reduces accidental deletion, but does not provide WORM guarantees. Back up outside the repository for disaster recovery. Fork code never receives archive write credentials; a trusted post-run publisher validates inputs before writing.

## Validation before merging this planning change
Run `python3 scripts/plan.py render`, `python3 scripts/plan.py check`, `python3 -m unittest discover -s scripts/tests`; commit generated views and task-card links, inspect dependency graph for cycles and critical-path regressions, rebase without overwriting concurrent main changes, and verify exact pushed SHA. Do not merge an unrendered planning branch.
