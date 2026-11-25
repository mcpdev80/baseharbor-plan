# Planning evidence path collision recovery

## PLAN

1. Verify the live planning repository remote, freshly fetched main tip, both recoverable source contents, and the missing canonical evidence path.
2. Restore the H-V59 w228 akte and w243 #1853 rundown to their requested evidence paths, then delete the misplaced root `akte.md`.
3. Add a changed-path validator that rejects new or modified files outside `evidence/`, permitting `tasks/` and `releases/` for card work and narrow implementation files for the validator itself.
4. Add focused unit coverage and wire the validator into the existing planning validation workflow.
5. Run plan rendering/checking and unit validation, prove branch ancestry and exact changed paths, publish one planning PR, merge it, and verify both artifacts on origin/main.

## Visible commit ansatz

This is a repository integrity repair and evidence relocation; it creates no task/card and changes no product repository. Lane identity: `w200-plan-akte-recovery`. Git user.name: `w200-plan-akte-recovery`; git user.email: `w200-plan-akte-recovery@baseharbor.local`. Literal invocation: `git -c user.name=w200-plan-akte-recovery -c user.email=w200-plan-akte-recovery@baseharbor.local commit -m "fix(plan): restore evidence paths and validate PR scope"`. Pre-push gate: `test "$(git show -s --format=%an HEAD)" = w200-plan-akte-recovery`.

## Source and base witnesses

Planning remote verified before worktree creation: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push). Fresh fetched base at worktree creation: `bc4689919f2cf8a1c7fdd7ddc817b39c14495fde` (`origin/main`); the candidate was integrated with current `origin/main` `4ad5606273cba90b0c27aaeaf33c003124f067f8`, then current `main` advanced to `4e1ab652f141cd57466d741ae91d2e3fbdd92c6e` (#45). That update added w244's correctly located evidence file; root `akte.md` remains w243's original blob `e5736dfa23a769a6e86845584601d6e32b057bd3`, so deleting the root still removes only the duplicate w243 placement. The source root file at `b21824438` is w243's #1853 rundown and has that same blob. The w228 H-V59 content is preserved in `272baad4384335f0a6d2501b48db39fdf75ee5b8^:akte.md`; its blob is `ad302f2a24f4a8d1e4ba1a1e0d0916acc6e7d395`. `git branch -r --contains 272baad43` returned no branches and `git merge-base --is-ancestor 272baad43 origin/main` failed: the rename commit is not on live main. The intended w228 path `evidence/w228-0428-216-huntv59/akte.md` was absent on main before repair. Both requested target paths were absent on the fresh base.

## Intended recovery

- Restore w228's content from the parent of rename commit `272baad4384335f0a6d2501b48db39fdf75ee5b8` to `evidence/w228-0428-216-huntv59/akte.md`.
- Restore w243's current root content from the source commit/tree at `b21824438` to `evidence/r29-welle6-2026-11-28/0428-253/w243-1853-rundown.md`.
- Delete root `akte.md`; do not rewrite or force-push history.
- Add a path policy to the planning PR validator: ordinary evidence PRs may change only `evidence/**`; card work may additionally change `tasks/**` and `releases/**`. Only root-file deletion is allowed as cleanup. The validator's own implementation/test/workflow files are an explicit narrow exception so the policy can be introduced and maintained. New or modified root `akte.md` remains rejected.

The requested #0428-313 skeleton is a separate disposition and is not included in this repair PR. No card was created or modified as part of this evidence-path recovery.

## CI route

The validator test will live under `scripts/tests/` and run in the existing `.github/workflows/validate.yml` `Unit tests` step (`python3 -m unittest discover -s scripts/tests -v`). The PR-scope validator will run in the same planning workflow's pull-request event before `plan.py check`, using the event base ref. No product repo workflow is involved.

## Publication witnesses

Worktree cut SHA: `bc4689919f2cf8a1c7fdd7ddc817b39c14495fde`; integrated base at publication: `4e1ab652f141cd57466d741ae91d2e3fbdd92c6e`. The branch retains the already-pushed history and merges newer `origin/main` normally; no force push or remote rewrite was used. `git merge-base --is-ancestor origin/main HEAD` succeeded. `git log --oneline origin/main..HEAD` output:

```text
f426a917d integrate previously pushed evidence history
7f6727793 evidence(plan): record akte recovery push witness
94fa78933 evidence(plan): record akte recovery provenance
217d1497b fix(plan): recover evidence paths and validate PR scope
481451072 evidence(plan): record akte recovery push witness
fed044693 evidence(plan): record akte recovery provenance
17c00f34a fix(plan): recover evidence paths and validate PR scope
```

`git diff origin/main...HEAD --name-only` output:

```text
.github/workflows/validate.yml
evidence/r29-welle6-2026-11-28/0428-253/w243-1853-rundown.md
evidence/r29-welle6-2026-11-28/plan-akte-collision/akte-recovery.md
evidence/w228-0428-216-huntv59/akte.md
scripts/tests/test_validate_pr_paths.py
scripts/validate_pr_paths.py
```

`git diff --name-status --no-renames origin/main...HEAD` output:

```text
M	.github/workflows/validate.yml
D	akte.md
A	evidence/r29-welle6-2026-11-28/0428-253/w243-1853-rundown.md
A	evidence/r29-welle6-2026-11-28/plan-akte-collision/akte-recovery.md
A	evidence/w228-0428-216-huntv59/akte.md
A	scripts/tests/test_validate_pr_paths.py
A	scripts/validate_pr_paths.py
```

`python3 scripts/validate_pr_paths.py 4ad5606273cba90b0c27aaeaf33c003124f067f8` reported `planning PR path scope accepted: 7 changed paths`. Tip author gate passed: `git show -s --format=%an HEAD` equals `w200-plan-akte-recovery`.

## Validation

`python3 -m unittest discover -s scripts/tests -v`: 72 tests passed, including four new changed-path policy tests. `python3 scripts/plan.py check`: 776 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 existing accepted-task dependency warnings. The path check is registered in `.github/workflows/validate.yml` for `pull_request`; its module tests run in the existing `Unit tests` step.

First branch push delivery witness: `fed044693b251ae81ebad6d635b355a273d24abc refs/heads/codex/w200-plan-akte-recovery-20261126` from `git ls-remote origin refs/heads/codex/w200-plan-akte-recovery-20261126`.

Updated branch push delivery witness after normal integration with newer main: `5770fd731a52e406eb92da4c39a92bc7ebc30e54 refs/heads/codex/w200-plan-akte-recovery-20261126` from `git ls-remote origin refs/heads/codex/w200-plan-akte-recovery-20261126`.
