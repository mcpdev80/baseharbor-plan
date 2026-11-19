# 0428-142 — perses status backend-witness — evidence, fix-3 (correction round STOP)

Card: t-20261119-r28-perses-status-backend-witness
CardNumber: 0428-142
Release: v0.4.28
Worker: laptop (correction round, 0428-142)
Date: 2026-11-20

## HEAD

Branch: lane-0428-142-statuswitness
PR: https://github.com/mcpdev80/baseharbor/pull/1702 (OPEN, not draft)

### Branch provenance (proof)

- `git ls-remote origin/refs/heads/lane-0428-142-statuswitness`: `6740299f91c040af7b1357d63be898eac57669f5`
- `git ls-remote origin/refs/heads/develop`: `4b3a3559070e9b81b1886a357f6a46bc6dfce790` (HEAD of develop at this reading)
- Candidate head `6740299f...` has exactly two parents (a real merge):
  - parent1 (my prior candidate head): `56d85ddb63aff806b10253912edc973c18c0e704`
  - parent2 (develop HEAD at the hopf): `28fb427f057499efca705c1b7459e7653bd532a8`
- `git log -1 --format=%P 6740299f91c040af7b1357d63be898eac57669f5` => `56d85ddb63aff806b10253912edc973c18c0e704 28fb427f057499efca705c1b7459e7653bd532a8` (two parents)
- `git merge-base --is-ancestor origin/develop 6740299f...` => exit 1: the candidate is **behind** the current develop head `4b3a3559070e` (develop advanced after the hopf). This is why A5 (a real merge onto the live develop) is not yet done.
- No force-push this shift. `git log --oneline origin/develop..6740299f` lists my hopf merge + gofmt follow-up only; no foreign candidate carried on top.

### CI run for the EXACT head this shift (only the SHA-genaue candidate counts)

- Run: `44621032956` | event: `pull_request` | head: `6740299f91c040af7b1357d63be898eac57669f5` | status: completed — conclusion: **success** | `PR Selected Checks` => success.
- This run is on the **unchanged** candidate head (no code change was made this shift, so there is no new run — see A6 below, which cannot produce one without a change).

## PLAN

1. Reality (§4.1): read the mission `/var/tmp/x-142r5.txt` verbatim, the review verdict `codex-review-wave/1702-0428-142-r4.md` verbatim, and the product source from a fresh clone of `https://github.com/mcpdev80/baseharbor` checked out at `lane-0428-142-statuswitness`. No quarantined checkout, no subagent.
2. Reproduced the P2 finding by code read (the task says "befund erst reproduzieren, dann aendern"):
   - `cmd/baha/app_status_result.go:76-139` — `persesBackendSignalWitnessFromManifest` derives **every** verdict from manifest-declaration checks only. `metricsProven := application.HasMetricsSources(m)` / `logsProven := application.HasLogsCollection(m)` / `tempoProven := application.HasOTLPTelemetry(m)` = `len(m.Metrics.Sources)`, `len(m.Logs.Collect)`, `m.Telemetry.OTLP != nil`. No backend's own answer is read. Declared signal => `configured`; absent => `not-configured`.
   - `cmd/baha/app_status_result.go:64-65` — `persesBackendUnreachable persesBackendSignal = "unreachable"` is DECLARED but has **no emission path anywhere in the tree**.
3. Confirmed there is no real backend evidence seam to wire in:
   - The only real backend probe in the tree, `internal/logs/loki_datasource.go:196` `BuildPersesLokiDatasourceWithProbe`, is a **dead endpoint** — declared, never called by any live path, and only for Loki (no Prometheus/Tempo equivalent exists).
   - `internal/capability/perses.go` `PersesManagementSurface.Now` carries a `Reachability` field but is **never wired** into the witness (`grep` of the whole tree confirms).
   - Both `persesBackendSignalWitnessFromManifest` call sites (`app_status_result.go:250`, `:353`) and the human face (`perses_lifecycle.go:232`) feed it only `resolved.Manifest`. No backend is ever observed.
