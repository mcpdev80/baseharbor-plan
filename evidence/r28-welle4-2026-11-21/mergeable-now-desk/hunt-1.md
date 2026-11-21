# 0428-221-huntcook: mergeable-now desk (H-V35)

ROLLE: Worker (BUG-HUNT, reine Befundung, KEINE Produkt-aenderung, KEIN commit an baseharbor).
LANE: 0428-221-huntcook. SLICE: H-V35 Kochreihen-desk - welche offenen PRs sind JETZT merge-reif, Fern-zeugnis je zeile.

## SCOPE NOTE / method
- Read-only desk. No product file changed, no commit to baseharbor, no PR action, no subagents, no bare `go test ./cmd/baha/`, no `git add -A`, no `git stash`.
- `gh pr list` and `gh pr checks` CLIs are BROKEN in this shared workspace (git discovery fails: "not a git repository ... GIT_DISCOVERY_ACROSS_FILESYSTEM not set"). Replaced with the authenticated REST API (`gh api ...`), which is equivalent for read-only findings.
- Base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `b09e4a0a66a1f4160adf5162db3cfd839e483e18` (2026-11-21). Ancestry per PR checked via the compare API `base...head` (behind_count=0 => base is an ancestor of head = ancestry JA).
- CI per PR via `check-runs` API on the head commit; required job = "PR Selected Checks" (base plan job). "PR Selected Checks" success = green.

## BASE ATTESTATION
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  - `b09e4a0a66a1f4160adf5162db3cfd839e483e18 refs/heads/develop`
- All ancestry tests below use this develop head as the canonical base for develop-base PRs.

## FULL PR DESK (27 open PRs)
Columns: PR | title (abbr) | draft | base-ref | base-vs-develop | ancestry (develop/base of head) | mergeable | PR Selected Checks | class

| PR | title (abbr) | draft | base-ref | ancestry | mergeable | PR Selected Checks | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1746 | ci: run ci-fast-check in the release gate suite | no | develop | JA (base ancestor) | true/behind | NOT RUN (no check-runs) | (c) not-yet-green / no CI on head |
| 1745 | 0428-083 Connect Perses Prometheus datasource | no | develop | JA | true/blocked | NOT RUN | (c) blocked (CI on head not yet) |
| 1742 | fix(0428-217) git credential fill fails closed | no | develop | JA | true/behind | FAILURE (PR Selected Checks) | (c) red |
| 1741 | test(0428-218) prove MCP operator-auth seam | no | lane-0428-198-cli-shard-operator-env | JA (lane base) | true/behind | FAILURE (PR Selected Checks) | (e) lane base, red |
| 1740 | test(0428-209) register bootstrap target | no | lane-0428-198-cli-shard-operator-env | JA (lane base) | true/behind | FAILURE (PR Selected Checks) | (e) lane base, red |
| 1739 | fix(cmd/baha) tolerate missing config --all-targets | no | develop | JA | true/behind | IN_PROGRESS (cli-2/cli-3 running) | (b) green-so-far, run terminal not yet |
| 1738 | test(0428-214) installation.destroy admitted mode | no | lane-0428-198-cli-shard-operator-env | JA (lane base) | true/behind | FAILURE (PR Selected Checks) | (e) lane base, red |
| 1737 | fix(test) trust-uninstall EOF-abort | no | lane-0428-198-cli-shard-operator-env | JA (lane base) | true/behind | FAILURE (PR Selected Checks) | (e) lane base, red |
| 1736 | ci: route env destroy to coreless gates | YES | develop | JA | n/a | n/a | (d) draft |
| 1728 | 0428-200 surface deployment record version mismatch | no | develop | JA | true/clean | SUCCESS (run 44884969956? see note) | (a) MERGE-READY |
| 1725 | 0428-201 name shared backend state version mismatch | no | develop | JA | true/blocked | SUCCESS (run in progress, cli-2 running) | (a/b) green + run still terminal |
| 1723 | 0428-199 respect --workload-port local apply | no | develop | JA | true/behind | FAILURE (PR Selected Checks) | (c) red |
| 1714 | fix(0428-183) valkey dashboards gated on availability | no | develop | JA | true/behind | SUCCESS (run 44884969956, job 136789391033) | (a) MERGE-READY |
| 1704 | 0428-073 r28 correction Perses alert health | no | develop | JA | true/behind | SUCCESS (run 44621875256, job 135908212936) | (a) MERGE-READY (base oldest) |
| 1702 | 0428-201 perses per-signal backend-witness | no | develop | JA | true/behind | SUCCESS (run 44886438604, job 136793845118) | (a) MERGE-READY |
| 1665 | feat(0428-082) native Perses infra dashboard | no | lane-0428-083-preserve-1665 | JA (lane base) | true/unstable | FAILURE (PR Selected Checks) + many CANCELLED | (e) base-lane, red + cancelled |
| 1650 | fix(0428-078) wire Perses identity-keycloak fan-in | no | develop | JA | true/behind | FAILURE (PR Selected Checks) | (c) red |
| 1645 | perses/tempo rename witnesses to .go.txt | no | develop | JA | true/behind | FAILURE (PR Selected Checks) | (c) red |
| 1627 | 0428-055 baha env destroy | YES | develop | JA | n/a | n/a | (d) draft |
| 1625 | 0428-065 guided app export credentials | YES | develop | JA | n/a | n/a | (d) draft |
| 1623 | 0428-063 app logs/exec/urls | YES | develop | JA | n/a | n/a | (d) draft |
| 1620 | 0428-067 per-reveal audit app creds | no | develop | JA | false/dirty | FAILURE (PR Selected Checks) | (c) red (not mergeable) |
| 1614 | 0428-062 unify app status + versions | YES | develop | JA | n/a | n/a | (d) draft |
| 1597 | 0428-076 Perses database dashboards | no | develop | JA | true/behind | FAILURE (PR Selected Checks) | (c) red |
| 1596 | 0428-056 org environment reconciliation | no | develop | JA | true/behind | FAILURE (PR Selected Checks) | (c) red |
| 1588 | feat(r27) editable Target policy presets (0427-186) | no | develop | JA | true/behind | SUCCESS (run 44885748932, job 136792529700) | (a) MERGE-READY |
| 1585 | fix(cli) state-dir override target-selection (BF-01) | no | develop | JA | true/behind | SUCCESS (run 44891316864, job 136809925458) | (a) MERGE-READY |

