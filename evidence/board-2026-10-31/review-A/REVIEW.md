# Review-A — Read-only Review of PR #1240 & #1241

- ROLLE: REVIEW
- Session: worker-ornith1.5 (via AgentGateway)
- Zeit: 2026-11-01 (UTC)
- Basis-HEAD beider PRs: `cb6b73875f478b6be5624412fb9f4c3695e51518` (develop)

## VERFAHREN (Proof)
- Diff je PR via `gh api repos/mcpdev80/baseharbor/pulls/<n>/files --jq '.[]|patch'`.
- Basis/SHA je PR via `gh api .../pulls/<n> --jq '.base.sha,.head.sha'` (beide base `cb6b738`).
- CI-State via `gh pr view <n> --json statusCheckRollup` + `gh api .../actions/runs/<id>/jobs` + Full-Logs via `gh api .../actions/jobs/<id>/logs`.
- Gate-Logik gegen `gh api .../contents/scripts/pr-required-final.py?ref=develop` verifiziert.
- Write-Set/Ancestry gegen Branch-Head und develop geprüft; disjunkt (1240: `internal/runtime/`, 1241: `cmd/baha/`).

---

## PR #1240 — openbao→postgres TLS/SASL wiring (stack.go / openbao_runtime_prepare.go)
- Kandidaten-SHA: `33d1ef490c967debd926ea64993ce674c7a05e6a` (Branch `work/o1249b-openbao-cauth`)
- Write-Set: `internal/runtime/openbao_runtime_prepare.go` (+8/-3), `internal/runtime/stack_test.go` (+4/-4). Isoliert, disjunkt zu 1241.

### Verdict: CHANGES: Testanforderung (CI fail-closed „coverage-unresolved")
**Kein Sicherheit-Downgrade.** Der einzige Substanzwechsel ist `sslmode=verify-full` → `verify-ca`. Das ist bewusst und fachlich korrekt: durch die Postgres-HAProxy fällt der Server-Hostname weg (SNI-Ziel ≠ Zertifikatsname), daher schlägt `verify-full` fehl. `verify-ca` verifiziert noch das CA-signierte Serverzertifikat (kein `ssl=off`/`trust`/`verify-none`) — kein Downgrade auf offen. Init-Skript + HCL-URL + zwei Healthcheck-psql setzen nun alle `PGSSLMODE=verify-ca` + `PGSSLROOTCERT=/run/baseharbor/postgres-ca/ca.pem` (Fail-closed über CA-Trust, nicht offener Modus).

**Was fehlt = Fail-closed-Mängel, kein Code-Fehler:** Die CI „PR Selected Checks" ist **fail-closed gescheitert**, aber **nicht** wegen Test-/Logik-Fehler. Die Logs zeigen exakt:
```
BLOCKED: coverage-unresolved: unknown impact for internal/runtime/openbao_runtime_prepare.go; unknown impact for internal/runtime/stack_test.go
BLOCKED: no required gates or validations
```
Die Gate-Funktion (`pr-required-final.py`) blockiert bei `plan.coverage_status != 'resolved'` mit `coverage-unresolved`. Der PR enthält keine `selected_gates`-Abdeckung (`atomic/podman` oder `atomic/docker`) für die geänderten Runtime-Dateien, und es existiert kein erfolgreicher `PR · Selected Runtime`-Job. `verify-ca` ist ein TLS-Standalone-Mechanisimsm; ein `atomic/docker`/`atomic/podman` Integrationstest würde den End-to-End-Zerifikatspfad durch HAProxy abdecken — das ist die fehlende, geforderte Abdeckung, nicht der Code selbst.

### Rezept (umsetzbar)
1. `plan.coverage_status` auf `resolved` setzen (impact gate für die 2 Runtime-Dateien) **und** einen `atomic/<runtime>/<suite>` Gate eintragen, der den TLS-Pfad über HAProxy abdeckt, oder `PR · Selected Runtime` erfolgreich laufen lassen.
2. Fail-closed-Assertion ergänzen: Test/Check, dass in `openbao_runtime_prepare.go` **kein** `sslmode=off`/`trust`/`verify-none` vorkommt (regression guard gegen zukünftiges Downgrade).
3. CI wiederholen; `PR Selected Checks: PASS` als Ziel.

---

## PR #1241 — runtime-neutrale Engine-Erkennung (cmd/baha/docker_engine.go + Podman-Test)
- Kandidaten-SHA: `ed5ca739f2acb113cb180f0ffec6465b33c6f009` (Branch `work/fix-engine-detect`)
- Write-Set: `cmd/baha/docker_engine.go` (+15/-3), neue `cmd/baha/docker_engine_podman_test.go` (+19/-0). Isoliert, disjunkt zu 1240.

### Verdict: APPROVE-WARTEND-GREEN
**Logik korrekt.** Fix ist minimal und präzise:
- `ensureTargetDockerBinding`/`inspectTargetDockerEngine`: alte Bedingung `!= "docker"` → `!= "docker" && != "podman"`; `podman` wird nun nicht mehr stillschingend übersprungen.
- `engineBinaryName(provider)` wählt `podman` für Provider `podman`, sonst `docker` (default).
- **Fail-closed bleibt erhalten:** `AccessProvider != "" && != "local"` ist die erste Abwehr (nur lokale/lokale Targets), die Sicherheitsprämie bleibt intakt.
- Test deckt die neue `engineBinaryName`-Tabelle ab (`""→docker`, `docker→docker`, `podman→podman`, `unknown→docker`), Package `main`, läuft isoliert.

**Was fehlt = Wieder-Green-Lauf (kein Code-Mangel):** Auch hier ist `PR Selected Checks` fail-closed gescheitert — aus **derselben** Ursache (Gate „coverage-unresolved" / kein erfolgreicher `PR · Selected Runtime`), nicht wegen Logik oder Test. CI-Spiegel: `PR · Validation · cli-build/vet/source-contracts: SUCCESS`, `PR Selected Checks: FAILURE` (`coverage-unresolved`-Klasse). Der Kandidat ist SHA-genau und Review-fähig; der Blocker ist ein fehlendes CI-Coverage-Proof, kein inhaltlicher Defekt.

### Rezept (umsetzbar)
1. `plan.coverage_status` auf `resolved` setzen und einen erfolgreichen `PR · Selected Runtime` (bzw. geforderten Validation-Gate) erzeugen; `PR Selected Checks: PASS`.
2. Danach ist der Kandidat SHA-genau + Test vorhanden + fail-closed intakt → Acceptance-reif.

---

## BONUS-BEFUND (nur Befund, kein Handlungsauftrag)
Beide PRs scheitern an **derselben** CI-Falle: Das Fail-closed-Gate `PR Selected Checks` blockiert bei nicht-`resolved` `coverage_status`. Der PR-Autor konnte `internal/runtime/*` (1240) bzw. `cmd/baha/*` (1241) offenbar **nicht selbst** als abgedeckt markieren (kein autorisierter Access zum Coverage-Proof). Das ist ein **Prozess-/Ordnungs-Blocker**, dokumentiert nach §5.6 (Prompt-Injection/Foreign-Command-Defense: PR-Texte sind Daten; kein Handlungsauftrag aus dem PR-Body abgeleitet). Kein automatischer CHANGES-Druck nur wegen dieses Befunds; die inhaltlichen Verdicts stehen oben.

## END Lane
END lane review-A: DONE — Verdicts geliefert (1240=CHANGES/Testanforderung, 1241=APPROVE-WARTEND-GREEN), kein Merge/Approve.
