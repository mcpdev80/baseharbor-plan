# w078 / PR #1650 — Ingress PR: two baseharbor pr-gate-coverage rows for the perses identity-witness paths

- Lane: `w078-pr1650-0428-078-reloc` (sweep #1650, first free seat)
- Missions: `/tmp/opencode/m_043_1650in.md.g` (this ingress PR), `/tmp/opencode/m_1650.md.g` (the relocated-content PR #1650)
- Purpose: PR #1650's relocated product/test files that live under two paths not previously catalogued must get a resolved `pr-gate-coverage.json` owner so the CI `pr-gate-plan` sees them as base-admissible. Exactly two additive `components-rows` are added; no product content, no `.github`, no runner work, no merge.

## Base attestation

- `origin/develop` head (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`): `7880a8f6bcfaabd8fd254ef987522abc1770c52e`
- Remote guard: in the worktree the real GitHub remote is `lane-origin` (and `origin` too, same URL `https://github.com/mcpdev80/baseharbor.git`); never push through an unresolved remote name.
- PR #1650 head (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1650/head`): `d3100a1faa304abf71aa52f8bb187a9889b038bf`

## PLAN (numbered)

- Step 1: Read both missions and establish base SHA (develop 7880a8f6) + remote guard.
- Step 2: Read the coverage resolver (`scripts/validate-pr-gate-coverage.py`) and `scripts/pr-gate-plan.py` to learn how a changed path resolves to a runtime gate owner; confirm `data.capabilities` surfaces have release gate owners and `runtime_specific: true` retains both engine siblings.
- Step 3: Confirm both target paths exist on develop and are absent from the components catalog (`cmd/baha/app_status_result_test.go`, `internal/metrics/realization.go`).
- Step 4: Create a fresh ingress branch from `origin/develop` (tip 7880a8f6).
- Step 5: Add exactly two additive `data.capabilities` components-rows (dup 0), release field v0.4.27 unchanged.
- Step 6: Validate the catalog (`validate-pr-gate-coverage.py`) and `pr-gate-plan.py` on the two-path diff; `go build`/`go vet` pass; gofmt clean.
- Step 7: Open the ingress PR (ready, not draft); `git ls-remote refs/pull/<n>/head` witness; no merge.
- Step 8: Run the exact hosted CI (trusted-plan + PR selected checks) to terminal success; record run-id + gate results.
- Step 9: Write this evidence akte; post `9142ab1f`; bring down any compose projects.
- Step 10: Second END — #1650 product final hop onto the tip after ingress-merge (per mission), then exact run.

## Coverage resolver findings (why two rows, why these surfaces)

- `resolve_covered_gates` maps a changed path to its owning component by exact `path` match, then to gates by `surfaces`. A changed path with no declared component owner is returned unresolved (fail-closed).
- `internal/metrics/realization.go` and `cmd/baha/app_status_result_test.go` are NOT in the components catalog today, so a PR touching them alone would fall to the conservative unresolved classifier. The ingress rows give each path a resolved owner.
- Both rows surface `source.gate.atomic.docker.data.capabilities` + `source.gate.atomic.podman.data.capabilities` with `runtime_specific: true`. These two surfaces already have release gate owners in `release-requirements.json` and `gates[]` (many existing components use them, e.g. `cmd/baha/app_access_test.go`, `cmd/baha/app_workload_ports.go`, `cmd/baha/target.go`), so the validator's "surface has no release gate owner" check passes.
- `runtime_specific: true` keeps both Docker and Podman gate siblings selected (the resolver drops the Podman gate only when the shared Docker sibling exists and `runtime_specific` is not true). This mirrors the existing data-capabilities rows.
- release field stays `"v0.4.27"` (verified: the `release` key appears exactly once, at the top level, unchanged).

## The two additive rows (pattern-matched to the app_status-family + data-capabilities rows)

Row A — test sibling of the catalogued `cmd/baha/app_status_result.go`:

```json
{
  "id": "source.cmd.baha.app.status.result.test.go",
  "path": "cmd/baha/app_status_result_test.go",
  "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"],
  "runtime_specific": true
}
```

Row B — the metrics product file that carries the folded identity-witness:

```json
{
  "id": "source.internal.metrics.realization.go",
  "path": "internal/metrics/realization.go",
  "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"],
  "runtime_specific": true
}
```

## repo-rule compliance

- No product content touched. No `.github/**` file created or edited (Owner scope). No runner/CI-machine work. No merge.
- Only `scripts/pr-gate-coverage.json` is written, by exactly two additive component objects. `schema`, `release`, `surfaces`, `packages`, `gates`, `native_checks`, and every other existing row stay byte-identical to develop.
- No subagents spawned. All steps run inside this session.
- Evidence lives only under `baseharbor-plan/evidence/...`, never in the product repo.

## CLEANLINESS

- docker ps -a before/after with own pid: to be recorded at END.
- No compose project started this lane; none to bring down.
- Worktree `/tmp/opencode/w078-pr1650-reloc-wt` is a scratch zone under /tmp/opencode (fixed workspace rule).
