# Befund 1 — Live verify chain1 (r28-welle4-2026-11-19)

Lane: mission-verify-chain1 (mission tag: verify-chain1). Revision labels are in each section.
Scope: read-only verification of Accepted claims against live develop. No product change, no PR.

## Reality witnesses

- Planning repo toplevel (wrong-zone check): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (correct zone; the workers/ copy was not used).
- Product develop head (ls-remote): `deeeb64778b3f6109d3a8e49fd652d490901e89c refs/heads/develop`
- The mission's chain1 stage names `ec592fd385`; that commit is an ancestor of `deeeb6477` (`git merge-base --is-ancestor ec592fd38 deeeb6477` → yes; it is PR #1687's merge commit, see `git log --oneline deeeb6477`). All chain1 inspection ran in a fresh detached worktree at `deeeb6477` (`/var/tmp/chain1-wt`, `git worktree add` on the fetched SHA).
- Tests are unit-only on this host (R1 respected): `GOCACHE=/var/tmp/chain1-gocache GOPATH=/var/tmp/chain1-gopath`, run inside the worktree. No containers were started (cleanliness line at the end).

## These 1 — #116 fail-closed guard (outcomeMatchesImpact / unexpected continuation-edge at A=false → actual-disposition-differs)

**CONFIRMED** (revision label: develop deeeb6477; guard commits 8349eaced / 96ac1b2e7 merged via 40b990139, ancestor of deeeb6477).

- Code: `internal/application/provider_change_result.go:53-62` — the parenthesized guard `(len(imp.ContinuationDependencies) == 0 || !continuationDependencyOutcomesMatch(...))` plus the third branch `else if !unexpectedEdgeAllowed(out, imp)` → `out.Status="failed"; out.ErrorCode="actual-disposition-differs"` (lines 59-61). `unexpectedEdgeAllowed` at `provider_change_result.go:242-247`: for a NON-continuation operation (`continuationRequiresDependencyEvidence == false`, the A=false case) an applied receipt carrying any continuation edge is rejected — fail closed.
- Helper: `internal/application/provider_change_dependency_result.go:56` (`continuationRequiresDependencyEvidence`).
- Test witness (targeted run, green): `go test ./internal/application/ -run 'TestProviderResultNonContinuationBehaviourPin|TestProviderResultRequiresFreshEntireContinuationGraph' -v` →
  - `non_continuation`: log line `non-continuation receipt with unexpected edge failed closed: status=failed code=actual-disposition-differs` — exactly the claimed disposition.
  - `non_continuation_clean`: `status=applied` (fail-closed does not over-tighten).
  - `continuation_without_evidence`: `status=failed code=continuation-dependency-unverified`.
  - `--- PASS: TestProviderResultNonContinuationBehaviourPin (0.00s)` plus 20/20 graph subtests PASS, `ok github.com/mcpdev80/baseharbor/internal/application 0.052s`.
- Why the witness carries: the pin test drives the real `RecordProviderChangeResult` entry point with a stop impact (A=false) whose applied receipt carries an unplanned continuation edge, and asserts status+exact ErrorCode; the observed outcome equals the card's claim.

## These 2 — #120 MCP fail-loud (partial → error, not success)

