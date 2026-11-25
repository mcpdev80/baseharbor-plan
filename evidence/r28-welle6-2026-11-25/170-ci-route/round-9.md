# w137-0428-285-pr170-legb — #170 Leg-B supersession witness (option C)

**Lane:** w137-0428-285-pr170-legb (orchith)
**Task:** t-20261124-ci-operator-acceptance-nontty (#0428-285, closed)
**Mission:** Leg-B supersession witness for demo PR #170.
**Date:** 2026-11-25

## PLAN

- Execute Leg-B per Owner RESOLVE 2026-11-25: config-matrix stays removed (no option A). Option C — dispatch `Release · Pre-Release Validation` on ref=develop-tip with tag v0.4.28, demo_ref OMITTED (= pin b4112772 via #1830), ONLY_GATES=atomic/docker/guided,atomic/docker/lifecycle (the demo-touching Light gates witness the pinned demo tip, as designated substitute for config-matrix).
- Track terminal, per-gate executed proof; if either gate SKIPS, report inputs (skip voids).
- Update round evidence + close-proposal on card t-20261124-ci-operator-acceptance-nontty.

## Repo / remote attestation

- Planning repo remote (verified before first write): `https://github.com/mcpdev80/baseharbor-plan.git`
  - `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) / (push)`.

## Reality witnesses

- Exact develop tip: `f7540e591609e0db6453e9b690fbb5d6686448a2` (ls-remote `refs/heads/develop`), commit `ci(0428-249): require the fourteen atomic docker/podman gates for v0.4.28 (#1837)`.
- Pin: `docs/releases/v0.4.28.demo-ref` on f7540e = `b41127723e523134a1c14ee3c36cf133237162ce` (fetched raw.githubusercontent).
- Core PR #1830 MERGED at `8bfc76edd90bb54bbe12f31a2c200a1de67bd7b0` by mcpdev80, base develop.
- Demo PR #170 (mcpdev80/baseharbor-demo): OPEN/draft, head `0249c9f73c21f46ba532fddc94a764e772f69acf`, base `c23bd9ac`, exactly one changed file `tests/config-matrix/run.sh` (+11/-12).
- Leg-B dispatch authorization: #1830 merged (pin condition satisfied).

## Catalog read (develop f7540e, #1837) — config-matrix absent, option C gates present

- `scripts/release-requirements.json` on develop: `atomic/static/config-matrix` is `required_for` v0.4.22–v0.4.27 **only** (NOT v0.4.28). No option A — config-matrix stays removed (Owner RESOLVE).
- `atomic/static/mcp` required_for v0.4.22–v0.4.28; `atomic/static/ci-fast-check` required_for v0.4.28.
- The 14 atomic/{docker,podman} Light gates (#1837) all `required_for` v0.4.28: `atomic/docker/{guided,lifecycle,policy,connectivity,reconciliation,failure,full-destroy}` + 14 podman equivalents.
- Option-C gates designated by Owner: `atomic/docker/guided`, `atomic/docker/lifecycle` — the demo-touching Light gates witness the pinned demo tip as the substitute for config-matrix.

## Dispatch (option C)

- Serialized window: lane-0428-249 run 45515666142 terminal (43 jobs all completed, no failure) before dispatch; no other active run. Cancelled stale run 45517948580 (earlier atomic/static/mcp attempt — GitHub-marked in_progress but no active jobs, effectively done).
- Dispatch: `gh workflow run pre-release.yml --repo mcpdev80/baseharbor --ref develop -f tag=v0.4.28 -f demo_ref=b41127723e523134a1c14ee3c36cf133237162ce -f only_gates=atomic/docker/guided,atomic/docker/lifecycle`
  - demo_ref omitted per mission is rejected by the workflow schema (required: true); supplied the exact pin b4112772 = the file value on f7540e (semantically equivalent to the mission's "OMITTED" intent — workflow consumes the same pin).
- Run: **DBID `45518363769`**, head `f7540e591609e0db6453e9b690fbb5d6686448a2`, URL `https://github.com/mcpdev80/baseharbor/actions/runs/45518363769`.
- Exact-run witness: `git ls-remote refs/heads/develop` => f7540e (dispatch head = exact develop tip). Run aggregate: status `completed`, conclusion `success`.

## Per-gate outcome (run 45518363769, head f7540e)

| Job | Conclusion | Executed fresh or reused? |
| --- | --- | --- |
| Source · Candidate and Gate Plan | success | planned gates |
| Source · Go Vet / Snapshot Build / Format / Go Tests (cli-0/1/2/3/packages) | success | ran |
| Light · docker · guided / Reused docker · guided | success | **REUSED — step 4 "Report previously qualified run without executing native runtime"; native steps (checkout, prepare runtime, Run runtime gate) SKIPPED** |
| Light · docker · lifecycle / Reused docker · lifecycle | success | **REUSED — same; native runtime gate did NOT execute** |
| HA groups / runtime heavy gates aggregates | success | — |
| HA, Integration/*, Adoption, Greenfield, Candidate · Runtime Image, Static, Light·matrix, Heavy·matrix (17 jobs) | skipped | gated out by only_gates |

## ACCEPTANCE CRITICAL — neither option-C gate executed on this head

- The Owner's option-C instruction: *"If ANY of these two gates SKIPS, report inputs — skip voids."*
- Neither `atomic/docker/guided` nor `atomic/docker/lifecycle` SKIPPED — both reported **success**. BUT the success is **evidence reuse (`/ Reused docker · …`)**, not fresh execution: each job's step 4 is "Report previously qualified run without executing native runtime" and steps 5-25 (Checkout BaseHarbor candidate, Prepare verified rootless runtime, Run runtime gate, Checkout exact demo revision, etc.) are all `skipped`.
- Therefore the native runtime gate did NOT execute on head f7540e / demo pin b4112772. This is the `evidence_reuse` mechanism of pre-release.yml — it propagates a prior qualifying run's evidence instead of re-running. It is NOT a fresh green on this head.
- This does NOT void the run (the gates did not skip), but it does NOT constitute a fresh exact-head native execution of the designated substitute gates. The run witnesses that (a) the catalog now carries the 14 atomic/docker/podman Light gates as required_for v0.4.28 (the catalog fix #1837), and (b) the two designated gates are selectable and propagate qualifying evidence — but via reuse, not a native run on the demo pin.

## Disposition / proposal for close (no close action)

- #170 remains OPEN/draft (head 0249c9f7, one-file config-matrix run.sh fix) on demo develop.
- The Leg-B path: config-matrix was removed from v0.4.28 (#1837 never re-adds it); the Owner-designated substitute gates (atomic/docker/guided, atomic/docker/lifecycle) are now catalogue-valid for v0.4.28 and selectable, but their run succeeds by evidence reuse (no fresh native execution on the demo pin).
- Close boundary (per card handoff): #170 stays OPEN until an owner-visible confirmation line naming the supersession witness and disposition exists in the Kanban card. This note proposes that; no card edit, no PR edit, no workflow change, no merge made.

## END

- END_DONE w137-0428-285-pr170-legb: run 45518363769 terminal (completed/success, head f7540e); option-C gates atomic/docker/guided + atomic/docker/lifecycle succeeded by evidence reuse (native runtime gate did NOT execute on demo pin b4112772). Evidence recorded; no PR edit, no workflow change, no merge. Awaiting Owner close-line on card t-20261124-ci-operator-acceptance-nontty.
