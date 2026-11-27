# 0428-284 — demo consent retry disposition

**Role:** Codex disposition. Evidence-only record; no code or task metadata changed.

## Witnesses

- The live 0428-284 card is `wait` with a blank/demoted owner and states that reactivation requires Codex/Owner disposition.
- Core PR #1866 is OPEN at `3702c09502203e82633d664690eac9484a370df9`, base `develop`, `mergeStateStatus=BLOCKED`.
- Pull-request run [45916731635](https://github.com/mcpdev80/baseharbor/actions/runs/45916731635), attempt 1, is FAILURE on that exact head. Its selected Docker and Podman `data-capabilities` jobs both failed; `PR Selected Checks` is the aggregate failure. The failing path is the demo guided-consent scenario, not a Core consent/auth behavior change. In `baseharbor-demo` develop, `tests/guided/drive.py:749-752` raises the guided-up abort before the second `up` when the retry flow has not completed.

## Disposition

Use the existing card **0428-284**; no new card is needed. The Owner expressly authorized one minimal demo-side PR in the test harness with consent/auth semantics unchanged. The write-set is only `tests/guided/drive.py`, to handle the nested consent hint, parse the digest, and explicitly retry with that digest. No Core product code, product consent/auth behavior, or workflow files are authorized by this disposition.

Target implementation lane: `w366-0428-284-democonsent`. This is a recommendation to reactivate the existing card with that worker target; the Coordinator retains its separate status/owner administration. No implementation, PR, close, or merge was performed here.
