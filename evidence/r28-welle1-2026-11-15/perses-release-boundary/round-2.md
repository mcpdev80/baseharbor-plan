# Mission: Fix r28 perses release-boundary mirror prose (round 2, PR #1577)

- Task: `t-20261114-r28-perses-release-boundary` (karte `t-20261114-r28-perses-release-boundary`)
- Candidate: `5e8d138cd659cbd7a72fde4713b3b1389b95dcdb`
- Base to attest as ancestor of first commit: `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95` (develop)
- Branch: `0428-092-perses-boundary` (draft PR #1577, base develop)

## PLAN

- Read recipe act-luna-r1.md and confirm the six EN/DE mirrors (release notes, reference, how-to) with the flagged state sentence
- Reduce each of the six mirror sentences to state-name mention + spec pointer, dropping the "depending on selected/pinned/reachable" paraphrase
- Run docs consistency/search check across the six mirrors + git diff --check locally
- Commit the fix on branch 0428-092-perses-boundary (FAST-FORWARD from 5e8d138)
- Push candidate, record ls-remote head SHA into evidence, push evidence to origin/main, post END_DONE

## Scope decision / instructions

- Recipe (luna-r1 verdict, REQUEST CHANGES): the six EN/DE-mirror release/reference/how-to passages name the states `not_configured`/`configured_unverified`/`verified` and add "...depending on whether it is selected, pinned and reachable..." / "...je nach Wahl, fixierter Pin und Erreichbarkeit...". That paraphrase omits the spec's required real health probe for `verified` and can imply reachability alone is sufficient. Fix = reduce each to state-name mention plus pointer to `docs/spec/management-access-v1.md`; do NOT introduce a competing shorthand. Stop if a wording change would redefine state semantics differently from the normative spec — then update spec first under its owning contract.
- Boundaries: no `.github/**`, no merge, no ready_for_review, no force-push, no subagent. Draft PR stays draft, base develop.

## Repo-rule compliance

- Docs-only change across six mirrors in the baseharbor product repo.
- No workflow files touched, no CI rerun/workflow_dispatch (Owner scope). No merge, no force-push, no subagent (§4.8).
- Evidence written only into baseharbor-plan (planning repo), never into the product repo.

## Base attestation

- Planning repo (baseharbor-plan) HEAD before first evidence commit:
  `git log --oneline -1` => `e8ea6ca0 kanban: t-20261114-r28-perses-release-boundary -> active`
  `git rev-parse HEAD` => `e8ea6ca0b1be2bae1663cfe5a750c0bc625c9288`
  (baseharbor-plan is the planning repo ONLY; workers/baseharbor-plan is NOT the planning repo.)
- Product base/ancestor attestations (ls-remote origin):
  `git ls-remote origin refs/heads/develop` => `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95`
  `git ls-remote origin refs/heads/0428-092-perses-boundary` => `5e8d138cd659cbd7a72fde4713b3b1389b95dcdb`
  Candidate head == recipe SHA 5e8d138. develop is the base ancestor of the branch.

## Before/after witnesses

Files changed: 6 (3 EN + 3 DE mirrors). Original sentence (EN, release notes) at `docs/releases/v0.4.28.md:15`:

> Perses is optional; its status may read `not_configured`, `configured_unverified` or `verified` depending on whether it is selected, pinned and reachable in the current environment. The normative state definition lives in docs/spec/management-access-v1.md.

Original sentence (DE, release notes) at `docs/de/releases/v0.4.28.md:13`:

> Perses ist optional; ihr Status kann `not_configured`, `configured_unverified` oder `verified` lauten, je nach Wahl, fixierter Pin und Erreichbarkeit in der aktuellen Umgebung. Die normative Zustandsdefinition steht in docs/spec/management-access-v1.md.

Original sentence (EN, reference) at `docs/reference/releases.md:31` and (DE) at `docs/de/reference/releases.md:30` (embedded in a larger paragraph, same "...depending on whether it is selected, pinned and reachable...").

Original sentence (EN, how-to) at `docs/how-to/observability.md:32` ("...depending on the current environment;...") and (DE) at `docs/de/how-to/observability.md:28` ("...je nach aktueller Umgebung;...").

## Correction applied (after)

EN mirrors now read (state-name mention + spec pointer only):

- `docs/releases/v0.4.28.md`:
  > Perses is optional; its state may be `not_configured`, `configured_unverified` or `verified`. The normative state definition lives in docs/spec/management-access-v1.md.
- `docs/reference/releases.md`:
  "The Perses visualization surface is optional; its state may be `not_configured`, `configured_unverified` or `verified`. The normative state definition lives in docs/spec/management-access-v1.md."
- `docs/how-to/observability.md`:
  "Its state may be `not_configured`, `configured_unverified` or `verified`; the normative state definition lives in docs/spec/management-access-v1.md."

DE mirrors now read:

- `docs/de/releases/v0.4.28.md`:
  > Perses ist optional; ihr Status kann `not_configured`, `configured_unverified` oder `verified` lauten. Die normative Zustandsdefinition steht in docs/spec/management-access-v1.md.
- `docs/de/reference/releases.md`:
  "ihr Status kann `not_configured`, `configured_unverified` oder `verified` lauten. Die normative Zustandsdefinition steht in docs/spec/management-access-v1.md."
- `docs/de/how-to/observability.md`:
  "Ihr Status kann `not_configured`, `configured_unverified` oder `verified` lauten; die normative Zustandsdefinition steht in docs/spec/management-access-v1.md."

None of the new wordings redefine state semantics; `verified` is no longer tied to reachability alone and defers to the normative spec.

## Checks

- `git diff --check` (local, working tree): clean
- docs consistency/search check across six mirrors: grep for the old "...depending on ... selected, pinned and reachable" / "...je nach Wahl, fixierter Pin und Erreichbarkeit..." pattern — returns NONE (all six sentences reduced; no competing reachability shorthand remains).
- exact-head docs CI: dispatched by coordinator (not run here; Owner scope).

## Branch provenance & delivery

- Product base/ancestor attestations (ls-remote origin):
  - `git ls-remote origin refs/heads/develop` => `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95` (base ancestor)
  - `git ls-remote origin refs/heads/0428-092-perses-boundary` before my branch => `5e8d138cd659cbd7a72fde4713b3b1389b95dcdb`
- Candidate branch `0428-092-perses-boundary` HEAD (ls-remote verified):
  `git ls-remote origin refs/heads/0428-092-perses-boundary` => `70b7bfc8e99c79cb20acc6974c67dcf2c037d446`
- Only my commit sits above the base: `git log --oneline 5e8d138..0428-092-perses-boundary` => `70b7bfc8e docs(perses): reduce release-boundary mirror prose to state-name mention + spec pointer`
- `git merge-base --is-ancestor 5e8d138 HEAD` => YES (fast-forward only; no foreign commits carried).
- PR #1577 (base develop, draft): `gh pr view 1577 --repo mcpdev80/baseharbor --json draft` => draft true.

## Recovery note (scope incident)

- After the first edit pass a foreign checkout (`lane-0428-080-r28-perses-selection`) moved the shared product-repo HEAD onto a merge of other lanes' commits and orphaned my working-tree edits. Recovered by: re-checking out the clean base `5e8d138`, re-applying the exact six sentence reductions, committing one docs-only commit `70b7bfc8e`, then pointing branch `0428-092-perses-boundary` at it and pushing. The contaminated foreign commits were never carried onto this branch. No product state was lost; the working-tree edits were re-applied from the known originals.

## Delivery

- Branch: `0428-092-perses-boundary` (draft PR #1577, base develop)
- Candidate pushed head (ls-remote): (paste)
- Evidence on origin/main: (paste `git ls-remote origin refs/heads/main`)

## END

END_DONE mission-fix-boundary.md: reduced six EN/DE perses-mirror sentences to state-name mention + spec pointer; candidate on 0428-092-perses-boundary @ 70b7bfc8e99c79cb20acc6974c67dcf2c037d446; evidence on baseharbor-plan origin/main @ 75ceb980

## Final attestations

- Product base (ls-remote origin): `git ls-remote origin refs/heads/develop` => `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95`
- Candidate head (ls-remote origin): `git ls-remote origin refs/heads/0428-092-perses-boundary` => `70b7bfc8e99c79cb20acc6974c67dcf2c037d446`
- Only my commit above base: `git log --oneline 5e8d138..0428-092-perses-boundary` => `70b7bfc8e docs(perses): reduce release-boundary mirror prose to state-name mention + spec pointer`
- `git merge-base --is-ancestor 5e8d138 HEAD` => YES (fast-forward only)
- PR #1577: `gh pr view 1577 --repo mcpdev80/baseharbor --json isDraft,state` => `{"isDraft":true,"state":"OPEN"}` (draft, base develop)
- Evidence commit: `git commit 75ceb980` on baseharbor-plan, file `evidence/r28-welle1-2026-11-15/perses-release-boundary/round-2.md` present in origin/main tree; origin/main HEAD (ls-remote) => `75ceb980849783553dc894fd11dd627311c41857`
- `git diff --check` clean; no old "...selected, pinned and reachable"/"...je nach Wahl, fixierter Pin und Erreichbarkeit"/"...je nach aktueller Umgebung"/"...depending on the current environment" pattern remains in docs/.
