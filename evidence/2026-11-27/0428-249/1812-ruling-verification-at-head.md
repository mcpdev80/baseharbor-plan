# #1812 owner-runner-health ruling — verification at exact head

Head verified: `6ab5310d17358bc0f4c86ef09bea476b82517e3e` (PR #1812 OPEN, fetched 2026-11-27).
Method: read workflow file contents at that ref via the hosted API; no candidate changes made here.

| requirement | evidence at head |
| --- | --- |
| evidence/qualification jobs never cancel | `cancel-in-progress: true` occurrences = 0 across `ci.yml`, `targeted-integration.yml`, `supplemental-release-validation.yml`, `podman-acceptance.yml`, `targeted-demo-acceptance.yml`; all groups pair with `cancel-in-progress: false` |
| qualification concurrency keyed by resolved tested head SHA, not branch ref | `targeted-integration.yml` groups use `${{ needs.resolve_candidate.outputs.head_sha }}`; `podman-acceptance.yml` groups use `${{ needs.resolve_candidate.outputs.candidate_sha }}`; `ci.yml` groups use `github.event.pull_request.head.sha || github.sha` plus `github.run_id` |
| long Podman proof split into independently terminal hosted jobs | `podman-acceptance.yml` carries per-scenario groups (`keycloak_single_native`, `select_develop`, …) with their own run-unique groups |

Witness run `45931118156` is terminal **FAILURE** and is therefore **not** proof of the ruling; it is kept as a
witness only (never cancelled). Its failing jobs split into the four already-dispositioned classes
(`policy/actionlint` undefined `matrix.*` refs, two stale-shape test fixtures, `#183` capture defect,
Keycloak `server.key`), so the ruling is embedded in the head while the *green* proof still requires the
forward carriers `8c83c7091` (matrix refs) and `0b343af5e` (test-only fixtures), held behind #183 merge + pin advance.
