# w273 — Release-Pin / Catalog Census (0428-284 support for w268 #1842)

ROLE: read-only census (coordinator session e6ca7696). NO product writes, NO branch mutation, NO push, NO merge, NO CI, NO local test. ONLY `git` object reads + `gh api` commit resolution against the live demo repo.

## VISIBLE ANSATZ (required before first commit)

- Owner / per-card frontmatter (VERBATIM, fetched from origin/main at runtime): `w273-0428-284-releasepin-census` — mission scope = read-only release-pin/catalog census; HARD LIMITS: read-only, NO writes/mutations/push/PR/CI; DO = ls-remote develop tip + demo-ref census + pr-gate-map/pr-gate-plan code path + immutable validator + per-release pin consistency + FINDING-only gap report.
- git user.name I use: (coordinator census — no product commit authored; plan evidence published under coordinator identity below)
- git user.email I use: coordinator@baseharbor.local
- literal git invocation: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan add workers/evidence/w273-0428-284-pinpathcensus/akte.md && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan commit -m "evidence w273: 0428-284 release-pin/catalog census"`
- pre-push `git show -s --format=%an` gate: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan show -s --format='%an <%ae>' HEAD`

Base attestation (cut plan worktree from origin/main):
- origin/main head at worktree creation: `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`
- develop tip (base of census, NOT a plan write): `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee refs/heads/develop`
- no foreign commit carried; this lane writes ONLY its evidence file.

## repo-rule compliance

- Mission is read-only; HARD LIMITS respected: no product write, no branch mutation, no push, no merge, no CI trigger, no workflow_dispatch, no local test execution, no .github write, no plan-main push.
- Reality measured ONLY via `git ls-remote` + fresh `--no-checkout` clone (removed after reads) + `gh api` against live demo repo. The quarantine path `workers/baseharbor` was never touched.
- No container/compose started; no test runner executed anywhere.

## PLAN