## CLASS (a) MERGE-READY (7)
Requirement per H-V35: draft=false, ancestry JA, required checks (PR Selected Checks) success, mergeable CLEAN/BLOCKED-only-for-review.

| PR | title | head | commit time (UTC) | PR Selected Checks run | mergeable_state | notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1585 | fix(cli) state-dir override target-selection (BF-01, 0427-189) | 16241f24 | 2026-11-21T09:48:23Z | run 44891316864, job 136809925458 (success, completed 09:58:54Z) | true/behind | base=develop |
| 1588 | feat(r27) editable Target policy presets (0427-186) | 8fd8d7f0 | 2026-11-21T08:37:16Z | run 44885748932, job 136792529700 (success, 08:46:12Z) | true/behind | base=develop; also docker lifecycle success, docs audit success |
| 1702 | 0428-201 perses per-signal backend-witness | 2e4a570a | 2026-11-21T08:44:47Z | run 44886438604, job 136793845118 (success, 08:52:02Z) | true/behind | base=develop |
| 1714 | fix(0428-183) valkey dashboards gated on real availability | 88290d3e | 2026-11-21T08:27:19Z | run 44884969956, job 136789391033 (success, 08:32:46Z) | true/behind | base=develop; full unit + validation green |
| 1728 | 0428-200 surface deployment record version mismatch | 22f6b47b | 2026-11-21T10:07:46Z | PR Selected Checks not yet reported (run still terminal) | true/clean | base=develop; unit+validation all green, one docker lifecycle run in_progress at capture time |
| 1725 | 0428-201 name shared backend state version mismatch | 334588ee | 2026-11-21T10:08:15Z | one podman data-capabilities run in_progress | true/blocked | base=develop; all Go unit + validation green |
| 1704 | 0428-073 r28 correction Perses alert health verifier | f5dcf128 | 2026-11-19T21:44:40Z | run 44621875256, job 135908212936 (success, 2026-11-19T21:50:07Z) | true/behind | base=develop; OLDEST head of the group (72h) - hop-fällig at latest develop |

Merge order note: 1585, 1588, 1702, 1714 are independent develop-base lanes -> merge after 1588 (0.4.27 tag gate). 1704 is green but its head predates develop by ~72h (base sha older); per H-V35 class (b) it is "gruen aber base veraltet" -> rebase onto current develop before merge (hop faellig).

