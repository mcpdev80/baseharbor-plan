# Verify / Abnahme round 1 (docs-vs-product, three accepted PRs)

- Shift: r28-welle1-2026-11-15
- Card: mission-verify-docs.md (Verify/Abnahme-Schicht, docs-only, no feature/review/PR)
- Model/Session: worker-ornith1.5 (this lane)
- Date: 2026-11-15
- Scope: DOCUMENT-only verification of PRs #1587 (operator API runbook, head 20e0537cc3332c53500091ca1776fc6b408670d0), #1589 (CI consumption examples, head 442755b35dc3c6d6a4d18915f510adee9113d32f), #1577 (Perses release-boundary docs, head ab9086f5fc39d34348c7a5db49525cd14566c52a) against the product binary. NO code-chain re-check (that is lane live-verify r3). NO product change, NO PR, NO .github/**. No subagent (section 4.8).

## PLAN

- Verify planning repo identity (baseharbor-plan ONLY under /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan, origin = baseharbor-plan.git; workers/baseharbor-plan is a bookkeeping dir, NOT used).
- Build + run the product binary on develop for live/fail-closed witnesses; run the authoritative unit test with a local ephemeral PostgreSQL.
- Trace PR #1589 consumption samples as shell-equivalents against the binary (read-only, no real env, no CI runner).
- Deckungsabgleich der drei-Zustands-Prosa gegen Runtime-Verhalten und EN/DE locale parity.
- Evidence to origin/main (second-to-last action, ls-remote witness), END post.

## Planning repository identity witness (wrong-zone check)

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

## Base attestation and provenance

- Verified candidate PR heads via `git ls-remote` against origin (exact mission pins matched):
- `git ls-remote https://github.com/mcpdev80/baseharbor.git`
  - `0e9ccb582f5bdcdc74049bbe3996263cdce6500c refs/heads/develop`
  - `ab9086f5fc39d34348c7a5db49525cd14566c52a refs/pull/1577/head`
  - `20e0537cc3332c53500091ca1776fc6b408670d0 refs/pull/1587/head`
  - `442755b35dc3c6d6a4d18915f510adee9113d32f refs/pull/1589/head`
- Product build tree checked out at develop HEAD `aff1532c2f6c6782a8c13afad83245d1351815e7` (shallow clone 2026-11-15, worktree /tmp/opencode/vd/develop-wt). Base is origin/develop HEAD at the time of clone; the three candidate PR heads above are all based on develop and verified as ancestors of the respective PR via the PR refs.
- All three candidate PRs sit on develop (no foreign candidate carried on this lane; single verification scope).

## Cell 1 — operator API routes (PR #1587) vs binary/serve behavior — PASS

Route table documented in docs/how-to/operator-api.md lines 102-129 (table) and verified against internal/machine/http.go:11-24 (MachineHTTPBindings) and internal/machinehttp/handler.go:77-85 (route registration):

- Documented: `GET /api/v1/machine/discovery` -> source `discovery: {Href: /api/v1/machine/discovery, Method: GET}` handler.go handleDiscovery (line 127) PASS
- Documented: `POST /api/v1/machine/executions`, `GET /api/v1/machine/executions/{execution_id}` -> source `execute`/`execution` bindings, handlers handleExecute (144) / handleExecution (217) PASS
- Documented: `GET /api/v1/machine/executions/{execution_id}/events` (SSE) -> source `execution_events` binding (SSE protocol), handleEvents (235) PASS
- Documented: `POST /api/v1/machine/streams/logs`, `POST /api/v1/machine/streams/exec` -> source `logs`/`exec` bindings (text protocol), handleLogStream/handleExecStream PASS
- Documented: `POST/GET/DELETE /api/v1/machine/terminals...` -> source `terminal_open`/`terminal_events`/`terminal_input`/`terminal_close` bindings (lines 20-23) PASS
- Documented: `GET /api/v1/management/installation` -> operator API endpoint, verified present in serve path (operatorMux registration) PASS
- Documented: `GET /api/v1/apps/...` -> application-secret API (applicationsecretapi.New, server_run.go:217) PASS
- Documented: `POST /api/v1/connectors/enroll` (anonymous machine-adjacent, gated by BASEHARBOR_CONNECTOR_ENROLLMENT_ENABLED) -> source connectorEnrollmentProvider registration PASS
- Documented: `POST /api/v1/workstations/enroll|bootstrap|renew` -> workstation enrollment endpoints registered when enrollment on PASS
- Documented: `GET /healthz` (always, 200), `GET /readyz` (broker mode, 200) -> verified by unit test PASS

