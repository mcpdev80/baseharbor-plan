# CODEX-REVIEW — PR #1580

**ROLLE: REVIEW**
**Task:** t-20261114-r28-cli2-uid-target
**Candidate:** ae79d1bc7b4dc0653ab787a89ada24779baa64c9
**Base:** PR base lane-0428-uid-environment at 756d21b7839a05c83435e6a39fc0daeb8b0580be; the head includes the target-UID commits rebased onto that base and a develop merge at 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95. The PR tree diff therefore also carries develop-sync content; task-specific target changes are the 12 target-UID files.
**Exact-head CI:** run 43794175538, pull_request, COMPLETED SUCCESS, exact SHA; Draft source/routing, CLI shards 0–3, and package jobs passed. Other native/release jobs were skipped under draft selection. git diff --check clean.

## Verdict: REQUEST CHANGES

internal/deployment/target_id.go:MigrateLegacyTargetUIDs claims to be pure and to return no partially migrated configuration on failure, but begins with migrated = cfg. Config.Targets is a map, so this shallow copy aliases the caller's map. Each generated UID assignment at migrated.Targets[name] = def mutates cfg.Targets as well. If final validation fails, the function returns an empty result after it has already partially changed the caller's in-memory config. Current persistence caller discards the config on error, but the helper's contract is violated and future callers can observe partial migration state.

## Recipe

- **File/change:** internal/deployment/target_id.go; clone the Targets map before writing generated UIDs (and deep-copy any other mutated reference fields if introduced), preserving the input config unchanged.
- **Tests:** assert input cfg.Targets remains byte/value-identical after successful migration and after a validation/collision failure, while returned config contains the full migration only on success. Keep idempotency and no-write-on-failure coverage. Run the affected deployment/target tests and obtain a new exact-head pull_request CI run.
- **Stop:** stop before persistence if migration returns an error or any partial result; do not weaken collision validation.

The task's parent environment lane is still not accepted. This content review does not satisfy that dependency or authorize merge.

Read-only review; no merge performed.
