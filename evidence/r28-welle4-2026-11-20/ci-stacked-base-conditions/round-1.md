# 0428-180 — CI on real stacked bases (round-1, delivery only)

worker-180 was dispatched to edit `.github/workflows/ci.yml` and prove exact-head CI on a stacked `cli2-*-head` and a `w0*` base. Work stopped immediately on an owner-stop (meldefrist) because the card was already claimed by another session.

## PLAN

1. Read mission-180.md, task card, baseharbor/AGENTS.md.
2. Measure remote truth: develop head via `git ls-remote`, ci.yml condition lines, open stacked PR base refs.
3. Locate the exact-head CI proof (existing run or own).
4. Stop on owner-stop: record measured findings, write THIS evidence (0 checkboxes), post END.
5. Release the seat for another card.

## Measured state at this stop

Base head (develop), witness:

    git -C baseharbor ls-remote lane-origin refs/heads/develop
    96f2ae11a25a508998c44a9854ef17f8fa15c112  refs/heads/develop

ci.yml condition lines (grep `startsWith(github.base_ref`):

    431  pr_native_impact
    481  pr_native_selected
    517  source_format
    714  pr_plan
    976  pr_runner_interface
    1000 pr_demo_pin
    1032 pr_candidate
    1075 pr_candidate (runtime_required + owner)  [pr_candidate]
    1114 pr_candidate_advisory
    1145 pr_focused
    1188 pr_unit_shards
    1211 pr_validations
    1333 pr_public_contracts
    1364 pr_public_contracts (runtime)
    1383 pr_selected_integration
    1400 pr_owner_node_native
    1439 pr_selected_final (aggregate)
    1534 pr_draft_focused (draft)
    1588 pr_draft_go_shards (draft)

All currently read: `github.base_ref == 'develop' || startsWith(github.base_ref, 'lane-') || startsWith(github.base_ref, 'cli2-') || startsWith(github.base_ref, 'w0')`.

The eight lines the card named (431, 481, 517, 714, 976, 1000, 1032, 1075) are therefore ALREADY widened to cover `cli2-*` and `w0*`. No edit was made by this worker.

Open stacked PRs and their base refs (witness: `gh pr view --repo mcpdev80/baseharbor`):

    #1615  base cli2-env-policy-head  head ca930ce63c4ff080a736c6e3439dc1d87d017e0c   0428-057
    #1623  base cli2-identity-secrets-head  head 4cbf92960cb5d97077370b7da052d45523ce0043   0428-063
    #1665  base w083-perses-datasources  head e580d32414565442376f23ace9a4a2dd7ed03838   0428-082

## Proof that exact-head checks run on a stacked cli2 base (run already logged by owner)

Run 44735405029 (witness via `gh api .../actions/runs/44735405029`):

    id: 44735405029
    name: CI · PR #1615
    event: pull_request
    status: completed
    conclusion: failure   (jobs failed, i.e. they RAN — not skipped for missing base)
    head_branch: cli2-identity-secrets-head
    head_sha: ca930ce63c4ff080a736c6e3439dc1d87d017e0c

Jobs that executed (conclusion present, not skipped) at that exact head:

    PR · Native gate plan ............ success
    PR · Go unit · cli-0 ............. failure  (ran, did not skip)
    PR · Go unit · cli-1 ............. failure  (ran, did not skip)
    PR · Go unit · cli-2 ............. failure  (ran, did not skip)
    PR · Go unit · cli-3 ............. failure  (ran, did not skip)
    PR · Exact Candidate ............. success
    PR · Runner Interface ............ success
    PR · Demo Pin .................... success
    PR · Focused Python .............. success
    PR · Validation · ci-actionlint .. success
    PR · Validation · cli-gofmt ...... success
    (full job list in evidence)

No job was skipped for an unresolved base_ref: the widened condition at ci.yml:431/481/517/714/976/1000/1032/1075 (and the aggregate at ci.yml:1439) let the whole graph run at the exact stacked head ca930ce6. This is exactly what acceptance item 2 requires.

## KREUZPRUEFUNG: der Owner-auftrag, mein stand war X

Mein stand war X = "die acht bedungungszeilen waren noch narrowed (nur develop/lane-); ich muss sie um cli2-/w0- erweitern und einen eigenen exakten head-run erzeugen". Bei beginn der arbeit war X bereits nicht mehr zutreffend: commit 387af401f ("fix(ci): route stacked PR bases and runtime coverage", an ancestor of origin/develop, reachable from current HEAD) hat alle acht zeilen plus die aggregate- und draft-bedingungen bereits auf `startsWith(github.base_ref,'cli2-') || startsWith(github.base_ref,'w0')` erweitert. Der owner hat karte 0428-180 selbst uebernommen (status active, owner 'Codex (baseharbor-pr-sweep-fortsetzen)') und den nachweis in commit d346f180 'plan: record exact stacked CI run result' eingetragen (run 44735405029). Zwei schreiber in ci.yml sind ein regelverstoss (§4.3); daher NICHTS geaendert, KEIN pr, KEIN push.

## repo-rule compliance

- Product code / tests / merge / force-push / subagents / `git add -A`: none.
- Work stayed on lane-0428-174-develop-runtime-red, an ancestor of origin/develop.
- `git merge-base --is-ancestor HEAD origin/develop` -> true (branch hygiene ok).
- Evidence written only in baseharbor-plan (product repo untouched).

## cleanliness: clean — no containers, networks, volumes or state directories started or left; evidence file is the only artifact created.

## END

END_DONE mission-180.md: card 0428-180 already claimed by another session; measured widened conditions + proof run 44735405029 (head ca930ce6, base cli2-env-policy-head), no edit made. Seat released for another card.
