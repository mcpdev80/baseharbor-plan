# H-V46 Verdict-Queue Desk — Hunt Akte

LANE: 0428-221-huntq
ROLLE: Worker (BUG-HUNT, reine Befundung, KEINE Produkt-aenderung, KEIN commit an baseharbor)
DATUM: 2026-11-21

## Remote attestation (base ref)

- develop remote SHA (via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`): `97b2ba5543f07b820b5c18a688058fd932c4516f`
- This SHA is the ancestry baseline for every ancestor test below.
- Planning repo remote (verified with `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`): `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. The `workers/baseharbor-plan` dir is the quarantined stale checkout and was NOT used.

## PLAN

- Schritt 1: Remote-Wahrheit messen — `gh pr list` (alle offenen PRs) und `git ls-remote` develop-Head. git remote auf github.com/mcpdev80 verifiziert. 24 offene PRs.
- Schritt 2: Pro PR — ancestry (merge-base develop..head via deep fetch), `gh pr checks` / rollup von 'PR Selected Checks' und 'Trusted Plan'.
- Schritt 3: Verdict-Bestand — neueste reviewer/act-Datei je PR aus baseharbor-plan origin/main gelesen, Kandidaten-SHA extrahiert, Objekt-Vorhanden + Ancestor-von-head geprueft.
- Schritt 4: Klassifizierung je PR in A/B/C/D.
- Schritt 5: Delta-Dateien (`diff develop..head`) + Tabu-Touch-Check je PR.
- Schritt 6: Diese Akte geschrieben, cleanliness, repo-rule compliance.

## Full sweep: all 24 open PRs

| PR | card | draft | mergeable | mergeStateStatus | ancestry (develop ancestor of head) | PR Selected Checks | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1747 | 0428-060 | false | MERGEABLE | BEHIND | NO (not fresh) | — | D (behind develop) |
| 1746 | — | false | MERGEABLE | CLEAN | YES (fresh) | COMPLETED/SUCCESS | A (ready, no verdict) |
| 1742 | — | false | MERGEABLE | CLEAN | YES (fresh) | COMPLETED/SUCCESS | A (ready, no verdict) |
| 1741 | — | false | MERGEABLE | UNSTABLE | NO (not fresh) | — | D (needs rebase) |
| 1740 | — | false | MERGEABLE | UNSTABLE | NO (not fresh) | — | D (needs rebase) |
| 1738 | — | false | MERGEABLE | UNSTABLE | NO (not fresh) | — | D (needs rebase) |
| 1737 | — | false | MERGEABLE | UNSTABLE | NO (not fresh) | — | D (needs rebase) |
| 1736 | — | true | MERGEABLE | BEHIND | NO (not fresh) | — | D (draft + behind) |
| 1725 | — | false | MERGEABLE | BEHIND | NO (not fresh) | — | D (behind) |
| 1723 | — | false | MERGEABLE | BEHIND | NO (not fresh) | — | D (behind) |
| 1714 | 0428-183 | false | MERGEABLE | BEHIND | NO (not fresh) | — | D (behind) |
| 1704 | 0428-073 | false | MERGEABLE | UNSTABLE | YES (fast-forward of develop) | COMPLETED/SUCCESS | A-ish: fresh but not mergeable yet (UNSTABLE, hopf on develop) |
| 1702 | 0428-142 | false | CONFLICTING | DIRTY | NO | — | D (conflicting) |
| 1650 | 0428-078 | false | CONFLICTING | DIRTY | NO | — | D (conflicting) |
| 1645 | 0428-091 | false | MERGEABLE | BEHIND | NO | — | D (behind) |
| 1627 | 0428-055 | true | MERGEABLE | BEHIND | NO | — | D (draft + behind) |
| 1625 | 0428-065 | true | CONFLICTING | DIRTY | NO | — | D (draft + conflicting) |
| 1623 | 0428-063 | true | MERGEABLE | BEHIND | NO | — | D (draft + behind) |
| 1620 | 0428-067 | false | CONFLICTING | DIRTY | NO | — | D (conflicting) |
| 1614 | 0428-062 | false | MERGEABLE | DIRTY | NO | — | D (dirty) |
| 1597 | 0428-076 | false | MERGEABLE | CLEAN | YES (fast-forward) | COMPLETED/SUCCESS | A (ready, verdict STALE — see below) |
| 1596 | 0428-056 | false | MERGEABLE | BEHIND | NO | — | D (behind) |
| 1588 | — | false | MERGEABLE | BEHIND | NO | — | D (behind) |
| 1585 | — | false | MERGEABLE | BEHIND | NO | — | D (behind) |

Ancestry method: deep `git clone --filter=blob:none` of the real github remote, then `git merge-base --is-ancestor 97b2ba55… <pull/$pr/head>` — all four ANCESTOR-OK PRs are fast-forwards of develop (merge-base == develop SHA).

## Class A — READY WITHOUT A VERDICT AT EXACT HEAD (the window's bottleneck)

These are FRISCH (develop is an ancestor of head), PR Selected Checks = pass, draft = false, and NO CODEX verdict exists at their current head. The abnahme-sitz should pick these up immediately.

### PR 1597 — card 0428-076 (Perses database dashboards) — HEAD 12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7
- Fresh: fast-forward of develop, mergeStateStatus = CLEAN.
- PR Selected Checks: COMPLETED/SUCCESS (run 44900492916, job 136836366758); Trusted Plan: pass.
- 1 own commit (`hop(0428-076): rebase perses dashboard work onto develop`).
- Delta (develop..head, 13 files): `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `go.mod`, `go.sum`, `internal/metrics/perses_dashboards.go`, `internal/metrics/perses_dashboards_helpers.go`, `internal/metrics/perses_dashboards_promql_test.go`, `internal/metrics/perses_dashboards_test.go`, 5 `internal/metrics/testdata/perses-dashboards/*.json`.
- Tabu touch: none.
- Verdict inventory: `evidence/r28-welle4-2026-11-19/codex-review-wave/1597-0428-076-independent-review.md` — an independent read-only review exists, but it is for the OLD head `540ed13cec363a231241a17baa68c8d32ebdae63` (an earlier draft that was DIRTY against a stale base `40944485…`).
  - Verdict-sha `540ed13c` object exists (not object-missing), but it is NOT an ancestor of the current head `12a6e7a4` — the PR was rebased onto develop (hop). => this is class C behaviour for the verdict object, BUT the underlying content is current and the PR is now fresh+clean, so the PR is still READY and the existing verdict is stale. The reviewer explicitly asked for a refresh from develop and a regular exact-head gate — both now hold.
- Class: A (ready-no-verdict-at-this-head). The one existing verdict is stale (C on the verdict-object axis) but does not block readiness.

### PR 1742 — fix(0428-217) git credential fill fails closed — HEAD 20ad0713e9892492204cf88910ee926ee20d1461
- Fresh: fast-forward of develop, mergeStateStatus = CLEAN.
- PR Selected Checks: COMPLETED/SUCCESS (run 44900657812, job 136836870356); Trusted Plan: pass.
- 2 commits (1 fix `fix(0428-217): git credential fill must fail closed…` + 1 `test(0428-217): prove the credential-fill fix…`).
- Delta (develop..head, 8 files): `cmd/baha/app_inspect_remote.go`, `cmd/baha/app_update.go`, `cmd/baha/app_update_gitstdin_test.go`, `internal/credential/native/credfill_noninteractive_test.go`, `internal/credential/native/credfill_pty_linux_test.go`, `internal/credential/native/credfill_pty_stub_test.go`, `internal/credential/native/gitcredential.go`, `internal/credential/native/host.go`.
- Tabu touch: none.
- Verdict inventory: NONE. No review/act file for PR 1742 in baseharbor-plan origin/main. Never reviewed.
- Class: A (ready-no-verdict-at-this-head).

### PR 1746 — ci: run ci-fast-check in the release gate — HEAD 82a12bed617b31b5fe4a39527c0f53f9368014ec
- Fresh: fast-forward of develop, mergeStateStatus = CLEAN.
- PR Selected Checks: COMPLETED/SUCCESS (run 44902159264, job 136841131554); Trusted Plan: pass.
- 4 commits, latest `build(0428-208): pin current v0.4.28 demo source`.
- Delta (develop..head, 10 files): `.github/workflows/pre-release-runtime-suite.yml`, `docs/releases/v0.4.28.demo-ref`, `scripts/ci-fast-check.sh`, `scripts/pr-gate-plan.py`, `scripts/pre-release-check-plan.py`, `scripts/pre-release-runtime-impact.json`, `scripts/release-requirements.json`, `scripts/test_ci_v0427_gate_catalog.py`, `scripts/test_pre_release_check_plan.py`, `scripts/test_pre_release_runtime_reuse.py`.
- Tabu touch: YES — `.github/**` (Owner scope, 0428-211) and `scripts/**` (Owner scope). => Zusatzvermerk: nur Owner — the release-gate/CI wiring touches the release matrix + CI scripts. Even though PR Selected Checks passed, this PR's write-set is Owner-only; it must not be handed to a worker lane.
- Verdict inventory: NONE. Never reviewed.
- Class: A (ready-no-verdict) but with an Owner-only tabu touch — the abnahme-sitz should flag it for Owner rather than pick it up.

### PR 1704 — card 0428-073 r28 correction: honest fail-closed Perses alert — HEAD 45ddf225ac60bf72bdaeaded7025aaa94bd64132
- Fresh ancestry (develop is a merge-base ancestor) but mergeStateStatus = UNSTABLE (multiple hopf merges onto develop; the PR is not a clean single-line fast-forward — 12 commits with several merge hops).
- PR Selected Checks: COMPLETED/SUCCESS (the run that is CURRENTLY reporting exists); the UNSTABLE state is a merge-time refresh condition, not a content blocker.
- Delta (develop..head) touches: `internal/metrics/perses_prometheus_alerts.go`, `internal/metrics/perses_prometheus_alerts_test.go`, `internal/metrics/prometheus*.go` (multiple), `internal/metrics/prometheus_ha_runtime_integration_test.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/prometheus_shared.go`.
- Tabu touch: none (no `.github/**`, `scripts/**`, `internal/operatorauth/`, `internal/identityprovider/`, `internal/serviceaccess/`, `internal/observability/registry.go`, `internal/capability/perses_selection.go`).
- Verdict inventory: `evidence/r28-welle4-2026-11-19/codex-review-wave/1704-0428-073-r3.md` — an exact-head review exists at old head `f5dcf12885489d8b8beb8a57720d659f4b737378`, verdict REQUEST CHANGES, but that head is stale vs current `45ddf225…` (the PR was reworked/refreshed after R3). The current head `45ddf225` is a fast-forward of develop and PR Selected Checks pass.
- Class: A-ish / borderline. Fresh ancestry + pass selected checks, but UNSTABLE merge-state and the only existing verdict (R3) is for a stale head. Not a clean single-commit ready candidate like 1597/1742. Flag for the abnahme-sitz as: re-run an exact-head review at `45ddf225` before accepting; merge-state needs a clean refresh.

## Class counts

- A (ready-no-verdict-at-exact-head): 1597, 1742, 1746, 1704 (1704 conditional)
- B (verdict object missing): 0
- C (verdict exists but stale / non-ancestor of current head): 1597 (verdict head `540ed13c` rebased away), 1704 (R3 head `f5dcf128` superseded)
- D (not ready: draft/behind/dirty/conflicting): 20 PRs (all the BEHIND/DIRTY/UNSTABLE/CONFLICTING above)

## Findings beyond the four ready cases (desk sweep)

- 12 open PRs have NO review/act file at all in baseharbor-plan origin/main (PR 1747, 1746, 1742, 1741, 1740, 1738, 1737, 1736, 1725, 1723, 1614, 1596) — never picked up by a CODEX-REVIEW. Most are not ready (behind/dirty/draft), but 1746 and 1742 ARE ready, which confirms the window.
- The abnahme-sitz is working one PR after another; the current ready set (1597, 1742, 1746, 1704) is exactly what should be triaged next, prioritized by fewest commits and smallest delta: 1597 (1 commit) and 1742 (2 commits) first, then 1704/1746.

## CLEANLINESS

- docker ps -a before: empty (no containers on host; this is the coordinator/codeman server, correctly left untouched — no test stacks started, per owner directive 2026-11-05).
- docker ps -a after: empty.
- host pid: 2511570. No containers were created, so daemon address pools are unaffected.
- No docker/podman compose projects were started; no VM smoke test was run (BUG-HUNT, read-only desk work).

## repo-rule compliance

- No product file edited; no commit to baseharbor; no PR action; no card changed.
- No subagents used (4.8).
- No bare `go test ./cmd/baha/`; no Go execution of any kind.
- No `git add -A`, no `git stash`, no push through an unresolved remote. All remote truth measured via `git ls-remote` / deep clone of the real github remote (`https://github.com/mcpdev80/baseharbor.git`) and `gh` against `mcpdev80/baseharbor`.
- Evidence written ONLY to baseharbor-plan (`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`), never in a product repo. No `.evidence/` directory in any product tree.
- This is a pure BUG-HUNT (read-only desk); no owner-scope `.github/**`/`scripts/**` file was edited — PR 1746's Owner-only touch is reported, not acted on.
- No markdown checkboxes anywhere in this file.

## END

0428-221-huntq: verdict-queue desk complete — ready set {1597, 1742, 1746, 1704}, PR 1746 Owner-only tabu. No product changes.
