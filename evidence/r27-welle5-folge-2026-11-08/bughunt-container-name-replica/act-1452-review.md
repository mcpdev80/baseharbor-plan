# CODEX-REVIEW 0427-128 container-name replica — PR #1452

## Verdict

ROLLE: REVIEW
URTEIL: korrektur (inhaltliche Abnahme ausgesetzt wegen rotem Hosted-CI-Gate)

## STATE: hosted CI failure

The live PR head is `c551fcd01a9276e2346624d47c689d2a562fd8e4`, base `develop` at `e39b0004346cdfd082e34ba55d94d24757bbbd27`. GitHub reports the PR open and mergeable. `gh pr checks` on this exact head reports `PR · Source format` failure and `PR Selected Checks` failure; the other required validation jobs shown here passed, while unrelated selected cells were skipped.

Exact failing log from run `42437310258`, job `PR · Source format` (`128598825185`):

```text
internal/runtime/container_identity_test.go
##[error]Process completed with exit code 1.
```

This is a hosted formatting failure. Under the workflow ownership boundary, the source review stops at this STATE and does not inspect or judge the candidate's implementation criteria yet. The claimed `go test ./internal/...` and `cli-guided-tests` successes do not replace the failed hosted check.

## Correction recipe

- File: `internal/runtime/container_identity_test.go`.
- Change: format the file with the repository's Go formatter (`gofmt -w internal/runtime/container_identity_test.go`) and commit the formatting correction on the existing PR candidate chain.
- Test requirement: allow the normal GitHub PR workflow to run on the resulting exact head; `PR · Source format` and `PR Selected Checks` must both pass. Do not rerun or dispatch workflows manually.
- Stop criterion: do not resume source-contract review until the exact new PR head has terminal green `PR · Source format` and `PR Selected Checks`. Then review planned-name derivation, quiesce diagnostics, cross-project collision coverage, and whether retirement/stop paths must use the same identity contract.

## Candidate and evidence provenance

- Exact PR head fetched from GitHub: `c551fcd01a9276e2346624d47c689d2a562fd8e4`.
- Exact PR base fetched from GitHub: `e39b0004346cdfd082e34ba55d94d24757bbbd27` (`develop`); `gh api repos/mcpdev80/baseharbor/pulls/1452` reported these head/base SHAs and `mergeable: true`.
- Exact-head hosted run: `42437310258`; Source format failed, PR Selected Checks failed.
- Round-1 evidence cited by the assignment: `evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/round-1.md`.
- Planning repository verified as `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `origin` fetch and push URLs are `https://github.com/mcpdev80/baseharbor-plan.git`.

END_DONE integration-1452-review: ROLLE REVIEW; CI STATE blocks source review at candidate `c551fcd01a9276e2346624d47c689d2a562fd8e4`.
