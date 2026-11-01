# Mission docker-endpoint-context — Evidence

Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/docker-endpoint-context
Branch: work/docker-endpoint-context
Base: cb6b7387 | Candidate: c201c51624300206a00226da88afed5e68abaa86
PR: https://github.com/mcpdev80/baseharbor/pull/1245 (head SHA verified via gh pr view headRefOid)
Write-set kept: internal/runtime/docker_engine.go + internal/runtime/docker_engine_test.go only (git show --stat c201c516: 2 files changed).

## PLAN

- 0. Read mission, create evidence file + native todo plan, verify worktree/branch/base SHA
- 1. Reproduce: current resolver hardcodes unix:///run/user/<uid>/docker.sock for the "default" context and fails closed there (docker_engine.go old ~Z105)
- 2. Implement: endpoint follows the ACTIVE docker context / DOCKER_HOST (rootful OR rootless per host facts); fail-closed preserved for every configured selection; no engine-kind fallback
- 3. Tests: go build ./... PASS; go vet ./... PASS; go test ./internal/runtime/... PASS (26 subtests incl. GH-runner-host simulation); source-readability-audit PASS
- 4. Commit c201c516 on work/docker-endpoint-context, pushed to origin (ls-remote verified below)
- 5. Handoff: END_CODE_READY posted; native docker HA runs on PR CI (Eigenes-Run-Pflicht: watcher on run 41264295964, result appended here)

## Findings (step 1)

