# PR #1582 Review R1 — BF-03

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1582 head/base ancestry, candidate commit-chain log, PR state, and specified pull_request run.
2. Trace the new target-selection storage path and verify user-private directory/file modes in implementation and tests.
3. Review one-time migration, search for remaining /tmp writes, and assess legacy symlink fail-closed behavior.
4. Check BF-01 scope separation, record verdict/recipe and validation state, publish evidence, verify origin/main, and post END.

## Candidate and provenance

- PR #1582 is OPEN and DRAFT; base `develop`, head branch `lane-0428-fix-bf03`.
- Exact head: `c678cdd0a7385504be76d4acf927e47080e3db81`; `refs/pull/1582/head` and `refs/heads/lane-0428-fix-bf03` both resolve to this SHA.
- Exact base fetched from `develop`: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`.
- `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c HEAD` returned success (`BASE-ANCESTOR=yes`).
- `git log --format='%H %s' 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..HEAD`:
  `c678cdd0a7385504be76d4acf927e47080e3db81 chore(BF-03): gofmt internal/orgconfig after world-writable fix`
  `829d75bc9e710daebee62ad16710dd468db1fe13 fix(BF-03): persist target selection in private user state (not world-writable /tmp)`
  These are the two candidate commits; no foreign commits are present in the base-to-head log.
- Changed paths are only `internal/orgconfig/store.go` and `internal/orgconfig/orgconfig_test.go`.
- Planning repository root verification, before evidence work: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- Planning origin main witness before evidence publication:
  `04d51314451bf1f0a52539042bd75bfe3dce5241\trefs/heads/main`

## Findings

- REJECT — migration does not adopt the prior `/tmp` selection. `configRoot()` at `internal/orgconfig/store.go:32-40` now derives `ActivePath()` from the current `BASEHARBOR_STATE_DIR` or `os.UserConfigDir()`. `SaveActive()` passes that already-resolved path to `migrateFromWorldWritable()` (`store.go:108-114`); the helper then calls `ActivePath()` again (`store.go:183-188`), so `newPath` equals `path`. For the usual migrated case where the current config root is private, the helper returns without looking for or copying the old `/tmp` file. If the caller still has `XDG_CONFIG_HOME` set to `/tmp`, it refuses the write rather than adopting the old selection. `TestWorldWritableMigrationAdoptsOnceThenFreezes` (`orgconfig_test.go:319-387`) seeds the current `ActivePath()` under a world-writable XDG root; it does not seed a legacy path and then switch to a private user config root before exercising adoption. Recipe: retain an explicit legacy-path resolver for the prior location, validate it without following links, copy validated state once into the private canonical path, and verify the source is never written again. Add a regression that seeds the actual prior `/tmp` location, switches to the private canonical root, and proves the value is adopted and subsequent writes touch only the canonical path.
- REJECT — legacy symlink handling follows a foreign target rather than failing closed. `os.Stat(path)` at `store.go:160` follows a symlink; `os.ReadFile(path)` at `store.go:208` reads its target; and `os.Chmod(path, 0o400)` at `store.go:226` also follows it and changes the target's mode. This permits importing attacker-controlled bytes and mutating a file outside the legacy selection path. Recipe: use `Lstat` and reject symlinks/non-regular entries before reading; open with no-follow semantics where supported, verify the opened file identity, and add a symlink-to-foreign-file regression asserting error plus unchanged target bytes and mode.
- Finding — the requested mode tests do not assert the active state file and canonical organization directory modes. `TestCanonicalLocationUsesUserConfigDir` (`orgconfig_test.go:278-296`) checks only that the test's XDG root lacks world-write bits; `TestWorldWritableMigrationAdoptsOnceThenFreezes` (`orgconfig_test.go:379-386`) checks only that `active.json` has nonzero size. The existing cache assertion at `orgconfig_test.go:85-86` is for the cache file, not the persisted active selection. Recipe: after `SaveActive`, stat the actual `active.json` for owner-only file permissions and its containing organization directory for private directory permissions.
- BF-01 scope: the shared target-resolution consumer remains `cmd/baha/target.go:98,127` via `orgconfig.LoadActiveOptional()`. The candidate changes only storage/migration and its tests; it does not alter BF-01 target-selection logic. The two defects above affect the trust of the persisted selection and should be corrected within BF-03 scope; no BF-01 changes are requested here.
- Search `rg -n '"/tmp|`/tmp|filepath\\.Join\\("/tmp|os\\.(WriteFile|OpenFile|Create)\\([^\\n]*/tmp|/tmp/.+active\\.json' internal/orgconfig --glob '*.go'` found no hard-coded `/tmp` writer. This does not demonstrate migration; the missing legacy-path lookup is described above.

## CI and validation

- Specified GitHub Actions run `43668270812`: completed, conclusion success, event `pull_request`, exact head `c678cdd0a7385504be76d4acf927e47080e3db81`.
- Relevant successful jobs: `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `PR · Draft Go · cli-1`, `PR · Draft Go · cli-2`, `PR · Draft Go · cli-3`, and `PR · Draft Go · packages`. This changed Go package is covered by the `packages` job under the `pull_request` trigger. Remaining unrelated jobs were skipped; no failing check was observed. Q-RUNTIME workflow_dispatch ambient failure is excluded per mission.
- Read-only candidate inspection: `git diff --check 0e9ccb582f5bdcdc74049bbe3996263cdce6500c...HEAD` passed. No local test or VM run was needed for this review; the exact-head CI evidence above was inspected.
- No `.github/**` files were changed or modified by this review.

## Verdict

REJECT. The storage path change removes the default `/tmp` selection location and the candidate's CI run is green, but the required one-time legacy adoption is not implemented, and a symlinked legacy path is followed and its target chmodded. The missing active-file/directory mode assertions are an additional acceptance gap. Apply the recipes above on the same candidate, then rerun the affected Go package through the existing `pull_request` Go package CI job and request the same-context review again.

END mission-rev1582-r1.md BLOCKED — review verdict REJECT; corrections are required on candidate `c678cdd0a7385504be76d4acf927e47080e3db81`.

## Planning validation and publication

- `python3 scripts/plan.py render && python3 scripts/plan.py check` is STATE: render stops before check at `scripts/plan.py:883` (`short_ref`, `repo, num = ref.split("#")`) with `ValueError: not enough values to unpack (expected 2, got 1)`. The unrelated current source references lack `#` in `tasks/t-20261115-bughunt-d28-tmp-selection.md:19` and four sibling D28 task notes. I did not alter these unrelated task records or generated views.
- Immediately before evidence publication, `git ls-remote origin refs/heads/main` returned exactly:
  `04d51314451bf1f0a52539042bd75bfe3dce5241\trefs/heads/main`
