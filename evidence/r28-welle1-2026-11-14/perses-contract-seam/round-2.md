# round-2 — 0428-075 define Perses prov seam

Lane: worker (worker-ornith1.5) — correction round r2 on existing candidate
Date: 2026-11-14
Card: t-20261114-r28-perses-contract-seam (0428-075), release v0.4.28
Task: read mission-075-r2.md; fix CODEX-REVIEW R1 REJECT on PR #1575
PR: #1575 (DRAFT, base develop 0e9ccb582), https://github.com/mcpdev80/baseharbor/pull/1575
Branch: lane-0428-075-perses-seam (existing; keep working here, no second branch)
MERGE-FROST: no merge, PR stays DRAFT.

Base attest: cut from base develop 0e9ccb582f5bdcdc74049bbe3996263cdce6500c (`git ls-remote origin develop`)
Branch provenance: PR #1575 head 61f76fa18897d4a0709c09c27ae67e1ded8dba20; develop 0e9ccb582 is an ancestor; only one candidate commit on top (witness pasted in END).

## SOURCE OF TRUTH

- akte act-1575-review-r1.md: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r28-welle1-2026-11-14/vm-bughunt/act-1575-review-r1.md
- task: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/tasks/t-20261114-r28-perses-contract-seam.md

## PLAN

- Read akte act-1575-review-r1.md + task; confirm scope against PR #1575 (draft, base develop 0e9ccb582).
- manifest.go: gofmt only, no semantic change.
- perses.go: Provisioned/verification must key on the actual selected/provisioned runtime path (provider-config instance + reachable health), never compile-time version/image defaults; no pinned release => not-configured/unsupported.
- management_ui.go: VerifyPersesManagementUIAt must fail closed without a pinned release and never report a false "configured" surface.
- docs/spec/provider-management-acceptance-v1.md: move Perses HA row to unsupported/unverified until real runtime proof (this PR brings none).
- tests: exercise the genuine CLI entry point (baha status / doctor) for the unprovisioned and unknown-ownership/missing-authorization cases, or narrow the implementation/spec claims; keep in the draft Go CI group.
- go build, go vet, go test affected packages locally.
- commit candidate to lane-0428-075-perses-seam; push PR #1575 (stays draft).
- report hosted CI run for the new head (capture run-id + PASS/FAIL lines); stop if source/routing is red.
- write round-2.md evidence, commit to planning origin/main, post END to coordinator.

## Review R1 verdict (quoted from akte)

REJECT for candidate 61f76fa18897d4a0709c09c27ae67e1ded8dba20. The candidate does not meet the fail-closed runtime and evidence requirements.

Findings:

- internal/capability/perses.go: PersesManagementSurfaceNow sets Provisioned=true when the compile-time default version/image strings validate. This does not verify that a Perses service is selected, provisioned, or reachable. internal/metrics/management_ui.go:VerifyPersesManagementUIAt likewise validates only the compile-time constant. A pinned declaration is realization metadata, not runtime provisioning evidence.
- docs/spec/provider-management-acceptance-v1.md: the new Perses row claims SUPPORTED availability across one Prometheus member failure. This PR adds no Perses runtime lifecycle or failover proof; the Prometheus backend's continuity does not establish the Perses UI's continuity. The row overstates verified behavior.
- The tests do not exercise a genuine user entry point. They call internal validation/descriptor helpers and manifest parse/render methods; no CLI command is invoked. The task explicitly requires the genuine entry point and forbids substituting an internal seam call for CLI coverage. The tests also do not exercise unknown ownership or missing authorization behavior.
- Hosted CI run 43637427710, exact candidate SHA, triggered by the draft PR update: PR · Draft Go · cli-0, cli-1, cli-2, cli-3, and packages succeeded. PR · Draft source and routing failed. Exact failing log line: Unformatted Go source: internal/application/manifest.go. Other displayed groups were skipped under draft selection. No rerun or workflow dispatch was initiated.

## Correction recipe (from akte, applied verifiably)

