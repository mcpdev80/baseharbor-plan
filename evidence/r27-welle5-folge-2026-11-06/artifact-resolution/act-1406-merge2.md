# CODEX-MERGE — PR #1406 / artifact-resolution

## Merge result

PR #1406 was squash-merged normally into `develop` on 2026-11-07 at 00:29:52Z.

- Candidate head before merge: `9ee857387c333131ec9e1c0f42839736314bab4b`
- `develop` before merge (`git ls-remote`): `f3db942859c68e78fe2e7c0a339be7eb0e380acb`
- `work/r27-artifact-resolution` before merge (`git ls-remote`): `9ee857387c333131ec9e1c0f42839736314bab4b`
- `develop` after merge (`git ls-remote`): `dddf0d7823f6eec161ad518bbced626fa9efe52e`
- PR state after merge: `MERGED`, merge commit `dddf0d7823f6eec161ad518bbced626fa9efe52e`
- GitHub reports merge commit parent `f3db942859c68e78fe2e7c0a339be7eb0e380acb`, confirming it landed on the refreshed `develop` head.
- The candidate branch no longer appears in `ls-remote` after merge (repository auto-delete); no explicit branch-delete option was issued.

## Gates checked immediately before merge

- Current PR head matched the mission pin exactly; PR was OPEN and mergeable/CLEAN.
- `act-1406b.md` is an independent CODEX-REVIEW ACCEPT for this exact candidate. The delta review maps the production resolver change, regression, causal production-line mutant (RED/GREEN), prior focused tests, write-set, and exact-head hosted CI.
- PR Selected Checks run `42297344340` completed SUCCESS on the exact candidate SHA. Its check run reports `app_id=15368` (GitHub Actions). Applicable source-format, trusted-plan, focused Python, CLI, Go build/test/vet, and source-contract checks completed SUCCESS. HA/runtime/release-only jobs reported SKIPPED and are not the required native artifact smoke for this card.
- The native Docker evidence is `round-4-native-docker.md`: live resolver cells passed for use-existing immutable image, native-build routing, and fail-closed mutable tag; claim/release journal entries and end-of-run host counts are recorded.
- The native Podman evidence is `round-5-native-podman-locked.md`: live resolver and immutable-pull cells passed; vm-lock claim/release entries and clean-host witness are recorded. This closes the form defect noted in `act-1406c.md`.
- The task's six prerequisites were all reported accepted by `python3 scripts/plan.py show t-20261018-r27-artifact-resolution`.
- PR has no review comments, submitted GitHub reviews, or unresolved review threads. Complete PR file list has four artifact-resolution paths and no `.github/**` changes.
- `develop` had advanced beyond the PR metadata's stored base `8bda98c1` to `f3db9428`. The live comparison against current `develop` still contains only the same four artifact-resolution files. The three intervening Develop files (`cmd/baha/path_prompt_context.go`, `cmd/baha/runtime_ports_test.go`, `internal/runtime/stack_test.go`) do not overlap the PR write-set. GitHub reported mergeable/CLEAN, and the resulting squash commit's parent is the refreshed `f3db9428` head.
- Effective `develop` rulesets were both `disabled`; classic branch protection returned HTTP 404. Merge command used `gh pr merge 1406 --squash --match-head-commit 9ee857387c333131ec9e1c0f42839736314bab4b`. No `--admin`, force, protection bypass, or CI override was used.

## Planning closeout

Planning closeout completed: `t-20261018-r27-artifact-resolution` is `closed` / `accepted`, with this HTTPS evidence linked in its frontmatter. `python3 scripts/plan.py render` and `python3 scripts/plan.py check` passed (380 tasks, 0 errors, 0 warnings). The card and derived views were published on Planning `main` by commit `6053da24f02b6f065150909c7cd69a9ca78d53b0`; this evidence record was published first by `ec2647fe5fd0db19da74a12c4e7a79a57cbc2c8f`.
