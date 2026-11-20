# H-V14 bughunt: secret reveal paths (card t-20261120-r28-bughunt-secret-reveal-paths, 0428-171)

ROLLE: worker, reine BEFUNDUNG — kein commit am produkt-branch, kein PR, kein merge. Reine Befundung.

## PLAN

1. develop read-only klonen, develop HEAD messen.
2. Anchor-Dateien cmd/baha/app_access.go und cmd/baha/app_access_urls.go lesen.
3. Schnitt 1: human vs runtime reveal — zwei getrennte pfade, jeder pfad schreibt wohin (stdout/datei/log/registry), belegen mit file:line.
4. Schnitt 2: aufhebung — wird ein enthüllter wert aus zustand/protokollen entfernt oder bleibt er? schreiben/löschen zeilen.
5. Schnitt 3: zugriffs-prüfung — jeder reveal-pfad mit berechtigungsprüfung? fehlende prüfung = fund.
6. Schnitt 4: invalid-input — fail-closed oder stiller leerwert bei unvollständigen/ungültigen keys?
7. Sicherheits-Check auf auth/token-file am host (nur Metadatum).
8. Akte schreiben, checks, END posten.

## repo-rule compliance

- Rolle: reine Befundung. Kein produkt-branch geschrieben. Keine .github-Änderung. Kein PR, kein merge.
- Kein subagent eingesetzt.
- Entwicklung nur aus /tmp/x-h14-clone (read-only checkout von develop). Evidence nur in /tmp/x-h14-plan (planning repo, fetch+rebase origin/main).
- Kein container/netzwerk/volume als dauerhafter test-traeger gestartet.

## base attestation

Pruefbefehl: `git ls-remote origin refs/heads/develop`
Ergebnis: 36d075fad77fa61ac8c153e979855546589b32c2	refs/heads/develop

Read-only checkout auf develop HEAD 36d075fad77fa61ac8c153e979855546589b32c2 im Clone /tmp/x-h14-clone. Build/vet/293 unit-tests clean.

## schnitt 1: human vs runtime reveal — zwei getrennte pfade

Ergebnis: ZWEI GETRENNTE PFADE bestaetigt. Human-creds-pfad (stdout) und runtime-env-pfad (stdout) zeigen unterschiedliche bytes; urls-pfad zeigt nur public urls, keine secrets.

Pruefweg: Quelltext der beiden anchor-dateien cmd/baha/app_access.go und cmd/baha/app_access_urls.go auf develop HEAD 36d075fad77f, gelesen im read-only clone /tmp/x-h14-clone.

### 1a. Human `baha app creds ... --reveal` — stdout, nur postgres/valkey

- `cmd/baha/app_access.go`, Z. 96-137: `appCredsCommand`, Usage "baha app creds postgres|valkey [INSTANCE] [--app NAME] [--reveal]".
- `cmd/baha/app_access.go`, Z. 121-134: schreibt RESOURCE/INSTANCE/HOST/PORT/DATABASE/USERNAME immer auf stdout; PASSWORD/URI nur bei `reveal=true` (Z. 128-129), sonst `<masked>` (Z. 130-133). Ziel: `out` (stdout).
- `cmd/baha/app_access.go`, Z. 115-120: JSON-Format (`outputJSON`) REVEALTIET IMMER — Z. 116-118 gibt `usageError("JSON connection metadata never reveals credentials", ...)` zurueck. JSON ist also kein reveal-pfad.
- `cmd/baha/environment_operations.go`, Z. 42-53: `publicApplicationConnection` gibt nur Resource/Instance/Host/Port/Database/Username zurueck — Password und URI bewusst NICHT im DTO. Dies ist der nicht-revealierte stdout-pfad.
- `cmd/baha/app_access.go`, Z. 243-248: privileged identities (postgres/baseharbor_admin/root) werden fail-closed blockiert — Z. 246 `usageError("privileged database identities cannot be opened by the developer console", ...)`.

### 1b. Runtime `baha app env [--reveal]` — stdout, dotenv/shell/json/yaml

- `cmd/baha/app_env.go`, Z. 17-48: `appEnvCommand`, Usage "...[--reveal]".
- `cmd/baha/app_env.go`, Z. 106-114: `maskRuntimeSecrets` — bei `!reveal` werden alle nicht-oeffentlichen felder auf `<masked>` gesetzt. Z. 110-111: `if value != "" && !isPublicRuntimeEnvironmentField(key) { values[key] = "<masked>" }`.
- `cmd/baha/app_env.go`, Z. 116-130: `isPublicRuntimeEnvironmentField` — oeffentlich nur BASEHARBOR_APP_NAME/ENVIRONMENT/BINDINGS und `*_CA_FILE` (nur CA-Zertifikate, kein privater key). Private secret-keys (API_TOKEN etc.) werden maskiert.
- `cmd/baha/app_env.go`, Z. 132-159: `writeApplicationEnv` schreibt auf `out` (stdout) in dotenv/shell/json/yaml.
- Ziel stdout; maskierung default, `--reveal` schreibt die realen werte auf stdout.

