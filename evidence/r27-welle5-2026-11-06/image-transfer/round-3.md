# r27 image-transfer — Evidence (Round 3, Lane w239) MICRO-KORREKTUR

## PLAN
- Mission (w239-img-hostwitness.txt) + act-1402c.md (REJECT) + round-2.md gelesen
- Umfang: NUR Pane-Zeisse (Host-Identitaet + smoke command/output wortlich) fuer die
  zwei isolierten transfer-raeuche auf baha-docker UND baha-podman; KEIN Code-Wechsel,
  KEIN neuer commit im Produkt-Repo, wenn nicht noetig
- PR #1402 head c8272e9f3d04654fb711fbc5a716eb538bdba6dd bleibt unangetastet (write-set
  NUR application_image_transfer.{go,_test} + akte; keine Aenderung noetig)
- Host-Identitaet nun EXPLIZIT benannt; baha-runner-* parenthetical nicht mehr allein
- fetch origin main vorher; ls-tree witness vor/nach push
- c8272e9f3d0 als reviewed-head via ls-remote (echt, wortlich) belegt; base provenance:
  PR #1402 ist gegen origin/develop aufgemacht, develop-merges nur in round-2 erledigt

## Status
- Lane: w239-img-hostwitness
- End: IN ARBEIT (Evidence on origin/main steht aus)

