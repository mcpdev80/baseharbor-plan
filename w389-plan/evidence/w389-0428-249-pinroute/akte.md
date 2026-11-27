# akte w389-0428-249-pinroute — Demo PIN read-only investigation

Card: 0428-249  · Lane: w389-0428-249-pinroute  · Repo: baseharbor  · PR: #1812 (read-only, NOT changed)
Date: 2026-11-27  · Type: READ-ONLY investigation. No push, no run, no workflow/pin/product/config change.

## 4-Feld w389-0428-249-pinroute

- WAS: investigate where the `BASEHARBOR_PR_DEMO_SOURCE_SHA` demo pin is set and read, which demo commit is the next qualifying pin value after #183, which CI gates consume the pin, and the exact ordered Owner action that unblocks #1812 (head c2dd3ff04, which runs only green behind that pin).
- GEFUNDET: the pin is a GitHub Actions *repository variable* `BASEHARBOR_PR_DEMO_SOURCE_SHA`, referenced only in `.github/workflows/ci.yml` (lines 951, 1140, 1151). It is never read inside either product's Go code and never written inside the demo repo. The currently-live value is `1a3c055cc0eef3f961722f12d843e33f6c1ca43e` (proven by the live run 45944501306 resolving `demo_ref` to exactly that SHA). #183 (demo repo, head d5b44c46c) is still OPEN (mergedAt null, state OPEN); it is not yet merged into demo develop (d5b44c46c is NOT an ancestor of demo develop). #1812's own run 45944501306 at head c2dd3ff04 completed with all 30 jobs success-or-skipped; the sole FAILURE was the aggregate `PR Selected Checks`, caused by `pr_runtime_selected` failing because the podman runtime gate hit "Missing release-gate catalog entry ... register it in scripts/release-requirements.json" (the exact candidate-image bug #1812 fixes) — NOT a demo-pin failure. The pin gate `pr_demo_pin` ran SUCCESS and resolved the demo source to `1a3c055`.
- BEWEIS: run 45944501306 (head c2dd3ff04, branch lane-0428-249-runtime-image-fix) job logs; `gh pr view 183 --repo mcpdev80/baseharbor-demo` (state OPEN); `git ls-remote` witnesses for demo develop/main/#183/#1812; ci.yml lines 946-1173.
- WEITER: Owner executes the ordered sequence in section (d). Lane stops here (read-only mission-scope).

## (a) Where the pin is set and read — file:line both repos

Set:
- GitHub Actions **repository variable** `BASEHARBOR_PR_DEMO_SOURCE_SHA` (repo mcpdev80/baseharbor, environment-scoped). Not stored in any tracked file; verified at runtime by run 45944501306 resolving `demo_ref` to it. The var is a 40-hex commit SHA on repo `mcpdev80/baseharbor-demo`.
- Resolution fallback (when the var is empty) is anonymous `git ls-remote` of demo `main` in ci.yml: line 966 and line 1153.

Read (baseharbor repo ONLY, `.github/workflows/ci.yml`, current HEAD):
- Line 951 — step "Pin immutable Demo source for safe native result reuse" (`pr_demo_pin`/`demo_source` source route): `EXPLICIT_PR_DEMO_SHA: ${{ vars.BASEHARBOR_PR_DEMO_SOURCE_SHA }}`, then line 959-960 uses it, else anonymous main at line 966.
- Line 1140 — job `pr_demo_pin` "PR · Demo Pin" env: `EXPLICIT_PR_DEMO_SHA: ${{ vars.BASEHARBOR_PR_DEMO_SOURCE_SHA }}`.
- Line 1151 — same job's run block: `demo_sha="${{ vars.BASEHARBOR_PR_DEMO_SOURCE_SHA }}"`, falls back to anonymous main at line 1153, clones the exact demo SHA, verifies `test "$(git ... rev-parse HEAD)" = "$demo_sha"` and `test -s .../baseharbor-core.ref`.

Read (demo repo): NONE. `git grep -n BASEHARBOR_PR_DEMO_SOURCE_SHA` across all demo refs, all workflow files on develop, and all ci.yml returns nothing. The demo repo never consumes the var; it only *provides* `baseharbor-core.ref`, which the pin pins.

## (b) Next qualifying pin value after #183 merge

Witnesses (anonymous `git ls-remote`, own persistent zone):
- demo develop = `58ac70679efe5f7e95bd47d602841704fb9ffa67` (matches mission).
- demo main = `2618b3962330509add5bf265522995da2a9034ce` (matches mission).
- demo PR #183 head = `d5b44c46c694c3099408939ec962cd723505003c` (`gh pr view 183 ... --json headRefOid` = same; `mergeable=MERGEABLE; state=OPEN`).
- baseharbor PR #1812 head = `c2dd3ff04e30c73046b4eeecb56f3cab20e56c92` (`gh pr view 1812 ... --json headRefOid` = same; base develop, state OPEN, authored by mcpdev80).

Ancestry facts (remote witnesses):
- `d5b44c46c` is NOT an ancestor of demo develop (verified `git merge-base --is-ancestor` against origin/develop via anonymous clone). #183 is NOT yet merged; it is still open.
- The currently-live resolved value `1a3c055cc0eef3f961722f12d843e33f6c1ca43e` (from run 45944501306) IS reachable from demo develop (4 commits behind tip 58ac70679), commit `1a3c055 test(fixture-consent): exact immutability message match, reject near-misses`, single parent 49328fb, `baseharbor-core.ref` = `087556457195b6472f98959c8df2d930019c33c3`. It is NOT a merge commit, NOT on demo main (2618b3962).

What the #183 merge mechanically delivers:
- Merging #183 (head d5b44c46c) into demo develop fast-forwards develop to include d5b44c46c's `test(demo): fix FINAL_DRAIN_CHUNKS scoping so counter advances (0428-284, PR #183)` and its 4 preceding test commits.
- Both demo develop (58ac70679) and #183 head (d5b44c46c) pin the SAME core ref `087556457195b6472f98959c8df2d930019c33c3` in `baseharbor-core.ref` — so the merge does NOT change the core pin value; it only adds demo test commits on top.
- Therefore the "next qualifying pin" for baseharbor #1812 is the demo develop tip AFTER #183 merges in = the demo develop tip that contains d5b44c46c. Until #183 is merged, demo develop's tip (58ac70679) does not contain d5b44c46c and is a different commit than the post-merge tip. The correct post-merge pin is `git ls-remote demo refs/heads/develop` measured AFTER the #183 merge (the new develop tip that is d5b44c46c's descendant).

Verdict: the mission's cited "demo develop 58ac70679 is the next pin" is not the post-merge tip. The post-merge tip is whichever SHA the merge produces on top of d5b44c46c. `1a3c055` (the live var) is an intermediate demo develop commit, not the merge result. Pin must be set to the post-#183 demo develop tip, then #1812 re-qualified against it.

## (c) Which gates read the pin — workflow file:line + runner role

Only `.github/workflows/ci.yml` reads `BASEHARBOR_PR_DEMO_SOURCE_SHA`. The other named workflows reference the pin ZERO times (verified per-file on develop):

- `.github/workflows/ci.yml:951` — job `pr_demo_pin` / source route (name "PR · Demo Pin"). Runner: `runs-on: ubuntu-latest` (GitHub-hosted shared runner), gated by `if: ... pull_request && draft==false && (runtime|integration|public_contracts|source_pin)==true`. Resolves the immutable Demo source SHA and pins it for safe native result reuse.
- `.github/workflows/ci.yml:1140` and `:1151` — same `pr_demo_pin` job "PR · Demo Pin" step "Verify exact Demo dependency against integration source". Runner: `ubuntu-latest` (GitHub-hosted shared). Clones the exact demo SHA, verifies `baseharbor-core.ref` non-empty and rev-parse == demo_sha.
- NOT read in: `targeted-integration.yml`, `targeted-demo-acceptance.yml`, `supplemental-release-validation.yml`, `podman-acceptance.yml` (grep returned nothing on develop).

Runner role for both consumers: GitHub-hosted shared runners (`ubuntu-latest`). No self-hosted runner builds the pin; no runner is registered/repaired by this investigation.

## (d) Ordered sequence that unblocks #1812 (Owner action, not a lane command)

The chain, in order, is: (1) merge demo PR #183 (head d5b44c46c) into demo develop; (2) set the repo variable `BASEHARBOR_PR_DEMO_SOURCE_SHA` to the new demo develop tip = the post-merge tip that contains d5b44c46c, measured with `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop` after the merge; (3) re-run baseharbor PR #1812 (head c2dd3ff04) so its `pr_demo_pin` and `pr_runtime_selected` gates evaluate against the new pin.

The single Owner sentence that describes the input: "Set repo var BASEHARBOR_PR_DEMO_SOURCE_SHA to `<post-merge demo develop tip>` (the demo develop SHA that contains d5b44c46c), then re-trigger baseharbor PR #1812 (head c2dd3ff04) and let its PR Selected Checks run to completion."

The one line that ties it together for the Owner: #1812 runs only green behind the pin, and #1812's run 45944501306 shows the ONLY failing aggregate was `PR Selected Checks` failing on `pr_runtime_selected` (podman policy/full-destroy) with the log line `::error::Missing release-gate catalog entry for $gate_id; register it in scripts/release-requirements.json` (the candidate-image bug #1812 fixes) — the demo-pin gate itself already ran SUCCESS resolving demo source to `1a3c055`. So the pin gate is not what blocks #1812; the runtime candidate-image catalog entry is. Both must be cleared for #1812 to go green.

## (e) Evidence

- Run 45944501306 (baseharbor PR #1812, head c2dd3ff04, branch lane-0428-249-runtime-image-fix): all 30 jobs success(20)/skipped(10); aggregate `PR Selected Checks` = FAILURE via `pr_runtime_selected` failure; `pr_demo_pin` = SUCCESS, `demo_ref=1a3c055cc0eef3f961722f12d843e33f6c1ca43e`. Job 140326573644 (podman policy) log line: `::error::Missing release-gate catalog entry for $gate_id; register it in scripts/release-requirements.json`.
- demo PR #183: `gh pr view 183 --repo mcpdev80/baseharbor-demo` = state OPEN, mergeCommit null, mergeStateStatus CLEAN, head d5b44c46c, base develop. d5b44c46c NOT ancestor of demo develop.
- demo develop 58ac70679, demo main 2618b3962, baseharbor #1812 head c2dd3ff04 (all via `git ls-remote`, anonymous).
- ci.yml source/targeted pin references at lines 951, 1140, 1151 (current HEAD); no other workflow references the pin.

## END

w389-0428-249-pinroute: DONE (read-only akte; no run, no push to product, no workflow/pin change; Owner sequence documented). candidate witness head c2dd3ff04 (#1812), demo develop 58ac70679, #183 head d5b44c46c, live pin var 1a3c055cc0eef3f961722f12d843e33f6c1ca43e.
