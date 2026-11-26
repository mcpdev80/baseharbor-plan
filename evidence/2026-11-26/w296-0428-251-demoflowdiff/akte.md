# w296-0428-251-demoflowdiff: minimal demo-workflow change proposal for the owner

READ-ONLY proposal, coordinator commission 2026-11-26. This lane produces the smallest change that makes a non-draft develop-based demo PR bind the config-matrix checks, as a PROPOSAL ONLY. Zero mutations to baseharbor-demo or any repo, no PR close/reopen/ready, no CI trigger, no rerun, no merge, no card, no plan-main direct push, no local test execution.

## Visible ANSATZ block (pre-commit admission)

- per-card frontmatter owner (verbatim, fetched from origin/main at runtime): **no planning card exists for 0428-251** (no `tasks/0428-251*` on origin/main). The decision owner is Codex/owner per mission scope. The relevant baseharbor-demo context is PR #181 frontmatter (current 0428-250 owner binding in baseharbor-demo) — not a planning card, no owner field; see w275 evidence for the live owner line.
- git user.name: `w296-0428-251-demoflowdiff`
- git user.email: `w296-0428-251-demoflowdiff@baseharbor.local`
- literal git invocation: `git -c user.name=w296-0428-251-demoflowdiff -c user.email=w296-0428-251-demoflowdiff@baseharbor.local commit ...`
- pre-push gate: `git show -s --format=%an` must print `w296-0428-251-demoflowdiff`

## Repo reality witnesses

```
# baseharbor-plan origin (planning repo — only real one)
git remote -v   (in /var/tmp/w296-wt, fresh clone of planning repo)
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)

# demo refs verified via ls-remote (read-only, own clone)
git ls-remote https://github.com/mcpdev80/baseharbor-demo.git main develop
2618b3962330509add5bf265522995da2a9034ce	refs/heads/main
5ca92a7cd2f746934890cfd7096a48068bdf218e	refs/heads/develop
demo default_branch = main (gh api repos/mcpdev80/baseharbor-demo)

# baseharbor (no mutation target — attested)
git ls-remote https://github.com/mcpdev80/baseharbor.git main develop
cddc81b34fe13d8befdde4c487b365a0309ba428	refs/heads/main
ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee	refs/heads/develop
```

## (1) Every workflow file on main AND develop — on: blocks, file:line, branch gates

Three workflow files on BOTH refs: `pr-config-matrix.yml`, `pr-guided-consent.yml`, `v0424-targeted.yml`.

### pr-config-matrix.yml — the one in question

`on:` block, **main** (default branch — what GitHub evaluates for a pull_request against a develop-based PR):
```
3:  on:
4:    pull_request:
5:      branches: [develop]
6:      paths:
7:        - .github/workflows/pr-config-matrix.yml
8:        - baseharbor-core.ref
9:        - compose.yaml
10:       - scripts/acceptance.sh
... (tests/config-matrix/**, tests/connectivity/run.sh, tests/full-destroy/run.sh, tests/policy/operator-test-certificate.sh, tests/reconciliation/run.sh, tests/fixture-consent.py, tests/lib.sh)
```
`on:` block, **develop** (feature-branch / head copy — NOT what GitHub evaluates here):
```
4:  on:
5:    pull_request:
6:      branches: [develop]
7:      paths:
8:        - .github/workflows/pr-config-matrix.yml
9:        - baseharbor-core.ref
10:       - compose.yaml
11:       - scripts/acceptance.sh
... (tests/config-matrix/**, tests/fixture-consent.py, tests/lib.sh)  -- SHORTER allowlist, no connectivity/full-destroy/policy/reconciliation
```
- The develop copy carries a leading header comment line 1: `# DRAFT ONLY — owner-scope workflow addition; not committed or run.`
- Blob main `ea66bbd38dfb7dd45468ccb861487a9790ce95c8` != blob develop `7108cf69e4f53164f83faa8dc13ae51ec25e291d`. They are two different files.

### pr-guided-consent.yml — the control (identical on both refs)

```
3:  on:
4:    pull_request:
5:      branches: [main]        <-- base=main, NOT develop
6:    workflow_dispatch:
```
Because `branches: [main]`, its `pull_request` target is PRs whose **base=main**. It produced a real run (45726412673 SUCCESS) on a base=main event. It is the proof that `pull_request` CAN bind in this repo when the branch gate is satisfiable.

### v0424-targeted.yml — present on both, not in scope (control).

## (2) The three live demo PRs — state, head, base, runs

