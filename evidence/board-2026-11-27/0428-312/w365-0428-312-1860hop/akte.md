# w365-0428-312-1860hop — Re-Hop + Qualifikation (0428-312, PR #1860, baseharbor)

**Card:** 0428-312 (hunt39 H-V39/F4: assert workload volumes in recovery manifest)
**PR:** #1860  **Repo:** baseharbor  **Branch head:** `w333-0428-312-volrecovery`
**Lane (canonical):** `w365-0428-312-1860hop`
**Mission:** `coordinator/missions/w365-0428-312-1860hop.txt`

## VISIBLE ANSATZ BLOCK (Owner directive, attested)

- Owner (verbatim, fetched from origin/main at runtime) — mission w365-0428-312-1860hop:
  "Re-Hop + Qualifikation auf existing Karte. KEIN Merge, keine neue Karte, single writer."
- git user.name I will use: `w365-0428-312-1860hop`
- git user.email I will use: `w365-0428-312-1860hop@users.noreply.github.com`
- literal git commit invocation: `git -c user.name=w365-0428-312-1860hop -c user.email=w365-0428-312-1860hop@users.noreply.github.com commit ...`
- pre-push gate line: `git show -s --format=%an HEAD` must equal exactly `w365-0428-312-1860hop`

## REALITY WITNESSES

- baseharbor remote (github): `https://github.com/mcpdev80/baseharbor.git`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `c167fa5dd323ae0746385caa2bdb8364ec7ad03f`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1860/head` = `6deab9ff68d15060525cc3078e828027e65e9955`
- `gh pr view 1860 --repo mcpdev80/baseharbor`: base=develop, headRefName=`w333-0428-312-volrecovery`, headRefOid=`6deab9ff…`, state=OPEN, isDraft=false
- Last exact-Head-Run 45839805123 (head 6deab9ff): FAILURE (Trusted Plan + PR Selected Checks)

## PR #1860 SCOPE

Two-source PR on head `6deab9ff` (base 5a37ddbd):
- `internal/applicationbackup/recovery_manifest_workload_test.go` (new fail-closed workload-volume recovery-manifest assertion)
- `scripts/pr-gate-coverage.json` (catalog entry for the new source; id corrected to `source.internal_applicationbackup_recovery_manifest_workload_test_go`, path `internal/applicationbackup/recovery_manifest_workload_test.go`, surfaces `source.gate.atomic.docker.data.capabilities` + `source.gate.atomic.podman.data.capabilities`, runtime_specific=true)

Four commits on the branch (fa16643a → 514d827c → f877febb → 6deab9ff): repeated attempts to fix the catalog id/path; final commit corrected the path from `internal/application/backup/...` to `internal/applicationbackup/...`.

## DIAGNOSIS — TRUSTED PLAN / PR SELECTED CHECKS FAILURE

Run 45839805123 on exact head `6deab9ff68d15060525cc3078e828027e65e9955` (terminal):
- `PR · Trusted Plan` → FAILURE. Exact log line:
  `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/applicationbackup/recovery_manifest_workload_test.go (id source.internal_applicationbackup_recovery_manifest_workload_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json`
- `PR Selected Checks` → FAILURE. Exact log line:
  `UNIT_SCOPE: ` (empty) / `UNIT_RESULT: skipped` / `REJECT: Go test selection missing or invalid`

Root cause (verified, not guessed):
- The PR diff against base `5a37ddbd` = 2 files: the new test + the catalog edit.
- The catalog at base `5a37ddbd` (133KB, schema `baseharbor.pr-gate-coverage/v1`, release v0.4.27) contains ZERO recovery-manifest entries; the catalog entry is introduced ONLY by this PR's head `6deab9ff`.
- The Trusted Plan resolver reads the coverage catalog at the resolved effective base (the PR base parent, `5a37ddbd`), where the introducing source is not yet cataloged. Therefore the new test source is reported `uncataloged` for this PR by construction.
- Same class as w361 (0428-299, PR #1863): base/lineage + catalog-read-at-base contract failing `PR · Trusted Plan` for every commit shape against the current develop tip. Cross-reference: `evidence/w361-0428-299-1863hop/akte.md` / `evidence/board-2026-11-27/0428-299/w361-0428-299-1863hop.md`.
- Distinguish from a real test problem: the test file itself is well-formed (gofmt/vet/build pass; the only CI failure is the catalog-resolution contract, not a test compile/semantic error). The catalog fix is already present on head; re-hopping forward-merge develop does not move the base the resolver reads the catalog from.

## PLAN

- Read mission + establish reality (gh pr view 1860, ls-remote heads)
- Create fresh baseharbor worktree, checkout PR #1860 head branch
- Attest base SHA (develop) and prove ancestor of current HEAD
- Forward-merge origin/develop onto candidate branch (no cherry-pick, no force)
- Set canonical lane identity + unset inherited GIT_*
- Non-test prechecks (gofmt/vet/build) only; no local tests, no VM
- Single normal push (no force) to PR #1860 head; verify with ls-remote
- Watch exact-new-head run to terminal state
- SUCCESS: PR comment (head SHA + run ID); END with parents + 4-field verify + run result. FAILURE: capture job log, classify resolver vs test, STOP+report

## RE-HOP ACTIONS TAKEN (before the diagnosis)

- (to be recorded once executed)

## CLEANLINESS

- docker/podman: none started this shift
- worktree: (to be recorded)

## HANDOFF / STATUS

- Status: BLOCKED — the only CI failures are the `PR · Trusted Plan` catalog-resolution contract (`uncataloged source change ... recovery_manifest_workload_test.go`) and the cascading `PR Selected Checks` REJECT. The new source's catalog entry is introduced only by this PR's head and is not present at the resolver's effective base (5a37ddbd); every commit shape of PR #1860 hits it by construction. This is the same base/lineage + catalog-read-at-base class as w361 (0428-299 / PR #1863), outside this worker's write-set. STOP per mission item (h). No blind retry.
- END line: END_BLOCKED — candidate SHA 6deab9ff68d15060525cc3078e828027e65e9955; blocker = `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change ... internal/applicationbackup/recovery_manifest_workload_test.go` (read at resolved base 5a37ddbd, which predates this PR's catalog fix); parent chain fa16643a→514d827c→f877febb→6deab9ff (base parent 5a37ddbd).
