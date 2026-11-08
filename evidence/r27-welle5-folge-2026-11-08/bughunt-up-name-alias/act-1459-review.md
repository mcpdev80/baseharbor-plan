# CODEX-REVIEW 0427-130 — PR #1459

## PLAN

1. Resolve the current PR head, develop base, ancestry, complete changed-file list, and hosted run from GitHub.
2. Compare the parser, both name-resolution call sites, consent path, regression tests, CI selection, and generated documentation at the exact head.
3. Record the verdict, remaining acceptance gap, and a concrete correction recipe.
4. Publish this review to the verified baseharbor-plan origin/main and verify both evidence and candidate remote SHAs.

## Verdict

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1459 head:** `b69c096242a8940f5365b683532313a4fb89e5bc`  
**Develop base:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**Hosted run:** `42462640598`, terminal success on the exact PR head.

### Findings

1. **Parser and source routing are aligned; consent behavior is unchanged by this diff.** `cmd/baha/runtime.go` adds the optional `Name`, accepts a single positional name, rejects a second, and retains the existing flag and consent parsing. `upNameArgs` supplies the name at both repository `resolveApplication` call sites: `cmd/baha/runtime_repository_up.go` and `cmd/baha/app_input_resolver.go`. The change does not modify the candidate-consent resolution path. The compare is based on the exact PR head, whose complete changed-file set is six `cmd/baha` files and the English/German CLI command indexes; no `.github/**` or consent implementation files are in the diff.

2. **The parser regression is picked up by hosted CI, but it does not prove the task's registered-deployment acceptance behavior.** `TestParseRuntimeUpOptionsAcceptsOptionalName`, `TestParseRuntimeUpOptionsRejectsSecondName`, and `TestParseUpParsesIdenticalToAppUpEnforcesParity` are in `cmd/baha/runtime_ports_test.go`. The parity test checks one positional-name/flag combination and compares the two parsers. It does not call the top-level command through `resolveApplication` outside an application repository or prove that a registered deployment named by the argument is resumed. The round-1 manual command stopped at a repository-inspection size-limit error, so it did not provide that acceptance proof either.

   The hosted `PR · Validation · go-unit-tests` job did execute on this candidate and passed. Its `ci.yml` mapping invokes `scripts/pr-unit-database.sh`, which runs `go test ./... -count=1`; this includes the changed `cmd/baha` tests on the `pull_request` trigger. Thus there is no CI-routing or hosted-run blocker for the parser test itself.

   **Correction recipe:** add a production-command regression in the existing `cmd/baha` test suite. From a temporary working directory with no repository application, seed/register a deployment with a known name, invoke the top-level `baha up NAME --yes --plain` path, and assert that resolution selects/resumes that registered deployment rather than resolving by current directory. Exercise the equivalent `baha app up NAME` path against the same fixture and compare the selected deployment/result. Keep consent assertions unchanged and fail closed for unknown names. The package-wide `go-unit-tests` job must discover and pass the new test on the corrected exact head.

3. **The documentation surface matches the implementation.** `cmd/baha/commands.go` now advertises `baha up [NAME]`; both `docs/cli/command-index.md` and `docs/de/cli/command-index.md` carry the same `[NAME]` usage row. The exact-head hosted `documentation-audit`, `mkdocs-en-strict`, `mkdocs-de-strict`, and `pages-candidate-build` jobs passed.

### Hosted-state correction

The run list was not empty. `gh api repos/mcpdev80/baseharbor/actions/runs?head_sha=b69c096242a8940f5365b683532313a4fb89e5bc` returned run `42462640598`; `gh run view` confirms `headSha=b69c096242a8940f5365b683532313a4fb89e5bc`, `status=completed`, `conclusion=success`. `gh pr checks 1459` shows `PR · Validation · go-unit-tests`, `PR Selected Checks`, `go-build`, `go-vet`, `cli-gofmt`, source format, trusted plan, focused Python, docs and wizard checks all passed. The runtime, native, and HA jobs were skipped as expected for this CLI-only diff.

The round-1 evidence names run `42461878643` as green on this head, but that run belongs to earlier head `fecfbabc752def7284b50e576d00f640286b0793` and concluded failure. It is not evidence for the reviewed commit. The later exact-head run `42462640598` is green, so this mismatch does not leave CI red, but the evidence should identify the correct run.

## SHA, ancestry, and scope witnesses

- `gh api repos/mcpdev80/baseharbor/pulls/1459` returned base `07ae6c3e91b081a189266ca4b162ba705d4aa78f` and head `b69c096242a8940f5365b683532313a4fb89e5bc`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1459/head` returned the same develop and PR-head SHAs.
- GitHub compare `develop...b69c096242a8940f5365b683532313a4fb89e5bc` returned `status=ahead`, `ahead_by=2`, `behind_by=0`, and merge base equal to develop. Its changed files match the set described above.
- No product file was modified, no local tests were run, and no workflow rerun or dispatch was requested.

## Stop criterion

Do not approve until a CI-discovered regression proves that `baha up NAME --yes --plain` outside a repository resumes the named registered deployment and matches the `baha app up NAME` outcome. Require the corrected exact-head hosted `go-unit-tests` and `PR Selected Checks` to pass. The existing parser-only regression and green run do not prove this runtime acceptance clause.

## END

END_BLOCKED 0427-130-review — KORREKTUR; PR #1459 head `b69c096242a8940f5365b683532313a4fb89e5bc`; exact-head hosted run `42462640598` passed; registered-deployment execution regression remains missing.

## Publication witnesses

Pre-publication remote output:

```text
e6b26ac982f074016ba4c03d918910149f770796\trefs/heads/main
07ae6c3e91b081a189266ca4b162ba705d4aa78f\trefs/heads/develop
b69c096242a8940f5365b683532313a4fb89e5bc\trefs/pull/1459/head
```
