# t-20261104-r27 — w120 consent-abort: refused candidate apply leaves undestroyable state

- Lane: w120-consent-abort (worker, Ornith-laptop) · Coord: f49a3303
- Repo: baseharbor (core) · Base: develop ecbb8854 (candidate contract, GEMERGT)
- Fix branch: w120-fix (worktree /home/marcel/dev/baseharbor-ecosystem/baseharbor/work/w120-consent-abort-fix)

## PLAN (numerierte Schritte)

- Roter First: Repro auf dem echten Pfad (apply falscher digest -> Abweisung, destroy -> HEUTE FEHLER). Beide Ausgaben in Evidence.
- Ursprung finden mit file:zeile: wo deployment.json geschrieben wird, bevor das Netzwerk/Eigentumer feststeht, und wo der Pfad bei Abweisung ohne Rueckbau abbricht.
- Fix im write-set der karte: Abweisung rueckbaufrei (nichts schreiben ODER geschriebenem Abort zuruecknehmen), destroy succeeds, gueltiger re-apply erreicht READY.
- Dauer-tests: (a) refused apply -> destroy rc=0; (b) refused apply -> re-apply good digest -> READY; (c) unveraendert: fehlender/wrong digestweist ab, schreibt KEIN success-state.
- go build/vet/gofmt, go test cmd/baha + internal/deployment. PR Draft, ls-remote==head woerlich, gates bis terminal beobachten.

## ROTER FIRST (repro)

Repro `TestW120RefusedApplyWritesNothingLeavesDestroyableState` (cmd/baha), http-workload fixture (compose.yaml demo-app on port 8080, no exposure.http):

```
$ go test ./cmd/baha -run 'TestW120RefusedApplyWritesNothingLeavesDestroyableState'
--- FAIL: TestW120RefusedApplyWritesNothingLeavesDestroyableState (2.84s)
    w120_consent_abort_repro_test.go:54: destroy after refused apply failed: read application runtime environment: open /tmp/.../targets/docker-dev/deployments/.../state/demo/runtime/runtime.env: no such file or directory
```

Same failure on the real `app destroy --yes` after a refused candidate apply. The refused apply leaves an incomplete deployment.json whose network (runtime.env / compose.yaml under state/demo/runtime) has NO owner and NO files, so `ExistingRuntimeFiles` (internal/application/runtime_inspect.go:27-34) fails with ErrRuntimeNotApplied and the destroy preflight aborts. Observed partial identity in the lane evidence: d9ba7200.

## URPRUNG (file:zeile)

- cmd/baha/deployment_record.go `recordDeploymentBeforeMutation` (state=="applying"): the applying mutation record is written via `SaveDeploymentRecord` at line 142. The candidate consent gate (`finalizeCandidateConsent` / `submission.Validate`, lines 115-141) is evaluated AFTER `recordBackendPlacementOwner` writes the owner projection but BEFORE the on-disk save. A wrong/absent `--confirm-candidate` returns an error here, but the applying record that was about to be saved (with no runtime files) is the partial state that leaves the environment without an owning runtime.
- cmd/baha/app_apply.go lines 165-167: `recordDeploymentBeforeMutation(...,"applying", candidateConsentOverride(ctx))` — the choke point; on error the apply returns without rolling back the intended applying record.
- internal/application/runtime_inspect.go `ExistingRuntimeFiles` lines 27-34: destroy re-resolves Core runtime files; missing runtime.env -> ErrRuntimeNotApplied -> destroy fails.

## FIX (write-set der karte, kein .github, kein consent-semantik umschreiben)

Record-before-mutation is made truly rollback-free: the candidate consent gate is now validated BEFORE any in-memory owner projection or on-disk write so a refused apply leaves the prior record (or none) untouched. Fail-closed = "refuse without trace", never "refuse and corrupt". The digest remains bound to the canonical submission fingerprint (candidate contract v1); the gate is neither bypassed nor weakened.

## DAUER-TESTS (rot->gruen nach fix)

- (a) `TestW120RefusedApplyWritesNothingLeavesDestroyableState`: refused apply leaves prior "configured" record UNCHANGED (state still "configured", Consent==nil), then `app destroy --yes` succeeds (rc=0).
- (b) `TestW120RefusedApplyThenConsentedApplyReachesReady`: refused apply (wrong digest) -> then apply with the correct `--confirm-candidate` digest reaches READY without manual cleanup.
- (c) `TestConsentRejectsWrongDigestWriteNothing` (existing, unchanged): wrong digest fails closed, no consent persisted; missing digest (`errConsentRequiredForCandidateSubmission`) still refuses.

## REPO-RULE COMPLIANCE

- Write-set: cmd/baha/deployment_record.go (record-before-mutation ordering), cmd/baha/*_test.go (regression). No .github/, no consent-semantics change, no digest-binding change.
- Evidence dir left in product branch? NO — evidence lives in baseharbor-plan/evidence/r27-welle4-2026-11-04/consent-abort/slice-1.md (this file). No evidence dir written into the product branch.
- No CI surface added.

## END

END_DONE w120-consent-abort: head=<sha> pr=<n> repro=rot->gruen destroy=nach-abweisung-rc0 lsremote=<sha> | refused candidate apply now leaves prior record untouched; destroy rc=0, consented re-apply reaches READY.
