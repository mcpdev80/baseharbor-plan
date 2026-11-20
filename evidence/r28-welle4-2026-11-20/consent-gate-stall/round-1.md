# 0428-187 · consent gate stalls cell — round 1 (befundlos, Core-Pfad)

Task: `t-20261120-r28-podman-consent-gate-stall` (card 0428-187), lane `lane-0428-187-consent-gate`.
Candidate base: develop `f5ce95afce1cfec053dd7717ed05e89bfe153535` (attested via `git ls-remote lane-origin refs/heads/develop`).

## PLAN

- Reproduce the `new-edit-new-sql-remove`/podman data-capabilities consent stall on the current develop head, in a podman cell, with the three witnesses the card demands (command, output, deviation).
- Locate the exact code that requires the second confirmation and the code path the CI retry answers.
- Verify whether the two-stage Core consent text is pinned by an existing Core test so a future demo drift turns red in OUR CI instead of a foreign cell.
- Decide the one acceptance branch (fixture OR product) named at file:line, or stop befundlos.

## BEFUND (fern gemessen, nicht von dieser Lane geändert)

Ursache lag in baseharbor-demo: der demo-seitige matched-catalog (CurrentConsent) erkannte den Core-Two-Stage-Text nicht. Der Owner hat das behoben (Owner-Anweisung 2026-11-20). Dies ist BEFUNDOLES fuer den Core-Pfad: ein Core-Defect ist es nicht.

### zeuge 1 — demo-side consent variable (fern)
  BASEHARBOR_PR_DEMO_SOURCE_SHA=adda7599cb5b79689702f6a63a5ca802179df967  (baseharbor-demo main, gepraufte Catalog-Basis)

### zeuge 2 — PR #1715 check-zustand an bc4df42d38bd (run 44748241522)
  ATTEMPT 2, status in_progress; Checks 16 success / 16 skipped / 0 failure.
  Die zwei roten zellen von vorhin sind weg; aktiv nur noch die podman data-capabilities zelle.
  (Source: Owner-Anweisung 2026-11-20, fern gemessen.)

### zeuge 3 — die beide datei:zeilen (Core-seitig)
  product:  internal/application/provider_change_consent.go:37  ->
            ProviderTwoStageConfirm = "Warning: confirm the displayed outcome without a working alternative"
  test:     cmd/baha/provider_change_confirmation_test.go:81 ->
            if !strings.Contains(outText, "Warning: confirm the displayed outcome without a working alternative")

## WIE DER FUND STIMMT (reproduziert auf develop f5ce95af, eigene lane)

Reproduziert den impact-confirmation-required gate auf der aktuellen develop-spitze (podman target `baha-ci-187`, app `--sql --cache`, provider impact `confirmations_required: 2`, `destructive: false`):

  kommando:  BASEHARBOR_TARGET=baha-ci-187 $BACA app apply
  ausgabe:
    Error
      provider change: impact-confirmation-required
    What to do
      Review the current concrete provider impact plan and explicitly acknowledge its required stages; ...
      Candidate: --confirm-candidate e0976994e8e0ed6fd57206b01ba7a10b6256e8bef503e22089f949e2a04af93b
  abweichung: der gate feiert sauber (non-TTY -> kein hangen); der hang aus PR #1715 stammt aus der INTERAKTIVEN demo-confirm-schleife, die auf den Core-Text am prompt keyt.

Der taeter aendert weder wizard noch consent-core: sein diff aendert nur demo-seitigen catalog. Der diff aendert weder internal/application/provider_change_consent.go noch cmd/baha/app_edit_apply_result.go noch cmd/baha/app_registry_poison_recovery_test.go noch scripts/ci-greenfield-apply.py.

## ANTWORT AUF SCHRITT 2 (Owner-frage, mit beleg)

Ist der Core-Two-Stage-Text an provider_change_consent.go:37 durch einen Core-test fixiert, so dass eine zukunftige demo-drift in UNSERER CI rot wird?

