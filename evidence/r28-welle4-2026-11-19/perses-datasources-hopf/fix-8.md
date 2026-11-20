# 0428-083 perses datasources — fix-8 (x-083h5, rebase onto live develop)

Lane: x-083h5 · card t-20261114-r28-perses-datasources (0428-083)
PR: https://github.com/mcpdev80/baseharbor/pull/1684
Branch: lane-0428-083-datasources-r2 (only candidate, remote HEAD 576c6ad8fb1a)
Mission: /var/tmp/x-083h5.txt

## PLAN

1. Reality witnesses: `git fetch --prune origin develop`, then `git ls-remote origin refs/heads/develop` — confirm tip is 6b8188df26a1 or newer before doing anything
2. Monotone rebase `git rebase origin/develop` onto candidate 576c6ad8fb1a; develop tip becomes an ancestor of new head (linear, no merge commit); no rebase/force/abort beyond this
3. Verify rebase did not alter my PR content: `git diff <old head 576c6ad8> <new head>` shows ONLY develop-side changes; each of my PR files byte-identical between old and new head
4. Stop with file:line if a conflict makes both sides diverge at the same location on a function I own (integration decision, not mine to resolve silently per corrected directive)
5. Push rebase with --force-with-lease, then one pull_request run watched to terminal aggregate (§4.6): report run-id, status, conclusion immediately
6. Plan-write evidence file fix-8.md into baseharbor-plan evidence dir via /var/tmp-clone (fetch + rebase origin/main first, only my file, no git -A, no writes into product repos)
7. Verify evidence is published on origin/main (ls-remote), then report END with new head, run-id/terminal result, mergeable_state

## Why the rebase

My fix-7 hopf landed on develop b7cbc00f0adf (PR #1707). Develop has since advanced; #1693 was merged (6b8188df26a1). The corrected Owner directive (2026-11-20) requires `git rebase origin/develop` (linear), not the earlier merge-hopf. The three relevant PRs (#1684, #1690, #1650) all have base=develop and their base-sha are ancestors of the current develop tip, so a linear rebase makes the develop tip an ancestor of the new head.

## Step 1 — reality witnesses (verbatim)

```
$ git fetch --prune origin develop
* branch              develop    -> FETCH_HEAD
$ git ls-remote origin refs/heads/develop
83b19dce24eed2f837dd2dda7d56222d20a7da32	refs/heads/develop
$ git merge-base --is-ancestor 6b8188df26a1e263750379a8c5e8255ee4ef740c origin/develop
6b8188df IS ancestor of current origin/develop (monotonic advance OK)
```

develop tip 83b19dce (parents 6b8188df + 2922f5ed). 6b8188df (#1693) is a monotone ancestor — tip is newer than required (6b8188df26a1).

## Step 2 — monotone rebase attempt (verbatim)

`git rebase origin/develop` onto candidate 576c6ad8fb1a. First conflict at commit b276977d "feat(0428-083): call the datasource materializer at the real apply boundary":

```
CONFLICT (content): internal/application/perses_runtime.go
CONFLICT (content): internal/application/runtime_lifecycle.go
CONFLICT (content): internal/application/runtime_postgres.go
error: could not apply b276977d
```

## Step 3 — conflict content: substantive integration divergence (STOP, file:line)

The three conflicts are NOT merge artifacts — they are two DIFFERENT refactors of the SAME Perses compose functions, one by my commit b276977d and one by develop since b276977d's base (85965486). Both sides changed the same functions with incompatible signatures. Verbatim witnesses:

FILE 1 — internal/application/perses_runtime.go, function `writePersesGatewayComposeServices`:
- develop 83b19dce:141 `func writePersesGatewayComposeServices(b *strings.Builder, m Manifest, files RuntimeFiles) error` (no splice, no datasource logic)
- my commit b276977d: `func writePersesGatewayComposeServices(b, m, files, contextDir string) error` + new `splicePersesDatasourceMounts(...)` (the 0428-083 datasource mount splice)

FILE 2 — internal/application/runtime_postgres.go, function `RuntimeComposeYAMLForProject`:
- develop 83b19dce:330 `func RuntimeComposeYAMLForProject(m Manifest, files RuntimeFiles) (string, error)`
- my commit b276977d: renamed to `func RuntimeComposeYAMLForProject(m Manifest, resourceProject string)` + added `func RuntimeComposeYAMLForContextDir(m Manifest, resourceProject, contextDir string)`

FILE 3 — callers diverge:
- internal/application/native_backend_inventory.go:22 — HEAD `RuntimeComposeYAMLForProject(m, files)` (struct); my commit b276977d `RuntimeComposeYAMLForProject(m, files.ResourceProject)` (string)
- internal/application/remote_runtime_projection.go:64 — same divergence
- internal/application/runtime_lifecycle.go:141 — HEAD `RuntimeComposeYAMLForProject(m, files)`; my side `RuntimeComposeYAMLForContextDir(m, resourceProject, files.Dir)`
- internal/application/runtime_postgres.go:131 — HEAD `RuntimeComposeYAMLForProject(m, files)`; my side adds `ensurePersesDatasourceRuntime(...)` then `RuntimeComposeYAMLForContextDir(...)`

The rebase onto the current develop tip does NOT produce a clean linear history: my PR's datasource refactor (b276977d) is built on develop 85965486 and refactored the compose signatures; develop has since refactored the SAME functions differently. This is an integration decision (which signature wins, how callers adapt) — not a content-resolve I may make per the corrected directive (file:line STOP).

## repo-rule compliance

- No merge performed; no rebase/force beyond the single monotone rebase. Working tree reset to clean candidate 576c6ad8fb1a after documenting conflicts.
- No .github/**, no scripts/*.py change (owner scope). No content product commit.
- No subagents (§4.8). No VM/container/network/volume.
- No evidence file written into any product repo.

## cleanliness:

- Working tree clean at candidate 576c6ad8fb1a (reset --hard).
- No stray untracked files in /var/tmp/x-083h5-clone.
- Plan clone rebase'd from origin/main before/after; only fix-8.md added.
