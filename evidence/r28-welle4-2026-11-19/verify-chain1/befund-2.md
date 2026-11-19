# Befund 2 — Live verify chain2 stage (r28-welle4-2026-11-19)

Lane: mission-verify-chain1 (mission tag: verify-chain1), chain2-stufe (same roof card, new round).
Scope: read-only verification of Accepted chain2 claims on live develop. No product change, no PR, no merge.

## PLAN

1. Read mission + coordinator ruling (121/122 = review, skip) — done
2. Reality witnesses: develop heads, merge ancestry, fresh worktree/clone — done
3. Verify #102 (PR #1677) — confirmed
4. Verify #093 (PR #1663) — confirmed
5. Verify #099 demo (PR #164) — confirmed
6. Verify #117 (PR #1687) + two-phase guard context — confirmed
7. Write befund-2.md, commit, push — this file
8. Cleanliness + END post

## Reality witnesses

- Product develop head (ls-remote, re-run this stage): `deeeb64778b3f6109d3a8e49fd652d490901e89c refs/heads/develop` — matches the mission's `deeeb6477`.
- Inspection ran in the same fresh detached worktree `/var/tmp/chain1-wt` at that exact SHA (added via `git worktree add` from a real fetch; the quarantined workers/baseharbor checkout was not cited).
- Planning repo toplevel (wrong-zone check): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- Demo develop head (ls-remote): `5d1cf312e18d06915db35c340bebe4e3d4f39d45 refs/heads/develop`; verified in a fresh clone under `/var/tmp/chain1-demo-wt` checked out at that SHA.
- Merge-commit ancestry into develop (all `git merge-base --is-ancestor <sha> deeeb6477` → YES): 97a840e54 (#1677), 9a37b4bc6 (#1663), ec592fd38 (#1687). Demo: `gh pr view 164` → MERGED 2026-11-18T23:59:37Z into develop at 5d1cf312e, and 5d1cf312e == current demo develop head.

## These (a) — #102, PR #1677 "register application-class signals"

**CONFIRMED** (revision label: develop deeeb6477, merge commit 97a840e54).

Card promise (PR body): register application-class Prometheus targets as application-scoped observability signals; explicit application metrics listing; provider scrape lists exclude these targets (no duplicate scrapes); verify registered app targets from the application scrape job; prune stale entries with their target files; workload-only apps stay a verification no-op.

- Code on develop:
  - `internal/observability/registry.go:559` `ApplicationMetricsSourceID(application, environment, source)` and `:588` `ListApplicationMetrics(placement, applications)` — the explicit application listing; `:563` `PruneApplicationMetrics` with the `application:metrics:` identity prefix (registry.go:569).
  - `internal/metrics/realization.go:181` — registration writes app targets under `ApplicationMetricsSourceID(target.Application, target.Environment, target.Source)`.
  - `internal/metrics/prometheus_verify.go:152` — verification reads `observability.ListApplicationMetrics(placement, allowedApplications)`; `:172` uses the `ApplicationMetricsSourceID(m.Name, m.Environment, "")` prefix for the verify/prune scope.
  - `internal/metrics/prometheus.go:439` — prune keep-set built from `ApplicationMetricsSourceID`, so stale app entries die with their target files.
- Test witness (targeted run, green): `go test ./internal/observability ./internal/metrics -count=1` → `ok github.com/mcpdev80/baseharbor/internal/observability 0.006s`, `ok github.com/mcpdev80/baseharbor/internal/metrics 0.188s` (full package runs, includes the workload-only no-op tests named in the PR's verification list).
- Why the witness carries: the card's promises are exactly the registry identity, listing, verify and prune code paths above, and their package tests cover the register/list/prune/no-op behaviors at this SHA.

## These (b) — #093, PR #1663 "i18n: localize Achtung to English Warning"

**CONFIRMED** (revision label: develop deeeb6477, merge commit 9a37b4bc6).

Card promise: replace the Germanism `Achtung` in non-test sites (9 CLI prompts + the contract marker `attention` const) with `Warning`, schema consts and testdata aligned; presence-based marker logic preserved; German docs stay German by design.

- Code on develop:
  - `grep -rn "Achtung" --include="*.go" internal/ cmd/ contracts/` (excluding `_test.go`) → zero hits outside docs.
  - `internal/application/provider_change_consent.go:36-37` — prompts now `Warning: confirm the displayed changes…` / `Warning: confirm the displayed outcome without a working alternative`.
  - `contracts/provider-impact/v1/scope.schema.json:30` — `"const": "Warning"`; impact.schema.json contains no `Achtung` (`grep -c` → 0 on both schema files).
- Test witness (targeted run, green): `go test ./cmd/baha/ -run TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker -v -count=1` → `--- PASS` (`ok github.com/mcpdev80/baseharbor/cmd/baha`). The broader `go test ./internal/application/` package run (befund-1) was green at the same SHA, covering consent/plan/scope.
- Why the witness carries: the named regression pins exactly the two claim axes — one user-output case (English prompt text) and one JSON-contract case (the renamed marker const).
- CI binding: the regression runs under the existing `release_source_preflight` → `go test ./cmd/baha` job (stated in the PR body); ordinary Go package-test discovery covers it on every PR path touching Go sources — no `.github/**` change was needed or made.

## These (c) — #099 demo, PR #164 "dual-match Achtung|Warning marker"

**CONFIRMED** (revision label: demo develop 5d1cf312e, PR MERGED 2026-11-18T23:59:37Z; core side checked at core develop deeeb6477).

Card promise: demo consumer matchers stay green against BOTH pre-merge core (`Achtung:`) and post-merge core (`Warning:`) via regex alternation; new test drives the post-merge prompt through the real production flow.

- Code on demo develop (fresh clone at 5d1cf312e):
  - `tests/guided/drive.py:507-508` — up_rules for stage 1/2 and 2/2 now carry `(?:…|Achtung: confirm the displayed outcome without a working alternative|Warning: confirm the displayed outcome without a working alternative)`.
  - `tests/guided/new_edit.py:203` — `CurrentConsent.rule()` same alternation.
  - `tests/guided/test_consent_capture.py:595` — `test_20_dual_match_accepts_achtung_and_warning_confirm_prompts`.
- Cross-repo consistency witness: core develop `internal/application/provider_change_consent.go:37` emits exactly `Warning: confirm the displayed outcome without a working alternative` — the string the demo alternation matches (functional proof of the pairing at both heads).
- Test witness (targeted run, green, Python 3.14.4): `python3 -m unittest tests.guided.test_consent_capture.ConsentCaptureRegression.test_20_dual_match_accepts_achtung_and_warning_confirm_prompts -v` → transcript shows the Warning prompts answered `yes`, reaching `READY application and requested infrastructure verified`, `Ran 1 test … OK`.
- Why the witness carries: the test drives the PRODUCTION `drive` module (`run_guided_consent_flow` + imported `up_rules`, not a local copy) against a fake core emitting the post-merge Warning prompt; a match failure would raise before READY.
- CI binding: the demo PR body wires it into the existing `pr-guided-consent.yml` `guided-consent` job, which discovers `tests/guided/test_*.py` on PR→main; no `.github/**` change was needed or made. (Job existence is asserted by the merged PR body and CI history on PR #164; this lane did not open `.github/**`.)

## These (d) — #117, PR #1687 "align app env recovery-flag docs" (docs claim + guard on the real path)

**CONFIRMED** (revision label: develop deeeb6477, merge commit ec592fd38; the two-phase guard itself lands via PR #1685 / lane-0428-115-twophase-doc, also ancestor-YES at deeeb6477).

Card promise: docs/cli/applications.md (+ DE mirror) state the true per-command contract: `--uuid` is the identity selector (app show/status/plan/destroy), `-e/--environment` is a value override and never disambiguates name collisions, `baha app env` rejects BOTH in its own parser.

- Docs code locations: `docs/cli/applications.md:241-257` — `--uuid` as identity selector routed "directly at the registry seam" (:246-247), `-e/--environment` "never disambiguates a name-colliding deployment the way a UUID does" (:248-250), `app env` "rejects both --uuid and -e/--environment in its own parser (`unknown option`)" (:254-256). DE mirror `docs/de/cli/applications.md` carries the same passage (PR #1687 file list).
- Guard on the real path:
  - `cmd/baha/app_env.go:51-83` `parseAppEnvArgs`: only `--reveal`, `--path`, `--format` (plus =-forms) and one positional NAME; any other `-`-prefixed arg (covers `--uuid`, `-e`, `--environment`) hits `case strings.HasPrefix(arg, "-")` → `usageError("unknown option …")`. Docs and parser agree.
  - `cmd/baha/app_context.go:219-223` — `--uuid` routes at the registry seam, "the unambiguous identity for name-colliding deployments (0427-149) that no -e value can disambiguate"; the docs sentence mirrors this source comment (this was the exact CODEX-REVIEW request on #1687, and the merged head satisfies it).
- Test witness (targeted run, green): `go test ./cmd/baha/ -run 'TestAppEnv|TestAppContext|UUID' -count=1` → `ok github.com/mcpdev80/baseharbor/cmd/baha 0.086s` (parser and resolver regressions exercised; docs-only change has no dedicated behavioral test beyond these, consistent with the card's "No behavior change" scope).
- Enrollment two-phase guard context (mission wording "guard-verhalten auf dem echten pfad"): the true two-phase enrollment content is 0428-115 (docs) over the existing implementation — `internal/database/workstation_enrollment.go:70/97` (outstanding-grant guard `consumed_at IS NULL AND expires_at > clock_timestamp()`), `:124-126` (consume in same tenant-local transaction, fail closed on missing/foreign/consumed/expired), ADR `docs/decisions/0020-scoped-connector-enrollment.md:36` ("Consumption and identity recording form two phases that commit in separate transactions"). All present at deeeb6477.
- Why the witness carries: each doc sentence names a parser/branch behavior that was directly inspected at file:line in the same head, and the command-level tests around those paths are green.

## Chain2 summary

All four chain2 theses (102, 093, 099-demo, 117) are confirmed on their live develop heads with file:line inspection plus green targeted runs. No contradiction findings; no card needed.

## repo-rule compliance

- No product changes anywhere (product worktrees were read-only detached; only `git worktree add` / `git clone` under /var/tmp).
- No `.github/**` touched, no reruns, no workflow_dispatch, no PR, no merge, no force, no subagents.
- Unit/interpreter tests only (R1): no containers, networks, volumes or compose projects were started on this host; no VM used (mission names none).
- cleanliness: before/after process lists equal apart from this lane's own short-lived go/python test processes; worktree and clone under /var/tmp removed at END; `docker ps` untouched by this lane. Clean.

## END marker

END mission-verify-chain1.md DONE
