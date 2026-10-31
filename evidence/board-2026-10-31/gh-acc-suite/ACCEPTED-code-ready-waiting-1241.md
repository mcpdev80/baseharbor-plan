# gh-acc-suite ACCEPTED code-ready (2026-11-01, Coordinator verified)
PR #1238 (work/gh-acc-suite). Runner-Migration erfolgreich (rootless docker+podman auf GH-hosted Schritt 1-9 gruen).
Restfail Schritt 10 = `inspectTargetDockerEngine` (cmd/baha/control_plane_operations.go:153) docker-only, kein podman
Binding -> genau das Thema von #1241 (fix-engine-detect, bereits code-ready). #1238 wartet auf Merge von #1241, dann
rebase+gruen. Lane freigegeben.