### 1c. Runtime `baha app env --path` — owner-only dotenv-datei, kein stdout-reveal

- `cmd/baha/app_env.go`, Z. 40-42: bei `pathOnly` wird nur der absolute pfad auf stdout geschrieben, der fileinhalt wird NICHT ausgegeben.
- `cmd/baha/app_env.go`, Z. 73-77: `--path` + `--reveal` = usageError. Kein kombinierter reveal ueber --path.
- Der raw dotenv-inhalt (mit secrets) liegt nur auf der owner-only datei (`files.ApplicationEnv`); er wird nie ueber die cli ausgegeben. Direktes lesen der datei ist execution-host zugriff (siehe machine_coverage.go).

### 1d. URLs — publicApplicationAccessURLs — keine secrets

- `cmd/baha/app_access_urls.go`, Z. 33-58: `publicApplicationAccessURLs` gibt nur http/https public-routes aus (Z. 41-50: filterts Visibility=="public", gueltige published-port, http/https). Keine creds/uris.
- `cmd/baha/app_access_urls.go`, Z. 14-31: `applicationAccessURLs` ruft `exposure.Load` und publicApplicationAccessURLs; bei fehler nil. Ziel ist die url-liste, kein secret.

## schnitt 2: aufhebung — bleibt der enthuellter wert liegen?

Ergebnis: kein persistenter zustand, der den wert nach einem --reveal enthaelt.

- Die reveal-werte (password/uri/env-secret) werden nur im prozess-lauf in lokale variablen/bytes geschrieben und nie in zustand-dateien oder logs geschrieben.
- `cmd/baha/secret_operations.go`, Z. 52-56: `setApplicationSecret` ruft `defer zeroBytes(value)` — der raw secret-wert wird nach dem setzen nullget. Das ist der aufhebungs-mechanismus fuer input.
- `cmd/baha/app_access.go`, Z. 41-52 / 84-91: bei `sql`/`cache` wird password in eine child-process env geschrieben (`replaceProcessEnv`/`replaceEnvIn`) und an das untergeprogramm uebergeben; es wird nicht in zustand oder log geschrieben.
- `cmd/baha/app_env.go`, Z. 32-34: `maskRuntimeSecrets(values)` wird auf der kopie ausgefuehrt; das original dotenv bleibt unangetastet (owner-only datei), der prozess-halter gibt nur die maskierte kopie zurueck.
- Es gibt keine stelle, die einen enthuellten secret-wert in ein zustand- oder log-file rueckschreibt. Der pfad ist zustandslos; der einzige persistent ort der secret ist der openbao-backed secret-service (setApplicationSecret/Z.57) bzw. die owner-only dotenv.
- Nachweis "schreiben aber noech loeschen": es gibt KEINE zeile, die den reveal-wert in zustand/log schreibt. Der einzige write des secrets ist openbao (Z.57) bzw. dotenv-datei (Z.66-70 von ResolveServiceBinding, die binding wird einmal materialisiert und nicht durch --reveal erneut geschrieben).

## schnitt 3: zugriffs-pruefung — berechtigungsprobe per reveal-pfad

Ergebnis: jeder reveal-pfad laeuft durch `authorizeApplicationOperation` (=> authorizeMCPOperation), also mit berechtigungsprobe.

- `cmd/baha/app_access.go`, Z. 215-226: `resolveAccessBinding` ruft `authorizeApplicationOperation(ctx, "app.connection", resolved)` vor dem return des bindings (das password/uri enthaelt). Fehlende pruefung = fund — hier PRESENT.
- `cmd/baha/app_access.go`, Z. 96-137: `appCredsCommand` ruft `resolveAccessBinding` (Z.111), also autorisierter pfad.
- `cmd/baha/environment_operations.go`, Z. 17-20: `inspectApplicationEnvironment` ruft `authorizeApplicationOperation(ctx, "app.environment", resolved)` (Z.18) vor dem env-reveal.
- `cmd/baha/secret_operations.go`, Z. 18-20: `authorizeApplicationOperation` => `authorizeMCPOperation`.
- `cmd/baha/mcp.go`, Z. 267-316: `authorizeMCPOperation` — registered machine operation (Z.268-271), managed-environment auth (Z.282-305), `operatorauth.AuthorizeMachineOperation` (Z.306-314). Fail-closed bei fehlender autorisierung.
- `cmd/baha/app_secret.go`, Z. 44-74: `secret set` ruft `resolveSecretApplication` + `setApplicationSecret` mit `authorizeApplicationOperation(ctx, "secret.set", ...)`.
- `cmd/baha/machine_coverage.go`, Z. 221: dokumentiert, dass --reveal und das laden der protected dotenv datei execution-host credential access sind und als solche als mcp-exposure ausgeschlossen sind ("MCP exposes masked values only"). Dokumentations-stelle, kein offener pfad.
- Fund: KEIN. Kein reveal-pfad ohne berechtigungsprobe gefunden.

