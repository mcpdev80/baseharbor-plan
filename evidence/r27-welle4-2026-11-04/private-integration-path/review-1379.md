# CODEX-REVIEW — PR #1379 (read-only)

Verdict: **REJECT** — exact reviewed head `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`.

## Switch and counter-probes

The PR API head and remote ref `work/r27-private-integration` both match `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`. Against its stated base `e444ae117173dcf84e7aa8b17f73c020d3e2923c`, the write set is eight files: `internal/application/manifest.go`, `manifest_parse.go`, `provider_placement.go`, `r27_private_integration_test.go`, `cmd/baha/use_target.go`, `cmd/baha/use_target_connection_test.go`, `internal/coreinstallation/selection.go`, and `selection_test.go`. The candidate's switch is `runtime.private: true`; `ResolveConfiguredProviderPlacement` forces SQL and Valkey to application scope while the default remains shared. The manifest parser only accepts the explicit boolean under `runtime:`.

Both requested directions were independently exercised at the exact candidate head with `go test ./internal/application -run '^TestPrivateIntegration_' -count=1 -v`: all four tests passed. Without the switch, the fixture resolves to `sql/shared` and SQL/Valkey remain shared. With the switch, both providers use application scope and the routing helpers report no shared backends. The counter-probes reject an implicit `profile` key and verify the default manifest remains non-private. This supports the requested switch behavior; the host-level positive application cycle is not claimed by this review.

Base drift is listed as requested, not treated as a recipe constraint: since the PR base `e444ae11`, current develop includes `512dcd72` (#1378), `3b5974ca` (#1382), `1a84726d` (#1369), `c762022e` (#1381), `0476164a` (#1362), and `24c7d049` (#1371). The current remote develop ref is `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`.

## Gate finding

The exact-head PR workflow run `41913050087` is terminal overall success, but its `PR Selected Checks` job is **skipped**, not success; only source-format and workflow-policy jobs passed. Therefore the required candidate check is not evidenced green at this SHA. The worker's earlier success on `efadde8` is stale and cannot qualify this changed head.

## Recipe

- **Files:** workflow selection/configuration only if the skipped context is caused by candidate selection; otherwise no product-code change is needed.
- **Change:** obtain a terminal `PR Selected Checks` success on this exact head through the repository's normal PR workflow. Do not count an overall-success run whose required job is skipped.
- **Test requirement:** verify the run's head SHA is exactly `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`, and the named check concludes success from integration 15368; retain the local private/default counter-probes.
- **Stop criterion:** if the exact-head selected check remains skipped, or either mode no longer resolves to its expected scope, do not accept.

No PR, branch, or card action was taken.
