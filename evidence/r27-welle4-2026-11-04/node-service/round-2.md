# Round 2 — r27 node-service lifecycle (baseharbor-node-connector)

- Role: Worker (Lane w130), Coordinator f49a3303
- Card: t-20261018-r27-node-service (Welle 4, Runde 2)
- Branch: `work/r27-node-service`, head `78b3c4f3c3a5ee046555445834a6350674dd2593`, PR #19
- Base: `origin/main` = `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`

## PLAN

- Read mission + review-19a fully; verify branch provenance
- Fix gofmt on `cmd/baseharbor-node-connector/main.go` and `internal/nodeservice/nodeservice.go`
- Fix the root cause of the gofmt failure (dangling `WithAuthorizer` comment + import ordering)
- Verify systemd.go real rootless lifecycle (ExecLine, XDG path, daemon-reload, supported systemctl ops, lingering)
- Verify cmd lifecycle is a real executable install/start/restart/uninstall, self-owned only
- Verify auth-before-effects on every side effect; ErrUnauthorized actually used
- Verify test coverage (restart evidence, missing-auth mutation, duplicate install, protected-key regression)
- Run hosted checks locally to terminal (gofmt, vet, build, test)
- Run native systemd-user smoke locally or STOP + MELDEN
- Write evidence, commit, push, capture witnesses
- Post END_BLOCKED to coordinator

## Provenance (proof of one candidate per chain)

- `git ls-remote origin main` -> `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`
- `git merge-base --is-ancestor origin/main HEAD` -> ANCESTOR_OK (origin/main is an ancestor of HEAD)
- `git diff origin/main...HEAD --name-only` -> cmd/baseharbor-node-connector/main.go, cmd/baseharbor-node-connector/main_test.go, internal/nodeservice/nodeservice.go, internal/nodeservice/nodeservice_test.go, internal/nodeservice/reenroll.go, internal/nodeservice/systemd.go

## Changes (own write-set only)

1. gofmt — `cmd/baseharbor-node-connector/main.go`: import block reordered so `internal/runtime` and `internal/targetaccess` sort after `internal/execx`/`internal/nodeservice` (gofmt import grouping).
2. gofmt — `internal/nodeservice/nodeservice.go`: the `WithAuthorizer` method comment had lost its `// WithAuthorizer` prefix, leaving a dangling comment with no blank line before it. Restored a proper blank line and a correct `// WithAuthorizer` method comment header. This is the root cause of the `gofmt -l` failure.
3. cmd dispatch — `run()` now dispatches the `service` subcommand BEFORE the full `parseConfig()`. Previously `parseConfig()` ran on the full arg list and rejected `service` as an unexpected positional argument, so the `service` lifecycle subcommand could never execute. This is the fix for recipe #2 (the production path can really call the lifecycle).

All three are confined to the write-set named by the mission (`main.go`, `nodeservice.go`). No `.github` edit, no second branch, no test deletion/rewrite.

## Hosted checks run locally (self-run, terminal)

- `gofmt -l cmd internal` -> EMPTY (exit 0). [was RED before fix]
- `go vet ./...` -> exit 0
- `go build -buildvcs=false ./...` -> exit 0
- `go test ./internal/nodeservice ./internal/targetaccess -count=1` -> `ok nodeservice 0.64s`, `ok targetaccess 15.1s` (exit 0)
- `go test ./... -count=1` -> ALL PASS across cmd, capability, connector, execx, fssecure, health, nodeservice, runtime, runtime/compose, runtime/container, runtime/quadlet, targetaccess (exit 0)

## Native systemd-user smoke (host: baha-runner-docker-2, Linux 7.0.0-38-generic)

- The systemd user manager IS reachable for transient units: `systemd-run --user --unit=r27-probe /bin/sleep 30` -> "Running as unit: r27-probe.service"; `systemctl --user is-active r27-probe` -> `active`; live `systemctl --user restart` -> exit 0; stop -> `inactive`. So `show-environment` answering is not a hollow probe — a live user manager exists.
- BUT units written to the XDG user unit dir are NOT visible to `daemon-reload` on this host: `systemctl --user show -p UnitSearchPath` returns EMPTY; a trivial `smoke.service` written to `~/.config/systemd/user/` and `daemon-reload`ed is not listed (`grep_exit=1`); `systemctl --user start baseharbor-node-connector.service` -> `exit status 5: Unit ... not found`.
- The Go native smoke test `TestNativeSystemdUserLifecycleSmoke` therefore FAILS at the `start` step on this host: `nodeservice_test.go:461: native install failed: exit status 5: Failed to start baseharbor-node-connector.podman.service: Unit baseharbor-node-connector.podman.service not found.` (smoke-ex=1). It does NOT skip and does NOT pass here.
- Manual CLI run against the connector's own unit: install writes the `.service` artifact to `~/.config/systemd/user/` with the validated `ExecStart=` line and `WantedBy=default.target`, 0600 perms (proves recipe #1 persist + recipe #3 lingering wiring), but `systemctl --user start` fails with unit-not-found because this host's user manager does not load units from the config dir without quadlet/persistent-session registration.
- This is a host/session systemd quirk (empty `UnitSearchPath`, no persistent user session registration), not a product-code defect. The write-set writes the unit to the correct XDG path with the correct content and uses only supported systemctl operations.

