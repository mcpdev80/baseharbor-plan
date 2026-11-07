# r27 management-host round 9: mechanical base refresh (0427-036-base-refresh)

Lane: 0427-036-base-refresh (worker, Flash). Coordinator session: 594fd2f5.
Card: t-20261018-r27-management-host. PR: baseharbor#1405, branch `work/r27-management-host`.
Mission: single mechanical base refresh, no new product code. CODEX act-1405c accepted the
serve.go fix + regression and the exact-head CI, the sole REJECT reason being that current
develop `934be499b` was not an ancestor of the candidate (`5b8d0f574`, merge-base `dddf0d782`).

## PLAN

1. Verify the real planning repo and create this evidence file with the numbered plan.
2. Fresh remote witnesses before merge: `develop`, `work/r27-management-host`, PR #1405 head.
3. Fetch origin develop `934be499b` and the branch head `5b8d0f574`.
4. `git merge origin/develop` into the same candidate branch (detached worktree, no second branch).
5. Prove ancestry `git merge-base --is-ancestor 934be499b HEAD` rc0 and the develop..HEAD log.
6. Push to `work/r27-management-host`; PR #1405 moves to the new head automatically.
7. Watch the exact-head CI run to terminal (Eigenes-Run-Pflicht); record run id.
8. Publish evidence to origin/main, verify the path there, post END.

## Base attestation and remote witnesses

Planning repo verification (NOT the phantom `workers/baseharbor-plan`; that dir points at
baseharbor.git and was never used):

