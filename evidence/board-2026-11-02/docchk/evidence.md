# docchk Evidence

## END_LINE
END_DONE docchk: pr=<n> head=<sha> run=<id> | <Satz>

## PLAN

1. **Reproduktion lokal mit BASEHARBOR_TEST_RUNTIME=podman** — Debug-Info-Funktion und podman_doctor_checks.go verstehen
2. **Kontext-sensitive Pruefung** — Docker-Check nur wenn Docker-Runtime, Podman-Check nur bei Podman-Runtime
3. **Unit-Regression fuer beide Kontexte** (Docker und Podman)
4. **PR gegen develop** — Podman-Core-Dispatch beobachten
5. **Architecture Boundary Test** — internal/providers/runtime/podman-Import loesen, Interface-/Port-Schicht nutzen

---

## Schritt 1: Reproduktion und Code-Analyse

### 1.1 Betroffene Dateien identifizieren