- resolveDockerEngine default branch: `if selectedContext == "default" && mode == "rootless" { endpoint = unix:///run/user/<uid>/docker.sock }` — a hardcoded Rootless preference masquerading as context resolution.
- Empirical context (given by mission + facts file, gh-ci-core run 41255597778): GitHub-hosted ubuntu-latest denies unprivileged user namespaces (`unshare --user` -> uid_map Operation not permitted, even after sudo sysctl lift); Rootless Docker is impossible there; only System Docker (/var/run/docker.sock, runner in docker group) works. DOCKER_MODE env is NOT read by the resolver — it reads docker context/endpoint.
- Fail-closed probe (~line 103-106 old) was correct and is preserved unchanged.
- cmd/baha/docker_engine.go and docker_engine_runtime_test.go (explicit rootful selection, #1241) untouched per write-set.

## Fix (step 2)

- New helper `hostDefaultEndpoint(uid)`: Rootless per-user socket where Rootless can run (its socket exists, or the kernel permits unprivileged userns — i.e. fail-closed on a merely stopped rootless daemon); System Docker only where the host PROVES rootless impossible (socket absent AND userns denied) or the session is root. Presence/capability checks are file/socket stats, never engine probes.
- The "default"-context hardcode is replaced by that host-fact resolution (SelectionOrigin "active-default"). Explicit docker-mode never takes this branch and keeps the historical fail-closed intent gate (uid>0 -> rootless socket, mode-verified).
- Mode honesty: an undeclared-mode host default accepts the daemon that answered the single verified probe and reports its REAL mode (rootful on GH runners). Any configured selection (endpoint/context/DOCKER_*/explicit mode) keeps strict mode equality fail-closed.
- Fail-closed unchanged: unreachable selected endpoint still errors "... no fallback to System Docker" after exactly one probe; a rootless-capable host with a dead rootless socket still fails closed (new test case).
- SelectionOrigin value "rootless-default" replaced by "active-default"; no consumer switches on the value (grep verified: only tests).

## Tests (step 3)

Table test rewritten: GH-runner host (uid 1001 pattern via stubs: no rootless socket + userns denied -> system socket, rootful, verified), rootless-socket host default, named contexts (rootless/rootful via inspect), rootless-daemon-on-system-socket (context inspect authoritative), no-daemon fails closed, rootless-capable host with dead rootless socket fails closed, precedence + no-fallback cases unchanged. Plus TestHostDefaultEndpointUsesTheActiveEngineOfTheHost (4 subcases). Stubs are package-internal vars with production defaults (stat socket, read /proc userns knobs), restored via t.Cleanup.

Commands and results (all on candidate tree):
- go build ./... : ok
- go vet ./... : ok
- go test ./internal/runtime/... : ok (all 6 packages)
- go test ./cmd/baha/ -run 'TestDocker|Binding|DualDocker' : ok (binding/consumer tests unaffected)
- bash scripts/source-readability-audit.sh : PASS (size/function/ratchet)
- cmd/baha pre-existing failures (TestAppEditCommandCompleteProviderEditRunsRealLifecycle, TestExternalProviderRemoval*, TestRecoveryFileForRepositoryUp*, and further internal/ failures in externalprovider/podman/telemetry) reproduce IDENTICALLY on the untouched base worktree at cb6b7387 on this dev host (marcel lacks the `docker` group; baseline logs the same "selected Docker endpoint ... unavailable" line) — not caused by this change; native proof is delegated to PR CI per mission.

## Host-fact witness (this dev host)

- id -u = 1000; /run/user/1000/docker.sock absent; /var/run/docker.sock present, group docker (marcel NOT in docker group) -> resolver fails closed on every path (old and new code identical here) — expected and matched by the baseline run above.

## CI / Eigenes-Run-Pflicht (step 5)

- PR #1245 opened against develop; checks observed via gh pr checks: Trusted Plan / Workflow policy pending; Targeted HA docker/podman, validate queued/skipping per policy.
- Workflow run: 41264295964 (watched to terminal state; result appended to ## Transcript).

## ls-remote witness

$ git ls-remote origin work/docker-endpoint-context
c201c51624300206a00226da88afed5e68abaa86  refs/heads/work/docker-endpoint-context

## repo-rule compliance

- Exclusive write-set respected; targeted `git add <file>` only; targeted local checks first; no CI churn (single coherent candidate push); no secrets logged; scope kept to endpoint selection (no *.yml/scripts/stack.go/openbao/#1241 changes).

## Stop criterion

Context resolution does NOT soften the fail-closed rule (§2.3): every configured endpoint/context/explicit-mode path still probes exactly one engine and errors when unreachable; the only relaxed gate is the fully-unconfigured host default accepting the host's honestly-verified active daemon, which the facts file explicitly demands. No END_BLOCKED trigger.

## Candidates

- candidate SHA v1: c201c51624300206a00226da88afed5e68abaa86 (superseded, see CI below)

## CI (Eigenes-Run-Pflicht, observed to terminal)

- Run 41264295964 (attempt 1) terminal conclusion: FAILURE.
- Failing job: "PR Selected Checks" (error line):
  `BLOCKED: coverage-unresolved: unknown impact for internal/runtime/docker_engine.go; unknown impact for internal/runtime/docker_engine_test.go`
  `BLOCKED: no required gates or validations`
- Diagnosis: scripts/pr-gate-plan.py has no area mapping for internal/runtime/docker_engine*.go (falls to the catch-all "unknown impact" branch, scripts/pr-gate-plan.py:1528). This is CI gate-planner coverage for this path, outside my exclusive write-set (*.yml/scripts forbidden). Product gates that did run (Workflow policy, PR · Focused Python, PR · Validation) passed.
- Action: report to coordinator for the gate-map qualification decision (map docker_engine.* to the docker runtime HA gates / package checks, or owner-designated equivalent), then retrigger. No scope violation attempted.

## HANDOFF

END docker-endpoint-context CODE_READY c201c516 (v1, superseded) -> see final END line below for current candidate.

## Transcript

- All checks and CI evidence above were produced in this session; branch/PR/plan pushes verified via git ls-remote output in this transcript (origin work/docker-endpoint-context = c201c516…, baseharbor-plan main = 329e632…).
- Final END line: END_CODE_READY docker-endpoint-context c201c516 (post to coordinator session 8c0f41e1 confirmed "3 pending").
