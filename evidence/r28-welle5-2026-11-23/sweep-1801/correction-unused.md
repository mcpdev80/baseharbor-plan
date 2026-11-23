# #1801 SCOPE CORRECTION — UNLANDED (coordinator decision C: ruhen lassen)

- sitz f0f6c8b4, lane w27-pr1627-0428-061-pull. Coordinator decision on QUESTION #1801 scope: option C — ruhen lassen mit Aktenvermerk. Neither (a) follow-up PR nor (b) revert.
- Begrundung (fecb, aac6fc60b): the delta-rekord (77+/0-, purely additive deviation) was approved as FUNKTIONAL NEUTRAL. A follow-up PR that post-does the file re-housing would be churn without functional deficit (minimal-diff-pflicht); a revert of the tagged develop content even less so.

## CORRECTION WORK (DONE VERIFIED LOCALLY, NOT LANDED)

- Reviewer REQUEST CHANGES c86e07033: PR #1801 head carried 3 files, 2 outside card 0428-257 write-set (cmd/baha/app_wizard_controller.go, cmd/baha/app_edit_apply_test.go).
- What I would / did prepare:
  - Restored app_wizard_controller.go + app_edit_apply_test.go to develop (f6ab22b7): scope-fremd for card 257.
  - Moved helper funcs selectedKindAtCursor / selectedKindSelected from app_wizard_controller.go into app_edit.go (card 257 write-set).
  - Re-hosted TestReview918SpaceToggleAcknowledgesOnScreen into NEW file cmd/baha/app_edit_ack_test.go (card 257 write-set).
  - Added minimal catalog row source.cmd.baha.app.edit_ack.test.go (surfaces data.capabilities docker/podman) for the new test file (uncataloged fail-loud resolved; catalog byte-valid).
  - Build: go build ./cmd/baha/ => BUILD_OK. go vet => clean. TestReview918SpaceToggleAcknowledgesOnScreen => PASS.
  - Diff vs develop == exactly: cmd/baha/app_edit.go (modified) + cmd/baha/app_edit_ack_test.go (new) + scripts/pr-gate-coverage.json (+1 row). .github/ untouched.
  - Hop lineage preserved additively: HEAD 3a63273a2, parent 7c4d36a12, ff81c5a17 hop still ancestor.
  - Pushed: w0428-257-0428-257-edit-toggle -> 3a63273a2. ls-remote witness captured.

## WHY NOT LANDED

- PR #1801 was auto-merged to develop at 2026-11-23T11:02:54Z (commit b41103867, title "fix(app-edit): acknowledge space-toggle state on screen #1801"), state MERGED, draft false. Merge diff b41103867 vs f6ab22b7 == cmd/baha/app_edit.go + cmd/baha/app_wizard_controller.go (my helpers +17) + cmd/baha/app_edit_apply_test.go (my test).
- develop now dddddbed16. Correction 3a63273a2 NOT reachable from develop (branch already consumed by merge). b41103867 parents f6ab22b7 only.
- No follow-up PR (churn without functional deficit, minimal-diff-pflicht), no revert (tagged develop content). Work parked at 3a63273a2, working tree clean, build OK.

## CLEANLINESS

- docker BEFORE: empty (header only, 0 containers).
- docker AFTER: empty (header only, 0 containers). My pid; no docker/podman compose projects or containers started. No networks/volumes/state directories created. ambient shared infra (bh-p427 pods, baseharbor-pre-release-registry) untouched.
- No develop writes, no force-push beyond 3a63273a2, no revert, no self-merge.
