# CODEX-REVIEW — fate of PR #1455

## PLAN

1. Read live remote refs and PR metadata for #1455, #1457, and develop.
2. Compare the complete #1455 commit set and file diff against #1457 and develop ancestry.
3. Identify any residual change and decide whether #1455 is cleanly superseded.
4. Publish this read-only fate review and verify it on baseharbor-plan origin/main.

## Verdict

**ROLLE: REVIEW**
**URTEIL: NICHT SAUBER IN #1457/DEVELOP AUFGEGANGEN — #1455 ENTHÄLT EINEN RESIDUAL-POSTEN.**

PR #1455 is stale and conflicting, but its destroy-data-root change is not in either of the requested replacement ancestries. Do not describe it as fully superseded by the CA/PKCE PR #1457. Do not merge #1455: its current scope is the separate destroy fix, and GitHub reports it conflicting with develop. A close-without-merge is appropriate only after the residual destroy change is explicitly preserved or separately assigned; this review does not close the PR.

### Remote and ancestry proof

- PR #1455 is open, head `9a9630003b1c9913626923adc06ef7d3402e5e34`, base branch develop at PR base snapshot `07ae6c3e91b081a189266ca4b162ba705d4aa78f`, GitHub state `DIRTY` / `CONFLICTING`.
- PR #1457 is open, head `83d175f54ea9aba432d192c87dfe6464e879e0df`, based on `48d6f10ac8a36ab8289f8981acef153c558dd2d7`.
- Live `refs/heads/develop` is `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`.
- `git rev-list --left-right --oneline origin/develop...origin/pr-1455` lists `a2761413` and `9a963000` on the #1455-only side. `git rev-list --left-right --oneline origin/pr-1457...origin/pr-1455` likewise lists both commits on the #1455-only side.
- `git merge-base --is-ancestor 9a9630003b1c9913626923adc06ef7d3402e5e34 origin/develop` exits 1; the same check against `origin/pr-1457` exits 1. Both comparisons have merge base `e39b0004346cdfd082e34ba55d94d24757bbbd27`.
- PR #1455's complete diff against both develop and #1457 is limited to `cmd/baha/runtime_destroy_all.go` and `internal/deployment/target.go` (58 insertions, 11 deletions). Those files are not in the current #1457 PR diff. The #1455 content is therefore not in the ancestry or current diff of either requested replacement.

### Residual change

The two #1455 commits implement owned Core target discovery for full destroy when a target has an installation under the data root but no config entry. `internal/deployment/target.go` adds `ResolveDataRootTarget`, which reads the target's own `runtime/installation.json` and constructs a locally owned resolved target. `cmd/baha/runtime_destroy_all.go` uses that resolver instead of leaving the discovered Core target unresolved and failing closed as “not configured.” The current develop and #1457 snapshots do not contain this resolver or its destroy-path call site.

### Recommended disposition and stop criterion

Do not merge the stale, conflicting #1455 PR. Preserve the destroy-data-root residual as a separate, correctly owned destroy task/PR, or provide a SHA-specific witness of another accepted replacement before closing #1455 without merge. Stop treating #1455 as a duplicate of the CA/PKCE work until that residual is accounted for. No product change, merge, or PR close was performed by this review.

## END

END_DONE 0427-134-review-fate — PR #1455 is not fully superseded: commits `a2761413` and `9a963000` remain outside both develop and PR #1457; the residual adds owned data-root target resolution to full destroy in two files. Preserve/reassign that work before closing the stale conflicting PR without merge.

## Publication witnesses

- Planning remote: `https://github.com/mcpdev80/baseharbor-plan.git`.
- Product refs were read from GitHub; no branch, PR, product file, or workflow was modified.
