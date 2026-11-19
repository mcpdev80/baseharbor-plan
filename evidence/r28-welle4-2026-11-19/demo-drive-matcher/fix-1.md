# 0428-129 — Demo `drive.py` matcher follows the core Warning-marker rule

- Mission: `/var/tmp/missions/mission-demo-drive-matcher.md`
- Card: `t-20261119-r28-demo-drive-matcher-warning-marker` (0428-129, baseharbor-demo, release v0.4.28)
- Content dependency: 0428-126 (core, PR https://github.com/mcpdev80/baseharbor/pull/1696, MERGED into core `develop` as `da76c5cf9c963207038d5599bd130b89ecb1e8a4`)
- Lane worktree: `/tmp/opencode/demo-drive-matcher-wt`, single candidate branch `lane-0428-demo-drive-matcher` (no second branch for this card)
- Wrong-zone check (pasted as required): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the real planning repo, not `workers/baseharbor-plan`)

## PLAN

1. Realitaetsabgleich: demo `ls-remote` (main/develop), core-akte `dualmatch-docs/fix-1.md`, core PR #1696 diff + merged files — DONE
2. Rote regression ZUERST: marked stages werden vom bisherigen Muster nicht erkannt — DONE (see "Red before green")
3. matcher in `drive.py` auf die core-Regel gezogen, `new_edit.py` teilt dieselbe Regel — DONE
4. demo regression erweitert (neue Faelle + unveraenderter Fall ohne Rutsch) — DONE
5. Kleinste passende demo-CI auf exaktem Kopf selbst bis terminal (Eigenes-Run-Pflicht) — DONE (run 44477622615 `completed success` at `bc4c6113b`)
6. Akte mit datei:zeile je aenderung, rot->gruen, run-id + kopf, revision-labels; committen/pushen — this file
7. PR im demo-repo (ein PR pro karte), handoff mit PR-nummer + head — DONE
8. Host besenrein, END-POST — DONE (see "cleanliness")

## Handoff

- PR: https://github.com/mcpdev80/baseharbor-demo/pull/165 (one PR for card 0428-129), base `main`, head branch `lane-0428-demo-drive-matcher`, head SHA `bc4c6113be92599c962b2377b038173593483a18`.
- Branch cut from demo `origin/develop@5d1cf312e18d06915db35c340bebe4e3d4f39d45`; `develop` is not an ancestor of `main`, and the demo PR gate only triggers on `main` (finding with file:line above) — that is why the PR base is `main`. After merge into `main` the normal promotion carries it into `develop`.
- Required check: run `44477622615` (`Demo · PR guided consent regressions`) `completed success` at the exact head, observed by this lane.
- Card state: `review`. Merge, acceptance and any release/tag are not this lane's steps.

## The real core rule (measured, not remembered)

Sources read at the merged core head `da76c5cf9…` (not from the memo):

- `cmd/baha/provider_change_confirmation.go` — `providerImpactAttentionLead(plan)` returns `"Warning: "` when and only when `plan.Attention != ""`, and `""` otherwise. It is PREPENDED to
  - `readProviderApplyAcknowledgement`: `"Apply these changes?"`, and for a destructive plan `"Apply these changes and permanently delete the listed data?"`;
  - `readProviderImpactAcknowledgements`: the fallback label `"Confirm the displayed provider changes"`.
  The same function then OVERWRITES that fallback with a catalog label when `plan.Destructive` (`ProviderDestructiveConfirm`) or `plan.ConfirmationsRequired == 2` (`ProviderTwoStageConfirm`) — no lead is prepended for those two branches.
