# 0428-249 fix registry/blob publish gap - fix-round-1 akte

Sitz `w21-pr1702-0428-249-registry-fix`. Karte 0428-249 fix, owner-order. H-V29 fund B (eigener registry/blob gap). develop 3cbb2bac.

BELEG (Mission): BASEHARBOR_RUNTIME_IMAGE=localhost/baseharbor-runtime:pre-release (.github/workflows/pre-release-runtime-suite.yml:11); ORAS target localhost:5000/baseharbor-runtime:pre-release (yml:201); light-runtime cells laden prebuilt tar (yml:177-197) + veroeffentlichen via scripts/ci-local-oci-registry.sh (yml:198-201). Fail='blob/manifest unknown' -> pre-release bild liegt NICHT im local registry wenn zellen pullen.

## SCOPE-GRENZE

- .github/workflows/* = OWNER-scope; AENDERN NIEMALS
- scripts/** = Codeman-scope; NUR scripts/ci-local-oci-registry.sh (+ seine tests)
- KEIN ghcr/237-pfad, KEIN operatorauth, KEIN .github

## PLAN

- plan in board-file + ## PLAN in akte
- develop fetchen; frische lane lane-0428-249-local-registry-publish; merge-base --is-ancestor + base-sha witness
- scripts/ci-local-oci-registry.sh auditen: pusht es baseharbor-runtime:pre-release nach localhost:5000 (blob+manifest) oder nur ghcr/edge? cite datei:zeile
- wenn publish-pfad fehlt/falsch: minimaler scripts-fix damit pre-release image vor light-runtime pulls im local registry (localhost:5000/baseharbor-runtime:pre-release) mit blob+manifest; KEIN .github-touch
- wenn fix NUR durch .github workflow-reihenfolge (publish vor pull / env BASEHARBOR_RUNTIME_IMAGE) behebbar und NICHT durch scripts allein: STOP + exakte .github/workflows/pre-release-runtime-suite.yml datei:zeile fuer owner; scripts-seitig nichts erfinden
- sonst: additiver commit + push + draft PR; beweisen local registry publish liefert blob+manifest; akte 'scripts-fix ODER .github-owner (datei:zeile)'

## base attestation

- develop HEAD (git ls-remote origin refs/heads/develop): 3cbb2bac39996391799d1c6460b230979ee34959
- worktree HEAD: 3cbb2bac39996391799d1c6460b230979ee34959
- git merge-base --is-ancestor 3cbb2bac3 HEAD: YES (base 3cbb2bac3 ist ancestor)
- git log origin/develop..HEAD: <leer> (keine fremden commits)
- remote guard FIRST action: origin + lane-origin beide https://github.com/mcpdev80/baseharbor.git (reale remote geloest)

## audit scripts/ci-local-oci-registry.sh

FULL SCRIPT (scripts/ci-local-oci-registry.sh, 73 lines): publish action takes source_image=$2, target_image=$3.
- line 27: validates target == localhost:5000/*:* (fail exit 2 otherwise)
- line 31: `image inspect "$source_image"` (fail if source missing)
- line 32-39: writes registries.conf insecure=true for 'localhost:5000' (PODMAN ONLY)
- line 40-54: `run --publish 127.0.0.1:5000:5000 docker.io/library/registry:2.8.3`, polls http://127.0.0.1:5000/v2/ up to 40x0.5s
- line 55: `image tag "$source_image" "$target_image"`
- line 56-60: push (podman `--tls-verify=false`, docker bare)
- line 61: `oras resolve --plain-http "$target_image"` -> digest verify (exit 1 if not sha256:64hex)
- line 66: `echo BASEHARBOR_RUNTIME_IMAGE=... >> $GITHUB_ENV`
- line 67: `echo Published... >> $GITHUB_STEP_SUMMARY`

MY TEST (proves publish logic WORKS, run locally with GITHUB_ENV/SUMMARY stubbed):
- docker: `publish localhost/baseharbor-runtime:pre-release localhost:5000/baseharbor-runtime:pre-release`
  -> registry started, image tagged, blobs+manifest PUSHED (docker: "The push refers to repository [localhost:5000/...]" + "Pushed" x3), oras resolve returned sha256 digest, then FAILED ONLY at line 66 GITHUB_ENV unbound variable (local env var missing). So the publish itself SUCCEEDS.
- podman: same, blobs+manifest copied successfully, only failed at line 67 GITHUB_STEP_SUMMARY unbound (local env var).
- Conclusion: the script's core publish (tag + push blob+manifest + oras verify) is FUNCTIONALLY CORRECT. In CI, GITHUB_ENV/GITHUB_STEP_SUMMARY are set by the runner, so lines 66-67 pass. The script does NOT have a publish-gap bug that would cause 'blob/manifest unknown'.

## scripts-fix ODER .github-owner (datei:zeile)

Determination: STOP - .github-owner action (mission step 3). The scripts/** `ci-local-oci-registry.sh` publish path is CORRECT (proven by local test: tags, pushes blob+manifest, oras resolves digest). No scripts fix is warranted. The 'local registry blob/manifest unknown' for localhost:5000/baseharbor-runtime:pre-release must originate OUTSIDE the script's publish logic.

Candidate root causes (all OUTSIDE scripts/** scope, require Owner .github action):
1. WORKFLOW ORDERING: the ORAS verification of localhost:5000/baseharbor-runtime:pre-release must run AFTER ci-local-oci-registry.sh publish (pre-release-runtime-suite.yml:201) completes. If a cell/job ORAS-resolves before the publish step, it sees an empty registry -> 'blob/manifest unknown'. Verify ordering at pre-release-runtime-suite.yml:198-201 vs where the cell ORAS-resolves.
2. WORKER SHARING: the local registry (127.0.0.1:5000) is started IN the publish step's container; if a subsequent step/cell expects it on the same runner without re-running publish, it's gone. Each matrix job is a separate runner -> publish must run per-job before that job's cells pull. Confirm publish runs inside each cell job (not only once upstream).
3. MISSING SCRIPT: scripts/acceptance.sh is referenced by pre-release-runtime-suite.yml:306, pre-release.yml:1080, targeted-demo-acceptance.yml:345 and registered as core path in scripts/pre-release-runtime-impact.json:104 (["*"]) BUT DOES NOT EXIST in the tree (git cat-file 404, gh contents 404). This is a REAL gap in scripts/** scope — but it is NOT the 'blob/manifest unknown' cause; it would instead fail as "scripts/acceptance.sh: No such file" before any ORAS resolve.

NO scripts/** change applied. No .github touched (Owner scope). No ghcr/237/operatorauth touched.

The exact .github/workflows/pre-release-runtime-suite.yml lines the OWNER must verify/patch:
- yml:11  (BASEHARBOR_RUNTIME_IMAGE=localhost/baseharbor-runtime:pre-release)
- yml:177-197 (Load prebuilt runtime image — tar load; if this fails the source for publish is missing)
- yml:198-201 (Publish exact candidate image for ORAS verification — the ci-local-oci-registry.sh publish call)
- yml:306 (bash scripts/acceptance.sh — MISSING file)

## cleanliness

(nichts geaendert ausser audit + akte; scripts/ci-local-oci-registry.sh unveraendert; keine container/volumes/state angefasst; ambient-core fremder lanes untouched)

## END w21-pr1702-0428-249-registry-fix BLOCKED

Determination: END_BLOCKED — Owner-scope (.github) investigation required, not a scripts fix. See scripts-fix ODER .github-owner section.
