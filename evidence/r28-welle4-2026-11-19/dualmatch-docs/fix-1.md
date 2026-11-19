# 0428-126 — Warning/Achtung dual-match: acknowledging CLI stages + EN normdoc alignment

- Mission: `/var/tmp/missions/mission-dualmatch.md`
- Card: `t-20261119-hunt-metrics-dualmatch-marker-docs` (0428-126, LOW/DOC), claim published in baseharbor-plan `a82cdc06ad1c2179ea6fe0c107edf14ddeb83f10`
- Source of findings: `evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md`, Befund 5 + Befund 4-sub (documentation drift part). Befund 4 itself is not card material here (already carded 105/112/073).
- Lane worktree: `/var/tmp/dualmatch-wt/wt`, branch `lane-0428-126-dualmatch-docs` (single candidate branch, no second branch created)
- Wrong-zone check: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the real planning repo, not `workers/baseharbor-plan`)

## PLAN

1. Claim card + ls-remote develop — DONE (claim commit `a82cdc06`, develop head at check-out `ec592fd3852328439ae9de8763c816ae9dd88dcc`)
2. Read hunt-metrics akte (Befund 5 + Befund 4-sub) and locate source/docs — DONE
3. Fix (a): Warning lead in every acknowledging CLI stage, semantics unchanged — DONE
4. Fix (b): EN docs aligned to the `attention: "Warning"` rename — DONE
5. Regression tests in `cmd/baha` (auto-discovered, CI-picked-up) — DONE
6. This akte with revision labels — this file
7. Monotonic hopf, push exact head, docs-check + affected checks terminal — IN PROGRESS
8. Evidence on origin/main, compose witness, END — PENDING

## Base attestation and provenance

