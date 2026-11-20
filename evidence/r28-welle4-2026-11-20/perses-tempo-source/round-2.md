# 0428-091 round-2 — perses-tempo-source on PR #1645 (lane x-m091)

## PLAN
- DONE Read review dossier 1645-0428-091.md; resolve github remote (REMOTE GUARD: `lane-origin` = https://github.com/mcpdev80/baseharbor.git)
- DONE P1–P4 fixes (routable gateway-alias endpoint; fail-closed AuthenticationRequired; restored two host-dashboard cells; three P4 points), mutation sondes measured
- DONE Diagnose the CI `PR · Go unit · packages` reds (valkey, Keycloak redirected, Loki MultiSource)
- FINAL CANDIDATE: ONE commit `4d73aa978` rebased onto develop tip `96f2ae11a` (see STATE below for why NOT 40cb28c75), pushed to `w091-tempo-r5-fix`
- Delivery witnesses + own-run terminal state recorded below

## remote witnesses
- `git ls-remote lane-origin refs/heads/w091-tempo-r5-fix refs/pull/1645/head` (after push, PR synced):
  - `4d73aa97808d000d2f70eaa193f8dbfc14e817a7  refs/heads/w091-tempo-r5-fix`
  - `4d73aa97808d000d2f70eaa193f8dbfc14e817a7  refs/pull/1645/head`
- Branch provenance: `git merge-base --is-ancestor 96f2ae11a 4d73aa978` = YES (base head fetched via `git ls-remote lane-origin refs/heads/develop` = `40cb28c75…`; the candidate intentionally rides `96f2ae11a`, the newest tip WITHOUT the #1594 policy rework — see STATE).
- `git log --oneline 96f2ae11a..HEAD` lists ONLY: `4d73aa978 fix(0428-091): Perses Tempo datasource adapter with routable gateway-alias endpoint and enforced mTLS (r2)`.
- Content preservation vs previous accepted head: `git diff 4abc25ab6 4d73aa978 --stat` = the develop-side delta only (#1594/#1712/#1713 content reverted by the base change); no file this card owns lost content: the diff of `internal/serviceaccess/pki.go`, `perses_compose_realization.go`, `internal/metrics/perses_tempo_source_test.go`, `internal/application/perses_fix6_regression_test.go`, `internal/identityprovider/keycloak_read_projection_test.go` between 4abc25ab6 and 4d73aa978 is EMPTY for the latter two and mid-fix-only for pki.go (projection preference + Lstat + sourceErr + requireClient fail-closed + fallthrough).
- Wrong-zone check: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` shows github.com/mcpdev80/baseharbor-plan — this evidence file lives there only.

## STATE — the 40cb28c75 tip is red WITHOUT this card
The rebase attempt onto tip `40cb28c75` (head `deb688450`) was measured red for BOTH:
- `TestPersesLokiDatasourceMultiSource*` (3 cells, `internal/logs/loki_test.go`, pinned foreign fixture, blob ce86670b4 — never writes a client pair): at clean develop-tip content the resolution now fails with `stat …/service-access/pki/client-cert.pem: no such file or directory`. Proven NOT lane code: base40 worktree at pristine `40cb28c75` (pki.go md5 24c0fa97) reproduces identically, as do foreign runs: PR #1684 run 44798687502 job 136504940003 and PR #1729 run 44805066271 job 136526893242 (develop content, same signature).
- `TestPersesTempoDatasourceSharedBackendGatewayStaysPolicyNeutral` (this card's pinned cell, `internal/metrics/perses_tempo_source_test.go:404`): #1594 removed the name-derived trust, so `Resolve("dev","cache",MTLS)` returns `AuthenticationRequired=true`; on tip there is NO policy at once satisfying this cell (pair == "") and the loki health path (client required, fixture has none). Every fix direction (projection variants, policy-neutral source reads, enrol-on-reconcile) trades one pinned cell for the other; only a change to `internal/logs/loki_test.go` (foreign, pinned) or `Resolve` semantics (Owner/#1594 scope) resolves it on tip.
- The same two cell families are exactly why the previous head 4abc25ab6's packages run (44731562217) went red after the merge window.
Decision: the candidate rides `96f2ae11a` (pre-#1594 tip, 2 commits old) until the loki-fixture/policy conflict is resolved by its owning card. When #1594's conflict is fixed upstream, this card rebases and the valkey+loki cells must both be re-verified.

## final candidate — measurements at 4d73aa978 (pushed content, worktree /var/tmp/x-m091-consolidate)
- `gofmt -l .` empty; `go build ./...` OK; `go vet` (card packages) clean.
- `bash scripts/source-readability-audit.sh`: PASS (Function span, Regression ratchet).
- `bash scripts/ci-fast-check.sh`: "OK — No candidate-added validation checks."
- Package battery (all `-count=1`):
  - internal/serviceaccess ok; internal/identityprovider ok (incl. `TestExistingKeycloakAccessNeverRewritesOrRepairsRuntimeProjection/redirected` PASS); internal/metrics ok; internal/logs ok; internal/traces ok; internal/capability ok; internal/telemetry ok; internal/objectstorage ok
  - internal/application: new-red vs baseline `/tmp/base-app-fails.txt` = EMPTY (ambient provider-registry/valkey-placement host reds unchanged)
  - cmd/baha: new-red vs `/tmp/base-cli.txt` = EMPTY (wizard reds are ambient; note-gate2 respected)
- Mutation sondes (earlier rounds, re-confirmed at this content class):
  - removing the `TempoAccessRuntimeComposeBind` mount line turns `TestPersesProductionComposeCarriesTheTempoAccessGatewayMount` RED
  - removing the sourceErr-`nil` fallthrough in `ExistingTLSMaterial` turns the Keycloak `redirected` cell RED
  - `os.Stat` instead of `os.Lstat` for the projection marker turns the redirected cell RED (reclassifies tampering as "no projection")
- New card tests and their CI route: `TestExistingTLSMaterialRedirectedProjectionFailsClosedUnderRequiredPolicy` (internal/serviceaccess) and `TestPersesProductionComposeCarriesTheTempoAccessGatewayMount` (internal/application) run in the standard `go test ./...` of the `PR · Go unit · packages` job (no path routing change needed; the packages job executes every package; no `.github/**` change).

## own hosted run (Eigenes-Run-Pflicht)
- Run 44814746593 (CI · PR #1645) at exact head 4d73aa978 — watched to TERMINAL: failure (12 success / 6 failure).
- 'PR Selected Checks' cell (job 136562618719) red at this head, clarification per note-091-sc.txt (ONE sentence, with job proof): the cli-0..3 shard failures are the field gate 0428-198 verbatim ('Managed-environment machine operations require an authenticated BaseHarbor operator.', e.g. agent_mcp_test.go:156, job 136560143562), and the packages shard (job 136560143717) does NOT speak my content — GitHub tests the MERGE branch: its checkout log reads 'HEAD is now at a2a2932 Merge 4d73aa97808d000d2f70eaa193f8dbfc14e817a7 into 40cb28c758b02960356434b630086a341ebe1738', so the four package reds (TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed / PartialMatchability / QueryOneSelectorPerSource + TestPersesTempoDatasourceSharedBackendGatewayStaysPolicyNeutral) are the tip-content defect documented in STATE — the pristine develop-tip worktree (pki.go 24c0fa97, develop loki fixture) reproduces the identical failure line — GATE-FAIL 0428-198 (cli shards) and the 40cb28c75 policy/fixture conflict owned by the #1594/loki-fixture cards (packages shard), not this card's content.

## cleanliness
- Session worktrees removed at END: /var/tmp/x-m091-consolidate, /var/tmp/x-m091-base40 (`git worktree remove` + `git worktree prune`).
- No containers/networks/volumes/state dirs created by this lane in the final stretch (unit-only work; earlier probe state dirs were t.TempDir()).
- Test binaries /var/tmp/*.test deleted.
- cleanliness: yes

END_DONE x-m091: consolidated single-commit candidate 4d73aa978 (rebased onto 96f2ae11a; STATE records that develop tip 40cb28c75 is red for loki MultiSource + valkey cells WITHOUT this card, reproduced on the bare tip and on foreign PRs #1684/#1729), all card packages green locally, readability PASS, delivery witnessed (branch == PR head), own run 44814746593 watched to terminal.
