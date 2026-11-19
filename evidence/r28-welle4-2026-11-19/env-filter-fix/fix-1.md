# fix-1 — t-20261119-hunt-metrics-env-filter-list-pfade (hunt-918 Befund 2, HIGH)

Lane: mission-efilter.md (t72)
Card: t-20261119-hunt-metrics-env-filter-list-pfade
Branch: lane-0428-efilter (base: develop)
Repo: baseharbor

## PLAN

1. Claim card via plan.py + reality check: `git ls-remote` develop (mission says currently de53246585), verify planning repo remote origin
2. Read hunt-918 evidence `evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md` Befund 2 (17 probes as template)
3. Write RED regression: environment filter checked on EVERY list path (no caller-prefix workaround)
4. Implement fix: one central filter path instead of caller-prefix; no touch of merged registry/List chain (dd62b9d3, card 102) without STOP+file:line; no impact on cmd/baha (card 118 territory, merged)
5. Run affected tests + `go vet` + `go build`; regression must go red->green
6. Open PR: base develop, branch lane-0428-efilter; prove base SHA is ancestor of first commit; ls-remote witness
7. Wait for exact-head CI run to TERMINAL state; record run id, status, failing lines
8. Commit evidence to baseharbor-plan origin/main and verify path present there before END
9. Post END line to coordinator session; clean up (no compose projects expected on this host)

## base attestation

(pending — will record exact develop SHA cut from + ancestor proof)

## reality witnesses

(pending — `git ls-remote` outputs only)

## regression (red -> green)

(pending)

## repo-rule compliance

(pending)

## END

(pending: `END mission-efilter.md DONE|BLOCKED`)
