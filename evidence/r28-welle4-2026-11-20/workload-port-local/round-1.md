# 0428-199 · workload-port ignored locally — w199-0428-199-workloadport

- Owner: w199-0428-199-workloadport
- Card: 0428-199
- Release: v0.4.28
- Type: bug (cli)
- Anchor SHA (develop, measured via ls-remote): 40cb28c758b02960356434b630086a341ebe1738
- Git remote guard: `git remote -v` on baseharbor shows `lane-origin https://github.com/mcpdev80/baseharbor.git`; `git ls-remote lane-origin refs/heads/develop` -> 40cb28c758b02960356434b630086a341ebe1738. Worktree cut from that exact head at /tmp/opencode/lane-0428-199-workloadport-wt.
- Evidence path: evidence/r28-welle4-2026-11-20/workload-port-local/round-1.md (baseharbor-plan)

## PLAN

1. Basis attestieren: develop head 40cb28c via ls-remote, Worktree aus develop, Binary aus source bauen.
2. Dokumentierten Text zeigen: cmd/baha/app_apply.go:42-43 (Usage + Long nennen '--workload-port NAME=PORT'); Remote-Pfad cmd/baha/management_remote_mutation.go:204-235 (extractRemoteWorkloadPorts) -> management_http_executor_lifecycle.go:153 (withRequestedWorkloadPorts, via machine_http_executor_lifecycle.go:153); app_workload_ports.go:33 withRequestedWorkloadPorts / 545 persistRequestedWorkloadPortSelections.
3. Lokal-Pfad zeigen: cmd/baha/runtime.go:78 parseRuntimeUpOptions (kein --workload-port case, unknown-option fallback), cmd/baha/app_input_resolver.go:475/601 resolveApplicationEnvironment, cmd/baha/app_context.go:597 extractApplicationEnvironment; cmd/baha/app_apply.go Run (kein Parse).
4. Build + beide Basisfehler wortlich wiederholen (app apply -> 'accepts at most one NAME'; up -> 'unknown option --workload-port', exit 2).
5. Fix Lokal-Pfad: app apply arg-strip + withRequestedWorkloadPorts; up parseRuntimeUpOptions WorkloadPorts + runtimeUpCommand context-set. Geteilte option-parade reused.
6. Regression Tests pro Kommando durch echte CLI-Oberflaeche (distinct failing test each).
7. gofmt/vet/build, Tests, feste Fehler bestaetigt, cleanup.
8. EIN commit, PR draft base develop, push, CI shard executed am exakten head.
9. Evidence auf baseharbor-plan origin/main, path-present, END.

## Fund / Aufgabe

Dokumentierter `--workload-port NAME=PORT` soll auf dem LOKALEN apply/up-Pfad dasselbe tun wie auf dem remote-Pfad. Remote-Pfad paart den Flag in `extractRemoteWorkloadPorts` (management_remote_mutation.go:204) und setzt `withRequestedWorkloadPorts` (via machine_http_executor_lifecycle.go:153); der lokale Pfad fuehrt den dokumentierten Wirtsport nie aus. Messen mit shipped binary:
- `baha app apply --workload-port web=9090` -> `Error: baha app apply accepts at most one NAME` (exit 2)
- `baha up --workload-port web=9090` -> `Error: unknown option --workload-port` (exit 2)

Beide Fehler mit lokalem Target (`--target local`) reproduziert; Texte stimmen mit Hunt-Akte ueberein.

## repo-rule compliance

- Erlaubtes Write-Set: cmd/baha/app_apply.go, cmd/baha/runtime.go, cmd/baha/app_input_resolver.go (nur der lokale --workload-port Parse + context-set, nicht die resolver-Logik), cmd/baha/app_workload_ports.go (nur die geteilte option-parade: extractLocalWorkloadPorts), plus neue Testdatei cmd/baha/workload_port_local_regression_test.go.
- Verschlossen, NICHT beruehrt: cmd/baha/context_terminal*.go (#1718), internal/observability/registry.go, internal/metrics/** (#1714), internal/serviceaccess/** + internal/application/perses_runtime.go (#1684), internal/identityprovider/** + internal/operatorauth/** + internal/machine/** (#1594/#1615/#1650).
- Kein .github/** Aenderung. Keine Tests anderer Pakete. Kein 'skip'.
- Kein `git add -A`. Kein Subagent (4.8). Alle Messungen via git ls-remote im eigenen Worktree.
- CI-Hinweis: Seit develop 40cb28c (#1594-merge) failen cli-0..3 shards mit operator/OIDC-Meldung (0428-198, andere lane). Eigener Fall kommt aus dem kleinsten passenden gate ('go test ./cmd/baha/... -run <tests>'); stirbt der run daran: run-id + zeierliche zeile, 'GATE-FAIL 0428-198'.

## cleanliness

- Container/Netzwerke/Volumes/State-Verzeichnisse: KEINE gestartet. Session-Host ist der Codeman/Coordinator-Server; Docker/Podman-Tests nur auf benannten SSH-Hosts.
- vorher: /tmp/lane-199-baha (binary), /tmp/opencode/lane-0428-199-workloadport-wt (worktree), /tmp/lane-199-err (state/config via BASEHARBOR_TARGET_LOCAL).
- nachher: alle /tmp/lane-199-* Temp-Zonen aufgeraemt; baseharbor-plan evidence nur auf origin/main (kein produkt-repo-write). ambient-core/ Bilder fremder Karren unangetastet.
- cleanliness: clean.

## END

END_DONE w199-0428-199-workloadport (0428-199 workload-port ignored locally). Fix am lokalen apply/up-Pfad + regression tests. candidate SHA: <to be recorded at push>; evidence: evidence/r28-welle4-2026-11-20/workload-port-local/round-1.md.
