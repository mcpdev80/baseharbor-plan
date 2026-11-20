# Shell wrapper cells must run (0428-179) — round-1 evidence

## PLAN

1. Read mission, task note, finding act, AGENTS.md, and the exact target source lines.
2. Remote reality witnesses: develop head 3653369, planning repo remote, base is ancestor, log line empty.
3. Confirm the silent-success bug: zsh/fish absent, test PASSES while skipping both paths.
4. Implement fail-loud + a dedicated CI cell that installs zsh/fish and owns the cmd/baha shell-path tests, wired into the CI group covering cmd/baha in the same PR.
5. gofmt/readability clean; run cmd/baha tests locally with shells present, and confirm fail-loud when absent.
6. Push branch from develop head + open PR (base develop), keep draft.
7. Hosted run at exact head showing cells EXECUTED (not skipped) or failing loudly; record run-id + terminal conclusion.
8. Preserve work to baseharbor-plan main (patch + evidence) because the product push needs a workflow-scope token this lane does not have.
9. Post END line; record END in evidence.

## Lane identity

- Owner / lane: w179-0428-179-shells (ornith channel).
- Product: mcpdev80/baseharbor.
- Branch: lane-0428-179-shell-wrapper-cells.
- Candidate SHA: 0eeda34426547941f0050c7bef2670fbe7560162 (local, intact; NOT pushed to product).

## Remote reality witnesses (before first evidence commit)

Planning repo remote (verified BEFORE first evidence commit):
```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Product remote used (first git action, resolved to github.com/mcpdev80):
```text
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```

Base develop head (via `git ls-remote origin refs/heads/develop`):
```text
3653369a4d832e16a427ebf862e959dcccb882b1	refs/heads/develop
```

Base is ancestor of branch head:
```text
YES: 3653369 is ancestor of HEAD
```

`git log --oneline origin/develop..HEAD` (lists ONLY my own commit):
```text
0eeda344 test(0428-179): fail-loud on missing zsh/fish wrapper shell and install them in the ci-3 shard
```

## Finding act (source of the card)

Post-merge review `evidence/r28-welle4-2026-11-20/codex-review-wave/post-merge-068-166-develop-96f2ae11.md`, B2:
`TestEndToEndInstalledZshAndFishWrappers` (cmd/baha/context_terminal_test.go:434-439, :491-505) drives
zsh/fish ONLY if the binary is present and continues otherwise; a runner without those shells reports
success without executing either path — not durable evidence for the fish recursion guard.

## Preconditions witnessed (before the change)

1. Conditional lines that make the case vanish — cmd/baha/context_terminal_test.go:436-440 (the zsh/fish
   guard) and the 15s timeout + run + assert body reached only when LookPath succeeds (~491-505):
```go
shellPath, err := exec.LookPath(shell)
if err != nil {
    t.Logf("%s is not installed; generated wrapper remains covered structurally", shell)
    continue
}
```

2. Proof the running job reports SUCCESS in BOTH cases without executing either path. The shell test is
   routed by SHA-256 of its name into CLI shard `cli-3`
   (`int.from_bytes(sha256("TestEndToEndInstalledZshAndFishWrappers")[:8]) % 4 == 3`), so the owning job is
   `PR · Go unit · cli-3` (and, on the develop full suite, `validate` / `go test ./...`). Local repro on a
   runner without zsh/fish:
```text
=== RUN   TestEndToEndInstalledZshAndFishWrappers
    context_terminal_test.go:438: zsh is not installed; generated wrapper remains covered structurally
    context_terminal_test.go:438: fish is not installed; generated wrapper remains covered structurally
