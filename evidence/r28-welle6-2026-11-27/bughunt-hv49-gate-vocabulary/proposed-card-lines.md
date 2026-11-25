# Proposed card lines for H-V49 fund

Card title (proposed): "pr-gate-coverage.json diverges from release-requirements.json on 3 archived consumer gates"

## Summary (one line)
`release-requirements.json` lists `integration/{docker,podman}/remote-target` and `integration/static/live-console` as release gates, but `scripts/pr-gate-coverage.json` declares no matching gate rows, so the validator (scoped to the active release) never sees the divergence.

## Evidence reference
Bug Hunt H-V49 akte: `evidence/r28-welle6-2026-11-27/bughunt-hv49-gate-vocabulary/w192-0428-224-hunt-v49.md` (Finding F1).

## Acceptance criteria
- [ ] A catalog-regression test asserts `set(release-requirements.gates) == set(coverage.gates)` EXCLUDING the three named archived consumer gates, so a future release bump of any archived gate trips red.
- [ ] The three archived gates keep an explicit, comment-documented status ("archived, do not select for v0.4.27") in both files.
- [ ] No `.github/**` change required for the test-only assertion (Owner scope untouched).

## Scope / write-set
- `scripts/test_ci_v0427_gate_catalog.py` (add a new test method) — within card write-set.
- Optional: `scripts/release-requirements.json` (remove archived gates, C3) — within card write-set, confirm no pre-release consumer references first.
- Explicitly OUT of scope: any `.github/workflows/**` edit; inventing a draft-aware gate token; touching the PR gate planner (`scripts/pr-gate-plan.py`) or CI-native planner (`scripts/pr-native-gate-plan.py`) — this card is documentation/validation only.

## Risk note
The drift is currently intentional and regression-tested (`test_ci_v0427_gate_catalog.py` asserts these three are NOT in the v0.4.27 selection). This card only makes the divergence VISIBLE to CI; it does not change gate selection behavior.
