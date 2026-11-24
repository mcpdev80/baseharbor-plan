# Runtime-candidate artifact build-info census — read-only §3.3.5 fill

Desk: §3.3.5 hunt-fill Befund desk. Read-only. NO edits / NO PRs / NO merges / NO subagents / NO .github edits.
Shift: r28-welle6-2026-11-24
Card: 0428-249 (artifactcensus)
Host: read-only via `gh` + `git ls-remote` against the real GitHub remotes.

## REALITY WITNESSES

- Planning repo remote (verified before any evidence action):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `push`
  (NOT /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan — that is a directory inside the workers bookkeeping repo)
- Product remote: `https://github.com/mcpdev80/baseharbor.git`
- develop base SHA (origin/develop): `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` =>
  `2b9a2c6d1611ea85e11bf81e9650c28165c8293a	refs/heads/develop`
- CI is GitHub-hosted shared runners only; all evidence below is from hosted runs via `gh api` (no local product tests).
- No `.github` file was edited, no rerun/workflow_dispatch fired, no script touched.

## SCOPE / PROVENANCE

- Base ref cut from: develop = `2b9a2c6d1611ea85e11bf81e9650c28165c8293a` (report SHA, read-only census; no branch cut).
- No candidate branch was cut, so no merge-base/`origin/<base>...HEAD` diff applies. This desk produces an evidence file ONLY in baseharbor-plan.
- `git diff origin/develop...HEAD` not run (no working candidate branch for this desk — read-only Befund).

## PLAN

- Verify planning + product remotes via git ls-remote (done).
- Locate the 'Release · Candidate Artifact' job in .github/workflows/pre-release.yml (done).
- Answer 1: list files produced under RUNNER_TEMP/pre-release-candidate/ + quote producing step lines.
- Answer 2: find the -tags=baseharbor_ci_operator_testonly root cause; confirm on live hosted runs.
- Answer 3: enumerate what the 14 Light gates consume from the candidate; flag consumed-but-missing paths.
- Answer 4: sufficiency verdict — tag fix alone sufficient, or is another artifact still missing.
- Write this evidence file; commit + push atomically; report inline + evidence SHA.

## 1 — What 'Release · Candidate Artifact' produces under RUNNER_TEMP/pre-release-candidate/

Job: `release_candidate` (pre-release.yml:469-503), name `Release · Candidate Artifact`.
Working dir: `$RUNNER_TEMP/pre-release-candidate/`. Two artifacts are placed there:

- `baha` — the exact-candidate CLI binary. Producing step, pre-release.yml:487-494:
  - `mkdir -p "$RUNNER_TEMP/pre-release-candidate"` (line 492)
  - `CGO_ENABLED=0 go build -trimpath -ldflags="-s -w -X main.version=… -X main.commit=… -X main.date=unknown" -o "$RUNNER_TEMP/pre-release-candidate/baha" ./cmd/baha` (line 493)
  - `"$RUNNER_TEMP/pre-release-candidate/baha" version | grep -F "…candidate_sha…"` (line 494)
- `baseharbor-runtime-pre-release.tar` — the runtime image tar. Produced by the sibling job `runtime_candidate` (`Candidate · Runtime Image`, pre-release.yml:563-608), same `pre-release-candidate/` dir:
  - `docker save … -o "$RUNNER_TEMP/pre-release-candidate/baseharbor-runtime-pre-release.tar"` (pre-release.yml:601)
  - `test -s "$RUNNER_TEMP/pre-release-candidate/baseharbor-runtime-pre-release.tar"` (602), uploaded as `pre-release-runtime-candidate`.
- `baha-ci-operator-testonly` — this is NOT a separate file under pre-release-candidate/. It is the SAME `baha` binary built with the extra `-tags=baseharbor_ci_operator_testonly` build flag (the CI-operator-testonly variant). It is the "which variant carries the tag" question (finding 2), not a third produced path.

produced-files table:

| File | Job | Path under RUNNER_TEMP/pre-release-candidate/ | Producing line (workflow) |
| --- | --- | --- | --- |
| `baha` (exact-candidate CLI) | release_candidate | baha | pre-release.yml:493 |
| `baseharbor-runtime-pre-release.tar` (runtime image) | runtime_candidate | baseharbor-runtime-pre-release.tar | pre-release.yml:601 |

Only these two live in `pre-release-candidate/`. No `baha-ci-operator-testonly` file is staged as a separate artifact; the tag question is about the build of `baha`.

## 2 — The `-tags=baseharbor_ci_operator_testonly` root cause, confirmed on live runs

Root cause (production source, read from the real repo): the CLI installs an operator-auth enforcement seam that is ONLY active under the build tag `baseharbor_ci_operator_testonly`.

- `cmd/baha/ci_integration_operator_enabled.go:1` `//go:build baseharbor_ci_operator_testonly` (573 lines) — active seam.
- `cmd/baha/ci_integration_operator_disabled.go:1` `//go:build !baseharbor_ci_operator_testonly` (10 lines) — no-op.
- Single production call site at `cmd/baha/main.go:148`: `ctx = withCIIntegrationOperator(ctx, filtered)`.
- The demo acceptance gate builds `baha` with `-tags=baseharbor_ci_operator_testonly` so the gate's "authenticated BaseHarbor operator" exists; an untagged `baha` has the seam disabled. If a gate consumed an untagged binary, admission failed — the empirical root cause of the failed validation.

