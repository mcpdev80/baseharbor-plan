# Hunt akte H-V34: ready-list dependency provenance

- role: Worker (BUG-HUNT, pure finding, no product change, no commit to baseharbor)
- lane: 0428-221-huntready
- slice: H-V34 "Erfullungs-desk der ready-liste sind die deklarierten abhaengigkeiten wirklich in develop?"
- card: t-20261121-base-branch-provenance-loss (0428-221)
- produced: 2026-11-21
- base attestation (planning repo, via real remote): `git ls-remote origin refs/heads/main` => `e09b76f85da7d1cc0b9b77ae0bde3bc12f747f3f refs/heads/main`; `git ls-remote origin refs/heads/develop` => `b09e4a0a66a1f4160adf5162db3cfd839e483e18 refs/heads/develop`
- product reality via API only (planning-local origin mirror is a stale partial fetch that drops `develop` on `git fetch`; authoritative witnesses taken from `git ls-remote` + `gh api`)

## Mission (verbatim)

Reading-only provenance audit of the `ready` list: for each ready card, read `depends_on`, and for each dependency check status/resolution, whether the dependency PR is merged (`gh pr view <n> --json state,mergedAt`), and whether its content sits in develop (`merge-base --is-ancestor <pr-head> develop`). For the two CLI-redesign deps (contract, env-policy) give the file/proof. For card 0428-221 acceptance points 2+3: does any plan-repo script catch 'accepted without mergedAt' or 'base not descendant of develop'; if not, name file:line where it would hang.

## Reality witnesses

- planning remote (authoritative): `git -C baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git`
- product remote (authoritative): `git -C workers remote -v` => `origin https://github.com/mcpdev80/baseharbor.git`
- `python3 scripts/plan.py list --ready` returns exactly five cards:
  - t-20261114-r28-cli2-app-lifecycle (0428-060), depends_on [cli2-contract, cli2-env-policy]
  - t-20261114-r28-cli2-coordination (0428-057), depends_on []
  - t-20261120-r28-keycloak-producer-target-mismatch (0428-136), depends_on []
  - t-20261120-r28-perses-status-never-verified (0428-137), depends_on []
  - t-20261121-base-branch-provenance-loss (0428-221), depends_on []
