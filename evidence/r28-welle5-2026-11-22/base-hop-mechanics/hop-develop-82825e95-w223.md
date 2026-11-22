# 0428-223-testctx — hop-wave akte: PR #1750 + PR #1753 onto develop 82825e95a6f

## PLAN

- (done) 1. ls-remote-zeugnis: develop 82825e95a6f, #1750 head f16cef27f4d (back=1), #1753 head 91f4e38795a (back=1)
- (done) 2. PR #1750: additiver hop git merge --no-ff 82825e95a6f -> 17f471cd3fe, back=0, no conflicts
- (done) 3. PR #1750: push ohne force + ls-remote delivery-witness
- (done) 4. PR #1750: PR-run 44982040951 terminal: completed SUCCESS (cli-0/1/2/3 + packages ausgefuehrt und groen)
- (done) 5. Korrektur-Meldung des Coordinators verarbeitet (cli-3-zeugnis + draft-schalter als einziger restpunkt); zusatzlicher run 44982566548 am selben head ebenfalls completed SUCCESS
- (done) 6. PR #1753: gleicher ablauf -> f29bf6fa303, back=0; run 44982699457 terminal completed SUCCESS; native-gate SKIPPED bleibt Owner-hand (scripts/pr-gate-plan.py:180, karte 0428-228) - nichts geaendert
- (done) 7. Akte publizieren auf plan origin/main + ls-tree-witness
- (pending) 8. END post aan 9142ab1f

## Mission

hopwave.md.g (instructie: twee hops, #1750 eerst, dan #1753, additief, geen force) + korr1750.g.md (correctie: niets nieuws, cli-3-zeugnis vastleggen; restpunt draft-schalter = Owner-hand).

## Base attestation + remote witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` (measured before hop A):
  `82825e95a6f6083702d0ba5401d97f356085c722  refs/heads/develop` — de squash-merge van #1754 (zsh/fish provisioning in de Draft Go cell), de basis voor beide hops.
- Vooraf: refs/heads/lane-0428-223-testcontext-target = refs/pull/1750/head = `f16cef27f4dfb45db528226e573a38bde503b6cc`;
  refs/heads/lane-0428-227-footprint-gate-admission = refs/pull/1753/head = `91f4e38795a2657d50228c569a684fcb77da031c`. Beide back=1 tegen develop.
- Planning repo (correcte zone): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## A) PR #1750 — lane-0428-223-testcontext-target

- Werkzone: mijn eigen bestaande worktree `/home/marcel/dev/baseharbor-ecosystem/workers/0428-223-testctx-wt` (geen /tmp-clone, geen vreemde worktree).
- `git merge --no-ff 82825e95a6f6083702d0ba5401d97f356085c722` → merge commit `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99`, rc=0, geen conflicten, back=0.
- `git merge-base --is-ancestor 82825e95a6f6… HEAD` → yes; `git merge-base --is-ancestor f16cef27f4d HEAD` → yes (FF-push mogelijk, geen force).
- `git diff --name-only f16cef27f4d HEAD` → `.github/workflows/ci.yml` uitsluitend: de 14 regels zsh/fish provisioning VAN DEVELOP ZELF via de merge. Door mij is GEEN enkel teken in `.github/**` of `scripts/**` gewijzigd.
- Push-witness: `f16cef27..17f471cd  HEAD -> lane-0428-223-testcontext-target`; daarna
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-223-testcontext-target refs/pull/1750/head` → beide `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99`. PR #1750 blijft draft=true, OPEN.
- Provenance `git log --oneline 82825e95a6f..17f471cd3fe`: enkel mijn eigen commits (17f471cd hop, f16cef27 hop, 4bd779b1 ORAS, 1588ee1b isolation) — geen vreemde content bovenop.
- Runs (Eigenes-Run-Pflicht):
  - run `44982040951` (pull_request, head 17f471cd): **completed success**; uitgevoerd en groen: PR · Draft source and routing (137084441293), cli-0 (137084441490), cli-1 (137084441489), cli-2 (137084441515), **cli-3 (137084441603) success** — het zsh-zeugnis dat de coordinator vroeg — en packages (137084441619). Alle overige jobs skipped, o.a. `PR Selected Checks` (137084443447) = skipping omdat de PR draft was; de draft-schalter is Owner-hand, niet van mij. Failed jobs: 0.
  - Na het openen van de schalter: run `44982566548` (pull_request, head 17f471cd, draft=false): **completed success**. Failed jobs: 0.
- Dit hop maakt AKTAAL het develop-weite validate-rot van de 14 tests (diagnose-1.md): `testIsolatedSelectionContext` + `provisionORASForIntegrationCell` (7 bestanden op mijn head, 0 op develop 82825e95a6f — gemeten met `git show 82825e95a6f:cmd/baha/test_operator_context_test.go | grep -c testIsolatedSelectionContext` = 0) komen met de merge van #1750 in develop.

## B) PR #1753 — lane-0428-227-footprint-gate-admission

- Niet mijn branch: isolatie in een eigen zone `/tmp/opencode/0428-223-hop1753` als detachete worktree op `91f4e38795a` uit de real URL (geen vreemde worktree aangeraakt).
- `git merge --no-ff 82825e95a6f…` → merge commit `f29bf6fa303718ee258f4edd40a62dbbecd37f77`, rc=0, back=0; diff t.o.v. oude head: opnieuw enkel `.github/workflows/ci.yml` (develop's eigen 14 regels), geen inhoudswijziging door mij.
- Push-witness: `91f4e387..f29bf6fa HEAD -> lane-0428-227-footprint-gate-admission`; `git ls-remote … refs/heads/lane-0428-227-footprint-gate-admission refs/pull/1753/head` → beide `f29bf6fa303`. PR = draft=false, OPEN; de review-aktus `review-1753-head91f4e38795a.md` (APPROVE op het vorige head) is van de andere lane.
- Runs (Eigenes-Run-Pflicht):
  - run `44982699457` (pull_request, head f29bf6fa): **completed success**. Failed jobs: 0.
  - run `44982391942` (head 27e509757b2, de andere lane's eigen hop-poging op deze branch, terminal BEFORE mijn push): completed failure — 2 failed jobs: `137085872631` (PR · Selected Runtime — podman/data-capabilities) en `137087397662` (PR Selected Checks). Getuige dat mijn mechanische hop GEEN rode trail achterlaat: het uiteindelijke PR-head f29bf6fa is groen.
- Native gate blijft SKIPPED tot kaart 0428-228 de path->gate-indracht in `scripts/pr-gate-plan.py:180` zet (Owner-hand; daar is door mij niets gewijzigd).
- Opschonen: `rm -rf /tmp/opencode/0428-223-hop1753` + `git worktree prune`.

## cleanliness

cleanliness: nothing started. Eigen pid 2073855 (en latere shells van dezelfde sessie). Geen enkele container, compose, netwerk of volume door deze dispatch gestart.

- `docker ps -a --format '{{.ID}} {{.Names}} {{.Status}}'` BEFORE (04:4x): lege lijst (0 entries).
- AFTER: lege lijst (0 entries).

END 0428-223-testctx DONE (candidate SHAs: #1750 = 17f471cd3fe, #1753 = f29bf6fa303)

## publishing witness

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep base-hop-mechanics/hop-develop-82825e95-w223
evidence/r28-welle5-2026-11-22/base-hop-mechanics/hop-develop-82825e95-w223.md
```
