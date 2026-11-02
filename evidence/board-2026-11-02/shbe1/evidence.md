# shbe1 Evidence — Shared-Backend-Umgebungsvergleich GH-Drift

**Mission:** `coordinator/missions/shbe1.txt`
**Repo:** baseharbor · **Base:** origin/develop `20083909` · **Branch:** `shbe1-fix`
**Roll:** Worker · **Modell:** Ornith · **Session:** 35cdb02e-a3b3-4e6d-86f9-1cbb35822587

## PLAN

1. [x] Diff der beiden Umgebungen rekonstruieren: Testlog + Codepfad (Datei:Zeile), welche Variable driftet
2. [ ] Entscheidung mit Begründung: semantische Backend-Schlüssel eingrenzen ODER Caller-Env-Bereicherung korrigieren
3. [ ] Regressionstest: beide Richtungen — echter Unterschied bleibt FAIL, Runner-Drift nicht
4. [ ] PR gegen develop; mcp-lifecycle-acceptance Dispatch auf PR-Branch beobachten

## END <lane>
DONE

## repo-rule compliance
- (wird während der Arbeit ergänzt)
