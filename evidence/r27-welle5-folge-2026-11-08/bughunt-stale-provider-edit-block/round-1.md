# 0427-150 · round 1 — stale provider-instance blocks need-edit

Lane: w150-staleedit (flash worker). Card: t-20261108-bughunt-stale-provider-edit-block (0427-150).
Source dossier: hunt H-P3 BF-03 ([hp3.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md)).

CI finding (STATE, no lane change): on candidate `8ce26c983` the draft PR job "PR · Draft focused checks"
(run 42509459864) failed with `stat …/cmd/baha.test: directory not found` for every selected package.
Root cause: `.github/workflows/ci.yml:1189-1193` builds the `selected` array from
`scripts/pr-draft-go-packages.py`, whose output (scripts/pr-draft-go-packages.py:39) contains
`<pkg>.test` pseudo-packages that `go test` cannot resolve; the same script's own selection
(`./cmd/baha` etc.) is correct. Both edits are under `.github/**`/script selection (Owner scope);
this lane did not touch them. The failure is a runner routing defect, not a product/test defect:
the identical package set passes locally with the CI env contract (see ## Local verification).


Note: this file was first written at ~09:30 into the planning checkout; another session's
`git pull`/reset of the shared checkout (8bd1bc88 → e8d5cf97) discarded the uncommitted file
before this lane could commit it. Re-created here from the lane's own records; all witnesses
below were produced by this session.

## PLAN

1. Reality check: fetch product/planning remotes, verify base SHA, create worktree — done
2. Read task contract and dossier BF-03; locate the provider-instance check in the edit-refresh path — done
3. Implement: stale instance = re-resolve against the live provider registry OR clear actionable error (no silent block) — done
4. Regression tests (CI-covered): state-only app same field + instance-really-gone fail-closed — done
5. Focused local runs: go test ./internal/application (full pkg), targeted ./cmd/baha groups, vet, build, readability — done
6. Candidate commit + drift merge + PR #1490 against develop — done
7. Hosted PR checks to terminal state (draft: policy/source gates) — running
8. Evidence on origin/main, END post — this file

## Base attestation and worktree

- Planning repo witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin` → `https://github.com/mcpdev80/baseharbor-plan.git` (the real planning repo, NOT the workers/baseharbor-plan quarantine directory).
- Product base: `git fetch origin develop && git rev-parse origin/develop` in the product clone → `d8849198265f13d34e1ece95d6982ce6b613d2aa` (the name-identity landing the mission points at; no side-bases).
- Branch `fix/0427-150-stale-provider-edit-block` cut at `d8849198265f13d34e1ece95d6982ce6b613d2aa` in worktree `/tmp/opencode/w150-staleedit-wt/0427-150-staleedit-wt`.
- Drift: develop advanced to `0e3a6975e2d96097c284b1f7b8042bfeed21001a` during the work; integrated by merge commit `8ce26c983` on the candidate.
- Ancestry witness: `git merge-base --is-ancestor d88491982 HEAD` and `git merge-base --is-ancestor origin/develop HEAD` → both true (BASES-ANCESTOR-OK).
- Cleanliness witness: `git log --oneline origin/develop..HEAD` lists ONLY `8ce26c983` (drift merge of origin/develop) and `1a4423b36` (this lane's fix commit) — no foreign candidate commits.

## Root cause (file:line on base d88491982)

The edit-refresh path validates stored provider-instance preferences against a stale, partially-reconciled in-memory projection instead of the live provider registry — and the block is a false positive even against the live provider:

1. `cmd/baha/app_edit.go:69-77` restored every stored explicit preference via `SelectProvider`; `cmd/baha/app_provider_choice.go:187-202` rejects any instance missing from the candidate list, so `appEditStart` aborted for EVERY app sharing the Target (wizard never opened) whenever a never-applied state-only sibling record (BF-03's `hp3c5`/`hp3c9`, instance `valkey/shared/environment-dev-91df0423`) left a dangling preference.
2. `cmd/baha/app_edit.go:79-101` (refresh) and `cmd/baha/app_edit_apply.go:251-252` (apply) fed the same stored instances into `appMachinePropose`, whose `app_machine_adapters.go:336-339` mapped an unavailable instance to the flat machine code `unsupported` — confirmation dead-ended with nothing stored and no clear error (the observed silent y→y→y no-op).
3. Projection staleness itself: `cmd/baha/app_core_requirement.go:59-75` keeps only bindings present in BOTH `deployments/*/deployment.json` and `provider-registry.json`, and `:81-113` derives snapshot instances from that projection only. The shared valkey/postgres instances that exist live on the Target but were registered by an unapplied record are invisible to the provider-instance check — the check runs against a stale state instead of the running provider.
4. `internal/application/provider_preferences.go` (`preferredProviderResource`, called from `registerReferenceProvidersAt` via `PreviewReferenceProviderRegistryAt`) is where the projection is built for every edit read/plan path; its re-adoption rule covered only `referenceProviderInstance`-canonical IDs, never live-registered instances the projection lost (`selected provider instance missing or incompatible` / `selected provider for %s/%s is missing or incompatible` fail-closed lines).
5. Preference persistence: `SaveDesiredProviderPreferencesAt` filled `ProviderKind` only from the projected registry — a drifted/canonical-but-absent instance persisted without a kind and silently degraded to automatic on reload.

## Fix

- `internal/application/provider_preferences.go`: `preferredProviderResourceAt(root, …)` (wired in `provider_registry.go:registerReferenceProvidersAt`) keeps the canonical projection rule and adds live re-resolution: an explicitly selected instance missing from the projection but registered in the live `provider-registry.json` under a BaseHarbor provider that supports the requirement is re-adopted; a genuinely gone instance fails closed naming the instance and the `automatic` re-resolution step. `ValidateProviderPreferencesAt` accepts drifted live identities; `SaveDesiredProviderPreferencesAt` pins the provider kind of canonical selections.
- `cmd/baha/app_provider_choice.go`: `appProviderChoicesWithPreferences` offers the live instances named by explicit preferences (the wizard can see and keep them); `Select` failure text unchanged in kind but no longer terminal for the session.
- `cmd/baha/app_edit.go`: `appEditStart` re-resolves stored preferences via `selectStoredProviderPreference` (projection → widened retry against live offers); only an instance resolvable nowhere degrades that ONE requirement to automatic with a visible line. The edit surface can no longer be blocked by a sibling's stale preference.
- `cmd/baha/app_edit_apply.go`: an unrelated needs edit carries stored explicit choices for requirements that stay declared but leave the compact decision (exposure/metrics/logs/OTLP) instead of silently rebinding them to automatic; preference equivalence compares per requirement (`appEditPreferencesEquivalent`).
- `cmd/baha/app_edit_apply_result.go`: the Edit choices authority passes the app's stored preferences into the choice surface so re-resolution is stable across refresh/propose.

## Tests and CI wiring (test → check → trigger)

- New `cmd/baha/app_provider_stale_instance_test.go`:
  - `TestProviderStaleCanonicalSharedInstanceIsReResolvable` — projection-lost live canonical instance is offered and selectable.
  - `TestProviderGoneInstanceFailsClosedWithNextStep` — instance really gone → fail-closed error names instance + next step; nothing published (read-only boundary).
  - `TestAppEditCommandStalePreferenceReResolvesFromLiveRegistry` — BF-03 field shape on the REAL authority wiring: state-only drift, `runAppEdit`-adjacent resolution + guided read stay reachable; source untouched.
  - `TestProviderStaleSiblingStateOnlyAppReResolves` — plan-authority re-resolution of the sibling residue without publishing.
  - `TestAppEditCommandStalePreferenceDegradesToAutomaticWithNotice` — gone preference: wizard still opens, one requirement degrades to automatic with a visible actionable notice (no silent block).
  - `TestAppEditCommandStalePreferenceCancelWritesNothing` — cancel/EOF with drift residue: registry and source byte-identical.
- CI: these are ordinary Go package tests. They run in CI job "CI · Full validation" step `unit_tests` (`go test ./...`, `.github/workflows/ci.yml:374-376`) and in "Release Source Preflight" (`go test ./contracts/... ./internal/... ./spec/...` + `go test ./cmd/baha`, ci.yml:120-123). PR trigger: `pull_request` events against develop select checks via `pr_plan`/gate map (`scripts/pr-gate-map-v1.json` maps `cmd/baha/**`, `internal/application/**`); the lifecycle/cli-surface group the card demands is covered by this unit surface without any `.github/**` change. VM smoke: not needed — the repro is registry state, fully reproduced in-process; no containers/compose were started anywhere by this lane (host cleanliness: `docker ps` untouched by this session).
- Red-proof: on the base (d88491982), the same preference input fails closed with `selected provider for cache.key-value/default is missing or incompatible` (no next step) and the wizard abort path returns an error instead of the notice — verified by a throwaway probe against a pristine base worktree during development; the new tests encode the fixed contract.

## Outcomes and candidates

- Fix commit: `1a4423b36`; drift-merge candidate HEAD: `8ce26c983`; remote witness `git ls-remote origin refs/heads/fix/0427-150-stale-provider-edit-block` → `8ce26c9831b9fcc7eb92a352f4cbdb2713eaa6ee`.
- PR: https://github.com/mcpdev80/baseharbor/pull/1490 (draft against develop, base head `0e3a6975e` at open).
- Candidate HEAD witness: `git ls-remote origin refs/heads/fix/0427-150-stale-provider-edit-block` → `8ce26c9831b9fcc7eb92a352f4cbdb2713eaa6ee refs/heads/fix/0427-150-stale-provider-edit-block`.
- `git log --oneline origin/develop..HEAD` lists ONLY: `8ce26c983` (drift merge of origin/develop) and `1a4423b36` (this lane's fix commit) — no foreign candidate commits.
- Local runs: `go build ./...`, `go vet ./cmd/baha ./internal/application`, `bash scripts/source-readability-audit.sh` PASS; `go test ./internal/application` full package ok (81.9s); targeted `cmd/baha` groups (edit/provider/wizard/apply/mcp/choice) ok. One environmental failure exists on the base too (needs CI's controlled Docker daemon): `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` fails identically on pristine d88491982 on this host ("existing native network lacks a protected Core or shared backend owner") — not caused by this change, recorded as STATE.
- Hosted runs: run 42509459864 ("CI · PR #1490", attempt 1) on candidate
  `8ce26c983` reached terminal FAILURE in the draft-only job "PR · Draft focused
  checks" (see STATE above); all other PR jobs SKIPPED by design while draft.
  After marking ready the selected required checks run; terminal results appended below.

## repo-rule compliance

- No `.github/**` edits; no reruns/dispatches; GitHub-hosted runners only; zero containers/compose started on the session host (this lane owns none; ambient lanes' stacks untouched).
- No subagents (AGENTS 4.8). All witnesses via `git ls-remote`/fresh fetches; the quarantined `workers/baseharbor` refs were never cited.
- Write-set matches the card: target-registry provider-instance refresh on the edit path (`cmd/baha/app_edit*.go`, `app_provider_choice.go`, `app_wizard_controller.go`, `internal/application/provider_preferences.go`, `provider_registry.go`, new test file).
- Incident note: an intermediate broken state of `cmd/baha/app_edit.go` (editor truncation during development) was restored from git and rewritten cleanly before commit; the committed tree builds and passes the focused suites.

## END

(pending — finalize after hosted runs reach terminal state)
