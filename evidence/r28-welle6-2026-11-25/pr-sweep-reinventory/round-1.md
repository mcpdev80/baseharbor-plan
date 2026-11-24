# PR-sweep re-inventory round 1 (read-only)

- Shift: w102-0428-216-prsweep2
- Card: inventory/prep only — no rebase / push / merge / CI-trigger / draft change on any PR
- Date: 2026-11-24
- Author: ornith worker, own session, no subagents (§4.8)
- Scope: refresh the open-PR inventory against the NEW develop so the serial-chain requalification + #1826/#1828 disposition is decided on current facts

## Reality witnesses

- baseharbor-plan remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (git remote -v)
- develop head (ls-remote): `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `f14fb87c8f5afd91168e4f174d620c9f00e6341e refs/heads/develop`
- baseharbor-plan main head (ls-remote): `87cd60666b0c5e2f74312c50af1c32fd7ea99b74`
- Fresh clone used for all merge-base / diff math: `git clone --no-checkout https://github.com/mcpdev80/baseharbor.git` at /tmp; origin/develop fetched to f14fb87c8

## Base attestation (develop f14fb87c8 = expected after #1823/#1824/#1825/#1821)

- develop log confirms the sweep: f14fb87c (#1823), 46d3dccc (#1825), 2b9a2c6d (#1824), 05ef4853 (#1821)
- Each PR head's shared base with develop is a develop commit (on origin/develop); no head was cut from a PR head. §3.8 single-candidate provenance holds.

## Open PR inventory (against origin/develop f14fb87c8)

| PR | head branch | head SHA | base | behind dev | ahead dev | draft | reviewDecision | latest Hosted run | run head_sha | run status | qualifying? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #1812 | lane-0428-249-runtime-image-fix | 47590207518ce9501f1b1bbb115d72d64a206d14 | develop | 1 | 1 | no | none | 45397265257 | 47590207 | success (PR Selected Checks pass) | YES (exact head) |
| #1819 | w54-0428-181-export | 17381017be986f0eccb25662ad742ad759296346 | develop | 3 | 2 | no | none | 45380314808 | 17381017 | cancelled (PR Selected Checks) | NO — terminal run cancelled, not a pass |
| #1820 | fix/broker-build-identity | 28803d11027197e7734fb3ec94bef9b34e224b0d | develop | 3 | 4 | no | none | 45382404741 | 28803d11 | cancelled; Selected Runtime docker data-capabilities FAIL 8m33s | NO — non-qualifying: fail + cancelled |
| #1818 | lane-0428-078-cf-fix | 20fc1cb7d49602dc7f8aa0004a7562a81311d78c | develop | 5 | 4 | no | none | 45316544436 | 20fc1cb7 | success | YES (exact head) — but head 20fc1cb7 is contaminated (see below) |
| #1826 | lane-0428-279-mcpcontract | 6589a37b00273913e9e14fd9832e93b72630f106 | develop | 1 | 2 | no | none | 45412208234 | 6589a37b | success (PR Selected Checks pass) | YES (exact head) |
| #1650 | lane-0428-078-perses-identity-on-resolver | 84943695be19300ef006a7986e1d110130943ce8 | develop | 10 | 18 | no | none | 45297432220 | 84943695 | success | YES (exact head) — owner-parked |

- Non-qualifying runs flagged: #1819 (run 45380314808 cancelled at PR Selected Checks), #1820 (run 45382404741 cancelled; docker data-capabilities job FAIL, log job/138405310739; also ran on a head that carries the #1820 regression but the run never completed — cannot be accepted evidence).
- #1812 and #1826 carry clean exact-head success on PR Selected Checks + full Go gate.

## Single-writer lane + eligibility NOW

- Serial chain #1812 -> #1819 -> #1818 (task dependency order, per r28 signal one write path / perses-078 lineage):
  - #1812 lane-0428-249-runtime-image-fix — eligible NOW. Clean exact-head success; write-set = ONLY .github/workflows/pre-release-runtime-suite.yml. Immediately actionable.
  - #1819 w54-0428-181-export — BLOCKED for acceptance: latest run cancelled (no qualifying pass). Needs a rerun on exact head 17381017 by its writer (w54-0428-181-export lane). Chain position: ahead of #1818, behind #1812's successor only if #1812 must land first.
  - #1818 lane-0428-078-cf-fix — BLOCKED on contamination: head 20fc1cb7 carries FORBIDDEN keycloak-identity catalog hits (cross-lane force-push by another session, per w55 note in t-20261114-r28-perses-dashboard-identity). Correct head is the clean 0f20a3b9 (0 catalog hits). Cannot accept 20fc1cb7; needs fresh-cut from 0f20a3b9 + rerun. Chain position: last in serial chain.
  - #1826 lane-0428-279-mcpcontract — independent. Eligible NOW (clean exact-head success). Not part of the serial chain; disposition #1826/#1828 separate.
  - #1650 lane-0428-078-perses-identity-on-resolver — independent, owner-parked DIRTY per owner. Clean exact-head success; not actionable without owner resume.

## Rebase-guard vs #1823 secret_* change + fresh-cut flags

- #1823 = f14fb87c (new develop head): `fix(0428-277): fail-closed AuthorizationResult for failed reveal`, touches cmd/baha/secret_audit_test.go + cmd/baha/secret_operations.go.
- Every PR head carries the older secret_audit_test.go / secret_operations.go from its pre-#1823 base. A rebase of any head onto current develop f14fb87c crosses the #1823 secret_* edit:
  - #1812 (base 46d3dccc, #1825): rebase onto develop crosses #1821, #1823 (and #1825) — rebase-guard needed; #1812 only touches .github yaml so secret-file conflict is unlikely but must be checked.
  - #1819 (base 05ef4853, #1821): rebase crosses #1823 secret_* edit — guard needed.
  - #1820 (base 05ef4853, #1821): rebase crosses #1823 — guard needed; also 28803d11 head needs fresh-cut from clean base regardless (cancelled/non-qualifying run).
  - #1818 (base 3ebfb90, #1815): rebase crosses #1823; plus contamination requires fresh-cut from 0f20a3b9, not a plain rebase.
  - #1826 (base 46d3dccc): rebase crosses #1825 + #1823; write-set is docs/releases/v0.4.28.demo-ref only, low conflict risk.
  - #1650 (base d4fa8c58, #1813): rebase crosses #1823; owner-parked, not actionable now.
- Fresh-cut / reset needed (contaminated or stale heads):
  - #1820 head 28803d11 — stale + non-qualifying run; fresh-cut from a clean base + rerun (cross-ref w89/w88/w99).
  - #1818 head 20fc1cb7 — contaminated with foreign keycloak-identity catalog hits; fresh-cut from clean 0f20a3b9, not rebase (per w55; cross-lane force-push must stop).

## Chain disposition summary

- Immediately actionable (clean exact-head pass, no contamination): #1812, #1826.
- Blocked — needs rerun on current exact head: #1819 (run cancelled).
- Blocked — needs fresh-cut + rerun: #1818 (contaminated 20fc1cb7), #1820 (stale 28803d11 + cancelled/fail run).
- Owner-parked, not actionable: #1650.
- Serial chain readiness gate is #1812 (clean) -> #1819 (rerun required) -> #1818 (fresh-cut required). #1826 and #1650 are independent.

## Evidence provenance

- Evidence file path: evidence/r28-welle6-2026-11-25/pr-sweep-reinventory/round-1.md (baseharbor-plan only; never in a product repo)
- No .github/** edited, no workflow_dispatch / rerun, no PR push / merge / draft change, no rebase, no subagents. This was read-only measurement + reporting.

## END

- Lane: w102-0428-216-prsweep2 — DONE (read-only re-inventory delivered).
