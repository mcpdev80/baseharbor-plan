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
- `docker ps -a --format '{{.Names}} {{.Status}}'` auf diesem host: nur ambient-core/ Bilder/fremde Container, keine dieser Lane; keine compose projects, no volumes/networks created (pure `go test` runs).

END verify-chain1 DONE
Candidate: keine Produktänderung (read-only + unit tests); planning head this lane: 2456350b (origin/main)

### Publication witness (second-to-last action)

- Akte commit: `1194076b` (content of all thesis sections, unchanged since).
- Final state witness: `git ls-remote origin main` → `0bc42332549b9b337159f95cc8b532d3f48e25f4` = `git rev-parse HEAD` (this lane's last planning commit; remote file read back via `git show origin/main:evidence/r28-welle4-2026-11-19/verify-chain1/befund-1.md`, workspace clean against origin/main). Witness-commit chain: 1194076b → bd752f7c → 85b26744 → cfb30a54 → c3c8fbf4 → 22b299fe → 2e96615c → c1226cf3 → 2456350b → 0bc42332, all rebased monotonically through the hot planning repo; no force, `git cherry` empty.
- Race note: the planning repo was hot while this lane worked (main moved dc45bbc2 → 08c5b593 → 9b9514e9 → 1194076b → …); the first push hit a ref-lock race whose remote head already equalled this lane's 1194076b, and one later push needed a plain `git rebase origin/main` (no duplicate patch left, `git cherry` empty, workspace clean). No force at any point.
