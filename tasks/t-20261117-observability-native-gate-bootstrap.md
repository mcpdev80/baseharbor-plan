---
id: t-20261117-observability-native-gate-bootstrap
card_number: "0428-114"
card_short_title: "Run observability Accept with"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: codex-open-pr-sweep-114
kanban_status: active
kanban_lane: active
kanban_summary: "Make the existing observability runtime acceptance runnable and selectable for application observability changes, so the Loki…"
kanban_title: 0428-114 · Run observability Accept with
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1708]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261117-observability-native-gate-bootstrap · CI: Run observability acceptance with verified ORAS bootstrap #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** codex-open-pr-sweep-114  
    **PR:** [baseharbor#1708](https://github.com/mcpdev80/baseharbor/pull/1708)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261117-docker-loki-ingestion-timeout](t-20261117-docker-loki-ingestion-timeout.md)  
**Owner:** codex-open-pr-sweep-114  
**Priority:** not set  
**PRs:** [baseharbor#1708](https://github.com/mcpdev80/baseharbor/pull/1708)  
**Source:** 
<!-- /generated:links -->

## Goal

Make the existing observability runtime acceptance runnable and selectable for application observability changes, so the Loki ingestion assertion executes on the exact candidate with the verified ORAS bootstrap installed.

## Scope

- In scope: add the existing verified ORAS installation step to observability-acceptance.yml; route the relevant internal/application observability source/test paths through the existing atomic/docker/observability and atomic/podman/observability gates; add focused selector/workflow regressions and verify positive and negative selection.
- Out of scope: new gates or CI framework, weakening Loki or consent assertions, changing security.go, full-release qualification; das Postgres-image bleibt non-root (owner-vorgabe 2026-11-19).
- Erweiterter umfang (Coordinator-entscheid 2026-11-19, delegation des owners): dieselbe korrekturklasse fuer die zwei funde aus 0428-128 — (a) `.github/workflows/docker-runtime-acceptance.yml`: der job `docker-runtime` (zeilen 174-330) erhaelt den existierenden ORAS-install-schritt `bash scripts/ci-install-oras.sh` (genau die zeile, die im push-job zeile 128 steht), damit der exact-head-dispatch-pfad den runtime-test mit trust-plane ausfuehrt; (b) `scripts/pr-gate-coverage.json`: ein gemappter trigger fuer `TestPersesRuntimeSmokeDockerIsolated` (BASEHARBOR_PERSES_RUNTIME_SMOKE), damit die native perses-zelle in den PR-checks laeuft statt still skipped.
- Akzeptanz-erweiterung: nach diesem change sind (i) auf #1690 (0428-119) und (ii) auf #1592 (0428-088) exact-head docker-runtime-zeugen produzierbar; die beiden karten bleiben bis dahin blocked mit ZWEIFEL.


## Acceptance

- PR native gate plan selects both existing observability gates for the 0428-113 application source paths and does not select them for an unrelated path.
- Docker and rootless Podman runs install verified ORAS and execute TestObservabilityFullStackAcceptanceInCI against exact SHA 504a8678c2391cb379622fa02c2c8d9769fa192b.
- Both runs reach the Loki provider workload query and pass without weakening the assertion; preserve expected negative-consent refusal.
- Record test -> gate -> trigger -> run URL/outcome. Keep PR #1680 unmerged until exact runtime evidence is green.

## Test binding

- Test binding: new existing-gate selection/workflow coverage; use the CI owner routed PR checks, not a new gate.
- Tests: add focused selector tests in scripts/test_pr_gate_plan.py for application observability paths (positive Docker+Podman selection and unrelated-path exclusion), plus a workflow contract assertion that the verified ORAS installer runs before the observability test.
- CI route: PR Focused Python / PR native gate plan, then existing atomic/docker/observability and atomic/podman/observability workflows on the exact 0428-113 candidate SHA.

## Required checks

- Existing failed dispatches [Docker 44057603711](https://github.com/mcpdev80/baseharbor/actions/runs/44057603711) and [Podman 44057705927](https://github.com/mcpdev80/baseharbor/actions/runs/44057705927) both stopped before runtime setup completed: ORAS missing at cmd/baha/app_observability_acceptance_test.go:34.
- The PR native gate matrix on [run 44057402207](https://github.com/mcpdev80/baseharbor/actions/runs/44057402207) selected no native gates for internal/application/runtime_observability.go.

## Dependencies and file ownership

- Owned files or areas: shared CI gate selection and observability acceptance workflow.
- Shared files: coordinate with the current CI owner before editing scripts/pr-gate-plan.py, CI workflow files or gate catalogs.

## Handoff

ZWEIFEL queued for the existing CI owner. Exact failure evidence is in runs 44057402207, 44057603711 and 44057705927. Product PR #1680 remains open pending proper runtime acceptance.

## Handoff update (2026-11-20)

- PR #1708 is OPEN + Ready at exact head `542e3b6e2d692e8b39db0b80fc4057f027fba452`; its recorded base SHA is `b7cbc00f0adfa36945d6f7af8098d88096276c4f`, while live `develop` has advanced to `83b19dce24eed2f837dd2dda7d56222d20a7da32`, so the PR is behind. The prior exact PR run `44655129333` was cancelled by the next head update while its selected Docker observability gate was executing; it is not a pass. New exact PR run `44656039328` is queued/running.
- Docker + Podman dispatch `44655136998` executed the acceptance test on both runtimes, but both failed at `TestObservabilityFullStackAcceptanceInCI`: the fixture's `app apply` supplied provider-impact consent but omitted the now-required exact `--confirm-candidate` digest. Runtime preparation, ORAS installation, image build and isolated OCI publication passed on both runtimes. This is acceptance-fixture behavior, not evidence of a runtime-specific failure.
- Updated the acceptance fixture to first observe the fail-closed candidate-consent error, extract only its exact digest, then retry with explicit candidate consent while retaining provider-impact consent. Local verification at the new source: `go test ./cmd/baha -run '^TestObservabilityFullStackAcceptanceInCI$' -count=1` (compile; skipped without runtime opt-in), source-readability audit, and `git diff --check` passed. Exact Docker + rootless Podman dispatch `44656074577` completed SUCCESS on the new head; both full-stack observability acceptance jobs passed. Exact PR run `44656039328` remains active in its selected Docker observability gate, with its non-runtime required jobs green at last check.
- The old acceptance target SHA `504a8678c2391cb379622fa02c2c8d9769fa192b` is no longer current develop. The next accepted-source run must use a verified current source commit after this PR head is qualified and hopped to current develop.
- Independent read-only audit of #1594 / 0428-053 confirms its policy-aware helpers have no production consumers; current callers still use name-only wrappers. Exact draft run `44653386231` failed the CLI shards because routine local `dev` flows now demand managed OIDC, and its package shard also has unrelated missing Perses/Loki client-cert fixtures. Stable target/environment IDs identify scope but do not grant `TrustedLocal`. Keep #1594 DRAFT and blocked pending an owner-approved authoritative policy source and production caller scope; do not infer trust from names or identifiers.
- Downstream blocked-stack audit: #1615/0428-057 is OPEN+Ready at `f93564a0` but based on `cli2-env-policy-head` (`2af892e4`) and has no PR run/status; #1620/0428-067 is OPEN+Draft at `fcba5d25`, one commit behind that base and has no PR run; #1623/0428-063 is OPEN+Draft at `8014d71e`, 167 commits behind current #1615 and has no PR run. Their plan blockers remain valid pending #1594 policy resolution, monotone stack hops and CI trigger repair. Independent audit also reconfirmed #1623 behavior gaps (`app logs -c` does not apply the filter, `app exec --cmd` does not shell-parse, child exit status is collapsed). Do not hop or change these owner PRs.

reichweite erwisert (entscheid statt sequenzierung): 114 besitzt jetzt beide 128-symptome mit datei:zeile. grund: 114 hat keinen lebenden sitz und keinen PR (nur ein nominaler owner-vermerk), eine sequenzierung 'warte auf 114, dann 128' wuerde 119/088 unbefristet blockieren; zugleich wuerde eine separate 128-aenderung dieselbe coverage-map zwei mal anfassen

inhalt bleibt gleich, nummer (e) neu aufgenommen: erklaert den F-7-fehljob aus dem closeout-heft, ohne dass die product-tests schuld sind

fund (e) erklaert F-7 aus dem closeout-heft ohne produkt-schuld; 119/#1690 bleibt davon unberuehrt blocked (wartet auf (a))

GEGENMASSNAHME VON MIR UMGESETZT: coord-state.py meldet jetzt DRAFT-CANDIDATE fuer jeden offenen draft-PR (neue aktion, syntax geprueft, erster treffer #1665) und der lanes=[]-bug ist behoben (beide schluessel 'session' und 'lane' akzeptiert) — dein punkt 4 aus dem prioritaeten-blatt

DRAHT-PUNKT (f) NEU, von zwei unabhaengigen beobachtungen belegt: PR-CI-FREIGABE FUER NIEDERLANDBASES. .github/workflows/ci.yml oeffnet PR-CI nur fuer base develop/main/'lane-*' — 'pull_request.branches' zeilen 14-18 und die job-bedingungen mit "github.base_ref == 'develop' || startsWith(github.base_ref, 'lane-')" auf develop zeilen 514/1137/1160 (auf dem basis-ast cli2-env-policy-head@5ef9329b analog 428/478/515). folge: jeder PR, dessen base ein ketten-ast OHNE 'lane-'-praefix ist (cli2-env-policy-head, cli2-identity-secrets-head, w083-perses-datasources, w091-0428-091), erhaelt NILLE required-CI — beleg #1615: check-suite 120471174270 'queued' seit 10:27:37Z, actions/runs?head_sha=f93564a0d… total_count=0 um 11:21:44Z, PR draft=false/ready, monoton, merge-tree 0 konflikte. VORSCHLAG: base-agnostisch machen ('github.event_name == "pull_request" && github.event.pull_request.draft == false') ODER die branches-liste um 'cli2-*' und 'w0*' erweitern; die liste ist der effektive filter, die job-bedingungen muessen mitziehen, sonst laufen die zellen als 'skipped' statt 'selected' ein. bestehende punkte bleiben: (a) ORAS-install im docker-runtime-job, (b) perses-smoke-zelle, (c) demo pr-guided-consent.yml zeilen 4-5, (d) docs/internal/*.json fuer documentation-audit, (e) toter dispatch-default 'release/v0.4.21'
