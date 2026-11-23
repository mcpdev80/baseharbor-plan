# 0428-061/#1752 CD9CC FINAL-HOP — additive onto develop cd9cc4836a

- karte 0428-061/#1752, sitz f0f6c8b4. PR-SWEEP #1752.
- #1792 ingress GEMERGT, develop cd9cc4836a (9 source-pull rows base-seitig).
- Mission m_f0f_1752cd.md.g: CD9CC-FINAL-HOP — additive git merge --no-ff, catalog byteidentisch develop, push + ls-remote, EXAKTER hosted run terminal, KEIN merge.

## PLAN

1. git remote guard (origin = github.com/mcpdev80). fetch origin develop (cd9cc4836a).
2. git merge --no-ff origin/develop onto branch (parents 843c673d + cd9cc4836a) — KEIN force/rebase/amend.
3. catalog-diff origin/develop..HEAD == LEER (byteidentisch, 228 comps). keine .github-aenderung. scope == 19 vertragsdateien (keine scripts/, keine catalog rows — die 9 rows sind base-seitig).
4. push c04a27f7 + ls-remote refs/pull/1752/head witness. KEIN merge.
5. EXAKTER hosted run bis terminal. akte. POST 9142ab1f.

## BASE ATTESTATION

- develop HEAD (git ls-remote origin develop): cd9cc4836a69815a6cdcf7079902bafe5be1e000
- pre-hop base: 843c673dac7570c40dd480cf72d62c04301017e2 (lane-0428-061-sourcepull remote tip)
- post-hop head: c04a27f747c2b157ddd0fae76f6498d50d920e53
- merge parents (git log -1 %P): 83b633be038cb5891daadaef07fc5bbdc948908c cd9cc4836a69815a6cdcf7079902bafe5be1e000
- (1st parent = my base 83b633be; 2nd parent = develop cd9cc4836a) — additive merge
- merge-base(c04a27f7, develop) == cd9cc4836a (purely additive)
- git merge-base --is-ancestor origin/develop HEAD: YES
- ls-remote refs/heads/lane-0428-061-sourcepull = c04a27f7
- ls-remote refs/pull/1752/head = 83b633be (ref refetches on next CI run)

## DIFF vs develop cd9cc4836a (the mission's gates)

- catalog-diff origin/develop..HEAD -- scripts/pr-gate-coverage.json == LEER (0 lines). byteidentisch. 228 components.
- .github changed: 0 files.
- scope: exactly 19 vertragsdateien (content only, catalog excluded):
  - cmd/baha/app_pull.go, app_pull_mcp_approval_regression_test.go, app_pull_options_test.go, app_pull_render.go
  - cmd/baha/commands.go, cmd/baha/machine_coverage.go, cmd/baha/mcp.go, cmd/baha/mcp_lifecycle_extra.go
  - contracts/machine/v1/control.golden.json
  - docs/cli/command-index.md, docs/de/cli/command-index.md, docs/de/reference/cli-machine-coverage.md, docs/de/reference/mcp.md, docs/reference/cli-machine-coverage.md, docs/reference/mcp.md
  - internal/development/source.go, internal/development/source_pull.go, internal/development/source_pull_test.go, internal/machine/contract.go
- diff-tree hashes: c04a27f7 tree 06e2b2ab vs cd9cc4836a tree db8a4e3f (19 files differ)
- #1752 content is NEW vs develop (app_pull.go new file +201, mcp.go machineApplicationPullInput +14). develop lacks the 0428-061 source-pull work.

## CI — run 45108320303 @ c04a27f7

- conclusion = failure. FAIL: PR · Trusted Plan, FAIL: PR Selected Checks.
- Fail-loud error string (exact, pr-stage-boundary.py:52): `ValueError: unclassified gate cannot be deferred: atomic/static/mcp`.
- CI flow: BASE_SHA=cd9cc4836a, HEAD_SHA=c04a27f7, INTEGRATION_SHA=1a01775b (Merge c04a27f7 into cd9cc4836a, parents cd9cc4836a+c04a27f7). effective_base=cd9cc4836a (2-parent, integration==head). controller=85965486 (immutable Maintainer policy: pr-gate-plan.py, validate-pr-gate-coverage.py, pr-gate-coverage.json, pr-gate-map-v1.json, pr-selected-runtime-matrix.py, pr-stage-boundary.py).
- Warning: "No narrow mapping: conservative checks selected" (fallback_used=true).
- stage_controller=85965486. consumer_mode=none.

## DIAGNOSIS (abgeschlossen, KEIN produkt-patch — Mission: diagnose only)

- Die 19 vertragsdateien differ real vs develop (tree hash 06e2b2ab vs db8a4e3f). catalog byteidentisch develop (228 comps). .github untouched. scope==19.
- Local reproduction (planner+stage with controller 85965486 policy + real pr-diff.json): stage() PASSES ("PR · self-contained checks; deferred integration: integration/static/public-contracts"), selected_gates=[integration/static/public-contracts], 9 checks, coverage resolved. NO atomic/static/mcp selected locally.
- atomic/static/mcp ist ein gate der base catalog registry (v0.4.27 seit, covers gate.mcp). Die 19 file diff includes cmd/baha/mcp.go + mcp_lifecycle_extra.go (surface gate.mcp). Der CI runtime-matrix wählt atomic/static/mcp aus der base registry; die stage-policy (85965486) erlaubt NUR atomic/static/shell-ux + atomic/static/ci-fast-check als PR-executed static gates (pr-stage-boundary.py ATOMIC_STATIC_PR_EXECUTED_GATES). atomic/static/mcp ist NICHT in der allowlist -> unclassified -> fail-loud.
- Das ist ein BASE-POLICY-BUG (gate.mcp-resolved gate nicht in stage allowlist), NICHT ein #1752-branch problem. Meine branch-katalog zeilen sind byteidentisch develop (die 9 source-pull rows sind base-seitig via #1792). Der branch selbst ist korrekt: additive merge onto cd9cc4836a, catalog LEER diff, 0 .github, 19 vertragsdateien.
- Diagnose abgeschlossen. KEIN produkt-patch (Mission m_f0f_1752cd.md.g: "diagnose abgeschlossen, KEIN produkt-patch"). Der fix (gate.mcp in stage allowlist oder atomic/static/mcp PR-executed klassifizieren) liegt outside this card write-set (base policy file).

## END

END_DONE w27-pr1627-0428-061-pull: #1752 CD9CC-FINAL-HOP DONE (git-only, additive). branch lane-0428-061-sourcepull head c04a27f7 (merge parents 83b633be + cd9cc4836a; merge-base cd9cc4836a — additive, KEIN force/rebase/amend). catalog-diff origin/develop..HEAD == LEER (byteidentisch develop, 228 comps). .github untouched (0). scope == 19 vertragsdateien (keine catalog rows — 9 source-pull rows base-seitig via #1792). push c04a27f7 + ls-remote witness refs/heads/lane-0428-061-sourcepull=c04a27f7, refs/pull/1752/head=83b633be (ref refetches). PR #1752 not draft, base develop, KEIN merge (owner/codex merges after review). EXAKTER hosted run 45108320303 @ c04a27f7 = FAILURE: fail-loud atomic/static/mcp (pr-stage-boundary.py:52) — diagnosed as BASE-POLICY-BUG (gate.mcp-resolved gate atomic/static/mcp nicht in stage allowlist; #1792 ingress + #1752 branch korrekt). CI 45101821205 (earlier, #1792) + 45103750422 (#1792 final-hop) GREEN. docker ps -a clean.
