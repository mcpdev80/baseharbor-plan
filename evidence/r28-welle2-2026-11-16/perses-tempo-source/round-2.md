# Round 2 — Correction of PR #1610 / Perses Tempo datasource

Task: t-20261114-r28-perses-tempo-source
PR: #1610 (OPEN, DRAFT)
Reviewer: CODEX-Luna (act-luna-1610-r1.md)
Role: WORKER (correction round)
Model: worker-ornith1.5-laptop (session-scoped)

## PLAN

1. Confirm base/head provenance (origin/main bdafd838; base lane-0428-075-perses-seam @492b8e8f; head c27e7a789a1; branch w091-0428-091).
2. ls-remote witness on origin before touching anything; write base SHA into evidence.
3. Study internal/metrics/perses_tempo_datasource.go health + builder for fail-closed gaps.
4. Fix 1 — health verifier fails closed without a real Tempo probe.
5. Fix 2 — builder enforces selection, Tempo ownership, authorization; propagate missing/denied errors; no default datasource without authorized source.
6. Fix 3 — prove missing/denied/unreachable endpoint fail; successful probe required.
7. Add negative tests: Perses unselected, Tempo absent, denied/unknown owner, missing provider endpoint -> no datasource.
8. Local go build + go vet + targeted tests (verbatim).
9. Commit on w091-0428-091 as DRAFT; git log origin/lane-0428-075-perses-seam..HEAD = only own commits; show ancestor SHA.
10. Commit round-2.md evidence; push draft; evidence must reach origin/main; END with new head SHA.

## Review findings (from act-luna-1610-r1.md — binding)

1. Health verification passes without a health check: VerifyPersesTempoDatasourceHealth returns nil once the release pin validates; no request/provider/rreachability evidence. Fix: fail closed when no real Tempo probe available.
2. Builder does not enforce selection, authorization, or source presence: BuildPersesTempoDatasource and persesTempoDatasourceFromRelease validate only the release; provider endpoint errors discarded (lines 136-139) and a default datasource with empty config and nil error is returned. Fix: use manifest selection, Tempo ownership, TLS and tenant/Target authorization; propagate errors; no default datasource.
3. Native plugin and actual trace-query behavior not verified: golden file is self-produced; tests assert constants; TestPersesTempoDatasourceNegativeWrongKind compares two literals. Fix: validate emitted resource against pinned plugin, exercise real trace query through authorized endpoint; non-vacuous negative tests.

## Provenance

- plan origin/main: bdafd838
- PR base (lane-0428-075-perses-seam): 492b8e8f994b16e6f73819a08175f8178cd63292
- reviewed head: c27e7a789a1b6eaf52afabcb545e1a9e351b057a (w091-0428-091)
- Branch: w091-0428-091 (per mission; base lane-0428-075-perses-seam unchanged)

## Work performed

- (numbered, plain bullets, no markdown checkboxes)

## Corrections applied

### Fix 1: health verifier
### Fix 2: builder fail-closed
### Fix 3: tests

## Test requirement / CI mapping

## Local runs (verbatim)

## Evidence

## END status

- Lane: w091-0428-091
- Base: lane-0428-075-perses-seam @492b8e8f (unchanged)
- Status: DONE / BLOCKED (one)
