---
id: core-888
title: Streamline development and CI
status: open
release: v0.4.26
parent: v0.4.26
sources: ["mcpdev80/baseharbor#888"]
---
# core-888 · Streamline development and CI

Source: [baseharbor#888](https://github.com/mcpdev80/baseharbor/issues/888). Child tasks: [views/epics.md](../views/epics.md#core-888). Release: [v0.4.26](../releases/v0.4.26.md).

## Binding dependency correction — 2026-10-15

Implementation order: **#892 → #893 planning/execution interface → #896 isolated runner implementation → #893 final runtime/evidence integration and acceptance.** #896 does not depend on completion or merge of all of #893.

In this vault the two #893 phases are separate entries so the order has no cycle:
[core-893-interface](../tasks/core-893-interface-agree-planning-execution-interface.md) → [core-896](../tasks/core-896-runners-isolate-parallel-pr-checks.md) → [core-893](../tasks/core-893-ci-enforce-selected-pr-checks.md) → [core-895](../tasks/core-895-reviews-require-maintainer-approval.md).

- PR #930 at `d56737bd147e54733c280383fa86ad2abccc7b33` is the interface reference, **not a qualified or merged dependency**. Inspect its latest head and agree the concrete interface before editing. Do not execute privileged untrusted code or claim missing gates as successful.
- #893 owns `.github/workflows/ci.yml`, PR planning/execution orchestration, authenticated gate-evidence consumption and the `PR Selected Checks` status.
- #896 owns dedicated runner-isolation helpers and tests: per-run Target/volume/port/state isolation, trust boundaries, cleanup and capacity. It is a separate small PR against develop; do not copy #930 wholesale or edit its owned files in parallel.
- Interface changes are agreed first and the shared-file integration is sequenced through the #893 owner. Inspecting an exact commit does not authorize unreviewed production activation.
- Qualify #896 with focused isolation fixtures and the two necessary small isolated pilot lanes; then integrate it and let #893 consume it. #893 stays open until authenticated runtime evidence and its Backup/Restore pilot pass.
- Required review/check protection (#895) follows a qualified #893 status check. Product implementation still requires the qualified #890–#893/#895/#896 foundation.
- One assigned task per session; stop after its handoff. No full pre-release, merge, tag or publication is authorized by this correction.

**Repository language:** issue titles, PR titles, section headings and contributor/agent instructions are English, titled `[release] Area: concrete outcome`. Public documentation keeps EN/DE parity.

## Goal and boundary

From v0.4.26: small independent PRs, understandable CI and targeted tests. `develop` integrates, `main` holds released source; release candidates are frozen separately. v0.4.25 (#872/#881) stayed on its earlier procedure. This epic coordinates and accepts; it is not a shared implementation branch. One reviewable result per task/PR. No new product architecture, provider, migration or generic CI/feature-flag framework.

## V1: deliberately conservative

Select every necessary check; extra checks are allowed. No claim to the mathematically smallest test set.

- A small versioned mapping **area/package → existing gates**, with documented shared inputs and consumers. Use existing Go tooling; do not build a universal change-impact analyzer.
- Compute changes against the real PR merge base, including deletes/renames. A missing or ambiguous base means an explained broader selection.
- A narrow selection accounts for actually affected packages and known consumers. Build tags, OS/arch, test imports, embedded/generated assets and external consumers count; when their effect is not reliably captured, broaden.
- Shared runtime/ownership/auth/TLS/schema/toolchain/image/policy changes propagate to every affected area.
- Current trusted coverage contract (#942, accepted): unknown/unqualified impact remains explicit `unresolved` and blocks the final check; it does not automatically launch the full release catalog. Qualify the actually required targeted checks independently before assignment/integration. No silent exemption via file names, skip labels or commit markers.
- The plan records base/head/integration SHA, selected gates and the reason. Planning uses trusted rules; a PR cannot switch off its own checks.
- An always-running required final check verifies the plan and every required result. Failed, missing, improperly skipped or cancelled blocks. "Not required" is not PASS.

**Stop rule:** validate the V1 selection with two representative correction rounds. If a narrow rule stays unstable, fall back to the documented conservative mapping plus broader checks. No further analyzer refinement is a prerequisite for #873; further optimization gets its own later item with a concrete benefit.

## Autonomous task readiness — 2026-10-16

Follow [executable task slices](../WORKFLOW.md#executable-task-slices). The next explicit prerequisite is [wizard-task CI readiness](../tasks/t-20261016-wizard-task-ci-readiness.md), not another product implementation session operating private pilots. It owns the complete trusted planning/execution/final-check delta. Component tasks own disjoint files and their full verification after this baseline is integrated. core-894 follows this shared CI writer. No per-task full release matrix and no message relay through the Maintainer.

## Work packages

| Package | Result |
| --- | --- |
| 1 · Process and docs | Short central rules, contributor/LLM entry points and templates (#890, closed) |
| 2 · PR test plan | Real diff base, conservative mapping, verified fallbacks (#891, #892, closed) |
| 3 · CI and presentation | Plan, selected jobs, required final check, readable summary (core-893, core-894) |
| 4 · Review and runners | Maintainer approval, solo exception, isolated trusted runners (core-895, core-896) |
| 5 · Candidate and evidence | v0.4.26 pins, existing verifier, safe promotion/forward-port/retention (#897–#899 closed, core-900) |
| 6 · Pilot | Qualify small parallel PRs and selection correctness; own the before/after record of run times, runner minutes and remaining cost (core-901) |

**Package 4 is minimum scope before foreign PRs are integrated regularly.** Early everyday operation needs #890–#893, #895 and #896. #894 improves presentation; #897–#900 must be complete before release acceptance. #901 documents the pilot and does not block already-qualified early product work.

## Tests and run time

Existing green runs are the starting point; **no new measurement campaign and no extra full matrix just for benchmarking.**

| Successful jobs | Docker | Podman |
| --- | ---: | ---: |
| [37713017303](https://github.com/mcpdev80/baseharbor/actions/runs/37713017303): complete journey | 25.4 min | 26.1 min |
| same run: Guided | 4.3 min | 5.1 min |
| same run: Backup/Restore | 7.5 min | 10.8 min |
| [37335642463](https://github.com/mcpdev80/baseharbor/actions/runs/37335642463): Guided | 3.5 min | 4.5 min |
| same run: Backup/Restore | 8.5 min | 9.3 min |
| [38642797305](https://github.com/mcpdev80/baseharbor/actions/runs/38642797305): Identity | 4.0 min | 4.7 min |

Job wall-clock times, not a statistical baseline. Historical greens are cost references, not acceptance of new candidates. A shared binary/image build already exists.

- Check logic/contracts without containers; provider integration with the services it needs. Reproduce failures first with a small regression test, then add the necessary native/consumer evidence.
- No complete journey for every PR. End-to-end transitions and unclear impact still need the relevant journeys; a mere package import does not.
- Look for proven waste in existing logs/scripts: duplicate starts, fixed sleeps, serial independent steps. Real readiness instead of blind waiting; keep bounded timeouts.
- Run Docker/Podman and independent scenarios in parallel within real runner capacity. No shared mutable Targets/volumes; no reused secret/recovery/provider state.
- Record before/after only from necessary regular runs: SHA, runner, scope, wall time/runner minutes. Promise no savings before they are shown.
- No expensive duplicate PR/push testing without changed inputs. Cancel only within the same PR lane; never displace other PRs/candidates. Forks get no secrets or privileged self-hosted runners.

## Evidence and release

Use the existing verifier/collector and gate catalog; no second authority.

- Reuse green evidence only with proven equality of bound inputs; check origin, run/attempt, artifact digest, schema, requirements, consumer pins and cleanup. Newer relevant negative attempts prevent falling back to old greens.
- Selecting a test now does not permit reusing old evidence. Cache is not evidence.
- V1 may keep the existing conservative fingerprint policy. Gate-specific fingerprints are an optional later optimization, not a start blocker. Changes only with a new qualified policy for v0.4.26+; never reinterpret old v0.4.25 receipts.
- Real immutable BaseHarbor/Demo/Console/Connector pins and complete required release coverage stay mandatory, including CLI/JSON/MCP, EN/DE docs, Pages candidate build and release notes.
- Freeze the candidate from verified `develop`; development may continue. Fix PRs target the candidate line, then forward-port to `develop`.
- Promote only the separately approved candidate; never take a later `develop` wholesale to `main`. Verify handoff/squash/ancestry rules with fixtures.
- GC protects open PRs, active candidates and needed evidence origins until the end of their defined use/retention. Production Pages only after promotion.

## Review rule

PRs from other contributors into develop need Maintainer (@mcpdev80) approval and green required checks; new commits invalidate the approval. The Maintainer may merge their own PRs without a second review for now; the PR and required green checks stay mandatory. Document once, centrally, using the role name **Maintainer**. Enforce with available rulesets/CODEOWNERS and read the result back. Keep review and CI protection separate where possible. GitHub bypass is not automatically limited to own PRs: this is a transparent solo-maintainer compromise, not a claimed author-based security guarantee. No direct push and no blanket contributor bypass.

## Readable Actions

- Short titles, e.g. `PR #901 · Edit wizard`; jobs e.g. `Identity · Docker`.
- Generate only needed matrix entries from the plan; no wall of skipped static jobs. Name unavoidable platform displays openly.
- Summary: **trigger, checked, reused, not required, failed/blocked, next action**; short names, durations and links; technical detail collapsible.
- Few graph stages: planning → selected checks → final check. Technical gate IDs and SHAs live in details/artifacts.
- Align display names with required checks and the verifier; do not break historical IDs for cosmetics.

## Short docs for people and LLMs

No process rules or extra process links in the product README. `docs/DEVELOPMENT_GUIDELINES.md` (+ German counterpart) holds the short central rules; `CONTRIBUTING.md`, `AGENTS.md` and `.github/copilot-instructions.md` link to them. Issue/PR templates cover result, dependencies, acceptance and tests/evidence. Keep the title scheme `[release] Area: outcome`; invent no patch assignment.

## Acceptance

- Twelve task issues created (#890–#901); native sub-issue/dependency links still to be added. Own small PRs, two independent tasks in parallel and one shared-interface case without overwriting, qualified.
- Selection/fallback verified for prose, Go/CLI, Docker-only, shared runtime/security and unknown impact; deletes/renames, consumers and relevant shared inputs covered.
- Missing/negative results and self-exemption block; integration-state checks after base changes/conflict resolution done.
- Review rule including the solo exception and CI protection qualified in practice; actual GitHub limits documented.
- Actions readable; necessary tests run and the pilot demonstrably saves effort or documents remaining cost.
- Candidate promotable correctly despite ongoing develop; pins, evidence and GC/handoff preserved.
- EN/DE docs and all entry points agree; README stays free of process rules.
- v0.4.25 unchanged; no full pre-release/tag/release without separate approval.

## Inspected baseline

Inventory of 2026-10-15 at candidate `1efb0baf7d1bc44a928e3a934b1f8b3bde2ada83`; check the current published state before implementing. Relevant sources: `.github/workflows/ci.yml`, `targeted-integration.yml`, `pre-release.yml`, `scripts/pre-release-resume.py` (conservative fingerprints), `targeted-atomic-plan.py` (not a general impact analyzer), `ecosystem_release_pins.py`, `release-handoff.py`, `ci-workflow-policy.sh` (workflow allowlist), `artifact-gc.yml`, `docs/reference/releases.md`. Rulesets 23754541/23754542 had 0 required reviews and no required status checks when read; check classic branch protection separately.

Closed tasks of this epic (historical context, not migrated): #890 rules/entry points, #891 diff base, #892 area-to-gate mapping, #897 ecosystem pins, #898 evidence policy, #899 candidate promotion — all closed as completed on 2026-10-15.
