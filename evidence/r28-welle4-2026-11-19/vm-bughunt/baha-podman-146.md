# Akte 0428-146 — lifecycle/consent-desk hunt (H-V7), baha-podman

## Superseding correction: 0428-151 was a false positive (2026-11-20)

The original Slice 1 observation (`instances=1, bindings=0` after removing the sole consumer) was accurate. Its interpretation as a leak was wrong under the current provider-ownership contract. This correction supersedes the original Slice 1 classification and the resulting card acceptance criteria. Product develop was audited at `d5c11753ea437495eb2469a02f80b91d788fef4f`.

A `ScopeShared` provider with `OwnershipBaseHarbor` is target/platform-owned inventory. Application bindings represent consumers. Removing the final consumer leaves an unused provider, not an ownerless provider; ownership-verified cleanup remains explicit. `ReleaseApplicationProviderRegistryAt` intentionally copies all `ScopeShared` instances, releases only the selected application/environment bindings, and registers those shared instances again. The source comment in `internal/application/provider_registry.go` states that removed capability instances retain their ownership and releasing a binding does not reclaim a provider. The user-facing lifecycle calls unused provider resources `[RETAINED]` and says reclamation needs explicit ownership-verified cleanup.

The original reading of `removeUnboundOwnedInstances` inverted the slice behavior: that function starts a new slice (`instances := r.Instances[:0]`); for an unreferenced BaseHarbor-owned shared instance, `case ScopeShared: continue` skips the append and therefore omits the entry. The overall app-release path preserves the inventory because its caller snapshots and restores shared instances.

Current exact source and existing regression evidence (pinned to the audited develop SHA):

