# PR #1575 Review R5

## PLAN

1. Verify exact PR #1575 r5 head/base ancestry, own-commit log, live PR state, and specified hosted run.
2. Recheck r1-r3 findings individually: manifest grounding, three status states, genuine CLI cells, positive assertions, and unknown-owner fail-closed.
3. Check documentation consistency with PR #1577 and record a SHA-specific verdict in planning evidence.
4. Run planning validation, publish evidence to origin/main, verify remote presence, and post END.

## Exact candidate and provenance

Role: CODEX-REVIEW r5; no merge. Live product witness from a fresh clone at `/tmp/opencode/mission-rev1575-r5-wt`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
792c921cbcdb87158aa9abfbd28e2f266a44af5a	refs/pull/1575/head
29dba54dddb02f48568c571e9ce37f671d21e6aa	refs/pull/1577/head
```

PR #1575 is OPEN and DRAFT, base `develop`, branch `lane-0428-075-perses-seam`, exact head `792c921cbcdb87158aa9abfbd28e2f266a44af5a`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 792c921cbcdb87158aa9abfbd28e2f266a44af5a` succeeded. `git log --oneline 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..792c921cbcdb87158aa9abfbd28e2f266a44af5a` lists only this chain's four commits:

```text
792c921c ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2 test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa1 feat(0428-075): define optional Perses provider seam (fail-closed)
```

The r4 commit parent is `c195a9a2049253accdf57a082e6eb33fc36ec7dd`; both commits have identical tree `949f2991995582854e53447ec2a7f5b795821247`. `git diff --stat c195a9a2049253accdf57a082e6eb33fc36ec7dd 792c921cbcdb87158aa9abfbd28e2f266a44af5a` is empty. Thus r5 contains no code or test correction beyond r3, despite the round-5 note claiming the r4 commit carries a positive assertion.

## Hosted run

Run `43651763019` is terminal `completed/success`, event `pull_request`, workflow `CI · Source & Quality`, exact head `792c921cbcdb87158aa9abfbd28e2f266a44af5a`. Active `PR · Draft source and routing`, `PR · Draft Go · cli-0/1/2/3`, and `PR · Draft Go · packages` jobs all passed. Other selected/release jobs were skipped under draft selection. No failing check was observed and no rerun or workflow dispatch was started in this review.

## R1–R3 findings rechecked

### Manifest grounding — addressed

`PersesManagementSurfaceNow(selected)` uses manifest selection plus a validated pinned release to set `Provisioned`; `ApplicationManagementUISurfaces` adds the observability entry only when `ObservabilityManagementUI && Perses` (`internal/capability/perses.go:126-169`; `internal/application/management_ui.go:401-414`). The CLI tests exercise selected and unselected manifests through `runWithIO` and positively require or reject the corresponding surface (`cmd/baha/app_perses_cli_test.go:155-189,191-222`). This resolves the original compile-time-default-only grounding finding.

### Configured versus reachability; required three states — still blocking

The internal `PersesManagementSurface` separates `Provisioned` from a `Reachability` string, but its only reachability constant is `unverified`; no real Perses health path or verified transition exists (`internal/capability/perses.go:118-169`; `internal/metrics/management_ui.go:89-100`). More importantly, `ApplicationManagementUISurfaces` discards both fields and exposes only service, purpose, URL, authentication and auth class (`internal/application/management_ui.go:401-412`). The public `baha status --json` test model also has no configured/provisioned or reachability field (`cmd/baha/app_perses_cli_test.go:28-49`). It therefore does not expose the required three distinct states: not configured; configured with reachability unverified; verified only after a real health path.

There is also a false-ready path. `VerifyManagementUIAt` dispatches selected Perses to `VerifyPersesManagementUIAt`, which only validates the pinned release and returns nil (`internal/metrics/management_ui.go:55-61,89-100`). `collectManagementUICheck` passes that nil result to `record`, which marks the management UI check ready and supplies a detail claiming the Prometheus management UI is reachable (`cmd/baha/app_status_collect.go:359-367,450-472`). A declaration-only check cannot establish runtime reachability.

### Genuine CLI entry — present, but its asserted Perses state is incomplete

