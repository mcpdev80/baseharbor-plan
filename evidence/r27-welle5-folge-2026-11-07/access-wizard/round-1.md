# Plan — 0427-access-wizard (card t-20261018-r27-access-wizard, 0427-013)

## Context
Task: guide profile assignment and deliberate offboarding of a person on a target.
Fail-closed on incomplete configuration. Acceptance text (word-for-word, card):
"Name->search/select Targets->rights->review; preserve selections across pagination/back,
show effective scope. Distinguish connection removal, device revoke, owned grant removal and
explicit managed-user disable/delete. Authorization/current-state recheck, offline/empty/
no-match feedback; no remote installation deletion from local cleanup."

Bounded write reservations (from card): bounded team profile/user/device removal wizard
adapters/tests; NO onboarding wizard file writes. Predecessor interfaces (accepted):
access-profiles (0427-011, PR #1384) = orgconfig.Manager + policy.Adapter; managed-users
(0427-035) and device-lifecycle (0427-027) siblings.

## Base attestation
- Base ref: origin/develop
- Base SHA: c8a79faff91cd870ac3904a2a392922a24cc7e13
- Branch: work/r27-access-wizard, cut from c8a79faff
- Ancestor check: `git log --oneline origin/develop..HEAD` empty at cut (only my own commits after); c8a79faff is an ancestor of HEAD.
- Isolated worktree: /tmp/opencode/0427-access-wizard-wt

## Steps
- Read mission, card contract, predecessor interfaces, repo rules; claim task
- Verify base SHA (origin/develop c8a79faff) as ancestor, cut isolated branch
- Design wizard domain model + fail-closed config checks against card acceptance
- Implement profile-assignment wizard (name->Targets->rights->review) + onboard/offboard path
- Wire the CLI command into the app command tree (owned path)
- Implement positive/negative regression tests (duplicate/large lists, cancel/EOF/stale/denied/offline)
- Wire tests into existing CI group; report needed .github change as finding (Owner scope)
- Local test pass, build, vet; host PR-check on final SHA (self-run, terminal watch)
- Commit evidence to planning repo (origin/main), publish handoff, END

## Scope / write-set boundaries
- Owned: new wizard adapters under cmd/baha + a bounded internal package for the access-wizard flow.
- MUST NOT touch: .github/** (Owner), scripts/*-CI (021), cmd/baha/app_remote_lifecycle.go (116),
  client_commands_behaviors/core_integration (022), broker/controlplaneruntime/source_oci (118).
- No onboarding wizard file writes (card reservation).

## Acceptance criteria (from card)
- Profile assignment wizard: name -> search/select Targets -> rights -> review.
- Preserve selections across pagination/back; show effective scope.
- Distinguish: connection removal, device revoke, owned grant removal, explicit managed-user delete.
- Authorization/current-state recheck; offline/empty/no-match feedback.
- No remote installation deletion from local cleanup.
- Fail-closed on incomplete configuration.
- Executable positive/negative regressions.

## Evidence
- Evidence file (planning repo, origin/main): evidence/r27-welle5-folge-2026-11-07/access-wizard/round-1.md
