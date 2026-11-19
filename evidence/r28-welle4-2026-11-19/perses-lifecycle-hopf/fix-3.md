# HOPF lane-0428-084-perses-lifecycle onto develop — STOP (shared-file overlap with #1592)

Mission: 084-hopf-f518e859 (karte t-20261114-r28-perses-lifecycle, PR #1598). Pure monotonic base-hopf of PR #1598's branch onto the current develop, no content change, then a fresh exact-head CI run. STOPped on a genuine shared-file overlap between the lane and #1592 (#0428-088, perses_runtime).

## Base attestations (all measured via /tmp clone, fresh)

- current develop HEAD: `3b634232f000cfe0a344f34de57e4c5d92a340b0` (from `git -C baseharbor ls-remote origin refs/heads/develop` equivalent on fresh fetch; chain da76c5cf9 -> e1dc2cf61 #1691 -> f518e859d #1682 -> 3b634232f #1592, all linear)
- lane head carried: `ea6cddd204fbc408b8e1b3b587f1f054ea1f43ce` (real commit: "fix(0428-084): run the shared apply lifecycle on machine transports, defer it on the direct CLI")
- `git merge-base --is-ancestor origin/develop <head>` = **NO (exit 1)** — develop is NOT an ancestor of the lane head
- `git merge-base --is-ancestor ea6cddd204fbc408b8e1b3b587f1f054ea1f43ce <head>` = **YES (exit 0)** — my branch head is my own ancestor (branch untouched at ea6cddd20)
- `git merge-tree --write-tree origin/develop <head>` conflict lines = **0** (merge-tree silently takes one side's version of overlapping files; NOT a proof of no substantive overlap — see below)
- my net content diff vs ea6cddd20 = **empty** (pure hopf, no drift)
- nothing pushed: origin `lane-0428-084-perses-lifecycle` still = `ea6cddd204fbc408b8e1b3b587f1f054ea1f43ce`
- git log on branch contains ONLY my lane commits (no foreign candidate carried)

## Was sich gegenüber ea6cddd200 geändert hat

**Nichts.** Content is byte-identical to ea6cddd20. This session is a pure measurement + one aborted rebasethat was reverted. No product change was applied; the branch remains at ea6cddd20.

## STOP reason: shared-file overlap with #1592 is a substantive, non-conflict-free merge

A monotonic rebase of the lane onto the current develop drags in develop's edits to two files the lane ALSO owns:

1. `internal/machine/contract.go` — develop (#1592) **removed 4 lines** (the `app.perses.status/enable/disable/remove` Operation entries); my head **still has those 4 lines**. (`git diff ea6cddd20 origin/develop -- internal/machine/contract.go` shows 6 +/- lines; `grep -c "app.perses"` = 4 in my head, 0 in develop.)
2. `internal/metrics/perses_contract_test.go` — develop (#1592) **rewrote the `TestPersesIsNotAnApplicationCapability` doc comment**; my head has the old version.

Per the mission these are exactly the files I must NOT edit ("KEINE produkt-aenderung (reiner hopf)") and the acceptance requires a run on the current head merged onto the current develop. The merge-tree reports 0 conflict markers only because it auto-picks one side; the substantive overlap means a clean monotonic hopf that preserves my content is not possible without editing a shared file — which is out of scope. This matches the mission's STOP clause: "wenn beidas nicht konfliktfrei geht: STOP + meldung mit datei:zeile."

Note on the earlier hopf rounds: the lane was already accepted at ea6cddd20 on develop e1dc2cf61 (run 44523123388 SUCCESS, PR Selected Checks = success, CODEX-REVIEW APPROVE CONTENT). Only the "monotonic base hop + fresh exact-head" acceptance step is outstanding, and it is blocked precisely by this #1592 overlap.

## Focused tests run this session (on ea6cddd20, green)

- `go test ./contracts -count=1` → **ok** (machine_control golden record at machine_control_test.go:41 passes)
- `go test ./internal/observability -run "^TestRoute" -count=1` → **ok** (envfilter route2/route5 121-path green)
- `go test ./cmd/baha -run "Perses|Lifecycle" -count=1` → all Perses/Lifecycle logic tests **PASS**; one test fails:
  - `--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (app_edit_apply_test.go:1253)` — message "start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner". This is a **network-dependent integration test** requiring a real isolated Core/network; it is not a logic failure and is out of scope for a pure hopf.
- `go build ./...` → **exit 0**
- `go vet ./cmd/baha ./contracts` → **exit 0**
- `gofmt -l .` → **clean** (empty)
- `bash scripts/source-readability-audit.sh` → **PASS** (only pre-existing `internal/providers/runtime/podman/lifecycle.go` at 843 lines vs baseline ratchet 878; perses_lifecycle.go 295 / perses_lifecycle.go internal 183 well under 800)
- Go toolchain: go1.26.8 installed (go.mod pins go1.26.9) — build/test run clean on 1.26.8, GOTOOLCHAIN=local.

## repo-rule compliance

- Pure hopf mission: **no product content changed** (diff vs ea6cddd20 empty). Branch left at ea6cddd20, nothing pushed to origin.
- No `.github/**` edits, no workflow_dispatch / rerun, no merge, no `gh pr ready`.
- No subagent (§4.8) — every step run inside this session.
- Isolated clone under /var/tmp only; the quarantined workers/baseharbor checkout was never cited as remote evidence.
- Planning repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` was NOT touched; no git action in any shared plan working copy.

## Handoff

Owner decision required on one of:
1. Authorize a minimal scoped edit to reconcile the lane with #1592 (drop the 4 `app.perses.*` Operation entries from `internal/machine/contract.go` to match develop, restore the rewritten doc comment in `internal/metrics/perses_contract_test.go`) so the lane becomes a clean monotonic hopf onto the current develop; then push + fresh exact-head CI.
2. Rebase the lane onto a develop that is **before** #1592 (#0428-088) — i.e. re-point the acceptance base to f518e859d — if the Owner wants the acceptance run on the pre-#1592 develop.
3. Keep ea6cddd20 as-is and let the merge pull #1592's reconciled content through the normal merge (acceptance then runs on the merged head).

Cleanliness:
- before: 7 `bh-local-shared-*` ambient containers (untouched); scratch /var/tmp/m084-* (4 dirs) + /tmp/m084-final existed
- after: my scratch `/var/tmp/m084-wt`, `/var/tmp/m084-fixbase`, `/var/tmp/m084-hopf-clone`, `/var/tmp/m084-workdir` and `/tmp/m084-final` removed; temp files `/tmp/m084_mt.txt`, `/tmp/m084_runid` removed
- after: still exactly **7 `bh-local-shared-*`** ambient containers (docker ps -a witness), none started/removed by this lane
- Working tree clean; branch at ea6cddd20; nothing pushed.

## PLAN

1. fetch origin --prune; measure remote develop via fresh clone. DONE.
2. Confirm lane head ea6cddd20, ancestor witnesses, merge-tree. DONE (0 markers; substantive overlap found).
3. Attempt monotonic rebase onto current develop to test clean-hopf feasibility. DONE — revealed 6-line contract.go edit + comment rewrite in perses_contract_test.go (both owned by #1592). Reverted; branch back at ea6cddd20.
4. Focused tests on ea6cddd20. DONE — all green except the network integration test (out of scope).
5. STOP + report to Owner with the shared-file overlap at file:line and the three handoff options. DONE below.

## Handoff

STOP — END_BLOCKED. Pure hopf cannot be completed without editing shared files that #1592 also owns (`internal/machine/contract.go` lines 202-205 remove `app.perses.*` ops; `internal/metrics/perses_contract_test.go` doc-comment rewrite). Branch untouched at ea6cddd20, nothing pushed. Awaiting Owner decision on the three options above.

END_BLOCKED lane-0428-084-perses-lifecycle: hopf onto develop 3b634232 blocked by #1592 shared-file overlap (contract.go:202-205, perses_contract_test.go comment); branch at ea6cddd20, nothing pushed