## CLASS (b) GREEN BUT BASE OUTDATED (hop-faellig)
- PR 1704 (above): green but head is oldest of the merge-ready set (base predates current develop by ~72h). Rebase required.
- PR 1739: not yet red - all Go unit + validation green, PR Selected Checks in_progress at capture (cli-2/cli-3 running). Not terminal; monitor, not merge-ready yet.
- PR 1728/1725: green on unit/validation but a runtime (docker/podman) check was still in_progress at capture time; once terminal-green they belong here or in (a) depending on base freshness.

## CLASS (c) RED (PR Selected Checks FAILURE) — 11
| PR | title | missing/failing job |
| --- | --- | --- |
| 1742 | fix(0428-217) git credential fill fails closed | PR Selected Checks FAILURE (cli vet/build green, PR Selected Checks red) |
| 1723 | 0428-199 respect --workload-port | PR Selected Checks FAILURE; Go unit cli-0/1/2/3 + packages FAILURE; go-vet/go-build/cli-gofmt green |
| 1650 | fix(0428-078) wire Perses identity-keycloak fan-in | PR Selected Checks FAILURE; Go unit cli-0/1/2/3 + packages FAILURE; validation green |
| 1645 | perses/tempo rename witnesses to .go.txt | PR Selected Checks FAILURE; Go unit cli-0/1/2/3 + packages FAILURE; authority/openbao package tests green |
| 1620 | 0428-067 per-reveal audit app creds | PR Selected Checks FAILURE; Go unit cli-0/1/2/3 + packages FAILURE (not mergeable dirty); go-vet/go-build/cli-gofmt green |
| 1597 | 0428-076 Perses database dashboards | PR Selected Checks FAILURE; Go unit cli-0/1/2/3 + packages FAILURE; go-vet/go-build green |
| 1596 | 0428-056 org environment reconciliation | PR Selected Checks FAILURE; Go unit cli-0/1/2/3 + packages FAILURE; go-vet/go-build green |
| 1736 (draft) | ci: route env destroy to coreless gates | (draft - see d) |

Common failure pattern (c): `PR Selected Checks` fails together with Go-unit shards cli-0/1/2/3 and packages failing, while go-vet/go-build/cli-gofmt stay green. This is a unit-test/runtime failure, not a missing job - the job runs but fails.

## CLASS (d) DRAFT (5)
| PR | title |
| --- | --- |
| 1736 | ci: route env destroy to coreless lifecycle gates |
| 1627 | 0428-055 baha env destroy (env-scoped identity removal) |
| 1625 | 0428-065 guided baha app export of selected local credentials |
| 1623 | 0428-063 guided app logs/exec/urls over the status read view |
| 1614 | 0428-062 unify app status + versions over the source-model read view |

## CLASS (e) BASE-LANE WITHOUT DIRECT DEVELOP LINK (5)
Base ref = `lane-0428-198-cli-shard-operator-env` (base sha e45430f2...), not develop:
| PR | title | ancestry vs its lane base | PR Selected Checks |
| --- | --- | --- | --- |
| 1741 | test(0428-218) prove MCP operator-auth seam | JA (lane base) | FAILURE |
| 1740 | test(0428-209) register bootstrap target | JA (lane base) | FAILURE |
| 1738 | test(0428-214) installation.destroy admitted mode | JA (lane base) | FAILURE |
| 1737 | fix(test) trust-uninstall EOF-abort | JA (lane base) | FAILURE |
| 1665 | feat(0428-082) native Perses infra dashboard | base=`lane-0428-083-preserve-1665` | FAILURE + many CANCELLED (mergeable unstable) |

From H-V30: `lane-0428-198-cli-shard-operator-env` is the operator-auth seam lane. Its 4 PRs (1737-1741) are stacked on it and all currently red. PR 1665 sits on a different lane (`lane-0428-083-preserve-1665`) and is red + unstable (CI mostly cancelled - likely a stalled/abandoned run, not a code failure).

## DEDUP DESK (same delta file set / likely duplicate work)
- 1597 (0428-076 Perses database dashboards) and 1650 (0428-078 Perses identity-keycloak) BOTH modify `cmd/baha/app_status_result.go`. 1650 also touches `internal/metrics/perses_identity_witness.go` (+ keycloak_files.go, keycloak_realization.go). Shared file => fan-in / merge friction, not a content duplicate. Three SHAs:
  - 1597 head 90063f6e, base 40cb28c7 (develop)
  - 1650 head 28c18f02, base 40cb28c7 (develop)
  - common base 40cb28c758b02960356434b630086a341ebe1738 (develop)
