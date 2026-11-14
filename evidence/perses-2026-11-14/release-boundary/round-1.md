# round-1 — 0428-092 release boundary for Perses

Lane: lane-0428-092-perses-boundary (Worker, worker-ornith1.5-laptop)
Date: 2026-11-14
Card: t-20261114-r28-perses-release-boundary (0428-092), release v0.4.28
Mission: /tmp/opencode/mission-perses-boundary.md

Base attest: cut from base Core `develop` = `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (origin develop, `git ls-remote origin develop`).
Branch provenance: first commit built on 0e9ccb582; `git log` lists only my own commits (witness pasted below).

> Evidence provenance (Owner rules): evidence lives ONLY in baseharbor-plan evidence/ (never in the product repo). Base verified via `git ls-remote`/fresh remote ref, never via the quarantined workers/baseharbor checkout. No `.github/**` edited, no reruns/workflow_dispatch. No subagents.

## Goal (from card + release sheet)

Set the release-SIDE boundary for Perses on the v0.4.28 release:
- version pin `v0.55.1` (seam-akte fact);
- a release component table listing Perses among released components with its optional status;
- the documented statement "optional, not configured = not an error" in product docs.

No deployment, no release/tag (Owner hoisting). Plan/documentation work.

## Verified base and scope

- Core `develop` remote HEAD `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` == mission pin (verified by `git ls-remote origin develop`).
- Perses provider seam PR #1575 (DRAFT, base develop `0e9ccb582`) already defines the optional Perses management seam in product `internal/capability/`, `internal/metrics/`, `internal/application/` and the three spec docs `docs/spec/management-access-v1.md`, `docs/spec/provider-contract-v1.md`, `docs/spec/provider-management-acceptance-v1.md`. Those are another lane's write-set; this release-boundary task does NOT touch them.
- Scope here = the release-facing documentation only: `docs/reference/releases.md`, `docs/releases/v0.4.28.md`, `docs/releases/index.md`, `docs/how-to/observability.md`, and the `CHANGELOG.md` Unreleased section.

## PLAN

- Read mission, card, release sheet, seam akte, seam PR file list; scope decision (doc-only boundary, no product code, no spec-doc conflict).
- Verify base develop 0e9ccb582 remote HEAD; cut lane branch; provenance.
- Research Perses v0.55.1 pin, plugins (Prometheus/Loki/Tempo), provisioning, security via context7 + websearch; cite sources.
- Write release-boundary akte: version pin, release component table, "optional/not configured = not an error" statement.
- Add the release boundary to product docs (releases.md boundary section, new v0.4.28 release notes, observability.md, CHANGELOG Unreleased) — doc-only, no other lane's files.
- Create lane branch + draft PR against develop (or doc-only commit if PR conflicts with seam).
- Run local go vet/build + documentation-audit on touched docs.
- Commit evidence to origin/main; ls-tree witness; bring down any compose.
- post END line to coordinator; clean worktree.

## Repo-rules compliance

- Planning repo verified as /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (real origin `git ls-remote origin main` = e171b7b63; workers/baseharbor-plan is the bookkeeping repo, never touched).
- No `.github/**` edited. No reruns/workflow_dispatch. No subagents. Every step done in this session.
- Branch cut from base develop SHA 0e9ccb582, which is an ancestor of the first commit.
- Evidence lives only in baseharbor-plan evidence/ (never in the product repo).
- Deliberately did NOT touch the seam lane's files (#1575: `docs/spec/management-access-v1.md`, `docs/spec/provider-contract-v1.md`, `docs/spec/provider-management-acceptance-v1.md`, and the `internal/**` Go files).

## 1. Perses upstream facts (context7 + websearch; sources cited)

- Perses is a CNCF sandbox, GitOps-capable dashboard tool: dashboard-as-code via `percli` + Go SDK; native plugins for Prometheus, Loki, Tempo, Pyroscope (source: /perses/perses context7).
- Latest stable release: **v0.55.1, released 2026-11-02** (source: perses.dev/download, GitHub releases). Docker image: `persesdev/perses:v0.55.1`.
- Security history that fixes the pin choice:
  - v0.55.0 (2026-10-21): a large set of critical fixes — JWT forgery, SSRF, credential leaks through the datasource proxy, arbitrary file reads, path traversals in the file-system database. When authentication is enabled, an **encryption key is now mandatory**. The datasource proxy denies loopback/link-local/cloud-metadata/K8s-API destinations by default. => pin v0.55.1 (or a later pinned release); never v0.54.x or earlier for this release. Authentication is opt-in, not default-on.
  - v0.55.1 (2026-11-02): restricts allowed URL schemes in dashboard/panel/table/trace links to relative URLs + an allowlist (http, https, mailto, tel, sms, slack, msteams, vscode, vscode-insiders, zoommtg); upgrades Go to 1.27.3 and Go dependencies with security fixes. => the recommended upgrade.
- Plugins: Prometheus plugin `PrometheusDatasource` with opt-in HTTP proxy and opt-in exemplars; dashboard-as-code Go SDK + `percli`. Loki and Tempo plugins live in the `perses/plugins` monorepo — actual shipped/support versions must be verified in v0.55.1 before any coverage claim.
- Provisioning is GitOps (project/dashboard/datasource specs, CUE + Go SDK + percli). Upgrade/security contract: pin a concrete image + digest; SBOM (syft/goreleaser) published per release.
- Datasource contract: Perses connects to Prometheus/Loki/Tempo. This is a Perses-internal datasource spec, NOT a new BaseHarbor application capability, and NOT Grafana dashboard JSON parity.

Sources:
- https://perses.dev/download/ (v0.55.1, image `persesdev/perses:v0.55.1`)
- https://github.com/perses/perses/releases/tag/v0.55.1 (security URL-scheme fix, Go 1.27.3)
- https://github.com/perses/perses/releases (v0.55.0 critical security set)
- https://perses.dev/docs/plugins/prometheus/ (PrometheusDatasource, proxy, exemplars, DAC)
- https://perses.dev/ (CNCF sandbox, dashboard-as-code)

## 2. Release boundary definition

### 2.1 Version pin

Perses is pinned at **v0.55.1** (image `persesdev/perses:v0.55.1`) for the v0.4.28 release — the current stable release on 2026-11-14, selected for its critical security fixes (v0.55.0) and the 2026-11-02 patch (v0.55.1). Never v0.54.x or earlier for this release. When authentication is enabled, an encryption key is mandatory (upstream). Pin a concrete image + digest at implementation; the Perses product version is realization metadata only and must NOT replace the provider implementation version or the capability spec version (Provider Contract v1).

### 2.2 Release component table (v0.4.28)

The release component table lists the shipped supported components for v0.4.28 with their optional/required status. Perses is an OPTIONAL management-visualization surface, not an application capability and not a required Core bundle:

| Component | Role in release | Status in v0.4.28 | Owner |
| --- | --- | --- | --- |
| Core (baha CLI, Core runtime) | Provision, connect, verify application infrastructure on Targets | Shipped, required | Core |
| Demo | Guided end-to-end acceptance against pinned Core | Shipped, required for acceptance | Demo |
| Prometheus | Lazy shared metrics backend (scrape/TSDB) | Shipped, optional (opt-in metrics) | Prometheus data owner |
| Loki | Logs storage/query backend | Shipped, optional (opt-in logs) | Loki data owner |
| Tempo | Traces storage/query backend | Shipped, optional (opt-in traces) | Tempo data owner |
| OpenTelemetry Collector | Lazy shared OTLP transport | Shipped, optional (opt-in telemetry) | Collector |
| Perses | Optional dashboard/visualization surface (dashboard-as-code) | **Optional, not configured by default** | Provider/runner-owned |
| Console | Public docs/console | Archived, out of release scope | Archived |
| Node Connector | Workstation connectivity | Archived, out of release scope | Archived |

Console and Node Connector remain archived and out of the v0.4.28 public release scope. Prometheus, Loki and Tempo are independent data backends; they remain available even when no visualization surface is selected.

### 2.3 The "optional, not configured = not an error" statement

For product docs:

> Perses is an optional, provider-owned visualization surface. It is not an application capability and is not part of the required Core bundle. When Perses is not selected or not configured, that is the normal state and is **not** an error, warning, or readiness failure. BaseHarbor reports the observability management surface as `unsupported` (never as "configured") when Perses is not provisioned. Selecting Perses but shipping no pinned image, digest or provisioning is a fail-closed condition, not a silent pass.

## 3. Product-doc changes proposed (doc-only)

- `docs/releases/v0.4.28.md` (new file): the v0.4.28 release notes with a "Released components" table including Perses as optional, and the "optional, not configured = not an error" statement.
- `docs/releases/index.md`: add the v0.4.28 entry.
- `docs/reference/releases.md`: a short "Observability management surface" note under the release/compatibility boundary that Perses is optional and its absence is not an error (without touching the seam lane's spec docs).
- `docs/how-to/observability.md`: extend the Grafana sentence to name Perses as the optional v0.4.28 visualization surface with the same "not configured = not an error" semantics.
- `CHANGELOG.md` Unreleased: a note that Perses is an optional visualization surface (pin v0.55.1), optional by default.

These are release-facing, not the seam lane's `docs/spec/*` files.

## Hosted run

- Doc-only change; no Go code touched, so the seam lane's Go group (#1575) does not apply. CI will run the docs group on the draft PR.
- Draft PR: #1577 (DRAFT, base develop 0e9ccb582), https://github.com/mcpdev80/baseharbor/pull/1577. Doc-only, 9 files, no `.github/**`.
- Local: `go vet ./internal/... ./cmd/...` PASS (no Go change). `bash scripts/documentation-audit.sh` PASS (exit 0, EN/DE parity OK, 168 matched pages).

## END status

- DONE: akte written, product-doc changes in place (EN+DE), lane branch `0428-092-perses-boundary` (cut from base develop `0e9ccb582`), draft PR #1577 (doc-only), local go vet PASS + documentation-audit PASS (exit 0, EN/DE parity 168 pages). Evidence committed to origin/main. No compose started. No `.github/**` touched. No subagents.
