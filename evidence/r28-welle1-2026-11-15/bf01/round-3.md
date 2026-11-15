# BF-01 fix round 3 — CI gruen auf exaktem Kandidatenkopf

- Mission: `/tmp/opencode/mission-bf01-fix2.md` (Karte `t-20261115-bughunt-d28-state-dir-target` = 0427-189)
- Rolle: FIX-LANE (Fortsetzung von round-1/round-2, derselbe Claim `lane-0428-fix-bf01` (flash))
- Coordinator-Inbox: `594fd2f5-4e80-43b6-9841-92879146a85e`
- Produktzweig: `lane-0428-fix-bf01-v2` == `lane-0428-fix-bf01` == DRAFT PR https://github.com/mcpdev80/baseharbor/pull/1585 (Kopf `7bdeaa08499f4b3d8113d537a48e36d4f9881bf0`)
- Base: develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/.models/flash/bf01-base-wt`
- Stand: 2026-11-15 ~08:00 CET

## Warum Runde 3

- Der in round-2 gemeldete grüne Run 43684179345 galt dem Kopf `8041a9f01`. Der Coordinator-Korrektauftrag verlangte den terminal grünen Nachweis auf dem aktuellen Kopf; die Review-Lane (#1584, closed-not-merged) hatte zusaetzlich die Test-Konstruktion als unecht gerügt.
- Der Zwischenzustand mit zwei Ketten (#1584/#1585/#1586, branch lane-0428-fix-bf01 vs -v2) ist konsolidiert: #1584 war ohne Merge geschlossen, #1586 (nur der Test-Fixup) wurde nach dem Push auf die bestehende Kette geschlossen. Massgeblich ist ausschliesslich #1585.

## Aenderung dieser Runde (test only)

Commit `7bdeaa084 test(cli): mirror real organization-state placement in the BF-01 regression`:

- Der Helfer `writeTestOrganizationSelection` schrieb das Organisationen-Objekt bisher mit der Phantasie-Quelle `/srv/organization`; der Loader konnte damit Root-zugehoerig und Fremd-Zustand nicht unterscheiden (Round-2-Befund). Er spiegelt jetzt, was `baha config organization set --source local` tatsaechlich pro Installation notiert (Quelle unter dem jeweiligen Root bzw. im Ambiente-Pfad).
- Die Aufloesungs-Assertion in Teil 2 akzeptiert kein stilles Auflösen mehr: unter einer frischen Root B mit fremdem Ambiente-Org-Default `alpha` muss der Resolver fehlerhaft oder root-lokal antworten, nie `alpha` (fail-closed ueber die Registrierungs-Grenze in `effectiveTarget`).
- Kein Produktcode geändert gegenueber `8041a9f01`; Schreibpfad/Tombstone bleiben Folge-Karte.

## Roter Zustand des Tests (ehrliche Einordnung)

- Auf base `0e9ccb582` mit dem base-Testblob: GRUEN (zwei Worktrees; Bestaetigung von round-2 bleibt).
- Auf base `0e9ccb582` mit dem TESTblob aus `7bdeaa084` (Produktcode zurueckgesetzt): FAELLT ER ROT — die Teil-2-Assertion durchlaeuft auf base die Fremd-Registrierungsloesung nicht. Der Fixup macht den Regressionstest erstmals mechanismus-kritisch.

## Required checks / run

- Lokal: `go build ./...`, `go vet`, `gofmt -l` sauber; `scripts/source-readability-audit.sh` PASS; Familien `TestAccess*`, `TestGuidedInit*`, `TestPersistActiveSameKeyCollisionGuard`, `TestStateDirIsolatesTargetSelection`, `TestTarget*`, `TestUseTarget*`, `TestPersisted*` PASS; `./internal/orgconfig`, `./internal/deployment` PASS.
- Voll `go test ./cmd/baha -count=1` auf diesem Rechner: drei Ausreisser (`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, `TestSharedBackendReconcileRejectsSecondProcess`, `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication`) — auf exakt base `0e9ccb582` auf demselben Rechner identisch failing; hostgebundene Defizite dieser Maschine (fehlende Core-Netzwerke/Images, Shared-Owner-Lock-Umgebung, 60s-git-archive-KILL), keine Kandidaten-Regressionen. In der CI-Zelle laufen sie gruen (Run unten).
- Gehosteter Kandidatenlauf: `CI · PR #1585`, Run `43685670514`, head SHA `7bdeaa08499f4b3d8113d537a48e36d4f9881bf0` — terminal: completed/success, keine fehlgeschlagenen Jobs (beobachtet per `gh run watch --exit-status`, Exit 0). Der Parallel-Lauf der geschlossenen Duplikat-Kette, `CI · PR #1586` Run `43685517913` (derselbe SHA), endete ebenfalls success.
- CI-Abdeckung des neuen Tests: `cmd/baha`-Pakettests in den `Draft Go · cli-*`-Shards (`go test ./cmd/baha -count=1`), ausgelöst durch PR-push auf dem Kandidatenkopf.

## Remote witnesses (literal)

`git ls-remote lane-origin refs/heads/lane-0428-fix-bf01 refs/heads/lane-0428-fix-bf01-v2 refs/heads/develop`:

```
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/heads/lane-0428-fix-bf01
7bdeaa08499f4b3d8113d537a48e36d4f9881bf0	refs/heads/lane-0428-fix-bf01-v2
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
```

Eigene Commits ueber base (`git log --oneline 0e9ccb582..7bdeaa084`):

```
7bdeaa084 test(cli): mirror real organization-state placement in the BF-01 regression
8041a9f01 fix(cli): keep foreign organization defaults out of isolated state roots
f048627c1 fix(cli): state-root override owns target selection state
18c922e37 test(cli): add BF-01 state-dir target-selection isolation regression
```

## repo-rule compliance

- Eine Kette, ein Kandidat: #1585 auf `lane-0428-fix-bf01-v2`; Zwilling Branch `lane-0428-fix-bf01` zeigt auf denselben SHA; #1586 geschlossen (Duplikat dieser Kette), #1584 ohne Merge geschlossen (Runde-1-Zustand).
- Merge-frost: DRAFT, kein Merge, develop unveraendert (`0e9ccb582` Witness oben).
- Keine `.github/**`-Aenderungen; nur PR-push.
- Keine Container/Netzwerke/Volumes von dieser Lane gestartet; Sauberkeit: nur /tmp-Fixtures (`hunt-bf01-v2`, `hunt-bf01-leak*`, `baha-bf01-*`), alle im Scratch-Zonen-Pfad dieser Lane.
- Secrets: keine gelesen oder geloggt.
- Hinweis PR-Bearbeitung: das Re-pointen von `lane-0428-fix-bf01-v2` erfolgte per Fast-forward-Push (8041a9f01..7bdeaa084); die Historie von #1585 bleibt linear, kein Force auf der PR-Kette selbst.

## END

END_DONE: Kandidat `7bdeaa08499f4b3d8113d537a48e36d4f9881bf0`, DRAFT PR #1585 (base develop, merge-frost gehalten), CI-Run `43685670514` terminal success auf exakt diesem Kopf, Akte publiziert. ls-tree-Zeuge:

```
git ls-tree -r origin/main -- evidence/r28-welle1-2026-11-15/bf01/round-3.md
100644 blob 8494fa6e74ba0b11e2f13dbfc51bbdd7cad545d8	evidence/r28-welle1-2026-11-15/bf01/round-3.md
```
