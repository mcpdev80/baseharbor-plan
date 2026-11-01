
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
