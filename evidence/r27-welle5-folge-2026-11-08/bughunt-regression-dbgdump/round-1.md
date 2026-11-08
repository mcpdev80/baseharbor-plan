# t-20261108-bughunt-0427-regression-debug-dump-consent (0427-129)

VERIFIED-NO-CHANGE. develop build `07ae6c3e91` (fix-merge HEAD for this wave) already contains the debug-stack removal from PR #1439 (`449f107ffc`), the regression from card 0427-120 is fixed on develop, and the focused regression test passes. No code change, no PR.

## PLAN

- Read mission-129.md and the task card
- Fetch develop, build develop-head
- Confirm whether develop still dumps the runtime stack on missing consent
- Verify PR #1439 (#1439) is the removal commit and is merged into develop
- Run the focused regression + consent test suite green
- Commit evidence, END

## Base attestation

Planning repo (authoritative, per AGENTS.md worker rules). The planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin
e6b26ac982f074016ba4c03d918910149f770796 HEAD
e6b26ac982f074016ba4c03d918910149f770796 refs/heads/main
```

origin/main HEAD: `e6b26ac982f074016ba4c03d918910149f770796`

Product base (baseharbor), measured via `git ls-remote origin` (NOT the quarantined workers/baseharbor checkout):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin
...
07ae6c3e91b081a189266ca4b162ba705d4aa78f HEAD (-> refs/heads/develop)
$ git ls-remote origin refs/heads/develop
07ae6c3e91b081a189266ca4b162ba705d4aa78f  refs/heads/develop
```

develop HEAD (base I inspected): `07ae6c3e91b081a189266ca4b162ba705d4aa78f`.

## Investigation result

Step 1 — IST (does develop still dump the stack on missing `--confirm-candidate`?):

Checked `cmd/baha/deployment_record.go` on develop `07ae6c3e91`. The consent-refusal branch no longer calls `runtime.Stack` / `fmt.Fprint(os.Stderr, ...)`. Import of `runtime` is gone. The current code is:

```
consent, consErr := finalizeCandidateConsent(rawCandidateConsent, "operator", submission)
if consErr != nil {
    return deployment.DeploymentRecord{}, consErr
}
if consent == nil {
    return deployment.DeploymentRecord{}, errConsentRequiredForCandidateSubmission
}
```

No debug dump is emitted. Build + vet + tests run against develop HEAD in `/tmp/opencode/mission-129-base` (worktree, not the quarantined checkout):

```
$ go build ./...
(exit 0)
$ go vet ./cmd/baha/
(exit 0)
$ go test ./cmd/baha/ -run TestMissingCandidateConsentDoesNotDumpRuntimeStack -v
--- PASS: TestMissingCandidateConsentDoesNotDumpRuntimeStack (0.01s)
PASS
ok      github.com/mcpdev80/baseharbor/cmd/baha	0.014s
```

Step 2 — ancestry / PR #1439:

```
$ git -C .../baseharbor log --oneline --all --grep="1439"
32ce55dd5 Merge pull request #1439 from mcpdev80/fix/0427-120-cli-consent-output
449f107ff fix(cli): remove debug stack dump from missing candidate consent
```

PR #1439 = commit `449f107ffc11993952182a8889460dab88047f71` `fix(cli): remove debug stack dump from missing candidate consent`, merged into develop 2026-11-08 (22 checks passed, GitHub PR #1439 page confirms "Merged ... into develop"). It removed exactly:

```
-			var buf [4096]byte
-			n := runtime.Stack(buf[:], false)
-			fmt.Fprint(os.Stderr, string(buf[:n]))
```

from the `if consent == nil` branch, and dropped the `runtime` import.

Ancestry proof:

```
$ git -C .../baseharbor merge-base --is-ancestor 449f107ffc11993952182a8889460dab88047f71 origin/develop && echo YES
YES - 449f107ffc11993952182a8889460dab88047f71 IS ancestor of develop
```

The exact fix commit `449f107ffc11993952182a8889460dab88047f71` is an ancestor of `origin/develop` `07ae6c3e91b081a189266ca4b162ba705d4aa78f`.

## Verdict

Card is VERIFIED-NO-CHANGE. develop `07ae6c3e91` already includes PR #1439's debug-stack removal. The 0427-120 regression is fixed; `baha up` without `--confirm-candidate` fails closed with `errConsentRequiredForCandidateSubmission` and emits no `goroutine`/`runtime.Stack` line. Acceptance criterion "stderr contains no goroutine line" holds on develop. No code change, no PR required.

Out of scope (untouched): consent semantics and exit codes, per card scope.

## CI / regression coverage

- Test: `TestMissingCandidateConsentDoesNotDumpRuntimeStack` in `cmd/baha/app_candidate_consent_test.go:256` (develop). Asserts `recordDeploymentBeforeMutation(... "applying", "")` fails closed with `errConsentRequiredForCandidateSubmission` and that stderr contains neither `goroutine` nor `runtime.Stack`.
- Positive/negative proof: ran locally on develop HEAD `07ae6c3e91` above (PASS). The negation is the removed code path — the pre-#1439 build would emit the stack and fail this assertion.
- CI gate + trigger (state only, per Owner directive 2026-11-07 — `.github/**` is Owner scope, not edited): this test lives in `cmd/baha/` and is picked up by the standard Go `go test ./...` job on the CI group that runs `cmd/baha` unit tests (develop integration + selected PR paths). The exact workflow file / trigger selection is Owner-owned; if the covering group's trigger does not currently run `cmd/baha` unit tests, that is a coverage gap to be closed by the Owner, not by this lane.

## Drift / cleanliness

- Single integration candidate expected per chain (AGENTS 3.8). This card is VERIFIED-NO-CHANGE, no branch cut, no PR. No drift to merge.
- No worktree or compose project to tear down.

## repo-rule compliance

- No subagents used (AGENTS 4.8). Every step run inside this session.
- No `.github/**` edits, no workflow dispatch, no reruns.
- Remote state measured only via `git ls-remote origin` and fresh worktrees under `/tmp/opencode/`; the quarantined `workers/baseharbor` checkout was never cited.
- Evidence written only into the planning repo (`baseharbor-plan/evidence/...`), never into a product repo.

## END

STATE: VERIFIED-NO-CHANGE mission-129.md. develop `07ae6c3e91` contains PR #1439 debug-stack removal (`449f107ffc` ancestor of develop); focused regression `TestMissingCandidateConsentDoesNotDumpRuntimeStack` PASS; build + vet clean. No PR. Resolution: close as VERIFIED-NO-CHANGE (no change needed).
