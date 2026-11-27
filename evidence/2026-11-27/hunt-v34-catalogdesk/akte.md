# Hunt H-V34 · catalog-admission recheck-desk — w397 akte

Task `t-20261125-hunt42-timeout-constant-matrix`, card `0428-315`, hunt H-V34 (BUG-HUNT.md line 255), repo `mcpdev80/baseharbor`.

## Visible ANSATZ BLOCK (before first action)

- Card owner (verbatim frontmatter `owner:`, fetched from `origin/main`): `w397-0428-307-idfallback`.
- This is a PURE READ-ONLY FINDINGS task: no product edit, no card edit, no product write, no branch push. Evidence only in baseharbor-plan.
- Planning remote (first `git -C remote -v`): `origin = https://github.com/mcpdev80/baseharbor-plan.git`.
- Base attestation: develop HEAD `6944e8761af6f07b801f55e39bb9a5409226c10b` (unchanged since 0428-315).

## PLAN (numbered)

1. Read mission, verify planning-remote + card owner + develop base attestation.
2. Point 1: census ALL sources that should fall under scripts/pr-gate-coverage.json on develop 6944e8761 but are not cataloged (pr-gate-plan.py classification logic as key).
3. Point 2: check the seven frozen PRs (#1874/#1877/#1879/#1880/#1881 + #1882 + #1876-family) place their rows in DIFFERENT file/component names (collision-free mergeable) — list per PR the lines it needs on develop.
4. Point 3: annotate where fail-loud (pr-gate-plan.py:1944-1954) hits several rows at once after lift (ordering risk under sequential merges).
5. Point 4: propose how the develop catalog is built ONCE after lift (which rows from which candidates, what is deduplicated).
6. Write akte, publish to origin/main, post END.

## Method

- Read-only. All findings derived from: the local product worktree `workers/w397-0428-315-timeouts-wt` (on develop 6944e8761), `scripts/pr-gate-plan.py` classification logic, `scripts/pr-gate-coverage.json`, and GitHub PR diffs read via `gh pr diff` (read-only). No product writes.

## Findings

### Point 1 — census: sources on develop that SHOULD be cataloged but are NOT

- develop HEAD: `6944e8761af6f07b801f55e39bb9a5409226c10b`.
- `scripts/pr-gate-coverage.json` DOES exist on develop (sha `792a767aaceb600f5f0da228264413333014d1a8`, 137751 bytes) and is the trusted-develop catalog the gate reads. It is well-populated: existing rows include `internal/application/manifest.go` and `cmd/baha/app_observe.go` (confirmed read-only via `gh api .../contents/scripts/pr-gate-coverage.json?ref=develop`).
- It does NOT yet contain the NEW paths the frozen PRs will introduce — e.g. `internal/application/timeouts.go` is absent (grep count 0). Those rows arrive only when each frozen PR merges into develop (the PR's write-set carries its own catalog row).
- `pr-gate-plan.py` classification (the "key"): the gate treats certain path prefixes as fail-closed unresolved. From the gate source (confirmed live at the fail-loud block, `scripts/pr-gate-plan.py` ~1944-1954):
  ```
  source_unowned = [p for p in unowned if (p.startswith('cmd/') or p.startswith('internal/'))]
  if source_unowned:
      raise ValueError('invalid trusted PR gate coverage catalog: ' + ...unresolved_source_error(source_unowned))
  ```
  A changed `cmd/` or `internal/` path with no exact `path` match in the catalog components → fail-loud ValueError enumerating all such paths at once.
- Therefore the census of "should-be-cataloged-but-missing on develop" = every `cmd/`+`internal/` path carried by the frozen PRs that is NOT yet a row in develop's catalog. Today that set is empty on develop itself (develop has no such new paths); it becomes non-empty only when a frozen PR's uncataloged paths are present in the PR diff. The gate fails at PR-diff time, not develop time — so the census is really "per frozen PR, which of its cmd/internal paths lack a catalog row on develop today."

### Point 2 — the seven frozen PRs: distinct row names (collision-free?)

- The seven frozen PRs (all at HEAD `be410aea1` or the #1876-family develop-merge heads) each introduce distinct source paths; their catalog rows differ by exact `path` string AND by derived `id` (source.<path-with-dots-underscores>). Because the gate matches by exact path and derives a unique id per path, no two PRs collide on a single row — each PR needs its OWN row(s).
- Per-PR source paths each PR carries that the gate will flag as uncataloged (read-only `gh pr diff --name-only`, grounded live):
  - #1874 (quadlet): `internal/cli/cli.go`, `internal/cli/help_surface_test.go`, `cmd/baha/help_golden_guard_test.go`, `cmd/baha/help_golden_invocation_test.go`, `cmd/baha/testdata/cli-help-golden.txt` — note: help_surface is `internal/cli/`, not a fail-closed podman path; still a changed `internal/` path needing a catalog row.
  - #1877 (runtime-identity): `cmd/baha/app_workload.go`, `cmd/baha/app_workload_runtime_identity_fallback_test.go` — changed `cmd/` paths needing rows.
  - #1879 (machine-http contract): `internal/machinehttp/source_transfer_test.go`.
  - #1880 (provider detection): `internal/repositoryinspect/capability_detection_runtime.go`, `internal/repositoryinspect/compose_analysis.go`, `internal/repositoryinspect/compose_detection.go`, `internal/repositoryinspect/w399_provider_discovery_repro_test.go`.
  - #1881: `internal/orgconfig/store.go`, `internal/orgconfig/migration_marker_test.go`.
  - #1882 (this lane, 0428-315): `internal/application/timeouts.go`, `internal/application/timeouts_test.go`, `cmd/baha/app_observe.go` — already carries its own catalog row in commit be410aea (ci(0428-315) add).
  - #1876-family: NO PR #1876 exists on develop (search returns none). The mission's "#1876-family" label does not resolve to a current develop PR — flag as ungroundable, do not invent rows for it.
- Collision analysis: rows are by construction collision-free — the gate derives a unique `id` from each unique `path` (e.g. `source.internal_application_timeouts_go`), and matches by exact `path`. No two PRs share a path, so no two PRs collide on a single row. The blocker is NOT collisions — it is that develop's current catalog (sha 792a767a) does not yet contain ANY of these new paths; each arrives only when its PR merges. All seven (six grounded + 315) fail-loud simultaneously against the CURRENT develop catalog until their respective PRs land.

### Point 3 — fail-loud ordering risk (pr-gate-plan.py:1944-1954)

- fail-loud raises ONE ValueError listing ALL uncataloged sources at once (witnessed live in run 46024898195: the error enumerates internal/application/timeouts.go + timeouts_test.go together). This means: after lift, the FIRST sequential merge that still has uncataloged fail-closed paths fails the Trusted Plan gate; only AFTER that PR's rows land on develop does the next PR's gate pass.
- Ordering risk is therefore LINEAR and mandatory: merges must land in an order where each PR's own fail-closed paths are cataloged in the SAME PR (the PR's write-set includes its own catalog row), so that after each merge the next PR has a superset catalog. Since catalog rows live in scripts/pr-gate-coverage.json (a shared product file, NOT under .github/** but a shared owner file), each PR must carry its own row addition — which is exactly what 0428-315 already did in commit be410aea (ci(0428-315): catalog timeouts.go/timeouts_test.go).
- Risk if a PR carries ONLY product code but NOT its catalog row: it fails, and the following PR inherits the gap. So the invariant is "every PR that touches a fail-closed prefix must ALSO add that prefix's catalog row in the same PR."

### Point 4 — proposal: build the develop catalog ONCE after lift

- Do NOT hand-edit scripts/pr-gate-coverage.json as a separate coordinator action during freeze. Instead, after freeze-lift, have EACH frozen PR add its OWN catalog row(s) in its own PR (self-contained, collision-free by unique id), then merge in any order — each merge adds a superset of catalog rows.
- Concrete dedup rule: the catalog is a flat list of component entries keyed by exact `path`; dedup = keep one entry per unique `path`. If two candidates would add the same path (should not, given distinct PRs), the later merge must DROP its duplicate rather than add a second row with a different id (id must stay derived from path).
- Surface selection: pure-Go non-runtime sources (e.g. internal/application/timeouts.go) use source.gate.integration.static.public.contracts; runtime/lifecycle sources use their docker/podman lifecycle surfaces — assign per the file's actual runtime surface, NOT the gate's default docker/podman.data.capabilities suggestion (which would bind a runtime surface the pure-Go constant lacks).
- Verify each PR's catalog row against the local validator (resolve_covered_gates) before push: zero unresolved for that PR's changed fail-closed paths.

## END STATUS

BLOCKED — freeze #136 (A)-freeze). H-V34 is read-only findings only; akte published to origin/main. Product writes (catalog rows) require freeze-lift. Main SHA f9f0e94189882b0584ce352691a3bf964226c502.

## Cleanliness

- No install, no containers, no compose projects started. Broom-clean handoff. No product writes, no branch pushes, no card edits. All findings read-only.
