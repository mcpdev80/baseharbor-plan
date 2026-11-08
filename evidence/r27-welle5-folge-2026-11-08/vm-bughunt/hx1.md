# H-X1 Bug-Hunt: Operator-Auth-Oberflaeche auf baha-docker

- Lane/Session: 635122aa-716a-4af9-99f7-91a634d9bf4c (whunt-pr-hx1, Ornith desktop)
- Shift: r27-welle5-folge-2026-11-08
- Mission: /tmp/opencode/mission-hunt-hx1.md
- Host unterucht: baha-docker (192.168.6.166, ssh-user marcel, hostname baha-runner-docker) — server host ist codeman, kein Test-Host
- Binary: ./baha-dev am Zielhost (dev build, commit bc8670c1dc6a2d7b5bf602ae7450f2e778a6f97a, built 2026-11-06T12:10:44Z); kein eigener build
- Scope: REINE BEFUNDUNG — kein produkt-code, keine PRs
- Ziel-Pfad Evidence: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx1.md

## PLAN (plain bullets; no markdown checkboxes)

- DONE 1 Host/Rahrendaten belegen (Server-vs-Test-Host, SSH, dev-Binary, Version)
- DONE 2 Auth-/Trust-/State-Architektur kartieren (config.yaml, developer-access, PKI, Sessions)
- DONE 3 login/logout-Zyklus: unauth Start OK; managed path braucht OIDC-Issuer -> lokaler Test-Issuer (self-signed CA + RS256 key) aufgebaut und in Trust-Store installiert; PKCE-Login gegen managed path
- IN ARBEIT 4 trust-prompts: neue CA hinzufuegen/widerrufen — Antworten y/n/invalid/EOF + Wirkung auf naechsten login
- TRAGEN 5 Fehlerpfade: falscher issuer, Reachability-Verlust (Port zu), Abbruch mitten im PKCE-Flow — Zustand in State-Dirs
- TRAGEN 6 mehrere Profile/Targets gemischt — login gilt wo? (Profil- vs Target- vs Umgebungs-Scope)
- TRAGEN 7 Positive Befunde notieren
- TRAGEN 8 VM-Besenrein (docker compose down, saubere Zeile)
- TRAGEN 9 Evidence committen (origin/main), END posten

## Fakten / Rahrendaten

- Server-Host (Session): codeman (7.0.0-42-generic). Nie Container/Tests hier laufen lassen.
- ssh baha-docker -> 192.168.6.166, user marcel, hostname baha-runner-docker; ssh config alias "baha-docker" mit IdentityFile ~/.ssh/mcp-home (direkte IP-Verbindung an 192.168.6.166 fehlgeschlagen, nur alias funktioniert)
- dev binary: /home/marcel/baha-dev, ELF x86-64, "BaseHarbor dev", commit bc8670c1...
- docker: Docker version 29.8.1
- config.yaml ConfigPath(): $BASEHARBOR_STATE_DIR/config/config.yaml (prioritaet), dann XDG_CONFIG_HOME/baseharbor/config.yaml, dann ~/.config/baseharbor/config.yaml
- DataRoot(): $BASEHARBOR_STATE_DIR (prioritaet); TargetStateRoot = <dataRoot>/targets/<name>
- session store: $BASEHARBOR_STATE_DIR/cache/sessions/operator-<target>-<env>.json (fallback: XDG_RUNTIME_DIR/baseharbor, dann os.UserCacheDir)
- ValidAt: braucht alle Felder + ExpiresAt.After(now + 30s); VerifySession: issuer/clientID must match config + OIDC sign verify + subject==session.Subject
- ManagedEnvironment: nur dev/development = trusted-local; alles andere = managed (OIDC required)
- Trust-Backends: nur podman/docker valid; anderes Backend -> PRESERVED + Fehler
- auth.json (Anmeldedatei) wurde NICHT gelesen/inhaltlich untersucht (Sicherheitsregel: nur als Metadatum dokumentiert)

## Befunde (BF-NN + Datei:#beleg + Klasse)

