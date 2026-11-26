# 0428-358 card authoring record

ROLLE: AUTHOR | lane: w267-0428-284-pridentity

## PLAN

1. DONE — Refresh coordinator checks and read current plan main, card rules, and publication requirements.
2. DONE — Verify PR #116 head `02870bdc6884cbc199b36efb951f883caf6eccd1` and inspect the H-V33 census evidence.
3. DONE — Decide one new card for the two Medium findings; classify the mitigated zsh/fish and HA-gated etcdctl findings as no tracking.
4. DONE — Post the no-tracking disposition on PR #116 (comment 7190917653).
5. DONE — Author task 0428-358 from the exact findings and preserve the `.github/**` owner boundary.
6. DONE — Render the generated planning views and validate the plan data.
7. PENDING — Publish the final card/evidence head and verify its Hosted Plan validation run reaches terminal success.
8. PENDING — Hand the final exact head to an independent Codex reviewer; do not accept or merge this lane's card.

## Disposition

Create one task for the two Medium H-V33 findings: OpenSSL availability for the Keycloak database-reload runtime path (source akte lines 123-127) and `podman-system-generator` availability for Podman Quadlet runtime cells (lines 129-132). The task is 0428-358, `t-20261126-runner-openssl-podman-generator.md`.

Do not track the mitigated zsh/fish Finding #1 (lines 163-168) or the HA-gated, path-pinned etcdctl Finding #4 (lines 134 and 161). The no-tracking decision is recorded on PR #116.

Source census: [PR #116 akte at reviewed commit](https://github.com/mcpdev80/baseharbor-plan/blob/02870bdc6884cbc199b36efb951f883caf6eccd1/evidence/2026-11-26/w317-0428-352-huntv33/akte.md).

## Publication

- Card author and commit author/committer: `w267-0428-284-pridentity`.
- Planning PR: #120.
- Initial task-only candidate: `91db8032b2e6725ed4e6762b23c5876b8e28aa19`.
- Initial Hosted Plan validation run: 45812645717 (attempt 1, success on the initial candidate; superseded when this evidence file is added).
- Reviewer boundary: the author does not accept or merge this card; an independent Codex lane must review the final head and its exact-head validation.
