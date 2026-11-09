# CODEX-REVIEW 0427-162 r4 — PR #1510

ROLLE: REVIEW

URTEIL: APPROVE

## PLAN

1. Verify the live PR head, base, current develop SHA, and exact-head CI run.
2. Compare only the r4 delta with the previously approved #1510 core and check the three recovery-hint changes.
3. Verify the new regression and its hosted CI selection.
4. Publish this review evidence before the authorized merge.
5. Merge by squash without force or bypass, then verify the new develop SHA and merge record.

## Candidate and delta

Repository: mcpdev80/baseharbor; PR #1510; task 0427-162.

- Exact PR head: 4ad2285f8d43dfbed59741903df5f8cd6f27a837.
- The immediately preceding approved head bc1a721e8e46ca82f81e978fc7c186bb135bf67a is the parent of this commit.
- The r4 delta is limited to cmd/baha/onboarding.go, cmd/baha/use_target.go, and cmd/baha/use_target_connection_test.go. The two production files change only the recovery-hint strings; no fail-closed selection, issuer verification, or persisted-state logic changed.
- Current develop is e072e142ec9511f3cc86ffa67c7debd022d7760a. PR API/run base is 942111d5a1c43f5257bf1627a966fa9e6c6f24bd, so develop advanced by #1505 after the hosted run's base. Git reports merge base 942111d5 and GitHub currently reports mergeStateStatus CLEAN / MERGEABLE. This drift is recorded for the landing check; the #1502 fail-closed core is already in the reviewed parent, and the intervening #1505 commit is outside the three-file r4 delta.

## Review findings

The formerly ambiguous plain `baha up` guidance now names the actual Core setup path at all five affected branches:

- cmd/baha/onboarding.go:201 directs onboarding recovery to `baha up --control-plane-only`.
- cmd/baha/use_target.go:91 and :98 direct missing or unverifiable installation recovery to the same command.
- cmd/baha/use_target.go:118 and :129 direct unavailable/unverifiable issuer recovery to the same command.

The flag is supported by the production CLI: cmd/baha/commands.go:78-79 documents `--control-plane-only` as the explicit management-Core setup mode, and cmd/baha/runtime.go:85 parses it.

The new `TestRecoveryHintNamesCoreSetupPath` at cmd/baha/use_target_connection_test.go:218-244 exercises missing and unreadable Core recovery through the onboarding identity resolver and the production `bindExplicitSelectionToConnection` seam. It asserts the typed conflict's recovery hint contains the actual Core setup flag at lines 277-287. It supplements, and does not weaken, `TestBindExplicitSelectionBindsWithoutLocalIssuerDir` and `TestBindExplicitSelectionFailsClosedOnAbsentCore`.

The new regression is included in `PR · Validation · go-unit-tests` on the standard pull_request run. Run 42594772123 completed successfully on the exact head. `PR Selected Checks` passed and its check run is from GitHub Actions app 15368. Build, vet, CLI gofmt, source format, and native impact selection passed. Native Keycloak/Core Docker and Podman and native destroy-retry Docker and Podman all executed and passed. Other jobs were skipped and are not counted as passes.

No new defect remains in this delta. The #172 fail-closed core approved on parent bc1a721e8 is unchanged.

## Merge authorization and stop criteria

Owner-authorized CODEX-MERGE is requested for this exact candidate using squash, with no force and no protection bypass. Before merge, recheck the remote PR head, terminal exact-head checks, and current develop. If any changes or a merge gate rejects the command, stop and record the exact response. After merge, verify refs/heads/develop and record the actual merge SHA and the genuine CI run link here.

## repo-rule compliance

- Product repository source and PR were read-only during review.
- No checks were rerun and no workflow files were changed.
- Evidence is in canonical baseharbor-plan, whose origin is https://github.com/mcpdev80/baseharbor-plan.git.

