---
id: r27-closeout-2026-11-14
kind: evidence
release: v0.4.27
cards: [t-20261017-release-0-4-27-verify, t-20261017-release-0-4-27-qualify, t-20261017-release-0-4-27-publish]
date: 2026-11-14
lane: mission-closeout27.md
---

# v0.4.27 closeout round 1 — verify / qualify / publish dossier

## PLAN

1. Reality check: ls-remote witnesses on origin/main, origin/develop, origin/release/v0.4.27, tags, PRs #1574/#1576, Demo PR #160, planning remote; read releases/v0.4.27.md, the three cards, decisions 2026-11-14, prior r27 prepare dossiers. (done)
2. Claim act: `plan.py claim` SUCCEEDED for all three cards (qualify/publish/verify, rc=0 each) and the claim state was published on baseharbor-plan main BEFORE the closeout work, per the claim protocol. The review transition is schema-denied (needs a card PR); see "Card disposition" for the exact witnesses. (done)
3. VERIFY pass: audit each acceptance point of 0427-010 against real artifacts. (done — findings F-V1..F-V5)
4. QUALIFY pass: sort the qualification matrix evidence of 0427-008; missing coverage listed. (done — findings F-Q1..F-Q4)
5. PUBLISH pass: preparation-only; exact guards + post-merge block recipe delivered; nothing irreversible executed. (done — findings F-P1..F-P3)
6. Evidence dossier on baseharbor-plan main; card disposition documented (no illegal state transition). (done)
7. Prove the F-Q3 divergence finding read-only (plan.py claim dry-run in a throwless state + read-back). (done — see claim-denial witness)
8. ls-tree witness that this dossier exists on origin/main, then END post with candidate SHAs. (done at end of lane)

## Zone attestation (wrong-zone check)

`git rev-parse --show-toplevel` in the planning working copy used for this dossier:

    /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
    remote origin = https://github.com/mcpdev80/baseharbor-plan.git

The directory /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan was NOT used (quarantined bookkeeping dir, per mission).

