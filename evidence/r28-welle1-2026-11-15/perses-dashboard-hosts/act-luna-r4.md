# CODEX-REVIEW — PR #1602 correction follow-up

**ROLLE: REVIEW**  
**Task:** `t-...-perses-dashboard-hosts`  
**Candidate:** `1f7b5eee92fb142ba94776fce6738df32c5aab7a`  
**Base delta:** prior reviewed head `8267a16df47ed9b3c3fb4fc26cc77959b7b2e01e` → candidate; only `internal/capability/perses.go` and its tests change.  
**Exact-head CI:** run `43815630416`, event `pull_request`, created `2026-11-16T06:16:28Z`, COMPLETED SUCCESS, exact head. `git diff --check` clean.

## Verdict: APPROVE CONTENT

The r3 correction is implemented: positive host dashboard availability now requires the native, backend-verified `collector-metrics` signal witness from the reference contract in addition to the selection/pin predicates. The resolver fails closed when the witness is absent, unknown, or not native/backend-verified; the focused tests assert this and retain unavailable status. The remaining Target/authorization axis belongs to the separately tracked owner finding (0428-080) and is outside this candidate's declared scope; under the mission's explicit direction, fail-closed/unavailable-preserving behavior satisfies this card without that resolver. The exact-head PR run is green.

## Recipe / stop

- **File/change:** no further change required for the candidate content reviewed here.
- **Checks:** exact-head PR run succeeded; retain the signal-witness negative cases and the positive native verified witness case.
- **Owner finding:** keep Target/authorization unresolved as a separate 0428-080 finding; do not claim target-specific authorization from this contract.
- **Stop:** if any missing/invalid signal can still produce available panels, or the candidate begins claiming Target authorization, request correction. No merge.
