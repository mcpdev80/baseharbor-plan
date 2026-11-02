# n1273 Evidence — PR #1273 native Qualifikation

Lane: n1273 · Coordinator: f49a3303-e8bb-491b-9e2c-b629783c4e5f · Modell: worker-ornith1.5-laptop
Auftrag: PR #1273 (mcpdev80/baseharbor, Broker/OpenBao Persistenz) auf head 6ce07ec4 voll native qualifizieren.

## PLAN

1. Realitätsabgleich (AGENTS 4.1/3.5): gh pr view 1273, git ls-remote head/develop, gh run list --branch work/bcore1. head == 6ce07ec4 + faelsche Runs bestaetigen.
2. Pruefe head == develop + PR-Aenderung; falls Branch-Sync noetig: merge origin/develop im Worktree + force-with-lease push + ls-remote Gegencheck (§6.5 KEIN Head-Switch-API).
3. Native Re-Qualifikation: Docker + Podman + Broker PARALLEL auf neuem head (Kann-jeder-Check Auth/PIN/ENV vom System dokumentieren).
4. Alle Runs bis terminaler Farbe selbst beobachten (Run-IDs + Fehlerzeilen).
5. Falls nativer Lauf inhaltlich failt: Root-Cause file:line + im #1273-Branch beheben.

## repo-rule compliance

- WRITE-SET nur #1273-Branch work/bcore1 + betroffene runtime-validation-Refs (AGENTS 4.3).
- Docker + Podman + Broker parallel, nie serialisiert (AGENTS 3.8).
- Kann-jeder-Check: Auth/PIN/ENV vom System/Owner, nie lane-gesetzt (AGENTS 3.8).
- Eigenes-Run-Pflicht 4.6: jeder gehostete Run bis terminaler Farbe beobachten.
- STOP: KEIN Force an develop/main; destruktive Runner-Aktion nur nach Drei-Punkte-Pruefung (§6.2).
- Merge NICHT durch diese Lane (CODEX-MERGE nach Review).

## Lane-Status

PENDING

## END-Zeile (an Coordinator)

<noch keine — Lauf arbeitet>
