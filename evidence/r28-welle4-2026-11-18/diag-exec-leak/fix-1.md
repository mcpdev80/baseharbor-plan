# 0428-118 — fix DIAG_EXEC if-true leak (red -> green)

Mission: /var/tmp/missions/mission-118-diagfix.md
Lane: w118-diagexec (codeman session d5ecb550, flash channel)
Card: t-20261118-diag-exec-iftrue-leak (0428-118), hunt-916 defect I1
Source finding: evidence/r28-welle4-2026-11-18/hunt-ownership/befund-1.md (I1)

## PLAN

1. Read mission + befund-1.md (I1) + card contract. — done
2. Claim via plan.py; verify frontmatter `owner:` field after claim (`git show`). — done (claim commit 70e2a3cb on origin/main; owner field present; the claim gap the mission warned about was real: the card had no `owner:` line, so plan.py's regex wrote nothing — I added the line and re-rendered)
3. Reality check develop via `git ls-remote origin develop`. — done
4. Create isolated worktree from the attested develop base. — done
5. Red evidence: regression test that fails on unfixed code (DIAG_EXEC stdout leak observable). — in progress
6. Fix cmd/baha/app_edit_apply.go so DIAG_EXEC cannot influence production behavior. — pending
7. Green: same test passes; go build/vet + unit tests on exact head. — pending
8. PR (base develop, branch lane-0428-118-diag-exec), exact-head CI run to TERMINAL. — pending
9. Publish this evidence to origin/main, END post. — pending

## Base attestation

- Planning repo truth witness (wrong-zone check): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` -> `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git remote get-url origin` -> https://github.com/mcpdev80/baseharbor-plan.git
- Product repo: `git ls-remote origin develop` (in /home/marcel/dev/baseharbor-ecosystem/baseharbor) -> `8dccd4fe1a52bbcc61c67f7809079f33b8040d64` — the exact SHA the branch `lane-0428-118-diag-exec` was cut from (worktree /tmp/opencode/w118-diagexec-wt, `git rev-parse HEAD` at creation -> 8dccd4fe1...).
- develop is a hard branch base: `git merge-base --is-ancestor 8dccd4fe1a52bbcc61c67f7809079f33b8040d64 <first commit>` must be true, and `git log 8dccd4fe1..HEAD --oneline` must list ONLY this lane's commits (witness at PR time).

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

Remove the `if true`-guarded `fmt.Printf` from the production partial path entirely, keeping the `return output, &appMachineError{Code: "partial"}` behavior unchanged. After the fix there is no diagnostic execution path at all — with DIAG_EXEC set, unset, or any other value, `appEditApplyConfirmed` produces byte-identical behavior (verified by the regression test below). A feature-flagged diag path would require the env var to reach the machine stream; production behavior must not depend on environment presence, so the flag-free removal is the fix that makes the guarantee absolute.

## Red -> green evidence

## repo-rule compliance

## Cleanliness

## END