- [provider_registry.go contract comment](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L49-L51)
- [shared snapshot/release/restore path](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L270-L289)
- [last-consumer removal followed by app destroy retains zero-binding inventory and reports it unused](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_core_requirement_test.go#L192-L212)
- [multi-environment retirement keeps shared ownership and sibling binding](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry_test.go#L347-L375)
- [zero-binding shared OpenBao control-plane root survives app release](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/runtime_openbao_registry_test.go#L39-L52)
- [unbound Shared branch omits rather than appends the instance](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/capability/registry.go#L366-L389)
- [unused resources are presented as retained pending explicit ownership-verified cleanup](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_metrics.go#L149-L156)

Disposition: close 0428-151 as accepted false positive; do not change product code or the ownership contract. The existing tests were inspected, not rerun; this is a planning/evidence correction only.

---


ROLLE: hunt-worker (REINE BEFUNDUNG, KEIN PR, KEINE Produktänderung).
SCHNITT: H-V7 (BUG-HUNT.md rotation 2026-11-19).
ANCHER develop: 223cb97a9d652a4672257cabbadf12e2b41ed9cd (git rev-parse origin/develop, vor Beginn gemessen; aktueller develop HEAD 6e87ddcb, nur 1 Commit später; 223cb97a ist Ancestor von develop und von origin/main).
EVIDENCE-CLONE: /tmp/opencode/x-146h-prod (baseharbor, Branch x-146h-bughunt ab 223cb97a), /tmp/opencode/x-146h-clone (baseharbor-plan, x-146h-bughunt ab origin/main 9fae8f7b).
PRODUKTBUILD: `go build ./...` auf develop @ 223cb97a = CLEAN.

## PLAN

1. VM-Lock und Host-Zustand pruefen (erste Handlung)
2. Slice 1 (0428-067) ownership-safe remove — bleibt was nach Zwei-Besitz-Ebenen-Remove?
3. Slice 2 (0428-051) target-defaults — Verhalten ohne ausdruecklichen Target bei Deployment-Ebenen
4. Slice 3 (0428-081) consent-aktualisierung — wirkt aktualisierter Consent auf registriertes Target?
5. Slice 4 (0428-049) rootless-zerlegung — welche Doku-Schritte sind ausführbar, wo bricht es

---

## VM-Lock und Host-Zustand

VERHALTEN KORREKT / kein Blocker.
lockctl existiert auf baha-podman NICHT (nicht installiert); kein VM-Lock durch tote Session gehalten — kein blockierender Inhaber, kein Ownership-Transfer nötig.
Live bh-podman-demo-* Stack lauft (~18:35, Besitzer marcel); foreign bh-local-shared-*/perses-Objekte vorhanden — UNANGETASTET.
Wzeug VM: expect=/usr/bin/expect, podman=/usr/bin/podman, docker-CLI nicht im PATH (nur podman).

BEFEHL (von MIR gemesen):
```
$ ssh baha-podman 'uname -a; command -v expect; command -v podman; command -v docker'
Linux baha-runner-podman 7.0.0-42-generic ... x86_64
/usr/bin/expect
/usr/bin/podman
(no output -> docker CLI nicht installiert)
```
VORAB-LISTE (podman ps -a, netze, volumes):
```
$ podman ps -a -> 16 laufende bh-podman-demo-* Container (openbao, postgres, haproxy, keycloak, caddy, prometheus, demo-app, metrics-demo, dev-gateway)
$ podman network ls -> 9+ baseharbor-* netze
$ podman volume ls -> 2 volumes: bh-podman-demo-shared_postgres-data-1, baseharbor-prometheus-data-podman-demo
```
VM-LOCK FREIGEGEBEN: lockctl NICHT vorhanden -> nichts freizugeben; VM nicht durch Session gelockt. Freigabe in dieser Akte bestaetigt.

---

## Slice 1 (0428-067) ownership-safe remove — two ownership tiers

VERHALTEN KORREKT. A shared tier-2 provider remains when a sibling application still binds it; the app-owned tier-1 provider is removed with its owner.

The original scenario B reported `instances=1, bindings=0` after removing the sole consumer and destroying the app. That output is correct, but the original "dangling registry/consent leak" label is a false positive: the remaining `ScopeShared` + `OwnershipBaseHarbor` instance is target-owned provider inventory, retained by contract. Zero application bindings means it is unused, not unowned. The destroy path deliberately snapshots shared inventory around app-binding release, and existing tests assert this behavior, including the shared control-plane OpenBao root.

The original source-level explanation was also incorrect. In `removeUnboundOwnedInstances`, an unreferenced BaseHarbor-owned shared instance reaches `case ScopeShared: continue` while the function is building a new instance slice. `continue` omits that instance from the result slice; it does not preserve it. `ReleaseApplicationProviderRegistryAt` is the layer that deliberately restores shared inventory after releasing the selected app's bindings.

Current source/test evidence at develop `d5c11753ea437495eb2469a02f80b91d788fef4f`:
- [shared provider retention contract and implementation](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L49-L51) · [release path](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry.go#L270-L289)
- [direct zero-binding lifecycle regression and unused-footprint assertion](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_core_requirement_test.go#L192-L212)
- [multi-environment/sibling binding regression](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/application/provider_registry_test.go#L347-L375)
- [unbound Shared control flow](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/internal/capability/registry.go#L366-L389) · [explicit retained-resource cleanup rule](https://github.com/mcpdev80/baseharbor/blob/d5c11753ea437495eb2469a02f80b91d788fef4f/cmd/baha/app_metrics.go#L149-L156)

The `x146` test output above remains historical evidence of the observed registry state; it does not establish a defect. Card 0428-151 is closed as accepted false positive. No product code or tests were changed, and no test was rerun for this planning disposition.

FUND-TITEL KORRIGIERT: Shared-Provider-Inventar bleibt nach letztem Consumer absichtlich erhalten; keine Registry-/Consent-Leak.

---

## Slice 2 (0428-051) target-defaults — Verhalten ohne ausdruecklichen Target

VERHALTEN KORREKT:
Core ResolveTarget (internal/deployment/target.go:419-456) priorisiert explicit > activated > DefaultTarget > sole-target > "local". CLI-Schicht bahaEffectiveBootTargetName (cmd/baha/deployment_record.go:339-355) fuegt BASEHARBOR_TARGET env VOR persisted VOR DefaultTarget.
```
$ go test ./cmd/baha/ -run TestX146TargetDefaultsPrecedenceNoExplicit -v
  core ResolveTarget baseline resolved="managed" provider="podman" (env NOT honoured by core resolver)
  effective-boot with env=local: got "local"
  PASS
```
DATEI: cmd/baha/x146_target_defaults_test.go
ANMERKUNG (kein Befund, dokumentiertes 2-Ebenen-Verhalten): BASEHARBOR_TARGET wird im CORE-Resolver ResolveTarget NICHT ausgewertet — erst die CLI-Schicht holt die env-Variable. Prioritaetskette verlauft über zwei Ebenen; kein Datenfehler.

---

## Slice 3 (0428-081) consent-aktualisierung — wirkt aktualisierter Consent auf registriertes Target?

VERHALTEN KORREKT:
ValidateProviderChangeConsent (internal/application/provider_change_consent.go:52-77) validiert consent.PlanID ZWINGEND gegen den PlanID des aktuellen registtierten Plans (validateProviderConsent:67). Aktualisierter Consent mit passender PlanID gilt; PlanID die nicht dem aktuellen Plan entspricht -> stale-impact-consent.
```
$ go test ./internal/application/ -run TestX146UpdatedConsentRequiresCurrentPlanId -v
  current-plan consent validated OK
  stale-plan consent rejected as expected
  PASS
```
DATEI: internal/application/provider_change_consent.go:66-77 (stale-impact-consent); RecordProviderChangeResult (internal/application/provider_change_result.go:83-84) fordert gleiche aktuelle PlanID.

---

## Slice 4 (0428-049) rootless-zerlegung — welche Doku-Schritte sind ausführbar, wo bricht es?

BEFUND: rootless-Doku (docs/cli/targets.md:188) verlangt für geleitete Reparatur Ubuntu/Debian + user systemd + docked-rootless-setuptool.sh + min. 65536 subordinate UID/GID-Mappings in /etc/subuid & /etc/subgid. Auf baha-podman:
- OS Ubuntu 26.04.1 LTS — ERFULLBAR
- user systemd: systemctl --user is-system-running = degraded (laeft, degraded)
- docked-rootless-setuptool.sh — MISSING (nicht installiert) — BRICHT AN DIESER STELLE
- rootlesskit — MISSING
- /etc/subuid: marcel:100000:65536 (exakt 65536 = Grundgrenze Erfuellt, keine Reserve); /etc/subgid analog
- docker CLI auf VM nicht installiert -> `docker rootless`-Pruefung nicht ausfuehrbar
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
FUND-TITEL: Rootless setup tool docked-rootless-setuptool.sh auf baha-podman nicht installiert — geleitete rootless-Reparatur nach docs/cli/targets.md:188 bricht an dieser Stelle ab; rootlesskit ebenfalls MISSING, docker CLI nicht im PATH.
FUND-DETAIL: subuid/subgid-Mappings existieren (65536, Grundgrenze Erfuellt), user-systemd laeft (degraded), aber das Setup-Tool fehlt -> Doku-Step-Installation auf dieser VM nicht ausfuehrbar.

---

## STOP / Meldefrist (2026-11-19 ~21:3x +0100)

Echte Kartenarbeit auf diesem Kanal erschienen (zwei blockierende Befunde an #1690, beide vom Owner im Code nachgemesen). Hunt-Lane wird mit Meldefrist gestoppt (§3.3#5).
- Ausgefuehrt: alle vier Slices, je eine Zeile oben (VERHALTEN KORREKT / BEFUND mit Befehl, Ausgabe, Datei:Zeile).
- Nicht ausgefuehrt (Stop mit Meldefrist 2026-11-19): keine weiteren Szenarien mehr.
- CLEANLINESS: vorher = 16 bh-podman-demo-* Container (openbao/postgres/haproxy/keycloak/caddy/prometheus/demo-app/metrics-demo/dev-gateway), 9 baseharbor-* netze (baseharbor-podman-demo-default, baseharbor-identity-core-podman-demo, ...), 2 volumes (bh-podman-demo-shared_postgres-data-1, baseharbor-prometheus-data-podman-demo); nachher = identisch, KEINE eigenen Container/netze/volumes erstellt. Fremde bh-local-shared-* sowie perses-probe/proto-perses/deny-perses-Objekte NICHT angefasst (nur gemeldet, vorhanden unveraendert). subuid/unveraendert (marcel:100000:65536).

## VM-LOCK (Block — nachtraglich, 2026-11-19 ~21:5x +0100)

BEFUND: VM-Lock auf baha-podman haelt weiter unter mission-hunt-146 (seit 17:18:46Z). Im Journal fuer baha-podman KEIN release (nur baha-docker wurde 17:48:48Z freigegeben).
lockctl existiert NICHT auf any erreichbarem Host (baha-podman, baha-docker, baha-k3s, baha-podman-2, baha-docker-2: `command -v lockctl` -> not found; nur /usr/bin/flock praesent). Der Lock-Manager + mission-hunt-146-Zustand liegt AUSSERHALB der erreichbaren VMs (coordinator/codeman-Host, von dieser Lane nicht erreichbar) — ich kann den Lock von hier aus NICHT freigeben.
BEFEHL (ausgefuehrt, fehler):
```
$ ssh baha-podman 'lockctl release baha-podman'
bash: line 1: lockctl: command not found
exit: 127
```
VOM OWNER: bei Freigabe-Haftung klaert der Owner (nicht die Lane auf eigener Faust). Melde hier nur Befehl + Fehlerzeile fuer die Owner-Klaerung.

---

## END

END_DONE.
Evidence-Pfad: evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md
Develop-SHA (Anchor): 223cb97a9d652a4672257cabbadf12e2b41ed9cd
