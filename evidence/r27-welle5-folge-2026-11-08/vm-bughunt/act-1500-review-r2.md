# CODEX-REVIEW 0427-165 r2 — PR #1500

ROLLE: REVIEW  
URTEIL: KORREKTUR  
Reviewed PR head: `a14cf361d0d6bacfe2a4ab1a963d1a39e676583a`  
Parent: `cbc9e1a8736a1e0d18f81ffdd6a8db28d1416fb5`  
Base branch head: `20902f0a6ab016fd8fe6a501751e1becc5f334dd` (`develop`)  
PR: https://github.com/mcpdev80/baseharbor/pull/1500

## PLAN

1. Freeze the exact PR and base refs; inspect only the r2 delta against r1 findings.
2. Check each recovery command against the develop CLI and trace the orphan inventory and identity checks.
3. Verify test-to-CI routing and terminal hosted results, including the native-state classification.
4. Publish this review to Planning main and confirm the product candidate did not move.

## Findings

### Blocking: `destroy --all` is still advertised as a collector

The r2 delta removes the unsupported `baha app destroy --uuid ...` recommendation, but `cmd/baha/target_definition_change_plan.go:160,166` still tells operators to restore the Target, “collect” these records with `baha destroy --all`, and then detach again. The inline note itself says those records appear as `SKIPPED`.

I built the CLI from the fetched exact develop head `20902f0a6ab016fd8fe6a501751e1becc5f334dd` (`go build -buildvcs=false -o .review-baha ./cmd/baha`). Its `destroy --help` describes `--all` as full installation cleanup. In an isolated temporary state directory I created a Target and an ownerless deployment fixture, then invoked `destroy --all --yes --plain --no-input` against a deliberately nonexistent Docker socket. The command was accepted but stopped at native inventory with `selected Docker endpoint ... is unavailable; ... no fallback to System Docker`; this safely confirms the command enters the installation-wide inventory path, not a per-orphan selector. I did not run destructive cleanup against a real engine. The hosted/native source path independently confirms ownerless records become skipped in `cmd/baha/runtime_destroy_all.go:388-417`, while full destroy removes installation state.

Thus removing the `app destroy --uuid` clause fixed one false route, but the remaining route does not collect the named records. “Then detach again” is not an accurate recovery instruction after an installation-wide destroy. The command’s presence in `--help` is not proof that it performs this targeted cleanup.

### Blocking: identity checks still accept blank decoded identity fields

The new checks in `internal/deployment/deployment_list.go:171-175` reject non-empty UUID and Target mismatches. They only reject when the decoded value is non-empty, however, so a record with a missing or whitespace-only `DeploymentID` or `Target` is still appended at line 177, although it does not equal its canonical folder/target identity. This contradicts the contract stated in the comment at lines 160-170 and leaves malformed records eligible to be called collectable.

The new non-empty mismatch tests are present: `TestCollectableOrphansRejectsUuidFolderMismatch` (`internal/deployment/collectable_orphans_test.go:120`) and `TestTargetDeleteRefusalIgnoresUuidFolderMismatch` (`cmd/baha/target_definition_orphan_refusal_test.go:200`). The matching-folder positive test is at `internal/deployment/collectable_orphans_test.go:137`. These tests do not cover absent/blank UUID or Target fields. The fail-closed detach guard remains in place, but the collector’s classification is not strict canonical equality yet.

### Native jobs: record as STATE, never as green

Run `42532556867` is terminal failure on the exact reviewed head. `PR · Native Keycloak/Core · docker` (`128889795939`) and `… · podman` (`128889795877`) failed at 22:59:17Z and 22:58:56Z. `PR Selected Checks` (`128892604917`) is also failure. Both native destroy-retry jobs succeeded. The ordinary `go-unit-tests` (`128889795978`) and `deployment-package-tests` (`128889795968`) jobs succeeded.

