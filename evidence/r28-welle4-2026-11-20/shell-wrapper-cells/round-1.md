# Shell wrapper cells must run (0428-179) — round-1 evidence

## PLAN

1. Read mission, task note, finding act, AGENTS.md, and the exact target source lines.
2. Remote reality witnesses: develop head, planning repo remote, base-ancestor, empty log line.
3. Confirm the silent-success bug: zsh/fish absent, test PASSES while skipping both paths.
4. Implement fail-loud + a dedicated CI cell that installs zsh/fish, wired into the CI group covering cmd/baha in the same PR.
5. gofmt/readability clean; run cmd/baha tests locally with shells present in a cell.
6. Push branch from develop head, open PR (base develop), set title/body via `gh api PATCH`, keep draft.
7. Hosted run at exact head showing cells EXECUTED (not skipped) or failing loudly; record run-id + terminal conclusion.
8. Commit evidence to baseharbor-plan main; verify path present on origin/main before END; bring down containers.
9. Post END line; record END in evidence.

## Lane identity

- Owner / lane: w179-0428-179-shells (ornith channel).
- Product: mcpdev80/baseharbor.
- Branch: lane-0428-179-shell-wrapper-cells.
- Base (cut from): develop = 3653369a4d832e16a427ebf862e959dcccb882b1 (measured via `git ls-remote origin refs/heads/develop`).

## Remote reality witnesses (before first evidence commit)

Planning repo remote:
```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Product remote used (first git action, resolved to github.com/mcpdev80):
```text
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```

Base develop head:
```text
3653369a4d832e16a427ebf862e959dcccb882b1	refs/heads/develop
```

Base is ancestor of branch head:
```text
YES: 3653369 is ancestor of HEAD
```

`git log --oneline origin/develop..HEAD` (must list ONLY my own commits):
```text
<empty until first commit>
```

## Finding act (source of the card)

Post-merge review `evidence/r28-welle4-2026-11-20/codex-review-wave/post-merge-068-166-develop-96f2ae11.md`, B2:
`TestEndToEndInstalledZshAndFishWrappers` (cmd/baha/context_terminal_test.go:434-439, :491-505) drives
zsh/fish ONLY if the binary is present and continues otherwise; a runner without those shells reports
success without executing either path — not durable evidence for the fish recursion guard
(cmd/baha/completion_setup.go:64-67 fish `command baha`, :78-80 `function baha` wrapper).

## Preconditions witnessed (before the change)

1. Conditional lines that make the case vanish — cmd/baha/context_terminal_test.go:436-440:
```go
shellPath, err := exec.LookPath(shell)
if err != nil {
    t.Logf("%s is not installed; generated wrapper remains covered structurally", shell)
    continue
}
```
   Same shape in the zsh/fish split loop body lines 491-505 (the 15s timeout + run + asserts are
   only reached when LookPath succeeds).

2. Proof the running job reports SUCCESS in BOTH cases without executing either path. Job name:
   `PR · Go unit · cli-3` (the shard `int.from_bytes(sha256("TestEndToEndInstalledZshAndFishWrappers")[:8]) % 4 == 3`).
   Local repro on a runner without zsh/fish:
```text
=== RUN   TestEndToEndInstalledZshAndFishWrappers
    context_terminal_test.go:438: zsh is not installed; generated wrapper remains covered structurally
    context_terminal_test.go:438: fish is not installed; generated wrapper remains covered structurally
--- PASS: TestEndToEndInstalledZshAndFishWrappers (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.009s
```
   zsh/fish presence on this host:
```text
which zsh fish bash: /usr/bin/bash only (zsh/fish absent)
```
   This is "silent success" — a PASS that executed neither the zsh nor the fish path. That is the defect.

3. Recursion guard being covered (cmd/baha/completion_setup.go:64-67, :78-80). Witness that the
   recursion guard IS exercised by a passing unit test even when the fish e2e path is never active:
```text
=== RUN   TestContextWrapperCallsRealCommandViaCommand
--- PASS: TestContextWrapperCallsRealCommandViaCommand
```
   (cmd/baha/context_terminal_test.go:217-230 asserts `command baha` in fish and rejects the bare recursive call.)

## Chosen approach (acceptance 1 + 2)

- Fail-loud: when zsh or fish is absent, `t.Fatalf` instead of `continue`, so the gate fails loudly
  rather than passing silently. The wrapper is now genuinely required to run in the cell.
- Dedicated cell: a CI cell that installs zsh and fish and owns the cmd/baha shell-path tests, so the
  shells are present and the two paths actually execute. The route to install the shells in the CI group
  that already runs the cmd/baha Go-unit shard (cli-3) is built in THIS PR (owner directive 51d95b99:
  gate wiring is part of implementation, not a separate .github finding).

## repo-rule compliance

- Write-set: cmd/baha/context_terminal_test.go (fail-loud change only, no production function change) and
  the .github/workflows/ci.yml group that runs the cmd/baha shell-path shard. No touch of the locked
  files in the mission boundaries (context_terminal.go production logic, registry.go, perses*, identityprovider*).
- No `git add -A`; targeted adds only.
- No subagents; every step run inside this session.
- No runner infrastructure built/registered/repaired.
- Containers (if any) brought down before END.

## Cleanliness

- before: no containers/networks/volumes/state dirs created by this lane on this host.
- after: (to be filled with `docker ps`/`podman ps` witness + cleanup before END).
- ambient-core/ images of other carts left untouched.

## END

<END_DONE w179-0428-179-shells: <one line + candidate SHA>>
