# WORKFLOW-QUALIFY.md — pure `.github/workflows/*` PRs werden in pr-gate-plan.py NIEMALS `resolved` (außer Receipt-Allowlist)

**Rolle:** ANALYSE (read-only; gh api + git, keine Änderung/Gen/Merge/CI)
**Modell:** Ornith · **Zeit:** 2026-11-01 · **Repo:** `mcpdev80/baseharbor`, classifier `scripts/pr-gate-plan.py` (develop `cb6b7387`), gate-map `work/gate-map` `9581193d`
**Reproduktion:** merge-base(parent..commit) lokal, `resolve_pr_diff` → `plan(diff, REQ, MAP, repository=., context_repository=mcpdev80/baseharbor, context_target_branch=main/develop)`.

---

## 1. STRUKTURELLE ANTWORT: (b) bleibt dauerhaft unresolved — es gibt KEINE Regel (a)

Ein `.github/workflows/*.yml`-File läuft durch die `elif`-Kette von `plan()` (scripts/pr-gate-plan.py) so:

1. `RECEIPT_CONTROL_PLANE_WORKFLOWS` (lines **746-751**) → nur `receipt-approval.yml`, `receipt-post-run.yml`, `receipt-shadow.yml` → `resolved` (CI_CHECKS + WORKFLOW_SYNTAX_CHECKS).
2. `PLANNING_WORKFLOWS` = `.github/workflows/pages.yml` (line **679**) → `documentation-workflow`, `resolved`.
3. **Catch-all** line **1515-1519**:
   ```python
   elif path.startswith('.github/workflows/'):
       area = 'runtime-workflow-unresolved'
       require(CI_CHECKS)
       require(WORKFLOW_SYNTAX_CHECKS)
       unresolved.append('workflow execution/cleanup/evidence impact requires native qualification: ' + path)
   ```
   → **jeder andere** workflow wird `unresolved` gesetzt.

**Es gibt KEINE Stelle im classifier, die ein grünes `atomic/docker/lifecycle`-Nativlauf referenziert und damit die workflow-Flags auflöst.** `selected.add('atomic/docker/lifecycle')` kommt **nur** in (a) WIZARD_COMPONENTS (cmd/baha), (b) CORE_917/CORE_918 reviewed-sets, (c) gate-map `internal/runtime/*.go` (line ~1487, 9581193d). **Niemals** im workflow-Branch. Der finale `coverage_status` (line ~1539) ist `'unresolved' if unresolved else 'resolved'` — ein unverändertes workflow-file hinterläßt `unresolved`, egal wie viele Gates sonst noch `resolved` sind.

> **Antwort:** (b) — dauerhaft `unresolved` bis die workflow-Datei in eine Allowlist (`RECEIPT_CONTROL_PLANE_WORKFLOWS` / `PLANNING_WORKFLOWS`) aufgenommen wird ODER eine gate-map-add-rule den workflow-prefix mappt. Ein grüner nativer Lauf ALLEIN löst das Flag in diesem classifier nicht auf (das ist designbedingt fail-closed: „workflow execution/cleanup/evidence impact requires native qualification").

**Warum #1243 speziell unresolved bleibt:** `.github/workflows/runtime-broker.yml`, `.github/workflows/runtime-s3-acceptance.yml` → beide `runtime-workflow-unresolved`. runner-swap (ubuntu-latest) ist „execution impact", aber kein mapped gate.

---

## 2. MERGE-BEISPIEL aus develop-GECHICHTE

### (A) RESOLVED: reine Receipt-Workflows → über Allowlist
|#1195|`bcfc2760`|2026-10-29|`.github/workflows/receipt-post-run.yml` (1 insert)|`resolved`|gates=[]|Allowlist line 746
|#1198|`7a417d37`|2026-10-29|`.github/workflows/receipt-post-run.yml`|`resolved`||
|#1211|`46ed3e8c`|2026-10-29|`.github/workflows/receipt-approval.yml`|`resolved`||
**Befund:** alle merge-zeitlich `resolved`, **weil** die Datei in `RECEIPT_CONTROL_PLANE_WORKFLOWS` steht (line 746).

### (B) UNRESOLVED: nicht-receipt reine workflow-PRs → CATCH-ALL (Trotz Merge!)
|#387|`ebfa762a`|2026-09-23|`release.yml`+`supplemental-release-validation.yml`|`unresolved`|beide workflow-unresolved
|#221|`4bf7ddf1`|2026-09-20|`pre-release.yml`|`unresolved`||
|#384|`e9c77907`|2026-09-23|`release.yml`|`unresolved`||
|#294|`3b83f2fd`|2026-09-21|`ci.yml`+5 workflows|`unresolved`|6 workflow-unresolved
|#218|`ad48c16c`|2026-09-20|`pre-release.yml`|`unresolved`||
|#219|`b84bc4f4`|2026-09-20|`pre-release.yml`|`unresolved`||
**Befund:** Diese PRs wurden **trotzdem gemergt** (in `main`), aber der **classifier klassifiziert sie merge-zeitlich als `unresolved`**. Merge ≠ resolver-resolved; die Kette merge über PR-Approval/owner-override, nicht über `coverage_status='resolved'`.

### (C) #1243 (aktller Kandidat, dieses Issue)
- Files: `.github/workflows/runtime-broker.yml` (runner swap), `.github/workflows/runtime-s3-acceptance.yml` (runner swap) — **pure `.github/workflows/*`, nur runs-on**.
- Classifier merge-zeitlich: **`unresolved`**, beide files `runtime-workflow-unresolved`, gates=[].
- Status: offen, nicht gemergt (`state=open, merged=false`).
- **Schluss:** #1243 bleibt unresolved bis gate-map-add (workflow-prefix mapping) ODER Aufnahme in eine workflow-allowlist — **nicht** durch grünen docker-lifecycle-Lauf auflösbar.

---

## 3. file:line-Zeugnisse
- Catch-all workflow rule: `scripts/pr-gate-plan.py` **lines 1515-1519**.
- Receipt workflow allowlist: `scripts/pr-gate-plan.py` **lines 746-751** (`RECEIPT_CONTROL_PLANE_WORKFLOWS`).
- Planning workflow allowlist: `scripts/pr-gate-plan.py` **line 679** (`PLANNING_WORKFLOWS = {'.github/workflows/pages.yml'}`).
- coverage-final: `scripts/pr-gate-plan.py` **line ~1539** (`status = 'unresolved' if unresolved else 'resolved'`).
- gate-map `internal/runtime/*.go` → lifecycle: `scripts/pr-gate-plan.py` **~1487** (9581193d); **kein** workflow-mapping.
- Merge-beispiele klassifiziert mit `resolve_pr_diff`+`plan()` (Transkript `evidence/integrate-map-plan.md`).

---

## 4. Implikation für integrate-map
#1238, #1243, #1225(ci.yml) sind workflow-only-PRs → **brauchen gate-map-add** (siehe MERGE-ORDER.md §3 C/D), nicht nur rebase. Ein grüner GH-hosted native Lauf macht den classifier **nicht** resolved. Merge dieser PRs erfordert daher **owner-Approval/override** (PR-Flow), weil der resolver fail-closed bleibt.

---

END integrate-map (read-only follow-up) DONE
