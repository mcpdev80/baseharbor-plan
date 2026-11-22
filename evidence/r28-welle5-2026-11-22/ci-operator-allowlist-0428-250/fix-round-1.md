# 0428-250: CI-operator fixture allow-list diagnosis + fix

- karte 0428-250, sitz f0f6c8b4. TEST-ONLY CI-operator fixture allow-list. develop HEAD 3cbb2bac39996391799d1c6460b230979ee34959 (current origin/develop; branch lane-0428-250-ci-operator-allowlist cut from it, merge-base confirmed: origin/develop is ancestor of HEAD).
- Basis: my H-V30 finding B. static/core-bootstrap gaeten (init, up-as-bootstrap, config-matrix, reference-journey, shell-ux) fail 'missing authenticated BaseHarbor operator' because their command forms are NOT admitted by the synthetic-operator allow-list in cmd/baha/ci_integration_operator_enabled.go, OR the binary is built without build tag baseharbor_ci_operator_testonly.
- Write set (per mission): ONLY cmd/baha/ci_integration_operator_enabled.go (+ tagged analog disabled file if needed). NO product operatorauth/mcp.go boundary change; NO .github; NO #1771 local-workload layer; NO target.create (0428-247).
- Remote guard: all remotes -> https://github.com/mcpdev80/baseharbor.git; used github.com/mcpdev80 remote. Method: read-only git show/grep/rg + gh api on develop 3cbb2bac and demo develop. No git write for product beyond the ONE allowed file. No subagent, no merge, no comment.

## PLAN

1. Establish reality (remote guard, branch from develop, merge-base). No product write.
2. Diagnose: trace which command forms of the static/core gaeten fall outside the synthetic-operator allow-list and why the operator is not stamped. Determine whether the cause is (a) a baseharbor allow-list gap (in my write-set) or (b) a demo-invocation gap (env var / build-tag) that is OUT of my write-set and must be an OWNER point.
3. If (a): add the missing forms to ci_integration_operator_enabled.go WITHOUT weakening the boundary. If (b): report the exact demo file:zeile as an OWNER point and do NOT edit demo files.
4. Regression witness: show a previously-failing static zelle (config-matrix core-up) that the operator is now stamped (trace witness) and it would pass. Run exact-hosted if lane-startable; else document the trace witness.
5. Write akte + fix-Art line + END + cleanliness. Publish to baseharbor-plan origin/main (ls-tree verify). Post to coordinator.

## Diagnose (read-only, file:line)

The synthetic operator is stamped by `withCIIntegrationOperator` (cmd/baha/ci_integration_operator_enabled.go:24-119) ONLY when `DEMO_ATOMIC_GATE=1` AND the binary carries the `baseharbor_ci_operator_testonly` tag (non-tagged build is the no-op ci_integration_operator_disabled.go:10). It then flows through `ciIntegrationManagedLocalGateReason` (:96-199), which admits a command to the synthetic operator via an EXACT allow-list (12 `managedWorkload = true` exceptions):

- ciIntegrationReadOnlyStatus (:116) — bare read-only status/show
- guided dev-domain/new/edit/footprint/MCPServe (:123,129,132,135,141) when `GATE == "guided"`
- observability log-probe (:148) when `GATE == "observability"`
- ciIntegrationReadOnlyDoctor (:155) — `doctor` / `doctor --json` / `doctor --output json`
- ciIntegrationRootInit (:161) — exact `baha init` (1 arg)
- ciIntegrationRootDestroy (:166) + ciIntegrationRootDestroyPreview
- ciIntegrationLocalCoreBootstrap (:78,304-352) — `baha up --yes [--json]` against a fresh `baseharbor-core-bootstrap.*` project root
- ciIntegrationTargetCreate (:87,352-369) — `baha target create <atomic-<runtime>-<gate>>` before Core exists
- target-or-gate pre-guard (:101-108): `target.Name == "atomic-"+runtime+"-"+gate` AND `BASEHARBOR_TARGET == atomic-<runtime>-<gate>` AND access `local` AND tenant unset AND runtime provider matches.

The demo harness (baseharbor-demo tests/acceptance.sh:248, :279) runs each gate script; in atomic mode every gate EXCEPT guided/config-matrix/init/mcp/agent goes through atomic-bootstrap.sh (:279), which:
- atomic-bootstrap.sh:14 runs `baha target create "$BASEHARBOR_TARGET" --provider <rt> --access local-<rt> --reference local --scope default --default` -> admitted by ciIntegrationTargetCreate (selectedTarget recovered from the gate/runtime pair, :352-369).
- atomic-bootstrap.sh:16 runs `tests/core-bootstrap.sh`.
- core-bootstrap.sh:9 sets `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$core_root"` where `$core_root` is `mktemp -d .../baseharbor-core-bootstrap.XXXXXX` -> its `baha up --yes` (core-bootstrap.sh:10) IS admitted by ciIntegrationLocalCoreBootstrap (prefix `baseharbor-core-bootstrap.` matches :329-330). -> operator stamped, core-bootstrap passes.

