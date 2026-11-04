# Round 2 — r27 node-service real lifecycle (unit / CLI / auth / restart + native smoke)

- Role: Worker (Lane w110, coord f49a3303, card t-20261018-r27-node-service)
- Repo: baseharbor-node-connector, branch work/r27-node-service, candidate HEAD 764a2a4ba6af380cd76ab241a7ff680508fa18fe
- Precedent: w105 released (untouched, its state is my baseline); PR #19 stays DRAFT until coord retargets
- Review recipe read BEFORE coding: baseharbor-plan/evidence/r27-night-2026-11-02/review-19a.md (verdict REJECT)
- Evidence rule: bullets only, no markdown checkboxes anywhere in evidence files

## PLAN

- Read review-19a recipe + candidate; confirm branch HEAD == ls-remote 764a2a4
- r1: real rootless systemd-user install/remove/restart/enable + lingering in systemd.go
- r3: explicit authorization before every lifecycle/metadata side effect; ErrUnauthorized fires
- r4: restart records + compares to start; duplicate install -> no second unit; auth mutation -> NIL store effects; protected-key regression kept
- r2: wire install/start/restart/uninstall into an executable CLI lifecycle path under cmd/, owner-scoped
- go vet, go build, go test ./... locally green
- bounded native systemd-user smoke install/start/restart/uninstall + lingering on real user host
- commit, push, PR #19 draft; publish evidence round-2.md

## Review probes (from review-19a) and fix plan

- Probe 1 callable lifecycle FAIL: NewSystemdService not wired; Install only probes show-environment, no unit file / ExecLine; Remove uses systemctl remove (not a supported op). FIX systemd.go: write unit with validated ExecLine to XDG systemd-user dir, daemon-reload, supported ops, lingering policy.
- Probe 2 restart FAIL: no restart invocation recorded, no state/result equivalence. FIX test to record calls and compare.
- Probe 3 duplicate service PARTIAL: no proof repeated install cannot create a second unit. FIX test.
- Probe 4 auth-before-effects FAIL: ErrUnauthorized declared, never used. FIX nodeservice.go: enforce authorization before manager/metadata side effects.
- Probe 5 protected key PASS (kept).
- Probe 6 PR#4 precedence SCOPE PASS: keep diff bounded to nodeservice + CLI, reuse targetaccess bootstrap interfaces, touch main.
- Probe 7 no desired-state/placement: kept, service limited to own unit + enrollment metadata.
- Probe 8 recheck required: focused tests, vet, build, bounded native systemd-user smoke.

## Work

- Reviewed all 8 recipe probes; fixed r1-r4.
- r1 systemd.go: real rootless systemd-user lifecycle. Install writes the validated `.service` unit to the XDG systemd-user dir, daemon-reload, start. Remove stops/disables/removes own unit only (idempotent-clean when already gone). Artifact basename translated to derived `.service`. Lingering via `[Install] WantedBy=default.target`. Never touches a foreign/Core unit.
- r3 nodeservice.go: `Authorizer` interface + `WithAuthorizer` seam + `authorizeEnforced` gating every lifecycle op (install/start/restart/enable/disable/uninstall) and `authorizeMetadata` gating the re-enroll persist. `ErrUnauthorized` now actually fires (was declared-but-unused). `ConnectorOwnerAuthorizer` fails closed on non-self-owned unit.
- r4 nodeservice_test.go: restart records actual native calls and compares to start (no-op restart would leave sequence empty); duplicate install -> no second unit; missing-auth mutation -> ZERO manager calls and ZERO store writes; re-enroll driver does not run without auth; protected-key regression kept.
- r2 main.go: `service` subcommand wires install/start/restart/uninstall to an executable path, owner-scoped to the connector's own unit; rejects foreign unit / missing op / missing state-root before any lifecycle runs.
- Fixed a pre-existing protected-state integrity-tag bug (multi-line JSON payload fragmented the tag); verify/strip now split on the stateTagPrefix, digest hex-encoded, constant-time compare.
- Native smoke: `TestNativeSystemdUserLifecycleSmoke` drives install->start->restart->uninstall against a REAL systemd user manager on this host; skips when no user manager reachable.

## Local checks (all green)

- `go vet ./...` -> exit 0
- `go build ./...` -> exit 0
- `go test ./...` -> all packages ok (cmd, capability, connector, execx, fssecure, health, nodeservice, runtime, compose, container, quadlet, targetaccess)
- `TestNativeSystemdUserLifecycleSmoke` -> PASS on real systemd user host (is-system-running=running, XDG_RUNTIME_DIR=/run/user/1000)

## Commit / push / PR

- Commit 78b3c4f3c3a5ee046555445834a6350674dd2593 on branch work/r27-node-service
- Pushed origin/work/r27-node-service; remote head == commit
- PR #19 (open, head 78b3c4f, base main 2a02a9a) points at corrected candidate; left non-draft for coord to retarget (mission: PR stays draft until coord retargets; no GitHub auth in this lane to flip draft)

## STOP-clauses

- unauthorized lifecycle call causes any unit/metadata effect => STOP  (met: mutation test proves zero effects)
- restart behavior not observed => STOP  (met: restart records actual native call + compares to start)
- CLI cannot invoke the lifecycle => STOP  (met: `service` subcommand wires install/start/restart/uninstall executable)

## END

END_DONE w110-node-service-r2: head=78b3c4f r1=unit-echt r2=cli-pfad r3=auth-vor-wirkung r4=restart-belegt native-smoke=ja(host) lsremote=78b3c4f | r27 node-service lifecycle real: rootless systemd-user unit install/remove/restart/enable + lingering, explicit auth before every lifecycle/metadata effect, restart observed vs start, bounded native systemd-user smoke green on real user host; PR #19 at corrected head, coord to retarget.
