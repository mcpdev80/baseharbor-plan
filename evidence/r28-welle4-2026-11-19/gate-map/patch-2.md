# gate-map patch draft v2 (karte 0428-134)

This is a **draft patch** for the Owner. It is NOT applied in any product repo — it stays a reviewable patch in `baseharbor-plan` (Owner scope), and applying it is the Owner's action.

- Mission: `gate-map-patch-draft` / correction round `gate-map-patch-correction` (karte 0428-134, Dachkarte 0428-114). Fundgrundlage: `evidence/r28-welle4-2026-11-19/ci-intake-audit/befund-1.md` (audit-commit 74fa2814) and the v1 draft `evidence/r28-welle4-2026-11-19/gate-map/patch-1.md`.
- v2 closes the two v1 gaps (CHANGE 1 now widens the `if`, CHANGE 2 now carries a real job hunk); CHANGE 3 + CHANGE 4 are unchanged from v1.
- Delivery: this file (reason + functional before/after per change) AND `gate-map-v2.patch` (git-apply-fähig).
- Base attestation: baseharbor develop head `907f16713cbf38693d30c9dadaad7fe299759219` (origin/develop); baseharbor-demo main head `adda7599cb5b79689702f6a63a5ca802179df967` (origin/main).

## CHANGE 1 — go-unit-on-PR (`.github/workflows/ci.yml:258`)

**Hole.** The full Go unit suite `go test ./...` runs only in the `validate` job at `.github/workflows/ci.yml:342`. That job's `if` at `ci.yml:259` is `github.event_name != 'pull_request' && ...`, so it never runs on a Pull Request. On PR, coverage is delegated to `pr_plan` selection; `pr_unit_shards` only runs when `needs.pr_plan.outputs.unit_scope != 'none'` (`ci.yml:1137`), and scope is `'full'` only when `go-unit-tests` is in the trusted `requested` set (`ci.yml:931`) or the sharding executor paths changed. `pr_focused` (`ci.yml:1091`) runs a fixed Python suite, not Go.

**Proposal (functional change).** Widen the `validate` `if` at `ci.yml:259` so it also matches `pull_request`. Existing runtime-validation source-prefix guards are preserved (only widened, never removed).

```
BEFORE (ci.yml:259):
  if: github.event_name != 'pull_request' && !startsWith(github.ref_name, 'runtime-validation/source-preflight/') && !startsWith(github.ref_name, 'runtime-validation/ha/')
AFTER:
  if: github.event_name == 'pull_request' || (github.event_name != 'pull_request' && !startsWith(github.ref_name, 'runtime-validation/source-preflight/') && !startsWith(github.ref_name, 'runtime-validation/ha/'))
```

Result: on PR, `go test ./...` now also runs in `unit_tests` (ci.yml:342). No new job, no new gate — reuses the existing unit routine and selection.

## CHANGE 2 — perses-smoke job (`.github/workflows/targeted-integration.yml`, after `focused`)

**Hole.** `TestPersesRuntimeSmokeDockerIsolated` (flag `BASEHARBOR_PERSES_RUNTIME_SMOKE`, guard at `internal/application/perses_runtime_test.go:372`) lives only on the perses candidate branch; the test and the file are absent from develop HEAD `internal/` (grep returns 0). No workflow references `BASEHARBOR_PERSES_RUNTIME_SMOKE` (grep `.github/` → 0). So the smoke test has no CI trigger.

**Proposal (real job hunk).** Add a `perses_runtime_smoke` workflow_dispatch job after the existing `focused` job. Home = `targeted-integration.yml` (not `docker-runtime-acceptance.yml`), because:
- The `focused` job already runs on the docker runtime path (rootless Docker + `ci-core-rootless-runtime.sh`), builds the control-plane image from `deploy/control-plane/Dockerfile`, installs ORAS (`scripts/ci-install-oras.sh`), and runs `go test ./cmd/baha -run '^Test...'`. This is exactly the runtime-docker path and `go test -run` body the perses smoke test needs (it calls `runtimeprovider.Resolve`, `runtime.ConfigProject`, `runtime.UpProject`), and the second workflow has no free `go test -run` slot without adding a new gate.