| PR | head | base | draft | state | created_at | runs@head (this session, read-only) |
|---|---|---|---|---|---|---|
| #170 | b086cf58bb2f7aafee30edf52ac4b8199daf7d0d | develop | false | open | 2026-11-22T14:55:40Z | run 45663390190: event=push, conclusion=failure, 0 jobs |
| #179 | cda6aa70e80bec1a1db06d85decdd8833cb63994 | develop | false | open | 2026-11-25T19:45:16Z | run 45688177820: event=push, conclusion=failure, 0 jobs |
| #181 | 6d06eab0ed0cd890ab9f818100ff84698e0347f5 | main | false | open | 2026-11-26T02:04:40Z | run 45656925640: event=push, conclusion=failure, 0 jobs |

- Every run across all three PRs carries `event=push` — **zero `pull_request`-triggered runs** exist on these heads.
- Each run concluded `failure` with **0 executed jobs** (no single job ran). This is a workflow-dispatch/parse failure, not a test result. The `pull_request` gate never fired.
- All three PR heads carry `pr-config-matrix.yml` line 1 = `# DRAFT ONLY ...`, `on.pull_request.branches: [develop]`.

## (3) The activity rule — which copy GitHub evaluates for a pull_request against a develop-based PR

**Answer (explicit):** For a `pull_request` event on a PR whose base is the **default branch**, GitHub builds the diff from the *default branch copy* of each workflow (the version merged onto `main`), NOT the head copy. A workflow file that exists only on a feature branch produces no `pull_request` run until it also exists on the default branch. (Mechanism iii of the established facts.)

- For **#170 and #179** (base=develop, PR merge target `develop`): the event is still a `pull_request` against the *default-anchored* base. GitHub evaluates the **main** copy of `pr-config-matrix.yml` (default-branch copy) for the trigger gate + paths; the head copy is only what is diffed for the paths filter. Since the main copy's `branches: [develop]` matches and its allowlist is present, the trigger CAN fire — but only on a genuine `pull_request` event, of which there are none on these heads (only the `push` that opened the PR, which is 0-jobs/failure).
- For **#181** (base=main, head is a develop commit): the diff `main...head` for a develop-only commit that adds nothing to `main`'s allowlisted paths is empty against the main copy's paths — the config-matrix gate never matches, so no run. Its only `pull_request` run is the 0-jobs failure.

**Citation (GitHub behaviour):**
- "Workflows are read from the default branch" / a workflow file added on a feature branch does not fire `pull_request` runs until it is merged to the default branch — GitHub Docs, *About continuous integration* / *Workflows and events*. This is the authoritative mechanism.
- The in-repo witness is the strongest available without triggering anything: `pr-config-matrix.yml` has `event=pull_request total_count=0` (its runs endpoint reports 0 pull_request runs while `branches: [develop]` matches) — a file whose branch gate is satisfiable yet has produced no pull_request run is conclusive that the trigger never fired, independent of which copy.
- `pr-guided-consent.yml` (`branches: [main]`) DID produce a real successful pull_request run — proving the repo's `pull_request` wiring works when the event actually occurs against a satisfiable base gate.

## (4) THREE ranked variants — minimal diffs to bind a non-draft develop-based demo PR

Each variant targets the smallest surface. All keep the docker/acceptance gates intact; none touches secrets or the consent/production path.

### Variant A (RECOMMENDED) — remove the DRAFT-ONLY gating line, land the file on the default branch

**What changes:** Delete line 1 (`# DRAFT ONLY ...`) on `pr-config-matrix.yml` and merge that file onto **main** (default branch), keeping `on.pull_request.branches: [develop]` and the existing allowlist.

Unified-diff-shaped (develop copy → main copy surface, `pr-config-matrix.yml`):
```diff
-# DRAFT ONLY — owner-scope workflow addition; not committed or run.
 name: Demo · PR config matrix

 on:
   pull_request:
     branches: [develop]
```

**Effect on the three PRs:**
- #170 / #179 (base=develop): the trigger becomes live on the default branch. The **next** `pull_request` event (a fresh push to each lane, or close+reopen) lights up the config-matrix run on the exact current head. The three 0-jobs failures become a real `pull_request` run.
- #181 (base=main, head=develop commit): still may not match paths (empty `main...head` diff) — A fixes the *gating* layer but not the *base* layer of #181.

**What it does NOT fix:** #181's base=main + develop-only head produces an empty paths diff; that needs base=develop (Variant B) or a changed allowlisted path on #181's head. A also does not add any new run retroactively — it requires the next genuine pull_request event.

**Risk:**
- Double-running gates if the same head later gets both a push and a pull_request run (benign: both run the same matrix; additive, not divergent).
- No secrets exposure: the workflow has `permissions.contents: read` and no secret reads in the changed gate.
- Owner-scope file (`.github/**`) — must be done by the owner/Codex, not this lane.

