# H-P6 adversarial bug hunt — list/prune path cuts (cmd/baha/app_prune.go, deployment list batch #174, internal/deployment/deployment_store.go)

- lane: 0427-hp6-list-prune-classification (session <sessionid>)
- date: 2026-11-09 (CET)
- host: baha-docker (=192.168.6.166, rootless docker 29.8.1, uid=1000, no podman)
- mission: /tmp/opencode/mission-hp6.md (Jagd, keine Produktänderung). Zerlege die HEUTE gelandeten Listen-/Pfadschnitte adversarisch nach prune-deletes-needed, concurrent-init classification drift, read-only list write, mixed-dead error mask.
- scope: KEINE produkt-aenderungen, KEIN PR, KEIN .github, KEINE workflow-aktion (Owner-Scope). Nur evidence-dateien (plan-repo) + vm selbst.
- build-quel: produkt develop HEAD (bughunt-quelle, NICHT branch-cut).
- akte pfad: evidence/r27-welle5-folge-2026-11-08/bughunt-hp6-list-prune-classification/hp6.md

## PLAN

- host-attestation auf baha-docker (SSH, whoami, uid, docker version) + container/image-snapshot vorher/nachher
- produkt develop HEAD attestieren (git ls-remote) + clone in /tmp/opencode/hp6-wt
- baha-vom develop-kopf bauen (go build, NICHT PR/branch-cut)
- path-map: app_prune.go handler chain, deployment list batch #174 klassifikation, deployment_store.go identity-check
- scenario 1: prune deletes a record another path still needs (foreign source / live deployment w/ applied intent / duplicate-name + foreign target) in real docker cell
- scenario 2: concurrent-init (175 family) causing read-only list to fall through to foreign/missing classification
- scenario 3: mixed-dead installation error masking in read-only list / prune
- befehle + output + datum pro behauptung notieren; evidence publish (origin/main); vm-compose down (ps-witness); END

## base attestation

- plan-repo origin/main (git ls-remote origin main): 43f6004b7f29e0aab3b1c2595ee25668114513da
- produkt develop HEAD (testquelle, NICHT branch-cut, dies ist bughunt): <sha> (git ls-remote https://github.com/mcpdev80/baseharbor.git develop)

## repo-rule compliance

- keine produkt-aenderungen, kein .github, kein PR, keine workflow-aktion (Owner-Scope).
- evidence liegt in baseharbor-plan (plan-repo), NICHT im produkt-repo.
- keine subagenten (owner-direktive 2026-11-04).
- build ausschliesslich aus develop; build-selbst nur build, keine produkt-aenderung.
- vm-compose-projekte werden am END von mir herunter gefahren (down, ps-witness).

## funde gesamt

- blocker: 0
- write-on-read-list: 0
- prune-deletes-needed: 0
- classification-drift (concurrent-init): 0
- mixed-dead-mask: 0
- (scenario-ergebnisse unten)

## END

- STATUS: IN ARBEIT
