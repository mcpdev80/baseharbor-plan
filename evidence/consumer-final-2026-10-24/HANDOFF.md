## Current final-input run

Root fixed final CoreR3e27497b4ef7b567858ba646bc3071bee37d19bd after green required release-notes CI. Demo121 is now a1051ec5f5c366cdfafe527298ac60e5db4f951c, treea372d0f5c473de417006ff6924632f11589073c9, direct parentf90d0623. Exact remote comparison proves sole changed file baseharbor-core.ref, ahead1/behind0. Both PR branch and existing release branch were non-force fast-forwarded with expected-SHA leases. Existing Podman-only native run40128218519 is in progress. Independent final-audit source review APPROVE at this exact head: complete helper/tests/workflow bytes preserved and only Core pin differs. Native receipt remains in progress; no PASS yet. Actual D/U pins remain pending predecessor merges.

# Final consumer qualification — 2026-10-24

## Assigned scope and current hold

Root assigned this lane final Demo/Console/Connector pin candidates and their existing native workflow routes. Root remains sole merger and final acceptance owner. Preserve prior session-2 evidence and existing branches; no Core changes, tags, force updates or duplicate runs. Final pin and runtime mutations are held until root supplies the final release-notes successor Core SHA. Current remote inventory is Demo121 f90d06235322e06f1fb2e4e58f0907b3c492aa91, Console9 6017de2845fa3e4e408c69038a0a5bdd7e82cad9, Connector10 e832d5651752121dea9484e18422d3e6459f9a72.

## Authenticated intermediate native receipt

Demo run40117924670 attempt1, job120943028221, executes Core64dbf1dfcb3397a14bdfc4f1e1d1f8203a936f5c and Demof90d06235322e06f1fb2e4e58f0907b3c492aa91 with native rootless Podman. Runtime step and whole job/run are success. Actual log records Backup/Restore PASS at18:18:43Z, acceptance cleanup beginning18:18:43Z and completing18:22:27Z.

Artifact12569249775 (`demo-v024-podman-40117924670`) was downloaded through GitHub MCP. The local ZIP SHA256 exactly equals GitHub digest `2d47ee6961d7c55df19630fbce837ecee2a4190cd4e4f6dc3d5328ff496892cc`. Its recovery-qualified.json binds those exact Core/Demo inputs, retained recovery, run/attempt40117924670/1, success and cleanup success. All15 actual verification fields are true. `pre_release_ready` remains false. Cleanup-preparation scope-result.json records mode `--unpause-owned`, outcome success, empty accounted/errors lists.

This receipt proves the corrected cleanup on its actual inputs only. The upcoming final successor Core and final consumer graph are not qualified by relabelling this receipt.

## Existing safe trigger/history routes

Demo's existing `work/v0.4.26-ecosystem-release` workflow selects only Podman when the candidate commit message includes `[demo-podman-runtime]`. Continue121 and fast-forward the trigger branch only after exact final Core pin publication. No new workflow or source edit is needed.

Console9 and the historical Console trigger69d1d14007fa43dc0c0457c3347280be7f802818 have completely identical blob/mode inventories. Connector10 and its triggerdf1f4378d8c7fdc3e174a1e9dc8ad0155a955571 differ only by base-owned `zz-o16-test.txt` (blobba86891cd387201ce0e9aa38763e795b8b81781b, mode100644), which must be retained.

After actual Demo merge D and Console merge U, repin Connector manifest to final R/D/U. A true history integration of its existing trigger branch as second parent can preserve all accepted main-line content and permit non-force fast-forward of that branch. Independently inspect the complete resulting tree; do not treat matching manifests alone as matching source. The existing Connector `release-integration.yml` push route uses `[ecosystem-runtime]` and runs Docker/Podman with maximum parallelism2, producing the actual Console-browser and remote-Connector native receipts jointly. A separate Console long browser run is redundant when the canonical joint receipt verifier accepts the actual matching inputs.

## Remaining gates

Final Core R from root; exact Demo pin and fresh native acceptance if required for new input; actual D; Console R/D source checks and actual U; Connector R/D/U source checks/history integration and joint native receipts; exact merged K and canonical graph qualification. No readiness or consumer acceptance is claimed.

## Source integration and native acceptance boundary

The current core-923 contract requires real final immutable consumer qualification before acceptance/readiness, but does not require a native run before each pin-only source integration. The existing Native-HANDOFF expressly sequences actual D, Console repin/review/integration to U, Connector repin/review/integration to K, then final graph/W1 execution. Its source-only warning forbids claiming skipped native jobs as PASS; native acceptance remains open after source-only integration. Demo121's concrete recovery/cleanup defect retains its distinct explicit native receipt-before-merge requirement.

Existing consumer source workflows intentionally gate native browser/transport/enrollment jobs to runtime-validation pushes; ordinary pull requests run source quality. Therefore a Maintainer may integrate exact reviewed pin-only Console/Connector candidates after their current mandatory source CI while retaining consumer native acceptance open, then execute the joint native workflow at actual merged K once. This is source integration, not task acceptance or release readiness.

All three consumer repositories currently allow genuine merge commits. For Connector, preserve old trigger ancestry in the candidate, then use a real merge rather than squash; include `[ecosystem-runtime]` in the actual merge commit message. The merged K remains descendant of the old trigger branch, permitting a non-force fast-forward directly to exact K. Squashing would discard that ancestry and prevent this exact-K route.

## Cheap unchanged-source preflight before final D/U

At Console6017de28, the existing52 contract tests passed with0skips on Node24.22.1; the architecture guard and candidate manifest schema passed. This is bounded source preparation, not the hosted full npm/browser proof.

At Connector e832d565, the complete existing Go race suite passed (11tested packages,2packages without tests), module checksums verified, vet and CLI build passed, canonical wire schema/golden hashes match exact workflow locks, and gofmt is clean. Local toolchain Go1.26.9 was reused; the existing hosted source workflow uses1.26.2 and will run on the actual new pin candidate. Final manifest value equality waits actual D/U; no future squash SHAs were guessed. No tests or source implementations were added or changed.

Actual final-Core contract comparison also passed: all6 Console control/read-model/terminal canonical artifacts equal the Git blobs at finalR3e27497b and match the Console source-lock SHA256 values. Connector wire.schema.json and wire.golden.json also equal finalR's canonical source exactly and retain their known locks. These are actual final-source compatibility checks, not an assertion based only on the historical harness Core pin.
