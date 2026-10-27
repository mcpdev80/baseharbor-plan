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
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/"]
---

- [x] t-20261027-r27-shadow-run · shadow-run pilot #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** coordinator-lane · **Priority:** critical  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
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

## Status 2026-10-27

- Producer run 40428162731 SUCCESS, gate `PR · Public Contracts` (PR #1094 head bd342b91, base 9a630665).
- Fixture 5ecabc1, receipt 06f25dcf, verifier live rc=0.
- Approval-dispatch run 40431294924 FAILED (dead pin + cross-repo gap).
- Activation merged via baseharbor#1095 (c11f0531); repair runs as the z2 PR.
- Proof paths: `evidence/board-2026-10-26/*` (y1, y2, y8, y9, z1).
- **Deadline:** 2026-10-29T23:35:50Z.

## Resolution 2026-10-27 (z19 planning lane, Owner mission z19)

Shadow chain complete, see `evidence/board-2026-10-26/SHADOW-RUN-RECORD.md` (root repo):
all five links proven in one genuine run — producer run 40428162731 SUCCESS, fixture
5ecabc1, receipt 06f25dcf, hosted Owner approval dispatch 40440882700 SUCCESS
(planning 8411672), retained verify rc=0. Deadline met on day 1. Accepted per
explicit Owner instruction (z19.txt); root-repo record is the authoritative
chain proof.

---

END Y2-SHADOW-RUN-PLANNED
