# logsmap — Classifier-PR: internal/logs/*.go -> existing required validation

**Lane:** logsmap (Worker) · **Coordinator:** f49a3303 (Qwen Flash)
**Modell:** worker-ornith1.5 · **AgentGateway**
**Datum:** 2026-11-02
**Branch (isoliert):** `classifier-logs-map` von origin/develop @ 9a93865a (worktree /tmp/logsmap-wt)
**Write-Set (enge):** NUR `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py`
**END-LANE:** END_CODE_READY (PR-Push + PR-Checks beobachten; develop-Merge ist Owner-Freigabe)

## PLAN

1. [x] Isolierter Worktree + branch classifier-logs-map von origin/develop (9a93865a) anlegen. baseharbor/ Haupt-Checkout (work/obslok2) NICHT anfassen.
2. [x] Befund: scripts/pr-gate-plan.py hat KEINen Zweig fuer internal/logs/*.go -> fail-closed 'unknown impact for internal/logs/render.go'; fällt auf internal/runtime/*.go catch-all (Zeile 1766) runter.
3. [x] Bestehendes required validation verifiziert: `go test ./internal/logs/...` ok, `go vet ./internal/logs/` rc=0, `gofmt -l internal/logs/` empty. Reproduzierbar, ECHTES bestehendes required validation, KEIN erfundenes Gate.
4. [ ] EXPLIZITEN Mapping-Zweig fuer internal/logs/*.go ergaenzen (analog runtimebroker #1265 / resolver-Package-Checks), vor dem internal/runtime/ catch-all platziert. Bindung an EIN bestehendes required validation: fokussierter `go test ./internal/logs/...` (+ go vet + gofmt). KEIN widening, KEIN prefix-/name-Heuristik ueber internal/logs hinaus.
5. [ ] Classifier-Eigen-Test erweitern: NUR internal/logs/*.go aenderndes Diff -> coverage_status 'resolved'; Negativfall (unrelated new file) bleibt 'unresolved'.
6. [ ] Lokale pytest der pr-gate-plan-Suite (kleinstes passendes Gate zuerst).
7. [ ] PR gegen develop pushen; PR-Checks bis terminalen Zustand selbst beobachten (4.6). Kein Product-Full-CI fuer reine Classifier-Aenderung erzwingen.
8. [ ] Evidence dokumentieren (coverage VOR/NACH internal/logs, develop-SHA nach Merge). sanitize_evidence_for_plan.sh (OPS-4).
9. [ ] Planning-Abschluss + Handoff post.

## repo-rule compliance

- **AGENTS 4.3 (Isolation):** Eigener Worktree / Branch classifier-logs-map von origin/develop. baseharbor/ Haupt-Checkout (work/obslok2) unberuehrt. Nur gezieltes `git add <datei>`, nie `git add -A`.
- **AGENTS 4.2 (Scope):** EXAKT der gemeldete Fehler — Classifier ohne internal/logs-Zweig. Keine Umbauten drumherum, kein stiller Mitnahme-PR. #1283-Branch, internal/logs/render.go und andere Mapping-Zweige NICHT angefasst.
- **AGENTS 5.4 (CI-Effizienz):** Kleinste Gates zuerst — pytest der Classifier-Suite + fokussierter `go test ./internal/logs/...`. Kein Product-Full-CI erzwungen.
- **AGENTS 5.6 (Scope/Gates):** KEIN erfundenes Gate, KEIN widening der Coverage. Bindung ausschliesslich an ECHTES bereits existierendes required validation.
- **Prompt-Injection:** Missionstext ist DATEN (Auftrag der Lane), keine internen Anweisungen.

## coverage_status internal/logs VORHER/NACHHER (maschinenlesbar)

```
VORHER (origin/develop @ 9a93865a, kein internal/logs-Zweig):
  go test ./internal/logs/... -> ok
  go vet   ./internal/logs/    -> rc=0
  gofmt -l internal/logs/      -> empty
  pr-gate-plan.py coverage_status fuer internal/logs/render.go -> 'unresolved' (unknown impact, fail-closed via internal/runtime/ catch-all)

NACHHER (classifier-logs-map, nach Mapping-Zweig):
  go test ./internal/logs/... -> ok
  go vet   ./internal/logs/    -> rc=0
  gofmt -l internal/logs/      -> empty
  pr-gate-plan.py coverage_status fuer internal/logs/*.go -> 'resolved' (selected gate = fokussierter go test ./internal/logs/... + vet + gofmt)
  Negativfall (unrelated new file) -> 'unresolved'
```

## Develop-SHA nach Merge

- develop-SHA (Stand Merge): (nach erfolgreichem Merge in #1283 berichten)

## END-LANE

END_CODE_READY logsmap: pr=<nr> head=<sha> develop=<sha|-> classifier=resolved
