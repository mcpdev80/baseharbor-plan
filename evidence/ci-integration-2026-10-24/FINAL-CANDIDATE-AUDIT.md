# v0.4.26 final candidate and evidence audit

Read-only assessment recorded 2026-10-24 by `/root/release_audit`. Product baseline: Core develop `133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f`. Planning baseline initially `3acef76f809b1263e9a5f619070dc3825615d82d`. No implementation, merge, dispatch or publication was performed in this lane. This is preparation evidence, not release approval.

## Existing canonical final-freeze route

Finish Core implementation, CI policy/execution changes and static release-preparation inputs before selecting final Core commit **R**. Then freeze actual Demo **D** with `baseharbor-core.ref=R`, Console **U** with `R/D`, and Connector **K** with `R/D/U`. Use exact `R/D/K` inputs for qualification; no guessed squash SHAs.

This route already exists:
- [pre-release.yml lines 131–137](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/.github/workflows/pre-release.yml#L131): v0.4.24/v0.4.25/v0.4.26 generate the versioned consumer-pins file at execution time using `--core HEAD`, exact Connector and Demo inputs. The reverse `*.demo-ref` source-file requirement is in the other branch.
- [ecosystem_release_pins.py lines 17–53](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/scripts/ecosystem_release_pins.py#L17): exact Core/Demo/Console/Connector bindings must agree; the v0.4.26 DAG is derived from them.
- [pre-release-resume.py lines 266–275](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/scripts/pre-release-resume.py#L266): Demo's immutable Core pin must equal the tested candidate. It explicitly documents why Core cannot embed its future consumer commit.
- [v0.4.25 release audit lines 140–149](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/docs/internal/release-audits/v0.4.25.md#L140): the same Core→Demo→Console→Connector freeze and dynamically generated pins were used before; a reverse Demo-SHA commit into Core would move the candidate after binding. Neither the qualified v0.4.25 Core `f325b93c589d8b807f44dd0086636aabe83fcd65` nor current released main contains `v0.4.25.consumer-pins.json` or `v0.4.25.demo-ref`.

W1 Core anchor **C** `1861ed07888a1ec22c218ca491d23ee54f48e261` remains a valid specifically assigned intermediate proof anchor. It must not be silently relabelled final R. A later final R requires consumers actually bound to R.

## #1050: actual scope, risk and smallest safe disposition

[PR #1050](https://github.com/mcpdev80/baseharbor/pull/1050), inspected at exact head `388967621c90750e59c5faab35344b46d4108fef`, adds exactly one file: `docs/releases/v0.4.26.consumer-pins.json` (72 lines). It stores historical C `1861ed07`, Demo `25c31969`, Console `69d1d140`, Connector `df1f4378`, the three joint-consumer gates and the four-role DAG. Its body records an Owner instruction to publish the data file and a later conditional core-tip update which never happened. Those old pins are not today's final consumer evidence.

There is no technical requirement in the existing v0.4.26 workflow to commit this intermediate file. The source job generates/overwrites it from the actual final graph. Two dispositions are technically possible, but neither permits presenting the historical file as final:
1. Integrate an explicitly historical C snapshot before final R, preserving its provenance and documenting that the final workflow-generated artifact supersedes it. This meets the original stored-file request, but adds a stale-looking generic versioned pin file and requires its remaining qualification/CI.
2. **Preferred minimal release path:** explicitly supersede/withdraw the historical persisted snapshot requirement in the coordinator's planning record, retain #1050 history and the old exact JSON in evidence, and deliver the final canonical generated JSON in immutable Planning evidence alongside the matching workflow approval/coverage matrix. Do not silently close or change the original Owner request; record the Maintainer's disposition and why the existing acyclic resolver is used.

The second option avoids a redundant Core write/qualification cycle and the temptation to invent reverse-pin policy. If the coordinator chooses the first, freeze final R only after #1050 integration; do not update the source pin file again after final R just to point to R/D/U/K, since that changes R.

No new cycle policy, hash exemption or handoff allowlist change is proposed. [release-handoff.py lines 50–54](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/scripts/release-handoff.py#L50) permits only the existing small publication-metadata set for v0.4.26; CI and consumer-pin deltas are outside it.

## Exact 65-gate fingerprint probe

The candidate-owned [release-requirements.json](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/scripts/release-requirements.json) requires **65** gate IDs for v0.4.26: 5 static atomic, 36 runtime atomic, 4 adoption, 8 HA, 2 reference journeys and 10 integration IDs.

A read-only probe called the existing `GitInputs.fingerprint` implementation for every v0.4.26 gate, using:
- old Core C `1861ed07888a1ec22c218ca491d23ee54f48e261`;
- current Core `133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f`;
- the same immutable Demo `f57c8b6e5ff39d0873df62b26272962765e88d6e` on both sides.

Result: **0 equal / 65 changed**. This is input-equivalence evidence, not execution evidence or a complete authenticated artifact sweep. It proves C-bound atomic/HA/journey inputs cannot be reused for today's Core solely because the product delta looks like CI. [fingerprint code](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/scripts/pre-release-resume.py#L197) includes candidate source objects and execution contracts; special native/pin-independent exemptions are limited to earlier releases. No broadening is proposed.

A complete history crawl was not required to establish this C→current mismatch. The existing canonical collector must still authenticate original artifacts, attempts, fingerprints and joint private-consumer origins for the final graph. Do not fabricate “all 65 untested” merely from this comparison; it rejects this particular C→current reuse, not every possible historical origin.

Cheapest safe scheduling: finish all Core/CI changes before R; then perform only required missing/affected final-input gates and preserve every verifier-valid successful origin. Four W1 tests alone are not complete release coverage.

## Documentation and remaining release boundaries

EN/DE release notes, release indices and CHANGELOG exist. The accepted [docs/Pages candidate run 40064756153](https://github.com/mcpdev80/baseharbor/actions/runs/40064756153) succeeded on source `4046bc93ebc7ce346d50d776551fba5ec60b6abf`. API comparison to Core `133e27f6` lists only `docs/internal/ci-binding-qualifications.md`, `scripts/pr-gate-plan.py`, `scripts/test_pr_gate_plan.py`; public EN/DE docs, MkDocs configuration and Pages workflow are unchanged. Keep that scoped accepted evidence. Final exact-candidate docs/source checks still belong to qualification, especially after any further publication-preparation edits.

At this baseline, `v0.4.26.evidence-runs`, `v0.4.26.selected-gates.json`, `v0.4.26.consumer-pins.json` and `v0.4.26.demo-ref` are absent from develop. Q20 lists these as future freeze followups, but the canonical v0.4.26 workflow shows generated consumer pins and no reverse demo-ref requirement. The coordinator must reconcile that dossier wording with the existing acyclic process rather than force a circular source edit.

Remaining actual boundaries:
- integrate the known CI/product chain with genuine required CI;
- obtain corrected Demo native cleanup proof and actual final consumer graph;
- execute/verify required New/Edit/SQL/provider and joint consumer native receipts;
- final source/docs/build and complete authenticated 65-ID coverage/approval;
- promotion to main, permitted metadata finalization, immutable tagging/publication;
- release archives/checksums, binary/image version, attestations/provenance and actual published Pages verification.

CHANGELOG's undated v0.4.26 candidate section and candidate release-note wording are intentional preparation state. Date/tag-link/publication wording belongs to promotion. Existing [readiness vocabulary](https://github.com/mcpdev80/baseharbor/blob/133e27f6b3ea9fd7b74dc2b7e5878c7091d9228f/docs/internal/pre-release-documentation-audit.md#L12) distinguishes pre-release-ready, release-ready and actual publication/post-release completion. No readiness is claimed by this audit.


## Coordinator disposition

The delegated Maintainer chose option 2 and closed #1050 as superseded preparation, not fulfilled/merged implementation. Independent /root/independent_review checked the disposition. The original source JSON is preserved as historical-consumer-pins-1050.json in this directory. Its old C/D/U/K are not final. The complete final canonical JSON and exact R/D/U/K, run/attempt and origins remain mandatory Planning evidence; the workflow approval upload does not automatically contain that JSON.
