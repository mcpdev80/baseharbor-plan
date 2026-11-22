# 0428-237 RESCOPE: broker-readiness NOT reproducible on current develop; shared blocker is PR1753 footnote-admission (karte 0428-237)

Card: t-20261122-runtime-broker-health-unhealthy (0428-237)
Lane: w27-pr1627-0428-061-pull
Shift: r28-welle5-2026-11-22
Status: END_BLOCKED — chronologie change STOPPED; card returned to Owner decision (takeover by this seat or merge with 0428-227). Rescope from mission rescope237.md.tail: 0428-237 is the footnote-admission/consent scope, not the broker-chronology readiness blocker.

## PLAN

- Mission go237.md + rescope237.md.tail: go237 asked for a chronology fix in internal/controlplaneruntime/**. rescope237 rescinds that: the window-blocker is NOT the broker chronology but the footnote admission, proven from the four job witnesses (137139636770, 137139636747, 137139969524, 137139969537).
- DO: 1) STOP the chronology change — no edit to internal/controlplaneruntime/**, no PR from this mission, until a repeatable not_ready on current develop 8629450ef3c is seen. 2) Write a '## abgrenzung:' section classifying the four witnesses: which is genuine /readyz readiness vs which is consent/admission. 3) If the readiness case cannot be isolated on develop 8629450ef3c, return card 0428-237 to Owner decision.
- Limits: NO subagents, NO merge/close/comment/rerun, post only to coordinator 9142ab1f. develop 8629450ef3c5198bb675331c12f56b2c9377aa1c.
- Akte: evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-3.md with ## PLAN + ## abgrenung:.
- END: 'chronologie gestoppt: ja', four job-ids with feature-counts, card-decision sentence.

## BRANCH / BASE ATTESTATION

- branch: lane-0428-237-broker-readiness-r2, head 8629450ef3c5198bb675331c12f56b2c9377aa1c, 0 own commits (no change committed; chronologie change stopped per rescope).
- base-attestation: git ls-remote origin develop = 8629450ef3c5198bb675331c12f56b2c9377aa1c; git log --oneline -1 on branch = 8629450ef3c; git merge-base --is-ancestor 8629450ef3c origin/develop = yes.
- diff origin/develop..HEAD --name-only: empty (no own commits).

## MESSEN: THE FOUR JOB WITNESSES (all run_id 45000121766)

| job-id | engine | PR | run head_sha | conclusion |
|---|---|---|---|---|
| 137139636770 | docker | 1761 (lane-0428-231) | 669d76ac447 | failure |
| 137139636747 | podman | 1761 (lane-0428-231) | 669d76ac447 | failure |
| 137139969524 | docker | 1725 (lane-0428-231) | 669d76ac447 | failure |
| 137139969537 | podman | 1725 (lane-0428-231) | 669d76ac447 | failure |

All four run on branch lane-0428-231-static-auth-helper head 669d76ac44792a56d2642df05c5211058460b3bb. GitHub compare 8629450ef3c...669d76ac447: merge_base = acc343239681feb235a33cf00c8ea754c537291f, ahead_by 4 / behind_by 5 — the run head is FIVE COMMITS BEHIND the current develop 8629450ef3c. It is NOT on current develop HEAD.

## AGRENZUNG: feature counts per witness

| job-id | engine | not_ready | broker-readiness failed | footprint show | refusing-to-record (consent) | verdict |
|---|---|---|---|---|---|---|
| 137139636770 | docker (PR1761) | 0 | 2 | 0 | 1 (a status line, not a refusal) | GENUINE /readyz readiness: `application runtime broker readiness failed: ... container health is unhealthy`, `[WAIT] ... (2m03s)`, `[FAIL] TestApplicationCapabilityLifecycleExistingCore/secrets (150.84s)` |
| 137139636747 | podman (PR1761) | 1 | 2 | 0 | 1 | GENUINE /readyz readiness: Podman health `{"Status":"unhealthy","FailingStreak":49,...,"Output":"{\"status\":\"not_ready\"}...error: 503"}` every 5s |
| 137139969524 | docker (PR1725) | 0 | 0 | 1 | 2 | FOOTNOTE-ADMISSION: `demo-data-capabilities FAIL` -> `candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`. Secrets PASS, Runtime Resources PASS. No readiness signal. |
| 137139969537 | podman (PR1725) | 0 | 0 | 1 | 2 | FOOTNOTE-ADMISSION (same signature as 524) |

Feature counts confirm the rescope: 'readiness timeout' is NOT zero (the PR1761 pair 770/747 carries a real 503 not_ready / unhealthy 49-failing-streak), but the PR1725 pair 524/537 carries ZERO readiness and TWO consent refusals with the secrets/runtime checks itself PASSing. The blocker the PR1725 pair hits is the data-capabilities acceptance gate consent (PR1753, card 0428-227), not broker readiness.

## WHICH PART IS GENUINE READINESS

- Genuine /readyz readiness (503 not_ready, unhealthy FailingStreak=49): jobs 137139636770 (docker, PR1761) and 137139636747 (podman, PR1761). Same signature the read-only chain already found in run 44994268323 / acc343239.
- Footnote-admission / consent (the rescope's real blocker): jobs 137139969524 (docker, PR1725) and 137139969537 (podman, PR1725). Their secrets/runtime-broker checks PASS; the failure is the data-capabilities acceptance `demo-data-capabilities FAIL` -> operator/automation consent refusal. That is PR1753 (0428-227), the shared blocker another lane already hops on.

## CONSISTENCY CHECK (rescope premise vs measured evidence)

- rescope237 claim: 'readiness timeout VIER MAL NULL, not_ready GENAU EIN mal (podman 137139636747)'. Measured: not_ready count across the four = 1 (only 137139636747 podman). broker-readiness-failed marker = 4 across the four (2 per job in 770/747; 0 in 524/537). footprint show = 2 (524/537). refusing-to-record = 2 (524/537). Consistent: exactly one literal not_ready token, one job-pair (1761) carrying the genuine readiness 503.
- Decisive freshness check: run 45002730550 + 45002730537 are on current develop head 8629450ef3c and conclude SUCCESS. The readiness witnesses (45000121766, head 669d76ac447) are 5 commits older. There is NO repeatable not_ready on current develop 8629450ef3c.

## CARD FATE (decision)

0428-237 cannot be isolated as a repeatable readiness failure on current develop 8629450ef3c (current develop passes; the only 503 not_ready witnesses are 5 commits older on lane-0428-231). The reproducible window-blocker the PR1725 pair hits is the PR1753 (0428-227) data-capabilities admission consent. Card 0428-237 is returned to Owner decision: (a) takeover of the readiness-fix ownership by this seat with a fresh reproducible run on current develop, or (b) merge with 0428-227 as the shared admission blocker. No chronology change was made; no product file edited; no PR opened.

## repo-rule compliance

- Chronologie change STOPPED: NO edit, NO delete, NO write to internal/controlplaneruntime/** or any product file.
- No subagents; every step executed inside this session (AGENTS 4.8).
- No container/compose started; no bare `go test ./cmd/baha/` on the coordinator host.
- No rerun / workflow_dispatch / PR opened from this mission (Owner scope; CI is Owner-gated).
- Evidence file lives only in baseharbor-plan; no .evidence/ in the product repo.
- Evidence on origin/main verified via ls-tree (see below).

## cleanliness

- No docker/podman compose projects or lifecycle containers started by this lane.
- All API access read-only via `gh api`; logs saved to /tmp/jobinvest/ (outside the ecosystem tree). No writes to the product repo or the planning repo beyond this akte.
- Pre-existing untracked worktree dir 0428-211-hopdevelop-wt/ in the main checkout left untouched (metadata only).
- Branch lane-0428-237-broker-readiness-r2 at 8629450ef3c with 0 own commits; nothing to clean.

## END

lane: w27-pr1627-0428-061-pull
status: END_BLOCKED
chronologie gestoppt: JA — kein internal/controlplaneruntime**-Change, kein PR aus dieser Mission.
four job witnesses (run 45000121766, head 669d76ac447, 5 commits behind current develop 8629450ef3c):
- 137139636770 docker PR1761: not_ready=0, broker-readiness-failed=2, footprint show=0, consent-refusing=1 -> GENUINE /readyz readiness (503 not_ready path, FAIL secrets 150.84s).
- 137139636747 podman PR1761: not_ready=1, broker-readiness-failed=2, footprint show=0, consent-refusing=1 -> GENUINE /readyz readiness (unhealthy FailingStreak=49, 503 not_ready).
- 137139969524 docker PR1725: not_ready=0, broker-readiness-failed=0, footprint show=1, consent-refusing=2 -> FOOTNOTE-ADMISSION (demo-data-capabilities FAIL; consent --confirm-candidate; secrets/runtime PASS).
- 137139969537 podman PR1725: not_ready=0, broker-readiness-failed=0, footprint show=1, consent-refusing=2 -> FOOTNOTE-ADMISSION.
card decision: 0428-237 cannot be isolated as a repeatable readiness failure on current develop 8629450ef3c (current develop runs 45002730550/45002730537 SUCCESS); the reproducible window-blocker on PR1725 is PR1753 (0428-227) data-capabilities admission consent -> card returned to Owner decision (takeover by this seat on a fresh reproducible run, or merge with 0428-227 as the shared admission blocker).
akte remote line: evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-3.md (baseharbor-plan origin/main)
