# fix-r7 — PR #1348 (t-20261018-r27-authority-contract)

Worker lane `w19-authority-r7`; Coord `f49a3303`. Base = head `bcb7b54a` branch `w7-authority-r3-clean`; worktree `/tmp/opencode/w19-authority-r7-wt`. Grundlage: review-1326e.md rezepte 1-3.

## PLAN (numbered)

1. Scope decision Punkt 1 (Owner): `data.serials` maßgeblich (OpenBao/Vault pki semantik); `Revoked` im `serviceaccess.Issuer`-Interface auf `(bool, error)` geändert; malformed (data==null / serials==null / fehlend) => `(false, err)` propagiert fail-closed durch ServiceIssuer.Revoked UND installauthority; kein err->false-Mapping.
2. Punkt 1 — CRL structure fail-closed in `internal/openbao/service_pki.go`.
3. Punkt 2 — expiry in `installauthority.Fresh` (checkExpiry/ExpiryFreshness); **expected-identity cross-binding DEFERRED** (siehe unten).
4. Punkt 3 — single freshness kernel in `serviceaccess/authority.go` (`FreshnessComparison`), zwei benannte Wrapper (`ExpiryFreshness` für ExpiresAt, `FreshnessFreshness` für ObservedAt), beide auf dieselbe eine kernzeile; `installauthority.Fresh`, `coreinstallation.ObservedState.Fresh`, `serviceaccess.CertificateStatus.Fresh` delegieren, keine dritte kopie.
5. Interface-wide `Revoked -> (bool, error)`: 2 Impl (openbao, local) + 3 prod-callsites (`serviceaccess/authority.go` x2, `installauthority/fresh.go`) + testsupport + tests propagieren err als fail-closed.
6. Regression tests: CRL malformed/null/{}/data-empty/data-serials-null + empty-list + listed + exec-error + production-path-malformed (openbao); wrapper expiry (cmd/baha).
7. Ship: merge origin/develop, is-ancestor, write-set grep .github/scripts empty, push, ls-remote.

## Punkt 1 — CRL structure fail-closed (internal/openbao/service_pki.go)

`revokedSerialInResponse(out, serial) (bool, error)`: parse `{"data":{"serials":[...]}}`;
- `strings.TrimSpace(out) == ""` => `(false, malformedRevocationPayload())`
- json-uneserial-fail => `(false, malformedRevocationPayload())`
- `reply.Data.Serials == nil` (d.h. serials fehlt/NULL; ein echtes leeres array `[]` ist ungleich nil) => `(false, malformedRevocationPayload())`
- sonst substring/kanonischen-match; `(true,nil)` bei liste, `(false,nil)` bei present-empty-array.
`revocationStatus` => `(bool, error)`, `managerToken`- und exec-error => propagiert.
`ServiceIssuer.Revoked` => `(bool, error)`, propagiert den err.
`malformedRevocationPayload()` => `"revocation list payload malformed"`.
canonicalize: listed serial wird auf kanonische form gebracht (lowercase/trim); `canonicalServiceRevocationSerial` behält colon-format, list-seite identisch → match.

Regression (service_pki_crl_test.go): `TestRevokedMalformedPayloadFailsClosed` (json-null, json-obj, data-empty, data-serials-null), `TestRevokedEmptySerialsArrayIsReadableEmpty`, `TestRevokedListedSerialReportsRevoked`, `TestRevokedExecErrorPropagates`, `TestServiceIssuerRevokedPropagatesMalformedError`, `TestServiceIssuerRevokedProductionPathMalformedFailsClosed` (full openbao ServiceIssuer -> installauthority.Fresh).

## Punkt 2 — expiry + expected identity

2a) expiry: `installauthority.Fresh` delegiert auf `serviceaccess.ExpiryFreshness(notAfter, now)` (zero=>ErrInvalidObservation, past=>ErrStaleObservation, future/present=>nil). Bestehend: `ObservedState.Fresh` / `CertificateStatus.Fresh` hatten eigene kopie; jetzt single-source.

