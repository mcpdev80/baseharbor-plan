# Akte w388-0428-216-blobcensus — card 0428-275 — Catalog row-delta listing (scripts/pr-gate-coverage.json)

**Lane:** w388-0428-216-blobcensus (Folgeauftrag; session registers as w388-0428-329-1861recipe)  **Karte:** 0428-275  **Repo:** baseharbor (read-only)
**ART:** Row-delta listing for the catalog-only group from my own blob census. Read-only; Akte als DATEI (plan freeze 2026-11-27T07:34:31Z); kein push, kein merge, keine Zeile geschrieben.

## PLAN

1. Belege 5 verschiedene `scripts/pr-gate-coverage.json` blobs je PR + merge-base (#1860, #1863, #1869, #1855, develop) — DONE (plus #1650 anomaly).
2. Pro blob: `git diff <merge-base> <head> -- scripts/pr-gate-coverage.json`, nummerierte HINZUGEFÜGTE Zeilen (id/path/surfaces/runtime_specific) — DONE.
3. Kreuzung mit catalog-row-demand-v1.md und codex-disposition-136.md: fehlend auf develop / identisch zu develop-Zeile / Widerspruch zur Codex-Entscheidung — DONE.
4. Je PR: ENTFERNE Zeile X / HALTE Zeile X als Liste an Codex, keine eigene Änderung — DONE.
5. Akte als Datei, 4-Feld, END mit pfad + sha256 — DONE.
6. END post — DONE.

## 4-Feld

- Lane: w388-0428-216-blobcensus
- Karte: 0428-275 (row-delta listing über die catalog-only-Gruppe des Zensus)
- Repo/PR: baseharbor; #1860 `057ce8c55`, #1863 `0eafa9f5a`, #1869 `467913b72`, #1855 `d18e4b367`, #1650 `37c4d847c`; develop `ea5218d72`
- Status: END_DONE (Akte nur als Datei, plan freeze eingehalten)

## Basis / Remote guard

First git action `git remote -v` (baseharbor): `origin https://github.com/mcpdev80/baseharbor.git`, `lane-origin https://github.com/mcpdev80/baseharbor.git` (beide github.com/mcpdev80). ls-remote-Witness live: develop `ea5218d72e263f21e79853b679af50074dab8c25`, heads `refs/pull/{1855,1860,1863,1869}/head` equal the census heads (no change since the census). Cross-repo plan evidence read from the planning checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (`origin https://github.com/mcpdev80/baseharbor-plan.git`) — read-only, nothing written there (freeze).

## (a) Die 5 verschiedenen catalog-blobs

| # | Ref | Blob (40-hex) | merge-base zu develop |
|---|---|---|---|
| D | develop `ea5218d72` | `792a767aaceb600f5f0da228264413333014d1a8` | (basis) |
| 1 | #1860 `057ce8c55` | `77db3a1d3fefa3938e6fb005eca3684bce9377e5` | `ea5218d72` (identisch D) |
| 2 | #1863 `0eafa9f5a` | `3b704b7fbd905260ae45f30140f42f4df7589622` | `ea5218d72` (identisch D) |
| 3 | #1869 `467913b72` | `a26dcc1a87a937c69eea41529c9fb9f93e9b0db7` | `5a37ddbd9` |
| 4 | #1855 `d18e4b367` | `205c26dfb22f77758c52bc18bf25bfdaa6a6e768` | `c167fa5dd` (blob dort = `792a767a`, = D) |

Zusatzbefund #1650 `37c4d847c`: blob `5eab592e63238bd4f5cb5737501f7831fc195852` ≠ alle fünf; merge-base `ac7c970fe` (blob dort `68ad2b45`). Der diff mb→head enthält KEINE Zeilenänderung, nur `-}`/`+}` = missing-final-newline. #1650 schreibt also faktisch keine Katalogzeile; die Zensus-Notiz „carries candidate-side catalog row" ist zu korrigieren: die Zeile kam bereits über gemergte Vorfahren in die Kette (`2c4073189d` rebase-drop recovery), der Delta ist EOL-only.

## (b) Hinzugefügte Zeilen je blob (`git diff <merge-base> <head> -- scripts/pr-gate-coverage.json`)

Head-seitige Zeilennummern (gemessen `git show <head>:scripts/pr-gate-coverage.json | grep -n`): #1860 R1 at :2720; #1863 R2 at :2536, R3 at :2544; #1869 R4 at :2071 (R5 direkt danach).

**Blob 1 — #1860 (numstat +9/−0):**
- R1: `{"id": "source.internal_applicationbackup_recovery_manifest_workload_test_go", "path": "internal/applicationbackup/recovery_manifest_workload_test.go", surfaces: [source.gate.atomic.docker.data.capabilities, source.gate.atomic.podman.data.capabilities], "runtime_specific": true}`

**Blob 2 — #1863 (numstat +16/−0):**
- R2: `{"id": "source.internal_stableid_lock_probe_go", "path": "internal/stableid/lock_probe.go", surfaces: [docker.data.capabilities, podman.data.capabilities]}` — **ohne** `runtime_specific`
- R3: `{"id": "source.internal_stableid_lock_probe_platform_test_go", "path": "internal/stableid/lock_probe_platform_test.go", surfaces: [docker.data.capabilities, podman.data.capabilities]}` — **ohne** `runtime_specific`

**Blob 3 — #1869 (numstat +25/−135):**
- R4: `{"id": "source.internal.deployment.damaged.state.skip.test", "path": "internal/deployment/damaged_namespace_test.go", surfaces: [source.gate.atomic.docker.lifecycle, source.gate.atomic.podman.lifecycle]}` — keine `runtime_specific`
- R5: `{"id": "source.internal.deployment.damaged.state.network.skip.test", "path": "internal/deployment/damaged_namespace_network_test.go", surfaces: [docker.lifecycle, podman.lifecycle]}` — keine `runtime_specific`
- Nebenbefund: −135 Zeilen gelöschter develop-Zeilen. Das ist der im w379/#1862-Kontext bekannte „revert catalog"-Effekt eines stale hop-base (`5a37ddbd9`), keine bewusste Produktänderung dieser Karte — BUT it must not survive any hop: #1869's blob deletes trusted develop rows.

**Blob 4 — #1855 (numstat +1/−1):**
- KEINE hinzugefügte Zeile. Einziger Unterschied zu D: trailing newline fehlt (`-}` → `+}\ No newline at end of file`).

**Blob D — develop:** Referenz; enthält keine der Zeilen R1–R5 (grep: recovery_manifest_workload_test 0 hits, stableid lock_probe 0 hits, damaged_namespace 0 hits; nur `source.internal.deployment.damaged.state.go` existiert für damaged_state.go).

## (c) Kreuzung mit catalog-row-demand-v1.md (w387) und codex-disposition-136.md (w255)

| Zeile | Status auf develop | gegen demand-v1 | gegen Codex-Disposition |
|---|---|---|---|
| R1 (#1860) | FEHLT (0 hits) | Group A #1 + Group B #7: genau dieses candidate-only-Muster, `runtime_specific: true` gefordert und vorhanden | Group B: „candidate-only, no self-justification"; Disposition: auf #1860 head NUR R1 entfernen (`:2720-2728`), Landung via develop baseline PR |
| R2/R3 (#1863) | FEHLEN | Group B #8/#9 benennt exakt diese rows + fehlendes `runtime_specific: true` als Gap | Disposition: von #1863 head entfernen (`:2536-2542`, `:2544-2550`); die baseline Version MUSS `runtime_specific: true` tragen — die Kandidaten-Zeilen widersprechen also zusätzlich der Formular-Forderung |
| R4/R5 (#1869) | FEHLEN | Group D #11: andere Fehlerklasse (release-label), surfaces `.lifecycle` statt `.data.capabilities`, ohne runtime_specific | Disposition: candidate-only, nicht Teil der 0428-359 family; #1869-Problem ist das `pr-gate-map-v1.json` release label (`v0.4.27`), Owner-Aktion — kein baseline row demand. Zusätzlich: der −135-Löschanteil verstößt gegen die Regel, develop-Zeilen unverändert zu lassen |
| (none, #1855) | n/a | — | Konform mit „no candidate-side rows": der blob ändert nur EOL; Zeilen der #1855-Linie (perses_cli_test, identity_dashboard_witness) sind bereits auf develop (via #1781/#1847) |
| (none, #1650) | n/a | — | EOL-only; kein Selbstberechtigungs-Delta |
| #1861-Familie | FEHLEN (alle drei paths 0 hits) | Group A #2/#3/#4: die drei repository-volume-inventory/preserve-test Zeilen, inkl. `cmd/baha/app_destroy_volumes_recovery_backup_test.go` | Disposition zählt 8 rows; #1861 hat selbst KEINE candidate catalog delta (blob = D) → korrekt, aber die develop-rows sind noch offen |
| permission_scope row | EXISTIERT auf develop `:2736-2741` | Group C #10: Feld-Fix `runtime_specific: true` fehlt | Disposition: field-only correction, keine duplicate row |

Widerspruch gegen „keine kandidatenseitige Selbstberechtigung": R1, R2, R3, R4, R5 sind per Definition kandidatenseitig (existieren nur auf heads) und dürfen nicht als Zulassungsnachweis zitiert werden — R1 wie von der Disposition vorgesehen entfernen; R2/R3 zusätzlich fehlerhaft im Format (fehlendes runtime_specific); der #1869-Löschanteil (−135) ist der schwerste Verstoß, weil er trusted rows löscht statt sie nur zu ergänzen.

## (d) Liste an Codex (Vorschlag, keine eigene Aktion)

- **#1860:** ENTFERNE R1 (Zeile `source.internal_applicationbackup_recovery_manifest_workload_test_go` auf head `057ce8c55`, `scripts/pr-gate-coverage.json` ~:2720-2728). HALTE nichts — product/test payload unverändert behalten. Row kommt über develop baseline (#136 family).
- **#1863:** ENTFERNE R2 und R3 (blöcke ~:2536-2542 und :2544-2550 auf head `0eafa9f5a`). HALTE nichts. Baseline-Version mit `runtime_specific: true` via develop PR.
- **#1869:** ENTFERNE R4, R5 UND restauriere die 135 gelöschten develop-Zeilen (d. h. der Hop auf aktuellen develop muss `scripts/pr-gate-coverage.json` auf develop-Blob `792a767a` zurücksetzen). Release-label-Frage (`pr-gate-map-v1.json` v0.4.27) bleibt Owner-Aktion, nicht Karteninhalt.
- **#1855:** HALTE den Zustand (keine row); optionaler Kosmetik-Hop bringt den blob auf exakt develop (`792a767a`) — beseitigt den missing-final-newline und macht den blob diff-frei.
- **#1650:** keine catalog-Aktion (EOL-only); content-superseded-Entscheidung bleibt bei #1855 (Zensus d.3).
- **#1861:** keine candidate row zu entfernen (blob = develop); seine drei develop-rows sind Teil derselben baseline-Lieferung (Group A #2/#3/#4).
- **develop baseline PR (0428-359 family):** alle 8 rows (R1-Format für #1860, korrigierte R2/R3 mit runtime_specific, die drei #1861 rows, zwei #1862 compose rows, #1860 recovery row bereits gelistet) + Feld-Fix `runtime_specific: true` an develop `:2736-2741` (permission_scope) — als EINE catalog-only PR, damit danach kein PR-Head mehr eigene rows trägt.

## cleanliness

- Read-only census follow-up: keine containers/compose, keine builds/tests, keine pushes, keine plan-writes (freeze), keine Kartenfelder, keine views. Refs: eigene `refs/w388c/*` (fetch-only).

## END

`END_DONE w388-0428-216-blobcensus` — row-delta listing complete; 5 blobs + #1650-Anomalie (EOL-only, Zensus-Nebenzählung korrigiert); 5 candidate-added rows R1–R5 nummeriert und gegen demand-v1/Codex-Disposition gekreuzt; ENTFERNE/HALTE-Liste an Codex übergeben; keine Produktzeile geschrieben, kein push. Candidate SHAs unchanged (read-only census). Akte file: workers/evidence/w388-0428-275-rowdiff/akte.md (sha256 im END-Post).
