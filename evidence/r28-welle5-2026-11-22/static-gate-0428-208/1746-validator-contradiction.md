# 0428-208 / #1746 — validator contradiction finding (2026-11-23)

## Status: ESCALATED to owner (conflict rule §1). Hold #1746 — no push, no force.

The empirical finding below is documented as evidence and accompanies an escalation to
the owner with a recommendation delivered THIS TURN. #1746 stands still until the owner
rules. Priority switch: the #1723 rest-hop (59f3470bb -> 15c65213) is pulled forward and
reported separately.

## The contradiction

The production validator `scripts/validate-pr-gate-coverage.py` computes the active
release gate set at lines 249-250:

```python
required_ids = {row.get("id") for row in requirements.get("gates", [])
                if isinstance(row, dict) and release in row.get("required_for", [])}
missing = sorted(required_ids - seen_gates)
extra = sorted(seen_gates - required_ids)
```

The single variable `release` is the catalog's one `release` field (assigned at line 120:
`release = coverage.get("release")`) and is used as the sole membership key of
`required_for`. It is the same value that is validated at line 121 (`release not in
requirements["releases"]`). Therefore a single `release` value can only select gates whose
`required_for` contains that one release string.

## Empirical results (three tests, all run locally, non-forceful)

### Test 1 — frozen branch 208ee7607, as delivered
- catalog `release` field = `v0.4.27`; 62 catalog gates, NO `atomic/static/ci-fast-check`
  gate present.
- `release-requirements.json`: all 62 existing gates carry `v0.4.28` added to their
  `required_for` (blanket add), and a new gate `atomic/static/ci-fast-check` with
  `required_for: [v0.4.28]` is appended.
- Full validator run: **valid** (exit 0).
- Replica of required_ids at release=v0.4.27: missing=[], extra=[].

### Test 2 — mission intent: add release-only ci-fast-check gate, keep the other 62 at v0.4.27
- catalog `release` field = `v0.4.27`; add `atomic/static/ci-fast-check` gate with
  `selection_scope=release-only`, `required_for=[v0.4.28]`.
- Remove `v0.4.28` from the other 62 gates' `required_for` (they were delivered in v0.4.27).
- Full validator run: **FAILS** with
  `coverage catalog includes gates outside active release catalog: atomic/static/ci-fast-check`.
- Replica: missing=[], extra=['atomic/static/ci-fast-check'].

### Test 3 — the impossible middle
- With the catalog `release` field fixed at a single value:
  - `release = v0.4.27` -> the 62 delivered gates are required; the v0.4.28-only
    ci-fast-check gate is `extra` -> FAILS.
  - `release = v0.4.28` -> only the v0.4.28 gates are required; the 62 v0.4.27-only gates
    become `extra` (62 entries) -> FAILS.
- There is no single `release` value that makes both the 62 delivered gates (v0.4.27) AND
  the ci-fast-check gate (v0.4.28-only) simultaneously required. This is a structural
  limitation of the single-release-field `required_ids` design at validator:249-250, not a
  data error in either file.

## Options matrix (all presented to the owner)

- (A) Keep the frozen blanket-add of v0.4.28 to all 62 existing gates (accept
  208ee7607's release-requirements file). Validator passes, but the mission states only
  ci-fast-check should move — the blanket add contradicts that intent.
- (B) Bump the catalog `release` field to v0.4.28. Already rejected by the owner earlier
  this turn; also flips the 62 delivered gates into `extra`.
- (C) Edit `scripts/validate-pr-gate-coverage.py:249-250` so `required_ids` is not keyed on
  a single `release` value. Already rejected by the owner this turn (no edits to
  scripts/*.py outside the write-set).
- (D) Document the validator `extra` flag as an upstream reconciliation item for the owner
  to resolve, leaving the release-only gate in place.

## Owner ruling (2026-11-23, authoritative, conflict rule §1)

None of the four options is to be executed. Escalate to the owner: the empirical finding
with file:line proof accompanies this escalation. For #1746, HOLD — do not force anything
locally, do not push, and leave 208ee7607 exactly as it is. The #1746 mission continues or
is rewritten only after the owner's ruling.

## File/line proof
- `scripts/validate-pr-gate-coverage.py:120` — `release = coverage.get("release")`
- `scripts/validate-pr-gate-coverage.py:121` — `release not in requirements["releases"]`
- `scripts/validate-pr-gate-coverage.py:249-250` — `required_ids` keyed on the single
  `release` value
- `scripts/pr-gate-coverage.json` — catalog `release` field, `atomic/static/shell-ux`
  `selection_scope`
- `scripts/release-requirements.json` — gate `required_for` lists, new
  `atomic/static/ci-fast-check` gate

## Cleanliness
- No files under `scripts/` were modified in this session. The working-tree catalog edit
  from an earlier turn remains but was NOT force-pushed; no remote state changed.
- No subagents. No push, no merge, no force.