## Recipe-by-recipe status

- (0) QUELLFORMAT — RESOLVED: `gofmt -l cmd internal` is empty; root cause fixed.
- (1) systemd.go rootless lifecycle — implementation present and correct (ExecLine to XDG path, daemon-reload, supported systemctl ops, lingering WantedBy). Native observation blocked by host user-manager unit-load quirk (see above).
- (2) cmd lifecycle executable — FIXED: `service` subcommand now dispatches and executes install/start/restart/uninstall (proven it reaches and drives the real systemd user manager; the only failing step is host-specific unit-not-found after daemon-reload).
- (3) auth-before-effects — present: `authorizeEnforced`/`authorizeMetadata` gate every lifecycle/metadata side effect; `ErrUnauthorized` returned on nil authorizer; tests prove zero manager/store effects.
- (4) tests — present: restart records calls vs start; missing-auth mutation proves zero effects; duplicate-install determinism; protected-key regression retained; native smoke skip-gate present.

## Blocker

The mission's native smoke requirement cannot be driven to terminal on this host because the systemd user manager does not load units from the XDG config dir (empty `UnitSearchPath`), so `TestNativeSystemdUserLifecycleSmoke` FAILS at `start` (unit not found). Per mission §native smoke: "Wenn DAFUER kein user-manager verfuegbar ist: NICHT erfinden und NICHT als success melden — STOP + MELDEN mit dem befehl und der ausgabe." The user manager is reachable (transient units work), but not for config-dir units — a host/session condition, not a code defect. The two currently-skipped hosted native jobs cannot be exercised to a green terminal here without a host that registers user units.

## Hosted CI (self-run watch to terminal)

- CI · Node Connector Quality #39 run #41879298406 sha=84cf6475ab status=completed conclusion=SUCCESS
- Connector Source Conformance #178 run #41879298413 sha=84cf6475ab status=completed conclusion=SUCCESS (the previously-RED `source`/gofmt gate is now green)
- Both run on GitHub-hosted shared runners; no runner infra touched.

## Witnesses (final, post-push)

- `git ls-remote origin/work/r27-node-service` -> `84cf6475ab94f58495b434683e6be529cf655f23` == local HEAD `84cf6475ab94f58495b434683e6be529cf655f23`
- `git ls-remote origin/main` -> `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`
- `git merge-base --is-ancestor origin/main HEAD` -> ANCESTOR_OK (origin/main is an ancestor of HEAD)
- `git diff origin/main...HEAD --name-only` -> cmd/baseharbor-node-connector/main.go, cmd/baseharbor-node-connector/main_test.go, internal/nodeservice/nodeservice.go, internal/nodeservice/nodeservice_test.go, internal/nodeservice/reenroll.go, internal/nodeservice/systemd.go (own write-set only)
- Local hosted checks (self-run): `gofmt -l cmd internal` EMPTY; `go vet ./...`=0; `go build -buildvcs=false ./...`=0; `go test ./internal/nodeservice ./internal/targetaccess`=ok; `go test ./...`=ALL PASS.

## Status

- BLOCKED — native smoke cannot be driven to a terminal green on this host. The systemd user manager is reachable for transient units (`systemd-run --user` -> active, live restart exit 0) but does not register units written to the XDG config dir (`UnitSearchPath` empty; `daemon-reload` sees nothing; `TestNativeSystemdUserLifecycleSmoke` FAILS at `start` with unit-not-found). Per mission §native smoke: do not manufacture success; STOP + MELDEN. All hosted checks are green (local + CI #39 and #178 at sha 84cf6475ab). gofmt fixed, auth-before-effects present and tested, cmd lifecycle dispatched correctly, write-set self-owned and pushed to the named candidate. Awaiting owner to arrange a host/runner that registers systemd user units, then the native smoke is the only remaining gate.
