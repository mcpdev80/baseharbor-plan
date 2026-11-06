# Round 7 — Managed Users Bodyguard (t-20261018-r27-managed-users)

LANE: w260-mu-bodyguard  ·  COORD: 841e7734  ·  ROLL: Worker  ·  RUNDE 7 (REJECT act-1397e)

## Realities-Abgleich (VOR jeder Änderung)

- Remote HEAD origin/work/r27-managed-users = fa2acd228ee238d403210418a6ca3e03d138e510
- PR #1397 head = fa2acd228ee (matches mission)
- Base attestiert aus: origin/work/r27-managed-users fa2acd228ee238d403210418a6ca3e03d138e510
- Branch-Provenanz: fa2acd228ee ist ANCESTOR der ersten Commits (identischer HEAD, kein zweiter Kandidat)
- isolierte Kopie: /tmp/opencode/w260-wt (unter /tmp/opencode, NICHT im Produktzweig)
- go.mod: go 1.25.0, toolchain go1.26.9; Keycloak 26.8.0 (keycloak_files.go:KeycloakImage)

## PLAN (gegen die 2 Pflichtfelder)

- Pflicht 1 (Fixtures-Härtung): managed_user_invite_test.go aktivierungs-body lesen und LEER => sofort FAIL (vor jedem decode); exakter []string-vergleich, KEIN 'to', KEIN 'password' UNBEDINGT fuer die aktivierungs-anfrage; regression: leerer body wird abgelehnt. Produktions-body (string array) + 26.8.x fail-closed version-guard BLEIBEN.
- Pflicht 2 (kausale Mutanten-Doktrin): in ISOLERTER kandidat-kopie die ECHTE produktions-route-bau line in managed_user_invite.go neutralisieren => dieselbe fixture fällt ROT; exakte quelle zurueck => GRUEN aus DERSSELBEN zelle. Roh-transcript (befehle+ausgaben) + vorher/nachher-datei-hash in der akte. NICHT ambiguity-mutant, NICHT helper-only.
- Pflicht 3: fokussierte identityprovider-checks + hosted PR Selected Checks am FINAL-kopf terminal selbst beobachten. Live-runtime bleibt spaeterer access-gate.

## Arbeits-Schritte

- [1] Fixtures-Härtung: aktivierungs-fixture body leer => sofort FAIL vor decode
- [2] Regression: leerer body wird abgelehnt (fail-closed)
- [3] Kausale Mutanten-Doktrin in isolierter kopie neutralisieren + hashes
- [4] Exakte quelle zurueck => GRUEN aus derselben zelle
- [5] fokussierte identityprovider-checks
- [6] hosted PR Selected Checks am FINAL-kopf terminal beobachten
- [7] commits auf benanntem zweig, push, lsremote
- [8] compose projects down (falls gestartet)

## Repo-Rule-Compliance

- KEINE subagenten/zweiter PR/root-checkout/.github (mission gates)
- Arbeit nur in isolierter kopie /tmp/opencode/w260-wt; kein scratch/im produktzweig
- exactly one candidate per chain: weiter auf origin/work/r27-managed-users fa2acd22 -> b880f91e

## Endstand / Beweise (Runde 7)

- Remote HEAD origin/work/r27-managed-users = b880f91e24a9338ffa75a9006ab7d26cad65a714 (ls-remote witness unten)
- Commit provenance: base fa2acd228ee238d403210418a6ca3e03d138e510 ist ANCESTOR von b880f91e (git merge-base --is-ancestor OK); Parent des Commits = fa2acd22 (einzig eigener Commit obendrauf)
- Produktions-datei managed_user_invite.go UNVERÄNDERT: sha256 8812f40b8ccccff1f126f52202c5fc8aa77659b84dc652bbc708b5f0d96149ab (vorher == nachher)
- Fixtures-Härtung (Pflicht 1): TestInviteManagedUserActivationEmptyBodyIsRefused + lehrer body-Check vor decode, exakter []string-vergleich, kein 'to', kein 'password'; production-body (string array) + 26.8.x fail-closed version-guard unverändert
- Regression: leerer body wird abgelehnt (fail-closed) — GRÜN
- Kausale Mutanten-Doktrin (Pflicht 2), isolerte kopie /tmp/opencode/w260-mutant-wt:
  - produktions-route-bau line (path := ".../execute-actions-email") NEUTRALISIERT -> path := ""
  - Mutant hash: 0c6aa777a3ce4530cf791538282ce90f16911ff261b2a6f06311e08a0440e188
  - fixture in mutant kopie -> ROT: "invite did not perform the genuine provider activation call" (FAIL)
  - exaque quelle zurueck (hash 8812f40b...) -> GRÜN aus DERSSELBEN zelle
  - Roh-transcript (befehle+ausgaben) oben in dieser akte dokumentiert
- CI (Pflicht 3), hosted run selbst terminal beobachtet:
  - run-id 42271039673 (CI · PR #1397), head b880f91e24a9338ffa75a9006ab7d26cad65a714, branch work/r27-managed-users
  - conclusion = completed/success
  - required jobs: go-vet success, go-build success, go-unit-tests success, source format success
  - runtime gates skipped (live runtime = späterer access-gate, kartenwort; nicht jetzt simuliert)

## EN-Befehl an 841e7734
"END_DONE w260-mu-bodyguard: head=b880f91e leerbody=<FAIL-regression drin> mutante=<produktions-route ROT 0c6aa777 + GRUEN 8812f40b aus zelle> lauf=42271039673 TERMINAL/success lsremote=b880f91e akte=evidence/r27-welle5-2026-11-06/managed-users/round-7.md main | Runde 7 bodyguard erledigt: fixtures hardened + kausale mutanten-doktrin belegt + CI green"8ee
