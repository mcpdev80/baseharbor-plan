---
id: t-20261106-r27-remote-up-podman-owner-missing
card_number: "0427-117"
card_short_title: "podman-family Deploy owner"
title: "Remote app up on Podman family fails with ErrDeploymentOwnerMissing"
release: v0.4.27
priority: high
type: bug
areas: [cli, remote]
owner: 0427-117-podman-owner
kanban_status: review
kanban_title: "0427-117 · podman-family Deploy owner"
kanban_lane: review
depends_on: [t-20261017-release-0-4-27-updates, t-20261106-r27-remote-up-cli-path]
prs: [mcpdev80/baseharbor#1419]
repos: [mcpdev80/baseharbor]
blocker: ""

---

- [ ] t-20261106-r27-remote-up-podman-owner-missing · Remote up: podman-family deployment owner missing (ErrDeploymentOwnerMissing) #task #release/v0-4-27 #status/review #view/review #area/cli #area/remote #kind/bug
    <!-- generated:card -->
    **Owner:** 0427-117-podman-owner · **Priority:** high  
    **PR:** [baseharbor#1419](https://github.com/mcpdev80/baseharbor/pull/1419)  
    **Needs:** [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md)  
**Owner:** 0427-117-podman-owner  
**Priority:** high  
**PRs:** [baseharbor#1419](https://github.com/mcpdev80/baseharbor/pull/1419)  
**Source:** 
<!-- /generated:links -->

## Purpose

w273 ran the pure-client remote `baha app up` cell at candidate head 2651a5c9869 on baha-podman-2
(vm-locked, journal claim 22:00->release 22:08Z): deployment reports ErrDeploymentOwnerMissing while the
Docker family passes the identical scenario (w264 round-2, baha-docker cell green). The connector-routed
up path apparently does not record or resolve the deployment owner for the podman runtime family.

## Acceptance

- Same-scenario cell on baha-podman passes (up -> doctor health OK); owner record present and resolvable.
- Root cause with file:line in the akte; regression cell red-first.

bahn nach system-reboot frisch beauftragt (takeover der toten lane), konfliktfreie produkt-/testarbeit unter aufgehobenem basis-HOLD (develop 934be499b), .github weiterhin owner-tabu

PR #1419 offen gegen develop (head work/r27-remote-up-owner-missing); 2 checks rot (PR Selected + Source format) — bahn 117 arbeitet selbst daran (eignes-run), noch kein END; diese karte ist der schluessel-unoock fuer 110/116.

kopf 8b5075d2 auf develop 934be499b (ancestor belegt), MERGEABLE, ci 42336410875 terminal (source-format per datei-auszug deployment_owner_loan.go 824->776, selected-checks base ok, validation gruen), unit-red-first TestOwnerLoanRegression gruen, podman-2 reproduction in akte owner-missing-round-2.md auf main. docker/podman runtime cells am PR skipped (ci.yml push-ref limit = OWNER-gate, siehe 1418). act-1419a review dispatcht.
