# H-V38 — PROVEN catalog patch that clears the 0428-242 guardian for #1810 and #1809 (read-only)

- Mission: `coordinator/missions/w38-hvcatalogpatch.txt` (H-V38, flash, READ-ONLY)
- Lane: w38-0428-242-hvcatalogpatch (hunt desk, no branch, no PR, no product change)
- Date: 2026-11-23
- Verdict up front: **proven-yes.** The 5-row (or 3-row catch-all) `scripts/pr-gate-coverage.json` patch below
  clears the fail-loud guardian offline: both PR plans go rc=1 (abort) → rc=0 with a non-empty selected-gate
  set for the exact heads `168d40950…` (#1810) and `034c0c7d…` (#1809). Diff at "Deliverable" below.

## PLAN

- Resolve the real GitHub remote (URL contains github.com/mcpdev80); work only in /tmp/opencode/hv38.
- Attest develop and both PR heads with ls-remote; fetch refs/pull/*/merge for the exact CI diff shape.
- Read catalog + planner guardian (pr-gate-plan.py:1833-1838) + catch-alls (1424/1449/1541-1544) at develop.
- Copy the develop catalog to /tmp and add rows for the 5 uncataloged cmd/**+internal/** paths, ids per the
  validator's derived convention, surfaces mirrored from nearest siblings.
- Run the planner OFFLINE before/after for both PR diff sets (real pr-diff-base.py output over the exact
  GitHub merge refs); record rc and selected-gate counts.
- Run validate-pr-gate-coverage.py against the patched catalog (lint/self-check).
- Test the catch-all alternative (packages rows instead of per-path rows) and compare row count + proof.
- Emit the apply-ready diff and the proposed new-card contract; write this evidence; push; END.

## Remote and base attestation (reality witnesses)

Planning repo, verified BEFORE the first evidence commit (wrong-zone rule):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v | head -1
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
```

Product repo remotes (all resolve to github.com/mcpdev80; REMOTE GUARD satisfied — `lane-origin` used for all
fetch/ls-remote witnesses; the quarantined `workers/baseharbor` checkout was never cited):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v
lane-origin https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin https://github.com/mcpdev80/baseharbor.git (push)
origin      https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin      https://github.com/mcpdev80/baseharbor.git (push)
upstream    https://github.com/mcpdev80/baseharbor.git (fetch)
upstream    https://github.com/mcpdev80/baseharbor.git (push)

$ git ls-remote lane-origin refs/heads/develop
dc8626e9c52be07a8ea5b87b468c5991b7540c4f	refs/heads/develop
$ git ls-remote lane-origin refs/pull/1810/head refs/pull/1809/head
034c0c7d21512a62b2ec236b779e84235da4f507	refs/pull/1809/head
168d40950bae5b8fb31862b36ceaffbdd1862207	refs/pull/1810/head
$ git ls-remote lane-origin refs/pull/1810/merge refs/pull/1809/merge
d9f415eca9429c44cbcfc346980e3f7e71dc10ae	refs/pull/1809/merge
3aae1c02deec40fbf3f2afa27e73aa924575148c	refs/pull/1810/merge
```

Both PR heads sit directly on develop `dc8626e9c` (merge-base of each head with develop = dc8626e9c; the
GitHub merge refs have parents exactly `dc8626e9c` + head). No branch was created; nothing pushed to any
product repo; no worktree beyond a throwaway blobless clone under /tmp/opencode/hv38/work.

## Method — faithful CI reproduction (offline, read-only)

The live Trusted Plan step runs (`.github/workflows/ci.yml` at develop, job `PR · Trusted Plan`):

1. `python3 scripts/pr-diff-base.py --target-base <effective_base> --head <head> --integration <INTEGRATION_SHA>`
   from a checkout of `effective_base`. I reproduced this exactly against the real objects: `--target-base
   dc8626e9c…`, `--head <pr head>`, `--integration <refs/pull/<pr>/merge>` (the real GitHub merge commits),
   using the develop `pr-diff-base.py`. Resulting `prdiff-1810.json` / `prdiff-1809.json` list exactly the
   mission's changed paths.
2. The planner trio (`pr-gate-plan.py`, `validate-pr-gate-coverage.py`, `pr-gate-coverage.json`) is extracted
   from the controller: `controller = effective_base` when `MIGRATION_CONTROLLER (859654861)` is an ancestor
   of it — and it is an ancestor of `dc8626e9c`, so controller == develop. I ran the planner as develop copies
   (md5 `70abdeec` planner, `049e1dcd` validator, `8c32ee36` catalog, all verified identical to the content of
   both the develop tree and the `refs/pull/*/merge` commits).
3. Invoked with the same authenticated env (`GITHUB_REPOSITORY=mcpdev80/baseharbor`,
   `GITHUB_BASE_REF=develop`, `--requirements release-requirements.json --mapping pr-gate-map-v1.json`).

## Task 1 — BEFORE: guardian abort for both PRs (rc=1)

`/tmp/opencode/hv38/final`, develop inputs, unpatched catalog (md5 `8c32ee36…`):

```
BEFORE PR1810 rc=1 uncataloged_msgs=1 stdout=0B
  -> ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime
     gate owner: internal/application/perses_lifecycle_test.go; internal/capability/perses.go;
     internal/capability/perses_test.go   (ids source.internal_* per the guardian message)
BEFORE PR1809 rc=1 uncataloged_msgs=1 stdout=0B
  -> ValueError: … uncataloged source change …: cmd/baha/secret_audit_test.go; cmd/baha/secret_operations.go
```

Selected-gate count before: NONE — the planner aborts at `scripts/pr-gate-plan.py:1835-1838` (guardian)
before printing any plan (stdout 0 bytes). This matches the H-V37 finding and the live reds
(`PR · Trusted Plan` failure on runs 45247799528 / 45244415977).

## Task 2 — the patch: 5 catalog rows (apply-ready diff)

Ids follow the validator's derivation (`validate-pr-gate-coverage.py:74`,
`"source." + path.replace("/", ".").replace(".", "_")`), as the H-V37 evidence records the guardian itself
prints. Surfaces mirror the nearest already-cataloged sibling for the same package:

- `cmd/baha/secret_*` → the two `data.capabilities` surfaces (the dominant cmd/baha convention, e.g.
  `source.cmd_baha_app_exec_go`), so the gate ids resolve to the existing
  `atomic/docker/data-capabilities` / `atomic/podman/data-capabilities` gates.
- `internal/application/perses_lifecycle_test.go` → observability surfaces with `runtime_specific: true`,
  mirroring `internal/application/perses_runtime_test.go` / `cmd/baha/app_perses_cli_test.go` →
  `atomic/{docker,podman}/observability`.
- `internal/capability/perses.go` + `_test.go` → `source.gate.integration.static.public.contracts`,
  mirroring every other `internal/capability/*` row (lifecycle.go, service_binding*.go, domain_test.go)
  → `integration/static/public-contracts`.

Exact diff (validated: `patch -p1` onto the develop catalog yields byte-identical output to the proven
patched file, md5 `3cf5e28d…`; JSON parses; 5 new components, 259 → 264):

```diff
--- a/scripts/pr-gate-coverage.json
+++ b/scripts/pr-gate-coverage.json
@@ -147,6 +147,32 @@
   "components": [
     {
+      "id": "source.cmd_baha_secret_audit_test_go",
+      "path": "cmd/baha/secret_audit_test.go",
+      "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]
+    },
+    {
+      "id": "source.cmd_baha_secret_operations_go",
+      "path": "cmd/baha/secret_operations.go",
+      "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]
+    },
+    {
+      "id": "source.internal_application_perses_lifecycle_test_go",
+      "path": "internal/application/perses_lifecycle_test.go",
+      "surfaces": ["source.gate.atomic.docker.observability", "source.gate.atomic.podman.observability"],
+      "runtime_specific": true
+    },
+    {
+      "id": "source.internal_capability_perses_go",
+      "path": "internal/capability/perses.go",
+      "surfaces": ["source.gate.integration.static.public.contracts"]
+    },
+    {
+      "id": "source.internal_capability_perses_test_go",
+      "path": "internal/capability/perses_test.go",
+      "surfaces": ["source.gate.integration.static.public.contracts"]
+    },
+    {
       "id": "source.cmd.baha.app.apply.go",
       "path": "cmd/baha/app_apply.go",
       "surfaces": [
```

## Task 3 — AFTER: planner rc=0 for both heads (proof)

Same harness, only the catalog changed (`/tmp/opencode/hv38/final`):

```
AFTER PR1810 rc=0 selected=resolved 3 ['atomic/docker/observability', 'atomic/podman/observability', 'integration/static/public-contracts']
AFTER PR1809 rc=0 selected=resolved 2 ['atomic/docker/data-capabilities', 'integration/docker/coreless-lifecycle']
```

Before/after summary table:

| PR | head | BEFORE (rc, selected) | AFTER (rc, selected) |
| --- | --- | --- | --- |
| #1810 | 168d40950bae5b8fb31862b36ceaffbdd1862207 | rc=1 abort, 0 gates | rc=0, 3 gates, `coverage_status=resolved`, `broad_required=false` |
| #1809 | 034c0c7d21512a62b2ec236b779e84235da4f507 | rc=1 abort, 0 gates | rc=0, 2 gates, `coverage_status=resolved`, `broad_required=false` |

Gate-id resolution proven by `resolve_covered_gates` directly (covered=[], unowned=5 paths before →
covered=3/2 gates, unowned=[] after; `scripts/validate-pr-gate-coverage.py:17-64`).

## Task 4 — validate-pr-gate-coverage.py against the patched catalog

```
$ python3 validate-pr-gate-coverage.py   # --coverage defaults to ./pr-gate-coverage.json (patched)
PR gate coverage catalog is valid
validate rc=0
```

No unresolved source, no undeclared surface, no duplicate id/path, no gate outside the active release
catalog. (Pristine develop catalog also validates clean — `[]` errors — so the lint baseline is fair.)

## Task 5 — catch-all alternative (fewer rows)

`resolve_covered_gates` falls back to `packages[]` directory prefixes when no exact component matches
(`validate-pr-gate-coverage.py:33-36`). Three package rows replace all five path rows and clear BOTH PRs
(identical selected-gate sets):

```diff
--- a/scripts/pr-gate-coverage.json
+++ b/scripts/pr-gate-coverage.json
@@ -117,6 +117,18 @@
   "packages": [
     {
+      "path": "cmd/baha",
+      "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]
+    },
+    {
+      "path": "internal/capability",
+      "surfaces": ["source.gate.integration.static.public.contracts"]
+    },
+    {
+      "path": "internal/application",
+      "surfaces": ["source.gate.atomic.docker.observability", "source.gate.atomic.podman.observability"]
+    },
+    {
       "path": "contracts",
       "surfaces": [
         "source.package.integration.static.public.contracts"
```

Proven: `catchall PR1810 rc=0 selected=resolved 3 …`, `catchall PR1809 rc=0 selected=resolved 2 …`,
`validate_rc=0` (longest-match keeps existing exact component rows authoritative; e.g.
`internal/application/perses_runtime_test.go` still resolves observability-only).

Recommendation: the mission asked for per-path rows; the catch-all is smaller but BROAD — it silently
auto-owns every future uncataloged file under those three roots (thousands of files; the H-V37 evidence
counts 86.7 % of cmd/**+internal/** otherwise unowned), which defeats the purpose of the 0428-242
fail-loud guardian. Land the 5 per-path rows; if the Owner prefers breadth, the 3-row variant is proven
equally green for these two PRs.

## Findings / caveats (STATE, no workflow edits)

- With the patched catalog, the legacy catch-all heuristics (`pr-gate-plan.py:1424` cmd/baha fallback,
  `:1449` internal/capability, `:1541-1544` internal/application) still append `unresolved` entries
  INSIDE `targeted_plan`, but the catalog branch then overwrites `selected_gates` as sole authority and the
  conservative fallback (enabled by `main()`, `conservative_fallback=True`, `pr-gate-plan.py:1941`) resolves
  the plan — final output `coverage_status=resolved`, `broad_required=false`, with broad Go validation
  checks (`cli-gofmt, go-build, go-unit-tests, go-vet`) plus the catalog gates. The earlier "unresolved/broad"
  reading in H-V37 came from calling `plan()` WITHOUT `conservative_fallback=True`; the live CI path passes
  it. Verified here with the exact CLI entry of `main()`.
- The abort is deterministic for every uncataloged cmd/**+internal/** path; catalog-only rows (this patch)
  are the guardian's prescribed fix ("add this source with its surfaces to scripts/pr-gate-coverage.json").
  No `.github/**` change is needed for these two PRs, so no Owner-scope workflow finding blocks this card.
- This proof re-used GitHub merge commits already public (read-only fetches); no PR, comment, rerun or
  dispatch was made by this lane.

## Proposed new-card contract (CI-owner card to land this)

One Owner-scope CI card ("0428-260 follow-through: register 5 residual source rows"): edit ONLY
`scripts/pr-gate-coverage.json` on develop with the 5-row diff above (the proven, validated patch — apply
as-is or its 3-row catch-all variant, decision recorded in the card), push as a scripts-only PR whose own
Trusted Plan is green by the self-change rule (`scripts/**` is outside the guardian's cmd/internal filter),
merge, then re-trigger PR CI on #1810 (`168d40950…`) and #1809 (`034c0c7d…`) with no content change; the
acceptance check is the `PR · Trusted Plan` step rc=0 with the exact selected sets recorded above
(3 gates / 2 gates) and the downstream `PR Selected Checks` aggregate green. Acceptance here means:
offline proof only — merging and re-triggering remain Owner actions because `scripts/**` is Owner/CI-reserved.

## cleanliness

- Read-only mission: all edits confined to `/tmp/opencode/hv38` (catalog copies, patched copies, plans).
  The product repos were touched only by `git fetch` (objects/refs under .git) — no checkout, no branch,
  no commit, no push into any product repo; no worktree created under /tmp beyond the blobless clone in
  `/tmp/opencode/hv38/work/bh` (delete-safe, this lane's own).
- No container/network/volume/compose project was started by this lane (read-only, no docker/podman calls);
  `docker ps -a` witness before and after:

```
$ docker ps -a --format '{{.Names}}' | sort
(no containers at all on this host — before AND after; this lane never issued docker/podman commands)
$ docker ps -a --format '{{.Names}}' | grep -c -i "hv38\|w38"
0
```

- Ambient images untouched; nothing registered or repaired; no VMs used.

## Evidence delivery witness (second-to-last action)

```
$ git -C baseharbor-plan fetch origin main
 * branch                main       -> FETCH_HEAD
$ git -C baseharbor-plan ls-tree -r --name-only origin/main | grep hunt-hv38-catalog-patch
evidence/recovery-2026-11-23/hunt-hv38-catalog-patch/round-1.md
```

Evidence commit `7da3c76e3` is on origin/main (pushed 2488a8c6c..7da3c76e3 main -> main).

## Verdict line

END_DONE hunt-hv38: proven-yes — the 5-row patch (`components` block, diff above; catch-all 3-row variant
also proven) clears the 0428-242 guardian: #1810 rc=1→0 with 3 gates (atomic/docker/observability,
atomic/podman/observability, integration/static/public-contracts) and #1809 rc=1→0 with 2 gates
(atomic/docker/data-capabilities, integration/docker/coreless-lifecycle), validate rc=0.

END hunt-hv38 DONE
