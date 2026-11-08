# 0427-136 app init Owner-Naht — native-hosted gate round-3

**Task:** t-20261108-bughunt-0427-appinit-owner-seam (karte 0427-136)
**Lane:** w136-appinit-r3
**Branch:** fix/0427-136-appinit-owner-seam (PR #1458)
**PR:** #1458 vs develop (base d30de3a4)
**Host:** this shared codeman host (coordinator server) — NO container/compose runs here
**Evidence dir:** `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-appinit-owner-seam/round-3.md`

## PLAN

- Fetch develop (d30de3a4), verify remote truth via ls-remote; confirm PR#1458 head and 1463 merged state.
- Drift-merge latest develop into PR#1458 branch (base now d30de3a4, contains 1453-merge); keep PR#1458 ready; verify exact head sits on new base.
- Watch the hosted native docker + podman jobs on the scripts/ci-native-installation-destroy.sh path on the EXACT head to terminal state, capture run-ids + PASS.
- Record run-ids + PASS in round-3.md.
- ls-remote witness; publish evidence to origin/main; bring down any compose projects; post END.

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`, PR #1458.
- develop head (base for this lane, refreshed): `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064` (`git ls-remote ... refs/heads/develop`).
- Owner PR #1463 merged to develop at `88acebc5` (develop now d30de3a4).
- PR #1458 head: `5c5e24a7cdfe74329f7d32c6fb84a26ce2b64e4b` (not a draft; base develop).
- CI path: docker-runtime-acceptance.yml `single_default_native` job runs `scripts/ci-native-installation-destroy.sh` -> `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` with `BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1`.
- Planning repo used: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (commit directly to main; no branches). origin/main HEAD: `449437cd7a4f18af56318beb27b942c84ca64503`.

## BLOCKER (Owner Sperr-Hinweis 2026-11-08 ~10:2x)

- NATIVE BUILD ERROR on develop: the native test build has a defect identified by the Owner. Fix is being handled in PR #1464 (headRefName test/0427-ready-native-proof, head 8e0ad76e; still OPEN).
- CONSEQUENCE: do NOT drive the drift-merge / PR #1458 onto develop until develop contains PR #1464.
- ACTION: short polling checks only (NOT a busy-wait loop) — every few minutes: `git fetch origin develop` then `git log -1 origin/develop`, until the #1464 fix commit appears on develop. This lane is the only active verification lane, so short pruef-polls are explicitly acceptable here.
- State before block: drift-merge performed LOCALLY to HEAD `837585139` (base d30de3a4). Builds clean (`go build ./cmd/baha` exit 0; `go vet ./cmd/baha/` exit 0). NOT pushed (remote PR branch rejected as non-fast-forward and remains at 5c5e24a7). PR #1458 still OPEN, not draft, base develop, head 5c5e24a7.
- Background poll `/tmp/opencode/poll-1464.sh` running (checks every 3 min, exits when origin/develop advances beyond d30de3a4; log at /tmp/opencode/poll-1464.log). Will wake on advance.
- Once develop includes the #1464 fix: re-verify `scripts/ci-single-default-impact.sh` still selects our test file (required=true) against the NEW develop head; if not, that is an Owner-side CI-selector finding (do not edit). Then re-perform drift-merge of the CURRENT develop head into fix/0427-136-appinit-owner-seam, push (fast-forward), verify PR #1458 head reflects new base, then run + watch the hosted native docker+podman jobs on scripts/ci-native-installation-destroy.sh to terminal state (run-ids + PASS), record in round-3.md.

## Scope finding (Owner scope, do NOT edit)

- PR #1464 (`test/0427-ready-native-proof`, head 8e0ad76e) also changes `scripts/test-ci-impact-selectors.sh:33` (adds `cmd/baha/runtime_destroy_all.go` to the selector coverage test). That is a CI-group/Owner-scope file. Per AGENTS §5.3 I must NOT edit it; reported here as a finding.
- My scope is `scripts/ci-single-default-impact.sh` only. PR #1464 does NOT touch that trigger selector (verified: `git diff d30de3a4 8e0ad76e -- scripts/ci-single-default-impact.sh` is empty). After develop includes #1464, the drift-merge of PR #1458 must re-verify `scripts/ci-single-default-impact.sh` still selects our test file (required=true) against the NEW develop head. If it does not, that is an Owner-side CI-selector finding, not something I edit.

## End state (block recorded 2026-11-08 ~10:3x)

- This lane is BLOCKED on the Owner's external PR #1464 (native test build fix). develop is still at `d30de3a4` (no #1464). The drift-merge of PR #1458 is done LOCALLY but must NOT be pushed until develop includes #1464.
- Background poll `/tmp/opencode/poll-1464.sh` (every 3 min) will wake this lane if/when origin/develop advances.
- No compose/container projects running on this host (host check: 0 docker, 0 podman).
- Repo-rule compliance: no product seam change, no `.github/**` edit, no CI rerun/dispatch, no push of the drifted PR branch. The only Owner-scope file touched by #1464 is `scripts/test-ci-impact-selectors.sh:33`, which I did NOT edit (reported as a finding).
- No Markdown checkbox task lines anywhere in this file (plain bullets only).
- Evidence written to baseharbor-plan (planning repo, origin/main), never a product repo.

- round-1: root-caused the regression (one-installation-owner seam `VerifyDeploymentOwner` fails on a fresh `--reference local` target before any Core bootstrap). Fix route B: bootstrap genuine Core via `baha up --control-plane-only` in the native acceptance test. Committed (7536878d), PR #1458.
- CODEX-REVIEW (act-1458-review.md): verdict KORREKTUR — the test-only change does not currently select the native acceptance gate (CI impact selector `scripts/ci-single-default-impact.sh:7` has no match for the test file -> `required=false` -> test skipped). Stop criterion: the documented Core bootstrap + app-init/destroy-retry acceptance must execute and PASS in the hosted native acceptance gate on the exact candidate SHA.

## Repo-rule compliance

- No product seam change, no .github/** edit, no workflow edit/dispatch. Hosted CI jobs only observed to terminal.
- No Markdown checkbox task lines anywhere in this file (plain bullets only).