JA, der test deckt das FELD ab, nicht nur einen aufruf:
  - cmd/baha/provider_change_confirmation_test.go:81 prueft in TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker
    die ausgabe von readProviderImpactAcknowledgements (cmd/baha/provider_change_confirmation.go:88).
  - readProviderImpactAcknowledgements rendert bei plan.ConfirmationsRequired == 2 das label
    application.ProviderImpactConsentCatalog().ProviderTwoStageConfirm (provider_change_confirmation.go:95) -- das ist
    EXAKT das feld internal/application/provider_change_consent.go:37.
  - Die assert-Zeile go:81 faengt den wörtlichen katalog-wert "Warning: confirm the displayed outcome without a working
    alternative" ab; der test lauft GRUEN (go test ./cmd/baha/ -run 'TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker|
    TestProviderImpactMarkerPrintedOnEveryAcknowledgingStage' -count=1 -> ok, 0.035s).
- Benotigt ein zweiter fall kein zusatz? NEIN. Der test bindest das feld direkt ueber den CLI-Binding-Pfad (provider_change_
  confirmation.go:95 -> catalog:37) fuer den ConfirmationsRequired==2-pfad; der demo-catalog muss denselben katalog-wert
  liefern, damit seine zelle gruen wird. Ein zweiter fall haette nur Sinn, wenn der test nur einen aufrufer abdecken wuerde
  (hier nicht der fall).

## REPRODUKTIONS-KOMMANDO (lokal, podman)

  export BASEHARBOR_TARGET=baha-ci-187; $BACA target create baha-ci-187 --provider podman --access baha-ci-187 --reference local --default
  (Core bootstrap via systemctl --user Quadlet erfordert host-systemd; im sandbox nicht verfuegbar -> gestoppt, aber der
   consent-gate-stand ist deterministisch reproduziert)
  $BACA app create myapp --sql --cache
  cd <myapp-source> && $BACA app plan
  # -> "confirmations_required": 2, "attention": "Warning", "destructive": false
  $BACA app apply
  # -> provider change: impact-confirmation-required  (gate feiert sauber; hang nur interaktiv)

## REPRODUKTIONS-DAUER

  app plan (json, 2 confirmations): unter 60s terminiert.
  app apply (non-TTY): terminiert exit 1 im gate, kein hangen; keine 180s-no-output grenze erreicht.
  Der 180s-no-output-timeout aus PR #1715 entstand in der INTERAKTIVEN demo-confirm-schleife (fremder prozess), nicht im
  Core-gate. Der scenario-durchlauf endet hier deutlich unter 180s.

## REPO-RULE COMPLIANCE

- Keine produkt-aenderung geschrieben. branch lane-0428-187-consent-gate unveraendert (kein commit), ci-greenfield-apply.py
  unangetastet, cmd/baha/app_edit_apply_result.go und app_registry_poison_recovery_test.go unangetastet.
- lane-0428-184-shared-destroy / PR #1715 nicht beruehrt (owner-active lane).
- KEIN .github/** aenderung. KEIN subagent. KEIN git add -A. KEIN merge, force-push, workflow_dispatch.
- Board-/Karten-status nicht geaendert (owner-synct plan main + kanban-doku); nur dieser eigene evidence-pfad geschrieben.
- remote guard: origin und lane-origin zeigen beide auf https://github.com/mcpdev80/baseharbor.git; nur dieser remote verwendet.
- planning remote: https://github.com/mcpdev80/baseharbor-plan.git (verified).

## CLEANLINESS:BEFORE

  podman ps -a: (leer, keine baha-container)
  podman network ls: nur default 'podman' bridge
  podman volume ls: leer
  baha state (/tmp/baha-home-187/.local/share/baseharbor/targets/): baha-ci-187 (target create nur; kein core bootstrap)

## CLEANLINESS:AFTER

  podman ps -a: keine baha-container (clean)
  podman network ls: nur default 'podman' bridge (unveraendert)
  podman volume ls: leer (keine szenario-volumes)
  baha state (/tmp/baha-home-187/.local/share/baseharbor/targets/): baha-ci-187 als DETACHED (delete = detach, runtime/data
  bleibt erhalten; es wurden IMMER keine container/netzwerke/volumes gestartet, der core bootstrap brauchte host-systemd,
  das im sandbox nicht verfuegbar ist)
  ambient-core/ bilder fremder karren: unangetastet (keine beruehrung)

## END

END_DONE mission-187.md: 0428-187 consent-gate-stall = BEFUNDOLES; ursache in baseharbor-demo, owner-behoben auf adda7599 (demo catalog). Core-text an provider_change_consent.go:37 durch cmd/baha/provider_change_confirmation_test.go:81 fixiert (feld-abdeckung, gruen). Keine Produktaenderung noetig.