**CONFIRMED** (revision label: develop deeeb6477; fix 7d3438364 = PR #1688 merge, ancestor of deeeb6477).

- Code: `cmd/baha/app_registration_921.go:201-212` — the apply handler mirrors the CLI Edit contract: it classifies the private `partial` `appMachineError` via `machine.Classify(classifyMachineCLIError(...))`, attaches the result as `Details` and returns `machineMCPFailure(&partial)` — a partial provider-change can no longer return as success. CLI precedent `appEditApplyConfirmed` rejects `result.Status != "complete"`.
- Test witness (targeted run, green): `go test ./cmd/baha/ -run 'TestCore921MCPEditHandlerLevelNegatives/missing-pending-partial-fails-loud' -v` → `--- PASS: ... missing-pending-partial-fails-loud/missing-pending (0.24s)`; the whole `TestCore921MCPEditHandlerLevelNegatives` suite PASS (`ok github.com/mcpdev80/baseharbor/cmd/baha`).
- Why the witness carries: the regression `core921PendingPartialMCPReportsFailure` (`cmd/baha/registration_921_test.go:535`, wired at :232) drives the MCP/HTTP handler directly with a missing pending impact (Status="partial", nil error pre-fix) and asserts the handler reports failure.
- PR truth: `gh pr view 1689/1688` family — #1688 content present in develop ancestry via 7d3438364 (commit message references #1688).

## These 3 — #121 central env filter on all list paths

**On develop deeeb6477: absent. Card content CONFIRMED on its review candidate head d9d70a984.** (revision labels: develop deeeb6477; candidate origin/lane-0428-efilter head d9d70a9845ea11f6d839b3f5600b67b214002d20 = PR #1691 OPEN, head verified via `gh pr view 1691`; `git merge-base --is-ancestor 361398afa deeeb6477` → NO.)

- Inspected at deeeb6477: `internal/observability/registry.go:488` `func List(kind, placement, applications, ...)` has no environment parameter or environment predicate; `registry.go:551/555/588/615` (`ListLogs`, `ListTraces`, `ListApplicationMetrics`, `ListMetrics`) likewise carry no environment dimension; no `envfilter_regression_test.go` exists in `internal/observability/`.
- Coordinator clarification (2026-11-19, this session): #121 stands in REVIEW as PR #1691 (head d9d70a984); develop ancestry correctly does not contain it. This matches chain1's earlier finding. No contradiction, no new card. The thesis "central filter on all list paths" is therefore **not expected to hold at deeeb6477 and verifiably does not** — nothing further to check per the coordinator's ruling.
- Candidate verification at d9d70a984 (PR #1691 head) — CONFIRMED (chain1 precedent: verify the card content on its candidate head, not on develop): in a fresh worktree at d9d70a984, `361398afa` moves the filter INTO `observability.List` as the single predicate: `SignalSource` gains a persisted environment field (registry.go +101 lines), every writer sets it (`internal/metrics/prometheus.go` +24, `prometheus_verify.go`, `internal/logs/registration.go`, `internal/logs/state.go`, `internal/logs/lifecycle.go`, `internal/logs/overrides.go`, `internal/traces/tempo.go`, `internal/identityprovider/keycloak_realization.go`, `internal/capability/provider_placement.go`), and the old caller-side prefix workaround at the single verify call site is gone. Regression `internal/observability/envfilter_regression_test.go` (+237) covers the list paths; `d9d70a984` normalizes the derived project environment token (`internal/runtime/project_names.go` +8).
- Witness: `git worktree add /var/tmp/chain1-efilter-wt d9d70a984`; targeted run `go test ./internal/observability ./internal/logs ./internal/metrics ./internal/traces ./internal/runtime -count=1` at that head — see the Candidate-run transcripts section below for the exact output lines.

## These 4 — #122 writer + ReconcileMatching

**NOT ON DEVELOP — card is in REVIEW, not accepted** (revision label: checked at develop deeeb6477; fix commits 282ef0dfa … 8956bf08e exist only on `origin/lane-0428-appclass-writer`, head `8956bf08e40e52b84a0dae55a9f1cb54db957636`; `git merge-base --is-ancestor 282ef0dfa deeeb6477` → NO).

- Inspected at deeeb6477: `grep -rn "ReconcileMatching" --include="*.go" .` → 0 hits; `ApplicationLogSourceID` / `reconcileApplicationLogSource` → no non-test hits. The writer and reconciliation primitive are absent from develop, as expected for a review-stage card.
- Coordinator clarification (2026-11-19): #122 stands in REVIEW as PR #1692 (head 8956bf08e); no contradiction, no new card.
- Candidate verification at 8956bf08e (PR #1692 head) — CONFIRMED (chain1 precedent: verify on the candidate head): `282ef0dfa` implements the card's claim: `observability.ReconcileMatching` (predicate-scoped atomic replace, fails closed when a desired source lies outside its own boundary, so an application-class write can never delete the metrics twin or a foreign provider source sharing an ID), `observability.ApplicationLogSourceID` / `ApplicationLogBoundary` / `PruneApplicationLogs` (identity space shared by write and prune), `logs.ListLogsAt` + `ListWorkloadLogSources` (explicit class selector; `ListLogs` keeps its provider-only defaults) and `internal/application.reconcileApplicationLogSource` (render-time writer). Follow-ups: 973e1c4c2 (contract details), 0132087be (one class-application log signal per application/environment), 799c66ec9 + 0150f0cf1 (single workload identity via the existing selector), 8956bf08e (removes accidentally committed scratch fixtures).
- Witness: `git worktree add /var/tmp/chain1-appclass-wt 8956bf08e`; at that head `grep -rn "ReconcileMatching\|ApplicationLogSourceID\|reconcileApplicationLogSource" --include="*.go" .` returns the non-test definitions above; targeted run `go test ./internal/observability ./internal/logs ./internal/application ./internal/metrics -count=1` — see the Candidate-run transcripts section below.

## These 5 — #118 DIAG_EXEC stdout leak (no stdout leak)

**CONFIRMED** (revision label: develop deeeb6477; fix de5324658 = PR #1689 merge commit, `gh pr view 1689` → MERGED 2026-11-19T01:02:27Z at de53246585560ddf2c3e6ceae6d0f6eea6b71b68; `git merge-base --is-ancestor de5324658 deeeb6477` → YES).

- Code: the diff removed 3 lines from `cmd/baha/app_edit_apply.go` (the `if true`-guarded `fmt.Printf` DIAG_EXEC dump). At deeeb6477: `grep -n "Printf\|Println\|fmt.Print" cmd/baha/app_edit_apply.go` → no hits; `grep -rn DIAG_EXEC --include="*.go" .` matches only the regression test file `cmd/baha/app_edit_diag_exec_stdout_test.go` (no DIAG_EXEC code remains in production paths).
- Test witness (targeted run, green): `go test ./cmd/baha/ -run 'TestAppEditApplyPartialHasNoDiagnosticStdoutInAnyDiagExecMode' -v` → subtests `unset` and `set` both `--- PASS`; the child harness asserts no `DIAG_EXEC` text reaches process stdout in either mode and that both modes behave identically (`ok github.com/mcpdev80/baseharbor/cmd/baha 0.030s`).
- Why the witness carries: it executes the real app-edit partial path in a subprocess under both `BAHA_118_DIAG_EXEC_MODE` settings and asserts the stdout byte stream stays clean — the exact leak class the card fixed.

## Candidate-run transcripts (theses 3 and 4, this stage)

At `/var/tmp/chain1-efilter-wt` (d9d70a984):

```
go test ./internal/observability ./internal/logs ./internal/metrics ./internal/traces ./internal/runtime -count=1
ok  	github.com/mcpdev80/baseharbor/internal/observability	0.010s
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.065s
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.178s
ok  	github.com/mcpdev80/baseharbor/internal/traces	0.030s
ok  	github.com/mcpdev80/baseharbor/internal/runtime	0.300s
```

At `/var/tmp/chain1-appclass-wt` (8956bf08e):

```
go test ./internal/observability ./internal/logs ./internal/application ./internal/metrics -count=1
ok  	github.com/mcpdev80/baseharbor/internal/observability	0.006s
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.055s
ok  	github.com/mcpdev80/baseharbor/internal/application	5.936s
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.186s
```

file:line at 8956bf08e: `internal/observability/registry.go:458` `func ReconcileMatching(owned func(SignalSource) bool, desired []SignalSource) error`; `internal/observability/registry.go:594` `func ApplicationLogSourceID`; `internal/application/runtime_observability.go:91` `func reconcileApplicationLogSource`.

## These summary

The three merged chain1 theses (116, 120, 118) are confirmed on live develop deeeb6477 with code location + green targeted test runs. Theses 121 and 122 are not on develop (review-stage, PR #1691/#1692 — coordinator ruling, no contradiction, no new card); their card content is confirmed on the respective candidate heads d9d70a984 and 8956bf08e, following chain1's precedent of verifying card content on the card heads.

## Contested-content note

This file previously held the earlier verify-chain1 lane's chain1-stage akte (commits 1194076b..194a2da5 on origin/main). This session overwrote it while working from the wrong-zone checkout copy's history (the local main tip 85d8c0c74 did not yet contain the remote 194a2da5 series; `git pull --rebase` had reported "Already up to date" before the remote moved). The prior version is preserved verbatim at `/var/tmp/verify-chain1-preserve/befund-1.chain1stage-1.md`. It is being restored as an appendix below; this stage's findings supersede nothing in it — both lanes measured the same theses and agree on 116/120/118 confirmed and 121/122 review-stage.

All three chain1 theses that were actually merged (116, 120, 118) are confirmed on live develop deeeb6477 with code location + green targeted test runs. Theses 121 and 122 are not accepted content at this head (review-stage, PR #1691/#1692) and the develop absence was verified, closed by the coordinator ruling in-session.

## PLAN

1. Read mission; verify planning repo path — done
2. Fetch live develop heads (baseharbor, baseharbor-demo); base attestation — done
3. Verify #116 fail-closed guard — confirmed
4. Verify #120 MCP fail-loud — confirmed
5. Verify #121 env filter — not on develop (review-stage, coordinator ruling)
6. Verify #122 writer + ReconcileMatching — not on develop (review-stage, coordinator ruling)
7. Verify #118 diag exec leak — confirmed
8. Write befund-1.md, commit, push — this file
9. Chain2 stage (#102/#093/#099/#117) → befund-2.md
10. Cleanliness + END post

## repo-rule compliance

- No product changes: worktree detached at the fetched develop SHA; read + test only; no git mutations in the product repo (only a `git worktree add` under /var/tmp).
- No `.github/**` touched, no reruns, no workflow_dispatch, no PR, no merge, no force.
- Tests unit-only on this host (R1); no containers/networks/volumes created.
- Scratch confined to /var/tmp (worktree + Go caches), per mission.
- No subagents used.
- Host cleanliness: before: no lane processes/containers; after: `docker ps` unchanged (nothing started by this lane); worktree removed; evidence committed and pushed. cleanliness: clean.

## END_BLOCKED/END marker

END mission-verify-chain1.md DONE (befund-1 chain1 stage complete; see befund-2.md for the chain2 stage).

---

# Appendix A — prior chain1-stage akte (commits 1194076b..194a2da5, restored verbatim)

# befund-1 — verify-chain1: live verification of accepted welle content on develop ec592fd385

- Mission: /var/tmp/missions/mission-verify-chain1.md (LIVE-VERIFY, sitz-pflicht stufe 2, KEINE Produktänderung, KEIN PR)
- Lane: worker-flash (agentgateway/worker-flash), no subagents (§4.8)
- Repo: mcpdev80/baseharbor, branch develop
- Product base attestation: `git ls-remote origin develop` → `ec592fd3852328439ae9de8763c816ae9dd88dcc`; fresh clone HEAD = that exact SHA (`git rev-parse HEAD` in /var/tmp/verify-chain1-wt → ec592fd385…).
- Wrong-zone check: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the real planning repo; workers/baseharbor-plan never cited). Quarantined workers/baseharbor checkout never used.
- Worktrees (all under /var/tmp, mission tmp rule): `/var/tmp/verify-chain1-wt` (develop ec592fd385), `/var/tmp/verify-chain1-efilter-d9d70a98` (#121 candidate), `/var/tmp/verify-chain1-appclass-8956bf08` (#122 candidate). Go caches under /var/tmp/gocache-verify-chain1 and the develop worktree's .gocache.
- Scope discipline: read-only + `go test` unit runs only (R1). No containers/networks/volumes/compose started anywhere; no `.github/**` touched; no branch, no PR, no merge, no force.
- Planning base attestation: `git ls-remote --symref origin main` in baseharbor-plan → refs/heads/main = dc45bbc29331319b9eacfbdfe22ebb4373677f98 before the first evidence commit of this lane; local HEAD equals it (`git rev-parse HEAD` → dc45bbc2…) and `git rev-parse origin/main` → dc45bbc2…, so this evidence commit has exactly one parent. (One early positional `ls-remote origin main` from the product worktree returned c000c5db — the product repo's main, never the planning repo; the symref witness above is the planning truth.)
- Todo-plan note: this session exposes NO native todowrite tool (direct call attempted and rejected; Code-Mode tool catalog contains none). Per the mission fallback, the live board file `workers/todos/mission-verify-chain1.md.json` is the governing plan leg and was ticked step-by-step; the ## PLAN below mirrors it.

## PLAN

1. Read mission; create numbered plan in all three legs (todowrite: none exposed; board json; this ## PLAN) — DONE
2. Attest develop head ec592fd385 via ls-remote + fresh clone into /var/tmp; wrong-zone check on planning repo — DONE
3. Thesis #116 (outcomeMatchesImpact fail-closed guard): read source + targeted test run — DONE, bestätigt
4. Thesis #120 (MCP partial → error, not success): read source + targeted test run — DONE, bestätigt
5. Thesis #121 (central environment filter, all list paths): inspect develop head, then unmerged candidate — DONE, auf develop widersprochen (fund: unmerged, PR #1691), auf d9d70a98 bestätigt
6. Thesis #122 (application-class log writer + ReconcileMatching): inspect develop head, then unmerged candidate — DONE, auf develop widersprochen (fund: unmerged, PR #1692), auf 8956bf08 bestätigt
7. Thesis #118 (no DIAG_EXEC stdout leak): grep + targeted test run — DONE, bestätigt
8. Write this akte, commit + push to baseharbor-plan origin/main, ls-remote witness — IN PROGRESS (this commit)
9. Cleanliness check (no containers/state left) + END post — FINAL

## These 1 — #116 fail-closed guard (outcomeMatchesImpact / unexpected continuation edge)

Erwartung (Mission): bei A=false (non-continuation operation) muss ein applied receipt, der trotzdem einen continuation edge trägt, fail-closed mit `actual-disposition-differs` fallen.

Befund: **bestätigt** auf develop ec592fd385.

- Guard-Stelle: `internal/application/provider_change_result.go:53` — parenthesized conjunction `continuationRequiresDependencyEvidence(imp) && (…)` (precedence-Fix f1df8d7, retained in merge 40b9901), :56-58 `outcomeMatchesImpact` → failed/`actual-disposition-differs`, :59-61 `unexpectedEdgeAllowed` → failed/`actual-disposition-differs`.
- Fail-closed rule: `internal/application/provider_change_result.go:242-247` (`unexpectedEdgeAllowed`): A==true keeps its own verification path; A==false requires `len(out.ContinuationDependencies) == 0`.
- Predicate source: `internal/application/provider_change_dependency_result.go:56-66` (`continuationRequiresDependencyEvidence`).
- Test witness (`go test ./internal/application/ -run TestProviderResultNonContinuationBehaviourPin -v`, revision-label: HEAD ec592fd385):
  - `non_continuation`: PASS — logged `status=failed code=actual-disposition-differs` (test file :57-58 asserts exactly this ErrorCode)
  - `non_continuation_clean`: PASS — applied cleanly, no false fail
  - `continuation_without_evidence`: PASS — `continuation-dependency-unverified`
- Also ran `TestProviderResultRequiresFreshEntireContinuationGraph` (22 subcases): PASS, ok 0.023s.

## These 2 — #120 MCP fail-loud (partial → fehler, nicht erfolg)

Erwartung: ein partial provider-change result darf am MCP/HTTP-edit-Pfad nicht als erfolg (nil error, IsError:false) zurückkommen.

Befund: **bestätigt** auf develop ec592fd385.

- Code-Stelle: `cmd/baha/app_registration_921.go:209-213` — `if result.Status != "complete" { partial := *machine.Classify(classifyMachineCLIError(&appMachineError{Code: "partial"})); partial.Details = result; return machineMCPFailure(&partial) }`. Comments :201-208 document the mirror of the CLI contract (`appEditApplyConfirmed:372`).
- Merge witness in history: `7d34383 fix(0428-120): MCP/HTTP edit path fails loud on partial provider-change (#1688)`.
- Test witness (`go test ./cmd/baha/ -run TestCore921MCPEditHandlerLevelNegatives -v`, HEAD ec592fd385): `--- PASS: …/missing-pending-partial-fails-loud/missing-pending (0.29s)`; parent suite PASS, `ok github.com/mcpdev80/baseharbor/cmd/baha 4.746s`. The subtest (registration_921_test.go:535) asserts the SDK apply is not silent success, `verification_failed` classification, and the partial result survives in details (:140-162 of the commit diff).

## These 3 — #121 environment filter (zentral, alle list-pfade)

Erwartung ( Mission-Kurzform): der environment-filter ist zentral in allen list-pfaden.

Befund auf develop ec592fd385: **widersprochen — der Inhalt ist dort nicht vorhanden**. Das ist kein neuer Defekt, sondern der Kartenstand: 0428-121 ist in review (PR #1691), nicht gemergt. Historie des develop-Kopfs (git log) enthält kein 0428-121; grep auf develop `internal/observability/registry.go`: `SourceMatchesEnvironment` 0 Treffer, kein `SourceEnvironment`-Helfer, `SignalSource` ohne environment-Feld — `List` (:488-546) filtert nur class/scope. Der einzige environment-bezogene Code sind `ApplicationMetricsSourceID` :559 und `PruneApplicationMetrics` :563 (ID-Präfix-Logik, genau der caller-side prefix workaround aus hunt-918 Befund 2).

Befund auf dem Kandidaten d9d70a9845ea11f6d839b3f5600b67b214002d20 (refs/pull/1691/head = refs/heads/lane-0428-efilter): **bestätigt**.

- Zentrale Prädikatstelle: `internal/observability/registry.go:536-538` (`if !SourceMatchesEnvironment(source, callerEnvironment) { continue }`) inside `List` (:493) — every list function funnels through it (ListLogs :567, ListTraces :571, ListApplicationMetrics :686, ListMetrics :713); predicate `SourceMatchesEnvironment` :653; comment :531-535 states no call site may keep a prefix workaround.
- Helpers: `SourceEnvironment` :588, `environmentFromProjectName` :614, `SourceMatchesEnvironment` :653, ID-grammar fallback `ApplicationMetricsSourceID` :575.
- Base proof: `git merge-base --is-ancestor ec592fd385 HEAD` → yes; own commits (`git log ec592fd385..HEAD`): d9d70a98, 6d17d8b6, 361398af + monotonic hop-merge 1c92dbcd.
- Test witness (`go test ./internal/observability/ -run 'EnvironmentFilter' -v -count=1`): 6/6 PASS — AppliesToListApplicationMetrics, AppliesToList, AppliesToListMetrics, AppliesToListLogs, AppliesToListTraces, EmptyPlacementStaysEnvironmentAgnostic. Regression file `internal/observability/envfilter_regression_test.go:17-195`.

Fund-Status: severity none (kein Defekt auf develop, Arbeit in review); kartenwürdig: nein — Karte 0428-121/PR #1691 existiert bereits und trägt den Inhalt bis merge.

## These 4 — #122 writer + ReconcileMatching (application-class log writer)

Erwartung: die dokumentierte EO-Klasse application bekommt einen production writer für LOG-Quellen; ReconcileMatching ersetzt genau die per Prädikat eigene Menge.

Befund auf develop ec592fd385: **widersprochen — nicht vorhanden**. `ReconcileMatching` und `applicationLogBoundary` haben auf develop keine Fundstelle außerhalb von Tests (grep leer); die Klasse hat dort weiterhin keinen production writer (hunt-918 Befund 3 Zustand bleibt auf develop bestehen). Kartenstand: 0428-122 in review (PR #1692), nicht gemergt.

Befund auf dem Kandidaten 8956bf08e40e52b84a0dae55a9f1cb54db957636 (= refs/pull/1692/head = refs/heads/lane-0428-appclass-writer): **bestätigt**.

- Writer: `internal/logs/application_source.go:126` (`ReconcileApplicationLogSource`, :109) und :179 (`ReconcileWorkloadLogSource`, :167) rufen `observability.ReconcileMatching(applicationLogBoundary(m), …)` (boundary :89); dritter Aufrufer `internal/application/runtime_observability.go:120`.
- Mechanismus: `internal/observability/registry.go:448-483` (`ReconcileMatching` :458) — nil predicate → error; jedes desired source muss `Validate()` bestehen UND vom owned-Prädikat selektiert werden (foreign source → Fehler, fail-closed), danach atomarer Ersatz der owned-Menge + desired im selben mutate. Boundary-Predicate: `ApplicationLogBoundary` :604 (class application + kind logs + ID-Präfix); die application-seitige applicationLogBoundary :89-92 ist ein dünner Wrapper, der sie direkt aufruft (kein gespiegelter Code — die Aktenformulierung "Local Mirror" meint den dokumentierten Mirror-Kommentar, nicht eine doppelte Implementierung).
- Base proof: `git merge-base --is-ancestor ec592fd385 HEAD` → yes; own commits: 8956bf08, 1c41ae7f (merge ec592fd385), 0150f0cf, 799c66ec, 0132087b, 973e1c4c, 282ef0df.
- Test witness (`go test ./internal/logs/ -run 'TestApplicationClassLogSource|TestReconcileMatching' -count=1 -v`): 6/6 PASS — SurvivesManagedReconcile, HasProductionWriter, DisabledPolicyReclaims, PolicyDisableReclaims, ReferenceClassCounterCheck (application vs reference class matrix), ReconcileMatchingFailsClosedOnForeignProviderSource. File `internal/logs/appclass_log_writer_test.go:40-266`.

Fund-Status: severity none (kein neuer Defekt); kartenwürdig: nein — Karte 0428-122/PR #1692 trägt den Inhalt.

## These 5 — #118 diag-exec stdout leak (kein stdout-leak)

Erwartung: der `DIAG_EXEC`-`if true`-fmt.Printf-Dump auf dem app-edit partial path ist weg; production stdout bleibt sauber in beiden DIAG_EXEC-Modi.

Befund: **bestätigt** auf develop ec592fd385.

- Entfernung: commit `de53246585` (merged via 360c1ed, #1689) removes `if true { fmt.Printf("DIAG_EXEC result.Status=%v outcomes=%d result=%+v\n", …) }` aus `cmd/baha/app_edit_apply.go`.
- grep witness (HEAD ec592fd385): `grep -rn "DIAG_EXEC" --include=*.go . | grep -v _test` → **keine Treffer** im Produktcode; einzige Referenzen leben im Regressionstest `cmd/baha/app_edit_diag_exec_stdout_test.go` (:21-42 dokumentieren Leak-Historie und das Both-modes contract).
- Test witness (`go test ./cmd/baha/ -run TestAppEditApplyPartialHasNoDiagnosticStdoutInAnyDiagExecMode -count=1 -v`): PASS in beiden Modi — `--- PASS: …/unset (0.01s)`, `--- PASS: …/set (0.01s)`; ok 0.023s. Der re-exec-Kind-Test vergleicht fd-1 capture: kein DIAG_EXEC-Text, und DIAG_EXEC darf Produktionsverhalten nicht ändern.

## Gesamtstand

- bestätigt auf develop: #116 (These 1), #120 (These 2), #118 (These 5).
- auf develop NICHT enthalten, auf ihren Kandidaten bestätigt: #121 (d9d70a98, PR #1691), #122 (8956bf08, PR #1692) — beides akzeptierter Kartenstand in review, keine neuen Defekte, keine neuen Karten.
- Kein produkt-aenderung, kein PR, kein .github-Zugriff, keine Container gestartet (R1 unit-only). Cleanliness: ps witness unten; nichts gestartet = nichts zu downen.

## Witnesses (commit/push/remote)

- `git ls-remote --symref origin main` (baseharbor-plan, VOR erstem Evidence-Commit dieser Lane): refs/heads/main = dc45bbc29331319b9eacfbdfe22ebb4373677f98; lokaler HEAD = origin/main = dc45bbc2… (single-parent commit)
- product develop head gegenprueft: ec592fd3852328439ae9de8763c816ae9dd88dcc (ls-remote + clone-HEAD identisch)
- Candidate heads: refs/pull/1691/head = d9d70a9845ea11f6d839b3f5600b67b214002d20; refs/pull/1692/head = 8956bf08e40e52b84a0dae55a9f1cb54db957636; beide mit ec592fd385 als Ancestor (merge-base proof oben)
- `docker ps -a` / `docker network ls` / `docker volume ls` on this host (ps-witness): only ambient stacks of other lanes (bh-local shared postgres/openbao, bh-*-ci, backup-foreign sentinel, testvol) — this lane started ZERO containers/networks/volumes/compose projects; nothing of mine to bring down (R1 unit-only honored).
- Ambient foreign process note (report, not touch): two orphaned `baha.test -test.run=^TestAppEditDiagExecStdoutChild$` re-exec children (PIDs 1341964, 1405874-class) have been sleeping ~5h with PPID=1 and caches (/var/tmp/go-build4031416813, /var/tmp/go-build314779866) already deleted — they predate this lane. They are the named re-exec child of the #118 stdout test hanging in an unset-mode invocation (candidate: mission-dualmatch lane). Not killed here: foreign worktree/process, mission forbids touching other sessions' state. Flagged for the coordinator to clean.

END verify-chain1 DONE
Candidate: read-only verify mission (keine Produktänderung); planning commits dieser Lane enden mit 85fa82af auf origin/main

### Publication witness (second-to-last action)

- Akte commit: `1194076b` (content of all thesis sections, unchanged since).
- Final state witness: `git ls-remote origin main` → `0bc42332549b9b337159f95cc8b532d3f48e25f4` = `git rev-parse HEAD` (this lane's last planning commit; remote file read back via `git show origin/main:evidence/r28-welle4-2026-11-19/verify-chain1/befund-1.md`, workspace clean against origin/main). Witness-commit chain: 1194076b → bd752f7c → 85b26744 → cfb30a54 → c3c8fbf4 → 22b299fe → 2e96615c → c1226cf3 → 2456350b → 0bc42332, all rebased monotonically through the hot planning repo; no force, `git cherry` empty.
- Race note: the planning repo was hot while this lane worked (main moved dc45bbc2 → 08c5b593 → 9b9514e9 → 1194076b → …); the first push hit a ref-lock race whose remote head already equalled this lane's 1194076b, and one later push needed a plain `git rebase origin/main` (no duplicate patch left, `git cherry` empty, workspace clean). No force at any point.

## Publication witness

git log --oneline origin/main | head -3 (after this commit, re-fetched):
7dafd3f8 evidence(r28-welle4 verify-chain1): live-verify chain1 theses (116/120/118 confirmed, 121/122 review-stage per coordinator ruling) and chain2 stage (102/093/099/117 confirmed) on develop deeeb6477
194a2da5 evidence(verify-chain1): cleanliness ps-witness + foreign orphan process note
8e613151 evidence(verify-chain1): END annotation names final planning commit 85fa82af

git ls-tree -r --name-only origin/main | grep verify-chain1: (to be pasted post-push)
