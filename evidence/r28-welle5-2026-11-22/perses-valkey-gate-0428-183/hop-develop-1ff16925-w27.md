# 0428-223-testctx — PR #1714 mechanical hop onto develop 1ff16925c4e

## PLAN

- (done) 1. ls-remote-abgleich: develop 1ff16925c4e, refs/pull/1714/head fc525970d41 (merge=BEHIND gemeten), branch lane-0428-183-valkey-dashboard-gate
- (done) 2. Additiever hop git merge --no-ff 1ff16925c4e → 67495fde968, back=0, keine Konflikte, kein rebase/amend/force
- (done) 3. Push ohne force fc525970..67495fde + ls-remote delivery-witness (branch und refs/pull/1714/head)
- (done) 4. Exakter PR-run am neuen head bis terminal: 44989324573 completed SUCCESS, failed jobs: 0
- (done) 5. BEWEIS: packages-shard job 137106741719 = 'PR · Go unit · packages', receipt-Zeilen unten (internal/metrics-Shard inklusive). Kein separater internal/metrics-Shard-Job in dieser Suite; die drei Tests liegen in internal/metrics und laufen im packages-Shard (datei:line unten).
- (done) 6. Akte publizieren auf plan origin/main + ls-tree-witness
- (pending) 7. END post aan 9142ab1f

## Witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1714/head` (before hop): develop `1ff16925c4e141d732459a34ddf0b7f49128a214`, PR head `fc525970d4171e5e15a1a734a1a38193dcd55971`; `gh pr view 1714` → base develop, OPEN, draft=false, **mergeStateStatus=BEHIND** (der einzige mechanische Mangel, gemessen).
- Remote guard: `git remote -v` → `origin https://github.com/mcpdev80/baseharbor.git` (alle fetch/push-Operationen über die echte URL).
- Plan repo zone: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## Hop (additiv, Inhalt unveraendert)

- Zone: eigene temporäre detached worktree `/tmp/opencode/0428-223-hop1714` (fremde Lane-Worktrees nicht angefasst; vor der Mission existierende Reste anderer Lanes dort wurden nicht erweitert).
- `git merge --no-ff 1ff16925c4e…` → merge commit `67495fde96837846d9d2b26e8db5ad93b7b7c988`, rc=0, keine Konflikte.
- Ancestry-Zeugen: `git merge-base --is-ancestor 1ff16925c4e HEAD` = yes; `--is-ancestor fc525970d41 HEAD` = yes (FF-push, kein force). back=0.
- `git diff fc525970d41 HEAD --name-only`: `.github/workflows/ci.yml`, `scripts/pr-check-runner.py`, `scripts/pr-gate-plan.py`, `scripts/pre-release-runtime-impact.json`, `scripts/test_pr_check_runner.py`, `scripts/test_pr_gate_plan.py`, `scripts/test_pre_release_runtime_reuse.py` = **develop's eigene Inhalte via merge** (der #1755-Zulassungsschwung); durch mich wurde KEINE Datei geaendert, insbesondere keine der gesperrten Pfade als BEARBEITUNG (`.github/**`, `scripts/**`, `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identity/**`, `internal/serviceaccess/**`, `internal/operatorauth/**`).
- `git log --oneline 1ff16925c4e..HEAD`: 67495fde (mein hop) + fc525970 (der eine feature-commit der Karte) + die historischen hop-merges der Lane (277ff976, 731302e9) + die r1-r4 feature commits (ecff7e2f, a11c44d7, 349372d7, 14403c77) = unveraenderte Lane-Geschichte, ein feature-Commit, keine fremde Kandidatenkette obendrauf.
- Push: `fc525970..67495fde HEAD -> lane-0428-183-valkey-dashboard-gate`; delivery witness `git ls-remote … refs/heads/lane-0428-183-valkey-dashboard-gate refs/pull/1714/head` → beide `67495fde96837846d9d2b26e8db5ad93b7b7c988` (PR-head mitbewegt).

## PR-run am neuen head (Eigenes-Run-Pflicht)

- run `44989324573` (pull_request): **completed SUCCESS**; failed jobs: **0**.
- Ausgeführt+success (14): Workflow policy 137106702250, Trusted Plan 137106702375, Native gate plan 137106702379, Source format 137106702403, Focused Python 137106741658, go-build 137106741669, go-vet 137106741727, Go unit cli-0/1/2/3 137106741710/840/677/713, owner 137106741716, **packages 137106741719**, PR Selected Checks 137107855881. Skipped: 21 (nicht-ausgewaehlte Runtime-/Release-Matrix, wie am alten head 44987822304 gemeldet).

## BEWEIS: die drei Tests am neuen head

- Die drei tests liegen in `internal/metrics/workload_only_source_test.go` (TestWorkloadOnlyRegistersSharedSnapshotOnDeploy, TestServiceAppKeepsRuntimeSourceRegistrationOnDeploy) und `internal/metrics/prometheus_verify_workload_only_test.go` (TestVerifyProviderAndApplicationSourcesSkipsOnlySnapshotMetadata) — gemessen per grep am head `67495fde`.
- Suite-Zuordnung: der packages-shard (job `137106741719`, "PR · Go unit · packages") führt `scripts/pr-go-unit-shard.py --mode packages`, das ALLE Nicht-CLI-Pakete ohne Testfilter laufen laesst (`go test -count=1 <116 pakete>`), also auch `internal/metrics`. Eine separate "internal/metrics"-shard-job existiert in diesem Workflow nicht (die Shard-Jobs der Suite heten cli-0..3/owner/packages); der internal/metrics-Nachweis ist die receipt-Zeile im packages-job:
  - `2026-11-22T05:28:02.3694701Z ok  github.com/mcpdev80/baseharbor/internal/metrics 0.490s` (out of `Running every non-CLI Go package (116), no test filters`, job-log 33,513 bytes)
  - Abschluss-Zeile: `PASS all non-CLI Go package tests`.
  - Damit sind die drei tests am exakten head 67495fde in einem ausgefuehrten, gruenen gehosteten job enthalten; der Runner printet keine per-test-Zeilen (fail-closed汇总), was hier als Belegform gemeldet wird statt eines Ersatzbelegs.

## repo-rule compliance

Keine Produkt-, .github/**- oder scripts/**-Bearbeitung durch diese Lane (nur develop-Inhalte via additive merge); kein rebase/amend/force; kein merge/close/ready; kein GitHub-Kommentar; keine subagenten; keine lokalen test-runs (sha256 d65b09b8ffed) — Beobachtung ausschliesslich ueber gh api + git ls-remote; posten nur an coordinator 9142ab1f.

## cleanliness

cleanliness: nothing started. Eigen pid 2448014. BEFORE `docker ps -a`: 1 entry `a0d40c5bcc8e baha-prunit-db-2286133` (fremde Lane, ~1h alt, nicht angefasst). AFTER: identisch (1 entry). Hopzone `/tmp/opencode/0428-223-hop1714` wird entfernt + `git worktree prune`; scratch `/var/tmp/0428-223` wird vor END geloescht.

END 0428-223-testctx DONE (#1714 new head 67495fde968, back=0, run 44989324573 completed SUCCESS, failed jobs 0, packages-shard job 137106741719 mit internal/metrics-receipt; kein separater metrics-shard-job in dieser Suite — datei:line gemeldet)

## publishing witness

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep perses-valkey-gate-0428-183/hop-develop-1ff16925-w27
evidence/r28-welle5-2026-11-22/perses-valkey-gate-0428-183/hop-develop-1ff16925-w27.md
```
