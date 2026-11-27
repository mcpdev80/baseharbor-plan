# PR #183 CI inclusion disposition — card 0428-284

## Verdict

IN-SCOPE for the existing 0428-284 authorization, limited to one purpose-bound test-only CI path in `baseharbor-demo/.github/workflows/pr-config-matrix.yml`. This is a scope classification only; it neither qualifies PR #183 nor changes any workflow itself.

## Source state

- Demo PR #183 is OPEN, base `develop`, head `83c80c917858e719118bd21e0183b4516959ac53`, merge state CLEAN. The exact-head commit has zero check runs (`check-runs?per_page=100`: `total_count=0`), so it has no Hosted evidence yet.
- The active Demo main workflow at `2618b3962330509add5bf265522995da2a9034ce` has `pull_request` branches `[develop]` and path filters at `.github/workflows/pr-config-matrix.yml:4-19`; `tests/guided/**` is absent. Its only job runs `bash scripts/acceptance.sh config-matrix` at `:24-59`, so it does not execute the changed Guided regression tests.
- The develop copy has a `# DRAFT ONLY — owner-scope workflow addition; not committed or run.` header at line 1 and includes `tests/guided/**` at line 16, but its changed-path selector at lines 70-88 has no Guided case and falls back to `config-matrix`. That copy does not provide the requested test evidence for #183.
- `tests/gates.json:7-9` registers a `guided` acceptance gate and `scripts/acceptance.sh:260-266` dispatches it to `tests/guided/run.sh`; that runner includes runtime lifecycle work. The smallest test-only evidence for this PR is the focused unit suite in `tests/guided/test_consent_capture.py`, which exercises the changed `tests/guided/drive.py` helper without running the full runtime gate.

## Approval and impact

Card 0428-284 covers the Demo consent-retry/capture failure and links PR #183 (`tasks/t-20261125-0428-284-1812-postretry-gate-failure.md:17-18,50-63`). Its acceptance requires the minimal fix in the correct repo/file and exact-head evidence; line 63 says a `.github` change requires separate Owner authorization. That authorization exists in the Owner's W34 ruling (2026-11-26): purpose-bound minimal path selection in `baseharbor-demo` is covered for an approved card, with no product consent/auth change and no `baseharbor` core `ci.yml` change. This disposition applies that narrow authorization only to the tests added by #183.

PR #183 changes only `tests/guided/drive.py` and `tests/guided/test_consent_capture.py`. It changes no product source, consent decision, authentication/authorization path, secrets, permissions, or workflow file. The regression assertions retain fail-closed behavior for absent digest and foreign errors. A focused workflow job therefore adds test evidence without changing product behavior.

## Exact worker edit set

Worker assignment: card owner verbatim `w366-0428-284-democonsent`; implementation must use the worker's own canonical lane identity. Filesystem evidence review and scope decision author: `w255-0428-251-demo170codex`.

1. In the active default-branch `.github/workflows/pr-config-matrix.yml`, add `tests/guided/**` to the existing `pull_request.paths` list at lines 6-19. This lets a future PR event for guided test changes select the workflow.
2. Add one separately named read-only job, `guided-consent-unit`, that checks out `github.event.pull_request.head.sha` and runs `python3 -m unittest discover -s tests/guided -p 'test_consent_capture.py' -v`. This executes the regression suite covering the two files changed by #183 and gives it a distinct Hosted check. Keep the existing config-matrix job unchanged. Do not call `tests/guided/run.sh`, which includes the runtime lifecycle acceptance flow.
3. Keep workflow permissions at the current `contents: read`; add no secrets, service permissions, trigger branches, or unrelated paths. Do not edit BaseHarbor `ci.yml`, product code, consent/auth behavior, or any other workflow.
4. The workflow update must land through the approved workflow path before a fresh pull_request event is requested for #183. Until that exact-head Hosted job executes and succeeds, #183 remains unqualified.

## PLAN

1. Read the current default-branch workflow, the develop copy, card 0428-284, and the exact #183 diff/check state.
2. Classify the test-only CI inclusion against the existing card authorization and the W34 Owner ruling.
3. Record the worker-only edit set and the evidence still required after it lands.

## Provenance and identity

Plan repository remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.

Plan main base at review: `f25e06380b1be1e55d6ad6223ec7a635694facbd` (live remote ref checked before publication). Review commit author and committer: `w255-0428-251-demo170codex`. Commit invocation: `git -c user.name="w255-0428-251-demo170codex" -c user.email="w255-0428-251-demo170codex@baseharbor.local" commit -m "disposition(0428-284): PR 183 test-only CI inclusion"`. Identity gate: `git show -s --format=%an HEAD` must equal `w255-0428-251-demo170codex`.

Publication-base update: the note was drafted from Plan main `f25e06380b1be1e55d6ad6223ec7a635694facbd`; before publication, this branch fast-forwarded through the live Plan main to `0637bc3c01e55fdd5a940384618978fc12ad5780`. The draft base remains an ancestor. The review commit carries only this disposition file.
