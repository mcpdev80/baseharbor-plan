# w81-0428-249-1812gates — card 0428-249 / PR #1812 gate chain step 1

Lane: w81-0428-249-1812gates. Mission: coordinator/missions/w81-0428-249-1812gates.txt.
Date: 2026-11-24. Status: BLOCKED pending coordinator decision (see END line at bottom).

## PLAN

1. Fetch origin develop, confirm 46d3dccc; locate branch lane-0428-249-runtime-image-fix — done.
2. Rebase lane-0428-249-runtime-image-fix onto origin/develop 46d3dccc, preserving the owner +20 delta byte-for-byte, develop wins on superseded files — done, no manual merge needed (single owner commit replayed cleanly).
3. Verify diff vs develop is only .github/workflows/pre-release-runtime-suite.yml — done (exact).
4. Evidence witnesses (base attestation, remotes, ancestry, log) — done below.
5. Force-push rebased branch, ls-remote delivery witness — done (PR head now 475902075).
6. Trigger/monitor Docker light-runtime gates on exact PR head — BLOCKED: no lane-triggerable route exists (finding below).
7. Trigger/monitor Podman light-runtime gates on exact PR head — BLOCKED: same finding.
8. Record gate outcomes + operator-auth admission — BLOCKED.
9. Push evidence, END post — this file.

## Remote and worktree witnesses

`git -C workers/w81-0428-249-1812gates-wt remote -v` (all three remotes resolve to the GitHub URL; no filesystem-origin in this worktree):

```
lane-origin https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin https://github.com/mcpdev80/baseharbor.git (push)
origin      https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin      https://github.com/mcpdev80/baseharbor.git (push)
upstream    https://github.com/mcpdev80/baseharbor.git (fetch)
upstream    https://github.com/mcpdev80/baseharbor.git (push)
```

