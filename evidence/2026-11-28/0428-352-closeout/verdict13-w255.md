# 0428-352 follow-up verdict 13

Role: read-only review. Candidate `2d357c3dfb99e18149c6b37825f0e9ffab7ea5ee`, delta against `0bcb37d0c`, checked against the verdict 12 recipe. No cleanup mutation was run; both worker-cleanup invocations below omitted `--run`.

## Verdict

PASS for the requested R13 corrections.

- A completed live-agent listing is distinguished from a failed lookup. The resolver now handles a completed empty list as an authoritative zero-match before registry/lineage fallback (`scripts/release-lane.py:159-199`). A raised listing is separately marked as lookup failure and returns unresolved when the lane name is known (`scripts/release-lane.py:200-207`).
- The shared-directory sibling fixture is injected into `rl.agents` for the production resolver test (`tests/test_0428_352_session_retention.py:658-669`).
- A new empty-list plus stale-registry case verifies unresolved `None`, the name/parent path was entered, the registry path was not used, and the sibling DB row remains (`tests/test_0428_352_session_retention.py:681-730`).

## Verification

Command: `python3 -m unittest discover -s tests`

Result: `Ran 40 tests in 0.913s` / `OK`. The suite emitted existing `ResourceWarning`s from `scripts/card-status.py:76` and `:94` for unclosed task file handles; there were no failures.

Dry-run command: `./scripts/worker-cleanup.sh w401-0428-292-consentfix`

```text
evidence accepted from acceptance.json path: evidence/2026-11-27/0428-292/korrektur-1884-fix.md
PLAN release name=w401-0428-292-consentfix codeman=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c opencode=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c (w401-0428-292-consentfix)
DRY-RUN pool reservations: none
cleanup plan complete for w401-0428-292-consentfix (RUN=0)
```

Dry-run command: `./scripts/worker-cleanup.sh w402-0428-315-constfix`

```text
evidence accepted from acceptance.json path: evidence/2026-11-27/0428-315/korrektur-1882-fix.md
PLAN release name=w402-0428-315-constfix codeman=e0ed81d0-fac2-4f3d-aae3-0009e872f466 opencode=e0ed81d0-fac2-4f3d-aae3-0009e872f466 (w402-0428-315-constfix)
DRY-RUN pool reservations: none
cleanup plan complete for w402-0428-315-constfix (RUN=0)
```

The two dry-runs resolve independently to the requested lane names and IDs, with no ambiguous-lineage message.

## Cleanup authorization

Review verdict: PASS. This review does not itself certify or grant Coordinator authorization for the real `worker-cleanup.sh w401-0428-292-consentfix --run` and `worker-cleanup.sh w402-0428-315-constfix --run` operations. The instruction supplied for this review explicitly limits execution to dry-runs, and no separate Coordinator authorization for those real cleanup runs is present in the reviewed material. Do not treat this verdict as permission to run either command with `--run`; obtain the Coordinator's explicit authorization first.

END_DONE w255-0428-251-demo170codex: R13 review PASS; cleanup authorization not evidenced; candidate 2d357c3dfb99e18149c6b37825f0e9ffab7ea5ee