- BF-01: Full managed PKCE login flow works. `baha login -e stage` auf Target (external-oidc) schliesst ab: entdeckt OIDC config, startet ephemeral callback listener, empfang browser redirect mit code, exchange code for RS256 id_token. Session persistiert in cache/sessions/operator-<target>-stage.json. (investigation tooling: /tmp/hx1-oidc/issuer.py, config an target+env in config.yaml unter operator-auth)
- BF-02: Session validation confirmed — ValidAt() braucht alle Felder + ExpiresAt.After(now+30s); VerifySession() checks issuer/clientID match + OIDC sign verify + subject match. Datei: internal/identityprovider/*.go, internal/operatorauth/*.go
- BF-03: operator-auth config storage in config.yaml unter targets.<t>.operator-auth.<env>; fallback auf env vars BASEHARBOR_OPERATOR_OIDC_ISSUER/CLIENT_ID. Datei: internal/deployment/target.go:57 (OperatorAuth map), cmd/baha/operator_auth_boundary.go:57 (resolveOperatorAuthBoundaryConfig)
- BF-04: logout removes session via ClearSession(); whoami uses resolveStoredOperatorAuthBoundary (config.yaml only, no env fallback). Datei: cmd/baha/operator_operations.go:36, operator_auth_status.go:43
- BF-05: session expiry fail-closed — expired session file exists but whoami returns "session is required" (not authenticated)
- BF-06: trust uninstall prompt [y/N] accepts y/yes/ja/j; n/invalid -> "Host trust unchanged."; EOF hangs (ReadString blocks, only non-EOF errors)
- BF-07: trust uninstall per-anchor fail-closed ("PRESERVED <path> (<fp>): <err>"); wrong backend ("managed-keycloak") -> PRESERVED + error. Datei: internal/runtime/hosttrust/*.go
- BF-08: trust install prompt accepts y/yes/j/ja; non-TTY/--yes -> no prompt; needs --yes for host mutation. Datei: cmd/baha/operator_auth_boundary.go (promptYesNo)

## Positives

- (wird gefuellt waehrend der Arbeit)

## VM-Besanrein

- (wird gefuellt: compose down + ps-witness + cleanliness-zeile)

## BF-09 (neu): Full managed PKCE login flow works end-to-end (positiv)

- `baha login -e stage --target hx1` auf dem external-oidc managed target schliesst den vollen Flow ab: discovers OIDC config, startet ephemeral callback listener (127.0.0.1:0), erhaelt browser redirect mit authorization code, exchange code for RS256 id_token via /token, sign verify bestanden. Treibwerk: lokaler Test-Issuer /tmp/hx1-oidc/issuer.py (self-signed CA + RS256, browser_sim -> 302-redirect). Treiber: /tmp/hx1-mg/hx1-drive-login.py (liest auth URL aus Log, injiziert ?simulate=1).
- Session persistiert an /tmp/hx1-mg/state/cache/sessions/operator-hx1-stage.json (Felder: target, environment, issuer, subject, client_id, id_token (RS256 JWT), expires_at).
- whoami nach Login: session valid (issuer/clientID match, OIDC sign ok, subject==operator-hx1-user), ABER: "The verified operator carried no claim-based tenant membership that permits this machine operation." — dies ist MANAGED-IDENTITY-ENFORCEMENT (kein claim-based tenant-role im Test-issuers), NICHT ein Auth-Fehler. Der OIDC-Verifikationsteil ist erfolgreich; die Meldung kommt erst nach erfolgreicher Session-Verifikation. Klasse: expected behavior (fail-closed auf tenant membership), keine Regression.
- Config-Pfad korrekt: config an $BASEHARBOR_STATE_DIR/config/config.yaml unter targets.<t>.operator-auth.<env>: provider=external-oidc, issuer=https..., client-id (HYPHEN, nicht underscore). Runtime-Block runtime.provider=docker + access.reference erforderlich fuer gueltige Target-Definition.
- BF-10 (positiv, ergaenzt): session store location confirmed at $BASEHARBOR_STATE_DIR/cache/sessions/operator-<target>-<env>.json.

## Status

- STATUS: IN ARBEIT (BF-01..BF-10 documented; continuing error-path testing, cut 5)
