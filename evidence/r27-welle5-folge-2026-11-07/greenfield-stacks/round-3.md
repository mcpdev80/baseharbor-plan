# 0427-003-greenfield-stacks — round-3 (quarkus-fix PR, 2026-11-07)

- ROLLE: Worker, lane 0427-003-greenfield-stacks, Coord 594fd2f5. KARTE: core-815.
- Mission (missions/0427-003-greenfield-r3-quarkus-pr.txt): quarkus-fix `0d8639c3d` auf neu develop `812c99c88` rebasieren (Drift: 0c4e59cdad → 812c99c88 = #110 lifecycle/fixture), PR gegen develop + CI terminal, Podman wartet auf #110 (#107/#110 readiness, NICHT host-blocker).

## Base attestation

- `git fetch origin develop` → `812c99c8873df400348fbc8cc9be5e650b8966c4`.
- `git merge-base --is-ancestor 812c99c88 origin/develop` → rc0 (812c99c88 in develop).
- Drift zwischen alt-greenfield-Base `0c4e59cdad` und neu develop `812c99c88`: 31-Datei-Change (lifecycle/fixture, registry, deployment, serve, CI-gate). Das ist #110, NICHT mein Scope.

## Rebase (clean, isoliert)

- Frischer Branch `quarkus-fix-r3` vom `812c99c88` (`git checkout -b quarkus-fix-r3 812c99c88`).
- `git cherry-pick 0d8639c3d` → sauber (conflict-frei).
- `git merge-base --is-ancestor 812c99c88 HEAD` → rc0 (812c99c88 IS ancestor).
- Delta gegen 812c99c88 (git diff --stat): NUR 2 Dateien:
  - `internal/development/quarkusadapter/adapter.go` (+4/-1)
  - `internal/development/quarkusadapter/adapter_test.go` (+12)
- Kein lifecycle/fixture/registry/deployment/serve/.github-Touch. Exact-one-candidate.

## Build / vet / test (lokal)

- `go build ./...` → clean.
- `go vet ./internal/development/...` → clean.
- `go test ./internal/development/quarkusadapter/...` → ok (TestQuarkusRoundTrip assertions compose contains /q/health).

## PR

- Branch `quarkus-fix-r3` → origin gepushed.
- PR #1429 gegen `develop`: https://github.com/mcpdev80/baseharbor/pull/1429
  - state=OPEN, mergeable=MERGEABLE.
  - Titel: "fix(quarkus): emit compose healthcheck (/q/health) so baha up reaches readiness"
  - Body: scope (exact one candidate), base 812c99c88, CI-Aufnahmepflicht-Hinweis.

## Hosted CI (terminal, witnessed)

- Run-ID: **42387327608**, status=completed, conclusion=success, head=0743011cfa5d9bd260d4a347ab94a6049ce960a2.
- Jobs: 8 success, 10 skipped, 0 failure. Alle terminal (keine in_progress).
- Docker-gate: `Targeted HA · docker` completed success.
- Podman-gate: `Targeted HA · podman` completed success.
- go-unit-tests: PR · Validation · go-unit-tests completed success (TestQuarkusRoundTrip läuft im CI unit-suite — CI-Aufnahmepflicht erfüllt).
- go-build, go-vet, Exact Candidate, Source format, Workflow policy, Release Source Preflight, Consumer Pins, Demo Pin, Selected Runtime, Public Contracts, Runner Interface — alle success.
- ls-remote-Zeugnis: origin/develop = 812c99c88 (pr-base verifiziert).

## Podman-seite

- Ausstehend, wartet auf #110 (podman readiness). NICHT als host-blocker verbuchen — external-blocker #107/#110.
- Go/Python/Next.js auf docker sind belegt (Next.js auf baha-docker-2 14GB READY).

## END

- END_DONE 0427-003-greenfield-stacks: head=0743011c base=812c99c88 pr=#1429(ornith, OPEN, mergeable) quarkus_fix=clean(0d8639c3d→812c99c88, delta 2-dateien) ci=run-42387327608 success(8/10) go-build=clean go-vet=clean unit-tests=success CI-aufnahme=erf podman=wartet-auf-#110 evidence=evidence/r27-welle5-folge-2026-11-07/greenfield-stacks/round-3.md
