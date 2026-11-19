# Akte 0428-146 — lifecycle/consent-desk hunt (H-V7), baha-podman

ROLLE: hunt-worker (REINE BEFUNDUNG, KEIN PR, KEINE Produktänderung).
SCHNITT: H-V7 (BUG-HUNT.md rotation 2026-11-19).
ANCHER develop: 223cb97a9d652a4672257cabbadf12e2b41ed9cd (git rev-parse origin/develop, vor Beginn gemessen; aktueller develop HEAD 6e87ddcb, nur 1 Commit später; 223cb97a ist Ancestor von develop und von origin/main).
EVIDENCE-CLONE: /tmp/opencode/x-146h-prod (baseharbor, Branch x-146h-bughunt ab 223cb97a), /tmp/opencode/x-146h-clone (baseharbor-plan, x-146h-bughunt ab origin/main 8267721e). KEIN Write in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.

## PLAN

1. VM-Lock und Host-Zustand pruefen (erste Handlung)
2. Slice 1 (0428-067) ownership-safe remove — was bleibt nach Zwei-Besitz-Ebenen-Remove
3. Slice 2 (0428-051) target-defaults — Verhalten ohne ausdruecklichen Target bei Deployment-Ebenen
4. Slice 3 (0428-081) consent-aktualisierung — wirkt aktualisierter Consent auf registriertes Target?
5. Slice 4 (0428-049) rootless-zerlegung — welche Doku-Schritte sind ausführbar, wo bricht es

---

## VM-Lock und Host-Zustand

STATUS: VERHALTEN KORREKT / kein Blocker.
lockctl existiert auf baha-podman NICHT (nicht installiert); kein VM-Lock durch tote Session gehalten — kein blockierender Inhaber, kein Ownership-Transfer nötig.
Live bh-podman-demo-* Stack lauft seit ~18:35 (Besitzer marcel); foreign bh-local-shared-*/perses-Objekte vorhanden — UNANGETASTET.
Werkzeug auf VM: expect=/usr/bin/expect, podman=/usr/bin/podman, docker-CLI nicht im PATH (nur podman).

BEFEHL (von MIR gemessen):
```
$ ssh baha-podman 'uname -a; command -v expect; command -v podman; command -v docker'
Linux baha-runner-podman 7.0.0-42-generic ... x86_64
/usr/bin/expect
/usr/bin/podman
(no output -> docker CLI nicht installliert)
```
VORAB-LISTE (docker/podman ps -a, netze, volumes):
```
$ podman ps -a  -> 16 laufende bh-podman-demo-* Container (openbao, postgres, haproxy, keycloak, caddy, prometheus, demo-app, metrics-demo, dev-gateway)
$ podman network ls -> 9 baseharbor-* netze (baseharbor-podman-demo-default, baseharbor-identity-core-podman-demo, ...)
$ podman volume ls -> 2 volumes: bh-podman-demo-shared_postgres-data-1, baseharbor-prometheus-data-podman-demo
```
CLEANLINESS: am Ende der Mission freigebebe VM-Lock (lockctl nicht vorhanden -> nichts freizugeben); keine eigenen Container/netze/volumes erstellt.foreign Objekte unangetastet.

---

## Slice 1 (0428-067) ownership-safe remove — Zwei-Besitz-Ebenen

VERHALTEN KORREKT (Szenario A: Shared-Instanz bleibt bei noch bestehendem Sibling-Binding):
Vollständiger lifecycle-destroy verwendet ReleaseApplicationProviderRegistryAt -> releaseDeployment -> removeUnboundOwnedInstances. Nach Remove bleibt NUR die Shared tier-2 Instanz (gebunden durch Sibling) zurueck; die app-eigene tier-1 Instanz wird gelöscht.
BEFEHL (Reproduktionstest, clean checkout):
```
$ go test ./internal/application/ -run TestX146OwnershipSafeRemoveTwoTierTarget -v
  AFTER full remove: instances=1 bindings=1
  instance id="sql/shared" scope=shared ownerApp=""
  binding app=... env="dev" inst="sql/shared"
  PASS
```
DATEI: internal/application/x146_ownership_two_tiers_test.go

BEFUND (Szenario B: Shared tier-2 Instanz ohne jeden Restbesitzer leakt als Doku-/Registry-Eintrag):
removeUnboundOwnedInstances (internal/capability/registry.go:381-384) behält ScopeShared-Instanzen IMMER (switch-case ScopeShared: continue), auch wenn keine Binding mehr existiert. Nur ScopeApplication-Instanzen werden bei Owner-Match behalten/entsprechend geprüft. Eine Shared-Instanz, die nach dem letzten Consumer niemand mehr bindet, wird NICHT aus dem Provider-Registry gelöscht — Registrierung/Consent-Eintrag verbleibt hängend.
BEFEHL (Reproduktionstest):
```
$ go test ./internal/application/ -run TestX146OwnershipSafeRemoveOrphanedSharedInstance -v
  AFTER remove of sole consumer: instances=1 bindings=0
  instance id="sql/shared" scope=shared
  BEFUND: orphaned shared instance "sql/shared" left dangling after sole consumer removed
  FAIL
```
DATEI: internal/capability/registry.go:381-384 (switch ScopeShared: continue)
FUND-TITEL: "Ungebundene Shared-Provider-Instanz nach letztem Consumer nicht aus Registry gelöscht (Registry-/Consent-Leak)"
FUND-DETAIL: removeUnboundOwnedInstances filtert BaseHarbor-owned Instanzen, behält aber ScopeShared implizit für immer — keine pruefung, ob noch eine Binding existiert.

