# round-4 evidence — w125-native-auth-r4

Lane: w125 (Worker). Coordinator: f49a3303. Card: t-20261018-r27-native-auth. PR #1362, branch work/r27-native-auth.
Candidate head: 9faf95f331e38dcc800bbfeb394e69ff618ed2d1 (based on develop ecbb8854). Reviewed SHA: a3eee132e3f2d1b65d7afee80efc3f9c0d166d6c.

## PLAN

- Read mission w125-native-auth-r4 + review-1362b artifact + task card. Confirm candidate head 9faf95f3 on branch work/r27-native-auth, base develop ecbb8854.
- Locate the production credential query path to wire the native broker in.
- Establish that the native broker currently has zero production importers (the REJECT core).
- Build the three planning artifacts (board json, evidence PLAN, todo-check) — no native todowrite tool in this session, so board + PLAN are the mandatory legs.
- Classify the change scope against the task write-set (internal/credential only) and decide whether production wiring is in scope or needs an Owner scope decision.
- If Owner authorizes: implement fail-closed broker wiring into the query path before interactive prompt, carry resolved credential through the in-memory credential contract, keep secrets out of errors/logs, add e2e caller counterprobe + regression.
- Run local go test/build/vet/gofmt, push on branch work/r27-native-auth, ls-remote head witness, watch gates to terminal.
- Post END_DONE / END_BLOCKED to f49a3303 with candidate SHA + lsremote witness.

## State found (investigation, 2026-11-04)

- Native package files present at candidate head: broker.go, caller_test.go, gitcredential.go, host.go, native_test.go, sources.go, sshagent.go.
- Broker implements credential.Broker (compile-time proof). Resolve reports a boolean native hit and returns empty credential.Data — never secret material.
- Zero production importers of internal/credential/native. Zero production callers of internal/credential/openbao (the only concrete credential.Broker). The native broker is a standalone adapter with no production query path.
- Task write-set (task card, "Dependencies and file ownership"): internal/credential/ bounded native-source adapters and tests; existing adapters only via accepted interface; shared indexes/registrations belong to a different task (t-20261018-r27-public-surfaces). No self-qualification; exact-SHA evidence required.
- PR #1362 reserved write-set: only internal/credential/native/*. (7 files).

## Scope conflict (blocking)

The REJECT recipe requires wiring the broker into the actual credential-query caller before any interactive prompt and carrying the resolved credential through the protected in-memory contract. That is a production-call-path change that touches other slices / shared registration, outside the reserved internal/credential/ write-set and outside the PR #1362 file reservation. This is an Owner scope decision (mission: "If you need a scope decision, post a QUESTION line"). Not acting on unauthenticated scope expansion without Owner confirmation.

## END

END_QUESTION w125-native-auth-r4: head=9faf95f broker=<empty-credential.Data> caller=<NONE> | Two-part scope decision needed before touching anything: (1) the reviewed Broker.Resolve returns empty credential.Data{} — the exact 'found-but-empty' defect — so it cannot carry the resolved credential through the protected in-memory contract; (2) there is NO production caller of internal/credential/native in cmd/baha, so no query-flow hook exists to attach to. Task write-set is internal/credential/ only; cmd/baha is a different slice (PR #1251). QUESTION posted to Owner f49a3303: authorize (A) a minimal bounded cmd/baha wiring + whether Broker must return the resolved credential (propose a new narrow method, not changing reviewed Resolve), or (B) deliver a self-contained internal/credential unit proving the counterprobe in-package with a follow-on task owning the cmd/baha wiring. Awaiting Owner input before any implementation.
