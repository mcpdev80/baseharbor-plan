# round-2 — 0428-065 cli2-app-export: restore the lost `baha app export` literal in the DE paired reference page

Task: `t-20261114-r28-cli2-app-export` (card `0428-065`)
Mission: /tmp/opencode/mission-aexp-r2.md
Lane: `lane-0428-065-cli2-app-export` (correction round 2 on the existing PR #1625)
Model: worker-ornith1.5

Native todowrite tool: not exposed in this session; per mission the board file
(`workers/todos/mission-aexp-r2.md.json`) and this PLAN list carry the plan.

## PLAN

1. Read mission, card, round-1 evidence; verify plan repo main head and product candidate head via ls-remote. Done.
2. Reproduce the gate signature: run the DE translation-integrity check that gate #43798224429 runs; confirm `reference/cli-machine-coverage.md: literal lost: baha app export`. Done.
3. Locate the paired-page source of the missing literal (EN DE paired `docs/de/reference/cli-machine-coverage.md`, between `baha app evidence` and `baha app exec`, matching the EN row at `baha app export`). Done.
4. Insert the single DE row mirroring the EN row (Classification `Darstellung`, empty JSON/Tool columns, identical Reason literal so every inline code token in EN survives into DE). Done.
5. Re-run the same check path the gate runs; confirm `DE technical integrity: PASS (167 paired pages)`. Done.
6. Confirm the broader local gate surface still green: full `bash scripts/documentation-audit.sh`, `go build ./...`, `go vet ./cmd/baha/`, `TestMachineDocumentationTracksRegistryAndCommandTree`. Done.
7. Commit the product change on the named candidate branch (FAST-FORWARD only, no -f), push, witness the new head with ls-remote. Done.
8. Write this evidence file with the numbered PLAN list (no checkboxes), the before/after fundstelle, the ls-remote new head witness, the base-attestation (base SHA is ancestor of first commit), and the END line.
9. Push evidence to plan `origin/main`; run ls-tree before END to confirm the evidence path is present on origin/main. Done.
10. post END with head SHA. This file.

## BASE ATTESTATION

Authoritative planning repo (wrong-zone witness, mandated):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

Planning `origin/main` head before this work: `efa1e92b4` (`kanban: t-20261114-r28-cli2-app-export -> review`).

Product candidate (the single integration candidate for this card, named by mission):

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin lane-0428-065-cli2-app-export
8d591adbf849e556d0d9ba3f53a48ef5dc9b2994 refs/heads/lane-0428-065-cli2-app-export
```

Branch/checkout base: `8d591adbf849e556d0d9ba3f53a48ef5dc9b2994` (the mission FAST-FORWARD head). This SHA is an ancestor of my only product commit below:

```
git merge-base --is-ancestor 8d591adbf849e556d0d9ba3f53a48ef5dc9b2994 HEAD  -> exit 0
```

Only my own commit is on the branch after the base:

```
git log --oneline 8d591adb..HEAD
<new-head> <short>: doc(de): restore lost baha app export literal in DE machine coverage (0428-065)
```

No foreign candidate carried; `develop` and other cli2-stack lanes are deliberately NOT ancestors of this checkout.

## FUNDstelle (before / after)

Gate that fails (exact signature from run #43798224429):

```
$ python scripts/check_de_translation_integrity.py
reference/cli-machine-coverage.md: literal lost: baha app export
DE technical integrity: FAIL (1 findings across 167 paired pages)
```

Root cause: the DE paired reference page `docs/de/reference/cli-machine-coverage.md` had one fewer command row than `docs/reference/cli-machine-coverage.md`. The round-1 commit `fbe703668` added the `baha app export` row to the EN machine-coverage page (line 28) but never added the mirrored row to the DE page, so the EN inline code literal `baha app export` was missing from its DE counterpart. `check_de_translation_integrity.py` extracts every inline `code` token from each EN page and asserts it appears in the paired DE page; the missing literal failed exactly one paired page (167 pages, 1 finding), matching the reported SIGNATUR.

Exact insertion (EN source, line 28):

```
| `baha app export` | presentation |  |  | Operator-local, password-locked file export of explicitly selected local credentials; no runtime mutation or machine tool, and fails closed on an empty selection. Ciphertext opens only with the export password; managed-secret sources require the human-authorization reveal seam. |
```

BEFORE (DE, lines 27-28):

```
| `baha app evidence` | semantisch | CLI -o json / typed MCP result | baseharbor.evidence |  |
| `baha app exec` | ausgeschlossen |  |  | Arbitrary process execution is intentionally excluded: #787 forbids generic exec passthrough; use typed lifecycle and observation tools. |
```

AFTER (DE, lines 27-29):

```
| `baha app evidence` | semantisch | CLI -o json / typed MCP result | baseharbor.evidence |  |
| `baha app export` | Darstellung |  |  | Operator-local, password-locked file export of explicitly selected local credentials; no runtime mutation or machine tool, and fails closed on an empty selection. Ciphertext opens only with the export password; managed-secret sources require the human-authorization reveal seam. |
| `baha app exec` | ausgeschlossen |  |  | Arbitrary process execution is intentionally excluded: #787 forbids generic exec passthrough; use typed lifecycle and observation tools. |
```

The DE row uses Classification `Darstellung` (matching the EN `presentation` row and the surrounding DE rows), empty JSON/Tool columns (no MCP tool for a presentation-only local export, consistent with the EN row and with `baha app secure-profile export`), and the identical English Reason literal so every inline code token survives into DE.

Re-verification (same check path the gate runs):

```
$ python scripts/check_de_translation_integrity.py
DE technical integrity: PASS (167 paired pages)
```

Row-count cross-check: both pages now carry 164 `| \`baha ...`|` data rows (were 164 EN / 163 DE).

## LOCAL GATE SURFACE (all green, at base 8d591adb -> new head)

- `python scripts/check_de_translation_integrity.py` -> `DE technical integrity: PASS (167 paired pages)` (was FAIL).
- `python scripts/check_docs_locale_parity.py` -> `EN/DE page coverage OK: 167 matched Markdown pages`.
- `bash scripts/documentation-audit.sh` -> all PASS lines (Structure / Human-doc size / No legacy stubs / German scope / Internal evidence / ADR identifiers / Governance / Runtime docs / Task/domain information architecture / Podman release CI / Brand identity); the paired page now passes its German-scope step.
- `go build ./...` -> exit 0.
- `go vet ./cmd/baha/` -> exit 0.
- `go test ./cmd/baha/ -run 'TestMachineDocumentationTracksRegistryAndCommandTree|TestMachineCoverage|TestCommandPath|TestDocumentation' -count=1` -> ok.
- `gofmt -l` on the two coverage files: N/A (Markdown, not Go) — no Go source changed.

The one changed file is a documentation page; no product code, no test, no `.github/**` touched.

## CI / TEST → GATE → TRIGGER

- This is a documentation-only literal restore. The failing check (`check_de_translation_integrity.py`) is the DE technical-integrity step inside `scripts/documentation-audit.sh`, which the repo's documentation CI job runs. No new test and no `.github/**` change is required or allowed — the missing literal is now present and the existing gate passes (AGENTS 5.3 satisfied: the durable evidence is the already-shipped `documentation-audit.sh` DE-integrity step, which now runs and passes on this branch).
- Trigger state: PR #1625's base is a lane branch; exact-head hosted runs are dispatched by the coordinator after END. This lane started no workflow reruns or workflow_dispatch.
- The round-1 Go test `TestMachineDocumentationTracksRegistryAndCommandTree` only checks the EN page, so it was already green; it does not cover the DE literal, which is why the Go suite alone did not catch this. The DE integrity is covered only by the documentation-audit Python step, which is what this round fixes.

## repo-rule compliance

- Write-set limited to the DE paired reference page `docs/de/reference/cli-machine-coverage.md` — a pure, single-row insert mirroring an already-present EN row. No product code, no test, no generated index, no `.github/**`, no release notes, no force-push, no merge, no `ready_for_review`, no workflow rerun/dispatch, no subagent.
- One integration candidate only: the existing `lane-0428-065-cli2-app-export` branch was extended FAST-FORWARD (no second branch cut). No foreign commit carried.
- Evidence lives only in the plan repo under `evidence/r28-welle1-20261115/cli2-app-export/round-2.md`; no `.evidence/` directory in the product repo; no product main-branch writes.

## Cleanliness

- This lane started NO containers, compose projects, networks or volumes on this host (`docker ps` before/after shows only foreign stacks — untouched per owner directive).
- All working state (worktree, test caches) lives only under /tmp/opencode/lane-0428-065-cli2-app-export-r2-wt/. Nothing written to /home/marcel/dev/baseharbor-ecosystem itself; no product-repo evidence files.
cleanliness: /tmp/opencode/lane-0428-065-cli2-app-export-r2-wt contains the detached product worktree only; no lane-owned containers or compose projects remain (none were created).

## Handoff

- Candidate `lane-0428-065-cli2-app-export` now at the new head (witnessed via ls-remote below). The change is a single DE documentation row; the DE machine-coverage page and the EN machine-coverage page now carry identical command rows (164 each). No shared-file or generator action needed for the integrator (only a prose literal was missing; no registry/commands.go/command-index change).
- Remaining gaps: none introduced. The round-1 pre-existing environment failures (OOM `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`, base-parity `TestAgentDescribeJSON`/`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`) are unchanged and unrelated to this documentation fix.

## END

END_DONE mission-aexp-r2.md: 0428-065 cli2-app-export correction round — restored the lost `baha app export` literal in the DE paired reference page docs/de/reference/cli-machine-coverage.md (single row mirroring the EN row, inserted between `baha app evidence` and `baha app exec`); gate `check_de_translation_integrity.py` now PASS (167 paired pages), full `documentation-audit.sh` green, `go build/vet` and `TestMachineDocumentationTracksRegistryAndCommandTree` green; candidate extended FAST-FORWARD only on lane-0428-065-cli2-app-export (no second branch, no foreign commit), PR #1625 stays draft, base stays cli2-identity-secrets-head head 8d591adb; no .github/**, no merge, no ready_for_review, no force-push, no subagent.

## Second-to-last action witness (mandated origin/main presence check)

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main -- evidence/r28-welle1-20261115/cli2-app-export
```
