# main-reg-evidence-route: how a main-targeted registration/PR carries a green "PR Selected Checks"

Lane: o212 · READ-ONLY research
Supports: t-20261027-r27-cutover-pr3 + t-20261029-r27-postrun-token-mapping (postrun card)
Answers codex-rv1204 finding #2 (PR #1204 head shows "PR Selected Checks = SKIPPING"; policy forbids treating skips as green)

## PLAN
1. Establish the binding CI contract from `origin/main:.github/workflows/ci.yml`.
2. Establish the repo's "PR Selected Checks" required-final contract (what makes the gate SUCCEED vs skip).
3. Empirically inspect three main-targeted PRs (#1186, #1176, #1159) and record the actual status of "PR Selected Checks" on their heads.
4. Trace how main's real history is populated (promote/merge vs CI-only main PR) — the "promotion" question.
5. Evaluate the three candidate routes (RUNBOOK §8a/8b/8d) against THIS case and select the one that legitimately makes PR #1204's exact head carry green PR Selected Checks (or an authorized substitute with policy file:line).

---

## 1. Binding CI contract (origin/main)

`on:` triggers in `origin/main:.github/workflows/ci.yml`:
```yaml
on:
  workflow_dispatch:
  push:
    branches:
      - 'runtime-validation/ci/**'
      - 'runtime-validation/source-preflight/**'
      - 'runtime-validation/ha/**'
  pull_request:
    branches:
      - develop
      - main          # a PR whose BASE is main DOES trigger this workflow
```
The workflow **does** trigger for a `pull_request` with `base == main`. It does **not** trigger a product/full CI on push to `main` (main push only runs `workflow_policy` + `release_source_preflight` when ref is a `runtime-validation/...` branch). So a CI-only main PR is the only realistic path to get the "PR · *" matrix onto a main-base PR head.

## 2. The "PR Selected Checks" required-final contract (decisive)

The gate job that sets the merged-state "PR Selected Checks" line is the last `PR · Selected Checks` job in `ci.yml`. Its run block proves the SUCCEED contract:

```python
required.update({"PR · Trusted Plan", "PR · Focused Python",
                 "Workflow policy", "PR Selected Checks"})
...
python3 "$RUNNER_TEMP/pr-required-final.py" \
  --plan pr-plan.json --results "$RUNNER_TEMP/pr-results.json" \
  --requirements scripts/release-requirements.json
```

Every check in that `required` set **must SUCCEED** for the final line to be green. A skip on any of them fails the required-final contract. Therefore a `pull_request` PR whose matrix jobs never run is structurally unable to produce green "PR Selected Checks".

## 3. Why every `base_ref == main` matrix job SKIPS — the root cause

**Every check matrix job in `ci.yml` is guarded by `github.base_ref == 'develop'`.** Concrete guards observed on origin/main:

- `PR · Trusted Plan` (line 433): `if: github.event_name == 'pull_request' && github.base_ref == 'develop'`
- `PR · Runner Interface` (485): `... && github.base_ref == 'develop' ...`
- `PR · Consumer Pins` (509): `... && github.base_ref == 'develop' ...`
- `PR · Exact Candidate` (588): `... && github.base_ref == 'develop' ...`
- `PR · Focused Python` (627): `... && github.base_ref == 'develop'`
- `PR · Validation` (665): `... && github.base_ref == 'develop'`
- `PR · Selected Runtime` (792): `... && github.base_ref == 'develop' ...`
- `PR · Public Contracts` (752): `... && github.base_ref == 'develop' ...`
- The final `PR · Selected Checks` enforce job (810): `if: always() && github.event_name == 'pull_request' && github.base_ref == 'develop'`

`github.base_ref` is the branch the PR merges **into**. For a PR whose base is `main`, `github.base_ref == 'main'`, so **`main != 'develop'` → every matrix job is skipped**, including the final enforcement job's own body (guarded by `always()` but requiring the required checks to have passed). The "PR Selected Checks" line then reports `skipping`. This is not a transient/scheduling skip; it is a structural consequence of `base_ref == main` combined with the `base_ref == 'develop'` guard.

Empirical confirmation — the three recent merged main-targeted PRs on the current board:

| PR | title | PR Selected Checks on head |
|----|-------|----------------------------|
| #1186 | promote: develop 9e50d8a4 → main (register de-poisoned, API-attempt writer) | **skipping** (all 26 checks skip; only Workflow policy passes) |
| #1176 | release: promote attempt-api fix | **skipping** |
| #1159 | release(v0.4.27): promote develop into main via merge (R27 chain) | **skipping** |

`gh pr checks` for all three shows `PR Selected Checks skipping 0`. This is the exact state PR #1204 is in. **It is the established, accepted precedent for main-targeted CI-only PRs in this repo** — these PRs merged despite the skip because they are not product cutover candidates; they are bookkeeping/promotion commits.

## 4. What "promotion" means here (develop → main route)

From `git log --all --oneline --grep=main` and merged-PR-to-main list:

- `364db5d4 release(v0.4.27): promote develop into main via merge (R27 chain) (#1159)`
- `df451e0d promote: develop 9e50d8a4 → main (register de-poisoned, API-attempt writer) (#1186)`
- `e13f1570 release: promote develop@post-#1169 to main (#1170)`
- `a0cdcb0c ci: bind exact SQL remove and replacement preview corrections` (an accepted exact-PR qualification merged into tested source)
- `d4015583 Merge accepted exact SQL preview qualification into tested product source`

**Promotion = `develop` merged into `main` via a release/promotion merge commit** (v0.4.26 / v0.4.27 pattern: "promote develop into main via merge", "promote verified BaseHarbor v0.4.25 to main"). The verified, CI-qualified work lives on **`develop`** (where every `base_ref == 'develop'` matrix job runs and can go green). The qualified lineage is then adopted onto main by a release/promotion merge.

Therefore: **CI-only main PRs are the wrong vehicle for a green product cutover candidate.** The binding route is develop → promotion-merge to main, with the green PR Selected Checks generated on the develop-base PR. This is exactly the established pattern (v0.4.26/v0.4.27).

## 5. Evaluation of the three candidate routes (RUNBOOK §8) — FOR THIS CASE

**Route (a) — qualified develop commit before the main PR.**
The verified work (green PR Selected Checks from a `base_ref == 'develop'` PR) is already the norm. For the *postrun-token-mapping* change (PR #1204), the same env mapping was already qualified on **develop** via PR #1202 (head SHA 7a417d37, "ci: reviewed-controller pin → dd8fb61d (--product wired)"). So the qualified lineage for this exact change exists on develop. Route (a) is satisfied by the develop-side PR + the standard promotion merge; the main-targeted PR #1204 then only forwards the (already-qualified) bookkeeping. **Route (a) is the established, authorized route for this case.**

**Route (b) — Classifier-Erweiterung (widening `base_ref` in ci.yml to also run the matrix on main).**
Would technically make a main-base PR's matrix run and could go green. **Rejected for this case:** it changes the binding CI contract for *every* main PR, it is a product/CI change that must itself go through the develop → promotion-merge route, and it is unnecessary: it does not change the fact that product cutover candidates belong on develop. Widening `base_ref` also risks turning main bookkeeping PRs into full product CI runs. No policy text in `docs/DEVELOPMENT_GUIDELINES.md` authorizes running the full selected-runtime matrix on main-base PRs; the contract as written is `base_ref == 'develop'`. Route (b) is a larger refactor, not a "route to get green checks on PR #1204's head today."

**Route (d) — selected-gates push format as the evidence route.**
This is the push-based qualification (`push` to `runtime-validation/...` branches → `release_source_preflight` / HA / source-preflight gates) — the same mechanism used to qualify the exact candidate. It is the vehicle that qualified #1202 on develop. For PR #1204's head to carry green PR Selected Checks, the *PR-path* final contract (section 2) is the only thing that writes that line; the push format qualifies the *candidate*, not the PR-selected line on a main-base PR. So route (d) does **not** by itself put green PR Selected Checks on PR #1204's main-base head — it supports route (a) by qualifying the lineage on develop (and on the push path for the promote merge).

## 6. Recommended route (concrete)

**Route (a): qualify the exact change on develop (green PR Selected Checks), then adopt onto main via the release/promotion merge. Do NOT rely on PR #1204's head being green.**

Reason: PR #1204 is a CI-only PR with `base == main`; by the binding guard `github.base_ref == 'develop'` (ci.yml lines 433/485/509/588/627/665/752/792/810) every `PR ·` matrix job — including the final "PR Selected Checks" enforcement — is skipped. The repo's required-final contract (pr-required-final.py, final enforce job) mandates SUCCEED on the whole required set, so a skip is not an authorized "green" for a product cutover candidate. The repo's own precedent (#1186, #1176, #1159) shows main-targeted PRs merge *with the skip* precisely because they are promotion/bookkeeping, not qualified candidates. The qualified lineage already exists: PR #1202 (develop, head 7a417d37) qualified the identical publish-step env + dd8fb61d pin forward-port. Adopt that lineage to main via a standard promote merge (v0.4.26/v0.4.27 pattern).

### Exact next commands
```bash
# 1) Re-confirm PR #1204's skip is structural (base_ref==main), not transient
gh pr check 1204

# 2) Re-confirm the develop-side qualified lineage for the same change
gh pr check 1202            # expect green PR Selected Checks on develop base
git -C baseharbor log 7a417d37 -1 --oneline   # develop-side candidate head

# 3) Adopt the qualified lineage onto main via the established promotion route
#    (a promote/merge PR whose base is develop, then main adopts it — the
#     v0.4.26/v0.4.27 "promote develop into main via merge" pattern), NOT by
#     trying to green PR #1204's main-base head.
#    e.g. create the promote branch from 7a417d37 and merge toward main via the
#    release/promotion channel documented in the RUNBOOK.
```

### Policy lines to cite
- Matrix jobs gated on develop: `origin/main:.github/workflows/ci.yml` lines 433, 485, 509, 588, 627, 665, 752, 792, 810 (`github.base_ref == 'develop'`).
- Required-final SUCCEED contract (skips are not green): final `PR · Selected Checks` enforce job body in `origin/main:.github/workflows/ci.yml` (`pr-required-final.py` + `pr-authenticated-results.py`, required set includes "PR · Trusted Plan", "PR · Focused Python", "Workflow policy", "PR Selected Checks").
- Promotion route precedent: `364db5d4 release(v0.4.27): promote develop into main via merge (R27 chain) (#1159)`, `df451e0d promote: develop 9e50d8a4 → main (#1186)`, `e13f1570 promote develop@post-#1169 to main (#1170)`.

## o212-DONE

## o212-BLOCKED
None. Research completed; no mutation performed (read-only lane).