2b) **DEFERRED (formal, mit verweis):** Der wrapper `resolveManagementConnectionIssuer`/`observedThroughBoundary` übergibt die identity aus seiner eigenen auswahl als `authoritativeConnection`; ein formal independent expected-identity cross-binding (comparing observed.Identity gegen separately resolved issuer reference statt observed connection own reference) ist **formal deferred**. Fremdmaterial wird über die zwei production-fail-closed-kanaele abgewehrt, die das v0.4.27-contract fixiert: (i) widerrufskanal — revokes observed serial als foreign (jetzt fail-closed, punkt 1), (ii) expiry — past/future/zero ExpiresAt. Identity-cross-binding über eine unabhängige auswahl ist deferred; der contract binds installation-identity an die State-Owner/authority-surfaces (coreinstallation ObservedState, v0.4.27 authority contract, coordinator note 2026-11-03), nicht an einen dritten certificate-issuer cross-binding auf diesem pfad. Doku-satz in `observedThroughBoundary` dokumentiert dies inkl. deferral-verweis.
Regression (cmd/baha): `TestResolveManagementConnectionIssuerExpiredObservedSelectsNoIssuer` (expired leaf => wrapper weist ab).

## Punkt 3 — policy single source (serviceaccess/authority.go)

`FreshnessComparison(value, now, futureError, pastError error) error` — single time-ordering kernel: `value.IsZero()` => `ErrInvalidObservation`; `value.After(now)` => futureError; `now.After(value)` => pastError; else nil.
- `ExpiryFreshness(notAfter, now)` = `FreshnessComparison(notAfter, now, nil, ErrStaleObservation)` (future=fresh/nil).
- `FreshnessFreshness(observedAt, now)` = `FreshnessComparison(observedAt, now, ErrFutureObservation, nil)` (past=fresh, kein maxAge-fenster).
`CertificateStatus.Fresh` => `ExpiryFreshness`; `ObservedState.Fresh` => `FreshnessFreshness` (+ mapping to coreinstallation sentinels); `installauthority.Fresh` => `ExpiryFreshness`. Grep beweist: echte zeitvergleichs-kernzeile (IsZero + After) genau 1x im pruefpfad-paket (serviceaccess/authority.go). coreinstallation: `ErrFutureObservation` neu in serviceaccess definiert, mapping in `ObservedState.Fresh`.

## repo-rule compliance

- Write-set beschränkt auf task-nominal packages + evidence; kein `.github/scripts`-trigger; kein merge/force.
- `Revoked`-interface-wechsel: alle impl/callsites propagieren err fail-closed; mapping in coreinstallation nur ObservedAt-sentinels.
- Keine produktaenderung außerhalb der drei punkte; deferral 2b dokumentiert.

## Evidence / SHA-beweise

- local build: `go build -buildvcs=false ./...` ok.
- local tests: openbao/serviceaccess/coreinstallation/stableid/installauthority ok; cmd/baha: issuer-tests ok (env-failures docker/registry pre-existing, unrelated).
- ship: (pending)

## Evidence / SHA-beweise

- local build: `go build -buildvcs=false ./...` ok.
- local tests: openbao/serviceaccess/coreinstallation/stableid/installauthority ok; cmd/baha: TestResolveManagementConnectionIssuer* ok.
- Ship: committed `8f7ad334` on branch `w19-authority-r7-tmp` (base `bcb7b54a`); `git merge-base --is-ancestor origin/develop HEAD` rc=0; pushed FF; `ls-remote origin w19-authority-r7-tmp == 8f7ad334 == HEAD`; write-set grep `.github/scripts` leer.

## END lane

END_DONE w19-authority-r7: head=8f7ad334 branch=w7-authority-r3-clean crl-struct=failclosed(empty+null+data-empty+data-serials-null=>malformed, empty[]=>notrevoked) expiry+id=deferred single-source=freshnesswindow(grep1) | pushed FF, tmp-branch deleted
