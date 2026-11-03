# R10 authority-contract fix evidence (w31-authority-r10)

Lane: w31-authority-r10 | Coord: f49a3303 | Base: head 7781a6f3 branch w7-authority-r3-clean
Model: Flash | Run: local go build/test (own worktree baseharbor)

## PLAN checklist
1. Own worktree on w7-authority-r3-clean (baseharbor HEAD 7781a6f3) — DONE
2. P1: replace both 5*time.Minute literals (maxAge + FreshnessWindow) with serviceaccess.DefaultObservationMaxAge — DONE
3. P1 regression: maxAge=0 + 30min-obs => fresh; 2h-obs => stale; grep 5*time empty — DONE
4. P2: real adapter integration test — BLOCKED on scope decision (see below)
5. go build/test + wrapper — pending P2
6. Merge origin/develop + push w7-authority-r3-clean — pending
7. Evidence + END line — pending

## P1 — single maxAge constant (DONE)
- File: internal/serviceaccess/authority.go
- maxAge() (line ~50): replaced `const defaultWindow = 5 * time.Minute` with `return DefaultObservationMaxAge`.
- FreshnessWindow() (line ~79): replaced `window = 5 * time.Minute` with `window = DefaultObservationMaxAge`.
- Source of truth: internal/serviceaccess/pki.go:23 `const DefaultObservationMaxAge = time.Hour` (one direction, not two numbers).
- grep evidence (proof path clean):
  `grep -n "5 * time.Minute\|time.Minute*5\|5*time" internal/serviceaccess/authority.go` => EMPTY
- Build: `go build ./internal/serviceaccess/` => OK
- Test: `go test ./internal/serviceaccess/` => ok 0.049s
- Regression (verified via FreshnessWindow semantics, single DefaultObservationMaxAge=1h):
  - maxAge=0 + observation 30min old => now-obs(30m) <= 1h window => FRESH (not stale)
  - maxAge=0 + observation 2h old => now-obs(2h) > 1h => STALE

## P2 — real adapter integration evidence (BLOCKED on scope decision)
Requirement (mission Punkt 2): openbao.ServiceIssuer against a real CA PKI env:
BaseSerial == echte CA-serial (HEX, not URI) AND RevokedStatus accepts that serial as serial-key
(CRL entry of that serie => revoked=true); BaseExpiry == geparstes NotAfter des CA-cert.

Finding (must be decided by Owner):
- Current ServiceIssuer.BaseSerial (internal/openbao/service_issuer.go:136) returns a HARDCODED
  mount reference URI `serviceIssuerReference = "openbao://baseharbor-pki/baseharbor-services"` — NOT a
  CA serial. Its own doc comment says "a stable mount-derived serial" (a URI string), which directly
  CONTRADICTS the mission's "BaseSerial == echte CA-serial (hex, NICHT URI)".
- Current ServiceIssuer.BaseExpiry (:151) returns `now.Add(90*24*time.Hour)` — a hardcoded 90d, NOT the
  parsed CA NotAfter.
- ServiceCA(ctx, executor, files) DOES read the real CA PEM from OpenBao (service_pki.go:152).
- LocalIssuer already implements the real-CA precedent: BaseSerial -> ca.SerialNumber.Text(16)
  (hex), BaseExpiry -> ca.NotAfter.UTC() (internal/serviceaccess/local_issuer.go:186/200).
- canonicalServiceRevocationSerial (internal/openbao/service_pki_serial.go:12) accepts hex serials with
  optional ':'/'-' separators, so a hex CA serial WOULD be accepted by RevokedStatus as a serial-key.

Blocker: The acceptance criteria cannot be satisfied without CHANGING ServiceIssuer.BaseSerial/BaseExpiry
to read the real CA (parse the ServiceCA PEM and return ca.SerialNumber.Text(16) / ca.NotAfter.UTC()).
This is a design change (the current "mount-derived reference" is intentional per existing code).
Two possible Owner directions:
  (A) Change ServiceIssuer.BaseSerial/BaseExpiry to the real-CA pattern (like LocalIssuer), then write the
      integration test; or
  (B) The test must instead prove the CURRENT contract (mount reference + reference time) is stable and
      that RevokedStatus still accepts a CA hex serial — i.e. keep URI BaseSerial, and prove the CRL
      round-trip on a hex serial separately.

Scope decision required BEFORE touching ServiceIssuer production code.

## repo-rule compliance
- Worktree only; no foreign trees touched. git add single files only.
- No secrets/tokens logged.

## END status
END_BLOCKED w31-authority-r10: head=7781a6f3 | P1 konstant-integriert (DefaultObservationMaxAge, grep 5*time leer) | P2 blockt: BaseSerial/BaseExpiry sind aktuell URI+90d-hardcode, nicht echte CA; Owner-Entscheidung A oder B notwenig.
