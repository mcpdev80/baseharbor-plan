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

END_QUESTION w125-native-auth-r4: head=9faf95f hook=app_apply.go:23/287 | Confirmed the exact testable hook (appApplySecretReadHidden seam). Two contract decisions block implementation: (1) DOMAIN MISMATCH — the required secret name here is an app-scoped OpenBao KEY NAME, but the reviewed native.Broker resolves a HOST credential (git helper/ssh-agent for an https://host); no host string exists at this call site. (2) VALUE CONTRACT — reviewed broker.Resolve returns empty credential.Data{} (found-only, the review-1362b defect); the value-carrying contract is openbao.Client.Resolve → credential.Data{Payload}. QUESTION (2nd) posted to Owner f49a3303: confirm the scoping model for a required secret AND authorize a NEW narrow native path returning credential.Data{Payload} (do NOT modify the reviewed empty-Data broker). Awaiting Owner input before any implementation.