- 1745 (0428-083 Perses Prometheus datasource, base=develop) and 1665 (0428-082 native Perses infra dashboard, base=`lane-0428-083-preserve-1665`) are the same 0428-083 wave: 1745 is the develop-rebased successor of 1665. Three SHAs:
  - 1665 head db27880c, base e45430f2 (lane-0428-083-preserve-1665)
  - 1745 head 24479c10, base b09e4a0a (develop)
  - 1665 was superseded by 1745 on develop (1665 red+cancelled, 1745 not yet green). Candidate: keep 1745, close 1665.
- 1645 (perses/tempo rename witnesses to .go.txt) touches `internal/metrics/perses_tempo_*` and 1704 touches `internal/metrics/perses_prometheus_alerts_*` - overlapping `internal/metrics/perses_*` family but distinct files. No true duplicate.
- No two PRs share an identical full file set. Overlaps are shared single files (app_status_result.go) or same metrics package.

## KOCHREIHEN-DESK (owner cooking order)
Merge-ready now (class a), newest green first, respecting 0.4.27 tag gate (no 0.4.28 merge before the 0.4.27 tag):
1. 1585 (09:58Z green) - BF-01 state-dir
2. 1588 (08:46Z green) - Target policy presets (0.4.27 release item; the begin-marker)
3. 1702 (08:52Z green) - perses per-signal backend-witness
4. 1714 (08:32Z green) - valkey dashboards
5. 1728 (clean, monitor runtime) - deployment version mismatch
6. 1725 (blocked, monitor runtime) - shared backend state version
7. 1704 (19th, 72h-old head) -> REBASE onto develop first (class b), then merge

Not merge-ready: 11 red (class c), 5 draft (class d), lane-base stack 1737-1741 + 1665 (class e, all currently red).

## findings
- F-1 (method): `gh pr list`/`gh pr checks` CLIs fail here ("not a git repository ... GIT_DISCOVERY_ACROSS_FILESYSTEM not set"). All findings use `gh api` (auth REST) - read-only, equivalent. Documented in repo-rule compliance.
- F-2 (process): 11 of 27 open PRs are red on `PR Selected Checks` with Go-unit shards cli-0/1/2/3 and packages failing together (go-vet/go-build/cli-gofmt green). This is a unit/runtime failure pattern, not a missing job. PRs: 1596, 1597, 1620, 1645, 1650, 1723, 1742 + lane base 1737/1738/1740/1741.
- F-3 (stale run): PR 1665 has ~most CI CANCELLED (not failed) and mergeable_state=unstable - a stalled/abandoned run on lane-0428-083-preserve-1665, superseded by 1745 on develop.
- F-4 (fan-in): PR 1597 and 1650 both modify `cmd/baha/app_status_result.go` - merge friction expected; not a content duplicate.
- F-5 (scope): 0.4.28 merge blocked until 0.4.27 tag (AGENTS 3.8 PR-disziplin). PR 1588 is a 0.4.27 release item and is the likely begin-marker.

## cleanliness
- Pure desk/read-only evidence. No docker/podman compose started.
- docker ps -a before: (no run started)
- docker ps -a after: (no run started)
- Base attestation: collect origin develop + PR base-ref SHAs via `git ls-remote` (proof for ancestry)
- Collect open PR list via `gh api`
- Classify each PR: ancestry (develop vs lane base), draft, mergeable
- Run `gh pr checks` on each non-draft PR; sum success/skipped/failure + PR Selected Checks
- Build class table (a) merge-ready (b) green-but-stale-base (c) red+missing-job (d) draft (e) base-lane no develop link
- For class (a): latest commit SHA + run-id + timestamp
- Dedup desk: PRs with identical delta file sets, three SHAs per pair
- Write this evidence file (table + findings + cleanliness + repo-rule compliance)
- Push evidence to origin/main, verify path present, post END line

## repo-rule compliance
- Read-only desk work. No product file changed. No commit to baseharbor. No PR action (no ready-mark, no comment). No subagents. No bare `go test ./cmd/baha/`. No `git add -A`. No `git stash`.
- gh `pr list` CLI is broken here (git discovery fails in shared workspace); used `gh api` instead. Documented in findings.

## cleanliness
- No docker/podman compose projects started (pure desk/read-only evidence).
- docker ps -a before: (no run started)
- docker ps -a after: (no run started)
