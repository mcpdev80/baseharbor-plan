# w340-0428-327-aktefix-r2: akte reissue, supersedes #132

Evidence-only reissue of the H-V46 collectable-orphan census for card 0428-327 (`t-20261126-hunt46-collectable-orphans-reserved-namespace`), replacing the contaminated PR #132 (`w322-hunt46-orphans`). This akte supersedes #132. No product changes, no card edit, no merge, no closing of #132 (coordinator routes after w267 content review, per mission STOPS).

## PLAN

- Establish identity gate (author AND committer == w340-0428-327-reissue132) in an isolated plan worktree cut from LIVE origin/main.
- Recreate the akte from sources only: card 0428-327 current main text, w255 HOLD verdict, plan #132 HOLD verdict.
- Reconcile the census conclusion with the live card finding (the contaminated "no leak" conclusion).
- Validate `python3 scripts/plan.py check` -> 0 errors.
- One ordinary commit, push branch, create PR, watch exact-head Hosted Plan validate to terminal.

## Identity gate

Local repo config in the plan checkout carried a foreign lane identity; cleared and set per-lane. Effective author AND committer (fresh worktree, before any commit):

- `git var GIT_AUTHOR_IDENT`: `w340-0428-327-reissue132 <w340-0428-327-reissue132@baseharbor.local>`
- `git var GIT_COMMITTER_IDENT`: `w340-0428-327-reissue132 <w340-0428-327-reissue132@baseharbor.local>`
- `git config --show-origin --get user.name`: `file:....git/config	w340-0428-327-reissue132`
- `git config --show-origin --get user.email`: `file:....git/config	w340-0428-327-reissue132@baseharbor.local`

