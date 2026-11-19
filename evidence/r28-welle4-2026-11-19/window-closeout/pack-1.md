# v0.4.28 merge-window closeout heft — pack-1

Mission tag: `window-closeout-pack`. Lane: window-closeout-pack (this session, codeman 59c94cab).
Shift: r28-welle4-2026-11-19. Revision label of this heft: **pack-1 r5 (2026-11-19)** (r2: 121-head-drift; r3/r4: END-zeugblock; r5: terminaler lauf 44485086467 eingemessen).
Every remote fact below was measured live at pack time via `git ls-remote` and `gh api`
(remotes of `mcpdev80/baseharbor`, `mcpdev80/baseharbor-demo`, `mcpdev80/baseharbor-plan`).
Nothing is from memory. This file changes nothing: cards, PRs and runs are read-only here.

## PLAN

1. Read mission; create the numbered plan in all three places — done. Native `todowrite` is not
   exposed by this session's tool surface (checked: the Code Mode tool catalog lists only
   opencode/browser/context7; per mission instruction no tool-hunt via execute) — recorded as
   finding F-5. The plan is carried by (a) the board file
   `workers/todos/mission-window-closeout-pack.md.json` and (b) this PLAN list.
2. Zone + provenance verification: planning repo is
   `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (see witness §0); the quarantined
   `workers/baseharbor` checkout was never cited — done.
3. Board status per card from `tasks/*.md` frontmatter (`kanban_status`) — done.
4. PR number + exact head SHA per card via `gh api pulls/{n}` cross-checked with
   `git ls-remote` of the lane branch — done.
5. Terminal run id + conclusion per exact head via `commits/{sha}/check-runs` — done.
6. Acceptance verdicts with comment/review ids via `issues/{n}/comments` and `pulls/{n}/reviews` — done.
7. Develop first-parent chain of the window with one-word annotations — done.
8. Open lines with why-not-merged causes (file:line or run id) — done.
9. Blob cross-references (§4) and revision labels per output (§5) — done.
10. Commit + push to origin/main, `ls-remote` witness, END post — last actions (see END block).

## 0. Witnesses (zones, remotes, window begin)

- Planning repo zone (wrong-zone rule): the real planning repo is
  `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `git remote -v` there shows
  `https://github.com/mcpdev80/baseharbor-plan.git`.
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main`
  returned at pack start `7a8245f5efb05f00946f9b1627d8a08c358c3bd9` and moved during the shift
  (parallel lanes): final origin/main witness is in the END block.
  `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan` is directory space inside the
  workers bookkeeping repo and was not used.
- Product remotes (measured):
  - `git -C baseharbor ls-remote origin refs/heads/develop` → `da76c5cf9c963207038d5599bd130b89ecb1e8a4`
  - `git -C baseharbor ls-remote origin refs/heads/main` → `c000c5db2560c471fe84842136e03d6e54d96779`
  - `git ls-remote origin refs/heads/main` (baseharbor-demo) → `adda7599cb5b79689702f6a63a5ca802179df967`
- Window-begin definition used in §2, and its evidence gap: the board rule
  ("Kein 0.4.28-Merge vor dem 0.4.27-Tag; den begin-Marker publiziert die erste gemergte Karte",
  coordinator AGENTS.md §3.3 item 8) has no published marker commit in baseharbor. The 0.4.27
  lineage ends at `main` `c000c5db2` (2026-11-17 01:57 +0100, "#1675"), which is NOT an ancestor
  of develop; develop diverged at merge-base `462d800b1`-era ancestry with 2053 commits in
  `main..develop`. This heft therefore draws the window chain in §2 over
  `git log --first-parent origin/develop` back to `907f16713` — the last develop merge before the
  0.4.28 window's first in-window merge (`aadee4520`, #1680, 2026-11-18 21:39Z). The published
  begin marker itself is an open item (finding F-1).

## 1. Karten-Tabelle des Fensters

Legende Spalten: Status = `kanban_status` aus der Karte (baseharbor-plan main). Head = EXAKTER
PR-head-SHA, gemessen per `gh api pulls/{n}` UND deckungsgleich mit `git ls-remote` der lane-Ref
(bei gemergten Karten = SHA des `head`-Feldes nach merge, lane-Ref ist dann gelöscht). Lauf =
terminaler `CI · Source & Quality`-Run auf exakt diesem Head (`commits/{sha}/check-runs` →
`PR Selected Checks`). Urteil = letztes CODEX-REVIEW/CODEX-MERGE-Protokoll mit comment/review-id.
Merge = merge-commit-SHA auf develop (gh `merge_commit_sha`, ancestry gegen `origin/develop` geprüft).

| karte | status | PR | head (exakt) | terminal-lauf → schluss | abnahme-urteil (id) | merge-sha |
| --- | --- | --- | --- | --- | --- | --- |
| 0428-088 | blocked | baseharbor#1592 | `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9` | 44467712113 → SUCCESS | runtime witness ACCEPT, Karte NOT ACCEPTED — issue-comment 7000435611 (c452f705c), recheck 7001328277 (76331c7d8); formale reviews: keine (`pulls/1592/reviews` = []) | — (offen, mstate=behind) |
| 0428-093 | closed | baseharbor#1663 | `d0351baf5def60d7ceaa40008d8553c809503310` | 44407750981 → SUCCESS | CODEX-REVIEW ACCEPT — comment 6995280942 (00:00:23Z, 7s vor merge); review-record 5936683530 steht auf altem head b6055fd47 | `9a37b4bc6ba372af517ea00b8d93c2085a2d4f95` (merged 2026-11-19T00:00:30Z) |
| 0428-099 | closed | baseharbor-demo#164 | `86afbbebb7574b5c4bc1caeb098a4406e1e4a9e3` | 43963399114 (workflow_dispatch `Demo · PR guided consent regressions`) → SUCCESS | CODEX-REVIEW exact-head verdict — comment 6995261700 | `5d1cf312e18d06915db35c340bebe4e3d4f39d45` (merged 2026-11-18T23:59:37Z, base develop) |
| 0428-102 | closed | baseharbor#1677 (+#1679) | `dd62b9d30d96ee988e6f914fe86c4d15bf762512` | 44427948182 → SUCCESS | CODEX-MERGE owner-authorized ACCEPT — comment 6995803623 | `97a840e54dd037949cea3e6ae2614621f637eefb` (merged 2026-11-19T00:28:55Z); #1679 earlier: `0ec4706b12c8fa869a2c23db18b6cab4f91f2178` |
| 0428-114 | active | — (owner-scope, keine PR) | — (Owner-Ausfuehrung .github/scripts) | — | — ; owner-Feld: "Owner-Ausfuehrung (.github/scripts); umfang erweitert 2026-11-19" | — |
| 0428-115 | closed | baseharbor#1685 | `50f87cfb8dd6e87913044f96cc0204af1423b61c` | 44460025899 → SUCCESS | ACCEPT dokumentiert in akte 1685-final.md; GitHub-seitig KEIN ACCEPT-Protokoll auf diesem head — letztes protokolliertes Urteil ist REQUEST CHANGES comment 6999847636 (bb685c2dc); reviews-API: [] (finding F-3) | `deeeb64778b3f6109d3a8e49fd652d490901e89c` (merged 2026-11-19T04:53:04Z) |
| 0428-116 | closed | baseharbor#1686 | `96ac1b2e7fa3f2af2a4767a24d980def0e32eeb3` | 44438849188 → SUCCESS | letztes GitHub-protokoll: REQUEST_CHANGES-follow-up comment 6997019930 / review-record 5968175843 (01:39Z) auf dem später gemergten head; board resolution=accepted — finding F-2 | `40b9901398a6bae5b92ee45494ef3b70f192a2a7` (merged 2026-11-19T01:55:06Z) |
| 0428-117 | closed | baseharbor#1687 | `a1f4dc76f6f67b5f17048bc164df169d4380a9c5` | 44441702644 → SUCCESS | CODEX-REVIEW ACCEPT — review-record 5968382711 (COMMENTED 02:21:45Z, head a1f4dc76f) + merge-record-akte 1687-r4.md | `ec592fd3852328439ae9de8763c816ae9dd88dcc` (merged 2026-11-19T02:21:50Z) |
| 0428-118 | closed | baseharbor#1689 | `2d8cef5ef091c10e2d2919695626a1504b335f05` | 44432398707 → SUCCESS | CODEX-REVIEW ACCEPT — review-record 5967738924 (01:02:12Z) | `de53246585560ddf2c3e6ceae6d0f6eea6b71b68` (merged 2026-11-19T01:02:27Z) |
| 0428-119 | blocked | baseharbor#1690 | `84ee9a93e11fcf275214de38beecc6ef0b9e4e59` | 44464033443 → SUCCESS (unit/selected; runtime gates skipped) | letztes GitHub-Urteil REQUEST CHANGES comment 6998925617 (fbd756122) + gate-qualification comment 7000435938; reviews-API: [] | — (offen, mstate=behind) |
| 0428-120 | closed | baseharbor#1688 | `75f67a526527dd9314808b0f7852a9b59b718944` | 44436020492 → SUCCESS | CODEX-REVIEW ACCEPT — review-record 5967944141 (01:25:44Z) | `7d343836447f976ec613fa4ae1cb09afcabbbbe0` (merged 2026-11-19T01:25:49Z) |
| 0428-121 | active | baseharbor#1691 | `4f4b3d7a60…` (ls-remote lane-0428-efilter; `93da0ffd42…` zur tabellen-r1-zeit, danach korrektur-push) | letzter terminaler lauf auf gemessenem kopf 4f4b3d7a60: 44485086467 → **FAILURE** (`PR Selected Checks` completed:failure); davor 44478641206 FAILURE (`PR · Source format`: registry.go 849>800 zeilen; `PR · Go unit · packages`: FAIL TestManagedRuntimeObservabilityUsesCanonicalServiceIdentities) | REQUEST CHANGES comment 6999540526 (d9d70a984) + blocker comment 7002582916 (93da0ffd4); reviews-API: [] | — (offen, mergeStateStatus=BLOCKED) |
| 0428-122 | active | baseharbor#1692 | `876329f733c7706a5a8dfb9a4227fb2c2698660c` | 44473809584 → SUCCESS | REQUEST CHANGES comment 7002202503 auf dem aktuellen head (876329f73); reviews-API: [] | — (offen, mstate=clean, wartet auf 121-merge) |
| 0428-123 | wait | baseharbor#1693 | `d751c83bb047989d5bb4b11bcee1d091cf08d96a` | 44465014249 → SUCCESS | REQUEST CHANGES (integration readiness) comment 6999540769 auf b7fd05bee; kein Urteil auf d751c83bb; reviews-API: [] | — (offen, mstate=behind) |
| 0428-124 | review | baseharbor#1695 | `4f0d5e9f7036aed3d54b67e2f79096b43db9f29c` | 44478473607 → SUCCESS (auf diesem head) | REQUEST CHANGES comment 7002942896 (4f0d5e9f7; formal nicht einreichbar, im Protokoll vermerkt); vorganger fb9396cd2 rot in 44473414532 | — (offen, mstate=clean) |
| 0428-125 | closed | baseharbor#1694 | `e1742275e984aebd4e0cef027a999aed6a6b7f97` | 44465054273 → SUCCESS | CODEX-REVIEW ACCEPT — comment 7000435315 (content, 4fcb2b35d) + lifted ACCEPT comment 7000915172 (e1742275e); reviews-API: [] | `21161b101f66a47fb1a253ae17e87fe82567ba4d` (merged 2026-11-19T05:44:27Z) |
| 0428-126 | closed | baseharbor#1696 | `864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c` | 44471319498 → SUCCESS | CODEX-REVIEW ACCEPT — comment 7001786084 (06:37:14Z) | `da76c5cf9c963207038d5599bd130b89ecb1e8a4` (merged 2026-11-19T06:36:01Z) |
| 0428-128 | closed (superseded) | — (probe-only, PR-los) | — | probe-run refs 57ffc7c6 in akte probe-1.md | superseded an 0428-114 (karten-text "erweiterter umfang … gleiche korrekturklasse") | — |
| 0428-129 | closed | baseharbor-demo#165 | `bc4c6113be92599c962b2377b038173593483a18` | 44477622615 (`Guided consent · production-path regressions`) → SUCCESS | CODEX-REVIEW ACCEPT — comment 7002848486 (07:36:04Z) | `adda7599cb5b79689702f6a63a5ca802179df967` (merged 2026-11-19T07:34:17Z, base **main** — finding F-4) |
| 0428-130 | closed (accepted) | — (coord live-verify, PR-los) | — | — | befund-1.md live-verify der environment-kette auf develop `da76c5cf9` | — |
| 0428-131 | blocked (board) | baseharbor#1697 | `3448f73e697cd7fdb1a338ef8422b5d484bbe814` | 44478483899 → SUCCESS | REQUEST CHANGES comment 7002848508 (3448f73e6); reviews-API: [] | — (offen, mstate=clean) |

Remote-deckungszeug für jede offene lane (ls-remote == PR head): `lane-0428-088-perses-runtime`
= `76331c7d8…`, `lane-0428-119-consent-hard` = `84ee9a93e…`, `lane-0428-efilter` = `93da0ffd4…`,
`lane-0428-appclass-writer` = `876329f73…`, `lane-0428-123-regvisibility` = `d751c83bb…`,
`lane-0428-124-metrics-verification-none` = `4f0d5e9f7…`, `lane-0428-131-en-docs-warning-term` =
`3448f73e6…`, demo `lane-0428-demo-drive-matcher` = `bc4c6113b…`. Gemergte lanes sind remote
gelöscht (ls-remote leer, z. B. `lane-0428-115-twophase-doc`), ihr letzter PR-head steht in der
gh-api und ist in develop enthalten (§2). Randzeug: ein zweiter Ref `lane-0428-efilter-r2w` =
`9a4325028…` existiert auf origin (nicht-PR-zweig der 121-runde; kein PR darauf) — dokumentiert,
nicht bewertet.

## 2. Develop-Linie des Fensters (first-parent-Kette)

`git log --first-parent origin/develop --format='%h %s'` ab window-begin-Anker `907f16713`
(letzter develop-merge vor dem Fenster, §0) — je ein Wort, was herein kam. Revision: r1.

| # | merge-sha | Quelle | inhalt (ein Wort) |
| --- | --- | --- | --- |
| 1 | `aadee4520` | #1680 (0428-113-Linie) | phantom-logs |
| 2 | `8dccd4fe1` | #1683 (0428-106) | consent-labels |
| 3 | `9a37b4bc6` | #1663 (0428-093) | Warning-i18n |
| 4 | `97a840e54` | #1677 (0428-102) | signal-registry |
| 5 | `de5324658` | #1689 (0428-118) | diag-leak |
| 6 | `7d3438364` | #1688 (0428-120) | mcp-fail-loud |
| 7 | `40b990139` | #1686 (0428-116) | receipt-guard |
| 8 | `ec592fd38` | #1687 (0428-117) | selector-docs |
| 9 | `deeeb6477` | #1685 (0428-115) | enrollment-adr |
| 10 | `21161b101` | #1694 (0428-125) | target-env-key |
| 11 | `da76c5cf9` | #1696 (0428-126) | warning-marker |

Kopf der Kette = aktueller develop `da76c5cf9` (ls-remote). Parallel dazu, außerhalb der
develop-Kette: demo#164 → demo-develop `5d1cf312e`, demo#165 → demo-main `adda7599c` (§1, F-4).

## 3. Offene Linien — warum nicht gemergt

- **0428-088 / #1592 (blocked):** hosted-Abnahmedraht fehlt: `TestPersesRuntimeSmokeDockerIsolated`
  hat keinen CI-trigger und `BASEHARBOR_PERSES_RUNTIME_SMOKE` ist nirgends gesetzt; gate-map und
  `.github` sind owner-scope und an 0428-114 gebündelt. Grundzeug: blocker-Text in
  `tasks/t-20261114-r28-perses-runtime.md:20`; Laufzeuge: 44467712113 SUCCESS (PR checks) +
  host-witness auf `76331c7d8` in `evidence/r28-welle4-2026-11-19/perses-runtime/witness-1.md`;
  Urteil comment 7001328277: Karte abnahmefähig im Inhalt, aber NOT ACCEPTED without coverage
  disposition (`codex-welle3-review/1592-r3-runtime.md`).
- **0428-119 / #1690 (blocked):** der `docker-runtime`-job in
  `.github/workflows/docker-runtime-acceptance.yml` (zeilen 174-330) hat keinen ORAS-install-schritt;
  die einzigen install-zeilen 127-128 liegen im push-job. Grundzeug: blocker-Text in
  `tasks/t-20261118-ownership-stale-consent-hardening.md:13`; Laufzeuge: 44464060182
  (`Run runtime integration tests serially` FAIL, log-Zeile: "ORAS is required before Core setup"
  in `app_workload_integration_test.go:60`-artigen triage-Pfaden) und 44463342207
  (`Verify exact SHA input` FAIL, dispatch ohne SHA-input). Fixzustand: owner-scope unter
  0428-114 (`tasks/t-20261117-observability-native-gate-bootstrap.md:25` erweiterter umfang).
- **0428-114 (active, PR-los):** owner-Ausführung `.github/scripts`; zwei Drähte offen: ORAS-step
  im docker-runtime-job und gemappter trigger für die Perses-smoke-zelle (`scripts/pr-gate-coverage.json`).
- **0428-106 / #1683 (active auf dem board, PR aber gemergt):** der fensterinhalt sitz seit
  `8dccd4fe1` in develop (merge 2026-11-18T21:50Z, exakt-head 44404152726 SUCCESS) — kartenstatus
  und remote-wahrheit laufen auseinander; schließauftrag an den coordinator (kein merge nötig).
- **0428-121 / #1691 (active):** exact-head-CI ist auf dem aktuellen head ROT: run 44485086467
  (head `4f4b3d7a60`) FAILURE; der lauf davor 44478641206 (`93da0ffd42`) FAILURE —
  `PR · Source format` (`internal/observability/registry.go` 849 > 800 zeilen) und
  `PR · Go unit · packages` (`--- FAIL: TestManagedRuntimeObservabilityUsesCanonicalServiceIdentities`,
  package `internal/application`). Dazu inhaltlicher blocker comment 7002582916. Kein merge vor grün.
- **0428-122 / #1692 (active, seriell hinter 121):** beide schreiben
  `internal/providers/runtime/observability`-pfade; abnehmer-reihenfolge 121 → 122r3 steht im
  handoff-text von `tasks/t-20261119-hunt-metrics-env-filter-list-pfade.md` ("122r3 laeuft erst
  NACH deinem merge — beide schreiben runtime_observability.go") und owner-Feld von
  `tasks/t-20261119-hunt-metrics-appclass-log-writer.md` ("wartet auf sitz, nach 121-merge").
  CI auf eigenem head ist grün (44473809584), aber letztes Urteil ist REQUEST CHANGES
  (comment 7002202503) → korrekturnotwendig.
- **0428-123 / #1693 (wait, abhaengigkeit 123→#1691):** wait_reason in
  `tasks/t-20261119-hunt-metrics-registration-visibility-only.md:21`: "nicht vor #1691 mergen;
  hopf auf den develop-kopf nach #1691, dann re-review". Dazu REQUEST CHANGES comment 6999540769.
- **0428-124 / #1695 (review):** letztes Urteil REQUEST CHANGES (comment 7002942896 auf exakt
  `4f0d5e9f7`; korrektur returned-for-review comment 7002691676); der vorletzte head fb9396cd2
  war rot in 44473414532, aktueller head grün (44478473607) — wartet auf re-review eines
  vollständigen kandidaten. Rezeptakte: `codex-welle3-review/1695.md`.
- **0428-131 / #1697 (blocked):** letztes Urteil REQUEST CHANGES (comment 7002848508 auf exakt
  `3448f73e6`, CI grün 44478483899). Zusätzlich owner-scope-gate im blocker-text von
  `tasks/t-20261119-r28-en-docs-warning-term.md:13`: der `PR · Validation · documentation-audit`
  materialisiert nicht für die geänderten `docs/**`/`internal/*.json`-pfade.
- **gate-map-dach (0428-134, unter 0428-114):** der owner-scope-draht liegt als git-apply-fähiger
  patch in baseharbor-plan: `evidence/r28-welle4-2026-11-19/gate-map/gate-map-v2.patch` +
  begründung `patch-2.md` (4 änderungen: go-unit-on-PR, perses-smoke-zelle, demo-branches,
  documentation-audit-pfad). Die offenen linien 088 (smoke-trigger), 131 (documentation-audit) und
  F-4 (demo branches) haengen an diesem patch — owner-aktion, keine lane-aktion.
- **window-begin marker (offen, F-1):** kein publizierter begin-commit; `main` ist nicht Ahn von
  `develop` (`git merge-base --is-ancestor c000c5db2 origin/develop` → false; 2053 commits in
  `main..develop`). §2 nutzt den messbaren Anker `907f16713`.

## 4. Querverweise auf die Akten (blob-links, keine doppelte Beweislast)

- Reviews: `evidence/r28-welle4-2026-11-19/codex-welle3-review/` — [1592-r3-runtime.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1592-r3-runtime.md),
  [1685.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685.md), [1685-final.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1685-final.md),
  [1686-r4.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1686-r4.md), [1687-r4.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1687-r4.md),
  [1688.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1688.md), [1689.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1689.md),
  [1690-gate-qualification.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1690-gate-qualification.md), [1691.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1691.md),
  [1692.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1692.md), [1693.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1693.md),
  [1694.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1694.md), [1695.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1695.md),
  [1697.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1697.md), [129-demo-165.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/129-demo-165.md)
- Worker-Akten: [env-filter-fix/fix-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/env-filter-fix/fix-1.md),
  [appclass-writer/fix-2.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/appclass-writer/fix-2.md),
  [reg-visibility/fix-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/reg-visibility/fix-1.md),
  [verification-none/fix-2.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/verification-none/fix-2.md),
  [target-env-key/fix-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/target-env-key/fix-1.md),
  [dualmatch-docs/fix-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/dualmatch-docs/fix-1.md),
  [enrollment-twophase/fix-4.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/enrollment-twophase/fix-4.md),
  [app-env-recovery-flags/r4.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/app-env-recovery-flags/r4.md),
  [ownership-hardening/r2-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/ownership-hardening/r2-1.md),
  [perses-runtime/witness-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/perses-runtime/witness-1.md),
  [docker-gate-wiring/probe-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/docker-gate-wiring/probe-1.md),
  [demo-drive-matcher/fix-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/demo-drive-matcher/fix-1.md),
  [en-docs-warning-term/fix-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-1.md),
  [verify-env-chain/befund-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/verify-env-chain/befund-1.md),
  [hunt-metrics/befund-1.md](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md)
- Karten: `tasks/t-2026111[4-9]-*.md` (pfade in §1/§3; `plan.py show <id>` ist der zugriffsweg).

## 5. Revision-Labels

- pack-1.md r1 — dieses heft (inventar, kette, offene linien, querverweise), 2026-11-19.
- Karten-/PR-/laufzustände: stand der ls-remote/gh-messungen im §0-zeugnis-Fenster; jede spatere
  Aenderung an develop, PR oder board erfordert pack-1 r2 (label je ausgabe, keine stumme updates).

## 6. Befunde (read-only festgestellt, nichts geaendert)

- F-1: Kein publizierter window-begin-marker für v0.4.28; `main` ist kein Ahn von `develop`
  (gemessen: `git merge-base --is-ancestor c000c5db2 origin/develop` = false). §2 nutzt den
  messbaren Anker `907f16713` (#1681, letzter merge vor dem Fenster).
- F-2: #1686 wurde 01:55:06Z gemergt, obwohl das letzte GitHub-Protokoll (review record
  5968175843, 01:55:09Z auf dem gemergten head 96ac1b2e7) ein FOLLOW-UP REQUEST_CHANGES war
  (kommentar-only beanstandung an `internal/application/provider_change_result.go:51-52`).
  Board resolution=accepted widerspricht dem fernzeug — merge vor bereinigturteil.
- F-3: #1685 ACCEPT liegt nur als planning-akte vor (`1685-final.md`); die GitHub-reviews-API ist
  leer und der letzte PR-kommentar (6999847636) war REQUEST CHANGES — Protokoll-Lücke wie F-2,
  nur harmloser (der beanstandete head bb685c2dc war nicht der gemergte).
- F-4: demo#165 ist gegen `main` gemergt (base_ref=main, msha `adda7599c`), waehrend demo#164 gegen
  `develop` ging; demo-develop (`5d1cf312e`) traegt den 129-inhalt nicht. Eine der beiden basisregeln
  verliert.
- F-5: Diese Session exponiert kein natives `todowrite`-Werkzeug (geprüft: nur die Code-Mode-
  Bausteine opencode/browser/context7; keine tool-Hunt-Suche nach AGENTS-4.4-Ausnahme). Der Plan
  lebt in der board-JSON und diesem PLAN-list.
- F-6: develop-integration schreibt keine `CI · Source & Quality`-runs auf merge-commits (gemessen:
  `actions/runs?head_sha=<merge>&event=push` liefert nur die Docker/Podman-core-runs); das
  `Receipt · Commit`-protokoll laeuft als schedule gegen main und schrieb in diesem Fenster keine
  sichtbaren checks auf develop-merge-shas (letzte pull_request_target-runs alt, letzte schedule-runs
  gegen main `c000c5db2` SUCCESS: 44474309722, 44479138624).
- F-7: Randzeug #1: develop@`deeeb6477` hat einen FEHLERLAG auf einem release-zweig-dispatch: run
  44466684726 (`Runtime · Docker Core · release/v0.4.21`, head_branch=develop, attempt 1) FAIL im
  job `docker-runtime` — die letzten Logzeilen zeigen keinen Kandidatenfehler, sondern einen
  aufgerissenen Pfad `/home/runner/work/_temp/docker-runtime-checks/tests/main.json` im verifikationsschritt
  ("Verify all eight executed runtime tests"). Kein blockierender Befund gegen die 115-karte
  (der push-run auf demselben head, 44461341870, ist SUCCESS mit skipped docker-runtime), aber die
  dispatch-pfad-lücke in §3-klasse (ORAS/sha-input) bleibt damit dreifach belegt.

## END

END window-closeout-pack DONE — pack-1.md geliefert (r5, revision-labels §5); read-only,
keine karte/PR/lauf geaendert. Persistiert in baseharbor-plan main unter
`evidence/r28-welle4-2026-11-19/window-closeout/pack-1.md`.
Letztes ls-remote-zeug: `git -C .../baseharbor-plan ls-remote origin refs/heads/main`
→ `6c3add19da15da743ba9504c50b0b9e4486c318a refs/heads/main` (END_COMMIT, der diesen satz
selbst traegt; gemessen nach dem push). Kandidaten/akte auf origin/main
vor diesem END-post (ls-tree-zeug oben). Host besenrein: keine container/netzwerke/volumes von
dieser lane; ambient `bh-local-shared-*` bleiben unangetastet.

Zeuge (zweitletzte aktion, exakte ausgabe):
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main`
→ `d287a3573c563a0d05cd586b04239fb095bce1bb refs/heads/main` (dieser satz liegt im gleichnamigen commit d287a357, der ihn auf den wert nach sich selbst setzt — letzte zeile dieses blocks: END_COMMIT d287a357)
`git -C ... log --oneline -1` → `e4b782bb evidence(window-closeout-pack): pack-1 r5 —
121 terminal-run 44485086467 FAILURE eingemessen`.
Das pfad-zeugnis gegen origin/main: `git ls-tree -r --name-only origin/main | grep window-closeout`
→ `evidence/r28-welle4-2026-11-19/window-closeout/pack-1.md` (vor dem END-post auf origin/main).
Host-cleanliness: keine container/netzwerke/volumes/state angelegt (diese lane ist read-only,
ls-remote/gh api/git fetch nur); temporär nur `/var/tmp/*.json`, `/var/tmp/collect_*.py`;
eigene worktrees: keine; keine compose-projekte gestartet. Sauberkeitszeug: `docker ps -q` →
4 container, alle com.docker.compose.project=bh-local-shared (ambient-core, 2 tage alt,
nicht diese lane — bleiben unangetastet, owner-direktive 2026-11-08); `podman ps -q` → 0.
cleanliness: besenrein, kein runtime-eingriff durch diese lane.

## 7. Zeugenblock (Messprotokoll, read-only)

- Zonen: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main`
  → (start) `7a8245f5efb05f00946f9b1627d8a08c358c3bd9`, (push-zeug) siehe END-Block.
- Produktdistor: `git ls-remote origin refs/heads/develop` → `da76c5cf9c963207038d5599bd130b89ecb1e8a4`;
  `refs/heads/main` → `c000c5db2560c471fe84842136e03d6e54d96779`.
- Ahnzeug der gemergten kandidaten (je `git merge-base --is-ancestor <base> <head>` gegen den
  frisch geholten develop): #1685 base `ec592fd38` YES; #1686 base `7d3438364` YES; #1687 base
  `40b990139` YES; #1688 base `de5324658` YES; #1689 base `97a840e54` YES; #1694 base `deeeb6477`
  YES; #1696 base `21161b101` YES. Merge-shas sind identisch mit den first-parent-einträgen in §2
  und liegen auf `origin/develop` (nachgemessen: alle YES).
- Kartenstatusquelle: `tasks/*.md` frontmatter `kanban_status` (board-Dateien in §1/§3 mit
  datei:zeile für jeden blocker/wait_reason).
- Laufquelle: `gh api repos/<r>/commits/<head>/check-runs` → job `PR Selected Checks` bzw.
  (demo) `Guided consent · production-path regressions`; run-level `status:conclusion` nachgezogen
  (alle completed; die runs 44478641206 und 44485086467 = failure).
- Urteilsquelle: `gh api issues/<n>/comments` + `pulls/<n>/reviews` (ids in §1); akten mit
  gegenlesenen verweisen in §4.