1. In internal/application/manifest.go, run gofmt and keep the change limited to formatting.
2. In internal/capability/perses.go and internal/metrics/management_ui.go, make Provisioned and verification depend on actual selected/provisioned runtime state. A valid version/image declaration alone must remain unconfigured/unsupported. Add a deterministic negative test where no Perses runtime exists, and test the actual CLI entry point that surfaces the result. Do not implement container lifecycle in this task.
3. In docs/spec/provider-management-acceptance-v1.md, classify Perses HA as unsupported or otherwise unverified until Perses-specific runtime evidence proves continuity; do not infer UI availability from Prometheus backend continuity.
4. Add deterministic tests for unknown ownership and missing authorization through the public CLI path, or narrow the implementation/spec claims if the existing boundary cannot support those cases. Keep new tests in the existing Go package coverage selected by the draft Go CI group and confirm the triggering source path; do not edit .github/**.
5. Re-run the changed candidate's required existing checks after the fixes are committed. Stop if the source/routing check remains red, the CLI still reports provisioned without runtime evidence, or the authorization/ownership result is not fail-closed.

## Owner scope decision (2026-11-14, direct)

"ein reines A oder B. Provisioned wird an der MANIFEST-WAHRHEIT geerdet und von der ERREICHBARKEIT GETRENNT:

1. provisioned = Oberflaeche im Manifest gewaehlt (services.perses) UND angepinntes Vertragsbild validiert — ausgegeben als configured; ohne Auswahl not configured (fail-closed).
2. zaetzlicher Zustand reachability: unverified — niemals true/healthy ohne echten Health-Pfad; keine SUPPORTED-HA-Zeile.
3. docs/spec/provider-management-acceptance-v1.md: HA auf unverified (configuration-only).
4. Tests: echter CLI-Eintritt ohne Container — Command-Pfad mit tmp-root ueber die injectierbaren Abhaengigkeiten (Praezedenz 175-r8: kein interner Helper-Aufruf, echte Command-Ausfuehrung); wo das nicht geht, Anspruch verschmaelern und Grenze in die Akte. Begruendung (1)-(4) in round-2.md fuer die Abnahme."

So: Provisioned is grounded in manifest truth (surface selected + pinned release validates), NOT the compile-time default string alone. A separate reachability state = "unverified" (never true/healthy without a real health path; no SUPPORTED HA line). Tests run the genuine CLI command with a tmp root over injectable deps (real command execution, per 175-r8), not an internal seam call.

## Implementation notes

- Go entry point for status/doctor: cmd/baha/app_observe.go (appStatusCommand / appDoctorCommand).
- Management-UI surface list: internal/application/management_ui.go ApplicationManagementUISurfaces -> PersesManagementSurfaceNow (candidate).
- metrics verify path: internal/metrics/management_ui.go VerifyManagementUIAt -> if m.Services.Perses { return VerifyPersesManagementUIAt(ctx) }.
- VerifyPersesManagementUIAt currently returns capability.ValidatePersesRelease(capability.PersesDefaultRelease) — keys off compile-time default, not runtime state.
- base develop 0e9ccb582 has no Perses block in ApplicationManagementUISurfaces (candidate adds it).
- Manifest parsing/validation: internal/application/manifest_parse.go, manifest_validation.go, manifest_render.go (candidate).
- Manifest round-trip test: internal/application/manifest_test.go.
- metrics test dir: internal/metrics/ (base has prometheus_integration_test.go etc.).

## repo-rule compliance

- Planning repo verified as /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (real origin). workers/baseharbor-plan is the bookkeeping repo and was NOT used; a misplaced evidence file there was removed before work.
- No .github/** edited. No reruns, no workflow_dispatch.
- No subagents used. Every step done in this session.
- Branch cut from base develop SHA 0e9ccb582, an ancestor of the candidate.
- Evidence lives only in baseharbor-plan evidence/ (never in the product repo).
- Managed compose/test stacks brought down by my last action (none started this round).

END round-2 in progress.
