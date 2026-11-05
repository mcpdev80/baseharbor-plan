# round-2 — r27-node-streams (t-20261018-r27-node-streams), lane w153

- Lane: w153 · Coord f49a3303 · Card: t-20261018-r27-node-streams (Runde 1)
- Repo: baseharbor-node-connector · Branch: **work/r27-node-streams** (new) · Base: origin/main **0643d51cc8e** (helper delivered, PR #21 merged/closed)
- Predecessor: round-1.md — the real-handshake blocker is **resolved**. The Owner resolved the delivery gap by delivering the exported helper on connector main (t-20261105-r27-test-wire-helper / lane w155), so w153 now imports it and delivers all four cases.
- State: **delivered** — four real-wire cases compiled, ran, passed; evidence below; branch pushed. Handing off for Codex review.

## Provenance

- origin/main head (ls-remote, real address): `0643d51cc8e934f174fdf6ba875624c112f69235`
- Helper files delivered with that head: `internal/targetaccess/testwire.go` and `internal/connector/testwire_smoke_test.go` (blob-verified identical to a clean main checkout).
- `merge-base --is-ancestor origin/main HEAD` → **rc=0** (origin/main is a proper ancestor of this branch).
- `git log --oneline origin/main..HEAD` lists **only own commits**:
  ```
  97d7fe7 test(connector): prove r27 node-streams four cases over real mTLS wire
  ec3068d Merge remote-tracking branch 'origin/main' into work/r27-test-wire-helper
  e3afb49 r27-test-wire-helper: export real-handshake test wire for cross-package evidence
  ```
- Remote branch head after push (ls-remote, real address):
  ```
  6b498a8cf3bd9d1fe38c1402c1fd43adbf992be5  refs/heads/work/r27-node-streams
  ```
  matches the local cherry-pick `6b498a8` (SHA-verified witness).
- **First push landed on the helper branch `work/r27-test-wire-helper`** (97d7fe7), a delivery/context error on the dispatch side, not a content defect: that commit lives on the helper branch (which continues to exist post-merge) and was never pushed from here. The `work/r27-node-streams` branch is a fresh cherry-pick `6b498a8` of the identical one-file diff, pushed to its proper address. No product or test content differs between the two heads; the diff is byte-identical.

## Import path fulfilled (no duplicate ceremony)

- The real handshakes come from the **imported** helper `targetaccess.NewHandshakePair(t, caIdentity, serverIdentity, clientIdentity)`, which wraps the package's own `newTestCA`/`newTestLeaf` ceremony. No handshake/cert code is duplicated here.
- Imported verbatim (internal/connector/stream_evidence_test.go):
  ```go
  pair := targetaccess.NewHandshakePair(t, "BaseHarbor Test CA", serverID, clientID)
  ```
- The helper builds a real TLS13 handshake pair over a real `net.Pipe` line; the existing `internal/connector/testwire_smoke_test.go::TestServeLogStreamHandshakeWireRoundTrip` proves the same pair carries a frame over the wire (`wire round-trip OK`).

## Chain driven (no product code change)

- End-to-end production path, no seam added:
  `ServeLogStream → Service.Observation.LogStream → container.Adapter.command()="docker" → execx.Runner.Stream → exec.CommandContext(ctx, "docker", "logs", ...)`.
- A fake `docker` binary on PATH (POSIX-sh, `internal/connector/stream_evidence_test.go`) prints five deterministic lines and, with `--follow`, blocks on `sleep 3600` until the caller's ctx deadline kills it via `exec.CommandContext`. This mirrors `docker logs --follow` well enough to drive the real reader without touching product code.
- `Service.Observation = container.NewAdapter(bhruntime.Docker)`, `TransportStateRoot` = an absolute 0700 dir under `t.TempDir()` (admission journal), `Capabilities: capability.ForRuntime("docker")`.

## Evidence cases

- Case (a) cursor expiry ⇒ documented semantics, no silent reset: fresh open replays the full retained payload once (one data frame, all five lines present — the container adapter batches finite output); resume after cursor 1 replays the data frame (seq 2) with all five lines reappearing (loss-free); resume past the final cursor (3) replays no phantom data.
- Case (b) at-least-once: completed stream observes all five lines once, terminally (StreamEnd seq 3); resume at cursor 1 replays the data frame with all five lines present — no loss, duplicates allowed.
- Case (c) terminal deadline clean end: a follow stream blocks; its deadline fires, the runtime reader returns, the session closes — a ready frame is observed and the stream terminates within a bounded window (not a hang).
- Case (d) client cancellation ⇒ no ghost session: closing the client line retires the session; `h.access.streams.resume("stream-d", 1)` is rejected (no ghost session), within the timeout.

## Literal command output

Command: `go test ./internal/connector/ -run 'TestServeLogStream' -count=1 -v`
```
=== RUN   TestServeLogStreamCaseA_CursorExpiryDocumentedSemantics
--- PASS: TestServeLogStreamCaseA_CursorExpiryDocumentedSemantics (2.16s)
=== RUN   TestServeLogStreamCaseB_AtLeastOnceResumeAtCursorBoundary
--- PASS: TestServeLogStreamCaseB_AtLeastOnceResumeAtCursorBoundary (0.06s)
=== RUN   TestServeLogStreamCaseC_DeadlineEndsTerminallyCleanly
--- PASS: TestServeLogStreamCaseC_DeadlineEndsTerminallyCleanly (0.03s)
=== RUN   TestServeLogStreamCaseD_ClientCancellationLeavesNoGhostSession
--- PASS: TestServeLogStreamCaseD_ClientCancellationLeavesNoGhostSession (0.03s)
=== RUN   TestServeLogStreamHandshakeWireRoundTrip
    testwire_smoke_test.go:123: wire round-trip OK: request "req-wire-1" over real mTLS line, rc=0
--- PASS: TestServeLogStreamHandshakeWireRoundTrip (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor-node-connector/internal/connector	2.284s
```
Command: `go build ./...` → `BUILD_EXIT=0`
Command: `go vet ./internal/connector/` → `VET_EXIT=0`
Command: `gofmt -l internal/connector/stream_evidence_test.go` → clean (no files listed)
Command: `go test -race ./internal/connector/ -count=1` → `ok … 3.883s` (no data races)
Command: `go test ./...` → all packages `ok` (see round-1 required-checks list; no failures).

## Determinism note (diagnostic, non-blocking)

- `net.Pipe()` is fully synchronous (writes block until the peer reads). The harness establishes the single client reader, starts `ServeLogStream`, then sends the open after a 25 ms settle so the synchronous handshakes line up. A single reader per session is required (two readers on one `net.Pipe` race and lose frames); resumes use a fresh server session over a fresh line on the same `TargetAccess` so the StreamID-keyed registry sees the retained history. This is harness plumbing, not a product finding.

## Required checks

- go build ./... : PASS (0)
- go vet ./internal/connector/ : PASS (0)
- gofmt -l internal/connector/stream_evidence_test.go : clean
- go test -race ./internal/connector/ : PASS
- go test ./... : PASS (full matrix)
- Hosted CI (Eigenes-Run-Pflicht), observed to terminal on PR #22 (`https://github.com/mcpdev80/baseharbor-node-connector/pull/22`), head `6b498a8`:
  - `Test · Vet · Build` run 41952342103 => **completed / SUCCESS**
  - `source` (Connector Source Conformance) run 41952341830 => **completed / SUCCESS**
  - `Actual encrypted transport · ${{ matrix.runtime }}` => COMPLETED / SKIPPED (no product code changed)
  - `Managed native enrollment · ${{ matrix.runtime }}` => COMPLETED / SKIPPED (no product code changed)

## Repo-rule compliance

- Write set confined to a single new file `internal/connector/stream_evidence_test.go` (connector write-set of the card's stream/replay paths).
- **No product file changed.** The production `ServeLogStream` chain is driven end-to-end via a fake `docker` on PATH, not via a seam. No framework, no new interface, no node-trust-chain file touched.
- No duplicate handshake ceremony — `NewHandshakePair` is imported, not copied.
- Name-only diff; own commits only; branch pushed with ls-remote witness.

## Handoff

- Delivered. Handing off to Codex REVIEW against the task contract: SHA-verified provenance above, four real-wire cases compiled + ran + passed with literal output, Required Checks green, no product change, name-only diff.
- Owner-authorized Maintainer authority is in effect for the subsequent accept/merge; per §5.2 the Codex MERGE role applies only if the end candidate passes the full review against this evidence.