--- PASS: TestEndToEndInstalledZshAndFishWrappers (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.009s
```
   zsh/fish presence on this host at that moment: `/usr/bin/bash` only (zsh and fish absent). This is
   "silent success" — a PASS that executed neither the zsh NOR the fish path. That is the defect.

3. Recursion guard being covered (cmd/baha/completion_setup.go:64-67 fish `command baha` inside
   `function _baha_context_wrapper`, :78-80 the `function baha --wraps _baha_context_wrapper` wrapper, and
   the `[[ $- == *i* ]]` / `status is-interactive` interactive guard). Witness that the recursion guard IS
   exercised by a passing unit test even when the fish e2e path is never active — the guard has a
   structural assertion that moves with the source:
```text
=== RUN   TestContextWrapperCallsRealCommandViaCommand
--- PASS: TestContextWrapperCallsRealCommandViaCommand
```
   (cmd/baha/context_terminal_test.go:217-230 asserts `command baha` in fish and rejects the bare recursive
   `baha context show` call). So the fish recursion guard is genuinely tested by the unit suite; it only
   lacked a real-`fish` e2e witness until this card.

## Change (two halves, file by file, with lines)

(a) cmd/baha/context_terminal_test.go — fail-loud (16 lines changed):
```diff
-// 'context use'/'context clear' in its own process (no marker file). Where a
-// shell is installed in CI (bash on ubuntu-latest), the shell is exercised;
-// where it is absent, the test is skipped and the gap is reported to the owner
-// as an owner-scope (workflow) point, not this lane's decision.
+// 'context use'/'context clear' in its own process (no marker file). Both shells
+// are mandatory here: the test fails loud when a shell is missing so the CI
+// shard cannot pass while skipping the zsh or fish path. The owning CI cell
+// installs zsh and fish so both paths actually execute.
```
```diff
 	for _, shell := range []string{"zsh", "fish"} {
 		shellPath, err := exec.LookPath(shell)
 		if err != nil {
-			t.Logf("%s is not installed; generated wrapper remains covered structurally", shell)
-			continue
+			// Fail loud: the wrapper for this shell must actually execute on the
+			// runner. A silent skip here (the pre-existing behaviour) lets the CI
+			// shard pass while NEITHER the zsh NOR the fish path runs, which is not
+			// durable evidence for the fish recursion guard. The owning CI cell
+			// installs zsh and fish so both paths run.
+			t.Fatalf("%s is required to run this wrapper path; install %s in the owning CI cell: %v", shell, shell, err)
 		}
```
   No change to the production function `context_terminal.go` — test code only.

(b) .github/workflows/ci.yml (+18 lines, two jobs) — install zsh and fish in the CI shard that owns the
   shell path:
   - `pr_unit_shards` job, new step gated on `matrix.shard == 'cli-3'` (the shard that carries
     `TestEndToEndInstalledZshAndFishWrappers`):
```diff
+      - name: Install interactive shells for the shell-wrapper path
+        if: matrix.shard == 'cli-3'
+        shell: bash
+        run: |
+          set -euo pipefail
+          sudo apt-get update
+          sudo apt-get install -y zsh fish
+          echo "zsh: $(command -v zsh)"
+          echo "fish: $(command -v fish)"
```
   - `validate` job (develop full suite), same step before "Reset persistent runner state":
```diff
+      - name: Install interactive shells for the shell-wrapper path
+        shell: bash
+        run: |
+          set -euo pipefail
+          sudo apt-get update
+          sudo apt-get install -y zsh fish
+          echo "zsh: $(command -v zsh)"
+          echo "fish: $(command -v fish)"
```
   This is the gate wiring for the cmd/baha shell path in THIS PR (owner directive 51d95b99: gate wiring is
   part of the implementation, not a separate .github finding). No change to the planner, the required-plan,
   or the release matrix.

## Local results (command + verbatim output)

With zsh/fish installed on the host, the shell-path test passes:
```text
$ go test ./cmd/baha -run 'TestEndToEndInstalledZshAndFishWrappers' -count=1 -v
=== RUN   TestEndToEndInstalledZshAndFishWrappers
--- PASS: TestEndToEndInstalledZshAndFishWrappers
ok  	github.com/mcpdev80/baseharbor/cmd/baha	8.033s
```
Without the shells on PATH the test fails loud (witness from the same session, earlier, when zsh/fish were
absent):
```text
=== RUN   TestEndToEndInstalledZshAndFishWrappers
    context_terminal_test.go:443: zsh is required to run this wrapper path; install zsh in the owning CI cell: exec: "zsh": executable file not found in $PATH
--- FAIL: TestEndToEndInstalledZshAndFishWrappers (0.00s)
FAIL
```
gofmt clean:
```text
$ gofmt -l cmd/baha/context_terminal_test.go
(empty)
```
go vet clean:
```text
$ go vet ./cmd/baha
(empty)
```
Related context/completion/e2e tests all pass (same session):
```text
TestContextWrapperCallsRealCommandViaCommand PASS
TestEndToEndBashInteractiveContextUseAndClear PASS
TestInteractiveGuardPresent PASS
TestEndToEndInstalledZshAndFishWrappers PASS (shells present)
```

## blockierung

The product push was refused by GitHub's OAuth App workflow-scope protection. The only available token has
scopes `gist, read:org, repo` — present scopes, and `workflow` absent — logged here as metadata only
(§5.6, no token value, no file contents beyond the public API message):
```text
! [remote rejected]   lane-0428-179-shell-wrapper-cells -> lane-0428-179-shell-wrapper-cells
    (refusing to allow an OAuth App to create or update workflow `.github/workflows/ci.yml` without `workflow` scope)
```
gh auth status (scopes only):
```text
Token scopes: 'gist', 'read:org', 'repo'
```
Per owner decision (mission-179-preserve.md): this workflow-scope edge is the owner's / a workflow-scope
token's job, not this lane's. No product push attempted again; work preserved on baseharbor-plan main via
patch instead.

## next step for the releaser (three lines, run with a workflow-scope token)

```text
git clone https://github.com/mcpdev80/baseharbor.git bh && cd bh
git am 0eeda344-shell-wrapper-cells.patch   (patch lives in baseharbor-plan evidence/r28-welle4-2026-11-20/shell-wrapper-cells/)
git push -u origin lane-0428-179-shell-wrapper-cells   then open PR (base develop, draft); hosted run on cli-3 shows the zsh/fish cells EXECUTED
```

## repo-rule compliance

- Write-set: cmd/baha/context_terminal_test.go (fail-loud only; no production function change) and
  .github/workflows/ci.yml (shell install step in the cli-3 shard and the develop validate job). No touch of
  the mission's locked files (context_terminal.go production logic, internal/observability/registry.go,
  perses*, identityprovider*).
- No `git add -A`; staged the two files explicitly.
- No subagents; every step run inside this session.
- No runner infrastructure built / registered / repaired.
- No product push / no PR attempt this shift (workflow-scope blocker, owner-accepted).
- Work preserved: patch + evidence committed to baseharbor-plan main, which needs no workflow scope.

## cleanliness

- before: no containers/networks/volumes/state dirs created by this lane on this host.
- after: no containers/networks/volumes/state dirs created (local Go tests need no runtime; the shells were
  installed via apt, not compose). ambient-core/ images of other carts left untouched.

## END

<END_BLOCKED w179-0428-179-shells: work preserved on baseharbor-plan main (patch 0eeda344 + evidence), product push blocked on workflow-scope token — 0eeda34426547941f0050c7bef2670fbe7560162>
