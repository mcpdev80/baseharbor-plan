# H-V40 — catalog-rows hunt: NEGATIVE verdict, package rows REJECTED (secure-by-design)

- Mission: `coordinator/missions/w40-hvcatalogrows.txt` (H-V40, flash, READ-ONLY)
- Lane: w40-0428-260-hvcatalogrows (hunt desk; no branch, no PR, no product change)
- Date: 2026-11-23
- Card: 0428-260 — **CLOSED by Owner** after the broad-package-row PR **#1814 was REJECTED** (Hosted run
  45268937124). This act records the **negative verdict** plus the reconciled facts.

## FINAL VERDICT: package-rows-REJECTED (secure-by-design)

The broad package/prefix-row design this mission commissioned **must not ship** and did not ship. It fails
four existing fail-closed guard tests in `scripts/test_pr_gate_coverage.py` — reproduced independently in
this lane (read-only) against develop tip `d4fa8c589`. Exact per-file `components[]` rows, as merged in
**#1813**, are the correct mechanism; the systemic future-new-file exposure is handled by **per-PR
component rows** (the PR that creates a file registers that file's row in itself), not by directory
prefixes.

## PLAN

1. Read mission + H-V38 (`ed1032734`) and H-V39 (`e99a0db21`) acts; resolve the real GitHub remote. DONE.
2. Clone develop read-only to /tmp/opencode/hv40; attest base + the three PR head/merge refs; build real
   changed-path sets with develop's pr-diff-base.py over the GitHub merge refs. DONE.
3. Build candidate catalog: H-V38's 5 rows + the #1650 new-file row + decisive + top-dir + tail package
   rows (0 unowned over the 2,617-path cmd/internal population). DONE (design later rejected).
4. Validate offline (validate-pr-gate-coverage.py): rc=0. DONE (a clean lint ≠ semantic acceptance).
5. Prove rc=1 (pre-#1813 catalog) → rc=0 (#1813 tip catalog) for #1810/#1809/#1650 with real PR diffs. DONE.
6. Synthetic new-file proofs under cmd/baha/ and internal/capability/. DONE — see "Corrected verdicts"
   for what those rc=0 runs do and do not prove.
7. Over-selection census (gates-per-path distribution, journey/ha unreachability). DONE.
8. OWNER UPDATE received mid-lane (three dispatches): #1813 MERGED with per-file rows; PR #1814 (this
   lane's design as shipped by Owner) REJECTED by Hosted run 45268937124; card 0428-260 CLOSED. Re-verified
   the rejection locally (guard tests). DONE.
9. Write this negative-verdict evidence, push to origin/main, END. DONE.

## Remote and SHA attestation (reality witnesses)

Planning repo (verified BEFORE the first evidence commit; wrong-zone rule):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v | head -1
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
```

Product remote resolved to github.com/mcpdev80 (REMOTE GUARD; direct `git ls-remote <real-url>`):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/main \
    refs/pull/1810/head refs/pull/1810/merge refs/pull/1809/head refs/pull/1809/merge refs/pull/1650/head refs/pull/1650/merge
c000c5db2560c471fe84842136e03d6e54d96779	refs/heads/main
d4fa8c589e02bf6708d9e6beba7a510c1a2efc7e	refs/heads/develop
cc4fc36f3f0732c1b50e1a9ccf8b453e1f971ce5	refs/pull/1650/head
994ec6640e5577e246be68da3e4142bfa9471c65	refs/pull/1650/merge
034c0c7d21512a62b2ec236b779e84235da4f507	refs/pull/1809/head
d9f415eca9429c44cbcfc346980e3f7e71dc10ae	refs/pull/1809/merge
168d40950bae5b8fb31862b36ceaffbdd1862207	refs/pull/1810/head
3aae1c02deec40fbf3f2afa27e73aa924575148c	refs/pull/1810/merge
```

- **Base attestation:** the catalog analyzed and diffed is develop tip `d4fa8c589` =
  "ci: register open PR gate coverage (#1813)", md5 `99d5123c5f7024b2e57d85e45acbdfd1` (file
  `base-pr-gate-coverage.tip.json`). The earlier mission-era develop `dc8626e9c` differs only in
  `scripts/pr-gate-coverage.json`; planner/validator/map/requirements are byte-identical between them
  (empty `git diff --stat dc8626e9c d4fa8c589 -- scripts/pr-gate-plan.py
  scripts/validate-pr-gate-coverage.py scripts/pr-gate-map-v1.json scripts/release-requirements.json`).
- The quarantined `workers/baseharbor` checkout was never cited. Read-only mission: no branch/PR opened,
  so the PR-provenance ancestor/log rules do not apply.

## Mission-status reconciliation

1. The mission says the H-V38 patch "has NOT landed yet". **It has:** #1813 (`d4fa8c589`) merged the 5
   H-V38 component rows PLUS `internal/metrics/perses_dashboards_keycloak.go` (the #1650 new-file row) —
   all six paths as exact per-file rows. The immediate #1810/#1809/#1650 guardian aborts are fixed at
   catalog level (measured rc=0 below).
2. The v0.4.28-stamp hazard H-V39 describes (catalog-mode bypasses legacy catch-alls; `release` mismatch)
   remains real and is the reason this bulk-registration card existed. The bulk answer is now resolved
   NEGATIVE: see verdict.

## Why package rows break the guards (4 tests: file:line + exact assertion)

Mechanics: `resolve_covered_gates` (`scripts/validate-pr-gate-coverage.py:29-36`) resolves a path by exact
component match, else by the LONGEST matching `packages[]` prefix; the guardian
(`scripts/pr-gate-plan.py:1830-1838`) aborts only when a changed `cmd/`/`internal/` path lands in
`unowned`. A directory prefix therefore removes precisely the sentinel paths the fail-loud guard (card
0428-242) is designed to reject.

Reproduction (read-only, this lane): fresh worktree of `d4fa8c589`;

```
$ python3 -m unittest scripts.test_pr_gate_coverage          # pristine develop tip
OK  (45 tests)
$ python3 -m unittest scripts.test_pr_gate_coverage          # same tree + the 122 candidate package rows
FAILED (failures=4)
```

(4 collateral ERRORs in that sandbox are path artifacts — those tests read `repo/../docs/**` files this
read-only mission never fetched; they pass identically with pristine and patched catalogs and are
unrelated to the design.)

| # | test | assertion defeated | how the package row defeats it |
| --- | --- | --- | --- |
| 1 | `scripts/test_pr_gate_coverage.py:569` `test_unreviewed_runtime_file_is_rejected_not_falled_back` | `with self.assertRaises(ValueError)` (:582) on a diff touching `internal/runtime/new_feature.go` | the `internal/runtime` prefix row owns the sentinel → `unowned=[]` → guardian silent → ValueError NOT raised |
| 2 | `scripts/test_pr_gate_coverage.py:604` `test_runtime_hint_without_catalog_owner_is_rejected` | `assertRaises(ValueError)` (:613), same sentinel | identical masking |
| 3 | `scripts/test_pr_gate_coverage.py:650` `test_uncataloged_source_is_rejected_with_precise_next_action` | `assertRaises(ValueError)` (:661), same sentinel (message must name `source.internal_runtime_new_feature_go`) | identical masking |
| 4 | `scripts/test_pr_gate_coverage.py:151` `test_application_observability_source_and_test_select_both_gates` | `assertEqual([], selected)` and `assertEqual(["internal/application/provider_union.go"], unresolved)` (:162-163) | the `internal/application` prefix row resolves the deliberate fail-closed sentinel to `['atomic/docker/lifecycle']` and hides it from unresolved |

The sentinel paths are intentional: `internal/runtime/new_feature.go` and `internal/application/provider_union.go`
are permanent tripwires proving the guardian still fires. The legacy planner asserts the same intent:
`scripts/test_pr_gate_plan.py:1074` `test_application_and_capability_production_remain_unresolved`
(capability/application production files stay `unresolved`) and `:1666`
`test_application_observability_mapping_does_not_hide_unreviewed_paths` (bundling a reviewed file with
`provider_union.go` keeps the whole PR unresolved). Package rows violate both the catalog guardian and the
fail-closed philosophy those tests encode. This is the failure of Hosted run 45268937124 → #1814 closed
without merge.

## Corrected verdicts (reconcile questions a/b)

**(a) Do package rows give genuine rc=0 coverage for a brand-new file in catalog-mode? NO — retract the
earlier claim.** Two interim artifacts were wrong and are corrected here:

- The `out-new-cmd.json` run (rc=0, `selected_gates=[]`, `fallback_used=True`, reason
  `cli-unresolved-runtime-impact`) was a harness bug: the planner loads the catalog beside itself
  (`pr-gate-plan.py:1822`) and that run directory had no candidate copy, so it fell to the legacy path.
- The corrected run, candidate catalog in place, authenticated env, develop-tip planner:

  ```
  NEW cmd/baha file, develop-tip catalog : rc=1 ABORT (guardian, uncataloged source change)
  NEW cmd/baha file, package-row candidate: rc=0 resolved broad_required=False fallback_used=True
                                           selected=['atomic/docker/data-capabilities']
                                           checks=['go-build','go-unit-tests','go-vet']   # broad Go, NOT the narrow cli-* checks
  ```

  The rc=0 is the **conservative-fallback branch**, not narrow coverage: the legacy catch-alls still
  append `unresolved` for these paths (e.g. `cli-unresolved-runtime-impact`, `pr-gate-plan.py:1420-1426`),
  the catalog branch moves them into `fallback_reasons` (:1861-1870), and `plan()` only skips the
  fallback tail when `targeted_plan` already returned `resolved` (:1872). An exact `components[]` row is
  what suppresses the catch-all (`elif` chain short-circuit) and yields `fallback_used=False` with narrow
  per-package checks — the behavior `test_pr_gate_coverage.py:624` (`test_planner_catalogs_app_broker_as_resolved`)
  asserts for registered paths. So package rows trade a loud, actionable abort for a silent, weakened
  pass: strictly WORSE, and the masking itself is the violation.
- Self-audit note on the earlier interim table: it claimed `fallback_used=False` on the three PR
  after-plans. Wrong — re-measured: `fallback_used=True` on all three (identical selected-gate sets across
  the old-catalog+H-V38-rows, the tip catalog, and the candidate). The selected sets come from the
  catalog; the narrow-check skip persists via fallback_reasons. The committed before/after plan JSONs
  show the truth.

**(b) The `release` field (catalog `v0.4.27`, mapping `v0.4.27`, v0.4.28 in requirements).** `plan()`
enters catalog-mode iff `coverage['release'] == mapping['release']` (`pr-gate-plan.py:1821-1824`;
`result['release']` is `mapping['release']`, :837). Today both read `v0.4.27` → catalog-mode + guardian
are LIVE for every PR (that is why #1810/#1809/#1650 aborts happened and why #1650's new file aborted at
`d4fa8c589`-minus-one-row). The mismatch case — Owner stamps the MAP to `v0.4.28` while the CATALOG still
says `v0.4.27` (or vice versa) — takes the else-branch: catalog bypassed entirely, `broad_required=True`,
`coverage_status=unresolved` for any path the legacy heuristics cannot own → every product PR resolves via
the conservative fallback with broad Go checks and zero native gates. A permissive hole, not a fix.
**What the Owner must set:** keep `coverage['release']` (`v0.4.27`) untouched in any catalog-content PR;
at the planned v0.4.28 transition, stamp `scripts/pr-gate-map-v1.json.release` AND
`scripts/pr-gate-coverage.json.release` in the SAME commit, and add the v0.4.28-only gate
`atomic/static/ci-fast-check` (`selection_scope: "release-only"`, never PR-selectable) to the catalog's
`gates[]` or validation fails "coverage catalog omits active release gates"
(`validate-pr-gate-coverage.py:257-268`). No other change makes stamping safe — per-file rows for every
path PRs actually touch are the prerequisite either way.

**(c) Honest conclusion.** The #1813 mechanism — exact per-file `components[]` rows added by the PR that
touches/creates the file — is the design and should continue for every new file. There is NO package/
prefix mechanism that works acceptably in catalog-mode: any prefix that covers sentinel dirs masks the
guardian (proven above); prefixes that dodge sentinels still convert unknown-new files from loud aborts
into fallback passes. The 2,231 currently-unowned develop paths only matter when a PR touches them (then
the guardian names them and the PR registers its exact rows — today's correct behavior).

## Offline proofs (real changed-path sets)

Harness = the real CI entry: `GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop python3
scripts/pr-gate-plan.py --diff prdiff-N.json --requirements scripts/release-requirements.json --mapping
scripts/pr-gate-map-v1.json` (`conservative_fallback=True` via `main()` :1941), against
`scripts/pr-diff-base.py --target-base <base> --head <pr-head> --integration <refs/pull/N/merge>` output
computed in worktrees of the real GitHub merge commits. Plan JSONs are committed beside this file.

| PR | head | BEFORE (catalog `8c32ee36`, pre-#1813) | AFTER (#1813 tip catalog `99d5123c`) |
| --- | --- | --- | --- |
| #1810 | 168d40950bae5b8fb31862b36ceaffbdd1862207 | rc=1 ValueError abort: `internal/application/perses_lifecycle_test.go`, `internal/capability/perses.go`, `internal/capability/perses_test.go` (`before-1810-error.txt`) | rc=0, `coverage_status=resolved`, `broad_required=False`, `fallback_used=True`, selected 3 gates: docker+podman observability, static/public-contracts (`plan-1810-tip-catalog.json`) |
| #1809 | 034c0c7d21512a62b2ec236b779e84235da4f507 | rc=1 ValueError abort: `cmd/baha/secret_audit_test.go`, `cmd/baha/secret_operations.go` (`before-1809-error.txt`) | rc=0, resolved, broad=False, `fallback_used=True`, selected 2 gates: docker data-capabilities, docker coreless-lifecycle (`plan-1809-tip-catalog.json`) |
| #1650 | cc4fc36f3f0732c1b50e1a9ccf8b453e1f971ce5 | rc=1 ValueError abort: `internal/metrics/perses_dashboards_keycloak.go` (`before-1650-error.txt`) | rc=0, resolved, broad=False, `fallback_used=True`, selected 5 gates: docker+podman data-capabilities, docker identity, docker+podman observability (`plan-1650-tip-catalog.json`) |

All three rc=1→rc=0 with real diffs; gate sets match H-V38's proven after-values for #1810/#1809 and
extend them for #1650. The `plan-*-catalog-8c32ee36.json` files are the same three PRs re-planned with the
pre-#1813 develop planner trio and the OLD (`8c32ee36`) catalog with only the H-V38 5 rows patched in —
they show #1810/#1809 already rc=0 there and #1650 still rc=1 (its sixth row came only with #1813);
`prdiff-*.json` are the real diff inputs for re-computation.

## The rejected candidate (witness only — DO NOT LAND)

- `rejected-catalog-candidate.json` — develop-tip components (265) + `packages` 4→126 prefix rows; md5
  `e27ba097546adb66cd04d7e4a0e9ca7a`; validates rc=0; 0 unowned over all 2,617 develop cmd/internal paths;
  still fails the 4 guard tests above.
- `rejected-catalog-candidate.diff` — the complete `git diff` (develop-tip catalog → candidate), 1,320
  lines (`a/scripts` → `b/scripts` headers; `patch -p0` round-trip re-proven byte-identical, md5
  `e27ba097…`, against the copies committed here).
- `base-pr-gate-coverage.tip.json` — the exact diff base (`d4fa8c589` catalog).
- `unowned-tip-population.txt` / `unowned-tip.txt` — the 2,617-path population and the 2,231 paths with
  no catalog owner at tip (the census this card was raised to register — now known to be the WRONG fix).

## Over-selection census (kept from the mission's task 3, moot under the verdict)

The candidate never selected `journey/*`/`ha/*` (no source surface reaches them); per-path gate counts
over all 2,617 develop paths: 0 gates: 5 (exact rows without gate-mapped surfaces — pre-existing
`cmd/baha` native-proof rows), 1 gate: 2,554, 2 gates: 51, 3 gates: 1, 4 gates: 5, 6 gates: 1 (all from
pre-existing exact rows, none introduced by package rows). The full release matrix was never force-
selectable. This analysis is recorded because the mission asked for it; it does not rehabilitate the
design — the masking failures above are dispositive.

## cleanliness

- Read-only mission. All edits confined to `/tmp/opencode/hv40/` (one blobless clone `repo/`; detached,
  branch-less worktrees `work/`, `p3/`, `reject-full/` — deleted after use; run dirs + deliverables).
  No product-repo push/commit/branch anywhere; no `.github/**` or `scripts/**` edit; no reruns, no
  dispatches; PR #1814 not touched.
- Guard-test reproduction note: in `reject-full/` the ONLY file changed was `scripts/pr-gate-coverage.json`
  (the candidate packages) purely inside the /tmp worktree for the unittest, then restored from
  `git checkout --`; the product repos and their refs are untouched (witness: the ls-remote block above,
  taken after all reproduction work).
- No containers/networks/volumes/compose projects started (no docker/podman invocation at all on this
  host); ambient images untouched; no VMs used. `docker ps -a` before == after; grep for hv40/w40 names = 0.

```
$ docker ps -a --format '{{.Names}}' | grep -c -i 'hv40\|w40'
0
```

cleanliness: read-only; edits confined to /tmp/opencode/hv40; no stack/worktree-with-branch/PR; ambient untouched

## Evidence delivery witness (second-to-last action)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main
 * branch                main       -> FETCH_HEAD
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep hunt-hv40-catalog-rows
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/base-pr-gate-coverage.tip.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/before-1650-error.txt
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/before-1809-error.txt
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/before-1810-error.txt
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/plan-1650-catalog-8c32ee36.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/plan-1650-tip-catalog.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/plan-1809-catalog-8c32ee36.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/plan-1809-tip-catalog.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/plan-1810-catalog-8c32ee36.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/plan-1810-tip-catalog.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/prdiff-1650.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/prdiff-1809.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/prdiff-1810.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/rejected-catalog-candidate.diff
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/rejected-catalog-candidate.json
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/round-1.md
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/unowned-tip-population.txt
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/unowned-tip.txt
```

Evidence commit `8938a6597` (pushed 339547f4f..8938a6597 main -> main).

## END

END_DONE hunt-hv40: package-rows-REJECTED (secure-by-design). Negative-verdict evidence at
evidence/recovery-2026-11-23/hunt-hv40-catalog-rows/round-1.md; broad `packages[]` prefix rows mask the
0428-242 guardian and fail scripts/test_pr_gate_coverage.py:569/:604/:650 (sentinel
`internal/runtime/new_feature.go` no longer raises ValueError) and :151-163
(`internal/application/provider_union.go` no longer stays unresolved) — reproduced at d4fa8c589;
#1813's exact per-file component rows are the merged, correct fix and the mechanism for every future new
file (proven rc=0 real-diff for #1810/#1809/#1650); package rows give NO genuine non-fallback coverage for
new files (corrected: fallback_used=True everywhere, rc=0 is a weakened silent pass); release-field
guidance: keep catalog release=v0.4.27; stamp map+catalog to v0.4.28 only in the same commit plus the
release-only ci-fast-check gate row. Mission obsolete; card 0428-260 CLOSED by Owner.

END hunt-hv40 DONE
