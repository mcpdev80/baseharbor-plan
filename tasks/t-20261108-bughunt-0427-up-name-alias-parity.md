---
id: t-20261108-bughunt-0427-up-name-alias-parity
card_number: "0427-130"
card_short_title: "baha up NAME rejected"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: ""
owner: codex-merge-1474
kanban_status: review
kanban_lane: review
kanban_summary: baha up NAME resolves the registered application NAME identically to baha app up NAME; the top-level alias exposes the full…
kanban_title: "0427-130 · baha up NAME rejected"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1459, mcpdev80/baseharbor#1474]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261108-bughunt-0427-up-name-alias-parity · Bug Hunt v0.4.27: baha up NAME rejected although app up [NAME] documented #task #release/v0-4-27 #status/review #view/review #area/dx #kind/bug
    <!-- generated:card -->
    **Owner:** codex-merge-1474 · **Priority:** normal  
    **PR:** [baseharbor#1459](https://github.com/mcpdev80/baseharbor/pull/1459), [baseharbor#1474](https://github.com/mcpdev80/baseharbor/pull/1474)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** codex-merge-1474  
**Priority:** normal  
**PRs:** [baseharbor#1459](https://github.com/mcpdev80/baseharbor/pull/1459), [baseharbor#1474](https://github.com/mcpdev80/baseharbor/pull/1474)  
**Source:** 
<!-- /generated:links -->

## Goal

`baha up NAME` resolves the registered application NAME identically to `baha app up NAME`; the top-level alias exposes the full documented argument surface.

## Scope

- In scope: align the top-level `up` argument parser (`cmd/baha/runtime.go`) with `app up` (`cmd/baha/app_lifecycle.go`) so the optional positional NAME is accepted; add parity test.
- Out of scope: consent semantics.

## Acceptance

- `baha up NAME --yes --plain` outside a repository resumes the registered deployment NAME (same result as `baha app up NAME`).
- Parser parity test: `up` and `app up` accept the identical flag/argument grammar.

## Required checks

- CLI parser unit test asserting `up <NAME>` parses; machine/CLI parity test against `app up`; documented in the existing cli-command grammar suite (no new CI framework).

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/runtime.go`, `cmd/baha/app_lifecycle.go`.
- Shared files: coordinate through the owning task.

## Handoff

- Found 2026-11-08 on develop 0fe53052d (build 0.4.11), test host 192.168.6.178.
- Report: ~/dev/Tests/Baha-Bug-09-up-name-vs-app-up-name.md


## PR-Lifecycle-Abgleich — 2026-11-08

- [Core PR #1459](https://github.com/mcpdev80/baseharbor/pull/1459) ist nach `develop` **gemergt** (GitHub-Status `closed/merged`, am 2026-11-08 live geprueft). Die Karte darf nicht mehr als offener PR-/CI-Fix dargestellt werden.
- Kanban bleibt vorerst `active`: die gesondert verlangte `baha up NAME --yes --plain`- und Parser-Paritaetsabnahme ist in dieser Karte nicht mit exaktem integriertem SHA dokumentiert. Der Wert `pending-lane-0427-130-r5` ist keine verifizierte laufende Session; Coordinator soll den Claim mit der tatsaechlichen Lane abgleichen oder nach Abnahme schliessen. Bestehende Worker-Dateien bleiben unangetastet.


## Code- und CI-Abgleich — 2026-11-08

- `baseharbor/develop` SHA `b73a13a909b2d7b811d6956b3bdaf93f17b80454`: `cmd/baha/runtime.go` Funktion `parseRuntimeUpOptions` akzeptiert ein optionales positional `NAME`, lehnt einen zweiten Namen ab; `runtime_repository_up.go` uebergibt `upNameArgs(opts.Name)` an den echten `resolveApplication`-Pfad.
- `cmd/baha/runtime_ports_test.go`: `TestParseRuntimeUpOptionsAcceptsOptionalName`, `TestParseRuntimeUpOptionsRejectsSecondName`, `TestParseUpParsesIdenticalToAppUpEnforcesParity` und `TestUpNameResumesRegisteredDeploymentAcceptsParity` decken den Parser und die registrierte Anwendung ab. [PR #1459 CI #42475609941](https://github.com/mcpdev80/baseharbor/actions/runs/42475609941) terminal SUCCESS am PR-Head `b3bb20416c69919af02bd854b3966cfe5e3761ca`; PR gemergt.
- **Code- und CI-Abnahme fuer die Kartenfunktion plausibel bestanden.** Eine eigenstaendige externe Laufzeitmessung mit `baha up NAME --yes --plain` ist hier nicht behauptet. Coordinator kann die Karte nach formaler Acceptance mit `plan.py render && check` schliessen; kein weiterer Produktfix am selben Scope noetig. Nicht ungeprueft neu zuweisen.
