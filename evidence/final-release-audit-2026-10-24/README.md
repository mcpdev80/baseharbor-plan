# Independent final release route audit — v0.4.26

Read-only audit by `/root/final_audit`, 2026-10-24. This file records preparation and scoped source review, not release approval. No product write, merge, workflow start, tag or publication was performed by this lane. Root owns integration and publication of this evidence.

## Current inspected anchors

- Remote Core develop: `67c30e8e46faf8fe9a0ef685be2e3cc661af07f0` (publication-prose #1069 merged).
- Remote Core main: `54acc4b66715681213788fdba395a569ddc95a1b`.
- Remote Planning main: `581deae246dbdb4e7239bec4b3e7b2aae663110f`.
- Core release notes are being shortened before the final immutable Core R. No later head is implicitly reviewed.

The successful native Go Docker run40117855934 and Demo Podman run40117924670 bind intermediate Core64dbf1df and Demof90d0623. They must not be relabelled final R/D coverage. Actual input compatibility must be established by the applicable verifier, or fresh execution supplied.

## Existing immutable freeze and workflow routes

Finish Core first, then freeze actual merged Demo D with Core R; Console U with R/D; Connector K with R/D/U. `scripts/ecosystem_release_pins.py` resolves and validates these exact source-owned references and generates the complete four-role DAG. No reverse D/U/K source commit into Core is required.

With no workflow-dispatch mutation in the connector, the existing push routes are:

1. `runtime-validation/docker/v0426-<unique>` pointing exactly at R: existing eight-family native Go Docker workflow. Do not use its special provider-ha or mcp-edit-native subroutes, which skip that job.
2. `validation/pre-release/selected/v0426-<unique>` pointing exactly at R after final graph freeze: existing selected preflight reads `docs/releases/v0.4.26.selected-gates.json`.
3. `release-candidate/v0.4.26-<unique>` pointing at the same R, only after preparation and atomic-first evidence are fulfilled: existing full65 release-boundary approval.

The orchestrator defaults Connector source to `work/v0.4.26-integrations-docs`; hold this branch at actual K during both resolver calls. The resolver captures immutable SHAs; do not update the branch between them. Exact final graph JSON remains mandatory external evidence, even though the source workflow generates its temporary copy.

The canonical selection was independently parsed:65 required gates comprise41atomic,4adoption,8HA,2journey and10integration. The selected file contains63 unique required IDs, no extras, omitting exactly `journey/docker` and `journey/podman`. File SHA256: `58911ae1b60200bb4085eeebb2d3378584169aad556e05a2ce2641192b3e0607`.

## Evidence and rerun limits

The selected preflight does not create release approval. The full workflow's final job must authenticate every unique required proof, exact candidate/Demo/consumer bindings, origins and complete coverage before producing approval/v2. Missing, failed or skipped required evidence remains blocking.

`pre-release-resume.py` reads explicit origins from `docs/releases/v0.4.26.evidence-runs` (or the provided `--runs` path). An absent file means no external Core origins; it does not automatically discover the earlier selected63 run. The approve mode adds its own current run. Consequently separate63 and65 runs duplicate selected execution under the current unchanged source. No verifier relaxation or post-freeze origin-list source edit is proposed. Within an existing run preserve successful jobs and rerun only diagnosed failures; original attempts must remain authenticated.

Required final evidence still includes native New/Edit/SQL/provider, No/Cancel, data/shared/foreign preservation and bounded cleanup; joint Connector Docker can supply the Console browser origin, plus Connector Podman for its other runtime. Native Go eight-family proof is distinct from the65-gate inventory: five named repository/workload test families are absent from that graph.

## Publication and promotion

`release-handoff.py` permits only CHANGELOG.md, docs/roadmap.md, docs/releases/index.md, the exact EN release note and exact internal release audit after approval. DE/README/front-page final wording must be correct before final R. #1069's neutral publication links address this without a policy exception.

The publisher requires the tagged commit on main, a successful compatible pre-release workflow, a matching immutable approval/v2 with65 proofs, the authenticated coverage digest, and reconstructed exact consumer bindings. Tag creation remains Marcel's final action; this lane creates none.

Current main/develop are history-diverged: GitHub reports380 ahead/33 behind at the inspected anchors. Its compare response contains the capped300-file list and is not a complete tree audit. A completed local Git tree comparison at those exact refs reports191 changed files (31,648insertions/1,019deletions); this count alone does not replace review. Inspect that full delta and the actual promotion result. Historical squash divergence does not by itself prove either conflict or content equivalence. Validate the actual published tree against approved R with the existing handoff verifier; preserve any intended main-only content explicitly.

Final date/publication metadata, qualified promotion, actual main containment and exact tag target remain outstanding. No tag command with a guessed SHA is approved here.

## Independent human release-note review

Inspected the local two-file simplification against67c30e8e: EN blob64938d7e and DEc144ca05. Technical verdict: **APPROVE** for this prose delta only. Four matching sections cover application authoring/editing, automation, backup/recovery and compatibility; PR/CI internals are removed. Cancel is limited to unapplied changes, applied changes are not automatically undone, and destructive changes still require consent. MCP proposal/consent/execution wording matches the public application-needs/MCP contracts. Actual backup source confirms the bounded fresh recovery context and attempted-owner recovery after writer-stop failure.

The existing publisher invokes GoReleaser with `--release-notes docs/releases/${tag}.md`, so the EN file is also the actual GitHub Release message. This is a technical independent source review, not a formal GitHub review. The coordinator's reported docs audit and strict EN/DE build results remain their actual executed validation; this lane did not claim to rerun them. Hosted required CI and exact published candidate review remain integration prerequisites.
