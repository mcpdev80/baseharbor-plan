# 0427-162 round-4 — recovery hint names `baha up --control-plane-only` for Core setup

Shift: worker (worker-ornith1.5-laptop) · Date: 2026-11-09
Card: t-20261108-bughunt-app-list-owner-check-scaling (0427-162)
Mission: /tmp/opencode/mission-162-r4.md
Branch: `lane/0427-162-r3` on PR #1510
Base: `bc1a721e8e46ca82f81e978fc7c186bb135bf67a` (PR #1510 head, the reviewed r3 candidate). `942111d5a1c43f5257bf1627a966fa9e6c6f24bd` (develop) is an ancestor of the branch base and of my fix commit `4ad2285f8`.
Plan repo origin/main HEAD: `34c61cc1fe065979aa1506ea1306bd6bd7e57c35` (pinned before first evidence commit; planning main is actively rewritten by the Coordinator)
Repo: mcpdev80/baseharbor (product), worktree `/tmp/opencode/0427-162-r4-wt`

## PLAN

- Round out PR #1510 (KORREKTUR block from act-1510-review.md): the recovery hint promised a plain, cwd-dependent `baha up`, which inside an Application repository runs application-lifecycle handling and does NOT set up the Management-Core.
- Replace all hint sites with the actual Core-setup path `baha up --control-plane-only`; no text may promise a command the application cannot fulfill.
- Add a CI-covered CLI regression that for a missing AND unreachable Core checks the emitted repair hint names `--control-plane-only`.
- Keep the content delta minimal (only the three affected files); keep existing tests green.
- Hosted run terminal on the exact fixed head; skipped as skipped; ls-remote + cleanliness.

## Fix (content delta)

Files: `cmd/baha/use_target.go` (hint sites 91, 98, 118, 129) and `cmd/baha/onboarding.go` (hint site 201).

- Every recovery hint previously read `(baha up)` / `baha up` — a bare command whose effect is cwd-dependent: inside an Application repository `baha up` is application-lifecycle handling (cmd/baha/commands.go:76-80, runtime_repository_up.go:14-17,35-46) and does not install the Management-Core.
- All five sites now name the explicit Core-setup command: `baha up --control-plane-only`. No remaining bare `baha up` recovery hint exists in cmd/baha (`grep "(baha up)"` / `grep "baha up"` against cmd/baha returns no recovery-hint matches).
- Wording kept otherwise byte-identical (target/issuer phrasing unchanged); only the command token changed.

## Test (CI-covered regression)

New test `TestRecoveryHintNamesCoreSetupPath` in `cmd/baha/use_target_connection_test.go`:

- Missing Core (`coreinstallation.Load` -> os.ErrNotExist) on BOTH seams: the onboarding seam (`boundManagementConnectionIdentity`) and the production `baha use` seam (`bindExplicitSelectionToConnection`, use_target.go) return a typed conflict whose `Next` hint names `--control-plane-only`.
- Unreachable/unverifiable Core (genuine installation whose runtime root is made unreadable via `os.Chmod(runtimeRoot, 0000)`) fails closed at the same recovery hint and also names `--control-plane-only`.
- The assertion requires `--control-plane-only` present AND forbids a bare cwd-dependent `baha up` as the only recovery.
- Existing tests untouched and green: `TestBatchedListClassifiesAccessForeignMissing` (covers resolver-injection, not this file-seen case), the positive Keycloak-bound selection `TestBindExplicitSelectionResolvesKeycloakCoreIssuer`, and the missing-core fail-closed counter-tests `TestBindExplicitSelectionFailsClosedWithoutCore` / `TestBindExplicitSelectionFailsClosedOnAbsentCore` all still pass.
- Negative-verified: reverting any affected hint site to a bare `baha up` makes the test fail (asserts the guard is real, not a tautology).

### CI coverage statement

- The new test lives in `cmd/baha/` and runs in the normal `go-unit-tests` job (`go test ./...`), ci.yml:338 "Run unit and package tests".
- Job `PR · Validation · go-unit-tests` for run `42594772123` on head `4ad2285`: executed, **success** — no `.github/**` change was needed; the existing go-unit-tests group already covers `cmd/baha/`.
- Trigger: `pull_request` on PR #1510 (base develop), selected by the CI PR path matrix. No Owner-scope workflow edit required.

## Hosted CI (witnessed, terminal)

- PR #1510 head `4ad2285f8d43dfbed59741903df5f8cd6f27a837` (branch `lane/0427-162-r3`), base develop `942111d5a`, open, mergeable.
- Run `42594772123` `CI · PR #1510`: **completed / success**, head `4ad2285`.
- Job summary: 14 success (executed), 11 skipped, **0 failure/cancelled**.
- Executed (not skipped): `go-unit-tests`, `go-build`, `go-vet`, `cli-gofmt`, source-format, trusted-plan, focused-python, native impact-selection, native destroy-retry docker/podman, native Keycloak/Core docker/podman.
- Skipped (correctly not counted): consumer pins, demo pin, public contracts, runner interface, selected runtime, exact-candidate, Targeted HA docker/podman, `validate` (go test ./..., PR path-selected skipped — same as the r3 run 42583974762).
- My new test executed within go-unit-tests (success).

## Drift against develop HEAD

- Branch base `bc1a721e8` was cut from develop `942111d5a` at PR creation; develop has since advanced (active maintainership). Only my single fix commit `4ad2285f8` sits on top of `bc1a721e8` (`git log --oneline bc1a721e8..HEAD`). `git merge-base --is-ancestor 942111d5a HEAD` -> 0. One integration candidate per chain: single branch `lane/0427-162-r3`.

## Cleanliness

No containers / compose projects started (pure Go unit-fix; required test is a Go unit test). State dir isolated under `/tmp/opencode/0427-162-r4-wt`. No baseharbor containers running (docker ps witness).

## Repo-rule compliance

- Write-set: only `cmd/baha/use_target.go`, `cmd/baha/onboarding.go`, `cmd/baha/use_target_connection_test.go`. No `.github/**` edit (Owner scope).
- Branch provenance: `lane/0427-162-r3` base `bc1a721e8` (a develop ancestor); only my fix commit `4ad2285f8` on top. Remote witness: `git ls-remote origin lane/0427-162-r3` -> `4ad2285f8d43dfbed59741903df5f8cd6f27a837`.
- One integration candidate per chain.
- Evidence lives only in baseharbor-plan (planning repo) at evidence/bughunt-app-list-owner-check-scaling/round-4.md. No evidence files in the product repo.
- No subagents (Owner directive 2026-11-04). All steps run in this session.

## Status
DONE — all five recovery hints now name `baha up --control-plane-only`; new CLI regression `TestRecoveryHintNamesCoreSetupPath` (missing + unreachable Core, onboarding + production seams) green and negative-verified; PR #1510 head `4ad2285`; hosted run `42594772123` terminal success (go-unit-tests executed+passed, skipped as skipped). Evidence pushed.

## Terminal run (reproduced below)
```
$ git ls-remote origin lane/0427-162-r3
4ad2285f8d43dfbed59741903df5f8cd6f27a837  refs/heads/lane/0427-162-r3
$ git merge-base --is-ancestor 942111d5a1c43f5257bf1627a966fa9e6c6f24bd HEAD
$ git log --oneline bc1a721e8e46ca82f81e978fc7c186bb135bf67a..HEAD
4ad2285f8 fix(cmd/baha): recovery hint names 'baha up --control-plane-only' for core setup
$ gh api 'repos/mcpdev80/baseharbor/pulls/1510' --jq '{state:.state,head:.head.sha,changed:.changed_files}'
{"state":"open","head":"4ad2285f8d43dfbed59741903df5f8cd6f27a837","changed":3}
$ gh api 'repos/mcpdev80/baseharbor/actions/runs/42594772123/jobs' --jq '{skipped:(.jobs|map(select(.conclusion=="skipped"))|length), success:(.jobs|map(select(.conclusion=="success"))|length), other:(.jobs|map(select(.conclusion!="skipped" and .conclusion!="success"))|length)}'
{"skipped":11,"success":14,"other":0}
```

## END
0427-162 r4 DONE — PR #1510 head `4ad2285f8` (branch `lane/0427-162-r3`), all five recovery hints renamed to `baha up --control-plane-only`, new CI regression `TestRecoveryHintNamesCoreSetupPath` green (negative-verified), hosted run `42594772123` terminal success (go-unit-tests executed+passed, 11 skipped as skipped, 0 failures). Evidence: baseharbor-plan evidence/bughunt-app-list-owner-check-scaling/round-4.md.
