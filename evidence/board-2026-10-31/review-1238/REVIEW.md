# REVIEW — PR #1238 (baseharbor): Self-Hosted/Rootless → GitHub-Hosted workflow migration

**Task:** review-1238
**Role:** REVIEW (read-only, no edit/merge/approve)
**Candidate SHA (head):** 33d1e49
**CI witness (run 41247466095):** runs RED only in PR-Selected-Checks coverage gate — unrelated to the three migrated workflows
**Session/Model/Zeit:** session 8c0f41e1 · agentgateway/worker-ornith1.5 · 2026-11-01
**Repo:** mcpdev80/baseharbor · base `develop` (cb6b738) · head `work/gh-acc-suite` (33d1e49)

---

## Overall Verdict

**{APPROVE-WARTEND-GREEN}** — The three acceptance workflows are correctly migrated from self-hosted to
GitHub-hosted (`runs-on: ubuntu-latest`). Per-file: **self-hosted = 0**, no rootless assumption baked
into the files, no gate weakened.
**Overlap with #1244: DISJUNCT / NEIN** — #1238's write-set is disjoint from #1244 (and #1239).
**ROLLE:REVIEW** · Modell: agentgateway/worker-ornith1.5 · Zeit: 2026-11-01.

---

## Per-file findings

### .github/workflows/mcp-lifecycle-acceptance.yml  (2 jobs: docker, podman)
- **self-hosted = 0**: both jobs' `runs-on: [self-hosted, Linux, X64, baseharbor, <runtime>]` → `ubuntu-latest`.
- **keine Rootless-Annahme in der Datei**: no `loginctl`, no `userns`/`apparmor`, no `dockerd-rootless`
  in the file. Runtime setup is delegated to the unchanged `scripts/ci-core-rootless-runtime.sh`
  (the proven interface; target reality per nc PR #17 + #1244 rootful script).
- **kein Gate abgeschwaecht**: original per-job `if:` guard retained; `timeout-minutes` unchanged;
  no test/assertion removed.

### .github/workflows/observability-acceptance.yml  (2 jobs: docker, podman)
- **self-hosted = 0**: both jobs → `runs-on: ubuntu-latest`.
- **keine Rootless-Annahme in der Datei**: same as above, no rootless assumption baked into the file.
- **kein Gate abgeschwaecht**: `if:` guards retained; timeouts unchanged (15 / 20); no deletion.

### .github/workflows/podman-acceptance.yml  (1 job: podman)
- **self-hosted = 0**: `runs-on: [self-hosted, Linux, X64, baseharbor, podman]` → `ubuntu-latest`.
- **keine Rootless-Annahme in der Datei**: no rootless assumption baked into the file; runtime setup
  delegated to the unchanged `ci-core-rootless-runtime.sh` (step id `setup_podman`).
- **kein Gate abgeschwaecht**: `if:` guard retained; `timeout-minutes` 75 unchanged.

---

## Overlap #1244 (and #1239) — DISJUNCT

- **#1238 write-set (head):** only the 3 workflow YAMLs above. Does NOT touch `ci-core-rootless-runtime.sh`.
- **#1244 (`work/podman-gh`):** `.github/workflows/ci.yml` (+1/-1, podman job line 244) + new
  `scripts/ci-podman-gh-runtime.sh` (+51, rootful podman on ubuntu-26.04).
- **#1239 (`work/gh-ci-core`):** `.github/workflows/ci.yml` (+16/-2, validate job) +
  `nextjs-greenfield-e2e.yml` + `ci-core-rootless-runtime.sh` (+37/-28) + test.
- **Befund:** #1238 touches NO file in #1244 or #1239 → **no merge-conflict risk for #1238.**
  (#1239 and #1244 overlap only on `ci.yml`, at disjoint hunks — their own matter, not #1238's.)

---

## Witness / CI status

- CI run **41247466095**, head **33d1e49**: PASS (Focused Python, Trusted Plan, Validation·ci-actionlint,
  Validation·ci-executor-verifier-tests, Validation·ci-policy, Validation·pr-planner-tests,
  Validation·receipt-execution-tests, Workflow policy); **RED only in the runtime-selection gate
  "PR Selected Checks"** (job 124674284505).
- This FAIL is in the runtime-lane selection gate and is **unrelated** to the three migrated workflow
  files — not a migration defect. Flagged for lane owner; not a CHANGES trigger on #1238.
- SKIPPING (expected pre-merge, no changed files trigger them): Consumer Pins, Demo Pin, Exact Candidate,
  Public Contracts, Runner Interface, Selected Runtime, Release Source Preflight, Targeted HA·docker/·podman, validate.

---

## END
END_DONE review-1238: datei-geschrieben
