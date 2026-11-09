# 0427-175 round 11 (Deckungsschließung) — END_DONE-Unterlage

**Task:** `t-20261108-bughunt-concurrent-init-double-registration` (card `0427-175`)
**PR:** [baseharbor#1512](https://github.com/mcpdev80/baseharbor/pull/1512) · branch `0427-175-initlock`
**Candidate HEAD:** `2dfcb21fed35b4672ddbd9dab931cb227f7a5d85` (= `origin/0427-175-initlock` = `origin/pull/1512/head`)
**Worker:** worker-ornith1.5 · `0427-175-r8`
**Basis dieser Unterlage:** Owner-Deckung (175-r8), Lauf `42687854644`

## Entscheidung (Owner-Regel, wörtlich)

> Gegenprobe läuft (workflow_dispatch auf develop d2e225f20). Ist develop
> rot: END_DONE-Unterlage mit Verweis auf meine Gegenprobe + dein PASS-Anteil.
> Ist develop grün: dann Wechselwirkung mit deinem Diff — Korrekturrunde.

## Befund

- **Gegenprobe = develop `d2e225f20` → ROT.** CI-Run `5571`, ausgelöst per
  `workflow_dispatch`, Kopf `d2e225f2000b88ee255559b0cc3f9ac51c225e7e`,
  `status=completed`, `conclusion=failure`, begonnen
  `2026-11-09T20:08:26Z`.
- **Daher: END_DONE-Unterlage.** Der w169-Fehler ist ein Base-Compound
  (bekannte `w169`-Fixture-Familie), **nicht** der 0427-175-Diff.

## Durable witness (Gegenprobe 5571)

Transkript: `evidence/bughunt-concurrent-init-double-registration/gegenprobe-develop-5571.json`

```json
{
  "conclusion": "failure",
  "createdAt": "2026-11-09T20:08:26Z",
  "headSha": "d2e225f2000b88ee255559b0cc3f9ac51c225e7e",
  "number": 5571,
  "status": "completed"
}
```

Quelle (API, reproduzierbar):
```
gh run list --repo mcpdev80/baseharbor --branch develop --event workflow_dispatch --limit 3
```

## Warum die zwei Ausfälle NICHT mein Diff sind

- Auslöser in Lauf `42687854644` (Paket `cmd/baha`):
  `TestRepositoryWorkflowRealLifecycle` und
  `TestRepositoryComposeWorkloadUsesBootstrap` / die `w169`-Serie.
- Fehlerbild durchgängig:
  `missing deployment state for w169-repository-workflow-... : deployment has
  no authoritative installation owner for its Target; the installation must be
  restored before its state is loadable` — erst-Apply-Zusammenstoß auf dem
  persistenten `validate`-Runner, Signatur eines Base-Compounds, nicht des
  0427-175-Diffs.
- Die Gegenprobe auf **vanilla develop** (`d2e225f20`, ohne jeglichen 0427-175-
  Anteil) schlägt **gleichlaufend rot**. Ein Diff, der auf develop nicht
  vorhanden ist, kann diese Ausfälle dort nicht verursachen.
- Die ausfallenden Tests rufen **keine** meiner änderten Funktionen auf
  (`saveDeploymentRecord`/`persistDeploymentRecord`, `resolveRecordByIdentity`,
  `assertSelectionResolvedIdentity`, `refuseRegistryApplicationIDConflict` sind
  in `repository_runtime_fixture_test.go` / `app_workload_integration_test.go`
  nicht vorhanden).

## Mein PASS-Anteil (isoliert belegt)

- **Readability / Source-Format Gate: PASS.** `app_context.go` = 716/800,
  `saveDeploymentRecord` = 152/200 — beide unter der Gate-Grenze; das
  source-format-Job hat **nicht** getriggert. Der Refactor (round-10) hielt.
- Lokale Verifikation auf `2dfcb21f`:
  - `go build ./...` → OK
  - `go vet ./cmd/baha/ ./internal/deployment/` → clean
  - `gofmt -l` auf den drei änderten Dateien → clean
  - `internal/deployment` full suite → ok
  - Fokussierte `cmd/baha`-Suite (registry/destroy/poison/repair/`TestUpNameResumes`) → ok
- Race regression `cmd/baha/app_init_concurrent_race_test.go` vs r7
  `a65f3d974` → diff 0 (unverändert).

## Was NICHT abgenommen ist

- Lauf `42687854644` (Kopf `2dfcb21f`) ist ein terminaler CI-**FAILURE** auf
  den `w169`-Native-Runtime-Tests. Das ist kein akzeptierter Kandidat.
- END (Abnahme des finalen, SHA-genauen Kandidaten) bleibt dem Owner / der
  Abnahme-Rolle vorbehalten. Diese Unterlage **dokumentiert** die Deckung,
  ersetzt aber **nicht** die eigentliche Abnahme/einen grünen Lauf.
- Der Owner hat die Gegenprobe als Decider gesetzt; die Unterlage verweist
  darauf und belegt den PASS-Anteil.

---

## END_DONE

0427-175 r8 Deckung geschlossen: develop `d2e225f20` CI-Run `5571`
(workflow_dispatch) = ROT → w169-Ausfälle sind Base-Compound, nicht der
0427-175-Diff. Readability-Gate PASS (app_context.go 716/800,
saveDeploymentRecord 152/200); lokale fokussierte Suite + race regression
grün; gegenprobe-Transkript in der Evidence. END_DONE 0427-175-r8-deckung:
develop 5571 failure (d2e225f20) = base w169 compound; readability PASS; PASS
anteil belegt — Abnahme/EIGO des finalen Kandidaten bleibt Owner.