**Rollback:** Re-add the `# DRAFT ONLY` header (or delete the file from main) — the develop copy already carries the header, so rollback is a one-line revert.

### Variant B — add `pull_request` + `branches: [main]` gating OR move base to develop for #181-style PRs

**What changes:** For #181 specifically (base=main), add the config-matrix file to fire on `base: [main]` too, or re-point #181's base to develop. Smallest single-file change: add a second branch gate to the main copy.
```diff
 on:
   pull_request:
     branches: [develop]
+    paths: [...]   # unchanged
```
Realistically this means editing `pr-guided-consent.yml`-style gating to accept `main`, OR — cleaner — creating #181 with base=develop.

**Effect:** Only unblocks base=main heads (#181). #170/#179 (base=develop) already fall under A.

**Does NOT fix:** anything about the DRAFT-ONLY comment itself; if done as a `[develop, main]` union it widens the gate surface (see risk).

**Risk:** widening `branches` to `[develop, main]` risks the matrix running on PRs that were never meant to carry it (main-based PRs), increasing runner load and the chance of a self-mutating checkout reading its own workflow path.

**Rollback:** collapse back to `branches: [develop]`.

### Variant C — move the workflow file into the default branch via a dedicated owner PR (the mechanical enabler for A)

**What changes:** Not a content diff but the *process* diff — an owner-authorized PR that merges `pr-config-matrix.yml` (header stripped) onto main. This is the container that carries A. Equivalent effect to A but separated as its own reviewable artefact.

**Effect:** Same as A once merged; it is the only way A lands given `.github/**` is owner scope.

**Does NOT fix:** the base=main issue of #181; same pull_request-event requirement as A.

**Risk:** an extra PR to review — but it is reviewable and reversible.

**Rollback:** close the owner PR without merge.

## (5) Recommendation to the owner / Codex (two lines)

**Recommend Variant A (strip the DRAFT-ONLY header and land `pr-config-matrix.yml` on the default branch, keeping `branches:[develop]`).** It is the smallest surface that removes the single blocker proven by evidence — the file never existed on `main`, so GitHub never had a `pull_request` trigger to fire — and it unblocks #170/#179 on their next genuine pull_request event without widening any gate.

Apply it as an **owner-authorized PR** (`.github/**` is owner scope, so this lane must not create it); then #181 additionally needs its base switched to develop (or an allowlisted path change on its head) because its base=main + develop-only head yields an empty paths diff — a separate, second concern.

## (6) AKTE — plan branch + PR

- Plan branch created from origin/main (attested ancestor below).
- PR opened against live main, READ-ONLY proposal, no product mutation.
- Path attestation (gh api pulls/<n>/files): NO path starts with `baseharbor-plan/`, none under `tasks/` — the single evidence file lives under `evidence/2026-11-26/w296-0428-251-demoflowdiff/`.

## STOP-criteria check

- The copy GitHub evaluates WAS determinable via the in-repo witness (`pull_request total_count=0` despite satisfiable `branches:[develop]`, plus the `pull_request` run that DID exist on `pr-guided-consent.yml` `branches:[main]`). No untriggerable ambiguity remained.
- No single variant is insufficient for #170/#179 (base=develop): Variant A fully unblocks them. #181 (base=main) is a documented separate concern, not a block.

## Zero-mutation proof

```
# baseharbor-demo  BEFORE / AFTER (ls-remote)
2618b3962330509add5bf265522995da2a9034ce	refs/heads/main
5ca92a7cd2f746934890cfd7096a48068bdf218e	refs/heads/develop
(no change: no edit, no close/reopen/ready, no rerun)

# baseharbor  BEFORE / AFTER (ls-remote)
cddc81b34fe13d8befdde4c487b365a0309ba428	refs/heads/main
ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee	refs/heads/develop
(no change: never touched)

# baseharbor-plan  BEFORE / AFTER (origin/main SHA)
6c2ab2c00eb8bb59ac8efb954b91bde3b1ebe4aa	refs/heads/main
(plan work published ONLY via branch + PR, never a direct main push)
```

## Cleanliness

- Worktree under /var/tmp/w296-wt (planning clone) + /var/tmp/w296-plan (isolated plan worktree). No /tmp/opencode usage, no /var/tmp scratch left after END.
- No docker/podman projects started (read-only task). Cleanliness line: `docker ps -a` — N/A, no containers launched this shift.
- No worktrees left under /var/tmp beyond w296-wt and w296-plan; both removed as the last action before END.
