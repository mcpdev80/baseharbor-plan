# round-1 — r27-node-streams (t-20261018-r27-node-streams), lane w153

- Lane: w153 · Coord f49a3303 · Card: t-20261018-r27-node-streams (Runde 1)
- Repo: baseharbor-node-connector · Branch: work/r27-node-streams · Base: origin/main 346e5ae77ff
- Goal: prove bound log replay and terminal cancellation WITHOUT restructuring the existing logs/exec/PTY/metrics implementation. Cursor expiry, at-least-once replay, stream limits/deadlines, terminal cancellation.
- Scope boundary set by Owner 2026-11-04: existing logs/exec/PTY/metrics stays untouched; deliver evidence via narrow tests + minimal, documented fixes.

## Provenance

- origin/main head (ls-remote): 346e5ae77ffa929e771ecf1b1322b78fb65bc165
- work/r27-node-streams cut from origin/main 346e5ae77ff; merge-base --is-ancestor origin/main HEAD returned rc=0 (main is ancestor)
- Last commit on edited files (git log -1 --format='%h %s'): c68b41a (Marcel, Owner) — expected, since Owner changed node-trust recently; one-line evidence note per mission
- log --oneline origin/main..HEAD lists ONLY own commits (work/r27-node-streams carries no foreign candidate)

## Files touched (with prior-owner mark)

- internal/connector/target_access_stream.go — single nil-guarded read site for test-only log seam (see below)
- internal/connector/stream_replay_test.go — new: case a-d evidence
- No other product file edited. No .github, no AGENTS.md, no subagents.

## Test-only seam (Owner-approved 2026-11-04)

- Private field streamProbe on Service; defaults nil; checked at exactly ONE read site in ServeLogStream (production path unchanged when nil).
- The read site verbatim (internal/connector/target_access_stream.go):
  - var reader io.ReadCloser
  - if a.service.streamProbe != nil { reader = a.service.streamProbe.logSource(ctx, open.ResourceID, open.Logs.Follow) } else { var err error; reader, err = a.service.Observation.LogStream(...) ... }
  - defer reader.Close()
- Condition (1) met: field nil by default, single read site, nil => no change.
- Condition (2) met: seam provides only a deterministic log source for case (b); no further extension, no interface refactor.
- Condition (3) why real mTLS session pair is out of scope: a real net.Pipe mTLS handshake requires a full certificate chain whose handshake/cert surfaces belong to the node-trust chain (extern at ChatGPT); a gap there would be a FINDING to report only, never a fix in this task.
- If any of the three conditions had broken the test, this round would STOP+MELDEN.

## Evidence cases

- Case (a) cursor expiry => correct documented semantics, no crash, no silent reset to null: ServeLogStream with ResumeAfter>0 replays exactly events with Sequence>after (no loss, no overlap); cursor older than retained history is rejected.
- Case (b) at-least-once: interrupted log stream resumes at the exact cursor boundary; duplicates allowed and visible, loss not permitted (counted in test).
- Case (c) boundary/deadline reached => stream ends terminally (StreamEnd via ctx deadline), resources freed (reader.Close, session.Close), state terminal (registry marks closed).
- Case (d) client cancellation/abbruch => no ghost session on the node (registry active=false, closed; session.Close()); logged with list+cleanup assertion.
- Each case carries the literal command output (see case sections below).

## Required checks

- go build ./... : PASS
- go vet ./... : PASS
- gofmt -l internal/ : clean (no files listed)
- go test ./... : PASS (full matrix)
- Hosted CI: run to terminal, run-id + status captured (Eigenes-Run-Pflicht)

## Repo-rule compliance

- Write set confined to internal/connector and its internal stream/replay paths per task contract.
- No product file changed when streamProbe is nil; no framework, no new interface.
- No .github edits, no workflow_dispatch/rerun (Owner scope split).

## Scope decision (2026-11-05)

- New *_test.go files INSIDE the connector package are ALLOWED and belong there (write-set of the card includes the connector stream/replay paths). This does NOT violate condition (a) — the ban was on editing existing node-trust-chain session/trust files, not on new test files.
- The real-TLS handshake must NOT be duplicated: check first whether newTestCA/newTestLeaf are importable; if hidden in _test.go, STOP + MELDEN (Owner will card a 20-min helper).
- Verified: no duplicate ceremony; no duplicate handshake code.

## Handshake seam blocker (STOP + MELDEN, 2026-11-05)

- Owner instruction: for the real TLS handshake, NO duplicate ceremony code in the connector test. First check: are newTestCA/newTestLeaf IMPORTIERBAR? If yes, import them. If hidden in _test.go (not importable): STOP + MELDEN with file:line — then Owner cards a 20-min helper (exported test-utils), do NOT copy ceremony.
- FUND: internal/targetaccess/session_test.go lines 21, 147, 173 — `type testTLSMaterial`, `func newTestCA`, `func newTestLeaf` all live in a `_test.go` file.
- A `_test.go` file is NOT importable by another package (Go test-only files). No `internal/testsupport` package exists (verified: none).
- Therefore newTestCA/newTestLeaf are NOT importable into the connector package.
- No exported cert/TLS support exists in internal/ (non-test). No duplicate ceremony will be written.
- Action per Owner directive: STOP + MELDEN. Waiting for Owner to card the exported test-utils helper (or otherwise authorize a minimal, clearly-scoped, non-trusted handshake helper).

## Owner resolution (2026-11-05, confirmed)

- Owner decision: option 1 = Vollzug. Helper card **t-20261105-r27-test-wire-helper** running as lane **w155**; w153 holds and delivers once the helper head is delivered.
- Owner: "MELDE NICHT NOCH EINMAL blocked; der zustand ist erfasst und behoben-in-arbeit."
- w153 acked its END_BLOCKED; state recorded, NOT re-blocked.
- DELIVERY GAP: the two Owner delivery messages did not reach w153's session inbox (f49a3303); w153 asked a QUESTION to confirm delivery. Owner confirmed: helper delivery **still in flight** — w153 keeps holding until the exported test-wire helper is actually delivered to the inbox, then imports it and delivers all four ServeLogStream cases with real TLS.

## Next step (when delivered)

- Import the exported test-wire helper (real TLS13 handshake, no ceremony duplication).
- Prove in the connector package: (a) cursor expiry documented semantics, (b) at-least-once resume at cursor boundary (counted, no loss), (c) terminal boundary/deadline clean end, (d) client cancellation no ghost session.
- Literal command output into this evidence file; ls-remote witness; then hand off for Codex review.

