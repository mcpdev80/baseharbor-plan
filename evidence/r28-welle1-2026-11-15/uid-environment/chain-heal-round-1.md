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

## Numbered facts (measured + delivered)
- merge-base (36c90e270 vs 22c545d82): `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95` (both develop-synced; coordinator-measured)
- side-branch commits brought by base-stand from 14d8f17d: `2b91371a` (race store Create single-owner convergence), `18b0ebc9` (fix concurrent uid-app test CWD race), `2bf0c929`, `c0664c8e`
- base-stand `22c545d82` tip of `lane-0428-uid-app`; `command_target_env.go` ABSENT there (rev-parse fatal)
- my HEAD `36c90e270` tip of `lane-0428-uid-environment`; all 6 uid files present at 36c90e270
- FRESH CLONE (coordinator NEW ARBEITSBAUM decision): `git clone -b lane-0428-uid-environment origin` in `/var/tmp/uidenv-heal-wt/fresh-uidenv`; first action verified HEAD == `36c90e270a921f7bf4039e6c7d53280630fe50b6` via ls-remote witness (NOT the old divergent local 7930095b0)
- MERGE-COMMIT: `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283` (normal merge-commit, no force/rebase/retarget)
- NEW HEAD after push: `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283` (confirmed via ls-remote AFTER push)
- PROVENANCE: `36c90e270` IS ancestor of `9c5bc09a` (merge-base --is-ancestor verified)
- CONTENT DIFF 36c90e270..9c5bc09a: EXACTLY 1 file `cmd/baha/app_init_uid_app_slice_test.go` modified; .github/** touches = 0
- go build ./... -> exit 0
- go vet ./cmd/baha/ -> exit 0
- race test `TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner` (+ all UIDApp/ConcurrentFirstCreate) -race -> ok 1.701s
- broader `./internal/environment/... ./internal/deployment/...` -> ok (0.002s / 0.882s)
- push refspec `origin HEAD:refs/heads/lane-0428-uid-environment`: `36c90e27..9c5bc09a` (exit 0; remote dependabot notice is informational, not a gate)
- ls-remote AFTER push: `lane-0428-uid-environment -> 9c5bc09a...`, `lane-0428-uid-app -> 22c545d82...`
- No container/compose started this shift; fresh clone only (git, no docker/podman)

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
END_DONE lane-0428-uid-environment. Candidate head `9c5bc09a` pushed and ls-remote-witnessed. END posted to coordinator d4212c96.

## Cleanup / hygiene (end-of-shift)
- Fresh clone at `/var/tmp/uidenv-heal-wt/fresh-uidenv` (git only; no docker/podman). /tmpfs clone hit a disk quota, moved to /var/tmp (sda1, 26G free) per mission guidance.
- Evidence akte committed to planning repo `baseharbor-plan` (origin/main): round-1 (4e4b02e3) + cleanup/hygiene note (7c77927b); both verified ancestor of origin/main before END.
- Product repo was NOT touched this shift (fresh clone only) — no dirty state to clean.

## BLOCKER (superseded by coordinator NEW ARBEITSBAUM decision)
The earlier END_BLOCKED was based on the WRONG local checkout (7930095b0, a divergent older-basis duplicate). Coordinator measured at the hub: merge-base(36c90e270, 22c545d82)=14d8f17d (both develop-synced); base-stand delta from 14d8f17d is small and .github-free; a merge into the ECHTEN head (36c90e270) sweeps NO 130 files. The correct path was a fresh clone into a new directory, verifying HEAD==36c90e270 first. Executed per the NEW decision.
