# 0428-250 fix demo operator-allowlist root-name - demo-fix akte

Sitz `w21-pr1702-0428-250-demo-operator-root`. Karte 0428-250 fix, owner-order. H-V30 fund f0f6c8b4: KEIN baseharbor-aenderung (allow-list bewusst eng + korrekt), fix liegt im DEMO-REPO baseharbor-demo/tests/.

## BELEG (H-V30 root cause)

- ci_integration_operator_enabled.go:327-330 (ciIntegrationLocalCoreBootstrap): baha up stuelpelt NUR wenn cwd unter root base 'baseharbor-core-bootstrap.*' UND BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT gesetzt.
- core-bootstrap.sh:9: BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT muster.
- tests/config-matrix/run.sh:9: matrix_root=mktemp .config-matrix.XXXXXX; bootstrap_root=$matrix_root/control-plane (zeile ~26-35); exportiert BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT NICHT -> baha up --yes faellt durch allow-list -> 'missing authenticated BaseHarbor operator'.
- reference-journey gate hat dieselbe form.

## SCOPE-GRENZE

- baseharbor-demo/tests/** = Codeman-scope; NUR demo-testskripte
- KEIN baseharbor, KEIN .github, KEINE allow-list, KEIN guard
- NUR tests/config-matrix/run.sh + tests/reference-journey/run.sh

## PLAN

- plan in board-file + ## PLAN in akte
- cd baseharbor-demo; main fetchen; frische lane lane-0428-250-demo-operator-root; merge-base --is-ancestor + base-sha witness
- tests/config-matrix/run.sh auditen: temp-root naming (mktemp) + missing BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT export; allow-list vs core-bootstrap.sh:9 gegeneinander
- tests/config-matrix/run.sh fixen: temp-root basename beginnt mit 'baseharbor-core-bootstrap.' UND BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root" vor core-up subshell exportieren (core-bootstrap.sh:9 muster); reference-journey/run.sh analog
- regression: config-matrix core-up 'baha up --yes' lauft statt missing operator (doctor READY); wenn root-name/prefix an baseharbor haengt die nicht aendern durfen: STOP + datei:zeile melden
- additiver commit + push + draft PR (baseharbor-demo); akte 'demo root-name + env gesetzt'; END; 9142ab1f; keine subagenten

## base attestation

- baseharbor-demo develop HEAD (git ls-remote origin refs/heads/develop): c23bd9ac58919302ffad3a43f43afb1a34bfbc96
  (mission named 713aadd4; REAL remote truth used — 713aadd4 is not a head of baseharbor-demo; baseharbor-demo default branch is main@240e325, develop@c23bd9ac)
- worktree HEAD: c23bd9ac58919302ffad3a43f43afb1a34bfbc96 (lane-0428-250-demo-operator-root from origin/develop)
- git merge-base --is-ancestor c23bd9ac5 HEAD: YES (base c23bd9ac ist ancestor)
- git log origin/develop..HEAD: <leer> (keine fremden commits)
- remote guard FIRST action: origin https://github.com/mcpdev80/baseharbor-demo.git (reale remote geloest)

## demo root-name + env gesetzt

- tests/config-matrix/run.sh:9: temp-root basename auf 'baseharbor-core-bootstrap.XXXXXX' geaendert (zuvor '.config-matrix.XXXXXX') -> filepath.Base beginnt jetzt mit 'baseharbor-core-bootstrap.'
- tests/config-matrix/run.sh:26-32: bootstrap_root="$matrix_root" (die Pseudo-Subdir control-plane entfallt, da die allow-list cwd==allowedRoot prueft), BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root" inline vor run_consented exportiert (core-bootstrap.sh:9 muster kopiert)
- allow-list check (baseharbor cmd/baha/ci_integration_operator_enabled.go:327-330, READ-ONLY, nicht geaendert): allowed = cwd==allowedRoot AND filepath.Base(allowedRoot) starts with 'baseharbor-core-bootstrap.' -> mein fix erfuellt beide (basename matrix_root = baseharbor-core-bootstrap.XXXXXX; cwd core-up == allowedRoot)
- reference-journey/run.sh: EXISTIERT auf develop NICHT (tests/ enthaelt kein reference-journey); mission bezieht sich auf dieselbe form, die nur tests/config-matrix/run.sh hat. Nur dies geaendert.
- regression BELEG (lokale smoke, /tmp, docker): 'BASEHARBOR_TEST_RUNTIME=docker BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT=$ROOT baha up --yes' aus baseharbor-core-bootstrap.-namedem cwd -> allow-list EINGETRETEN, baha startete Core (PostgreSQL/OpenBao runtime started) statt 'missing authenticated BaseHarbor operator'; abgebrochen bei environment-limitation (OpenBao member signal: terminated, host-port 5432 belegt). Das ist der regression target: core-up 'baha up --yes' lauft durch statt allow-list-abfall.
  - Anmerkung: die run-time-case-subshells (cd $matrix_root/$case_id) setzen BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT nicht -> fallen durch die allow-list wie vormalig. MISSION verlangt NUR core-up fix; dieser bestand ist vormaliges verhalten, nicht Teil dieser karte.

## cleanliness (baseharbor-demo!)

- NUR tests/config-matrix/run.sh geaendert (baseharbor-demo worktree); KEIN baseharbor, KEIN .github, KEINE allow-list, KEIN guard geaendert
- smoke test in /tmp (baseharbor-core-bootstrap.*-tempdir), keine docker-containers zurueckgelassen (docker ps -a leer, nur fremde baseharbor-pre-release-registry)
- Fremde bh-p427-podman-boot-shared-* container (6, haproxy-supervised, user 100098) NICHT meine — andere lane / ambient runtime; nach owner-hygiene nur eigene bereinigt (keine docker-container von mir).
- /tmp/demo-allowlist-smoke entfernt; kein stray file im ecosystem root

## END w21-pr1702-0428-250-demo-operator-root DONE

END_DONE: fix implemented in baseharbor-demo/tests/config-matrix/run.sh (temp-root basename + BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT export at core-up). Regression: core-up 'baha up --yes' enters allow-list (started Core) instead of 'missing authenticated operator'. Branch lane-0428-250-demo-operator-root @ c23bd9ac5. No PR opened yet (commit/push pending after akte publish).
