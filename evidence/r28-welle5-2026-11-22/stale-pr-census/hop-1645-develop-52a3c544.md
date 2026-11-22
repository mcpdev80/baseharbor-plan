# Hop 1645 to develop 52a3c5446f

Card t-20261121 (PR #1645, stale-pr hop), mission `hop1645.md.g`.

## Context

PR #1645 = w091-tempo-r5-fix, "perses/tempo: rename .go witnesses to .go.txt (CI package-selection
fix)", base develop, OPEN, head 4d73aa97808d000d2f70eaa193f8dbfc14e817a7, mergeable_state BEHIND.
Earlier this shift the hop was measured conflict-free on current develop 52a3c5446f (in-file merge
test: auto-merged, zero unmerged files). Directive: execute the hop (git merge --no-ff 52a3c5446f,
NO rebase/amend/force, push without force), watch the hosted PR-run to terminal, report run-id,
failed-count, and the job-ids of "PR · Selected Runtime" and "PR · Native · matrix". No content
change, no merge/close/ready, no GitHub comment, no subagents.

## Witness

- develop: 52a3c5446f41a1dd8678d99875e4cb1eee67874c
- PR #1645 head (old): 4d73aa97808d000d2f70eaa193f8dbfc14e817a7
- back vs develop: 1 (directive's "back=263" is stale; current distance 52a3c5446f..4d73aa97 = 1)

## Hop

- branch (gh pr view 1645 --json headRefName): w091-tempo-r5-fix
- git merge --no-ff 52a3c5446f on exactly w091-tempo-r5-fix -> 326ca9005267c135feb31cdfde8ac69a3c17508e
  (Merge commit '52a3c5446f...'; own commits = branch commit 4d73aa97 + this merge, nothing else)
- push without force: 4d73aa97..326ca900 w091-tempo-r5-fix -> w091-tempo-r5-fix
- no content changed; no fan-in to PR #1761; no merge/close/ready; no GitHub comment

## Hosted CI run at new head

- PR #1645 run db=44996055999, head 326ca900, terminal: completed/failure
- failed-count: 2 (PR · Go unit · packages job 137127343932 + PR Selected Checks aggregate 137128679130)
- gate job-ids:
  - PR · Selected Runtime id 137127345558: SKIPPED (candidate not catalog-relevant enough to run
    the real runtime gate despite the diff; the 1756-merge did not make it run)
  - PR · Native · matrix id 137127405068: SKIPPED (same)
  - PR · Go unit · packages id 137127343932: FAILURE
- The failure is a real, content-caused unit failure in the candidate's own code, NOT the
  data-capabilities runtime gate (so NOT the 0428-237 blocker):
  TestPersesTempoDatasourceSharedBackendGatewayStaysPolicyNeutral,
  internal/metrics/perses_tempo_source_test.go:419:
  "a dev non-RequireClient gateway must not enroll a client pair"
  This is identical to prior run 6833 at 4d73aa97 (same test, same file:419, same failure), so it
  is the candidate's pre-existing content failing, not introduced by the hop.

## gate-lage

Candidate #1645 is red on its own perses/tempo unit test (TestPersesTempoDatasourceSharedBackendGatewayStaysPolicyNeutral,
internal/metrics/perses_tempo_source_test.go:419). This is a candidate-own defect, not the
data-capabilities / secure-runtime-broker-503 (0428-237) blocker. Per directive scope (no content
change) the candidate is handed off as-is for the Owner to triage the unit failure.
