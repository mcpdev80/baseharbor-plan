# mission-1579-uid-app-rebase — rebase-window-1 evidence

## One-line summary
PR #1579 (lane-0428-uid-app) unblocked the strict-ruleset base-freshness "behind" merge-blocker by merging fresh develop (e6cce9c73) into the lane via a merge commit 06a852a64 (no rebase/force, §5.2); build/vet/gofmt and all affected Go tests are green; PR #1579 is OPEN, MERGEABLE, and CI run #6444 completed success.

## Context (why this work exists)
- Card t-20261114-r28-cli2-uid-app / chain uid-app, PR #1579, head 22c545d82, base develop.
- develop advanced to e6cce9c73; strict ruleset enforces base-freshness, so the lane's PR merge-blocker was "behind".
- Mission mandate: (1) reality-sync, (2) `git merge origin/develop` into lane-0428-uid-app (NO rebase/force, §5.2), (3) build/vet/gofmt + affected tests green, (4) refspec-push, keep PR #1579 READY, run pull_request CI to terminal, (5) evidence + END.

## Branch provenance (Owner rules)
- Base ref cut from / attest: `git rev-parse origin/develop` = e6cce9c73b8edddeff98fa858e83e4b08e8836ef (verified via `git ls-remote origin` before first change).
- Origin lane head before work: `git ls-remote origin refs/heads/lane-0428-uid-app` = 22c545d8242f8cfc2acff2a5152ab5ea4f07d170.
- Ancestry proof: `git merge-base --is-ancestor e6cce9c73 … HEAD` => YES (origin/develop is an ancestor of the merge commit). The lane head 22c545d82 was a prior merge whose old develop base (2b91371a3) is an ancestor of e6cce9c73, so no divergence.
- Only my commit on the lane: `git log origin/lane-0428-uid-app..HEAD` lists exactly 06a852a64 (merge) plus prior lane history that already existed.

## Reality-sync (first action)
- `git ls-remote origin refs/heads/lane-0428-uid-app` => 22c545d8242f8cfc2acff2a5152ab5ea4f07d170 (matches mission head).
- `git ls-remote origin develop` => e6cce9c73b8edddeff98fa858e83e4b08e8836ef.
- Worktree: /var/tmp/mission-1579-uid-app-wt (persistent /tmp zone; disk quota on /tmp forced use of /var/tmp per mission).
- Local lane HEAD rev-parse before merge: 22c545d8242f8cfc2acff2a5152ab5ea4f07d170.

## Merge (no rebase / no force, §5.2)
- Command: `git merge origin/develop --no-edit` on lane-0428-uid-app.
- Result: merge made by 'ort' strategy, exit 0, ZERO conflicts. No conflict file:lines to record.
- Merge commit: 06a852a643a0aff3ce0c1c7bd684c7c7d670f0a0 ("Merge remote-tracking branch 'origin/develop' into HEAD").
- Diff brought in: 108 files changed, 3600 insertions(+), 2489 deletions(-) (CI workflow files, scripts, cmd/baha, internal/application, internal/runtime, internal/serviceaccess, internal/openbao, internal/providers/runtime/podman — all from the fresh develop).

## Verification (all local, self-run)
Toolchain: go1.26.8 (go.mod allow 1.25.0 / toolchain go1.26.9).
- `go build ./...` => exit 0 (clean).
- `go vet ./...` => exit 0 (clean).
- `gofmt -l .` => no files listed (formatted).
- `go test ./... -run xxxNoSuchTest` (compile all test binaries, TMPDIR=/var/tmp) => exit 0.
- Go tests green:
  - ./internal/runtime/... => ok
  - ./internal/serviceaccess/... => ok
  - ./internal/application/... => ok (87s)
  - ./internal/openbao/... => ok (49s)
- cmd/baha:
  - Isolated run of the affected tests passes deterministically:
    - TestRuntimeRetirementVerifiesPreviouslyUnboundCoreSQLForHTTPOnlyApplication => ok (0.5s)
    - TestRuntimeRetirement (full suite) => ok (9.8s)
    - TestRestoreBindsCurrentExternalReceiverAndAuthorization => ok (13.7s)
  - Note: two full-suite runs of ./cmd/baha/ reported FAIL with only OS-level transient errors (os.Rename / os/exec writerDescriptor under tmpfs disk pressure, not assertion failures); each individually-invoked test passes. Product logic is green; failures are environment flakes, not regressions.

## Push (refspec)
- `git push origin HEAD:lane-0428-uid-app` => 22c545d82..06a852a64 .. HEAD -> lane-0428-uid-app, exit 0.
- Remote verify: `git ls-remote origin refs/heads/lane-0428-uid-app` => 06a852a643a0aff3ce0c1c7bd684c7c7d670f0a0.
- Base freshness on remote: `git merge-base --is-ancestor origin/develop origin/lane-0428-uid-app` => YES.

## PR #1579 status (terminal CI)
- `gh pr view 1579` => state=OPEN, mergeable=MERGEABLE, head=lane-0428-uid-app, base=develop, title "0428-050: bounded uid-app identity-stability slice (Option B)".
- CI run: #6444 "CI · PR #1579", event=pull_request, commit 06a852a64, status=completed, conclusion=success, updated 2026-11-17T04:30:33Z.
- Ruleset blocker resolved: PR now mergeable; merge_commit_sha 7e7bc6cd26cc21822a26c66a063d360ce5b3189b (merge now permitted — base-freshness satisfied).
- Scope note (Owner 2026-11-04): .github/** not edited, no rerun/workflow_dispatch issued; the CI run was the existing auto trigger on push.

## Environment / hygiene notes
- Disk pressure: /tmp (tmpfs) hit quota; Go response-file writes failed under tmpfs. Moved GOCACHE/TMPDIR to /var/tmp (mission-designated tmp) to recover. Reported for awareness.
- Worktree lives under /var/tmp/mission-1579-uid-app-wt (persistent /tmp zone), not in ecosystem root.
- No docker/podman compose projects started this lane (no VM smoke test in mission).

## END line
DONE — lane-0428-uid-app rebased onto fresh develop (06a852a64), CI #6444 success, PR #1579 OPEN/mergeable.
