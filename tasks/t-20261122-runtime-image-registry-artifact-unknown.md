---
id: t-20261122-runtime-image-registry-artifact-unknown
card_number: "0428-249"
card_short_title: "light-runtime blob unknown"
type: bug
areas: [ci, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-249 · light-runtime blob unknown
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "Owner-Entscheidung 2026-11-22: Freigabe für eine Ursachenprüfung und genau einen PR mit der eng begrenzten Reparatur, soweit durch Befund belegt: Reihenfolge und Registry-Verfügbarkeit in .github/workflows/pre-release-runtime-suite.yml; der fehlende scripts/acceptance.sh-Vertrag in den drei Workflows, die ihn referenzieren (pre-release-runtime-suite.yml, pre-release.yml, targeted-demo-acceptance.yml), sowie scripts/pre-release-runtime-impact.json. Eine frühere Fassung von acceptance.sh nur aus belegbarer Git-Historie wiederherstellen; andernfalls die Verweise auf den vorhandenen Einstiegspunkt anpassen. Keine Ersatzlogik erfinden. .github/workflows/ci.yml und der normale CI-Pfad bleiben unverändert. Vor dem Merge müssen die Light-Runtime-Gates für Docker und Podman auf dem exakten PR-Head grün sein. Erfordert der belegte Fix weiteren Umfang, erneut Owner-Entscheidung einholen."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-runtime-image-registry-artifact-unknown · Light-runtime blob/manifest unknown root cause is not a scripts publish gap, it is .github workflow ordering plus a dangling acceptance.sh reference (owner decision) #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Blocker:** Owner-Entscheidung 2026-11-22: Freigabe für eine Ursachenprüfung und genau einen PR mit der eng begrenzten Reparatur, soweit durch Befund belegt: Reihenfolge und Registry-Verfügbarkeit in .github/workflows/pre-release-runtime-suite.yml; de…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Finding (0847d100 audit, develop 3cbb2bac  713aadd4)

`scripts/ci-local-oci-registry.sh` publish path is CORRECT (local docker+podman test: it tags, pushes blob+manifest, and oras resolves the sha256 digest; it only fails on the local-only unbound GITHUB_ENV/GITHUB_STEP_SUMMARY vars). So no scripts fix is warranted.

The 'blob/manifest unknown' seen by the light-runtime cells comes from causes outside `scripts/**`:
1. `.github/workflows/pre-release-runtime-suite.yml:198-201`  the publish-before-ORAS-resolve ordering must be verified.
2. per-job runner registry sharing (the local registry may not be shared across runner jobs).
3. `scripts/acceptance.sh` is MISSING from the tree (`git cat-file` 404, `gh contents` 404) yet is referenced in `.github/workflows/pre-release-runtime-suite.yml:306`, `pre-release.yml:1080`, `targeted-demo-acceptance.yml:345`, and registered as a core in `scripts/pre-release-runtime-impact.json:104`.

This is an Owner `.github` + missing-file decision; a lane must not fabricate a scripts workaround.

Die Freigabe ist auf den belegten Pre-Release-Fix begrenzt. ci.yml und der normale CI-Pfad bleiben unverändert.
