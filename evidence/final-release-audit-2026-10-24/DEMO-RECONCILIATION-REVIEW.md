# Bounded Demo reconciliation correction review

Reviewed against actual Demo D `03396c805369e61d2e0745d00f78c8add809e2e0`. Source verdict: APPROVE; exact publication and merge identity independently authenticated through GitHub.

The sole delta is one added `run_consented` wrapper around the existing `baha app apply` call after stopping the selected shared PostgreSQL container. New `tests/reconciliation/run.sh` blob: `2c128dbc455647088d2259d08d2fc9208617dadf`. No helper, Core pin, backup, installation, cleanup, acceptance-driver or workflow bytes change.

The existing fixture helper first executes the selected Core command without provider consent, validates the actual typed current impact refusal, and supplies matching plan identity and required acknowledgement stages within an isolated owned fixture. It does not manufacture success. Its installation-remainder handling is separate and bounded; arbitrary stale-plan errors are not retried. The script retains the real provider stop, failed degraded doctor, recovery execution, shared isolation check and doctor READY assertions.

Independently executed: helper unit tests 4 PASS, bash syntax PASS, git diff --check PASS; exact changed paths/count 1 file, 1 insertion and 1 deletion. This review does not claim actual native reconciliation executed yet.

## Existing backup receipt attribution

Standalone Demo native backup run `40128218519` and artifact `12574207477` remain attributable only to source `a1051ec5f5c366cdfafe527298ac60e5db4f951c` (whose tree equals D). The targeted native workflow executes installation, backup acceptance and unchanged helper/syntax/cleanup paths; reconciliation is not part of that execution. A reconciliation-only successor therefore preserves those actual execution inputs, while no receipt is relabelled as a new successor run.

The canonical Core R `GitInputs.fingerprint` intentionally remains more conservative for tag v0.4.26: reconciliation is included in every gate's Demo object list. Consequently old canonical gate evidence cannot be reused across this change by asserting path irrelevance. Fresh planned selected 63 and full 65 must bind the actual final successor D; no verifier/source exception is proposed.

## Published and merged identity

PR #122 qualified source `9611629bf053b4ff08f29a8459b4e69f4248ed12` has sole parent old D `03396c805369e61d2e0745d00f78c8add809e2e0`. Actual resulting D is `09595781b68e1f41caaba9aec1402eb8009d700f`, with parents old D and source 9611629b. Both complete trees equal `9219f48d5abd04b8a062edf2d22b265e025ed82a`.

Remote old-D to actual-D comparison authenticates exactly the reviewed one-file, one-line delta, blob `2c128dbc455647088d2259d08d2fc9208617dadf`, with no other changed paths. Actual D's `baseharbor-core.ref` remains exact R; its blob remains `42fe65908c5bcaa8edb22e2ed60ede126c818e06`. No native result is relabelled to this merge commit.
