# Probe 0428-136 — docker-runtime missing `tests/main.jsonl` (dispatch run 44466684726)

Mission tag: `docker-checks-jsonl`. Read-only probe: no `.github`/`scripts` commit, no product PR, no merge, no
rerun/workflow_dispatch. Only host read via `gh api`/`gh run` logs and an isolated clone under `/var/tmp`.

## PLAN

1. Verify planning repo path + fetch remote truth, base attestation. — done
2. Create isolated clone/worktree under `/var/tmp` only. — done
3. Read job `docker-runtime` fully + verify-step; find which step writes `tests/main.jsonl`. — done
4. Compare with green `single_default_native`; counter-probe a real terminal SUCCESS run. — done
5. Pull failed job log 135366064519 (read-only), tie claims to file:line + run witness. — done
6. Decide root cause (dir vs path vs ORAS step). — done
7. Minimal owner patch sketch (ORAS step + JSONL path) — no new gate/cell/test-semantics change. — done
8. Impact on 0428-119/#1690 and 0428-114. — done
9. Write this dossier, END line — no markdown checkboxes. — done
10. `git ls-remote` witness + confirm evidence on origin/main, commit and push. — done
11. Host cleanliness before/after, END post to coordinator. — done

## Base attestation (planning repo)

Real planning repo (NOT the quarantined `workers/baseharbor-plan` directory):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

`origin/main` at start of this probe: `56eb6ac585f7c822d06f5062f0dde851847e1545`
(witness below; candidate evidence commit pushed on top: `03507b321ab6a54e868b8d164d46b70b784dcaca`).

## Isolated product clone

```
$ git clone --branch develop --single-branch https://github.com/mcpdev80/baseharbor.git /var/tmp/0428-136-probe
$ git -C /var/tmp/0428-136-probe rev-parse HEAD
da76c5cf9c963207038d5599bd130b89ecb1e8a4
```

Workflow file under analysis: `.github/workflows/docker-runtime-acceptance.yml` (658 lines), read in this clone.
All file:line references below are this file on develop `da76c5cf`.

## (1) Which step writes `_temp/docker-runtime-checks/tests/main.jsonl`

- The file is written by the step **`Run runtime integration tests serially`**, id `runtime_integration`,
  **line 322-328**. Line 328: `go test ... -json 2>&1 | tee "$RUNNER_TEMP/docker-runtime-checks/tests/main.jsonl"`.
  The other three JSONL files (`recovery.jsonl` line 351, `logs.jsonl` line 359, `traces.jsonl` line 367) are
  written the same way by the `recovery`/`log_ingestion`/`trace_ingestion` steps.
- Path prefix / environment variable: `RUNNER_TEMP`. The `out` shell variable at **line 204**
  (`out="$RUNNER_TEMP/docker-runtime-checks"`) and the literal path at line 328 both expand `RUNNER_TEMP`. The
  `tests` subdirectory is created **once**, at **line 205** `mkdir -p "$out/tests"` inside step
  `Record exact source and toolchain` (id `source_identity`, line 199). The verify-step reads it back at
  **line 385** `root = Path(os.environ['RUNNER_TEMP']) / 'docker-runtime-checks/tests'` and opens each
  `<name>.jsonl` at **line 400** `...read_text()`.
- Same proof mechanism in a job that runs: `single_default_native` (job line 105) writes and reads
  `$RUNNER_TEMP/single-default.jsonl` at **line 134 / 137** and `$RUNNER_TEMP/pinned-workload.jsonl` at
  **line 157 / 158**. It tees directly into `$RUNNER_TEMP` (flat, no subdirectory) and verifies the file in the
  SAME shell block, so a green `single_default_native` run always shows the JSONL produced before it is asserted.
  Crucially, `single_default_native` has the **`Install verified ORAS for native Core bootstrap`** step at
  **line 127-128**; the `docker-runtime` job has **no** ORAS step (grep for `ci-install-oras` across
  `docker-runtime-acceptance.yml` returns exactly one hit: line 128, in `single_default_native`).

## (2) Why `docker-runtime` did not produce the file in run 44466684726

It is NOT that the output directory is missing, and NOT (in this run) that the tests were aborted by ORAS. The job
never reached any test-writing step. The job-level step outcomes for `docker-runtime`, job 135366064519
(`gh api .../actions/jobs/135366064519`), are:

- `Checkout requested ref` — **failure** (step 2, 05:39:46→05:40:12, `The process '/usr/bin/git' failed with exit code 1`, log line at 05:40:12.7464878Z).
- `Set up Go` … `Cleanup Docker runtime` (steps 3-17) — **skipped**, because the non-optional checkout step failed.
- `Record exact source and toolchain` — skipped → so the `mkdir -p "$out/tests"` at line 205 never ran.
- `Run runtime integration tests serially` — skipped → so `tee` (line 328) never created `main.jsonl`.
- `Verify all eight executed runtime tests` — has **`if: always()`** (line 378), so it RAN despite the abort and hit
  `FileNotFoundError: [Errno 2] No such file or directory: '/home/runner/work/_temp/docker-runtime-checks/tests/main.jsonl'`
  at log line 05:40:12.8761787Z (`<stdin>`, the line-400 `read_text`).

