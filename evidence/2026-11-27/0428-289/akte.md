# Evidence — 0428-289 Detect mixed Compose providers

Lane: w399-0428-289-providers · Card: t-20261116-r28-bug-provider-discovery · Repo: baseharbor (area: wizard)

## Root cause of Trusted Plan (verified)

The Trusted Plan executes scripts/pr-gate-plan.py from the BASE/controller checkout (ci.yml "Resolve exact immutable PR inputs using trusted base policy": checkout ref = ${{ github.event.pull_request.base.sha }}; planner line 1902-1904 loads ROOT/'pr-gate-coverage.json' = the controller catalog; fail-loud guard lines 1946-1952 aborts when a changed cmd/ or internal/ source has no row in the BASE catalog). Catalog rows added inside this PR are therefore invisible to the gate — my same-PR fix commit 8c7f54b679 cannot turn Trusted Plan green. Local reproduction (pr-diff of head 8c7f54b679 vs ea5218d7 through the controller planner) raises the identical ValueError. Required route: a catalog PR adding the three source rows (capability_detection_runtime.go, compose_analysis.go, compose_detection.go; surfaces = the atomic docker/podman capabilities their siblings carry) to develop FIRST, then this candidate rebases/absorbs develop and qualifies. The w399 test file is NOT a source component; its row is optional (the in-PR row stays as harmless pre-registration).

## Gate catalog addition (in this PR, context)

Hosted run 46011069186 (event pull_request, head 8fe1b3a5ad, conclusion failure) failed at "PR · Trusted Plan": `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner` for the four new/changed sources under internal/repositoryinspect (validate-pr-gate-coverage.py:98). First fix attempt: 4 component rows in this PR (commit 8c7f54b679); run 2 46011641329 failed IDENTICAL (Trusted Plan reads the base catalog, see Root cause).

## PR + CI state

- Orphan-ref witness (coordinator step 1, one sentence): refs/heads/lane-0428-289-provider-discovery tip = commit 95b683472638586dc8eb76712cb436daed3c95a1, author w335-0428-318-lowpair@baseharbor.local, 2026-11-26, stale base 5a37ddbd, not-in-develop, contained in NO PR — documented only, not touched (witness for later cleanup disposition).
- Product PR: mcpdev80/baseharbor#1880, base develop, head branch lane-0428-289-provider-discovery-providers-2 (coordinator option c), head 8c7f54b679bc75a258040b5d38c6e84533add7f2.
- Delivery proof: git ls-remote lane-origin refs/heads/lane-0428-289-provider-discovery-providers-2 -> 8c7f54b679; refs/pull/1880/head follows head.
- Run 1: 46011069186 pull_request event, head 8fe1b3a5ad, TERMINAL conclusion failure (Trusted Plan catalog error; downstream "REJECT: Go test selection missing or invalid").

## PLAN

