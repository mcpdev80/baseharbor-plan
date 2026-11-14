# round-2 — 0428-092 release boundary correction (CODEX-REVIEW r1)

Lane: lane-0428-092-seam-r2 (mission mission-092-r2.md)
Date: 2026-11-14
Card: t-20261114-r28-perses-release-boundary (0428-092), release v0.4.28
PR: https://github.com/mcpdev80/baseharbor/pull/1577 (OPEN, DRAFT)
Prior candidate reviewed: e955f43507de193cb21dee51ce4021248f3bd08f (REJECT per evidence/r28-welle1-2026-11-14/vm-bughunt/act-1577-review-r1.md)
Candidate after this round: 79a2bf6ccdcdc0e0423003b75066c725e445658f

## PLAN

- Read the CODEX-REVIEW r1 act (file/line findings, recipe 1-4, stop criteria) before the first edit. Done.
- Reality witnesses: PR #1577 head, branch 0428-092-perses-boundary, develop base, PR #1575 head. Done.
- Fix 1: name the complete active v0.4.28 scope in docs/development/pre-release-readiness.md (EN/DE) and docs/internal/pre-release-documentation-audit.md. Done.
- Fix 2: scope `unsupported` to the selected Perses surface without provisioning in docs/releases/v0.4.28.md, docs/reference/releases.md, docs/how-to/observability.md and the German counterparts; hold the authentication-class claim conditional on PR #1575 r2 gating on actual provisioning. Done.
- Fix 3: repair German orthography (Verschlüsselungsschlüssel, Visualisierungsoberfläche, Normalzustand) and run the truncation self-check plus a full read of every changed DE line. Done.
- Fix 4: state explicitly that the Perses provider pin v0.55.1 is separate from BaseHarbor v0.4.28. Done.
- Local docs gates (documentation-audit.sh, locale parity, DE integrity); commit, push to the named candidate branch, PR body refresh, hosted run watched to terminal state. Done.
- Evidence published to planning origin/main before END; END posted. Done (this file is that evidence).

## Provenance and reality witnesses

Planning repo identity, exact command and output before the first evidence commit:

    git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
    /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan

Remote product truth (never the quarantined workers/baseharbor checkout as evidence of remote state):

    git ls-remote origin refs/heads/develop refs/heads/0428-092-perses-boundary refs/pull/1577/head refs/pull/1575/head
    79a2bf6ccdcdc0e0423003b75066c725e445658f	refs/heads/0428-092-perses-boundary
    0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
    dc670bfd4d32baf29afde0e4b021bfdb63f4e0be	refs/pull/1575/head
    79a2bf6ccdcdc0e0423003b75066c725e445658f	refs/pull/1577/head

Base attestation: this round continues the existing PR #1577 branch (the mission
names it as the single candidate; no second branch). The round-1 base is
develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, which is an ancestor of the
prior head `e955f43507de193cb21dee51ce4021248f3bd08f` (verified by the review
act and re-verified here via `git merge-base origin/develop HEAD` =
0e9ccb582f5bdcdc74049bbe3996263cdce6500c).

Own-commits-only log line over the fetched base:

    git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..HEAD
    79a2bf6cc docs(0428-092): state the Perses encryption-key startup boundary (upstream v0.55.0)
    a78bb4189 docs(0428-092): correct v0.4.28 release scope, Perses boundary wording and DE terms (review r1)
    e955f4350 docs(v0.4.28): set optional Perses release boundary (pin v0.55.1)

All three commits are 0428-092 release-boundary work (the first from round 1 of
this same card/PR chain, the latter two from this session); no foreign
candidate is carried on top.

## Changes applied (mapping to the review recipe)

Recipe 1 — active release/audit entry points:
- `docs/development/pre-release-readiness.md` and `docs/de/development/pre-release-readiness.md`: the v0.4.27-scope sentence is replaced by the v0.4.28 active scope: Core, Demo, the delivered CLI and the optional Perses provider surface, with the workstation-to-Core journeys, CLI/JSON/MCP/HTTP compatibility, EN/DE docs, Pages candidate, changelog, release notes, immutable SHAs and the versioned test plan. An unselected Perses surface is stated as `not configured`, no error/readiness failure, and no release proof may assert a Perses instance is implemented or provisioned. Console and Node Connector are excluded as archived snapshots and active consumers only, explicitly without weakening their archived provenance. No gate was removed or softened.
- `docs/internal/pre-release-documentation-audit.md` (the canonical audit; EN-only, `docs/de/**` excludes internal): same v0.4.28 active-scope statement in the binding readiness vocabulary.