Root cause of the abort: the checkout input. The job checks out **`ref: ${{ inputs.ref || github.sha }}`**
(line 190). For a `workflow_dispatch` event where `inputs.ref` is unset, it falls back to the workflow_dispatch
**default `release/v0.4.21`** (line 16). That branch does not exist on origin:

```
$ git ls-remote origin refs/heads/release/v0.4.21   # (no output) -> branch absent
$ git ls-remote origin refs/tags/v0.4.21            # cb408c6a... refs/tags/v0.4.21 (a TAG, not the branch)
$ git ls-remote --heads origin | grep release/v0.4  # only refs/heads/release/v0.4.26 exists
```

`actions/checkout` therefore fails to resolve `release/v0.4.21`, the whole job chain is skipped, and the
`always()` verify-step reports `FileNotFoundError`. The dispatched `head_sha` `deeeb64778b3f6109d3a8e49fd652d490901e89c`
does exist and is an ancestor of current `develop` (`git merge-base --is-ancestor` exit 0), but the checkout never
used it because it tried the stale default ref instead. The workflow that produced this run is itself
`Runtime · Docker Core · release/v0.4.21` — i.e. it is being invoked from the v0.4.21 era where that default ref
was valid; the default is now stale.

Note on the mission's ORAS hypothesis: the ORAS step is genuinely missing from `docker-runtime`, but that is NOT
what caused THIS FileNotFoundError. The two are independent failure modes, witnessed separately below.

## (3) Counter-probe (jobs/runs that isolate each mechanism)

- Path/checkout axis — run **44466684726** (this mission): `docker-runtime` failed at checkout because
  `inputs.ref` defaulted to the dead `release/v0.4.21` branch. (Confirmed by the checkout `ref: release/v0.4.21`
  input echo in the job log, line 05:39:46.1975564Z.)
- Path/checkout axis — run **44464060182** (dispatch with `inputs.ref` set to a valid SHA
  `84ee9a93e11fcf275214de38beecc6ef0b9e4e59`): checkout **succeeded**, `Record exact source and toolchain`
  succeeded (so `mkdir -p "$out/tests"` ran), and the failure MOVED downstream to
  `Run runtime integration tests serially` = **failure**, then `Verify all eight` = failure (different message:
  the file now exists but a test failed/aborted). This proves that when the checkout ref is real, the JSONL is
  produced and the FileNotFoundError does not occur.
- ORAS/trust-plane axis — the downstream abort in run 44464060182 is the ORAS gap already documented by the
  closed 0428-128 probe (`evidence/r28-welle4-2026-11-19/docker-gate-wiring/probe-1.md`):
  `app_repository_integration_test.go:27` "prepare BaseHarbor integration trust plane: ORAS is required". This is
  a second, distinct defect: even with a correct ref, `docker-runtime` lacks the ORAS step, so the exact-head
  dispatch runtime tests abort before a clean JSONL PASS.
- develop-push axis — run **44461341870** (push, develop head `deeeb6477`, run SUCCESS): here `docker-runtime`
  is **skipped entirely** by the job-level `if:` at line 175
  (`github.event_name != 'push' || github.ref_name != 'develop'` is false for a develop push). So the green
  develop-push route never runs `docker-runtime`; it cannot be used as a "JSONL was produced" witness.
- green JSONL producer (same proof mechanism) — `single_default_native` runs on develop pushes and writes
  `$RUNNER_TEMP/single-default.jsonl` (line 134). Every green develop-push run of this workflow (e.g. 44461341870,
  44467228776) exercised and passed that JSONL produce+verify, including its ORAS step (line 127-128).

## (4) Minimal owner recipe (patch sketch — owner scope, `.github/**`; lane does not apply it)

Two independent one-line-class hunks, no new gate, no new cell, no test-semantics change. Both live under
`.github/**` (owner scope), so this lane only sketches them.

Hunk A — add the existing ORAS step to `docker-runtime`, identical to `single_default_native` line 127-128,
placed after `Prepare isolated hosted rootless Docker` (line 216-219) and before the image is packaged:

```
       - name: Prepare isolated hosted rootless Docker
         id: runtime_setup
         timeout-minutes: 10
         run: bash scripts/ci-core-rootless-runtime.sh

+      - name: Install verified ORAS for native Core bootstrap
+        run: bash scripts/ci-install-oras.sh
+
       - name: Build BaseHarbor
```

