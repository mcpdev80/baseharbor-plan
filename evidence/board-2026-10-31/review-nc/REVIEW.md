# REVIEW — node-connector PR #17 (review-nc)

- **VERDICT: APPROVE-FEIER-GRUEN**
- **ROLLE: REVIEW**
- **Session/Modell:** worker-ornith1.5 / agentgateway
- **Datum:** 2026-11-01
- **PR:** #17 `mcpdev80/baseharbor-node-connector`, branch `work/nc-gh-hosted`
- **Kandidat SHA:** `4aa41acccb58114e6aa3084474142f77f2b1b124` (verified via `gh api .../commits/4aa41acc`, message: "ci: report which podman mode works on GH-hosted runners (rootful vs cgroupfs)")
- **Base:** `main` · mergeable: MERGEABLE · reviewDecision: none · state: OPEN

## Method (read-only, gh)
- `gh pr diff 17 --repo mcpdev80/baseharbor-node-connector` → 2 changed files, 120 / 43 lines.
- `gh api …/actions/runs?head_sha=4aa41acc` → 2 completed runs, both `conclusion=success`, `event=workflow_dispatch`.
- Jobs: run 41262442519 / 41262420312 → job 124718273779 "Actual encrypted transport · podman" = success on runner **GitHub Actions 1000026912**; job 124718273931 "source" = success on GitHub Actions 1000026913; "Managed native enrollment" = skipped (matrix not selected on dispatch, expected).
- Repo-rule grep: `self-hosted` in `.github/workflows/` = **0 matches**. `continue-on-error` / `if: false` gate / SKIP / test deletion = **none**.

## 1. Rootless/loginctl pre-treatment — removed, replaced with rootful/cgroupfs (not a diagnostic echo)
Both `source.yml` (transport + enrollment jobs) and `release-integration.yml` (podman matrix job) replaced the old single rootless block (`sudo loginctl enable-linger`, `XDG_RUNTIME_DIR=/run/user/$uid`, `DBUS_SESSION_BUS_ADDRESS`, `systemctl --user show-environment`, `test … rootless = true`) with a guarded block:

```
set -euo pipefail
if ! command -v podman; then sudo apt-get update && sudo apt-get install -y podman; fi
if [[ "$RUNNER_ENVIRONMENT" == github-hosted ]]; then
  if podman run --rm --pull=always alpine:3.23 true; then echo ::notice:: rootful OK
  elif podman --cgroup-manager=cgroupfs run … alpine:3.23 true; then echo ::notice:: cgroupfs OK
  else echo ::error:: podman cannot execute containers; exit 1
  fi
  podman info --format '… cgroup_manager=… rootless=…'
else
  … loginctl / systemctl --user dance …
  test "$(podman info … rootless)" = true
fi
```

The rootless dance is **not** merely shadowed by an echo — on GH-hosted runners a real `podman run` executes alpine and the job **fails closed** (`exit 1` + `::error::`) when neither rootful nor cgroupfs works. The old rootless `test … = true` assertion is **retained verbatim** in the self-hosted `else` branch. No leftover GH-hosted path that would fail on GitHub-hosted runners. ✅

## 2. No weakened gate / SKIP / test deletion / self-hosted runs-on
- No `continue-on-error`, no `if: false` gate bypass (only `persist-credentials: false` / `cache: false` / `fail-fast: false` — all standard).
- No test removal; only the podman-prepare step changed.
- `runs-on` now only `ubuntu-latest` / `ubuntu-26.04`; **no `self-hosted` anywhere** (verified by repo-wide grep = 0).
- `workflow_dispatch` input `runtime` (choice podman/docker, default podman) drives the transport/enrollment matrix via `format('["{0}"]', inputs.runtime)`. ✅

## 3. Fail-closed + real (non-SKIP) success
- Three podman-prepare steps each end with `exit 1` + `::error::` on failure → job aborts visibly ≠ 0; no green certificate when Podman cannot run containers.
- The witnessed CI run "Actual encrypted transport · podman" = **success** on GitHub-hosted runners (Run 41262442519 / 41262420312, job 124718273779). This is the mission's positive real-evidence; verified as a real run, not SKIP. ✅

## 4. Disjoint write-set + nc-AGENTS
- Write-set restricted to 2 files in `baseharbor-node-connector` only — disjoint from all `baseharbor/*`. ✅
- nc-AGENTS.md honored: CI lives in this repo; no runtime matrix required for planning/instruction edits. Task note/evidence protocol referenced. ✅

## Boundary note (non-blockading, per §5.3)
No defect found; the change is faithful to the task intent (100 %-GitHub-hosted gates, rootless assumption removed). No correction round requested.

## Conclusion
Candidate matches contract: rootless/loginctl pre-treatment genuinely replaced by rootful/cgroupfs with fail-closed `exit 1`; no weakened gate/SKIP/test-deletion/`self-hosted` runs-on; real green CI witnessed; disjoint write-set; nc-AGENTS honored.

---
**lane DONE** — review-nc: #17=APPROVE-FEIER-GRUEN