The same two Keycloak/Core job names failed on the exact parent candidate `cbc9e1a8736a1e0d18f81ffdd6a8db28d1416fb5` in run `42519204316`: Podman completed at 20:18:55Z and Docker at 20:19:17Z. This is consistent with the supplied 0427-172 parked-state witness and is not evidence that r2 introduced the failure. I classify the native result as STATE: it remains red and blocks a green acceptance claim; it is not counted as pass and is not assigned as an r2 lane defect. The current `round-2-r2.md` identifies `TestControlPlaneSingleDefaultNativeRuntimeInCI` as the failed test, but the GitHub job annotations themselves only report process exit code 1; I could not independently verify that test-level detail from the hosted annotations. The owner’s 172 incident record remains the source for precise cause attribution.

### CI routing and base provenance

The new mismatch and command regressions are in packages executed by the exact-head pull-request run: `go-unit-tests` passed and `deployment-package-tests` passed. The latter job’s log selected `./internal/deployment`; the command tests are in `cmd/baha`, included in the package-wide Go unit job. These tests were executed, not skipped. This supports their CI routing, but does not waive the two failed native jobs or the failed aggregate check.

The live refs are `develop=20902f0a6ab016fd8fe6a501751e1becc5f334dd` and `PR #1500=a14cf361d0d6bacfe2a4ab1a963d1a39e676583a`. `develop` is not an ancestor of the PR head: merge-base is `128e6f50b538cb6ba2925432740aa37014fcc09a`. The PR remains open and GitHub reports `MERGEABLE`, `UNSTABLE`. This is base drift, not a mergeability claim; recheck the diff and rerun required checks on the final rebased head before acceptance.

Planning now provides `round-1.md`, `round-2.md`, and `round-2-r2.md` under `evidence/r27-welle5-folge-2026-11-08/bughunt-target-delete-orphan-records/`. The r2 dossier correctly records that `destroy --all` skips ownerless records, then incorrectly calls it the “honest collect path” and says the refusal text is restricted to paths that collect. The source still says “collect” and “then detach again” at lines 160 and 166, so the dossier’s conclusion does not match either its own finding or the candidate. Source and hosted-run checks above were independently performed against the live candidate.

## Actionable correction recipe

1. In `cmd/baha/target_definition_change_plan.go:160,166`, stop claiming that `baha destroy --all` collects these individual ownerless records. State the actual supported recovery prerequisite. If there is no safe targeted collector, say that no supported per-record recovery command exists and keep the Target attached for operator recovery. Do not present full installation destroy as a targeted cleanup route.
2. In `internal/deployment/deployment_list.go:171-177`, require decoded `DeploymentID` and `Target` to be present and exactly match the canonical directory UUID and requested target before appending a record. Preserve the detach refusal for every malformed or mismatched identity.
3. Add regressions for missing and whitespace-only UUID and Target fields, in addition to the existing non-empty mismatch and matching-identity cases. Assert that malformed records are never listed as collectable, the Target remains attached, and no record/state is modified.
4. On the final exact PR head, confirm those regressions run in `go-unit-tests` and `deployment-package-tests`. Confirm the recovery guidance against the actual command entry and resulting state. Rebase onto the fetched current develop head and rerun the required jobs. Stop only when ordinary required checks and `PR Selected Checks` are terminal success; continue to label the 0427-172 native failures as STATE until the owner-documented incident is resolved or explicitly waived. Do not call skipped or failed native work green.

## Provenance and publication

Product remote witness before Planning publication:

```text
20902f0a6ab016fd8fe6a501751e1becc5f334dd	refs/heads/develop
a14cf361d0d6bacfe2a4ab1a963d1a39e676583a	refs/pull/1500/head
```

Planning checkout: `/tmp/opencode/0427-165-review-wt`, remote `https://github.com/mcpdev80/baseharbor-plan.git`; fetched `origin/main` was `4261e444bbbf8449054813dbcf16111d0a13e542` before this evidence commit.

END_DONE 0427-165-review-r2: KORREKTUR — recovery guidance remains non-collecting and malformed blank identities remain admitted; native 172-related jobs are red STATE, not green. Candidate `a14cf361d0d6bacfe2a4ab1a963d1a39e676583a`.
