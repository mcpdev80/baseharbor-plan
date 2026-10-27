---
id: t-20261027-r27-shadow-run
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: coordinator-lane
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/"]
---

- [ ] t-20261027-r27-shadow-run · shadow-run pilot #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** coordinator-lane · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** coordinator-lane  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Schattenlauf: Producer CI run + writer + Owner-approve + tasklink + retained verify

### Ziel
EIN vollständiger Schattenlauf des v0.4.27 Receipt-Pipelines durchspielen:
1. **Producer CI run** — Auslösen des receipt-producer Workflows gegen develop
2. **Writer** — receipt_writer.py persistiert ein receipt JSON
3. **Owner-approve** — receipt-approval.yml authentifiziert und approved
4. **Tasklink** — automatische task reference im Planning-commit
5. **Retained verify** — receipt_verifier.py verifiziert Git-Ancestry und approval-Edit

### Write-Set
- `evidence/receipts/**` — receipt JSON Artefakte
- Handoff-Dokumentation

### Abhängigkeiten
- PR1 (#1090) merged: TRUE (content via PR2 squash auf develop)
- PR2 (#1091) merged: TRUE
- Merged-Commit-Referenz: 9a630665

### Deadline-Referenz
`2026-10-29T23:35:50Z`

### Akzeptanzkriterien
Alle 5 Kettenglieder in GitHub/Planning verifizierbar:
1. Producer CI run completed with SUCCESS
2. Writer persisted receipt JSON to evidence/receipts/
3. Owner-approve authenticated and approved
4. Tasklink auto-generated in Planning commit
5. Retained verify passed Git ancestry check

### Evidence-Pfade
- receipt JSON: `evidence/receipts/<gate>/<run>-<attempt>.json`
- CI run logs: GitHub Actions run history
- Tasklink: Planning commit diff

---

END Y2-SHADOW-RUN-PLANNED
