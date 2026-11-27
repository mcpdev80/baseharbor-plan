# Plan PR backlog disposition

## PLAN

1. Read Plan repository guidance and the bounded PR inventory for open Plan PRs #147–#189.
2. For every currently open PR in scope, bind head SHA, ancestry against current main, exact file diff/zero-diff status, and whether its corresponding card/evidence row is present on main.
3. Mark frozen-linked PRs for #136-hop/#161 and #1863-hop/#178 without changing them.
4. Close only individually proven superseded or zero-diff-with-ancestry PRs, each with a supersession comment; leave genuine content gaps open and record the exact missing content.
5. Write the per-PR disposition table here, run render/check if Plan content changes, and commit only this evidence file.
6. Push one branch, open a Plan PR only if main-file content needs publication, wait for exact-head validation, merge normally after ancestry proof, and verify the akte on main.
7. Report the closed/open totals and final main SHA; post the coordinator END status.

## Identity and source attestation

This is a mission-scoped disposition akte and does not modify a single owned task card; owners are recorded per row from each mapped card's current frontmatter when applicable.
Canonical lane identity: `w255-0428-251-demo170codex`.
Git user.name: `w255-0428-251-demo170codex`.
Git user.email: `w255-0428-251-demo170codex@baseharbor.local`.
Commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit ...`.
Pre-push gate: `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`.
Verified Plan remote: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
Exact fetched main base before branch creation: `e06de0fc45479a59272daea0f662e9bb6b058012`.
After the live main ref advanced during the read-only census, unpublished local merge scaffolding was discarded in this isolated clone before the first candidate commit. Main then advanced normally from `83c45f78b588180fb3e7441f0ba6fa575add9691` to `edfa742ea8ca9d3a6d4e14ad689620f507f2655d`. I rebased only my unpublished evidence commit onto that latest base; first candidate commit `e03957ff365362c0d564b50a6e3c5a9bf27e3bee` has canonical author/committer, `origin/main` is its ancestor, and the resulting candidate history contains only this lane's commits. No remote branch was created or rewritten.

## Inventory and disposition

Current inventory was obtained with `gh pr list --repo mcpdev80/baseharbor-plan --state open --json number,headRefOid,headRefName,title,updatedAt,baseRefName`, then each head was rechecked using `git ls-remote origin refs/pull/<N>/head`, `gh pr view --json headRefOid`, a fetch of that pull ref, ancestry tests, the GitHub `pulls/N/files` path list, and exact-path checks against `origin/main`. Final census main was `edfa742ea8ca9d3a6d4e14ad689620f507f2655d`; an immediate recheck confirmed all eight PRs remain open with unchanged API-matched heads and unchanged ancestry, zero-diff, and file counts. No PR head is an ancestor of main, main is not an ancestor of any head, and no PR tree equals main. No PR met the mission's safe-close condition.

| PR | exact head | card/evidence row on main | ancestry / file witness | disposition |
| --- | --- | --- | --- | --- |
| #147 | `3a560adde4cef48bc8ce3c5a577e65e7dd58905e` | 0428-327 task row exists; owner empty, `planned`, `prs=[]`, `evidence=[]`. Reissue akte `evidence/2026-11-27/w339-0428-327-reissue132/akte.md` is absent. | Neither-side ancestry and nonempty tree diff. GitHub lists 548 changed paths; 534 added paths are absent from main, including the named reissue akte. | Leave open: real evidence/content gap. |
| #156 | `607e98e8aebd72b6f1d3cce8b19b2cdc51d3769d` | 0428-344 row exists; owner verbatim `"" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)`, status blocked, PRs #1872/#1871, `evidence=[]`. | Neither-side ancestry and nonempty tree diff. Its sole changed file, `evidence/2026-11-26/w347-0428-344-baseline/akte.md`, is absent from main. | Leave open: missing baseline akte. |
| #158 | `071616a4e2c768932491be4312b962aeed3e85d2` | No 0428-359 task frontmatter row on main. Related main evidence rows do exist at `evidence/w348-0428-359-batchhop/akte.md`, `evidence/w350-0428-359-batchhop2/akte.md`, and `evidence/2026-11-27/w369-0428-359-136hop/disposition.md`. | Neither-side ancestry and nonempty tree diff. GitHub lists 543 changed paths; 530 added paths are absent from main (for example `evidence/2026-11-26/w255-0428-251-284-close/akte.md`). | Leave open: the claimed transport-only candidate has substantial unlanded file content; title alone cannot establish zero diff. |
| #161 | `bcc30d9998aaa4735690e658e722664f0f8349f6` | 0428-359 task frontmatter row absent; associated batch-hop evidence exists on main as above. | Frozen-linked to the explicit 0428-359 / PR #136 hop. Neither-side ancestry, nonempty tree diff, 549 changed paths and 533 added paths absent from main. | Frozen-linked: do not touch. |
| #178 | `f08d1c0f45c2076b689103ec03dfdbf02e4185bb` | 0428-299 task exists; owner empty, blocked, PR #1863, `evidence=[]`. | Frozen-linked to the explicit #1863 hop. Neither-side ancestry and nonempty tree diff; both added files are absent, including `evidence/w362-0428-299-1863hop/akte.md`. | Frozen-linked: do not touch. |
| #182 | `51bcb2fe8b69cbc64b498eec55b09b5055b09eef` | 0428-249 task exists; owner `w362-0428-249-1812rebase`, blocked, PRs #1812/#1837; current evidence links product PR #175 and failure run 45944501306. Candidate 0428-249 akte path exists on main but its blob differs from this PR. | Neither-side ancestry and nonempty tree diff; 36 changed paths, 13 existing paths differ. Two additions absent from main: `evidence/w362-0428-299-1863hop/akte.md` and `w219-0428-271-0428-286-1820hop-plan/evidence/2026-11-25/w219-0428-271-0428-286-1820hop.md`. | Frozen-linked via the explicit #1863-hop artifact; do not touch. Also retains unlanded content. |
| #184 | `1250f02bbf3b98cc8c5ecab992e42924573e5816` | 0428-299 task exists; owner empty, blocked, PR #1863, `evidence=[]`. | Frozen-linked to the 0428-299/#1863 pre-hop thread. Neither-side ancestry and nonempty tree diff; `evidence/2026-11-27/0428-299/w378-0428-299-1863pre.md` is absent from main. | Frozen-linked: do not touch. |
| #189 | `a20abbcf29fc486cb12a93afa413d5aec4d3808a` | 0428-326 task exists; owner verbatim `"" (lane w341 idle-PARKED on external map gate; claim released for board truth, RESUME trigger = pr-gate-map landing)`, blocked, PR #1868, `evidence=[]`. | Neither-side ancestry and nonempty tree diff; 12 changed paths, 11 existing paths differ. `evidence/w382-0428-326-1868pre/akte.md` is absent from main. | Leave open: missing 1868 pre-work akte and changed task content. |

Disposition count: closed 0; open 8 (4 content-gap rows and 4 frozen-linked rows). No comments or close operations were issued.

Exact live remote head witnesses:

```text
3a560adde4cef48bc8ce3c5a577e65e7dd58905e refs/pull/147/head
607e98e8aebd72b6f1d3cce8b19b2cdc51d3769d refs/pull/156/head
071616a4e2c768932491be4312b962aeed3e85d2 refs/pull/158/head
bcc30d9998aaa4735690e658e722664f0f8349f6 refs/pull/161/head
f08d1c0f45c2076b689103ec03dfdbf02e4185bb refs/pull/178/head
51bcb2fe8b69cbc64b498eec55b09b5055b09eef refs/pull/182/head
1250f02bbf3b98cc8c5ecab992e42924573e5816 refs/pull/184/head
a20abbcf29fc486cb12a93afa413d5aec4d3808a refs/pull/189/head
```

## Validation and cleanliness

`python3 scripts/plan.py render && python3 scripts/plan.py check`: 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 existing accepted-dependency warnings. Render regenerated `views/overview.md`, `views/kanban-dashboard.md`, and `views/releases/v0.4.28.md` because latest main changed the unrelated 0428-HV42 timeout task from active to wait; no task file was edited by this disposition.

Docker witness PID 2767166 before work: `docker ps -a` returned only the header and no containers. No containers or compose projects were started.

## END

END DONE — every open PR in the requested range was individually measured; none met the authorized close rule, frozen-linked PRs were left untouched, and all genuine gaps are recorded above.