Functional change of the new job:
- Trigger: `if: github.event_name == 'workflow_dispatch' && inputs.gate == 'perses-runtime-smoke'` (dispatch-only gate; no concurrency group, no shared-state race).
- `BASEHARBOR_PERSES_RUNTIME_SMOKE: "1"` (sets the flag the test guards on; previously never set).
- Steps reuse the existing docker path: checkout `inputs.ref` → setup-go → rootless Docker → **`bash scripts/ci-install-oras.sh`** (the step the docker-runtime job at ci.yml:174-330 was missing) → build image → `go test ./internal/application -run '^TestPersesRuntimeSmokeDockerIsolated$' -count=1 -v -timeout 15m` → cleanup runner state.

No new concurrency group, no new gate id, no shared-state mutation.

## CHANGE 3 — demo pr-guided-consent branches (baseharbor-demo)

**Hole.** `baseharbor-demo/.github/workflows/pr-guided-consent.yml:5` declares `on.pull_request.branches: [main]`. A develop integration PR (base `develop`) never matches, so the guided-consent python regressions never fire on the normal develop PR.

```
BEFORE (.github/workflows/pr-guided-consent.yml:5):
    branches: [main]
AFTER:
    branches: [main, develop]
```

One-line change, no new workflow, no new trigger.

## CHANGE 4 — documentation-audit path for docs/internal/*.json (`scripts/pr-gate-plan.py:1189`)

**Hole.** `ci.yml:1186` runs `bash scripts/documentation-audit.sh` unconditionally when `VALIDATION == documentation-audit`. But `scripts/pr-gate-plan.py:1189` only emits `DOC_CHECKS` for `docs/*.md`, `docs/*.rst`, the mkdocs/root doc files, and `site/`. `docs/internal/*.json` matches none, so a PR that changes only such a file routes to no `documentation-audit` selection → the audit job does not run. This blocks 0428-131 / #1697.

**Proposal.** Extend the `documentation` area path selection so `docs/internal/*.json` also emits `DOC_CHECKS`.

```
BEFORE (scripts/pr-gate-plan.py:1191-1193):
        elif (path.startswith('docs/') and path.endswith(('.md', '.rst')) or
                path in ('README.md', 'CONTRIBUTING.md', 'CHANGELOG.md',
                         'mkdocs.yml', 'mkdocs.de.yml') or
                path.startswith('site/')):
AFTER:
        elif (path.startswith('docs/') and path.endswith(('.md', '.rst')) or
                path in ('README.md', 'CONTRIBUTING.md', 'CHANGELOG.md',
                         'mkdocs.yml', 'mkdocs.de.yml') or
                 path.startswith('docs/internal/')) or
                path.startswith('site/')):
```

Reuses the existing `documentation-audit` validation case; no new gate.

## repo-rule compliance

- Read-only audit artifact. No commit, push, merge, PR, workflow_dispatch, or new test in any product repo.
- No edit to `.github/**`, `scripts/**` (product), or product code — all changes are patch text only, in the evidence path.
- Isolated clones under `/var/tmp/gate-v2/` (outside the shared copy). No containers/compose started.
- No subagent (§4.8). Every step run in this session.

## cleanliness

- before: no containers, no compose projects, no /var/tmp state besides existing clones; no running services.
- after: /var/tmp/gate-v2/{core (develop-tracking clone), core-wt (patchable working tree at origin/develop 907f1671), demo (origin/main clone)} — read-only clones + one patchable working tree only. No containers, no compose, no running services.
- docker/podman ps witness: (none started)

## dry-run witnesses (git apply --check, rc=0)

1. `cd /var/tmp/gate-v2/core-wt && git checkout -- . && git apply --check /tmp/gate-v2-core.patch` against `907f1671` (CHANGE 1 ci.yml + CHANGE 2 targeted-integration.yml + CHANGE 4 pr-gate-plan.py) → **rc=0** (no output).
2. `cd /var/tmp/gate-v2/demo && git checkout -- . && git apply --check /tmp/gate-v2-demo.patch` against `adda7599` (CHANGE 3) → **rc=0** (no output).

## END

END_DONE mission-gatemap-patch-correction (karte 0428-134). Draft v2 written (patch-2.md + gate-map-v2.patch); CHANGE 1 now widens ci.yml:259 `if` to also run `go test ./...` on PR, CHANGE 2 now carries a real `perses_runtime_smoke` job hunk on the docker path (with the previously-missing ORAS-install step), CHANGE 3/4 unchanged; every hunk `git apply --check`-verified (rc=0) against current heads; no product write, no workflow/scripts edit, no PR, no merge, no subagent. Evidence on origin/main.

END_DONE
