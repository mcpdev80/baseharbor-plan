# 0428-352 closeout receipt

## PLAN

1. Claim the existing 0428-352 card in the isolated Plan worktree and record the exact base and commit identity.
2. Copy the R1–R13 review records, W392 implementation note, and W255 practice retest into this card's Plan evidence directory.
3. Record the Coordinator-reported W401/W402 RELEASED receipts and check current session/pool metadata without running cleanup.
4. Update only card 0428-352 with its closure resolution and evidence links, then render and check the complete Plan repository.
5. Push the existing candidate branch, open a Plan PR, wait for exact-head Plan validation, review the final diff, and merge only if all gates pass.

## Commit identity and provenance

Card owner frontmatter verbatim after claim: `w255-0428-251-demo170codex (session eb8c3da9-6fcb-43a7-949e-dc1833cd7beb)`.
Commit author/committer name: `w255-0428-251-demo170codex`.
Commit email: `w255-0428-251-demo170codex@baseharbor.local`.
Invocation: `git -c user.name='w255-0428-251-demo170codex' -c user.email='w255-0428-251-demo170codex@baseharbor.local' commit ...`.
Pre-push author gate: `git show -s --format=%an HEAD` must print `w255-0428-251-demo170codex`.

Plan repository remote witness: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
Base point fetched from origin/main: `96cada1245dcaaf325a7785644371e471a264f17`.

## Status

Closeout content is prepared in this isolated branch. Plan render/check passed with zero errors and ten existing warnings. Exact-head Plan PR validation remains pending.

## Closeout findings and receipts

The coordinator repo contains the reviewed commit `2d357c3dfb99e18149c6b37825f0e9ffab7ea5ee`, authored by `w392-0428-284-demo183fix5`. W255's independent verdict 13 accepts that candidate after the authoritative-empty-list, fail-closed lookup-error, injected sibling-fixture, and stale-registry regression fixes. The R13 test command was `python3 -m unittest discover -s tests`; result: 40 tests passed, with existing `ResourceWarning`s from `scripts/card-status.py` file handling.

Coordinator release receipt records from `coordinator/scripts/.release-receipts.json`:

- W401 `w401-0428-292-consentfix`: `session_id=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c`, `opencode_id=2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c`, timestamp `2026-11-28T01:14:55Z`; Coordinator reports `RELEASED`, `pool=none`.
- W402 `w402-0428-315-constfix`: `session_id=e0ed81d0-fac2-4f3d-aae3-0009e872f466`, `opencode_id=e0ed81d0-fac2-4f3d-aae3-0009e872f466`, timestamp `2026-11-28T01:15:01Z`; Coordinator reports `RELEASED`, `pool=none`.

Bounded current session check: `codeman agent list --json` filtered by exact names returned W255 busy, W267 idle, W392 idle; W401 and W402 were absent. `python3 scripts/pool-reconcile.py status` reported `counts={flash:0,laptop:0,ornith:1}`, `worker_count=1`, `unknown_workers=[]`, and no expired holds. Thus the named W401/W402 sessions are no longer present, with W392 as the only remaining worker in that status snapshot.

Replay storm counters for the resolved transport/inventory incident: W392 ×45, W255 ×90, W267 ×69, W401 ×36, W402 ×34. Root cause and repair: shared `workers/.models/<channel>` paths made directory-based lane mapping ambiguous; the early PARTIAL path did not preserve an exact durable reference; stale pending events replayed cleanup. The accepted exact-identity resolver, retained retry ticket, reservation-until-gone rule, and remove-time replay suppression close those paths. Source files for every review round are listed in this directory: verdict01 through verdict13, `implementation-w392.md`, and `praxis-w255.md`.

Closeout Plan PR and exact-head validation details will be recorded after the final PR head is known. Exact plan base: `96cada1245dcaaf325a7785644371e471a264f17`.
