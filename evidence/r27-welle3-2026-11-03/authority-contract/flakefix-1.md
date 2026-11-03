# w37-authority-flakefix Evidence

- Role: Worker (Lane w37), Coordinator f49a3303
- Micro: 1 line test-robustness PR #1348, based on review-1326j recipe 1
- Base = head `5b6681bd`, branch `w7-authority-r3-clean`
- Repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor`

## PLAN

1. fetch origin w7-authority-r3-clean + develop; worktree add at /tmp/opencode/w37-flakefix-wt
2. Fix: normalize caSerialHex to even hex length in service_issuer_integration_test.go (left-pad "0"), +comment; NO change to BaseSerial
3. Proof: go test ./internal/openbao -run TestServiceIssuerBaseSerialIsRealCASerial -count=200 => 0 FAILS (full output in this file)
4. Merge origin/develop (if ahead), ancestry rc=0, ls-remote SHA, go build ./..., push FF, ls-remote==head (no tmp branch, no PR)
5. Write END_DONE to coordinator f49a3303

## ROOT CAUSE (diagnosis)
`ca.SerialNumber.Text(16)` in buildRealCA can yield an odd number of hex digits
(128-bit ECDSA serial +1 is random). `baseSerial` from the real CA is the same
`Text(16)`, but the canonicalization path `canonicalServiceRevocationSerial`
normalizes odd-length hex by left-padding "0". The test compares
`baseSerial != caSerialHex` directly and then runs `hex.DecodeString(baseSerial)`.
With an odd-length `caSerialHex`, the direct comparison diverges and the hex
decode fails — a flaky race. Fix normalizes the reference `caSerialHex` to even
length (pad left with "0") so both sides are canonical hex; BaseSerial itself is
correct and unchanged.

## repo-rule compliance
- Exactly one file changed (the test file); BaseSerial/production code untouched.
- One logical change (normalize caSerialHex), one line + one comment.
- No `git add -A`; targeted add only.
- No PR, no tmp branch; push FF on w7-authority-r3-clean.

## PROOF (go test -count=200)

Command: `TMPDIR=/tmp GOCACHE=/tmp/opencode/gc go test ./internal/openbao -run '^TestServiceIssuerBaseSerialIsRealCASerial$' -count=200 -v`
Result: `ok github.com/mcpdev80/baseharbor/internal/openbao 0.066s` — PASS, EXIT=0, 0 FAIL across all 200 runs.

Before fix (baseline flake): odd 128-bit serials produced odd-length hex;
`BaseSerial = "c369cd36b09c756aaed44cda93ce01e"` vs canonical `"0c369cd36b09c756aaed44cda93ce01e"` => mismatch/`hex.DecodeString` failure.

## source-readability-audit (hosted-run 41616994198 follow-up, READ-only, NICHT geändert)
Command: `bash scripts/source-readability-audit.sh`
Result: AUDIT_EXIT=0, PASS on all three checks. No file is listed as violating.
Audit scans only non-test *.go for line count (<=800) and function span (<=200).
My changed file service_issuer_integration_test.go is 182 lines; longest function
well under 200. Audit passes on original HEAD 5b6681bd AND on head cf95e6e1.
gofmt -l internal: clean (file now gofmt-compliant).

## END
END w37-authority-flakefix: head=cf95e6e1 count200=0fail | audit PASS, gofmt clean
