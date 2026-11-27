# w362-0428-299-1863hop — Evidence (akte)

Lane: w362-0428-249-1812rebase executing card 0428-299 mission (owner dual-duty instruction 03:34:12Z)
Card: 0428-299 · Repo: baseharbor · PR: #1863 · Branch: w336-0428-299-goprereq

## PLAN
1. Fetch card 0428-299 from plan origin/main; verbatim owner + identity block.
2. Reality check ls-remote (develop tip; PR #1863 head; stale fail 45913103879 witness).
3. Clean worktree from the #1863 head commit; remote URL resolved to github.com/mcpdev80.
4. git merge origin/develop forward-only; 4-Feld identity verify; ancestry + log gates.
5. Prechecks gofmt/vet/build only; NO local tests, NO VM.
6. ONE normal push + ls-remote delivery witness.
7. Fresh pull_request run on exact new head to terminal; gate/job census + failure lines in this akte.
8. Publish this akte to plan main via isolated plan worktree + PR; verify on origin/main; END.

## ANSATZ (visible identity block)
- Card fetched at runtime from plan origin/main (main >= 2be21b378): `tasks/t-20261125-hunt33-go-runtime-prereq.md`,
  card_number "0428-299", frontmatter owner VERBATIM: `owner: w362-0428-299-1863hop` (no "(lane X)" wrapper
  → full owner value is the canonical identity for THIS card's commits; distinct from my 249 lane identity).
- git user.name: `w362-0428-299-1863hop`; email `w362-0428-299-1863hop@baseharbor.local`.
- Literal invocation: `git -c user.name=w362-0428-299-1863hop -c user.email=w362-0428-299-1863hop@baseharbor.local merge …`
- Pre-push gate: `git show -s --format=%an HEAD` == `w362-0428-299-1863hop`.
- Mission deviation noted: the in-chat instruction said "identity w362 kanonisch"; card 0428-299's own
  frontmatter owner is `w362-0428-299-1863hop`, so per the admission rule (canonical = card frontmatter
  value) commits here carry `w362-0428-299-1863hop`. Documented, not silent.

## Remote resolution witnesses
- `git -C baseharbor-plan remote -v` → origin https://github.com/mcpdev80/baseharbor-plan.git (verified earlier, same session).
- Worktree `git remote -v` → `origin https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80 URL);
  all remote truth via `git ls-remote https://github.com/mcpdev80/baseharbor.git`.

## BASE ATTESTATION
- `git ls-remote https://github.com/mcpdev80/baseharbor.git`:
  - refs/heads/develop = `ea5218d72e263f21e79853b679af50074dab8c25` (merge input)
  - refs/pull/1863/head (pre-push) = refs/heads/w336-0428-299-goprereq = `4160d53f736b3c978b1df028ff90cd2b7d033d49`
  - stale fail witness: run `45913103879` (pull_request, head 4160d53f) = completed/failure (gh run view).
- Worktree cut at `refs/remotes/lane-origin/pr1863` = 4160d53f (fetched from the GitHub URL; the PR branch
  per gh pr view 1863 headRefName `w336-0428-299-goprereq`).

## Merge + gates
- `git merge origin/develop` forward-only (clean): merge commit `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f`,
  4-Feld: `an=w362-0428-299-1863hop ae=…@baseharbor.local cn=same ce=same`.
- Ancestry: develop ea5218d72 ancestor of HEAD = OK; PR branch 4160d53f ancestor of HEAD = OK.
- `git log --oneline ea5218d72..HEAD` = only the #1863 chain (4919ef850, 34c9d7bdb, 4160d53f merge,
  0eafa9f5a my merge). No foreign candidate.
- `git diff --name-only ea5218d72..HEAD` = internal/stableid/lock_probe.go,
  internal/stableid/lock_probe_platform_test.go, scripts/pr-gate-coverage.json (the PR's own doc/coverage
  delta; merge-absorbed develop files excluded by the three-dot comparison semantics — gh pr diff shows the
  same 3 files).
- Prechecks: gofmt clean, `go vet ./internal/stableid/` green, `go build ./...` green. NO tests executed
  locally, NO VM. Test binding for the changed test file: normal auto-discovery (`go list ./...`/`go test -list`)
  via 'PR · Go unit · shards' selection in Hosted CI; the coverage catalog row for internal/stableid is
  already registered in scripts/pr-gate-coverage.json (part of this PR's existing content, w336/w361 line).

## Push + delivery witness
- Push: `4160d53f7..0eafa9f5a HEAD -> w336-0428-299-goprereq` (normal push, no force).
- ls-remote after push: refs/heads/w336-0428-299-goprereq = refs/pull/1863/head = `0eafa9f5a42dc068f653b565f9f5c8c91bed4c5f`.
- Fresh pull_request run on exact new head: `45935170048` (queued at push; watcher active in this session).

## Hosted CI gate census (run 45935170048, head 0eafa9f5a)
- Terminal: completed/failure. Full census (29 jobs): success 3 (`Workflow policy`, `PR · Source format`,
  `PR · Native gate plan`), failure 2 (`PR · Trusted Plan`, `PR Selected Checks`), skipped 24
  (all downstream gates blocked by the Trusted Plan abort). Failure detail in the diagnosis section.

## repo-rule compliance
- Test execution exclusively via Hosted CI; local runs were non-test prechecks only (gofmt/vet/build).
- One push, forward-only merge of origin/develop, no force, no cherry-pick; identity 4-Feld
  `w362-0428-299-1863hop` verified pre-push (`git show -s --format=%an HEAD`).
- Card 0428-299 scope (hunt33 Go-runtime doc prerequisite): no product-behavior change beyond the
  PR's existing doc/coverage delta; the hop added none.
- The #183 correction send (03:43:32Z) was REVOKED by the owner at 03:46:05Z in favor of w267
  (one task per worker). All local edits I had made in the demo worktree were reverted
  (`git reset --hard 83c80c917`, worktree removed); no push, no branch, no commit was ever made
  to baseharbor-demo by this lane.

## 1863 akte-publish route (plan PR #178) — base-red blocker
- Plan PR #178 (branched at ef0bcfbcf) is OPEN but `Plan · validate` FAILS on the MAIN tip:
  `evidence/w350-0428-359-batchhop2/akte.md` lines 21-25 contain checkbox syntax outside tasks/
  (would become CardBoard cards). Zero errors from my file. Pre-existing main breakage (w350 lane),
  NOT introduced by me; any plan PR is red until main is fixed. Plan PR #136 (w267) proposes the
  row; #178 cannot merge green while main is red.
- Akte is committed and pushed verbatim on plan branch `w362-0428-299-akte` (5b5e6d821); it will be
  on origin/main as soon as the base validator defect is fixed and the queue merges.

## END line
END (STATE handoff): #1863 hopped forward-only to `0eafa9f5a`, ONE push, fresh run `45935170048`
observed to terminal = completed/failure with deterministic root cause (base-checkout catalog
fail-loud, diagnosis section). No further push or rerun by this lane pending Coordinator/Codex
disposition (waiver / route via develop / different carrier). Akte published via plan PR #178,
merge blocked only by the pre-existing main validator defect above. 249 remains in the push-gate
hold (demo #183 merge + pin advance pending; carriers 8c83c7091+0b343af5e local, remote stays
6ab5310d1).

## cleanliness
- No containers/compose started by this mission on this host (docker was not invoked at all).

## 1863 failure diagnosis (run 45935170048 on 0eafa9f5a = completed/failure)
- Failed jobs: `PR · Trusted Plan` (140296599429), `PR Selected Checks` (140296724470).
- Root cause (exact log line, Trusted Plan): `ValueError: invalid trusted PR gate coverage catalog:
  uncataloged source change, no declared runtime gate owner: internal/stableid/lock_probe.go …
  lock_probe_platform_test.go …` from `pr-gate-plan.py` line 1952.
- Mechanism: the trusted planner runs from the TARGET-BASE checkout (`pr-gate-plan.py` +
  `validate-pr-gate-coverage.py` + `pr-gate-coverage.json` as of base `ea5218d72`, fetched via the
  `MIGRATION_CONTROLLER`/base bootstrap in `.github/workflows/ci.yml`), while the CHANGED-PATHS
  inventory is base→candidate-head. Local reproduction (deterministic): base planner + base catalog
  over the two changed stableid sources => `([], [both paths])` — the exact fail-loud abort; the
  candidate catalog's new rows (added by this PR: `source.internal_stableid_lock_probe_go`,
  `source.internal_stableid_lock_probe_platform_test_go`) are invisible to the base-planner resolve
  => `(['atomic/docker/data-capabilities'], [])`. So the catalog registration is correct CONTENT but
  cannot take effect until it exists on develop. Same class as the stale fail 45913103879 on 4160d53f;
  a doc/coverage-only hop cannot change it, because the catalog version that gates is decided by the
  planner bootstrap (base checkout), not by candidate PR content.
- Break-the-cycle options for the Coordinator (none inside my write-set): (a) merge with the
  catalog-row route proven and the base-planner abort waived by policy; (b) land the two
  pr-gate-coverage.json rows on develop via an existing branch that is already merge-qualified;
  (c) register the rows so the base planner's deletion/unknown handling admits them without a
  catalog edit (not observable in the current base planner — it fail-louds on any uncataloged
  cmd/internal source).
- `PR Selected Checks` fails downstream of the same planner abort (its routing inputs come from
  Trusted Plan; no independent product failure observed).
- Disposition per AGENTS 4.7/5.4: NO blind rerun, NO scope widening (touching the catalog/CI
  bootstrap is outside card 0428-299's hunt33 doc scope and belongs to the CI-owner routing
  decision). Reported as STATE with file:line.

## 249 sequencing note (owner 03:37:31Z, recorded here since my 249 akte stays local until GO)
- 45930995254/45931118156 terminal FAILURE (witnesses in the 249 editset akte); carriers 8c83c7091+0b343af5e
  preserved locally on branch `lane-0428-249-editset-wip` (refs/heads there), remote stays 6ab5310d1.
- NO push / no new matrix until Demo baseharbor-demo#183 is ACCEPT+merged (run 45934997844 SUCCESS on
  83c80c9, w255 reviewing) AND the PR demo pin advances; a push before that would re-matrix the known
  consent/cert failures. Lane holds; my active work is this #1863 mission (run 45935170048 watched).

