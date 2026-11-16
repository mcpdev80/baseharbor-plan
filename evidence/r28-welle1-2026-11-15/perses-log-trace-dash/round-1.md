# Round 1 evidence — t-20261114-r28-perses-log-trace-dash (0428-085)

Lane: lane-0428-085-perses-log-trace-dash
Shift: 2026-11-15/16
Author: w085 (worker)

## Task
Perses log and trace VIEWS — native Perses log/trace dashboards that consume the
existing Loki adapter (lane 086, internal/logs/loki_datasource.go) and Tempo
adapter (lane 091, internal/metrics/perses_tempo_datasource.go) read-only, with
a golden test per view and fail-closed when no validated Loki/Tempo signal or
release pin is present. No edits to the 086/091 adapter files.

## Union-fan-in base (regel 8)
- Approved seam 492b8e8f994b16e6f73819a08175f8178cd63292 is an ancestor of the
  base head I cut from (verified: git merge-base --is-ancestor 492b8e8f994 HEAD).
- Basis heads fetched via git ls-remote origin (fresh), not the quarantined
  workers/baseharbor checkout.
- Tempo basis head: origin/w091-0428-091 = d8ffac475e28ed82220e48e5216df287adadc6df
  (mission's 99859f60b7a... is stale; the current remote head is d8ffac47).
- Loki basis head: origin/lane-0428-086-perses-loki-source = 7bf8f407afebc1cf605376cd53e79201a69b8fe3
- Union merge commit: edc69c19a32f577d852c10a5a18ec8fea4517a9c
  parents: d8ffac47 (tempo) 7bf8f407 (loki)
  git rev-parse edc69c19 -> %H %p shows exactly two parents, both basis heads.
- Merge was conflict-free (disjoint adapter files), as the mission predicted.

## Remote witnesses (git ls-remote origin, fresh)
```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w091-0428-091
8... d8ffac475e28ed82220e48e5216df287adadc6df
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-086-perses-loki-source
... 7bf8f407afebc1cf605376cd53e79201a69b8fe3
git ls-remote https://github.com/mcpdev80/baseharbor.git 492b8e8f994b16e6f73819a08175f8178cd63292
... 492b8e8f994b16e6f73819a08175f8178cd63292
```

## Scope decision (coordinator 2026-11-16)
- Implement option A with placement-correct: NO new internal/observability package.
- Deliver internal/logs/perses_log_views.go + internal/traces/perses_trace_views.go
  (new files in the existing packages), go-structs -> deterministic JSON following
  the prometheus_files.go pattern, consuming the 086/091 adapter output read-only.
- Golden test per view; meaningful no-data + verified cells as the card requires;
  fail-closed on no validated signal / release pin.
- CLI hook only if the acceptance text explicitly asks, otherwise not.
- Schema = repo's own Perses-native format (precedent files), no external schema.
- Option B rejected (adapters are explicitly 086/091 work; my card is the view layer).
- Option C void (coordinator supplied the schema/source guidance directly).

## Import-cycle constraint (design driver)
- internal/metrics imports internal/traces (perses_tempo_datasource.go:17).
- Therefore internal/traces CANNOT import internal/metrics (would cycle).
- The trace view in package internal/traces builds from Tempo's own domain data
  (traces.ProviderEndpoint / traces.Placement / application.HasTraceSignal),
  mirroring the tempo adapter's PersesTempoDatasource shape with its own struct —
  the trace view owns the trace side of the Perses view layer, exactly as
  internal/logs owns the log side.

## Repo-rule compliance
- No edits to internal/logs/loki_datasource.go (lane 086).
- No edits to internal/metrics/perses_tempo_datasource.go (lane 091).
- No .github/** edits (Owner scope).
- No force-push, no merge into develop, no ready_for_review.
- Evidence lives ONLY in baseharbor-plan (evidence/r28-welle1-2026-11-15/), never
  in the product repo.

## Deliverable (HEAD: 91e7d1b8c38c2cab6ccb70def56210df8d90cf0f)
- Branch: lane-0428-085-perses-log-trace-dash (pushed to origin, head 91e7d1b8)
- Draft PR: https://github.com/mcpdev80/baseharbor/pull/1619 (base w091-0428-091,
  draft, title has 0428-085)
- 2 own commits: edc69c19 (union-fan-in) + 91e7d1b8 (view layer). No foreign
  commits. Cherry comparison --cherry shows only my 2 commits on top of the two
  basis heads.
- internal/logs/perses_log_views.go — Perses-native log view (one scoped LogQL
  panel per owned Loki datasource, no-data, fail-closed, JSON witness).
- internal/traces/perses_trace_views.go — Perses-native trace view (one scoped
  Trace panel per owned Tempo path, no-data, fail-closed, JSON witness), builds
  from Tempo's own domain data (no metrics import cycle).
- perses_log_views_test.go + perses_trace_views_test.go — fail-closed (unselected,
  foreign provider, unknown scope, unprovisioned Tempo), ProviderEndpoint
  contract, built-when-selected (one scoped panel, owner ref, native panel kind),
  deterministic JSON witness.
- Adapter files (internal/logs/loki_datasource.go, internal/metrics/perses_tempo_datasource.go
  + their tests + tempo.json) are BYTE-IDENTICAL to lane 086 / 091 heads
  (git diff empty): NO modifications, 086/091 ownership preserved.

## Verification (all local, own run)
- go build ./... : EXIT 0
- go vet ./internal/logs/ ./internal/traces/ : EXIT 0
- gofmt -l : clean (all 4 view files formatted)
- go test ./internal/logs/ ./internal/traces/ : ok / ok
- go test ./internal/capability/ ./internal/observability/ ./internal/application/ : ok / ok / ok

## Repo-rule compliance
- No edits to 086/091 adapter files (verified byte-identical).
- No .github/** edits (Owner scope).
- No force-push, no merge into develop, no ready_for_review.
- Evidence lives ONLY in baseharbor-plan evidence/r28-welle1-2026-11-15/, never
  in the product repo.
- No containers/compose projects started (no cleanup needed).

## END to coordinator
END_DONE head=91e7d1b8c38c2cab6ccb70def56210df8d90cf0f pr=1619 base=w091-0428-091
ci=dispatched by coordinator (Owner scope; no workflow_dispatch / no rerun).
