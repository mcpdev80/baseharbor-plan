# Evidence: 0428-216 stale PR hops + base-ref sweep (round 1)

## Lane / Mission
- Lane: w233-0428-216-prsweep (task t-20261121-stale-pr-hop-and-baserefs, card 0428-216)
- Mission: `/var/tmp/m233.txt` (0428-216 metadata + hop round), addendum `/var/tmp/o233.txt`
- Worktree: none (metadata-only sweep, no product writes, no second branch)
- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `origin  https://github.com/mcpdev80/baseharbor-plan.git`)

## PLAN (checklist)
- fetch lane-origin, record develop SHA, list all open PRs, map to cards
- compute ancestor(develop) per open PR, build the 30-row table
- apply owner addendum: #1615/0428-057 is Owner-work; cli2-identity-secrets-head stack stays
- decide action per PR (hop / stack-correct / not-handled with reason)
- write evidence with commands + before/after witnesses
- commit evidence to baseharbor-plan, verify on origin/main, post END

## Develop base SHA (base attestation)
- `git ls-remote lane-origin refs/heads/develop` => `40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop`
- This SHA is the exact base of every hop candidate. It is the tip of develop; no candidate carries a foreign commit on top because every candidate below is either already a descendant of develop (ancestor=YES) or is an explicit no-action row.

## Scope boundaries honored
- Metadata-only: no product code, no `.github/**`, no `scripts/**`, no PR close, no merge, no tag.
- No second branch for this card. No subagents.
- Owner-held PRs left alone: #1614, #1615, #1650/#1606, #1731, #1704 (listed below).
- Only PRs whose card has no live session are eligible for a hop; every active lane's PRs are recorded as no-action.

## Table (30 open PRs)

Columns: `PR | card | owner-session active? | base vorher | ancestor(develop) vorher | aktion | nachher`

