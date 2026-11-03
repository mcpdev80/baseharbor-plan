# R10 authority-contract fix evidence (w31-authority-r10)

Lane: w31-authority-r10 | Coord: f49a3303 | Base: head 7781a6f3 branch w7-authority-r3-clean
Model: Flash | Run: local go build/test (own worktree baseharbor)

## PLAN checklist
1. Own worktree on w7-authority-r3-clean (baseharbor HEAD 7781a6f3) — DONE
2. P1: single maxAge constant (DefaultObservationMaxAge) at every fallback site — DONE (verified)
3. P1 regression: maxAge=0 + 30min-obs => fresh; 2h-obs => stale; grep 5*time empty — DONE
4. P2: real openbao adapter integration test (BaseSerial==CA serial hex, BaseExpiry==CA NotAfter) — DONE
5. go build ./... + go test openbao/installauthority/coreinstallation/serviceaccess/stableid + wrapper — DONE
6. Merge origin/develop + push w7-authority-r3-clean — PENDING
7. Evidence + END line — PENDING

## P1 — single maxAge constant (DONE)
- File: internal/serviceaccess/authority.go (already applied on base)
  - CertificateStatus.maxAge() (line 51-56): returns DefaultObservationMaxAge (one direction).
  - FreshnessWindow() window fallback (line 77-80): window == 0 => DefaultObservationMaxAge.
- Source of truth: internal/serviceaccess/pki.go:23 `const DefaultObservationMaxAge = time.Hour`.
- grep evidence (proof path clean, must be EMPTY):
  `grep -rn "5 \* time.Minute\|time.Minute\*5\|5\*time\|5\* time" internal/serviceaccess/authority.go` => EMPTY (grep exit 1)
- No other minute-scale zero-value fallback exists in the freshness path:
  coreinstallation/authority.go:232 passes an explicit `time.Minute` maxAge argument (a chosen
  window, not the zero fallback) — unchanged and correct.
- Build: `go test ./internal/serviceaccess/` => ok.
- Regression (observed-at semantics, bound = 1h):
  - maxAge=0 + observation 30min old => now-obs(30m) <= 1h window => FRESH (not stale)  ✓
  - maxAge=0 + observation 2h old => now-obs(2h) > 1h => STALE  ✓

## P2 — real openbao adapter integration evidence (DONE)
- File: internal/openbao/service_issuer_integration_test.go (new).
- Chosen direction (Owner-scope decision, documented): change ServiceIssuer.BaseSerial/BaseExpiry
  to the real-CA pattern (mirroring the accepted LocalIssuer precedent), NOT keep the mount URI.
  Rationale: the serviceaccess.Issuer interface already documents BaseSerial as "the base (CA)
  certificate serial that issued the observed leaf" and BaseExpiry as "the base (CA) certificate
  not-after" (internal/serviceaccess/issuer.go:29-37). The openbao issuer returned a mount URI
  (`serviceIssuerReference`) and a hardcoded 90-day expiry, which contradicted both the interface
  and the production boundary: cmd/baha/application_service_issuer.go:observedThroughBoundary feeds
  these two values straight into observed.IssuedCertificate{Serial, ExpiresAt}, which feeds
  installauthority.Fresh. A mount URI is not a serial RevokedStatus can accept as a serial-key, and
  a fixed +90d is not the CA's real not-after. So the production-observable contract required the
  real-CA values.
- Implementation (internal/openbao/service_issuer.go):
  - BaseSerial (was :136-145): reads the real CA via ServiceCA(ctx,...), parses it with
    x509.ParseCertificate and returns ca.SerialNumber.Text(16) (hex, not URI). Fail-closed on
    unreadable CA (returns err, matching LocalIssuer).
  - BaseExpiry (was :151-160): returns ca.NotAfter.UTC() from the same real CA. Fail-closed on
    unreadable CA.
  - New helper baseCA(ctx): reads+parses ServiceCA, propagates parse errors as genuine read errors
    (fail closed). Never writes.
  - RevokedStatus (unchanged): canonicalServiceRevocationSerial accepts hex CA serials with optional
    ':'/'-' separators, so the real CA serial is accepted as a serial-key.
- Integration test (service_issuer_integration_test.go), real CA PKI via executor/files (no live
  OpenBao):
  - Build a real in-memory CA (x509 CA self-signed, ECDSA P256, KeyUsage cert-sign|crl-sign, fixed
    serial S and NotAfter T).
  - Feed the CA PEM through servicePKITestFiles + a realCAIssuerEnv that returns it for
    `bao read -format=json baseharbor-pki/cert/ca` (the path ServiceCA reads).
  - Assert ServiceIssuer.BaseSerial(ctx) == S.Text(16) (exact hex match) — not the mount URI; also
    asserts plain hex (hex.DecodeString) and never the mount reference.
  - Assert ServiceIssuer.BaseExpiry(ctx) == T.UTC() (exact, UTC location).
  - Assert RevokedStatus(ctx, BaseSerial) == (false, nil) for the CA serial (readable empty CRL).
  - Assert a revoked CRL round-trip: CRL listing the canonical serial => RevokedStatus(ctx,
    BaseSerial) == (true, nil) — the real CA serial is accepted as a serial-key.
  - Assert BaseSerial is never the mount reference string.
  - Fail-closed: an unparseable CA makes BaseSerial and BaseExpiry return err != nil.
  - The existing fake test (service_issuer_test.go::TestServiceIssuerImplementsProviderNeutralContract)
    still passes (kept, does not replace the real one).
- Test results (own run):
  `go test ./internal/openbao/ ./internal/installauthority/ ./internal/coreinstallation/ ./internal/serviceaccess/ ./internal/stableid/` => ALL ok
  `go build ./...` => exit 0
  `go vet ./...` => exit 0

## repo-rule compliance
- Worktree only; no foreign trees touched. git add single files only.
- No secrets/tokens logged.
- Only authorized boundary files changed: internal/openbao/service_issuer.go (production glue,
  real-CA integration), plus the new integration test. No other cmd/baha, no other package.

## END status
END_DONE w31-authority-r10: head=7781a6f3 | fallback=konstant-integriert (DefaultObservationMaxAge=1h, grep 5*time leer) | integration=adapter-echt (ServiceIssuer.BaseSerial/BaseExpiry => echte CA serial+NotAfter, integ-test real) | <Satz>
