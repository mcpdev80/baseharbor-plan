---
id: t-20261120-perses-tmpfs-mountpoint
card_number: "0428-177"
card_short_title: "Perses runtime smoke cannot"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-083-
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-177 · Perses runtime smoke cannot
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-perses-tmpfs-mountpoint · Perses runtime smoke cannot mount tmpfs at /etc/perses/database on hosted runners #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** 0428-083-  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-083-  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.


## Ziel

Der gehostete Smoke-Gate `PR · Native · native/docker/perses-runtime-smoke` ist auf GitHub-Runnern rot, weil Docker den
Mountpoint fuer die tmpfs-Zielstelle `/etc/perses/database` im container-rootfs nicht anlegen kann. Die Karte behebt das
an der Produktstelle, die diese tmpfs-Anlage erzeugt - NICHT durch Wegnahme des Smoke-Gates.

## Befund (gemessen, nicht interpretiert)

Fehlertest: `TestPersesRuntimeSmokeDockerIsolated` (Datei `internal/application/perses_runtime_test.go`), Paket
`internal/application`, Laufzeit 11.51 s.

Fehlerzeile aus dem Job-Log (Lauf 44717007640, PR #1684, head 43d3a8dc0c6c, 2026-11-20T10:12:15Z):

```text
Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed:
runc create failed: unable to start container process: error during container init: error mounting "tmpfs" to rootfs at
"/etc/perses/database": create mountpoint for /etc/perses/database mount: make mountpoint "/etc/perses/database":
mkdirat /home/runner/.local/share/docker/...
```

Einordnung gegen die geschlossene Karte 0428-174: deren Fix betraf den Postgres-Pfad (uid70-Rueckfall nach `gosu`,
Datei `internal/runtime/...`/`runtime_multi_integration_test.go`) und ist gemergt (`dbe7fbc3905b`). Der hier beschriebene
Fehlschlag liegt an ANDERER STELLE und bleibt danach nachweislich rot (Lauf 44717007640 auf gerebasefter Spitze). Wer
diese Karte als "Duplikat von 174" schliesst, widerlegt sich selbst mit dem genannten Lauf.

Beteiligte Produktstellen (Stand develop `dbe7fbc3905b`, wo die tmpfs-Zeile entsteht):
- `internal/application/perses_runtime.go`
- `internal/serviceaccess/perses_compose_realization.go`
- `internal/serviceaccess/perses_config_render.go`

## Erwartung vs. Ist

Erwartet: der Smoke-Gate faehrt einen Perses-Container mit tmpfs unter `/etc/perses/database` auf einem Standard-Runner.
Ist: das Starten scheitert im container-init, das Verzeichnis des Mountpoints kann im rootfs nicht erzeugt werden.

## Leistung dieser Karte

1. Reproduce the failure locally on a Docker cell with the same storage driver setting, and record the command output.
2. Choose between the two candidate fixes and justify the choice against the contract: (a) ensure the mountpoint's parent
   exists in the image / create it before mount; (b) replace the tmpfs with a named volume or bind mount that carries the
   same isolation guarantee. Whichever is picked must keep the security property that motivated the tmpfs.
3. Add or extend a regression test that runs in GitHub CI and fails when the mount configuration is removed (§5.3, CI
   intake duty for new tests). Name the job that executes it.
4. Do NOT delete or skip the smoke gate, and do NOT touch `.github/**` (owner scope).

## Stop-Kriterium

Bleibt der Mount-Fehler auf dem Runner, obwohl die Produktstelle korrekt ist (storage-driver-bedingter Runner-Defekt),
dann ist das kein Produktbug: Karte auf `blocked` mit dem Lauf als Zeugen und klaerer Owner-Anfrage.

karte aus dem fehlgeschlagenen smoke-run 44717007640 (PR #1684) gegossen - fund->karten-pflicht, damit der beund nicht in einer lane-meldung verdampft. besetzt mit der lane, die ihn gefunden hat (sid 473e54be, '0428-083-', ornith 2/2), weil dort der kontext schon liegt; die umbenennung der lane folgt dem muster 'eine lane, zwei auftraege nur nacheinander' - ihr alter auftrag 0428-083 steht solange auf blocked. entscheidungsbedarf in der karte: elternverzeichnis vor dem mount anlegen ODER benanntes volume/bind mit gleicher isolation; sicherheitseigenschaft der tmpfs muss erhalten bleiben; regression muss in der CI rot werden, wenn die mount-konfiguration fehlt. STOPP-KRITERIUM: bleibt es ein runner-defekt, ist die karte kein produktfehler - dann koennte nur der owner einen anderen gate-ort freigeben
