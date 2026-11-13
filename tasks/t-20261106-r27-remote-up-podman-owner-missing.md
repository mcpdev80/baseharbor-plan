---
id: t-20261106-r27-remote-up-podman-owner-missing
card_number: "0427-117"
card_short_title: "podman-family Deploy owner"
title: "Remote app up on Podman family fails with ErrDeploymentOwnerMissing"
release: v0.4.27
priority: high
type: bug
areas: [cli, remote]
owner: mcpdev80
kanban_status: closed
kanban_title: "0427-117 · podman-family Deploy owner"
kanban_lane: closed
depends_on: [t-20261017-release-0-4-27-updates]
prs: [mcpdev80/baseharbor#1419]
repos: [mcpdev80/baseharbor]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-7.md"]

---

- [x] t-20261106-r27-remote-up-podman-owner-missing · Remote up: podman-family deployment owner missing (ErrDeploymentOwnerMissing) #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/cli #area/remote #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 · **Priority:** high  
    **PR:** [baseharbor#1419](https://github.com/mcpdev80/baseharbor/pull/1419)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-7.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261106-r27-remote-up-cli-path](t-20261106-r27-remote-up-cli-path.md)  
**Owner:** mcpdev80  
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

CODEX act-1419a REJECT_LANE_FIX (inhaltlich, NICHT wegen ci-cells): bisher nur marker-proof am seam, realer remote-podman app-apply faellt weiter auf ErrDeploymentOwnerMissing. rezept= deployment_record.go:57-65,137-145 echte owner-resolution. frische bahn 0427-117-owner-resolve dispatched; dieser fix unblockt 110+116.

r4 geliefert: head c0ac3bef auf develop eee11d50 (ancestor rc0), MERGEABLE, run 42342771963 terminal incl selected-checks+source-format, owner-resolution jetzt REAL (BASEHARBOR_TARGET-first) statt marker-only, regression ROT-ohne/GRUEN-mit, akte auf main. act-1419b re-review dispatcht; dieser merge unblockt 110+116.

CODEX act-1419b REJECT_LANE_FIX (inhaltlich): owner-loan ist testing.Testing()-GATED, loest NICHT den produktiv-podman apply; regression ruehrt SaveDeploymentRecord direkt statt echtem CLI apply. rezept= recordDeploymentBeforeMutation echte owner-resolution + echter-cli-apply regression mit woertlicher ausgabe. frische bahn 0427-117-prod-owner dispatched (ornith); unblockt weiterhin 110+116.

r5 geliefert: head 438895466 auf develop eee11d50 (ancestor rc0), MERGEABLE, run 4989 terminal incl selected+cli-package, 0 fails. PROD-PFAD jetzt real un-gated (recordDeploymentBeforeMutation->productionLoanAuthorityForTarget, local-boot-CORE only, fail-closed erhalten) = genau das Option-1-design das ich autorisiert hatte. regression un-gated GREEN + connector RED, akte round-5.md auf main (20e80c39). docker/podman skipped=owner ci.yml-gate (kein lane-fehler). re-review act-1419c dispatcht; ACCEPT merged und unblockt 110+116.

codex act-1419c REJECT_LANE_FIX (eng+test-only): prod-owner UN-GATED real + fail-closed ok BESTAETIGT, aber positive regression ruehrt bei zeile 302 saveThroughApplySeam statt echtem CLI app apply. rezept=echter CLI apply im test. bahn 0812eb78 re-woken fuer r6 (code fertig, nur test).

r6 geliefert+verifiziert: head f69f2a6c auf eee11d50 (ancestor rc0), MERGEABLE, cli-package-tests+selected GRUEN (run 4991 terminal). delta=test-only (eine regression datei, code unveraendert vom als richtig bestaetigten prod-pfad). positive regression faehrt JETZT echten CLI app apply (runApplicationApplyLifecycle) statt saveThroughApplySeam = act-1419c rezept exakt getroffen. re-review act-1419d (eng, code schon accepted) dispatcht; ACCEPT merged -> unblockt 110+116.

codex act-1419d REJECT (eng/konvergent): delta ok, code accepted-correct, nur die regression ruft record... DIREKT statt echtem lifecycle (deployment_owner_loan_regression_test.go:381-390). rezept=runApplicationApplyLifecycle/executeApplicationApplyLifecycle durchlaufen + persisted owner-record assertieren. bahn 0812eb78 r7 re-woken. jede runde enger (marker->code->seam-test->write-func->jetzt lifecycle-runner), konvergiert.

r7 disk-verifiziert: PR #1419 head 5c08ed6be echter product-owner-fix + opt2 test, hosted CI GRUEN, develop ancestor. CODEX-REVIEW laeuft.

MERGED 11:33:39Z develop beb923fe6. CODEX approve+merge, kein force. Worker freigegeben. #116 damit entblockt (wartete auf diesen landing).
