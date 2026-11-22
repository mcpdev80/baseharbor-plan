# 0428-249 runtime-image registry gap characterization - characterize-round-1 akte

Sitz `w21-pr1702-0428-249-runtime-image`. Karte 0428-249, owner-order. READ-ONLY charakterisierung, develop 676909a7, KEINE aenderung/commit/push/subagent.

Kontext: (#1773/246 ist geblockt bis #1774 landet; das hier ist die neue fuelle). FUND (owner, #1746 pre-release 45028181619 light-runtime zellen): 'local registry blob/manifest unknown' fuer bild baseharbor-runtime. Owner will das ALS EIGENES bild-artefakt/registry problem erfasst, NICHT verwechselt mit operator-auth.

Ziel: EXAKTE referenz die light-runtime zellen ziehen + wo es gebaut/gepusht werden soll (scripts/ci-native-pr-gate.sh image-build vs registry publish); klassifizieren A (gleich wie 237, ein fix loest beide) ODER B (eigener registry-push/blob gap, eigene PR noetig).

## PLAN

- plan in board-file + ## PLAN in akte
- develop fetchen (refs/heads/develop), HEAD-sha in akte; NUR lesen (git show/grep/rg, ggf. read-only durchgang)
- exakte image-ref der light-runtime zellen locate (localhost/... baseharbor-runtime:<tag>?) + build/publish ort (scripts/ci-native-pr-gate.sh image-build vs registry publish); cite datei:zeile
- bestimmen ob same moving-edge vs SHA-pinned fall wie 0428-237/#1770 ODER eigener registry-push/blob gap; begrundung datei:zeile + fehlendes manifest/age
- klassifizieren A (gleich wie 237 - one fix resolves both) ODER B (eigener registry/artefakt-schritt fehlt - own PR); key datei:zeilen
- cleanliness (nichts geaendert; keine eigenen container/volumes); 9142ab1f posten; keine subagenten

## Fund (owner #1746, pre-release 45028181619, light-runtime zellen)

- error: 'local registry blob/manifest unknown' fuer bild baseharbor-runtime

## Befunde

develop HEAD: 3cbb2bac39996391799d1c6460b230979ee34959 (git ls-remote origin refs/heads/develop; mission target 676909a7 was HEAD earlier, develop has since advanced via forced update)
run 45028181619: Pre-Release · v0.4.28 (workflow_dispatch), head 887058a6a824af3a65fd987cbab5b5c60f625075, conclusion cancelled (no per-job FAILURE rows in the run — the owner's blob/manifest error was observed in the light-runtime zellen during the same pre-release, before cancellation)

### B1 — EXAKTE referenz die light-runtime zellen ziehen (datei:zeile)
- BASEHARBOR_RUNTIME_IMAGE in der Atomic Acceptance Gate = localhost/baseharbor-runtime:pre-release  (pre-release-runtime-suite.yml:11, env for every native gate cell)
- Der ORAS-verification target (das was ORAS resolves) = localhost:5000/baseharbor-runtime:pre-release  (pre-release-runtime-suite.yml:201: `bash scripts/ci-local-oci-registry.sh publish "$BASEHARBOR_RUNTIME_IMAGE" localhost:5000/baseharbor-runtime:pre-release`)
- Der ORAS resolve wird getrieben durch pullResolvedRuntimeImage(ctx, compose, location, requested) mit location = os.Getenv("BASEHARBOR_RUNTIME_IMAGE")  (cmd/baha/app_broker.go:80-87)
- ORAS selbst: `oras resolve <ref>` (cmd/baha/application_registry_source.go:389 `s.run(ctx, "resolve", ref)`); der 'local registry blob/manifest unknown'-error kommt aus dem ORAS-Exit/Response, klassifiziert als ErrRegistrySourceUnavailable  (cmd/baha/application_registry_source.go:36-39, 22)

### B2 — wo es gebaut/gepusht werden soll (image-build vs registry publish) (datei:zeile)
- RELEASE/PUBLISH eines immutable runtime images nach ghcr (edge + sha-<short> + stable tags): .github/workflows/runtime-image.yml (job build; docker/login-action@ghcr; build-push-action push:true tags edge/sha-/stable; attest to-registry)  (runtime-image.yml:95-131)
- DEFAULT_IMAGE = "ghcr.io/mcpdev80/baseharbor-runtime:edge"  (internal/runtimebroker/broker.go:23)
- IN DER LIGHT-RUNTIME ZELLE: kein ghcr-pull. Das Bild wird LOCAL gebailed/gebupt:
  - "Load prebuilt runtime image" lädt eine vor gebaute tar-archive (pre-release-candidate/baseharbor-runtime-pre-release.tar) via docker/podman load  (pre-release-runtime-suite.yml:177-197)
  - "Publish exact candidate image for ORAS verification" taggt das lokale image und pusht es in die isolated localhost:5000 registry  (pre-release-runtime-suite.yml:198-201; scripts/ci-local-oci-registry.sh:22-42)
  -> Die light-runtime zellen ziehen NIEMALS ghcr; sie ziehen das lokal gebaute pre-release image (localhost/baseharbor-runtime:pre-release) und verifizieren es via ORAS gegen localhost:5000/baseharbor-runtime:pre-release

### B3 — moving-edge (ghcr :edge) vs SHA-pinned (ghcr :sha-<commit>) — der mechanismus (datei:zeile)
- defaultRuntimeImage(version): dev/dirty -> edge; sonst versionTag; -> ghcr.io/mcpdev80/baseharbor-runtime:<edge|version>  (cmd/baha/main.go:117-123)
- ensureMatchingDevelopmentRuntimeImage (cmd/baha/development_runtime_image.go:25-88): nur wenn (a) image == ghcr...:edge UND (b) commit ist ein 40-hex SHA UND (c) BASEHARBOR_RUNTIME_IMAGE != edge-manuel: dann wird das installed baha binary in ein localhost/baseharbor-runtime:dev-<sha256> image gebaut (lokal, CGO) — kein ghcr-pull. Das ist die DEV-only SHA-nahe reproduktion.
- IsMutableDevelopmentImage(image) == (image == ghcr...:edge)  (internal/runtimebroker/broker.go:30-32); refreshMutableImage triggert pullResolvedRuntimeImage(..., runtimeImage, "edge")  (cmd/baha/app_broker.go:84-88)
- pullResolvedRuntimeImage: ORAS resolve -> unverifizierbare/digest-mismatch = HARD REJECTION (ErrRegistryUnverifiable), NUR ErrRegistrySourceUnavailable + BASEHARBOR_ALLOW_MUTABLE_DEVELOPMENT_IMAGE opt-in zieht den mutable edge-tag; public-default/denial/unverifiable sind fail-closed  (cmd/baha/application_registry_source.go:60,315-357)
- 0428-237/#1770 war der fix der die SHA-pinned vs moving-edge disambiguierung eingefueht hat (development_runtime_image.go:23-29 dokumentiert: "cannot consume an unrelated moving edge build"); das ist die ghcr :edge vs :sha-<commit> frage

### B4 — der fehlende schritt / manifest (der eigentliche fund)
- Der ORAS 'local registry blob/manifest unknown'-error ist KEIN operator-auth problem (operator-auth ist eine eigene fehlerklasse errClassDenied, application_registry_source.go:330-345) — es ist ein registry-artefakt problem: localhost:5000/baseharbor-runtime:pre-release konnte nicht ORAS-resolved werden, weil das image NICHT in die localhost:5000 registry gepupt wurde (ci-local-oci-registry.sh publish) ODER die tar-vorlage (pre-release-candidate/baseharbor-runtime-pre-release.tar) fehlt/leer ist.
- die "Publish exact candidate image for ORAS verification"-stufe (pre-release-runtime-suite.yml:198-201) ist die letzte vor dem ORAS-resolve; wenn hier tag/push fehlt oder die source-image inspect (docker inspect BASEHARBOR_RUNTIME_IMAGE, yml:196) schon fehlschlaegt, ist der blob/manifest error die direkte consequence.
- BEGRUNDUNG datei:zeile: pullResolvedRuntimeImage yml-201-publish -> ORAS resolve application_registry_source.go:389 -> ErrRegistrySourceUnavailable application_registry_source.go:22/39; operator-auth class errClassDenied ist getrennt application_registry_source.go:330-345 -> NICHT verwechselt mit operator-auth

## Klassifikation A/B

B = EIGENER registry/artefakt-schritt fehlt (NICgleich-wie-237).

- 0428-237/#1770 (B-Alternative): ghcr :edge vs :sha-<commit> moving-edge disambiguierung — ein fix loest beide. Das ist die SHA-pinned-vs-moving-edge frage in development_runtime_image.go / defaultRuntimeImage / IsMutableDevelopmentImage.
- 0428-249 fund: localhost:5000/baseharbor-runtime:pre-release ORAS 'local registry blob/manifest unknown' — ein REGISTRY-PUSH/BLOB gap in der atomic acceptance gate (ci-local-oci-registry.sh publish, pre-release-runtime-suite.yml:198-201) oder eine fehlende/leere prebuilt tar (yml:177-197). Das ist ein SEPARATER schritt (registry publish) von der ghcr edge/sha disambiguierung.
- EIN fix loest BEIDE NICHT: 237 patcht development_runtime_image.go (ghcr dev sha); 249 muss in der pre-release atomic-acceptance-image-pipeline (ci-local-oci-registry.sh / pre-release-runtime-suite.yml:177-201) ansetzen. -> eigene PR noetig (B).
- OWNER-Wunsch bestaetigt: "ALS EIGENES bild-artefakt/registry problem erfasst, NICHT verwechselt mit operator-auth" — B bestaetigt (registry/artefakt-schritt, nicht operator-auth class).

## Klassifikation A/B

(to be filled: A gleich-wie-237 ODER B eigener-registry-gap)

## cleanliness

(nichts geaendert; keine eigenen container/volumes/state angelegt; ambient-core fremder lanes untouched)

## END w21-pr1702-0428-249-runtime-image DONE

- develop HEAD (witness): 3cbb2bac39996391799d1c6460b230979ee34959 (git ls-remote origin refs/heads/develop; mission target 676909a7 was HEAD earlier)
- run 45028181619: Pre-Release · v0.4.28 (workflow_dispatch), head 887058a6a824af3a65fd987cbab5b5c60f625075, cancelled
- klassifikation: B = EIGENER registry/artefakt-schritt fehlt (NOT A/gleich-wie-237); eigene PR noetig
- image-ref die light-runtime zellen ziehen: BASEHARBOR_RUNTIME_IMAGE=localhost/baseharbor-runtime:pre-release (pre-release-runtime-suite.yml:11); ORAS target=localhost:5000/baseharbor-runtime:pre-release (pre-release-runtime-suite.yml:201)
- build/publish ort: release/ghcr = runtime-image.yml (edge+sha+stable, docker/login-action@ghcr, build-push-action push:true); light-runtime zelle = prebuilt tar load (pre-release-runtime-suite.yml:177-197) + ci-local-oci-registry.sh publish (pre-release-runtime-suite.yml:198-201, ci-local-oci-registry.sh:22-42) — kein ghcr-pull
- key datei:zeilen: cmd/baha/app_broker.go:80-87 (pullResolvedRuntimeImage location=env), cmd/baha/application_registry_source.go:389 (oras resolve -> ErrRegistrySourceUnavailable), cmd/baha/application_registry_source.go:22/330-345 (unavailable vs errClassDenied getrennt -> NICHT operator-auth), internal/runtimebroker/broker.go:23/30-32 (DefaultImage edge + IsMutableDevelopmentImage), cmd/baha/main.go:117-123 (defaultRuntimeImage), cmd/baha/development_runtime_image.go:23-88 (ghcr dev-sha path = 237 area), runtime-image.yml:95-131 (ghcr publish)
- begrundung B: ORAS blob/manifest error = registry-push/blob gap in atomic acceptance image-pipeline (ci-local-oci-registry.sh publish / pre-release-runtime-suite.yml:198-201), separate von 237 ghcr edge/sha disambiguierung; ein fix loest beide NICHT
- owner-wunsch bestaetigt: als bild-artefakt/registry problem erfasst, NICHT operator-auth
- keine eigenen container/volumes/state angelegt; ambient-core fremder lanes untouched