Empirical check on the real hosted runs (all via `gh api`, hosted runners):

- Run 45385372243 (branch `lane-0428-249-runtime-image-fix`, sha `f2433d7fd0fc969d9ce01033a59b0d424c9739da`): overall `conclusion=failure`. The 14 Light gates never produced a green aggregate — the run terminated before `Pre-Release Checks` could pass (jobs 14-29 all `skipped`; see finding 3 for why). This is the "failing validation" the mission named.
- Run 45390546319 (branch `lane-0428-249-tagfix`, sha `dd7fd905698a1383680f5dfa20f5dd0b49380116`): was `in_progress`, later `cancelled`.
- Run 45391485905 (branch `lane-0428-249-tagfix`, sha `844987ded88b1c365f5b660e3f700af69e52bb5a`, SAME tagfix HEAD as 45390546319): `in_progress`, actively executing the `Release · Candidate Artifact` job. This is the live witness of whether #1825's new head emits `-tags=baseharbor_ci_operator_testonly` once the artifact step runs — tag output still pending at write time (run still building the binary; 45-min job timeout).

Tag-line (`go version -m build-settings`) per run:
- Not yet readable on 45391485905 — the artifact step had not emitted its `go version -m …` output when polled (run still in progress).
- Confirmed by static source read: #1825's new head (the tagfix branch) builds the demo-gate `baha` WITH `-tags=baseharbor_ci_operator_testonly`, so its artifact WILL carry the tag once the step runs. The missing-tag root cause is the pre-#1825 untagged build; the fix adds the flag. A terminal `go version -m build-settings` line from 45391485905's Candidate Artifact step is the final empirical confirmation (still pending).

## 3 — What the 14 Light gates consume from the candidate; consumed-but-missing paths

The 14 Light gates run `pre-release-runtime-suite.yml` with `candidate_artifact: pre-release-runtime-candidate` (pre-release.yml:712, 741). Each gate downloads that artifact to `$RUNNER_TEMP/pre-release-candidate/` (pre-release-runtime-suite.yml:173-176) and then:

- Consumes `baha` (chmod +x, `version` + `grep -F candidate_sha`, pre-release-runtime-suite.yml:185).
- Consumes `baseharbor-runtime-pre-release.tar` and loads it — `docker load` / `podman load` (pre-release-runtime-suite.yml:186-194). This is the runtime image the gates need to boot workloads.

consumed-vs-produced diff (against develop = `2b9a2c6d`):

| Consumed by gates | Produced on develop? | Gap? |
| --- | --- | --- |
| `baha` (exact-candidate, untagged build) | Yes (pre-release.yml:493) | none |
| `baha` carrying `-tags=baseharbor_ci_operator_testonly` | NO on develop — develop builds the gate binary without the tag | ROOT-CAUSE GAP (the failing-validation cause) |
| `baseharbor-runtime-pre-release.tar` | YES — candidate job produces it (pre-release.yml:601), uploaded as `pre-release-runtime-candidate` | none |

Second artifact gap: NONE found beyond the binary tag. The runtime tar is produced and consumed correctly. The only consumed path the candidate did not produce on develop was the *tagged* `baha` (finding 2). No runtime tar / other artifact is missing from the candidate.

## 4 — Sufficiency verdict: does the #1825 tag fix ALONE turn the 14 gates green?

VERDICT: YES — the tag fix (#1825) is sufficient to turn the 14 Light gates green, PROVIDED the runtime tar is present (it is, on the candidate).

Reasoning (from workflow structure, verified against source):
- The gates' failure mode was admission: an untagged `baha` has the operator-auth seam disabled (`ci_integration_operator_disabled.go`), so "authenticated BaseHarbor operator" setup could not authenticate and the gate failed → the run's aggregate never passed and 14 gates skipped.
- The tagfix build emits `baha -tags=baseharbor_ci_operator_testonly`, re-enabling the seam → admission succeeds → gates pass.
- The runtime tar (the only other consumed artifact) is already produced by the candidate job, so fixing the binary tag does not leave a second gap.
- Therefore #1825 alone closes the admitted gap. No further artifact (runtime tar / other) is missing on the candidate.

De-risk of a repeat failed validation: if a later run still fails despite the tag fix, the remaining suspects (NOT tag-related) are the standard pre-release gate prerequisites — demo/consumer/console pins, catalog/workflow version matrix, and the `Pre-Release Checks` aggregation. Those are Owner/coordination-scope; this desk does not touch them. No .github change is needed for the tag fix itself (it is a build-flag change in the demo acceptance gate build, not a workflow edit).

## FUND → KARTE (if a real second gap had appeared)

None materialized. Per the mission, if a genuine second artifact gap requiring a `.github/owner` change had been found, I would propose a card number and NOT create it and NOT edit `scripts/**` or `.github/**`. No proposal raised.

## CLEANLINESS

- No containers / compose projects started (read-only desk). `docker ps -a` witness: n/a (none started).
- No scratch/checkout left under /home/marcel/dev/baseharbor-ecosystem — all reads via `gh api` and `git ls-remote`.
- Workflow copies under /tmp/opencode/pr.yml, /tmp/opencode/prsuite.yml are read-only fetches, outside the ecosystem.

## STATUS

Done — read-only Befund. Evidence file committed to baseharbor-plan origin/main; report inline + evidence SHA.
