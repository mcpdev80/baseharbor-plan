# #1801 SCOPE CORRECTION — BLOCKED, awaiting coordinator/owner decision

- sitz f0f6c8b4, lane w27-pr1627-0428-061-pull. Reviewer REQUEST CHANGES c86e07033: PR #1801 head carried 3 files, 2 outside card 0428-257 write-set (cmd/baha/app_wizard_controller.go, cmd/baha/app_edit_apply_test.go).
- m_1614_hop mission file is for PR #1614 (rotation of 043d) — stale/mismatched dispatch for my lane. Coordinator's #1801 scope correction is authoritative; continuing that.

## SCOPE CORRECTION CONTENT (DONE, verified locally)

- Restored app_wizard_controller.go + app_edit_apply_test.go to develop (f6ab22b7): they are scope-fremd for card 257.
- Moved helper funcs selectedKindAtCursor / selectedKindSelected from app_wizard_controller.go into app_edit.go (card 257 write-set).
- Re-hosted TestReview918SpaceToggleAcknowledgesOnScreen into NEW file cmd/baha/app_edit_ack_test.go (card 257 write-set).
- Added minimal catalog row source.cmd.baha.app.edit_ack.test.go (surfaces data.capabilities docker/podman) to resolve uncataloged fail-loud for the new test file. Catalog byte-valid.
- Build: go build ./cmd/baha/ => BUILD_OK. go vet => clean. TestReview918SpaceToggleAcknowledgesOnScreen => PASS.
- Diff vs develop == exactly: cmd/baha/app_edit.go (modified) + cmd/baha/app_edit_ack_test.go (new) + scripts/pr-gate-coverage.json (+1 row). .github/ untouched.
- Hop lineage preserved additively: HEAD 3a63273a2, parent 7c4d36a12, ff81c5a17 hop still ancestor. Commit message documents the correction.
- Pushed: w0428-257-0428-257-edit-toggle -> 3a63273a2. ls-remote witness done.

## DISCOVERY (blocking)

- PR #1801 was AUTO-MERGED to develop at 2026-11-23T11:02:54Z (commit b41103867, title "fix(app-edit): acknowledge space-toggle state on screen #1801"), state MERGED, draft false.
- Merge diff b41103867 vs f6ab22b7 == cmd/baha/app_edit.go + cmd/baha/app_wizard_controller.go (my helpers, +17) + cmd/baha/app_edit_apply_test.go (my test). i.e. the merge carried the scope-fremd content the reviewer flagged.
- develop now dddddbed16. My correction 3a63273a2 is NOT reachable from develop (branch already consumed by merge). b41103867 parents f6ab22b7 only.
- app_edit.go in merged develop carries my toggle-ack (count 1 via grep on app_edit.go at b41103867); helpers live in app_wizard_controller.go at b41103867 (count 2) — i.e. exactly the out-of-write-set layout the correction removes.

## BLOCKED — QUESTION POSTED

- QUESTION to 9142ab1f: PR #1801 auto-merged with scope-fremd content; write-set correction is done+verified locally at 3a63273a2 but branch already merged, cannot land on merged PR. Need coordinator/owner decision on resolution path: (a) follow-up card/PR applying 3a63273a2 as a new change, or (b) revert b41103867 then re-merge corrected.
- Did NOT self-merge, did NOT touch develop, did NOT revert, did NOT force-push. Working tree at 3a63273a2 (clean, build OK). Docker ps -a clean.

## END

END_BLOCKED w27-pr1627-0428-061-pull: #1801 scope correction content DONE+verified (3a63273a2, diff vs develop == app_edit.go + app_edit_ack_test.go only, catalog row added, .github untouched, hop lineage kept). BLOCKED: PR #1801 was auto-merged to develop b41103867 (2026-11-23T11:02:54Z) carrying the scope-fremd content the reviewer flagged; branch already consumed by merge — cannot land correction on merged PR. QUESTION posted to 9142ab1f for coordinator/owner decision on resolution path (follow-up card/PR vs revert+re-merge). No self-merge/revert/develop touch. Docker ps -a clean.
