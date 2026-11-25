# Bug Hunt H-V50 — TLS/cert & rotation surface

Lane: w195-0428-224-hunt-v50
Type: pure finding, no product changes (read-only)
Anchor (ls-remote witness): `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82` refs/heads/develop
`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82 refs/heads/develop`
Worktree: `/tmp/opencode/w195-hunt-v50-wt` (cut at exact develop tip, detached HEAD at `99d9ddebc`)
Build: `go build -o /tmp/baha-w195 ./cmd/baha` => exit 0 (surface compiles)
Vet: `go vet ./internal/dcspki/ ./internal/serviceaccess/ ./internal/exposure/` => clean
Evidence location: baseharbor-plan (planning repo `https://github.com/mcpdev80/baseharbor-plan.git`, verified via `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)` — this is the only planning repo; the `workers/baseharbor-plan` dir is a bookkeeping checkout, never used for evidence)

## Cross-reference (no duplicate rows)

- H-V47 (`../bughunt-hv47-upgrade-migration/README.md`, same anchor `99d9ddebc`): version-upgrade & migration surface. Touches NO TLS/cert code (`git grep` for cert/tls/x509/rotation in that akte returns nothing on the cert rows). No overlap — H-V50 is a disjoint slice.
- H-V46 (state-lifecycle / destroy-quarantine): covered elsewhere; the etcd DCS PKI and OpenBao trust roots are runtime-internal trust anchors, not lifecycle/quarantine records. H-V50 does not restate lifecycle vocabulary.
- H-V45 (cert-failure error vocabulary): H-V50 row BF-50-7 feeds H-V45 cards; cross-referenced only, not restated.

## PLAN

