# Probe 1 — docker-lifecycle dispatch-vs-push asymmetry (ORAS / trust plane)

Mission: docker-gate-probe. Lane: mission-docker-gate-probe.md. Read-only diagnosis; no product change, no PR, no .github edit.

## Work plan (## PLAN)

1. Read mission; before-list on baha-docker host — done (see cleanliness).
2. A/B dispatch observation — A (develop head `deeeb6477`) dispatched as run 44466684726 and B (candidate `84ee9a93e`, only reachable via ref `lane-0428-119-consent-hard`, PR #1690; raw-SHA dispatch is rejected by GitHub: `No ref found for: 84ee9a93e…`, 422) dispatched as run 44466748992. Both were observed to terminal FAILURE by this lane before the coordinator stand-meinung arrived; no further dispatches were made afterwards.
3. Log comparison, first separating step, file:line — done.
4. Evidence committed and verified on origin/main.
5. END post, host besenrein.

## Reality witnesses

`git remote -v` on the planning clone → origin URL = github.com/mcpdev80/baseharbor-plan (verified before first evidence commit; NOT the quarantined `workers/baseharbor-plan` directory). Token redacted here per secret rules.
- Product refs read only via `gh api` / `gh run view --log` and a fresh clone in `/tmp/opencode/docker-gate-probe-wt` (never from the quarantined `workers/baseharbor` checkout).
- `git merge-base --is-ancestor 84ee9a93e deeeb6477` → NO (candidate is an open-PR head, not on develop).

## Runs (the four of the A/B matrix)

| run id | event | ref / sha | job that ran | conclusion | first separating evidence |
| --- | --- | --- | --- | --- | --- |
| 44461341870 (#654) | push | develop `deeeb6477` | green via job "Native single-default · Docker"; job "docker-runtime" was **skipped** | SUCCESS | step "Install verified ORAS for native Core bootstrap" = success (log observed); zero `ORAS is required` lines in the whole run log (grep count 0) |
| 44467228776 (#660) | push | develop | same shape as #654 (coordinator stand-meinung, accepted as witness) | SUCCESS | — |
| 44466684726 (#658) | workflow_dispatch | ref `develop` → `deeeb6477` | job "docker-runtime" executes (its `if:` at line 175 is true for non-push) | FAILURE | checkout step fails 3× (`The process '/usr/bin/git' failed with exit code 1`) because the dispatch default `inputs.ref: release/v0.4.21` (line 19) overrides the REST-API `ref`; remaining steps skipped |
| 44463592314 (#656) | workflow_dispatch | `4e032c858` | "docker-runtime" executes | FAILURE | "Run runtime integration tests serially": `prepare BaseHarbor integration trust plane: ORAS is required before Core setup` |
| 44464060182 (#657) | workflow_dispatch | `84ee9a93e` | "docker-runtime" executes | FAILURE | same ORAS line, `app_repository_integration_test.go:27`, `app_workload_integration_test.go:60`, `:191` |
| 44466748992 (#659) | workflow_dispatch | ref `lane-0428-119-consent-hard` → `84ee9a93e` | "docker-runtime" executes | FAILURE | same shape as #657 (this lane dispatched it to complete the B-side; stand-meinung confirms) |

Note on #658: it is the develop-head dispatch but used the workflow's default `inputs.ref` (`release/v0.4.21`), so it failed *earlier* (checkout) than the ORAS bootstrap gap. The path-level conclusion is nevertheless the same — dispatch route never green. The clean comparison is #654/#660 (push, green) vs #657/#659 (dispatch on a real ref, red at the same step regardless of candidate).

## First separating step (file:line, `.github/workflows/docker-runtime-acceptance.yml` at develop `deeeb6477`)

- Line 174-175, job `docker-runtime` with `if:` that is TRUE only for non-push or non-develop pushes → the dispatch route runs **this** job.
- Its steps span lines 186-330. There is **no** ORAS bootstrap step anywhere in this job (verified by `awk`-scan of lines 174-380 for `oras|ORAS`: no match).
- Lines 127-128: `- name: Install verified ORAS for native Core bootstrap` / `run: bash scripts/ci-install-oras.sh` — this step exists **only** in the push-route job `Native single-default · Docker` (job guard at line 108: `if: github.event_name == 'push' && github.ref_name == 'develop' …`).
- The push route never runs `docker-runtime` at all on develop pushes (line 175 `if:` → skipped, observed in run #654), so the ORAS-missing bootstrap is invisible there.
- The test-side bail-out: `cmd/baha/oras_setup.go:43` raises `ORAS is required before Core setup; install it manually or rerun 'baha up' in an interactive terminal…` when `oras` is not on PATH and stdin is not a terminal (non-interactive CI, `oras_setup.go:35-44`); reached via `ensureRuntimeIntegrationTrustPlane` → `cmd/baha/runtime_integration_test_support_test.go:840` `t.Fatalf("prepare BaseHarbor integration trust plane: %v", …)`.
- `inputs.ref` propagation: only consumed at line 190 (`ref: ${{ inputs.ref || github.sha }}`); it is not forwarded anywhere else, and `github.sha` in a dispatch run is the workflow-file commit, not the requested ref — a secondary wiring observation (dispatch runs of `docker-runtime` that DO pass checkout test whatever `inputs.ref` resolved to, while the workflow definition itself always comes from the dispatch ref).

## The one reason (why push is green and dispatch is red)

Not environment flakiness and not the candidate: the **bootstrap of the trust-plane dependency is path-dependent in the workflow definition itself**. The ORAS install (`scripts/ci-install-oras.sh`, added to develop in ff9e8b2d, 2026-11-13) was wired ONLY into the push-gated job "Native single-default · Docker" (lines 127-128). The job that the dispatch route actually executes, `docker-runtime`, has no ORAS install step, so on the fresh GitHub-hosted runner `oras` is absent, the integration-trust-plane helper hits the non-interactive bail-out at `cmd/baha/oras_setup.go:43`, and every `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` test fails identically. On develop pushes the `docker-runtime` job is skipped entirely (line 175), which is why the asymmetry looks "green push / red dispatch".

## Candidate blame assessment

The candidate is NOT at fault: the identical ORAS failure occurs on dispatch runs of both `4e032c858` (#656) and `84ee9a93e` (#657/#659), and the defect line (missing install step in `docker-runtime`) is present verbatim on the develop head itself (lines 174-330 contain no ORAS step). Counter-proof pending on the *checkout-passing* develop-head dispatch is already covered by #656/#657 being two different candidates with byte-identical failure mode.

## Fix direction (Owner scope, finding only — no edit made)

Add to the `docker-runtime` job in `.github/workflows/docker-runtime-acceptance.yml`, after "Prepare isolated hosted rootless Docker" (line 219), the same step from lines 127-128 (`Install verified ORAS for native Core bootstrap` / `bash scripts/ci-install-oras.sh`). Consider also making `workflow_dispatch` `inputs.ref` actually honored (line 19 vs line 127 default `release/v0.4.21`) so develop/candidate dispatches stop failing at checkout.

## Own commits witness (no foreign candidate)

Evidence commit on origin/main (final amend chain): parent `fef982b6`, this file present in that commit's tree (witness: `git ls-tree origin/main evidence/r28-welle4-2026-11-19/docker-gate-wiring/` → `probe-1.md`; `git log --oneline origin/main~1..origin/main` → exactly one entry, no foreign commits). The SHA self-reference is omitted on purpose because amending to embed it changes it. Base attestation: branch point = origin/main head `fef982b6` at first commit, ancestor of the pushed evidence commit.

## Cleanliness

- Host used for mission bookkeeping only: `baha-docker`. This lane started ZERO containers, compose projects, or daemons on it (start and end lists are equal; only ambient pre-existing stacks and foreign `bh-w169-*`/`bh-gfield0427-*` images remain, untouched per owner directive).
- Before-list (baha-docker, 2026-11-19T05:39:15Z): `ps` = pre-existing `baha-dev login -e stage` (10 days), dockerd, docker-proxies, openbao (all 10 days, foreign); `docker ps -a` = empty; images = pre-existing ambient set (listed in transcript).
- After-list: identical — this lane ran no docker commands on the host at all (diagnosis was 100% from CI logs and git objects).
- Scratch zone: `/tmp/opencode/docker-gate-probe-wt` (git clones only, no containers).
- Host after-list (baha-docker, 2026-11-19T05:53:50Z): `docker ps -a | wc -l` = 0, `docker ps -q | wc -l` = 0 — identical to the before-list; ps shows only the pre-existing foreign daemons/stacks.
- END witness: evidence on origin/main = `git rev-parse origin/main` output in this lane's transcript immediately before the END post; the file's own commit SHA cannot be inlined because each embedded-SHA amend replaces it.
- cleanliness: ok

Evidence commit on origin/main (single candidate commit for this task; its parent is the fetched origin/main head `fef982b6` — base attestation and proof that no foreign commit is carried). `git log --oneline origin/main~1..origin/main` = exactly one entry, message "evidence(docker-gate-probe): final witness, closes probe-1". The commit SHA is deliberately not stated in-file: any amend that embeds it changes it (several transient SHAs during the amend-chain; see this lane's transcript); the authoritative witness is `git rev-parse origin/main` taken at END, which must equal the SHA posted in the END line.

END_DONE mission-docker-gate-probe.md — diagnosis complete, no product change, no PR, no .github edit. Evidence lives on origin/main; final SHA witness lives in the END post and this lane's transcript (in-file self-SHA is impossible under amend; see witness section).
