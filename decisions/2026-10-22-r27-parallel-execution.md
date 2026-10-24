---
id: 2026-10-22-r27-parallel-execution
status: accepted
date: 2026-10-22
title: v0.4.27 parallel execution and evidence-first launch
---

# v0.4.27 parallel execution and evidence-first launch

## Hard start sequence
1. Complete v0.4.26 and release cleanup before v0.4.27 integration or activation. Do not touch Codeman's active product branches. An explicit owner-authorized exception permits isolated, non-mutating v0.4.27 planning/contract preparation on separate branches while v0.4.26 is in flight; it does not make waiting implementation tasks ready, alter v0.4.26 candidate SHAs, or authorize merge into the active release line.
2. Integrate release-start dependency updates and freeze actual baseline SHAs.
3. Evidence contract accepted; publisher and resolver developed in parallel by different owners.
4. Trusted verifier and independent human/agent/fork acceptance; ordinary PR generates and archives evidence automatically, including planning linkage. Archive errors fail closed where required.
5. Authority, access, delivery and runtime CI gates each require evidence acceptance and their relevant contract. The four gates may proceed concurrently with disjoint files; central trusted CI writer integration is serialized.
6. Dispatch product tasks when their own contracts, accepted CI lane and exact interfaces are available. Never wait for an unrelated domain gate. Integration surfaces have one writer.
7. End-to-end proof, docs, cross-domain CI integration, pre-release preparation and separately authorized release qualification.

## Isolated early preparation and simplicity acceptance

- The same ordinary task -> branch -> PR -> selected CI -> review -> merge path applies to humans, Codeman, Codex and external contributors. No agent-specific commands, hand-authored manifests, copied evidence URLs or special handoff documents are prerequisites for qualification.
- Early work may inspect the current CI/planning baseline, specify minimal contracts and prototype read-only preflight or evidence tooling on separate branches. Keep v0.4.26 workflow files, release candidate, runners, consumer pins and active write sets untouched. Do not merge or activate v0.4.27 product/CI changes into v0.4.26 `develop` before Verify.
- Do not remove startup dependencies or mark implementation cards ready merely to allow preparatory research. A future dependency change must identify the precise isolated work and be rendered/checked before publication.
- CI should generate and archive bounded proof, bind exact source/integration SHAs, and link task/PR automatically; use valid exact-input green checks rather than rerunning. A cheap read-only release preflight should detect missing or inconsistent consumer pins, source candidates, notes and dependencies before expensive matrix dispatch. Any future pin freeze automation must produce reviewed immutable candidates rather than inventing or silently mutating pins.
- Failure feedback must name the broken prerequisite, affected repository/task and a concrete repair action. Fail closed on invalid provenance or mandatory checks; avoid administrative holds unrelated to actual prerequisites.

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
