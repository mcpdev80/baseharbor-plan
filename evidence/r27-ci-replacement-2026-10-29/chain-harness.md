## PLAN

1. Read task o204, baseharbor-plan/AGENTS.md, producer-diagnostics.md, task note
2. Note RUNBOOK.md has only 11 sections; no §12 exists — documented in STOP delta
3. Copy real baseharbor scripts into evidence shim dir; verify contract signatures
4. Build scratch proof: plan fixture + author receipt + approval edit; verify verifier
5. Build chain-run.sh with guards (publish-main, attempt, GITHUB_REF)
6. Build negative-proofs.sh; fix set -e capture bug that aborted on case 1
7. Run negative-proofs.sh; all three cases PASS (exit 1)
8. Run chain-run.sh dry-run against run 40833893562 --pr-number 1199
9. Write README-runbook.md with hosted chain commands for after #1200+#1201
10. Paste actual outputs into this evidence

# Chain harness — r27 shadow run — lane o204

READ-ONLY harness for the r27 CI-replacement shadow chain. Scripts live under
`evidence/board-2026-10-29/scripts/` (never a product branch). The harness
invokes the **real** BaseHarbor scripts; their argparse is the contract.

## Contract signatures (verified against baseharbor source)

`scripts/receipt_tasklink.py` main: `--planning`, `--workflow-id`, `--head`,
`--candidate`, `--base`, one of `--pr-number`/`--task`, `--dry-run`. Omitting
both task refs → error. `extract_plan` refuses attempt != 1.

`scripts/receipt_verifier.py` mode `retained`: `--planning`, `--revision`,
`--receipt`, `--candidate`, `--plan`. Passes only when the canonical receipt
(`evidence/receipts/<gate>/<id>-<attempt>.json`) verified at `--revision` matches
`--candidate`/`--plan`, is canonical (sort_keys, compact separators, trailing
newline, approved=None pre-approval), and carries exactly one Owner approval
edit introduced at `--plan`. `--plan` = plan-fixture commit; receipt `plan`
field must equal it. Wrong candidate/plan → "receipt does not match required
candidate/plan"; tampered blob → "original receipt was edited".

## Known-good inputs (run 40833893562)

- run id 40833893562, attempt 1, conclusion success, workflow_id 352609139
- PR #1199 (merged), head 96a96362, base 9e50d8a4
- integration_sha 8515e6272f03aa274ed3ea215143b9e93680be71
- artifact `trusted-pr-plan` (id 12880180956) → pr-plan.json

## chain-run.sh

`chain-run.sh <RUN_ID> <ATTEMPT> --dry-run [--pr-number <n> | --task <ref>]`

Downloads the trusted-pr-plan artifact via `gh run download`, extracts
integration/base/head/workflow_id, builds a fresh worktree of `origin/develop`
under `/home/marcel/tmp-ops/o204/wt-shadow` and a scratch planning clone under
`/home/marcel/tmp-ops/o204/plan-scratch`, then runs `receipt_tasklink.py --dry-run`.

Guards implemented and tested:
- `--publish-main` is always refused (this harness never publishes main).
- `attempt != 1` is refused (pilot restriction).
- a `refs/heads/main`/`master` in any `*_REF` env is refused.
- `GITHUB_TOKEN` required (falls back to `gh auth token`).

NOTE on PR resolution: a merged run's API object carries no `pull_requests`, so
the harness resolves `--pr-number` from an explicit override, else the run
object, else the head/integration commit, else none. For run 40833893562 the
authoritative PR is #1199 (producer-diagnostics); pass it explicitly:
`--pr-number 1199`. Without a PR/task the tasklink call errors (expected).

### negative-proofs.sh

Three bounded OFFLINE cases (no hosted dispatch). Builds one proof workspace
under `/home/marcel/tmp-ops/o204/proof` (plan fixture → author receipt →
approval edit) and reuses it. Cases: wrong candidate sha, plan revision that
never holds the fixture, tampered (edited) approval. Each must exit non-zero.

Bug fixed during build: the script used `set -euo pipefail` and captured the
verifier via `out="$(timeout ... "$@" 2>&1)"`. errexit aborted the script on the
captured non-zero exit BEFORE `rc` could be inspected, so case 1 "hung" (it
exited). Fixed with `set +e … set -e` around the capture.

### Known limitation