## Remote truth witnesses (all fetched 2026-11-14, late-evening UTC, live `git ls-remote` / `gh api`)

    aff1532c2f6c6782a8c13afad83245d1351815e7  refs/heads/main              (baseharbor)
    0e9ccb582f5bdcdc74049bbe3996263cdce6500c  refs/heads/develop           (baseharbor)
    385b0410d6b5182471028e0f8616ad8196925f1f  refs/heads/release/v0.4.27   (baseharbor; equals refs/pull/1574/head)
    893e01d55be4f082f26918ddcdc043d84f7c138c  refs/heads/codex/fix-pre-release-source-db-v0427 (PR #1576 head, base main, OPEN, MERGEABLE)
    d09e1b024d1b161836b477ec37a95d017402fddc  refs/tags/v0.4.26            (latest published tag; NO v0.4.27 tag exists)
    e898945cdeb33f09e46898bffaf457e7dd3bb7bc  refs/heads/main              (baseharbor-demo)
    2494b05a6492f0e6a258cd2441a8179672b007dd  refs/heads/codex/pre-release-core-bootstrap-v0427 (Demo PR #160 head, OPEN, not yet on demo main)
    424f8a9c1919e3c566c55058573666ae3b982969  refs/heads/main              (baseharbor-plan)

Candidate-branch content check (fresh clone /tmp/r27-inspect/bh):

    git merge-base --is-ancestor origin/develop origin/release/v0.4.27  -> true
    (develop 0e9ccb58 IS an ancestor of the release branch head 385b0410)
    git log --oneline origin/develop..origin/release/v0.4.27            -> exactly 15 commits,
      all authored by Marcel Pfingstgräf (owner prepare-lane owner-chatgpt-r27),
      newest 385b0410, oldest fe018b97; no foreign candidate carried on top
    git diff --name-only origin/develop origin/release/v0.4.27 | grep '^\.github' -> 0 files
      (the release branch changes NO workflow file relative to develop)
    git merge-base --is-ancestor origin/main origin/release/v0.4.27     -> false
      (main aff1532c is NOT an ancestor of the release branch; PR #1574 is CONFLICTING)

## What the cards require vs what exists (VERIFY — 0427-010)

The card's own gate is "Require authorized tag/publish completion, not merely a prepared command."
Current facts:

- F-V1 (blocking by definition): No `v0.4.27` tag, no GitHub Release (latest remains v0.4.26, targetCommitish main, published 2026-10-26). Publication verification is therefore NOT POSSIBLE yet and must not be fabricated. Verify remains legitimately waiting.
- F-V2: No post-promotion Pages deployment can be verified; candidate Pages builds exist only inside PR runs and are explicitly not site evidence per the card.
- F-V3: GHCR version/compatible/latest channels: unverifiable for 0.4.27 because the publish workflow never ran for the version; the isolated-registry publishing machinery was only just being built (see F-Q3) and never produced published artifacts.
- F-V4: Changelog/doc witnesses that DO exist and will feed later verification: CHANGELOG.md `## [0.4.27]` section and docs/releases/v0.4.27.md (EN) plus the de mirror are present on develop and identical on the release branch (git diff develop..release shows no delta for those files).
- F-V5: Closeout reconciliation witnesses recorded above (open PR inventory: baseharbor #1574 draft, #1576 open, #1575/#1577-#1580 v0.4.28 lanes; demo #160; planning #24 draft docs branch NOT containing the three cards).

## Qualification matrix state (QUALIFY — 0427-008)

- F-Q1: No complete pre-release validation run exists on any 0.4.27 candidate head. Full-history evidence: the only `pre-release.yml` runs are workflow_dispatch on `codex/fix-pre-release-source-db-v0427` (all failure/cancelled) and a failed dispatch on main `aff1532c` (run 43636632008), plus October v0.4.26 validations. Nothing on develop `0e9ccb58`, the release branch or any eventual candidate SHA.
- F-Q2: Targeted run 43633496362 (workflow `targeted`, event pull_request, head fe018b97, conclusion failure, 2026-11-14T19:41Z) — required log lines:
      RuntimeError: new-edit-new-sql exceeded no-output timeout: elapsed=156s no-output=90s limit=90s
      demo-data-capabilities FAIL / demo-policy FAIL / demo-connectivity FAIL / demo-reconciliation FAIL / demo-backup-restore FAIL / demo-full-destroy FAIL / RESULT FAIL
      (job "Reference Journey · docker · Full E2E", step "Run complete reference journey")
    This was an earlier release head; the CURRENT head 385b0410 shows "no checks reported on the 'release/v0.4.27' branch" (gh pr checks 1574).
- F-Q3: The pre-release SOURCE gate itself is broken on main: run 43636632008 proved `BASEHARBOR_TEST_DATABASE_URL` absent, runtime matrices were skipped after source failure. The repair PR #1576 targets `main`, but its two workflow files differ from the identical files on develop and the release branch (blob witnesses: pre-release.yml 7889f179 on 1576-head vs 3ca2ebdd on develop/release; pre-release-runtime-suite.yml c73eee77 vs a7038275). `git merge-tree origin/main origin/release/v0.4.27` reports 478 conflicted paths, overwhelmingly `.github/workflows/*` (Owner scope): merging #1576 into main would make #1574 structurally unmergeable. This is a routing finding, not an edit (mission: kein .github/**, no reruns, no dispatches).
- F-Q4: Candidate freeze is not closed: docs/releases/v0.4.27.demo-ref pins Demo `2494b05a`, which lives only on the unmerged Demo PR #160 head (open, MERGEABLE) and is not an ancestor of demo `main` `e898945c`. The pinned Demo head in turn records Core `08755645` in baseharbor-core.ref, which is neither current develop `0e9ccb58` nor a release-branch commit. Pre-release source resolution would only accept the candidate via the `release/v0.4.27` branch-tip branch of its ancestry guard (pre-release.yml lines ~95-105 of origin/release/v0.4.27 blob 3ca2ebdd).
- Sorting conclusion: per the card, required coverage is MISSING (F-Q1) and there is no recorded Maintainer authorization for a complete pre-release. Qualify cannot pass; its blockers are F-Q1..F-Q4.

## Publish preparation (PUBLISH — 0427-007)

- F-P1: Prerequisites fail today: complete validation missing (F-Q1) and no separate Maintainer promotion authorization recorded for a frozen SHA. Publication/tags were NOT executed (mission scope: owner points only).
- F-P2: The card's handoff demands a ready-to-paste block with the ACTUAL resulting main SHA. Since the promotion merge SHA does not exist (PR #1574 is CONFLICTING against main), a placeholder-free final block cannot honestly be delivered yet. The correct pre-merge validation block is below; the final post-merge block must be regenerated from the actual main SHA by the owner/prepare lane at promotion time.
- F-P3: Ready-to-paste tag-absence/validation guards usable NOW against the current candidate (annotated tags, remote, no moving target; run from a clone with remote `origin` = https://github.com/mcpdev80/baseharbor):

      git fetch origin --tags --prune --prune-tags
      git rev-parse --verify -q refs/tags/v0.4.27 && echo "LOCAL TAG EXISTS - STOP" || echo "local v0.4.27 absent: OK"
      git ls-remote origin refs/tags/v0.4.27 | grep . && echo "REMOTE TAG EXISTS - STOP" || echo "remote v0.4.27 absent: OK"
      git update-ref refs/tags/v0.4.27-verify $(git hash-object -t tag -w - <<< "tag v0.4.27-verify
      tagger $(git config user.name) <$(git config user.email)> $(date -R)

      verification tag - not a release")) && echo "annotated tag write path OK (scratch ref)"
      git update-ref -d refs/tags/v0.4.27-verify
      # After the authorized promotion merge, replace <MAIN_SHA> with the ACTUAL 40-hex main SHA and only then:
      # git cat-file -e <MAIN_SHA> && git tag -a v0.4.27 <MAIN_SHA> -m "BaseHarbor v0.4.27" && git push origin v0.4.27

## Card disposition (this lane's publishing act)

    $ python3 scripts/plan.py claim t-20261017-release-0-4-27-qualify --owner "mission-closeout27"   # rc=0; claim published on main before closeout work
    $ python3 scripts/plan.py claim t-20261017-release-0-4-27-publish --owner "mission-closeout27"   # rc=0 (same)
    $ python3 scripts/plan.py claim t-20261017-release-0-4-27-verify  --owner "mission-closeout27"   # rc=0 (same)
    $ python3 scripts/plan.py claim t-20261017-release-0-4-27-publish --owner "mission-closeout27"   # rc=1: '... is active; only planned, wait or blocked tasks can be claimed'

- Correction of this dossier's first draft: `plan.py claim` did NOT reject the dependency-waiting cards; it only refuses a foreign owner or an already-active card. The three claims succeeded and were committed/pushed to planning main before the closeout work, per the claim protocol.
- Review-state trial (schema denial, quoted verbatim): with `kanban_status: review` set on the three cards, `python3 scripts/plan.py check` returned

    error: tasks/t-20261017-release-0-4-27-qualify.md: status review requires at least one PR
    error: tasks/t-20261017-release-0-4-27-publish.md: status review requires at least one PR
    error: tasks/t-20261017-release-0-4-27-verify.md: status review requires at least one PR

  (plan.py lines 416-417: `if st == "review" and not item["prs"]: self.err(...)`.) The trial edits were reverted; the published state is `active` under this lane.
- The mission step "die drei karten auf review setzen mit akte" is therefore schema-impossible for these three acceptance cards: they own no product PR (`repos:` baseharbor/baseharbor-demo), their acceptance content IS an evidence dossier, and inventing an irrelevant product PR or pointing `prs:` at a planning-repo PR would violate the cards' own scope and the one-candidate rule. The cards stay `active` under `mission-closeout27` with the dossier linked; their Handoff sections carry the review-pending act explicitly.
- No acceptance, qualification, publication or tag is claimed by this act.

## Decisions 2026-11-14 consumed

- drop-standalone-stage-proof (video card closed as dropped), owner-close-inherited-work (012/046/053/185/187 accepted by owner direction; 020/059/169/186 stay open; Connector work closed), perses-replaces-grafana-v0428 (Grafana UI cards superseded, Perses is v0.4.28), public-console-connector-scope (Console/Connector archived; NOT v0.4.27 gates).
- Consequence applied here: only Core + Demo are release surfaces; Console/Connector PRs are excluded from the closeout matrix.

## Tools / sources

- gh CLI manual (gh release create --target/--verify-tag semantics) via context7 /cli/cli; git merge-tree, git ls-remote, gh pr checks/run list as above; product workflows read read-only from origin/release/v0.4.27 blobs.

## Evidence publication witness (required by mission, ran as second-to-last action)

    $ git fetch --quiet origin main
    $ git ls-tree origin/main evidence/r27-closeout-2026-11-14/
    100644 blob b0e3edad77b2837b192b962e77c3695a8480d758	evidence/r27-closeout-2026-11-14/round-1.md
    $ git rev-parse origin/main
    2218a1c986b85951bd6d5d86acb2bdbb41337bc2

Candidate/act SHAs (baseharbor-plan main): claim commit 9639472346dee29c50fbe31006f3e96f66baed44, evidence commit 2218a1c986b85951bd6d5d86acb2bdbb41337bc2 (ancestor: 96394723; `git log 96394723..2218a1c9 --oneline` lists exactly this one closeout commit — no foreign candidate on top).
Candidate refs verified (baseharbor): release/v0.4.27 = 385b0410d6b5182471028e0f8616ad8196925f1f (develop 0e9ccb58 is an ancestor; main aff1532c is NOT — see F-P2). No product-branch work was created by this lane (closeout = reading, attestation and planning only; mission freeze respected).

## VM / runtime hygiene

No containers, compose projects or VM cells were started by this lane (read-only closeout); nothing to bring down.

## Open points for the owner (next triggers)

0. Routing question for this closeout (the only decision this lane cannot make itself): the Qualify and Publish cards each require a Maintainer authorization the mission does not contain ("fehlendes als QUESTION/befund"). Triggering the complete pre-release matrix, merging anything to main, or pushing tags all sit beyond this lane's scope; the three cards stay `active` under `mission-closeout27` with the blockers F-Q1..F-Q4 documented, and cannot legally enter `review` without a card PR. Decide one of: (a) dispatch the full pre-release on a re-frozen candidate after points 1-2 below close, (b) hand the cards to the prepare lane `owner-chatgpt-r27`, or (c) accept the review-state limitation and let the owner close the cards from this dossier.
1. Decide the main-line routing of the pre-release source-gate repair: PR #1576 vs the develop/release workflow divergence (F-Q3). Suggested order: integrate the workflow fix through the normal develop path or land #1576 on main and refresh #1574 by merging main into the release branch inside the prepare lane (owner-chatgpt-r27).
2. Merge or replace Demo PR #160 so the pinned Demo SHA is reachable (F-Q4), then re-pin docs/releases/v0.4.27.demo-ref if the SHA moves.
3. Record explicit Maintainer authorization and dispatch the complete pre-release on the exact frozen candidate (Qualify card).
4. Only after a green complete validation: promotion merge → actual main SHA → final tagging block (Publish card) → tag push (owner) → this lane's successor verifies publication (Verify card).

END_BLOCKED mission-closeout27.md: closeout dossier published; all three cards blocked on real prerequisites (no v0.4.27 tag/Release, no complete pre-release run, candidate not mergeable/frozen); nothing irreversible executed.