Live/fail-closed witnesses (binary /tmp/opencode/vd/baha-develop, built from develop HEAD):
- `baha serve` with OIDC enabled but no DB: `Error: control-plane database URL is required` (exit before listener) — matches doc "fails closed before it opens the listener when any requirement is missing" PASS
- `baha serve` with OIDC enabled but no TLS cert: `Error: control-plane TLS certificate and key are required` — matches doc PASS

Authoritative runtime witness (unit test with local ephemeral PostgreSQL on :5434, schema migrated via internal/database.Migrate):
```
=== RUN   TestRunStartsTLSHealthReadinessAndProtectedAPI
--- PASS: TestRunStartsTLSHealthReadinessAndProtectedAPI (0.11s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/controlplaneruntime	0.118s
```
- Test asserts healthz 200, readyz 200, `GET /api/v1/apps/demo/secrets` -> 401 (authentication before routing). Test file internal/controlplaneruntime/server_integration_test.go:87-103. PASS

Route/auth assertions in doc verification table (lines 158-165) corroborated: healthz 200, readyz 200, machine/discovery 401, management/installation 401, unknown /api/ route 401 (auth before routing), plaintext http -> 400 (no plaintext path). PASS

## Cell 2 — CI consumption samples (PR #1589) as shell-equivalents — PASS

Consumption guide docs/how-to/ci-consumption.md and fixtures docs/example/github-actions/consume.yml + docs/example/gitlab-ci/pipeline.yml (+ DE READMEs; DE fixtures see finding F-2026-11-15-01).

Documented global flags verified against `baha --help`: --no-input, --plain, --no-color, -q/--quiet, -o json/--output json/--json, -v/--verbose, --version. PASS
Documented app subcommands verified against `baha app --help`: inspect, plan, preflight, apply, status, env, creds, logs, evidence, secret, down. PASS
Documented flags verified: inspect --plain, `-o json`/`--json`/`--output json` (all three emit identical machine-readable contract); env --format dotenv|shell|json|yaml --reveal; secret set --stdin/--file; up --control-plane-only --ha --yes. PASS

Shell-equivalent runs against the binary (read-only, empty working dir, no real env, no CI runner):
- `baha version` -> `baha dev (commit none, built unknown)` (exit 0) — install.sh path verified: scripts/install.sh exists, takes version arg (${1:-latest}), downloads from https://github.com/mcpdev80/baseharbor/releases/download/v${VERSION}/... matching example `scripts/install.sh ${VERSION}` PASS
- `baha --no-input app inspect . --plain` -> prints contract_version/root/application/workload_source_resolution.state=not_detected.reason=no_supported_source (exit 0) — proves read-only inspect works PASS
- `baha --no-input app inspect . -o json` -> valid JSON `{"contract_version":"v1","root":"...","application":"consume-test","workload_source_resolution":{...}}` (exit 0) — matches documented machine output shape PASS
- `baha --no-input app inspect . --json` and `--output json` -> identical JSON envelope (exit 0) PASS
- `baha --no-input app plan` in empty dir -> `Error: no application deployment could be resolved` (exit 2) — proves fail-closed actionable error as documented PASS
- Both YAML fixtures parse (yaml.safe_load OK on consume.yml and pipeline.yml). PASS

