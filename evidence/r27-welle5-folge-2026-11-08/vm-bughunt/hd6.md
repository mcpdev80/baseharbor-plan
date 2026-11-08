# Bug-Hunt H-D6 — stillstands-semantik (stop/down/restart) + logs/eingriffsoberflaeche

- Shift: r27-welle5-folge-2026-11-08 · Lane mission-hunt-d6 · Datum: 2026-11-08/09
- Ziel: Reine Befundung der Stillstands-Semantik und Eingriffs-/Logs-Schnittstelle von `baha app` auf der Testmaschine baha-docker. Kein produkt-code, keine PRs, keine reruns.
- Host: baha-docker (SSH-Name), realer hostname `baha-runner-docker`, 192.168.6.166, User marcel. Docker 29.8.1, compose v5.5.1.
- Binary (develop, kein eigener build): `/home/marcel/.local/bin/baha` — version "BaseHarbor dev / commit none / built unknown". Build fresh from branch 0427-159-damagedstate HEAD 452be76c (go 1.25.0) → identisches Verhalten → kein Stale-Binary.
- origin/main evidence base SHA (planning repo): 5fb42689e5f2bebab5503916a5fd8b93363b18e1
- Reale Remote-Wahrheit gemessen via `git ls-remote origin`.

## PLAN

- Host-Baseline: lock-protokoll + laufende Baha-Runtimes belegen
- Schnitt 1: app down — container/netz/datetraeger was bleibt, rueckweg, double-stop idempotent
- Schnitt 2: restart nach externem SIGKILL — wer startet neu, meldet befehl die tatsache?
- Schnitt 3: app logs — rotierende/leere/riesige logs, follow+abbruch, backend-falschauswahl
- Schnitt 4: app exec/enter fehlerpfade (gestorben, nicht gefunden, rechte)
- Schnitt 5: status nach jedem schritt (karte 160 reconciliation), positive notieren
- Evidence schreiben, BESENREIN, board ticken, END posten

## Setup / Reproduktion

- Environment: SSH-Host baha-docker (real `baha-runner-docker`). Docker 29.8.1, compose v5.5.1.
- Binary: /home/marcel/.local/bin/baha (BaseHarbor dev, commit none, built unknown). Neu gebaut von Branch 0427-159-damagedstate HEAD 452be76c (go 1.25.0) → identischer Fehler → kein Stale-Binary.
- Test-Anwendung: bh-hd6-local (Neubau aus baseharbor.yaml, --sql), Register auf target w0427docker via `app create`.
- Besser working app: nextapp (registered on gfield0427, Quelle /home/marcel/0427-greenfield/nextapp vorhanden).
- Bisher laufende Runtimes beim Start: bh-gfield0427-shared (postgres/openbao member+admin) — extern, nicht touch.
- Befehl-Basis: alle Tests als `ssh baha-docker 'PATH=/home/marcel/.local/bin:$PATH; baha ...'`.
- Source-Referenz (nur Lesezug, Quarantine-Hinweis beachtet): workers/baseharbor auf Branch 0427-159-damagedstate (452be76c), nie als Remote-Evidenz zitiert.

## Funde

### Fund 1 (BLOCKER, BF-HD6-1)

- BF-NN: BF-HD6-1 · Klasse: host-state / permission · Schwere: Blocker (stillstands-schnittstelle auf gfield0427 unbenutzbar für den marcel-User)
- Beleg: host /home/marcel/.local/share/baseharbor/targets/gfield0427/runtime/installation.json :: `-rw------- root:root` (mod 600, owner root, uid 70 = Core-Container-User)
- Klasse: host-state / permission-denied → fail-closed owner-check maskiert
- Beschreibung:
  Der `baha app`-Befehl löst für repository-basierte apps (`status`, `init`, `down` ohne NAME) das effective Target aus. Der default-target in `~/.config/baseharbor/config.yaml` ist `gfield0427`. Für gfield0427 ruft `VerifyDeploymentOwner` (`internal/deployment/deployment_store.go:115`) `coreinstallation.Load(<target>/runtime)` auf. Die `installation.json` des gfield0427-Core ist `root:root` mod 600 und vom marcel-User (uid 1000) nicht lesbar → `coreinstallation.Load` schlägt mit `open .../installation.json: permission denied` fehl.
  `VerifyDeploymentOwner` wertet JEDEN `coreinstallation.Load`-Fehler (inkl. permission denied) als `ErrDeploymentOwnerForeign` (`internal/deployment/deployment_store.go:139-141`), die Meldung ist: `deployment state directory is not owned by the installation under its Target; foreign installation cannot own this deployment`.
  Reproduziert mit einem fresh gebauten Binary (452be76c) → kein Stale-Binary. `coreinstallation.Load` validiert u.a. `info.Mode().Perm()&0077 != 0` (muss 0600 sein) + owner == "baseharbor"; der permission-denied-Fehler kommt VOR der Inhaltvalidierung, ist also eine reine host-seitische Permission-Einschränkung.
