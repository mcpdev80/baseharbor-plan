# CODEX-REVIEW 0427-003 Quarkus adapter — PR #1429

## PLAN

1. Read mission, canonical task contract, relevant repo rules, and prior evidence; identify exact review scope — DONE.
2. Fetch exact live product refs and inspect candidate ancestry, changed files, code, tests, and hosted checks — DONE.
3. Assess healthcheck path, readiness proof, write-set, CI capture, and preservation of other stack expectations — DONE.
4. Write SHA-specific verdict and actionable recipe, publish this planning evidence, verify remote witnesses, then post END — DONE.

## Review identity

- Lane: `0427-003-quarkus-review`.
- Role: CODEX-REVIEW only; no merge, candidate mutation, local test run, or CI rerun.
- Product: `mcpdev80/baseharbor`, PR #1429, slice `core-815`.
- Candidate head: `0743011cfa5d9bd260d4a347ab94a6049ce960a2`.
- Live base `develop`: `812c99c8873df400348fbc8cc9be5e650b8966c4`.
- Planning repository verification: `git rev-parse --show-toplevel` returned `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git remote -v` showed `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push. No evidence was written to a product repository.

## Verdict: REQUEST-CHANGES

The Quarkus source change is correctly scoped and points Compose healthchecks at Quarkus's `/q/health` endpoint. Its regression test checks for that URL in generated Compose text, but does not prove that `baha up` transitions to READY with the healthcheck and stays non-ready without it. The exact hosted run passed unit CI, but the Docker and Podman Targeted HA jobs were skipped. The existing round-3 report's claim that those two jobs succeeded conflicts with GitHub's exact run data.

This verdict is limited to the Quarkus code slice. Core-815 remains active for its broader four-stack and native-runtime acceptance, including separate Podman and other-stack work.

### Exact refs and provenance

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1429/head` returned:

  ```text
  812c99c8873df400348fbc8cc9be5e650b8966c4 refs/heads/develop
  0743011cfa5d9bd260d4a347ab94a6049ce960a2 refs/pull/1429/head
  ```

- Fetched both refs into `/tmp/opencode/0427-003-quarkus-review-wt`. `git merge-base --is-ancestor refs/remotes/origin/develop refs/remotes/origin/pr/1429` returned `0`; merge-base is the exact fetched develop SHA.
- `git log --format='%H %an %s' develop..head` lists one candidate commit: `0743011cfa5d9bd260d4a347ab94a6049ce960a2 Worker 0427-003-greenfield-stacks fix(quarkus): emit compose healthcheck (/q/health) so baha up reaches readiness`.
- PR API: OPEN, base `develop` at `812c99c8873df400348fbc8cc9be5e650b8966c4`, head `0743011cfa5d9bd260d4a347ab94a6049ce960a2`, mergeable `true`, merge state `clean`.

### Acceptance review

1. **Healthcheck endpoint and adapter consistency: PASS by source inspection.** `internal/development/quarkusadapter/adapter.go:59` declares the Quarkus health action as `/q/health`; the ExposureHTTP plan includes `io.quarkus:quarkus-smallrye-health` at line 67. The generated Compose healthcheck uses `127.0.0.1:8080/q/health`, and sets `PORT` to `8080`, matching the generated application configuration. Go, Next.js, and Python adapters use their own `/healthz` route and corresponding healthcheck command; those files are unchanged.
2. **Readiness regression proof: INCOMPLETE.** `internal/development/quarkusadapter/adapter_test.go:13-41` extends `TestQuarkusRoundTrip` to assert that generated `compose.yaml` contains `/q/health`. This is a useful generation-level regression and would fail against the prior generated Compose output, but it does not exercise the health response, Compose health state, or `baha up` READY behavior. It therefore does not establish the mission's requested behavioral red-without/green-with-healthcheck proof.
3. **Write-set: PASS.** The full diff against fetched develop contains exactly `internal/development/quarkusadapter/adapter.go` and `internal/development/quarkusadapter/adapter_test.go`. No other stack adapter, lifecycle/fixture, script, or `.github/**` file changed.
4. **Hosted CI capture: PARTIAL.** Run `42387327608` completed `success` on exact head `0743011cfa5d9bd260d4a347ab94a6049ce960a2`. `PR · Validation · go-unit-tests` passed (9m10s), as did go-build, go-vet, source format, workflow policy, focused Python, trusted plan, and selected checks. The adapter regression is in the Go package suite executed by the hosted `go-unit-tests` check on pull-request events. However, `Targeted HA · docker` and `Targeted HA · podman` both show `skipped`; no runtime readiness result exists in this run. The prior `greenfield-stacks/round-3.md` says both completed successfully, which contradicts the exact run's current GitHub job results. No rerun was triggered.
5. **Other stack expectations: PASS.** Only Quarkus adapter and its test changed. No existing Go, Next.js, Python, or Podman expectations were altered or weakened.

