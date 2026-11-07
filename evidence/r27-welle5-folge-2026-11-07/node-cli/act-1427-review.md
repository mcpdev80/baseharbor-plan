# CODEX-REVIEW 0427-node-cli-r2 — PR #1427

## PLAN

1. Read mission, mandatory coordinator authorization files, task contract, and product rules — DONE.
2. Fetch exact PR and base refs; verify ancestry, implementation, write-set, tests, and hosted CI without changing the candidate or rerunning CI — DONE.
3. Record SHA-specific verdict and actionable recipe in canonical baseharbor-plan evidence — DONE.
4. Publish evidence to origin/main, verify candidate and evidence witnesses, then post END — IN PROGRESS.

## Review identity

- Role: CODEX-REVIEW only; no merge, candidate mutation, local test run, or CI rerun.
- Task: `t-20261018-r27-node-cli`, card 0427-039.
- Product: `mcpdev80/baseharbor`, PR #1427.
- Candidate head: `0dc4c4d4f3e8c27bc9d48019d0b210807d45f951`.
- Exact fetched base `develop`: `06e4b1eaa01fe10b3edb5f0ca59ce5232d110156`.
- Planning repository verification before evidence commit: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` returned `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` showed `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push. The canonical planning clone is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, not `workers/baseharbor-plan`.

## Verdict: REQUEST-CHANGES

The two-file write-set and candidate ancestry are clean, and the required hosted Go unit/build/vet checks pass. However, the new `node list` state is derived only from local records whose `Enrolled` and `ExpiresAt` are never populated, so it reports PENDING after enrollment and cannot show live expiry or revocation. `node status` calls Core, but its current status response does not include the serial or capabilities the new client code attempts to decode. No changed regression tests cover these new client behaviors. The implementation therefore does not yet satisfy the task's live trust and capability surface or its fail-closed behavior requirements.