Branch cut: `w340-0428-327-aktefix-r2` from LIVE origin/main tip `3d31d1a4ac4d9efa33263995d76a6efaf940c258`. Provenance: `git merge-base --is-ancestor 3d31d1a4a HEAD` => ancestor confirmed; `git log 3d31d1a4a..HEAD` empty before this commit (only this lane's commits will appear). This is a clean reissue: no object copied from, no cherry-pick of, and no push onto the READ-ONLY contaminated branch `w322-hunt46-orphans` (orphan heads `9629d6e60882ca9e6e3e39185fb3541027d22b75`, `fe79bb3c03bfe45a4dbc6c77afe91db5d5d686eb` and commit `8d9c79c472f1c9b0421375b886a62735005e907e` are never touched).

## Sources

1. Card 0428-327, current main text `tasks/t-20261126-hunt46-collectable-orphans-reserved-namespace.md` (fetches from LIVE `origin/main`, sha `3d31d1a4a`). Task section line 73: "BF-46-3 LIVE (proven by repro at intake). `CollectableOrphans` (internal/deployment/deployment_list.go:185) enumerates each direct child directory of `deployments/`... current code only avoids listing it by relying on the read of a nonexistent `never-delivered/deployment.json` to bail. If the subtree ever contains a `deployment.json` whose embedded `DeploymentID=='never-delivered'` and `Target==target`... the guard attributes the reserved dir as a collectable orphan UUID." Acceptance (lines 56-58): `CollectableOrphans` must explicitly skip the reserved `never-delivered` subdirectory regardless of contents.
2. w255 REVIEW verdict, gh comment `7197905382`: authorship HOLD on exact head `fe79bb3c` + correction `9629d6e6`. Forward recovery: "publish an akte-only reissue from a fresh clean branch under the executing lane's correct canonical identity (w335-0428-318-lowpair); do not rewrite or cherry-pick these commits." (This lane reissues under its OWN canonical identity w340-0428-327-reissue132.)
3. plan #132 REVIEW verdict, gh comment `7197353979`: content HOLD on head `8d9c79c472f1c9b0421375b886a62735005e907e`. The original akte concluded "NO PRODUCT LEAK FOUND IN RESERVED-NAMESPACE ORPHAN SURFACE" and classified `CollectableOrphans` as "safely guarded by DeploymentID==folder and Target matching", which conflicts with the live card finding: the crafted `never-delivered/deployment.json` with `DeploymentID=="never-delivered"` and matching Target was reproduced as a collectable orphan. This is an evidence-content issue, not a request for product edits.

## Census: collectable-orphan / garbage-routine surface (0428-327, BF-46-3)

Scope: collectable-orphan and garbage-routine readers that touch objects in the reserved `never-delivered` namespace under `deployments/`, and objects carrying the reserved `baseharbor-internal-`/`__baseharbor_...` markers, per the H-V46 hunt.

Row for BF-46-3 (this card's seam):

- Reader: `CollectableOrphans` (product source `internal/deployment/deployment_list.go`, referenced in card at line 185, enumerate line 189 `deploymentID := entry.Name()`).
- Surface: each direct child directory of `deployments/` is enumerated as a would-be deployment UUID.
- Reserved namespace: `never-delivered/` is a direct child of `deployments/`, so it is enumerated.
- Current guard state (main `3d31d1a4a`): the reader avoids listing `never-delivered/` only by relying on the read of a nonexistent `never-delivered/deployment.json` bailing early. There is NO explicit reservation skip for the namespace.
- Reproduction (card Task line 73; intake w189 proven): a crafted `never-delivered/deployment.json` with `DeploymentID=="never-delivered"` and `Target==target` is returned by `CollectableOrphans` as a collectable orphan (FAIL at intake w189, test then removed). This is a LIVE finding, not a hypothesis.
- Consequence: the reserved namespace is not fail-closed against a synthetic in-namespace record; an owner-verified exclusion cannot be trusted to exclude it.

Census verdict for BF-46-3: NOT safely guarded. The reserved `never-delivered` namespace is NOT excluded by an explicit reservation skip in `CollectableOrphans`; the current "safe" behaviour is an accident of a missing-record read that a crafted record defeats. This is the same root-cause cluster as BF-46-4 (0428-328, `DamagedDeploymentNamespace`).

## Conclusion

The contaminated PR #132 akte ("NO PRODUCT LEAK FOUND IN RESERVED-NAMESPACE ORPHAN SURFACE", `CollectableOrphans` "safely guarded") is INCONSISTENT with card 0428-327's live finding and is superseded by this akte. The census now states the opposite conclusion, consistent with the card: `CollectableOrphans` (BF-46-3) lacks an explicit `never-delivered` reservation skip, so the reserved namespace is enumerated and a synthetic `never-delivered/deployment.json` is advertised as a collectable orphan. This is an evidence-content correction reconciling the census with the live card (source revision: card 0428-327 at LIVE `origin/main` `3d31d1a4a`, product seam `internal/deployment/deployment_list.go`); it is not a product edit and does not accept #132. Authorship of this akte is the executing lane's own canonical identity (w340-0428-327-reissue132), satisfying the w255 authorship disposition and the commit-identity admission rule; the contaminated objects under w322-0428-249-pr1812gate are left READ-ONLY.

## repo-rule compliance

- Planning-only change: one evidence file under `evidence/2026-11-27/w340-0428-327-aktefix-r2/`. No card edit, no product-repo commit, no `.github/**` edit, no merge, no closing of #132.
- Isolated plan discipline: this akte is authored and committed from an isolated worktree `workers/w340-0428-327-reissue132-plan` (branch `w340-0428-327-aktefix-r2`), NOT from the shared/active checkout. Only this lane's own files are staged.
- `python3 scripts/plan.py check` run before commit (render first if required): recorded in the Evidence-on-origin witness.
- Evidence lives only in baseharbor-plan. Written with lane identity w340-0428-327-reissue132.
- No markdown checkboxes in this file outside the sanctioned form (none).
- No subagents; no containers/networks/volumes started (see cleanliness).

## cleanliness

- This lane started zero docker/podman compose projects; no container, network, volume or state directory was created.
- `docker ps -a` before (this lane pid at time of check): zero container rows.
- `docker ps -a` after (END verification): zero container rows.
- Worktree `workers/w340-0428-327-reissue132-plan` left at detached branch `w340-0428-327-aktefix-r2` from LIVE origin/main `3d31d1a4a`, single akte commit; no stray files under the ecosystem root beyond the worktree and evidence.
- cleanliness: besenrein.

## Evidence-on-origin witness

```text
ls-remote origin/main HEAD (LIVE tip before branch cut): 3d31d1a4ac4d9efa33263995d76a6efaf940c258
commit <hash> authored by w340-0428-327-reissue132 -> push refs/heads/w340-0428-327-aktefix-r2
git ls-tree -r --name-only origin/main | grep w340-0428-327-aktefix-r2:
  evidence/2026-11-27/w340-0428-327-aktefix-r2/akte.md
Plan SHA: <hash>
```

END w340-0428-327-reissue132 DONE — akte reissued under own canonical identity, supersedes contaminated PR #132; candidate SHA <hash>; PR <n>; Hosted Plan run <run-id> terminal SUCCESS.
