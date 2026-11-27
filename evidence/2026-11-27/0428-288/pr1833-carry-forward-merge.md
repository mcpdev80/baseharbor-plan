# PR #1833 exact-head carry-forward and merge disposition

## Pre-merge disposition

ACCEPT — the content review at the accepted predecessor `ae49d2838d1a71c3a6e96440dc02d3a37a818b6d` carries forward to final head `12c3531c90d88b7e5f19d023d00f851885517386` because the complete three-file diff is byte-identical and the fresh exact-head Hosted run succeeded.

| File | Blob at accepted head ae49d283 | Blob at final head 12c3531c | Result |
| --- | --- | --- | --- |
| `internal/application/manifest_validation.go` | `7fa7a175ee19c01e1fac1999aeafe905740bf0fa` | `7fa7a175ee19c01e1fac1999aeafe905740bf0fa` | identical |
| `internal/application/workload.go` | `2287c2e9a4c7305389f48480f1734fa44cb98da1` | `2287c2e9a4c7305389f48480f1734fa44cb98da1` | identical |
| `internal/application/workload_test.go` | `f43f886c2037fae93d7f7ed74d7fee3f0ac3d00b` | `f43f886c2037fae93d7f7ed74d7fee3f0ac3d00b` | identical |

The pull request file list contains exactly these three paths. The updated head is an ordinary forward merge onto current develop: GitHub compare reports base `6d237ccdf3a5db19c5814ad5b76d01be6c38c35c` as merge base, ahead 12, behind 0, status `ahead`.

## Hosted evidence

- Run `45920639113`, attempt 1, `pull_request`, SUCCESS on accepted head `ae49d2838d1a71c3a6e96440dc02d3a37a818b6d`.
- Run `45924207053`, attempt 1, `pull_request`, SUCCESS on exact final head `12c3531c90d88b7e5f19d023d00f851885517386`.
- Final run census: 36 jobs, 19 SUCCESS, 17 SKIPPED, zero failed or pending. Both selected data-capabilities runtime gates executed successfully: Docker and rootless Podman. `PR Selected Checks`, `PR · Exact Candidate`, Trusted Plan, source format, focused Python, Go shards, vet, and build all succeeded.
- PR #1833 was OPEN, CLEAN/MERGEABLE, base `develop`, exact head `12c3531c90d88b7e5f19d023d00f851885517386` at review time.

The earlier independent content review covered the card 0428-288 contract: logical-ID to raw-key mapping, fail-closed collision handling, and the materialization regression, with consent/auth unchanged. Blob equality and exact-head Hosted evidence establish that this reviewed content is unchanged on the final candidate.

## Merge procedure and post-merge receipt

Before merge, post the PR comment `ROLLE: MERGE` with both run IDs, the exact final head, the 19/17 census, and the three-file blob-equality table. Merge #1833 using the repository's squash-only method, without bypass or force. Then record the old and new develop SHAs, UTC merge time, resulting merge commit, and post-merge runtime workflow IDs/conclusions here.

## PLAN

1. Verify PR head, clean merge state, exact-head run, job census, three file blobs, and current develop ancestry.
2. Publish the accepted carry-forward and exact-head evidence before the merge.
3. Post the `ROLLE: MERGE` comment, merge by squash, and record develop before/after plus post-merge checks.

## Provenance and identity

Card owner verbatim from 0428-288 frontmatter: `w147-0428-288-pr1833-fix`. Executing reviewer lane and commit author/committer: `w255-0428-251-demo170codex`. Planned commit invocation: `git -c user.name="w255-0428-251-demo170codex" -c user.email="w255-0428-251-demo170codex@baseharbor.local" commit -m "evidence(0428-288): PR 1833 exact-head merge"`. Identity gate: `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`.

Plan remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`. Plan main base at akte creation: `f25e06380b1be1e55d6ad6223ec7a635694facbd`; confirm this exact SHA is an ancestor of the review commit before publication.

Publication-base update: Plan main advanced from the akte-creation tip `f25e06380b1be1e55d6ad6223ec7a635694facbd` to `6d4cd06caa85d48086c442142a659e1046f3f9d7` before commit. The publication branch fast-forwarded to that exact live tip; the akte-creation tip remains an ancestor. No unrelated working-tree changes are staged.