### Exact refs and provenance

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1427/head` returned:

  ```text
  06e4b1eaa01fe10b3edb5f0ca59ce5232d110156 refs/heads/develop
  0dc4c4d4f3e8c27bc9d48019d0b210807d45f951 refs/pull/1427/head
  ```

- Fetched `develop` and PR head into `/tmp/opencode/0427-node-cli-r2-review-wt`. `git merge-base --is-ancestor 06e4b1eaa01fe10b3edb5f0ca59ce5232d110156 refs/remotes/origin/pr/1427` returned `0`.
- `git log --format='%H %an %s' 06e4b1eaa01fe10b3edb5f0ca59ce5232d110156..refs/remotes/origin/pr/1427` lists exactly one commit, the candidate commit: `0dc4c4d4f3e8c27bc9d48019d0b210807d45f951 Worker w280 feat(node): surface live trust/expiry/capabilities (PR#1427, drift-free on 06e4b1e)`.
- `git diff --name-status develop...head` contains exactly `M cmd/baha/node.go` and `A cmd/baha/node_read.go`. No #110 lifecycle/fixture, maintenance, `.github/**`, or unrelated files are changed.
- GitHub PR API reports OPEN, base `develop`, head exactly `0dc4c4d4f3e8c27bc9d48019d0b210807d45f951`, mergeable `MERGEABLE`, merge state `CLEAN`.

### Acceptance review

1. **List/status state coverage: FAIL.** `cmd/baha/node.go:61-62` adds `nodeRecord.Enrolled` and `ExpiresAt`, but the only `saveNodeRecord` call is `node.go:202-207`, where neither field is assigned. `cmd/baha/node_read.go:43-49` reads that record and silently leaves the list item at zero values when the record is missing or invalid. `node_read.go:59-65` consequently displays PENDING for normal records and does not surface live Core state in the list. It cannot report REVOKED there. The status command does map Core `revoked`, `enrolled`, and expiry into REVOKED/ENROLLED/EXPIRED/PENDING at `node_read.go:93-100`.
2. **Capabilities, serial, and fail-closed evidence: FAIL.** `node_read.go:160-166` tries to decode optional `capabilities` from the Core response. The current Core status handler at `internal/targetenrollment/http.go:221-229` returns contract version, target/node identity, runtime, enrolled, revoked, and expiry only; it sends neither serial nor capabilities. `internal/targetenrollment/authority.go:69-74` also tags `NodeStatus.Serial` as `json:"-"`. The new capability parser therefore cannot produce the promised live capability surface against the current API. In addition, `node_read.go:44-48` suppresses local record errors and emits a misleading PENDING state rather than surfacing unknown/unavailable metadata. No causal tests were added for valid status variants, capability mapping, mismatched identity, malformed responses, expired/revoked state, or authority failure.
3. **Write-set: PASS.** Exactly `cmd/baha/node.go` and `cmd/baha/node_read.go` changed; the diff does not include the #110 lifecycle/fixture files, `cmd/baha/node_install.go`, maintenance files, or `.github/**`.
4. **Hosted CI capture: PASS for the selected Go checks; native runtime jobs skipped.** Run `42392156346` completed `success` on the exact candidate SHA. `PR · Validation · go-unit-tests`, `go-build`, `go-vet`, `PR Selected Checks`, `PR · Trusted Plan`, `PR · Source format`, `PR · Focused Python`, and `Workflow policy` passed (8 successful checks). The Go unit job ran rather than being skipped. Docker and Podman Targeted HA and path-unrelated checks were skipped; no CI rerun was triggered. Because the current patch is a CLI read-path change, the mission's selected CI requirement is the Go unit job; the absent behavioral tests remain a code/evidence gap despite the green package job.
5. **No weakening: PASS by diff inspection.** The candidate changes only the node CLI source files and does not modify tests, workflows, runtime policies, or other stack expectations.

## Actionable recipe

- **Files and changes:** In `cmd/baha/node_read.go:35-49`, source list state from the authoritative Core lifecycle status (or represent unavailable/unknown explicitly); do not convert missing/corrupt local records into PENDING. In `cmd/baha/node.go:202-207` and the node record contract, persist only the local enrollment metadata that is actually authoritative and available. The existing Core status response at `internal/targetenrollment/http.go:221-229` does not publish serial or capabilities, and `internal/targetenrollment/authority.go:69-74` intentionally omits serial from JSON. Use an already-authorized public contract or obtain an explicit scope/contract update before changing those API files; the current two-file slice cannot surface fields the authority does not return. Include disconnect reason only if the accepted authority contract supplies it.
- **Tests:** Add focused tests under `cmd/baha/node*_test.go` for PENDING, ENROLLED, EXPIRED, and REVOKED; capability and expiry mapping from the real status schema; unavailable Core, malformed JSON, identity mismatch, and unreadable local metadata remaining explicit errors/unknown rather than success-shaped PENDING. Include causal negative variants that change each authoritative field and prove the displayed result changes accordingly. Keep them in `cmd/baha` so the existing hosted `PR · Validation · go-unit-tests` (`go test ./...`) executes them on pull-request changes.
- **Stop criterion:** Do not approve until the exact candidate provides authoritative list/status state and capability fields under the accepted contract, fail-closed regressions pass in hosted Go unit CI, the write-set remains within the assigned node slice (or scope is explicitly updated for shared API ownership), and the PR head remains ancestry-clean against fetched `develop`.

## Repository-rule compliance

- Review was read-only for the product repository and PR. No local tests, candidate changes, CI reruns, merge, VM smoke test, or workflow changes were performed.
- No Docker/Podman project or runner infrastructure was started or changed.
- Evidence is stored only in the canonical `baseharbor-plan` repository. This file contains no Markdown checkbox syntax.

## END

END_BLOCKED 0427-node-cli-r2-review: REQUEST-CHANGES; candidate 0dc4c4d4f3e8c27bc9d48019d0b210807d45f951 is ancestry-clean and selected hosted Go CI is green, but node list is permanently PENDING from unset local fields, Core status omits serial/capabilities, and new client behavior has no regression tests.
