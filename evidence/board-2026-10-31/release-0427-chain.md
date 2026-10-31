
## Product-GAP aufgedeckt (2026-10-31, gh-acc-suite PR #1238)
Control-Plane docker-only + podman-only acceptance Step10 -> inspectTargetDockerEngine (docker-only) fails.
Vorbestehende Luecke, out-of-scope der Migration -> eigener Fix (app/doctor Engine-Erkennung runtime-neutral).
Produkt-Sprache: "BaseHarbor erkennt das Laufzeit-Backend falsch, wenn Control-Plane und Test-Runtime (docker vs podman)
nicht uebereinstimmen." Lane: product-gap-engine (App/Doctor Write-Set, disjunkt von CI/openbao).
