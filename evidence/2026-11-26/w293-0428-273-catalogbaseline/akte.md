# w293-0428-273-catalogbaseline — Akte

## Mission
Minimal trusted-catalog baseline for card 0428-273 (tasks/t-20261124-gate-catalog-baseline-1819.md; Codex w267 ruling 2026-11-26T04:45Z). First step of the owner's fixed sequence: trusted catalog baseline -> #1855 hop onto updated develop -> two distinct green pull_request runs. The trusted planner loads the catalog from the BASE ref (ci.yml:865-876), so #1855's candidate-side catalog edits could never be trusted; runs 45752959319 (78d05dc6b), 45755906112 (123666c82) and 45756612395 (572d64891) all failed 'PR · Trusted Plan' with 'invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner'. Two focused test sources need catalog rows so the gates that execute them are declared.

## Visible Ansatz Block (owner directive, attested in PROTOCOL history; date citation non-authoritative as date, fixed 2026-11-26)
- exact per-card frontmatter owner VERBATIM (fetched from origin/main at runtime): card 0428-273 has NO local task note; frontmatter owner sourced from the mission + w267 ruling (see below).
- git user.name / user.email: w293-0428-273-catalogbaseline / w293-0428-273-catalogbaseline@baseharbor.local
- literal git -c commit invocation: `git -c user.name=w293-0428-273-catalogbaseline -c user.email=w293-0428-273-catalogbaseline@baseharbor.local commit -m "..."`
- pre-push git show -s --format=%an gate line: `git -c user.name=w293-0428-273-catalogbaseline -c user.email=w293-0428-273-catalogbaseline@baseharbor.local log --format='%h an=%an cn=%cn' -1` => `b1333d6a4 an=w293-0428-273-catalogbaseline cn=w293-0428-273-catalogbaseline`

## Base Attestation
- real product remote: `https://github.com/mcpdev80/baseharbor.git` (verified via `git remote -v`; all remotes resolve to github.com/mcpdev80).
- develop head cut FROM: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` (via `git ls-remote origin refs/heads/develop`).
- ancestry: `git merge-base --is-ancestor origin/develop HEAD` => OK. `git log --oneline origin/develop..HEAD` => ONLY my commit b1333d6a4.
- Isolated candidate worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w293-0428-273-catalogbaseline-wt` (no foreign work entangled).

## Two Rows Added (exact)
Both modelled on existing neighbour row `source.internal_metrics_identity_dashboard_witness_go` (path `internal/metrics/identity_dashboard_witness.go`, surfaces docker+podman data.capabilities, `runtime_specific: true`); the plain data-capabilities neighbours `source.cmd_baha_app_status_collect_go` and `source.internal_metrics_perses_backend_status_test_go` carry only id/path/surfaces, so I dropped `runtime_specific` to match them.

Row 1:
{"id":"source.cmd_baha_app_identity_dashboard_status_test_go","path":"cmd/baha/app_identity_dashboard_status_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}

Row 2:
{"id":"source.internal_metrics_identity_dashboard_witness_test_go","path":"internal/metrics/identity_dashboard_witness_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}

## Surface Id Verification (verbatim existence in file)
- `source.gate.atomic.docker.data.capabilities` => PRESENT as an id in the file top-level `surfaces` array.
- `source.gate.atomic.podman.data.capabilities` => PRESENT as an id in the file top-level `surfaces` array.
- Both ids are the data-capabilities docker+podman source.gate.atomic ids named by w267; they match the ValueError recipe in evidence r28-welle6-2026-11-27/bughunt-hv51-config-env/w197-0428-224-intake.md line 37 and the neighbour row. No invented ids.

## Payload Guard (single file only)
`git diff origin/develop...HEAD --name-status` => only `scripts/pr-gate-coverage.json` (M). No product code, no test code, no `.github/**`, no `release-requirements.json`, no `scripts/pr-gate-plan.py`, no `scripts/pr-gate-map-v1.json`. JSON validated with `python3 -m json.tool` (format check only; no test execution — CI runs `scripts/test_pr_gate_coverage.py`).

## Commit Identity
- SHA: b1333d6a4c091aa2f5315dc118ea975a8ec7be19
- branch: w293-0428-273-catalogbaseline (cut from origin/develop head)
- author+committer: w293-0428-273-catalogbaseline @ baseharbor.local (full canonical name, never shortened, never 'coordinator', never card owner name)
- push delivery proof (git ls-remote): `b1333d6a4c091aa2f5315dc118ea975a8ec7be19  refs/heads/w293-0428-273-catalogbaseline`

## PR
- ONE PR, non-draft: #1857, base develop, title `fix(0428-273): catalog identity_dashboard sources for trusted planner gate`.
- head sha b1333d6a4c091aa2f5315dc118ea975a8ec7be19, baseRefName develop, isDraft=false, state=OPEN.
- Plan PR #96 (head 167683a33) is the Codex-side classification record (separate); this PRODUCT PR against develop is what unblocks #1855's hop.

## Run Census (Hosted CI — the only verification)
AWAITING. Eigenes-Run-Pflicht: watch my own run on PR #1857 to terminal. Report run ID + per_page=100 census including attempts with executed vs skipped; quote Trusted Plan log lines proving the 'uncataloged source change' ValueError is GONE for both files. Missing/skipped/queued is NOT a pass.

## END Status
END_DONE pending: head SHA + develop ancestry + payload guard + run ID with executed/skipped census + Trusted Plan log lines + plan PR number + zero local test execution + cleanliness line.
