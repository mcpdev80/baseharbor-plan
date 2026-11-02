# authz1 — Authorisierungs-Vertrag (Workload Compose optional)

- **Status:** active
- **Lane / Session:** authz1-worker (Ornith), worktree `workers/worktrees/authz1`
- **Branch:** `authz1-fix` (Base: `origin/develop` = 20083909)
- **Evidence:** baseharbor-plan/evidence/board-2026-11-02/authz1/evidence.md

## ## PLAN

1. Befund reproduzieren: `go test ./cmd/baha/ -run TestMCPAuthoring` → FAIL seit #1265.
2. Ursache: `Workload.Compose` durch #1265 (Commit 1a4f9b8c) hinzugefügt; jsonschema-Generator markiert jede `omitempty`-lose Struct-Field als `required` → MCP-Autorisierungs-Intent verlangt `Compose`, verstößt gegen `spec/application-contract-v1.md` (source provenance darf nicht portable-pflichtig sein).
3. Entscheidung dokumentieren: **optional**. Komposition braucht `workload.components`, keine `Compose`-Pflicht.
4. Fix: `internal/application/manifest.go` `Workload.Compose` ein `json:"...",omitempty"`-Tag geben → Schema markiert optional.
5. Regressionstest: gültiger Autorisierungs-Pfad OHNE Compose bleibt OK (kein Test-Downgrade); YAML mit `compose:` bleibt lesbar.
6. `go vet ./...`, `go test ./cmd/baha/...`, `go test ./internal/application/...`, `go build`.
7. Gegen develop pushen, PR + PRSC/CI beobachten (Eigenes-Run-Pflicht 4.6).
8. Evidence + Planning-Update + Handoff post.

## Befund

```
$ go test ./cmd/baha/ -run 'TestMCPAuthoring'
--- FAIL: TestMCPAuthoringAssignsCanonicalIdentityWithoutClientID/create
    author without identity: {... "validating /properties/intent/properties/Workload: required: missing properties: [\"Compose\"]" ...}
```

Bestätigt reproduzierbar auf `origin/develop` = 20083909.

## Ursache

- `cmd/baha/mcp_application_authoring.go` baut den MCP-Intent-Schema über `jsonschema.For[application.Manifest](nil)`.
- jsonschema-go v0.4.3 (`infer.go:342-343`): `if !settings["omitempty"] && !settings["omitzero"] { s.Required = append(s.Required, info.name) }` — **jede Exported-Struct-Field ohne omitempty wird required**.
- #1265 (Commit 1a4f9b8c "accept compose workload field shape") addierte `Compose string` in `WorkloadConfig` **ohne omitempty**, ohne es im Schema optional zu machen.
- Generiertes Schema (lokal verifiziert): `Workload.required = ["Components", "Compose"]`.
- Folge: ein gültiger Autorisierungs-Intent ohne Compose schlägt an der Schema-Validierung fehl.

## Entscheidung (scope decision, selbst getragen)

Ist `Compose` PFLICHT? **NEIN — optional.** Begründung:

- `spec/application-contract-v1.md:66`: *"Repository workload-source kind, source path, Kubernetes kind/name, **Quadlet filename and Compose service syntax are source provenance and MUST NOT be required as portable Application Intent.**"*
- `docs/spec/application-contract-v1.md:52-66` + `docs/reference/manifest.md:38`: `workload.components` ist das portable Feld; `compose` ist source provenance (Compose/Quadlet/Kubernetes-Kennzeichnung).
- Was die Komposition/S3-Annahme braucht: `workload.components` (logische Workload-Komponenten). Das wurde durch #1265 **nicht** angetastet; nur die Parser-Länge für das `compose:` YAML-Feld wurde ergänzt. Die S3-Annahme sendet `compose:` — das muss **lesbar** bleiben (Parse-Erlaubnis), aber **keine Pflicht im Intent-Schema** sein.

Entscheidung: `Compose` bleibt lesbar (Parser akzeptiert `compose:`), wird im MCP-Autorisierungs-**Schema optional**. Keine Umbau der Komposition/Annahme.

## Fix

`internal/application/manifest.go` — `Workload.Compose` optional taggen:

```go
type WorkloadConfig struct {
	Components []string
	Compose    string `json:"compose,omitempty"`
}
```

## repo-rule compliance

- Scope exakt auf den gemeldeten Fehler (Compose-Schema). Kein `shared_backends_inventory.go` (STOP), keine Workflow-Dateien, kein Merge, kein Spawn.
- Repo-Regel: portable intent ≠ provider/source-Realisierung; source provenance darf nicht Pflicht sein.
- Kein Test-Downgrade; Regressionstest prüft echten validen Pfad OHNE Compose.

## Evidence

- Schema-Lokalisierung: jsonschema-go infer.go:342-343; lokaler Schema-Dump `Workload.required = ["Components","Compose"]`.
- Spec-Zitate: application-contract-v1.md:66; manifest.md:38.
- Commit-Analyse: 1a4f9b8c / aef6b0e1 (#1265).

## END

ACTIVE — Fix implemented, local verification pending.
