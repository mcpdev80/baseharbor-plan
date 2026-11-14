# Release lifecycle

Every future concrete release has six visible task cards. The already-running v0.4.26 has only the four completion cards; its startup is not replayed. Planning is live on `main`; product changes retain their own PR/review rules. Creating a card is neither acceptance nor authorization to execute a release.

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

The current Owner instruction removes CI evidence manifests, verification/reuse and extra receipt approvals everywhere. Historical release records are preserved. Actual product tests, immutable source pins, published artifact checksums and build provenance remain required.

## Cleanup

Inventory all relevant product/consumer/planning PRs, task claims, branches and CI. Close only superseded/incorporated work with a reason and destination. Preserve active future work, unmerged required changes, other owners, immutable tags, protected refs and retained evidence. Remove incorporated temporary branches under existing retention rules. Record what was removed, retained and deferred; do not turn migration closure or housekeeping into product acceptance.

## Updates

Process all pending applicable Renovate updates first: dependency dashboard, grouped/superseded PRs, manifests/locks, action/toolchain/container pins across active BaseHarbor and Demo repositories (and plan tooling if present); archived Console and Node Connector are excluded. Review, integrate and run sufficient impact-based checks through existing product PRs before feature development. Fix actual conflicts/failures. Incompatible/unverified updates remain an explicit blocker until corrected or the Maintainer records a deliberate exclusion; no blind auto-merge or silent omission. Record the resulting immutable baseline. Later arrivals remain normal dependency intake; candidate changes re-enter affected qualification.

## Prepare

Apply audit sections 1–8 and section 9 atomic-first prerequisites. The Prepare card depends on the completed Updates stage (no retroactive startup cards for v0.4.26), not on every feature card. It can track release-readiness preparation while development proceeds. CardBoard feature cards and epics remain the authoritative progress view. **Qualification**, not Prepare, requires all scoped implementation, CI, docs and consumer tasks to be accepted. Preparation does not grant permission to qualify, publish, or tag. Newly added scope must also be complete before qualification or any later accepted release stage; the release-cycle validator enforces this even after scope changes. Also inspect release/epic requirements that have no leaf task yet, and any explicitly deferred acceptance/test debt. Zero children is not completed scope.

Readiness includes active BaseHarbor and Demo, current CLI/JSON/MCP/HTTP semantics, real supported auth/mTLS/lifecycle/cleanup and developer journeys, standards/ownership/security review, EN/DE user/reference/spec docs, navigation/links/staleness, strict Pages candidate builds/workflow, changelog and concise developer-facing release notes. Notes cover what changed, why it matters, usage/upgrade/compatibility, security and deliberate deferrals. The product README stays compact and free of process rules. Do not publish Pages to claim readiness.

Freeze exact actual ecosystem sources, immutable consumer bindings, candidate tree and release-specific test inventory without circular pins. Check the required platform/runtime/HA/consumer coverage, current source qualifiers and available tooling. Missing/failed/skipped/unverified required coverage blocks readiness. Produce an exact-source test plan and concrete run inputs for review. Preparation alone authorizes no complete pre-release, merge, tag or publication.

## Qualify

Require accepted preparation plus explicit Maintainer authorization. Freeze the actual candidate and ecosystem source pins. Use the normal Pre-Release jobs and canonical test inventory; inspect queued/running equivalent work before dispatch. Required job results determine success. Missing, failing, cancelled or improperly skipped required work blocks. During diagnosis rerun failed or affected tests, not unrelated full matrices.

No gate manifests, archived evidence reuse, Actions run/job re-verification or release-approved.json is produced or consumed. Targeted `only_gates` execution validates only the chosen scope. Complete pre-release validation executes every required test on the exact source inputs. A successful CI receipt never authorizes promotion or publication.

## Publish

Require complete validation and separate Maintainer authorization. Use one release/promotion PR and verify the resulting Git tree against the intended frozen candidate, including main-only hotfixes. Do not promote later unrelated develop changes or bypass actual technical gates.

Before completion provide one complete executable tagging block with the actual version and full resulting main SHA. Verify repository/remote, clean state, fetched main/tree and local/remote tag absence. Create an annotated immutable tag on that explicit SHA and push only that tag. If only preparation is authorized, do not execute it. Never move a published tag.

The normal Release workflow validates the tag and directly runs reusable pre-release checks on that exact source before publishing images, binaries, checksums, human release notes and build provenance. It does not consume an approval artifact or query earlier CI runs. A prepared command is not a pushed tag or a verified publication.

## Verify

Complete audit sections 10–13: immutable tag/main/tree, GitHub Release, required archives/checksums and actual `baha version` version/commit metadata, build/runtime provenance, matching versioned GHCR image and required compatible/latest channels. Verify actual post-promotion Pages deployment and live EN/DE release notes/navigation/roadmap/references, plus release-mode Demo/consumer dispatch where required. Candidate Pages builds are not live deployment evidence.

Record actual results in the audit and release/task notes; qualify/publish only after the required checks succeed. Reconcile roadmap/current-version/next-release messaging and remove incorporated temporary branches/obsolete PRs under retention rules. Do not call a pushed tag release completion, and do not start duplicate validation while equivalent jobs are running.

## Maintain the cards

After adding a concrete release note or an explicitly scheduled patch version:

```bash
python3 scripts/release_cycles.py sync
python3 scripts/plan.py check
python3 -m unittest discover -s scripts/tests
```

The synchronizer creates missing cards from `templates/release-cycle/`, preserves existing IDs/owners/status/evidence/handoffs, clears obsolete per-feature Prepare dependencies, and refreshes required stage dependencies and views. The validator rejects missing/duplicate stages, missing preparation prerequisites and future feature tasks lacking startup intake. It does not mark any stage accepted. New scope requires another sync; closed readiness must be reopened/requalified when scope changes, never silently grandfathered.

Concrete versions come from numeric `kind: release` notes, explicit task `version` fields and optional `cycle_versions` lists in series notes (v0.5.0 is explicitly scheduled in v0.5.x). Backlog, triage, maintenance and unspecified `x` versions do not invent releases or tags. The six stages also apply to subsequently scheduled hotfixes.

v0.4.26 was already in development when this policy was added. Its two mistakenly introduced startup cards were removed by explicit Maintainer instruction; their IDs remain reserved in Git history and must not be recreated or reused. Its four preparation/qualification/publication/verification cards remain. Future release implementation depends on accepted startup cleanup/updates; no active or accepted v0.4.26 product task is rewritten. No production run, merge, tag or publication was authorized by this planning change.
