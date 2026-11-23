# H-V35 — PR/branch liveness + supersession inventory (read-only)

Lane: w35-0428-216-hvprinv. Mission: `coordinator/missions/w35-hvpr-inventory.txt`.
Pure inventory: no product edit, no push/merge/close/comment to the product repo, no worktree created.
Distinct from H-V34 (content-landing check): this maps BRANCH/PR ANCESTRY and base-refs only.

## PLAN
1. Resolve real GitHub remotes; verify planning-repo path. DONE.
2. `git fetch --all --prune`; list every `refs/heads/lane-*` and `refs/heads/codex/*`. DONE (42 branches).
3. Measure develop head. DONE = dc8626e9c52be07a8ea5b87b468c5991b7540c4f (matches expected dc8626e9c).
4. Per-branch ancestor test + ahead-count + diff sample. DONE.
5. Open-PR cross-reference. DONE (1 OPEN: #1650).
6. Closed-unmerged v0.4.28 PRs: closedAt vs mergedAt. DONE.
7. Write evidence file. DONE (this file).
8. Push evidence to baseharbor-plan origin/main; verify path present on origin/main. PENDING (this commit).
9. Cleanliness + END post. PENDING.

## Remotes / provenance (ATTESTATION)
- Real product remote URL: `https://github.com/mcpdev80/baseharbor.git` — `origin` in the shared checkout
  `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` resolves to that github.com URL
  (`git remote -v` = `origin  https://github.com/mcpdev80/baseharbor.git`).
  All ancestry tests run against `origin/develop` after `git fetch --all --prune`.
- Planning repo (evidence lives here ONLY): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
  -> `git remote -v` = `https://github.com/mcpdev80/baseharbor-plan.git`. This is the real plan repo, NOT
  `workers/baseharbor-plan` (that path is a wrong-zone directory whose origin is the product repo).
- develop head: `git ls-remote ... refs/heads/develop` = `dc8626e9c52be07a8ea5b87b468c5991b7540c4f`.
- `git fetch --all --prune` pruned 14 stale branch refs (lane-0428-060-updown, lane-0428-061-sourcepull,
  lane-0428-208-static-release-gate-recut, lane-0428-240-broker-diagnostics, lane-0428-ingress-1623-catalog,
  lane-0428-wizard-org-default-usageerror, w0428-217credfill, w201-0428-201-statever, 0428-256-wizard-confirm-context,
  0428-ingress-wizard-catalog, 1793-fix-final-mapping, pr/1725-head, pr/1798-head + others) — those remote branches
  are now DEAD (deleted upstream), not merely unmerged.

## Branch table (lane-* and codex/*)
Classification: ANCESTOR = branch SHA is an ancestor of origin/develop (landed by SHA).
AHEAD = `git rev-list --count origin/develop..<sha>`. N = `git diff --name-only origin/develop...<sha>` file count.
"content-in-develop" note distinguishes branches whose content was merged via a different (squash/rebase) commit
from branches whose content is genuinely absent.

### Landed (SHA is ancestor of develop) — 3
| branch | sha | ancestor? | ahead | note |
| --- | --- | --- | --- | --- |
| codex/minimal-receipt-controller | 32eaaa116 | YES | 0 | receipt-controller lineage in develop |
| lane-0428-083-preserve-1665 | 24479c10 | YES | 0 | preserved 1665 content |
| lane-0428-212-loki-verify-probe-r2 | 45d181ab | YES | 0 | 0428-212 probe landed |

### Content-equivalent, no SHA ancestry — 1
| branch | sha | ancestor? | ahead | note |
| --- | --- | --- | --- | --- |
| lane-0428-063-index-carrier | 8d64f0cf | NO | 1 | empty diff vs develop; content already present. PR #1764 closed-unmerged is REDUNDANT (no content loss). |

### NOT ancestor, content live (would be lost if abandoned) — 14 codex/*
| branch | sha | ahead | N | sample files |
| --- | --- | --- | --- | --- |
| codex/broker-acceptance-consent | 4a61f3f1 | 3 | 3 | .github/workflows/runtime-broker.yml, scripts/ci-broker-typed-consent.py, scripts/test_ci_broker_typed_consent.py |
| codex/broker-docs-url | 19614e4a | 5 | 5 | runtime-broker.yml, scripts/ci-broker-docs-url.py |
| codex/broker-partial-inventory | 3458c9f8 | 5 | 8 | runtime-broker.yml, cmd/baha/application_broker_*.go |
| codex/fix-pre-release-source-db-v0427 | 893e01d5 | 6 | 2 | .github/workflows/pre-release*.yml |
| codex/fix-remote-stop-provider-consent | 687f1068 | 1 | 2 | cmd/baha/management_remote_mutation*.go |
| codex/pr-actual-base-unqualified | dc3d52d4 | 1 | 4 | .github/workflows/ci.yml, scripts/pr-diff-base.py |
| codex/receipt-evidence-hardening | d76c399e | 20 | 4 | receipt_machine_evidence.yml, receipt_merge_evidence.py |
| codex/receipt-forward-base-proof-unqualified-v1 | 9ca6723a | 1 | 6 | receipt-post-run.yml, receipt_verifier.py |
| codex/receipt-forward-controller-proof-unqualified-v1 | 752e635b | 1 | 2 | receipt_verifier.py |
| codex/receipt-machine-evidence | 3af934f8 | 1 | 2 | receipt_merge_evidence.py |
| codex/receipt-merge-minimal | b410a953 | 16 | 7 | receipt-post-run.yml, receipt_verifier.py |
| codex/receipt-v2-controller | 43aa9236 | 2 | 5 | receipt_closed_run.py, receipt_writer.py |
| codex/receipt-workflow-recovery-unqualified | afbb1da1 | 3 | 7 | receipt-post-run.yml, receipt_closed_run.py |

(notes: codex/minimal-receipt-controller is landed; the receipt-* codex branches are the r27/receipt machinery, largely superseded by develop's current CI but their scripts/ diffs are still NOT-in-develop.)

### NOT ancestor, content live — 24 lane-* (incl. #1650's branch)
| branch | sha | ancestor? | ahead | N | sample files |
| --- | --- | --- | --- | --- | --- |
| lane-0428-076-hop2 | 8225f3e6 | NO | 1 | 13 | internal/metrics/perses_dashboards*.go |
| lane-0428-078-appstatus-integration | 022c454c | NO | 28 | 18 | .github/workflows/ci.yml + 4 more |
| lane-0428-078-perses-identity | 4e81c16d | NO | 21 | 25 | cmd/baha/app_status_result.go, docs/spec/management-access-v1.md |
| **lane-0428-078-perses-identity-on-resolver** | **abf93203** | **NO** | **12** | 6 | cmd/baha/app_status_result*.go, internal/identityprovider/keycloak_*.go — HEAD of OPEN PR #1650 |
| lane-0428-078-perses-identity-on-resolver-r3 | 008354eb | NO | 38 | 25 | app_status_identity_gate_vm_test.go + 24 more |
| lane-0428-085-perses-log-trace-dash | fbffb965 | NO | 22 | 29 | app_status_result.go, management-access-v1.md |
| lane-0428-142-perses-status-backend-witness | 2b1fdcc0 | NO | 3 | 3 | cmd/baha/app_status_result*.go, perses_lifecycle.go |
| lane-0428-149-orgconfig-error-redaction | c90c3b89 | NO | 5 | 3 | internal/orgconfig/*.go |
| lane-0428-198-cli-shard-operator-env | e45430f2 | NO | 11 | 29 | cmd/baha/agent_mcp_test.go + 28 more |
| lane-0428-202-lokifix | bddb27e6 | NO | 1 | 1 | internal/logs/loki_test.go |
| lane-0428-208-static-release-gate | a2f816cb | NO | 29 | 16 | pre-release*.yml, CHANGELOG.md |
| lane-0428-209-native-cell-operator-recut | f4e340ec | NO | 1 | 2 | cmd/baha/control_plane_single_native_ci_test.go |
| lane-0428-209-native-cell-operator-seam | 0ffe0933 | NO | 15 | 31 | cmd/baha/agent_mcp_test.go + 30 more |
| lane-0428-213-trust-uninstall-false-green | 37587b0e | NO | 13 | 30 | cmd/baha/agent_mcp_test.go + 29 more |
| lane-0428-214-destroystamp-recut | 2e654a13 | NO | 1 | 1 | cmd/baha/core_installation_runtime_test.go |
| lane-0428-218-mcp-operator-seam | fb5a5dea | NO | 13 | 30 | cmd/baha/agent_mcp_test.go + 29 more |
| lane-0428-222-hopdev | 342dd1e1 | NO | 4 | 8 | internal/corebackup/etcd/*_0428_222_test.go |
| lane-0428-223-testcontext-target | aedf79f7 | NO | 7 | 8 | cmd/baha/app_init_*_test.go |
| lane-0428-227-footprint-gate-admission-rh2 | 43d85d63 | NO | 2 | 2 | cmd/baha/ci_integration_operator_enabled*.go |
| lane-0428-228-operator-seam-gate-mapping | c178412b | NO | 7 | 7 | cmd/baha/app_env_test.go + 6 more |
| lane-0428-244-core-network-owner-assertion | bfebc35e | NO | 1 | 1 | cmd/baha/operator_core_network_binding_native_test.go |
| lane-0428-efilter-r2w | 9a432502 | NO | 1 | 2 | internal/observability/envfilter_route2_test.go, registry.go |
| lane-0428-fix-bf01 | 13e096fc | NO | 8 | 6 | cmd/baha/target*.go |
| lane-hop-5ca8420c-1725c | 22087745 | NO | 11 | 3 | internal/application/shared_backends*.go |
| lane-hop-5ca8420c-dev | 5f6f3a98 | NO | 7 | 4 | cmd/baha/app_apply.go, app_workload_ports.go |

Branch totals: 42 (29 lane-*, 14 codex/*). 3 SHA-landed, 1 content-equivalent-noancestry, 38 NOT-ancestor.
Of the 38 NOT-ancestor: the live PR #1650 branch is 1; the rest are either stale superseded candidates or
abandoned-unmerged work whose content is not in develop.

## Open PRs
| PR | title | base | head ref | head sha | head ancestor of develop? |
| --- | --- | --- | --- | --- | --- |
| #1650 | fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in | develop | lane-0428-078-perses-identity-on-resolver | abf93203 | NO (12 ahead, 6 files live) |

Only #1650 is OPEN (expected ~1, confirmed). Its backing branch abf93203 is NOT-ancestor — the identity-witness
content is present in develop ONLY partially via the merged ingest #1794 (3b1fa817); #1650 still carries app_status_result
identity wiring not in develop.

## Recently closed PRs of v0.4.28 cards — merged vs closed-unmerged
Card-PR mapping (latest merged PR with mergedAt, plus latest closed-unmerged PR). "replaced" = content reached
develop via a later merged PR while an older candidate PR closed unmerged; "LOSS" = NO merged PR found carrying
that card's content, closed-unmerged = provenance-loss class.

### LOSS-class (closed-unmerged, no later merged PR found carrying the card)
| card | closed-unmerged PR | head ref | head sha | still live? |
| --- | --- | --- | --- | --- |
| 0428-085 | #1619 (2026-11-16) | lane-0428-085-perses-log-trace-dash | fbffb965 | branch live, NOT-ancestor 22/29 |
| 0428-091 | #1610 (2026-11-16) | w091-0428-091 | d57ab527 | head ref (not a lane-*/codex ref) NOT-ancestor |
| 0428-198 | #1726 (2026-11-21) | lane-0428-198-cli-shard-operator-env | e45430f2 | branch live, NOT-ancestor 11/29 |
| 0428-202 | #1732 (2026-11-21) | lane-0428-202-lokifix | bddb27e6 | branch live, NOT-ancestor 1/1 (internal/logs/loki_test.go) |
| 0428-213 | #1737 (2026-11-22) | lane-0428-213-trust-uninstall-false-green | 37587b0e | branch live, NOT-ancestor 13/30 |
| 0428-244 | #1767 (2026-11-22) | lane-0428-244-core-network-owner-assertion | bfebc35e | branch live, NOT-ancestor 1/1 |

### replaced-class (older candidate closed-unmerged, a later merged PR carries the card) — not loss
0428-053 (#1593, head ancestor, replaced by #1594), 0428-063 (#1764 empty-diff, replaced by #1623),
0428-073 (#1613, replaced by #1704), 0428-077 (#1601 ancestor, replaced by #1602), 0428-078 (#1606, ingest #1794 merged; #1650 still OPEN),
0428-079 (#1603, replaced by #1701), 0428-083 (#1684 ancestor, replaced by #1745), 0428-098 (#1669, replaced by #1664),
0428-199 (#1760, replaced by #1723), 0428-200 (#1727, replaced by #1728), 0428-201 (#1759, replaced by #1725),
0428-208 (#1746, replaced by #1805), 0428-209 (#1740, replaced by #1765), 0428-218 (#1741, replaced by #1769),
0428-242 (#1775, replaced by #1776), 0428-258 (#1806, replaced by #1804).

The "replaced" 0428 cards are accounted for: their content is in develop via the listed merged PR; the surviving
lane-* branch heads that still test NOT-ancestor (e.g. lane-0428-218, lane-0428-209, lane-0428-213-*, lane-hop-*) are
stale candidate bases that were superseded — they are NOT provenance loss, they are simply not re-based.

## cleanliness:
No worktree/stack created (read-only, no clone under /tmp). `git fetch --all --prune` mutated only the shared
checkout's refs (pruned + updated remote-tracking refs), no branch/PR changes. No container/compose project started
(docker not used); no ambient images touched. `docker ps -a` was empty at start and no test stack started here.

## fund→card note (0428-216 / 0428-221 decisions)
- 0428-216 (stale PR hops / base refs): the branch table resolves which lane-*/codex branches are ancestors vs stale.
  Landed-by-SHA: only codex/minimal-receipt-controller, lane-0428-083-preserve-1665, lane-0428-212-loki-verify-probe-r2.
  Everything else labelled "replaced" already reached develop through its listed merged PR (content present, base stale) —
  those cards can be CLOSED as landed, no re-land needed. The genuine candidates needing a decision are the LOSS-class
  six below (their content is NOT in develop).
- 0428-221 (base provenance loss): the closed-unmerged LOSS set is exactly the re-land list —
  0428-085 (fbffb965, 29 files), 0428-091 (d57ab527), 0428-198 (e45430f2, 29 files),
  0428-202 (bddb27e6, 1 file: internal/logs/loki_test.go), 0428-213 (37587b0e, 30 files),
  0428-244 (bfebc35e, 1 file: cmd/baha/operator_core_network_binding_native_test.go).
  For each, either re-land the named branch onto develop dc8626e9c, or reopen the card if content is unwanted.
  #1650 (0428-078) is the single live OPEN PR and needs a base hop onto dc8626e9c (its branch is 12 ahead).
- H-V35 inventory complete: 42 branches, develop dc8626e9c, 1 OPEN PR, 6 cards in the closed-unmerged loss class.

END_DONE hunt-hv35: develop dc8626e9c; 42 lane/codex branches inventoried (3 landed, 38 not-ancestor), 1 OPEN PR #1650, 6 cards closed-unmerged LOSS (085/091/198/202/213/244).
Candidate (planning-repo commit): cd14e2f1c.
