# ROLLE: REVIEW — POST-MERGE AUDIT PR #1790

Session: codex-rev-1747; model: GPT-6-Luna; audit time: 2026-11-23 00:10 UTC.
Candidate: merged develop commit `c6a7138ce2bf7de88f45f2a68e5168c835601a16` (PR #1790 head `b103495b6ee53ee61b4f9d4ddd85400ca12b2367`; exact run 45086017941 success).

## PLAN

1. Read the post-merge audit contract and create the numbered plan on the live board and in this evidence file.
2. Independently fetch the merged catalog and compare the three rows byte-for-byte with the required model; verify there is no package-root row or changed/deleted existing row and release remains `v0.4.27`.
3. Trace longest-path resolution and focused-gate intersection for each source; determine whether base catalog resolution admits #1753 and #1765 paths.
4. Check whether the underscore ID variant recorded by #1765 is handled without duplicate catalog entries.
5. Record commands, extracts, verdict and any precise follow-up recipe; finish without pushing or merging.

## Remote and diff witnesses

Read-only product remote resolution (`git -C baseharbor remote -v`) showed `lane-origin`, `origin`, and `upstream` all resolve to `https://github.com/mcpdev80/baseharbor.git`; the bare URL line was also that same GitHub URL. No fetch/push or product checkout mutation was needed for this audit; catalog and resolver inputs were fetched from the exact GitHub commit with `gh api`.

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1790/head` output:

```text
c6a7138ce2bf7de88f45f2a68e5168c835601a16	refs/heads/develop
b103495b6ee53ee61b4f9d4ddd85400ca12b2367	refs/pull/1790/head
```

GitHub PR files API for #1790 reports one file, `scripts/pr-gate-coverage.json`, status modified, 27 additions, 0 deletions. Comparison of JSON fetched at base `ef73b50b6aee3dea8d4badf347c264daefa3d064`, PR head, and merge commit confirms:

- release is `v0.4.27` at all three refs;
- component count is 215 at base and 218 at PR head and merge;
- added paths are exactly `cmd/baha/control_plane_single_native_ci_test.go`, `internal/operatorauth/local_runtime.go`, and `internal/operatorauth/local_runtime_test.go`;
- deleted paths: none; changed existing component rows: none;
- merged catalog equals the PR-head catalog;
- package-root rows for `cmd/baha` and `internal/operatorauth`: none.

Required pattern row at merge commit:

```json
{"id":"internal.operatorauth.test.operator.go","path":"internal/operatorauth/test_operator.go","runtime_specific":true,"surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}
```

Each of the three added rows, after excluding its path-specific `id` and `path`, is byte-for-byte equal to that model’s remaining fields (`runtime_specific: true`; the same two surfaces). Thus there are precisely three pure component additions with the requested row shape.

## Resolver trace

The resolver source was fetched from the exact merged commit. In `scripts/validate-pr-gate-coverage.py`, lines 29–41 first choose exact component-path owners; package-prefix fallback is used only if there is no exact component row; then the longest matching path determines the owning surfaces. Lines 42–45 retain only `gates` whose `selection_scope` is `focused` (default included) and whose `covers` intersects the row’s surfaces. Lines 51–60 preserve both runtime siblings when the longest owner has `runtime_specific: true`.

I loaded that exact-revision resolver and catalog and called `resolve_covered_gates([path], catalog)` separately for every path. Results:

- `internal/operatorauth/local_runtime.go`: row count 1; covered `atomic/docker/data-capabilities`, `atomic/podman/data-capabilities`; unowned `[]`.
- `internal/operatorauth/local_runtime_test.go`: row count 1; covered `atomic/docker/data-capabilities`, `atomic/podman/data-capabilities`; unowned `[]`.
- `cmd/baha/control_plane_single_native_ci_test.go`: row count 1; covered `atomic/docker/data-capabilities`, `atomic/podman/data-capabilities`; unowned `[]`.

Both focused runtime gate records explicitly cover their corresponding `source.gate.atomic.{docker,podman}.data.capabilities` surface. Each new component is an exact-path match, so no broader package row can shadow it. This confirms Trusted Plan’s base-side ownership resolution admits the two #1753 paths and the #1765 path.

## #1765 underscore-ID check

The #1765 evidence records a prior candidate row ID `source.cmd_baha_control_plane_single_native_ci_test_go`, generated in the fail-loud error by `unresolved_source_error` (resolver lines 75–84). At the merged base, the single row for this path has ID `cmd.baha.control_plane_single_native_ci_test.go`. The admission resolver does not resolve coverage by ID: it finds the exact path at lines 29–31 and intersects the row’s surfaces with focused gate `covers` at lines 39–45. Running the exact path therefore resolves both gates with no unowned path regardless of that prior candidate ID spelling.

The underscore-form ID is not present as a second row, and exactly one component row exists for the path. Adding an ID alias row would duplicate the same component path; the catalog validator rejects duplicate component paths (`validate-pr-gate-coverage.py` lines 172–192). No alias or follow-up change is needed for base-side Trusted Plan admission.

## Verdict

VERDICT: CONFORMANT. The merged diff is exactly three pure additions, matches the requested component-row model, leaves release `v0.4.27` and all existing rows unchanged, has no package-root entry, and routes each exact path through longest-path ownership and focused-surface intersection to both atomic data-capabilities runtime gates. The #1765 underscore ID is an error-message/candidate spelling, not a key used by this admission resolver; the merged path row admits it without a duplicate entry.

No follow-up finding or correction is indicated by this audit. This was read-only against product state. No push, merge, workflow dispatch, CI rerun, or container activity was performed.

END_DONE codex-rev-1747: POST-MERGE-AUDIT #1790 CONFORMANT at c6a7138ce2bf7de88f45f2a68e5168c835601a16; exact-path resolver admits all three paths and underscore-ID spelling requires no duplicate.
