# fix-1 — enrollment consume/issue two-phase boundary documentation

- Task: t-20261118-enrollment-two-phase-boundary-doc (card 0428-115), hunt-914 Befund 2 (medium)
- Mission: `/var/tmp/missions/mission-115-twophase-doc.md`
- Lane/session: w115 (opencode `ses_e0f576c30ffeTN65CZJgxKpOfk`), no subagents used (AGENTS 4.8)
- Product repo: `mcpdev80/baseharbor`, branch `lane-0428-115-twophase-doc`, PR base `develop`
- Candidate SHA: `2039628ba8d981488d93e90f59dff5023fb9a477`
- PR: https://github.com/mcpdev80/baseharbor/pull/1685
- Host note: this session runs on the coordinator/codeman server. No container, compose
  project, network, volume or daemon was started here or anywhere else (docs-only mission).

## PLAN

- Claim the card with `plan.py claim`, publish the claim commit to baseharbor-plan `origin/main`.
- Read hunt-914 `befund-1.md` slice (b) and the boundary itself: `internal/targetenrollment/authority.go`
  (`Consume` at :148-151, issuer sign at :156, `RecordIssued` + revoke path at :167-172) and
  `internal/database/connector_enrollment.go` (`Consume` :76-102 with the
  `previous_certificate_serial` clause at :87-90, `RecordIssued` :109-137 with the
  `certificate_serial IS NULL AND EXISTS(... consumed ...)` guard at :125-135).
- Reality check `develop` with `git ls-remote`, attest the base SHA, confirm the planning repo path.
- Make the two-phase boundary explicit: one contiguous paragraph in the enrollment/trust-plane docs
  (ADR 0020, EN + the mandatory DE counterpart) and one targeted comment block in `authority.go`.
  No behavior change, no migration, no refactoring.
- Verify: `gofmt`, `go build ./...`, `go vet` on touched packages, `go test ./internal/targetenrollment/...`,
  `bash scripts/documentation-audit.sh`, `mkdocs build --strict` for both locale configs.
- Push, open PR against `develop`, watch the exact-head CI run to a terminal state (self-run duty).
- Write this akte, move the card to review, publish the board, post END.

## Workspace / zone witnesses

- Planning repo toplevel (verified BEFORE the first evidence commit, per the wrong-zone warning):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` ->
  `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
  The planning work happened in that repo only; `workers/baseharbor-plan` was never used.
- Product worktree: `/tmp/opencode/w115-twophase-wt` (git worktree of
  `/home/marcel/dev/baseharbor-ecosystem/baseharbor`, created with
  `git worktree add -b lane-0428-115-twophase-doc ... 8dccd4fe1`). Caches under
  `/tmp/opencode/w115-gocache` and `/tmp/opencode/w115-gopath`. No scratch in the ecosystem root.
- Claim commit (baseharbor-plan main): `65685e32986ae53b4be84c27649d7def95cdf4ac`, pushed and
  witnessed by `git ls-remote origin refs/heads/main`.

## Base attestation

