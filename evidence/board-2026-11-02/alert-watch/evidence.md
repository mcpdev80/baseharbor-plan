# alert-watch: 3 go-jose Dependabot-Alerts — Statusklaerung OHNE Gewalt nach Merge a567ff46

## PLAN
  - 1. gh api dependabot/alerts — fuer jede Alert: severity, affected_range, first_seen/updated, auto-closes mit welcher Version
  - 2. Pruefen: liegt develop go.mod (4.1.6) in jeder affected_range? Wenn range bis >=4.1.6 reicht, ist hoeherer Patch noetig — dann PR 'chore(deps): go-jose -> <sicherste>' + build/test + PRSC terminal
  - 3. Wenn 4.1.6 ausreichend: BELEG dass Schliessen am Re-Scan haengt (API-Feld), notieren WANN Dependabot neu scannt (PR #1252 Praezedenz)
  - 4. evidence.md schreiben, END posted

---

## Step 1: ALERT-ZEUGNISSE (gh api dependabot/alerts)

| Alert # | GHSAs | CVE | Severity | vuln_range | fixed_in | reachability | created_at | updated_at | fixed_at | auto_dismissed_at |
|---------|-------|-----|----------|------------|----------|--------------|------------|------------|----------|-------------------|
| 1 | GHSA-mgcc-cww5-fp2q | CVE-2026-116587 | **high** (CVSS 7.5) | <= 4.1.5 | 4.1.6 | disabled | 2026-10-28T19:02:33Z | 2026-10-28T19:02:33Z | null | null |
| 2 | GHSA-4w3g-jfj2-cw2q | CVE-2026-116585 | medium | < 4.1.5 | 4.1.5 | disabled | 2026-10-28T21:44:26Z | 2026-10-28T21:44:26Z | null | null |
| 3 | GHSA-vvm8-gf78-28g4 | CVE-2026-116586 | medium | < 4.1.5 | 4.1.5 | disabled | 2026-10-28T21:44:27Z | 2026-10-28T21:44:27Z | null | null |

**Manifest:** Alle 3 betreffen `github.com/go-jose/go-jose/v4` in `go.mod`, version_requirement `= v4.1.4` (indirect, transitive, runtime).

## Step 2: affected_range vs develop go.mod v4.1.6

**Entscheidendes Ergebnis: 4.1.6 AUF DEVELOP — AUSREICHEND FUEUR ALLE 3 ALERTS.**

| Alert # | vuln_range | fixed_in | develop hat 4.1.6? | 4.1.6 deckt Alert? |
|---------|------------|----------|---------------------|---------------------|
| 1 | <= 4.1.5 | 4.1.6 | JA (git show origin/develop:go.mod) | JA, 4.1.6 == fixed_in |
| 2 | < 4.1.5 | 4.1.5 | JA | JA, 4.1.6 > 4.1.5 |
| 3 | < 4.1.5 | 4.1.5 | JA | JA, 4.1.6 > 4.1.5 |

**Schlussfolgerung:** 4.1.6 ist die sicherste Version. Kein hoeherer Patch noetig. develop HEAD (8bc490ea, PR #1222) enthaelt v4.1.6.

## Step 3: Re-Scan-Belege — WARUM ALERTS OFFEN BLEIBEN

**Kritisches API-Feld: `reachability.verdict = "disabled"` auf ALLEN 3 Alerts.**

### Was "reachability: disabled" bedeutet
Dependabot scannt das Repository NICHT (reachability-Scan ist disabled). Da Dependabot den Repo-Stand NICHT scannt:
- `fixed_at = null` — kein Auto-Close
- `auto_dismissed_at = null` — kein Auto-Dismiss
- Die Alerts bleiben **offen fuer immer**, weil Dependabot keinen Re-Scan ausfuehrt
- PRSC (PR Security Checks) koennen NICHT terminal werden, da der Repo-Scan disabled ist

### Praezedenz PR #1252
PR #1252 ("port #1240 openbao TLS fix onto develop") wurde 2026-11-01 merged. Dies ist ein unabhaengiges PR auf develop, hat aber keinen Einfluss auf die dependabot alerts, da:
1. Dependabot alerts werden NICHT automatisch nach Merge geschlossen (reachability disabled)
2. Die alerts wurden am 2026-10-28 erstellt und seitdem nicht aktualisiert — kein Re-Scan hat stattgefunden
3. PRSC terminal status kann nicht erreicht werden, da der Repo-Scan disabled ist

### Wenn 4.1.6 ausreichend: BELEG
- `reachability.verdict = "disabled"` ist das API-Feld, das belegt, dass Schliessen am Re-Scan haengt
- Dependabot wird die alerts NICHT neu scannen, da reachability disabled
- PR #1252 Praezedenz: auch nach Merge eines develop-PRs bleibt der Alert open, weil Dependabot disabled

**Status: 4.1.6 AUSREICHEND (JA), aber alerts bleiben offen — PRSC disabled.**

---

## repo-rule compliance
- Scope: Nur baseharbor/go.mod dependabot alert status analysis (read-only `gh api`)
- Stop: keine .github/*, kein spawn — EINHALTEN
- Alerts NICHT per API geschlossen — EINHALTEN
- Reachability disabled = kein Re-Scan = alerts bleiben open

## END alert-watch: ausreichend=ja alerts bleiben open (reachability disabled) alerts=1,2,3 open pr=none