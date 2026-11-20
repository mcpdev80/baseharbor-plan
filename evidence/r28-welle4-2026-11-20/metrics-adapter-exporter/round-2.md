# 0428-182 — adapter without exporter (correction round 0428-182, PR #1716)

- Mission: `/var/tmp/mission-182.md` + Owner correction round (posted to this session 2026-11-20)
- Rolle: WORKER (0428-182, my session owns card w182-0428-182-metricsadapter)
- Datum: 2026-11-20
- Karte: `t-20261120-r28-metrics-adapter-without-exporter` (0428-182)
- My branch: `lane-0428-182-metrics-adapter`, my head: `7725cdc1` (from develop head `96f2ae11`)
- **STOP: parallel session w206 implemented the SAME card on the SAME branch.**

## Correction-round befund (von mir umgesetzt)

Owner korrigiert: `TestRequiresAdapterMetricsSourceWithoutProducerFailsCatalog` war ein **Pauschalverbot** — er machte ANY `RequiresAdapter`-metrik rot, AUCH mit producer. Akzeptanz 2 verlangt aber ROT nur bei `RequiresAdapter` + KEIN producer.

### Loesung (a) — CONDITIONAL guard, zwei Faelle
Der test prueft jetzt ZWEI faelle und beweist damit die BEDINGUNG, nicht das verbot:
- Branch A (GRUEN): `RequiresAdapter` metrics mit adapter realization (`Mode: ObservabilityAdapter`) validiert — producer vorhanden.
- Branch B (ROT): `RequiresAdapter` metrics ADAPTER REALISIERUNG AB (`Mode: ""`) — fail-closed.

Proveniitz (unabhaengig gemessen, Test `TestZZConditionalProof`, kurz ausgefuehrt):
- Branch A WITH producer: PASS (green) — korrekt.
- Branch B WITHOUT producer: FAIL (red) — korrekt.

Damit prueft der test die bedingung (producer vorhanden/abwesend), nicht die erklaerung allein. In der akte dokumentiert: die naechte abnahmepruefung setzt an der zwei-faell-struktur an.

### reference.go
Unveraendert seit round 1: postgres (Zeile 46) + valkey (Zeile 59) metrics von `RequiresAdapter` -> `Unsupported`, dokumentierter comment (goes-metrics-ohne-producer).

## CHANGE (correction round)
- `internal/capability/integration_contract_test.go`: `TestRequiresAdapterMetricsSourceWithoutProducerFailsCatalog` -> conditional (Branch A green / Branch B red), doc-updated.
- EIN letzter commit, head `7725cdc1` (amended von `1a67bd27`).

## Branch provenance (meine arbeit)
```
$ git merge-base --is-ancestor origin/develop HEAD
ANCESTOR=YES
$ git log --oneline origin/develop..HEAD
7725cdc1 fix(0428-182): declare postgres/valkey metrics unsupported, not adapter-required
$ git diff origin/develop...HEAD --name-only
internal/capability/integration_contract_test.go
internal/capability/reference.go
```

## STOP-GRUND (Report an Owner — keine weitere action ohne Weisung)
- Remote-branch `lane-0428-182-metrics-adapter` head ist `3a8f058b`, authored **"Worker w206"** — eine PARALLELE session, die denselben card 0428-182 independently implementiert hat (reference.go fix identisch, test name `TestPostgreSQLAndValkeyMetricsWithoutProducerFailCatalog` = das ursprüngliche Pauschalverbot, das die correction round verworfen hat).
- PR #1716 head ist seit `2026-11-20T13:53:48Z` w206's `3a8f058b` (meine arbeit wurde ueberholt/superseded).
- Regelkonflikt (§3.8: EIN integration-candidate per Kette; §4.3: fremde commits nicht uebernehmen; mission: fremde session-commits nicht auf eigenem branch). Ich trage w206's commit NICHT auf meinem branch und force-push NICHT.

## Was ich NICHT tue (bewusst, regelkonform)
- KEIN force-push auf w206's commit.
- KEIN zweiter branch / zweiter PR fuer dieselbe karte (§3.8, mission "EXACTLY ONE CANDIDATE PER CHAIN").
- KEIN ueberschreiben w206's diff.

## Optionen (fuer Owner-Entscheidung — hier keine eigenmaechtige entscheidung)
1. w206's PR #1716 (oder ein von ihm gefuehrtes) als den integration-candidate fuer 0428-182 akzeptieren; meine arbeit ruhen lassen.
2. meine `7725cdc1`-arbeit (conditional guard) in w206's PR integrieren — w206 als owner.
3. Owner entscheidet, welche version (meine conditional ODER w206's) in den merge geht; die andere wird nicht gemergt.

## CI-AUFNAHME (r1, meine version)
- Run `44746178682`, conclusion **success**, head `1a67bd27`, Job `PR · Go unit · packages`. (Nur r1; r2 correction-round wurde durch w206 superseded, daher kein neuer run von mir.)

## cleanliness
- Vorher/nachher: keine container/netzwerke/volumes angelegt (reine go build/test/git-arbeit).
- cleanliness: these lanes no new containers/networks/volumes/state-dirs; no compose project touched; ambient-core/ bilder fremder karren bleiben unangetastet.

## END
END_BLOCKED mission-182.md (0428-182 correction round) — correction-round conditional-guard UMGESETZT (branch A gruen/branch B rot proveniitzt), head `7725cdc1`, aber STOP: PARALLELE session w206 hat karte 0428-182 auf demselben branch implementiert (remote head `3a8f058b`), PR #1716 seit 13:53Z w206's. Report an owner: welche version integrieren? Kein force-push, kein zweiter branch, fremde commits nicht uebernommen.
