---
id: core-815
card_number: "0427-003"
card_short_title: "start all greenfield stacks on"
areas: [testing]
type: acceptance
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-003-podman2-bughunt
kanban_lane: active
kanban_summary: Every shipped built-in greenfield stack satisfies baha app new … → generated source repo → baha up → READY on Docker and Podman…
kanban_status: active
kanban_title: "0427-003 · start all greenfield stacks on"
depends_on: [core-893, core-895, core-896, t-20261017-release-0-4-27-updates, t-20261103-ci-plain-checks]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1429, mcpdev80/baseharbor#1432]
sources: ["mcpdev80/baseharbor#815"]
source_updated: "2026-10-15T16:50:55Z"
labels: [kind/acceptance, area/runtime, area/evidence, area/dx]
blocker: ""
resolution: ""
evidence: []
wait_reason: ""

---

- [ ] core-815 · Tests: start all greenfield stacks on native runtimes #task #release/v0-4-27 #status/active #view/active #area/testing #kind/acceptance
    <!-- generated:card -->
    **Owner:** lane-0427-003-podman2-bughunt  
    **PR:** [baseharbor#1429](https://github.com/mcpdev80/baseharbor/pull/1429), [baseharbor#1432](https://github.com/mcpdev80/baseharbor/pull/1432)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md)  
**Owner:** lane-0427-003-podman2-bughunt  
**Priority:** not set  
**PRs:** [baseharbor#1429](https://github.com/mcpdev80/baseharbor/pull/1429), [baseharbor#1432](https://github.com/mcpdev80/baseharbor/pull/1432)  
**Source:** [baseharbor#815](https://github.com/mcpdev80/baseharbor/issues/815)
<!-- /generated:links -->

## Goal

Every shipped built-in greenfield stack satisfies `baha app new … → generated source repo → baha up → READY` on Docker and Podman with required managed bindings and no manual source repair.

## Scope

- Remaining scope after published v0.4.23: the Go/Next.js/Quarkus build corrections were delivered in merged PR #809 / v0.4.23. Native template run [37508074031](https://github.com/mcpdev80/baseharbor/actions/runs/37508074031) at `9865135c613c2c5cb73f88f95c60a65685ee6227` passed fresh image builds for all four stacks on Docker and Podman (SQL/managed-secret contracts, no runtime credentials as build inputs) and actual Python startup/secret delivery; it does **not** qualify startup of all four stacks.
- Open: Docker/Podman generated-application startup and READY evidence for Go, Next.js, Python and Quarkus on the current candidate with exact inputs; historical v0.4.23 greens cannot substitute.
- Original defects (baseline v0.4.22 `1aa1a503facc1f4cbbd58fab21619fda53ed6d47`): Go `go.sum`/module state required `go mod tidy`; Next.js validated runtime env at build time; Quarkus Maven config did not produce `target/quarkus-app/`. Python was the control.

## Acceptance

- Go fresh scaffold builds and reaches READY without manual `go mod tidy`.
- Next.js fresh scaffold builds with runtime bindings resolved at runtime, not build import time.
- Quarkus fresh scaffold produces the artifact layout its Dockerfile consumes.
- Python remains green.
- The generated portable contract remains equivalent across stacks except app identity.
- Focused Docker + Podman scaffold acceptance, including READY for all four stacks.

## Required checks

- Targeted native template startup gates on Docker and Podman for the current candidate.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Earlier parent #571 (closed); related #210 (closed).

## Handoff

- Build part delivered; startup acceptance outstanding (pre-freeze acceptance under v0.4.31).

## Additional acceptance: control-plane default (Owner, 2026-11-06)

- Governing contract: `t-20261106-r27-control-plane-single-default`. Every fresh, unmodified `baha up` default path for all four greenfield stacks MUST demonstrate the actual SINGLE control-plane topology (exactly one instance per required service, no HA members or load balancer). Reaching `READY` alone is insufficient.
- On BOTH `baha-docker` and `baha-podman`, record product SHA, rendered default Compose configuration, container count/names, service health, and exact startup commands. Fixtures must not silently enable HA or override the default.
- Before accepting this card, demonstrate both an explicit HA positive scenario and a default-HA negative scenario from the governing contract. Older green HA-default runs do not qualify this requirement.

owner-direktive #5 + karte 'no open deps, build delivered' -> startup READY acceptance (Go/Next/Quarkus/Python) + single-control-plane default proof. docker jetzt (host sauber), podman-seite moeglichst #107-DNS-blocked (ehrlich melden). write-set templates, NICHT source_oci/registry (#118) noch .github (#021).

r1 END_DONE: Go+Python READY+SINGLE-default auf baha-docker belegt, regression keiner-neu. r2 laeuft (lane busy): QUARKUS-FIX 0d8639c3d (emit compose healthcheck /q/health -> baha up READY) GELIEFERT aber DRIFT (base 0c4e59cdad, develop 812c99c88 NICHT vorfahr) -> VOR REVIEW rebase. nextjs/quarkus JETZT auf baha-docker-2 (14GB avail, maschine bereitgestellt gem. owner-direktive, KEIN host-blocker). PODMAN-SEITE noch NICHT -> haengt an #110/#107 podman readiness. karte active bis alle 4 stacks x docker+podman READY.

quarkus healthcheck fix PR#1429 (0743011c) drift-frei, delta nur quarkusadapter 2 dateien, CI 8pass. CODEX-REVIEW. REST der karte (podman-seite + alle 4 stacks) haengt an #110/#107 podman readiness -> karte bleibt active bis podman zellen durch.

DOCKER-SEITE + QUARKUS-FERTIG: Go/py/nextjs READY+single-default belegt, quarkus PR#1429 (0743011c) drift-frei CI terminal 8-pass -> CODEX-REVIEW. lane 9389395c PARKTE an shell (blind-spot) -> freigegeben (PR ist traeger). REST DER KARTE: PODMAN-SEITE aller 4 stacks + single-default noch NICHT belegt — haengt an #110/#107 podman runtime readiness (KEIN host-blocker; maschinen bereitgestellt). karte bleibt active bis podman-zellen durch. re-dispatch wenn #110 podman ready.

## Owner CI wiring — 2026-11-07

- [Core PR #1432](https://github.com/mcpdev80/baseharbor/pull/1432) adds real eight-cell native Greenfield `go/nextjs/python/quarkus × docker/podman` source-to-`baha up` checks to the **existing** `nextjs-greenfield-e2e.yml` and wires a mandatory `v0.4.27` full Pre-Release job; no additional workflow file and no new default PR Runtime-gate.
- Exact candidate native validation [run 42390280687](https://github.com/mcpdev80/baseharbor/actions/runs/42390280687), code SHA `163561dc14bcc2c2afe940a1d2bb0f911c736b01`, was started. A newer branch revision additionally binds the Pre-Release check; validate that revision separately before merge.
- Card **remains active** until all eight native cells genuinely PASS, default SINGLE control-plane resource counts and explicit HA/negative checks are documented. A mere workflow definition, pending run or source-format green is **not** an accepted Greenfield test.

## Native test result — 2026-11-07

- Actual [native run 42390908119](https://github.com/mcpdev80/baseharbor/actions/runs/42390908119), exact candidate `7065690f130fd2718c4e6852824bf0d2915ff724`: **Next.js / Docker PASS**, including real `baha app new`, Core bootstrap, scoped non-destructive provider consent, `baha up`, status + doctor and cleanup. Other seven matrix cells were not yet all terminal at this snapshot. Do not generalize that one PASS into an eight-cell acceptance.
- [PR #1432](https://github.com/mcpdev80/baseharbor/pull/1432) now adds a stronger typed JSON `ready=true`, workload and per-service readiness verification and the explicit v0.4.27 pre-release gate; validate on newer exact-source [run 42391107321](https://github.com/mcpdev80/baseharbor/actions/runs/42391107321).
- Keep 0427-003 **active** pending eight native successes, default-SINGLE + explicit HA and negative topology evidence; source PR is not merged.

## Native 8/8 qualification — 2026-11-07

- [Greenfield Native Stack E2E #42391107321](https://github.com/mcpdev80/baseharbor/actions/runs/42391107321) completed **SUCCESS** on exact candidate `6e06cb6a85ede34df5a0ea9fd23a825f49c8f03b`. All **8 required native matrix jobs** completed SUCCESS: Go, Next.js, Python, Quarkus each on Docker and Podman. Legacy Next.js Docker E2E also SUCCESS.
- [PR #1432 CI #42391093788](https://github.com/mcpdev80/baseharbor/actions/runs/42391093788) completed SUCCESS on the **same SHA**. No skipped required Greenfield matrix job in the native run.
- **Do not mark card accepted yet:** exact SINGLE default topology container counts plus explicitly enabled HA positive and default-HA negative scenario remain required by the governing card. This native application READY matrix is not proof of those topology assertions. PR #1432 remains open pending those acceptance details.

## Mitarbeit / Assignment-Abgleich — 2026-11-07

- **Mitwirkender:** ChatGPT (CI/Owner-Unterstützung). Implementiert PR [#1432](https://github.com/mcpdev80/baseharbor/pull/1432), Native Docker/Podman Matrix 8/8 auf SHA `6e06cb6a85ede34df5a0ea9fd23a825f49c8f03b` geprüft und Kanban/Evidence aktualisiert. Der bestehende `owner` bleibt die Implementierungs-Lane; ChatGPT betreut CI-Integration/Abnahme. Status **active** bis vollständiger SINGLE-/HA-Nachweis und Merge.

podman-seite: hand-festival auf baha-podman-2 (frisch rebuildet, w283) — gleiche direktive: greenfield/brownfield/wizards, KEIN HA, nur befundung. lane 486b2d02.


## PR-Lifecycle-Abgleich — 2026-11-08

- [PR #1429](https://github.com/mcpdev80/baseharbor/pull/1429) ist inzwischen gemergt; [PR #1432](https://github.com/mcpdev80/baseharbor/pull/1432) ist weiterhin offen auf Head `6e06cb6a85ede34df5a0ea9fd23a825f49c8f03b`.
- Der dokumentierte native 8/8 Docker/Podman-READY-Lauf ist nicht gleichbedeutend mit den separat geforderten SINGLE-/HA-Topologie-Nachweisen. Karte deshalb weiterhin `active`, keine Doppelarbeit durch neuen Worker und kein irrtuemlicher Mergehinweis fuer #1432.


## Source-Vergleich zu PR #1432 — 2026-11-08

- PR #1432 (`6e06cb6a85ede34df5a0ea9fd23a825f49c8f03b`) hat einen alten erfolgreichen [CI-Lauf #42391093788](https://github.com/mcpdev80/baseharbor/actions/runs/42391093788), liegt gegen aktuelles `develop` jedoch **135 Commits behind, 14 ahead** (divergiert). Der bisherige 8/8 Native-Greenfield-Erfolg ist SHA-genau, aber nicht automatisch ein PASS auf aktuellem Integrationskopf.
- Vor Merge aktualisierten Diff auf `develop` abstimmen; danach relevante native Zellen inkl. SINGLE-default, HA-opt-in und HA-negative acceptance auf exakt dem Integrations-SHA pruefen. Solange kein aktueller Beleg vorliegt bleibt `active`, kein Merge allein aufgrund historischer gruener CI.
