# Fix 3 — 0428-083 state at a9befb312; integration work deferred until 088 merges (coordinator decision (b))

Mission: mission-083-runtime-provisioning.md (r3) + coordinator decision message (option b, two steps)
Card: t-20261114-r28-perses-datasources · PR #1684 · Branch: lane-0428-083-datasources-r2
Candidate head (stands unchanged): `a9befb3127b26a8a0f622bcf686fb6bcbb9b9e6e`
Date: 2026-11-19

## Decision honored (coordinator, authoritative)

Option (b): the coordinator brings 0428-088 into the window first (hopf + fresh exact-head run + new verdict + CODEX-MERGE). This lane therefore:

- left `a9befb312` EXACTLY as pushed: no new commits, no touches to `internal/application/perses_runtime.go`, no helper file simulating it. The round-3 scratch edits I had begun in the worktree before the directive arrived were discarded with `git checkout -- internal/metrics/perses_prometheus_datasource_runtime.go`; `git status --porcelain` (tracked) -> empty; HEAD == `a9befb3127b26a8a0f622bcf686fb6bcbb9b9e6e` (witnesses below).
- my self-run duty for `a9befb312` was already discharged before the directive: run `44522363321` observed to terminal `completed/success` via `gh run watch` in this session (exit 0).
- the follow-up work (apply-boundary call site, compose mounts from the materializer result, isolated Docker runtime test with a GlobalDatasource-load proof) is TRIGGERED by 088 landing on develop; then this lane rebases onto develop and delivers it. Committing `perses_runtime.go` here now would fork another card's candidate (§4.3/§3.1) — explicitly avoided.

## Dependency proof (measured, this session)

`git cat-file -e <rev>:internal/application/perses_runtime.go`:

- `origin/develop` -> `fatal: path 'internal/application/perses_runtime.go' does not exist in 'origin/develop'` exit 128
- `e1dc2cf61ebbd7ee4e0467a5d33e22345c2e6b88` -> fatal, exit 128
- `a9befb3127b26a8a0f622bcf686fb6bcbb9b9e6e` -> fatal, exit 128
- `f0adef107bf9d95ac2537a1e224783d3eed962d5` -> fatal, exit 128
- EXISTS on `76331c7d8` (`lane-0428-088-perses-runtime`) — the only branch carrying the file.
- `git ls-remote origin refs/heads/develop refs/heads/lane-0428-083-datasources-r2 refs/heads/lane-0428-088-perses-runtime` -> `e1dc2cf61...`, `a9befb312...`, `76331c7d8...` (live remote, 2026-11-19).
- PR #1592: state OPEN, draft=false, mergeable=MERGEABLE (gh api). Coordinator's parallel measurement (`merge-base --is-ancestor e1dc2cf61 <088-branch>` fails; merge-tree 0 conflicts) matches.

## Why run 44522363321 is NOT a qualification run (recorded per directive)

On `a9befb312`, jobs `PR · Selected Runtime` and `PR · Selected Core-less · ${{ matrix.runtime }}` were SKIPPED (gh run jobs evidence). The coordinator does not count the run as the runtime qualification — correct, because the runtime mount seam is absent until 088 lands. The unit gates that DID execute (14 successful jobs incl. `PR Selected Checks` and `PR · Go unit · packages`) qualify only the materializer layer.

## State of the candidate a9befb312 (unchanged, self-contained)

- `internal/metrics/perses_prometheus_datasource_runtime.go`: fail-closed materializer writing `providers/management-ui/perses/config.yaml` (file database + `provisioning.folders` + 300s interval) and `provisioning/globaldatasource-baseharbor-prometheus.json` (native `GlobalDatasource` / pinned `PrometheusDatasource` plugin / `HTTPProxy` access / materialized endpoint / pinned allowlist / no secrets), plus Target-bound build entry, ownership-safe removal and provider-path helper.
- Tests: runtime provisioning join test, fail-closed removal test, isolated runtime query/proxy/TLS test, endpoint negatives, 2 goldens. All in `internal/metrics`, executed by `PR · Go unit · packages` on every push (CI pickup: existing Go-unit group, trigger = PR push on non-draft; no `.github/**` change needed).
- Ancestor witnesses still hold at this head: `e1dc2cf61 -> a9befb312` YES, `f0adef107 -> a9befb312` YES, `ab6932296 ->` YES, `8c71395045 ->` YES. `git log --oneline origin/develop..a9befb312` lists only this chain's commits (a9befb312, f0adef107, a4a9efee9, ab6932296, 8c7139504).

## Follow-up matrix (to execute when 088 is on develop)

- call site: `internal/application/perses_runtime.go` apply boundary -> `MaterializePersesPrometheusDatasourceAt` before Perses start, mount paths taken FROM the materializer result (file:line at delivery)
- compose mounts: read-only `config.yaml:/etc/perses/config.yaml` + `provisioning:/etc/perses/provisioning` rendered from the returned paths (same dataDir convention as commit a9befb312's header comment)
- runtime test: isolated Docker cell starting pinned `docker.io/persesdev/perses:v0.55.1` with those mounts, GlobalDatasource LOADED (API/config view) + allowed query through Perses' real HTTPProxy + untrusted-TLS/denied-source fail-closed
- gate: the executing PR runtime cell (`PR · Selected Runtime` or the perses-group equivalent); if it stays skipped, finding with the skip-condition file:line in `.github/workflows/ci.yml` (Owner scope, not edited here)

## repo-rule compliance

- No `.github/**`/`scripts/**` edits; no reruns/dispatch; no merge (§GRENZEN); no PR comments on foreign PRs; no subagent (§4.8); no second lane/branch (§3.8); targeted `git add` only; worktree `/tmp/opencode/083-datasources-r2-wt`; quarantined `workers/baseharbor` never cited (all remote truth via ls-remote/gh api/fetch in my own worktree).

## Cleanliness

- Before/after `docker ps -a --format '{{.Names}}'` on this host: identical, 7 lines, all ambient `bh-local-shared-*` (other cards, untouched). This lane started NO container/volume/network anywhere this round.
- cleanliness: host besenrein; no orphan from this lane.

## END

END_DONE mission-083-runtime-provisioning.md: a9befb3127b26a8a0f622bcf686fb6bcbb9b9e6e stands unchanged (decision (b) step 1 honored, no perses_runtime.go touch, scratch reverted); dependency proof recorded; run 44522363321 terminal success but runtime cells skipped = not qualification; follow-up matrix ready for when 088 lands.
