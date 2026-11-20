---
id: t-20261120-r28-bughunt-target-uid-migration
kanban_title: 0428-161 · bughunt target uid migration
card_number: "0428-161"
card_short_title: "bughunt target uid migration"
type: task
areas: [cli, application, security]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: ""
kanban_status: planned
kanban_lane: ready
blocker: ""
resolution: ""
evidence: []
prs: []
created: 2026-11-20
wait_reason: ""

---
- [ ] t-20261120-r28-bughunt-target-uid-migration · ## Ziel

Bug-Hunt-Schnitt H-V11 auf dem frisch gemergten uid-target-pfad (#1580, merge bbc937c8f1,
'fix: serialize legacy target UID migration writes'). Reine befundung, keine produktaenderung.

## Pruefschnitte

1. V1 idempotenz: zwei laeufe der migration auf demselben bestand.
2. V2_serialisierung: zwei schreibende zugaetze gleichzeitig, kein verlorengegangener eintrag.
3. V3 no-mutation-rule: MigrateLegacyTargetUIDs veraendert nichts an bestehender uid.
4. V4 was ein observer sieht: status/desk vor und nach der migration.

## Akte

evidence/r28-welle4-2026-11-19/bughunt-target-uid-migration/round-1.md

## Ziel

Bug-Hunt-Schnitt H-V11 auf dem frisch gemergten uid-target-pfad (#1580, merge bbc937c8f1,
'fix: serialize legacy target UID migration writes'). Reine befundung, keine produktaenderung.

## Pruefschnitte

1. V1 idempotenz: zwei laeufe der migration auf demselben bestand.
2. V2_serialisierung: zwei schreibende zugaetze gleichzeitig, kein verlorengegangener eintrag.
3. V3 no-mutation-rule: MigrateLegacyTargetUIDs veraendert nichts an bestehender uid.
4. V4 was ein observer sieht: status/desk vor und nach der migration.

## Akte

evidence/r28-welle4-2026-11-19/bughunt-target-uid-migration/round-1.md

## Pruefschnitte

1. Symlink-Enthaltung an jedem Ort, der einen Component-Pfad aufloest (S1).
2. 'unique components' gegen registry und footprint (S2).
3. maschinelle CLI-Registrierung (machine_coverage.go, handschriftlich) gegen den echten Kommando-Baum (S3).
4. wizard- und mcp-Pfade gegen denselben Validierungshelfer wie der source-model-Zweig (S4).

## Akte

evidence/r28-welle4-2026-11-19/bughunt-uid-app/round-1.md
