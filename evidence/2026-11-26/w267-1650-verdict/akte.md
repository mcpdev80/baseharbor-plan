# Bounded Codex review — product PR #1650 (0428-078)

**Role:** REVIEW
**Candidate:** `37c4d847ca377d1555163ac4791c8ba08b85de77`
**Card:** `tasks/t-20261114-r28-perses-dashboard-identity.md` from Plan `origin/main`
**Review:** GitHub review on PR #1650 submitted as COMMENTED (not APPROVED): https://github.com/mcpdev80/baseharbor/pull/1650
**Disposition:** MERGE WITHHELD. The exact-head run pair is successful, but the candidate has two genuinely foreign author identities and content criteria remain unproven. No product merge, product write, or product CI trigger was performed.

## Content verdict

The candidate PR files API lists four paths: `cmd/baha/app_perses_cli_test.go` (modified), `cmd/baha/app_status_result.go` (modified), `internal/metrics/identity_dashboard_witness.go` (added), and `scripts/pr-gate-coverage.json` (modified). The JSON diff changes only the final newline; it is not a semantic catalog change. The task scope at card lines 48–50 is “Own identity dashboard assets and focused tests.”

| Card acceptance criterion (quoted) | Verdict and candidate-diff evidence |
|---|---|
| “Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.” | **PARTIAL.** The candidate consumes the current Perses probe at `cmd/baha/app_status_result.go:319` and requires verified Perses at `cmd/baha/app_status_result.go:481-490`. It does not establish the Perses pin or change/verify a native dashboard format. |
| “Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.” | **PASS for the added witness checks; otherwise no change.** Target-root validation is at `internal/metrics/identity_dashboard_witness.go:68-80`; identity/placement fail-closed checks at `:42-57`; owner, scope, sharing-boundary, and native signal-shape checks at `:111-133`. The candidate adds no service. Secret handling is not changed by this diff. |
| “Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Deliver identity-provider panels only for verified current Keycloak metrics; do not rely on obsolete SPI assumptions.” | **PARTIAL.** Verified Perses plus the target-bound witness gate eligibility at `cmd/baha/app_status_result.go:325-336`; native current Keycloak signal shape is checked at `internal/metrics/identity_dashboard_witness.go:83-90,111-133`. No panel definitions or backend ownership/removal code changes in this candidate diff, so panel delivery and ownership/removal are not evidenced here. |
| “For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.” | **NOT DEMONSTRATED.** No alerting contract or evaluator change is in the diff. |
| Required checks: “Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof.” | **FAIL TO QUALIFY.** Exact SHA and successful executed test/runtime jobs are recorded below, but Native Keycloak/Core was skipped in both runs. The run pair does not prove that gate executed. |

## Exact-head run evidence

The runs API records two distinct `pull_request` runs on the exact candidate SHA, both attempt 1, both completed SUCCESS (not reruns):

