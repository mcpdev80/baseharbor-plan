# qualify-5 — w57-ci-access-e

- Lane: w57-ci-access-e (Worker, Coordinator f49a3303)
- Task card: t-20261022-r27-ci-access · PR #1357 · base = work/r27-ci-access-ab
- Role: Worker — narrow test-wiring fixes only; everything else already FESTGESTELT (restore OK, server-config OK, gofmt/hosted OK, flag-gegenprobe OK).
- Evidence date: 2026-11-03

## PLAN

1. Fetch origin (already done, rc=0 verbatim) + worktree /tmp/opencode/w57-ci-access-e-wt on work/r27-ci-access-ab (already done, head 067274a1).
2. Punkt 1 — negative Check() tests watch the correct handler: per-path reach-flag for execute vs check; negative tests observe the READY/handler Check actually invokes; positive counter-flag both paths flag false->true on valid material.
3. Punkt 2 — stricter cause: replace assertTLSHandshakeCause with type-strict check (errors.As on *x509.UnknownAuthorityError / x509.CertificateInvalidError / tls.CertificateRequired-Alert, or errors.Is(tls.HandshakeFailure)); pure substring tolerance on "tls"|"x509"|"certificate" removed. TestMutualTLSRejectsInvalidCAPEM asserts concrete server-side verification cause, not transport abort.
4. Local checks: gofmt -l empty; diff '^-func Test' non-empty; go test ./internal/runtimeexecutor -count=1 green; go build ./...
5. Commit (git add internal/runtimeexecutor/client_test.go only); push; verify ls-remote == head.
6. Eigenes-Run: gh pr checks 1357 --watch to terminal, capture run-id; write this evidence; END line to f49a3303.

## repo-rule compliance

- Write-set: internal/runtimeexecutor/client_test.go only.
- No existing test function deleted: diff '^-func Test' must be non-empty (verified).
- gofmt -l empty.
- `go test ./internal/runtimeexecutor -count=1` green under GOCACHE=/tmp/opencode/gc TMPDIR=/tmp.
- `go build ./...` clean.
- PR status not touched. No branch-protection bypass.

## END

Lane w57-ci-access-e: BLOCKED — in progress (plan written; work on Punkt 1/2 not yet started).