- Refresh develop tip via ls-remote, anchor SHA in header (done)
- Fresh isolated worktree at exact tip (done, `/tmp/opencode/w195-hunt-v50-wt`)
- Map cert loading paths: demo test-only fixtures (0428-284 era) vs product code (done)
- Inspect expiry handling and rotation-on-upgrade / cross-ref H-V47 (done)
- Inspect trust-store/CA pinning incl baseharbor-node-connector (done)
- Inspect error text on cert failure -> H-V45 cards (done)
- Write per-row file:line + proposed card lines (done)
- Commit evidence to baseharbor-plan worktree, push, verify on origin/main (done)
- Clean worktree, END_DONE with fund count (this action)

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`
- Worktree `/tmp/opencode/w195-hunt-v50-wt` checked out at exactly `99d9ddebc` (detached HEAD).
- Read-only hunt: no candidate branch, no commits in the product repo, so there is no commit-ancestor relationship to prove and no PR was opened.

## Surface map (findings)

Rows are grouped by the mission's four surfaces. Every row is a concrete file:line with a
proposed card line. "No gap" rows are findings that document existing, correct fail-closed
behaviour and propose no card (recorded so later hunts do not duplicate them).

### A. Cert loading paths — demo test-only fixtures vs product

BF-50-1  demo-app `tlsConfigFromCAFile` (baseharbor-demo/demo-app/main.go:714-727) loads a CA
file into `x509.NewCertPool()` and sets `MinVersion: tls.VersionTLS12` + `RootCAs`. It is used
only as a *client-side* trust bundle (redis/S3/otel/oidc), never to serve the demo's own HTTPS
listener, whose server cert comes from `TLS_CERT_FILE`/`TLS_KEY_FILE`. This is the 0428-284 era
demo, intentionally decoupled from product cert semantics. Proposed card: none (documented;
matches "test-only demo fixture, no product binding").
file: line `demo-app/main.go:714-727`, `demo-app/main.go:652-665` (serverTransport), `demo-app/main.go:86-88` (ListenAndServeTLS).

BF-50-2  Product `existing`-mode cert load (`cmd/baha/app_tls.go:459-481` readManagedCertificate,
`483-492` certificateFromPEM, `494-508` validateLeafCertificate) parses PEM/DER, requires
X509KeyPair match, and validates NotBefore/NotAfter + VerifyHostname. Clear product/test split:
product loads with full validation; test helpers in `app_runtime_init_test.go:206-225`
(testCertificatePair) and `app_secret_tls_test.go:60-95` mint short-lived self-signed leaves for
validation only. Proposed card: none (correct split, no gap).
file: line `cmd/baha/app_tls.go:459-508`, `cmd/baha/app_runtime_init.go:365-374` (dir scan filters non-leaf/expired/CA), `cmd/baha/app_secret_tls.go:78-102`.

BF-50-3  `app_runtime_init.go:365-381` discovers a cert/key pair in a configured cert dir during
runtime init: it skips any cert that is expired, not-yet-valid, a CA (`leaf.IsCA`), or whose
hostname does not verify against the FQDN, then requires a unique X509KeyPair match. Failure
returns `cmd/baha/app_runtime_init.go:402` "no valid certificate/private-key pair for FQDN ... found".
Proposed card: none (robust fail-closed discovery).
file: line `cmd/baha/app_runtime_init.go:346-413`.

### B. Expiry handling

BF-50-4  Application TLS expiry is enforced in three product paths with identical windows:
`cmd/baha/app_tls.go:494-508` (validateLeafCertificate), `cmd/baha/app_secret_tls.go:96-102`
(setApplicationTLSMaterial). Both reject `now.Before(leaf.NotBefore)` and `!now.Before(leaf.NotAfter)`
with human-readable timestamps. Proposed card: none (no gap).
file: line `cmd/baha/app_tls.go:494-508`, `cmd/baha/app_secret_tls.go:96-102`.

BF-50-5  `app_tls.go` surfaces expiry with graded health prefixes (`certificateHealthPrefix`,
`app_tls.go:547-559`: `[FAIL]`<=0d, `[CRITICAL]`<=7d, `[WARN]`<=30d, `[OK]` otherwise) and
`certificateRemaining` (`app_tls.go:535-545`), rendered in `printApplicationTLSStatus`
(`app_tls.go:561-588`) and diagnostics (`app_tls.go:590-612`). No proactive pre-expiry *alert*
threshold drives an automatic action — expiry is detected at inspect/update time only.
Proposed card: **optional** — "surface a calendar/heartbeat alert for certs within N days of expiry"
if the product owns lifecycle alerts; otherwise record as done-as-designed. Not a defect.
file: line `cmd/baha/app_tls.go:535-559`, `561-588`.

BF-50-6  ACME mode (`app_tls.go:89-91, 375-376, 581-582`) delegates expiry entirely to the
workload TLS provider; BaseHarbor renders only "delegated". The actual issuance/expiry lives in the
external ACME challenge — outside this write-set. Proposed card: none (delegated; document boundary).
file: line `cmd/baha/app_input_resolver.go:457-458`, `cmd/baha/app_runtime_init.go:126-127,287-288`.

### C. Rotation on upgrade

BF-50-7  `cmd/baha/app_tls.go:159-202` (updateApplicationTLS) is the only product cert-rotation
entrypoint: it compares source vs installed `NotAfter`, refuses downgrades
(`app_tls.go:186-188` "refusing TLS certificate downgrade"), and on install stops the workload +
managed exposure, writes the new files, restarts and re-verifies with atomic rollback
(`cmd/baha/app_tls.go:204-278` installApplicationTLS). This is a *manual* operator rotation
(`baha app tls update` + MCP `runtime-identity.tls.update`), not an automatic upgrade-time rotation.
Proposed card: **optional** — "rotate on version upgrade / manifest TLS-mode change" is an explicit
product-scope decision (rotation currently is change-driven, not upgrade-driven); if the product wants
automatic rotation on upgrade, card it separately. Not a defect in current behaviour.
file: line `cmd/baha/app_tls.go:159-202, 204-278`, `cmd/baha/mcp_identity_tls_tools.go:45-58`.

BF-50-8  etcd DCS PKI `internal/dcspki/pki.go` rotates leaf certificates under the existing CA
before expiry (`leafLifetime=90d`, `renewBefore=14d`, `Ensure` `pki.go:86-103`) and is
deliberately fail-closed on CA rotation (`caGuard=90d`, `pki.go:87-89` "etcd CA rotation requires
explicit fenced DCS migration"). This is the strongest rotation path in the tree. Proposed card:
none (correct, well-scoped).
file: line `internal/dcspki/pki.go:19-24, 86-103, 137-189`.

BF-50-9  Local service-access issuer `internal/serviceaccess/local_issuer.go`: CA validity is 5y with
a 90-day pre-expiry trust check on load (`local_issuer.go:174`) requiring explicit trust rotation;
leaf TTL capped at 90d (`Issue` `local_issuer.go:237-249`), `Renew` validates the current leaf is
signed by the local CA and not revoked (`local_issuer.go:264-289`), and revocation is enforced via
a signed CRL (`Revoke`/`RevokedStatus` `local_issuer.go:324-452`). Proposed card: none (correct).
file: line `internal/serviceaccess/local_issuer.go:100-137, 174, 229-289, 324-452`.

BF-50-10 Node connector bootstrap re-enrollment `internal/nodeservice/reenroll.go` reuses the
security-critical `targetaccess.BootstrapEnroll`/`InstallEnrollment` checks (nonce, pinned server
identity, client-only leaf binding, one-time token) — rotation re-anchors a fresh leaf under the
same pinned CA. Proposed card: none (correct; no separate rotation logic to grade).
file: line `internal/nodeservice/reenroll.go:11-75`.

### D. Trust-store / CA pinning in connectors (baseharbor-node-connector included)

BF-50-11 Node bootstrap client `internal/targetaccess/bootstrap.go:163-193` pins: `MinVersion:
tls.VersionTLS13`, `RootCAs` from the trust bundle, plus `VerifyConnection` requiring a presented
peer cert and `verifyPeerIdentity` against `ExpectedServerIdentity`. Proposed card: none (strong).
file: line `internal/targetaccess/bootstrap.go:163-193`.

BF-50-12 Install-enrollment chain validation `internal/targetaccess/install.go:16-57`: rejects
non-client-only leaves, enforces the scoped URI identity, matches the local private key, builds a
`RootCAs` pool from the returned trust bundle (`parseCertPool` `install.go:112-132`, rejects any
non-CA), and verifies the full chain + expiry against `now`. Proposed card: none (correct).
file: line `internal/targetaccess/install.go:16-57, 112-132`.

BF-50-13 `internal/targetaccess/enrollment.go:84-88` rejects an expired enrollment cert
("enrollment certificate is expired"); `install.go:48-50` rejects expiry mismatch between the
response and the certificate. Proposed card: none (correct).
file: line `internal/targetaccess/enrollment.go:84-88`, `internal/targetaccess/install.go:48-50`.

BF-50-14 Caddy exposure `internal/exposure/caddy.go` serves the configured leaf under
`existing` mode and trusts the workload mTLS CA via `workload-ca.pem` (`tls_trust_pool file`,
`caddyfile` `caddy.go:581-583`); `existing` preflight requires `cert.pem`/`key.pem` present
(`caddy.go:134-144`). Trust is file-mounted, not ambient. Proposed card: none (documented boundary).
file: line `internal/exposure/caddy.go:129-148, 428-431, 490-508, 563-565`.

BF-50-15 Service-access HTTPS client `internal/serviceaccess/http_gateway.go:552-586` builds a
`RootCAs` pool from the trust bundle and loads the client identity via `LoadX509KeyPair`; a missing
bundle fails with "no certificates". Proposed card: none (correct).
file: line `internal/serviceaccess/http_gateway.go:552-586`.

### E. Error text on cert failure (feeds H-V45 cards)

BF-50-16 `conciseTLSStatusError` (`cmd/baha/app_tls.go:384-399`) maps raw x509 failures to stable,
user-facing phrases: expired -> "certificate expired", hostname mismatch -> "certificate does not
cover configured hostname", key mismatch -> "certificate and private key do not match", else
"certificate state could not be verified". This is the primary error-text seam for H-V45 cards.
Proposed card: **optional** — "cover additional failure modes (e.g. revoked, intermediate-broken)
with stable phrases" only if H-V45 requires them; currently the four phrases are coherent.
file: line `cmd/baha/app_tls.go:384-399`.

BF-50-17 Product error strings are descriptive and include the offending timestamp in RFC3339:
`cmd/baha/app_tls.go:500` "certificate expired at <time>", `app_tls.go:187` downgrade message with
both expiries, `cmd/baha/app_secret_tls.go:101` "TLS certificate expired at <time>". Node connector
errors are terse and machine-oriented (`enrollment certificate is expired`, `enrollment response
expiry differs from certificate validity`). Consistent two-register vocabulary (human CLI vs machine
wire). Proposed card: none (no gap; document as the H-V45 source).
file: line `cmd/baha/app_tls.go:496-504, 186-188`, `cmd/baha/app_secret_tls.go:97-101`,
`internal/targetaccess/enrollment.go:84-88`, `internal/targetaccess/install.go:48-50`.

## Summary

- Total findings: 17 (BF-50-1 .. BF-50-17).
- Defect cards to propose (real gaps): **0**.
- Optional/scope-decision cards (Owner/product call, not defects): BF-50-5 (expiry alert),
  BF-50-7 (rotate on upgrade), BF-50-16 (extra error phrases) — each recorded with file:line and
  scoped to product-scope decisions, not defects.
- Documented-correct rows (no card, prevents duplicate filing): BF-50-1,2,3,4,6,8,9,10,11,12,13,14,15,17.

## Cleanliness

docker ps -a before: (no containers started — read-only hunt, no compose/daemon)
docker ps -a after:  (none)
worktree removed: `git worktree remove --force /tmp/opencode/w195-hunt-v50-wt`
cleanliness: worktree gone, no containers/networks/volumes/state created, no stray files under the
ecosystem root.

## END

END w195-0428-224-hunt-v50 DONE
Fund count: 0 defect cards; 3 optional/scope-decision rows (BF-50-5, BF-50-7, BF-50-16) handed with
file:line for an Owner/product scope decision; 14 correct-behaviour rows documented as no-card.
