# 0428-060-updown-parity: converge down onto the authorized lifecycle

ROLLE: Worker. KARTE: t-20261114-r28-cli2-app-lifecycle. PR: #1747 (base develop).

## PLAN-Checkliste

- Baum + Identitaet: worktree /tmp/opencode/0428-060-updown-wt, lane-0428-060-updown, user.name 0428-060-updown
- Mission-Deps gelesen: brief.md + command-map; up/apply bereits konvergiert, down Pfad analysiert
- down consent gate: reachable down path (retireRuntimePreservingData) bereits gegated via e.confirmed + authorizeApplicationStop (app_runtime_retirement.go:99/112)
- helper downRequiresConfirmedConsent + TestDownConsentGoesBothWays (two-way) implementiert
- neue fn in CI-zelle gewiret (plain *_test.go unter ./cmd/baha gate, ci.yml:128)
- commit 8103f0065, push lane-origin, PR #1747 base develop
- host-CI zum terminalen zustand: alle Go unit + validation success, handoff an coordinator fuer Codex-abnahme

## Basis-Attestation

- git ls-remote lane-origin refs/heads/develop (letztes Messen): 77c1e60f51b91003ac3ddc391008c15e4a713a5c
- git ls-remote lane-origin refs/heads/develop (beim dispatch): 57d2f2751086
- branch base (ancestor of first commit): 77c1e60f51b91003ac3ddc391008c15e4a713a5c
- merge-base --is-ancestor 77c1e60f51b9 HEAD: JA

## write-set-pruefung

git diff --name-only 77c1e60f51b9..HEAD:
- cmd/baha/app_lifecycle.go
- cmd/baha/app_lifecycle_down_convergence_test.go

cmd/baha/app_update.go NICHT im diff. 0428-217 (5758bfc1) sauber (owner nachgessen, kollisionsverdacht widerlegt).

## Konvergiente stelle (vor/nach, datei:zeile)

Realer down-dispatch: app down/stop -> appStopCommand.Run (setzt applicationStopModeKey) -> appDestroyCommand.Run -> executeApplicationDestroyLifecycle -> retireRuntimePreservingData.
Dieser pfad hat bereits: Target-lock (executeApplicationDestroyLifecycle), provider-retirement plan, authorizeApplicationStop (stop-mode, app_runtime_retirement.go:112), preflight, verify, state-recording.
Consent-gate: e.confirmed (aus --yes via parseDestroyArgs, app_destroy_lifecycle.go:157) -> app_runtime_retirement.go:99 (refused) / :74 (never-delivered refused).

SEAM (neu, app_lifecycle.go, nach isApplicationDownMode ~zeile 45):
  func downRequiresConfirmedConsent(ctx context.Context) bool { return assumeYes(ctx) }

GATE (neu, executeApplicationStop ~zeile 115, nach preflight, vor erster runtime mutation):
  if !downRequiresConfirmedConsent(ctx) {
      fmt.Fprintln(out, "No changes were made. Re-run with --yes to stop the owned application runtime while retaining its data.")
      return nil
  }

semantische gleichwertigkeit: up/apply laufen durch plan/preflight/apply/verify mit assume-yes. down konvergiert verhalten; keine neue oberflaeche; keine sicherheitspruefung weicher gemacht.
authorizeApplicationStop (app_runtime_retirement.go:112) UNBERUEHRT (boundary 0428-209/214).

## identitaets-ausgabe

- git config: user.name 0428-060-updown, user.email 0428-060@baseharbor.local
- git log -1 --format=%an nach commit: 0428-060-updown
- commit 8103f006509855341bc67573c7b4dd5502c2d401

## mutations-beleg

- go build ./...: BUILD-EXIT 0 (against develop 77c1e60f5)
- go vet ./cmd/baha/: VET-EXIT 0
- go test ./cmd/baha -run ^(TestDownRequiresConfirmedConsent|TestDownConsentGoesBothWays)$ : ok 0.349s
- go test ./cmd/baha (destroy/retirement/down subset) : ok 0.407s
- ci-fast-check.sh: EXIT 0 (gofmt clean, readability baseline, workflow policy)
- git diff --name-only 77c1e60f5..HEAD: app_lifecycle.go, app_lifecycle_down_convergence_test.go (write-set clean)
- ancestor: merge-base --is-ancestor 77c1e60f5 HEAD = JA; log 77c1e60f5..HEAD = nur commit 8103f0065
- push lane-origin: [new branch] lane-0428-060-updown; delivery witness git ls-remote: 8103f006509855341bc67573c7b4dd5502c2d401 refs/heads/lane-0428-060-updown

## host-CI zum terminalen zustand (run 8103f0065, PR #1747)

- Alle check-runs terminal: IN_PROGRESS NONE, FAILED NONE, CANCELLED NONE
- required/unit Go jobs completed success: cli-0, cli-1, cli-2, cli-3, packages, owner
- validation success: go-build, go-vet, cli-gofmt
- 20 skips = release/matrix gates (Consumer Pins, Exact Candidate, Selected Runtime, Native Keycloak/Core, Pre-Release, docker/podman HA): korrekt fuer diese karte (kein shared planner/release-matrix/.github touch)
- neue *_test.go lauft unter ./cmd/baha unit gate (ci.yml zeile 128) -- CI-zelle = go test ./cmd/baha, trigger = PR selected checks. KEINE .github-aenderung noetig.
- mergeStateStatus BLOCKED = branch-protection (review pending), NICHT CI-failure; abnahme = coordinator/Codex.
- develop beim push neu gemessen: 77c1e60f5 (unveraendert, ancestor bleibt gueltig).

## repo-rule compliance

- write-set nur app_lifecycle.go + test; tabu-files unberuehrt (app_update.go, app_commands.go, mcp.go, app_lifecycle_lock.go nicht geaendert)
- boundary: app_runtime_retirement.go:112 (authorizeApplicationStop caller) NICHT angefasst (0428-209/214)
- PR #1747 single PR, base develop, kein 2. kandidat
- evidence im plan-repo baseharbor-plan (remote github.com/mcpdev80/baseharbor-plan.git), NICHT im product repo
- kein subagent; kein runner-infra gebaut

## cleanliness

docker ps -a vor: (<empty> - kein container/compose dieser lane gestartet)
docker ps -a nach: (<empty>)
compose-projekte dieser lane: keines. nichts herunterzufahren.
