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

## BF-11..BF-16 (neu): Fehlerpfade + Session-Haesigkeit (cut 5/6)

- BF-11 (Sicherheit, fail-closed): falscher issuer -> saubere Fehlermeldung "discover operator OIDC provider: ... no such host" (DNS). Datei: internal/operatorauth/login.go:48 (err wrap "discover operator OIDC provider"). Kein stack trace, keine Info-Leake.
- BF-12 (fail-closed): closed port (issuer https://127.0.0.1:9999) -> "dial tcp 127.0.0.1:9999: connect: connection refused"; whoami danach "session required". Recovery ohne state-cruft.
- BF-13 (fail-closed): SIGKILL mitten im PKCE-Flow (nach auth-URL, vor callback-redirect) hinterlaesst KEINE partial session file. Sessions-Direktorium nach Abbruch leer. Kein Halbfinished-Credential auf Disk.
- BF-14 (fail-closed): expired session (expires_at=2020, ansonsten gueltige Felder) -> whoami "session required". Cause: ValidAt() Require "ExpiresAt.After(now + 30s)" (30s grace). SaveSession refused invalid sessions (kann nicht manuell persistiert werden). Datei: internal/operatorauth/session.go:26 ValidAt, :75 SaveSession.
- BF-15 (fail-closed): tampered session issuer mismatch (https://tampered-issuer.test) -> "session required". VerifySession checks issuer==config.Issuer. Datei: internal/operatorauth/session.go:139.
- BF-16 (fail-closed): tampered session subject mismatch (attacker-superuser) -> "session required". VerifySession subject==session.Subject. Logout idempotent: ClearSession treats os.ErrNotExist as success ("Operator session removed" auch ohne Session); operator_auth.go:72.
- BF-17 (positiv): login per-target scoped. Login hx1 -> nur operator-hx1-stage.json; whoami hx2 -> "session required". Session-Name-Schema operator-<target>-<env>.json.

## BF-18..BF-20 (neu): env-fallback + config-mutation-scope (cut 6)

- BF-18 (Sicherheit/Usability): Mit KEINEM per-target operator-auth in config.yaml UND gesetzten env vars (BASEHARBOR_OPERATOR_OIDC_ISSUER/CLIENT_ID) laeuft der login bis zum exchange, schlägt aber am persist-Schritt fehl: "Target configuration mutation requires its protected owner directory". Cause: persistOperatorAuthBoundary -> config_mutation.go:72 ProtectedStateOwner(root) fail fuer /tmp (nicht owner-geschuetzt). Datei: internal/deployment/config_mutation.go:72; cmd/baha/operator_auth_boundary.go:158 persistOperatorAuthBoundary.
- BF-19 (positiv, praezision): whoami/observe verwendet resolveStoredOperatorAuthBoundary (config.yaml ONLY, KEIN env fallback) — BF-04 bestaetigt. ConfigFromEnv() fallback existiert nur in resolveOperatorAuthBoundaryConfig (login-pfad). Trennung klar: whoami liest nur config.yaml; login kann aus env bootstrappen, darf aber nur in protected owner dir persistieren.
- BF-20 (positiv): config mutation path validiert config (Validate) + .installation.lock owner-read, bevor persistiert wird. Defensiv.

## Positives

- POS-1: Full managed PKCE login works end-to-end (integrierter OIDC-Flow: discover -> callback listener -> code -> RS256 id_token -> persist). BF-09.
- POS-2: Fail-closed across ALL error paths (DNS, closed port, mid-flow kill, expiry, issuer-tamper, subject-tamper). Session validation robust.
- POS-3: logout clean + idempotent; no credential residue on failure.
- POS-4: Managed-identity enforcement returns a clear, non-auth-error message ("no claim-based tenant membership") AFTER successful OIDC verification — good separation of auth vs authorization.

## Trust prompts + per-anchor fail-closed (cut 4)

## BF-21..BF-27 (neu): trust uninstall prompts + per-anchor fail-closed (cut 4)

- BF-21: trust status lists anchors per-anchor as "PRESERVED <path> (<fp>; <backend>; missing; trusted=false)" when Core not installed / file missing. Status output is informational (read-only).
- BF-22: trust uninstall VALID backends are `linux-update-ca-certificates` and `linux-update-ca-trust` (hosttrust.go:458 backendByName). NOT "podman"/"docker"/"managed-keycloak".
- BF-23: uninstall --yes (no prompt) removes owned anchors; host-trust.json deleted after removal. Backend refresh (update-ca-certificates) runs per anchor.
- BF-24: uninstall prompt "[y/N]: " — non-TTY (piped) SKIPS prompt and errors "trust uninstall requires explicit approval" (readerIsTerminal false). Requires --yes for non-interactive.
- BF-25: prompt accepts y/yes/ja/j (incl. German ja/j); n/invalid("xyz")/empty-line(Enter) -> "Host trust unchanged.", anchors preserved. 
- BF-26 (FUND - prompt EOF): EOF (Ctrl-D, no newline) on uninstall prompt surfaces ERROR "read host trust removal approval: read /dev/stdin: input/output error" (ReadString('\\n') surfaces non-EOF... actually EOF error, not handled as decline). Fail-closed (anchors preserved) but erroring instead of clean "unchanged". Datei: cmd/baha/trust.go ~225 bufio.NewReader(guidedTrustInput).ReadString('\n') -> "read host trust removal approval: %w". Install-pfad (maybeOfferManagedHostTrust) HAT errors.Is(io.EOF) graceful handling; uninstall does NOT.
- BF-27 (Sicherheit, per-anchor fail-closed): wrong backend ("managed-keycloak") -> PRESERVED with error "unsupported recorded host trust backend", while valid anchors in same run ARE removed. host-trust.json retains only the preserved bogus anchor. Per-anchor isolation confirmed (hosttrust.go:241 "PRESERVED %s (%s): %w").

## VM-Besanrein

- Scope: reine CLI-Befundung (login/logout/whoami/trust). KEIN `baha up` ausgefuehrt -> KEINE neuen Docker-Container erzeugt. Bestehende gfield0427-Container (4h alt) unveraendert (nicht von dieser Lane).
- Isser (investigation tooling): root-owned python3 pid 1940252 auf 127.0.0.1:443 -- SELF-SIGNED TEST CA, nur fuer BF-09/11/12. Verbleibt als isolierter Test-Issuer; kein Produkt-Zertifikat.
- /tmp/hx1-mg (isolierter managed boundary: HOME + state dir) + /tmp/hx1-oidc (issuer) = Untersuchungswerkzeuge, nicht Produkt-Config.
- cleanliness: state/cache/sessions leer (alle Test-Sessions aufgeräumt); host-trust.json letzter Test-Zustand (nur preserved bogus anchor); kein Produkt-Workspace touch.

## Status

- VM-BESAINREIN: Isser (pid 1940252, root, 127.0.0.1:443) per sudo kill -9 beendet + PORT_443_FREE verifiziert. Tooling /tmp/hx1-mg + /tmp/hx1-oidc + hx1-pub-/hx1-tls-Temps + hx1_testkey.pem per sudo rm -rf aufgeraeumt (TMP_CLEAN). KEIN `baha up` -> KEINNeue Docker-Container (NO_HX1_CONTAINERS). Bestehende gfield0427-Runtime unveraendert.
- STATUS: FINAL — 27 Befunde + 4 Positives dokumentiert; Evidence origin/main (43855612); todos work/r27-node-cli (3c73e37d); VM besenrein; END in geteilte Inbox gepostet.
