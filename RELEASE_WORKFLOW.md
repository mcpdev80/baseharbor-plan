# Release lifecycle

Every concrete release has six visible task cards. Planning is live on `main`; product changes retain their own PR/review rules. Creating a card is neither acceptance nor authorization to execute a release.

| Stage | Result | Boundary |
| --- | --- | --- |
| Cleanup | Previous leftovers reconciled | Before new development |
| Updates | Renovate intake integrated and baseline recorded | Before feature development |
| Prepare | Complete ecosystem pre-release readiness | No complete pre-release yet |
| Qualify | Complete authenticated pre-release approval | Explicit Maintainer run authorization |
| Publish | Approved promotion and exact tagging command | Separate merge/tag/publication authorization |
| Verify | Published artifacts, Pages and closeout verified | Tag push alone is insufficient |

## Binding sources

Read the current product sources at execution time; this page is a short planning entry, not a second release contract:

- [Canonical release audit](https://github.com/mcpdev80/baseharbor/blob/develop/docs/internal/pre-release-documentation-audit.md), including its readiness vocabulary, complete ecosystem checklist and sections 1–13.
- [Releases and versioning](https://github.com/mcpdev80/baseharbor/blob/develop/docs/reference/releases.md), [readiness](https://github.com/mcpdev80/baseharbor/blob/develop/docs/development/pre-release-readiness.md), [development rules](https://github.com/mcpdev80/baseharbor/blob/develop/docs/DEVELOPMENT_GUIDELINES.md) and [agent/CI rules](https://github.com/mcpdev80/baseharbor/blob/develop/AGENTS.md).
- Actual [pre-release workflow](https://github.com/mcpdev80/baseharbor/blob/develop/.github/workflows/pre-release.yml), [resume/evidence verifier](https://github.com/mcpdev80/baseharbor/blob/develop/scripts/pre-release-resume.py), [promotion verifier](https://github.com/mcpdev80/baseharbor/blob/develop/scripts/release-handoff.py), [release workflow](https://github.com/mcpdev80/baseharbor/blob/develop/.github/workflows/release.yml) and [Pages workflow](https://github.com/mcpdev80/baseharbor/blob/develop/.github/workflows/pages.yml).

Source inspection on 2026-10-17 used product `develop` at `b73e27603ee082f2fabb81df1b2789fba3367d23`. Historical release-specific exceptions do not automatically apply to the next release. The audit still contains older wording about one run reproducing every gate; actual workflows support authenticated resumed coverage. Preparation must reconcile documentation against the actual candidate-owned verifier before execution, rather than demanding unrelated green jobs be repeated or weakening approval requirements.

## Cleanup

Inventory all relevant product/consumer/planning PRs, task claims, branches and CI. Close only superseded/incorporated work with a reason and destination. Preserve active future work, unmerged required changes, other owners, immutable tags, protected refs and retained evidence. Remove incorporated temporary branches under existing retention rules. Record what was removed, retained and deferred; do not turn migration closure or housekeeping into product acceptance.

## Updates

Process all pending applicable Renovate updates first: dependency dashboard, grouped/superseded PRs, manifests/locks, action/toolchain/container pins across BaseHarbor, Demo, Console and Connector (and plan tooling if present). Review, integrate and run sufficient impact-based checks through existing product PRs before feature development. Fix actual conflicts/failures. Incompatible/unverified updates remain an explicit blocker until corrected or the Maintainer records a deliberate exclusion; no blind auto-merge or silent omission. Record the resulting immutable baseline. Later arrivals remain normal dependency intake; candidate changes re-enter affected qualification.

## Prepare

Apply audit sections 1–8 and section 9 atomic-first prerequisites. The Prepare card depends on both startup cards and every scoped implementation task, including newly added tasks. Also inspect release/epic requirements that have no leaf task yet, and any explicitly deferred acceptance/test debt. Zero children is not completed scope.

Readiness includes BaseHarbor, Demo, Console, Node Connector, current CLI/JSON/MCP/HTTP semantics, real supported auth/mTLS/lifecycle/cleanup and developer journeys, standards/ownership/security review, EN/DE user/reference/spec docs, navigation/links/staleness, strict Pages candidate builds/workflow, changelog and concise developer-facing release notes. Notes cover what changed, why it matters, usage/upgrade/compatibility, security and deliberate deferrals. The product README stays compact and free of process rules. Do not publish Pages to claim readiness.

Freeze exact actual ecosystem sources, immutable consumer bindings, candidate tree and release-specific gate inventory/evidence plan without circular pins. Check the required platform/runtime/HA/consumer coverage, current source qualifiers and available tooling. Missing/failed/skipped/unverified required coverage blocks readiness. Produce an exact-source dossier and concrete run inputs for review. Preparation alone authorizes no complete pre-release, merge, tag or publication.

## Qualify

Require accepted preparation plus explicit Maintainer authorization. Use existing workflows, original gate owners and verifier; inspect queued/running equivalent work before dispatch. No full-matrix debugging loop or duplicate orchestrator.

An overall failed workflow may contain valid successful individual receipts. Reuse these only when the existing verifier authenticates compatible inputs, source/gate/runtime/resource profile, origin run/attempt/artifact/digest and freshness. A newer relevant negative attempt blocks stale-green fallback. Fix demonstrated failures and rerun only failed, missing or affected gates. Cache is not evidence; not-required needs a reason and is not PASS. Do not assume cross-SHA compatibility.

Final complete approval must include every unique required gate and immutable ecosystem input through the canonical coverage verifier and `release-approved.json`. Targeted `only_gates` runs never authorize a release. Current `pre-release.yml` accepts `tag`, exact source `ref`, exact `demo_ref` and an exact `consumer_ref` when applicable; inspect the candidate workflow for release-specific changes. Store the actual dispatch and approval origin in the task. Green source CI alone is insufficient.

## Publish

Require complete approval and separate Maintainer authorization. Use one release/promotion PR and the existing candidate/promotion model, with strict review/CI. Inspect `develop` versus `main`, main-only hotfixes and the exact tree. Do not accidentally promote work added to develop after the approved candidate; do not improvise branch/ruleset bypasses.

Before completion, the Publish task MUST contain a complete executable tagging block for the Maintainer, with the actual release version and full approved resulting main SHA. It must verify the correct repository/remote, clean state, exact fetched main/tree and approval binding, absence of local AND remote version tags, then create an annotated immutable tag on that explicit SHA and push only that tag. No placeholders, unverified SHA or `git push --tags`. If authorization is to prepare only, deliver the commands without executing them. If execution is authorized, record the actual tag/publish run separately.

The existing release workflow consumes matching immutable approval and performs only required supplemental/publication work. Never move an existing published tag. A prepared command is not a pushed tag or verified publication.

## Verify

Complete audit sections 10–13: immutable tag/main/tree, GitHub Release, required archives/checksums and actual `baha version` version/commit metadata, build/runtime provenance, matching versioned GHCR image and required compatible/latest channels. Verify actual post-promotion Pages deployment and live EN/DE release notes/navigation/roadmap/references, plus release-mode Demo/consumer dispatch where required. Candidate Pages builds are not live deployment evidence.

Record actual results in the audit and release/task notes; qualify/publish only with accepted evidence. Reconcile roadmap/current-version/next-release messaging and remove incorporated temporary branches/obsolete PRs under retention rules. Do not call a pushed tag release completion, and do not rerun qualified runtime gates merely for publication.

## Maintain the cards

After adding a concrete release note or an explicitly scheduled patch version:

```bash
python3 scripts/release_cycles.py sync
python3 scripts/plan.py check
python3 -m unittest discover -s scripts/tests
```

The synchronizer creates missing cards from `templates/release-cycle/`, preserves existing IDs/owners/status/evidence/handoffs and refreshes required dependencies and views. The validator rejects missing/duplicate stages, missing preparation prerequisites and future feature tasks lacking startup intake. It does not mark any stage accepted. New scope requires another sync; closed readiness must be reopened/requalified when scope changes, never silently grandfathered.

Concrete versions come from numeric `kind: release` notes, explicit task `version` fields and optional `cycle_versions` lists in series notes (v0.5.0 is explicitly scheduled in v0.5.x). Backlog, triage, maintenance and unspecified `x` versions do not invent releases or tags. The six stages also apply to subsequently scheduled hotfixes.

v0.4.26 was already in development when these cards were added: its startup cards are honest catch-up work, not retroactive acceptance or a rewrite of active/accepted product tasks. Future release implementation depends on accepted startup cleanup/updates. No production run, merge, tag or publication was authorized by this planning change.
