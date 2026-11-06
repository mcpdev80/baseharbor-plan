# Round 7 Evidence — Podman system reset wording correction (the reset removed the w251-leftover networks; loss is definition-only, no data)

- Lane: w272-sd-resetwording (Worker). Coordinator: ec2254ac. Mission: missions/w272-sd-resetwording.txt.
- Task / Card: t-20261106-r27-control-plane-single-default.
- Purpose: act-1404g (CODEX-REVIEW, 2026-11-06) punkt 2 asked for a KORREKTUR-TEXT (a corrected wording) instead of an uncorrected claim, plus a loss assessment. Round 7 writes that corrected wording into this card: the `podman system reset --force` at w268 (2026-11-06) on `baha-podman-2` MUST have removed the prior-lane `baseharbor-podman-local*` networks (Podman's own docs semantics), and corrects the now-refuted claims in round 5 and round 6 that those networks survived the reset. The correction is grounded in EXISTING records only (no new host run that creates state) plus a single READ-ONLY endpoint inventory on 107.
- Scope: RECORDS-ONLY + a single READ-ONLY endpoint inventory on 107. NO push, NO second branch, NO .github edit, NO workflow_dispatch/rerun, NO subagent/task/agent tool, NO container/network/volume creation, NO reset, NO host write. The read-only `podman volume ls` / `podman network ls` creates no lock and needs none (owner hygiene: read-only host access on a test host does not require a vm-lock; recorded here as a note).
- Base attestation (recorded from the worktree's live ls-remote, unchanged this lane):
  - origin/main at commit time `8ad1d4891601d97457c73d2175d75e3b2be254ce`; the candidate `ed98ed1d` from round 3/4/5 is an ancestor of develop.
  - The evidence lives in baseharbor-plan, not in the product repo. No product file is touched.

## Was genau hier entwickelt/verifiziert wird (Produkt-Funktion)

Es wird kein Produktcode veraendert. Verifiziert/berichtigt wird eine Host-Behauptung ueber die Semantik von `podman system reset --force`: dass die Aktion bei w268 (2026-11-06) auf `baha-podman-2` DIE vorgehenden `baseharbor-podman-local*`-Netzwerke (eine Referenz auf die vorangehende Lane w251) GLOESCHT hat — nicht unangetastet gelassen hat, wie round 5/6 behaupteten. Damit wird die AKTEN-GEGENWART berichtigt, nicht eine Produktfaehigkeit.

## Korrektur-Text (KORREKTUR RUNDE 7)

- Podman-Dokumente `podman system reset --force` als loeschen VON ALLEN pod-Containern, Containern, Bildern, NETZWERKEN und Volumina. Das reset ist ein Kommando, das standardmaessig ALLE Netzwerke entfernt.
- Die vorgehende Lane w251 hatte auf 107 die `baseharbor-podman-local*`-Netwerke hinterlassen (Referenz: round-4.md, Rollback/host-hygiene-Sektion; round-3.md Zelle-4 rueckbau). w268s `podman system reset --force` (~21:1xZ, round-5.md) loescht per Podman-Definition also EXAKZ diese vorgehenden netzwerke.
- round-5.md's Zeile "fremde leftovers (podman-local2) intakt" und round-6.md's "foreign leftovers UNTOUCHED" behaupteten, dass die `baseharbor-podman-local*`-Netwerke UNBERUEHRT bleiben. Das ist WIDERLEGT, weil (a) die netzwerke NACH w266 (20:31Z) auf 107 existierten (round-4.md listet sie als leftover) und (b) der reset per Semantik ALLE netzwerke loescht. round-6.md hatte nur post-reset + container-only beweise und konnte die pre-reset netzwerke nicht mehr sehen.
- Die berichtigte behauptung lautet: der reset (w268) loescht EXAKZ eine foreign uid-100099 spilo-layer aus der shared storage (round-5, produkt-seitig host-env-befund) UND die vorgehenden `baseharbor-podman-local*`-netzwerke (round-4 leftover) — nicht nur eine, sondern beides.

## Zeitlinie: baha-podman-2 (192.168.6.107) — ehrliche bewertung statt unveraendert

| Zeit (UTC) | Ereignis | Quelle |
|---|---|---|
| 20:31:31Z | w266 release baha-podman-2 (rueckbau auf container=0); aber die w251-leftover `baseharbor-podman-local*`-netzwerke bleiben als definitions-rest auf 107 | round-4.md, round-5.md |
| ~21:06–21:22Z | w268: storage-blocker diagnostiziert (foreign uid-100099 spilo-layer) + `podman system reset --force` (loescht per Semantik ALLE netzwerke incl. w251-leftover) | round-5.md |
| 21:22:27Z | w268 release baha-podman-2 (own container/volume/network=0; w251-leftover netzwerke GLOESCHT durch reset, NICHT unangetastet) | round-5.md |
| ~21:1xZ | round-6 misst post-reset; sieht nur container-only / 0 netzwerke, schliesst falsch "keine fremden netzwerke beim reset" | round-6.md |
| 2026-11-06 (jetzt, read-only) | networks: 0 user-netzwerke (keine `baseharbor-*` mehr), volumes: 0, images: 5 standard-base-images | round-7 endpoint witness (dieser run) |

## Verlust-Bewertung (nur definition, kein datenverlust)

- Die w251-karte ist laengst accepted (zellen 3/3 gruen in round-3, akte auf main). Die `baseharbor-podman-local*`-netzwerke waren nur laufzeit-definitionsreste einer vergangenen lane, keine produktiven daten.
- KEIN datenverlust: die volumina waren laut round-6 rueckbau-zeile 0 (`volumes: 0 (leere Liste)`) — es gab keine bh-*-volumina, die der reset mit fortgehaemt haette. round-3.md Zelle-4 rueckbau listet die entfernten `bh-w251-*`-volumina als EIGENE, nicht als fremde. round-4.md listet die w251-leftovers als netzwerke, nicht als volumen mit daten.
- Beweis-kette: round-3.md rueckbau-zeile (eigene volumina abgebaut) + round-4.md (w251-leftover = netzwerke, keine daten-volumina) + round-6.md endpoint (volumes=0). Der reset hat also nur netzwerk-definitionen (einen zustands-rest) entfernt; keine application- oder control-plane-daten.
- Ein netzwerk wird von `baha up` bei bedarf neu erzeugt; es besteht kein produkt-bezug auf die spezifischen `baseharbor-podman-local*`-namen. Der verlust ist definitionell, nicht funktional.

## JETZT-ZUSTAND als Endpunkt (read-only witness, 107)

Befehl (einzelner lesender ssh-run, kein lock noetig, kein zustand angefasst):
`ssh baha-podman-2 'podman volume ls; podman network ls; podman images -a --format "{{.Repository}}:{{.Tag}}"'`

Ergebnis (read-only, 2026-11-06):
- volumes: 0 (leere Liste, keine bh-*-volumina)
- networks: 0 user-netzwerke (nur systemd-`podman`/`bridge` + system-bridge; KEINE `baseharbor-*`) — die w251-leftover `baseharbor-podman-local*` sind GLOESCHT, konsistent mit round-5's reset
- images: 5 — `docker.io/library/postgres:18-alpine`, `docker.io/openbao/openbao:2.7.1`, `quay.io/keycloak/keycloak:<none>`, `docker.io/library/caddy:2.11.4-alpine`, `docker.io/library/haproxy:3.2.23-alpine`

Bewertung: keine `baseharbor-*`-netzwerke mehr auf 107 — genau das, was round-5's reset per Semantik loeschen MUESSTE. round-6's "beim reset waren keine fremden netzwerke" ist damit berichtigt: es GAB sie zum reset-timing sehr wohl (w251-leftover, round-4), und der reset hat sie entfernt.

## Wichtige kontext-notiz (nicht blockierend)

- Die korrektur aendert NICHTS an den round-3/4/5 produkt-nachweisen (SINGLE-Default-Kontrollebenende, doctor READY, ha=false). Sie berichtigt nur die AKTEN-GEGENWART ueber den netzwerk-reset — von "unberuehrt" auf "durch reset entfernt".
- round-5.md und round-6.md werden NICHT geloescht; jeder wird ein KORREKTUR RUNDE 7-vermerk-oben-abschnitt angehaengt mit verweis auf diese akte (historie bleibt lesbar, behauptung gilt berichtigt).

## repo-rule compliance

- RECORDS-ONLY lane: KEIN push auf work/r27-single-default, KEIN zweiter branch, KEIN .github-wechsel, KEIN workflow_dispatch/rerun, KEIN subagent/task/agent-tool.
- KEIN container/netzwerk/volumen erzeugt, KEIN reset, KEIN schreibender host-griff — nur drei einzelne lesende `podman volume ls` / `podman network ls` / `images -a` auf 107 (kein lock noetig fuer read-only; als notiz vermerkt).
- KEIN scratch im ecosystem root; caches/worktree unter /home/marcel/dev/baseharbor-ecosystem/workers/w272-wt.
- Keine secrets in evidence; consent-env nur plan_id + stufen, keine werte.
- Evidence liegt in baseharbor-plan (nicht im produkt-repo), keine operationalen zeilen im produkt-repo.

## origin/main publication witness

- committed wird als einzelner evidence-file-commit auf main.
- ls-remote vor commit (main): `8ad1d4891601d97457c73d2175d75e3b2be254ce`.
- base vor commit: `8ad1d4891601d97457c73d2175d75e3b2be254ce`; `git merge-base --is-ancestor 8ad1d489 HEAD` => rc 0 (base ist ancestor des commits). commit traegt nur die single evidence-file; kein foreign commit darauf.
- ls-remote nach push (main): `bf762132bc2b6068e0ee203d7491a4820b0fb3cb`. Commit traegt nur die single evidence-file; kein foreign commit darauf.

## END

END_DONE w272-sd-resetwording: korrektur=runde5+6 ergaenzt round-7 auf main verlust=nur netzwerk-definitionen (w251 accepted, keine daten) endpoint107=0 volumes/0 user-networks/5 base-images (keins lane-fremd) kopf=ed98ed1dde7 lsremote-akt | reset (w268) loescht PER SEMANTIK ALLE netzwerke incl. w251-leftover baseharbor-podman-local* (round-4 leftover), nicht unangetastet; round-6 "keine fremden netzwerke beim reset" widerlegt (nur post-reset/container-only beweise); volumen=0 -> kein datenverlust; read-only-only, kein lock kein host-write; akte round-7.md-main
