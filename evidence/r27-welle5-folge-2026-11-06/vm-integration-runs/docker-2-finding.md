# w269 finding: docker-2 `local` Core half-frozen (compose.yaml missing, phase=sql_failed)

**Lane:** w269-vm-integration-runs  **Coord:** ec2254ac  **Karte:** t-20261104-r27-vm-integration-runs
**Befund-Karte:** t-20261106-docker-2-half-frozen-core-stack (neu angekuendigt, coord reicht sie ein)
**Host:** baha-docker-2 (baha-runner-docker-2, 192.168.6.205)

## KOORDINATOR-ENTSCHEIDUNG (ec2254ac, 2026-11-06)

- DER HALB-FALLETTE DAUERSTAPEL AUF DOCKER-2 ist NICHT reparatur-auftrag w269. compose.yaml fehlt,
  phase=sql_failed, container laufen seit ~4h: sieht aus wie Hinterlassenschaft eines aelteren
  zustands-zells (w252 zeitfenster).
- Als BEFUND: neue FEHLERKARTE in dieser akte ankuendigen, coord reicht sie ein; w269 repariert
  keinen host-zustand in einer matrix-lane.
- MATRIX-UMPLANUNG konfliktfrei: docker-haelfte auf baha-docker (166, FREI, dauer-stapel gesund 8/0),
  podman-haelfte auf baha-podman (148, FREI). NICHT podman-2 (belegt w273). vm-lock pro phase,
  rc=3=wechsel nicht warten.

## BEGRUNDUNG DES BEFUNDES

- Der `local`-Target-Core ist auf baha-docker-2 LAUFEND: bh-local-shared-postgres-1, -member-1-1,
  -admin-1, bh-local-shared-openbao-1, -member-1-1, bh-local-shared-openbao-admin-1,
  bh-local-core-shared-keycloak-1-1 (healthy) — alle "Up 4 hours".
- Trotzdem steht die Installation auf `phase=sql_failed, ready=false`. `baha up --control-plane-only`
  haengt an der fail-closed Kanonizitaets-Pruefung:
  `existing native network lacks a protected Core or shared backend owner`.
- Gr: der Verifier (`internal/runtime/control_plane_inventory.go`, `inspectCoreDefaultNetworkBinding`
  in `cmd/baha/core_network_binding.go`) liest `targets/local/runtime/compose.yaml` ein und prueft
  gegen die Kanonizitaets-Definition; diese Datei ist auf dem Host NICHT vorhanden. Ohne kanonische
  Compose-Datei darf die Installation laut fail-closed-Vertrag NICHT abgeschlossen werden.
- Keine Container/Volumen/Netze von w269 existieren. Der laufende Stapel stammt aus einer
  unterbrochenen frueheren `up`-Aktion (w252-Fenster), nicht aus w269.

## ZEUGNIS (ls + ps + datei-liste des targets)

### docker ps -a (alle Container)
```
bh-w266dn-shared-openbao-1                                  | Created
bh-w266dn-shared-openbao-member-1-1                         | Created
bh-w266dn-shared-postgres-init-1                            | Exited (1) 40 minutes ago
bh-w266dn-shared-postgres-1                                 | Up 41 minutes
bh-w266dn-shared-postgres-admin-1                           | Up 41 minutes
bh-w266dn-shared-postgres-member-1-1                        | Up 41 minutes
bh-w266dn-shared-openbao-admin-1                            | Up 41 minutes
bh-local-core-shared-keycloak-access-1                      | Up 4 hours
bh-local-core-shared-keycloak-1-1                           | Up 4 hours (healthy)
bh-local-shared-openbao-1                                   | Up 4 hours
bh-local-shared-openbao-member-1-1                          | Up 4 hours
bh-local-shared-postgres-init-1                             | Exited (0) 4 hours ago
bh-local-shared-postgres-1                                  | Up 4 hours
bh-local-shared-postgres-member-1-1                         | Up 4 hours
bh-local-shared-postgres-admin-1                            | Up 4 hours
bh-local-shared-openbao-admin-1                             | Up 4 hours
```

### networks (12 baseharbor-netze)
```
baseharbor-identity-core-local, baseharbor-identity-core-local-internal,
baseharbor-identity-core-w257-ha, baseharbor-identity-core-w257-ha-internal,
baseharbor-identity-core-w257-local, baseharbor-identity-core-w257-local-internal,
baseharbor-identity-core-w266dn, baseharbor-identity-core-w266dn-internal,
baseharbor-local-default, baseharbor-local-secrets
```

### volumes
```
bh-local-shared_postgres-data-1
bh-w266dn-shared_postgres-data-1
```

### target state dir targets/local/runtime
```
drwx------ .installation.lock   (0 byte)
drwx------ docker-engine.json   (237 byte)
drwx------ installation.json    (524 byte)
compose.yaml  => NICHT VORHANDEN  (ls: no such file or directory)
```

### installation.json phase
```
phase= sql_failed   ready= False   ha= False
```

### Reproduktion des Fehlers (baha 8bda98c1cd3)
```
baha up --control-plane-only --no-input
  -> Error: Core sql failed: existing native network lacks a protected Core or shared backend owner
baha doctor --plain
  -> FAILED runtime-config : Core installation is incomplete; inspect retained installation state
```

## repo-rule compliance

- Kein produkt-code veraendert. Kein .github veraendert. Kein runner/infra angefasst.
- Der dauer-stapel wurde NICHT angefasst (keine matrix-lane reparatur). Nur lesezugriff (ls/ps) auf
  dem host.
- Baha-binary revision auf docker-2: 8bda98c1cd3 (identisch zum build-stand der matrix).

## END-VERMERK

Die docker-2 haelfte wurde als BLOCKED-mit-zeugnis dokumentiert (ls + ps + datei-liste des targets
siehe oben). Die restliche matrix wurde auf baha-docker (166) + baha-podman (148) gefahren.
Die fehlerkarte t-20261106-docker-2-half-frozen-core-stack ist neu angekuendigt; coord reicht sie
als eigene karte ein. w269 repariert keinen host-zustand.
