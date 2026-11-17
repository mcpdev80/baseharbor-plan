# Release-Gate-Audit — develop (reine Befundung, keine Aenderung)

- Mission: `/var/tmp/missions/mission-hunt-releasegate.md`
- Rolle: WORKER (Bug-Hunt, keine Produktaenderung, keine Commits im Produkt)
- Datum: 2026-11-17
- Lane-Worktree (nur Lesereferenz): `/tmp/opencode/miss-releasegate-wt`, Branch `develop`, detached auf Produkt-Basis 4bab986dc
- Modellkanal: Ornith-Sitz

## PLAN

- Mission lesen; develop-Remote-HEAD via ls-remote ermitteln, Plan-Repos-Pfad verifizieren, isolierter Worktree
- Release-boundary-contract-Erwartungen aus Karten 0428-092 (boundary) + 0428-073 (alerts) + Karten-Akzeptanztexte lokalisieren
- Jede Erwartung gegen aktuellen develop-Stand (Code + Tests) mit file:line mappen: durch code+tests gedeckt / nur tests ohne code / fehlt
- gezielte run-bare Probes (build, vet, CLI production entrance), keine deployments
- Befund als `evidence/r28-welle3-2026-11-16/hunt-releasegate/befund-1.md` in baseharbor-plan schreiben
- Sauberkeit: container/netz-liste vorher/nachher, cleanliness-Zeile, END-Post

## Zone- und Basis-Zeugen

