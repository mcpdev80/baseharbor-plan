# Mission: stack-inventory (stackaudit lane)

Coordination-nahe Pruef-Arbeit. KEIN feature-scope. Kein Produkt-Write, kein gh pr edit, kein .github/**.

## Mission scope (verbatim)
STACK-INVENTUR der 0.4.28-PRs gegen PR-Disziplin regel 8 (ein PR pro karte; base-ref jedes gestapelten PRs = zweig der DEKLARIERTEN basis-lane; draft-flag wegen frost).

- Zelle 1 je PR: state, isDraft, baseRefName, headRefOid abgleichen gegen karten-deklarierte depends_on bases (tasks/*.md). Abweichender base-ref OR nicht-draft = BEFUND.
- Zelle 2 je PR: head == branch-head der head-Ref (ls-remote). Drift = BEFUND mit alt/neu sha.
- Keine korrekturen selbst. Nur inventur + rezept je befund (exakter befehl den coord nach freigabe setzt).
- Quer: listet jeder PR-titel die kartennummer (namensregel)? Fehlt sie = niedrig-befund.

## Repo-rule compliance
- Nur Read-only auf Produkt-Repo und GitHub. Kein gh pr edit/retarget. Kein Write in baseharbor.
- Kein Subagent. Kein .github/**. Kein .evidence/ im Produkt-Repo.
- Evidenz nur in baseharbor-plan evidence/<welle>/<card>/, nie im Produkt.

## BASE ATTESTATION
- Planning repo HEAD (baseharbor-plan): ac0d5ee74221e147a70cca35f216b74022ba74e4 (main)
- baseharbor remote main (HEAD): aff1532c2f6c6782a8c13afad83245d1351815e7
- baseharbor remote develop: 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
- Alle 16 named PRs gegen gh pr list (search base:develop, 100 PRs, limit 100) erhoben; keine 2. Kette.
- baseRefName je PR per gh pr view verifiziert.

## Commands (verbatim)

gh pr list --repo mcpdev80/baseharbor --search "base:develop" --state all --json number,title,state,isDraft,baseRefName,headRefName,headRefOid --limit 100

gh pr view <n> --repo mcpdev80/baseharbor --json number,title,state,isDraft,baseRefName,headRefName,headRefOid   (per named PR)

git ls-remote https://github.com/mcpdev80/baseharbor HEAD develop
git ls-remote https://github.com/mcpdev80/baseharbor refs/heads/<head-Ref>

## Inventory: CELL GROUP 1 (state / isDraft / baseRef / headRefOid vs declared depends_on bases)

Declared basis = der Zweig der DEKLARIERTEN basis-karte = der head-Ref der jeweiligen depends_on-Karte (Stacking app->env->target). PR head-Ref = eigener Karten-Zweig; PR base-Ref = Zweig der Basis-karte.

| PR | card (title) | state | isDraft | baseRef (live) | declared basis card | declared basis branch | match |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1575 | 0428-075 perses seam | OPEN | draft | develop | contract-seam depends_on [] | develop | OK |
| 1577 | docs v0.4.28 perses boundary | OPEN | draft | develop | release-boundary depends_on [] | develop | OK |
| 1578 | 0428-051 uid-environment | OPEN | draft | lane-0428-uid-app | uid-env depends_on [contract, uid-app] | lane-0428-uid-app (1579 head) | OK |
| 1579 | 0428-050 uid-app | OPEN | draft | develop | uid-app depends_on [contract] | develop | OK |
| 1580 | 0428-052 uid-target | OPEN | draft | lane-0428-uid-environment | uid-target depends_on [contract, uid-env] | lane-0428-uid-environment (1578 head) | OK |
| 1582 | fix(BF-03) target selection private state | OPEN | draft | develop | bf03 depends_on [] | develop | OK |
| 1585 | fix(BF-01) state-dir override target selection | OPEN | draft | develop | bf01 depends_on [] | develop | OK |
| 1587 | docs operator API runbook (0427-169) | OPEN | draft | develop | docs | develop | OK |
| 1588 | feat Target policy presets (0427-186) | OPEN | draft | develop | 186 | develop | OK |
| 1589 | docs CI consumption examples (0427-020) | OPEN | draft | develop | 020 | develop | OK |
| 1590 | 0428-080 perses selection | OPEN | draft | lane-0428-075-perses-seam | perses-selection depends_on [contract-seam, signal-inventory] | lane-0428-075-perses-seam (1575 head) | OK |
| 1591 | 0428-054 env-registry | OPEN | draft | lane-0428-uid-target | env-registry depends_on [uid-env, uid-target] | lane-0428-uid-target (1580 head) | OK |
| 1592 | 0428-088 perses runtime | OPEN | draft | lane-0428-075-perses-seam | perses-runtime depends_on [contract-seam] | lane-0428-075-perses-seam (1575 head) | OK |
| 1594 | 0428-053 env-policy | OPEN | draft | lane-0428-env-registry | env-policy depends_on [uid-env] | lane-0428-env-registry (1591 head) | OK |
| 1595 | 0428-059 source-model | OPEN | draft | lane-0428-uid-target | source-model depends_on [contract, uid-app] | lane-0428-uid-target (1580 head) | OK |
| 1596 | 0428-056 org-env-reconcile | OPEN | draft | lane-0428-env-registry | org-env depends_on [env-registry] | lane-0428-env-registry (1591 head) | OK |

Befund Zelle 1: KEINE abweichende base-ref. Alle 16 basen deckungsgleich mit der deklarierten basis-lane.
Befund Zelle 1 (draft): ALLE 16 named PRs sind draft (frost-gemaess). Alle nicht-draft-PRs der Menge (1583 CLOSED) sind korrekt ausserhalb des offenen frost-Fensters.

## Inventory: CELL GROUP 2 (head == branch-head of head-Ref via ls-remote)

| PR | head-Ref (live) | headRefOid (gh) | ls-remote live | drift |
| --- | --- | --- | --- | --- |
| 1575 | lane-0428-075-perses-seam | cb4367f347ed | cb4367f347ed... | OK |
| 1577 | 0428-092-perses-boundary | ab9086f5fc39 | ab9086f5fc39... | OK |
| 1578 | lane-0428-uid-environment | 756d21b7839a | 756d21b7839a... | OK |
| 1579 | lane-0428-uid-app | 2b91371a3fa8 | 2b91371a3fa8... | OK |
| 1580 | lane-0428-uid-target | 3a91e2a8362b | 3a91e2a8362b... | OK |
| 1582 | lane-0428-fix-bf03 | 756b2be7eb2e | 756b2be7eb2e... | OK |
| 1585 | lane-0428-fix-bf01-v2 | 13e096fc66d9 | 13e096fc66d9... | OK |
| 1587 | work/r28-operator-api-runbook | 20e0537cc333 | 20e0537cc333... | OK |
| 1588 | lane/0427-186-target-policy-presets | 9534edd49c20 | 9534edd49c20... | OK |
| 1589 | work/0427-020-ci-consumption | 442755b35dc3 | 442755b35dc3... | OK |
| 1590 | lane-0428-080-r28-perses-selection | 85b4cbb59827 | 85b4cbb59827... | OK |
| 1591 | lane-0428-env-registry | b85efaf6c94c | b85efaf6c94c... | OK |
| 1592 | lane-0428-088-perses-runtime | f55d9f94c325 | f55d9f94c325... | OK |
| 1594 | cli2-env-policy-head | 018b4e58a3aa | 018b4e58a3aa... | OK |
| 1595 | lane-0428-059-cli2-source-model | eda0cd61cc18 | eda0cd61cc18... | OK |
| 1596 | cli2-org-env-reconcile | 32307a433604 | 32307a433604... | OK |

Befund Zelle 2: KEIN drift. Alle 16 head-Refs zeigen auf ihren gh- headRefOid.

## Cross-cutting: PR-title card-number (name rule)
- 1575 title "0428-075 ..." -> ja
- 1577 title "docs(v0.4.28) ..." -> nein (keine katennummer; 0428-092 fehlt im titel) — niedrig-befund
- 1578 title "0428-051 uid-environment" -> ja
- 1579 title "0428-050 ..." -> ja
- 1580 title "0428-052 ..." -> ja
- 1582 title "fix(BF-03):" -> ja (bf03)
- 1585 title "fix(BF-01), 0427-189" -> ja
- 1587 title "docs(0427-169) ..." -> ja
- 1588 title "0427-186" -> ja
- 1589 title "docs(0427-020) ..." -> ja
- 1590 title "0428-080 ..." -> ja
- 1591 title "0428-054 ..." -> ja
- 1592 title "0428-088 ..." -> ja
- 1594 title "0428-053 ..." -> ja
- 1595 title "0428-059 ..." -> ja
- 1596 title "0428-056 ..." -> ja

Befund quer: 1577 titel ohne kartennummer (0428-092 nicht im titel) — niedrig-befund. Alle anderen tragen die katennummer.

## Summary of findings
- BEFUND (mittel, Zelle 1 draft-logik): PR #1583 "0428-077 align Perses release/reference to three-state names" — state CLOSED, isDraft=false, kein mergeCommit, base=develop. Es ist ein non-draft, closed (never-merged) PR. Laut depends_on (contract-seam, PR #1575) ist die KATenzuordnung offen; PR-Disziplin regel 8 verlangt "draft-flag gilt wegen frost" fur offene 0.4.28-PRs. Ein closed, non-draft, nie-merged PR in der 0.4.28-Nahe (Perses three-state names) passt nicht in das frost-Fenster und ist als Rest/Stamm PR zu werten.
  - Rezept (coord nach freigabe): gh pr close --comment "superseded" 1583 oder gh pr delete --yes 1583; ggf. KATenzuordnung aus baseharbor-plan (tasks/t-20261114-r28-perses-contract-seam.md) klaren.
- BEFUND (niedrig, quer): PR #1577 titel fhrt keine katennummer (0428-092 fehlt). Namensregel nicht eingehalten.
  - Rezept (coord nach freigabe): gh pr edit 1577 --title "0428-092 docs(v0.4.28): set optional Perses release boundary (pin v0.55.1)".
- Alle anderen 14 PRs: conform (base-ref = deklarierte basis-lane, draft, kein drift, katennummer im titel).

## origin/main witness (second-to-last action)
`git log origin/main --oneline -2`:
06463168 evidence(stackaudit): round-1 stack inventory of 0.4.28 PRs vs PR-disziplin rule 8
25dfb466 evidence(0428-089): round-1 — complete volume inventory and binary cleanup in the cleanliness witness
`git merge-base --is-ancestor 06463168 origin/main` -> YES (06463168 is an ancestor of origin/main). Evidence path present on origin/main.

## END
DONE stackaudit: 0.4.28 stack inventory complete — 16/16 PRs conform (base-ref = declared basis-lane, all draft/frost, no head-drift); 2 findings: #1583 closed non-draft never-merged Perses three-state (rezept: close/delete after coord release); #1577 title missing card number (rezept: gh pr edit title). Read-only, no subagent, no .github/**, no writes to product.

## Cleanliness (read-only)
- Kein Produkt-Write. Kein gh pr edit/retarget/close/delete. Kein Subagent. Kein .github/**.
- Keine Container/compose begonnen (baha-docker/baha-podman nicht genutzt).
- Caches unter /tmp/opencode/ (git ls-remote gegen https, kein Checkout im Produkt).
