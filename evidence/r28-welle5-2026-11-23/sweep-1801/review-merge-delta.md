# PR #1801 post-merge review delta

Role: REVIEW.

## PLAN

- 379. Read the #1801d mission payload and capture its exact role, candidate, scope, verdict, and evidence requirements.
- 380. Reconcile the new mission with the prior #1801 review and verify current GitHub remote state before deciding any action.
- 381. Inspect the exact candidate diff, task contract, prior CI receipt, and any new exact-head run required by the mission.
- 382. Apply only explicitly authorized review or merge actions after all exact-head acceptance criteria pass; otherwise record precise blockers and repair steps.
- 383. Write and validate the required Planning evidence, including remote witnesses, cleanliness, literal verdict, and END line.
- 384. Publish the evidence on Planning origin/main, update this board, and post the required END.

## Live remote and merged candidate

- Product repository remote inspection identified `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)`; all inspected GitHub URLs were for the authorized mcpdev80 account.
- Remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1801/head`:
  - `b41103867e370f6588a396cb08ab0b3013e209ac refs/heads/develop`
  - `ff81c5a17ba0ba6c1f784773302497771ab089d8 refs/pull/1801/head`
- GitHub pull request API reports #1801 closed and merged at 2026-11-23T11:02:54Z. Base was `develop` at `f6ab22b7dc9793ccd2872cb7717402816561c401`; source head was `ff81c5a17ba0ba6c1f784773302497771ab089d8`; merge commit is `b41103867e370f6588a396cb08ab0b3013e209ac`, whose parent is the base SHA.
- The merged diff from the base is additive: 77 insertions, zero deletions, in `cmd/baha/app_edit.go` (+6), `cmd/baha/app_wizard_controller.go` (+17), and `cmd/baha/app_edit_apply_test.go` (+54).

## Scope extension and neutrality

- `cmd/baha/app_wizard_controller.go` adds `selectedKindAtCursor` and `selectedKindSelected`. They only read the visible needs/cursor and the selected map; they do not modify selection or provider state. `app_edit.go` uses these reads to print the intended selected/deselected acknowledgement after a Space toggle.
- `cmd/baha/app_edit_apply_test.go` adds only `TestReview918SpaceToggleAcknowledgesOnScreen`; it does not alter existing test behavior. Its fixture is in-memory and has no skip path.
- These two additional files are functionally neutral to selection, consent, provider, and fail-closed semantics. Their only contribution is the acknowledgement read path and its regression coverage. No revert is needed, and no owner-scope conflict remains once the scope extension is recorded.
- Card 0428-257 now documents all three paths in its Scope section and links this delta evidence. The lifecycle status remains `review`; this mission asked for the scope correction record and review verdict, not a Planning status transition.
- There are no changes to `.github/**`, consent rules, fail-closed behavior, or provider selection.

## Test-to-CI receipt chain

- The added test is `TestReview918SpaceToggleAcknowledgesOnScreen` in package `./cmd/baha`, file `cmd/baha/app_edit_apply_test.go`.
- Package route: `scripts/pr-draft-go-packages.py` maps the changed `cmd/baha` Go path to `./cmd/baha`. The CI shard selector then routes that package into CLI shards; the exact job log for cli-3 shows `python3 scripts/pr-go-unit-shard.py --mode "$SHARD"` and `SHARD: cli-3`.
- Test assignment is deterministic. At the candidate version, `scripts/pr-go-unit-shard.py` discovers CLI test names and assigns each name by the first eight SHA-256 bytes modulo four. `TestReview918SpaceToggleAcknowledgesOnScreen` maps to shard cli-3. The test source and `app_edit_apply_test.go` blob are unchanged at candidate `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`, hopped head `ff81c5a17ba0ba6c1f784773302497771ab089d8`, and merge `b41103867e370f6588a396cb08ab0b3013e209ac`; the file blob is `873501b9fe07a25f389a185e4f16c7e2094f5e22` at all three.
- Actual package receipt: run 45152943243, event `pull_request`, candidate head `c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`, job 137618621308 (`PR · Draft Go · cli-3`), terminal success. Job environment recorded `BASE_SHA=304b3ad1d88647377ea647d0d94174bfc9298e14`, `HEAD_SHA=c3677dfa19f4aa0d0bc7ceccb51a6929b84f400c`, `SHARD=cli-3`. Log receipt: `PASS cli-3: 438 passed / 16 intentionally skipped / 454 discovered; CLI inventory total=1872`. The shard runner executes its selected test names with `go test ./cmd/baha -count=1 -json -run <selected-name-regex>` and fails on missing, incomplete, or failed selected tests. The new test is assigned to this shard and its fixture/body does not skip.
- The mission explicitly accepts a package receipt with documented test-to-shard mapping, analogous to the cited #1606 review standard. This evidence supplies that mapping and terminal package receipt; it does not claim the log printed an individual named PASS line.
- Final ready-run evidence: pull_request run 45157306258 at `ff81c5a17ba0ba6c1f784773302497771ab089d8` completed success. `PR · Trusted Plan`, `PR · Validation · wizard-app-edit-tests`, both selected Docker runtime jobs, and terminal `PR Selected Checks` job 137645497479 succeeded. That run skipped Go unit shards after the current-base hop; its `wizard-app-edit-tests` validation uses the narrower `^TestGuided` selector and is not the package receipt cited above. The code/test blob identity carries the earlier cli-3 package receipt to the merged tree under the mission's package-receipt rule.
- Post-merge push workflows for commit b41103867 ran Docker Core (45161575342) and Podman Core (45161575371) successfully. Their native workload jobs were skipped by selection and are not used as unit-test evidence.

## Planning and repository rules

- Evidence repository is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; verified remote line before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Product repository was read-only during this delta review. No new local tests or containers were run. No PR mutation or merge action occurred; #1801 was already merged before this mission.
- `python3 scripts/plan.py render` updated the card preview. `python3 scripts/plan.py check` reported 698 tasks, 7 epics, 13 releases, 24 decisions; 0 errors and 10 pre-existing dependency warnings.
- Evidence contains plain bullets, no Markdown checkbox lines.

## cleanliness

- Before: PID 2049847; `docker ps -a` returned only the header, no containers.
- After: PID 2054546; `docker ps -a` returned only the header, no containers. No Docker or Podman workloads were started.

## Verdict

VERDICT: APPROVE — the scope-additional files are additive and neutral to underlying selection/consent semantics; no revert is required. The package-shard receipt and mapping satisfy the mission's stated package-receipt rule.

END DONE codex-rev-1747: APPROVE #1801 post-merge delta; merged commit b41103867e370f6588a396cb08ab0b3013e209ac; no revert required.
