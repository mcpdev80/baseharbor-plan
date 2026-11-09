# CODEX-REVIEW 0427-173 r3 — PR #1505

## PLAN

1. Verify live PR head, PR base, current develop, ancestry, and the exact-head hosted run.
2. Review the MCP target-resolution/authorization/mutation path and the new CLI missing-source/applied-intent regression against r2's findings.
3. Check the one-name contract in help, user-facing errors, and DE/EN generated documentation; identify executed versus skipped native jobs.
4. Publish the SHA-specific verdict with an actionable recipe and post END.

## Verdict

**ROLLE: REVIEW — KORREKTUR; approval withheld.** The r3 changes address important parts of the r2 review: the in-memory MCP regression shows that a non-default `input.Target` is honored, and a `runWithIO` CLI regression reaches the missing-source/applied-intent guard. The exact-head run is terminal success, with `PR Selected Checks` passing. However, authorization is performed against one resolved identity and the MCP handler then resolves by name again before mutation; the implementation does not carry the authorized identity through to deletion. The applied-intent test reads both “before” and “after” bytes only after invoking the CLI, so its byte-preservation assertion is vacuous. The ambiguous-name error still recommends unsupported `--uuid`, contrary to the one-name contract. Finally, the candidate does not include the current develop head `b3a8042d1`; its PR base remains `20902f0a6`.

### Candidate and base

- PR #1505 is open at exact head `bcdede014979de5692b2879eb6ddcd17141c2677`; the latest exact-head run is `42553125972` (`pull_request`, terminal `completed/success`). The r3 source head is `bd5df838`; the r3-to-r4 diff is one gofmt-only change in `cmd/baha/app_prune_test.go`.
- GitHub PR metadata reports base SHA `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Live `git ls-remote origin develop` is `b3a8042d18ea60f162a32a51df34a499cad6a237`. The PR base SHA is an ancestor of the candidate (exit 0), but current develop `b3a8042d1` is not (exit 1). The round-3 dossier also records that develop drift and says integration is still required.
- The current exact run therefore proves the checks for this head, not that the candidate is based on current develop. Refresh the candidate and recheck the resulting exact head before acceptance.

### MCP target selection and identity stability

The Target-selection correction itself is present. `registerMCPAppPruneTool` sets `input.Target` at `cmd/baha/app_prune.go:321-323`, and `resolvePruneByName` retains the override (`:233-245`). `TestAppPruneMCPPreservesTargetOverride` (`cmd/baha/app_prune_test.go:528-633`) uses an in-memory MCP transport, a non-default Target, and an ambient-target negative control; it proves the handler does not silently fall back to the ambient Target.

The resolved deployment identity is not stable through authorization and mutation. At `cmd/baha/app_prune.go:323-328`, the handler calls `resolvePruneCandidate` and authorizes that result. It then calls `executeApplicationPrune` by name at `:330-331`; `executeApplicationPrune` resolves again at `:76-86` and deletes the second result at `:129`. No lock or equality check binds the second resolution to the identity that was authorized. A same-name record replacement between those operations could therefore change which deployment is deleted.

**Correction recipe:** In `cmd/baha/app_prune.go:76-86,129,321-335`, pass the already resolved object into the mutation routine after authorization, or compare the full identity (Target, DeploymentID, ApplicationID, application name, environment) from a fresh resolution with the authorized identity and fail closed on any difference. Add an MCP test with an injected change between authorization and mutation; assert the replacement record remains byte-identical and only the originally authorized deployment can be removed. Stop when authorization and deletion demonstrably use the same identity.

### Applied-intent refusal and byte preservation

`TestAppPruneRefusesDanglingRecordWithAppliedIntent` (`cmd/baha/app_prune_test.go:435-478`) is a real CLI-entry test: it creates a record whose source is missing but whose applied intent is present, invokes `runWithIO`, and asserts `RECORD_NOT_DANGLING`. That does exercise the intended guard rather than the earlier `SOURCE_PRESENT` branch.

The record-byte assertion is not a before/after comparison. The CLI call occurs at line 450; the variable named `before` is first read at line 468, after the call, and `after` is read immediately afterward at line 472. The test checks that the record still exists but cannot detect a mutation that preserves the path.

**Correction recipe:** Read and retain `deployment.json` bytes before `runWithIO`; after the refusal, read them again and compare the snapshots. Keep the cause-code assertion. Stop when the test fails if the CLI changes or removes the record and passes only when the file is byte-identical across the invocation.

### One-name help and documentation consistency

The user-facing `Usage` and long help text enforce `baha app prune <name>` and exactly one name (`cmd/baha/app_prune.go:41-42`); generated command indexes in `docs/cli/command-index.md:39` and `docs/de/cli/command-index.md:39` also show that one-name form. But the ambiguity refusal at `cmd/baha/app_prune.go:291` still says `baha app prune --uuid <deployment-id>`, while the parser at `:203-224` rejects flags and accepts exactly one positional name. The stale source comments at `:29-31` and resolver comments at `:79-85` also claim `--uuid`/`-e` are supported. The machine is being given a next step that this command rejects.

**Correction recipe:** Remove the stale selector claims and make the ambiguous-name `Next` text honest under the one-name contract. Do not recommend `--uuid` or `-e` unless the parser and tests actually support them. Add an ambiguity CLI regression that checks the suggested action is accepted by the parser or explicitly reports that prune cannot disambiguate; keep all matching records unchanged. Stop when source comments, generated DE/EN help, and runtime refusal agree.

### Hosted checks and native-cell status

Run `42553125972` is terminal `completed/success` on exact head `bcdede014979de5692b2879eb6ddcd17141c2677`. `PR Selected Checks` (`128955981675`) passed. The hosted `pull_request` `PR · Validation · go-unit-tests` job (`128953051670`) passed and runs `go test ./... -count=1` via `scripts/pr-unit-database.sh:32-33`; it therefore covers the new `cmd/baha` regression. The deployment and documentation gates, build, vet, formatting, and wizard-registration jobs also passed.

Native status must be read literally:

- `PR · Native destroy retry · docker` (`128953048384`) passed.
- `PR · Native destroy retry · podman` (`128953048482`) passed.
- `PR · Native Keycloak/Core` (`128953052688`) was **skipped**, not executed and not a pass. The related targeted HA and other skipped jobs likewise remain skipped.

No `.github/**` change or workflow rerun was made.

## Stop criteria

- Authorization and mutation use the same full deployment identity, with an MCP regression that changes the candidate record between those steps and proves fail-closed behavior.
- The missing-source/applied-intent CLI test snapshots the record before invocation and proves byte identity afterward.
- Ambiguous-name guidance matches the parser's actual one-name support, with a non-mutating regression.
- Rebase/integrate current develop `b3a8042d1`, then require a terminal exact-head run; report skipped native cells as skipped, never as green.

## END

END_DONE 0427-173-r3-review: KORREKTUR — PR #1505 head `bcdede014979de5692b2879eb6ddcd17141c2677`; MCP Target selection works but identity is re-resolved after authorization, applied-intent byte snapshot is post-call, ambiguous-name guidance recommends unsupported `--uuid`, current develop is not an ancestor. Run `42553125972` success; Native Keycloak/Core skipped. Evidence publication SHA to follow.
