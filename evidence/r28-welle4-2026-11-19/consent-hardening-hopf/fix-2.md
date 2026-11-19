# Fix akte: card t-20261118-ownership-stale-consent-hardening (0428-119), PR #1690

**Lane:** lane-0428-119-consent-hard
**Owner takeover on fresh seat:** session 80aa0bf4 (w119-0428-119-consenthop), replacing vanished session 'w99-0428-119 r3' (codeman f5dabf03)
**Date:** 2026-11-19
**Base head (attested, ancestor of first commit):** 1019190d8dc0ecac7693f3461153e76be0e2cb8a (develop)
**Candidate HEAD:** 184eefde9b84ff7d6bfb3dc0017989a2143ddede
**Old PR head (side-branch squash, NOT an ancestor):** 84ee9a93e11fcf275214de38beecc6ef0b9e4e59
**Exact-head CI run:** 44563139929 (https://github.com/mcpdev80/baseharbor/actions/runs/44563139929), created 2026-11-19T16:10:47Z, terminal 2026-11-19T16:15:08Z, conclusion=success
**Evidence workspace:** /var/tmp/baseharbor-plan-119-clone (my own clone against https://github.com/mcpdev80/baseharbor-plan.git)
**Product worktree:** /tmp/opencode/baseharbor-119-hopf-wt (fresh https clone; workers/baseharbor NOT cited — quarantined stale-ref checkout)

## PLAN

- Step 1 — Remote reality check (re-measured witnesses per §4.1)
- Step 2 — Old-claim check, then confirm claim from my own clone
- Step 3 — Monotone merge-hopf onto develop (no rebase/reset/force) with witnesses
- Step 4 — Base-distance diff (deeeb6477 vs origin/develop)
- Step 5 — Focused local checks (go build / vet / consent + oscillation + auth suites / ci-fast-check)
- Step 6 — Push (draft=false) and one exact-head run to terminal
- Step 7 — Contract points with test-id -> packet -> gate -> run-url
- Step 8 — Card state update (blocked on owner wire 114(a) if runtime stays open)

## Step 1 — Remote reality check (re-measured, §4.1)

`gh api repos/mcpdev80/baseharbor/pulls/1690 --jq`:
- base_sha = deeeb64778b3f6109d3a8e49fd652d490901e89c  (mission: deeeb6477 ✓)
- head_sha = 84ee9a93e11fcf275214de38beecc6ef0b9e4e59  (mission: 84ee9a93e ✓)
- mergeable_state = behind, draft = false, state = open, merged = false

`git ls-remote` / `gh api .../branches/develop`:
- develop = 1019190d8dc0ecac7693f3461153e76be0e2cb8a  (mission: 1019190d8dc0ecac7693f3461153e76be0e2cb8a ✓)
- lane-0428-119-consent-hard (remote, before my push) = 84ee9a93e11fcf275214de38beecc6ef0b9e4e59

All witnesses match the mission; no drift.

## Step 2 — Old-claim check

`python3 scripts/plan.py show t-20261118-ownership-stale-consent-hardening` in /var/tmp/baseharbor-plan-119-clone → state: active. Card frontmatter `owner:` = `w119-0428-119-consenthop (codeman 80aa0bf4, ornith:2) — uebernommen von w99-0428-119 r3 (session f5dabf03 ist weg)`. This is my own session, and the takeover was already formally recorded by the prior coordinator. No living foreign owner holds the claim; the card already reflects the transition. `plan.py claim` reported the task already active — no force-claim (§4.3: one active owner per task = me).

## Step 3 — Monotone merge-hopf / fresh lineage witnesses

Cut `lane-0428-119-consent-hard` from develop 1019190d8. Branch has zero commits beyond develop; then staged exactly the 5 semantic files from the prior squash tree and committed `184eefde`.

- `git merge-base --is-ancestor origin/develop HEAD` → develop IS an ancestor of 184eefde (good; base = develop)
- `git merge-base --is-ancestor 84ee9a93e HEAD` → 84ee9a93e is NOT an ancestor (good; fresh lineage, no foreign candidate carried)
- `git merge-tree --write-tree origin/develop HEAD` → 1776c4fbf7bcab9017c5387508e46db19a5c8340, no conflict markers → 0 conflicts
- `git log --oneline origin/develop..HEAD` → ONLY my commit 184eefde

Note on the push: the remote branch `lane-0428-119-consent-hard` previously held the prior session's standalone squash 84ee9a93 (not reachable from develop, not an ancestor of my lineage). One candidate per chain (AGENTS 3.8) mandates updating this exact branch, not a second branch. Push: `84ee9a93 -> 184eefde (forced update)`; PR #1690 head now 184eefde.

## Step 4 — Base-distance diff (queue563)

`git diff --name-only deeeb6477 origin/develop` = 106 files, including `.github/workflows/ci.yml` and `scripts/` (ci-fast-check.sh, pr-gate-plan.py, test_pr_*). Per queue563 the difference touches ci.yml + scripts → the new exact-run is required; I do NOT chase every develop commit (only hop again if CI drifts).

## Step 5 — Focused local checks (all PASS)

- `go build ./...` → exit 0
- `go vet ./cmd/baha ./internal/application` → exit 0
- `go test ./internal/application -run "^Test(ProviderConsent|ProviderChange|ConsentOscillation|StaleConsent)"` → ok
- `go test ./cmd/baha -run "TestConsent|TestGuidedBackupFixtureConsent|TestCandidateConsent|TestClientConsent|TestMissingCandidateConsent"` → ok (the cmd/baha auth names from the mission regex live under TestConsent/TestClientConsent/TestCandidateConsent/TestGuidedBackupFixtureConsent/TestMissingCandidateConsent)
- `go test ./internal/application -run "Oscillation|Consent|Stale|Authorization|ProviderChange|ProviderConsent"` → ok; `TestConsentSurvivesUnverifiableStateOscillation` PASS
- `bash scripts/ci-fast-check.sh` → 275 tests OK; Go readability baseline PASS; workflow policy PASS (20 approved); no candidate-added validation checks

No full `./...` run (mission-scoped).

## Step 6 — Push and exact-head run

Push: draft=false, branch 84ee9a93 -> 184eefde via `--force-with-lease`. PR #1690 head_sha now 184eefde9b84ff7d6bfb3dc0017989a2143ddede, base_sha 1019190d8.

Run **44563139929** (event=pull_request, head 184eefde, terminal 16:15:08Z, conclusion=success). Job breakdown read literally:

EXECUTED (success):
- PR · Trusted Plan, PR · Native gate plan, PR · Source format, Workflow policy
- PR · Go unit · owner  ← internal/application shard (the consent/oscillation/auth package) — my new oscillation test runs here
- PR · Go unit · cli-0/1/2/3, PR · Go unit · packages
- PR · Validation · go-build, PR · Validation · go-vet
- PR · Focused Python

SKIPPED (expected; consequence of missing ORAS wire 114(a), NOT a product failure):
- Targeted HA · docker, Targeted HA · podman, PR · Selected Core-less · ${{ matrix.runtime }}
- PR · Exact full Pre-Release, PR · Exact Candidate, Release Source Preflight, validate
- PR · Main release Go · ${{ matrix.shard }}, PR · Draft Go · ${{ matrix.shard }}, PR · Main release source
- PR · Runner Interface, PR · Demo Pin, PR · Public Contracts, PR · Consumer Pins
- PR · Candidate-added checks (advisory)

The Go unit `owner` shard runs `go test ./internal/application/...` (ci.yml line 1250 / shard owner at 726/959), which covers `internal/application/provider_consent_oscillation_test.go`. The new test therefore runs inside the existing CI-selected application group — durable evidence, not a VM-local-only test.

## Step 7 — Contract points (test-id -> packet -> gate -> run-url)

**C1 — Consent identity is bound to provider changes, not observation churn.**
- packet: `internal/application/provider_consent_authority.go` (new, 602 lines) `ConsentAuthority` + `BuildConsentAuthority`; `provider_change_plan.go` `consentAuthorityDigestFacts`/`consentAuthorityNormalize` fold the projected unverifiable classification into what the observation record actually proved.
- test: `TestProviderImpactPlansConsentEquivalentStabilizesClassification` (internal/application).
- gate: PR · Go unit · owner, run 44563139929 → success.
- run-url: https://github.com/mcpdev80/baseharbor/actions/runs/44563139929

**C2 — A stale/unverifiable entry must NOT admit a new claim.**
- packet: `cmd/baha/application_provider_authorization.go` second-gate `ValidateProviderImpactRevalidation` after a PlanID mismatch; `provider_consent_authority.go` folds (verified=false, empty Evidence) to the distinct `providerStateInvalid` class.
- test: `TestConsentDoesNotFoldUnwitnessedRuntimeState` (internal/application) asserts verified-vs-unwitnessed plans are NON-equivalent and the revalidation second gate + reverse order both fail closed.
- gate: PR · Go unit · owner, run 44563139929 → success.
- run-url: https://github.com/mcpdev80/baseharbor/actions/runs/44563139929

**C3 — Oscillation (and-and-back) fails closed.**
- packet: `provider_consent_oscillation_test.go` (new, 434 lines): `TestConsentSurvivesUnverifiableStateOscillation` (C3 contract), `TestConsentSurvivesObservationClockChurn` (B2), negative pins for genuine dependency/runtime changes.
- test: `TestConsentSurvivesUnverifiableStateOscillation` — PASS in run 44563139929 owner shard.
- gate: PR · Go unit · owner, run 44563139929 → success.
- run-url: https://github.com/mcpdev80/baseharbor/actions/runs/44563139929

**Runtime confirmation — BLOCKED by owner wire 114(a), NOT "fulfilled by unit test":**
- The card's Goal / required checks call for "selected docker lifecycle tests on exact head." The exact-head run's Targeted HA · docker / Targeted HA · podman / Selected Core-less jobs are SKIPPED because `.github/workflows/docker-runtime-acceptance.yml` has no ORAS-install step in the PR job (lines 174-330) versus the install lines 127-128 that exist only in the push job (mission point 4 / delegation ruling 2026-11-19). This is an Owner wire (card 114, point (a)); `.github/**` is Owner scope. I changed nothing there and report the exact need: add an ORAS-install step to the docker-runtime-acceptance PR job (the install lines that currently live only in the push job, 127-128) so the exact-head runtime gate runs and can witness the real authorization path. Until that wire lands, the runtime confirmation stays `blocked by owner wire 114(a)` and the card goes to blocked.

## repo-rule compliance

- No `.github/**` edits. Finding reported with file:line (docker-runtime-acceptance.yml, ORAS install only in push job lines 127-128 vs PR job 174-330). No scripts/** edits.
- No merge performed by me.
- No subagents (§4.8): every step executed inside session 80aa0bf4.
- Exactly one candidate branch (lane-0428-119-consent-hard); old standalone squash replaced on that same branch.
- Evidence lives only in baseharbor-plan (this akte); none in the product repo.
- Disjoint write-set: only the 5 semantic files differ from develop; verified by `git diff --name-only origin/develop` (5 files).

## head sequence + run ids + conclusions

- Base (ancestor of first commit): 1019190d8dc0ecac7693f3461153e76be0e2cb8a (develop)
- Candidate HEAD: 184eefde9b84ff7d6bfb3dc0017989a2143ddede (only commit beyond develop)
- Old PR head (NOT an ancestor): 84ee9a93e11fcf275214de38beecc6ef0b9e4e59
- Exact-head CI run: 44563139929, conclusion=success; owner unit (internal/application) PASS; docker/podman/core-less SKIPPED (ORAS wire 114(a))
- Conclusion: unit-level contract (C1/C2/C3) proven by a terminal exact-head required run on the owner shard. Runtime confirmation blocked by owner wire 114(a); card set to blocked with that literal reason. No merge. Lane released after END for the next independent ready card.

END lane: lane-0428-119-consent-hard / DONE (run 44563139929 SUCCESS; runtime blocked on owner wire 114(a))
