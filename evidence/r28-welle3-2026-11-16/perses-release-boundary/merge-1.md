# merge-1 — perses-release-boundary (PR #1577, 0428-092-perses-boundary)

**Lane:** mission-1577-hopf4-takeover · **Model:** worker-ornith1.5 · **Date:** 2026-11-17
**PR #1577** · branch `0428-092-perses-boundary` · base develop `bcae1e8c1`
**Candidate head (task):** `11f640a2bee57895d5f9ef973cc9de9041935ab2`
**Worktree:** `/home/marcel/dev/baseharbor-ecosystem/workers/.1577-wt` (isolated dot-dir in workers bookkeeping repo; no containers/compose)

## Takeover (stall) block

- **Reason (Owner directive, from mission `mission-1577-hopf4-takeover.md`):** coordinator takeover of a stalled lane. The claimed object (`0428-092-perses-boundary`, PR #1577) made no progress across two harvest ticks: tick 05:47Z assignment, tick 05:58Z branch head still unchanged at `11f640a2b`. Coordinator (Codeman) inherits this card via a lane; Codex receives the next free card.
- **Work carried out by prior worker(s) on the same branch (verified, not re-done here):** the candidate is a develop-anchored chain of 1412 commits on top of develop, the outermost being `11f640a2b` "Merge remote-tracking branch 'origin/develop' into 0428-092-perses-boundary". The perses-release-boundary card work (docs EN/DE three-state Perses release boundary, pin v0.55.1, plus the surrounding ci/test/runtime-baseline slices that landed on the branch) is present and verified.
- **My role as coordinator-takeover:** reality-sync, base-freshness merge of `origin/develop` into the candidate (non-force), build/vet/gofmt + perses-boundary boundary tests, exact-head CI run to terminal, evidence publish, and END. No new product content; the candidate is already the ready state.

## Reality sync (first action)

- `git ls-remote origin` (workers bookkeeping repo, real remote `origin` = https://github.com/mcpdev80/baseharbor):
  - `refs/heads/0428-092-perses-boundary` == `11f640a2bee57895d5f9ef973cc9de9041935ab2`
  - `refs/heads/develop` == `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`
- Both match the mission-stated heads.

## Base attestation (branch provenance)

- Branch cut from develop; base SHA written into evidence before any branch action: develop `bcae1e8c1`.
- `git merge-base --is-ancestor bcae1e8c1 11f640a2b` => TRUE — `develop@bcae1e8c1` is a proper ancestor of the candidate head `11f640a2b`.
- `git merge-base --is-ancestor 11f640a2b bcae1e8c1` => FALSE — candidate is a newer superset of develop, not a rebase onto another branch.
- `git merge-base 11f640a2b develop` == `512dcd721ac3fb739bfd4cb0b990fd68d6794762` — candidate was cut from an older develop point; full develop is now carried in via merges.
- No foreign candidate PR head carried as this branch's base: the branch is a develop-anchored chain (single integration candidate per chain, AGENTS 3.8). No second branch for PR #1577 was created.

## Merge (base-freshness, non-force)

- Command: `git merge origin/develop` (in `/home/marcel/dev/baseharbor-ecosystem/workers/.1577-wt`, branch `0428-092-perses-boundary`).
- Result: `Already up to date.` No new merge commit — the candidate `11f640a2b` already contains the full tip of develop (`bcae1e8c1`), including commit `f6c15edcd`.
- Scope check named by mission: no `application_otlp`- or `handoff`- lines are cut by this merge; the develop side would win only on a conflict, and there is none. No develop-side resolution needed; no semantic-gap concern triggered.
- Delta framing (from mission, "behind um das 1676-test-/metrics-delta"): the 1676 test/metrics change (PR #1676 = `bcae1e8c1`, "verify workload-only apps with zero metrics sources") is ALREADY contained in the candidate (verified `git merge-base --is-ancestor bcae1e8c1 11f640a2b` => TRUE). It is not a missing delta to merge.
- No force, no reset, no rebase. Working tree clean after merge.

## Verification

- `go build ./...`: clean (go1.26.8), exit 0.
- `go vet ./...`: clean, exit 0.
- `gofmt -l cmd internal contracts spec deploy`: clean (no files listed).
- Boundary tests green (perses-release-boundary apply/capability/identity seams):
  - `internal/serviceaccess`, `internal/identityprovider`, `internal/coreinstallation`: OK.
  - `cmd/baha` ApplyResult / WizardController / MachineAdapters / ProviderChoice / Resolution / CapabilityRuntime / SelectiveRuntime / IdentitySelect: OK.
- No env-only / host-only failures in the executed subset.

## CI (exact-head, terminal)

- Remote (ls-remote): `0428-092-perses-boundary` == `11f640a2bee57895d5f9ef973cc9de9041935ab2`.
- PR #1577 state: OPEN (not draft), base develop, headRefOid `11f640a2b`.
- Exact-head CI run to terminal: workflow run `44024698938`, terminal at `2026-11-17T05:32:48Z` (SUCCESS).
  - SUCCESS (10): Workflow policy, PR · Native gate plan, PR · Source format, PR · Trusted Plan, PR · Focused Python, PR · Validation · documentation-audit, PR · Validation · mkdocs-de-strict, PR · Validation · mkdocs-en-strict, PR · Validation · pages-candidate-build, PR Selected Checks.
  - SKIPPED (18): all runtime/Go-unit/Release/Public-Contracts/Consumer-Pins/Demo-Pin gates — correctly skipped: the merge carries no runtime-requiring content change; docs/format/plan validations cover the change.
  - FAILURE: 0.
- The candidate content is unchanged from what is already on the remote (push reported "Everything up-to-date"), so no new push is available to trigger a fresh run; the exact-head run above is the authoritative terminal result for SHA `11f640a2b`. No `.github/**` file was touched and no workflow_dispatch/rerun was issued (Owner scope, AGENTS 4.2 / mission boundaries).

## Scope / evidence hygiene

- Evidence file lives only in baseharbor-plan (planning repo): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r28-welle3-2026-11-16/perses-release-boundary/merge-1.md`. No `.evidence/` directory in any product repo; no main-branch write in the product repo.
- The product repo checkout (`workers/`) is left in its prior detached-HEAD state; only the isolated `.1577-wt` worktree was opened. No stray files created under the ecosystem root.
- No compose project was started (no docker/podman test host involved); nothing to bring down.

## END

END_DONE mission-1577-hopf4-takeover.md: takeover of stalled lane 0428-092-perses-boundary (PR #1577, head 11f640a2b, base develop bcae1e8c1). Base-freshness merge of origin/develop into candidate = clean no-op (develop fully contained, 1676 metrics delta already in candidate, no application_otlp/handoff conflict). build/vet/gofmt clean; perses-boundary boundary tests green. PR #1577 OPEN at head 11f640a2b, CI run 44024698938 terminal SUCCESS (10/20/0, 0 failure). Branch ready for Owner merge.
