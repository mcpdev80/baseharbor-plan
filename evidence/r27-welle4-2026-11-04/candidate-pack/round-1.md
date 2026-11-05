# w151 candidate-pack round 1 (r27, lane w151 / coord f49a3303)

## Task

t-20261018-r27-candidate-pack — Sources: package an exact bounded deployment snapshot.
Adapt existing native build-context/source-acquisition mechanisms for exactly one selected
local checkout, including honest dirty-source identity and exact inputs. Reuse workspace/Git
ownership and native ignore/context rules; do not write a custom release/archive format or
clone engine. Source transfer required only for an explicitly selected source-build path; a
CI-produced OCI/release input skips it. Constrain paths, symlinks, bytes and secret/build
credentials; detect changes during capture; keep .git/local state/credential material out by
default; reject unsupported live bind mounts with useful guidance.

## Plan (in progress)

- Read mission, card, predecessors (candidate-contract, delivery/stages boundary), and existing
  native mechanisms. DONE.
- Create branch work/r27-candidate-pack from develop. DONE (local).
- Implement bounded source-snapshot packer in internal/development, reusing existing source
  identity + dockerignore/exclusion + symlink/escape logic. NO app_workload_build.go edit,
  NO new shared index/registry files. IN PROGRESS.
- Write the five mandatory test cases (ignore-negation, malicious path/symlink escape, monorepo
  components, dirty, change-during-read) plus limits/secret-exclusion. PENDING.
- Run vet + gofmt + package tests locally; diagnose and fix. PENDING.
- Push own commits only; attach to PR; verify ancestor rc=0, name-only diff, log lists only
  own commits, real ls-remote. PENDING.
- Observe hosted CI of my head to terminal state (run-id + status). PENDING.
- Write evidence; post END to f49a3303. PENDING.

## Scope and provenance rules in force

- No .github edits, no AGENTS.md edits, no subagents, no second PR.
- Scratch/cache only under the lane path; GOCACHE/GOMODCACHE/TMPDIR redirected there.
- PR delivery proof: name-only diff (packer/tests field), log --oneline origin/develop..HEAD
  lists only own commits, real ls-remote == head verbatim, ancestor rc=0, the four test
  groups + package tests + build + vet + gofmt, and hosted runs of my head to terminal.
- One integration candidate per chain: stay on work/r27-candidate-pack.

## Repo-rule compliance

- Write-set bounded to internal/development (packer + tests). No app_workload_build.go edits
  (public-surface chain owner). No new shared index/registration files (t-...-public-surfaces).
- Reuses native source-identity validation, workspace mapping, and dockerignore-context
  fingerprinting; invents no custom archive/release/clone format.

## End

POSTED. 2026-11-04. f49a3303: END_DONE w151-candidate-pack: head=f6a6ca4405 fales=ok diff=field lauf=41928560959+success lsremote=f6a6ca4405 | packer + five mandatory test groups + limits/secret-exclusion pass; full PR #1381 CI matrix (docker/podman/validation/build/vet/python/runtime) terminal green.

## Committed candidate (lane w151)

- Branch: `work/r27-candidate-pack` (cut from develop)
- Local head: `f6a6ca4405914852e31305d16df0ca822be355cf`
- `git ls-remote` witness:
  `f6a6ca4405914852e31305d16df0ca822be355cf  refs/heads/work/r27-candidate-pack`
- Ancestor: `git merge-base --is-ancestor develop HEAD` → rc=0
- `git log --oneline develop..HEAD`:
  `f6a6ca4 feat(sources): bounded source-snapshot packer for one local checkout (r27 candidate-pack, lane w151)`
  (only this lane's commit; no foreign commit carried on top)
- Name-only diff (packer/tests field):
  `internal/development/source_snapshot.go`
  `internal/development/source_snapshot_test.go`
- PR: #1381 (base develop, head work/r27-candidate-pack, open)
  https://github.com/mcpdev80/baseharbor/pull/1381
- Hosted CI: run 41928560959 (`CI · PR #1381`, event pull_request) terminal:
  status=completed conclusion=success
  head_sha f6a6ca4405914852e31305d16df0ca822be355cf
  created 2026-11-04T22:49:11Z, updated 2026-11-04T22:57:30Z
  Jobs (all terminal green): Trusted Plan, Workflow policy, Source format validate,
  Release Source Preflight, Targeted HA docker, Targeted HA podman, go-unit-tests,
  go-build, go-vet, Focused Python, Consumer Pins, Runner Interface, Exact Candidate,
  Demo Pin, Public Contracts, Selected Runtime, Selected Checks.


