# Round 2 — r27 node-service lifecycle (baseharbor-node-connector)

- Role: Worker (Lane w130), Coordinator f49a3303
- Card: t-20261018-r27-node-service (Welle 4, Runde 2)
- Branch: `work/r27-node-service`, head `78b3c4f3c3a5ee046555445834a6350674dd2593`, PR #19
- Base: `origin/main` = `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`

## PLAN

- Read mission + review-19a fully; verify branch provenance
- Fix gofmt on `cmd/baseharbor-node-connector/main.go` and `internal/nodeservice/nodeservice.go`
- Fix the root cause of the gofmt failure (dangling `WithAuthorizer` comment)
- Verify systemd.go real rootless lifecycle (ExecLine, XDG path, daemon-reload, supported systemctl ops, lingering)
- Verify cmd lifecycle is a real executable install/start/restart/uninstall, self-owned only
- Verify auth-before-effects on every side effect; ErrUnauthorized actually used
- Verify test coverage (restart evidence, missing-auth mutation, duplicate install, protected-key regression)
- Run hosted checks locally to terminal (gofmt, vet, build, test)
- Run native systemd-user smoke locally or STOP + MELDEN
- Write evidence, commit, push, capture witnesses
- Post END_DONE to coordinator

## Provenance (proof of one candidate per chain)

- `git ls-remote origin main` -> `2a02a9a5d2e95b9f627fe6f42d71be0d7b9d8a57`
- `git merge-base --is-ancestor origin/main HEAD` -> ANCESTOR_OK (origin/main is an ancestor of HEAD)
- `git diff origin/main...HEAD --name-only` -> cmd/baseharbor-node-connector/main.go, cmd/baseharbor-node-connector/main_test.go, internal/nodeservice/nodeservice.go, internal/nodeservice/nodeservice_test.go, internal/nodeservice/reenroll.go, internal/nodeservice/systemd.go

## Current-state findings before change

- Review-19a verdict was REJECT; four recipes + gofmt gate.
- The candidate already implements a real systemd-user lifecycle: Install writes the .service artifact to the XDG systemd-user dir via `atomicWriteUnit`, runs `daemon-reload`, then `systemctl --user start`; Remove stop/disables via supported operations then removes the own unit; `restart`, `enable`, `disable`, `stop` are supported systemctl operations; lingering via `WantedBy=default.target` in the [Install] section.
- `cmd/.../main.go` wires a real `service` subcommand: install/start/restart/uninstall, self-owned only.
- `Service.authorizer` gates every lifecycle/metadata side effect via `authorizeEnforced`/`authorizeMetadata`; `ErrUnauthorized` is declared and returned (nil authorizer fails closed).
- Tests cover restart-evidence, missing-auth zero-effects, duplicate-install determinism, protected-key regression, native smoke skip-gate.
- GOFTM FAILURE (the only blocking defect): `gofmt -l cmd internal` reports `cmd/baseharbor-node-connector/main.go` and `internal/nodeservice/nodeservice.go`. Root cause in `nodeservice.go`: lines 457-461 — the `WithAuthorizer` method comment lost its `// WithAuthorizer` prefix, leaving a dangling comment with no blank line before it. gofmt wants a blank line before the comment.

## Changes

- (applied after local verification below)

## Hosted checks run locally (self-run)

- (record after running)

## Native systemd-user smoke

- (record command + output, or STOP + MELDEN)

## Witnesses (final)

- `git ls-remote` head == commit SHA
- `git merge-base --is-ancestor origin/main HEAD`
- `git diff origin/main...HEAD --name-only` (own write-set only)

## Status

- IN PROGRESS
