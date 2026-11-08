---
id: t-20261108-bughunt-wizard-foreign-records
card_number: "0427-144"
card_short_title: "Foreign records stall"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w144-foreignrec
kanban_status: active
kanban_lane: active
kanban_summary: Provider resolution tolerates foreign records cleanly or reports the concrete conflict actionably; regression with two apps on…
kanban_title: 0427-144 · Foreign records stall
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md"]
---
- [ ] t-20261108-bughunt-wizard-foreign-records · Bug Hunt v0.4.27: Foreign records stall wizard #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w144-foreignrec · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w144-foreignrec  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Provider resolution tolerates foreign records cleanly or reports the concrete conflict actionably; regression with two apps on one target in the lifecycle group.

## Problem (source evidence in the dossier)
Wizard runs on a target with foreign/pending deployment records can fail provider resolution on a missing dependency (after an sql+http app, later http-only wizard cells failed on a real host target). Source: hunt H-P1 BF-06.

## Acceptance
Provider resolution tolerates foreign records cleanly or reports the concrete conflict actionably; regression with two apps on one target in the lifecycle group.

## Dependencies and file ownership
None. Write-set: internal provider resolution + deployment records.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (mapping): shares provider-resolution surface with #149/#150; fixes must state which registry layer they touch. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)
