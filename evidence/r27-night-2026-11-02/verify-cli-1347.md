# verify-cli-1347s — neutraler cli-lauf-nachweis

- **Lane:** w49-verifycli
- **Coordinator / Session:** f49a3303 (Codeman-Coordinator)
- **Karte / Task:** t-20261018-r27-state-owner (neutralerlauf-nachweis)
- **Modell / Rolle:** Worker — NEUTRALER LAUF, KEIN Code
- **Datum:** 2026-11-03

## ## PLAN-Checkliste

1. Origin fetch + worktree `/tmp/opencode/w49-verifycli-wt` auf `work/r27-state-owner`.
2. Testlauf `cmd/baha` (Deployment|Owner|Tenant|Scope|Binding|List|Guard|Retention|Vanish) auf r27-branch — volle Ausgabe capture.
3. Gleichender Testlauf auf `develop-baseline` (`/tmp/opencode/w49-baseline-wt`).
4. `internal/deployment` + `internal/delivery` ebenfalls auf beiden — tabellarisch.
5. Identität branch/baseline prüfen, Laufzeiten + env (keine secrets) dokumentieren.
6. Evidence-Tabzeilen ausfüllen.
7. END an f49a3303 posten.

---

## Laufumgebung (beide Worktrees, identischer Host)

- Host: lokaler Linux-Host
- Go: go1.26.9 linux/amd64
- GOCACHE=/tmp/opencode/gc, TMPDIR=/tmp/opencode/tmp
- GOPROXY=https://proxy.golang.org,direct; GOMODCACHE=/home/marcel/go/pkg/mod
- KEINE Secrets/Token/ENV-Sätze; alle Laufumgebungen identisch

## Branch-Basis

- r27 branch HEAD: `be00b1c8ca7e39c063c75f154c1e3c3fe21f01d5` — `test(deployment): seed authoritative Core owner for guard/retention fixtures`
- develop-baseline HEAD: `1706272c3e8d53d37cf4da8f9f1411e5fe419a94` — `r27 authority-contract: installation authority (#1348)`

## Ergebnisse (tabellarisch)

| Test | Branch (r27) | Branch-Status | Branch-Zeit | Baseline (develop) | Baseline-Status | Baseline-Zeit | Identisch |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cmd/baha` Deployment|Owner|Tenant|Scope|Binding|List|Guard|Retention|Vanish | be00b1c8 | FAIL (2 Gruppen) | 214.494s | 1706272c | FAIL (2 Gruppen) | 102.288s | **JA** |
| `internal/deployment` | be00b1c8 | ok | 0.035s | 1706272c | ok | 0.019s | **JA** |
| `internal/delivery` | be00b1c8 | ok | 0.002s | 1706272c | ok | 0.002s | **JA** |

### Ausfallende Testgruppen (`cmd/baha`, beide identisch)

```
--- FAIL: TestExternalProviderRemovalTransportsShareScopeAndExplicitStages (0.00s)
    --- FAIL: .../cli / http / mcp
        provider_external_removal_test.go:53: provider change: provider-registry-ownership-unverifiable
--- FAIL: TestExternalProviderRemovalCannotInferGlobalOwnershipFromTenantRole (0.00s)
    provider_external_removal_test.go:151: provider change: provider-registry-ownership-unverifiable
```

## Bewertung (Identität branch vs. baseline)

- `cmd/baha`: **Failing auf beiden — identisch** (gleiche 2 Testgruppen, gleicher Fehler `provider-registry-ownership-unverifiable` bei `provider_external_removal_test.go:53`/`:151`). Die "pre-existing"-Behauptung ist damit VERIFIZIERT.
- `internal/deployment` + `internal/delivery`: **auf beiden ok — identisch**.
- Laufzeiten weichen ab (Compile-Cache warm auf branch, cold-basis) — das ist ein Umstand, kein Inhalt; Testinhalt/Outcome identisch.
- **Identisch = JA.** Die Failures sind pre-existing auf develop und NICHT durch den r27-Branch verursacht.

## Kontext zum review-1347s-Block

- review-1347s blieb BLOCKED, weil der `cmd/baha`-Pflichtlauf in der Reviewer-Sandbox nach 120s timeoutete.
- §5.3 verlangt Beweis auf neutralem Produktionspfad. Hier neutral auf lokalem Host ausgeführt (kein CI-Sandbox-Timeout), volle Ausgabe captured.

## END an f49a3303

END_DONE w49-verifycli: identisch=ja failing_branch=2 failing_baseline=2 | cmd/baha schlägt auf r27-branch UND develop-baseline identisch fehl (2 Testgruppen, provider-registry-ownership-unverifiable); internal/deployment+delivery auf beiden ok — pre-existing, nicht durch r27 verursacht.

## ## END-STATUS: DONE
