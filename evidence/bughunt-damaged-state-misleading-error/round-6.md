# 0427-159 r6 — round-6 evidence

Mission: `/tmp/opencode/mission-159-r6.md` (0427-159 r6 on PR #1499). Review decision: `evidence/bughunt-damaged-state-misleading-error/act-1499-review-r5.md` (KORREKTUR).

## LANE: mission-159-r6 — DONE

## TASK
r5 review held PR #1499 open with one remaining point:
- F1: repository assignment can invent ownership — `resolvedRepositoryApplication` binds a target-wide damaged orphan to the requested manifest identity without a trusted ownership basis. Fix: require an authenticated retained identity (retained ownership band) before attribution; without it => unknown owner, never the request-app/manifest.
- F2: `app_lifecycle_damaged_state_test.go` 'damaged-owned' fixture is malformed and proves nothing. Replace with an explicitly-present, production-read trustworthy ownership band and assert exact ordering. Harden foreign-orphan to assert full identity + record-only error.
- F3: drift check (develop >= b3a8042d1), rebase if needed, new terminal run on exact head.

## EXACT CANDIDATE
- Repository: `mcpdev80/baseharbor`; PR #1499; task 0427-159.
- PR head (base SHA cut from): `794ffe435e14276a88d918fd9cc5029ae1f6afc7`.
- Live develop head: `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 794ffe435e14276a88d918fd9cc5029ae1f6afc7` => exit 0 (develop is ancestor of candidate).
- Candidate chain (develop..PR head): 4 commits, all on the 0427-159 chain — `61f69c20`, `79f1a8f1`, `43fab0e5`, `794ffe435` — no foreign commit.

## BASE ATTESTATION
- Branch cut from PR head `794ffe435`; that SHA is the ancestor of every commit in this lane (verified via `git log` listing only `794ffe435..` commits).

## REPO RULE COMPLIANCE
- No `.github/**` files edited; no CI reruns or workflow_dispatch.
- Evidence committed to canonical `baseharbor-plan` (origin https://github.com/mcpdev80/baseharbor-plan.git), never to a product repo.
- No subagents (4.8); every step run in this session.
- Candidate kept on the exact PR #1499 chain; no second branch invented.

---

END in shared inbox after terminal CI verification.