---

## Slice 2 (0428-051) target-defaults — Verhalten ohne ausdruecklichen Target

VERHALTEN KORREKT:
Core ResolveTarget (internal/deployment/target.go:419-456) priorisiert explicit > activated > DefaultTarget > sole-target > "local". Die CLI-Ebene bahaEffectiveBootTargetName (cmd/baha/deployment_record.go:339-355) fuegt BASEHARBOR_TARGET env VOR persisted VOR DefaultTarget.
BEFEHL (Reproduktionstest):
```
$ go test ./cmd/baha/ -run TestX146TargetDefaultsPrecedenceNoExplicit -v
  core ResolveTarget baseline resolved="managed" provider="podman" (env NOT honoured by core resolver)
  effective-boot with env=local: got "local"
  PASS
```
DATEI: cmd/baha/x146_target_defaults_test.go
ANMERKUNG (kein Befund, dokumentiertes Verhalten): BASEHARBOR_TARGET wird im CORE-Resolver ResolveTarget NICHT ausgewertet — erst die CLI-Schicht bahaEffectiveBootTargetName holt die env-Variable. Kein Datenfehler; die Prioritaetskette verläuft über zwei Ebenen.

---

## Slice 3 (0428-081) consent-aktualisierung — wirkt aktualisierter Consent auf registriertes Target?

VERHALTEN KORREKT:
ValidateProviderChangeConsent (internal/application/provider_change_consent.go:52-77) validiert consent.PlanID ZWINGEND gegen den PlanID des aktuellen registtierten Plans (validateProviderConsent:67). Ein aktualisierter Consent, dessen PlanID nicht dem aktuellen Plan entspricht, wird als stale-impact-consent zurückgewiesen; ein Consent mit passender PlanID gilt.
BEFEHL (Reproduktionstest):
```
$ go test ./internal/application/ -run TestX146UpdatedConsentRequiresCurrentPlanId -v
  current-plan consent validated OK
  stale-plan consent rejected as expected
  PASS
```
DATEI: internal/application/provider_change_consent.go:66-77 (stale-impact-consent); RecordProviderChangeResult (internal/application/provider_change_result.go:83-84) fordert同样的 aktuelle PlanID.

---

## Slice 4 (0428-049) rootless-zerlegung — welche Doku-Schritte sind ausführbar, wo bricht es?

BEFUND: Die rootless-Doku (docs/cli/targets.md:188) verlangt für die geleitete Reparatur Ubuntu/Debian + user systemd + docked-rootless-setuptool.sh + min. 65536 subordinate UID/GID-Mappings in /etc/subuid & /etc/subgid. Auf baha-podman:
- OS: Ubuntu 26.04.1 LTS — ERFOELLBAR
- user systemd session: systemd --user is-system-running = degraded (läuft, aber degraded)
- docked-rootless-setuptool.sh: MISSING (nicht installiert) — BRICHT AN DIESER STELLE
- rootlesskit: MISSING
- /etc/subuid: marcel:100000:65536 (exakt 65536 — GRUNDGRENZE ERFÜLLT, aber keine Reserve); /etc/subgid analog
- docker CLI auf VM nicht installiert -> `docker rootless`-Pruefung nicht ausführbar

BEFEHL (von MIR gemessen):
```
$ ssh baha-podman 'cat /etc/os-release | grep NAME; systemctl --user is-system-running; command -v dockd-rootless-setuptool.sh; ls -la /usr/bin/*rootless* 2>/dev/null; command -v rootlesskit; grep -c "^marcel:" /etc/subuid; awk -F: "{print \$3}" /etc/subuid'
NAME="Ubuntu" VERSION="26.04.1 LTS"
degraded
MISSING
(no /usr/bin/*rootless* files)
(rootlesskit MISSING)
1
65536
```
DATEI: docs/cli/targets.md:188 (Anforderung); cmd/baha/rootless_bootstrap.go (Implementierung)
BEFUND-TITEL: "Rootless setup tool docked-rootless-setuptool.sh auf baha-podman nicht installiert — geleitete rootless-Reparatur nach docs/cli/targets.md:188 bricht an dieser Stelle ab; rootlesskit ebenfalls MISSING; docker CLI nicht im PATH"
BEFUND-DETAIL: subuid/subgid-Mappings existieren (65536, Grundgrenze erfüllt), user-systemd lauft (degraded), aber das Setup-Tool fehlt — die Doku-Step-Installation ist auf dieser VM nicht ausführbar.
