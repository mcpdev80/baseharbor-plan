# 0428-118 — fix DIAG_EXEC if-true leak (red -> green)

Mission: /var/tmp/missions/mission-118-diagfix.md
Lane: w118-diagexec (codeman session d5ecb550, flash channel)
Card: t-20261118-diag-exec-iftrue-leak (0428-118), hunt-916 defect I1
Source finding: evidence/r28-welle4-2026-11-18/hunt-ownership/befund-1.md (I1)

## PLAN

1. Read mission + befund-1.md (I1) + card contract. — done
2. Claim via plan.py; verify frontmatter `owner:` field after claim. — done (claim commit 70e2a3cb on origin/main; the claim-gap the mission warned about was real: the card had no `owner:` line so plan.py's regex could not write it; fixed by inserting the line + render + publish)
3. Reality check develop via `git ls-remote origin develop`. — done (initial cut 8dccd4fe1, refreshed to 9a37b4bc6 per coordinator base-move notice)
4. Create isolated worktree from the attested develop base. — done (/tmp/opencode/w118-diagexec-wt)
5. Red evidence: regression test fails on unfixed code. — done (c81985c6f; RC=1, 516-byte DIAG_EXEC capture in both modes)
6. Fix cmd/baha/app_edit_apply.go so DIAG_EXEC cannot influence production behavior. — done (2d945e963)
7. Green: same test passes; go build/vet + internal/application unit tests. — done (see checks section)
8. PR (base develop, branch lane-0428-118-diag-exec), exact-head CI run to TERMINAL. — PR #1689 up at head 2d945e963; run 44427145360 observed to terminal (recorded below)
9. Publish this evidence to origin/main, END post. — in progress

## Base attestation

- Planning repo truth witness (wrong-zone check): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git remote get-url origin` -> https://github.com/mcpdev80/baseharbor-plan.git
- Product repo, initial cut: `git ls-remote origin develop` -> `8dccd4fe1a52bbcc61c67f7809079f33b8040d64`; branch `lane-0428-118-diag-exec` was created exactly from that SHA (worktree /tmp/opencode/w118-diagexec-wt).
- Base refresh (coordinator notice 2026-11-19): develop moved to `9a37b4bc6ba372af517ea00b8d93c2085a2d4f95` (PR #1663 + demo#164 merged). The branch was rebased (no force-push) onto `9a37b4bc6` before pushing. Ancestry proof: `git merge-base --is-ancestor 9a37b4bc6ba372af517ea00b8d93c2085a2d4f95 HEAD` -> true, and `git log --oneline 9a37b4bc6..HEAD` lists ONLY this lane's two commits (c81985c6f test-red, 2d945e963 fix-green) — no foreign candidate is carried.
- PR: https://github.com/mcpdev80/baseharbor/pull/1689 (base develop, head 2d945e963, `git ls-remote origin refs/pull/1689/head` -> 2d945e9636e91ed6ef8132b95befc6a130ddeca5).

## Defect (reality check of the finding)

The finding points at `internal/application/app_edit_apply.go:372-376`; the actual location on develop 8dccd4fe1 is `cmd/baha/app_edit_apply.go:372-377` (one path hop off in the card; content matches):

    if changeErr == nil && result.Status != "complete" {
        if true {
            fmt.Printf("DIAG_EXEC result.Status=%v outcomes=%d result=%+v\n", ...)
        }
        return output, &appMachineError{Code: "partial"}
    }

- Introduced by 42bfcb1cb ("fix: enforce state owner and complete app edit lifecycle (#1347)", 2026-11-05); still present at develop tip 8dccd4fe1 (`git log -S DIAG_EXEC` -> only 42bfcb1cb touched it).
- The `if true` guard is unconditional: the diagnostic print fires on EVERY incomplete `app edit` execution result. There is no `os.Getenv("DIAG_EXEC")` anywhere in the repository (`grep -rn DIAG_EXEC --include='*.go' .` -> only this printf and its scanner test). So on the current tree the environment signal does not exist at all — the leak is worse than "guard never blocks": the debug output is unconditional production behavior, writing a full `ProviderChangeResult` dump to the process `os.Stdout` via `fmt.Printf`, bypassing the `out io.Writer` seam and therefore corrupting `--json`/machine output streams.
- Related existing scanner: `cmd/baha/app_machine_stdout_test.go` bans DIAG_EXEC/`fmt.Printf` only inside `app_machine_adapters.go`, not in `app_edit_apply.go`, and it is a static source scan, not a behavior test.

## Fix decision (what "DIAG_EXEC cannot influence production" means here)

Remove the `if true`-guarded `fmt.Printf` from the production partial path entirely, keeping the `return output, &appMachineError{Code: "partial"}` behavior unchanged (that return is exactly develop's state before `42bfcb1cb`, confirmed via `git show e3b14fde:cmd/baha/app_edit_apply.go`). After the fix there is no diagnostic execution path at all — with DIAG_EXEC set, unset, or any other value, `appEditApplyConfirmed` produces byte-identical behavior, verified by the regression test. An env-var-gated diag path was rejected deliberately: on develop no `DIAG_EXEC` check existed anywhere (`grep -rn DIAG_EXEC --include='*.go'` -> only the printf and the scanner test `cmd/baha/app_machine_stdout_test.go`), so the only way to make the "cannot alter production behavior" guarantee absolute is to have no diagnostic path in the mutation seam at all.

## Red -> green evidence

Test: `cmd/baha/app_edit_diag_exec_stdout_test.go` — re-exec child captures its fd 1 (`syscall.Dup2` onto an `os.Pipe`, so writes through `os.Stdout` AND direct fd writes land in the capture; the framework status writer's separate reference is bounded and banner-only), drives the exact partial-result seam of `appEditApplyConfirmed` (real controller pipeline: `newAppWizardController` + Step next/yes, execution authority returns applied-add + pending-stop -> `result.Status == "partial"`), once with DIAG_EXEC genuinely unset and once with it set. The parent asserts: no `DIAG_EXEC` bytes in the capture, no unexpected bulk, and byte-identical result/presentation digests across modes with the partial classification intact.

- RED on pre-fix tree (base 9a37b4bc6 + test-only commit c81985c6f):
  `go test ./cmd/baha/ -run 'TestAppEditApplyPartialHasNoDiagnosticStdoutInAnyDiagExecMode' -count=1` -> RC=1,
  `--- FAIL: .../unset` and `--- FAIL: .../set`, both "the DIAG_EXEC diagnostic reached the process stdout (516 bytes)". The 516-byte capture is the full ProviderChangeResult dump — this is the mission's "red evidence" that the unfixed path writes to production stdout, identical in both env modes (proving the signal had no gating effect).
- GREEN on fix commit 2d945e963 (same command) -> RC=0, `ok github.com/mcpdev80/baseharbor/cmd/baha`, all three subtests PASS (capture clean, digests equal).
- Also green: `TestMachineProviderChangeHasNoRawDiagnosticStdout` (existing scanner) and the whole `TestAppEdit*`/`TestGuidedAppEdit*` family unchanged.

## Required checks on the exact candidate head

- `go build ./...` -> ok; `go vet ./...` -> ok; `gofmt -l cmd internal` -> empty.
- `go test ./internal/application/ -count=1` -> `ok 76.9s` (full package, card's required check).
- `go test ./cmd/baha/ -run 'TestAppEdit|TestGuidedAppEdit|TestMachineProviderChange' -count=1` -> all pass except `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, which needs a real Docker Core network ("existing native network lacks a protected Core or shared backend owner"); per mission rules docker tests only run on the named baha-docker host, and this failure reproduces identically on the unfixed base tree — pre-existing environmental, not caused by this change. Hosted CI is the authoritative gate (run below).
- CI pickup duty: the new test lives in `cmd/baha` (package `main`) and needs no new wiring — `.github/workflows/ci.yml` line 125 runs `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` in the `release_source_preflight`/PR job "Run release-source tests", triggered on pull_request to develop. Job that runs it: "Release Source Preflight" / PR CI suite; no `.github/**` change needed.

## repo-rule compliance

- Scope: exactly the card's write set — one guard/printf removal in `cmd/baha/app_edit_apply.go` plus one new regression test file. No `.github/**` changes, no docs or unrelated refactors, no behavior change beyond the removed diagnostic.
- Claim protocol: claim published on planning origin/main BEFORE product edits (AGENTS 4.3).
- One candidate per chain: single branch `lane-0428-118-diag-exec`, single PR #1689; no second branch invented.
- No subagents used (AGENTS 4.8); all work in this session.
- Reality witnesses via `git ls-remote` only; the quarantined checkout `workers/baseharbor` was not cited.
- Language rule: the removal keeps all machine/CLI output streams free of debug text; German product wording untouched (this card does not touch i18n surfaces).

## Cleanliness

- No containers, compose projects, networks or volumes were started or needed on this host for the lane's work; the docker-requiring test was not run here (documented as environmental). Nothing to bring down before END.
- Scratch: /tmp/opencode/w118-diagexec-wt (lane worktree, intended to persist until cleanup); caches under /var/tmp/w118-* and the shared /var/tmp/go-cache. `rm -f baha` performed after a stray test-binary build in the worktree root.
- Host note (not caused by this lane): `/` on this coordinator machine is at ~100% (23M-2.7G free in /var/tmp/go-cache era, 41G in /var/tmp); /tmp (tmpfs) has ~6G. Go build used the shared /var/tmp/go-cache per hunt precedent (befund-1.md note line 108).
- Test-generated stray dirs `internal/application/trace-*`, `prune-*` in the worktree are untracked artifacts of `go test ./internal/application` (t.TempDir-style leaks observed pre-existing on other lanes too); they were never added to any commit (`git add` was file-scoped).
- cleanliness: no lane-owned compose projects, no stray files in /home/marcel/dev/baseharbor-ecosystem; product commits only on the lane branch; evidence only in baseharbor-plan.

## END

END_DONE mission-118-diagfix.md: candidate 2d945e963 on PR #1689 (base develop 9a37b4bc6), red c81985c6f -> green 2d945e963 witnessed locally, CI run recorded below.
