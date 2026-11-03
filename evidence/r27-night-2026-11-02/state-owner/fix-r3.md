# Fix round r3 — grant-only TenantOwnerResolver + real seams

Lane: w14-stateowner-resolver · Role: Worker · Coord: f49a3303
Basis: PR #1347 head 47c1993d (branch work/r27-state-owner, base develop)
Evidence contract: plain bullets, no checkboxes.
Befundquelle: review-1347b.md befunde 1-3. Kernfehler: deployment.TenantOwnerResolver war ein VETO-hook
(authorized=false => ErrDeploymentOwnerForeign) und coreinstallation.Load lief NUR wenn hook==nil. Der
CLI-hook gab bei nicht-aufloesbarem/nicht-tenant target (true,nil) => Core-pruefung komplett umgangen
(fail-open bei config-fehler).

## PLAN

1. HOOK SEMANTIKN: internal/deployment/deployment_store.go VerifyDeploymentOwner — TenantOwnerResolver
   ist jetzt GRANT-only: (true,nil) => tenant-pfad autorisiert, return nil. Alle andere rueckgaben
   ((false,nil), (false,err), (true,err)) => NICHT autorisiert, durchfallen auf den unveraenderten
   coreinstallation.Load ein installations-owner-check. Doku-Kommentar ergänzt: grant-only; a resolver
   that does not grant falls through to the standard single-installation-owner verification.
2. CLI HOOK: cmd/baha/deployment_record.go init — !ok oder !isTenant => (false,nil) durch zur
   Core-pruefung (frueher (true,nil), fail-open). tenant+connectorScopeForTarget err => (false,err)
   propagiert. scope.Validate() err => (false,nil); nur gueltiger scope => (true,nil). fail-open
   vorueber.
3. TESTS (echte seams):
   a) internal/deployment: unit-test fuer alle drei hook-ergbnisse (grant=>nil,
      (false,nil)=>faellt durch auf coreinstallation-pruefung (fehlt/corrupt => dessen fehler, nicht
      Foreign-only), err=>propagiert). Tests TestTenantOwnerResolverGrantOnly +
      TestDeploymentOwnerTenantBypassGrantOnlyThroughSeam (nein) + bestehende TestDeploymentOwnerTenantBypassRemoved.
   b) cmd/baha: integration-test des echten pfades recordPendingDeployment/SaveDeploymentRecord —
      negativer tenant scope => abgewiesen (beweis: kein bypass, kein persisted state); nicht-tenant
      target ohne gueltige Core installation => abgewiesen; gueltiger tenant => durchgelassen.
      TestDeploymentOwnerResolverCLIFallsThroughProvesNoBypass + TestDeploymentRecordHookPropagatesError.
   c) fixture-helfer configureTestTargetEmpty (cmd/baha/target_test_helpers_test.go): RemoveAll/
      TargetStateRoot-fehler => t.Fatal bei err statt stiller skip.
4. ANSANDE-PFLICHT: merge origin/develop (is-ancestor rc=0); write-set grep-leer (.github/scripts/contracts).
5. TESTS: TMPDIR=/tmp go build ./... + go test ./internal/deployment ./cmd/baha.

## repo-rule compliance

- Write-set streng auf Task-Vortrag begrenzt: internal/deployment/deployment_store.go,
  cmd/baha/deployment_record.go, cmd/baha/target_test_helpers_test.go, neue state-owner tests
  (deployment_owner_binding_test.go, deployment_tenant_owner_hook_test.go). Keine CI/authority-Dateien.
- Merge origin/develop, FF auf remote tip, ls-remote Beweis.
- STOP-Regel eingehalten: 1 Iteration je Punkt; bei Unklarheit END_BLOCKED mit datei:zeile. Kein
  Merge-Force, kein Force-Push.

## END line

END_DONE w14-stateowner-resolver: head=<sha> grant-only=3tests | <Satz>
