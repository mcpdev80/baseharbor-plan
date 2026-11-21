# H-V49 sitz-isolation-desk — which lanes work in the SAME checkout/worktree, and which git identity do they write there

ROLLE: Worker (BUG-HUNT, reine Befundung). KEINE Produkt-aenderung, KEIN commit an baseharbor, keine PR-aktion, keine subagenten (§4.8).
LANE: 0428-076-huntiso (session 5a3b1749). DATE: 2026-11-21. Fenster: r28-welle4.
AKTEN-HISTORIE: die akte existierte bereits auf origin/main (commit 860aa6d5d, autor coordinator, 21.11. 15:56 — zeitgleich mit meinem ersten write-versuch; mein write hat die vorhandene datei UBERSCHRIEBEN). Die hiesige fassung fuehrt den coordinators-text fort und ergaenzt die eigenständig gemessenen tabellen (section 1/1b/1c/3, summen, funddetails 4-7). Ursprung des overlapping-hunt dokumentiert, nicht bereinigt.
MELDEFRIST: /var/tmp/stop-iso.md empfangen (echte Kartenarbeit fuer diesen Sitz) — diese Akte liefert ab, es wurde nichts Neues gestartet.
Fund→Karte: die Befunde gehoeren zu t-20261121-base-branch-provenance-loss (0428-221) und tooling-issue #24; Vorlaeufer-Akten: evidence/r28-welle4-2026-11-21/lane-authorship-desk/hunt-1.md und .../stale-worktree-inventory/hunt-1.md.

## PLAN

1. Remote-Attest: `git remote -v` auf baseharbor, workers/baseharbor und baseharbor-plan; nur github.com/mcpdev80-URLs benutzt; `docker ps -a` vorher.
2. `git worktree list` in BEIDEN baseharbor-Stores (baseharbor/ und workers/baseharbor/) plus `ls -d workers/.w* /var/tmp/*wt`; je Eintrag: pfad | head | user.name | dirty | alter.
3. Jedes worktree einer lane zuordnen (%an des letzten commits vs. config user.name des checkouts) und klassieren (i)-(iv).
4. QUER-PRUEFUNG ueber alle offenen PRs (`gh pr list --state open`): letzte 8 commits mit auteur; ueberall melden, wo der auteur nicht zur karte des PR passt.
5. Fuer jeden fund `git show --name-only <sha>` (nur dateinamen): fremder INHALT oder nur die schale.
5b. Zusatz (MELDEFRIST): PR #1747 fb841c2c2 vs develop 22fc68ebc065 gemessen — hop ist noch noetig (develop NOT ancestor von fb841c2c2).
6. Akte schreiben, summen je klasse, commit + push auf origin/main, ls-tree-witness, END mit plan-sha.

## base attestation + remote guard (gemessen)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v`: lane-origin, origin und upstream zeigen alle auf `https://github.com/mcpdev80/baseharbor.git`. Kein lokaler Dateipfad in diesem Checkout; alle ls-remote/fetch doch nur gegen die echte URL.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`: `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` — das ECHTE planning repo; verifiziert VOR dem ersten evidence-commit (diese Datei liegt dort, nicht in workers/).
- `git -C /home/marcel/dev/baseharbor-ecosystem/workers remote -v`: `origin  https://github.com/mcpdev80/baseharbor.git` — BEWEIS: workers/ ist selbst ein checkout des PRODUKT-repos baseharbor (branch lane-0428-215-native-cell-operator-seam, HEAD c331a43f8). Die 949 board-Dateien in workers/todos/ sind dort untracked; der workers/ bookkeeping-stand ist also ein Nebenprodukt der Quarantaene (s.u.), kein eigenes repo.
- Remote heads (ls-remote, echte URL): develop = `22fc68ebc0655874bc3f6aa886ff356dcad79624`, lane-0428-060-updown = `fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a`, baseharbor-plan main = `5066fad34b98f21b3c523d19e967b0dda86b8e1e`.

## KERNBEFUND (mechanische Ursache der gemeldeten Faelle)

