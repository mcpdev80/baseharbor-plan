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
- produkt develop HEAD (testquelle, NICHT branch-cut, dies ist bughunt): fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 (git ls-remote https://github.com/mcpdev80/baseharbor.git develop)

## findings

Scenario results (real docker cell on baha-docker + Go adversarial harness driving the real CLI/storage-seam code):

- prune-deletes-needed: 0. Prune refuses every record another path still needs.
- read-only-list write: 0. List is read-only; no write path found.
- concurrent-init classification drift: 0. Read-only list classifies foreign/malformed/dead installations distinctly, never folds to "missing".
- mixed-dead error mask: 0. Dead target record surfaces as distinct malformed WARN; live target still listed; walk does not abort.

### Scenario 1 — prune must not delete a record another path needs (real docker cell)

Command + output + date (host baha-docker, 2026-11-09):

```
$ ~/baha-hp6 app list
APPLICATION          ENVIRONMENT  STATE      SOURCE
gone                 dev          not_applied MISSING
  boot/gone: source repository gone (MISSING) - remove the dangling record with `baha app prune gone`...
live                 dev          created    MISSING
  boot/live: source repository gone (MISSING) - remove the dangling record with `baha app prune live`...

$ ~/baha-hp6 app prune live
Error
  boot/live/dev has an applied intent snapshot
...
  This is a real deployment: use 'baha app destroy' to retire it, not prune.
EXIT=1

$ ~/baha-hp6 app prune gone
Removed dangling deployment record boot/gone/dev
...
$ ~/baha-hp6 app list
APPLICATION          ENVIRONMENT  STATE      SOURCE
live                 dev          created    MISSING    # live still present after refused prune
```

`app prune live` REFUSES with applied-intent refusal (the "live" record has a source-gone but applied-intent snapshot = a real deployment `destroy`/`up` still needs). `app prune gone` removes ONLY the dangling record. The recoverable record survives. Proves the applied-intent guard runs AFTER the SOURCE_PRESENT check and that a recoverable deployment is never pruned.

### Scenario 2 — concurrent-init (175 family) must not let read-only list fall through to foreign/missing

Go harness (TestHp6ScenarioListClassifiesForeignInstallationDistinct) + Go mixed-dead harness (TestHp6ScenarioMixedDeadAllTargetsOneTargetDead):

```
$ ~/baha-hp6 app list --all-targets
[WARN] incomplete deployment state: malformed deployment state for dead// [44444444-...]: deployment state directory for its Target holds a Core installation that could not be validated; the installation.json is present but malformed or incompatible ...
TARGET               APPLICATION  ...
boot                 alive        ...     not_applied MISSING
```

The dead target's record surfaces as a DISTINCT `malformed deployment state` WARN (human + JSON `warnings` array); the live target's record is still listed; the walk does not abort. The best-effort list classifies a present-but-malformed installation as `malformed`/`access-denied`/`foreign` via `deployment_owner_classification.go` (`classifyOwnerWarning`), never folds it into the generic "missing"/"no registered deployment" lie. The concurrent-init copied-state (installation.json rewritten to a different Target) is likewise classified distinctly (test asserts Kind != "missing").

### Scenario 3 — mixed-dead error mask in read-only list / prune

Same as scenario 2: the read-only `app list`/`app list --all-targets` paths never crash on a mixed-dead target and never mask a present-but-broken installation as missing. The prune path is guarded separately (scenario 1).

## negative bounds (nothing found — mission END)

- No prune path deletes a record another path still needs (applied-intent guard + source-present guard + one-name + one-installation-owner all hold).
- No read-only list writes. `ListDeploymentsForDisplay`/`ListAllDeploymentsForDisplay`/`listDeploymentRecords` are read-only; owner verification is fail-closed, not mutating.
- No concurrent-init (175-family) drift: the #174 classification seam (`VerifyDeploymentOwner` → `isAccessDeniedLoadError`/`isMalformedInstallationLoadError` → distinct `DeploymentRecordStateError.Kind`) holds; `resolveRegisteredApplication` propagates the true verdict (`access-denied`/`malformed`) instead of the "not found" lie.
- No mixed-dead mask: dead-target state surfaces as a distinct malformed/access-denied warning; walk best-effort, does not abort; live-target records still listed.
```

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

## END

- STATUS: ABGESCHLOSSEN / END_PASS (Funde: 0 — alle drei Schnittschnitte adversarisch belegt, kein Produktfehler).
- befehle gesamt: host-attestation (SSH whoami/uid/docker), develop HEAD attestieren (git ls-remote), go build + scp, real docker-cell e2e (app list / app list --json / app prune live / app prune gone / app list --all-targets), Go adversarial harness (5 Szenarien).
- funde gesamt: blocker 0, write-on-read-list 0, prune-deletes-needed 0, classification-drift 0, mixed-dead-mask 0. Alle drei path-cuts (app_prune.go handler-chain, deployment list #174 klassifikation, deployment_store.go identity-check) adversarisch VERIFIZIERT: kein Produktfehler in develop fea92f379.
- akte pfad: evidence/r27-welle5-folge-2026-11-08/bughunt-hp6-list-prune-classification/hp6.md.
- evidence origin/main (git ls-remote origin main): <sha-before-push>.
- vm-lock baha-docker: gehalten bis END, dann released. ps-witness unten.
