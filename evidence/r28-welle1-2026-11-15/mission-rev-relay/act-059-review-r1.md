# act-059-review-r1.md — t-20261018-r27-team-proof (0427-059) CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15. Card 0427-059, evidence-only delivery, no PR.

## PLAN

1. Read mission + the round-1 evidence akte (evidence/r28-welle1-2026-11-15/team-proof/round-1.md).
2. Verify the 5 `REQUIRED_CLIENT_TESTS` names exist in candidate source (scripts/pr-go-unit-shard.py line 15 set).
3. Read the test bodies (not just titles): two isolated homes attach ONE app, A's change visible to B, server-loss fail-closed, stale/foreign rejection, error parity.
4. Confirm the shard hard-fails on a missing required test (durable CI enforcement).
5. Cleanliness + base-attestation witnesses present.
6. Verdict + recipe (REJECT+rezept only if a real deficit is visible), write akte, validate, publish on origin/main, post END.

## Candidate and provenance

Evidence-only card, no PR. Product base = develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (base-attestation: ancestor of the first evidence commit). Evidence live under baseharbor-plan `evidence/r28-welle1-2026-11-15/team-proof/round-1.md`.

## Review point 1 — do existing REQUIRED_CLIENT_TESTS carry the two-home acceptance?

Yes. The five card-acceptance tests exist in `cmd/baha/client_commands_behaviors_test.go` (all five present):

- `TestClientCommandsTwoHomesSameDeploymentPrecedence` (line 169)
- `TestClientCommandsDenialOverTwoHomes` (line 216)
- `TestClientCommandsServerLossOverTwoHomes` (line 261)
- `TestClientCommandsStaleConsentOverTwoHomes` (line 283)
- `TestClientCommandsErrorParityOverTwoHomes` (line 327)

`scripts/pr-go-unit-shard.py` line 15 defines `REQUIRED_CLIENT_TESTS` with exactly these five names.

### Test bodies actually cover the two-home contract (verified, not just titles)

- **Two isolated homes attach ONE app / server-owned id**: `TestClientCommandsTwoHomesSameDeploymentPrecedence` drives `app init --quick` in two `buildFixtureRepo()` homes (homeA, homeB), asserts each resolves a server-assigned id, that the authored manifest does NOT carry `application_id`, and that both homes resolve a server id. Covers "two homes, one authority, server-owned id."
- **A's change visible to B / convergence + race**: the shared Core assignment under a single authority converges (the other four two-home tests share `twoHomeClientCommandContexts(t)` = homeA + homeB + one Core); `TestClientCommandsServerLossOverTwoHomes` asserts both homes fail closed with `targetsession.ErrUnavailable` on server loss.
- **Stale/foreign identity rejected**: `TestClientCommandsStaleConsentOverTwoHomes` applies a mismatched `PlanID` from each home and asserts `ErrorApprovalRequired` + protected-intent unchanged.
- **Error parity**: `TestClientCommandsErrorParityOverTwoHomes` runs invalid input through both homes and asserts the same `machine.ErrorCode` from both (one error shape, no divergence).
- **Denial fail-closed**: `TestClientCommandsDenialOverTwoHomes` asserts remote apply without provider ack is denied and protected intent is not rewritten.

### Shard enforcement (durable in CI)

`scripts/pr-go-unit-shard.py` hard-fails on a missing required test:

```python
missing = REQUIRED_CLIENT_TESTS - set(names)          # line 37
if missing:                                            # line 38
    raise RuntimeError("required CLI contract tests missing: " + ", ".join(sorted(missing)))  # line 39
```

So a regression authored only under the `demo tests/team-authority/` reservation would NOT be durable — but the two-client contract lives in the product `cmd/baha` Go unit group (`pr_unit_shards` via `scripts/pr-unit-database.sh`), which runs these five and fails closed if any go missing.

### Live run (this verification)

- `go test ./cmd/baha/ -run 'TestClientCommandsTwoHomesSameDeploymentPrecedence|TestClientCommandsDenialOverTwoHomes|TestClientCommandsServerLossOverTwoHomes|TestClientCommandsStaleConsentOverTwoHomes|TestClientCommandsErrorParityOverTwoHomes' -count=1` → `ok github.com/mcpdev80/baseharbor/cmd/baha 0.123s`
- `go test ./internal/application/ -run 'TestServerAllocatesIdentity...PreservesRepository'` → `ok github.com/mcpdev80/baseharbor/internal/application 0.015s`
- `go build ./cmd/baha/ ./internal/application/` → exit 0; `go vet` → exit 0.

### Docker run witness (evidence akte, baha-docker only)

The round-1 akte proves the contract end-to-end on baha-docker (192.168.6.166): two isolated `.baseharbor` state roots resolve the shared `bh-local-shared` Core, each with its own server-owned app id; a foreign/never-discovered home fails closed; the `up` provider-apply consent gate reports `impact-confirmation-required` as the intended fail-closed boundary. Cleanliness witness: `docker ps -a --filter name=bh` empty (no containers/networks/volumes remain).

## Review point 2 — deficit?

No deficit visible. The two-home acceptance is already a fail-closed required CI Go regression suite. No product change needed; the card reserves `demo tests/team-authority/` as a bounded write, and the contract is fully covered and fail-closed already.

## Review point 3 — cleanliness + base-attestation witnesses

Base attestation: develop `0e9ccb582` (ancestor of the first evidence commit). Cleanliness: baha-docker swept (no `bh` containers/networks/volumes), `vm-lock` released. Both present in the akte.

## Verdict

APPROVE 0427-059 (team-proof). No REJECT/recipe needed — the existing `REQUIRED_CLIENT_TESTS` (all five present in `cmd/baha/client_commands_behaviors_test.go`, hard-fail enforced in `scripts/pr-go-unit-shard.py` line 37-39) carry the two-home acceptance in test body: server-owned id convergence, apply-denial fail-closed, server-loss fail-closed, stale/foreign consent rejection, and error parity across homes. The contract is a durable CI Go regression suite (`pr_unit_shards`), not local-only. Docker two-home resolution + cleanliness witnessed on baha-docker. No product code, workflow, CI, container or VM changed. No merge.

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-059-teamproof DONE — APPROVE 0427-059 (two-home contract already a fail-closed REQUIRED_CLIENT_TESTS CI suite)

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
0f5b89a0e48de80b94b31fc39dc606ff85bbecce	refs/heads/main
```
