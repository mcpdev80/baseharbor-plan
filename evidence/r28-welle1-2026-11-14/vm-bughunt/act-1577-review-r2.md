# PR #1577 Review R2

ROLLE: CODEX-REVIEW. Read-only review; no merge.

## PLAN

1. Fetch and verify exact PR #1577 candidate/base and all specified hosted run witnesses.
2. Review readiness/audit scope, overlap with PR #1575 r2, German text, and Perses version pin.
3. Record exact-SHA verdict and correction recipe in planning evidence.
4. Validate and publish evidence to planning origin/main, post END, then hold.

## Scope and witnesses

- PR #1577 candidate: `29dba54dddb02f48568c571e9ce37f671d21e6aa`, branch `0428-092-perses-boundary`, base `develop` at `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`.
- PR #1575 r2 comparison candidate: `dc670bfd4d32baf29afde0e4b021bfdb63f4e0be`.
- Exact `git ls-remote origin refs/heads/develop refs/pull/1575/head refs/pull/1577/head` output:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
dc670bfd4d32baf29afde0e4b021bfdb63f4e0be	refs/pull/1575/head
29dba54dddb02f48568c571e9ce37f671d21e6aa	refs/pull/1577/head
```

- `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 29dba54dddb02f48568c571e9ce37f671d21e6aa`: exit 0.
- `git log --format='%H %an <%ae> %s' 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..29dba54dddb02f48568c571e9ce37f671d21e6aa` lists only the four task-chain commits: `29dba54` (German sentence flow), `79a2bf6` (Perses encryption-key startup boundary), `a78bb41` (r1 documentation corrections), and `e955f43` (optional Perses release boundary). No foreign candidate commit appears.
- PR #1577 remains open/draft. Diff is limited to 12 documentation/changelog files; no product code or `.github/**` change. `git diff --check` is clean.

## Review findings

PASS — The English pre-release readiness page and internal pre-release documentation audit identify the full v0.4.28 scope: Core, Demo, delivered CLI, and optional Perses. They exclude archived Console and Node Connector as active consumers and avoid compatibility claims. The German readiness document is aligned.

PASS — Changed German text includes the required complete terms `Verschlüsselungsschlüssel`, `Visualisierungsoberfläche`, and `Normalzustand`. Full lines sampled from the German v0.4.28 release note, observability how-to, and release reference were read; no truncation was found.

PASS — Perses is consistently pinned to `v0.55.1` / `persesdev/perses:v0.55.1`, explicitly separate from BaseHarbor `v0.4.28`. The official Perses releases page identifies v0.55.1 as the latest release; the official v0.55.0 upgrade guide documents the encryption-key boundary.

BLOCKER — The PR #1577 copy states that a selected but unprovisioned Perses surface is reported as `unsupported` / not configured and is not claimed provisioned. That behavior is inconsistent with PR #1575 r2. In `internal/metrics/management_ui.go`, `VerifyPersesManagementUIAt` validates the compiled-in Perses release pin and returns nil without probing runtime reachability. In `cmd/baha/app_status_collect.go`, the status collector treats a nil verifier result as ready and records the default detail “Prometheus management UI reachable over TLS”; its aggregate management-ui check is successful when selected entries are ready. Thus a pin alone can make `baha app status` report a reachable Prometheus UI when no Perses runtime is provisioned. This conflicts directly with the reviewed release and readiness statements.

Correction recipe: in PR #1575 r2, make status distinguish manifest selection/configuration from runtime reachability. A pin validation must not mark the Perses/Prometheus surface reachable or healthy. Represent the absent runtime as unsupported/not configured (or explicitly unverified where runtime probing is unavailable), then align PR #1577’s English and German statements to the implemented state and repeat the same cross-diff review. Keep both PRs draft until corrected. No product edits or workflow edits were made in this review.

## Hosted runs

- Run `43642605616`: terminal success, `pull_request`, head `a78bb4189a845e9ee4c8bf1e8132c7d34a22679a` (not the reviewed head). Draft source/routing, Draft Go packages, and CLI shards 0–3 succeeded.
- Run `43642760720`: terminal success, `pull_request`, head `79a2bf6ccdcdc0e0423003b75066c725e445658f` (not the reviewed head). Draft source/routing and Draft Go groups succeeded.
- Run `43643473988`: terminal success, `pull_request`, exact reviewed head `29dba54dddb02f48568c571e9ce37f671d21e6aa`. Draft source/routing and Draft Go CLI shards 0–3 and packages succeeded. Workflow policy, source format, selected checks, and runtime jobs were skipped by draft selection; this is not evidence those gates passed.
- No rerun or workflow dispatch was requested or triggered.

## Repo-rule compliance

- Evidence repository root, verified before the evidence commit: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (`git rev-parse --show-toplevel`).
- Planning repository was pulled fast-forward from `origin/main`; pre-commit HEAD and remote `main` were both `24ef397da28786f986cdcd55601474f5d6b4ca2b`.
- Exact `git ls-remote origin main` output immediately before evidence publication:

```text
24ef397da28786f986cdcd55601474f5d6b4ca2b	refs/heads/main
```
- Only this planning evidence file is intended for this review commit. A pre-existing unrelated modified file `evidence/r28-welle1-2026-11-14/cli2-uid-environment/round-1.md` was left untouched.
- `python3 scripts/plan.py check`: 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors, 10 pre-existing dependency warnings.

## Verdict

REJECT PR #1577 r2 at `29dba54dddb02f48568c571e9ce37f671d21e6aa` on the cross-PR false-success/status inconsistency above. The documentation scope, German terms, and version pin otherwise pass. No merge.

END DONE — PR #1577 r2 rejected; review evidence published to planning origin/main.

## PLAN

1. Fetch and verify exact PR #1577 candidate/base and all specified hosted run witnesses.
2. Review readiness/audit scope, overlap with PR #1575 r2, German text, and Perses version pin.
3. Record exact-SHA verdict and correction recipe in planning evidence.
4. Validate and publish evidence to planning origin/main, post END, then hold.

