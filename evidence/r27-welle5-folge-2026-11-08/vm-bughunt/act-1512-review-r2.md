git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1512/head => fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 refs/heads/develop; 135c8be1abd80b7351432d7ffe0ffb886ace0d5f refs/pull/1512/head
gh pr view 1512 --repo mcpdev80/baseharbor --json state,mergeCommit => {"mergeCommit":null,"state":"OPEN"}

# CODEX-REVIEW 0427-175 r2 — PR #1512

ROLLE: REVIEW

URTEIL: KORREKTUR

## PLAN

1. Verify the live PR/develop refs, open/merged state, candidate ancestry, and exact-head terminal run.
2. Inspect the prior recovery-command and incomplete-registration findings against the new candidate.
3. Check the historical STATE claim using the cited commits and actual run evidence.
4. Publish the SHA-specific verdict and actionable correction recipe in this file.

## Exact remote state and hosted run

- `git ls-remote` returned develop `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` and `refs/pull/1512/head` `135c8be1abd80b7351432d7ffe0ffb886ace0d5f`.
- `gh pr view 1512 --json state,mergeCommit` returned `{"mergeCommit":null,"state":"OPEN"}`. The PR head is `135c8be1abd80b7351432d7ffe0ffb886ace0d5f`, branch `0427-175-initlock`, base branch `develop`.
- `origin/develop` is an ancestor of `origin/pr1512`; `git rev-list --left-right --count origin/develop...origin/pr1512` returns `0 5`. The current base integration is present.
- Run `42601589418` is terminal `completed/success` on this exact head: [run](https://github.com/mcpdev80/baseharbor/actions/runs/42601589418). `PR · Validation · go-unit-tests` (`129107210964`), `deployment-package-tests` (`129107211002`), source format and `PR Selected Checks` (`129111491334`) passed. Native destroy-retry Docker/Podman passed. Native Keycloak/Core and unrelated impact groups were skipped; they are not counted as passes.

## Prior STATE claim

The earlier assertion that `TestResolveRegisteredApplicationPropagatesOwnerStateNotNotFound` had the same failure on `1080ac444` and `32365b743` is not supported by the cited sources:

- GitHub resolves `1080ac444` to `1080ac444d4b7d0f1cf6d20d31b51d51519fbc7a`; that commit's tree does not contain `cmd/baha/app_context_owner_state_test.go`, so this named test could not have failed there. Its cited run `42558911822` is terminal success on `1080ac444`.
- GitHub API lookup for `32365b743` returns HTTP 422, “No commit found for SHA”; it is not a verifiable baseline.
- On current head `135c8be1a`, the test exists at `cmd/baha/app_context_owner_state_test.go:14-88`, and the exact-head `go-unit-tests` job passed. The current failure is resolved, but the asserted historical equivalence is not established and must not be repeated as fact.

## Remaining blocking review findings

The poisoned-registry recovery instruction still advertises a command that the CLI rejects:

- `internal/deployment/registry_conflict.go:26-36` emits `baha app destroy --uuid <id> --full-reset` as the repair for each duplicate.
- `cmd/baha/app_lifecycle.go:329-348` parses destroy arguments; `--uuid` reaches the generic unknown-option branch at lines 339-340.
- `cmd/baha/app_destroy_lifecycle.go:51-66` builds resolver arguments only from the positional name, so the destroy path does not forward an exact UUID to the resolved execution.
- `cmd/baha/app_registry_poison_recovery_test.go:146-200` exercises `status --uuid`, not `destroy`; it also accepts a registry-conflict error as a successful test outcome. The command-text assertion at lines 62-89 checks the wording, not that the advertised repair works. Therefore the diagnostic remains misleading and an operator cannot safely retire one twin by the promised route.

The concurrency proof also needs a tighter assertion. `TestConcurrentInitAcrossRealProcessesIsSerializedOrRefused` launches the re-exec process while the first writer is parked (`cmd/baha/app_init_concurrent_race_test.go:104-151`) and checks the final one-record count, but it ignores `childErr` at lines 156-162. If the child fails before attempting `SaveDeploymentRecord`, the test can still pass from the parent's single record. The separate incomplete-record classification test does not exercise a competing first registration during an interrupted/incomplete write, so the requested combined edge remains unproven.

## Actionable correction recipe and stop criteria

- In `cmd/baha/app_lifecycle.go` and `cmd/baha/app_destroy_lifecycle.go`, either implement UUID selection for destroy and carry the selected deployment identity unchanged through authorization, preflight and mutation, or replace the registry-conflict remediation text with a recovery command that is already supported and safe. Do not leave `--uuid` advertised while the parser rejects it.
- Add a poisoned-registry production CLI regression that executes the actual `app destroy --uuid <one-id> --full-reset` path. Verify the selected record is removed, the other twin remains byte-identical, and the subsequent list is healthy; also verify omission/invalid UUID remains fail-closed. Include a counterfactual assertion proving the regression fails when UUID parsing/routing is removed.
- In `cmd/baha/app_init_concurrent_race_test.go`, assert the child actually reaches the registration seam and exits with the expected duplicate/busy refusal (or explicitly validate an allowed convergence result); fail on unexpected child exit/panic instead of discarding `childErr`. Add the interrupted/incomplete-record versus competing-registration regression; assert the incomplete state is surfaced and no duplicate is persisted.
- Keep the current exact develop ancestry and obtain a new terminal exact-head run after those changes. Require the relevant unit/package checks and `PR Selected Checks` to pass; report skipped native gates as skipped, not green.
- Stop until the advertised repair is executable and proven, the race tests prove the contender outcome and partial-record boundary, and the corrected exact-head checks are terminal-success. No merge was performed.

## Repo-rule compliance

- Product repository and GitHub were read-only; no tests, reruns, workflow dispatches, approvals, or merges were performed.
- No `.github/**` files were changed.
- Evidence is in canonical baseharbor-plan, whose `origin` is `https://github.com/mcpdev80/baseharbor-plan.git`.

END_DONE 0427-175-r2-review: KORREKTUR PR #1512 head 135c8be1abd80b7351432d7ffe0ffb886ace0d5f; exact run 42601589418 succeeded and develop is an ancestor, but advertised `app destroy --uuid` is rejected and the recovery test only exercises `status --uuid`; the historical STATE claim about 1080ac444/32365b743 is unsubstantiated.
