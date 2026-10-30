# CODEX-REVIEW — AUFGABE B: core-750 source-neutral capability findings (#1222)

ROLLE: CODEX-REVIEW (retroaktiv, Mission w750c). PR #1222 (core-750 Produktcode) wird gegen den Task-Vertrag `core-750-inspect-source-neutral-findings.md` geprüft.

## SHA-Angaben
- PR #1222 HEAD: `74a35765` branch `work/v0.4x-core-750-inspect-source-neutral-findings`, base develop.
- MERGE-COMMIT (reviewed head): `74a35765` gegen develop-Vorstand `72ba7a99` (#1224 Mapper-Merge已在 develop).
- CI: Run #41059938103 (PR #1222) — terminal success. `PR Selected Checks` success, all jobs success/skipped.
- Write-Set (gegen HEAD): `internal/repositoryinspect/inspect.go` (+111/-3), `internal/repositoryinspect/workload_source_parity_test.go` (+110). Kein cmd/baha/Plan/PR/CI-File im Product-PR.

## Prüfungspunkte gegen den Task-Vertrag
1. **Source-neutral projection from normalized evidence.** inspect.go:217 ruft `shareProjectSummaryFromComponents(&result, result.WorkloadEvidence)` im `else`-Zweig (nicht Compose) — projiziert Ports, Health, Workload/Infra-Klassifikation aus `WorkloadEvidence.Components` für alle Source-Familien. Compose behält seinen dedizierten Parser (Zeilen 162-193, `SelectedCompose`-Pfad). ✔
2. **Ports/Health/Workload vs Infrastructure für alle Familien.** `shareProjectSummaryFromComponents` (inspect.go:468) projiziert `component.Ports` → `Ports`, `component.Health` → `HealthChecks` (Kind `EvidenceHealth`), und klassifiziert `InfrastructureClass` ∈ {database.sql, cache.key-value, database.document, messaging, object-storage.s3} → InfrastructureServices, Rest (Ports/Health/Image/Build) → WorkloadServices. ✔
3. **Capability findings source-neutral.** `capabilityFindingForInfrastructureClass` (inspect.go:502) mappt normalized InfrastructureClass → Capability-Finding (Capability=Class, Name=component.ID, Confidence=Detected). Quadlet/Kubernetes zeigen dieselben Capability findings wie Compose. ✔
4. **Logs-Vorschlag nicht Compose-only + korrektes Evidence-Kind.** inspect.go:215-226: Gate nun `manifest == nil && result.SelectedWorkloadSource != nil && len(result.WorkloadServices) > 0` (nicht mehr `SelectedCompose != ""`), Evidence-Kind `sourceEvidenceKindScalar(result.SelectedWorkloadSource.Kind)` — Compose → `EvidenceCompose`, alle anderen → `EvidenceConfig`. Der alte Bug (false `EvidenceCompose`-Label, inspect.go:221 Original) behoben. ✔
5. **Parity-Test.** `TestInspectProjectsNeutralSummaryForAllSourceFamilies` (workload_source_parity_test.go) asserted Ports/Health/Workload/Infra/Capability findings für compose/quadlet/kubernetes-Fixturen; `assertSourceEvidenceKind` verlangt Compose-korrektes Evidence-Kind für Compose und `EvidenceConfig` für alle anderen (kein falsches Compose). ✔
6. **Keine Repo-Mutation.** Keine Schreiboperation; nur Projektionslogik. ✔
7. **Kein Selbstqualifizierungs-Zirkel.** `shareProjectSummaryFromComponents`/`capabilityFindingForInfrastructureClass`/`sourceEvidenceKind*` sind neue private Funktionen im Write-Set; die CI-Auflösung (`INSPECT_PROJECTION_REVIEWED` → `inspect-implementation-resolved`) ist #1224s Mapper-Merge, kein Zirkel. ✔

## Repo-rule compliance
- Write-Set nur `internal/repositoryinspect` (Produktarea inspect). Kein Plan/PR/CI im baseharbor-PR. ✔
- Branch-Isolation: isolated worktree `worktrees/w750b`, branch `work/v0.4x-core-750-inspect-findings` (lokal, NICHT für den Produkt-PR verwendet; #1222s eigener Branch wurde korrigiert). ✔
- Commit: ein fokussierter Commit `74a35765`. PR #1222 body trägt kein `Closes`. ✔
- Kein Force-Push auf fremde Branches ohne Korrektur; #1222s Branch-Korrektur war notwendig, da der ursprüngliche Branch einen noch fehlerhaften Evidence-Kind-Bug enthielt (AUFGABE B explizit gefordert). ✔

## RUN-ZEUGE (lokal, §4.6)
- `go test -count=1 ./internal/repositoryinspect/` — ok 0.070s, inkl. `TestInspectProjectsNeutralSummaryForAllSourceFamilies` (compose/quadlet/kubernetes PASS).
- `go vet ./internal/repositoryinspect/` — clean (exit 0).
- `go test -count=1 ./internal/capability/ ./internal/application/` — ok (application 51s).
- Full `go test ./...` — sandbox timeout (124s) während cmd/baha native-runtime compile volume; betroffene Pakete (repositoryinspect/capability/application) alle OK. Kein Code-Signal.
- CI Run #41059938103: `PR Selected Checks` success, alle Jobs success/skipped.

## VERDICT: ACCEPT
PR #1222 erfüllt den core-750-Vertrag: source-neutral Shared-Summary-Projektion aus normalisierter `WorkloadEvidence.Components` für Compose/Quadlet/Kubernetes, capability findings source-neutral aus normalisierter `InfrastructureClass`, Logs-Vorschlag nicht-Compose-only mit korrektem Evidence-Kind, Parity-Test grün, kein Repo-Mutation. SHA-genau bestätigt gegen Run #41059938103.

CODEX-MERGE: autorisiert nach #1224-Muster (Owner-Autorisierung in Mission w750c + baseharbor-plan AGENTS.md Owner-delegation). Merge nur über den Merge-Button, keine direkte Branch-Bearbeitung.

END rv1224-B DONE
