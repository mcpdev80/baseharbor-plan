# 0428-083 · Connect Perses Prometheus datasource — round-2 evidence

Mission: /tmp/opencode/mission-ds-r2.md
Card: 0428-083 · release v0.4.28 · type task · areas observability
Repeats round-1 work (round-1 akte: evidence/r28-welle1-2026-11-15/perses-datasources/round-1.md)

## PLAN (nummerliste)

- Read mission + akte round-1; confirm defect = gofmt on internal/metrics/perses_prometheus_datasource.go
- Verify base head via ls-remote (w083-perses-datasources @ 18360b69f9); cut wt from it; confirm ancestor
- gofmt -d witness before, gofmt -w, gofmt -d witness after
- fmt-commit on branch w083-perses-datasources (fast-forward-only, no -f)
- go build + go vet + targeted perses datasource tests all green
- git log origin/w083..HEAD = only my own commit
- Write this evidence akte (PLAN nummerliste, no checkboxes, gofmt before/after witness, test output, ls-remote new head)
- Confirm PR #1608 head updated, still draft
- Commit evidence to planning origin/main; confirm present; post END line + END to coordinator

## SCOPE

Round-2 is a formatting-only correction. No source semantics, no new tests, no shared-file edits, no .github/** edit. The akte round-2 @ 3fc50c52 attests SIGNATUR F: "Check formatting" red = gofmt defect in internal/metrics/perses_prometheus_datasource.go (and its test) on head 18360b69f9. Round-2 fixes only the flagged file.

## BASE ATTESTATION

- `git ls-remote origin refs/heads/w083-perses-datasources`:
  `18360b69f9070356d999ef54cf31fa9041c63f4e`
- Branch cut from that head; `git merge-base --is-ancestor 18360b69... HEAD` → YES.
- Candidate only my own commit on top of base (git log witness below):
  `git log --oneline 18360b69..HEAD` = only `01bc7d448`.

## GOFMN WITNESS (before / after)

Before (gofmt -l flags the file):
```
$ gofmt -l internal/metrics/perses_prometheus_datasource.go
internal/metrics/perses_prometheus_datasource.go
```

Before diff (gofmt -d), exactly two alignment groups:
```
diff internal/metrics/perses_prometheus_datasource.go.orig internal/metrics/perses_prometheus_datasource.go
--- internal/metrics/perses_prometheus_datasource.go.orig
+++ internal/metrics/perses_prometheus_datasource.go
@@ -69,10 +69,10 @@ type PersesPrometheusDatasourceConfig struct {
 // represented; the marshalling is deterministic and golden-tested.
 type PersesPrometheusDatasource struct {
-	Kind     string                         `json:"kind"`
-	Name     string                         `json:"name"`
-	Default  bool                           `json:"default"`
-	Config   PersesPrometheusDatasourceConfig `json:"config,omitempty"`
+	Kind    string                           `json:"kind"`
+	Name    string                           `json:"name"`
+	Default bool                             `json:"default"`
+	Config  PersesPrometheusDatasourceConfig `json:"config,omitempty"`
 	// Owner is the real observability capability owner Perses visualises.
 	// It is the Prometheus provider kind, named as an owner reference, NOT a
 	// Perses-declared capability. It is not serialized: the datasource declares
@@ -150,8 +150,8 @@ func persesPrometheusDatasourceFromRelease(m application.Manifest, release capab
 		}
 	}
 	return PersesPrometheusDatasourceResult{
-		Datasource:     datasource,
-		Reachability:   PersesPrometheusReachabilityUnverified,
+		Datasource:   datasource,
+		Reachability: PersesPrometheusReachabilityUnverified,
 	}, nil
 }
```

After (file clean):
```
$ gofmt -w internal/metrics/perses_prometheus_datasource.go
$ gofmt -l internal/metrics/perses_prometheus_datasource.go
(empty = clean)
$ gofmt -d internal/metrics/perses_prometheus_datasource.go
(empty = clean)
```

The test file internal/metrics/perses_prometheus_datasource_test.go was already gofmt-clean on 18360b69 (only the source file was flagged).

## TEST + BUILD VITNESSES

```
$ go build ./...
(no output)
$ go vet ./internal/metrics/
(no output)
$ go test ./internal/metrics/ -run TestPersesPrometheusDatasource -v
=== RUN   TestPersesPrometheusDatasourceShape
--- PASS: TestPersesPrometheusDatasourceShape (0.00s)
=== RUN   TestPersesPrometheusDatasourceNamesPrometheusOwner
--- PASS: TestPersesPrometheusDatasourceNamesPrometheusOwner (0.00s)
=== RUN   TestPersesPrometheusDatasourceNoCapabilityClaim
--- PASS: TestPersesPrometheusDatasourceNoCapabilityClaim (0.00s)
=== RUN   TestPersesPrometheusDatasourceNoSecretInDescriptor
--- PASS: TestPersesPrometheusDatasourceNoSecretInDescriptor (0.00s)
=== RUN   TestPersesPrometheusDatasourceAccessIsProxy
--- PASS: TestPersesPrometheusDatasourceAccessIsProxy (0.00s)
=== RUN   TestPersesPrometheusDatasourceFailClosedWhenUnpinned
--- PASS: TestPersesPrometheusDatasourceFailClosedWhenUnpinned (0.00s)
=== RUN   TestPersesPrometheusDatasourceUnverifiedReachability
--- PASS: TestPersesPrometheusDatasourceUnverifiedReachability (0.00s)
=== RUN   TestPersesPrometheusDatasourceVerifyFailClosed
--- PASS: TestPersesPrometheusDatasourceVerifyFailClosed (0.00s)
=== RUN   TestPersesPrometheusDatasourceGoldenFiles
--- PASS: TestPersesPrometheusDatasourceGoldenFiles (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.005s
```

## CI COVERAGE (Owner directive 2026-11-07)

The fmt change touches only the source file covered by the existing unit-test group that already runs `TestPersesPrometheusDatasource*` (all 9 pass). No `.github/**` edit is required:

- `.github/workflows/ci.yml` runs `go test ./contracts/... ./internal/... ./spec/...` and `go test ./...` (round-1 akte, unchanged). The metrics package is part of `./internal/...`, so the gofmt'd file is exercised by the existing CI group. No VM-only or local-only test was introduced; no CI change needed.

## PR STATUS

- PR #1608 (gh): baseRefName `lane-0428-075-perses-seam`, headRefOid `01bc7d448665654124fd13908424c52eecc60cb9`, isDraft true, state OPEN. Draft remains draft; head already follows the new branch head.

## WITNESSES

- Branch provenance (origin, before first evidence commit):
```
$ git ls-remote origin refs/heads/w083-perses-datasources
18360b69f9070356d999ef54cf31fa9041c63f4e	refs/heads/w083-perses-datasources
```
- Candidate head + provenance (origin, after push):
```
$ git ls-remote origin refs/heads/w083-perses-datasources
01bc7d448665654124fd13908424c52eecc60cb9	refs/heads/w083-perses-datasources
$ git log --oneline 18360b69..origin/w083-perses-datasources
01bc7d448 fmt(0428-083): gofmt perses_prometheus_datasource.go (round-2)
```
- Only my own commit on top of base 18360b69 (git log witness). No second candidate branch.

## REPO-RULE COMPLIANCE

- Single write-set, fmt-only change to own adapter file. No shared/seam/capability file edits.
- No `.github/**` edits (Owner scope). No reruns, no workflow_dispatch.
- No containers/compose started (coordinator/codeman host is a forbidden test host; baha-runner-* are not test hosts).
- No subagents (§4.8).
- Branch provenance: cut from 18360b69f9, only my own commit 01bc7d448 on top (git log witness). No second candidate branch.

## CLEANLINESSION (/tmp/opencode/w083-r2)

- No docker/podman compose projects, networks, volumes or state directories started.
- Worktree /tmp/opencode/w083-r2 contains only the baseharbor checkout + my one staged file. No stray test artifacts.
- `docker ps`/`docker compose ls`/`docker network ls`/`docker volume ls` all empty (no containers). No orphan cleanup needed.

## END LINE

END DONE mission-ds-r2.md: 0428-083 Perses datasource round-2 gofmt fix applied to internal/metrics/perses_prometheus_datasource.go (two gofmt alignment groups realigned, pure formatting, test file already clean), go build/vet clean, all 9 TestPersesPrometheusDatasource* tests pass, fast-forward fmt-commit 01bc7d448 on branch w083-perses-datasources (base 18360b69f9, only own commit), draft PR #1608 head now 01bc7d448 still draft, no .github edits, no containers, no subagents.
