# 0428-253 owner ruling and admission note

## PLAN

1. Verify current origin/main and the live 0428-253 task owner.
2. Add the exact owner-approved admission sentence to the existing task note, keep its owner field unchanged, and record the scoped Owner ruling in the card body.
3. Record the authorship boundary verbatim and provenance in this akte.
4. Prove current-base ancestry and one-card-plus-akte diff; commit under the executing lane's canonical identity and verify author/committer.
5. Publish one Plan PR, wait for exact-head Hosted Plan validation, merge under scoped authority, and record the post-merge witness.

## Exact admission note

Erste zwei Übernahmen als gekürzte Identität der eigenen Bahn übernommen (w205 ≙ w205-0428-253), Eigentümer-Erkenntnis 25.11., keine Umschreibung.

## Owner boundary (verbatim)

admissible ONLY where authorship is conclusively the SAME lane with shortened canonical formatting; a FOREIGN lane identity is NOT admissible and goes through Coordinator recovery/republication; the exception is NOT generalized.

## Identity and provenance

Card frontmatter owner verbatim: `w205 (lane w205-0428-253)`; the owner field remains unchanged.

Executing reviewer lane and commit author: `w255-0428-251-demo170codex`.

Git user.name: `w255-0428-251-demo170codex`.

Git user.email: `w255-0428-251-demo170codex@baseharbor.local`.

Commit invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit -m 'docs(0428-253): record shortened identity ruling'`.

Pre-push author/committer gate: `git show -s --format=%an%n%cn HEAD`; both lines must equal `w255-0428-251-demo170codex`.

The owner-authorized card content distinguishes the historical same-lane shortened formatting from foreign-lane authorship. The text does not authorize putting `w205-0428-253` in new commit metadata.

Plan repository remotes were verified as:

```text
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The branch is rebased onto current `origin/main` `053b2b6d1af11ad0f926949ef39c7fdbf0e400bf`. The target task path has no intervening commits from the prior fetched base `76ab859144661e7fdabdc10e36b9cee5f3ce99ad` to current main. Hosted Plan validation will be recorded after the PR runs.

## Current local state

The exact task sentence and Owner ruling are prepared on a branch based on current main. No commit or push has occurred yet. END DONE will be recorded after the merged readback.

## Publication status

Hosted Plan validation must succeed on the exact final PR head. The Plan PR number and actual hosted run are recorded in the final handoff; the post-merge task-note readback is captured there as well.

## END

END w255-0428-251-demo170codex DONE

Planning precheck: `python3 scripts/plan.py render` and `python3 scripts/plan.py check` completed successfully with 0 errors and 10 existing dependency warnings. Render touched an unrelated generated task note, which was restored to the current base so the publication remains limited to the requested card and this akte.

publication under the executing reviewer lane's own canonical identity per the coordinator's written correction; card owner w205-0428-253 remains unchanged; executing reviewer lane: w255-0428-251-demo170codex.

## Candidate provenance before Plan PR

- Current origin/main at commit time: `053b2b6d1af11ad0f926949ef39c7fdbf0e400bf`.
- `git merge-base --is-ancestor origin/main HEAD` exited 0.
- `git log --oneline origin/main..HEAD` before this provenance update listed only `5796f99ae docs(0428-253): record shortened identity ruling`, authored and committed by `w255-0428-251-demo170codex`.
- `git diff origin/main...HEAD --name-only`:

  ```text
  evidence/w255-0428-253-authorship-boundary/akte.md
  tasks/t-20261123-planner-deleted-source-advisory.md
  ```

- Initial push witness for branch `w255-0428-253-admission`:

  ```text
  5796f99aeeed2bdace38a6fe66d849fe03d01e0f refs/heads/w255-0428-253-admission
  ```

Second push delivery witness:

```text
2bf9101dcdcbe82ab619415c32763f0b2dc78020 refs/heads/w255-0428-253-admission
```

## Hosted validation witness

Plan PR #68 head `a3f01dea035432376641f2eea485b54131c3a23e` was validated by Hosted run `45734311673` (`pull_request`, conclusion SUCCESS). The executed job was `Plan · validate` and its required steps, including unit tests and vault/generated-file validation, succeeded. Run: https://github.com/mcpdev80/baseharbor-plan/actions/runs/45734311673. This run validates the note and ruling; the PR will also validate the final akte update on its new exact head.