- `internal/application/provider_change_consent.go` — `ProviderImpactConsentCatalog()` values ALREADY carry the lead inside the string: `"Warning: confirm the displayed outcome without a working alternative"`, `"Warning: confirm the displayed changes and permanent data deletion"`.
- `internal/application/provider_change_plan.go:93,98` — the shipped marker VALUE is `"Warning"`; the German prose `"Achtung:"` is retired (core #1663 rename, 0428-093).

Rule for the consumer, in one sentence: an acknowledging stage prints one of those labels, optionally with a core-prepended `"Warning: " ` lead on the two hardcoded labels, and the lead never changes the gate (`attention != ""` presence).

## What the demo did wrong (the gap)

`tests/guided/drive.py` (pre-fix, lines 507/508/520) and `tests/guided/new_edit.py:203/209` hardcoded a per-spelling alternation:

- stage matcher knew only `Confirm the displayed provider changes` (marker-less, hardcoded, position `(1/1` or `(1/2`) and the catalog label `…confirm the displayed outcome without a working alternative` at `(1/…` and `(2/2`, plus the RETIRED `Achtung:` spelling as an alternative;
- the destructive catalog label `Warning: confirm the displayed changes and permanent data deletion (1/2|2/2, plan …)` was absent entirely, and so was any marked apply-stage form — including `"Warning: Apply these changes and permanently delete the listed data? [y/N]: "`.

Consequence: for those stages the demo driver typed nothing, so an acknowledged stage read as not-acknowledged (demo-side false negative), exactly what the mission describes.

## Red before green (mission point 2)

The regression is written first, at the untouched base `5d1cf312e…`, with the matchers NOT yet changed. `tests/guided/test_consent_capture.ConsentCaptureRegression` collects `PRE_COUPLING_UP_RULES` — a verbatim copy of the pre-fix matcher set — and asserts the gap against it, plus asserts the production rule set no longer behaves that way.

Red witness at the base (matchers pre-fix, `git stash push -- tests/guided` then the same test bodies; `/var/tmp/demo-drive-matcher-red-base.log`):

```
FAIL: test_22_pre_coupling_matcher_misses_marked_stages
AssertionError: unexpectedly None : CurrentConsent rule misses: 'Warning: confirm the displayed changes and permanent data deletion (1/2, plan aaa…)? [y/N]: '
FAIL: test_21_core_acknowledging_stages_lead_rule_matches_up_rules
AssertionError: ["no up rule matches: 'Warning: confirm the displayed changes and permanent data deletion (1/2, plan …)? [y/N]: '", … ]
```

i.e. the marked destructive stage and the marked apply stage are provably NOT recognized by the pre-coupling pattern. Green at the candidate (`/var/tmp/demo-drive-matcher-green-tests.log`, exact head `bc4c6113be92599c962b2377b038173593483a18`):

```
test_21_core_acknowledging_stages_lead_rule_matches_up_rules ... ok
test_22_pre_coupling_matcher_misses_marked_stages ... ok
test_23_current_consent_rule_accepts_marked_and_plain_stages ... ok
test_24_marker_lead_only_variants_are_the_same_stage ... ok
test_25_replaced_led_alternation_is_retired ... ok
```

## Changes (file:line at candidate `bc4c6113be92599c962b2377b038173593483a18`)

- `tests/guided/drive.py:208-262` — new single source of truth: `ACKNOWLEDGE_LABELS` (the three consequence labels exactly as the core renders them), `ATTENTION_MARKER`/`ATTENTION_LEAD`, `RETIRED_ATTENTION_MARKER` (documentation/negative guard only), `CORE_PREPENDED_LEAD_LABELS` (the two labels whose lead the core PREPENDS, i.e. can appear or vanish), `stage_pattern(label)` and the two generators `provider_impact_acknowledgement_pattern(stage, total)` / `provider_impact_apply_pattern()`.
- `tests/guided/drive.py:571-578` (`up_rules`) — the two stage rules and the apply rule now come from those generators; the hardcoded alternation and the retired `Achtung:` alternative are gone.
- `tests/guided/new_edit.py:17-23` — imports `ACKNOWLEDGE_LABELS`, `provider_impact_apply_pattern`, `stage_pattern` from `drive` (one rule, no second interpretation).
- `tests/guided/new_edit.py:203-211` (`CurrentConsent.rule`) — built from `stage_pattern` over `ACKNOWLEDGE_LABELS`, keeping the positional `(stage)/(total)/plan` capture groups the replay guard in `respond()` depends on.
- `tests/guided/new_edit.py:214-216` (`apply_changes_rule`) and `tests/guided/new_edit.py:449` (edit-into-lifecycle apply rule) — use `provider_impact_apply_pattern()`.
- `tests/guided/test_consent_capture.py:80,88` — the fake-core fixture recognizes the apply prompt by prefix (`"Apply these changes"`) instead of the exact marker-less string, so a marked apply stage still behaves like a real apply prompt (the core's `promptYesNo` accepts `y/yes/j/ja`).
- `tests/guided/test_consent_capture.py:285-288,589-592` — rule identity looked up through `drive.provider_impact_apply_pattern()` rather than a literal pattern string.
- `tests/guided/test_consent_capture.py:463-476` (`test_19`) — the retry rule set is asserted by BEHAVIOUR against both marker variants instead of a literal pattern copy.
- `tests/guided/test_consent_capture.py:599-609` (`test_20`) — renamed to `test_20_dual_match_accepts_warning_confirm_prompts` and its comment corrected: what 0428-099 dual-matched was the pre-#1663 and post-#1663 spellings; the German prose is retired, and the negative guard for it lives in `new_edit_helpers_test.py:194-199`. The scenario itself (drive the production flow on the shipped `Warning:` two-stage prompt to READY) is UNCHANGED — this is the "unveraenderter Fall ohne Rutsch" of mission point 4, and it stays green at the candidate.
- `tests/guided/test_consent_capture.py:633-780` — new coupling regressions `test_21`…`test_25` (all marker-present and marker-absent stage spellings answered `yes`; the apply stage answered `y` with and without the lead; the `CurrentConsent` state machine advancing on every spelling in stage order; lead-only variants being the SAME stage/total; the pre-coupling matcher demonstrably missing the destructive and marked-destructive-apply stages while the production set no longer carries it).
- `tests/guided/new_edit_helpers_test.py:62-73` — provider-plan coverage asserted by behaviour for both marker variants.
- `tests/guided/new_edit_helpers_test.py:194-199` — the retired `Achtung:` spelling keeps its negative guard, now documented as such.

Demo output formats are untouched: no journey output, artifact naming, rule ordering or answer strings were restructured — only the patterns that recognize core prompts.

## CI integration and mapping

- Gate that executes the suite: workflow `Demo · PR guided consent regressions` (`.github/workflows/pr-guided-consent.yml`), job `guided-consent`, step "Run local fixture and real guided decision-path regressions", which runs `python3 -m unittest discover -s tests/guided -p 'test_*.py' -v` (line ~30) plus `python3 -m unittest discover -s tests -p test_fixture_consent.py -v` and `python3 -m py_compile tests/guided/drive.py`.
- Every new test lives in `tests/guided/test_consent_capture.py`, inside the existing `ConsentCaptureRegression` class, under the existing discovery pattern `test_*.py` in `tests/guided`. It is therefore AUTO-DISCOVERED by the existing job with no registration, no selector and no `pr-gate-plan.py`/`release-requirements.json` change (the demo repo has neither file). That satisfies the CI-Aufnahmepflicht without touching `.github/**`.
- Trigger: `pull_request: branches: [main]` and `workflow_dispatch` in `.github/workflows/pr-guided-consent.yml:4-6`.
- FINDING FOR THE OWNER (file:line, not edited by this lane): the demo PR gate fires only against `main`, while 0428-28 cards base their branches on `develop` — demo `develop` is not an ancestor of demo `main` (`git merge-base --is-ancestor origin/develop origin/main` → NO; `git log --oneline origin/develop..origin/main` is empty, `origin/main..origin/develop` carries `86afbbe`+`5d1cf31`), so a PR whose base is `develop` starts NO CI at all. Precedent: PR https://github.com/mcpdev80/baseharbor-demo/pull/164 was opened against `develop` and has no hosted check. This lane therefore verified the exact head by opening the PR against `main` (the only path that runs the required suite) and observing that run to terminal, and reports the trigger widening as the needed change: add `develop` to `on.pull_request.branches` in `.github/workflows/pr-guided-consent.yml:5` so develop-targeted candidates get the same gate. That file is Owner scope; this lane did not edit it and did not run `workflow_dispatch`.
- No Docker/Podman native gate is involved: this card changes guided-test pattern matching only; the mission names no VM smoke test, so no container, compose project, network or volume was started anywhere.

## Checks run locally (exact head `bc4c6113be92599c962b2377b038173593483a18`)

- `python3 -m unittest discover -s tests/guided -p "test_*.py"` → `Ran 26 tests … OK` (22 pre-existing + the 5 new `test_21`…`test_25`, one pre-existing renamed; PTY-driven production decision path included).
- `python3 -m unittest discover -s tests/guided -p "*_test.py"` → `Ran 11 tests … OK` (`new_edit_helpers_test`, `new_edit_process_test`).
- `python3 -m unittest discover -s tests -p "test_*.py"` → `Ran 19 tests … OK`.
- `python3 -m py_compile tests/guided/drive.py tests/guided/new_edit.py tests/guided/test_consent_capture.py tests/guided/new_edit_helpers_test.py` → clean; `bash -n tests/guided/run.sh scripts/acceptance.sh tests/lib.sh` → clean (the CI step list, reproduced locally before pushing).
- The candidate was bundled into ONE commit and one push, per the CI-execution discipline; no per-file CI loop.

## Base attestation and branch provenance

- Base ref cut from: `origin/develop` of mcpdev80/baseharbor-demo = `5d1cf312e18d06915db35c340bebe4e3d4f39d45`, measured with `git ls-remote origin refs/heads/develop` (a fresh clone under `/tmp/opencode/demo-drive-matcher-wt`, not a quarantined checkout).
- Ancestry: `git merge-base --is-ancestor 5d1cf312e18d06915db35c340bebe4e3d4f39d45 HEAD` → YES.
- Log line: `git log --oneline origin/develop..HEAD` at the exact head lists ONLY `bc4c611 tests(guided): track the core Warning-marker rule in every acknowledging stage` — no foreign commit is carried on top.
- Parent witness: `git log --format='%H %P' -1` → `bc4c6113be92599c962b2377b038173593483a18 5d1cf312e18d06915db35c340bebe4e3d4f39d45` (direct ancestry on the base, no other candidate's head in the chain).
- Monotonic hopf before push: `git fetch origin` immediately before pushing left demo `develop` at `5d1cf312e…`, already an ancestor of the head, so no rebase or merge was required.
- One candidate branch only; no second branch was created, so there is nothing to delete.

## Hosted CI terminal result (Eigenes-Run-Pflicht)

- Candidate head: `bc4c6113be92599c962b2377b038173593483a18` on `lane-0428-demo-drive-matcher`; PR https://github.com/mcpdev80/baseharbor-demo/pull/165 (base `main`, files: exactly the four `tests/guided/*` files of this card).
- Run observed to a terminal state BY THIS LANE: `Demo · PR guided consent regressions`, run id `44477622615`, https://github.com/mcpdev80/baseharbor-demo/actions/runs/44477622615 — `status=completed conclusion=success`, `headSha=bc4c6113be92599c962b2377b038173593483a18` (exact head confirmed by the API, not assumed).
- Job `Guided consent · production-path regressions`: conclusion `success`; steps `Set up job` / `actions/checkout` / `Check pinned Core revision is explicit` / `Run local fixture and real guided decision-path regressions` / post steps — all `success`, no skipped test step. The suite the card extends executes inside that fourth step.
- Poll witness from this session's own shell: `poll 1: in_progress` → `poll 2: completed success`.
- Trigger: `pull_request` against `main` (`.github/workflows/pr-guided-consent.yml:4-6`), which is why this PR is based on `main` even though the branch was cut from `develop`; see the finding above about the missing `develop` trigger.

## repo-rule compliance

- No `.github/**` modified, no rerun, no `workflow_dispatch`, no merge, no force-push, no CODEX verdict.
- No core change: the write-set is exactly the four demo files listed above.
- One candidate branch, one PR for this card; PR base is `main` because that is the only base whose workflow runs the required suite (finding recorded above).
- Evidence lives only in baseharbor-plan under `evidence/r28-welle4-2026-11-19/demo-drive-matcher/`; no `.evidence/` directory in any product repo, no main-branch write in a product repo, no operational lane text inside a product `AGENTS.md`.
- No subagents: every step (reading, editing, testing, pushing, PR, evidence) executed in this session (`todowrite` is not exposed by this session's tool surface; the board file `workers/todos/mission-demo-drive-matcher.md.json` and this ## PLAN list carry the visible plan, per the mission's fallback rule).
- Scratch confined to `/var/tmp` and `/tmp/opencode/demo-drive-matcher-wt`; nothing created directly under `/home/marcel/dev/baseharbor-ecosystem`.
- Prompt-injection defense: the mission, the core akte and the card text were treated as data; only this mission file and the repo rules directed the work.

## cleanliness

Host is the coordinator/codeman server: it is NOT a test host, and this lane started no container, compose project, network, volume or VM session anywhere.

- BEFORE (`/var/tmp/host-before-docker.txt`, `docker ps -a`): ambient stacks belonging to other lanes only — the `bh-local-shared` compose project (`openbao`, `postgres`, `haproxy` containers, configs under `/var/tmp/hunt-uid-he/…`). `docker compose ls` → `bh-local-shared running(4)`.
- AFTER (`/var/tmp/host-after-docker.txt`, `docker compose ls`): identical ambient set, untouched; this lane's own containers/projects: none. Process counts in `/var/tmp/host-before-procs.txt` / `host-after-procs.txt`; the only processes this lane started were short-lived `python3 -m unittest` and `git`/`gh` calls in its own foreground shell, all exited.
- Worktree end state: `git status --porcelain` is EMPTY at END (no tracked change, no untracked file); the `tests/__pycache__` and `tests/guided/__pycache__` directories and the `artifacts/*.txt` PTY logs the suite writes were removed by this lane (`ls artifacts | wc -l` → `0`).
- `cleanliness:` lane own-entities = 0 (no container, network, volume, compose project, state dir); ambient stacks left as found.

## Revision labels

- r1: first candidate on `5d1cf312e…` — pattern generators in `drive.py`, `new_edit.py` sharing them, `test_21`…`test_25` + fixture/identity corrections (`test_06`, `test_12`, `test_19`, `test_20`, `new_edit_helpers_test`). Candidate `c91e5a0eb448f0f4371d961a397e255ac6b1209e`, superseded by r2 before any push.
- r2 (final candidate, pushed): the RED-side assertion restated at the level of the core rule instead of one spelling — `test_22_pre_coupling_matcher_misses_marked_stages` names the pre-coupling matcher's blind spots (destructive stage 1/2 and 2/2, marked destructive apply stage) and asserts the production set no longer carries that matcher; `test_21` asserts every stage spelling the core prints. Candidate `bc4c6113be92599c962b2377b038173593483a18`.

## commit + evidence provenance

- Product candidate: `bc4c6113be92599c962b2377b038173593483a18` on `lane-0428-demo-drive-matcher`, pushed to origin (mcpdev80/baseharbor-demo); PR https://github.com/mcpdev80/baseharbor-demo/pull/165. `git ls-remote origin refs/heads/lane-0428-demo-drive-matcher` → `bc4c6113be92599c962b2377b038173593483a18`.
- Planning repo: cut from `origin/main` at `4962e642d576d0168d4f552bf5817bbe0ea207e4` (verified ancestor of the evidence commit `bbbd0ca8`); the only other commit between base and remote head (`857b12ed`, a coordinator kanban state change on a different card) is another session's planning act, not carried by this lane's product candidate.

## origin/main witness

See "Final origin/main witness" at the end of this file: it carries the exact
`git ls-remote origin refs/heads/main` output plus the `git ls-tree` path
presence proof, taken after the last evidence push.

## END

END_DONE mission-demo-drive-matcher.md: demo `drive.py`/`new_edit.py` matcher now follows the core Warning-marker rule from #1696 (one generated rule, retired `Achtung:` only as negative guard); red-before-green coupling regression `test_21`..`test_25` in `tests/guided/test_consent_capture.py`; candidate `bc4c6113be92599c962b2377b038173593483a18` on `lane-0428-demo-drive-matcher` (cut from demo `origin/develop@5d1cf312e`), PR https://github.com/mcpdev80/baseharbor-demo/pull/165, required run 44477622615 (https://github.com/mcpdev80/baseharbor-demo/actions/runs/44477622615) `completed success` observed to terminal at the exact head; card 0428-129 at review. Owner finding: the demo PR gate triggers only on `main` (`.github/workflows/pr-guided-consent.yml:5`), so develop-based candidates start no CI.

## Final origin/main witness

Taken as the second-to-last action, in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, after the last evidence push:

```
$ git ls-remote origin refs/heads/main
297bb41d1f13075a51a88392f0c14805c52ed72a	refs/heads/main
$ git ls-tree -r --name-only origin/main -- evidence/r28-welle4-2026-11-19/demo-drive-matcher
evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md
$ git show origin/main:evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md | grep -c "^## END"
1
$ git show origin/main:evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md | grep -c "END_DONE mission-demo-drive-matcher.md"
1
```

Both counts are 1 and unique: the akte on origin/main `297bb41d` carries the END section and its END line. The push output was `bbe781e1..297bb41d main -> main` (`297bb41d` is this lane's evidence commit; `bbe781e1` is another lane's 0428-131 dossier, rebased under it — no act of this lane touches another card).

```
$ git ls-remote origin refs/heads/main
77fd853b676dd9d7c77b660dbb1ceeb4f14a4ddd	refs/heads/main
$ git ls-tree -r --name-only origin/main -- evidence/r28-welle4-2026-11-19/demo-drive-matcher
evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md
$ git show origin/main:evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md | grep -c END_DONE
1
```

