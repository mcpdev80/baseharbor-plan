# w80-candidate-consent-harness: demo harness passes --confirm-candidate

- [x] w80-candidate-consent-harness · CORE-REPO test harness (scripts/acceptance.sh / guided-up pfad) uebergibt die vertraglich vorgesehene candidate-submission zustimmung (--confirm-candidate) an `baha app apply` weiter; gate bleibt ohne zustimmung ROT (negative regression), kein produktcode-umbau.
  <!-- lane w80 · coord f49a3303 · worker · branch work/r27-candidate-contract · evidence baseharbor-plan/evidence/r27-welle3-2026-11-03/candidate-contract/harness-consent-1.md -->

## PLAN

1. Mission + Task-Vertrag + diag-1 lesen; fehlerzeile im CORE-REPO-Harness verifizieren (DONE)
2. Consent-Gate im Produkt repo lokalisieren + digest-ableitung belegen (DONE)
3. Nachweisen, dass `run_consented` (tests/fixture-consent.py) provider-plan- consent kann, aber candidate-submission (--confirm-candidate) NICHT (DONE)
4. Minimal-fix in fixture-consent.py: --confirm-candidate fail-closed auflösen und mit flag wiederholen; negative regression (zustimmung wegzulassen => fehler bleibt) erhalten; KEIN produktcode-umbau
5. `go build ./...` + `go test ./internal/delivery ./internal/deployment ./cmd/baha -count=1` auf base 2cadfcee (work branch) gruen
6. Nur gezielte files committen (`git add <datei>`), push work branch; ls-remote == head
7. EIGENES-RUN: PR #1355 lifecycle + backup-restore JETZT ECHT gruen beobachten, Run-ID/status belegen
8. Evidence schreiben (checkbox->bullet), END-Zeile an agent, alle drei board-synchronisierungen

## Observable outcome (fehlerzeile belegt)

- CI-Output (diag-1, hosted run 41726952164 / docker/lifecycle):
  `Error: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`
  → `RuntimeError: guided-up failed with exit code 1` → `##[error]Process completed with exit code 1.`
- Quelle im Produkt repo: `cmd/baha/deployment_record.go:25-27` `errConsentRequiredForCandidateSubmission` (wortlich identisch), gefeuert aus `recordDeploymentBeforeMutation` (line 131), aufgerufen in `cmd/baha/app_apply.go:165` nach `promptConfirmCandidateSubmission`.
- Gate-Codepfad: `cmd/baha/app_candidate_consent.go` + `internal/delivery/candidate.go` (`CandidateConsentDigest` = sha256 der canonical JSON von `CandidateSubmission`; `finalizeCandidateConsent` prueft konstante zeit, `Validate` fail-closed).

## Fundstelle (wo harness gebaut wird)

- `scripts/acceptance.sh` ruft pro gate `bash tests/$gate/run.sh` auf; gate-skripte rufen `run_consented "$BAHA" ...` (lib.sh:182-183) → `python3 tests/fixture-consent.py "$@"`.
- `run_consented` wrappt den baha-aufruf, loest provider-plan refusale (`approval_required`/`impact-confirmation-required`) auf und setzt `BASEHARBOR_PROVIDER_CHANGE_CONSENT`. Er kennt den **candidate-submission**-pfad (`--confirm-candidate`) **nicht** => die zustimmung wird noch nicht uebergiebt (mission line 5).
- Demo-ref `cd9176e` ist aktuell, kein drift; fix gehoert in den CORE-REPO-harness, NICHT baseharbor-demo (fix-9-final bestaetigt).

## repo-rule compliance

- Nur evidence/datei + CORE-REPO harness (`tests/fixture-consent.py`) geaendert.
- KEIN produktcode-umbau: gate bleibt ohne zustimmung ROT (negative regression).
- branch = work/r27-candidate-contract (base 2cadfcee).
- Nur gezieltes `git add` der geaenderten harness-file; kein `git add -A`.
- gh api nur lesend; evidence gegen neutrales produkt-/harness-repo verifiziert.

## END

_LANE w80: END_DONE · fundstelle=tests/fixture-consent.py (run_consented) bietet provider-plan-consent, aber KEIN --confirm-candidate; fix=minimal candidate-consent-passthrough (fail-closed auloesen + flag wiederholen, negative-regression erhalten); branch work/r27-candidate-contract (base 2cadfcee) · <sha10> · lifecycle=<gruen|rot> lsremote=<sha10> · <Satz>_
