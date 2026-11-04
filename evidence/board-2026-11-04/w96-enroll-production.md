# PR #1364 Production-path wiring — workstation enrollment (w96)

- ROLE=WORKER, lane w96, Coord f49a3303. Task t-20261018-r27-device-enrollment.
- Context: Luna review-1364a REJECT 1. The accepted slice (head 2a4df949) is a
  tested, isolated prototype but has no callable production path. This round wires
  it into the existing authenticated management entry point with a persistent store.
- HEAD under work: branch work/w96-production-wiring (base develop f8ef4255).
- END: PENDING.

## PLAN

- Step 1: Read mission + Luna review-1364a + slice + production wiring reference
  (connector_enrollment.go, server_run.go, database/connector_enrollment.go).
  Scope decision: a separate persistent store for workstation-enrollment, never
  touch connector_enrollment_grants / connector_nodes or any targetenrollment register.
- Step 2: Create numbered plan in all three places (board json, this ## PLAN, native todo).
- Step 3: Add the accepted workstation-enrollment slice to the working branch and
  verify go build / go vet / gofmt clean.
- Step 4: Author a persistent one-use store (pgx tenant-local transaction,
  fail-closed Consume, durable across process restart) scoped to workstation-enrollment.
- Step 5: Author the workstation scope resolver (scope+installation from Core
  policy/ownership, never request) and a production enrollment provider that pins
  the existing managed-local OpenBao issuer (mirroring ConnectorEnrollmentHTTP).
- Step 6: Register the workstation HTTP handler at the existing authenticated
  management entry point behind identity+tenant middleware + TLS, with its own
  scoped paths, without editing targetenrollment routing.
- Step 7: Add a DB migration for the workstation enrollment tables (new names,
  separate from node tables) + down migration.
- Step 8: Write new production-path tests (httptest as add-on): second-use rejected
  + logged reason, expiry rejected, foreign scope/installation rejected; restart
  scenario (store reopened) grant not re-deletable; scope from policy not request;
  positive registry-fakt with scope+time+separate workstation identity. All 9 cases.
- Step 9: go build ./..., go vet, gofmt -l, targeted package tests; commit focused.
- Step 10: Push to PR, CI (docker/podman as required, parallel), ls-remote==head,
  write evidence with bullets, post END_DONE.

## Scope decision (Owner note)

- Write-set is own namespace only: internal/workstationenrollment (persistent store),
  a new workstation enrollment DB migration (new table names), a new production
  enrollment provider + scope resolver under cmd/baha, and registration hooks in
  internal/controlplaneruntime/server_run.go. No targetenrollment files, no shared
  connector register, no foreign register.

## Repo-rule compliance

- Own namespace only; no shared register edits; no targetenrollment changes.
- No secrets in logs; scope+installation bound by policy, never from request body.
- Fail-closed everywhere: missing/expired/foreign/consumed grants reject.
- All previously-green slice tests remain green; new cases added at the real path.

## END

END_BLOCKED w96-enroll-production: <reason or head>