1. Der user.name in einem checkout wird von der ZULETZT dort aktiven lane gesetzt und bleibt stehen (config-Wert in der gemeinsamen .git/, ueberlebt lane-release). Naechste Lane schreibt dann unter fremder Identitaet.
   - baseharbor/.git/config: `user.name = 0428-222-childenv` — die 53 worktrees DIESES Stores erben diese Identitaet, sobald eine Lane ohne eigene config schreibt. Bewiesener Fall: fb841c2c2/f6a6eb0ce auf PR #1747.
   - workers/baseharbor/.git/config: `user.name = 0428-076-nativeshape` (quarantined checkout).
   - baseharbor-plan/.git/config: `user.name = 0428-076-nativeshape` — letzte geschriebene lane; die planning-identitaet ist NICHT lane-proportional (72f3690f/5afc2481 unter 0428-214-scopeop, 096938c1 unter 0428-210-authzkeep, obwohl die Inhalte 0428-221-huntci/huntbase-Akten sind).
   - ~/.gitconfig (global): `user.name = lv4-verify`, `user.email = worker@baseharbor.local` — jede Lane ohne lokale config landet als "lv4-verify"/"worker" (PR-#1725/#1650-#1627-Fundserie).
2. ZWEI getrennte baseharbor-Objektstores bedienen denselben branch-Namen: `lane-0428-060-updown` = 8103f0065 im baseharbor-Store, = fb841c2c2 im workers-Store (PR-head). Beide zeigen als `.git`-datei formal auf denselben branch; die branch ist dort mit `+` (checked-out) markiert, die PR-wahre Version liegt nur im Quarantaene-store. Genau das hat tooling-issue #24 naechvollziehbar gemacht.
3. Das selbe Muster laeuft im workers/store weiter: 0428-142-genuine (LIVE session 8d1c9d8b, workingDir .models/ornith) hat `user.name = 0428-142-genuine` in die /home/marcel/dev/baseharbor-ecosystem/workers/.git/config geschrieben; damit arbeiten drei weitere, ANDEREN karten zugehoerige paths im selben store unter IDENTISCHER lane-identitaet (nativefaildiag-wt, 183-hopdev-wt, r9-0428-142-genuine-r2base, workers/workers/*) — PFAD GEHORT ZWEI LANEN.
4. Nested checkout-Falle (Wrong-zone, aktuell gemessen): /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan/ enthaelt einen evidence/-baum, ist aber KEIN eigenes repo — `git -C workers/baseharbor-plan remote -v` loest zum baseharbor.git-remote des workers/-stores auf (HEAD fahrt mit c331a43f8 = workers/-repo). Eine Lane, die dort committet, schreibt in den PRODUKT-zweig-Store und sieht ihre evidence nie auf github (identisches Muster zu den phantom commits 9ca27c9f/aff1532c/e53eedd0 vom 2026-11-07; in dieser welle real als 096938c1-Family, s. section 5).
5. Aktive sessions nutzen geteilte stores OHNE eigene worktrees: 5a3b1749 (huntiso, diese Lane) cwd workers/.models/flash. Im workers/-store (baseharbor.git-clone) sitzt die workers/-Buchhaltung AUF einem PRODUKT-branch: branch lane-0428-215-native-cell-operator-seam, HEAD c331a43f8. Die board-dateien und board-commits der lanes (todos/*.json sind dort untracked) committen als %an="worker" DIREKT auf diesen produkt-branch — c8393e72d/e048ceafc/c331a43f8 "0428-217: tick board ..." (0428-217-credfix2-Arbeit, generic "worker"-schale). Der branch existiert NICHT auf github (ls-remote leer) — ein lokaler phantom-branch, auf dem 15+ worktrees des workers/-stores haelten, inkl. dreier live-genutzter.

## 1. Worktree-Tabelle — Store baseharbor.git (Haupt-Store, 53 worktrees)

Spalten: pfad | letzter sha | %an (letzter commit) | zugeordnete lane | user.name des checkouts | klasse | dirty | alter (.git-mtime, gekuerzt).
Klassen: (i) pfad gehoert der lane, deren name im letzten commit steht; (ii) PFAD GEHORT ZWEI LANEN (identitaet != lane der arbeit); (iii) verwaist (keine lebende session); (iv) unklar.
Lebende sessions (gemessen `codeman agent list --json`): w1-Coordinator(9142ab1f), 0428-142-genuine(8d1c9d8b), 0428-076-nativeshape(395cfe04), 0428-060-rev2(47e440e7), codex-rev-1747(fecbada9), 0428-208-devci(0a1a3e07), 0428-076-huntiso(5a3b1749, diese Lane).

| pfad | sha | %an | lane (pfad/karte) | user.name | klasse | dirty | alter |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseharbor/ (main) | 37587b0ed | 0428-213-compilefix | 0428-213 | 0428-222-childenv | (ii) 213-head in 222-store | 1 | 11-21 15:30 |
| .codex-worker-1401 | 9e1b905cf | Worker w206 | PR#1401 review | 0428-222-childenv | (iii) | 0 | 11-06 |
| 0428-210-authzkeep-wt | 52866ae38 | 0428-210-authzkeep | 0428-210 | 0428-222-childenv | (i) arbeit / (ii) identitaet | 0 | 11-21 10:06 |
| 0428-210-hopfix3-wt | 6442955f4 | 0428-210-hopfix3 | 0428-210 | 0428-222-childenv | (i)/(ii) wie oben | 0 | 11-21 09:22 |
| 0428-213-rebase1737-wt | 3010b212c | 0428-213-rebase1737 | 0428-213 | 0428-222-childenv | (i)/(ii) | 0 | 11-21 08:48 |
| 0428-215-natfix-wt | 1167ea455 | 0428-215-natfix | 0428-215 | 0428-222-childenv | (i)/(ii) | 0 | 11-21 08:34 |
| 0428-219-exportauth-wt | e45430f2f | Marcel Pfingstgräf | 0428-219 (owner-write) | 0428-222-childenv | (i) owner | 0 | 11-21 07:00 |
| baseharbor/0428-211-hopdevelop-wt | 44b55ea4b | Marcel Pfingstgräf | 0428-211 (owner-write) | 0428-222-childenv | (i) owner | 0 | 11-21 10:37 |
| work/0427-175-wt | 2dfcb21fe | Marcel Pfingstgräf | 0427-175 | 0428-222-childenv | (iii) + (ii) | 41 | 11-09 |
| work/0428-102-wt | d144945af | worker-ornith1.5 | 0428-102 | 0428-222-childenv | (iii)/(ii) | 9 | 11-17 |
| work/0428-113-wt | 46de903f1 | worker-ornith1.5 | 0428-113 | 0428-222-childenv | (iii)/(ii) | 9 | 11-18 |
| .models/flash/bf01-base-wt | 13e096fc6 | Marcel Pfingstgräf | 0427-189/bf01 | 0428-222-childenv | (iii)/(ii) | 0 | 11-15 |
| .models/flash/bf01-fix-wt | 0e9ccb582 | Marcel Pfingstgräf | bf01 | 0428-222-childenv | (iii)/(ii) | 2 | 11-15 |
| .models/flash/wt | 092008692 | 0427-maintenance-r3 | w131 (flash-model) | 0428-222-childenv | (iii)/(ii) | 0 | 11-08 |
| workers/.tmp/0428-100-wt | 178b8a00a | mcpdev80 | 0428-100 | 0428-222-childenv | (iii)/(ii) | 0 | 11-17 |
| workers/.w082-r3-wt | d2a9cd11d | mcpdev80 | 0428-082 | 0428-222-childenv | (iii)/(ii) | 0 | 11-16 |
| workers/.w217-0428-204-entrypoints | 7db142852 | Marcel Pfingstgräf | 0428-204 | 0428-222-childenv | (iii) owner-tree | 1 | 11-20 |
| workers/.w230-base | 40cb28c75 | Marcel Pfingstgräf | w230-hop basis | 0428-222-childenv | (iii) | 0 | 11-21 02:14 |
| workers/.w230-oldbase | 3f7600ded | worker | 0428-142-stoff | 0428-222-childenv | (ii) — gemeldeter fall: 142-inhalt unter generic "worker" im 230er-pfad | 0 | 11-21 02:17 |
| workers/0428-086-wt | 7042ee612 | worker-ornith1.5 | 0428-086 | 0428-222-childenv | (iii)/(ii), dirty=9 sind test-reste (?? internal/application/trace-*/) | 9 | 11-17 |
| workers/0428-142-witnessfix3-wt | 015ce675b | 0428-142-witnessfix3 | 0428-142 | 0428-222-childenv | (i)/(ii) | 0 | 11-21 08:44 |
| workers/0428-217-credfix2-wt | 719d28a88 | worker | 0428-217 | 0428-222-childenv | (ii) 217-arbeit unter generic "worker" | 0 | 11-21 08:05 |
| workers/0428-222-childenv-wt | ddfa80f72 | Marcel Pfingstgräf | 0428-222 | 0428-222-childenv | (i)/(iii) owner-rebase | 4 | 11-21 14:37 |
| workers/080-r28-selection-wt | f611060cf | mcpdev80 | 0428-080 | 0428-222-childenv | (iii)/(ii) | 0 | 11-16 |
| workers/ci-reds-fix-062-wt | 80d4df52e | w073-perses-alerts | 0428-062 | 0428-222-childenv | (ii) 062-pfad, 073-author — gemeldetes muster | 0 | 11-16 |
| workers/w245-image-transfer | 1c024d11b | Worker w224 | r27 (historisch) | 0428-222-childenv | (iii) | 0 | 11-06 |
| workers/w263-wt/repo | 746afe6d8 | coord-welle5 | r27 (historisch) | 0428-222-childenv | (iii) | 0 | 11-06 |
| workers/w264-wt | 5e4fde717 | Marcel Pfingstgräf | r27 | 0428-222-childenv | (iii) | 4 | 11-06 |
| workers/w286-wt2 | 8b5075d25 | Worker w280 | r27 | 0428-222-childenv | (iii) | 0 | 11-07 |
| worktrees/w108-traceprobe/baseharbor | 39810520b | worker-ornith1.5 | 0428-108 | 0428-222-childenv | (iii)/(ii) | 0 | 11-17 |
| worktrees/w218-gate-catalog-fix | 40cb28c75 | Marcel Pfingstgräf | 0428-218-review | 0428-222-childenv | (iii) | 0 | 11-21 00:21 |
| /tmp/0428-142-hopci-wt | 2e4a570a7 | 0428-142-witnessfix3 | 0428-142 | 0428-222-childenv | (i)/(ii) | 1 | 11-21 09:40 |
| /tmp/opencode/0428-060-updown-wt | (PRUNABLE) | — | 0428-060 alt | — | (iii) prunable, geloeschter pfad | — | — |
| /tmp/w198-cli-wt | 7546b1806 | w198-0428-198-cligate | 0428-198 | 0428-222-childenv | (iii)/(ii) | 1 | 11-20 |
| /tmp/w207-lokifix-wt | bddb27e62 | worker | 0428-202 | 0428-222-childenv | (ii) 202-lokifix unter generic "worker" | 0 | 11-20 |
| /var/tmp/0428-208-static-gate | e362a71bb | **0428-060-updown** | 0428-208 | 0428-222-childenv | **(ii) FUND: 208-branch, letzter commit von 060-lane geschrieben** | 0 | 11-21 10:26 |
| /var/tmp/baseharbor-0428-088 | 54fbe4771 | worker-ornith1.5 | 0428-088 | 0428-222-childenv | (iii)/(ii) | 0 | 11-19 |
| /var/tmp/baseharbor-0428-116 | 7459d615d | worker-ornith1.5 | codex-hopf-1686 | 0428-222-childenv | (iii)/(ii) | 9 | 11-19 |
| /var/tmp/c213 | 37587b0ed | 0428-213-compilefix | 0428-213 | 0428-222-childenv | (i)/(ii) | 0 | 11-21 10:20 |
| /var/tmp/coord-fmt-177 | 03b66ceca | worker | coord (0428-177) | 0428-222-childenv | (iii)/(ii) | 0 | 11-20 |
| /var/tmp/dualmatch-wt/wt | 864fdcd3a | worker-ornith1.5 | 0428-126 | 0428-222-childenv | (iii)/(ii) | 0 | 11-19 |
| /var/tmp/gmcheck/core | da76c5cf9 | Marcel Pfingstgräf | coord-check | 0428-222-childenv | (iii) | 1 | 11-19 |
| /var/tmp/m121-efilter-wt | d1fcfdf6b | worker-ornith1.5 | 0428-121 | 0428-222-childenv | (iii)/(ii) | 10 | 11-19 |
| /var/tmp/m122-appclass-wt | 876329f73 | worker-ornith1.5 | 0428-122 | 0428-222-childenv | (iii)/(ii) | 9 | 11-19 |
| /var/tmp/m122-integration-check | f06221125 | worker-ornith1.5 | 0428-122 | 0428-222-childenv | (iii)/(ii) | 9 | 11-19 |
| /var/tmp/mission-093-scope-wt | d0351baf5 | worker-ornith1.5 | 0428-093 | 0428-222-childenv | (iii)/(ii) | 9 | 11-18 |
| /var/tmp/mission-110-wt | fb6f36936 | worker-ornith1.5 | 0428-110 | 0428-222-childenv | (iii)/(ii) | 0 | 11-18 |
| /var/tmp/mission-1599-wt | e43552734 | worker-ornith1.5 | review PR#1599 | 0428-222-childenv | (iii)/(ii) | 9 | 11-18 |
| /var/tmp/mission-1602-wt | b6c9702ba | worker-ornith1.5 | review PR#1602 | 0428-222-childenv | (iii)/(ii) | 0 | 11-18 |
| /var/tmp/w073-wt | d8838f622 | worker-ornith1.5 | w073 | 0428-222-childenv | (iii)/(ii) | 9 | 11-19 |
| /var/tmp/w220-0428-205/wt | 5e3074379 | **0428-213-compilefix** | 0428-205 | 0428-222-childenv | **(ii) FUND: 205-lane, letzter commit von 213-lane geschrieben** | 0 | 11-20 23:53 |
| /var/tmp/wt-078-r4 | 9add5e8a2 | worker | 0428-078 | 0428-222-childenv | (iii)/(ii) | 0 | 11-20 |
| /var/tmp/wt-091-r1 | 253883eb9 | worker | 0428-091 | 0428-222-childenv | (iii)/(ii) | 1 | 11-20 |

## 1b. Worktree-Tabelle — Store workers/baseharbor (QUARANTINED checkout, 11 worktrees)

Dieser store fuehrt denselben branch-Namen `lane-0428-060-updown` mit ANDEREM inhalt (fb841c2c2) als der haupt-store (8103f0065). Der PR-head (remote) = fb841c2c2 = DIESE store. Regelkonform sollte die 060-Lane im haupt-store arbeiten; sie arbeitet im quarantaene-store.

| pfad | sha | %an | lane | user.name | klasse | dirty | alter |
| --- | --- | --- | --- | --- | --- | --- | --- |
| workers/baseharbor/ (main) | 6f8fa120f | 0428-217-cloneenv | 0428-217 | 0428-076-nativeshape | (ii) 217-head, 076-config | 0 | 11-21 15:30 |
| workers/.0428-060-downroute-wt | fb841c2c2 | **0428-076-nativeshape** | **0428-060** | 0428-076-nativeshape | **(ii) GEMELDETER FALL: 060-inhalt (cmd/baha/app_lifecycle*.go) von 076-lane geschrieben** | 1 | 11-21 13:05 |
| workers/.w282-compose-wt | f236b6610 | Worker w206 | r27-compose | 0428-076-nativeshape | (iii)/(ii) | 0 | 11-07 |
| workers/0428-076-hop2-wt | 37d396000 (15:31) | 0428-076-hop2→0428-076-nativeshape | 0428-076 | 0428-076-nativeshape | (i) — aber: identischer inhalt (head sha) wie /var/tmp-Pfad unten = ZWEI pfade, eine lane | 0→9 | 11-21 12:26 |
| workers/0428-218-mcpseam-wt | de4a45ec5 | Worker w206 | 0428-218 | 0428-076-nativeshape | (ii) 218-arbeit unter w206-schale | 0 | 11-21 06:07 |
| workers/baseharbor/workers/w174-r3-wt | 50b99c462 | w129-codec-r5 | r27-w174 | 0428-076-nativeshape | (iii)/(ii) | 0 | 11-05 |
| workers/w162-protected-credentials-wt | 31cc10a01 | w129-codec-r5 | r27-w162 | 0428-076-nativeshape | (iii)/(ii) | 0 | 11-05 |
| workers/w207-journal-wiring-wt | efa1600c7 | Worker w203 | r27-w207 | 0428-076-nativeshape | (iii)/(ii) | 0 | 11-06 |
| workers/w229-wt | 65ed48d60 | Worker w206 | r27-w229 | 0428-076-nativeshape | (iii)/(ii) | 0 | 11-06 |
| workers/w274-wt | 55f12a8af | Worker w274 | r27-w274 | 0428-076-nativeshape | (iii) | 0 | 11-06 |
| /home/marcel/tmp/0428-142-authfixture-wt | b2f2fd3ac | Worker w206 | 0428-142 | 0428-076-nativeshape | **(ii) FUND: 142-arbeit unter w206-schale** | 0 | 11-21 06:23 |

## 1c. Worktree-Tabelle — Store workers/ (Buchhaltung, 18 worktrees) und Store baseharbor-plan/ (27 worktrees)

workers/-store: Haupt-pfad = das eigentliche baseharbor-repo-clone mit branch lane-0428-215-native-cell-operator-seam; board-/evidence-commits der lanes (todos/*.json, evidence/<datum>/*) landen dort auf einem PRODUKT-branch, nie auf github.

| pfad | sha | %an | lane | user.name | klasse | dirty |
| --- | --- | --- | --- | --- | --- | --- |
| workers/ (main) | c331a43f8 | worker | 0428-217 board-commits | 0428-142-genuine | (ii) 217-commits, 142-config | 954 untracked |
| workers/0428-183-hopdev-wt | 0afcaf374 | 0428-183-hopdev | 0428-183 | 0428-142-genuine | **(ii) 183-arbeit, 142-config** | 1 |
| workers/0428-215-nativefaildiag-wt | c331a43f8 | worker | 0428-215 | 0428-142-genuine | **(ii) nested auf workers/-head** | 0 |
| workers/r9-0428-142-genuine-r2base | 2e4a570a7 | 0428-142-witnessfix3 | 0428-142 | 0428-142-genuine | (i)/(ii) | — |
| workers/r9-0428-142-genuine-wt | 26a17d89c | 0428-142-genuine | 0428-142 | 0428-142-genuine | (i) — LIVE session 8d1c9d8b (ornith) | 8 |
| workers/workers/0428-111-json-classify-wt | ddfa80f72 | Marcel Pfingstgräf | 0428-111 | 0428-142-genuine | (iii)/(ii), dirty=488 (teststaende!) | 488 |
| workers/workers/0428-217credfill-wt | 0df7efc00 | worker | 0428-217 | 0428-142-genuine | (ii) | 9 |
| /var/tmp/tempo-r4/wt, mission-1579-uid-app-wt, w083-hopf-wt, ... | — | worker / w091-0428-091 | gemischt aelter | 0428-142-genuine | (iii)/(ii) | 0 |

| workers/0428-210-finalhop-wt | bb98e2259 | 0428-210-finalhop | 0428-210 | 0428-142-genuine | **(ii) 210-work, 142-config** | 0 |
| workers/perses-tmpfs-mountpoint-wt | b71c6da27 | lv4-verify | 0428-083 | 0428-142-genuine | (ii) | 0 |
| workers/w177-journal-r7-wt | a896bf61c | w163 access-profiles worker | r27-w177 | 0428-142-genuine | (iii)/(ii) | 2 |

plan-repo store (baseharbor-plan/, 27 worktrees): haupt-pfad identity = `0428-076-nativeshape` (zuletzt geschrieben); eine unbekannte horde worktrees unter `~/.local/share/horde/...` (fremdes tool), plus:

| pfad | sha | %an | lane | klasse |
| --- | --- | --- | --- | --- |
| work/0428-102-plan-wt | 270406fff | (codex branch) | 0428-102 | (iii) |
| work/0428-109-plan-publish-wt | f2a83752d | publish branch | 0428-109 | (iii) |
| workers/codex-luna-img-1402d-plan | 0e81a9896 | — | codex review | (iii) |
| workers/w240-plan / w244-plan / w245-plan-evidence | detached | — | r27 | (iii) |
| /var/tmp/plan-* (7 pfade), /home/marcel/tmp-ops/opencode/plan-sup | detached | — | aelter | (iii) |

Koordinaten-Notiz: der plan-store hat 27 registrierte worktrees, darunter 10 unter ~/.local/share/horde/ (fremder manager, keine lane-identitaet, alle auf fc666256b/f6fea0fde) — ausserhalb dieser lane, nicht angefasst, nur inventarisiert.

## 2. Summen je klasse

- (i) CLEAN (pfad-lane == letzter author): 0 von 63 vollstaendig — jede (i)-zeile oben traegt den zusatz "(ii) identitaet", weil NUR der checkout-user.name aus einer anderen lane stammt und damit der NAECHSTE commit des pfads fremd signiert waere. Der gemeldete fb841c2c2-fall ist der exemplarische eintritt dieses zustands.
- (ii) PFAD GEHORT ZWEI LANEN: 58 (alle 53 des haupt-stores: %an-lane != checkout-config-lane; + 4 im workers/baseharbor-store; + alle workers/store-zeilen: lane-im-pfad != 0428-142-genuine-config).
- (iii) VERWAIST (keine lebende session, %an-lane nicht in agent list): 24 pfade (r27-historik + worker-ornith1.5-serie + alle /var/tmp/mission-*).
- (iv) UNKLAR: 2 (/tmp/opencode/0428-060-updown-wt prunable; /home/marcel/tmp-ops/opencode/plan-sup).
- doppelte pfade fuer EINE lane: 1 gesichert — 0428-076: workers/0428-076-hop2-wt (sha 12a6e7a46→37d396000) und der 076-config im workers/baseharbor-store + der 076-config im plan-store: dieselbe session beschriftet drei getrennte stores.

## 3. PR-Tabelle — 22 offene PRs (gh pr list --state open), letzte commits mit auteur

Passt-Regel (mission): PR-branch heisst `lane-0428-<n>-...`; die kartennummer muss im commit-text ODER im branch stecken; der auteur muss zur karte passen. "passt?" = auteur-Lane == PR-Karte.

| pr | letzter commit | %an | karte | passt? | dateien (%an != karte) |
| --- | --- | --- | --- | --- | --- |
| 1747 | fb841c2c2 | 0428-076-nativeshape | 0428-060 (branch lane-0428-060-updown) | **NEIN — GEMELDETER FALL** | cmd/baha/app_lifecycle.go, cmd/baha/app_lifecycle_down_route_0428_060_test.go = 060-INHALT unter 076-schale |
| 1747 | f6a6eb0ce | 0428-076-nativeshape | 0428-060 | **NEIN** | merge-commit (hop onto develop) — nur schale |
| 1747 | 2d848f446 | 0428-060-downroute <lane@> | 0428-060 | ja (anderer 060-lane-name) | merge |
| 1746 | e362a71bb | 0428-060-updown | 0428-208 (branch static-release-gate) | **NEIN — FUND** | .github/workflows/pre-release.yml |
| 1741 | de4a45ec5 | Worker w206 | 0428-218 | **NEIN** | cmd/baha/mcp_operator_seam_test.go = 218-inhalt unter w206-schale |
| 1738 | 7e6792939 | 0428-214-scopeop | 0428-214 | ja | cmd/baha/core_installation_runtime_test.go |
| 1737 | 37587b0ed | 0428-213-compilefix | 0428-213 | ja | cmd/baha/trust_uninstall_test.go |
| 1723 | 26755fc1e | worker (generic) | 0428-199 | karte nur im commit-text | cmd/baha/app_apply.go u.a. |
| 1714 | 0afcaf374 | 0428-183-hopdev | 0428-183 | ja | internal/metrics/perses_dashboards_valkey*.go |
| 1702 | 37e1fd8ab | 0428-142-genuine | 0428-142 | ja | cmd/baha/app_status_result*.go |
| 1650 | 28c18f020 | Marcel Pfingstgräf | 0428-078 | owner-write | internal/identityprovider/..., internal/metrics/... |
| 1645 | 4d73aa978 | worker (generic) | 0428-091 | karte im commit-text | internal/metrics/perses_tempo_contract.go u.a. |
| 1627 | 202b984e2 | Marcel Pfingstgräf | 0428-055 | owner-write | cmd/baha/app_identity_selective_runtime_test.go |
| 1625 | 010db47da | Codex | 0428-065 | codex-write (erlaubt, role b) | cmd/baha/app_export*.go |
| 1623 | 4cbf92960 | Marcel Pfingstgräf | 0428-063 | owner-write | cmd/baha/app_access.go, app_interact_test.go |
| 1620 | 28cb907dc | Marcel Pfingstgräf | 0428-067 | owner-write | cmd/baha/app_access_test.go |
| 1614 | 80d4df52e | w073-perses-alerts | 0428-062 | **NEIN** | cmd/baha/app_edit_apply_test.go u.a. = 062-karte, 073-schale (historisch, base-heal merges) |
| 1597 | 12a6e7a46 | 0428-076-hop2 | 0428-076 | ja | perses dashboards (13 files) |
| 1596 | 6135e73a6 | Marcel Pfingstgräf | 0428-056 | owner-write | internal/orgconfig/orgconfig_test.go |
| 1588 | 993b3ec06 | Marcel Pfingstgräf | 0427-186 | owner-write | merge |
| 1585 | 16241f24a | Marcel Pfingstgräf | 0427-189/bf01 | owner-write | merge |
| 1740 | 0ffe09335 | Marcel Pfingstgräf | 0428-209 | owner-write | cmd/baha/control_plane_single_native_ci_test.go |
| 1736 | 8f11a34da | Marcel Pfingstgräf | env-destroy-gate | owner-write (.github, Owner-scope) | scripts/pr-gate-* |

Autheur-Summen ueber die letzten 8 commits je PR (gemessen): die 060-lane (updown/downroute) signiert commits in PR #1746 (0428-208-karte, 5 commits) und PR #1747 (eigene karte, korrekt); die 076-lane (nativeshape) signiert PR #1747-fremde commits (2) und den plan-store; w073-perses-alerts signiert 6 PRs fremder karten (1614/1627/1625/1623/1596/1597-serie); generic "worker"/"lv4-verify" taucht in 7 PRs auf.

## 4. Funddetail — fb841c2c27c (PR #1747), der anlass der mission

- `git show -s --format="author=%an <%ae> committer=%cn <%ce>"` auf fb841c2c2 UND f6a6eb0ce: beide `0428-076-nativeshape <0428-076@baseharbor.local>` (author == committer, 2026-11-21 15:06/15:08 +0100).
- `git show --name-only fb841c2c2`: cmd/baha/app_lifecycle.go, cmd/baha/app_lifecycle_down_route_0428_060_test.go — Inhalt der karte 0428-060 (down/stop route), commit-text traegt korrekt "0428-060". Nur die SCHALE (identitaet) ist falsch.
- f6a6eb0ce ist der merge-hop auf develop dea88c8f2 — ebenfalls 076-schale, kein inhalt (name-only leer, merge-commit).
- Wo passiert: `git -C workers/baseharbor reflog show lane-0428-060-updown` — commits {0} und {1} = fb841c2c2/f6a6eb0ce; der branch wurde im quarantined store workers/baseharbor gefuehrt, dessen .git/config user.name = 0428-076-nativeshape. Die 060-Lane hat ihre eigene config NICHT gesetzt (oder nicht zurueckgesetzt nach einem 076-hop in dem store).
- Ancestry-Check (MELDEFRIST-zusatz): `git merge-base --is-ancestor 22fc68ebc0655874bc3f6aa886ff356dcad79624 fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a` -> FEHLGESCHLAGEN: develop 22fc68ebc (gemessen via ls-remote + fetch refs/remotes/ls-remote-check/develop) ist NICHT ancestor von fb841c2c2 — der hop auf den neuen develop steht aus.

## 5. Funddetail — 3f7600ded (workers/.w230-oldbase), der zweite fall

- `git show -s 3f7600ded`: author == committer == `worker <worker@baseharbor.local>` (= globaler fallback, keine lane-config). Datum 2026-11-21 01:02.
- `git show --name-only 3f7600ded`: cmd/baha/app_status_result.go, cmd/baha/app_status_result_test.go, cmd/baha/perses_lifecycle.go — 0428-142-stoff (status-witness dateien) auf der basis 40cb28c7, registriert NUR im haupt-store, branchname (detached), auf github nirgends.
- Klasse (ii)+(iii): pfad gehoert "w230" (hop-Lane), inhalt gehoert karte 0428-142, identitaet ist der generic-fallback. Die preserve-lane hat denselben content spaeter dokumentarisch gesichert (plan-commit 6634bf762 "preserve w230 detached head 3f7600ded"); das object existiert lokal in beiden stores.

## 6. Funddetail — plan-commits unter fremden identitaeten (72f3690f / 5afc2481 / 096938c1)

Alle drei in baseharbor-plan auf origin/main, Inhalt = 0428-221 hunt-Akten:

| sha | author | inhalt (name-only) | echte besitzer-lane |
| --- | --- | --- | --- |
| 72f3690f0 | 0428-214-scopeop <0428-214-scopeop@users.noreply.github.com> | evidence/.../base-branch-liveness/hunt-1.md (checkbox-fix) | 0428-221-huntbase |
| 5afc24819 | 0428-214-scopeop | tasks/t-20261121-static-gate-registration.md | 0428-221/coordination |
| 096938c18 | 0428-210-authzkeep <0428-210@baseharbor.local> | evidence/.../ci-intake-desk/huntci/hunt-1.md | 0428-221-huntci |

Mechanik gemessen: der plan-store traegt user.name = Zuletzt-Schreiber (jetzt 0428-076-nativeshape, davor 0428-210/214/217/215). Eine hunt-lane ohne eigene config committet dort unter dem namen der zuletzt aktiven lane oder (global-fallback) als coord/worker/lv4-verify. Statistik (500 letzte origin/main-commits, gemessen): 124 coord <coord@local>, 100 worker <worker@baseharbor.local>, 42 coordinator <coordinator@baseharbor.local>, dazu lane-fremde autoren wie 0428-215-nativefaildiag mit 18 commits deren email = worker@baseharbor.local (author != eigene lane-email) — d.h. die lane setzt user.name aber NICHT user.email (config halbvoll).

## 7. Funddetail — weitere (ii)-stellen im selben muster (auteur != karte, Inhalt fremd)

- /var/tmp/0428-208-static-gate: letzter commit e362a71bb auf branch lane-0428-208-static-release-gate, author 0428-060-updown — ein 060-worker committet in den 208-worktree (PFAD GEHORT ZWEI LANEN, bestaetigt durch PR-#1746-zeile oben).
- /var/tmp/w220-0428-205/wt: letzter commit 5e3074379 auf branch lane-0428-205, author 0428-213-compilefix.
- workers/0428-076-hop2-wt UND /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor/.git/worktrees/0428-076-hop2-wt: dieselbe lane hat zwei registrierte heads; der workers/-store-hopp2 schrieb 37d396000 (15:31, same session-zeitfenster wie der 076-hop2 plan-commit 6df6169ba) — hop-arbeit laeuft parallell auf zwei pfade.
- workers/store board-commits (c8393e72d..c331a43f8, "0428-217: tick board", author generic worker): bookkeeping landet auf dem produkt-branch lane-0428-215-native-cell-operator-seam, der auf github NICHT existiert (ls-remote refs/heads/<name> = leer) — phantom-branch als ablageflaeche.

## 8. Loesungsansatz (Befund, keine Aenderung — zur karten-nummerierung durch den coordinator)

Vier minimal-schritte (Reihenfolge egal, keiner braucht .github/**):

1. spawn-lane.sh (coordinator/scripts): beim start jeder lane `git -C <wt> config user.name <lane>` UND `git -C <wt> config user.email <lane>@baseharbor.local` setzen (beide felder — das halbvoll-setzen ist fund 6). Betrifft die 63 bestehenden worktrees beim naechsten dispatch. Der nachlauf: `scripts/`-aenderung, laeuft ohne CI-Workflow-anderung; wenn die lane-schreib-pruefung (scripts/source-readability-audit.sh) anlaeuft, ist die ak auf die datei beschraenkt.
2. dispatch-lane.sh (coordinator/scripts): im auftragstext eine zeile "BEFORE your first commit, run `git config --get user.name` in your worktree; if it is not your lane name, the checkout is SHARED with another lane's leftovers — set it to your lane name (user.name AND user.email) and say so in your evidence, do not commit under a foreign name". Damit faellt jede fehlbeschriftung VOR dem commit auf, nicht im ls-remote danach.
3. worker-cleanup.sh (coordinator/scripts): vor der freigabe eines lanes den checkout auf eine neutrale identitaet zuruecksetzen (`git config user.name coord-reset-<lane>` statt wert-loeschen, damit die last-writer-spur sichtbar bleibt und kein naechster name geerbt wird). Damit hat die naechste lane einen faelschbaren, aber nicht-verfuehrerischen wert.
4. Karten-nummer: die Funde sind werkzeug-seitig und gehoeren in das vorhandene tooling-issue #24 (baseharbor-plan), das die identitaets-spur bereits traegt; parallel dokumentiert t-20261121-base-branch-provenance-loss (0428-221) dieselbe lane-autheurs-reihe. Empfehlung: punkt 1-3 als PR in baseharbor-plan unter referenz auf issue #24.

Kein bedarf an: git worktree prune, container,VM, CI-Workflow-aenderung, baseharbor-commit.

## 9. Was der fall NICHT ist

- Kein inhalt-diebstahl: alle gezeigten dateien stammen aus der karte, deren text sie tragen (commit-message + name-only deckungsgleich); nur %an/%ae ist fremd. Eine andere lane hat also NICHT in die fremde karte geschrieben, sondern FÜR sie — unter falschem namen.
- Kein fall von parallelem schreiben in derselben datei ohne plan (AGENTS 4.3): die 060/076-commits liegen sequentiell (reflog), nicht gleichzeitig.
- Kein CI-/gate-defekt: PR #1746/#1747 checks sind davon unbeeinflusst; git-identity hat keine CI-wirkung.

## 10. Zeugen

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-060-updown` (gemessen 15:3x): develop 22fc68ebc0655874bc3f6aa886ff356dcad79624, lane-0428-060-updown fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-215-native-cell-operator-seam`: leer (phantom-branch bewiesen).
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`: 5066fad34b98f21b3c523d19e967b0dda86b8e1e (base vor diesem commit).
- Ancestry: `git -C workers/baseharbor merge-base --is-ancestor 22fc68ebc065 fb841c2c27c` -> exit!=0 (hop offen).
- `codeman agent list --json` (15:2x): 7 sessions; die 5 worker-namen, die in den PR-autheuren 13x auftauchen (0428-213-compilefix, 0428-060-updown, Worker w206, w073-perses-alerts, lv4-verify), sind NICHT darunter — jede zeile mit "%an != live-session" ist ein dead-lane-autor (uebereinstimmend mit lane-authorship-desk/hunt-1.md derselben welle).

## ## nicht geschafft (MELDEFRIST: echte Kartenarbeit uebernahm den Sitz; Aktenlieferung schliesst hier)

- PR-zaehler-zeile: 22 offene PRs gecheckt (gh pr list --state open, baseharbor): 4 PRs mit auteur != karte direkt gemessen (#1747 076->060 inhalt, #1746 060->208, #1741 w206->218, #1614 073->062-historie); in der Serie ueber die letzten-8-commits traegt zusaetzlich w073-perses-alerts fremde commits in #1627/#1625/#1623/#1596/#1597 und generic worker/lv4-verify in 7 PRs. Damit sind 14 von 22 offenen PRs von der identitaets-verletzung beruehrt (inhaltlich korrekt, zuschreibung falsch).
- Nicht geschafft wurde schritt 4 der mission in der vollen tiefe: die letzten-8-commits-tabelle ist je PR nur im auteur-summary (gruppe_by) extrahiert, die sha-je-commit-zeile nur fuer den letzten commit je PR vollexplizit (section 3). Die 7 zusatzlichen PRs (#1740/#1736/#1738/#1737/#1723/#1714/#1702) wurden punktgenau gegen den neuen develop (22fc68ebc065) NICHT einzeln gecheckt, weil dafuer 7 weitere fetches noetig gewesen waeren (195 G platte, 95 % voll) und die MELDEFRIST neuearbeit untersagt.
- Nicht geschafft: die zuordnung der 10 ~/.local/share/horde/worktrees des plan-stores zu lanen (fremder manager ausserhalb des oekosystems; nur inventarisiert, nicht zugeordnet).
- Nicht geschafft: du-/stat-belege je worktree-groesse (H-V44 hat das bereits gemessen; hier nicht wiederholt).

## cleanliness (besenrein — ihr nachfolger sitzt auf demselben rechner)


- vorher (`date; docker ps -a`, 15:37 CET): CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES — TABELLE LEER (0 container, 0 eigene compose-projekte, pid 3959711).
- diese lane hat nichts gestartet: kein container, kein netzwerk, kein volume, kein state-verzeichnis, kein compose-projekt. Keine produktdatei geaendert, kein git worktree angelegt/entfernt, kein commit an baseharbor, keine PR-aktion, kein stash, kein go test.
- nachher: identisch leer (siehe naechste zeile, gleich nach dem letzten schreibenden aktion).

`docker ps -a` nachher (pid 3959711): TABELLE LEER (0 container).

cleanliness: clean — 0 container vorher, 0 container nachher, keine test-eigenen artefekte.

## repo-rule compliance

- AGENTS 4.8 keine subagenten: alles in dieser session gemessen und geschrieben; kein subagent/task-tool gerufen. (Anmerkung: ein frueherer versuch, messdaten per tools.shell in execute/Code-Mode zu holen, schlug fehl — "Unknown tool 'shell'" — und wurde ausschliesslich mit direkten shell-call-fortsetzungen erledigt; es wurde nichts delegiert.)
- BUG-HUNT-grenzen der mission: reine befundung; die einzige datei-aenderung ist diese Akte im plan-repo (evidence/r28-welle4-2026-11-21/worktree-isolation-desk/hunt-1.md), kein commit an baseharbor, keine PR-aktion, keine karte geaendert.
- WORKSPACE LAYOUT: keine scratch/caches/checkouts im ecosystem-root angelegt; die einzigen lege-artefakte liegen in /tmp/opencode/ (wtscan.sh, quota-bedingt leer), dort auch erlaubt.
- WORKER-RULES aus dem dispatch: kein nacktes go test ./... (gar kein go test), kein git add -A (nur gezielte dateien), kein git stash, kein codeman agent post in andere sessions (nur der eine END-post an den coordinator 9142ab1f), keine test-VM, keine runner-Aktionen, .github/** nicht angefasst.
- REALITY WITNESSES: remote-wahrheit ausschliesslich via ls-remote auf echten URLs gemessen; /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor (quarantined) wurde nur als objekt-lokalQuelle fr commits gelesen und als store-B in section 1b ausgewiesen — nicht als remote-zeugnis.
- PLAN-SICHTBARKEIT (§4.4): board-file workers/todos/0428-076-huntiso.json + ## PLAN oben; diese session exponiert kein natives todowrite-tool, daher leg (0) uebersprungen (dispatch: "if unsure, skip leg (0)").

## delivery witness + END

- `git -C baseharbor-plan fetch origin main` + `git ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/worktree-isolation-desk` (output, gemessen 16:0x CET):
  `evidence/r28-welle4-2026-11-21/worktree-isolation-desk/hunt-1.md`
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`: `861b97afca24034ef3ae3eceedfc8b0c79991e10  refs/heads/main` — plan-sha des END.
- base-attestation: geschnitten auf 5066fad34b98f21b3c523d19e967b0dda86b8e1e (origin/main, ls-remote-attested); `git merge-base --is-ancestor 5066fad34 HEAD` = 0; `git log --oneline origin/main..HEAD` zeigte ausschliesslich meine commits (bfa73046d, 861b97afc).

END 0428-076-huntiso DONE — akte auf origin/main (plan-sha 861b97afca24034ef3ae3eceedfc8b0c79991e10); product-repo baseharbor unveraendert (BUG-HUNT); 0 container.
