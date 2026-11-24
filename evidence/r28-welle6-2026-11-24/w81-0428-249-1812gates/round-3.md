# w81-0428-249-1812gates — round 3: run 45398943139 diagnosis (matrix claim + consent failures)

Candidate unchanged: PR #1812 head `47590207518ce9501f1b1bbb115d72d64a206d14`, base develop `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` (verified this turn via `git ls-remote lane-origin refs/heads/develop refs/pull/1812/head` → develop 46d3dccc1, PR head and branch head both 475902075). No new commits were pushed this round (see "Why no code fix" below).

## PLAN

1. Reality check: fetch develop + PR refs, confirm head unchanged — done.
2. Diagnose the claimed matrix-condition/output-propagation defect against run 45398943139 — done: CLAIM DISPROVED by the run's own job timeline (witnesses below); no workflow defect exists to fix.
3. Root-cause the 4 failing Docker light gates on the exact head — done: all end at the same `--confirm-candidate` refusal on the `baha up` path; evidence below.
4. Land any fix strictly inside #1812's existing diff scope — decision: none possible (see "Why no code fix"); STOP+REPORT per mission.
5. Round-3 evidence commit to baseharbor-plan origin/main + post to coordinator — done below.

## 1. The "matrix job skipped despite execute_count=7" claim — disproved by run 45398943139 itself

Full job timeline of the run (attempt 1, completed/failure, started 13:00:05Z), read via `gh api repos/mcpdev80/baseharbor/actions/runs/45398943139/jobs`:

- 13:07:38Z — one job named `Light · ${{ matrix.runtime }} · ${{ matrix.gate }}` (job id 138466521125) → skipped, 0 steps. That is `runtime_light_gates_podman` (pre-release.yml:743): its matrix `needs.source.outputs.light_podman` was empty because the owner dispatched `only_gates=atomic/docker/...` only. Correct fail-closed behavior for a dispatch that excluded Podman — exactly the pattern every other excluded family shows in the same run (`Heavy · …` ×2, `HA · …` ×2, all `Integration · …`, `Static · …` matrix jobs skipped at the same instant).
- 13:07:40Z–13:15:34Z — SEVEN expanded jobs `Light · docker · <gate> / Executed docker · <gate>` (ids 138466518597/674/714/757/846/935/939) RAN on GitHub-hosted runners. The `runtime_light_gates_docker` matrix (pre-release.yml:714) DID populate and execute: `fromJSON(needs.source.outputs.light_docker)` expanded to 7 rows, as `light_docker_execute_count=7` predicted.
- 13:15:36Z — `runtime light gates · All runtime results` → success; 13:15:42Z `Pre-Release Checks` → failure (because 4 of the 7 executed gates failed — a test failure, not a routing failure).

Therefore the premise "GitHub shows the Docker matrix job SKIPPED while outputs were emitted" is wrong: the skipped template-titled job is the Podman family; the Docker family executed and its outcomes are the 7 real gate verdicts. The output-propagation path is intact: `steps.runtime_reuse.outputs.light_docker` → declared in the `source_prepare` job outputs (pre-release.yml:24) → re-exported by `source` (pre-release.yml:540). No unset/empty-output zero-expansion defect exists on this head.

## 2. Per-gate outcomes on exact head 475902075 (owner-dispatched run 45398943139, monitored to terminal)

Operator-auth admission is FIXED — verified per gate: `baha v0.4.27 (commit 47590207518ce9501f1b1bbb115d72d64a206d14, built unknown)` version matches and the trace lines now read `[ci-operator-testonly] decision=managed-local-gate ...` (the tag binary is in use). No gate fails at the operator step anymore.

| Gate | Verdict | Evidence (job log) |
| --- | --- | --- |
| guided | PASS | RESULT PASS; "Guided Fail-Closed Consent + New/Edit PASS"; demo HEAD f23b6e09 checkout |
| lifecycle | PASS | RESULT PASS (note: consent refusal text appears inside; its scripted expectations still met — PASS-mechanics observation below) |
| failure | PASS | "PASS Secret Leak Checks", "PASS Unsupported -> Blocked", RESULT PASS |
| policy | FAIL | 13:11:50Z `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state` → `demo-policy FAIL / RESULT FAIL`; plus `Error: operator authentication needs interactive setup but input is not a terminal` |
| connectivity | FAIL | same consent refusal → `demo-connectivity FAIL / RESULT FAIL` |
| reconciliation | FAIL | same consent refusal → `demo-reconciliation FAIL / RESULT FAIL` |
| full-destroy | FAIL | same consent refusal (then destroy proceeded; `owned runtime evidence unavailable: ValueError (phase=owner-preview)`) → `demo-full-destroy FAIL / RESULT FAIL` |

