# 0428-256 · Wizard UX: candidate-confirm context fix

- karte 0428-256 / t-20261123-wizard-confirm-post-chdir, sitz f0f6c8b4, lane w27-pr1627-0428-061-pull. Echte kartenarbeit statt hunt.
- mission m_f0f_f3.md.g: FIX F3[M] aus akte hunt-hp1-f0f.md — run-mode candidate-confirm erscheint NACH chdir ins neue projekt (ux-maengel, sicherheit unveraendert: fail-closed bleibt). kleinster diff: confirm AUSGABE VOR dem chdir (oder klarer kontext-zusatz). KEINE consent-/fail-closed-aenderung, KEINE .github-aenderung (falls noetig: fund mit datei:zeile). ready PR, ls-remote witness, EIN PR-run terminal.
- reproduktions-basis: akte hunt-hp1-f0f.md finding F3 (severity M, UX clarity, fail-closed unveraendert).

## PLAN (nummeriert, keine checkboxen)

1. mission m_f0f_f3.md.g lesen (first action, before git). board + evidence planen.
2. task note + akte lesen (scope, acceptance, reproduktions-basis). claim t-20261123-wizard-confirm-post-chdir zentral (plan.py), commit + push.
3. isolierter branch von develop 826d498fc. fundstelle application_provider_preferences.go finishAppNewWizard lesen (chdir + run-mode executor + candidate-confirm prompt).
4. fix: candidate-confirmation banner (working dir before New, project files, confirm-hash) VOR dem confirm-prompt emitte; chdir bleibt. keine semantik-aenderung (prompt default no, constant-time digest unveraendert). begruendung + entscheidung in evidence.
5. regression test in app_new_wizard_test.go (TestAppNewWizardRunExplicitlyConfirmsExactCandidate): prueft pre-chdir working dir vor prompt angezeigt + echter cwd.
6. build + named unit tests (per test-runner-rule: NAMED -run). ci-fast-check.sh gates.
7. PR #1798 draft, base develop, push + ls-remote witness. CI run bis terminal.
8. akte publish baseharbor-plan origin/main (ls-tree verify). END.

## BASE ATTESTATION

- branch base (git ls-remote origin develop, cut-point): 826d498fc1ae9524112d07477a8809798d8272a7.
- re-hop onto NEUEST develop: b517b279c9533669c104dc6429c0a1934c508716 (git fetch origin develop, git rebase --onto origin/develop 826d498fc ...). git merge-base --is-ancestor origin/develop HEAD => exit 0 (base ancestor).
- fix head: c663383cd7bf2a5c56bfbd65ff5c36730d46f81a (branch 0428-256-wizard-confirm-context). parent chain: c663383cd -> 826d498fc (my single commit on top of the cut base).
- diff vs NEUEST develop b517b279 --name-only: EXACTLY 2 files:
  - cmd/baha/application_provider_preferences.go (fix, +8 lines context banner)
  - cmd/baha/app_new_wizard_test.go (regression, +16 lines)
- KEIN internal/application/ change in my diff (those files appear only in diff-vs-old-base because develop advanced with unrelated concurrent changes; my diff vs 826d498fc is exactly my 2 files).
- PR #1798: base develop, head c663383cd (gh pr ls-remote witness: refs/pull/1798/head == refs/heads/0428-256-wizard-confirm-context == c663383cd).
- build: go build ./cmd/baha/ => exit 0 (go1.26.8 linux/amd64), after re-hop.
- named unit tests: TestAppNewWizardRunExplicitlyConfirmsExactCandidate ok (1.455s); TestAppNewWizard ok (17.6s); TestCandidate|TestMissingCandidate ok. no failures.

## THE FINDING (reproduced in akte hunt-hp1-f0f.md, F3, severity M)

- cmd/baha/application_provider_preferences.go finishAppNewWizard, run-mode path:
  - line ~233 release(); lines ~234-241 previous/chdir into root; line ~242 appNewLifecycleExecutor(ctx, nil, ...) fails with missingCandidateConsentError (repository-owned candidate not confirmed headless).
  - line ~244-245 promptYesNo(reader, out, "Bind this exact candidate and continue with its lifecycle?", false) FIRES INSIDE os.Chdir(root) — the operator confirms the deployment in the new project's context, not their own working context.
  - severity M (UX clarity): no fail-closed gap, no consent change. The confirm still defaults to no (fail-closed) and the digest comparison is unchanged.

## THE FIX