R3 does execute public `baha status --json` and `baha app status --json` through `runWithIO`; the unknown-owner test also executes the production `app status` and `app show` paths. This resolves the earlier helper-only/no-op CLI finding (`cmd/baha/app_perses_cli_test.go:51-66,224-262,268-355`).

### Positive assertion and vacuity — still blocking

`assertPersesSurfaceUnverified` does not require a Perses surface, an explicit `reachability=unverified` value, or even one management-UI check. It only rejects a matching check if that check happens to be `ready`/`verified` (`cmd/baha/app_perses_cli_test.go:80-103`). The selected test separately asserts that a surface exists, but the public surface has no reachability field. `persesProbeApp` writes manifest/compose/env/deployment state but starts no runtime (`:110-152`); `finishApplicationStatusCollection` returns immediately with state `stopped` when components are stopped, before managed-service checks run (`cmd/baha/app_observe.go:57-68`). Consequently the no-ready-check loop can still pass with no checks at all and cannot detect the false-ready path above. The round-4/5 claim that the positive non-vacuous assertion is present is contradicted by the exact tree at `792c921`.

### Unknown owner fail-closed — addressed

`TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI` removes the deployment identity sources, then requires repository status to fail with no JSON report, UUID status to fail on the orphan, and name-resolved `app show` not to invent an owner. It also checks the display registry reports an ownerless damaged entry (`cmd/baha/app_perses_cli_test.go:268-355`). This is a substantive positive negative-case assertion, not helper-only coverage.

## PR #1577 documentation consistency — blocking mismatch remains

Current #1577 head is `29dba54dddb02f48568c571e9ce37f671d21e6aa`, OPEN/DRAFT. Its English release note says a selected but unprovisioned Perses surface is `unsupported` “never as configured” and that no release reports it provisioned when it is not (`docs/releases/v0.4.28.md:15`); German release wording is equivalent (`docs/de/releases/v0.4.28.md:15`). English and German release references also say selected-but-unprovisioned is `unsupported` rather than configured (`docs/reference/releases.md:31`; `docs/de/reference/releases.md:30`).

That wording still conflicts with #1575's `Provisioned=true` for manifest-selected plus valid pinned declaration, even though #1575 internally labels reachability `unverified`. #1575 itself does not update release-note wording. #1577 remains WAITING until the wording explicitly distinguishes declaration/configuration from actual provisioning and health-verified reachability. Do not approve either candidate on the current prose.

## Verdict and correction recipe

REJECT exact candidate `792c921cbcdb87158aa9abfbd28e2f266a44af5a`. Blocking findings: the public status does not expose the required three states; pin validation can become a ready/reachable check without a health path; the purported positive assertion remains vacuous about reachability and the test fixture exits before checks; #1577 wording still conflicts with declaration-based configuration. Manifest grounding, genuine CLI dispatch, and unknown-owner fail-closed coverage are present. The exact-head hosted run passed but does not resolve these contract defects.

Correction recipe: expose exactly `not configured`, `configured / reachability unverified`, and `verified`; make only an actual Perses health-path success produce `verified`; never map release-pin validation to ready. Exercise the non-stopped public status path and assert the explicit configured/unverified state plus a present, non-ready/unverified check; include a verified case only through the real health path. Preserve the existing unknown-owner negative test. Align #1577 EN/DE release and reference wording with declaration versus runtime semantics. Keep all tests in the existing `cmd/baha` CI selection (`PR · Draft Go · cli-0/1/2/3`, `pull_request`); no `.github/**` change is needed for the added test path.

## repo-rule compliance

Planning repository verified before this evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

The review used a fresh product clone; the quarantined stale-ref checkout was not consulted. No product files, workflow files, PR state, or CI state were changed; no local tests, reruns, workflow dispatch, containers, or merges were performed.

Planning validation: `python3 scripts/plan.py render && python3 scripts/plan.py check` reported 531 tasks, 7 epics, 13 releases, 22 decisions; 0 errors and 12 dependency warnings.

Planning `origin/main` exact `git ls-remote` witness before the evidence commit:

```text
e6f233ab9a91353ef0147ef3319ea88d3cb72dc8	refs/heads/main
```

## END DONE
