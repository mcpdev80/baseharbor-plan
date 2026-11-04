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

(plain bullets, filled as work proceeds)

## STOP-clauses

- unauthorized lifecycle call causes any unit/metadata effect => STOP
- restart behavior not observed => STOP
- CLI cannot invoke the lifecycle => STOP

## END

END w110-node-service-r2: <in progress>