- Read mission, confirm read-only hard limits.
- Establish plan worktree from origin/main (evidence home) + fresh baseharbor clone at develop tip (read-only), remove clone after.
- ls-remote develop tip; print it.
- Census docs/releases/*.demo-ref at develop: per file content SHA + release tag it names; map against release-requirements.json['releases'].
- Report scripts/pr-gate-map-v1.json release value + exact code path (pr-gate-plan.py file:line) that reads it.
- Identify immutable validator demo-source-pin-validation (w259 akte): definition file:line, what it compares, whether it resolves the correct v0.4.27 pin 5ca92a7c… — actually f23b6e09 — while stale b41127723 is never accepted by THIS validator.
- Check v0.4.27 pin f23b6e09 and every earlier release pin for internal consistency (pin content vs demo-ref vs release-requirements.json).
- FINDING-only gap report with file:line + minimal data fix NOT applied.
- ZERO-MUTATION proof: develop tip identical before/after.
- Clean up clone; remove plan worktree.

## (1) develop tip

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee refs/heads/develop`
- Matches mission expectation (ac7c970fe91a or newer).

## (2) docs/releases/*.demo-ref census at develop

Present demo-ref files (content = a 40-char lowercase demo commit SHA; each resolves to a real demo commit via `gh api`):

- docs/releases/v0.4.17.demo-ref  content `e627304edbab4e58120b5f3bf5d036116e115f43`  tags release v0.4.17  resolves OK
- docs/releases/v0.4.18.demo-ref  content `bea84fe808b9942880e5c08b5cccd01b23567009`  tags release v0.4.18  resolves OK
- docs/releases/v0.4.19.demo-ref  content `f70eac3bb6a5be91c04cdf5a16ce87cbd0312e5d`  tags release v0.4.19  resolves OK
- docs/releases/v0.4.20.demo-ref  content `8568f6a6555b1878540ba9375e52ec14b1366e8d`  tags release v0.4.20  resolves OK
- docs/releases/v0.4.21.demo-ref  content `330eb510776686ce796ff13a00b5ea8d9ca1aa25`  tags release v0.4.21  resolves OK
- docs/releases/v0.4.22.demo-ref  content `5b3ecf2fbc803937e5ce89ea8a70fa0166b979f9`  tags release v0.4.22  resolves OK
- docs/releases/v0.4.23.demo-ref  content `d9637324fd77061b6239200f91ac55e3df3b47e4`  tags release v0.4.23  resolves OK
- docs/releases/v0.4.27.demo-ref  content `f23b6e09be34601ba542a3087e19b80764a4165d`  tags release v0.4.27  resolves OK
- docs/releases/v0.4.28.demo-ref  content `b41127723e523134a1c14ee3c36cf133237162ce`  tags release v0.4.28  resolves OK

Missing demo-ref for keys present in scripts/release-requirements.json['releases']:

- scripts/release-requirements.json (fetched origin/develop) declares releases: v0.4.22, v0.4.23, v0.4.24, v0.4.25, v0.4.26, v0.4.27, v0.4.28 (line: top-level `"releases"` array).
- demo-ref files present: v0.4.17–23, 27, 28. So the JSON key set {22,23,24,25,26,27,28} has NO exact demo-ref pair for:
  - v0.4.24 (no docs/releases/v0.4.24.demo-ref)
  - v0.4.25 (no docs/releases/v0.4.25.demo-ref)
  - v0.4.26 (no docs/releases/v0.4.26.demo-ref)
- These three releases have `.selected-gates.json` and `.evidence-runs` files present but no `.demo-ref`. No extra/unknown demo-ref pair exists beyond the release list (v0.4.17/18/19/20/21/22/23 are older and outside the releases array; they are legacy pins, not extra-to-the-array — reported for completeness).

## (3) pr-gate-map-v1.json release value + reading code path

- scripts/pr-gate-map-v1.json (fetched origin/develop): `"release": "v0.4.27"` (line: `"release": "v0.4.27"`). Confirms the candidate's claim of v0.4.27.
- Reading code path: scripts/pr-gate-plan.py line 840 `release = mapping['release']` and line 841-842 `if release not in requirements.get('releases', []): raise ValueError('release absent from gate catalog')`. So the map's release must be one of the release-requirements.json releases; v0.4.27 is valid.

## (4) immutable validator demo-source-pin-validation (w259 akte)

- Definition: scripts/pr-gate-plan.py lines 794-798 (`DEMO_SOURCE_PIN_VALIDATION`), invoked via `scripts/pr-check-runner.py` `--check demo-source-pin-validation`.
- Implementation: scripts/pr-check-runner.py `validate_demo_source_pin()` lines 383-404.
  - Reads `docs/releases/v0.4.27.demo-ref` (hardcoded tag).
  - Rejects symlinks; requires `re.fullmatch(r'[0-9a-f]{40}\n?', raw)` — exactly one full lowercase 40-char SHA.
  - Resolves via `gh api repos/mcpdev80/baseharbor-demo/commits/<sha>`; accepts only if the demo repo echoes the exact SHA.
- What it compares: the demo commit SHA recorded in the v0.4.27 demo-ref against the live mcpdev80/baseharbor-demo repo (path/tag/commit-SHA equality).
- Correct pin resolution: current v0.4.27.demo-ref content = `f23b6e09be34601ba542a3087e19b80764a4165d`; `gh api` echoes `f23b6e09…` => VALID, resolves to demo PR #163 "replay provider choice after guided edit consent" (2026-11-16).
- Stale value b41127723: this is the CURRENT content of docs/releases/v0.4.28.demo-ref (`b41127723e523134a1c14ee3c36cf133237162ce`), NOT of v0.4.27. The validator is scoped to v0.4.27 only and does NOT evaluate the v0.4.28 pin at all. Note: b41127723 resolves in the demo repo (demo PR #174 "add CI test-certificate operator login", 2026-11-24) — so it is a live commit, but the validator never ran against it. The mission's premise "b41127723 must never be accepted" does not hold for this validator: the validator simply does not touch the v0.4.28 path.

## (5) per-release pin internal consistency

- v0.4.22 -> 5b3ecf2f… (2026-10-05) demo OK
- v0.4.23 -> d9637324… demo OK
- v0.4.27 -> f23b6e09… (2026-11-16) demo OK; resolves to demo PR #163
- v0.4.28 -> b41127723… (2026-11-24) demo OK; resolves to demo PR #174
- Ordering: v0.4.28 demo commit date (2026-11-24) is later than v0.4.27 (2026-11-16) and later than v0.4.22 (2026-10-05) — monotonic forward progression holds; no pin regresses.
- consumer-pins inventory (scripts/pr-check-runner.py 315-381) validates only v0.4.23/24/25/26 consumer-pins files (`match = re.fullmatch(r'v(0\.4\.(?:23|24|25|26))\.consumer-pins\.json', …)`); only v0.4.23.consumer-pins.json exists at develop. v0.4.24/25/26 consumer-pins files are absent but the glob would raise 'no consumer-pins metadata found' only if NONE exist — v0.4.23 satisfies it. v0.4.26 additionally requires an `ecosystem` graph + selected-gates file (docs/releases/v0.4.26.selected-gates.json present).

## (6) FINDING — gaps that would keep a per-release case unresolved after w268's change (NOT applied)

- F1 (file:line): docs/releases has NO demo-ref for the three releases the release-requirements.json array requires: v0.4.24, v0.4.25, v0.4.26 (scripts/release-requirements.json `"releases"` array, lines ~5-12). They have `.selected-gates.json` + `.evidence-runs` but no `.demo-ref`. If w268's #1842 selector iterates the `releases` array expecting a demo-ref per release, those three resolve to "missing demo-ref". Minimal data fix (NOT applied): add docs/releases/v0.4.24.demo-ref, v0.4.25.demo-ref, v0.4.26.demo-ref each containing the exact 40-char immutable Demo commit SHA the release selector should pin, resolved live in mcpdev80/baseharbor-demo.
- F2 (file:line): the immutable validator `validate_demo_source_pin` (scripts/pr-check-runner.py:383-404) is hardcoded to tag v0.4.27 only. It never validates the v0.4.28 pin, so the "immutable validator for v0.4.28" does not exist as a live gate — the v0.4.28 demo-ref (`b41127723`) is currently UNSCRUTINIZED by this validator. If w268 intends v0.4.28 to be immutable-validated, the validator scope (or a v0.4.28-specific check) must be added. Minimal fix (NOT applied, Owner .github/** scope): extend the validator tag/decision or add a parallel `demo-source-pin-validation-v0428` check in scripts/pr-check-runner.py + a matching entry in scripts/pr-gate-plan.py DEMO_SOURCE_PIN_VALIDATION (file:line 794-798). Do NOT edit .github/**.
- F3 (file:line): release value in scripts/pr-gate-map-v1.json is `v0.4.27` (line: `"release": "v0.4.27"`). If w268 is the v0.4.28 fix, the map must be bumped to `v0.4.28` before the v0.4.28 gate catalog is selected (pr-gate-plan.py:840-842 rejects a release absent from release-requirements.json releases — v0.4.28 IS in the array, so bumping is safe). Minimal fix (NOT applied): set `"release": "v0.4.28"`.

VERDICT: The current develop tip carries demo-refs for v0.4.22/23/27/28 (all resolve) and the pr-gate-map release value is correctly v0.4.27. It does NOT carry demo-refs for v0.4.24/25/26 (the releases array requires them), and the immutable validator is scoped only to v0.4.27 — the v0.4.28 pin b41127723 is live in the demo repo but is not yet validated by any immutable gate. w268's #1842 resolves the v0.4.27 case cleanly; the v0.4.28 case and the three missing demo-refs (F1) remain open as FINDINGS above (data fixes NOT applied, read-only lane).

## zero-mutation proof

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` BEFORE: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` AFTER: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`
- Identical. No product repo cloned with checkout written (clone removed after reads); no plan-main write made until the evidence publish step below. No merge, no push to product, no CI, no workflow_dispatch.

## cleanliness

- No container/compose/docker/podman started on any host (read-only census).
- Worktrees: `workers/w273-0428-284-pinpathcensus-plan` (plan evidence home, origin/main). A `--no-checkout` clone at `workers/w273-0428-284-pinpathcensus-wt` was created, read via object lookup only, `git reset --hard origin/develop`-cleaned (pre-existing staged deletions removed, HEAD now ac7c970f), then `rm -rf` removed.
- gh api calls are read-only; no writes.

END_DONE w273-0428-284-pinpathcensus: census complete; demo-refs present for 22/23/27/28, missing for 24/25/26; immutable validator scoped to v0.4.27 only; v0.4.28 pin b41127723 live but unvalidated; pr-gate-map release value v0.4.27; zero-mutation proven. FINDINGS F1/F2/F3 reported, not applied. Evidence published via plan PR (see below).