- only 0428-060 carries non-empty depends_on. The other four have empty depends_on => no dependency provenance to verify; findings: clean.
- `plan.py` `accepted()` (scripts/plan.py:510) = `resolution == "accepted"` (or superseded chain). No `mergedAt`, no git call. `derived_state()` (line 731) derives `ready` from "every dep accepted + release active/early". Nothing in scripts/plan.py calls ls-remote/mergedAt/merge-base (grep of scripts/*.py: only snapshot.py uses subprocess for gh, unrelated).
- The one test that documents the gap: `test_card_readiness_changes_only_when_prerequisite_is_accepted` (scripts/tests/test_plan.py:574) asserts "A merged PR alone does not accept the prerequisite" and drives readiness purely off the `- [x]`/`resolution: accepted`/`evidence:` flip in the card. The card frontmatter field that carries a PR reference is `prs:`.

## FINDINGS by ready card

- t-20261114-r28-cli2-coordination (0428-057): depends_on []. No dependency. Clean.
- t-20261120-r28-keycloak-producer-target-mismatch (0428-136): depends_on []. No dependency. Clean.
- t-20261120-r28-perses-status-never-verified (0428-137): depends_on []. No dependency. Clean.
- t-20261121-base-branch-provenance-loss (0428-221): depends_on []. No dependency. Clean. (This is the owning card; its own acceptance points 2+3 answered in FINDING-2/3.)
- t-20261114-r28-cli2-app-lifecycle (0428-060): depends_on [t-20261114-r28-cli2-contract (0428-049), t-20261114-r28-cli2-env-policy (0428-053)].

## FINDING-1: 0428-060 deps carry content in develop, but the plan-tool cannot prove it

Dependency 1: t-20261114-r28-cli2-env-policy (0428-053)
- card frontmatter: kanban_status=closed, prs=[mcpdev80/baseharbor#1594]
- `gh pr view 1594 --json state,mergedAt,mergeCommit` => state=MERGED, mergedAt=2026-11-20T16:06:23Z, merge_commit_sha=40cb28c758b02960356434b630086a341ebe1738
- develop head (API) = b09e4a0a66a1f4160adf5162db3cfd839e483e18
- `gh api .../compare/<merge>...develop` => total_commits ahead = 146 => develop contains the merge plus more => the env-policy content IS a descendant of develop (in develop). Confirmed.
- files changed by 1594 (API /files): internal/application/workload_security.go (+18/-2), internal/application/workload_security_explicit_policy_test.go (+58), internal/application/workload_security_test.go (+17/-4), internal/operatorauth/authorization_test.go (+7/-10), internal/operatorauth/config.go (+26/-6), internal/operatorauth/config_explicit_policy_test.go (+65), internal/operatorauth/operatorauth_test.go (+6/-6), internal/serviceaccess/policy.go (+62/-6), internal/serviceaccess/policy_explicit_test.go (+82), internal/serviceaccess/policy_test.go (+4/-4). All present at develop HEAD (policy.go 11613B, config.go 5046B, workload_security.go 11020B via API size probe).
- conclusion: DEPENDENCY SATISFIED (content in develop). But the plan tool reports this as `accepted` purely from `resolution: accepted` with NO mergedAt/ancestor proof.

Dependency 2: t-20261114-r28-cli2-contract (0428-049)
- card frontmatter: kanban_status=closed, prs=[]
- No PR exists on develop for 0428-049. Searched merged+open+closed PRs for queries "0428-049", "cli2-contract", "cli contract", "CLI contract" => all empty. `gh pr list --state merged --base develop --search "cli contract in:title"` => empty.
- This is EXPECTED by design: 0428-049 is a plan-only deliverable (its own round-1 akte, evidence/cli-redesign-20261114/contract/round-1.md, line "This is a plan-only deliverable; there is no product change and therefore no PR is required"). The contract lives in the PLANNING repo as evidence/cli-redesign-20261114/contract/cli-command-contract-v1.md, not in baseharbor product source.
- contract surface that 0428-060 must have "before itself" (from the code-entry-index, generated against product develop @ cd77e20e107d7f29020c167ae143eaf1e6598b40): the CLI command tree under cmd/baha/ (app.go:21 appCommand, commands.go:33-166 root registration, app_apply.go:38 appApplyCommand, app_lifecycle.go:21 appDownCommand/app_lifecycle.go:197 appDestroyCommand, etc.) + the reviewed contract doc cli-command-contract-v1.md.
- The contract is a spec/plan artifact; there is no product file to merge. So "is its content a descendant of develop" is the wrong predicate for a plan-only card. The correct predicate: is the contract doc committed to the planning repo? It is (evidence/cli-redesign-20261114/contract/cli-command-contract-v1.md, present, authored 2026-11-14).
- conclusion: DEPENDENCY SATISFIED in the plan-only sense (contract authored + reviewed, no PR expected). But again the plan tool reports `accepted` from `resolution: accepted` with no mergedAt/ancestor proof and no way to distinguish a plan-only deliverable from an unmerged implementation dependency.

Net for 0428-060: both deps are satisfied, exactly like the env-policy proof the card's own author wrote. This is precisely the scenario the mission warns about: `ready`/`accepted` prove the DEPENDENCY CARD is done, never that the DEPENDENCY CONTENT is a descendant of the base 0428-060 is cut from. The tool has no mergedAt or ancestor witness on the depends_on edge.

## FINDING-2 (acceptance pt 2): no plan-repo check catches 'accepted without mergedAt'

- `grep -rn "mergedAt"` in scripts/** => NO matches. `accepted()` (plan.py:510) never inspects a merge timestamp.
- The ONLY reference to mergedAt in the whole repo is the doc comment in tests/test_plan.py:574 ("A merged PR alone does not accept the prerequisite") and this akte. It is a UNIT-TEST assertion, not a live gate; the gate it guards (render of the readiness tag) still only flips on the card's `- [x]`/resolution/`evidence:` fields, exactly the field that can be set without any merge.
- `accepted()` treats `resolution: accepted` as conclusive proof of "dependency is ready", with no requirement that a PR be merged or that its merge be a descendant of develop. A card could be flipped to `accepted` by hand after the base lane was abandoned, and nothing in plan.py rejects it.
- Where it would hang (the exact hook that is missing): plan.py line 510, function `accepted(self, tid)`. It is a pure Python read of the card frontmatter with no git/HTTP witness. A correct gate would, on `depends_on` edges to a card that declares `prs:`, resolve the PR head via `git ls-remote`/`gh api`, require `state==MERGED` with a non-null `mergedAt`, and assert `git merge-base --is-ancestor <pr-head> <develop> == 0`. That hook is absent at plan.py:510-518. No other script (grep for merge-base/--is-ancestor/ls-remote across scripts/*.py) defines such a check; snapshot.py's subprocess only runs gh for unrelated release snapshots.

## FINDING-3 (acceptance pt 3): no check catches 'base not descendant of develop'

- The owning card 0428-221 is itself on the ready list (its own dep is empty), and its whole premise is that the base content was lost. The plan tool has NO check anywhere that a ready/active/review card's integration base is a descendant of develop.
- `grep -rniE "descendant|is-ancestor|merge-base|provenance"` across scripts/** => NO matches in plan.py/snapshot.py/release_cycles.py.
- The closest real machinery is the externally referenced `scripts/pr-gate-plan.py` diff-base tool, which the evidence corpus cites as NOT existing as a file (find scripts/pr-gate-plan.py => none; it appears only in task notes and evidence prose). It is therefore not a live gate. No `.github`, `scripts/**`, or JSON (`release-requirements.json`, grepped for mergedAt/ancestor/develop/provenance => empty) enforces base-ancestry.
- Where it would hang (the missing hook): the readiness render at plan.py `derived_state()` (line 731) and `accepted()` (line 510). Both are frontmatter-only; neither performs a base-ancestry test. A correct gate would, on any state transition of a card whose brief requires a product base, resolve `origin/develop` via `git ls-remote`, and reject (via `self.err`) a card whose declared integration head is not `git merge-base --is-ancestor <develop-tip> <head>`. That test is absent at plan.py:731/510. The card's own acceptance prose (0428-221 brief) demands exactly this and the tool provides no enforcement.

## Net finding

- The `ready` list is true for "no open dependency card and release active", but the plan tool cannot distinguish (a) a satisfied dependency whose content is a real descendant of the base, from (b) a card whose dependency is marked accepted yet whose content was never merged / whose base lane was abandoned. 0428-060 is the live example: both deps are genuinely satisfied, but the only witnesses are the env-policy PR merge (1594) and a plan-only contract doc with no PR; `plan.py` reports `accepted` from a single frontmatter field and never calls git. The two acceptance points 2 and 3 map to the same structural hole at plan.py:510 (`accepted`) and plan.py:731 (`derived_state`): no mergedAt, no base-ancestry, no git witness on the depends_on edge.
- This is a finding for the Owner/planning-repo owner to fix (a script change in baseharbor-plan/scripts/plan.py or a new gate). It is OUTSIDE this hunt lane's write-set. No product or planning file was changed.

## ## cleanliness

- No containers/compose/projects started. `docker ps -a` before: 0 rows (empty table). `docker ps -a` after: 0 rows (empty table). podman identical. No orphan risk.
- my shell pid this shift: 709451 (no baha test runner invoked; only gh/gh api/git ls-remote/python3 plan.py).
- cleanliness: clean, no containers/volumes/networks/state created or left.

## ## repo-rule compliance

- Read-only hunt: no product file edited, no commit to baseharbor, no PR opened/merged/closed, no `.github/**` touched, no workflow_dispatch/rerun, no subagent spawned, no bare `go test ./cmd/baha/`, no `git add -A`, no `git stash`.
- Reality taken via `git ls-remote` (real github.com/mcpdev80 remotes) + `gh api`; the planning-local origin mirror's `git fetch` cannot resolve `develop` (stale partial mirror) and was never cited as remote truth.
- No evidence written into any product repo; evidence lives in baseharbor-plan/evidence/r28-welle4-2026-11-21/ready-dependency-provenance/hunt-1.md (planning repo, origin/main).
- GATE: this hunt does not add or change any test; findings 2/3 are a gate-plan gap (plan.py:510 / plan.py:731) reported to the planning-repo owner. No CI route needed for this finding; it is a reporting-only deliverable.

## END

- lane: 0428-221-huntready
- status: END_DONE
- candidate SHA: n/a (no product/planning candidate; read-only finding)
- found 4 clean ready cards (empty deps) + 1 satisfied-but-unprovable-by-tool dependency pair (0428-060); gate gap at plan.py:510 and plan.py:731.