- Cut base: `ec592fd3852328439ae9de8763c816ae9dd88dcc` — `git ls-remote origin refs/heads/develop` at lane start. Verified ancestor of the first commit at cut time: `git merge-base --is-ancestor ec592fd38… HEAD` → yes.
- Monotonic hopf immediately before push: develop had advanced to `deeeb64778b3f6109d3a8e49fd652d490901e89c`; branch rebased onto it (fast-forward chain, no second branch, no force). Witness: `git merge-base --is-ancestor deeeb64778b3f6109d3a8e49fd652d490901e89c HEAD` → YES; `git log --oneline origin/develop..HEAD` lists ONLY `8fe570fe7 feat(cli,docs): print Warning marker in every acknowledging stage; align EN docs with i18n rename (0428-126)` — no foreign commit carried on top.
- Candidate head (exact SHA for checks and PR): `864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c` (PR #1696; earlier same-content candidates `4a8c51e30`, `8fe570fe76521d84a661a25f800e1c390a0e95ab` on the same single branch `lane-0428-126-dualmatch-docs`, superseded by the monotonic hopf rebases, never a second branch)

## Revision r1 — Fix (a): marker in every acknowledging stage (befund-1.md Befund 5 sub-finding)

The akte (low): `readProviderImpactAcknowledgements` selected a catalog label only for `Destructive` or `ConfirmationsRequired == 2`; the single-confirmation non-destructive stage printed a hardcoded `Confirm the displayed provider changes` with no marker, and the two apply-stage labels in `readProviderApplyAcknowledgement` (`Apply these changes?` / `…permanently delete the listed data?`) were likewise marker-less. A demo rule that gates on the marker string never sees those stages (akte witness `TestHunt918DemoMatcherVocabularyCoversBothMarkers`).

Change (presentation only; the gate keys on `plan.Attention != ""` — presence, not value — so no consent semantics move):

- `cmd/baha/provider_change_confirmation.go`: new `providerImpactAttentionLead(plan)` renders `Warning: ` when and only when the plan carries an attention marker; it prefixes the single-confirmation stage label and both apply-stage labels.
- Scope-derived presentation plans now propagate `Scope.Attention` at every direct call site (the scope constructors always set `Attention` together with any raised confirmation requirement, `internal/application/provider_change_scope.go:53-61`, so a stage that collects a consequence acknowledgement always prints the marker):
  - `cmd/baha/application_destroy_authorization.go` (readProviderApplyAcknowledgement)
  - `cmd/baha/application_restore_authorization.go`
  - `cmd/baha/application_stop_impact.go`
  - `cmd/baha/control_plane_stop_impact.go`
  - `cmd/baha/node_disconnect_client.go`
  - `cmd/baha/provider_external_removal.go`
  - `cmd/baha/runtime_destroy_impact.go`
  - `cmd/baha/management_remote_installation_destroy.go`
  - `cmd/baha/target_definition_change.go`
- Paths that pass a full plan (`app_edit_apply.go` wizard impact, `acknowledgeProviderImpact` on apply/up) carry `Attention` from plan construction and needed no call-site change; the lead keys on the value already present.
- NOT touched (documented as correct, mission point 3): the machine surface (`"attention":"Warning"`, schemas pinned `const`), MCP/HTTP (structured field only, no prose marker), the catalog labels, and the `candidate_confirmation_required` plain yes/no in `management_remote_apply_cli.go:212` — that prompt approves a source-candidate digest, not an impact plan (no `ProviderImpactPlan` exists at that point), and it is not one of the `readProvider*Acknowledgement*` stages the akte names.

Demo-repo note (no change, other repo, out of write-set): `baseharbor-demo` `tests/guided/drive.py:507` and `new_edit.py:203` carry the pre-fix alternation `Confirm the displayed provider changes|…`; after this change the stage prints `Warning: Confirm the displayed provider changes`, which matches neither branch. The rules are `optional=True` (the stage only appears for single-confirmation scopes), but a lane that exercises exactly that stage would stall on the unmatched prompt. Recommend a follow-up line in the demo repo adding the pattern.

New regression tests (both PASS at `8fe570fe7`):

- `TestProviderImpactMarkerPrintedOnEveryAcknowledgingStage` (`cmd/baha/provider_change_confirmation_test.go`): every printed line of each acknowledging stage (1-stage, 2-stage, destructive) leads with `Warning: `; apply-stage labels carry the lead; a plan without attention keeps the plain label (negative assertion that the lead never appears without a marker).
- `TestProviderImpactAcknowledgementStagesAllCarryAttention`: enumerates the scope-derived presentation sites and asserts each carries the marker end-to-end through `readProviderImpactAcknowledgements`.

## Revision r1 — Fix (b): EN normdoc behind the i18n rename (befund-1.md Befund 4-sub)

The rename commit `9a37b4bc6` (#1663) updated contracts and schemas but no `docs/**` file; EN pages still named the marker **Achtung** while the shipped value is `Warning` (`internal/application/provider_change_plan.go:93,98`, `contracts/provider-impact/v1/*.schema.json` `"const": "Warning"`). Per `docs/STYLE_GUIDE.md:77` EN pages are normative for behavior. Aligned pages (marker-name mentions only, no other content touched):

- `docs/spec/capability-first-v0425.md` (3 spots), `docs/spec/runtime-explorer-v1.md` (1)
- `docs/reference/backup-and-restore.md` (1 — this one printed an `Achtung:` sentence as if it were real CLI output)
- `docs/how-to/machine-operations.md` (1), `docs/how-to/external-providers.md` (1)
- `docs/cli/applications.md` (1), `docs/cli/targets.md` (2)
- `docs/releases/v0.4.25.md` (1), `docs/releases/v0.4.25.preparation.md` (1)
- `docs/internal/v0.4.25-provider-mutation-coverage.md` (3)

Residual audit: `grep -rn "Achtung" docs/ --include="*.md" | grep -v "^docs/de/"` → no matches. `docs/de/**` occurrences are legitimate German prose and were NOT changed (they describe the German label in German pages; DE translation-integrity check passes: 168 paired pages).

## Checks run locally (exact head 864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c)

Final candidate is `864fdcd3a…` (monotonic hopf: rebased onto develop `21161b101f66a47fb1a253ae17e87fe82567ba4d` immediately before push; `git merge-base --is-ancestor 21161b101 HEAD` → yes; `git log --oneline origin/develop..HEAD` → exactly the one commit). Earlier candidate `8fe570fe7` was the same content on develop `deeeb6477`.

- `go build ./cmd/baha` + `go vet ./cmd/baha` PASS; `gofmt -l cmd/baha` empty; `bash scripts/documentation-audit.sh` PASS; `check_de_translation_integrity.py` PASS; `source-readability-audit.sh` PASS.
- Consent/regression families incl. the two new tests, plus the three lifecycle tests that hung under the parallel run (`TestRestoreRefuses…`, `TestCorelessApplicationStopConsent…`, `TestManagedCollectorAndRegisteredReceiverReplacement…`): `ok cmd/baha` in isolation. `go test ./internal/application` ok.
- Full-package `go test ./cmd/baha -count=1` does not converge on this shared host: every run hit the 10m package timeout on a DIFFERENT docker-backed lifecycle test, and a control worktree at untouched base `ec592fd38` fails identically (`/var/tmp/dualmatch-base-full.log` — `--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, then package timeout). These tests start real compose stacks and need the clean isolated Docker daemon hosted CI provides; this coordinator host is not a test host and none was started here. Hosted CI at the exact head is the terminal authority (watch: `/var/tmp/dualmatch-ci-watch.log`).

## CI integration and mapping

- The two new tests are ordinary Go unit tests in package `github.com/mcpdev80/baseharbor/cmd/baha`, auto-discovered by `go test ./cmd/baha`.
- Gate that executes them: `cli-package-tests` (`go test ./cmd/baha -count=1`, declared in `scripts/pr-gate-plan.py:90`) selected because the PR touches `cmd/baha/*.go`; the documentation changes select `documentation-audit`, `mkdocs-en-strict`, `mkdocs-de-strict`, `pages-candidate-build` (`scripts/pr-gate-plan.py` DOC_CHECKS); develop integration runs the full `go test ./cmd/baha` in `CI · Source & Quality` (`.github/workflows/ci.yml:125`).
- Selection proof: `python3 scripts/pr-gate-plan.py --diff <changes.json>` with `GITHUB_BASE_REF=develop` on this lane's real diff returned ids `cli-build, cli-gofmt, cli-package-tests, cli-vet, documentation-audit, mkdocs-de-strict, mkdocs-en-strict, pages-candidate-build, source-contracts` — positive selection for exactly the changed paths. An unrelated-path diff is covered by the existing gate-plan tests in CI; no new CI framework and no `.github/**` change was needed or made.
- No Docker/Podman native gate is required: the change is CLI presentation + markdown docs; no runtime path is touched.

## repo-rule compliance

- No `.github/**` modified, no rerun, no workflow_dispatch, no merge, no force-push.
- One candidate branch (`lane-0428-126-dualmatch-docs`), no second branch.
- No subagents: every step in this session. `todowrite` is not exposed by this session's tool surface (verified: not in the Code Mode catalog, never hunted via `execute` per mission); the board file `workers/todos/mission-dualmatch.md.json` and this ## PLAN list carry the visible plan.
- Evidence lives only in baseharbor-plan (`evidence/r28-welle4-2026-11-19/dualmatch-docs/`); no `.evidence/` in any product repo, no main-branch write in a product repo.
- Scratch confined to `/var/tmp/dualmatch-*`; nothing created under `/home/marcel/dev/baseharbor-ecosystem` itself.

## cleanliness

- This lane started no container, compose project, network or volume on any host (coordinator host is not a test host; the mission names no VM). `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` was executed under `go test` at base and candidate and aborts before any stack creation on this host (that is the environment failure above).
- Worktree end state: `git status --porcelain` shows only scratch dirs created by the `internal/application` test suite (`prune-owner/`, `prune-sameid/`, `trace-*`), removed at END; 0 tracked changes after commit.

## Revision labels

- r1: initial implementation — both fixes (marker lead + attention propagation at 9 call sites; 15 EN marker mentions aligned), two regression tests. Candidate `4a8c51e30` (on develop `ec592fd38`).
- r2: monotonic hopf #1 — rebase onto develop `deeeb6477`; content identical; targeted re-verification. Candidate `8fe570fe7`.
- r3: monotonic hopf #2 directly before push — rebase onto develop `21161b101`; content identical; re-verified build/vet/gofmt/documentation-audit and the affected `cmd/baha`/`internal/application` test families at the exact head. Final candidate `864fdcd3a`, pushed (branch `lane-0428-126-dualmatch-docs`), PR https://github.com/mcpdev80/baseharbor/pull/1696 against develop.

## commit + evidence provenance

- Final candidate `864fdcd3a` has exactly one parent, `21161b101…` (the develop head fetched immediately before push — direct ancestry, `git log --format='%H %P'`): `864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c 21161b101f66a47fb1a253ae17e87fe82567ba4d`. Provenance chain: original cut `ec592fd38` (develop at lane start, verified ancestor of the first commit `4a8c51e30`); r2 rebase onto `deeeb6477`; r3 rebase onto `21161b101`; no other commits in `git log --oneline origin/develop..HEAD`.

- Planning repo: cut from `origin/main` at claim time (`a82cdc06` includes the claim); evidence commits listed via ls-remote below.
- `git ls-remote origin refs/heads/main` in baseharbor-plan, pasted as second-to-last action: (see END section)
- Product candidate: `864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c` on `lane-0428-126-dualmatch-docs`, pushed to `origin` (mcpdev80/baseharbor); PR https://github.com/mcpdev80/baseharbor/pull/1696 against develop. Card state at review; merge is the Codex acceptance step, not this lane's.

## Hosted CI terminal result (exact head 864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c)

PR #1696, workflow run 44471319498 (`CI · Source & Quality`), observed to terminal by this lane. All executed checks pass; unselected matrix jobs are `skipping` by the normal path-selection rules (release/HA/draft chains are not selected by these paths). Key results:

- Workflow policy pass · PR · Native gate plan pass · PR · Trusted Plan pass · PR · Source format pass · PR Selected Checks pass
- PR · Validation · documentation-audit pass (the docs fix gate)
- PR · Validation · mkdocs-en-strict pass · mkdocs-de-strict pass · pages-candidate-build pass · go-build / go-vet / cli-gofmt / Focused Python pass
- PR · Go unit · packages / owner / cli-0 / cli-1 / cli-2 / cli-3 all pass (the `cmd/baha` package, i.e. the two new regression tests, executes in these shards; cli-family selection confirmed by `PR · Native gate plan`)
- PR · Native Keycloak/Core · docker pass · podman pass · PR · Native · native/podman/installation-destroy pass

## END

END_DONE mission-dualmatch.md: Warning/Achtung dual-match complete — every acknowledging CLI stage prints the `Warning:` lead (semantics unchanged) and EN normdocs follow the i18n rename; candidate `864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c`, branch `lane-0428-126-dualmatch-docs`, PR https://github.com/mcpdev80/baseharbor/pull/1696 (run 44471319498: all selected checks pass at the exact head, docs-audit + mkdocs-en/de-strict + Go unit cli shards included); card t-20261119-hunt-metrics-dualmatch-marker-docs at review.

Follow-up finding (not in this write-set, baseharbor-demo repo): `tests/guided/drive.py:507`/`new_edit.py:203` match the old marker-less prompt text `Confirm the displayed provider changes`; after this change the stage prints `Warning: Confirm the displayed provider changes`. Rules are optional=True, but the demo matcher should add the new pattern in a demo-repo card.
