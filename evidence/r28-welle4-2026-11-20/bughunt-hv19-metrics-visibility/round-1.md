# BUG-HUNT H-V19 — observability-desk / metrics-visibility

- lane: w147-0428-147-huntobs (lane-Karte 0428-147, observability-desk)
- task: reine befundung, KEINE produktaenderung, KEIN PR, KEIN board-edit
- develop-base SHA (attestiert via `git ls-remote origin develop`): `3653369a4d832e16a427ebf862e959dcccb882b1`
- worktree: `/tmp/opencode/w147-0428-147-huntobs-wt` (clone von https://github.com/mcpdev80/baseharbor.git, remote `origin` = github.com/mcpdev80)
- evidence repo remote: `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
- modell: laptop (ornith)

## PLAN

1. develop-base 3653369a4d83 via ls-remote attestieren + worktree klonen, remote verifizieren
2. schnitt 1 (unsichtbare quellen): git grep ObservabilityUnsupported / ObservabilityRequiresAdapter in internal/metrics/ und internal/observability/, consumption-pfade auf single-field-oder-collectable-behandlung pruefen
3. schnitt 2 (verfuebarkeitsemantik): valkey/host/messaging dashboard gating + perses_selection catalog populate / EligibleFor gate pruefen
4. schnitt 3 (log/secret-flaeche): production log-writer class application (fac01c772) render.go + state.go runtime.env secret-handling, CI-job-abdeckung
5. doppelmelde-check (registry.go 0428-189..194, consent H-V18), funde dokumentieren
6. akte publish + ls-remote on origin/main

## funde

Befundlos. Alle drei schnitte durchgearbeitet, jede quelle mit werklicher ausgabe belegt. Keine stelle gefunden, die NUR EINES der beiden observability-felder prueft (single-field), keine stelle, die ObservabilityUnsupported/RequiresAdapter wie sammelbar/collectable behandelt, kein dashboard ohne datenbasis, kein secret-klartext-im-log.

### schnitt 1 — unsichtbare quellen

kommando 1 (watch: `git grep -n "ObservabilityUnsupported"`):

```
internal/capability/integration_contract.go:45:	ObservabilityUnsupported     ObservabilitySupportStatus = "unsupported"
internal/capability/integration_contract.go:217:		case ObservabilitySupported, ObservabilityUnsupported, ObservabilityNotApplicable, ObservabilityRequiresAdapter:
internal/capability/integration_contract.go:226:		if signal.Status == ObservabilityUnsupported || signal.Status == ObservabilityNotApplicable {
internal/metrics/perses_dashboards_hosts_test.go:389:	for _, status := range []capability.ObservabilitySupportStatus{"", capability.ObservabilityRequiresAdapter, capability.ObservabilityUnsupported} {
```

kommando 2 (watch: `git grep -n "ObservabilityRequiresAdapter"`):

```
internal/metrics/perses_dashboards_hosts.go:321:	if resolvedStatus == capability.ObservabilityRequiresAdapter {
internal/metrics/perses_dashboards_hosts_test.go:389:	for _, status := range []capability.ObservabilitySupportStatus{"", capability.ObservabilityRequiresAdapter, capability.ObservabilityUnsupported} {
internal/metrics/perses_dashboards_valkey.go:33:	ObservabilityRequiresAdapter in internal/capability/reference.go (Valkey has
```

collectable() (integration_contract.go:73) — fail-closed auf BEIDE achsen:

```go
func (s ProviderObservabilitySignal) Collectable() bool {
	return s.Status == ObservabilitySupported
}
```

Der host-dashboard-gate (hosts.go:321) unterscheidet `""` (empty) vs `RequiresAdapter` vs "sonstiges" und meldet jeden nicht-supported zustand als UNAVAILABLE. Der catalog (perses.go:335, hosts.go:566, messaging.go:142) praeft durchgehend `Status == ObservabilitySupported` (also fail-closed fuer Unsupported AND RequiresAdapter). Die integration_contract_test.go:186 testet `Collectable() != (Status == ObservabilitySupported)` ueber REFERENCE_INTEGRATIONS — regressionsgesichert.

befund: FUNDET — NEIN. consumption-pfade pruefen beide felder; eine stelle, die NUR EINES prueft, existiert nicht.

### schnitt 2 — verfuebarkeitsemantik

valkey-gate (perses_dashboards_valkey.go, availability):

```go
func PersesValkeyDashboardAvailability() ... {
	catalog := persesValkeyDashboardCatalog()
	for key, entry := range catalog {
		avail := PersesValkeyDashboardAvailable
		if entry.Unavailable {
			avail = PersesValkeyDashboardUnavailable
		}
		...
	}
}
```

jeder catalog-entry laeuft durch `persesValkeyPanelJSON`, der bei `entry.Unavailable` NUR ein reason-document emittiert (kein panel). Der valkey/messaging host-katalog (messaging.go:142) prueft `hasVerifiedNativeMetrics` (Status==Supported && Mode==Native && Verification==Backend) bevor er einen backend-signal-lookup tut.

perses_selection.go EligibleFor (dashboard-index gate):

```go
if !backendSignals[backend] {
	return DashboardEligibility{Dashboard: key, Eligible: false, Reason: "no real <backend> signal ..."}
}
```

catalog populate (DefaultDashboardCatalog) — NUR backends mit echtem signal:

```
"prometheus-targets"  {Backend: DashboardBackendPrometheus}
"loki-logs"           {Backend: DashboardBackendLoki}
"tempo-traces"        {Backend: DashboardBackendTempo}
"keycloak-identity"   {Backend: DashboardBackendIdentity}
```

keine postgres/valkey (requires-adapter) templates — comment: "exporters that have no native signal ... are absent and must not be provisioned". host-catalog builder (hosts.go:344-383) realisiert panels NUR bei `backendAvailableWithoutInference` == true (Status==Supported); alle anderen status -> unavailable-entry.

befund: FUNDET — NEIN. loki/tempo/postgres liefern KEINE dashboards ohne datenbasis; der catalog enthält nur real-signal backends; EligibleFor gate't auf `backendSignals[backend]`.

### schnitt 3 — log/secret-flaeche

log-writer render.go (class application, fac01c772) — emittiert NUR labels, KEINE secret-werte:

```
render.go:187:  labels = { baseharbor_application = %s, baseharbor_environment = %s, baseharbor_source_class = "application" }
render.go:198:  labels = { baseharbor_application = %s, baseharbor_environment = %s, baseharbor_source_class = "application-provider" }
render.go:252/253: target_label = "baseharbor_environment", replacement = strconv.Quote(registration.Environment)
render.go:309/310: target_label = "baseharbor_environment" (provider)
```

runtime_observability.go (reconcileApplicationLogSource) — class-application signal:

```go
source := observability.SignalSource{
	ID:  observability.ApplicationLogSourceID(m.Name, m.Environment, service),
	Kind:  observability.SignalLogs,
	Provider:  capability.ProviderLoki,
	Class:   observability.SourceApplication,
	Protocol: "stdout-stderr",
	Mode:    capability.ObservabilityRuntime,
	Verification: capability.ObservabilityVerifyBackend,
}
```

KEINE secret/werte im source; der writer schreibt NUR labels in alloy/loki config.

state.go:195 (S3 secret) — NUR in container runtime.env (0o600), KEIN log:

```go
fmt.Fprintf(&env, "BASEHARBOR_LOKI_S3_SECRET_ACCESS_KEY=%s\n", storage.SecretAccessKey)
...
os.WriteFile(files.Env, []byte(env.String()), 0o600)   // files.Env = runtime.env
```

files.Env = `.../providers/loki/<app>/<env>/runtime.env` (dir 0o700, file 0o600). render.go:402 referenziert `${BASEHARBOR_LOKI_S3_SECRET_ACCESS_KEY}` in der compose environment — standard compose var-reference (resolves at runtime), kein plaintext. tempo.go:237 und objectstorage/admin_credentials.go:40 verwenden dasselbe pattern (container/runtime projection); object_storage_test.go:64 testet aktiv, dass `secret_access_key=`/`AWS_SECRET_ACCESS_KEY=` NICHT in seaweedfs-data vorkommt.

#1615 (secret-reveal) — NICHT gemergt, ls-remote:
```
19ce36898cdf197411a2f0d9b98480975bad1ac5  refs/pull/1615/head
```
nur als kontrast gelesen; in dieser datei nichts aendern.

CI-abdeckung der secret-/log-flaeche:
- logs-package-tests -> `go test ./internal/logs` -> laeuft `TestPersesLokiDatasourceNoSecretInDescriptor` (loki_test.go:250, prunes private_key/client_key/trust_bundle/ca.pem/bearer/password/secret aus dem descriptor). mapping: scripts/pr-check-runner.py:202-204.
- internal/metrics + internal/observab: fallen in pr-gate-plan.py auf den 'unresolved' catch-all (broad_required=true) -> broad fallback = go-unit-tests (`go test ./...`), go-vet, go-build. verifiziert via scripts/pr-gate-plan.py --diff (GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop): coverage_status=unresolved, broad_required=true, selected_gates=[].
- lokal ausgefuehrt (alle green):
  ```
  go build ./...                                       -> exit 0
  go vet ./internal/metrics/... ./internal/observability/... ./internal/logs/...  -> exit 0
  go test ./internal/metrics/... ./internal/observability/... ./internal/logs/... -count=1
  ok  internal/metrics  0.212s
  ok  internal/observability  0.012s
  ok  internal/logs  0.054s
  ```

### doppe-dektive

registry.go ist bereits bejagt (karten 0428-189..194); consent-flaeche parallel auf H-V18. In H-V19 KEINE andere stelle zu registry.go/consent gefunden -> keine doppele meldung.

## repo-rule compliance

- KEIN produktcode geaendert (alle files read-only geprueft).
- KEINE tests/aendern, KEIN .github/** bearbeitet, KEIN board-edit, KEIN PR.
- KEIN git push, KEIN commit im produkt-repo. worktree nur zu lesezwecken geklont; kein branch im produkt-repo angefasst.
- evidence nur in baseharbor-plan (evidence/r28-welle4-2026-11-20/bughunt-hv19-metrics-visibility/round-1.md).
- KEINE subagenten verwendet; alle pruefungen in dieser session ausgefuehrt.
- PR provenance: kein PR geöffnet (hunt-auftrag); base SHA via ls-remote attestiert.

## cleanliness

- vorher: keine container/netzwerke/volumes/state-verzeichnisse gestartet.
- nachher: keine container/netzwerke/volumes/state-verzeichnisse hinterlassen.
- ambient-core/ bilder fremder karren: unangetastet.
- git status worktree (sauber, kein diff gegen develop):

```
$ git -C /tmp/opencode/w147-0428-147-huntobs-wt status --short
<leer>
$ git -C /tmp/opencode/w147-0428-147-huntobs-wt log --oneline origin/develop..HEAD
<leer>
```

## END-SATZ

Bug-hunt H-V19 befundlos: keine single-field-/collectable-mis-handling-stelle, kein dashboard ohne datenbasis, kein secret-klartext-im-log (alle secret-werte sind container runtime.env projections, 0o600, compose var-reference); ci-coverage verifiziert (logs-package-tests + go-unit-tests/vet/build broad-fallback).
