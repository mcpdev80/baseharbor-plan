# W1-C — Connector Draft #4 Reconcile — Evidence

**Mission:** `coordinator/missions/w1-connector-reconcile.txt`
**Repo:** `mcpdev80/baseharbor-node-connector` (mcpdev80) — **NUR Analyse + Evidence, KEINE Produktänderungen**
**Coordinator lane / Task-Id:** `f49a3303-e8bb-491b-9e2c-b629783c4e5f`
**Draft #4 head (PR #4):** `365094890c091fbf627c9d71c94e44751018e6e9` (Marcel Pfingstgräf, 2026-10-08)
**Ist-SHA today's main:** `188036f25fe6e7dbfd69f840c35a9e2eff50fb96` "Merge PR #17: Node-Connector CI 100% GitHub-hosted (rootful Podman)"
**Merge base (Draft#4 ↔ main):** `572b81dab1e48ef7df18c4e40b038ba33e196827` — dies ist der nc-3-Akzeptanz-Baseline-Commit (nc-3 task §Goal).
**Method:** `git diff --name-only origin/main 365094890c091fbf627c9d71c94e44751018e6e9` → 17 Dateien; für jede Datei `git cat-file -e origin/main:<file>` + sha256-Vergleich; Diff-Inhalte gelesen. **Keine Produktänderung durchgeführt.**

## PLAN (4.4 — getickt)

- [x] Draft #4 vollständig holen (head 36509489); jede geänderte Datei listen
- [x] Realitätsgleichgewicht: heutiges main fetchen, Stand/SHA dokumentieren (4.1)
- [x] Dateiengauer Vergleich pro Datei: [a] in main, [b] Konflikt, [c] fehlende Implementierung
- [x] nc-3-Abhängigkeiten prüfen (node-cli/service/streams/trust, nur Lesen)
- [x] CI-Dateien (.github/**, workflows): NICHT ändern, Bedarf als Befund
- [x] Gap-Map (Datei → Status a/b/c → nc-Task → nächster Schritt) + Kurzbewertung
- [x] Evidence geschrieben
- [x] HANDOFF: END_DONE posten

## Ist-SHA main (Realitätsgleichgewicht 4.1)

- today main HEAD: `188036f25fe6e7dbfd69f840c35a9e2eff50fb96` (nach `git fetch origin main`, 2026-11-02)
- PR #4 ist CLOSED, Inhalt laut Release-Note **erhalten**; der PR-SHA ist `365094890c091fbf627c9d71c94e44751018e6e9`
- Draft #4 ist **kein** ancestor von main und main **kein** ancestor von Draft#4 — die beiden Linien sind seit Baseline `572b81d` auseinandergegangen
- **Wesentlich:** heute main ist das **Oberfeld** von Draft #4 im Sinne „enthält alles + mehr": alle 17 diff-Dateien existieren auch auf main; main hat **10 Dateien entfernt**, die Draft#4 noch hatte, und an den restlichen 7 Dateien ist main die jüngere/andere Version

## Draft #4 — geänderte Dateien (diff vs today's main, 17 Dateien)

| # | Datei | Status (a/b/c) | Befund |
|---|-------|----------------|--------|
| 1 | `internal/targetaccess/bootstrap.go` | **b — Konflikt mit heutigen Vertrag** | Draft#4 nutzt `os.Stat`; main nutzt strikter `os.Lstat` + „symlinks forbidden". |
| 2 | `internal/targetaccess/bootstrap_test.go` | **b — Konflikt (Test)** | Draft#4 **enthält nicht** `TestEnsureEnrollmentPrivateKeyRejectsSymlink`; main enthält ihn. |
| 3 | `.github/workflows/ci.yml` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 4 | `.github/workflows/release-integration.yml` | **a — in main (superseded)** | Draft#4 = ältere rootless-Version; main = PR#17 GH-hosted rootful-Neischrift (vollständig ersetzt). |
| 5 | `.github/workflows/source.yml` | **a — in main (superseded)** | Draft#4 = ältere rootless-Version + `workflow_dispatch`-Input; main = GH-hosted Rewrite ohne Input. |
| 6 | `.github/copilot-instructions.md` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 7 | `AGENTS.md` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 8 | `CLAUDE.md` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 9 | `CONTRIBUTING.md` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 10 | `LICENSE` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 11 | `SECURITY.md` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 12 | `docs/RELEASE-INTEGRATION.md` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4. |
| 13 | `docs/DEPLOYMENT-BOUNDARY.md` | **a — in main (superseded)** | Exists on main; Draft#4 enthält ältere v0.4.24-Kompatibilitäts-Sektion. |
| 14 | `README.md` | **a — in main (superseded)** | Exists on main; Draft#4 enthält v0.4.26/v0.4.24-Kompatibilitäts-Abschnitte. |
| 15 | `integration-candidate.json` | **a — in main (neu/ersetzt)** | Exists on main (Schema `…/v1`, release `0.4.26`); Draft#4 enthält ältere `console`-Variante. |
| 16 | `scripts/release-integration-receipt.py` | **a — in main (superseded)** | Exists on main; Draft#4-Version enthält ältere receipt-Kontrakte. |
| 17 | `zz-o16-test.txt` | **a — in main (neu)** | Exists on main, **deleted** in Draft#4 (public-consumer-source-lock v1). |

## Gap-Map (Datei → Status a/b/c → nc-Task → nächster Schritt)

| Datei | Status | nc-Task-Bezug | Empfehlung nächster Schritt |
|-------|--------|---------------|-----------------------------|
| `internal/targetaccess/bootstrap.go` | **b — Konflikt** | `t-20261018-r27-node-service` (install/bootstrap/enrollment; file-ownership §) | **Verwerfen, nicht reaktivieren.** Main (`Lstat`+symlink-reject) ist strikter und sicherer. Draft#4 `Stat` würde symlink-resilience zurückbauen — fail-closed-Vertrag verletzt. nc-3-Abschluss muss `Lstat` behalten. |
| `internal/targetaccess/bootstrap_test.go` | **b — Konflikt (Test)** | `t-20261018-r27-node-service` | **Verwerfen.** Draft#4 enthält den symlink-reject Test nicht; main schon. Reaktivierung würde fail-closed Test entfernen. |
| `.github/workflows/release-integration.yml` | **a — in main (superseded)** | `t-20261018-r27-ci-runtime` (CI) | Draft#4-Verion **nicht** vorbefüllen; main ist die GH-hosted Vollversion. |
| `.github/workflows/source.yml` | **a — in main (superseded)** | `t-20261018-r27-ci-runtime` | Wie oben. |
| `.github/workflows/ci.yml` | **a — in main (neu)** | `t-20261018-r27-ci-runtime` | Draft#4 hatte ci.yml **nicht**; nichts zu vorbefüllen. |
| `.github/copilot-instructions.md` / `AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING.md` / `LICENSE` / `SECURITY.md` | **a — in main (neu)** | — (docs/hygiene) | Alle auf main vorhanden. Draft#4 enthält sie nicht; nichts vorbefüllen. |
| `docs/DEPLOYMENT-BOUNDARY.md` / `README.md` / `docs/RELEASE-INTEGRATION.md` | **a — in main (superseded)** | `t-20261018-r27-docs` | Main-Inhalt gilt; Draft#4-Kompatibilitäts-Abschnitte historisch, nicht reaktivieren. |
| `integration-candidate.json` | **a — in main (neu)** | `nc-3` (candidate-acceptance) | Main-Kandidat `0.4.26` gilt. Draft#4 `console`-Variante veraltet. |
| `scripts/release-integration-receipt.py` | **a — in main (superseded)** | `t-20261018-r27-ci-runtime` | Main-Receipt-Kontrakte gelten. |
| `zz-o16-test.txt` | **a — in main (neu)** | — | Auf main vorhanden. |

## Summary counts

- **files = 17** (Dateien im Diff main ↔ Draft#4 head)
- **in_main = 17** (alle 17 existieren auch auf today main — main ist Oberfeld)
- **superseded_by_main = 13** (docs/README/CI/receipt/candidate/hygiene — historisch, nicht reaktivieren)
- **conflict = 2** (`bootstrap.go`, `bootstrap_test.go` — Draft#4 ist **schlechter/strenger-vertrag-verletzend** als main)
- **missing = 0** (Draft#4 enthält **keine** echte, in main fehlende Implementierung; der Diff ist rein deletions-/retention-dominiert: 197 + / 652 −)

## Befunde / nc-3-Abhängigkeiten (nur Lesen)

- **Baseline `572b81d`** ist der nc-3-Akzentanz-Baseline-Commit (nc-3 §Goal: Connector `572b81dab1e48ef7df18c4e40b038ba33e196827`). Draft #4 wurde darauf aufbauend fortgeführt, main jedoch **nicht**.
- **Draft#4 ist inhaltlich eine ÄLTERE/STUFEN-Abzweigung** der main-Linie seit Baseline: an allen 17 diff-Dateien ist main das jüngere Superseded (10 komplett entfernt, 7 ersetzt/aktualisiert).
- **Echte Produktimplementierung im Draft#4-Diff = 0.** Die einzigen zwei Go-Quelldateien (`bootstrap.go`, `bootstrap_test.go`) sind **zurückgebaut** (Strengerkeit/`Lstat`-symlink-reject in main erhalten). Draft#4 führt **keine** neuen nc-3-Fähigkeiten, die in main fehlen würden.
- **nc-3-Teile, die Draft#4 „vorbefüllt" hätte sein können:**
  - `t-20261018-r27-node-service` → `internal/targetaccess/bootstrap.go` / install.go: **Draft#4 vorbefahlt NEGATIV** — main hat die strikere `Lstat`-Implementierung bereits; Draft#4 würde sie zurückbauen. **Nicht reaktivieren.**
  - `t-20261018-r27-node-trust` → `internal/targetaccess/session*.go` / `outbound*.go`: **Draft#4 berührt diese Dateien nicht** (0 Änderungen) → nichts vorbefüllt.
  - `t-20261018-r27-node-streams` → `internal/connector/target_access_stream.go`, `stream_replay.go`, `internal/targetaccess/streams.go`: **Draft#4 berührt keine** → nichts vorbefüllt.
  - `t-20261018-r27-node-cli` (Repo `baseharbor`, nicht connector) → `cmd/baha/node*.go`: **Draft#4 (connector) berührt nichts** → keine Bezüge.
- **nc-3-Abschluss-Regel (aus der Karte):** „Keep historical PR #4/source branches intact; historical source evidence does not qualify the current candidate." → Draft#4 wird **als Branch bewahrt**, aber **nicht als Implementierung reaktiviert**; die aktuellen Kontrakte (main) bleiben autoritativ.
- **nc-3 ist State `waiting`** (v0.4.27 formal zurück auf waiting, Outcome-Referenzen verlinkt). Kein nc-3-Task aktiv — W1-C ist rein analyse/evidence.

## empty reimplementation avoided — wie

Die Release-Note fordert „never replace its work with an empty reimplementation." Diese Lane hat:
1. **Kein Produkt berührt** (Scope „NUR Analyse + Evidence", CI-Regel Nacht). Keine Datei geschrieben/geändert/gelöscht; kein Branch-Check-out zur Änderung.
2. **Draft #4 als bewahrter SHA dokumentiert** (`365094890c091fbf627c9d71c94e44751018e6e9`, PR #4 CLOSED, Inhalt erhalten laut Release-Note und nc-3-Handoff). Die Karte verlangt explizit „Keep historical PR #4/source branches intact."
3. **Die „leere Reimplementierung" gerade verhindert**, indem nachgewiesen wurde: Draft#4 enthält **keine echte, in main fehlende Implementierung** (missing=0); die zwei Go-Differenzen sind ein **Zurückbau** (wieder `Stat` statt main's strikter `Lstat`), den main **nicht** übernommen hat. Also ist kein Reimplementieren nötig — und ein „Wiederbeleben" von Draft#4 würde **fail-closed-safety zurückbauen** (symlink-resilience). Das wäre eine aktive Schädigung, keine Wiederaufnahme.
4. **Gap-Map statt Reimplementation geliefert** — jede Datei → Status a/b/c → nc-Task → nächster Schritt. Das ist die geforderte „maschinenlesbare Tabelle + Kurzbewertung", keine Produktänderung.

## repo-rule compliance

- Mission: „NUR Analyse + Evidence, KEINE Produktänderungen" — eingehalten. `git status` des connector-Worktrees unverändert; keine Datei geschrieben im Produkt-Repo.
- CI-Regel Nacht (Mission Punkt 4): `.github/**` und workflows **nicht** geändert (nur gelesen, als Befund).
- AGENTS 4.5: keine `git add -A`, keine Änderung fremder Bäume; 4.6: kein gehosteter Run ausgelöst (nur lokaler `git`-Lesen).

## END (Handoff)

END_DONE w1-connector-reconcile: files=17 in_main=17 conflict=2 missing=0 revive=no — Draft#4 ist seit Baseline 572b81d ein ÄLTERES/Teile-entferntes Oberfeld-Hybrid von main (13 superseded docs/CI/receipt, 2 Go-Konflikte zugunsten main's strikter Lstat fail-closed); kein fehlende Implementierung → nicht reaktivieren, nur als Branch bewahren.
