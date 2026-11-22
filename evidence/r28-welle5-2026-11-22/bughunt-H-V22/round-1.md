# H-V22 bug-hunt footprint/record-deployment desk - round-1 akte

Sitz `w21-pr1702-0428-bughunt-hv22`. Bug-hunt H-V22, owner-order, REINE BEFUNDUNG, develop-stand, KEINE Produkt-/Datei-Aenderung.

Auftrag: footprint-/record-deployment-desk. Pruefen ob `app footprint show -o json` eine LESE-operation ist (kein --confirm-candidate brauchen sollte) oder ob ein record-schritt korrekt als mutation gilt; wo die footprint-ausgabe vom contract (JSON/MCP) abweicht.

GRENZE (read-only, NICHT aendern): cmd/baha/app_apply.go:189-192, cmd/baha/app_candidate_consent.go, internal/deployment/deployment_record.go:520-542. 227/237-area.

## PLAN

- plan in board-file + ## PLAN in akte
- develop fetchen, HEAD-sha in akte (read-only: gh/d, fetch refs/heads/develop)
- footprint show read-classification auditen (app_apply.go:189-192, app_candidate_consent.go, deployment_record.go:520-542); NICHT aendern
- record-deployment mutation-classification + footprint output vs contract (JSON/MCP) abgleichen
- je flaeche positiver + negativer fall, datei:zeile, reproduzierbar; klassifizieren: ECHTER DEFECT / doku-luecke / kein-befund
- fund kartenwuerdig: datei:zeile + mindest-rezept in akte (Owner giesst karte); KEIN produkt-aendern, KEIN PR, KEIN kommentar
- cleanliness + END; 9142ab1f posten

## Befunde

develop HEAD: 64eab13e23fba8bca07a1d68c687fa36afedb64e (git ls-remote origin refs/heads/develop)

### Befund B1 — READ-CLASS: `app footprint show` IS a read operation (kein --confirm-candidate, no operator required for local targets) — KEIN DEFECT, positive befund

- cmd/baha/app_footprint_show.go:23-27: `appFootprintShow` "It never calculates a footprint, queries a runtime or persists state." Only reads a GuidedReadContext and renders it (human or JSON).
- internal/machine/contract.go:243: `app.footprint.show` is registered with `Safety: SafetyReadOnly`. machineMCPTool(cmd/baha/mcp.go:266-281) derives readOnlyHint=true, destructiveHint=false from this.
- cmd/baha/app_registration_921.go:39-41: command Summary "Read the current application footprint"; child "Display the authoritative Target footprint without mutation".
- cmd/baha/mcp.go:332 authorizeMCPOperation: `LocalWorkloadOperation` (internal/operatorauth/local_runtime.go:54-63) does NOT list "app.footprint.show", so `verifiedLocalWorkloadAuthority` (cmd/baha/local_workload_authority.go:41-110) returns `(nil,false,nil)` for show -> the managed-environment operator boundary (`ensureManagedEnvironmentOperatorBoundary`) is skipped for non-managed/local targets. show fails closed only on a genuinely operator-required managed-environment (OIDC), exactly like other read tools (app.show, app.preflight).
- Reproduzierbar (positiv): read-only, no mutation, no candidate-consent. Negativ: no `--confirm-candidate` required, no persisted DeploymentRecord (recordDeploymentBeforeMutation is only called on the APPLY path, app_apply.go:192 / app_remote_lifecycle.go:163, state="applying").
- Klassifizierung: KEIN DEFECT. footprint show correctly classified read-only; the 227/237 "consent refusal for show" concern (proven in card 0428-227/237 consent-mechanism-round-1 akte) is not live here - show is read-only by contract and by the LocalWorkloadOperation allowlist.

### Befund B2 — RECORD-DEPLOYMENT is correctly classified as a mutation choke point — KEIN DEFECT, positive befund

- cmd/baha/deployment_record.go:400 `recordDeploymentBeforeMutation(ctx, resolved, state, rawCandidateConsent)`. For state=="applying" (app_apply.go:192, app_remote_lifecycle.go:163) it gates on `deployment.EvaluateDeploymentAdmission` (internal/deployment/target_deployment_policy_admission.go:25-75): requires Core-verified source provenance; refuses dirty/disallowed-branch/unverified-commit/image/approval per Target DeploymentPolicy. Fails closed.
- cmd/baha/app_candidate_consent.go:58-96: `promptConfirmCandidateSubmission` shows the exact canonical content-hash digest the write binds and requires `--confirm-candidate <64-hex>`; without it the apply fails closed. The digest is recomputed from the current source each re-run (repositoryDesiredStateFingerprint), not frozen at an old persisted digest.
- The "record" step (pending DeploymentRecord written BEFORE the mutation) is the authoritative one-installation-owner binding (deployment_record.go:430-445, VerifyDeploymentOwner). Correctly a mutation choke point.
- Reproduzierbar: state="configured" (deployment_record.go:362, legacy, no admission gate) vs state="applying" (gated). Negativ: apply without --confirm-candidate fails closed.
- Klassifizierung: KEIN DEFECT. record-deployment correctly counts as mutation; the admission + candidate-consent gates are in place.