### CI routing boundary

The unit regression is durably covered by `PR · Validation · go-unit-tests` (`go test ./...`) on pull-request events, so no workflow edit is needed for that test. A real `baha up` readiness cell is not selected by this PR run: `.github/workflows/ci.yml:171-176` gates the Docker Targeted HA job to pushes on `runtime-validation/ha/...`, and lines 191-199 list supported HA groups without Quarkus; the Podman job has the analogous push-only gate at lines 213-240. If the readiness acceptance is implemented as a native runtime test, the Owner must wire a Quarkus greenfield startup check into the appropriate CI group/trigger. This review does not edit owner-owned workflow files.

## Actionable recipe

- **File and change:** In `internal/development/quarkusadapter/adapter_test.go`, add a regression that validates the rendered healthcheck configuration and demonstrates the readiness behavior when the check is absent versus present. Keep `/q/health`, the matching port, and the generated SmallRye Health dependency aligned. Do not change other adapters.
- **Test requirement:** Preserve the current generated-file check in hosted `go-unit-tests`. Add or use a Quarkus startup acceptance that runs `baha up` and observes READY with this healthcheck, plus the negative case without it. The native runtime result must be captured by a CI job as well as any smoke validation. The run cited for this SHA has no such result because both Targeted HA jobs were skipped.
- **Owner-scope CI finding:** If a native Quarkus test is added, the required trigger/selection change is in `.github/workflows/ci.yml` around lines 171-199 for Docker (and 213-240 for Podman if brought into this scope). The Owner must add the Quarkus greenfield path/group to a hosted CI route; this review does not edit `.github/**` or dispatch a workflow.
- **Stop criterion:** Keep the verdict at request-changes until the exact healthcheck is shown to drive Quarkus `baha up` to READY, the no-healthcheck case is red, and the applicable hosted job actually executes and passes on the candidate SHA. Do not infer a runtime pass from the generated-text assertion or from skipped job status.

## Repository-rule compliance

- Review was read-only for the product repository and PR; no local tests, candidate changes, merges, or CI reruns were performed.
- No workflow was edited or dispatched; no runner infrastructure or VM was touched.
- Evidence is stored only in the verified `baseharbor-plan` repository. This evidence file contains no Markdown checkbox lines.

## Planning publication note

The shared planning checkout contained an unrelated unpublished coordinator commit; it was preserved and excluded. This review was published from a clean checkout of the canonical `baseharbor-plan` origin.

## END

END_BLOCKED 0427-003-quarkus-review: REQUEST-CHANGES; candidate 0743011cfa5d9bd260d4a347ab94a6049ce960a2 is ancestry-clean with hosted unit CI green, but the test proves generated URL text only and the exact run skipped Docker and Podman runtime gates.

Remote publication witness from `git ls-tree -r origin/main --name-only | rg '^evidence/r27-welle5-folge-2026-11-07/core-815-quarkus/act-1429-review\.md$'`:

```text
evidence/r27-welle5-folge-2026-11-07/core-815-quarkus/act-1429-review.md
```