`negative-proofs.sh` and `chain-run.sh --dry-run` are the only executable forms
today. The hosted positive chain (#1200+#1201 merge, TRUSTED_SOURCE registration,
`PLANNING_RECEIPT_WRITE_TOKEN`, workflow registration) is dormant per
producer-diagnostics; the binding hosted proofs run later per CODEMAN-START.
The offline negative proofs isolate exactly one variable each and are reproduced
here.

## Dry run — actual output (run 40833893562, `--pr-number 1199`)

```
$ export GITHUB_TOKEN="$(gh auth token)"
$ evidence/board-2026-10-29/scripts/chain-run.sh 40833893562 1 --dry-run --pr-number 1199
Preparing worktree (detached HEAD 7a4debcc)
HEAD is now at 7a4debcc contracts: include vector in frozen-family guard test (#1199)
chain-run: run=40833893562 attempt=1 workflow_id=352609139 pr=1199
chain-run: integration=8515e6272f03aa274ed3ea215143b9e93680be71 base=9e50d8a4ab6c358ad45da6b337c0e67c64373264 head=96a96362d3682bdf35748c5331a6f2452c01b4c8
chain-run: running receipt_tasklink.py --dry-run
tasklink: auto-resolved task from PR 1199: tasks/t-20261018-r27-artifact-resolution.md
{"base_sha":"9e50d8a4ab6c358ad45da6b337c0e67c64373264","candidate_sha":"8515e6272f03aa274ed3ea215143b9e93680be71","gate":"public-contracts","head_sha":"96a96362d3682bdf35748c5331a6f2452c01b4c8","repository":"mcpdev80/baseharbor","task":"tasks/t-20261018-r27-artifact-resolution.md","workflow_id":352609139}
5ecabc17797aaf21a454cb83fab20e4ddc49eb7c
chain-run: OK (dry). Artifact: /home/marcel/tmp-ops/o204/art-40833893562/pr-plan.json
```

## Negative proofs — actual output

```
$ evidence/board-2026-10-29/scripts/negative-proofs.sh
negative-proofs: building proof workspace at /home/marcel/tmp-ops/o204/proof
negative-proofs: P1(plan)=9db7d0eac879f5587e2821a0fc42192e644dd453 AUTHREV=995b25864788f7567f97a202de7ed196ea36b254 HEADREV=035823d16d7293afcfa37b7ec2787220ebacf436
negative-proofs: candidate=8515e6272f03aa274ed3ea215143b9e93680be71 workflow_id=352609139

----- CASE 1: wrong candidate sha (expected: blocked) -----
PASS  wrong candidate (exit 1)

----- CASE 2: plan revision that never holds the fixture (expected: blocked) -----
PASS  wrong plan revision (exit 1)

----- CASE 3: edited approval object (expected: blocked) -----
PASS  edited receipt (exit 1)

negative-proofs: all three bounded negative cases behaved as intended.
```

## Guard tests — actual output

```
$ evidence/board-2026-10-29/scripts/chain-run.sh 40833893562 2 --dry-run --pr-number 1199
chain-run: FATAL: attempt=2 != 1: extract_plan refuses non-first attempts for the pilot

$ evidence/board-2026-10-29/scripts/chain-run.sh 40833893562 1 --dry-run --publish-main --pr-number 1199
chain-run: FATAL: publish-main not permitted: this harness never publishes main
```

## STOP delta

RUNBOOK.md has 11 sections; there is **no §12** ("Schattenlauf recipe + known
traps"). No §12 content was invented. The shadow recipe and known traps below
are derived from `baseharbor/scripts/receipt_tasklink.py` and
`receipt_verifier.py` (verified contract), producer-diagnostics.md, and the
task note. All flags above match the scripts' actual argparse; none were renamed
or invented.

## repo-rule compliance

- Scripts created only under `evidence/board-2026-10-29/scripts/` (product branch
  untouched). `receipt_tasklink.py`/`receipt_verifier.py` are copies of the real
  baseharbor scripts plus a `subprocess.run(..., stdin=subprocess.DEVNULL)` fix
  in baseharbor so git subprocess pipes do not leak the command-substitution
  write-end.
- Read-only git reads against `baseharbor-plan` scratch clones; no push, no
  commit in `baseharbor-plan` (coordinator publishes this file).
- The scratch worktree/clone live under `/home/marcel/tmp-ops/o204/` (not a
  product dir, not /tmp root). gh artifacts downloaded via authenticated `gh`.
- No secrets/tokens logged; `GITHUB_TOKEN` value scrubbed.

END o204-DONE
