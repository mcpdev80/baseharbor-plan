# Bug-hunt H-V44: docs cross-reference integrity (read-only findings)

Lane: w180-0428-224-hunt-v44
Date: 2026-11-25
Slice: H-V44 (pure FINDING, no product changes, read-only)

## PLAN

- Step 0: Numbered plan created in the todos board file (`workers/todos/w180-0428-224-hunt-v44.json`) and this ## PLAN list. No native `todowrite` tool is exposed in this session's toolset, so per dispatch rule the board file (a) is the visible leg; Code-Mode was not used to hunt for the tool.
- Step 1: Anchor - ls-remote develop tip, fresh clone at exact tip
- Step 2: Relative links in docs/** - resolve all against current tip
- Step 3: Code-path references (file:line style) in docs/** - verify targets exist
- Step 4: Epic/spec references to retired paths
- Step 5: EN/DE docs index parity
- Step 6: Per-row findings + proposed card lines in this evidence directory
- Step 7: Cleanliness (docker ps before/after, no state left)
- Step 8: Push evidence, ls-tree witness, END post

## Anchor

- Command: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
- develop tip at anchor: `a87da7d179e08d43e8987885c38ab459ff1d887d`
- Re-verified before findings: `git fetch <url> refs/heads/develop && git rev-parse FETCH_HEAD` = `a87da7d179e08d43e8987885c38ab459ff1d887d` (tip unchanged).
- Working copy: fresh clone `/tmp/opencode/w180-0428-224-hunt-v44-wt/bh` checked out at the exact tip SHA (`git rev-parse HEAD` = `a87da7d1...`).
- Method: scripted scan (Python) over all 417 tracked `*.md` files (whole repo walked; docs/** is the finding scope):
  - every relative markdown link target and `#anchor` fragment in docs/** (EN and de trees), resolved against the tip tree;
  - every repo-path reference in prose (backticked or bare `docs/...`, `internal/...`, `contracts/...`, `spec/...`, `cmd/...`, `scripts/...`, `conformance/...`) with `:line` where present, existence-checked against the tip tree.

## Findings

### F1 — Six docs cite `docs/spec/management-access-v1.md` as plain prose text, not as links (4 EN, 2 DE)

The sentence "The normative state definition lives in docs/spec/management-access-v1.md" appears as raw text. The target file exists, but the reference is not a resolvable cross-link and breaks the docs-linking convention (docs/STYLE_GUIDE.md).

| file | line | reference |
| --- | --- | --- |
| docs/releases/v0.4.28.md | 23 | `docs/spec/management-access-v1.md` (plain text) |
| docs/reference/releases.md | 31 | `docs/spec/management-access-v1.md` (plain text) |
| docs/how-to/observability.md | 32 | `docs/spec/management-access-v1.md` (plain text) |
| docs/de/releases/v0.4.28.md | 13 | `docs/spec/management-access-v1.md` (plain text) |
| docs/de/reference/releases.md | 30 | `docs/spec/management-access-v1.md` (plain text) |
| docs/de/how-to/observability.md | 28 | `docs/spec/management-access-v1.md` (plain text) |

Proposed card: convert the six mentions to relative markdown links (`[Management access v1](../spec/management-access-v1.md)` / DE equivalents; `docs/`-rooted form is fine inside docs/spec).

### F2 — Retired top-level docs paths referenced by historical release audits (25 rows, 5 files)

Files like `docs/application-contract.md`, `docs/architecture.md`, `docs/cli.md`, `docs/capability-provider-model.md`, `docs/releases.md`, `docs/input-resolution.md`, `docs/backup-and-restore.md`, `docs/provider-integration-contract.md`, `docs/secrets-and-openbao.md`, `docs/runtime-secret-broker-security.md`, `docs/pre-release-documentation-audit.md` and `docs/release-audits/v0.2.0.md` no longer exist at tip (content lives under `docs/explanation/`, `docs/reference/`, `docs/how-to/`, `docs/spec/`, `docs/releases/`, `docs/internal/`). All citing rows are inside `docs/internal/release-audits/` historical files.

| file | lines | retired reference |
| --- | --- | --- |
| docs/internal/release-audits/v0.2.0.md | 55 | docs/pre-release-documentation-audit.md |
| docs/internal/release-audits/v0.3.0.md | 3 | docs/release-audits/v0.2.0.md |
| docs/internal/release-audits/v0.4.5.md | 42 | docs/cli.md |
| docs/internal/release-audits/v0.4.5.md | 43 | docs/application-contract.md |
| docs/internal/release-audits/v0.4.5.md | 44 | docs/architecture.md |
| docs/internal/release-audits/v0.4.5.md | 45 | docs/capability-provider-model.md |
| docs/internal/release-audits/v0.4.5.md | 46 | docs/input-resolution.md |
| docs/internal/release-audits/v0.4.5.md | 48 | docs/releases.md |
| docs/internal/release-audits/v0.4.5.md | 90 | docs/application-contract.md |
| docs/internal/release-audits/v0.4.5.md | 91 | docs/architecture.md |
| docs/internal/release-audits/v0.4.5.md | 92 | docs/capability-provider-model.md |
| docs/internal/release-audits/v0.4.5.md | 93 | docs/provider-integration-contract.md |
| docs/internal/release-audits/v0.4.5.md | 94 | docs/secrets-and-openbao.md |
| docs/internal/release-audits/v0.4.5.md | 95 | docs/runtime-secret-broker-security.md |
| docs/internal/release-audits/v0.4.5.md | 97 | docs/releases.md |
| docs/internal/release-audits/v0.4.6.md | 66 | docs/application-contract.md |
| docs/internal/release-audits/v0.4.6.md | 67 | docs/architecture.md |
| docs/internal/release-audits/v0.4.6.md | 68 | docs/capability-provider-model.md |
| docs/internal/release-audits/v0.4.6.md | 69 | docs/provider-integration-contract.md |
| docs/internal/release-audits/v0.4.6.md | 70 | docs/cli.md |
| docs/internal/release-audits/v0.4.6.md | 71 | docs/backup-and-restore.md |
| docs/internal/release-audits/v0.4.6.md | 73 | docs/releases.md |
| docs/internal/release-audits/v0.4.7.md | 70 | docs/application-contract.md |
| docs/internal/release-audits/v0.4.7.md | 71 | docs/architecture.md |
| docs/internal/release-audits/v0.4.7.md | 72 | docs/capability-provider-model.md |
| docs/internal/release-audits/v0.4.7.md | 73 | docs/provider-integration-contract.md |
| docs/internal/release-audits/v0.4.7.md | 74 | docs/cli.md |
| docs/internal/release-audits/v0.4.7.md | 76 | docs/releases.md |

Note: v0.2.0.md line 55 and v0.3.0.md line 3 claim the *current* audit "lives at" / is "preserved under" the missing path; today the file is `docs/internal/pre-release-documentation-audit.md` and `docs/internal/release-audits/v0.2.0.md`.

Proposed card: decide a policy for historical audit files — either add a "historical paths" header (as v0.2.0/v0.3.0 do partially) or repoint the paths to the current locations with an annotation. At minimum fix the two "lives at/preserved under" pointer sentences (v0.2.0.md:55, v0.3.0.md:3), which describe CURRENT state with stale paths.

### F3 — `docs/spec/credential-access-v1.md:129` cites a file that never resolves in-tree (retired name)

"…the portable management-access contract previously documented in `docs/spec/management-access-profiles-v1.md`". No such file exists at tip and none ever landed there; the contract is `docs/spec/management-access-v1.md`. The word "previously" softens it, but the name points to a path that cannot be found, so the historical trace is broken. Same row in the DE copy.

| file | line | reference |
| --- | --- | --- |
| docs/spec/credential-access-v1.md | 129 | docs/spec/management-access-profiles-v1.md |
| docs/de/spec/credential-access-v1.md | 129 | docs/spec/management-access-profiles-v1.md |

Proposed card: add the predecessor file name to the rename/lineage table in docs/STYLE_GUIDE.md (or link to docs/releases history where the old contract is recorded).

### F4 — `conformance/v1` used as an identifier prefix that shadows the real directory `conformance/provider/v1`

docs/spec/provider-conformance-v1.md:7 and docs/de/spec/provider-conformance-v1.md:7 write identifiers `provider-contract/v1`, `baseharbor.provider-conformance/v1`, `baseharbor.provider/v1`. The substring `conformance/v1` matches no directory; the package and profile live at `conformance/provider/v1` and `contracts/conformance/provider/v1/profile.json` (both exist). A reader (or an agent resolving the identifier as a path) lands on a nonexistent directory.

Proposed card: low severity — add the directory mapping sentence ("Profile metadata: contracts/conformance/provider/v1/profile.json; harness: conformance/provider/v1") to the spec page.

### F5 — EN-only `docs/internal/` tree while docs/internal is linked from DE product pages

`docs/internal/` holds 34 EN files (22 release audits + guidelines/audits). The DE tree `docs/de/internal/` contains only 2 files (v0.4.25-contract-baseline.md, v0.4.25-runtime-inventory.md). DE product pages point at the EN internal files via absolute GitHub-blob URLs (docs/de/reference/releases.md:84, docs/de/development/pre-release-readiness.md:3, docs/de/DEVELOPMENT_GUIDELINES.md:166) or plain prose paths (docs/de/DEVELOPMENT_GUIDELINES.md:4); all targets exist, so nothing is broken today — but two styles (blob URL vs prose path) coexist for the same normative audit file.

Proposed card: declare the internal-audits tree explicitly EN-only in docs/STYLE_GUIDE.md (parity scope = nav pages only), or translate the pointer files that DE product docs cite. Decision needed; no broken link today.

## Clean pass results (negative findings recorded for completeness)

- Relative markdown links in docs/** (EN + de, 417 md files scanned, nav blocks excluded): 0 broken files, 0 missing anchors or `#fragment` targets.
- mkdocs nav parity: 97 entries EN, 97 DE; no EN-only or DE-only nav pages; every nav target file exists in both languages. Every non-internal docs file has a DE counterpart (0 missing), and no DE-only files exist.
- Code-path references to `*.go` files in docs prose: all resolve except the historical-audit references below.
- (Verified from `git show HEAD:<path>` at the anchor commit; the same files also sit dirty in other lanes' shared-checkout working trees — that dirty state was not used as evidence.) `docs/internal/release-audits/v0.4.25.md:311-315,321` and `docs/development/v0.4.22-evidence-resume.md:17` (+ DE copy line 17) reference `tests/init/run.sh`, `tests/mcp/run.sh`, `tests/agent/run.sh`, `tests/shell-ux/run.sh`, `tests/config-matrix/run.sh`, `tests/lib.sh` — no top-level `tests/` directory exists at tip (test entry points live under `scripts/` and `.github/workflows/`). These are historical/resume documents, but the paths silently rotted. (Part of the F2 family: historical references to retired paths.)
- `docs/development/v0.4.20-release-runbook.md:28` references `conformance/real-world` — directory does not exist at tip (historical runbook, same family).
- `docs/reference/releases.md:142` "provider conformance/fault injection" — prose wording, not a path reference; verified false positive (no `conformance/fault` path claimed).
- Root README.md / AGENTS.md / CLAUDE.md / CONTRIBUTING.md / COMPATIBILITY.md / SECURITY.md relative links: 0 broken.

## Witnesses

- Planning repo remote (before first evidence commit): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` = `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Base attestation: evidence commits sit on `origin/main` e9e948125; own commit 5a9057baf (author `w180-0428-224-hunt-v44`), pushed to main.
- Post-push witness: `git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep ...` output: `evidence/r28-welle6-2026-11-27/bughunt-hv44-doc-links/hunt-1.md` (present on origin/main before END post).
- Product repo read-only: no branches, no pushes, no commits to baseharbor; anchor clone in /tmp/opencode only.
- Foreign working-tree file in baseharbor-plan (`evidence/board-2026-11-26/w136-pr1836-rowsreview.md`, modified by another session before this lane started) was preserved via stash and restored unstaged; it is not part of this lane's commit.

## Cleanliness

- Read-only hunt: no containers started, no compose projects, no state written on this host.
- `docker ps -a` before (host this session runs on; no test containers were started during this hunt): recorded in `/tmp/opencode/w180-0428-224-hunt-v44-wt/docker-ps-before.txt` — header line only (no containers).
- `docker ps -a` after: identical to before (no containers added or removed by this lane).
- Worktree/clone zone: `/tmp/opencode/w180-0428-224-hunt-v44-wt` (lane-owned, disposable).

## END w180-0428-224-hunt-v44 DONE — 5 findings (F1-F5), 40 per-row reference defects across 20 docs files, anchored at develop a87da7d179e08d43e8987885c38ab459ff1d887d
