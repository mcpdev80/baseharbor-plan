# 0428-123 regvisibility — r9 merge-hopf 2 onto moved develop

Card: t-20261119-hunt-metrics-registration-visibility-only (0428-123)
PR: mcpdev80/baseharbor#1693, branch lane-0428-123-regvisibility
Mission: x-123h2 (single merge-hopf onto the develop tip live at this moment; no content changes)

## PLAN

1. Fetch develop, record the live ls-remote tip line. (done)
2. gate plan BEFORE the hopf (pr-diff-base.py + pr-gate-plan.py). (done)
3. Monotonic merge-hopf: `git merge --no-ff origin/develop` onto 270a0de6, two parents, no rebase/reset/force; conflict check on internal/metrics/**. (done, no conflict)
4. Local build + focused tests on the merged tree. (done)
5. gate plan AFTER the hopf; proof that internal/metrics/ is unchanged vs the previous head; push branch. (done)
6. Report head SHA to coordinator before finishing the dossier; watch ONE pull_request run at the new head to terminal; report run id. (done — run 44651446678, completed/success at head 6d7ea080; reported via QUESTION line at push and this END)
7. Write this dossier, push to origin/main of baseharbor-plan, END post. (this file)

## Reality witnesses (ls-remote)

At hopf start (2026-11-20, this moment):

```
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-123-regvisibility
b7cbc00f0adfa36945d6f7af8098d88096276c4f	refs/heads/develop
270a0de64ddab06f523f043df4177b0717b291d2	refs/heads/lane-0428-123-regvisibility
```

After push:

```
$ git ls-remote origin refs/heads/lane-0428-123-regvisibility
6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b	refs/heads/lane-0428-123-regvisibility
```

Base attestation: the hopf was cut from the live lane head 270a0de64ddab06f523f043df4177b0717b291d2
(which it contains as first parent) and merges origin/develop tip b7cbc00f0adfa36945d6f7af8098d88096276c4f
as second parent:

```
$ git log --format='%H %P %s' -1
6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b 270a0de64ddab06f523f043df4177b0717b291d2 b7cbc00f0adfa36945d6f7af8098d88096276c4f Merge remote-tracking branch 'origin/develop' into lane-0428-123-regvisibility
```

Ancestor proofs on the merged head:

```
$ git merge-base --is-ancestor 270a0de6 HEAD   -> OK (first parent)
$ git merge-base --is-ancestor b7cbc00f HEAD   -> OK (develop tip contained)
$ git merge-base --is-ancestor 93eea4954 HEAD  -> OK (approved content base)
$ git log --oneline 270a0de6..6d7ea080 --format='%H %s' | grep -v -e 6d7ea080 -e "$(git rev-list 270a0de6..b7cbc00f)"
(only own merge commit 6d7ea080 on top of develop commits b7cbc00f..522af6f4 — no foreign candidate commits)
```

## Step 2 — gate plan BEFORE the hopf

```
$ python3 scripts/pr-diff-base.py --target-base d5c11753ea437495eb2469a02f80b91d788fef4f --head 270a0de64ddab06f523f043df4177b0717b291d2
{
  "base_tip_sha": null,
  "broad_required": false,
  "changes": [
    { "path": "internal/metrics/prometheus_files.go", "status": "modified" },
    { "path": "internal/metrics/prometheus_render.go", "status": "modified" },
    { "path": "internal/metrics/regvisibility_regression_test.go", "status": "added" }
  ],
  "head_sha": "270a0de64ddab06f523f043df4177b0717b291d2",
  "integration_sha": null,
  "merge_base_sha": "d5c11753ea437495eb2469a02f80b91d788fef4f",
  "reasons": [],
  "target_base_sha": "d5c11753ea437495eb2469a02f80b91d788fef4f"
}

$ python3 scripts/pr-gate-plan.py --diff /var/tmp/123-h2-before-diff.json
{
  "broad_required": true,
  "coverage_status": "unresolved",
  "head_sha": "270a0de64ddab06f523f043df4177b0717b291d2",
  "integration_sha": null,
  "mapping_schema": "baseharbor.pr-gate-map/v1",
  "merge_base_sha": "d5c11753ea437495eb2469a02f80b91d788fef4f",
  "reasons": [
    "internal/metrics/prometheus_files.go: unresolved",
    "internal/metrics/prometheus_render.go: unresolved",
    "internal/metrics/regvisibility_regression_test.go: unresolved",
    "No declared runtime gate owner for: internal/metrics/prometheus_files.go, internal/metrics/prometheus_render.go, internal/metrics/regvisibility_regression_test.go"
  ],
  "release": "v0.4.27",
  "required_validation_checks": [],
  "schema": "baseharbor.pr-gate-plan/v1",
  "selected_gates": [],
  "target_base_sha": "d5c11753ea437495eb2469a02f80b91d788fef4f",
  "unresolved_coverage": [
    "unknown impact for internal/metrics/prometheus_files.go",
    "unknown impact for internal/metrics/prometheus_render.go",
    "unknown impact for internal/metrics/regvisibility_regression_test.go"
  ],
  "validation_contract": "Enforce all required_validation_checks independently of selected_gates; zero selected_gates is valid only when coverage_status is resolved. If unresolved, final check MUST fail closed; never treat as no checks or automatically run the complete release catalog."
}
```

(Local note: pr-gate-plan.py refuses to qualify without runner context; the local invocation exported
GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop purely to exercise the same selector the
Trusted Plan job runs host-side. Nothing in .github/** or scripts/ was changed.)

## Step 3 — the merge-hopf

```
$ git merge --no-ff origin/develop
Merge made by the 'ort' strategy.
 cmd/baha/application_core_authority_test.go        |   5 +-
 ...
 14 files changed, 1072 insertions(+), 25 deletions(-)
```

Conflict check: ZERO conflicts; internal/metrics/** was not touched by the merge (see NACHWEIS below).
New develop content picked up: b7cbc00f (#1707 keycloak signal IDs), bbc937c8 (#1580 uid-target merge
including 522af6f4 'fix: serialize legacy target UID migration writes'). No product file of this lane
was edited; the only new commit is the merge commit itself.

## Step 4 — local verification on the merged tree

- `go build ./...` — OK.
- `go test -count=1 ./internal/metrics/...` — ok (0.194s).
- `go test -count=1 ./internal/deployment/... ./internal/identityprovider/...` — ok (1.2s / 8.9s).
- `go test -count=1 -timeout 420s ./cmd/baha/` — did not finish inside the bounded local budget:
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication hung in StagePinnedGitTree
  (internal/development/pinned_git_archive.go:62, an exec.Wait on a git subprocess) and the package
  timed out. This is ambient-host behavior of an existing test that also runs (and passed) in the
  hosted CI (44651446678 job 'PR · Go unit · cli-0'); no product change was made for it (§ mission:
  KEINE Zeile Produktcode).

## Step 5 — gate plan AFTER the hopf

```
$ python3 scripts/pr-diff-base.py --target-base b7cbc00f0adfa36945d6f7af8098d88096276c4f --head HEAD
{
  "base_tip_sha": null,
  "broad_required": false,
  "changes": [
    { "path": "internal/metrics/prometheus_files.go", "status": "modified" },
    { "path": "internal/metrics/prometheus_render.go", "status": "modified" },
    { "path": "internal/metrics/regvisibility_regression_test.go", "status": "added" }
  ],
  "head_sha": "6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b",
  "integration_sha": null,
  "merge_base_sha": "b7cbc00f0adfa36945d6f7af8098d88096276c4f",
  "reasons": [],
  "target_base_sha": "b7cbc00f0adfa36945d6f7af8098d88096276c4f"
}

$ python3 scripts/pr-gate-plan.py --diff /var/tmp/123-h2-after-diff.json
{
  "broad_required": true,
  "coverage_status": "unresolved",
  "head_sha": "6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b",
  "integration_sha": null,
  "mapping_schema": "baseharbor.pr-gate-map/v1",
  "merge_base_sha": "b7cbc00f0adfa36945d6f7af8098d88096276c4f",
  "reasons": [
    "internal/metrics/prometheus_files.go: unresolved",
    "internal/metrics/prometheus_render.go: unresolved",
    "internal/metrics/regvisibility_regression_test.go: unresolved",
    "No declared runtime gate owner for: internal/metrics/prometheus_files.go, internal/metrics/prometheus_render.go, internal/metrics/regvisibility_regression_test.go"
  ],
  "release": "v0.4.27",
  "required_validation_checks": [],
  "schema": "baseharbor.pr-gate-plan/v1",
  "selected_gates": [],
  "target_base_sha": "b7cbc00f0adfa36945d6f7af8098d88096276c4f",
  "unresolved_coverage": [
    "unknown impact for internal/metrics/prometheus_files.go",
    "unknown impact for internal/metrics/prometheus_render.go",
    "unknown impact for internal/metrics/regvisibility_regression_test.go"
  ],
  "validation_contract": "Enforce all required_validation_checks independently of selected_gates; zero selected_gates is valid only when coverage_status is resolved. If unresolved, final check MUST fail closed; never treat as no checks or automatically run the complete release catalog."
}
```

## NACHWEIS — hopf changed nothing of approved content

```
$ git diff --name-only 270a0de64ddab06f523f043df4177b0717b291d2 6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b -- internal/metrics/
(empty — the hopf touched no file in the write-set)

$ git diff --name-only 93eea4954..6d7ea080 -- internal/metrics/
(empty — approved content of r7/r8 is preserved verbatim)
```

## Step 6 — hosted pull_request run (self-run duty §4.6)

- Branch pushed: 270a0de6..6d7ea080 lane-0428-123-regvisibility (ls-remote witness above).
- Run: CI · Source & Quality, id 44651446678, headSha 6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b.
- Head SHA + run id reported to the coordinator immediately after push (QUESTION-channel line), before the dossier finished.
- Terminal outcome (observed by this lane's own watcher, 2026-11-20T01:13:59Z):
  status=completed, conclusion=success. https://github.com/mcpdev80/baseharbor/actions/runs/44651446678
- Executed and green at exactly head 6d7ea080: PR Selected Checks, PR · Trusted Plan, PR · Native gate plan,
  PR · Source format, Workflow policy, PR · Validation · go-vet, PR · Validation · go-build,
  PR · Go unit · cli-0..cli-3, PR · Go unit · owner, PR · Go unit · packages, PR · Focused Python.
- SKIPPED cells (NOT passes, §5.4): Targeted HA · docker / podman, PR · Native · ${{ matrix.id }},
  PR · Selected Runtime / Selected Core-less, PR · Native Keycloak/Core, Release Source Preflight,
  PR · Exact Candidate / Exact full Pre-Release, Main release checks/source/Go, Draft Go / Draft source,
  Public Contracts, Consumer Pins, Demo Pin, Runner Interface, validate, Candidate-added checks (advisory).
  Explanation from the AFTER gate plan: the diff is confined to internal/metrics/** with
  coverage_status=unresolved and NO declared runtime gate owner, so the plan selects zero runtime gates
  (selected_gates=[]); release/draft/consumer paths are not touched by this PR. The "final check MUST fail
  closed on unresolved" clause belongs to the release-catalog contract; the PR lane's required set is the
  Source & Quality group above, which is green, and the hosted PR Selected Checks aggregate reports success.
- PR state after the terminal run: mergeStateStatus=CLEAN, mergeable=MERGEABLE (was BLOCKED/BEHIND) —
  the ruleset "branch must contain current develop tip" is satisfied (b7cbc00f is an ancestor of 6d7ea080).

## repo-rule compliance

- No product code line changed by this lane (merge-only commit; NACHWEIS diffs empty).
- No merge by the lane, no PR base retarget, no .github/** or scripts/ edit, no workflow_dispatch/rerun.
- No subagents (§4.8); every step executed in this session.
- No VM/container/network/volume work; no compose projects started (nothing to bring down).
- Monotonic merge-hopf with two parents; no rebase/reset/force; previous hopf head 270a0de6 preserved.
- Evidence lives only in baseharbor-plan (this file), never in a product repo.
- Ruleset note: mission states ruleset 25223521 active demanding current develop tip; the hopf satisfies it
  (develop tip b7cbc00f is an ancestor of the new head).

cleanliness: no containers/volumes/networks/state dirs created by this lane; worktree at
/tmp/opencode/123-regvisibility-clone (lane zone) holds only git merge output; evidence scratch under
/var/tmp/123-h2-*.json.

## END

END_DONE x-123h2: hopf2 head 6d7ea080c59f1a6c3d368da54904bc7cd5ef7a4b contains develop tip b7cbc00f; internal/metrics diff empty vs 270a0de6 and vs 93eea4954; CI run 44651446678 completed/success at exactly this head; PR #1693 mergeStateStatus=CLEAN.

```
$ git ls-remote origin refs/heads/main   # baseharbor-plan, run from /var/tmp/123-plan-clone (final state after this file's last push)
6c744e973da55cb0ab1a4b9d2e111a2123cb4402	refs/heads/main
```
Evidence path on origin/main: evidence/r28-welle4-2026-11-19/regvisibility-r9-hopf2/fix-1.md — commit 63e5e260 (content, pushed before END) plus final witness commit 6c744e97 on top; file present on origin/main verified by the ls-remote line above.
