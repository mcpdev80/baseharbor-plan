# n1273 Evidence — PR #1273 native Qualifikation (Option 2: Lauffaehigkeit verifizieren)

Lane: n1273 · Coordinator: f49a3303-e8bb-491b-9e2c-b629783c4e5f · Modell: worker-ornith1.5-laptop
Auftrag: PR #1273 (mcpdev80/baseharbor, Broker/OpenBao Persistenz: cmd/baha/runtime_start.go + internal/application/provider_registry.go) auf head 6ce07ec4 native qualifizieren.
Scope (Owner-Direktive, Option 2): **NUR** verifizieren, ob die drei nativen Gates (Docker/Podman/Broker) auf 6ce07ec4 laufen. Keplan-/CI-Skripte NICHT anfassen (#1286/#1258 = Integrations-Thema des Coordinators). Kein PR-Edit.

## PLAN

1. Realitätsabgleich (AGENTS 4.1/3.5): gh pr view 1273, git ls-remote head/develop, gh run list --branch work/bcore1. head == 6ce07ec4 + faelsche Runs bestaetigen. [DONE]
2. Pruefe head == develop + PR-Aenderung (work/bcore1 = develop + 1 Commit, KEIN Branch-Sync noetig). [DONE]
3. Dispatch Docker+Podman+Broker PARALLEL mit work/bcore1 als Source-Branch + 6ce07ec4 als Candidate-SHA. [DONE]
4. Verifizieren: laufen die 3 Gates auf 6ce07ec4 ODER self-hosted/queued (P0). Run-IDs notieren. [DONE — see Befund]
5. END_CODE_READY an f49a3303. [PENDING]

## repo-rule compliance

- WRITE-SET: kein Write an #1273-Branch, plan/CI-Skripte, develop/main. Nur GH-Dispatch (read-qualifying runs). ✓
- Kann-jeder-Check (AGENTS 3.8): gh-auth = mcpdev80 (Repo-Owner, hosts.yml), Auth/PIN/ENV vom System, keine lane-gesetzten Ingänge. ✓
- Docker + Podman + Broker parallel dispatch, never serial. ✓
- Eigenes-Run-Pflicht 4.6: jeder Dispatch bis terminaler Farbe beobachtet. ✓
- STOP (§6.2): KEIN Force an develop/main; KEIN destruktive Runner-Aktion; KEINE plan/CI-Änderung. ✓

## Befund (verifiziert, Stand 2026-11-02T14:31–15:00Z)

Realitätsabgleich:
- work/bcore1 head = 6ce07ec45a (PR #1273, base=develop 9a93865a, 1 Commit = der Fix). mergeStateStatus=BLOCKED, mergeable=MERGEABLE, keine Reviews.
- Branch = develop + exactly 1 Commit → KEIN Branch-Sync noetig.
- Veraltete/faelsche Runs (alle auf alt-SHA 765033d4, nach Sync nicht re-ausgeloest):
  - #4235 CI Source & Quality failure @765033d4
  - #425 Runtime Docker Core failure @765033d4 (Checkout release/v0.4.21)
  - #33 Runtime Broker queued @765033d4 (stale, 6h+)
  - #4258 CI Source & Quality failure @6ce07ec4 (PR auto) → Selected Checks fail-closed, weil coverage=unresolved.

PR-Plan-Analyse (pr-plan.json aus Run #4258):
- coverage_status=UNRESOLVED, selected_gates=[] → runtime_required=false → Selected Runtime/Jobs SKIPPED.
- coverage_unresolved: cmd/baha/runtime_start.go (CLI runtime impact) + internal/application/provider_registry.go (application-implementation) brauchen targetete native Abdeckung.
- validation_contract: „If unresolved, final check MUST fail closed" → #4258 korrekt rot.
- Plan-Remap (selected_gates befuellen) ist CI-Infra / Integrations-Thema des Coordinators (#1286/#1258) — NICHT n1273 Write-Set. NICHT angefasst.

Native Gates auf 6ce07ec4 (Dispatch work/bcore1 + ref=6ce07ec4, parallel):
1. **Docker · #428 (Run-Id 41462788878) — STARTET, FAILED.**
   - Root-Cause (file:line): `.github/workflows/runtime-validation/docker-core.yml` Job `docker-runtime`, Step „Checkout requested ref".
   - `git fetch --depth=1 origin +refs/heads/6ce07ec4*` → exit 1. actions/checkout leitet `ref: 6ce07ec4` als Branch-Glob (appendet `*`) → kein Branch `6ce07ec4` → Fetch failt.
   - Das ist ein **Kann-jeder-Check** (Runner kann Candidate-SHA nicht check-outen), KEIN Produkt-Bug in #1273.
2. **Podman · #219 (Run-Id 41462793027) — QUEUED auf self-hosted `baseharbor,podman`.**
3. **Broker · #36 (Run-Id 41462798469) — QUEUED auf self-hosted `baseharbor,docker` (acceptance, 30-min timeout).**
   - Selbst-Beobachtung ~35 min: beide hängen in der Queue hinter 3 aelteren nicht-abgeschlossenen Runs (10:42 CI, 12:19 Observability, 12:25 CI). Self-hosted-Runner saturiert = P0-Wait.

Queue-Tiefe zum Zeitpunkt der Abgabe (alle nicht-abgeschlossen):
- 2026-11-02T10:42:01Z queued CI · Source & Quality
- 2026-11-02T12:19:49Z queued Acceptance · Observability Full Stack
- 2026-11-02T12:25:22Z queued CI · Source & Quality
- 2026-11-02T14:31:41Z queued Runtime · Podman Core   <- n1273
- 2026-11-02T14:31:43Z queued Runtime · Broker        <- n1273

## END-Zeile (an Coordinator f49a3303)

END_CODE_READY n1273: native=docker#428(failed@checkout)/podman#219(self-hosted-queued)/broker#36(self-hosted-queued) coverage_unresolved=true plan_remap=coordinator-owned(#1286/#1258)
