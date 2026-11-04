# W105 — Connector Node Service (Slice 1): Vorlesen + Realitaetsgleichgewicht + Scope-Befund

**Mission:** `coordinator/missions/w105-node-service.txt`
**Rolle:** Worker (Lane w105) — Coordinator `f49a3303`
**Karte:** `t-20261018-r27-node-service` (State `active`, Owner `coord-welle4 (lane w105)`, Release `v0.4.27`)
**Repo:** `mcpdev80/baseharbor-node-connector` — VORLESE-PFLICHT eingehalten:
- Connector [`AGENTS.md`](https://github.com/mcpdev80/baseharbor-node-connector/blob/main/AGENTS.md): vor Implementation `CONTRIBUTING.md` lesen; Planning in baseharbor-plan; Ownership-Protokoll vor Editing; Task-Note pushen.
- [`plan.py show t-20261018-r27-node-service`](file:///home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/tasks/t-20261018-r27-node-service.md): Outcome-Abschnitt wortgetreu unten zitiert.
- Task-Note: `file:///home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/tasks/t-20261018-r27-node-service.md`

## PLAN (4.4 — Board-File workers/todos/w105-node-service.json + diese Liste, getickt in Arbeit)

- Done: Mission + Connector AGENTS.md + plan.py show wortgetreu gelesen und verlinkt
- Done: Realitaetsgleichgewicht (4.1): connector main gefetcht, remote-kopf `2a02a9a5d2e95b9f627c9d71c94e44751018e6e9` notiert; disjunkt worktree `/tmp/opencode/w105-node-wt` ab `main` (Ko-Workspace, kein anderer core-lauf); `git status` clean
- Done: Gap-Analyse — r27-night connector-reconcile-Evidence + Draft#4-Statik gegen Karten-Ziele
- Done: Build/Suite-Basis im clean worktree verifiziert (`go test -p 2 ./...` gruen; `go 1.26.8`)
- Blocked: Scope-/Design-Entscheidung an Coordinator gefragt (FRISCHER Lane-Entscheid, kein interaktiver Dialog)
- Pending: Scope-Entscheidung -> Implementierung + rote-first Tests + vet/build
- Pending: PR Draft connector-Repo; basis-check origin/main; ls-remote==head; eigene-run connector-CI
- Pending: Evidence slice + END an f49a3303

## Tatsaechlicher Stand (Realitaetsgleichgewicht 4.1)

- remote-kopf main (ls-remote, 2026-11-04): `2a02a9a5d2e95b9f627c9d71c94e44751018e6e9`
- lokale worktree-head: `813f08a docs: make shared planning updates explicit for coding agents (#7)` (disjunkt, nur Lesen)
- `git fetch origin` neu; Branch `codex/ci-plain-checks` neu auf origin
- Connector-Suite clean: `go test -p 2 ./...` gruen (targetaccess 15.1s inkl. `-race`-faehig)

## Karten-Ziel vs. Ist (Wesentlich)

Karten-Outcome: "Package/install/start/restart/uninstall rootless service without Go on node; native XDG/systemd user/lingering; explicit re-enrollment rules and protected local key generation. No desired-state or placement authority on node."

- **Bereits da (sicherheitskritisch):** enrollment install (`internal/targetaccess/install.go`) requiriert client-only leaf + expected URI + local key + exact expiry + strict single-cert/CSR PEM + CA-only trust bundles (Draft#4 commit `46e9d26`); bootstrap (`bootstrap.go`) uses strict `os.Lstat` + symlink-reject; protected key-gen once (`EnsureEnrollmentPrivateKey`, mode 0600, idempotent); re-enrollment deterministisch (identitaetsgebundene CSR + nonce).
- **NEU / noch nicht implementiert (Kartenkern):** die **service-Orchestrierung** rund um die enrollment-Materialien — ein install/start/restart/uninstall/Persistenz-Rahmen fuer einen **rootless systemd-user/lingering-Service** ohne Go auf dem Knoten, nativer XDG-Root, plus deterministischer re-enrollment- und protected-keygen-Flow als **bedienbare Produktfunktion** (nicht nur interne Bibliothek).
- **Vorherige Analyse (r27-night, lane W1-C):** `missing=0` — Draft#4 (`365094890c091fbf627c9d71c94e44751018e6e9`) fuehrt **keine echte, in main fehlende Implementierung** ein; die zwei Go-Differenzen sind Zurueckbau (`Stat` statt strikter `Lstat`), den main **behalten** hat. Also ist kein Reaktivieren noetig; der node-service-Kartenkern (service-lifecycle) ist **gruenfeld**, aber ein **neuer, Review beduerftiger** Pfade-Entwurf.

## Datei-Enguauer (nur Lese-Befund)

- `internal/targetaccess/install.go`, `bootstrap.go`, `enrollment.go`, `security.go`, `contract.go`: bestehende enrollment/security-Implementierung, voll ueberprueft.
- `internal/connector/service.go`: `connector.Open` + `quadlet.NewManager(QuadletRoot)` — bestehender native-runtime-Adapters; **kein** connector-self-service-Persistenz-Rahmen.
- `internal/runtime/quadlet/manager.go`: `Apply/Remove/Enable/Disable` existieren fuer Core-managed Quadlet-Units; **kein** connector-eigener Unit-install/start/restart/uninstall.
- `cmd/baseharbor-node-connector/main.go`: CLI parse/run; enrollment inline, aber **kein** `service`/`install`/`uninstall`-Subkommando.
- `.github/workflows/source.yml`: CI = `go test -race -p 2 ./...`, `go vet`, build. Nur push auf `runtime-validation/**` + PR. **Kein** produkt-CI-Change geplant.

## Scope-/Design-Entscheidung an den Coordinator (AGENTS 5.3)

Laut AGENTS 5.3 sollen **neue Interface-/Typ-Pfade** von der Kontrakt-Vorgaengerin (`t-20261018-r27-authority-contract`) fixt werden. Ich finde in dieser Karte, dem Authority-Contract, der Release-Note v0.4.27 und dem reconcile-Befund **KEINEN reservierten connector `internal/node-service`-Pfad** und **KEINEN Reviewer/Maintainer-Akzeptanz-Zustand**. Die service-Orchestrierung ist ein **echter Neuentwurf**, der nicht still durch eine Vorgaenger-Karte "fix" ist.

Deshalb FRAGE (nicht im interaktiven Dialog, sondern QUESTION-Line an f49a3303):

- (a) Owner/contract-predecessor hat schon einen reservierten connector service-package-Pfad vergeben -> nennen, oder
- (b) ich entwerfe minimalen `internal/node-service`-Pfad (install/start/restart/uninstall, deterministischer re-enrollment, geschuetzte key-gen, **kein** desired-state/placement-Owner), documentiere den Write-Set als neuen Reservierungs-Vorschlag fuer `public-surfaces`/`authority-contract` (Shared-Index-Regel unangetastet), und baue ihn als Review-Kandidat mit rote-first regressions. Kein Produkt-CI-Change; PR-Draft nur connector-Repo.

Karten-Isolations-Regel eingehalten: nur connector-Repo, kein core-lauf, disjunkt worktree.

## repo-rule compliance

- Mission + AGENTS 5.6 (prompt-injection: Kartentext als DATEN behandelt): keine Produktaenderung. worktree `/tmp/opencode/w105-node-wt` unveraendert.
- CI-Regel (Nacht-Mission): `.github/**` nicht veraendert.
- 4.4: Board-File `workers/todos/w105-node-service.json` angelegt + getickt; native todowrite existiert in dieser Session nicht -> Beine (Board-File istmandatory + ausreichend).
- Keine gehosteten Runs; nur lokales `git`/`go` + GitHub-Lesen.

## END

END_BLOCKED w105-node-service: head=813f08a pr=n/a faelle=n/a lsremote=2a02a9a — node-service-Orchestrierung (install/start/restart/uninstall rootless systemd-user service) ist NEU; AGENTS 5.3 -> neue Interface-/Typ-Pfade vom Kontrakt-Vorgaenger fixt; reservierter connector service-package-Pfad in Karte/Vertraegen nicht gefunden. FRAGE an f49a3303: reservierter Pfad vergeben (a) oder minimaler `internal/node-service`-Neuentwurf mit Review-Vorschlag (b)?