- Remote truth (never the quarantined `workers/baseharbor` checkout):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin refs/heads/develop` ->
  `8dccd4fe1a52bbcc61c67f7809079f33b8040d64        refs/heads/develop`
- The branch was cut from exactly that fetched SHA (`git worktree add -b lane-0428-115-twophase-doc
  /tmp/opencode/w115-twophase-wt 8dccd4fe1...`), i.e. `develop` head, not another PR head.
- Ancestor proof, before opening the PR:
  `git merge-base --is-ancestor origin/develop HEAD` -> exit 0 ("origin/develop ancestor: OK")
  with `origin/develop` == `8dccd4fe1a52bbcc61c67f7809079f33b8040d64` == the base SHA.
- Log-line witness (`git log --oneline origin/develop..HEAD | cat`) lists ONLY my commit:
  `2039628ba docs(0428-115): make the enrollment consume/issue two-phase boundary explicit`
  No foreign candidate is carried on top.
- Remote branch witness after push:
  `git ls-remote origin refs/heads/lane-0428-115-twophase-doc` ->
  `2039628ba8d981488d93e90f59dff5023fb9a477        refs/heads/lane-0428-115-twophase-doc`
- Exactly one branch and one PR for this card; no second candidate was created.

## Write-set and content

- `internal/targetenrollment/authority.go` — one comment block on the `Store` interface, the point
  where the two phases are declared (`Consume` / `RecordIssued`). Names the separate transactions,
  the consumed-but-unissued window, the fail-closed properties, the revoke-on-persistence-failure,
  the serialization guards and the only recovery path. Comment-only.
- `docs/decisions/0020-scoped-connector-enrollment.md` — the contiguous English paragraph that makes
  the two-phase boundary explicit right after the existing consumption paragraph.
- `docs/de/decisions/0020-scoped-connector-enrollment.md` — the mandatory DE counterpart (the
  `scripts/check_docs_locale_parity.py` and DE technical-integrity gates require a paired page and
  shared literals; ADRs are translated pages in this repo, so a DE paragraph is added rather than an
  EN-only stub).
- No `.github/**` file touched, no runtime behavior, no schema/migration, no refactoring, no
  `internal/database/` change.

## Checks (local)

- `gofmt -l internal/targetenrollment/` -> no output (clean).
- `go build ./...` -> OK; `go vet ./internal/targetenrollment/ ./internal/database/` -> OK
  (toolchain go1.26.8 from `go.mod`).
- `go test ./internal/targetenrollment/...` -> `ok github.com/mcpdev80/baseharbor/internal/targetenrollment 0.121s`.
  This is the affected-package test; the change is comment-only, so compile plus this package test is
  the smallest sufficient Go check. No new test was added, therefore the CI-capture rule (AGENTS 5.3)
  is not triggered and no `.github/**` change is needed.
- `internal/database` unit run: `go test ./internal/database/...` fails with
  `BASEHARBOR_TEST_DATABASE_URL is not set; the workstation enrollment store test must run against the
  configured test database` in `TestWorkstationEnrollmentDuplicateLiveBootstrapRejected`. Pre-existing
  environment-gated PostgreSQL integration test, unrelated to a comment-only change; I did not start a
  database on this host (test hosts are the named SSH hosts only) and did not modify it.
- `bash scripts/documentation-audit.sh` -> `EN/DE page coverage OK: 168 matched Markdown pages`,
  `DE technical integrity: PASS (168 paired pages)`, and "Documentation audit ... PASS" for all sections.
- `mkdocs build -f mkdocs.yml -d ... --strict` -> rc=0 (English linkcheck).
- `mkdocs build -f mkdocs.de.yml -d ... --strict` -> rc=0 (German linkcheck).

## CI (self-run duty)

- Run: `44408281995` ("CI · PR #1685 · CI · Source & Quality") on head
  `2039628ba8d981488d93e90f59dff5023fb9a477`. Terminal state and per-job outcomes recorded in the
  "CI terminal witness" section below, written after the run reached a terminal state.

## repo-rule compliance

- AGENTS 4.2 scope: documentation + one comment block only; no behavior change, migration or
  refactoring.
- Workflow files untouched; no rerun or `workflow_dispatch` was triggered (Owner scope).
- One candidate branch, base `develop`, branch provenance shown by ancestor test plus log line.
- Evidence lives only in baseharbor-plan under `evidence/r28-welle4-2026-11-18/enrollment-twophase/`;
  nothing was written to a product repo (no `.evidence/` directory).
- No subagents; every step executed in this session.

## cleanliness

- No docker/podman containers, networks, volumes, compose projects or daemons started on any host by
  this lane. `ps` witness for this host: no lane-owned compose project exists (`docker ps` was never
  needed for a docs-only change; nothing was created to bring down).
- Scratch confined to `/tmp/opencode/w115-twophase-wt`, `/tmp/opencode/w115-site*`,
  `/tmp/opencode/w115-gocache`, `/tmp/opencode/w115-gopath`, `/tmp/opencode/w115-pr-body.md`.
- "cleanliness: PASS"

## CI terminal witness

(pending — filled in when run 44408281995 reaches a terminal state)

## END

- END_PENDING: mission-115-twophase-doc.md — waiting for the exact-head CI run 44408281995 to terminate.