The lane worktree is `/home/marcel/dev/baseharbor-ecosystem/workers/w81-0428-249-1812gates-wt`, a `git worktree` of the shared card-249 checkout `workers/0428-249-tagfix-wt` (the card's own branch home); no second clone was made.

## Base attestation

- Base ref SHA (fetched fresh, mission confirmed): `git ls-remote lane-origin refs/heads/develop` → `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`. Confirms the mission's "develop = 46d3dccc".
- Pre-rebase PR head / branch head (both equal): `f2433d7fd0fc969d9ce01033a59b0d424c9739da` (ls-remote of refs/heads/lane-0428-249-runtime-image-fix and refs/pull/1812/head).
- Old base was merge-base `05ef48536` (develop before #1825). The branch carried exactly one commit, the owner's `f2433d7fd` "ci: reload candidate image before runtime publish" (Codex <codex@openai.com>, +20 lines in .github/workflows/pre-release-runtime-suite.yml only).

## Rebase and byte-for-byte preservation proof

Command: `git rebase --onto lane-origin/develop 05ef48536 lane-0428-249-runtime-image-fix`. Result HEAD: `47590207518ce9501f1b1bbb115d72d64a206d14`.

- `git merge-base --is-ancestor lane-origin/develop HEAD` → true (46d3dccc is an ancestor of 475902075).
- `git log --oneline lane-origin/develop..HEAD` → exactly one line: `475902075 ci: reload candidate image before runtime publish` (no foreign commits carried).
- `git diff --name-only lane-origin/develop HEAD` → exactly one file: `.github/workflows/pre-release-runtime-suite.yml` (mission check passes; all superseded files — pre-release.yml, scripts/pr-gate-coverage.json, operatorauth/* — take develop's version automatically via the rebase).
- Byte-for-byte: `git diff f2433d7fd HEAD -- .github/workflows/pre-release-runtime-suite.yml` → empty (0 lines). Independent replay proof: applying the saved `git format-patch` delta of f2433d7fd to develop's own copy of the file reproduces HEAD's copy identically ("BYTE-IDENTICAL to develop+delta").

## Push and delivery witness

`git push --force-with-lease lane-origin lane-0428-249-runtime-image-fix` → `+ f2433d7fd...475902075 (forced update)`.

Delivery (ls-remote after push):

```
47590207518ce9501f1b1bbb115d72d64a206d14 refs/heads/lane-0428-249-runtime-image-fix
47590207518ce9501f1b1bbb115d72d64a206d14 refs/pull/1812/head
```

PR #1812: OPEN, base develop, not draft, head 47590207518ce9501f1b1bbb115d72d64a206d14.

## PR-triggered CI on the exact head 475902075

Run 45397265257 (CI · Source & Quality, event pull_request, head 475902075). Terminal aggregate observed:

- `PR Selected Checks` → completed/success.
- All base-selected required jobs either success (Workflow policy, Source format, Native gate plan, Trusted Plan, Candidate-added checks advisory, Validation checks, Focused Python) or skipped — including `PR · Selected Runtime` = skipped, exactly as the mission anticipated ("as seen before").

## Gate route finding (why step 2 stops here)

The mission's fallback ("prepare the two workflow_dispatch gate runs") does not exist for this chain in a form a lane may invoke:

1. `Atomic Acceptance Gate` (.github/workflows/pre-release-runtime-suite.yml, workflow id 371960202) has **no `on:` block at all** (file lines 1–4: name/permissions/jobs only). It is reusable-only (called by ci.yml:1431, pre-release.yml:697/726/755/804/833, targeted-demo-acceptance.yml:191). `gh workflow run` cannot dispatch it — confirmed: the workflow's runs list is empty.
2. The only route that executes the 14 light runtime gates (7 Docker + 7 Podman) is `Pre-Release · v0.4.27` (pre-release.yml, workflow id 362658451) via **workflow_dispatch with owner credentials**, and it needs tag/candidate_sha/demo_ref inputs (pre-release.yml lines 2150–2178). Per this mission's own scope rules ("workflow files .github/** belong to the Owner — never … trigger workflow_dispatch") that dispatch is the owner's step. The prior owner dispatch 45385372243 (2026-11-24T11:34Z, candidate f2433d7fd, pre-rebase) is exactly the run whose evidence this chain must regenerate.
3. A run numbered 341, `Pre-Release · v0.4.27`, workflow_dispatch, head_sha 47590207518... (the exact new PR head), appeared at 12:53:22Z. This lane did **not** start it (the lane issued zero workflow_dispatch calls in this session; its last push was ~12:47Z). It was actor mcpdev80, and it was cancelled ~12:57Z before any gate executed — the cancellation arrived while only `Source · Candidate and Gate Plan` and `Release · Candidate Artifact` had finished. Recording it here as STATE so the owner can re-dispatch it deliberately; the two gate run ids the owner asked for therefore do not exist yet.

## Operator-auth admission STATE (why gates were red on old candidate f2433d7fd, expected green on 475902075)

From run 45385372243 (old pre-rebase head) job logs (e.g. job 138418584024 `Light · podman · guided`, 138418584692 `Light · docker · guided`): all 14 light gates failed with exactly:

```
Error
  Managed-environment machine operations require an authenticated BaseHarbor operator.
Resolution
  authenticate the BaseHarbor operator
```

Cause: `Candidate · Runtime Image` on f2433d7fd ran pre-release.yml whose line 505 built `baha-ci-operator-testonly` **without** `-tags=baseharbor_ci_operator_testonly`; the suite (pre-release-runtime-suite.yml "Run runtime gate", env `GOFLAGS: -tags=baseharbor_ci_operator_testonly`, `testonly version | grep -F "$CANDIDATE_SHA"`, `BASEHARBOR_PREBUILT_BINARY="$testonly"`) then executed a non-admitting binary. #1825 (merged as develop 46d3dccc1) adds the tag at pre-release.yml:505 plus the `go version -m` build-settings proof. Rebased head 475902075 carries develop's pre-release.yml, so dispatching Pre-Release on it resolves the mission's premise ("now that the tag binary is present"). Note: the suite itself (reusable workflow) is identical between develop and this head except the owner's +20 reload delta — see diff witnesses above.

## cleanliness

- No containers/networks/volumes were created by this lane: all execution happened on GitHub-hosted runners; nothing ran locally on the coordinator host (no `go test`, no docker/podman). The lane worktree under workers/ holds only the rebased branch (no untracked product edits).
- Planning-repo note: the shared baseharbor-plan checkout had a parallel lane's uncommitted edits (card 0428-278 task + generated views); this lane did NOT touch or commit them. My evidence commit landed on origin/main (24ce334d2) via a temporary worktree off origin/main, which was then removed (git worktree remove). Local main was fast-forwarded to origin/main; a stray backup branch was deleted.
- Side effects on remotes: branch force-push (witnessed above); cancel request for run 45397880292 (an owner-dispatched v0.4.27 run on the exact new head 475902075 that appeared at 12:53Z and was already being cancelled by its dispatcher; this lane's request confirmed terminal state `{"conclusion":"cancelled","status":"completed"}` before any gate executed). The owner must dispatch a fresh run.

## Handoff / decision needed from coordinator

The work of this mission that a lane can do (steps 1 + branch delivery) is complete and verified on exact head `47590207518ce9501f1b1bbb115d72d64a206d14`. What remains (the two gate runs) is owner-only under the dispatch rules above.

- QUESTION (answered by this block, posted to coordinator): exact owner command — dispatch workflow `Release · Pre-Release Validation` (.github/workflows/pre-release.yml, id 362658451) with `tag=v0.4.27`, `ref=47590207518ce9501f1b1bbb115d72d64a206d14` (or the branch), `demo_ref=` the pinned v0.4.27 demo SHA (docs/releases/v0.4.27.demo-ref per pre-release.yml:175), develop_sha optional. Then this lane (or a follow-up) can monitor both 7-gate families to terminal on that run and record run id + per-gate outcomes + operator-auth admission. Run 45397880292 was cancelled before gates started; a fresh dispatch is required.

END_BLOCKED w81-0428-249-1812gates: rebased PR #1812 head 47590207518ce9501f1b1bbb115d72d64a206d14 delivered+verified (PR checks green, Selected Runtime skipped as expected); gate dispatch is owner-only per finding — needs the Pre-Release v0.4.27 workflow_dispatch on this head (prior run 45397880292 cancelled before gates).