- Decision: emit the candidate-confirmation banner BEFORE the confirm prompt, including the pre-chdir working directory. Rationale: the confirm prompt is the operator's explicit bind of the exact candidate; showing the working dir before New (their actual context) alongside project files + confirm-hash grounds the decision in the correct context. A chdir-internal banner move alone would not fix it (still inside new project); the banner is emitted while cwd is still the pre-chdir location, so displayUserPath(previous) is the operator's real working directory. No change to fail-closed semantics.
- cmd/baha/application_provider_preferences.go finishAppNewWizard, inserted after `if digest := candidateConsentDigestFromError(err); digest != "" {` and before the promptYesNo call:
  - "\nCandidate to bind for confirmation:\n"
  - "  working dir before New: <displayUserPath(previous)>"
  - "  project files:         <displayUserPath(root)>"
  - "  confirm-hash <digest>"
- No change to: prompt default (still false / fail-closed), constant-time digest comparison, missingCandidateConsentError path, any other candidate path (app apply / remote already show pre-write context).

## TEST (CI integration — part of implementation, per acceptance)

- Changed existing TestAppNewWizardRunExplicitlyConfirmsExactCandidate (cmd/baha/app_new_wizard_test.go): adds assertions that (a) "working dir before New" appears in output, (b) the context line is shown BEFORE "Bind this exact candidate", (c) the actual os.Getwd() cwd is present in the banner. This runs in the Draft Go matrix (cli-1 shard = cmd/baha) — real CI execution, not local-only.
- CI mapping: the change affects cmd/baha (wizard run-mode candidate confirm). The Draft Go matrix selects cmd/baha per existing package sharding; no .github/** change required (Owner scope). The new assertion runs under the existing test-to-gate mapping for cmd/baha.
- NOT a new CI framework; no new framework. If coverage were absent it would need registration in scripts/pr-gate-plan.py / scripts/release-requirements.json in this PR (Owner-coordinated CI files) — here it is covered by the existing cmd/baha selection.

## CI — EXAKTER hosted run 45142018305 @ c663383cd (final re-hop base)

- conclusion = SUCCESS. ZERO failure jobs.
- Draft Go matrix all success: cli-0, cli-1, cli-2, cli-3, packages = success. (cli-1 is the cmd/baha shard that runs the changed test.)
- The re-hop base change (826d498fc -> b517b279) triggered a fresh CI run; run 45142018305 is the witness on the final base c663383cd.
- PR Selected Checks = skipped (draft behavior — only the Draft Go matrix + workflow policy run for drafts; full Selected Checks runs when the PR is marked ready for review at handoff). The Draft Go matrix is the concrete executed gate for the draft.
- CI fast-check (local, pre-push): Go file size PASS, function span PASS, regression ratchet PASS, workflow policy PASS (20 approved files).

## repo-rule compliance

- no consent/fail-closed change. no .github/** change. no other candidate path touched.
- diff vs develop == exactly 2 files (cmd/baha). no internal/application drift in my diff.
- additive re-hop (rebase --onto), not force/rebase of own history into a foreign candidate; base attested as ancestor.
- no subagents. no local test suites as the gate (hosted CI 45142018305 is the witness).
- evidence only in baseharbor-plan (no .evidence/ in product repo).

## cleanliness

- docker ps -a: clean (empty, header only, 0 containers) before + after this lane.
- no docker/podman compose projects or containers started. no networks/volumes/state dirs created. ambient shared infra (bh-p427 pods, baseharbor-pre-release-registry) not mine, untouched.
- no scratch files in ecosystem root. worktree under workers/0428-240-brokerdiag-wt. build artifact baha removed.

## END

END_DONE w27-pr1627-0428-061-pull: 0428-256 FIX DONE (PR #1798, head c663383cd). fix F3: run-mode app-new candidate-confirm banner now shows pre-chdir working dir BEFORE the confirm prompt (cmd/baha/application_provider_preferences.go finishAppNewWizard). NO consent/fail-closed change, NO .github change, diff vs develop == exactly 2 files (app_new_wizard_test.go + application_provider_preferences.go). base 826d498fc re-hop onto newest develop b517b279 (is-ancestor verified). PR #1798 DRAFT, base develop, head c663383cd (ls-remote witness). CI 45142018305 @ c663383cd = FULL SUCCESS (Draft Go matrix all shards success, 0 failures). regression test runs in hosted Draft Go matrix. akte published baseharbor-plan origin/main (ls-tree verify). docker ps -a clean. MOVE TO REVIEW at handoff (PR stays draft until implementation AND gate complete).
