# PR #1351 Squash-Merge

ROLLE=MERGE. Autorisierung: `review-1351b.md` ACCEPT und explizite Merge-Mission. Vorher: PR OPEN, head `c83a56542493c73eb6fc35eedf53cb0bdf5dbc66`, MERGEABLE, CLEAN, keine fehlgeschlagenen Checks; `PR Selected Checks` SUCCESS, Check-App 15368, Head identisch. `git ls-remote`: develop `5813ef8581feb0cb7943038ab1c44545186f650f`, PR-Head `c83a56542493c73eb6fc35eedf53cb0bdf5dbc66`. GitHub-Identität `mcpdev80`; Branch-Rules-API meldete keine aktiven Regeln.

`gh pr merge 1351 --squash --match-head-commit c83a56542493c73eb6fc35eedf53cb0bdf5dbc66` erfolgreich, Exit 0, ohne `--admin`. GitHub danach: state MERGED, mergedAt `2026-11-03T14:24:34Z`, mergeCommit `0107d8e1530ff3469048022d7035a2a472dbda34`. `git ls-remote` bestätigt develop `0107d8e1530ff3469048022d7035a2a472dbda34`; `git fetch origin develop` und `git rev-parse FETCH_HEAD` bestätigen dieselbe SHA.

Diffproof: `git diff --exit-code c83a56542493c73eb6fc35eedf53cb0bdf5dbc66 FETCH_HEAD -- internal/testsupport/externalprovider/seed.go cmd/baha/provider_external_removal_test.go` leer, Exit 0.

Nach Merge im sauberen Archiv des neuen develop: `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp/opencode XDG_DATA_HOME=/tmp/bh1351merged-data XDG_CONFIG_HOME=/tmp/bh1351merged-config go test ./cmd/baha -run TestExternalProviderRemoval -count=1 -timeout 8m` PASS (0.062s). Planning-Abschluss durch zuständigen Coordinator.