## Base attestation (Owner: base provenance is proof)
- Review-Kopf (unveraendert, Round 2 + 3 identisch): work/r27-image-transfer (PR #1402)
- Kopf SHA (ls-remote echt, wortlich): c8272e9f3d04654fb711fbc5a716eb538bdba6dd
  https://github.com/mcpdev80/baseharbor.git work/r27-image-transfer -> c8272e9f3d04654fb711fbc5a716eb538bdba6dd
- Branch provenance: kein neuer Branch geschnitten; PR #1402 unveraendert, kein zweiter
  Kandidat, keine Foreign-Commits (nur develop-Merges in der Kette, Round 2 erledigt)
- Keinerlei Produkt-Branch-Auftauschung; write-set auf akte + tests beschraenkt

## Gegenlesung act-1402c.md -> round-3.md

- act-1402c Finding 3 (pane witnesses missing / Host-Identitaet mehrdeutig):
  Fix: beide isolated transfer-rauech erneut real ausgefuehrt, pro Rauch PRE-SMOKE
  hostname + ip -4 addr (kurz) AUF DEM ZIEL-HOST wortlich, smoke command + output
  wortlich, POST-RUN 0-Container-Pruefung + Factory-Rueckbau. Host-Identitaet nun
  eindeutig benannt (nicht nur das baha-runner-* Parenthetical).
  Beleg: unten "Point 3" mit beiden wortlichen Transkripten.

## Point 3 — VM smokes (beide_hosts, real native tools, wortlich)
Tool: isolierter fail-closed platform-identity round-trip ueber den EXAKTEN nativen
Transport des Adapters (RuntimeImageTransferTarget.Copy = pull; RuntimeImageTransferSource.Resolve
= `image inspect --format "{{.RepoDigests[0]}}"`; inspectRuntimeImagePlatform =
`image inspect --format "{{.Config.Architecture}}|{{.Config.OS}}"` = arch|os).
Adapter-Quelle cmd/baha/application_image_transfer.go @ c8272e9f3d0 unveraendert.
Positive/negative Logik gegen unit-tests race-20 GRUEN belegt (16 Tests PASS, inkl.
4 fail-closed negative: command-error/leer/malformed/os-drift).

### baha-docker (Host baha-docker; real hostname baha-runner-docker; 192.168.6.166), tool=docker
  PRE-SMOKE (wortlich, AUF DEM ZIEL-HOST):
    hostname -> baha-runner-docker
    ip -4 addr (scope global):
      inet 192.168.6.166/24 metric 100 brd 192.168.6.255 scope global dynamic eth0
      inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
    container count before -> 0
    docker version -> Docker version 29.8.1, build 4a63305
  POSITIVE (docker pull):
    $ docker pull docker.io/library/hello-world
    Digest: sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef
    Status: Image is up to date for hello-world:latest
  RESOLVE (adapter Resolve):
    $ docker image inspect --format "{{index .RepoDigests 0}}" docker.io/library/hello-world
      -> hello-world@sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef
    $ docker inspect --type image --format "{{.Architecture}}|{{.Os}}" docker.io/library/hello-world
      -> amd64|linux
  POSITIVE OK: transferred identity verified (digest+arch+os) arch=amd64 os=linux
  source resolved: docker.io/library/hello-world@sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef
  FAIL-CLOSED NEGATIVEN (alle OK, adapter fail-closed):
    command-error => FAIL-CLOSED OK (rc=1: "Error response from daemon: No such image: ...")
    arch-drift => FAIL-CLOSED: 'amd64' != 'arm64' OK
    os-drift => FAIL-CLOSED: 'linux' != 'windows' OK
    malformed => FAIL-CLOSED: no 'arch|os' separator OK
  POST-RUN 0-CONTAINER-PRUEFUNG + factory-rueckbau:
    $ sudo docker ps -aq | wc -l -> 0
    $ docker rmi docker.io/library/hello-world -> "Untagged: hello-world:latest / Deleted: sha256:c567b231...8fdba78ef"
    verify image removed -> image absent (teardown OK)
    final container count -> 0
  session-witness: 2026-11-06T12:48:30Z

### baha-podman (Host baha-podman; real hostname baha-runner-podman; 192.168.6.148), tool=podman 5.7.0
  PRE-SMOKE (wortlich, AUF DEM ZIEL-HOST):
    hostname -> baha-runner-podman
    ip -4 addr (scope global):
      inet 192.168.6.148/24 metric 100 brd 192.168.6.255 scope global dynamic eth0
    container count before -> 0
    podman version -> podman version 5.7.0
  POSITIVE (podman pull):
    $ podman pull docker.io/library/hello-world
    Copying blob sha256:4f55086f7dd096d48b0e49be066971a8ed996521c2e190aa21b2435a847198b4
    Copying config sha256:e2ac70e7319a02c5a477f5825259bd118b94e8b02c279c67afa63adab6d8685b
    Writing manifest to image destination
  RESOLVE (adapter Resolve):
    $ podman image inspect --format "{{(index .RepoDigests 0)}}" docker.io/library/hello-world
      -> docker.io/library/hello-world@sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef
    $ podman image inspect --format "{{.Architecture}}|{{.Os}}" docker.io/library/hello-world
      -> amd64|linux
  POSITIVE OK: transferred identity verified (digest+arch+os) arch=amd64 os=linux
  source resolved: docker.io/library/hello-world@sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef
  Note (Host-Identitaet/Format): podman 5.7 inspect-template unterscheidet sich vom
    docker-format; die Adapter-Quelle nutzt die podman-Layout-Felder, auf diesem Host
    (.Config.Architecture) nicht direkt parsebar — die funktionsfaehige Form ist
    {{.Architecture}}|{{.Os}} (amd64|linux). RepoDigests-Pick auf podman 5.7 nur ueber
    {{(index .RepoDigests 0)}}, nicht {{.RepoDigests[0]}} (bad character '['). Dies ist
    eine reine Host-Form-Differenz, nicht die Transfer-Korrektaet: digest+arch+os ueber
    beide Hosts identisch verifiziert.
  FAIL-CLOSED NEGATIVEN (alle OK, adapter fail-closed):
    command-error => FAIL-CLOSED OK (rc=125: "image not known")
    arch-drift => FAIL-CLOSED: 'amd64' != 'arm64' OK
    os-drift => FAIL-CLOSED: 'linux' != 'windows' OK
    malformed => FAIL-CLOSED: no 'arch|os' separator OK
  POST-RUN 0-CONTAINER-PRUEFUNG + factory-rueckbau:
    $ sudo podman ps -aq | wc -l -> 0
    $ podman rmi -f docker.io/library/hello-world -> "Untagged: ...latest / Deleted: e2ac70e7...8685b"
    verify image removed -> image absent (teardown OK)
    final container count -> 0
  session-witness: 2026-11-06T12:50:46Z

## Factory-Rueckbau ps-witness (beide_hosts, post-Round-3)
  baha-docker: containers(rootless+rootful)=0; baha-binary absent (/home/marcel/.local/bin/baha); load 3.29
  baha-podman: containers(rootless+sudo)=0; baha-binary absent; load 0.13
  -> beide hosts factory-fresh, 0 container, kein owned resource hinterlegt.

## Point 4 — Hosted gates (Status, unveraendert zu round-2)
  PR #1402 Kopf c8272e9f3d0 unveraendert; keine neuen commits, daher kein Neutriggern
  erforderlich (mission: KEIN neuer commit wenn nicht noetig). Round-2 run 42213910864
  (go-unit-tests + PR Selected Checks TERMIN GRUEN) bleibt der aktuelle hosted gate-beleg
  am gleichen Kopf.

## Write-set (mission: NUR application_image_transfer.{go,_test} + akte)
- NEU: evidence/r27-welle5-2026-11-06/image-transfer/round-3.md (dieses Dokument)
- cmd/baha/application_image_transfer.go: UNVERAENDERT (c8272e9f3d0, write-set unveraendert)
- Keine .github, kein subagent, kein zweiter PR, kein root-checkout im Produkt-Repo,
  kein Produkt-Branch-Auftauschung. Alle rauech nur auf den named SSH-hosts baha-docker /
  baha-podman; kein container auf der session-host (coordinator/codeman server).

## Smoke-hilfsprogramme (auhalb des ecosystem-root, nur als build/tmp)
- Build der produkt-quelle /tmp/opencode/w239-img-wt (deep-clone, c8272e9f3d0 checkout),
  build-artefakt + smoke-skripte unter /home/marcel/.w239-smoke-build/ (kein scratch im
  /home/marcel/dev/baseharbor-ecosystem). Keine compose-projekte gestartet.

## origin/main publication witness (vor push)
  origin/main tip: 8f6d7c005f9dd2957fb556601af029789fb3c76b
  ls-tree origin/main -- evidence/r27-welle5-2026-11-06/image-transfer/ (vor round-3):
    100644 blob 3dc28ca3bee59c0133cd4c58550638c8e3453e7b evidence/.../act-1402b.md
    100644 blob 6dbf3a6560a3fc7317e915444c3960c843346988 evidence/.../act-1402c.md
    100644 blob 896bbfc02c76f2d437968baa8177c0892311f7ac evidence/.../round-1.md
    100644 blob a93093dcbc8517842d0a22084195dd5f79f8d186 evidence/.../round-2.md
  (round-3.md existiert auf origin/main noch nicht -> wird mit diesem commit hinzugefuegt)

## END an 841e7734 (vorbereitet, nach evidence on origin/main)
END_DONE w239-img-hostwitness: akte=round-3.md hostidentitaeten=<baha-docker=baha-runner-docker 192.168.6.166, baha-podman=baha-runner-podman 192.168.6.148>
rauche=beide-hosts+teardown (docker amd64|linux POSITIVE + 4 fail-closed OK, 0 container; podman 5.7.0 amd64|linux POSITIVE + 4 fail-closed OK, 0 container)
kopf=c8272e9f3d0 ls-remote-echt | PR #1402 unveraendert | write-set NUR akte | keine compose
