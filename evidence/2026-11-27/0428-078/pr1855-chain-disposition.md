# 0428-078 — #1855 serial chain disposition

**Role:** Codex disposition against the live card contract. Evidence only; no card fields, product files, or PRs changed.

## Contract and current witnesses

The live task is `tasks/t-20261114-r28-perses-dashboard-identity.md` (0428-078) on plan main `2f8c70604d08b1c1cdc710f48331563d5ab6c907`. Its current blocker records the required serial order: #1812 -> #1819 -> #1820, then refresh #1855 and obtain exact-head Codex acceptance, and only then close #1650/#1818. Its acceptance still requires verified current Keycloak metrics, Target/tenant-scoped fail-closed authorization, and the card-owned dashboard/tests; a green runtime matrix does not waive these functional requirements.

At the inspected snapshot, product develop is `c167fa5dd323ae0746385caa2bdb8364ec7ad03f`:

- #1867 is MERGED as `f36d29301e16845b5034a9c7103c053a6a869585` (merge time 2026-11-26T22:28:15Z). This catalog PR is not a completion witness for the serial product chain.
- #1812 is OPEN/BLOCKED at `05cb3fd95bdb390175482f1c08eadb28d9c9863a`.
- #1819 is OPEN/BEHIND at `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`.
- #1820 is OPEN/BEHIND at `8f6b2444bdc9baabf4f492e930533c7c36406979`.
- #1855 is OPEN/BLOCKED at `d18e4b367940ad5ee36862dbda1eea2d7a605db0`. Exact-head pull_request run [45911769054](https://github.com/mcpdev80/baseharbor/actions/runs/45911769054), attempt 1, concluded FAILURE. Its job census is 46 total: 27 success, 16 skipped, 3 failures (Go packages, identity-provider package tests, and PR Selected Checks aggregate). The selected runtime jobs executed and succeeded, including Docker/Podman data-capabilities and observability. The Go failures include `TestKeycloakSignalRegistrationTargetProductionAttribution` (observed attribution root `docker-dev`, expected the producer state root) and the identity-dashboard witness target-attribution tests. These failures leave the #1819 producer seam unresolved; the successful runtime jobs do not override them.
- The current w349 artifact `evidence/w349-0428-078-154156hop/evidence.md` records Plan PRs #154 and #156 as transport hops only; it is not final #1855 acceptance evidence.

## Decision and required sequence

**HOLD; the live contract is not complete.** The missing work is the successful, serial producer chain and a refreshed, independently accepted #1855 candidate—not another catalog transport record.

1. Qualify and land #1812 on its final exact head, including the card-required Docker then Podman Light runtime gates.
2. Only after #1812 lands, refresh and qualify #1819 against that develop tip; then land it.
3. Only after #1819 lands, refresh and qualify #1820 against the resulting develop tip; then land it.
4. Refresh #1855 against the completed chain. Resolve the current producer/Target-attribution test failures, preserve the card's dashboard and authorization acceptance criteria, and obtain a fresh exact-head Codex ACCEPT with the required checks executed successfully.
5. Only after that acceptance, close #1650 and then #1818 as superseded records, preserving their cross-links. No closure is authorized by #1867, the failed #1855 run, or the #154/#156 transport artifacts.

This disposition adds no acceptance criterion beyond the live 0428-078 contract and does not perform any implementation, PR closure, or merge.
