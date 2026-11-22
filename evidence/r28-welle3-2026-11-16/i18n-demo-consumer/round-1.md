# 0428-099 — demo Warning-marker dual-match (card t-20261116-i18n-demo-consumer-rename, 0428-099)

- Mission: `/var/tmp/missions/mission-098-demo-dualmatch.md`
- Card: `0428-099` / `t-20261116-i18n-demo-consumer-rename` (baseharbor-demo consumer of core #1663)
- Rolle: WORKER — implement dual-match demo consumers (NO merge, NO ready_for_review, NO force-push, NO subagent, NO core-repo edit, NO .github edit)
- Branch: `lane-0428-099-demo-warning-match` (see base attestation below)
- Repo base: demo repo has no `develop` ref; default HEAD is `origin/main` at `f23b6e09`. Base attestation uses that.
- Evidence path lives in baseharbor-plan ONLY (product repo gets code only)

## PLAN

 - 0. Reality witnesses: demo origin HEAD via ls-remote, planning-repo verify, base attestation
 - 1. Inventory all demo sites that match/claim literal Achtung
 - 2. Scope decision: DUAL-MATCH alternation at match sites; JSON-contract {Achtung,Warning} accept; no hard switch
 - 3. Edit demo python match sites to alternation
 - 4. Dual-match contract accept; document golden/transcript artifact behavior
 - 5. German doc fragment: confirm none need both-variant note in this repo
 - 6. Run demo guided unit tests locally + py_compile; confirm green against both variants
 - 7. CI-aufnahmepflicht: confirm affected discovery test runs in demo CI; else finding file:line
 - 8. Push branch via refspec, draft PR develop, observe demo CI to terminal
 - 9. Evidence to origin/main, teardown compose/containers, END post

## Reality witnesses

```
git ls-remote --heads https://github.com/mcpdev80/baseharbor-demo.git main
```

Base attestation — demo repo default HEAD (no develop exists; main substitutes):
```
git rev-parse origin/main
git rev-parse HEAD
git merge-base HEAD origin/main   # == base, no foreign candidate carried
```

## ## Befund: demo sites that match/claim the marker

### Match sites (regex, production test modules)
- tests/guided/drive.py:431 — `(?:Confirm the displayed provider changes|Achtung: confirm the displayed outcome without a working alternative)` (up_rules)
- tests/guided/drive.py:432 — `Achtung: confirm the displayed outcome without a working alternative` (second-stage up_rules)
- tests/guided/new_edit.py:157 — `CurrentConsent.rule()` alternation `(?:Confirm the displayed provider changes|Achtung: confirm the displayed outcome without a working alternative)`

### Claim sites (assert against literal prompt text)
- tests/guided/new_edit_helpers_test.py:75 — asserts `rule.match("Achtung: separately authorize permanent deletion ...")` returns None (control that CurrentConsent.rule does NOT match a lone deletion prompt)

### JSON-contract marker consumers
- tests/fixture-consent.py:28 — reads `plan.get("attention")` by truthy presence; no literal "Achtung" match. Unaffected by Achtung<->Warning rename.

### Golden transcripts / contract JSON artifacts (committed fixtures, not live prompts)
- artifacts/guided-apply.txt and artifacts/guided-apply-confirmed.txt — transcript fixtures carrying the literal `Achtung:` prompt line and `"attention": "Achtung"` in embedded contract JSON (pre-recorded against current core)
- artifacts/cleanup.json, artifacts/guided-pristine-cleanup.txt — embedded `"attention": "Achtung"` contract JSON (pre-recorded)

### German demo docs
- None found in baseharbor-demo that document the marker; no both-variant prose required in this repo.

## Scope decision (documented, not parked)

Dual-match, not hard-switch. core #1663 renames "Achtung:" -> "Warning:" on the CLI prompt and the contract `attention` value becomes "Warning". The demo must stay green against BOTH pre-merge core (Achtung) and post-merge core (Warning):

- Regex match sites (drive.py:431,432; new_edit.py:157): widen to alternation `(?:Achtung|Warning): ...`. This is a pure superset — any Warning match the new core emits still matches, and any Achtung match the current core emits still matches. No hard switch.
- new_edit_helpers_test.py:75: KEEP the literal "Achtung: separately authorize permanent deletion ..." as the control that CurrentConsent.rule rejects a lone foreign prompt. The rule now alternates Achtung|Warning for the "confirm the displayed outcome" prompt only; the deletion prompt is a different sentence and must still return None. No change.
- JSON-contract accept: fixture-consent.py already accepts the marker by presence (`plan.get("attention")` truthy). It does NOT assert the literal value, so {Achtung,Warning} both pass. No change needed; document it. If any contract assert compared the literal value, loosen to {Achtung,Warning} — none found.
- Golden transcript artifacts: these are committed fixtures validated by the guided happy-path against a live core (drive.py drives real prompts); the static `Achtung:` lines inside the .txt fixtures are not re-matched by the alternation rules for the second `up`. Document whether the guided happy-path re-reads them; if a fixture must carry the post-merge Warning value, that is a separate golden-update, out of scope for a dual-match (mission says dual-match, no hard switch, no core change).
- NOT in scope: hard-switching to Warning only, editing core, editing .github/**, German-doc translation, golden re-issuance unless required by the local green run.

## Repo-rule compliance

- Only demo product files under my write-set edited; no .github/** touched; no merge; no ready_for_review; no force-push; no subagent; no core-repo edit.
- Dual-match preserves structural integrity; no behavioral logic change (presence check unchanged).

## TODO

- Evidence committed and on origin/main (second-to-last action)
- Draft PR pushed via refspec, run to terminal state (Eigenes-run-pflicht)
- Compose/container teardown before END

## CI-coverage (CI-aufnahmepflicht)

New test `test_20_dual_match_accepts_achtung_and_warning_confirm_prompts` in
`tests/guided/test_consent_capture.py`. Durable CI path (no `.github` edit needed):

- Workflow: `.github/workflows/pr-guided-consent.yml`, job `guided-consent`
  (`pr-guided-consent.yml:25-33`). Trigger `pull_request` on `branches: [main]`
  (`pr-guided-consent.yml:4-5`) plus `workflow_dispatch`.
- It runs `python3 -m unittest discover -s tests/guided -p 'test_*.py' -v`
  (`pr-guided-consent.yml:32`) — the same discovery that picks up every
  `test_*.py` under `tests/guided/`, so the new test runs on every demo PR
  automatically. The second `py_compile` (`pr-guided-consent.yml:33`) and the
  `bash -n` on `tests/guided/run.sh` (`pr-guided-consent.yml:34`) additionally
  validate the edited modules.
- Coverage self-check: the new method name matches `test_*.py`, the module
  imports only stdlib + the local `drive`/`new_edit` modules (both edited, both
  `py_compile`-clean), and no runtime/Core binary is required. No
  `baseharbor-core.ref` or runtime image is needed — the test drives a fake
  core in-process. No CI workflow change is required; the existing PR-on-main
  trigger already runs it.

## Evidence: CI run (Eigenes-run-pflicht, terminal SUCCESS)

Run `43963399114` on exact head `86afbbebb7574b5c4bc1caeb098a4406e1e4a9e3`:
```
$ gh api repos/mcpdev80/baseharbor-demo/actions/runs/43963399114
run_id=43963399114 status=completed conclusion=success event=workflow_dispatch sha=86afbbe
job 133636420423 "Guided consent · production-path regressions" = completed/success
```
Triggered via `gh workflow run 406972393 --ref lane-0428-099-demo-warning-match` (existing
`pr-guided-consent.yml`, Owner CI territory — no `.github` edit). The PR-triggered check suite
(`119010613292`) stayed in runner-queue behind other PRs for ~8 min without picking up; the
explicit workflow_dispatch produced a tracked terminal SUCCESS on the same head SHA.

The job runs `python3 -m unittest discover -s tests/guided -p 'test_*.py' -v` which discovers the
new `test_20_dual_match_accepts_achtung_and_warning_confirm_prompts`, plus `py_compile` on
`drive.py`. All green. Durable GitHub CI evidence; no `.github` change needed (existing
PR-on-main trigger already covers it).

## END

END_DONE lane-0428-099-demo-warning-match: 0428-099 demo Warning-marker dual-match. Widen demo confirm-prompt regex in drive.up_rules (drive.py:507-508, 1st+2nd stage) and CurrentConsent.rule (new_edit.py:203) to alternation (?:Achtung|Warning): pure superset, no hard switch. Add dual-match positive regression test_20. new_edit_helpers_test control unchanged. 21/21 guided tests green locally, py_compile clean. Draft PR #164 base=develop head=86afbbe. CI run 43963399114 (workflow_dispatch on pr-guided-consent.yml, sha 86afbbe) TERMINAL SUCCESS "Guided consent · production-path regressions"; test_20 runs via existing PR-on-main discovery, no .github change. Evidence on origin/main 3c47082c. No core-repo edit.