THE GAP (concrete, named, file:line): `tests/config-matrix/run.sh` does NOT set `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT`. Its core-up runs (`config-matrix/run.sh:30`, `:61`) inside `bootstrap_root="$matrix_root/control-plane"` where `matrix_root="$(mktemp -d "$DEMO_ROOT/.config-matrix.XXXXXX")"` (config-matrix/run.sh:9). So the `baha up --yes` cwd base prefix is `.config-matrix.<rand>` (or `control-plane`), NOT `baseharbor-core-bootstrap.`. ciIntegrationLocalCoreBootstrap (:327-330) requires either `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` set with a `baseharbor-core-bootstrap.` prefix, OR `GATE == "guided"` (which config-matrix is not) -> returns `false`. The command then falls through :78-90, is not a target create, and `withCIIntegrationOperator` returns the UNSTAMPED `ctx`. The managed boundary (mcp.go:300/314-323) fails closed -> 'missing authenticated BaseHarbor operator'.

The SAME shape applies to the reference-journey / shell-ux atomic runtime gates IF they run `baha up --yes` in a non-`baseharbor-core-bootstrap.*` root without setting the env var. shell-ux (tests/shell-ux/run.sh) sets `BASEHARBOR_TARGET="shell-ux-static"` (line 14, NOT `atomic-<rt>-shell-ux`), so its target create and subsequent completion/prompt commands run as a STATIC gate in suite mode (DEMO_ATOMIC_GATE != 1) -> no synthetic operator needed (completion/prompt are not managed-boundary ops); the only managed-boundary command shell-ux emits is the target create, which is admitted by ciIntegrationTargetCreate only under the atomic gate pair — in suite mode shell-ux does not hit the managed boundary at all.

ROOT-CAUSE CLASSIFICATION: the baseharbor allow-list (ci_integration_operator_enabled.go) is NARROW AND CORRECT. The failing gaeten fail because the DEMO harness invokes `baha up --yes` from a fixture root that (i) is not the `baseharbor-core-bootstrap.*` project the core-bootstrap.sh path binds, and (ii) never sets `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT`. The synthetic-operator gate is a test-only seam; the fix is a DEMO-invocation change (set the env var at the config-matrix/reference-journey invocation), which is OUT of the 0428-250 baseharbor write-set. The build-tag/baseharbor_ci_operator_testonly is applied by the pre-release workflow at .github/workflows/pre-release-runtime-suite.yml:288 (GOFLAGS) and pre-release-runtime-suite.yml:306 (DEMO_ATOMIC_GATE=1) — that invocation is correct; it is not a missing-tag problem.

## Fix-Art

**fix-Art: build-tag/demo-invocation OWNER point (NOT a baseharbor allow-list gap).**

- The baseharbor synthetic-operator allow-list (cmd/baha/ci_integration_operator_enabled.go:24-119, :78-90, :304-352) is correct and narrow; it intentionally binds the bootstrap `up` to the `baseharbor-core-bootstrap.*` project root via `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT`.
- The concrete gap is in the DEMO harness: `tests/config-matrix/run.sh` (and any reference-journey gate that runs `baha up --yes` outside a `baseharbor-core-bootstrap.*` root) does NOT set `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` around its core-up, so ciIntegrationLocalCoreBootstrap returns false and the synthetic operator is not stamped.
- The correct fix is a demo-repo change: in baseharbor-demo tests/config-matrix/run.sh wrap the core-up subshell (config-matrix/run.sh:26-35) with `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root" \` exported, and similarly ensure the reference-journey gate sets it around its `up`. That makes `ciIntegrationLocalCoreBootstrap` admit the `up --yes` (prefix check :329-330) and stamps the operator.
- I do NOT edit demo files (out of the 0428-250 write-set) and do NOT widen the baseharbor allow-list (widening to admit `.config-matrix.*` / `.reference.*` roots would over-admit synthetic-operator authority to arbitrary demo fixture roots — a security-relevant expansion of the test-only operator seam, and exactly the kind of boundary change the mission forbids). Per the scope split, this demo-invocation fix is an OWNER point.

No baseharbor code change was made. No product operatorauth/mcp.go boundary weakened. No .github, no #1771 local-workload layer, no target.create (0428-247) touched.

## Regression witness (read-only trace, not an exact hosted run)

Exact hosted run was not startable from this session (it requires the demo repo checkout with the demo invocation fixed, which is the OWNER/demo fix). Trace witness that the fix would work: with `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root"` set around config-matrix/run.sh:26-35, `ciIntegrationLocalCoreBootstrap` (ci_integration_operator_enabled.go:316-330) evaluates `allowedRoot` = `$bootstrap_root` (symlink-resolved), `cwd == allowedRoot` (the subshell `cd "$bootstrap_root"` at config-matrix/run.sh:27), and the prefix check passes ONLY if `filepath.Base(allowedRoot)` starts with `baseharbor-core-bootstrap.`. Note `$bootstrap_root` is `.config-matrix.<rand>/control-plane` — its base prefix is `control-plane`, NOT `baseharbor-core-bootstrap.`. Therefore simply exporting the env var is INSUFFICIENT: the prefix guard `:329-330` (`strings.HasPrefix(filepath.Base(allowedRoot), "baseharbor-core-bootstrap.")`) would still reject it.

