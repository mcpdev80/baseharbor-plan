# CODEX-REVIEW: PR #1753 exact-head review

## PLAN

1. Read mission and record the review plan.
2. Verify repository policy, real GitHub remote, exact base/head, ancestry, authorship, and commit scope.
3. Inspect source diff and exact PR CI run evidence without local tests.
4. Publish the SHA-exact content verdict and evidence.

## Scope and refs

- Role: CODEX-REVIEW; PR #1753, card 0428-227.
- PR state at review: open, ready for review, mergeable; author `mcpdev80`.
- Exact base: `develop` at `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7`.
- Exact head: `91f4e38795a2657d50228c569a684fcb77da031c` (`refs/pull/1753/head`).
- Fresh GitHub remote witness: `8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 refs/heads/develop`; `91f4e38795a2657d50228c569a684fcb77da031c refs/pull/1753/head`.
- `git remote -v` in the BaseHarbor checkout showed `lane-origin`, `origin`, and `upstream` all resolve to `https://github.com/mcpdev80/baseharbor.git`; fetches used `lane-origin` only.
- `git merge-base --is-ancestor 8b9a8f50645db1dbaad4a5e1f2140930436d3ea7 91f4e38795a2657d50228c569a684fcb77da031c` exited 0.
- `git diff 8b9a8f50645db1dbaad4a5e1f2140930436d3ea7...91f4e38795a2657d50228c569a684fcb77da031c --name-only`:
  - `cmd/baha/ci_integration_operator_enabled.go`
  - `cmd/baha/ci_integration_operator_enabled_test.go`
- `git log --oneline 8b9a8f50645db1dbaad4a5e1f2140930436d3ea7..91f4e38795a2657d50228c569a684fcb77da031c`:
  - `91f4e3879 Merge commit '8b9a8f50645db1dbaad4a5e1f2140930436d3ea7' into HEAD`
  - `71deb610a Merge commit '6209874428f08dc3e90d6e29a42b30683ce9932a' into HEAD`
  - `03ef125e6 fix(0428-227): admit canonical footprint show on data-capabilities gate`
- The feature commit has author and committer `0428-227-footprintgate <0428-227-footprintgate@users.noreply.github.com>`; they match. The two sync merges are authored and committed by `0428-061-sourcepull <0428-061@baseharbor.local>`. No author/committer rewrite was observed. The sync merge parents are the assigned base and its prior develop ancestor; no unrelated feature commit appears in the base-to-head diff.

## Content review

- `cmd/baha/ci_integration_operator_enabled.go:138-147` admits the footprint probe only when the selected gate is exactly `data-capabilities`, the managed-workload predicate has not already matched, and the argument predicate matches. The fail-closed rejection at `:189-190` remains intact.
- `:242-249` reuses the existing exact argument matcher: `app footprint show -o json` (arguments after the root command). It does not accept `--json`, omitted output mode, a positional application name, or extra arguments.
- `cmd/baha/ci_integration_operator_enabled_test.go:352-419` adds positive coverage for the canonical command on `data-capabilities`, negative cases for noncanonical/unrelated commands, preserves the guided allowance, and rejects the command on lifecycle. Existing behavior is asserted; no existing test was weakened or removed in the diff.
- Review found no second content defect. The product diff is narrowly the requested command exception and its policy regression test.

## CI and gate evidence

- Exact run: [44978381512](https://github.com/mcpdev80/baseharbor/actions/runs/44978381512), completed with conclusion `success`, event `pull_request`, head `91f4e38795a2657d50228c569a684fcb77da031c`.
- `PR Selected Checks` completed `success` for that exact head.
- `PR · Go unit · cli-3` completed `success`; its log reports `426 passed / 16 intentionally skipped / 442 discovered; CLI inventory total=1843`. `PR · Validation · go-build`, `go-vet`, and `cli-gofmt` also completed `success`. No local test was run, per mission.
- The native gate plan job itself completed `success`; its log shows selection is computed from changed paths. The actual `PR · Native · ${{ matrix.id }}` matrix was `skipped`, and `PR · Selected Runtime` was `skipped` for this exact head. Thus the terminal aggregate success does not establish execution of the data-capabilities Docker/Podman runtime gates.
- At the exact base, `scripts/pr-gate-plan.py:172-175` maps `app_edit` paths to data-capabilities, while `:180` lists `app_footprint_show.go` with an empty gate set; the changed `ci_integration_operator_enabled.go` paths have no data-capabilities routing entry. `scripts/pre-release-runtime-impact.json:30-31` routes `app_machine_adapters.go` and its test to data-capabilities but does not route the changed integration operator files. This is the separately tracked missing gate admission (0428-228), not a defect in this PR’s narrowly scoped content.

## Verdict

VERDICT: APPROVE (content) / MERGE: BLOCKED-BY-0428-228

Merge remains blocked until the separate gate-admission work makes the real data-capabilities native/runtime gate reachable and that required gate passes. Do not treat skipped runtime jobs as a pass. This verdict is for the exact reviewed head only.

## repo-rule compliance

- Read-only review of the product repository; no product files changed, no local tests run, and no PR state/comment/rerun/merge action taken.
- The planning repository used for evidence is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git -C ... remote -v` reported `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `(push)`.
- Planning `main` was fetched before editing; local `main` matched the freshly fetched `origin/main` at `77363dba52c276d24abff5901727ea827a41b8ba`. Only this evidence file is staged for publication; unrelated untracked evidence files are preserved.
- Native todowrite is not exposed as a direct session tool, so that optional leg was skipped. The required board and evidence plans were recorded.

## END codex-rev2-1736 DONE

END codex-rev2-1736 DONE — content approved, merge blocked by 0428-228; candidate `91f4e38795a2657d50228c569a684fcb77da031c`.

## Published-path witness

Exact output of the required fetch and remote tree lookup:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch            main       -> FETCH_HEAD
evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-head91f4e38795a.md
```
