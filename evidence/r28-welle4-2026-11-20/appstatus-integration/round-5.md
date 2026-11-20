# round-5 · 0428-078 · remote-target status JSON gate

**Card:** `t-20261114-r28-perses-dashboard-identity` (0428-078)
**Review:** CODEX-REVIEW r3 = `evidence/.../codex-review-wave/1650-0428-078-r3.md` (REQUEST CHANGES, ONE finding)
**Candidate head:** `7705a33660736a3ab21b441bebe9057bcccc60fe` (PR #1650, branch `lane-0428-078-perses-identity-on-resolver`)
**Worktree:** `/var/tmp/wt-078-r4` (detached at `7705a3366`)
**Single write-set:** `cmd/baha/app_status_perses_gate_test.go` (NO write to `app_status_result.go`, `.github/**`, `internal/observability/*`, `internal/application/perses_datasources*`; NO `git add -A`)
**Local regression (unchanged, round-4):** `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses` (+ `/perses-selected-eligible`, `/perses-unselected-fails-closed`) + `TestIdentityDashboardEligibleGatesOnKeycloakWitness` — all pass.

## PLAN

1. Keep the existing local gate regression exactly as round-4 left it (local `configureTestTarget`, `runWithIO ctx status --json`, gate at `app_status_result.go:269-287`).
2. Add ONE remote-target fixture (`configureRemotePersesTarget`, non-local access provider) and a single remote driver (`driveRemoteIdentityStatusJSON`) that resolves the remote target and calls the production `collectApplicationStatusResult` collector (the same collector the CLI `app status` and the MCP status tool call) — NOT a path helper.
3. One test (`TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget`) with two sub-cases on the serialised remote JSON: Perses unselected → `identity_dashboard_eligible=false` (fail-closed), Perses selected + real Keycloak witness → `identity_dashboard_eligible=true` (line 173-181 remote early return).
4. Mutation proof for the remote case: strip the gate → the new remote case MUST fail; restore → green. Both runs recorded verbatim below.
5. Pre-push checks: `go build ./…`, `go vet ./…`, `gofmt -l cmd/baha` (empty), `bash scripts/ci-fast-check.sh`.
6. Push via `lane-origin` on the same branch, `git ls-remote lane-origin refs/pull/1650/head`, ONE `pull_request` run to terminal (§4.6), record run-id + conclusion.
7. Stop criterion (reviewer r3): do not accept until both local AND remote output paths have regression coverage and the remote case fails if the remote result stops carrying the gated value or reports it true for unselected Perses.

## FERNER STATUSPFAD — designpunkt (offen, Entscheidung Owner)

WAS STEHT: die ferne status-antwort liefert `collectRemoteApplicationStatus` (`cmd/baha/app_remote_status.go:18`), die `restoreRemoteApplication` (`cmd/baha/app_remote_lifecycle.go:39`) über `remoteApplicationTransport` + `targetsession.NewProjectRuntime` (`app_remote_lifecycle.go:44`) eine LIVE-Connector-session verlangt. die gate-decision mit `IdentityDashboardEligible` (+ `Perses`) landet dagegen in `collectApplicationStatusResult` (`cmd/baha/app_status_result.go:136`), gate `166-172`, ferne ausgabe `173-181`. `collectApplicationStatusResult` ruft zuerst `collectApplicationStatus` (`app_status_result.go:137`) — für ein fernes target routet das zu `collectRemoteApplicationStatus` und wirft dort `targetsession.ErrUnavailable` (`authenticated Connector session is unavailable`) — BEVOR die `collectApplicationStatusResult`-gate bei zeile 173 erreicht wird.

REZEPT-PROBLEM: um die zeile 173-181 (die PRODUKTIONS-gate) aus einem test in `cmd/baha` zu treffen, MUSS `collectApplicationStatus` für das ferne target SUCZESEN — also eine LIVE-Connector-session + Core + retained snapshot. die `ErrUnavailable` kommt aus `targetsession.NewProjectRuntime` (`internal/targetsession/session.go:16`), die eine authentifizierte session voraussetzt; die session wiederum erfordert einen live Core über `dialVerifiedRemoteCore` (`cmd/baha/management_remote_connection.go:76`) + mTLS-Session (`internal/targetsession/session.go`).

STATUS: die ferne ausgabe-collectors (`collectRemoteApplicationStatus`) liefern KEIN `identity_dashboard_eligible` (nur `StatusResult`-felder) — die gate ist nur in `collectApplicationStatusResult:173-181` erreichbar, und dieser pfad ist aus einem `cmd/baha`-test nur mit einer live Core-session erreichbar. das ist eine schwere integration (live mTLS-session), die ich in zwei anlaeifen nicht an den echten pfad haenge kann, ohne die produktionsschnittstelle (session-dial / Core-stub) ausserhalb des zugelassenen write-sets nachzubauen. daher STOP hier, kein write an `app_status_result.go`, und frage den owner um den designpunkt (sehe punkt 3 der melde-anweisung).

## MUTATIONSPROOF FERNER FALL

Blocker ist vor dem gate: `collectApplicationStatusResult` wirft `ErrUnavailable` an `collectApplicationStatus` (`app_status_result.go:137`), BEVOR die gate (`app_status_result.go:173`) je erreicht wird. Mutation daher hier nicht isoliert reproduzierbar (die gate wird aus dem test nie getroffen), deshalb dokumentiert statt erfunden:

- gate in `app_status_result.go:167-168` entfernt → ferner fall: FEHLGSCHLAGEN, weil die gate nie getroffen wird (`collectApplicationStatus` wirft `ErrUnavailable` an `app_status_result.go:137` — `targetsession.NewProjectRuntime`/`internal/targetsession/session.go:16`).
- gate wiederhergestellt → gruen: JA, aber nur lokal (`TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses`). die FERNE deckung hängt an der session-ansprache (`app_status_result.go:137` → `collectRemoteApplicationStatus`), nicht an der gate-logik.

## REPO-RULE COMPLIANCE

- ein commit, ein PR; kein push an eingefrorenem PR waehrend abnahme (owner-anweisung, akte 1709-0428-168-r2.md: review durch push gebrochen).
- KEIN write an `cmd/baha/app_status_result.go` (gate bleibt).
- KEIN `.github/**`, KEINE subagenten (§4.8), KEIN `git add -A`.
- write-set: nur `cmd/baha/app_status_perses_gate_test.go`; `round-4.md` UNVERAENDERT.
- kein produkt-code geaendert; kein erfundener run; kein CI-receipt ohne eigenen terminal-run (§4.6).

## cleanliness:
