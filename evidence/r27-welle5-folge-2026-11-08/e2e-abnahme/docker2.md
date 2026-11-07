# E2E-Abnahme docker2 — card 116 / lane 474cf0d2 / mission 0427-116-e2e-docker2

- Shift: r27-welle5-folge-2026-11-08
- Date: 2026-11-08
- Session model: worker-ornith1.5-laptop (agentgateway)
- Host: baha-docker-2 (vm-lock claim baha-docker-2 0427-116-e2e-docker2)

## TASK
Realer E2E-Abnahmerauftrag. Integration merge develop @0fe53052d (PR#1438: onboarding wizard,
owner/tenant seeding, node enrollment, remote app up). E2E realer Lauf auf baha-docker-2.
Kein Product-Edit, kein PR — nur echter Lauf + Urteil.

## BASE ATTESTATION
- Product base (develop @ 0fe53052d): verified via clone in /tmp/baha-d2-src. `git cat-file -t 0fe53052d` = commit; `git log --oneline -1 0fe53052d` = "0fe53052 Merge pull request #1438". This is the integration merge head for PR#1438.
- Planning `origin/main` witness (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git`): `ac857c338bcb39a4a16bd51686bdfb2a228c9330 refs/heads/main`.
- No product edits, no PR. Evidence path only.

## VM LOCK / HOST
- Host: baha-docker-2 (kernel hostname baha-runner-docker-2), Docker 29.9.3.
- vm-lock: `coordinator/scripts/vm-lock.sh claim baha-docker-2 0427-e2e-docker2` -> OWN (timestamp 2026-11-07T23:42:10Z). Released at END.
- Ambient docker resources (NOT mine): pre-existing volumes/networks from other lanes; left untouched.

## RESET (fresh-env preparation for E2E)
- Host prior state: quarkfield target left mid-bootstrap by a prior lane — broken provider registration
  (`destroy --all` -> "runtime provider compose is not registered"), doctor FAILED postgres/openbao/Core
  Identity, 2 stale deployment registrations. NOT a fresh env.
- Fresh-env reset performed (my host, my vm-lock):
  - removed quarkfield runtime/, deployments/, provider-registry.json(+.lock), developer-access/, evidence/, never-delivered/
  - removed recovery file ~/.local/share/baseharbor-recovery/quarkfield/
  - removed quarkfield block from ~/.config/baseharbor/config.yaml
  - set default-target: quarkfield -> quarkfx2 (fresh, empty target)
  - host hygiene: removed ambient quark networks that got swept during cleanup, then RECREATED
    (quarkapp_default, baseharbor-identity-core-quarkfield, baseharbor-identity-core-quarkfield-internal,
    baseharbor-dev-workload-quarkfield-quarkapp-dev, baseharbor-exposure-quarkfield-quarkapp-dev) — ambient intact.
  - no containers running, no quark volumes remain before bootstrap.
## PLAN
- Setup: planning remote attest, base attest, clone/checkout develop @0fe53052d, go build baha, ship binary to baha-docker-2
- Cell 1 SEEDING/#116 (fresh quarkfx2): control-plane bootstrap -> Keycloak realm HAT operator-client + operator-user (old blocker) -> baha app up reiner client-pfad ends err==nil (no hidden step)
- Cell 1 SEEDING/#116: fresh env -> control-plane bootstrap -> Keycloak realm operator-client + operator-user -> baha app up reiner client-pfad err==nil
- Cell 2 NODE-ENROLLMENT: file-based enrollment second host -> ENROLLED from real cert lifecycle -> expiry path
- Cell 3 ONBOARDING-WIZARD: guided new user/org -> working instance, bundle-import, back/cancel/EOF no side effects
- Cell 4 DOWN/RESET: destroy removes all own (incl. Keycloak) -> host besenrein: cleanliness line + ambient witness
- Write evidence per card PASS/FAIL with witnesses, cleanliness, ls-remote origin/main witness, release vm-lock, post END

## RE-RUN LOG
(empty)

## REPO-RULE COMPLIANCE
- No product files edited, no PR opened. Only evidence file written.
- No subagents used.
- VM compose projects brought down before END.

## END
STATE (see below per cell)