### Befund B3 (ECHTER DEFECT, dokumentiert) — Human footprint presentation drops the `Unused` field that the JSON/machine contract carries; no test covers human parity for it

- internal/application/footprint.go:122: `Footprint.Unused []string` is part of the canonical JSON schema (`json:"unused"`) and is populated at footprint.go:347-350 (resolved-but-never-selected provider instances).
- cmd/baha/app_footprint_presenter.go:22 `renderAppFootprint(...)` renders Version/Target/Realization counts/Core/Complete/Existing/Additional/Requirements/Dependencies ONLY. It NEVER iterates or prints `Unused`. The human view silently drops provider instances that were resolved but not selected.
- cmd/baha/app_footprint_show.go:65-82: JSON path marshals the whole `view.Footprint` (includes `unused`); human path (options.JSON=false) calls renderAppFootprint which omits it. So for the SAME resolved view the two transports diverge: JSON carries `unused: [instanceIDs]`, human prints nothing about them.
- Positive reproduzierbar: resolve an application where a provider instance is resolved but not selected (len(Unused)>0) - human `baha app footprint show` omits it, JSON shows it. Negativ: no test asserts the human presenter surfaces `unused`.
- Mindest-rezept (card-worthy, Owner giesst): human presenter should surface unused resolved instances, e.g. append after the Existing/Additional loop in renderAppFootprint (cmd/baha/app_footprint_presenter.go): `for _, id := range fp.Unused { fmt.Fprintf(&out, "- %s: resolved but not selected (unused)\n", footprintLabel(id)) }` plus a one-line summary in the summary block; add an assertion in app_footprint_show_test.go comparing human vs JSON for a footprint with len(Unused)>0 so the parity is durable. Scope: cmd/baha/app_footprint_presenter.go + tests only.
- Klassifizierung: ECHTER DEFECT (contract/presentation divergence) - low severity (information-loss, no write, read-only surface), card-worthy per H-V22.

### Befund B4 (doku-luecke / stale reference) — Mission references internal/deployment/deployment_record.go:520-542; that file does not exist on develop

- The deployment record logic lives in cmd/baha/deployment_record.go (761 lines) since a refactor; internal/deployment/ holds config_mutation.go, damaged_state.go, target_deployment_policy_admission.go - no deployment_record.go. The read-only gate boundary the mission pointed at (520-542) is now cmd/baha/deployment_record.go:400 (recordDeploymentBeforeMutation) + target_deployment_policy_admission.go:25 (EvaluateDeploymentAdmission).
- Klassifizierung: doku-luecke / stale path reference in the mission; not a product defect. B2 maps the actual location.

## Fundbilanz

- Echte Dekte: 1 (B3 - human footprint omits Unused vs JSON contract)
- Doku-luecke: 1 (B4 - stale file path reference in mission; actual boundary documented)
- Kein-befund: B1 (show is read-only, correctly), B2 (record-deployment correctly a mutation choke point)
- Gesamtflaeche: 4 Befunde; 1 card-worthy defect (B3)

## cleanliness

(nichts geaendert; keine eigenen container/volumes/state angelegt; ambient-core fremder lanes untouched)

## END w21-pr1702-0428-bughunt-hv22 DONE

- develop HEAD (witness): 64eab13e23fba8bca07a1d68c687fa36afedb64e (git ls-remote origin refs/heads/develop, github remote)
- 4 Befunde; read-only audit only, KEIN produkt/datei-aendert, KEIN commit/push, KEIN PR, KEIN kommentar
- B1 (kein-befund): app footprint show IS read-only (contract.go:243 SafetyReadOnly; app_footprint_show.go:23-27 no runtime/persist; LocalWorkloadOperation allowlist omits show -> no operator for local targets)
- B2 (kein-befund): record-deployment correctly a mutation choke point (deployment_record.go:400; EvaluateDeploymentAdmission target_deployment_policy_admission.go:25-75; --confirm-candidate choke app_candidate_consent.go:58-96)
- B3 ECHTER DEFECT: human footprint presenter drops `Unused` field the JSON/machine contract carries (footprint.go:122,347-350 vs app_footprint_presenter.go:22 renderAppFootprint omits it) - minimal fix recipe in akte; scope cmd/baha/app_footprint_presenter.go + tests
- B4 doku-luecke: mission path internal/deployment/deployment_record.go:520-542 does not exist on develop; actual location cmd/baha/deployment_record.go:400 + target_deployment_policy_admission.go:25
- fund B3 kartenwuerdig, rezept in akte (Owner giesst karte); kein produkt-aendern, kein PR, kein kommentar