4. Decision per A2/A5: the fix (a per-backend evidence seam consuming an authoritative, source-id-bound backend answer for Prometheus/Loki/Tempo, plus a real `unreachable` emission path) is exactly the artifact card **0428-143** defines. It does not exist. The task forbids (a) inventing the seam / fabricating `unreachable` from a manual flag, (b) touching `cmd/baha/app_status_collect.go` beyond A1-A3 (0428-152 is deliberately parked behind this PR), (c) touching the P4/P5 owner-gated paths. So the P1/P2 core cannot be fixed this shift without a scope violation.
5. Consequences of the stop, mapped to the mission's own fixable list:
   - **A3 (P3) `TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends`:** only meaningful once P1/P2 are fixed. Extending it now would pin the *current* over-claiming witness (every backend `configured`) as the contract — precisely what the review rejects. Deferred with P1/P2.
   - **A4 (P7 akte neu, fix-3.md):** requires a *new* run on a *new* head, the red-before/green-after, the job conclusions, and the post-push `ls-remote`. None can exist without a change — so A4 is **also** blocked this shift. Writing an "erledigt" now would reproduce exactly the P7 defect.
   - **A5 (real hopf) + A6 (new CI run):** require a code change on a live develop; impossible without a change. The candidate remains behind live develop `4b3a3559070e`.
6. Scope guard (P5) respected: did not touch `internal/application/provider_registry.go`, `internal/observability/registry.go`, `internal/application/provider_consent_authority.go`, or `cmd/baha/app_status_collect.go`. No write, no merge, no `.github/**`, no `scripts/test_pr_*`, no subagent.
7. Host hygiene: no container/compose/volume started on this host (the coordinator server); host besenrein.

## repo-rule compliance

- No code change this shift: the candidate head `6740299f91c040af7b1357d63be898eac57669f5` is unchanged; no new PR run exists, which is correct (A6 cannot produce one without a change).
- Base attestation: candidate cut from hopf base `28fb427f057499efca705c1b7459e7653bd532a8` (second parent of the two-parent merge `6740299f`), confirmed via `git log -1 --format=%P`. Current develop head `4b3a3559070e` is a later docs-only commit (#1697, identical blobs); the candidate is behind it and awaiting a real merge (A5) once the P1/P2 blocker is resolved.
- Evidence written from my own fresh clone of `https://github.com/mcpdev80/baseharbor`, NOT the quarantined workers checkout. No write under `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- No subagent (§4.8): every step in this session.
- P4/P5 left to the Owner exactly as the task directs: P4 = acceptance held until `unreachable` has a real/owner-authorized evidence path; P5 = the `cmd/baha/` vs `internal/application/` scope split is an Owner question, not a fix.

## CLEANLINESS

- no containers / compose projects / volumes / networks started on this host
- cleanliness: clean

## BLOCKER (the exact place and the verdict sentence I cannot satisfy)

**File: `cmd/baha/app_status_result.go`, function `persesBackendSignalWitnessFromManifest` (lines 76-139) and enum `persesBackendUnreachable` (line 64-65).**

The review verdict (`1702-0428-142-r4.md`, P2/P4) and the mission's A2/A5 require: a per-backend evidence seam that consumes an **authoritative, source-id-bound backend answer** for Prometheus/Loki/Tempo, and a real emission path for `unreachable`. This does not exist in this Core:

- `configured` is emitted from manifest flags alone (`HasMetricsSources`/`HasLogsCollection`/`HasOTLPTelemetry`) — no backend is ever observed. Over-claim the card forbids.
- `unreachable` has no emission path; the only real backend probe (`BuildPersesLokiDatasourceWithProbe`) is a dead endpoint, and no Prometheus/Tempo probe exists. The `Verification=none`/probe contract that would make `unreachable` decisionable lives in card **0428-143**, which the task marks as an open owner dependency.

A2 is explicit: when the only path to `unreachable` requires an evidence proof 0428-143 does not yet grant, STOP at that file:line and report the unsatisfiable verdict sentence — build no throwaway test that produces `unreachable` from a manual flag. I stop exactly there.

## END

`END_BLOCKED x-142r5: 0428-142 correction round. The P1/P2 core cannot be fixed this shift: `persesBackendSignalWitnessFromManifest` (cmd/baha/app_status_result.go:76-139) emits `configured` from manifest flags alone and `persesBackendUnreachable` (cmd/baha/app_status_result.go:64-65) has no emission path — the fix needs the per-backend evidence seam + `Verification=none` probe contract of card 0428-143, which is an open owner dependency. Task forbids inventing the seam or fabricating `unreachable`. A3/A4/A5/A6 are downstream of P1/P2 and thus also blocked. Candidate head 6740299f91c040af7b1357d63be898eac57669f5 (two parents, base 28fb427f) unchanged; behind live develop 4b3a3559070e awaiting a real merge once P1/P2 resolves. Scope guard (P5/P4) respected: no write, no merge, no .github/scripts. CI run 44621032956 head=6740299f pull_request=success (unchanged candidate).`
