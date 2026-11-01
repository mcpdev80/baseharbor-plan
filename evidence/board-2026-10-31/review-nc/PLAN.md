# PLAN — review-nc (Review PR #17 node-connector)

- Task-ID / Mission: review-nc (read-only review of node-connector PR #17)
- Session/Modell: worker-ornith1.5 / agentgateway (read-only review)
- Datum: 2026-11-01

## Steps

- [ ] Step 0: Setup todo + evidence file
- [ ] Step 1: Fetch PR #17 diff (source.yml + release-integration.yml) via gh
- [ ] Step 2: Check rootless/loginctl pre-treatment removed vs. rootful Podman (not just diagnostic echo)
- [ ] Step 3: No gate weakened / SKIP / test deletion / runs-on self-hosted remaining
- [ ] Step 4: Fail-closed check — job aborts visibly != 0 when Podman can't run rootful/cgroupfs; "Actual encrypted transport · podman" is real, not SKIP
- [ ] Step 5: Write-set disjoint from baseharbor/*; nc-AGENTS repo rules
- [ ] Step 6: Write REVIEW.md verdict + ROLL:REVIEW + Session/Modell/Zeit

## Evidence locations
- /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-10-31/review-nc/REVIEW.md

## STOP criteria
- Any evidence of weakened gate, SKIP, self-hosted runs-on, or leftover rootless path failing on GH-hosted => CHANGES with file/line/Stop-Kriterium.
