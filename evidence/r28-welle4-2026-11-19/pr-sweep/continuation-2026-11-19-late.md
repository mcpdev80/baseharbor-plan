# Open PR sweep continuation — 2026-11-19 late

Maintainer-directed sweep note. These are point-in-time findings; refresh GitHub, plan and Codeman before any subsequent action. This note does not accept a product task or change task scope.

## Live inventory and Codeman boundary

- GitHub search at 2026-11-19 22:03 UTC returned 27 open PRs: #1704, #1702, #1695, #1693, #1690, #1684, #1665, #1650, #1645, #1627, #1625, #1623, #1620, #1615, #1614, #1606, #1597, #1596, #1595, #1594, #1591, #1588, #1587, #1585, #1582, #1580, #1578.
- Read-only Codeman observation at 22:05 UTC: coordinator 9142ab1f; all five worker seats busy. Active writes: #1693 (`internal/metrics/prometheus_files.go`, `prometheus_render.go`, regression test); #1684 (Perses datasource / application / service-access paths); 0428-151 provider registry retention + tests; #1690 provider consent authority + tests; #1697 planning witness closeout. The #1702 separate review session is editing its plan evidence; do not touch its card or worktree. No Codeman messages or mutations were made.

## PR #1704 / card 0428-073

- Exact head `f5dcf12885489d8b8beb8a57720d659f4b737378`, base `develop` at `28fb427f057499efca705c1b7459e7653bd532a8`, PR workflow run `44621875256` terminal SUCCESS. Independent review confirms r28 fixed the earlier selected/unselected wording and guard findings.
- Acceptance is still unmet: `persesAlertRealEvaluatorContractPresent()` remains permanently false; no rule evaluation or persistence and no production caller exists. Task 0428-073 requires a real evaluator and notification owner unless the Owner explicitly revises that acceptance. Dependency 0428-083 remains open. A follow-up task is not a waiver.
- Formal REQUEST_CHANGES review is prohibited by GitHub because the authenticated Maintainer account is also the PR author. A top-level PR comment (issue-comment id `7023558377`) records the exact blocker and requested implementation/Owner decision. No merge was attempted.

## PR #1702 / card 0428-142

- Exact head `6740299f91c040af7b1357d63be898eac57669f5`, run `44621032956` terminal SUCCESS on the PR head; `PR Selected Checks` succeeded. The PR has no current formal review decision, and later `develop` advanced to `4b3a3559070e9b81b1886a357f6a46bc6dfce790`, leaving the PR behind.
- SHA-exact independent review evidence is `../codex-review-wave/1702-0428-142-r4.md` (published on plan main `97e92302`). Findings: backend states are inferred only from manifest flags; `unreachable` is declared but never emitted; tests lack per-backend match/no-match/error evidence and full text/JSON tuple parity; out-of-scope capability/runtime files are included; the run evidence file misstates skipped jobs and lacks reproducible gate-plan comparison/cleanliness entry. Review verdict: REQUEST CHANGES. Do not merge.
- The reviewer session is independently recording the finding. Do not edit its worktree or card. The related 0428-152 caller task waits on #1702 and must not overlap its `cmd/baha/app_status_collect.go` change.

## CLI2 branch routing

- #1615 exact head remains `f93564a0d707983bfe6a8b59375c1c1c914d7827`, with no exact-head PR run. Current PR refs: #1594 head `cli2-env-policy-head`; #1615/#1620/#1627 base that branch; #1615 head `cli2-identity-secrets-head`; #1623/#1625 base that second branch.
- The previously authorized `cli2-*` to `lane-*` branch rename is not safe to execute yet: canonical card 0428-053 is active under Coordinator ownership, while 0428-054 and the upstream UID chain remain in wait/frost sequencing. Renaming a branch that is the live 0428-053 basis would interfere with that stack. A base edit alone also is not a configured `pull_request` trigger. No refs or PR metadata were changed.

## Disposition

No PR merge/close occurred in this continuation. Keep #1704 and #1702 open for their acceptance blockers and their assigned follow-up. Continue on a live, disjoint task when one is available; keep monitoring the Codeman pool read-only and refresh the inventory before each mutation.