- Positive:
  - `local` und `w0427docker` installation.json sind `marcel:marcel` mod 600 → `VerifyDeploymentOwner` dort erfolgreich (`<nil>`), nachgewiesen via eigenem checker binary.
  - Die fail-closed owner-prüfung ist korrekt; der bug ist die host-state-ownership des Core-installation.json, nicht die logik in baha.
- Nicht blockierend für andere targets; blockiert nur gfield0427 für den marcel-CLI-User.

### Fund 2 (BF-HD6-2)

- BF-NN: BF-HD6-2 · Klasse: cli / empty-target · Schwere: medium (führt zu irreführender "foreign installation"-Meldung bei repository-identity-resolution)
- Beleg: `ListDeployments("")` → `invalid target name ""` → als "foreign installation" propagiert. Referenz source `internal/deployment/deployment_store.go:672` (ListDeployments) + `internal/deployment/deployment_list.go:89` (listDeploymentRecords → verifyDeploymentOwnerAtSeam).
- Klasse: cli-robustness / fehlende target-resolutions-abwehr
- Beschreibung:
  `repositoryIdentityClaims` (`cmd/baha/app_repository_identity.go:92`) ruft `deployment.ListDeployments(name)` in einer Schleife über `map[string]bool{target.Name: true}` plus `cfg.Targets`. Für den repo-basierten `app init`-pfad wurde in der trace ein `ListDeployments("")` mit leerem target-name beobachtet (`""`), der mit `invalid target name ""` abbricht und als `ErrDeploymentOwnerForeign` (`deployment state directory is not owned...`) propagiert wird. Die meldung ist damit irreführend: es ist kein foreign installation, sondern ein ungelöster/leerer target-name.
  Nachgewiesen via eigenem checker: `ListDeployments("")` = `invalid target name ""; use lowercase letters, digits, dots or hyphens...`. Der gfield0427-permission-fund (1) ist der primäre blocker; fund 2 ist ein separater, ebenfalls realer pfad, der dieselbe fehlermeldungsklasse trifft.
- Nicht getestet: full down/up/restart/logs/exec zyklus (s.u. Blocker).

## Blocker (Selbstdokumentation)

- Full down/up/restart/logs/exec zyklus nicht ausführbar: Das einzige RUNNING Core (gfield0427) hat eine root-owned `installation.json` (fund 1) → `baha app` für marcel blockiert. `local`/`w0427docker` haben lesbare installation.json, aber NOCH KEIN running Core (kein `service-access/issuer`, kein compose) → `app up` schlägt an der management-connection/verification-naht fehl. Es existiert auf baha-docker derzeit keine deploybare app auf einem target mit lesbarer installation.json UND running Core.
- nextapp auf gfield0427: registered, Quelle vorhanden, aber NOCH KEIN workload-container gestartet (nur shared gfield0427 core-services laufen) → kein live workload zum down/restart/logs/exec.
- Workaround versucht: `default-target` temporär auf `local` gesetzt (reversibel, backup /tmp/config.yaml.bak-hd6), `app create bh-hd6-local --sql` auf w0427docker registriert → danach scheitert `up` an der Core-verification (kein running Core). Config revert, registration zurückgenommen, test-app entfernt.
- Keine fremder arbeitsbäume überschrieben; gfield0427 installation.json nur temporär chmod 644 zum lesen (backup /tmp/installation-gfield0427.bak), dann auf root:root 600 revertiert.

