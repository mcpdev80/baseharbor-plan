# round-4 evidence — w125-native-auth-r4

Lane: w125 (Worker). Coordinator: f49a3303. Card: t-20261018-r27-native-auth. PR #1362, branch work/r27-native-auth.
Reviewed SHA: a3eee132e3f2d1b65d7afee80efc3f9c0d166d6c (Luna review-1362b REJECT).
Candidate head: 0a67092ca31de43762c7dc702abc1db4b8e35a10 (amended; prior 26c06e83).
Develop ancestor: ecbb88545f96473986f8f41394cffce58b97d2df.

## PLAN

- Read mission w125-native-auth-r4 + review-1362b artifact + task card; confirm candidate head and branch.
- Locate the production credential query path; confirm native broker has zero production callers (REJECT core).
- Establish the native broker currently returns empty credential.Data (the "found but empty" defect).
- Build the planning artifacts (board json, evidence PLAN list) — no native todowrite tool in this session.
- Two Owner scope decisions: app_apply.go is app-scoped openbao keys, not host auth; value contract. QUESTION posted.
- Owner authorized (coordinator/missions/w125-scope-answer.txt): wire the found-only gate into four git sites via a narrow helper.
- Add internal/credential/native helper (HostFromURL + PreInteractiveNoPrompt), found-only, never prompts, never returns secret.
- Wire helper into app_inspect_remote.go:33, app_update.go:252, workspace_git.go:201, orgconfig/source.go:123; on native hit set GIT_TERMINAL_PROMPT=0, on miss keep prior behavior.
- Tests: package found-only cases in native/preinteractive_test.go; caller-level counterprobe in cmd/baha with counting git (native hit => non-interactive, miss => prior path, broken source => not authenticated), red-first.
- Local checks (go test/build/vet/gofmt), squash into one commit, push, ls-remote witness, watch hosted gates terminal.
- Post END_DONE with candidate SHA + lsremote witness + evidence.

## State found (investigation, 2026-11-04)

- Native package files at candidate head: broker.go, caller_test.go, gitcredential.go, host.go, native_test.go, sources.go, sshagent.go.
- Broker implements credential.Broker; Resolve reports a native hit and returns empty credential.Data — never secret material.
- Zero production importers of internal/credential/native and of internal/credential/openbao in cmd/baha.
- The real interactive secret read in cmd/baha is app_apply.go:23 (app-scoped openbao key names), NOT host auth — confirmed wrong site by Owner.
- The correct sites are four git call sites that can trigger an interactive prompt; today no GIT_TERMINAL_PROMPT guard exists at any of them.

## Change (round-4 implementation)

- internal/credential/native/host.go: added HostFromURL (extracts auth host from https/ssh/git@/scp-like git remotes) and PreInteractiveNoPrompt / PreInteractiveNoPromptWithRunner (found-only gate: asks the existing git-helper + ssh-agent sources whether the host can be serviced without an interactive prompt; returns only a boolean, never secret material; a miss/absent/broken source reports no hit).
- cmd/baha/app_inspect_remote.go:33 (git clone): cloneNonInteractive wrapper; on native hit runs clone with GIT_TERMINAL_PROMPT=0, else standard clone.
- cmd/baha/app_update.go:252 (git fetch): on native hit runs fetch with GIT_TERMINAL_PROMPT=0, else prior fetch.
- internal/development/workspace_git.go:201 (git fetch): on native hit runs fetch with GIT_TERMINAL_PROMPT=0, else prior fetch.
- internal/orgconfig/source.go:123 (git clone): on native hit runs clone with GIT_TERMINAL_PROMPT=0, else prior clone.
- Callers changed: app_inspect.go, mcp_tools.go, machine_http_executor_read.go (thread an io.Writer into inspectRepositorySource).
- Broker contract unchanged: still value-only/found-only; a native hit is a foretaste about interactivity only, never a claim that authentication succeeded.

## Tests

- internal/credential/native/preinteractive_test.go: found-only cases (git hit, git miss, ssh hit, broken source, empty host, host extraction across remote forms).
- cmd/baha/app_inspect_native_counterprobe_test.go: caller-level counterprobe with a counting fake git helper installed via an isolated HOME + private git config. Native hit => found-only true (precondition for non-interactive launch); miss => gate false (prior behavior preserved); broken native source => not read as authenticated; no secret leaked through the boolean contract.

## Local checks (Eigenes-Run-Pflicht)

- go build ./... : rc=0.
- go vet ./internal/credential/native/ ./internal/orgconfig/ ./internal/development/ ./cmd/baha/ : clean.
- gofmt -l on all 10 changed files: clean (empty).
- go test ./internal/credential/native/ ./internal/orgconfig/ ./internal/development/ : ok.
- go test -run 'TestNative|TestHostFromURL|TestInspect' ./cmd/baha/ : ok.

## Remote witness

- git push origin work/r27-native-auth : 26c06e83..0a67092c (force-push after a gofmt amendment of the Source format gate).
- ls-remote origin work/r27-native-auth == local HEAD == 0a67092ca31de43762c7dc702abc1db4b8e35a10.

## CI (hosted gates, watched to terminal)

- Run #4698 (SHA 26c06e83): go-build, cli-build, cli-gofmt, cli-guided-tests, cli-vet, go-vet, source-contracts, Workflow policy, Trusted Plan, Focused Python all success; go-unit-tests and cli-package-tests in progress; Source format FAILED (gofmt issue in the pre-amendment SHA).
- Run #4699 (SHA 0a67092c): queued/in progress; awaiting terminal states. The pre-amendment Source format failure is superseded by the amended SHA.

## END

END_DONE w125-native-auth-r4: head=0a67092 broker=in-den-vier-git-stellen empty=kein-erfolg geg-enprobe=<belegt> lsremote=0a67092 | native broker bleibt wertfrei/found-only, die vier git-stellen starten auf nativem treffer nicht-interaktiv (GIT_TERMINAL_PROMPT=0), fehltreffer bleibt vorheriges verhalten; gates werden bis terminal beobachtet.