## 3. Root cause of the 4 consent failures — product defect in `baha up`, NOT #1812's diff

- The candidate binary enforces two-stage consent since the v0.4.27 line: `cmd/baha/app_apply.go:43` documents "the apply prints the candidate's canonical content hash and requires --confirm-candidate with that exact hash before writing any deployment state; without the flag the apply fails closed" (introduced ecbb88545 #1355, refined e7f830873 #1486 "up non-TTY: two-stage consent honours --yes").
- Every failing gate dies inside the demo harness's `baha up` step: log shows `next: run 'baha up'` → `Re-run with --confirm-candidate a36c321d0580… to acknowledge this exact submission.` → the refusing-to-record error. The consent digest is never propagated through `baha up`.
- Known fix exists but is NOT on develop: branch `fix/up-confirm-candidate-propagation`, commit `5f9c67102` "fix: preserve candidate consent in root up", opened as PR **#1647 — CLOSED, never merged** (verified this turn: `git merge-base --is-ancestor origin/fix/up-confirm-candidate-propagation lane-origin/develop` → NOT in develop; `gh pr list --head fix/up-confirm-candidate-propagation --state all` → #1647 CLOSED). The branch tip `5f9c671` sits on the OLD base (parent `fae335a3e` #1642, before the v0.4.27 release merge `6c40fab4d`).
- 0428-226 (consent-planid) is on develop (`2b9a2c6d1` #1824 lineage) but did not cover the root `up` path.

## Why no code fix (mission rule: fix outside #1812's diff scope → STOP + report)

#1812's authorized write-set is the owner's +20 reload delta in `.github/workflows/pre-release-runtime-suite.yml` (unchanged; `git diff --name-only lane-origin/develop HEAD` still returns exactly that one file). The needed changes are (a) product Go code (`cmd/baha` up-path consent propagation, e.g. revive/rebase #1647's `5f9c67102` onto current develop) or (b) the demo repo's `scripts/acceptance.sh` harness. Editing ci.yml/pre-release.yml to add matrix outputs was ruled out because (i) no defect exists there and (ii) those files are outside this card's write-set. No new commit was pushed; candidate head remains 475902075 (ls-remote witness in section 1).

## repo-rule compliance

- Hosted-only: all diagnosis read-only via `gh api` job logs of run 45398943139; no local product test executed (no `go test`, no docker/podman on this host).
- No .github/** edits, no workflow_dispatch, no rerun triggered by this lane; no ci.yml change; no catalog rows; mcp.go untouched; #1819/#1820 not started; no subagents (§4.8); no merge.
- Remote truth only via `git ls-remote`/`gh api` against https://github.com/mcpdev80/baseharbor.git (remote resolved via `git remote -v`: all refs of my worktree point at the GitHub URL).

## cleanliness

- No container/network/volume/state created by this lane (hosted CI only). Nothing to bring down; no compose project owned by this lane.
- Side effect on remotes this round: none (no push; branch/PR head unchanged, re-verified 475902075).

## Handoff

Decision needed from coordinator/owner: commission the `baha up` consent-propagation fix as its own card (candidate recipe: rebase `5f9c67102` from PR #1647 onto develop 46d3dccc, add a regression test wired into the CI group covering `cmd/baha` up-path), OR route demo-repo owners to make the light-gate harness pass `--confirm-candidate` after the apply. Until then, re-dispatching Pre-Release on the current head reproduces exactly 3 PASS + 4 FAIL. Podman family per prior instruction stays parked until Docker is terminal-green, which cannot happen without that fix.

END_BLOCKED w81-0428-249-1812gates: run 45398943139 terminal on head 475902075 — matrix claim disproved (7 Docker light gates EXECUTED; skipped template job is Podman/only_gates-restricted); 3 PASS / 4 FAIL; operator-auth FIXED (binary 475902075 admitted); all 4 FAILs = unmerged `baha up` --confirm-candidate propagation (PR #1647 CLOSED, fix 5f9c67102 not on develop) — outside #1812 write-set, STOP + report per mission rule 2.
