---
id: t-20261108-bughunt-0427-shared-core-machine-consent
card_number: "0427-123"
card_short_title: "shared-core consent blocks"
type: bug
areas: [lifecycle,dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "coordinator"
kanban_status: closed
kanban_lane: closed
kanban_summary: Merged unit/contract fixes are not native Docker/Podman PTY acceptance; see open test requirements below.
kanban_title: "0427-123 · shared-core consent blocks"
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1445, mcpdev80/baseharbor#1446]
sources: []
blocker: ""
wait_reason: "PRs #1445 and #1446 merged. Native PTY Docker/Podman two-stage app down and denial proof still needed."
resolution: accepted
evidence: ["https://github.com/marcel/dev/baseharbor/commit/db06f01e9", "https://github.com/mcpdev80/baseharbor/commit/db06f01e9", "https://github.com/mcpdev80/baseharbor/commit/1446"]

---

## Outcome and acceptance

Merged unit/contract fixes are not native Docker/Podman PTY acceptance; see open test requirements below.

- [x] t-20261108-bughunt-0427-shared-core-machine-consent · 0427-123 · App up/down haengt an machine-consent #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/dx #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1445](https://github.com/mcpdev80/baseharbor/pull/1445), [baseharbor#1446](https://github.com/mcpdev80/baseharbor/pull/1446)  
    **Waiting:** PRs \#1445 and \#1446 merged. Native PTY Docker/Podman two-stage app down and denial proof still needed.  
    **Evidence:** [proof 1](https://github.com/marcel/dev/baseharbor/commit/db06f01e9), [proof 2](https://github.com/mcpdev80/baseharbor/commit/db06f01e9), [proof 3](https://github.com/mcpdev80/baseharbor/commit/1446)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1445](https://github.com/mcpdev80/baseharbor/pull/1445), [baseharbor#1446](https://github.com/mcpdev80/baseharbor/pull/1446)  
**Source:** 
<!-- /generated:links -->

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF-2 docker2 hunt: up/down on shared-core is not completable without machine-consent digest; down hangs after consent prompt. Related to (not identical with) 0427-120's --confirm-candidate flag.

## Acceptance

up/down complete through documented interactive flow without hanging; any required confirmation is explicit, single, and recoverable; stuck-state cleanup exists.

## Dependencies and file ownership

Depends only on the release umbrella. Write-set per repo rules; intake evidence carries the exact repro.

## 2026-11-08 Takeover (ChatGPT)

- Owner `owner:chatgpt`; `active`. Security-relevant consent flow: investigate the interactive app-up/down path and the existing `ProviderChangeConsent` check against the VM reproduction. Do not weaken the release or data-deletion gates. First a real negative/positive test, then a tighter product fix.

## 2026-11-08 Consent path check (ChatGPT)

- The current local CLI stop path `authorizeApplicationStop` under `cmd/baha/application_stop_impact.go` offers `readProviderImpactAcknowledgements` on a detected terminal, then checks afterwards via `ValidateProviderImpactScopeConsent`, and verifies the unchanged plan before mutation. The machine-readable consent remains bound to the current `plan_id` via `BASEHARBOR_PROVIDER_CHANGE_CONSENT`; generic `--yes` is **intentionally** not enough.
- The bug hunt describes a blocking prompt on real rootless Docker for `baha app down`, but still no exact current `develop` PTY trace that distinguishes missing terminal input, divergent plan ID, and missing scope confirmation. The existing `readProviderImpactAcknowledgements` test validates the security logic, but not the real PTY path.
- Kein Sicherheits-Bypass und keine behauptete Behebung. Naechster konkreter Nachweis: PTY-E2E mit 2× `y`, Plan-SHA-Vergleich und timeout-gesteuertem Abbruch; danach ggf. lokaler CLI-Input-Fix. Karte bleibt `active`.

### 2026-11-08 DIAG_EXEC-Teilfehler (ChatGPT)

- In `cmd/baha/app_machine_adapters.go`, the current `develop` has two **unconditional** `fmt.Printf("DIAG_EXEC ...")` on machine-provider-change failure. These debug outputs bypass the stable machine-readable error boundaries, disturb stdout, and may expose outcome details. As a safe, tightly scoped **partial fix** of 0427-123 they are removed without changing the consent/result logic and tested against regression. This partial fix is **not** the solution to the PTY down hang; the card stays active thereafter.

- **Partial-error fix PR:** [#1445](https://github.com/mcpdev80/baseharbor/pull/1445), head `f80dc0b9eefc0b4f757ec4ba4d05a500e569f450` removes both unfiltered `DIAG_EXEC` stdout prints and adds a source regression. No consent security bypass. Exact-head CI open, PTY hang still to be fixed separately.

## 2026-11-08 Merge Evidence PR #1445 (ChatGPT)

- **Partial-error fix: unfiltered DIAG_EXEC stdout removed:** [PR #1445](https://github.com/mcpdev80/baseharbor/pull/1445) merged to `develop`, merge SHA `db06f01e9fd793706da5072769922a0c64afecf0`; [exact-head CI #42430983626](https://github.com/mcpdev80/baseharbor/actions/runs/42430983626) terminal `success`, no failed jobs.
- **Card stays `active`:** the real native Docker/Podman end-to-end acceptance of the original bug is still pending. The merged partial fix does not replace this.

## 2026-11-08 Interactive consent regression test (ChatGPT)

- [PR #1446](https://github.com/mcpdev80/baseharbor/pull/1446) Head `90e9aae7f5c07729a309f97672f60247885c4845`: reproduziert `authorizeApplicationStop` auf dem echten CLI-Autorisierungspfad mit einer endlichen interaktiven Eingabe (2x `yes`, Ablehnung Stufe 1, Ablehnung Stufe 2). Prueft Erfolg nur bei aktueller Plan-ID und fail-closed bei Ablehnung. Noch kein echter PTY auf Docker/Podman; CI offen, Karte weiterhin `active`.

## 2026-11-08 PR #1446 successfully merged (ChatGPT)

- [PR #1446](https://github.com/mcpdev80/baseharbor/pull/1446) successfully merged to `develop`: `f9e207ac0d0b4c983fbb01d4357a8784c41c92de`. Exact-head [CI #42431899984](https://github.com/mcpdev80/baseharbor/actions/runs/42431899984) terminal `success`, **10 PASS, 0 FAIL, 0 pending**.
- Real `authorizeApplicationStop` code path with two yes-confirmations, refusal in level 1/2, current plan bound regression-tested. **Card stays active:** real PTY and native Docker/Podman lifecycle evidence still pending, no security bypass whatsoever.

## 2026-11-08 Acceptance correction (ChatGPT)

- **Prior `closed/accepted` was premature**: code/PR merge links are not native end-to-end proof. Real PTY two-stage app down on BOTH Docker and Podman still lacks exact SHA and PASS-not-SKIP evidence.
- Reopened to `active` with existing code evidence retained. Do not close until exact integration SHA, native runtime output, verified resource preservation/removal, no SKIP, and VM cleanup are recorded.

## 2026-11-08 Owner Release and Handover

- Processing owner changed from `"owner:chatgpt"` to `coordinator`. Board column `wait` (dependency / pending native acceptance; **no** technical `blocked` alarm).
- PRs #1445 and #1446 merged. Native PTY Docker/Podman two-stage app down and denial proof still needed.
All existing PR, commit, and CI evidence remains unchanged. No new PASS claimed.