- [45734193200](https://github.com/mcpdev80/baseharbor/actions/runs/45734193200), `2026-11-26T01:12:49Z`, attempt 1.
- [45737093207](https://github.com/mcpdev80/baseharbor/actions/runs/45737093207), `2026-11-26T01:38:17Z`, attempt 1.

The following census was fetched from `actions/runs/<id>/jobs?per_page=100`; all listed jobs completed, every job attempt is 1. `S` = success/executed, `K` = skipped. Each of the four selected runtime jobs in both runs executed (not a prior-evidence no-op):

| Run | S — executed jobs | K — skipped jobs |
|---|---|---|
| 45734193200 | `PR · Native gate plan`; `Workflow policy`; `PR · Source format`; `PR · Trusted Plan`; `PR · Demo Pin`; `PR · Focused Python`; `PR · Runner Interface`; `PR · Exact Candidate`; `PR · Candidate-added checks (advisory)`; `PR · Go unit · cli-0`; `cli-1`; `cli-2`; `cli-3`; `packages`; `owner`; `PR · Validation · receipt-execution-tests`; `ci-policy`; `go-build`; `pr-planner-tests`; `cli-gofmt`; `ci-executor-tests`; `go-vet`; `PR Selected Checks`; `PR · Selected Runtime (atomic/docker/observability, docker, observability) / Executed docker · observability`; `PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) / Executed podman · data-capabilities`; `PR · Selected Runtime (atomic/podman/observability, podman, observability) / Executed podman · observability`; `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities` | `PR · Main release source`; `Targeted HA · podman`; `PR · Draft source and routing`; `Targeted · Workstation onboarding · ${{ matrix.runtime }}`; `Release Source Preflight`; `PR · Exact full Pre-Release`; `Targeted HA · docker`; `PR · Main release Go · ${{ matrix.shard }}`; `validate`; `PR · Draft Go · ${{ matrix.shard }}`; `PR · Native · ${{ matrix.id }}`; `PR · Native Keycloak/Core · ${{ matrix.runtime }}`; `PR · Consumer Pins`; `PR · Main release checks`; `PR · Selected Core-less · ${{ matrix.runtime }}`; `PR · Public Contracts` |
| 45737093207 | `Workflow policy`; `PR · Native gate plan`; `PR · Trusted Plan`; `PR · Source format`; `PR · Runner Interface`; `PR · Exact Candidate`; `PR · Candidate-added checks (advisory)`; `PR · Focused Python`; `PR · Demo Pin`; `PR · Go unit · cli-0`; `cli-1`; `cli-2`; `cli-3`; `packages`; `owner`; `PR · Validation · pr-planner-tests`; `go-vet`; `go-build`; `cli-gofmt`; `receipt-execution-tests`; `ci-policy`; `ci-executor-tests`; `PR Selected Checks`; `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities`; `PR · Selected Runtime (atomic/podman/observability, podman, observability) / Executed podman · observability`; `PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) / Executed podman · data-capabilities`; `PR · Selected Runtime (atomic/docker/observability, docker, observability) / Executed docker · observability` | `PR · Main release Go · ${{ matrix.shard }}`; `Release Source Preflight`; `PR · Exact full Pre-Release`; `PR · Draft source and routing`; `Targeted · Workstation onboarding · ${{ matrix.runtime }}`; `Targeted HA · docker`; `Targeted HA · podman`; `validate`; `PR · Draft Go · ${{ matrix.shard }}`; `PR · Main release source`; `PR · Native · ${{ matrix.id }}`; `PR · Consumer Pins`; `PR · Native Keycloak/Core · ${{ matrix.runtime }}`; `PR · Selected Core-less · ${{ matrix.runtime }}`; `PR · Public Contracts`; `PR · Main release checks` |

The skipped `PR · Native Keycloak/Core` job is material to the card’s native proof requirement. Relevant behavior logs from the four selected runtime jobs in each run show:

- Docker data-capabilities: `PASS New/Edit SQL Lifecycle`, `demo-data-capabilities PASS`, `RESULT PASS`.
- Podman data-capabilities: `PASS New/Edit SQL Lifecycle`, `demo-data-capabilities PASS`, `RESULT PASS`.
- Docker observability and Podman observability: each logs `PASS Metrics`, `PASS Telemetry / Traces`, `PASS Logs`, `demo-observability PASS`, `RESULT PASS`.

These log lines evidence execution of the selected demo data-capabilities and observability workloads; they do not evidence Native Keycloak/Core execution.

## Commit identity verdict

Scope: all ten commits in `origin/develop..HEAD`, read as `%H %an %ae %cn %ce %s`, plus the relevant commit bodies. The canonical card owner is `w165-0428-078-pr1650-basehop` (`tasks/t-20261114-r28-perses-dashboard-identity.md:38`).

| Commit(s) | Identity and subject | Class |
|---|---|---|
| `37c4d847`, `1c33e910`, `af256c3f`, `156507ee`, `903991f3`, `8e4a10f3` | Author and committer `w165-0428-078-pr1650-basehop <w165-0428-078-pr1650-basehop@baseharbor.local>`; merge, fix and test subjects for #1650 | Canonical lane |
| `2c4073189d8a` | Author/committer `w165-0428-078-pr1650-basehop`; `fix(0428-078): reintroduce #1650 identity-keycloak dashboard witness on new develop (rebase-drop recovery)`. Body documents restoring the 0428-078 witness after a rebase drop and wiring it into local/remote faces. | **Same-lane shortened-formatting class; admissible documentation** for canonical lane w165 |
| `b95df510879e` | Author/committer `w165-0428-078-pr1650-basehop`; `style(0428-078): retrigger full CI on hop head c6ba608f6 (second same-head run)` | **Same-lane shortened-formatting class; admissible documentation** for canonical lane w165 |
| `ed2fb751a45e` | Author `w181-0428-doclink-sweep <w181-0428-doclink-sweep@baseharbor.local>`; committer w165; `docs: reconcile PR #1843 row count from 40 to itemized 38 (H-V44 arithmetic)` | **Genuinely foreign**: card 0428-319, owner w181 at `tasks/t-20261125-hunt44-doclink-repair-sweep.md:10` |
| `f89f506f50c2` | Author `w181-0428-doclink-sweep <w181-0428-doclink-sweep@baseharbor.local>`; committer w165; `docs: remove stray top-level file from #1843 (keep docs/**-only)` | **Genuinely foreign**: card 0428-319, owner w181 at `tasks/t-20261125-hunt44-doclink-repair-sweep.md:10` |
| `2c407318` and `b95df510` are documented as same-lane shortened formatting; `ed2fb751` and `f89f506f` remain genuinely foreign after re-reading their commit bodies. |  | **IDENTITY FAIL — MERGE WITHHELD.** Rebase/base integration and green CI cannot admit foreign authorship. |

## Reissue recommendation for Coordinator dispatch

Choose **clean single-lane rebuild**, not a forward-only attestation. A forward-only attesting commit can make provenance visible and produce a reviewable new head, but it cannot remove the two foreign ancestors from the existing PR lineage; therefore it cannot cure the admission failure.

Start a fresh branch owned by canonical card owner `w165-0428-078-pr1650-basehop` at current `develop` `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`. PR #1650 Files API returns these paths: `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `internal/metrics/identity_dashboard_witness.go`, `scripts/pr-gate-coverage.json`. Reapply only the substantive 0428-078 payload in the first three files. The JSON file has a final-newline-only diff, so it is not a semantic write-set change. The card’s declared scope is identity dashboard assets and focused tests (card lines 48–50); close the noted panel and alerting evidence gaps within that declared scope before acceptance. Keep #1650 OPEN until replacement reviewable, then close it as contaminated-lineage audit when the replacement is ready. No history rewrite or force-push.

```sh
git fetch origin develop
git switch -c wNNN-pr1650-0428-078-clean-reissue origin/develop
# Reapply only the reviewed card-scoped payload with canonical lane identity.
git diff origin/develop...HEAD --name-status  # require non-empty, scoped payload
git merge-base --is-ancestor origin/develop HEAD  # require exit 0
```

## Other open PRs in the same reissue class

The prior seven-PR identity audit classified every listed head as carrying at least one genuinely foreign author; there was no admissible shortened-formatting exception in those heads. These are the other sweep PRs to dispatch once, as Coordinator-led clean reissues under their card owners:

| PR | Identity witness | Reissue owner |
|---|---|---|
| #1833 | 6/6 commits foreign | `w147-0428-288-pr1833-fix` |
| #1820 | 18/18 commits foreign | `w69-0428-271-brokerid2` |
| #1819 | 9 foreign, 2 canonical | `w54-0428-181-export` |
| #1818 | 4/4 commits foreign | `w165-0428-078-pr1650-basehop` |
| #1812 | 9/9 commits foreign | `w170-0428-249-demo-pr175-fixup` |
| #1842 | 3 foreign, 8 canonical | `w198-0428-284-demo-parser` |

#1842 is the live implementation PR rather than a worker-evidence PR; its foreign ancestry still puts it in the same reissue class.

## Final witnesses

- GitHub review exists on #1650 with state COMMENTED, not APPROVED.
- #1650 remains OPEN at exact head `37c4d847ca377d1555163ac4791c8ba08b85de77`.
- develop unchanged at `ac7c970fe91a`, #1650 OPEN, zero CI triggers.