So the TRUE minimal demo fix is one of:
- (demo, owner) name the config-matrix core-up temp root with a `baseharbor-core-bootstrap.` prefix (e.g. `bootstrap_root="$(mktemp -d "$DEMO_ROOT/.config-matrix.XXXXXX"/baseharbor-core-bootstrap.XXXXXX)"`) and export `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root"`, OR
- (demo, owner) relax the prefix guard in ci_integration_operator_enabled.go:329-330 to also accept a `BASEHARBOR_DEMO_GATE_ROOT` marker file the demo writes — but that IS a baseharbor allow-list widening (the forbidden boundary expansion), so prefer the demo-side root-name fix.

Static zelle gruen wegen operator-stamp: NOT run (no exact hosted run; the fix is a demo-invocation change, out of write-set). The trace confirms the operator would be stamped ONLY after the demo core-up root is named/admitted; the baseharbor allow-list itself needs NO change.

## Fundbilanz

- baseharbor allow-list: CORRECT, no change needed (fix-Art: build-tag/demo-invocation OWNER point).
- The failing gaeten fail at a DEMO-invocation gap (missing `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` + non-`baseharbor-core-bootstrap.` root name in tests/config-matrix/run.sh and any reference-journey gate), NOT at a missing baseharbor allow-list entry.
- Minimal rezept (OWNER/demo, NOT implemented): rename the config-matrix core-up temp root so `filepath.Base` begins `baseharbor-core-bootstrap.` and export `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` around the core-up subshell (config-matrix/run.sh:26-35); apply the same to the reference-journey gate. Confirm `baha up --yes` then passes ciIntegrationLocalCoreBootstrap (:316-340) and the synthetic operator is stamped.

## cleanliness

- Read-only in the product repo: NO change to cmd/baha/ci_integration_operator_enabled.go or any other baseharbor file. NO product operatorauth/mcp.go boundary change. NO .github, NO #1771 local-workload layer, NO target.create (0428-247).
- Branch lane-0428-250-ci-operator-allowlist cut from origin/develop (3cbb2bac3), merge-base confirmed (origin/develop ancestor of HEAD). NO commits, NO push in the product repo. Left the pre-existing modified scripts/pr-gate-coverage.json untouched.
- No container/network/volume/state created. No docker/podman compose project started (coordinator/codeman host; tests run only on named SSH hosts).
- ambient-core / fremder-lane images untouched.
- cleanliness: nothing changed in the product repo. The outcome is an OWNER/demo-invocation finding (demo file:zeile), not a baseharbor code change.

## END

w27-pr1627-0428-061-pull DONE — 0428-250: NO baseharbor code change; fix-Art = build-tag/demo-invocation OWNER point.
branch: lane-0428-250-ci-operator-allowlist. head: 3cbb2bac39996391799d1c6460b230979ee34959 (origin/develop, merge-base confirmed). PR: none opened (read-only scope, no demo write-set). class: fix-Art build-tag/demo-invocation OWNER point. exact run-id: none (no exact hosted run; trace witness only). static zelle gruen wegen operator-stamp: ja erst nach DEMO-fix (baseharbor-side allow-list needs NO change).
Konkrete demo-luecke: tests/config-matrix/run.sh setzt BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT nicht um seinen core-up-Subshell (config-matrix/run.sh:26-35); der `baha up --yes`-cwd hat Basis-Präfix `.config-matrix.<rand>/control-plane`, nicht `baseharbor-core-bootstrap.`, donc ciIntegrationLocalCoreBootstrap (:329-330 Präfix-Check) liefert false -> synthetischer Operator nicht gestempelt -> 'missing authenticated BaseHarbor operator'. core-bootstrap.sh:9 setzt die Env var und benennt den Temp-Raum baseharbor-core-bootstrap.* -> sein up-läuft grün. Fix = DEMO-Seite (Owner-Punkt), nicht in diesem Write-Set.
No product change, no PR, no comment, no subagent. Evidence published to baseharbor-plan origin/main.
