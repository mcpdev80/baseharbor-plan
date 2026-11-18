# BUG-HUNT 915 — Befund: `baha app env` erwähnt Recovery-Fahnen, die die Command selbst ablehnt

Lane: hunt-cli2merged. Mission: /var/tmp/missions/mission-hunt-cli2merged.md.
Datum: 2026-11-18. Reine Befundung, keine Produktänderungen, kein .github/**, keine Container.

## PLAN

- Objekt: baseharbor develop, Objekt SHA 907f16713 (gemergte cli2-flaeche, PR #1681). develop HEAD ist weitergezogen auf aadee4520; 907f16713 ist echter Ancestor von develop, nur aadee4520 folgt.
- Worktree + Binary build von exakt 907f16713 (detached), getestet in /tmp/hunt-probe
- Schnitt (a): Exit-Codes + stdout/stderr-Trennung und JSON-Schema-Treue der app/env-Familie gegen die reale binary
- Schnitt (b): Silent-Failure-Audit der CLI2-Command-Wiring (verschluckte Fehler, toter Flag-Pfad)
- Befund-Datei in baseharbor-plan, push auf origin/main, Sauberkeit, END

## Basis-Attestation

- Plan-Repo-Verifikation (wrong-zone check): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
- Produkt-Basis: `git ls-remote origin refs/heads/develop` → `aadee4520ce5c01cf614662d078c05d684f44233 refs/heads/develop`; Worktree/Build exakt auf `907f16713cbf38693d30c9dadaad7fe299759219` (detached).
- 907f16713 ist echter Ancestor von develop: `git merge-base --is-ancestor 907f16713 origin/develop` → true; der einzige Nachfolger auf develop ist `aadee452 fix: drop phantom prometheus workload logs`.
- Kein Produkt-Branch, kein PR: Hunt ist reine Befundung; das einzige Artifact ist diese Datei in baseharbor-plan.
- Beweismittel-Logik: alle CLI-Zeugen stammen aus `./baha …` (built from 907f16713) in `/tmp/hunt-empty`, einem leeren Testverzeichnis. Dieses Host-Verzeichnis (coordinator/codeman server) hat keinen container runtime Zugang; runtime-pflichtige Beispiele brechen dort ab — das ist Umgebung, kein Produktbefund.

## Befund B1 (mittel, CLI-Vertrag) — `baha app env` recovery-Flags `--uuid`/`-e/--environment` sind tot; read-Commands brauchen `--uuid` Positional-NAME

### Aussage

Die gemeinsame Resolver-Hilfe in `cmd/baha/app_context.go` (Resolution-Helfer, Fehler `machine.ErrorOwnershipAmbiguous`, `application_name_ambiguous`) weist bei mehreren Deployment-Fällen für denselben App-Namen eine Recovery an:

> `Select one deployment by uuid: baha app <command> --uuid <deployment-id>, or by a distinct environment with -e/--environment.`

Diese Fahnen werden generisch über `<command>` eingefügt und gelten formal für **jede** `baha app <command>`-Resolution über `resolveApplication`. Für `baha app env` ist die vorgeschlagene Recovery nicht ausführbar: `app env` akzeptiert weder `--uuid` noch `-e`/`--environment` in seinem eigenen Parser `parseAppEnvArgs` (`cmd/baha/app_env.go:50-83`, `case strings.HasPrefix(arg, "-")` → `usageError("unknown option "+arg, …)`). Die von der binary selbst vorgeschlagene Recovery ist für `app env` damit nicht ausführbar.

Zusätzlich: Der `--uuid`-Selector erfordert für die read-Commands (`app show`/`app status`) einen Positional-`NAME` — `baha app status --uuid <id>` ohne NAME löst nicht, sondern meldet `no application deployment could be resolved` (repo-los). Der dokumentierte Weg `baha app <cmd> NAME --uuid <id>` (docs/cli/applications.md:233) ist nur mit NAME lauffähig; für `app env` ist er tot, weil die Command den `--uuid`/`-e`-Flag im Parser ablehnt.

### Beweis im Quelltext

- `cmd/baha/app_env.go:21` Usage: `baha app env [NAME] [--format dotenv|shell|json|yaml] [--reveal] [--path]` — kein `--uuid`, keine `-e/--environment`.
- `cmd/baha/app_env.go:50-83` `parseAppEnvArgs`: Der einzige `strings.HasPrefix(arg, "-")`-Fall wirft `unknown option`; es gibt keine `--uuid`-/`-e`-Ablösung.
- `cmd/baha/app_context.go:495` generischer `Next:`-Text mit `--uuid`/`-e/--environment` für **alle** über `resolveApplication` laufenden Commands.
- Gegenvergleich: `cmd/baha/app_lifecycle.go:444-446` (`baha app destroy`) und `cmd/baha/app_context.go:143-145` (`extractApplicationUUID`) verarbeiten `--uuid` korrekt; `app show`/`app status`/`app plan` laufen über `parseReadOutputArgs` (`cmd/baha/output.go:17`) + gemeinsamen Resolver und akzeptieren `--uuid`, aber nur mit Positional-`NAME`.
- Test deckt nur den direkten Resolver: `cmd/baha/app_context_duplicate_name_test.go:107` prüft `--uuid` auf `resolveRegisteredApplication`, **nicht** auf `parseAppEnvArgs`. Der Test umgeht also gerade den Parser, der die Fahnen ablehnt.

### Reproduktion (reale binary, registrierter Poison-Target)

Umgebung: `cd /tmp/hunt-empty` (kein `baseharbor.yaml`). `baha app list` zeigt `perses-cli` mit 6 kollidierenden Deployments auf `p427-podman-boot`.

```
$ baha app env perses-cli
Error
  application "perses-cli" has multiple registered deployments on target "p427-podman-boot":
    dev: 0c768991-4d1b-4aaa-ab17-20f8c9685cc6, 0d5d3994-..., ...
Resolution: operator_review
Next: Select one deployment by uuid: baha app env --uuid <deployment-id>, or by a distinct environment with -e/--environment.

# Vorschlage der binary befolgen:
$ baha app env perses-cli --uuid 0c768991-4d1b-4aaa-ab17-20f8c9685cc6
Error: unknown option --uuid
Next:
  Run 'baha app env --help' for available options.
  Did you mean '--quiet'?
  rc=2

$ baha app env perses-cli -e dev
Error: unknown option -e
Next:
  Run 'baha app env --help' for available options.
  Did you mean '-h'?
  rc=2
```

Gegenprobe: `baha app status --uuid <id>` ohne NAME löst im repo-losen Kontext nicht (`no application deployment could be resolved`), erst mit Positional-`NAME` (`baha app status NAME --uuid`) greift der Selector.

### Schwere / Auswirkung

Mittel. Der Nutzer erhält eine maschinengenerierte Recovery-Fahne, der die Command selbst widerspricht. Auf einem Target mit Duplicate-Records (`application_name_ambiguous`, ADR 0017 `(application_id, environment)` Pair als Systemidentität) ist `app env` blockiert, obwohl andere read-Commands (`app show`/`status`/`plan`) mit Positional-`NAME` + `--uuid` weiterlaufen. Die Doku `docs/cli/applications.md:237` bestätigt den `--uuid`-Weg ausdrücklich ("Commands addressed by --uuid keep working"), deckt sich aber nicht mit `app env`.

## Zusammenfassung

- B1: `baha app env` wirft `--uuid`/`-e/--environment` als Recovery-Vorschlag, lehnt sie im eigenen Parser ab — toter Flag-Pfad. `cmd/baha/app_context.go:495` + `cmd/baha/app_env.go:50-83`. read-Commands (`status/show`) brauchen `--uuid` als Positional-`NAME` (`baha app <cmd> NAME --uuid`), repo-los ohne NAME nicht lauffähig.
- Kein weiterer Silent-Failure im geprüften Schnitt: JSON-Error-Envelopes (`{contract_version:v1, error:{code,message,next}}`) sind schema-konform gegen `contracts/machine/v1/control.schema.json`, Exit-Codes konsistent (rc=2 bei Usage-Fehlern), `--json`/`--format json`/`-o json` für status/show/plan/env/version一致 (rc=2, envelope auf stderr).
- `app list`, `app creds`, `app versions` besitzen kein JSON-Schema; die CLI-Maschinenabdeckung `docs/reference/cli-machine-coverage.md` listet nur `app env` als JSON-fähig. Konsistent, kein Befund.

Jeder Befund braucht eine Bug-Karte (Fund→Karte-Pflicht); die Kartennummern setzt der Coordinator, diese Akte bleibt der Evidence-Ort.

## Sauberkeit

- Start `docker ps`/`podman ps`: keine Container gestartet (R1, keine Container).
- Ende `docker ps`/`podman ps`: keine eigenen Container/netzwerke/volumes/state-verzeichnisse hinterlegt.
- cleanliness: clean. Alle Artefekte liegen unter /tmp (hunt-probe, hunt-empty, /tmp/baha-hunt915, /tmp/repro-env.txt); nichts im Ökosystem-Wurzelverzeichnis.
- Build-Artefakt `/tmp/baha-hunt915` (56 MB) wird mit END aus /tmp entfernt.

## END

END_DONE hunt-cli2merged — Befund B1 (app env toter --uuid/-e-Fahnen-Pfad; read-commands --uuid nur mit Positional-NAME). Objekt 907f16713, binary build von diesem SHA. Reine Befundung, kein Produkt-Change.
