# #1578 uid-environment basis-heal — chain-heal-round-1

## Mission (coord-auftrag)
Der base-branch `lane-0428-uid-app` ist auf `22c545d82` (luna-approved). Ziel: content-merge des base-stands in `lane-0428-uid-environment`, exakt dieser head, damit ein qualifizierbare PR existiert. GRENZEN: KEIN .github/**, kein PR-merge, kein ready_for_review, kein force-push, kein retarget, kein subagent (§4.8).

## PLAN (numbered steps, §4.4)
- Step 1 — Remote truth verify: ls-remote `lane-0428-uid-app` -> `22c545d8242f8cfc2acff2a5152ab5ea4f07d170`, `lane-0428-uid-environment` -> `36c90e270a921f7bf4039e6c7d53280630fe50b6`; `merge-base --is-ancestor 22c545d82 36c90e270` -> FALSE (22c545d82 NOT ancestor of 36c90e270). Confirmed before any change.
- Step 2 — Ensure branch `lane-0428-uid-environment` is checked out (base attestation).
- Step 3 — `git merge --no-ff --no-commit origin/lane-0428-uid-app`; resolve conflicts only if declifiable.
- Step 4 — Normal merge-commit (no force/rebase/retarget); keep only product changes, never .github/**.
- Step 5 — `go build ./...` + targeted uid/environment tests.
- Step 6 — push `HEAD:refs/heads/lane-0428-uid-environment`; ls-remote witness AFTER push.

## Base attestation / branch provenance
- Product repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor`.
- Planning repo origin/main head: `e25d7dccf6dfee8ceeffacb0e7296b164c22e9ba` (verified via ls-remote before committing akte).
- Cutting branch from existing local `lane-0428-uid-environment`; remote head `36c90e270`.

## Numbered facts (measured, delivered)
- merge-base (base vs mine): `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95`
- base-stand `22c545d82` = tip of `lane-0428-uid-app`; `command_target_env.go` ABSENT there (`git rev-parse 22c545d82:cmd/baha/command_target_env.go` -> fatal: path does not exist)
- my remote head `36c90e270` = tip of `lane-0428-uid-environment`; all 6 uid files PRESENT (`command_target_env.go` blob `4a8bf930...`)
- local working branch head `7930095b0`, 2 local commits `670402fde`/`7930095b0` on an OLDER develop basis (`22c545d82` NOT an ancestor)
- `git diff 22c545d82 36c90e270 -- cmd/** internal/**`: these 6 files are ADDED by `36c90e270` (my head has them; base-stand lacks them)
- A full `git merge --no-ff --no-commit origin/lane-0428-uid-app` from `36c90e270` auto-merges cleanly but pulls 133 staged files incl. 5 `.github/workflows/**` (Owner scope) + 2 `baseharbor-plan/evidence/**` (cross-repo), and would DELETE the 6 uid files -> not a bounded basis-heal
- PR #1578 head `f353d1f736` exists, base `lane-0428-uid-app`, OPEN/DRAFT (sibling lane `cli2-uid-environment`)
- No container/compose started this shift; product repo left clean (`git checkout -- .github/`, removed stray `baseharbor-plan/`)
- push ls-remote AFTER: (none — blocked before push)

## BLOCKER (scope conflict requiring Coordinator/Owner decision)
The measured reality INVERTS the mission premise:
- My head `36c90e270` HAS all 6 uid files; base-stand `22c545d82` LACKS them (verified: `git rev-parse 22c545d82:cmd/baha/command_target_env.go` -> fatal).
- A full `git merge origin/lane-0428-uid-app` from `36c90e270` would (a) sweep 130+ unrelated files incl. Owner-scope `.github/**`, and (b) DELETE my 6 uid files — neither matches a bounded "basis-heal".
- My local branch `7930095b0` is a divergent older-basis duplicate; `22c545d82` is not an ancestor of it either.
- No bounded, declifiable path keeps head = `36c90e270` AND restores the missing uid-app content WITHOUT touching `.github/**`. QUESTION posted to Coordinator; awaiting direction.

## repo-rule compliance
- No .github/** edited (Owner scope). No PR merge, no ready_for_review, no force-push, no retarget, no subagent (§4.8).
- Evidence lives only in planning repo, never in the product repo.
- No container/compose started this shift; product repo left clean.

## Lane status
END_BLOCKED lane-0428-uid-environment (scope conflict; END_BLOCKED posted to coordinator d4212c96). Awaiting scope direction.

## Cleanup / hygiene (end-of-shift)
- Product repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor`: clean, on branch `lane-0428-uid-environment` head `7930095b0`. No in-progress merge.
- Stray `baseharbor-plan/` tree left in product repo by an earlier aborted dry-merge was removed; `.github/workflows/**` restored via `git checkout -- .github/`.
- Evidence akte committed to planning repo `baseharbor-plan` (origin/main), commit `4e4b02e3` (verified ancestor of origin/main before END).
- No containers/compose started by this lane. The 6 docker containers currently running (`bh-w169-ci-bootstrap-*`) belong to lane w169, not this lane — left untouched.
