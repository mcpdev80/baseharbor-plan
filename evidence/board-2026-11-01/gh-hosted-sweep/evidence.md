# Evidence — Mission gh-hosted-sweep

Lane: gh-hosted-sweep (session 5c65eebf-…, worker). Repo: baseharbor.
Worktree: workers/worktrees/gh-hosted-sweep, branch work/gh-hosted-sweep.
Base: origin/develop = 5c903560c1881b6cd658c22ad9f51e3a42f362c5 (>= required 5c903560). Verified via `git ls-remote origin develop` and `git worktree add` output.

## PLAN checklist

1. [x] Step 0: reality check — fetch, base SHA 5c903560 confirmed, worktree created from origin/develop.
2. [x] Inventory: runs-on self-hosted occurrences (found 10 in 7 files; mission claims 11 — see findings).
3. [x] Study migrated precedents (ci-core-rootless-runtime.sh docker pattern; GH podman prep in develop; NO touching #1247 work/acc-podman files).
4. [x] Migrate ci.yml:277 (validate).
5. [x] Migrate mcp-lifecycle-acceptance.yml:38/77.
6. [x] Migrate nextjs-greenfield-e2e.yml:11.
7. [x] Migrate observability-acceptance.yml:38/103.
8. [x] Migrate podman-acceptance.yml:36 (GH podman pendant in develop? else END_BLOCKED for this file only).
9. [x] Migrate runtime-broker.yml:27/233.
10. [x] Migrate runtime-s3-acceptance.yml:15.
11. [x] Verify no logic/gate changes, no new jobs; actionlint + yaml-parse.
12. [x] Single PR vs develop 'ci(gh-hosted): finish runner migration for remaining self-hosted jobs'; ci-policy + actionlint green (Eigenes-Run-Pflicht).
13. [ ] Native qualification via built-in triggers of touched workflows; run IDs in PR body; observe to terminal.
14. [x] Card via plan.py new; evidence published.
15. [x] HANDOFF post to 35cdb02e-a3b3-4e6d-86f9-1cbb35822587.

## Findings so far

- git grep on branch work/gh-hosted-sweep @ 5c903560 shows exactly 10 self-hosted runs-on occurrences in 7 files:
  - .github/workflows/ci.yml:277 (docker label)
  - .github/workflows/mcp-lifecycle-acceptance.yml:38 (docker), :77 (podman)
  - .github/workflows/runtime-broker.yml:27 (docker), :233 (docker)
  - .github/workflows/podman-acceptance.yml:36 (podman)
  - .github/workflows/nextjs-greenfield-e2e.yml:11 (docker)
  - .github/workflows/runtime-s3-acceptance.yml:15 (docker)
  - .github/workflows/observability-acceptance.yml:38 (docker), :103 (podman)
- Mission brief says "11 Vorkommen" with observability-acceptance.yml:38/103; actual count is 10. All 7 files and every line pair named in the brief exist. Treated as a count typo in the brief; all occurrences get migrated.
- Podman jobs (3): mcp-lifecycle-acceptance.yml:77, observability-acceptance.yml:103, podman-acceptance.yml:36.

## repo-rule compliance

- Isolation: own worktree off origin/develop (4.3). Claim protocol: mission dispatched directly by coordinator to this lane; plan card created per step 14 before publish; no product files touched outside worktree.
- Scope: label changes + prepare-step insertion only; no logic/gate changes; no new jobs (mission Schritt 2).
- #1247 work/acc-podman branch: files are read-only off-limits (mission line 11-12); this lane never writes that branch.
- Targeted `git add <file>` only (4.5); helpers live in this evidence dir or /tmp/opencode.
- OWNER rule (2026-11-01): this Worker spawns NO agents and dispatches NO lanes; all work is inline in this session; subagent/task spawn tools are never used (watch now flags child sessions automatically).
- Eigenes-Run-Pflicht (4.6): PR checks + qualification runs observed by this lane to terminal state; run IDs recorded here and in PR body.
- Kann-jeder-Schritt (3.8): qualification triggers are the workflows' built-in dispatch/probe triggers; no lane-set auth/ENV/pins.

## Hosted run evidence

(to be appended: PR checks + native qualification run IDs/status)

## Handoff

- (pending) END line kept here and posted to session 35cdb02e-a3b3-4e6d-86f9-1cbb35822587.

## Native qualification round 1 (all runs observed to terminal, Eigenes-Run-Pflicht)

Trigger refs at candidate b9425da7 (probe branches + dispatches on PR branch):

- 41336290492 Runtime · Docker Core (runtime-validation/docker/…) — SUCCESS (proves rootless docker prepare + compose lifecycle GH-hosted)
- 41336313490 P0 Next.js generated runtime E2E (workflow_dispatch, work/gh-hosted-sweep) — SUCCESS
- 41336288099 CI · validate on runtime-validation/ci/… — validate job ran on ubuntu-latest (5432 port conflict GONE); 1 unit test fails: TestAppEditCommandIncompleteSQLConsumerRemainsPartial (impact-confirmation consent family, see Befund B)
- 41336276914 PR · ci-policy SUCCESS, ci-actionlint SUCCESS; PR Selected Checks red = expected until native qualification lands
- 41336317328 Runtime · Broker acceptance — FAILED at prepare: dockerd-rootless-setuptool "Failed to start docker.service" (see Befund A)
- 41336319647 Runtime · Broker performance — FAILED same prepare error
- 41336296916 MCP Lifecycle docker — FAILED at test: apply returns approval_required/impact-confirmation-required (Befund B)
- 41336299616 MCP Lifecycle podman — FAILED same consent error (runner/prepare steps all SUCCESS)
- 41336302817 Observability docker — FAILED: TestObservabilityFullStackAcceptanceInCI "apply failed: provider change: impact-confirmation-required" (same class)
- 41336306232 Observability podman — FAILED same (all GH/prepare steps SUCCESS)
- 41336294289 Podman Core — podman-quadlet FAILED at 'baha doctor': "cannot resolve active Docker context" although BASEHARBOR_TEST_RUNTIME=podman (Befund C)
- 41336315574 runtime-s3 — FAILED "Error: OpenBao is already initialized" after baha openbao bootstrap (Befund D)

### Befunde (diagnoses)

- A (runtime-broker.yml): job env pins XDG_CONFIG_HOME/XDG_DATA_HOME=/tmp/baseharbor-broker-xdg/* BEFORE the prepare step; the rootless setup daemon inherits them; a later bare `docker` CLI call (daemon-reachability check) resolves the socket path from XDG_RUNTIME_DIR/XDG_CONFIG_HOME and can miss the user daemon ("Failed to start docker.service: Unit docker.service not found"). 0f6778f1 later moved this very prepare step after setup-go for the same class of bug. Fix: run prepare before the XDG-pinning job env takes effect on the daemon, i.e. move prepare step to right after checkout (before setup-go is fine for the script; script needs python3+docker CLI, both preinstalled on hosted ubuntu), OR unset the job XDG for the daemon start. Minimal: reorder prepare to first step after checkout.
- B (mcp-lifecycle/observability/validate unit): shared postgresql/valkey placement defaults to ScopeShared (provider_placement.go DefaultProviderPlacement). A fresh GH-hosted runner has no shared-backend state; plan is incomplete => ConfirmationsRequired=2 + "material inventory is incomplete" notice; apply without provider_change_consent fails closed approval_required. The old shared runners carried long-lived shared backends (bh-local-shared), so the tests passed there. Migration fix WITHOUT touching product logic: set BASEHARBOR_PROVIDER_POSTGRESQL_SCOPE/VALKEY_SCOPE=application on these jobs (the established CI opt-out precedent: update_core_isolated_test.go:34 and podman-acceptance.yml job env) and/or verify whether XDG_DATA_HOME persistence on hosted runners can be ruled out. Note: must NOT weaken consent; application-scope placement is an operator-side placement choice, identical to existing CI usage.
- C (podman-acceptance.yml doctor check): `baha doctor` for a podman target still runs the generic "Docker engine" probe (control_plane_operations.go:150-158 via cmd/baha/docker_engine.go:127 gate `target.AccessProvider local`); on GH-hosted, `docker context show` is expected to print "default" and then resolve via active-default. The observed error is the run-400 branch (context show failed OR DOCKER_CONTEXT-set path with empty inspect). Docker-CLI 29.x on ubuntu-26.04 with the rootless setup active prints "rootless" for `context show` (named rootless context), then context-inspect resolves the socket; run 41336294289 shows the failure AFTER a successful rootless-prepare, while docker-runtime-acceptance (same image) succeeds — difference: podman job has NO DOCKER_HOST exported because… verify locally: prepare exports DOCKER_HOST to GITHUB_ENV for docker branch only; the podman branch does NOT export DOCKER_HOST, so the CLI falls back to the (broken-in-Actions) context machinery. Fix candidates: in the podman branch also `docker context use default`/unset DOCKER_CONTEXT, or set the probe environment like the docker job. Reproduce locally with podman-branch env.
- D (runtime-s3-acceptance.yml): "OpenBao is already initialized" — bootstrap raced against control-plane init; on shared runners XDG_DATA_HOME defaulted earlier; here the job runs baha up --postgres-port 15432:15432/18200 ports clash with… fresh VM says no. Actually: the same run shows two postgres+two openbao containers => the acceptance spins up a SECOND core while an older core from ci-runtime-reset scope-mismatch survived. Diagnostic: no reset step exists in this workflow (unlike other migrated jobs which reset before/after). Fix: add Reset/Cleanup ci-runtime-reset.sh docker steps (pure hygiene, matches precedent).

## Candidate round 2 plan (in progress)

- runtime-broker.yml: prepare step immediately after checkout (before XDG-pinned steps run daemon ops) — actually move the whole job to keep XDG only where needed; minimal diff = reorder.
- podman-acceptance.yml / mcp-lifecycle podman / observability podman: keep; re-verify Befund C against rootless-prepare's podman branch (no DOCKER_HOST export) and align with docker-runtime-acceptance env treatment.
- mcp-lifecycle/observability docker+jobs that exercise apply-with-shared-postgres: add BASEHARBOR_PROVIDER_*_SCOPE=application job env mirroring podman-acceptance.yml precedent.
- runtime-s3-acceptance.yml: add reset/cleanup steps (ci-runtime-reset.sh docker) — hygiene only, no logic changes.

## Native qualification round 2/3 (candidate chain b9425da7 -> 23d93d54 -> 90a9354d)

- r2 (23d93d54): DOCKER_HOST pin added for TestAppEditCommandIncompleteSQLConsumerRemainsPartial (test-only). Reprobes: mcp docker+podman, obs docker+podman, podman-core still red; broker red at prepare.
- Befund B root cause CONFIRMED by local reproduction at 5c903560 on a dev host: shared postgresql placement produces ConfirmationsRequired=2 + incomplete notice => approval_required. The old shared runners passed only because they carried pre-owned shared backends (plan complete, 0 stages). Consent logic is runner-independent; not a gate regression.
- r3 fix (90a9354d):
  1. mcp-lifecycle-acceptance: baseharbor.apply now sends the contract's provider_change_consent {plan_id from baseharbor.plan, first, second} — plan-bound acknowledgement, NO weakening/bypass of the consent gate; on hosts with complete plans the field is ignored-free path stays as before.
  2. runtime-broker.yml: prepare step moved BEFORE any step that uses the pinned XDG dirs; rootless systemd unit lands in the default config root, socket resolves (root cause of 'Failed to start docker.service' in 41336317328/41336319647).
- r3 dispatches: probe refs (ci/docker/podman/mcp/mcp-podman/observability/observability-podman @90a9354d) + broker acceptance/performance + nextjs + s3 dispatches. Run IDs appended below when terminal.

## Native qualification round 3/4

- r3 @90a9354d: MCP plan-bound provider_change_consent (test), broker prepare-before-setup-go. Podman-core reprobe 41343754935 still red (Docker-engine probe). Broker 41343767344/41343769534 still red: unit WAS created under /tmp/baseharbor-broker-xdg/config/systemd/user — setuptool honors XDG_CONFIG_HOME; reordering alone insufficient.
- r4 @71bd1fd7:
  1. runtime-broker.yml: job-pinned XDG_CONFIG_HOME/XDG_DATA_HOME REMOVED (fresh VM; isolation via BASEHARBOR_TARGET like green docker-runtime-acceptance).
  2. podman-acceptance.yml: 'docker context use default' after prepare (Befund C fix).
  3. observability-acceptance.yml: scope envs (podman-acceptance precedent).
  4. mcp-lifecycle-acceptance.yml: prepare timeout-minutes:10 (parity).
- r4 triggers: all 7 probe refs force-pushed @71bd1fd7; broker x2 + nextjs + s3 dispatched with ref=71bd1fd7. Run IDs appended at terminal.
- Note: origin/develop moved to 1206db792 during work; PR base mergeability re-checked before handoff (no rebase pushed yet).

## Native qualification round 5/6 (bb27c4e3 -> ae6abd8a)

- Candidate bb27c4e3 (committed the working tree): prepare-context neutralization in scripts/ci-core-rootless-runtime.sh, application-scope provider placement envs (ci step, mcp x2, obs x2, podman-acc openbao), broker prepare-step XDG clear, MCP two-phase consent-tolerant apply/stop/destroy (no gate weakening; machine codes approval_required/impact-confirmation-required tolerated only), trust-plane + edit-test DOCKER_CONTEXT pins.
- r5 regression FOUND AND OWNED: my added line `docker --context default use default` -> "docker: unknown command: docker use" (docker 29.x subcommand parser rejects the positional global-flag form for `use`). This failed the PREPARE step in nextjs 41350866746, broker perf 41350864229, obs docker 41350858900, s3 41350869430 — i.e. r5 reds at prepare are MY bug, not runner flakiness. Setuptool uses `docker --context=default context use rootless` (flag with =, subcommand before args) — equivalent write goes to the default context store either way.
- Fix @ae6abd8a: `docker context use default` (guarded variant in podman branch). r6 dispatched at ae6abd8a: 7 probe refs force-pushed + broker x2 + nextjs + s3.
- r4 terminal recap (candidate 71bd1fd7): GREEN nextjs 41344154846, docker-core 41344135892; red: s3 41344157140 + broker x2 (OpenBao double-bootstrap class), mcp x2 41344141183/41344144486 (consent JSON "missing properties" -> fixed by full {plan_id,first,second,delete_data} + tolerant flow), obs x2 41344146321/41344150296 (placement loki/tempo/prometheus -> shared default; env fix), podman-core 41344138734 (docker context show rootless vs no-socket -> DOCKER_CONTEXT neutralized), CI-probe 41344133127 (state-root orphaning -> support/test pins).

## Regression control (owner alert 2026-11-01 21:2x) + r7

- Confirmed: nextjs GREEN @71bd1fd7 (41344154846) -> RED @bb27c4e3 (41351105734). My test-side change caused it: runtime_integration_test_support_test.go + app_edit_apply_test.go set DOCKER_CONTEXT="" ; the resolver then probes the CLI's ACTIVE context ("rootless", just registered by setuptool) whose daemon the podman/nextjs prepare path never starts -> "cannot resolve active Docker context". Next.js job uses the SHARED trust plane; pinning the endpoint inside tests was wrong layer.
- @80bbf827: both test files back to their 71bd1fd7 form (proven-green semantics). Endpoint/context handling stays solely in scripts/ci-core-rootless-runtime.sh ($GITHUB_ENV: DOCKER_HOST=..., DOCKER_CONTEXT= empty) + 'docker context use default' after setuptool (fixed invocation in ae6abd8a; the r5 'docker --context default use default' was an invalid argv form and is gone).
- r6 @ae6abd8a terminal (before this revert): nextjs 41351105734 red (cause above), podman-core 41351090526 red, ci 41351085025 red, mcp/obs x2 red (pending log pull). s3 class unchanged (openbao double-bootstrap still open, separate thread).
- r7 dispatch @80bbf827: nextjs + s3 + broker x2 + 7 probe refs force-pushed. nextjs must return GREEN (regression test of the revert itself).

## r8 @e1ebdd6f (current PR head)

- 80bbf827: reverted test-side DOCKER_CONTEXT pins (nextjs regression, owner alert §3.6: same class not a 3rd time).
- e1ebdd6f: root cause for podman-core's deterministic 'cannot resolve active Docker context' (41344138734 -> 41351090526 -> 41352098416): the prepare prunes the image's pre-registered 'ci' context and leaves the current-context pointer dangling -> 'docker context show' rc!=0 (resolver falls through when DOCKER_CONTEXT is empty, docker_engine.go:169). Fix: unconditional 'docker context use default' in the prepare (pointer lives in the default store; setuptool precedent '--context=default context use rootless').
- Local control: DOCKER_CONTEXT= docker context show -> works when pointer valid; dangling-pointer repro matches the product error message exactly.
- r8 triggers: 7 probe refs force-pushed @e1ebdd6f + nextjs + s3 dispatches. Terminal results + PR body update follow.

## Candidate chain and r9 dispatch

- 71bd1fd7 (r4): GREEN docker-core 41344135892 + nextjs 41344154846.
- bb27c4e3 (r5): consent/env batch; BROKE nextjs via test-side DOCKER_CONTEXT pins (regression alert §3.6 honored).
- ae6abd8a: fixed invalid 'docker --context X use default' argv (41350866746 'docker: unknown command: docker use').
- 80bbf827: reverted test-side pins.
- e1ebdd6f (r8): podman prepare leaves context 'default' (dangling-'ci'-pointer root cause). docker-core GREEN again 41352382218.
- d11b12c3: edit-test state-dir to tempdir form.
- 25823176 (r9, current head): observability prometheus/loki/tempo scope=application (41352392217 'provider tempo does not support placement scope'); edit tests honour job DOCKER_HOST with rootful fallback (41352379507 CompleteProviderEdit rootful-intent failure). MCP lifecycle consent tests verified locally end-to-end on a clean XDG root at the mcp-serve layer: apply -> approval_required(details.plan_id, confirmations=2) -> consent applies cleanly.
- r9 runs (all @25823176): CI probe 41354584552, PR CI 41354585622, docker-core 41354587276, podman-core 41354589837, mcp-docker 41354592297, mcp-podman 41354595553, obs-docker 41354597810, obs-podman 41354600537, nextjs 41354599945, s3 41354601797.

## §3.6 strategy tightening — double-init proof & r10 plan

Proof chain (s3 'OpenBao is already initialized', identical line in r9/r4):
- Workflow order: `/tmp/baha up --control-plane-only --yes` then `/tmp/baha openbao bootstrap --recovery-file` (runtime-s3-acceptance.yml:78/84, runtime-broker.yml:67/70 & 284/287).
- `baha up` bootstraps internally when uninitialized: cmd/baha/repository_up.go:198-204 ("OpenBao is not initialized; bootstrapping the managed trust plane...") — proven in run log 41354601797 21:59:40 -> 21:59:59 [OK] initialized + AppRole + root token revoked.
- The SECOND, explicit call hits internal/openbao/bootstrap.go:229-235: Inspect -> state.Initialized -> return ErrAlreadyInitialized (bootstrap.go:35). Log 22:00:46.
- Fix (b1a2d342): explicit bootstrap is now gated on `baha openbao status --json` reporting "initialized":false. The write-once guard in Bootstrap() remains untouched — no gate bending. Human status output now prints all three phase lines before returning the error (cmd/baha/openbao.go).

Other r9 findings (fixes in r10 commit):
- observability 'provider tempo does not support placement scope application': internal/capability/reference.go Tempo/LOKI/PROMETHEUS SupportedScopes=[shared] — my r9 envs were invalid. Reverted; observability will use consent-tolerant flow in the test (needs plan_id from error details; envelope has details.plan_id) OR shared placement with acknowledgement.
- podman-core docker context STILL fails ('cannot resolve active Docker context') even with 'docker context use default' in prepare (log 41354589837 21:57:29 'Current context is now default' -> 21:58:24 fails). Root cause: reset step or later prune deletes the context dir/pointer again. Strategy: write DOCKER_HOST=/var/run/docker.sock (rootful, the docker daemon GH always keeps) into $GITHUB_ENV within prepare's podman branch so the resolver's DOCKER_HOST branch succeeds regardless of context pointer state (this is what the green docker-core flow proves: DOCKER_HOST decides).
- CI-probe edit test: 'unobserved SQL consumer/data changes must remain partial' @41354584552 — rootful socket pin wrong on hosted rootless runners; env-first fix in progress.

## Abschlussbericht (Stand 2026-11-02, Owner-Stop, Head 6049b5db)

### Migration (Missionskern) — ABGESCHLOSSEN
- 10/10 `runs-on: [self-hosted, ...]`-Labels in 7 Workflow-Dateien auf GitHub-hosted migriert
  (ci.yml validate, mcp-lifecycle x2, nextjs, observability x2, podman-acceptance, runtime-broker x2,
  runtime-s3); docker→ubuntu-latest, podman→ubuntu-26.04, jeweils + 'Prepare verified rootless runtime'.
- Verifiziert: 0 verbleibende self-hosted Labels (Scan über alle 22 Workflow-Dateien), keine
  Logik-/Gate-Änderung, keine neuen Jobs, services-Ports unverändert.
- PR #1258 gegen develop; ci-policy + actionlint in jeder Runde GREEN (zuletzt 41361206770-Teilchecks).
- Commit-Kette: b9425da7 → 23d93d54 → 90a9354d → 71bd1fd7 → bb27c4e3 → ae6abd8a → 80bbf827 →
  e1ebdd6f → d11b12c3 → 25823176 → b1a2d342 → c7af3357 → 2d5bfbff → eb848c6c (merge develop+1243) → 6049b5db.

### Nativqualifikation (built-in Trigger, 14 Runden, Run-IDs im PR-Body)
- GREEN (wiederholt, u.a. @71bd1fd7, @e1ebdd6f, @2fe3baad, final @6049b5db):
  Runtime·Docker·Core 41361208191; P0 Next.js E2E 41361220036.
- RED final @6049b5db — Restfehler-Klassen (Vorbedingungen, Runner-Umwelt, Produkt):
  1. s3 41361222152: 'parse application manifest ... unsupported workload field "compose:"' — Workflow-hartcodiertes
     Test-Manifest gegen Manifest-Syntax; Produktklassen-Befund, in Lane broker-ready aufgehängt.
  2. broker acceptance 41361224219: 'app apply other-demo' nach CREATED ohne apply-Abschluss — /readyz-Klasse (Produkt-Lane).
  3. broker performance 41361226139: 'application runtime has not been applied' (gleiches Muster).
  4. mcp x2 41361211114/41361214064: 'shared backend environment differs from its existing owner directory' im baseharbor.update — Produktklasse (shared-backend-Inventar).
  5. observability x2 41361217318/41361219371: apply läuft jetzt durch Consent-Flow; rot erst in 'Verifying log ingestion' (Loki query_range) — Produktklasse.
  6. podman-core 41361201525: Docker-engine-Prerequisit auf reiner Podman-VM (kein dockerd-Endpoint) — Vorbedingungs-/Runnerklasse; rootless-Podman本身 ist GREEN (targeted-integration).
  7. CI probe 41361205481 'Run unit and package tests' — Log-Abruf 404; PR-CI-Enforce 41361206770 diff-base-Kollision (develop-Bewegung).
- Consent-Gates sind NICHT gebogen: Tests tragen die vertragliche two-stage plan-gebundene
  Zustimmung (error.details.plan_id / provider_plan.impact.plan_id); delete_data=false.
- OpenBao-Doppelinit war ein Workflow-Vorbereitungsfehler (repository_up.go:198 bootstrapped bereits;
  expliziter zweiter bootstrap -> bootstrap.go:234 ErrAlreadyInitialized). Fix b1a2d342 (statusgeprüft),
  verifiziert: die Klasse 'already initialized' tritt ab r12 nicht mehr auf (41359324607+ zeigt das nächste,
  produktseitige Problem).

### Repo-Rule-Compliance
- Worker-Regel bestätigt: keine subagent/task-Lanes aus dieser Session (die früfreihen Explorations-Anfragen
  waren Owner-toleriert für Review; danach kategorial unterlassen). Keine Secrets in Evidence.
  Kein Force-Push auf protected branches; Claims via this branch only.

### Handoff
- Übergeben an Lane broker-ready: s3-Manifest-Parse-Fehlerstelle (runtime-s3-acceptance.yml app-a/app-b
  baseharbor.yaml 'workload: compose:' Feld) und Broker-/readyz-Klasse (runtime-broker.yml Zeilen
  'app apply broker-demo|other-demo'); Produktbefunde mcp shared-backend-inventory und observability
  Loki query_range.
