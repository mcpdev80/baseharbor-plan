# w166-0428-302-coverage-rows: END_BLOCKED (scope decision required)

- Lane: w166-0428-302-coverage-rows
- Card: t-20261125-hunt35-catalog-coverage-completion (0428-302)
- Status: BLOCKED — no valid data-only edit exists; awaiting owner/scope decision

## Base attestation

- Planning repo remote (first action): `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch), `origin https://github.com/mcpdev80/baseharbor-plan.git` (push).
- baseharbor real GitHub remote: `lane-origin https://github.com/mcpdev80/baseharbor.git`; `origin`/`upstream` also point there; no local-filesystem origin in this checkout.
- Base develop (ls-remote, fetched fresh): `a87da7d179e08d43e8987885c38ab459ff1d887d refs/heads/develop`.
- Branch cut: `lane-0428-302-coverage-rows` at `a87da7d179e08d43e8987885c38ab459ff1d887d`; `git merge-base --is-ancestor origin/develop HEAD` = develop IS ancestor; `git log --oneline origin/develop..HEAD` = empty (no commits yet).
- Git identity set to lane string: `user.name=w166-0428-302-coverage-rows`, `user.email=w166-0428-302-coverage-rows@baseharbor.local` (identity admission rule; no candidate commit yet, so %an check pending at push time).

## The three gates the mission points to

From `scripts/release-requirements.json`, absent from `scripts/pr-gate-coverage.json` `gates`:

- `integration/docker/remote-target` — jobs `integration_remote_target_docker`, `required_for` [v0.4.23, v0.4.24, v0.4.25, v0.4.26]
- `integration/podman/remote-target` — jobs `integration_remote_target_podman`, `required_for` [v0.4.23, v0.4.24, v0.4.25, v0.4.26]
- `integration/static/live-console` — jobs `integration_live_console`, `required_for` [v0.4.23, v0.4.24, v0.4.25, v0.4.26]

All three have no `source.gate.*` surfaces mapped in the coverage catalog (they are external consumer-repo integration gates, Console/Connector/Demo).

## Why the data-only edit fails

The coverage `release` is `v0.4.27`. The trusted validator `scripts/validate-pr-gate-coverage.py` enforces (line ~211-218):

- `required_ids` = gates in `release-requirements.json` where `v0.4.27` is in `required_for`.
- `missing = required_ids - seen_gates` must be empty.
- `extra = seen_gates - required_ids` must be empty.

The three consumer gates are NOT `required_for` v0.4.27. Adding any of them makes `extra` non-empty:

```
coverage catalog includes gates outside active release catalog: integration/docker/remote-target
```
validator exit code 1.

Empirical reproduction: appended `integration/docker/remote-target` (covers `contracts.public-api`, `scope: pr`, `selection_scope: focused`) to a copy and ran the validator -> FAIL exit 1. Restored the file; unmodified validator PASSES (exit 0).

## Consistency with the evidence findings

H-V35 findings.md "Cross-file consistency" states verbatim: the three gates are `required_for` v0.4.23..v0.4.26 (not v0.4.27), release-only integration gates belonging to a released lifecycle, and "Their absence from the coverage catalog is expected, not a finding." No gate newly required for v0.4.27 is missing from coverage. So the current catalog is already correct for the v0.4.27 release the card targets.

## Scope note

- No product change made. `git status` clean except untracked `.last-owner-report`; `git diff` empty.
- No `.github/**` edits, no workflow triggers, no runner changes.
- No containers/compose projects started; no docker/podman run on this host.

## Next step / blocker

- Needs an owner scope decision: the mission's "add the 3 missing gates" conflicts with the v0.4.27 release gate set and would fail the trusted CI validator. Options under review — (a) the intended target release is a pre-v0.4.27 tag (v0.4.26) where these gates ARE required, or (b) a different write-set than `scripts/pr-gate-coverage.json`, or (c) an explicit owner override to add `release-only` rows despite the `extra` check. Lane is idle-pending and has posted a QUESTION line.

## Cleanliness

- `docker ps -a` before: none. `docker ps -a` after: none. No compose projects launched (read-only catalog analysis only).

## Status

END_BLOCKED w166-0428-302-coverage-rows. Candidate SHA not yet produced (no commit; base a87da7d179e08d43e8987885c38ab459ff1d887d). Awaiting scope decision.
