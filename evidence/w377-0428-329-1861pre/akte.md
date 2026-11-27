# Evidence — w377-0428-329-1861pre

Disjunct prework for PR #1861 (card 0428-329). Local hop, NO push, NO hosted re-run, NO merge, NO product changes. Qualification of this lane stays strictly AFTER plan #136 landing (baseline-family catalog rows) and AFTER the #183-pin sequence.

## ANSATZ block (visible, verbatim — visible before first commit)

- Owner / canonical lane identity (from this mission frontmatter): `w377-0428-329-1861pre`
- commit `user.name`: `w377-0428-329-1861pre`
- commit `user.email`: `w377-0428-329-1861pre@baseharbor.local`
- literal commit/merge invocation used (none created — this lane is a local hop; no product commit):
  `git -c user.name=w377-0428-329-1861pre -c user.email=w377-0428-329-1861pre@baseharbor.local commit ...`
- pre-push author gate line (mechanically verified before any push; not pushed here):
  `git show -s --format=%an HEAD` must equal `w377-0428-329-1861pre` exactly; on mismatch STOP + report.

## (a) PR Ist-Zeuge (PR #1861; internal handle "1861pre" == branch w334-0428-329-recoveryheuristic)

`gh pr view 1861 --repo mcpdev80/baseharbor --json headRefOid,headRefName,baseRefName,state,mergeable`

```json
{"baseRefName":"develop","headRefName":"w334-0428-329-recoveryheuristic","headRefOid":"ade7dab3cf06658efd9a172ce3a674b887bd3c79","mergeable":"MERGEABLE","state":"OPEN"}
```

Full mergeStateStatus: `BLOCKED`. PR title: "fix(0428-329): tighten recovery/backup preserve to authoritative label-key".

Remote attestations (own `git ls-remote`, github.com/mcpdev80, via `baseharbor` remote in the worktree):
```
ade7dab3cf06658efd9a172ce3a674b887bd3c79  refs/heads/w334-0428-329-recoveryheuristic
ea5218d72e263f21e79853b679af50074dab8c25  refs/heads/develop
```
Note: `gh pr view 1861pre` / `gh pr checks 1861pre` return "no pull requests found for branch 1861pre" — `1861pre` is an internal lane handle, not a GitHub PR number. The real PR is #1861. This is a disposition finding, not a blocker.

## (b) Worktrees

Product worktree (from PR branch head, exact checkout):
```
/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w377-0428-329-1861pre-1861pre
HEAD = ade7dab3c fix(0428-329): ...full destroy
remote baseharbor = https://github.com/mcpdev80/baseharbor.git   (only github.com/mcpdev80 remote used)
```
Isolated plan worktree (plan repo, NOT the quarantined workers/baseharbor-plan dir):
```
/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w377-0428-329-1861pre-plan
remote baseharbor = https://github.com/mcpdev80/baseharbor-plan.git  (origin in that worktree)
```
Plan remote verified via `git -C <path> remote -v` before first evidence commit. No foreign worktree touched (not reused, not deleted).

## (c) Develop merge — BASE and result

Base attestation (before branch/merge):
```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
=> ea5218d72e263f21e79853b679af50074dab8c25
```
`baseharbor/develop` at `ea5218d72` is the DIRECT parent of PR head `ade7dab3c` (`git merge-base HEAD baseharbor/develop` == `ea5218d72`, and `git log baseharbor/develop..HEAD` lists only `ade7dab3c`). Nothing changed in develop since the PR base, so the develop merge is a no-op.

Merge attempt:
```
git merge baseharbor/develop
=> fatal: refusing to merge unrelated histories
```
This refusal is a git heuristic that fires when the merge-base equals one tip exactly (no divergence to combine). It is NOT a real content conflict — develop has zero new commits relative to the PR base. The clean merge result is therefore the PR head `ade7dab3c` unchanged. No conflict file:line (there is none). No push, no force.

