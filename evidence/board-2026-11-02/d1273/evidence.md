# d1273 Evidence — CI-Stabilisierung v0.4.27 (PR #1273)

## PLAN

1. **Schritt 1: Realitätsabgleich** — `gh pr view 1273` + `gh run list`, develop-HEAD bestätigen (9a93865a), aktuelle Docker/Broker/Podman Run-IDs + Status prüfen
2. **Schritt 2: Root Cause feststellen** — Workflow-Dateien lesen, CWD/Evidence-Pfade mit file:line belegen
3. **Schritt 3: Fix-Kategorie bestimmen und anwenden** — (a) Branch-Sync auf develop, (b) Workflow-Fix, (c) Trusted-Base-PR
4. **Schritt 4: Hosted-Runs parallel beobachten** — Eigenes-Run-Pflicht, Docker- UND Podman-Gates parallel, kann-jeder-Check dokumentieren, planning evidence schreiben

## repo-rule compliance

- WRITE-SET: nur PR #1273 Branch + betroffener runtime-Workflow
- KEIN #1283/internal/logs
- KEIN Force-Push an develop/main
- Evidence nach AGENTS 4.2/4.3/4.5

## Status:

- END: waiting — awaiting start of work