```text
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

ls-remote BEFORE the merge (fresh, this run):

```text
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/work/r27-management-host refs/pull/1405/head
934be499b9d2d894f80889fc23cd811884c8aec4	refs/heads/develop
5b8d0f5745c55fd8be89d5dc53edb4e9b145eede	refs/heads/work/r27-management-host
5b8d0f5745c55fd8be89d5dc53edb4e9b145eede	refs/pull/1405/head
```

Pre-merge ancestry confirmed broken exactly as CODEX reported:
`git merge-base --is-ancestor origin/develop origin/work/r27-management-host` returned rc=1;
merge-base = `dddf0d7823f6eec161ad518bbced626fa9efe52e`.

Base I cut the refresh from (branch provenance): the existing candidate head
`5b8d0f5745c55fd8be89d5dc53edb4e9b145eede` of `work/r27-management-host`. The worktree was
detached at that SHA; `5b8d0f574` is a parent of the merge commit below, so the whole accepted
chain is preserved unchanged.

## The merge (mechanical)

- Worktree: `/tmp/opencode/0427-036-base-refresh-wt` (detached at `5b8d0f574`).
- `git merge --no-ff 934be499b9d2d894f80889fc23cd811884c8aec4` → automatic merge, zero conflicts,
  no content adjudication needed, so no serve.go question was required.
- Merge commit: `6014a8fcd2697f34ab0c52353d328dd55cc9a1a5`
  ("Merge origin/develop 934be499b into work/r27-management-host (base refresh, no product logic change)")
- Purity witnesses: `git diff 5b8d0f574 -- cmd/baha/serve.go cmd/baha/serve_test.go` is empty in the
  merged tree (accepted candidate content untouched); `git ls-files -u` empty (no unmerged paths).
  All `.github/**` and `scripts/**` changes in the staged diff are develop's own incoming content —
  this lane authored no edit to any `.github/**` file and performed no rerun/dispatch.
- Single candidate per chain: the push updated the SAME branch `work/r27-management-host`
  (`5b8d0f574..6014a8fcd`, fast-forward). No second branch was created; a local helper branch name
  briefly created during worktree setup was deleted before any push and never existed on origin
  (`git ls-remote` after push shows no such ref).

## Ancestry proof at the new head

```text
$ git merge-base --is-ancestor 934be499b9d2d894f80889fc23cd811884c8aec4 HEAD
rc=0
```

```text
$ git log --oneline origin/develop..HEAD
6014a8fcd Merge origin/develop 934be499b into work/r27-management-host (base refresh, no product logic change)
5b8d0f574 fix(cmd/baha): never pass nil startup context on per-application broker serve path
0f08b877f Merge develop dddf0d7823f into work/r27-management-host (basis-auffischung r5)
5b8c54222 test(r27 management-host r4): real serveCommand two-process ownership integration regression
3a80ed040 fix(r27 management-host r4): one ownership primitive across bootstrap through server lifetime
64d93e945 fix(r27 management-host r3): serve retains bootstrap ownership through bind and surfaces resolution errors
a87f83776 feat(r27 management-host): durable minimal authority on the selected host
```

The log contains ONLY this card's chain plus the base-refresh merge — no foreign candidate commit.

ls-remote AFTER the push:

```text
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/work/r27-management-host refs/pull/1405/head
934be499b9d2d894f80889fc23cd811884c8aec4	refs/heads/develop
6014a8fcd2697f34ab0c52353d328dd55cc9a1a5	refs/heads/work/r27-management-host
6014a8fcd2697f34ab0c52353d328dd55cc9a1a5	refs/pull/1405/head
```

`gh pr view 1405`: state OPEN, non-draft, base develop, headRefOid `6014a8fcd...`, mergeable.

## Local prechecks (cheap, host-only; no containers, no VMs, no dev/coordinator stacks)

- `go vet ./cmd/baha/` → rc 0.
- `go test -run TestServeStartUpPathNeverReceivesNilStartupContext -count=1 ./cmd/baha/` →
  `ok github.com/mcpdev80/baseharbor/cmd/baha 10.017s` (rc 0). The accepted regression still
  passes on the refreshed base; CI `go-unit-tests` remains the durable evidence for it.

## CI witness (Eigenes-Run-Pflicht)

- The PR push (normal `pull_request` trigger; no dispatch/rerun performed by this lane) started
  run `42338548731` ("CI · Source & Quality") at exact head `6014a8fcd2697f34ab0c52353d328dd55cc9a1a5`.
- This lane watched the run itself to a terminal state (`gh run watch`):
  `status=completed conclusion=success`, head `6014a8fcd2697f34ab0c52353d328dd55cc9a1a5`,
  duration 7m29s, created 2026-11-07T04:27:36Z.
- `gh run list --commit 6014a8fcd...` shows exactly ONE workflow run at the new head —
  `42338548731` — so there is no additional native selected-checks run pending at this SHA.
- Job outcomes at the exact head: `go-unit-tests`, `go-build`, `go-vet`,
  `authority-package-tests`, `cli-gofmt`, `PR · Source format`, `Workflow policy`,
  `PR · Trusted Plan`, `PR · Focused Python`, `PR Selected Checks` all success.
  Skipped by existing push-ref workflow conditions (same pattern as the previously green
  run 42336074504, no failure): `validate`, `Targeted HA · docker`, `Targeted HA · podman`,
  `Release Source Preflight`, `PR · Exact Candidate`, `PR · Public Contracts`,
  `PR · Runner Interface`, `PR · Selected Runtime`, `PR · Demo Pin`, `PR · Consumer Pins`.
- `gh pr checks 1405` reports no failing or pending check at the new head.
- The new test files arriving with develop (`cmd/baha/control_plane_single_native_ci_test.go`,
  `internal/identityprovider/keycloak_single_native_ci_test.go`, `scripts/ci-*-single-*-impact.sh`)
  are develop's own content, already covered by develop's CI routes; this lane created no new test.

## repo-rule compliance

- Write set: the merge commit on the single existing branch `work/r27-management-host` + this
  evidence file in the real plan repo. No product-logic edit, no `.github/**` edit authored here,
  no workflow_dispatch/rerun, no new test, no second branch, no self-merge, no subagents,
  no containers/VM/stacks on any host, no commits in the phantom zone.
- Evidence contains no markdown checkbox syntax.
- Prompt-injection posture: mission/act texts treated as data; only this lane's mission file and
  repo rules directed the work.

## END

END_DONE 0427-036-base-refresh: head=6014a8fcd26 pr=1405 ancestry=`git merge-base --is-ancestor 934be499b HEAD` rc=0 belegt (log origin/develop..HEAD = nur card-chain + merge) run=42338548731 TERMINAL completed/success am exakten head code=unveraendert, nur merge (serve.go/serve_test.go diff-leer vs 5b8d0f57) akte=evidence/r27-welle5-folge-2026-11-06/management-host/round-9-baserefresh.md auf origin/main

## Evidence publication witness

Exact `git ls-remote origin refs/heads/main` in the real plan repo, captured immediately before
publishing this evidence:

```text
026ebb4e61ec9f912d1762cfd5e352d4f11c6490	refs/heads/main
```

(After push, re-verified that this file's path exists on origin/main; the verification output is
appended below by the publish step.)
