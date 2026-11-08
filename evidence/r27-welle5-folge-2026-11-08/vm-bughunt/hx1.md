# H-X1 Bug-Hunt: Operator-Auth-Oberflaeche auf baha-docker

- Lane/Session: 594fd2f5-4e80-43b6-9841-92879146a85e (worker, Ornith, server host codeman)
- Shift: r27-welle5-folge-2026-11-08
- Mission: /tmp/opencode/mission-hunt-hx1.md
- Host unterucht: baha-docker (192.168.6.166, ssh-user marcel, hostname baha-runner-docker) — server host ist codeman, kein Test-Host
- Binary: ./baha-dev am Zielhost (dev build, commit bc8670c1dc6a2d7b5bf602ae7450f2e778a6f97a, built 2026-11-06T12:10:44Z); kein eigener build
- Scope: REINE BEFUNDUNG — kein produkt-code, keine PRs
- Ziel-Pfad Evidence: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx1.md

## PLAN (plain bullets; no markdown checkboxes)

- DONE 1 Host/Rahrendaten belegen (Server-vs-Test-Host, SSH, dev-Binary, Version)
- DONE 2 Auth-/Trust-/State-Architektur kartieren (config.yaml, developer-access, PKI, Sessions)
- IN ARBEIT 3 login/logout-Zyklus: unauth Start OK (dev=trusted-local); managed path braucht OIDC-Issuer -> lokaler Test-Issuer (sel sign CA + signing key) wird aufgebaut; Token-Ablauf erzwungen (Config-Manipulation am Test-Target); Login mit/ohne --no-browser; Meldungen; wer ist eingeloggt (Profil/Target/Umg)
- TRAGEN 4 trust-prompts: neue CA hinzufuegen/widerrufen — Antworten y/n/invalid/EOF + Wirkung auf naechsten login
- TRAGEN 5 Fehlerpfade: falscher issuer, Reachability-Verlust (Port zu), Abbruch mitten im PKCE-Flow — Zustand in State-Dirs
- TRAGEN 6 mehrere Profile/Targets gemischt — login gilt wo? (Profil- vs Target- vs Umgebungs-Scope)
- TRAGEN 7 Positive Befunde notieren
- TRAGEN 8 VM-Besenrein (docker compose down, saubere Zeile)
- TRAGEN 9 Evidence committen (origin/main), END posten

## Fakten / Rahrendaten

- Server-Host (Session): codeman (7.0.0-42-generic). Nie Container/Tests hier laufen lassen.
- ssh baha-docker -> 192.168.6.166, user marcel, hostname baha-runner-docker; BatchMode ok, Timeout ~30s
- dev binary: /home/marcel/baha-dev, ELF x86-64, "BaseHarbor dev", commit bc8670c1...
- docker: Docker version 29.8.1
- config.yaml: default-target=gfield0427; Profile: hd5access(ssh), local(local), ssh(ssh); Targets: gfield0427(docker rootless, access=local), hd5iso, hd5own, local, w269-matrix, w0427docker
- existierendes Runtime-Target: gfield0427 (bh-gfield0427-shared), compose unter ~/.local/share/baseharbor/targets/gfield0427/runtime/compose.yaml
- PKI/Trust: ~/.local/share/baseharbor/targets/<target>/developer-access/dev/gateway/pki/{ca.pem,server-cert.pem,state.json}; host trust ~/.config/baseharbor/config.yaml
- operator-auth config: gespeichert an target+env in config.yaml unter operator-auth: (aktuell LEER); sonst fallback auf env vars BASEHARBOR_OPERATOR_OIDC_ISSUER/CLIENT_ID/SCOPES/CALLBACK_PORT
- session store: $BASEHARBOR_STATE_DIR/cache/sessions/operator-<target>-<env>.json (fallback: XDG_RUNTIME_DIR/baseharbor, dann os.UserCacheDir)
- ValidAt: braucht alle Felder + ExpiresAt.After(now + 30s); VerifySession: issuer/clientID must match config + OIDC sign verify + subject==session.Subject
- ManagedEnvironment: nur dev/development = trusted-local; alles andere = managed (OIDC required)

## Befunde (BF-NN + Datei:#beleg + Klasse)

- (wird gefuellt waehrend der Arbeit)

## Positives

- (wird gefuellt)

## VM-Besenrein

- (wird gefuellt: compose down + ps-witness + cleanliness-zeile)

## Status

- STATUS: IN ARBEIT