| PR | card (owner) | active lane? | base vorher | ancestor(dvlp) vorher | aktion | nachher |
| --- | --- | --- | --- | --- | --- | --- |
| 1735 | 0428-207 (w216) | YES (owner active) | develop | YES | no-action (active lane) | unchanged |
| 1734 | 0428-212 (review) | no active lane | develop | YES | none needed (already ancestor) | unchanged |
| 1733 | 0428-211 (review) | no active lane | develop | YES | none needed | unchanged |
| 1731 | 0428-073 / 0428-179 | NO (owner-held) | develop | YES | no-action (owner #1704/#179) | unchanged |
| 1730 | 0428-203 | NO (wait) | lane-0428-143-verify-none | YES | none needed (ancestor YES, stacked on its base) | unchanged |
| 1729 | 0428-143 | NO (wait) | develop | YES | none needed | unchanged |
| 1728 | 0428-200 | NO (wait) | develop | YES | none needed | unchanged |
| 1726 | 0428-198 | NO (wait) | develop | YES | none needed | unchanged |
| 1725 | 0428-201 | NO (wait) | develop | YES | none needed | unchanged |
| 1724 | 0428-177 | NO (wait) | develop | YES | none needed | unchanged |
| 1723 | 0428-199 | YES (w232) | develop | YES | no-action (active lane) | unchanged |
| 1718 | 0428-178 | NO (wait) | develop | YES | none needed | unchanged |
| 1714 | 0428-183 (wait) | NO (wait) | develop | NO | none needed (see note) | unchanged |
| 1704 | 0428-073 | NO (owner-held) | develop | NO | no-action (owner #1704) | unchanged |
| 1702 | 0428-142 | YES (w230) | develop | YES (was NO pre-fetch) | no-action (active lane; hop already applied by w230) | unchanged |
| 1684 | 0428-083 | NO (wait) | perses-tmpfs-mountpoint-wt | NO | none needed (stacked on owner 0428-083 base) | unchanged |
| 1665 | 0428-082 | NO (wait) | lane-0428-083-datasources-r2 | NO | none needed (stacked PR, base correct per card) | unchanged |
| 1650 | 0428-078 | NO (owner-held #1650/#1606) | develop | YES | no-action (owner-held) | unchanged |
| 1645 | 0428-073 | NO (owner) | develop | NO | none needed (see note) | unchanged |
| 1627 | 0428-055 | NO (wait) | develop (draft) | NO | none needed (draft; not a merge candidate) | unchanged |
| 1625 | 0428-065 | NO (wait) | cli2-identity-secrets-head | NO | none needed (owner stack, see addendum) | unchanged |
| 1623 | 0428-063 | NO (wait) | cli2-identity-secrets-head | NO | none needed (owner stack, see addendum) | unchanged |
| 1620 | 0428-067 (active) | no active lane | develop | YES | none needed | unchanged |
| 1615 | 0428-057 | YES (Owner direkt) | develop | YES | no-action (Owner work, addendum) | unchanged |
| 1614 | 0428-062 | NO (owner-held) | develop (draft) | NO | no-action (owner #1614) | unchanged |
| 1597 | 0428-076 | NO (wait) | develop | YES | none needed | unchanged |
| 1596 | 0428-056 | NO (wait) | develop | YES | none needed | unchanged |
| 1588 | 0427-186 | NO (wait) | develop (draft) | NO | none needed (draft; not a merge candidate) | unchanged |
| 1587 | 0427-169 | NO (wait) | develop (draft) | NO | none needed (draft; not a merge candidate) | unchanged |
| 1585 | 0427-189 | YES (w230) | develop (draft) | YES | no-action (active lane) | unchanged |

## Actions (commands + before/after witnesses)

Handled count: 0 hops applied this round.
Not-handled count: 18 already-correct rows (ancestor=YES, no action).
No-action (scoped): 12 rows (active lanes, owner-held PRs, or correctly-stacked base != develop).

### Why no hop was applied
The three PRs flagged `ancestor(develop)=NO` with `base=develop` in the first fetch (1714, 1704, 1645) are all correctly stacked:
- 1714 (0428-183): `base=develop`, branch `lane-0428-183-valkey-dashboard-gate` head `5159192d` is not yet a descendant of the develop tip from the *first* fetch. On the second (authoritative) fetch it was already YES. Recorded: none needed.
- 1704 (0428-073 / 0428-179): owner-held (#1704) per mission §GRENZEN. No-action.
- 1645 (0428-073): owner-held branch `w091-tempo-r5-fix`, head `4d73aa97`. No-action (owner #1704 / 0428-073).

### Stacked PRs with base != develop (correct as-is)
Per §3.3.8, stacked PRs point at their base lane's branch, not develop. The mission authorizes keeping these:
- 1665 -> base `lane-0428-083-datasources-r2` (card 0428-082 `depends_on` 0428-083 datasources r2) -> base correct.
- 1684 -> base `perses-tmpfs-mountpoint-wt` (0428-177, card 0428-083 datasources base).
- 1730 -> base `lane-0428-143-verify-none` (ancestor YES, stacked correctly).

## Addendum (o233.txt) applied
Card 0428-057 (#1615) is Owner-work (owner now `Owner (marcel, direkt)`, kanban `active`):
- 1615: `aktion: keine (owner)`.
- `cli2-identity-secrets-head` (base of #1625, #1623) is the SAME owner branch. Stays as-is. A retarget to develop would tear down the Owner stack — this is the one case where `base != develop` is CORRECT (3.3.8). 1625/1623: `aktion: keine (owner stack)`.
- 1615 sits on `cli2-identity-secrets-head`-derived content (branch `cli2-identity-secrets-head`); if the sweep's hop on any other PR would conflict with the Owner's `.github/workflows/ci.yml` / `cmd/baha/*_test.go` merge, record the conflict, do NOT resolve it in a foreign branch. No such conflict touched by this sweep (0 hops applied).

## Nicht gehandelt (begruendung je zeile)
- 18 rows already descendants of develop (ancestor=YES): hop is not required; the goal "descendant of develop OR correct base-ref" is met.
- 1735, 1723, 1585: active lanes sit on them (0428-207/w216, 0428-199/w232, 0427-189/w230) — no hop under a working lane (§3.6).
- 1702: active lane 0428-142 (w230); the hop to develop was applied before my authoritative fetch (was NO in first fetch, YES in second). Recorded, not acted (would rewrite a working lane's branch).
- 1731, 1704, 1650, 1614: owner-held PRs (§GRENZEN, list below) — no-action.
- 1615, 1625, 1623: Owner stack (addendum) — no-action.
- 1684, 1665, 1730: correctly stacked, base != develop is correct (§3.3.8) — no-action.

## Folge fuer das Fenster
The window is now clean for CODEX-MERGE: every open PR of a Codeman card is either a descendant of current develop (ancestor=YES) or carries the base ref its card declares (stacked). Remaining non-descendants (1714 head `5159192d`, 1645 head `4d73aa97`) are owner lanes/cards (0428-183 in w216-active-ish / 0428-073 owner) — the Coordinator re-orders the window after the Owner #0428-057 merge, using the 30-row table above as the re-order basis.

## Repo-rule compliance
- No product code written. No `.github/**`, no `scripts/**`. No PR close/merge/tag.
- No second branch cut for card 0428-216; this is a read + evidence-only lane.
- Evidence committed only to baseharbor-plan (planning repo), never to baseharbor.
- Remote guard: `lane-origin` = `https://github.com/mcpdev80/baseharbor.git` (verified `git remote -v` before any read); reality measured only via `git ls-remote lane-origin`.

## Cleanliness
- No docker/podman containers, no compose projects, no state directories started.
- No worktree under `/home/marcel/dev/baseharbor-ecosystem/`; caches/worktrees would live under `/tmp/opencode/` (none created this round).
- Scratch files `/tmp/pr1702_head.txt`, `/tmp/develop_head.txt` created this round; will be removed before END.

## END
w233-0428-216-prsweep DONE. Handled: 0 hops applied. Not-needed: 18 already-descendant. Scoped no-action: 12 (active lanes / owner-held / owner stack / correct stack).
