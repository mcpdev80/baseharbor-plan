# Fix r6 — PR #1348, points 1 + 2

- Worker lane w17-authority-r6; coord f49a3303; base = w7-authority-r3-clean @ f58fb180 (review base).
- Worktree /tmp/opencode/w17-authority-r6-wt on f58fb180; baseharbor repo itself on develop (9a57107f); PR is a commit on w7-authority-r3-clean, NO merge, NO force-push.

## Punkt 1 — OpenBAO CRL fail-closed (internal/openbao/service_pki.go + service_issuer.go)
- Finding: RevokedStatus -> revokedSerialInResponse treats empty/`{}`/`null`/missing data.serials as (false,nil); only malformed JSON errors. Empty list currently = "not revoked" = fail-open window for an unreadable provider response.
- Fix: empty/malformed/missing provider revocation response => revoked=true (or err!=nil); only a provably valid (parseable) empty serials list => not-revoked.
- Regression via fake server: (a) empty body -> reject, (b) junk body -> reject, (c) valid CRL without serial -> not-revoked as before.

## Punkt 2 — ObservedAt through the wrapper (cmd/baha/application_service_issuer.go ~101+134)
- Finding: resolveManagementConnectionIssuer computes observedAt := time.Now().UTC() and ignores observed.ObservedAt from observedThroughBoundary (which is time.Now() at line ~134). Freshness not checked against real observation.
- Fix: pass observed.ObservedAt to installauthority.Fresh.
- Test strengthened: TestResolveManagementConnectionIssuerSuppliesObservedAtFreshness zero/future/stale via the WRAPPER path; future case must fail with wrong time.Now() assumption (assert observedAt==status.UpdatedAt threaded through).

## Tests / checks
- go build ./... ; go test ./internal/openbao ./internal/installauthority ./internal/coreinstallation ./internal/serviceaccess ./internal/stableid + wrapper e2e in cmd/baha (only affected tests).
- write-set grep empty in .github/scripts; not global cmd/baha green.

## END
- DONE. head=bcb7b54a8c378e84c93e28de4e8b08c60cc810a1. crlfailclosed=3wrapper observedAt=e2e3.
- FF merge origin/develop (9a57107f is ancestor, .github net-diff empty) then commit bcb7b54a on w7-authority-r3-clean (f58fb180); FF push f58fb180..bcb7b54a; ls-remote==head.
- go build ./... rc=0; go vet openbao/cmd/baha rc=0; focused pkg tests green; wrapper e2e TestResolveManagementConnectionIssuerSuppliesObservedAtFreshness green and regression-guarded (future case fails with old time.Now()).