Planning-Repo-Verifizierung (wrong-zone check, Mission 2026-11-07):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git HEAD refs/heads/main
e092a0187c4895f9ee0d801dd78173db7b974c54	HEAD
e092a0187c4895f9ee0d801dd78173db7b974c54	refs/heads/main
```

Produkt-Basis (develop, Remote-HEAD beim Start):

```
$ git ls-remote origin refs/heads/develop   # baseharbor
4bab986dc65ae2bdbc6696328026d86fc2c57f9e	refs/heads/develop
```

Worktree ist detachter develop-Checkout exakt auf `4bab986dc`; alle `file:line`-Zitate gelten gegen diesen SHA. Keine anderen Kandidaten-Basen im Worktree.

## Release-boundary-contract (Quelle der Erwartung)

Karten-Akzeptanztexte (baseharbor-plan, origin/main `e092a018`):

- **0428-092** `tasks/t-20261114-r28-perses-release-boundary.md` (card `0428-092`, PR #1577):
  - Goal: "Align current Core release/audit entry points with the accepted public scope: Core, Demo, the delivered CLI and optional Perses. Archived Console and Node Connector must not be required as active release consumers. Do not rewrite historical release records or claim a release has passed."
  - Owner decision 2026-11-15: normativity of `docs/spec/management-access-v1.md` LIMITED to authentication and role-mapping findings; Perses pin/release scope/state semantics NOT normatively derived from that spec.
- **0428-073** `tasks/t-20261114-r28-perses-alerts.md` (card `0428-073`, PR #1613):
  - Goal: "Define actual alert rule evaluation and persistence using supported existing Prometheus contract or an Owner-approved alternative; Perses UI is not assumed to be the evaluator."
  - Acceptance: "Define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default."

Binding release-readiness vocabulary (baseharbor product, develop `4bab986dc`):

- `docs/internal/pre-release-documentation-audit.md:21`: "Console and Node Connector are archived and excluded from v0.4.27; this release makes no compatibility claim for them."
- `docs/development/pre-release-readiness.md:10-12`: Console/Node Connector archived and excluded; Core-only green does not qualify.
- `docs/internal/pre-release-documentation-audit.md:153`: exact Demo SHA in `docs/releases/vX.Y.Z.demo-ref`; older consumer matrices historical.

## Deckungs-Matrix

### 0428-092 (boundary)

| Erwartung (Akzeptanz) | develop-Stand | Status | Beleg (file:line) |
|---|---|---|---|
| Core/CLI release/audit entry pointsexclude archived Console/Node Connector; Demo active consumer | Docs enthalten die statement; Console/NodeConnector nur historisch | **durch code+tests gedeckt (Doku + Referenz)** | `docs/internal/pre-release-documentation-audit.md:21`; `docs/development/pre-release-readiness.md:10-12`; `docs/releases/v0.4.27.demo-ref` = `f23b6e09b` (Demo pin) |
| Perses optional, nicht als implementiert asserted | Perses als optionaler management-ui-Realisierung deklariert, `Provisioned`/`perses` fail-closed | **durch code+tests gedeckt** | `internal/capability/perses.go:19-24,145-150,263-280`; `internal/application/manifest_validation.go:508-528`; Tests `internal/capability/perses_test.go`, `internal/metrics/perses_contract_test.go` |
| `docs/spec/management-access-v1.md` nur auth/role-mapping normativ (Owner-Entscheidung 2026-11-15) | Perses pin/release/scope/state-NormativITAT NICHT aus Spec abgeleitet; nur faktische Release-Zusammenfassung | **abzudecken (Fund)** | Owner-Entscheidung in Kartentext; Spec-Referenz `docs/spec/management-access-v1.md` (nur auth/role-mapping) |
| Kein falscher Release-Pass / kein Rewriting historischer Records | Historische Release-Docs unveraendert; v0.4.27 demo-ref als einzige aktuelle Pin | ** gedeckt (Doku)** | `docs/releases/v0.4.27.demo-ref`; v0.4.23 consumer-pins.json nur historisch |

### 0428-073 (alerts)

| Erwartung (Akzeptanz) | develop-Stand | Status | Beleg (file:line) |
|---|---|---|---|
| Real alert rule **evaluation + persistence** via Prometheus contract | Nur Contract-Deklaration (surface/pin/fail-closed); KEINE Regel-Evaluation, KEIN Regel-Persistenz, KEIN notification/routing owner | **FEHLT** (nur tests ohne code: Test deckt nur Deklaration + fail-closed) | `internal/capability/perses.go` (keine rule/eval/notification-Funktion); kein `alert`/`evalrule`/`rule_file`/`notify`/`route`-Code in `internal/capability`, `internal/metrics`, `internal/application`; `internal/capability/provider_change_contract.go:43-44` nennt nur `metrics.rules` permission + `rule` material (kein Evaluator) |
| Perses UI **nicht** als evaluator angenommen | Konform: `PersesManagementSurfaceNow` liefert nur `Provisioned` + `Reachability=unverified`, kein health-probe | **durch code+tests gedeckt** | `internal/capability/perses.go:196-254`; `internal/metrics/perses_contract_test.go:38-77` |
| Fail-closed "not configured" statt false "configured" | Implementiert: `ValidatePersesRelease` + `PersesNotConfiguredError` | **durch code+tests gedeckt** | `internal/capability/perses.go:152-174,289-301`; `internal/capability/perses_test.go:5-20` |
| Externe notifications nicht standardmaessig aktivieren | `AuthenticationClass` default `unsupported`; kein notification-code | **durch code+tests gedeckt (negativ)** | `internal/capability/perses.go:145-150,292-301` |

## run-bare probes (develop `4bab986dc`)

- `go build ./...`: OK
- `go vet ./internal/capability/... ./internal/metrics/... ./internal/application/... ./cmd/...`: OK
- `go test ./internal/capability/...`: ok
- `go test ./internal/metrics/... -run 'Perses|Scope|Topology|WorkloadOnly|Retirement|Source|ProviderObservability|WebConfig|Health|Integration|Verify'`: ok
- `go test ./internal/application/...`: ok (4.8s)
- `go test ./cmd/baha/... -run 'Perses'` (production CLI entrance, runWithIO): ok (8.6s) — proveniert die seam ueber den echten `baha` command path, nicht ueber interne seam helper (vgl. 0427-175 r8 precedent)
- Keine deployments, keine container/compose gestartet.

## Befunde

1. **0428-073 alert rule evaluator/persistence FEHLT (Fund).** Die Karten-Akzeptanz verlangt "define the real rule evaluator and notification owner" und "actual alert rule evaluation and persistence". Der aktuelle develop-Stand deklariert nur die Perses-management-surface + pin + fail-closed seam; es gibt keine Regel-Evaluation, keine Regel-Persistenz und kein notification/routing owner in `internal/capability`, `internal/metrics`, `internal/application`. Bestanden sind nur die Deklaration + fail-closed Tests. Die `metrics.rules` permission (`provider_change_contract.go:43`) und `rule` material (`:44`) sind deklariert, aber nicht evaluiert. Status: **FEHLT** — deckt sich mit "nur tests ohne code" fuer die eigentliche Evaluierungs-/Persistenz-Anforderung.
2. **0428-092 owner-decision 2026-11-15 coverage (Fund/Bestaetigung).** Die Einschränkung der Normativitaet von `docs/spec/management-access-v1.md` auf auth/role-mapping ist im Kartentext festgehalten; der develop-Stand leitet Perses pin/release/scope/state NICHT normativ aus der Spec ab (deckt sich mit der Owner-Entscheidung). Boundary (Console/Node Connector archiert, Demo active consumer) durch Doku + demo-ref pin gedeckt. Status: **durch code+tests/doku gedeckt**.
3. **Historische consumer-pins (Befund, nicht blockierend).** `docs/releases/v0.4.23.consumer-pins.json` referenziert Console + Node Connector als active consumers; dies ist eine historische v0.4.23-Matrix und nicht die aktuelle v0.4.28-Scope (`v0.4.27.demo-ref` = `f23b6e09b`, kein Console/Connector in der aktuellen demo-ref). Konform mit "older consumer matrices remain historical and unchanged" (`pre-release-documentation-audit.md:153`).

## Scope / evidence hygiene

- Akte liegt ONLY in baseharbor-plan (planning repo): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r28-welle3-2026-11-16/hunt-releasegate/befund-1.md`. Keine `.evidence/` im Produkt-repo, kein main-branch write im Produkt.
- Produkt-Checkout: isolierter Worktree `/tmp/opencode/miss-releasegate-wt`, detached auf develop `4bab986dc`. Kein scratch/caches/stray unter dem ecosystem-root.
- Keine workflow-Datei (.github/**) aendern, kein rerun/workflow_dispatch (Owner-Scope), kein runner repair.
- Subagenten: kein spawn/delegate (eigene Session).

## Sauberkeit / containers

- vorher: keine container/netz/volumes gestartet.
- nachher: keine container/netz/volumes gestartet.
- cleanliness:-zeile: sauber, keine container/netz/volumes/ state-verzeichnisse hinterlassen.

## END

END_DONE mission-hunt-releasegate.md: Release-Gate-Audit develop (4bab986dc). Deckungs-Matrix fertig: 0428-092 (boundary) durch code+tests/doku gedeckt (Console/Node Connector archiert, Demo active consumer, Perses optional fail-closed, owner-decision 2026-11-15 normativity-limited). 0428-073 (alerts): alert rule **evaluation + persistence FEHLT** — nur Deklaration + fail-closed tests, kein Evaluator/Persistenz/notification-owner; metrics.rules permission deklariert, nicht evaluiert. run-bare probes build/vet/tests + production CLI entrance (baha perses) ok, keine deployments.

Evidence committed to baseharbor-plan origin/main: commit `ce9ed512` "hunt-releasegate: release-gate-audit develop befund-1" — verified ancestor of origin/main `be0f39bf` (git ls-remote refs/heads/main tip).
