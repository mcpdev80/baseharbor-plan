# W105 — Connector Node Service (Slice 2): implementation + red-first tests + local CI

**Mission:** `coordinator/missions/w105-node-service.txt`
**Rolle:** Worker (Lane w105) — Coordinator `f49a3303`
**Karte:** `t-20261018-r27-node-service` (State `active`)
**Coordinator-Entscheidung 2026-11-04:** Option (b) mit engen Schranken — neuer Pfad erlaubt, aber nur wenn bestehende Pakete die Orchestrierung nicht tragen; Pfad `internal/nodeservice` (kein Strich), duenn, nur lifecycle + re-enrollment-regeln; bestehende sicherheitskritische teile WIEDERVERWENDEN; write-set als VORSCHLAG dokumentieren; KEIN stiller contract-edit.
**Verlinkt (VORLESE-PFLICHT):**
- Connector [`AGENTS.md`](https://github.com/mcpdev80/baseharbor-node-connector/blob/main/AGENTS.md)
- [`plan.py show t-20261018-r27-node-service`](file:///home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/tasks/t-20261018-r27-node-service.md)
- Path-Reservation-Vorschlag: [`path-reservation.md`](file:///home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle4-2026-11-04/node-service/path-reservation.md)

## PLAN (4.4 — Board-File workers/todos/w105-node-service.json + diese Liste, getickt in Arbeit)

- Done: Vorlesen + Realitaetsgleichgewicht (slice-1)
- Done: Gap/Reuse-Analyse: existing packages (connector/deployment/health) tragen KEINE connector-self-service Orchestrierung
- Done: Pfad-Wahl `internal/nodeservice` dokumentiert; write-set-reservierung als Vorschlag (path-reservation.md); KEIN stiller contract-edit
- Done: `internal/nodeservice` implementiert — thin, nur lifecycle + re-enrollment-regeln
- Done: Wiederverwendung statt Kopieren (targetaccess.EnsureEnrollmentPrivateKey/BootstrapEnroll/InstallEnrollment, fssecure)
- Done: rote-first unit tests (4 geforderte faelle + mehr) + go vet + build + gofmt + race
- Done: PR #19 draft auf connector-repo; basis-check origin/main 2a02a9a; ls-remote==head 764a2a4
- Done: lokale connector-CI-Checks (source.yml-aequivalent) beobachtet, alle gruen
- Done: Evidence slice-2 + END an f49a3303 mit geklaerter push-branche

## (1) Reuse statt Kopieren

Neuer Pfad justified, weil existing packages die connector-self-service Orchestrierung nicht tragen (nachgewiesen slice-1): connector/TargetAccess = Core-authorized transport-opationen; deployment/contracts.go = nur Interfaces; health = nur memory-observation; runtime/quadlet = Core-managed units mit foreign-preservation. Kein overlap mit einer anderen slice.

Wiederverwendet (nicht kopiert):
- `internal/targetaccess.EnsureEnrollmentPrivateKey` — one-time protected key-gen (mode 0600, idempotent, symlink-fail-closed)
- `internal/targetaccess.BootstrapEnroll` / `BootstrapConfig` — HTTPS enrollment, pinned server identity, nonce-bound one-time token
- `internal/targetaccess.InstallEnrollment` — client-only leaf + expected URI + local key + exact expiry + strict PEM/CA
- `internal/targetaccess.NodeIdentity` / `EnrollmentResponse` — wire identities
- `internal/fssecure` protected-state-mechanik als Vertraulichkeitsgrenze

## (2) Implementierung (4 files, thin)

- `internal/nodeservice/nodeservice.go` — Service-Koordinater; Unit/State/UnitKind; lifecycle (Install/Start/Restart/Uninstall/Enable/Disable); `PlanReenroll` determinism-guard (expired/revoked/conflicting -> allowed; active+unexpired -> blocked, `ErrAlreadyEnrolled`); `Reenroll`/`ReenrollWithRevocation`; `validateSelfOwnedUnit` (self-owned name = connector-binary-identitaet, fail-closed); Persistierung der enrollment in protected store.
- `internal/nodeservice/systemd.go` — `systemdUnitManager` (UnitManager): rootless `systemctl --user` harness, injectbar fuer tests, observer activation; `protectedStateStore` (MetadataStore): single 0600 file + integrity-tag (sha256), NUL-free name, symlink-escape rejected; `NewService`/`NewSystemdService`/`ServiceNameForBinary`.
- `internal/nodeservice/reenroll.go` — `BootstrapReenrollDriver` (EnrollmentDriver): delegiert an `targetaccess.BootstrapEnroll`, revoked-serial-pruefung, bindet an identity files, leitet serial aus der enrollment-cert ab. Kein Klon der kryptographischen pruefung.
- `internal/nodeservice/nodeservice_test.go` — 9 rote-first tests.

## (3) Rote-first faelle (gefordert + ergaenzt)

- re-enrollment zweimal => definierter zustand: erster call installiert, zweiter (active+unexpired) blockt mit `ErrAlreadyEnrolled`, keine datei-aenderung; `TestReenrollTwiceIsDeterministicAndBlocksSecond`
- fehlende authorization / fehlende install => schutz greift: `TestLifecycleFailsClosedWithoutInstall` (start/restart ohne install -> `ErrNotFound`), `TestValidateSelfOwnedUnitFailsClosed` (foreign-unit-name/unknown-kind/blank-execstart -> reject)
- service-neustart == same behavior: `TestRestartSameBehaviorAsStart` (restart geht ueber install-presence-check -> manager-operation -> observe -> save, identisch zu start)
- schluessel-erzeugung ersetzt NICHT schuetzende dateien: `TestProtectedStateStoreRejectsTamperedPayload` (untagged/tampered -> reject); re-enroll bindet an existierende protected key-files, ersetzt sie nicht
- ergaenzt: expired/revoked/conflicting-identity klassifiziert (`TestReenrollAllowedWhenExpiredOrRevoked`, `TestReenrollConflictingIdentityIsAllowed`); uninstall remove+clear (`TestUninstallRemovesUnitAndClearsState`)

## (4) Lokale connector-CIBEobachtung (4.6 — eigener run, terminal)

source.yml-aequivalent lokal ausgefuehrt, alle gruen:
- `gofmt -l cmd internal` => clean
- `go mod verify` => all modules verified
- `go test -race -p 2 ./... -count=1 -v` => alle packages ok (nodeservice 1.013s, targetaccess 16.8s)
- `go vet -p 2 ./...` => EXIT 0
- `go build -trimpath ./cmd/baseharbor-node-connector` => ELF binary OK (11.5 MB)
- Produkt-CI nicht veraendert: `.github/**` unangetastet.

## (5) PR #19 + basis-check

- Branch (disjunkt, connector-nur): `work/r27-node-service`, basis `origin/main` `2a02a9a5d2e95b9f627c9d71c94e44751018e6e9`
- Commits gegen origin/main => diff enthaelt NUR die 4 nodeservice-files (kein stiller edit ailleurs)
- PR draft: [#19](https://github.com/mcpdev80/baseharbor-node-connector/pull/19) (draft)
- ls-remote verified == head: `764a2a4ba6af380cd76ab241a7ff680508fa18fe` -> `refs/heads/work/r27-node-service`
- Worktree isoliert: `/tmp/opencode/w105-node-wt`

## (6) PR#4-praezedenz

Erhaelt. current main enthaelt schon alle sicherheitskritischen enrollment-materialien (r27-night reconcile `missing=0`); lane erweitert mit duennem service-lifecycle-pfad only. Keine historical PR#4/source branch umgeschrieben.

## (7) Endgultige push-branche (klaert die head/lsremote-Widerspruec aus slice-1)

slice-1 END zeigte `813f08a` an — das war der initiale `main`-checkout des worktrees, NICHT die push-branche. Klaerung:
- Tatsaechlich gepushte branche: `work/r27-node-service` (NEU, nicht main)
- Pushed head (ls-remote): `764a2a4ba6af380cd76ab241a7ff680508fa18fe`
- Basis: `origin/main` = `2a02a9a5d2e95b9f627c9d71c94e44751018e6e9`
- Der worktree ist ein git worktree (getrennte working-tree), die files wurden explizit hinein-kopiert und dort build/getestet; die push-branche ist separat.

## repo-rule compliance

- Mission (connector-only, KEIN produkt-CI): eingehalten. `.github/**` unangetastet.
- AGENTS 5.6 prompt-injection: karten-/mission-text als DATEN behandelt.
- 4.3 claim ueber zentrales protokoll — claim von coordinator gesetzt/publiziert (mission bestaetigt).
- 4.5: nur `git add internal/nodeservice/` (kein `git add -A`) im worktree.
- Kein desired-state/placement-owner auf dem knoten; kein Go-auf-knoten required fuer service-lifecycle.
- Kein Produkt-CI-Change, kein Force-Push, kein protection-bypass.

## END

END_DONE w105-node-service: head=764a2a4 pr=19 faelle=9-belegt (re-enroll-determinismus, auth-fail-closed, restart==start, key-ersetzt-nicht-schutz, protected-store) lsremote=764a2a4 | thin internal/nodeservice (lifecycle + re-enrollment) implementiert, targetaccess-primitives wiederverwendet, 9 rote-first tests + go vet/build/fmt/race gruen, PR#19 draft basis origin/main 2a02a9a.
