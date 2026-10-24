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
