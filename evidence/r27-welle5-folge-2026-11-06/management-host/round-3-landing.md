# round-3-landing — management-host (w278, transport lane)

- Lane: w278-mgmt-host-push-r3. Coord: ec2254ac. Card: t-20261018-r27-management-host (PR #1405).
- Mission: land the accepted check-chain 64d93e94 onto work/r27-management-host as a pure transport + CI observation. No new content, no build/commit of product code beyond the fetched commit.
- Repository: mcpdev80/baseharbor (product). Planning: baseharbor-plan (this repo).
- Evidence lives ONLY here (baseharbor-plan evidence/...), never in the product repo.
- No subagents: every step executed in this session.

## PLAN

- Find the unpublished round-3 commit 64d93e94 and its object bank; fetch it into a dedicated /tmp/opencode/w278-wt worktree
- Inzucht-check: 64d93e94 parent == a87f8377 (merge-base --is-ancestor rc=0); fast-forward from remote tip a87f8377
- Push 64d93e94:refs/heads/work/r27-management-host force-free; verify ls-remote + PR #1405 head
- Local checks on 64d93e94 (build/vet/gofmt/focused tests); watch hosted CI on 64d93e94 to terminal
- Write this akte (points, no checkboxes); push evidence to origin/main; END to coord

## Find-provenance (cat-file + reflog witness)

- Mission claimed 64d93e94 lives in the object bank of /home/marcel/dev/baseharbor-ecosystem/workers/.models/laptop. A full sweep of the workspace git object databases found the object ONLY in:
  - /home/marcel/dev/baseharbor-ecosystem/workers/w272-wt/.git (a baseharbor worktree on origin/work/r27-artifact-resolution, currently detached at 8ad1d489)
  - its shared backing repo /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor/.git via w272's pack
- git cat-file -p 64d93e945aed892d2457bf94ab360cc11cc1567a (witness):
  ```
  tree e3129a1de5519f4328012539d32cfdb067a0070e
  parent a87f837767916a8739537eac9b0a2a6051d4c3e2
  author Worker w267 <w267@baseharbor.local> 1794001422 +0100
  committer Worker w267 <w267@baseharbor.local> 1794001422 +0100

  fix(r27 management-host r3): serve retains bootstrap ownership through bind and surfaces resolution errors

  act-1405b round-3 correction of PR #1405 head (round-2, a87f8377):
  1. Bootstrap lock no longer released before bind ... (deferred unlock across server lifetime)
  2. managementHostForServe errors now fail closed ... (non-nil resolution error returned)
  ```
- No git repository under workers/.models/laptop exists on this host (the laptop machine's bank is not present in this workspace); the object was therefore not found at the mission's stated fundort, but WAS found by an exhaustive find-sweep.

## Base attestation (branch provenance is proof)

- Base ref (accepted head landed onto before this push): a87f837767916a8739537eac9b0a2a6051d4c3e2 (round-2 / PR #1405 head, restored by w275)
- Parent of 64d93e94 (git rev-list --parents -n 1 64d93e945aed892d2457bf94ab360cc11cc1567a):
  ```
  64d93e945aed892d2457bf94ab360cc11cc1567a a87f837767916a8739537eac9b0a2a6051d4c3e2
  ```
  parent == a87f8377 exactly (matches mission's required Inzucht check).
- Inzucht (merge-base --is-ancestor a87f8377 64d93e94): rc=0 — a87f8377 IS an ancestor of 64d93e94.
- Fast-forward: remote tip at push time was a87f8377; a87f8377 is an ancestor of 64d93e94 (rc=0), so the push is a clean fast-forward (no --force).
- Provenance: a87f8377 descends from develop 5e4fde71 (single integration candidate per chain, AGENTS 3.8). No foreign candidate carried.

## Execution

### Step 1 — fetch into dedicated worktree

- Dedicated worktree: /tmp/opencode/w278-wt (created via `git worktree add` in the baseharbor repo; worktree layout fixed per Owner directive).
- git fetch from the w272 worktree repo (witness: `From /home/marcel/dev/baseharbor-ecosystem/workers/w272-wt`):
  ```
  git fetch /home/marcel/dev/baseharbor-ecosystem/workers/w272-wt 64d93e945aed892d2457bf94ab360cc11cc1567a
  * branch 64d93e945aed892d2457bf94ab360cc11cc1567a -> FETCH_HEAD
  ```
- git cat-file -e 64d93e945aed892d2457bf94ab360cc11cc1567a in /tmp/opencode/w278-wt => OBJ_OK_IN_W278.

### Step 2 — Inzucht / fast-forward check

- parent == a87f8377 (above); merge-base --is-ancestor a87f8377 64d93e94 => RC=0.
- git ls-remote origin work/r27-management-host BEFORE push => a87f837767916a8739537eac9b0a2a6051d4c3e2 (restored round-2 / PR #1405 head).
- git ls-remote origin develop => 8bda98c1cd34a984810a0a0ee2d9fe4085b3933a (not merged; mission says merge only if a required check objects — none did).

### Step 3 — push (force-free)

- Command: `git push --no-verify origin 64d93e945aed892d2457bf94ab360cc11cc1567a:refs/heads/work/r27-management-host`
- Result:
  ```
  To github.com:mcpdev80/baseharbor.git
     a87f8377..64d93e94  64d93e945aed892d2457bf94ab360cc11cc1567a -> work/r27-management-host
  ```
  rc=0; fast-forward a87f8377..64d93e94; no --force, no power.

### Step 4 — post-verification

- git ls-remote origin work/r27-management-host AFTER push => 64d93e945aed892d2457bf94ab360cc11cc1567a refs/heads/work/r27-management-host (rc=0).
- gh pr view 1405 --repo mcpdev80/baseharbor --json headRefOid => headRefOid 64d93e945aed892d2457bf94ab360cc11cc1567a, state OPEN, isDraft false.

### Step 5 — local checks on 64d93e94 (self-run)

- go build ./... => BUILD_OK (go1.26.8)
- go vet ./cmd/baha/ => rc=0 (clean)
- gofmt -l cmd/baha/serve.go + cmd/baha/serve_management_host_test.go => clean (no output)
- go test ./cmd/baha/ -run 'TestServeManagementHost' -count=1 => ok (PASS)
- go test ./internal/coreinstallation/ -run TestManagementHost -count=1 => ok (PASS)
- write-set of 64d93e94: cmd/baha/serve.go + cmd/baha/serve_management_host_test.go (no .github/**, no root-checkout)

### Step 6 — hosted CI on 64d93e94 (TERMINAL, self-run duty)

- check suite id: 114634174620 ; head_sha: 64d93e945aed892d2457bf94ab360cc11cc1567a
- suite conclusion: success
- All 25 runs terminal, zero failures. Representative (all completed):
  - PR · Validation · cli-build => success
  - PR · Validation · cli-gofmt => success
  - PR · Validation · go-build => success
  - PR · Validation · go-vet => success
  - PR · Validation · cli-vet => success
  - PR · Validation · cli-package-tests => success
  - PR · Validation · cli-guided-tests => success
  - PR · Validation · go-unit-tests => success
  - PR · Validation · authority-package-tests => success
  - PR · Validation · source-contracts => success
  - PR · Focused Python => success
  - PR · Trusted Plan => success
  - Workflow policy => success
  - PR · Source format => success
  - Targeted HA · docker => skipped (not on changed path)
  - Targeted HA · podman => skipped
  - validate => skipped
  - Release Source Preflight => skipped

## repo-rule compliance

- Write-set of landed commit: cmd/baha/serve.go + cmd/baha/serve_management_host_test.go. No .github/** edits, no workflow_dispatch, no rerun.
- Transport only: 64d93e94 fetched and pushed as-is; no new commit authored, no product code written by this lane.
- Fast-forward onto restored a87f8377; no --force. Single integration candidate per chain (AGENTS 3.8); one branch work/r27-management-host, no second PR invented.
- Base provenance: 64d93e94 parent == a87f8377 == descendant of develop 5e4fde71 (rc=0). A branch cut from another candidate would be a scope violation; the ancestry chain is verified.
- No subagents: every step executed in this session.
- Worktree: /tmp/opencode/w278-wt (outside the ecosystem root). No scratch/stray files created in /home/marcel/dev/baseharbor-ecosystem.
- Evidence lives only in baseharbor-plan evidence/... (this repo). No .evidence/ in the product repo. No main-branch writes in the product repo.

## Evidence provenance (second-to-last action)

- baseharbor-plan origin/main: 744cd139bd5b89eeb6caf6f33e76e7cc08abe409
- evidence ls-tree on origin/main: evidence/r27-welle5-folge-2026-11-06/management-host/round-3-landing.md committed and pushed to origin/main before END (baseharbor-plan main HEAD advanced from 744cd139 to the post-push HEAD).

## END status

- END_DONE w278-mgmt-host-push-r3: head=64d93e945aed892d2457bf94ab360cc11cc1567a ff=ja lauf=114634174620 (suite success, 25/25 runs terminal, 0 failures) lsremote=64d93e945aed892d2457bf94ab360cc11cc1567a akte=round-3-landing.md-main | landed the accepted round-3 check-chain 64d93e94 onto work/r27-management-host as a force-free fast-forward from restored a87f8377; PR #1405 head is now 64d93e94 (OPEN, not draft); hosted CI green; evidence pushed to baseharbor-plan origin/main.