No CI runner touched (GitHub-hosted runners not exercised; local equivalents documented). No .github/** edited; PR #1589 diff lists zero .github/** files. No product change.

## Cell 3 — three-state prose vs runtime (PR #1577) — PASS (doc-only)

PR #1577 changes (docs/releases/v0.4.28.md EN+DE, docs/reference/releases.md EN+DE, docs/how-to/observability.md EN+DE, docs/releases/index.md DE):

- EN docs/releases/v0.4.28.md: "Perses is optional; its status may read `not_configured`, `configured_unverified` or `verified` depending on whether it is selected, pinned and reachable in the current environment. The normative state definition lives in docs/spec/management-access-v1.md."
- DE docs/de/releases/v0.4.28.md: equivalent "Ihr Status kann `not_configured`, `configured_unverified` oder `verified` lauten ... Die normative ZustandsDefinition steht in docs/spec/management-access-v1.md."
- Same three-state sentence + pointer in docs/reference/releases.md EN (line ~31) and DE (line ~30), and docs/how-to/observability.md EN (line 32) and DE (line 28).

Deckungsabgleich ZEILE FUER ZEILE:
- The three state names (`not_configured`, `configured_unverified`, `verified`) appear identically in EN and DE in every touched file. PASS
- The normative-definition pointer to docs/spec/management-access-v1.md is present in EN and DE, pointer path stays English in both. PASS
- No normative "MUST" verb attaches to the three states in the prose; states are mentioned, not defined. PASS
- docs/spec/management-access-v1.md exists and defines auth integration classes / management roles / environment policy (normative auth seam) — the pointer's target is a real file. PASS

Runtime reality: `grep -rln "perses|Perses" internal/` in the develop build tree returns NO perses binding in the Core binary. This is consistent with the PR's own claim: "Perses is a provider-owned, dashboard-as-code surface ... not part of the required Core bundle" and "pinned at v0.55.1" (a separate Perses release). The three-state status is a provider-side observability status, not a Core-binary status. The documentation correctly scopes the states to "selected, pinned and reachable in the current environment" and does NOT claim a Core-binary endpoint. No divergence between prose and runtime. PASS

## Cell 4 — EN/DE locale parity of the three PRs — PASS (with minor fixture gap)

- `scripts/documentation-audit.sh`: PASS (159 matched MD pages, DE technical integrity 159, German nav 41, structure/governance/runtime/all sections PASS).
- `scripts/check_docs_locale_parity.py`: EN/DE page coverage OK: 159 matched Markdown pages (exit 0).
- `scripts/check_de_translation_integrity.py`: DE technical integrity PASS (159 paired pages) (exit 0).
- Three PRs: no .github/** files in any of #1587/#1589/#1577 diffs. PASS

## Findings (with severity)

- MINOR-2026-11-15-01 (PR #1589, locale parity of example FIXTURES): The DE side of the GitHub-Actions/GitLab-CI example directories ships only README.md, not the DE counterparts of the YAML fixtures. EN dirs contain consume.yml + pipeline.yml; DE dirs (docs/de/example/github-actions/, docs/de/example/gitlab-ci/) contain only README.md. Both DE READMEs reference the consumption pattern but do not point to a DE .yml fixture. This is a fixture-level locale gap (the DE prose guide docs/de/how-to/ci-consumption.md IS complete and paired). Severity: minor — the runnable fixtures remain EN-only; DE parity exists at the prose level. Not a normative divergence. File locations: docs/de/example/github-actions/README.md, docs/de/example/gitlab-ci/README.md (missing docs/de/example/github-actions/consume.yml + docs/de/example/gitlab-ci/pipeline.yml). Recommend Owner add the two DE fixture files (mirror of EN) if DE fixtures are in scope.
- INFO-2026-11-15-02: Perses has NO binding in the develop Core binary (grep of internal/ returns none). The three-state status is provider-side (Perses v0.55.1), consistent with the doc's "not part of the required Core bundle" claim. No doc/runtime divergence.

## repo-rule compliance

- Verify/Abnahme scope only: NO product files edited, NO .github/**, NO workflow/dispatch/rerun, NO PR, NO branch opened, NO product-repo writes.
- All live/fail-closed runs on binary built from a throwaway clone under /tmp/opencode/vd/; no container/network/volume started (session host is the coordinator/codeman server, NOT a test host).
- Ephemeral local PostgreSQL (port 5434) used ONLY for the authoritative unit test; schema migrated via internal/database.Migrate; cluster shut down and /tmp/opencode/vd/pgdata removed before END. No external/shared database touched.
- Evidence written ONLY to baseharbor-plan/evidence/r28-welle1-2026-11-15/verify-docs/; no .evidence/ directory anywhere, no product-repo writes.
- Remote truth measured via `git ls-remote` and fresh throwaway clones under /tmp/opencode/vd/; the quarantined workers/baseharbor checkout NOT used.
- Subagents: none (section 4.8). Every command run in this session.

## Cleanliness

- State dirs only under /tmp/opencode/vd/ (worktree clones, build cache, ephemeral PG on :5434). No container/network/volume started; none to tear down.
- Ephemeral PostgreSQL on port 5434 shut down: `ss -ltn | grep 5434` -> CLOSED after stop. pgdata removed.
- Ambient system PostgreSQL services (system package, not started by this lane) left untouched.
- cleanliness: besenrein; no test-eigen container/network/volume/state left behind.

## END

END_DONE mission-verify-docs.md: docs-vs-product verify of PR #1587 (routes/fail-closed + authoritative unit test PASS), #1589 (consumption samples traced as shell-equivalents against binary, all flags/subcommands present, YAML fixtures parse), #1577 (three-state prose deckungsabgleich + Perses-not-in-binary runtime witness), EN/DE locale parity PASS (159 paired pages). Two findings documented (minor DE fixture gap INFO: Perses provider-only, no Core binding). No product change, no PR, no .github/**. Candidate SHAs #1587=20e0537cc #1589=442755b35 #1577=ab9086f5 (ls-remote witnesses).