Hunk B — make the stale dispatch default ref resolve to a real ref. The default `release/v0.4.21` no longer
exists as a branch; either update the default to a currently-live ref (e.g. `develop` or `release/v0.4.26`) or
require an explicit `ref` so a missing input fails fast instead of checking out a dead branch:

```
   workflow_dispatch:
     inputs:
       ref:
         description: Git ref to test
         required: false
-        default: release/v0.4.21
+        default: develop
         type: string
```

The `mkdir -p "$out/tests"` (line 205) and the `tee` targets (line 328 etc.) need NO change: they are correct,
they only never ran because the checkout abort skipped `source_identity`. No path change is required — once the
checkout ref resolves, step 4 creates the directory and the test steps create the files.

CI mapping: no new test is introduced, so no `scripts/pr-gate-coverage.json` / selector change is needed for THIS
FileNotFoundError fix; the ORAS bootstrap belongs to the same correction class already tracked in 0428-114
(which absorbed 0428-128). If the exact-head docker-runtime witness is to be made selectable for PRs, that is
0428-114's (b) scope, not this probe's.

## (5) Impact — blocked state of 0428-119/#1690 and 0428-114

- Does this probe change the blocked state of 0428-119/#1690 (exaktkopfiger docker-zeuge)? NO. Run 44466684726
  never produced an exact-head docker witness (it died at checkout). Producing one needs BOTH hunks above plus a
  dispatch with a valid ref; the correction is `.github/**` (owner) + the exact-head dispatch route owned under
  0428-114. #1690 stays blocked pending owner-applied 0428-114(a) (ORAS bootstrap) and a valid-ref dispatch —
  consistent with 0428-128's closeout ("nach der owner-korrektur ist der exact-head-beleg fuer #1690 (119) sofort
  nachfahrbar").
- Does this change 0428-114? NO, it confirms and refines it. 0428-114 already absorbed 0428-128 and owns
  `.github/workflows/docker-runtime-acceptance.yml`: ORAS-install in the `docker-runtime` job (= Hunk A) and the
  `scripts/pr-gate-coverage.json` `TestPersesRuntimeSmokeDockerIsolated` trigger (= 114(b)). This probe adds one
  NEW finding 0428-114 did not name: the **stale `workflow_dispatch` default ref `release/v0.4.21` (line 16)** is
  the direct cause of the FileNotFoundError in run 44466684726 — independent of ORAS. Recommend folding Hunk B
  into 0428-114's `.github` change so a single owner PR fixes both the dead-default-ref and the missing ORAS step.

## cleanliness

This lane started no containers, compose projects, networks, volumes or state directories and ran nothing on the
session host's runtime; the session host is the coordinator/codeman server, and no test stack was launched there.
All runtime truth came from `gh api`/`gh run` logs (read-only) and an isolated `git clone` under `/var/tmp`.

before / after (identical — ambient foreign `bh-local-shared-*` core left untouched per owner directive
2026-11-08):

```
$ docker ps -a --format '{{.Names}}\t{{.Status}}'
bh-local-shared-openbao-1                Created
bh-local-shared-openbao-member-1-1       Created
bh-local-shared-postgres-init-1          Exited (1) 2 days ago
bh-local-shared-postgres-1               Up 2 days
bh-local-shared-openbao-admin-1          Up 2 days
bh-local-shared-postgres-admin-1         Up 2 days
bh-local-shared-postgres-member-1-1      Up 2 days
$ podman ps -a
/bin/bash: line 1: podman: command not found   # podman not installed on this host
```

cleanliness: pass — 0 new containers/networks/volumes by this lane; ambient bh-local-shared-* and core/* untouched;
`/var/tmp/joblog.*` download artifacts removed.

## ls-remote / origin/main witness

```
$ git ls-remote origin main
03507b321ab6a54e868b8d164d46b70b784dcaca	refs/heads/main
$ git cat-file -e origin/main:evidence/r28-welle4-2026-11-19/docker-checks-jsonl/probe-1.md && echo PRESENT
PRESENT   # evidence path confirmed present on origin/main
$ git log --oneline -1 origin/main
03507b32 evidence(0428-136): docker-checks-jsonl probe — root-cause FileNotFoundError in dispatch run 44466684726
```

Candidate (evidence) SHA: `03507b321ab6a54e868b8d164d46b70b784dcaca` on baseharbor-plan origin/main.
Product repo untouched (read-only probe); no product candidate SHA.

## END

END docker-checks-jsonl DONE — probe-1.md delivered read-only; root cause = stale `workflow_dispatch` default ref
`release/v0.4.21` aborts checkout (job skipped, always()-verify -> FileNotFoundError); ORAS-step gap is a separate
downstream abort (run 44464060182), owned by 0428-114(a); #1690(119) unchanged/blocked, 0428-114 confirmed + one
new finding. No product change, host besenrein.
