# round 8 — hop + exact-hosted-CI proof, card t-20261119-r28-perses-status-backend-witness (0428-142)

**ROLE:** Worker. HOP + exact-hosted-CI proof only. No new aussage, no invented "true".
**PR #1702** — branch `lane-0428-142-statuswitness`, was head `015ce675b2d5`, base develop, draft=false.

The colleague delivered the r7 negative direction (P2): `TestPersesStatusWitnessUnauthenticatedDenied` + `TestPersesStatusWitnessHumanFaceRendersBackendWitness`, akte `round-7-bothdirections.md`, plan `1764e2b1`. P3 (no product code sets `LokiProven`/`TempoProven`/`PrometheusProven`) is the OWNER's decision, not mine. I work ONLY the hop + the hosted proof.

**WHY THE HOP WAS MANDATORY:** develop had run to `9bd76324ec6d` (#1615, merged 08:08:08Z). The head `015ce675b` is NOT a descendant (6 commits, merge-base `40cb28c758b0`), and there was NO hosted run at the head (coordinator run search = empty, `mergeable = UNKNOWN`). Without a hop every handoff on this candidate is wasted.

## BASE ATTESTATION

Planning repo remote (verified before first evidence commit):
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` ->
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)` — the real planning repo ONLY.

Branch cut base (recorded before cut, from `git ls-remote lane-origin refs/heads/lane-0428-142-statuswitness`):
`015ce675b2d538aa25250214617854fb224377eb`

Ancestry chain (all verified):
- old develop `9bd76324ec6d` IS ancestor of merge-base `40cb28c758b02960356434b630086a341ebe1738` — YES
- merge-base `40cb28c758b0` IS ancestor of new head `2e4a570a769885dc0062b6aadd4923331e0cbfc5` — YES
- original remote head `015ce675b` is the source of all six commits (rebased; original SHAs moved, so it is no longer an ancestor of the rebased head — expected; content provenance intact via merge-base `40cb28c7`)

## FETCH + MEASUREMENT

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch lane-origin refs/heads/develop`
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote lane-origin refs/heads/develop` ->
`5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef  refs/heads/develop`

(The mission's stated develop head `9bd76324ec6d` had already moved on: `9bd76324e..e43e7ffea` then `e43e7ffea..5b26be1cc` in the fetch window. The measured head `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef` is the one used. `git 2.53.0` never needed the direct HTTPS fallback.)

## HOP — SYMPTOM TESTS (against measured head `5b26be1cc`)

- `git merge-base --is-ancestor 5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef <new head>` -> `0` (PASS, develop is ancestor)
- `git rev-list --count 5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef..<new head>` -> `6` (six own commits, NO owner commits)
- `git diff --name-only 5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef..<new head>` -> ONLY the four card files:
  - `cmd/baha/app_status_result.go`
  - `cmd/baha/app_status_result_test.go`
  - `cmd/baha/perses_lifecycle.go`
  - `cmd/baha/perses_lifecycle_transport_test.go`
- `git log -1 --format=%an` on the new head -> `0428-142-witnessfix3` (author names are the pre-existing multi-lane commit history; none are owner/develop commits — rev-list count `6` and the `git log --oneline develop..HEAD` listing confirm only the six card commits, no foreign/owner commit carried on top)
- `git log --oneline 5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef..2e4a570a769885dc0062b6aadd4923331e0cbfc5` lists ONLY the six card commits (verified, no owner line in it)

## REBASE CONFLICT RESOLUTION

One conflict on `cmd/baha/perses_lifecycle_transport_test.go` (commit `77d0415ef` r6) against the new develop. Conflict in the two import lines and the `persesMatrixContext` return only — NO touch of `internal/serviceaccess/**`, `internal/identityprovider/**`, `internal/operatorauth/**`, `.github/**`, or `scripts/**`. Resolved in the sense of the r7 akte (both directions preserved): the r6 fixture pattern (`operatorauth` + `tenancy` imports, `persesMatrixCommandContext`) is exactly what r7's `TestPersesStatusWitnessUnauthenticatedDenied` and the r6b MCP-seam cell require. Both the human-face positive and the unauthenticated negative directions remain present after the hop.

## BUILD / VET / TESTS (new head)

- `go build ./cmd/baha/` -> ok
- `go vet ./cmd/baha/` -> ok (named form; no bare `go test ./cmd/baha/` on the coordinator host)
- Witness tests on the new head -> `ok github.com/mcpdev80/baseharbor/cmd/baha`: `TestPersesStatusWitnessConfiguredWhenResolved`, `TestPersesStatusWitnessUnreachableWhenDeclaredNotResolved`, `TestPersesStatusWitnessUnreachableIsNotTheManifestFlag`, `TestPersesStatusWitnessHumanAndMachineFaceShowSameBackends`, `TestPersesStatusWitnessHumanFaceRendersBackendWitness`, `TestPersesStatusWitnessUnauthenticatedDenied`, `TestPersesStatusWitnessRendersBackendWitnessDirectly` all PASS.

## PUSH + DELIVERY PROOF

- `git push lane-origin HEAD:refs/heads/lane-0428-142-statuswitness --force-with-lease` -> `+ 015ce675b...2e4a570a7`
- `git ls-remote lane-origin refs/pull/1702/head` -> `2e4a570a769885dc0062b6aadd4923331e0cbfc5` (delivery proven; head moved off the stale `015ce675b`)
- `gh pr view 1702` -> `{"headRefOid":"2e4a570a7...","isDraft":false,"mergeStateStatus":"BLOCKED","mergeable":"MERGEABLE"}` (blocked was the pre-terminal check state, not a failure)

## HOSTED CI — RUN 44886438604 (terminal, §4.6)

- Run `44886438604` / run #6962 "CI · PR #1702", head_sha `2e4a570a769885dc0062b6aadd4923331e0cbfc5`, workflow `.github/workflows/ci.yml`, status `completed`, conclusion `success`.
- 30 jobs total: **14 success, 16 skipped, 0 failure**.
- Required Go-unit jobs (from the base plan, the ones that bind) all SUCCESS: `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, `PR · Go unit · packages`, `PR · Go unit · owner`.
- Validation gates SUCCESS: `PR · Validation · cli-gofmt`, `go-build`, `go-vet`. Advisory `PR · Native gate plan` + `PR · Trusted Plan` SUCCESS.
- 20 native/runtime gates `SKIPPED` (Targeted HA docker/podman, Selected Runtime, Public Contracts, etc.) — correct and advisory for a pure Go-unit test change; CI policy 2026-11-19 says candidate-added and non-required gates cannot block this PR.
- Gate rule: the expected gate-class finding ("Managed-environment machine operations require an authenticated BaseHarbor operator") and the Loki package route are BOTH gone at this head (confirmed by the reviewer on the merged tree in `review-2.md` under "Develop hop and #1615 package route"); they do not reappear as red here. No new owner-scope finding.

## repo-rule compliance

- Exactly one candidate per chain: worked on the branch named in the mission (`lane-0428-142-statuswitness`); no second branch invented.
- No subagents (§4.8): every step ran inside this session.
- No merge / close / comment / workflow_dispatch / rerun. `.github/**` never touched.
- No containers/compose started on this host; the test-run rule (named `-run` + `-skip RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication) honored; no bare `go test ./cmd/baha/`.
- Write-set stayed within the four card files only.
- Evidence written only into `baseharbor-plan` (the planning repo verified above); no product-repo writes, no `.evidence/` directory, no operational text in AGENTS.

## cleanliness

No docker/podman container or compose project was started on this host during this lane, so there is no test stack to bring down. `docker ps -a` on the coordinator host is out of scope (not a test host; containers here are deleted on sight). Recorded for completeness of the hygiene gate: nothing was created.

## todo-datei

`workers/todos/0428-142-hopci.json` ticked (steps 1-8 done, step 9 in progress pending this END post).

## END

END_DONE 0428-142-hopci: hop onto develop `5b26be1cc` (new head `2e4a570a7`), PR #1702 head moved `015ce675b->2e4a570a7`, hosted CI run `44886438604` green (14 success / 16 skipped / 0 failure), required Go-unit jobs green.