Recipe 2 — `unsupported` scoping:
- `docs/releases/v0.4.28.md` / `docs/de/releases/v0.4.28.md`, `docs/reference/releases.md` / `docs/de/reference/releases.md`, `docs/how-to/observability.md` / `docs/de/how-to/observability.md`, `CHANGELOG.md`: `unsupported` is now stated only for the Perses visualization surface when it is selected but not provisioned; the unselected/unconfigured case remains the non-error normal state. The blanket "reports the observability management surface as unsupported when Perses is not provisioned" claim is gone.
- PR #1575 r2 current state (head `dc670bfd4d32baf29afde0e4b021bfdb63f4e0be`) still reports `Provisioned=true` from the pinned declaration (manifest-truth gating) with `Reachability=unverified` and `AuthenticationClass=unsupported`. To stay truthful under that candidate, the release notes carry one explicit current-behavior sentence: until the provider seam gates on actual provisioning rather than the pinned declaration, BaseHarbor reports the observability management authentication class as `unsupported` regardless of the declaration. No page claims Perses is implemented, provisioned or configured. When #1575 lands its final provisioning-gated behavior this sentence is the only piece to revisit.
- No seam files touched (this PR changes only documentation; the `docs/spec/*` and `internal/**` write-set of #1575 is untouched — verified via `git diff --stat origin/develop..HEAD` showing 12 documentation files only).

Recipe 3 — German orthography:
- `Verschlüsselungsschl` -> `Verschlüsselungsschlüssel`; `Visualisierungsoberfolge` -> `Visualisierungsoberfläche` (two places); `Normalzust` -> `Normalzustand`; plus `zukünftig Releases` -> `zukünftiger Releases` and `Release-Scope` -> `Release-Scopes` in the archived-repositories sentence, `Nachweise` -> `Auslieferung` to match the EN "Deliveries" section.
- Self-check ran: `grep -rnE "[a-zäöüß]{18,}(sschl|flae|zust)" docs` over the changed files returns only the intact word `Anbieterrealisierungszustand` in an untouched spec page; every new/changed DE line was read once in full. No half-word line remains in the changed pages.

Recipe 4 — pin separation:
- Both release notes, both reference/releases pages and CHANGELOG now state that the Perses provider pin v0.55.1 (image `persesdev/perses:v0.55.1`) is provider-component metadata, separate from BaseHarbor's own release version. The encryption-key sentence was verified against upstream Perses docs (v0.55.0 upgrade note: auth enabled requires an exactly 32-byte `encryption_key`, Perses refuses to start without it).

## Checks and hosted runs

Local gates on the worktree:
- `bash scripts/documentation-audit.sh` — PASS (all sections).
- `python3 scripts/check_docs_locale_parity.py` — PASS (168 matched pages).
- `python3 scripts/check_de_translation_integrity.py` — PASS (168 paired pages).
- `git diff --check` — clean.
- No new tests were added (documentation-only change), so no CI routing change is needed; the docs audit and strict EN/DE builds already cover these files in the non-draft selected checks.

Hosted runs (self-observed to terminal state, no reruns or dispatch, no `.github/**` change):
- Run `43642605616` on candidate `a78bb4189` — completed/success. `PR · Draft source and routing` and all five `PR · Draft Go` jobs succeeded; remaining jobs skipped under draft selection, as on round 1.
- Run `43642760720` on candidate `79a2bf6cc` — completed/success. Same draft-selection pattern: `PR · Draft source and routing` + `PR · Draft Go · cli-0..3` + `packages` succeeded, all others skipped.

## Scope and repo-rules compliance

- Evidence lives only in baseharbor-plan (`evidence/perses-2026-11-14/release-boundary/round-2.md`); nothing was written to the product repo or a `.evidence/` directory.
- Single candidate: work continued on branch `0428-092-perses-boundary` (PR #1577 head branch), the branch the mission names for this card. No second branch was created; nothing to delete.
- Merge frost honored: no merge, PR remains DRAFT (isDraft=true verified after push).
- No `.github/**` edit, no workflow_dispatch, no rerun; failing checks would have been reported as state only — none failed.
- No subagents; every step executed in this session.
- No containers/compose projects were started on this host; no VM smoke test is part of this mission.
- Planning repo push witness (second-to-last action):
  - `git ls-remote origin main` before push: `3803c2f670adc9d018cb2a268749d99ed0daec99	refs/heads/main`

END mission-092-r2.md DONE — candidate 79a2bf6ccdcdc0e0423003b75066c725e445658f on PR #1577 (draft), runs 43642605616 and 43642760720 terminal success.
