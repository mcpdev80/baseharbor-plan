
## Product-GAP aufgedeckt (2026-10-31, gh-acc-suite PR #1238)
Control-Plane docker-only + podman-only acceptance Step10 -> inspectTargetDockerEngine (docker-only) fails.
Vorbestehende Luecke, out-of-scope der Migration -> eigener Fix (app/doctor Engine-Erkennung runtime-neutral).
Produkt-Sprache: "BaseHarbor erkennt das Laufzeit-Backend falsch, wenn Control-Plane und Test-Runtime (docker vs podman)
nicht uebereinstimmen." Lane: product-gap-engine (App/Doctor Write-Set, disjunkt von CI/openbao).

## (2026-10-31) runtime-neutral engine detection #1241 code-ready (accepted, runtime rides GH-hosted HA gate)
gh-dispatch-runtime END_BLOCKED waiting on gh-ci-core (rootless docker provisioning in ci-core-rootless-runtime.sh on ubuntu-latest). gh-ci-core = jetziger Linchpin.
## #1160 dep-bump (2026-11-01): rebased 6389342d, build/test clean, mergeable; aggregate red nur wg.
   native-HA-skipped/coverage (dasselbe Endpoint/CI-Gate-Loch). Wartet auf Endpoint-Fix + CI-Etablierung wie der Rest.
## #1243 broker+s3 acceptance GH-hosted (2026-11-01, verified self-hosted=0, mergeable=true; native green gated on endpoint fix)
## #1240 sslmode regression-guard ACCEPTED (2026-11-01, coord eigenverifiziert): neuer Head 116adb3d auf
   work/o1249b-openbao-cauth; additive openbao_sslmode_guard_test.go (+84, liest echte Quelle, lehnt off/trust/
   verify-none/disable ab, verlangt positiv verify-ca im Code + Init-Skript). Coordinator-Run: go test PASS (0.009s).
   review-A Rezept Pkt2 damit erfuellt; Pkt1 (coverage-resolved) bleibt am Endpoint-Gate haengen. PR #1240 =
   CODE-ready, mergeable nur nach echtem gruuen GH-hosted native-qualification-Lauf.
## Node-Connector CI cutover DONE (2026-11-01): PR #17 MERGED, nc main=188036f, self-hosted=0, GH-hosted
   transport·podman SUCCESS (rootful) witnessed. nc-Repo 100% GitHub-hosted. review-nc=APPROVE-FEIER-GRUEN.
## podman-gh #1244 (2026-11-01, CODE-ready): scripts/ci-podman-gh-runtime.sh rootful + Podman-HA-Prepare umgestellt.
   Bewiesen auf GH-hosted: Setup-Schritt setzt CONTAINER_HOST=unix:///run/podman/podman.sock + Job laeuft weiter
   (podman rootful funktioniert). Job-Rot nur wegen "Resolve HA group" exit 2 — Branch-Name "work-podman-gh" kein
   erlaubter HA-Gruppenname (Dispatch-Artefakt, kein Podman-Fehler). Merge-Status wie #1243: native PR-Gate (Rule 7),
   nicht Code-Fehler.
## Ruleset/Erzwingungs-Inventur (2026-11-01, BEWIESEN): baseharbor/develop hat GENAU 1 Required-Check
   `PR Selected Checks` = ubuntu-latest (ci.yml:811) -> bereits GH-hosted, 0 umzustellen. main + nc: keine
   Required-Checks (nc Rulesets [], Protection 404). self-hosted `validate` (ci.yml:275) ist push-only & NICHT
   required. 3 online self-hosted Runner dienen nur noch PUSH/DISPATCH-Acceptance (podman-acceptance.yml:36 etc.)
   -> die migrieren #1239/#1238/#1243/#1244. => ERZIEHUNGS-/Pflicht-Seite des Cutover ist faktisch erfuellt; der
   Rest ist Coverage-Klassifizierung (gate-map) + echte native Laeufe. #1239 echt auf develop rebased (develop Ahn).
## gh-ci-core SCOPE ACCEPTED (2026-11-01): #1239 rebased auf develop (head 486abbca, mergeable), Skript nutzt
   SYSTEM-daemon (kein rootless-socket-export), DOCKER_MODE nicht mehr verhaltenssteuernd. validate rot NUR weil
   #1245 noch nicht in develop (Alter Resolver => compose-tests sehen /run/user/1001). Kein Fehler in #1239.
   Aufloesung via kombinierter Kandidat (native-probe) = genau die vom Worker korrekterweise ans Coordinator-
   Integration verwiesene Stelle. Merge-Reihenfolge bleibt: gate-map -> kombinierter Kandidat (#1245+#1239) -> Rest.
## Keystone gate-map #1246 MERGED (develop 437358e4). Docker-Beweislauf deckte Rest-BUG in #1245 auf:
   rootlessCapable() false-positiv auf GH-hosted (liest unprivileged_userns_clone, fehlt auf Ubuntu; AppArmor
   blockiert userns real) -> hostDefaultEndpoint waehlt toten /run/user/1001 statt System-daemon. endpoint-refine
   (qwen) fixt das in #1245 + erzwingt gruenen nativen docker-HA-Lauf auf develop+fix+#1239. PODMAN ist bereits
   BEWIESEN gruen auf GH-hosted (Targeted runtime podman=success, ubuntu-26.04, run 41267346809).
## Node-Connector 100% GH-hosted BESTAETIGT (2026-11-01, coord-verifiziert): alle runs-on GH-hosted; der
   loginctl/rootless-Code steckt NUR im `RUNNER_ENVIRONMENT != github-hosted`-Fallback (laeuft auf GH-hosted nie);
   GH-Pfad nutzt rootful/cgroupfs podman + fails closed (exit1). nc-Repo: 0 self-hosted Runner. nc-Cutover KOMPLETT.
