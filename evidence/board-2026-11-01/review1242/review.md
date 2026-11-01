# review1242 — CODEX-REVIEW (read-only) — PR #1242 verdict

- ROLLE: REVIEW (CODEX-REVIEW). Read-only. No candidate change, no merge, no spawn.
- Session/Org: baseharbor-ecosystem/workers/.models/ornith — review1242
- Modell: Ornith (worker) — alle Prüfeingang über gh + lokales Build/Vet geprüft
- Zeit: 2026-11-01 (CET)
- Kandidat: PR #1242 `fix(observability-acceptance): follow plan→apply flow to satisfy consent guard`
  - Head SHA (exakt, bestätigt via gh pr + git): `d65ba9917c1ed85efa7eb38d56cc51f4c3772475`
  - Base/develop: `46307b75` (Merge PR #1259 gate-map)
  - Status: OPEN, nicht merged (mergeCommit null)
  - Nur geänderte Datei vs develop: `cmd/baha/app_observability_acceptance_test.go`

## Verdict: APPROVE

Kandidat erfüllt den Task-Vertrag (fix-observ-consent, Entscheidung (A) TEST-FEHLER): der
Akzeptanztest `TestObservabilityFullStackAcceptanceInCI` fuhr früher blind `app apply` ohne
die vorgeschriebene Plan→Apply-Bestätigung, was am Consent-Guard (`provider_change_consent.go`)
an der Stelle `impact-confirmation-required` scheiterte. Der Fix fährt jetzt den vorgeschriebenen
plan→apply-Pfad: resolved-Anwendung auflösen → Impact-Plan bauen → Zwei-Stufen-Consent passend zu
`PlanID`/`ConfirmationsRequired` konstruieren → `ValidateProviderChangeConsent` präventiv prüfen →
mit `withProviderChangeConsent` durch den Apply-Lifecycle tragen. Kein Produktcode geändert,
kein blindes `--force` auf echte Löschung, Write-Set exakt vertragsgemäß (nur die Testdatei).

## SHA-genauer Diff vs. Vertrag (Wahrheitsnachweis)

Diff vs develop nur in `cmd/baha/app_observability_acceptance_test.go`:
- `runWithIO(ctx, ["app","apply"], …)` ersetzt durch:
  - `resolveApplication(ctx, application.Store{}, nil, "apply")` → `buildResolvedApplicationPlan(ctx, resolved)`
  - `plan.ProviderPlan.Impact` nicht-NULL geprüft (`Impact == nil` → Fatal)
  - `consent := &application.ProviderChangeConsent{PlanID: impact.PlanID, First: true, Second: impact.ConfirmationsRequired == 2, DeleteData: false}`
  - `application.ValidateProviderChangeConsent(*impact, *consent)` → Fatal bei Fehler
  - `runWithIO(withProviderChangeConsent(ctx, consent), ["app","apply"], …)`
- Nebeneffekt/Sauberkeit: die bestehende `resolved`-Variable der Status-Phase in `statusResolved`
  umbenannt, um Shadowing durch die neue `resolved`-Deklaration aufzuheben (korrekt, keine Logikänderung).
Byte-Identität vs Commit bestätigt via `git show`/`git diff origin/develop`.

## Pflichtcheck: PRSC = success auf d65ba991 (nachgepruft, Run 41344810206)

- `gh run view 41344810206 --repo mcpdev80/baseharbor`:
  - `PR Selected Checks`: completed / **success** (Coverage aufgelöst, kein unvernetzter Pfad)
  - `PR · Selected Runtime … / docker · observability`: completed / **success**
  - `PR · Selected Runtime … / podman · observability`: completed / **success**
- Alle anderen Gates success; skipped nur `Consumer Pins`, `Public Contracts`, `Release Source Preflight`,
  `validate`, `Targeted HA · docker/podman` (nicht für diesen Fix relevant).
- Kein Gate geschwächt; die Full-Stack-Run hat echt durchlaufen (Artefakt `pr-exact-candidate-d65ba991…`).

## Pflichtcheck: Logik-Wahrheit (kein Umgehung/Force-Bypass)

- `ValidateProviderChangeConsent` (internal/application/provider_change_consent.go):
  `Complete=false` oder `ConfirmationsRequired==2` → `First+Second` nötig, sonst `impact-confirmation-required`;
  `Destructive && !DeleteData` → `data-deletion-consent-required`. Der Fix liefert genau First=true,
  Second=(confirmations==2), DeleteData=false → passt zur vorgeschriebenen Logik.
- `apply` benötigt valider Consent: `app_edit_apply.go:314`/`provider_change_confirmation.go` rufen
  `ValidateProviderChangeConsent` zwingend auf; `application_destroy_authorization.go:114` ebenso.
  Kein `--force`-Umgehungspfad nachweisbar. Der Fix fährt den echten Zwei-Stufen-Acknowledgement-Pfad.
- `withProviderChangeConsent(ctx, consent)` legt den Consent in den Context
  (`provider_change_context.go:25`), `invocationProviderChangeConsent` liest ihn — der Lifecycle holt
  den über den Context geführten Consent, nicht blindes `--yes`.

## Pflichtcheck: Symbol- und Typauflösung (alle vorhanden, Typen passen)

- `resolveApplication(ctx, application.Store{}, nil, "apply")` — cmd/baha/app_context.go:68 ✓
- `buildResolvedApplicationPlan(ctx, resolved)` — cmd/baha/app_core_requirement.go:219 ✓;
  `.ProviderPlan.Impact` ist `*ProviderImpactPlan` (provider_union.go:39) mit Feldern `PlanID`,
  `ConfirmationsRequired`, `Destructive`, `Complete` (provider_change_types.go:168-177) ✓
- `application.ProviderChangeConsent{PlanID,First,Second,DeleteData}` — provider_change_types.go:182 ✓
- `application.ValidateProviderChangeConsent(current, consent)` — provider_change_consent.go:12 ✓
- `withProviderChangeConsent(ctx, *ProviderChangeConsent)` — cmd/baha/provider_change_context.go:25 ✓
- `application.New(name, env, sql, cache, secrets)`, `WithRuntimePermission`, `ProviderScopeEnv(k)`,
  `writeInitializedAuthoredManifest(t, path, m, mode)`, `runWithIO(ctx, args, out, errOut io.Writer)`
  — alle gefunden ✓

## Pflichtcheck: Build/Vet/Compile (lokal auf d65ba991 ausgeführt)

- `go build ./...` → Exit 0
- `go vet ./cmd/baha` → Exit 0
- `go test -c -o /dev/null ./cmd/baha` (Test-Package-Kompilation) → Exit 0

## repo-rule compliance

- Write-Set exakt auf die vertraglich erlaubte Testdatei beschränkt; `internal/application/…`
  (Querschnitt) unangetastet.
- Read-only Review-Lane eingehalten: kein Merge, kein Produktcode, kein `codeman agent spawn/rm/send`,
  kein Subagent/Syntax-Spawn.
- Evidence reproduzierbar: PR-SHA via gh + git, CI-Run-ID 41344810206, lokale Build-/Vet-/Compile-Exit-Codes.

## Zwischenstand / Einschränkung

- Vollständige End-to-End-Integration nur über den gehosteten docker/podman Full-Stack-Gate (Run
  41344810206: beide success). Lokaler Docker-Lauf nicht erneut gestartet (CI-Evidence reicht für den
  SHA-nauen Nachweis; kein double-review des unveränderten Kandidaten).

## END

END review1242 DONE — Verdict APPROVE, SHA d65ba9917c1ed85efa7eb38d56cc51f4c3772475, PRSC=success + docker/podman observability gates success.
