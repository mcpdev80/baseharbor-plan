# CODEX-REVIEW — PR #1385, review 1385d

Review role: CODEX-REVIEW (read-only; no merge or PR action). Review pane: `codex-luna-ch`, session `ab08e19f-3b8b-41dc-b817-41f3d8879948` (Codeman metadata reports GPT-6-Luna). Recorded during rebind on 2026-11-05; the race and mutation verdicts below recover the completed 1385d review result. The fresh rebind session could not replay Go tests because compilation exhausted the writable filesystem quota before test execution.

## PLAN

1. Confirm the task candidate, current PR head, branch ref, base ancestry, and hosted check run.
2. Inspect the race cell and mutation harness at the exact candidate; sample the unchanged recovery/read-back test path and changed-file names.
3. Record the recovered 1385d verdict and the rebind replay limitation without treating a compile failure as a product-test result.

## Candidate and remote witness

- PR #1385 is OPEN, base `develop`, current head `0e2b4803736dffb3e374b9526c30fb1fe211f337`.
- GitHub branch ref `work/r27-protected-credentials` resolves to the same SHA.
- The commit has parents `f518b5f571b8f6a7335dbd6e4fc2b32655bdebfe` and `77511c8a6672f34faf0d5ac543ba126485f05c41`; the required develop merge `77511c8a6672` is a parent of the candidate.
- GitHub compare `77511c8a6672...0e2b4803736` is ahead by five commits, with the task's eight changed paths: `cmd/baha/dev_access.go`, `cmd/baha/dev_access_real_cas_race_test.go`, `cmd/baha/dev_access_reconcile_test.go`, `cmd/baha/openbao.go`, `internal/deployment/operator_auth.go`, `internal/devaccess/rebind.go`, `internal/devaccess/rebind_test.go`, and `internal/openbao/managed_credentials.go`. The only changed OpenBao-package path is `internal/openbao/managed_credentials.go` (name-only scope check).
- `cmd/baha/dev_access_reconcile_test.go`, `internal/devaccess/rebind.go`, and `internal/deployment/operator_auth.go` have the same GitHub blob IDs at parent `f518b5f5` and candidate `0e2b4803`; the round-4 addition does not alter those recovery/read-back paths. The previous review-1385c recorded that the read-back path returns the concurrent winner and fails closed on the conflict.

## Required race and mutation evidence

- **Race cell — PASS in the completed 1385d review.** `TestReconcileRealCreateOnlyCASSurvivesConcurrentSeed` drives `openbao.GetManagedCredential` and `openbao.SetManagedCredentialIfAbsent` through the production command adapters. Two goroutines contend on the same managed reference. The test asserts exactly one production Get, at least one create-only rejection, zero overwrites, and preservation of the existing concurrent value. The exact candidate's round-4 evidence records the focused race cell green.
- **Production-option mutant — RED in one run.** Removing `-if-not-exists` from the production `bao kv put` command turns the write unconditional. The captured failure is:

  ```text
  dev_access_real_cas_race_test.go:181: mutant managed value = "{\"username\":\"developer\",\"password\":\"local-opt-in\"}", want the concurrent winner "{\"username\":\"concurrent\",\"password\":\"concurrent-secret\"}" to survive an unconditional seed
  FAIL
  ```

  The single-run requirement is met by the recovered 1385d result; `round-4.md` also records the same deterministic red result across three consecutive runs. The mutation harness changes the exact production command in a disposable product copy and invokes a real `go test` process.
- **Read-back/recovery sample — unchanged and fail-closed.** The round-4 addition is a separate test file. The relevant recovery source and prior reconciliation test have unchanged blob IDs from the round-4 parent; review-1385c's earlier sample records read-back of the winning value and no overwrite on conflict.
- **Hosted run 42043134426 — terminal SUCCESS** at exact head `0e2b4803736dffb3e374b9526c30fb1fe211f337`; `PR Selected Checks` and the selected Go/OpenBao/CLI validations succeeded. The run was queried through GitHub Actions and matched the current PR head.
- Remote SSH `ls-remote` was unavailable in this environment because `/etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf` failed its local permissions check. GitHub's read-only branch-ref API returned the exact candidate SHA, providing the remote-ref witness.

## Rebind replay limitation

I attempted the focused unmutated test through a Go overlay containing the exact candidate test file. The existing worker checkout was not the candidate tree, so the overlay was used only for the added test. The first compile failed before test execution because the configured Go cache was read-only; retrying with a writable `/tmp` cache failed with `disk quota exceeded` while compiling dependencies. No race or mutant result is inferred from that failed compile. The verdict below is the recovered completed 1385d review result, supported by the candidate source, round-4 evidence, and exact-head hosted run; this rebind attempt is not represented as a new successful local run.

## Verdict: ACCEPT

The completed 1385d review's required race cell was green, and removing the production `-if-not-exists` option made the same-path conflict outcome red in a single run. The exact current PR head contains the develop merge and the required terminal hosted checks. This record does not authorize or perform any PR action.

## repo-rule compliance

- Read-only review of PR #1385; no product files, PR metadata, branch, or review state was changed.
- No subagents, merge, or force operation.
- The new evidence file is the only file staged for the Planning commit; unrelated untracked Planning evidence remains untouched.
