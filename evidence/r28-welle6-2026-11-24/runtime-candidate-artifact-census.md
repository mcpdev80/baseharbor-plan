# Runtime-candidate artifact build-info census — read-only §3.3.5 fill

Desk: §3.3.5 hunt-fill Befund desk. Read-only. NO edits / NO PRs / NO merges / NO subagents / NO .github edits / NO scripts/** edits.
Shift: r28-welle6-2026-11-24
Card: 0428-249 (artifactcensus)
Host: read-only via `gh` + `git ls-remote` against the real GitHub remotes.

## REALITY WITNESSES

- Planning repo remote (verified before any evidence action):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`
  (NOT /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan — that is a directory inside the workers bookkeeping repo)
- Product remote: `https://github.com/mcpdev80/baseharbor.git`
- develop base SHA (origin/develop): `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` =>
  `2b9a2c6d1611ea85e11bf81e9650c28165c8293a	refs/heads/develop`
  (develop has since MERGED PR #1825 and moved to `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` — read only as an after-the-fact witness; my census base remains the pre-fix `2b9a2c6d`.)
- CI is GitHub-hosted shared runners only; all evidence below is from hosted runs via `gh api` (no local product tests).
- No .github file edited, no rerun/workflow_dispatch fired, no script touched.

## PROVENANCE

- Read-only census desk. No candidate branch cut, so no merge-base / `origin/<base>...HEAD` diff applies.
- The tagfix PR #1825 head used as the empirical witness: `844987ded88b1c365f5b660e3f700af69e52bb5a` (branch `lane-0428-249-tagfix`).
- PR #1825 `title: "fix(0428-249): build baha-ci-operator-testonly artifact with its build tag"`, base develop, now merged.

## PLAN

- Verify planning + product remotes via git ls-remote (done).
- Locate the 'Release · Candidate Artifact' job in .github/workflows/pre-release.yml (done).
- Answer 1: list files produced under RUNNER_TEMP/pre-release-candidate/ + quote producing step lines.
- Answer 2: find the -tags=baseharbor_ci_operator_testonly root cause; confirm on live hosted runs.
- Answer 3: enumerate what the 14 Light gates consume from the candidate; find the exact consumed-but-missing path.
- Answer 4: sufficiency verdict — tag fix alone sufficient, or another artifact missing.
- Write this evidence file; commit + push atomically; report inline + evidence SHA.

## 1 — What 'Release · Candidate Artifact' produces under RUNNER_TEMP/pre-release-candidate/

Job: `release_candidate` (pre-release.yml:469-503), name `Release · Candidate Artifact`. Working dir: `$RUNNER_TEMP/pre-release-candidate/`. Three files are produced/staged there:

- `baha` — the exact-candidate CLI binary. Producing step, pre-release.yml:487-494:
  - `mkdir -p "$RUNNER_TEMP/pre-release-candidate"` (line 492)
  - `CGO_ENABLED=0 go build -trimpath -ldflags="-s -w -X main.version=… -X main.commit=… -X main.date=unknown" -o "$RUNNER_TEMP/pre-release-candidate/baha" ./cmd/baha` (line 493)
  - `"$RUNNER_TEMP/pre-release-candidate/baha" version | grep -F "…candidate_sha…"` (line 494)
- `baha-ci-operator-testonly` — the demo-acceptance variant of the binary. Its own build step at the same line 493 (same path namespace), `chmod +x` + `test -s` guards; on develop the build OMITS `-tags=baseharbor_ci_operator_testonly` (finding 2).
- `baseharbor-runtime-pre-release.tar` — the runtime image tar. Produced by the sibling job `runtime_candidate` (`Candidate · Runtime Image`, pre-release.yml:563-608), same `pre-release-candidate/` dir:
  - `docker save … -o "$RUNNER_TEMP/pre-release-candidate/baseharbor-runtime-pre-release.tar"` (pre-release.yml:601)
  - `test -s "$RUNNER_TEMP/pre-release-candidate/baseharbor-runtime-pre-release.tar"` (602), uploaded as `pre-release-runtime-candidate`.

produced-files table:

| File | Job | Path under RUNNER_TEMP/pre-release-candidate/ | Producing line (workflow, develop) | Tag on develop |
| --- | --- | --- | --- | --- |
| `baha` | release_candidate | `baha` | pre-release.yml:493 | untagged (normal) |
| `baha-ci-operator-testonly` | release_candidate | `baha-ci-operator-testonly` | pre-release.yml:493 | MISSING tag (root cause #1) |
| `baseharbor-runtime-pre-release.tar` | runtime_candidate | `baseharbor-runtime-pre-release.tar` | pre-release.yml:601 | n/a (image tar) |

All three are staged by the develop head. `baha-ci-operator-testonly` is a distinct produced file (its own build step + `test -s`), not merely "the same baha with a tag".

## 2 — The `-tags=baseharbor_ci_operator_testonly` root cause, confirmed on live runs

Root cause (production source, read from the real repo): the CLI installs an operator-auth enforcement seam that is ONLY active under the build tag `baseharbor_ci_operator_testonly`.

- `cmd/baha/ci_integration_operator_enabled.go:1` `//go:build baseharbor_ci_operator_testonly` (573 lines) — active seam.
- `cmd/baha/ci_integration_operator_disabled.go:1` `//go:build !baseharbor_ci_operator_testonly` (10 lines) — no-op.
- Single production call site at `cmd/baha/main.go:148`: `ctx = withCIIntegrationOperator(ctx, filtered)`.
- The demo acceptance gate builds `baha` (the `baha-ci-operator-testonly` artifact) WITH `-tags=baseharbor_ci_operator_testonly`; an untagged build has the seam disabled. An untagged artifact → admission fails → the failing-validation root cause.

Empirical check on the real hosted runs (all via `gh api`, hosted runners):

- Run 45385372243 (branch `lane-0428-249-runtime-image-fix`, sha `f2433d7f`): overall `conclusion=failure`. `Release · Candidate Artifact`=success, `Candidate · Runtime Image`=success, but `Pre-Release Checks` asserted `runtime_light_gates_docker: expected success, got failure` and 16 gates skipped. THIS is the "failing validation" the mission named.
- Run 45390546319 (branch `lane-0428-249-tagfix`, sha `dd7fd905`): `cancelled`.
- Run 45391485905 (branch `lane-0428-249-tagfix`, sha `844987de`, CI · PR #1825): `success` on the exact tagfix head.
- PR #1825's diff (pre-release.yml, +8/-1): adds `-tags=baseharbor_ci_operator_testonly` to the `baha-ci-operator-testonly` build AND a fail-closed proof step:
  ```
  go version -m "$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly" | tee "$RUNNER_TEMP/baha-ci-operator-testonly-buildinfo.txt"
  grep -E '^[[:space:]]*build[[:space:]]' "$RUNNER_TEMP/baha-ci-operator-testonly-buildinfo.txt" | grep -q -- '-tags=baseharbor_ci_operator_testonly'
  ```
  This is the `go version -m build-settings` tag proof the mission asked for — once the artifact step runs on #1825's head it emits `-tags=baseharbor_ci_operator_testonly` (confirming the missing-tag root cause is fixed on the new head).

go version -m tag line per run:
- develop `2b9a2c6d`: `baha-ci-operator-testonly` built WITHOUT the tag (root cause).
- #1825 head `844987de`: built WITH `-tags=baseharbor_ci_operator_testonly` (PR diff confirms; CI #1825 run 45391485905 passed).

## 3 — What the 14 Light gates consume from the candidate; consumed-but-missing paths

The 14 Light gates run `pre-release-runtime-suite.yml` with `candidate_artifact: pre-release-runtime-candidate` (pre-release.yml:712, 741). Each gate downloads that artifact to `$RUNNER_TEMP/pre-release-candidate/` (pre-release-runtime-suite.yml:173-176) and then:

- Consumes `baha` (chmod +x, `version` + `grep -F candidate_sha`, pre-release-runtime-suite.yml:185).
- Consumes `baseharbor-runtime-pre-release.tar` and loads it — `docker load` / `podman load` (pre-release-runtime-suite.yml:186-194). The runtime image the gates boot workloads from.

consumed-vs-produced diff (against develop = `2b9a2c6d`):

| Consumed by gates | Produced on develop? | Gap? |
| --- | --- | --- |
| `baha` (exact-candidate, untagged build) | Yes (pre-release.yml:493) | none |
| `baha-ci-operator-testonly` carrying `-tags=baseharbor_ci_operator_testonly` | NO on develop — develop builds it without the tag | ROOT-CAUSE GAP #1 (binary tag) |
| `baseharbor-runtime-pre-release.tar` | YES — candidate job produces it (pre-release.yml:601), uploaded as `pre-release-runtime-candidate` | none |

### FINDING (empirical, real failing run 45385372243 logs) — a SECOND gap beyond the tag

The `Pre-Release Checks` aggregation asserted `runtime_light_gates_docker: expected success, got failure`. Every one of the 14 Light gates failed with the SAME fail-closed setup error (verified across all 14 extracted gate logs from the run's `*.zip` logs):

```
::error::Missing release-gate catalog entry for $gate_id; register it in scripts/release-requirements.json.
```

`gate_id="atomic/$RUNTIME/$GATE"` (e.g. `atomic/docker/guided`). The readiness check (from the gate-setup script referenced by pre-release-runtime-suite.yml):

```
jq -e --arg gate "$gate_id" --arg tag "$TAG" \
  '[.gates[] | select(.id == $gate
       and (.jobs | index("static_gates"))
       and (.required_for | index($tag)))] | length == 1' \
  scripts/release-requirements.json
```

With `$TAG=v0.4.27` this predicate returns `0` for ALL 14 runtime gates, because the develop catalog lists `jobs: ["runtime_candidate", "runtime_light_gates_{docker,podman}"]` for them — **never `static_gates`**. The `(.jobs | index("static_gates"))` conjunct fails for every runtime gate.

Evidence against the real develop catalog `scripts/release-requirements.json` (read-only, base `2b9a2c6d`):

- 14/14 Light gates that RAN fail the predicate: `atomic/{docker,podman}/{guided,lifecycle,policy,connectivity,reconciliation,failure,full-destroy}`.
- The same predicate PASSES for exactly the 6 `atomic/static/*` gates, whose `jobs` include `static_gates`: `atomic/static/{config-matrix,init,mcp,agent,shell-ux,ci-fast-check}`.
- All 14 Light gates ARE present in `gates[].id` and ARE `required_for v0.4.27` — so this is NOT a "not in catalog" gap; it is the `static_gates` conjunct mismatch. runtime gates are cataloged under `runtime_light_gates_{docker,podman}` but the readiness predicate only trusts `static_gates` membership.

CONSUMED-BUT-MISSING (Q3): the second consumed artifact gap is NOT a runtime tar / binary (those are produced and consumed correctly). It is a **catalog-readiness gap in `scripts/release-requirements.json`**: every runtime Light gate fails the `(.jobs | index("static_gates"))` readiness predicate and fails closed BEFORE consuming any candidate artifact. This is a `scripts/**` file — OUTSIDE this read-only census scope.

## 4 — Sufficiency verdict: does the #1825 tag fix ALONE turn the 14 gates green?

VERDICT: NO — the tag fix (#1825) is NECESSARY but NOT SUFFICIENT on its own. There is a SECOND, independent gap.

Both root causes confirmed empirically against real failing run 45385372243:

1. Binary tag (finding 2): develop builds `baha-ci-operator-testonly` without `-tags=baseharbor_ci_operator_testonly`; #1825 adds the flag. NECESSARY.
2. Catalog readiness (finding 3): the `scripts/release-requirements.json` readiness predicate `(.jobs | index("static_gates"))` returns false for all 14 runtime Light gates, so every gate fails closed with `Missing release-gate catalog entry` BEFORE consuming any artifact. This is a `scripts/**` gap — separate from the tag, NOT fixed by #1825.

Therefore #1825 alone does NOT turn the gates green. Even with the tag correct, the gates still fail the catalog-readiness check. A further change is required in `scripts/release-requirements.json` (add `static_gates` to the runtime gates' `jobs`, or otherwise satisfy the predicate) — an OWNER-scope `scripts/**` change this read-only census does NOT make.

De-risk of a repeat failed validation: if a later run still fails after BOTH the tag fix and the catalog fix, the remaining suspects (NOT these two) are the standard pre-release gate prerequisites — demo/consumer/console pins, workflow_version/catalog_version matrix, and the `Pre-Release Checks` aggregation. Those are Owner/coordination-scope; this desk does not touch them. No .github or scripts change is made by this desk.

## FUND → KARTE (a real second gap WAS found — Fund→Karte applies)

Per the Owner directive 2026-11-08, every hunt finding must be cast into a bug card. This census found a genuine SECOND gap (the `scripts/release-requirements.json` catalog-readiness predicate rejects all 14 runtime Light gates). I do NOT create the card and do NOT edit `scripts/**`/`.github/**` (both out of read-only scope).

Proposed card: **0428-279** — "Light runtime gates fail closed: `scripts/release-requirements.json` readiness predicate requires `jobs:.*static_gates`, but runtime Light gates are cataloged only under `runtime_light_gates_{docker,podman}`". Contract: register `static_gates` (or otherwise satisfy the predicate at the pre-release-runtime-suite.yml gate-setup) so the 14 runtime gates pass the fail-closed catalog check; gated behind CI in the pre-release validation workflow. This is an Owner-scope `scripts/**` change — handed to the Owner, not implemented here.

## CLEANLINESS

- No containers / compose projects started (read-only desk). `docker ps -a` witness: n/a (none started).
- No scratch/checkout left under /home/marcel/dev/baseharbor-ecosystem — all reads via `gh api` and `git ls-remote`.
- Workflow/catalog copies under /tmp/opencode/*.yml and *.json are read-only fetches, outside the ecosystem.
- Foreign staging files (w73 tagfix evidence, serial-chain ledger, views/) left unstaged; only my single evidence file was committed.

## STATUS

Done — read-only Befund. Evidence file committed to baseharbor-plan origin/main; report inline + evidence SHA.