REMOTE GUARD observed: in this worktree `origin` points at `baseharbor-plan` (not the product); the product remote is `baseharbor` (https://github.com/mcpdev80/baseharbor.git). Only `baseharbor` was used for fetch/merge.

## (d) Residual failure surface — classified, NO hosted/local run executed

Hosted run already present on the exact head (run 45931739218, event `pull_request`, headSha `ade7dab3...`, conclusion `failure`):

| Gate | Status | Witness |
|---|---|---|
| PR · Trusted Plan | **FAIL** | job 140285684691 conclusion=failure; PR Selected Checks aggregate job 140287344703 failure |
| PR Selected Checks (aggregate) | **FAIL** | job conclusion=failure (driven by Trusted Plan) |
| PR · Native gate plan | PASS | job 140285684742 conclusion=success |
| PR · Source format | PASS | job 140285684680 conclusion=success |
| PR · Workflow policy | PASS | job 140285684074 conclusion=success |
| All runtime / Go unit / release / Consumer-Pins / Demo-Pin / Exact-Candidate gates | SKIPPING | matrix `{"include":[]}` (no runtime required yet — expected for a code-defect fix with no catalog rows) |

Exact failing log line (Trusted Plan job 140285684691, `pr-gate-plan.py` line 1952 -> raise at 548):
```
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner:
  cmd/baha/app_destroy_volumes_recovery_backup_test.go (id source.cmd_baha_app_destroy_volumes_recovery_backup_test_go);
  internal/runtime/repository_volume_inventory.go (id source.internal_runtime_repository_volume_inventory_go);
  internal/runtime/repository_volume_inventory_test.go (id source.internal_runtime_repository_volume_inventory_test_go)
add these sources with their surfaces to scripts/pr-gate-coverage.json, e.g.
{"id":"source.cmd_baha_app_destroy_volumes_recovery_backup_test_go","path":"cmd/baha/app_destroy_volumes_recovery_backup_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]};
{...repository_volume_inventory_go...}; {...repository_volume_inventory_test_go...}
```

This is a **catalog-prerequisite failure surface**, not a code defect: the gate fails because three uncataloged source paths are not yet declared in `scripts/pr-gate-coverage.json`. Verified locally:
- `git diff baseharbor/develop..HEAD --name-only` == exactly the three flagged paths (new test + removed recovery/backup substring heuristic + new full-destroy test).
- `scripts/pr-gate-coverage.json` (schema `baseharbor.pr-gate-coverage/v1`, release `v0.4.27`) has 321 components; NONE of the three flagged paths are present, while many sibling paths (`*_destroy_*.go`, `*inventory*.go`) ARE cataloged. So the missing baseline row the Trusted Plan gate demands is the `components` array entries for these three paths in `scripts/pr-gate-coverage.json`.
- The actual code change itself (`internal/runtime/repository_volume_inventory.go`) only REMOVES a `recovery/backup` substring label heuristic — that is the card's code-defect fix; it is not itself the failing item.

Scope note on the fix: the diff removes the substring-based `Shared`/"recovery/backup data; preserved" logic so full destroy deletes every owned recovery/backup volume under authoritative ownership. This is the card #0428-329 fix and is within a normal product PR — but per this mission this lane is a local hop only, so no edit is made here.

## (e) What is first responsible after #136 landing

The ONE thing that first must happen: plan #136 must land (landing of plan #136 = the catalog rows for the baseline family), THEN this lane #1861 prework qualifies. Until #136 is landed the catalog-prerequisite gate cannot be closed here. Concretely, the next responsible artifact (Owner/plan scope, NOT this lane): add the three missing `components` entries to `scripts/pr-gate-coverage.json` (the missing baseline row named in (d)) — this is a `scripts/` change owned by the plan/CI owner, so it is a finding with `file:line` here, not a local edit. After the catalog row is in and #136 is landed, the Trusted Plan gate re-runs green on head `ade7dab3c` and this lane's prework is qualified.

## Cleanliness / runtime

- No docker/podman compose project started (local hop). `docker ps -a` not applicable.
- No build/run/test executed on this host.
- Branch provenance: base `ea5218d72` (develop) shown as ancestor via `git merge-base --is-ancestor` semantics (merge-base == develop tip); `git diff baseharbor/develop..HEAD --name-only` pasted above lists only the three own commits.

## END

`END_DONE w377-0428-329-1861pre` — local hop complete, no push, no hosted run, no merge, no product edit. Classification + missing catalog row documented with file:line. Next responsible act = plan #136 landing, then #1861 catalog qualification.