## schnitt 4: invalid-input — fail-closed oder stiller leerwert

Ergebnis: fail-closed durchgehend bei kritischen inputs.

- `cmd/baha/app_access.go`, Z. 334-368: `parseCredsArgs` — unvollstaendige args => usageError (Z.355-357); `redis` => alias valkey (Z.359-361); nicht postgres/valkey => usageError (Z.362-364). Kein stiller leerwert.
- `cmd/baha/app_access.go`, Z. 252-268: `selectAccessInstance` — keine instance => error (Z.254-255); unbekannte instance => error (Z.259-260); mehrere instance => error, keine wahl (Z.266-267). Fail-closed.
- `cmd/baha/internal/application/access.go`, Z. 27-38: `ResolveServiceBinding` — `instance == ""` => error (Z.33-34); `files.Bindings == ""` => error (Z.36-38). Fail-closed.
- `cmd/baha/internal/application/access.go`, Z. 58-88: `read` helper — required missing => error; `password`/`uri`/`certificates` required (Z.66,70,82). certificates leer => error (Z.86-88). Password/uri sind required: fehlt der wert, ist das ein fail-closed, kein stiller leerwert.
- `cmd/baha/app_env.go`, Z. 86-104: `loadApplicationEnv` — ungueltige zeile (kein `=` oder leerer key) => error (Z.98-100). Fail-closed.
- `cmd/baha/app_env.go`, Z. 73-77: `--path` + `--reveal` => usageError. Kein stiller leerwert.
- `cmd/baha/app_access.go`, Z. 35-40: `--app` ohne wert => usageError. Fail-closed.
- Fund: KEIN. Kein stiller leerwert bei invalid-input gefunden; kritische inputs fail-closed.

## security finding (metadata only)

FUND (§5.6): auf dem rechner fand sich eine anmelde-/token-datei. NUR METADATUM (inhalt NICHT gelesen/kopiert/verschoben/geloescht, rotation liegt beim owner). Ausdrucklich NICHTS vom inhalt: kein wort aus dem inhalt, kein teil eines werts, keine laenge des werts, kein 'gueltig aussehend'.

- path: /home/marcel/.codex/auth.json
- owner/user: marcel
- owner/group: marcel
- dateimodus: 600
- groesse: 4362 bytes
- mtime: 2026-11-18 09:14:31
- pruefbefehl: `stat -c 'name=%n owner=%U group=%G mode=%a size=%s mtime=%y' <path>`

Dieses metadatum wurde dem owner als QUESTION und in der END_DONE-meldung gemeldet. Inhalt nicht gelesen; falls doch, haette ein satz stehen muessen, dass dies geschah — hier: NICHT gelesen.

## findings

Keine produkt-schwache als fund bestaetigt. Alle vier schnitte ergeben VERHALTEN KORREKT:

- VIER SCHNITTE geprueft (human vs runtime reveal, aufhebung, zugriffs-pruefung, invalid-input).
- Anker cmd/baha/app_access.go und cmd/baha/app_access_urls.go gemessen; karte 0428-057 'separate human/runtime secret reveal' ist bestand (getrennte pfade bestaetigt).
- Alteannahme karte 0428-151 (invalid org environment key) als false positive geschlossen; schnitt 1b/4 neu geprueft ohne dieseannahme: maskierung + isPublicRuntimeEnvironmentField fail-closed, CA-only oeffentlich.
- Kein fund ohne quelltext-zeile. Kein reveal-pfad ohne berechtigungsprobe. Kein stiller leerwert bei invalid-input. Kein persistenter zustand mit enthuellter secret.

Einzigster weiterfuehrender befund: security-metadatum einer auth-file (siehe abschnitt 'security finding (metadata only)'), an owner gemeldet.

## cleanliness:

- Vorher: kein container/netzwerk/volume/compose dieses shifts gestartet.
- Nachher: kein container/netzwerk/volume/compose hinterlassen.
- ambient-core/bilder fremder karren: nicht angefasst.
- Clone /tmp/x-h14-clone (read-only, kein write am produkt-branch). Planning-clone /tmp/x-h14-plan. Evidence nur in /tmp/x-h14-plan.