1. Create numbered work plan in all three places (board file, evidence PLAN, todos) — DONE
2. Verify environment: remote -v, real plan repo path, pull current state — DONE
3. Read card contract + baseharbor/AGENTS.md + DEVELOPMENT_GUIDELINES — DONE
4. Claim the card, pull-before-push, forward-only push to plan main — DONE (plan commit 5725634c0)
5. Set up isolated worktree + base attestation — DONE
6. Reproduce the bug: verify provider-detection path in code, confirm mixed provider misidentification — DONE (code + CLI witness)
7. Implement fix: distinguish SQL Postgres/pgvector vs MongoDB, scrutinize scraper-like services, verifiable S3 ID — DONE (candidate 8fe1b3a5, local)
8. Keep existing safety gates unchanged (consent, ownership, isolation) — DONE (only repositoryinspect touched)
9. Add positive AND negative regression tests in existing package test-scaffold — DONE (inspect-package-tests route; no ci.yml change)
10. Classify baseline-red vs candidate-green — DONE (baseline vs candidate inspect witness)
11. Run local pre-checks: format/vet/build only — DONE (all pass)
12. Commit under canonical lane identity — DONE locally (8fe1b3a5, %an=w399-0428-289-providers); push BLOCKED by foreign orphan ref (see Findings + QUESTION)
13. Push branch, open PR against develop, prove delivery — DONE (PR #1880, head 8c7f54b679, ls-remote delivered)
14. Monitor own hosted CI runs — DONE (run 1 46011069186 failure; run 2 46011641329 failure; root cause = base-catalog gap, cannot fix in-PR without scripts/pr-gate-coverage.json edit)
15. Publish evidence akte to plan origin/main — DONE via plan PR #234 (branch evidence-0428-289-w399)
16. Move card to review (card-status.py) — pending coordinator answer (route decision)
17. END line with candidate SHA — QUESTION posted 2026-11-27 (catalog route)

## Canonical commit identity (per AGENTS / owner ruling 2026-11-26)

- Lane full canonical name (VERBATIM from this mission's `worker` dispatch): w399-0428-289-providers
- Card frontmatter owner field: currently `owner: w399-0428-289-providers` after my claim (will re-read from origin/main at handoff)
- git user.name = w399-0428-289-providers
- git user.email = w399-0428-289-providers@baseharbor.local
- Invocation (every commit/merge): `git -c user.name=w399-0428-289-providers -c user.email=w399-0428-289-providers@baseharbor.local commit ...`
- Pre-push gate line (run before every push): `git show -s --format=%an HEAD` must equal `w399-0428-289-providers` exactly; on mismatch STOP + report (no silent amend)

## Base attestation

- Real product remote URL: https://github.com/mcpdev80/baseharbor.git (verified via `git ls-remote`, NOT the quarantined workers/baseharbor checkout whose origin points at baseharbor-plan.git)
- develop SHA cut from: ea5218d72e263f21e79853b679af50074dab8c25 (refs/heads/develop @ ls-remote)
- develop head subject: `fix(0428-288): preserve Compose service IDs through workload preflight (#1833)`
- Ancestor proof: `git merge-base --is-ancestor origin/develop HEAD` -> true (origin/develop IS ancestor of HEAD)
- `git log --oneline origin/develop..HEAD` at branch creation: empty (only my own commits will appear)
- Plan repo remote: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan origin -> baseharbor-plan.git (verified `git remote -v`)

## Findings (investigation)

Detection chain: `baha app init` (cmd/baha/app_init_detection.go:72) → `repositoryinspect.AnalyzeComposeFile` (internal/repositoryinspect/compose_analysis.go:72) → `detectComposeServices` (internal/repositoryinspect/compose_detection.go:43). The wizard's provider proposal is built from composeService flags (Postgres/MongoDB/ObjectStorage/Ambiguous), so the bug lives entirely in this package — no workflow/ci.yml touch.

Baseline misclassification on the J-Commerce fixture (services with keyword-carrying images):
- vector_db (image pgvector/pgvector:pg16): NOT detected as Postgres. Detection only matched "postgres"/"postgresql"; the "pg" token was in NO marker at all, so pgvector images were dropped → "omitted vector_db".
- floci (S3 emulator, e.g. localstack/localstack): NOT detected as object storage (markers were minio/seaweedfs/radosgw only).
- Any service name containing "pg" (e.g. a "db-scraper" using a `pg`-prefixed tool, or the substring "pg" in "postgresql") — the "six Postgres" inflation — after adding a naive "pg" match would misclassify scrapers. Fix: never match bare "pg"; classify pgvector only via its image word.

Env-var detector (capability_detection_runtime.go sqlSignals/documentDatabaseSignals:50,74): DATABASE_URL/POSTGRES_URL/MONGODB_URL/MONGO_URL only — note it does NOT include PG_URL (the J-Commerce variable). That gap only bites when a provider image carries no keyword; not part of the reproduction transcript. Left unchanged (minimal scope; would need its own red-first evidence).

BLOCKER (stop condition): remote refs/heads/lane-0428-289-provider-discovery already exists = commit 95b683472638586dc8eb76712cb436daed3c95a1, author w335-0428-318-lowpair@baseharbor.local (dated 2026-11-26), based on an older develop (5a37ddbd), containing a DIFFERENT 0428-289 implementation ("classify via env-var evidence + flag scraper services" + provider_discovery_jcommerce_test.go). No PR references it; it is not in develop; card owner on origin/main before my claim was "". My claim (commit 5725634c0, owner w399-0428-289-providers, status active) is authoritative. NOT force-pushing over a foreign candidate and NOT creating a second branch; asked coordinator via QUESTION. My candidate is ready at 8fe1b3a5 (clean descendant of develop ea5218d72e). Evidence published via plan PR #234 (branch evidence-0428-289-w399 @ 5a92cac8d; main is protected, no direct push).

## Reproduction

Baseline witness via CLI binary (non-test check on this host): built develop ea5218d7 (`baha-baseline`) and candidate `baha-w399`, ran `baha inspect --json --no-input` on /tmp/opencode/w399-jcommerce (J-Commerce-shaped compose: app + product_db[mongo:7] + vector_db[pgvector/pgvector:pg16] + floci[localstack/localstack:3] + identity-db-scraper + orders-scraper).

BASELINE (ea5218d7):  app=None, floci=None, identity-db-scraper=None, orders-scraper=None, product-db=database.document, vector-db=None
CANDIDATE (w399):    app=None, floci=storage.object, identity-db-scraper=None, orders-scraper=None, product-db=database.document, vector-db=database.sql

Delta proves: pgvector now SQL (red→green), localstack now object storage (red→green), scrapers correctly NOT SQL, MongoDB still document. Binding names preserved (vector-db/product-db slugify naming untouched). Go regression test TestComposeDetectionDistinguishesMixedJCommerceProviders asserts the same through AnalyzeComposeFile (red on baseline via SQLInstances/ObjectStorageServices misses; green on candidate).

## Implementation

Candidate commit 8fe1b3a5 (branch lane-0428-289-provider-discovery, local only pending coordinator disposition of the foreign-orphan blocker):
- internal/repositoryinspect/compose_detection.go: extract composePostgresMarker (postgres|postgresql|pgvector, bare "pg" deliberately excluded), composeMongoDBMarker (mongo), composeScraperMarker (scraper); image-driven scraper suppression (an image that is only a scraping tool, e.g. */*-scraper, never counts as Postgres even if its name matched); add ScrapingService flag; volume-reclaim guard no longer treats scraper services as replaced Postgres providers.
- internal/repositoryinspect/compose_analysis.go: comment + pgvector handled via markers; NO logical-name change → valid app binding names preserved (acceptance).
- internal/repositoryinspect/capability_detection_runtime.go: composeObjectStorageMarker now recognizes localstack/moto/zenko/storageos (floci-class S3 emulators) — identifies verifiable S3 use WITHOUT claiming floci equals a canonical S3 provider.
- internal/repositoryinspect/w399_provider_discovery_repro_test.go: TestComposeDetectionDistinguishesMixedJCommerceProviders (positive+negative; RED on baseline for SQL/ObjectStorage assertions, GREEN on candidate; asserts scrapers absent from SQL/Infrastructure) and TestComposeDetectionKeepsPostgresProviderMarkers (guards the marker boundary: postgres:16 yes, bare "pg" no).

Safety gates: untouched. No consent, ownership, isolation or preflight logic changed. Only detection classification code in internal/repositoryinspect.

## Tests + CI route

Route: scripts/pr-gate-plan.py:456 'inspect-package-tests' runs `go test ./internal/repositoryinspect/ -count=1` (package-wide discovery — my tests are discovered automatically) plus the `go test ./...` path (ci.yml). No REQUIRED_CLIENT_TESTS-style list exists for this package; doctrine allows package discovery. Path selector: edits under internal/repositoryinspect/** select inspect-package-tests. NO change to .github/** needed (finding: none).

## repo-rule compliance

- No workflow/ci.yml change; tests registered in existing package discovery (AGENTS: never a per-test registration list for ordinary Go unit tests).
- No local test execution (CI policy); verification via non-test build/vet + CLI inspect binary; red/green classification recorded in evidence.
- Remote truth measured only via `git ls-remote`/`git fetch` of https://github.com/mcpdev80/baseharbor.git; the workers/baseharbor checkout (origin→plan URL) is quarantined, unused.
- Plan writes: claim commit 5725634c0 touched only my card + generated views, explicit paths, forward-only push to plan main (accepted by protection); evidence will publish via plan PR (protected main).
- No product-PR merge; no force-push; candidate descends from exact develop head ea5218d7 (ancestor proof above).

## cleanliness

docker ps -a before: (no containers started by this lane; no VM/compose work — tests run in hosted CI)
docker ps -a after: none. No compose project created; no scratch in ecosystem root (worktree in /tmp/opencode/w399-0428-289-providers-wt, baseline in /tmp/opencode/w399-baseline, fixture in /tmp/opencode/w399-jcommerce).

## Final state (coordinator instruction 2026-11-27T14:06Z)

- NO second catalog PR: develop catalog path is frozen by a task-specific Owner hold (#136 baseline + fan-in #1861/#1862/#1863); a lane-side catalog-only PR would be the forbidden implicit lift. My option-(c) execution judged correct/clean.
- Candidate 8c7f54b679 rests on PR #1880 — no further pushes, no new branches (Eigenes-Run-Pflicht fulfilled: both run IDs observed terminal by this session).
- Card 0428-289 moved to wait via card-status.py (coordinator Nachlauf 2026-11-27T14:10Z ordered normal push to plan main): published as plan commit, verified on origin/main (owner=w399-0428-289-providers, kanban_status=wait, prs=[mcpdev80/baseharbor#1880], wait_reason per instruction with run witnesses 46011069186/46011641329). The earlier branch+PR attempt (#236) is superseded by the direct push and can be closed by the coordinator.
- Orphan-ref findings remain as documented (no cleanup by this lane).
- Resume: coordinator-driven when the owner freeze-lift decision lands.

END_BLOCKED w399-0428-289-providers: candidate 8c7f54b679 rests on PR #1880 (branch lane-0428-289-provider-discovery-providers-2); Trusted Plan runs 46011069186/46011641329 terminal-failed (base-catalog owner hold #136 + fan-in #1861/#1862/#1863); card moved to wait via card-status.py; akte+evidence on plan PR #234; resume coordinator-side on owner decision.

## END

QUESTION w399-0428-289-providers: card claimed (active, owner w399-0428-289-providers @ 5725634c0). My candidate (develop ea5218d7 → 8fe1b3a5, image-marker fix, tests + red/green proof ready) cannot push: refs/heads/lane-0428-289-provider-discovery holds foreign commit 95b68347 (author w335-0428-318-lowpair, stale base 5a37ddbd, not in develop, no PR, card never assigned to w335). No force-push/2nd branch per rules. Disposition requested: (a) delete orphan ref → I push+PR; (b) reassign card to w335 → I stand down; (c) I push a suffixed branch for comparison review (deviates from branch name — needs your OK). END pending answer.