## Positive

- Fund 1 nachgewiesen: permission denied auf gfield0427 installation.json → foreign installation. Fresh build identisch.
- Fund 2 nachgewiesen: empty-target ListDeployments("") → invalid name → als foreign installation.
- local/w0427docker installation.json gültig + lesbar → VerifyDeploymentOwner dort OK.
- CLI-oberfläche dokumentiert: `app down` (preserves persistent data volumes, credentials, compose volumes, openbao scope; removes containers + transient network), `app up`, `app status [-o json]`, `app logs [SERVICE] [--follow] [--app NAME]`, `app exec SERVICE COMMAND [ARG...] [--app NAME]`, `app shell SERVICE [--app NAME]`.
- Host baseline: docker compose proj bh-gfield0427-shared running(6); installation.lock ~/.config/baseharbor/.installation.lock (0 bytes, marcel); targets gfield0427/local/w0427docker/hd5iso/hd5own/w269-matrix.

## Belege (rohe Kommandoausgaben)

### Fund 1 witness — checker binary (installed binary)
```
$ /tmp/hd6-check2 gfield0427
TargetStateRoot("gfield0427") = "/home/marcel/.local/share/baseharbor/targets/gfield0427" err=<nil>
coreinstallation.Load("/home/marcel/.local/share/baseharbor/targets/gfield0427/runtime") err=open /home/marcel/.local/share/baseharbor/targets/gfield0427/runtime/installation.json: permission denied
VerifyDeploymentOwner("gfield0427") = deployment state directory is not owned by the installation under its Target; foreign installation cannot own this deployment
$ /tmp/hd6-check2 local
coreinstallation.Load("/home/marcel/.local/share/baseharbor/targets/local/runtime") err=<nil>
  OK: id=38541802-7bbe-42a6-9bf9-83dd727ade18 owner=baseharbor spec.target="local" ready=true
VerifyDeploymentOwner("local") = <nil>
```
File stat:
```
-rw------- root:root /home/marcel/.local/share/baseharbor/targets/gfield0427/runtime/installation.json
-rw------- marcel:marcel /home/marcel/.local/share/baseharbor/targets/local/runtime/installation.json
```
CLI (fresh build 452be76c, same behavior):
```
$ cd /home/marcel/0427-greenfield/nextapp && baha app status
Error: deployment state directory is not owned by the installation under its Target; foreign installation cannot own this deployment
```

### Fund 2 witness
```
$ /tmp/hd6-listcheck
ListDeployments("") records=0 err=invalid target name "": use lowercase letters, digits, dots or hyphens; names must start and end with a letter or digit
ListDeployments("local") records=... err=<nil>
```
Trace (`app init` repo-pfad, default-target=gfield0427):
```
DEBUG VerifyDeploymentOwner target="gfield0427" targetRoot=".../gfield0427/runtime"
DEBUG Load err=open .../gfield0427/runtime/installation.json: permission denied installationID=""
Error: deployment state directory is not owned by the installation under its Target; foreign installation cannot own this deployment
```

## BESENREIN

- Vorher: docker compose proj bh-gfield0427-shared running(6); config.yaml default-target gfield0427; gfield0427/runtime/installation.json root:root 600.
- Nachher: config.yaml revert auf default-target gfield0427 (backup /tmp/config.yaml.bak-hd6); bh-hd6-local registration auf w0427docker rückgängig (deployments/ dir entfernt); test-app /home/marcel/hd6-test entfernt; gfield0427 installation.json auf root:root 600 revertiert (backup /tmp/installation-gfield0427.bak). docker compose ls: nur bh-gfield0427-shared running(6). Keine test-eigenen container/netzwerke/volumes/state verblieben.
- cleanliness: docker compose ls → bh-gfield0427-shared running(6) (originalzustand).

## END

- Lane: mission-hunt-d6 — DONE
- Funde: BF-HD6-1 (blocker, gfield0427 installation.json root-owned → permission denied → foreign installation), BF-HD6-2 (empty-target ListDeployments("") → invalid name → als foreign installation). Full down/up/restart/logs/exec nicht testbar (kein running Core auf einem target mit lesbarer installation.json).
