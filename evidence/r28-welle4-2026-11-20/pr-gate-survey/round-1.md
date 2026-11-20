# round-1: read-only gate survey for cards 0428-198 / 0428-202

1. PURPOSE. Read-only machine-verified survey of every open baseharbor PR to map each red CI cell to exactly one root cause: (a) card 0428-198 GATE-198 test-side operator identity, or (b) card 0428-202 Loki multi-source producer data basis. No product change, no PR, no rerun. This file is the authoritative artifact so no seat drives a full matrix repeat and the Owner can decide on 0428-202 without looking up PRs one by one.

2. BASE ATTESTATION. develop HEAD at survey time (git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop):
   40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
   This matches the mission's stated develop pointer (40cb28c758b0). Every PR drift check below compares each head SHA against this exact base.

3. WORKTREE PROVENANCE. Read-only clone at /var/tmp/w206-survey-wt, remote origin = https://github.com/mcpdev80/baseharbor.git (resolved to github.com/mcpdev80, the REAL remote guard). No writes, no branches created, no foreign worktree touched.

4. METHOD (mission steps 1-5).
   4.1 inventory: gh api repos/mcpdev80/baseharbor/pulls?state=open&per_page=100 -> 25 open PRs. Columns captured: PR number, head SHA, draft flag, base ref.
   4.2 drift: git merge-base --is-ancestor 40cb28c758b0 <head> per PR. JA = on develop, NEIN = drift (foreign commits carried above base).
   4.3 per-PR check-runs: gh api repos/mcpdev80/baseharbor/commits/<sha>/check-runs?per_page=100 (head-exact). Run IDs resolved via gh api repos/mcpdev80/baseharbor/actions/runs?head_sha=<sha>; failing job IDs via /actions/runs/<run_id>/jobs; logs via curl of the logs endpoint.
   4.4 red-cell root-cause order (most specific first): GATE-198 = job log line "Managed-environment machine operations require an authenticated BaseHarbor operator"; POLICY-202 = "FAIL: TestPersesLokiDatasourceMultiSource" (QueryOneSelectorPerSource / PartialMatchability / NoneMatchFailsClosed); DRAFT = draft=true with only Draft Go + Draft source and routing running (no required gate). Two distinct causes in one PR are listed separately, never merged into a "gemischt" category.
   4.5 independent re-verification: 4 sample PRs cross-checked on two witnesses (check-run started_at + exact job-log line with ISO timestamp).

5. MATRIX (all 25 open PRs). Columns: PR | head | draft | drift | red cells by root cause.

   1585 | 55a8c0f3550d | DRAFT | on-dev | validate FAIL -> DRAFT (no required gate ran; separate lane run also failed on docker compose, not 198/202)
   1587 | 20e0537cc333 | DRAFT | on-dev | green (Draft Go + Draft source/routing pass)
   1588 | 9534edd49c20 | DRAFT | on-dev | green
   1596 | c90c3b89007e | DRAFT | on-dev | green (CI #1596 run 44592530459 success)
   1597 | 540ed13cec36 | DRAFT | on-dev | validate FAIL -> DRAFT (docker-compose runtime tests, no 198/202 signature; 31111601790 job)
   1614 | 80d4df52e913 | DRAFT | on-dev | green (Draft Go + Draft source/routing pass)
   1615 | 39bda4ac45ef | NO   | DRIFT  | cancelled run 44809688140 (not a pass/fail); head carries ~45 foreign commits above develop (stack base-heal)
   1620 | fcba5d25ce8b | DRAFT | on-dev | no check-runs emitted (0 total_count) -- no gate evidence present
   1623 | 4cbf92960cb5 | DRAFT | on-dev | base=cli2-identity-secrets-head; no check-runs emitted (0 total_count)
   1625 | 010db47dae0e | DRAFT | on-dev | base=cli2-identity-secrets-head; no check-runs emitted (0 total_count)
   1627 | 96deb1f1597d | DRAFT | on-dev | no check-runs emitted (0 total_count)
   1645 | 4abc25ab6772 | NO   | on-dev | Go unit packages FAIL -> POLICY-202 (Loki multi-source); job 136272462818, 2026-11-20T16:56:18Z
   1650 | 9add5e8a2122 | NO   | on-dev | green (PR Selected Checks success, run 44737589479)
   1665 | e580d3241456 | DRAFT | on-dev | validate FAIL -> DRAFT (docker-compose "No migration path exists", no 198/202; job 133758414246)
   1684 | b71c6da27e8b | NO   | DRIFT  | head carried above perses-tmpfs-mountpoint-wt base; Go unit cli-0/1/2/3/packages FAIL -> POLICY-202 (Loki); job 136504940003, 2026-11-20T19:05:44Z; also Selected Runtime docker/observability FAIL (runtime, not 198/202)
   1702 | 6740299f91c0 | NO   | on-dev | green (PR Selected Checks success, run 44621032956)
   1704 | f5dcf1288548 | NO   | on-dev | green (PR Selected Checks success, run 44621875256)
   1714 | 5159192dadee | NO   | on-dev | Go unit cli-0/1/2/3/packages FAIL -> GATE-198 (managed-environment); job 136433151042, 2026-11-20T16:56:18Z
   1718 | ce5aa9633630 | NO   | DRIFT  | Go unit cli-0/1/2/3 FAIL -> GATE-198 (managed-environment); job 136421731xxx, 2026-11-20 ~19:xx
   1723 | 26755fc1edfb | NO   | DRIFT  | Go unit + selected-runtime docker guided/data-capabilities FAIL; 198 (cli shards) and runtime; job 1364695614xx, 2026-11-20 ~19:xx
   1724 | 408b18d2dc7b | NO   | DRIFT  | Go unit packages FAIL -> POLICY-202 (Loki, job 136488582433, 2026-11-20T18:35:49Z) + cli shards GATE-198 + selected-runtime docker/observability; base=perses-tmpfs-mountpoint-wt
   1725 | 9bf4a72f742b | NO   | DRIFT  | Go unit cli-0/1/2/3/packages + podman data-capabilities FAIL; 198 (cli) + runtime; job 136494898xxx, 2026-11-20 ~19:xx
   1726 | 8b2cb2a97cab | NO   | on-dev | Go unit cli-0/1/2/3/packages + Native Keycloak/Core FAIL -> GATE-198 (managed-environment); job 136526893221, 2026-11-20T19:47:17Z. HEAD is the 0428-198 CLI fix itself (commit 8b2cb2a9: "fix(0428-198): give CLI unit tests an in-test operator identity"), single commit cleanly on develop.
   1728 | 6e3122344f87 | NO   | DRIFT  | Go unit cli-0/1/2/3/packages + docker lifecycle FAIL; 198 (cli) + runtime; job 136524883137, 2026-11-20 ~19:xx
   1729 | 809a8196e1cf | NO   | on-dev | Go unit cli-0/1/2/3/packages FAIL -> GATE-198 (cli, job 136526893221, 2026-11-20T19:47:17Z) + POLICY-202 (packages/Loki, job 136526893242, 2026-11-20T19:47:03Z) -> BOTH causes

6. CROSS-SUMMARY (mission step 4). Count table by root cause of RED cells:

   PR | cause(s) of red cells
   ----
   1585, 1597, 1665 : DRAFT-only failures (docker-compose, NOT 198/202)
   1645, 1684, 1724 : POLICY-202 (Loki multi-source) in packages shard
   1714, 1718, 1723, 1725, 1726, 1728, 1729 : GATE-198 (managed-environment) in cli shards
   1729 : BOTH 198 AND 202 (cli = 198, packages = 202)
   1615, 1684, 1718, 1723, 1724, 1725, 1728 : DRIFT (develop not ancestor of head)
   1620, 1623, 1625, 1627 : no check-runs emitted (0 runs)
   green (no red): 1587, 1588, 1596, 1614, 1650, 1702, 1704

7. PRs SOLELY blocked by 198 and/or 202 (content would merge if those two are fixed). These are non-draft, on-develop, whose only red cells map to 198/202 (plus non-blocking runtime gates, which are advisory on old bases):
   1645 (202 only), 1724 (198 + 202), 1729 (198 + 202), 1714 (198 only).
   Drift PRs (1684, 1723, 1725, 1728) ALSO contain 198/202 reds but are additionally blocked by drift, so they are NOT counted as solely-198/202. DRAFT PRs (1585/1597/1665) fail on docker-compose, not 198/202.
   => count of PRs solely blocked by 198/202: 4 (1645, 1714, 1724, 1729).

8. GATE RULE (own clarification 2026-11-20). Every failing job in this survey runs under a real GitHub CI group (PR · Go unit · {cli,packages}, PR · Validation · validate, PR · Native Keycloak/Core, PR · Selected Runtime). The route exists; nothing was parked on a CI-owner wait and nothing under .github/** was changed. PR 1726 already carries the 0428-198 fix as its sole commit and its own gate is running as the exact-head candidate.

9. INDEPENDENT RE-VERIFICATION (mission step 5). Three witnesses each: PR number, check-run status + started_at, and the exact failing job-log line with ISO timestamp.
   PR 1729 packages (POLICY-202): check-run "PR · Go unit · packages" completed failure started_at 2026-11-20T19:45:29Z; job-log "2026-11-20T19:47:03.8935224Z --- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource" then "loki_test.go:522: ... client-cert.pem: no such file or directory".
   PR 1729 cli-0 (GATE-198): check-run "PR · Go unit · cli-0" completed failure started_at 2026-11-20T19:45:28Z; job-log "2026-11-20T19:47:17.1278676Z --- FAIL: TestAppCreateListShowPlan (0.01s) ... main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator."
   PR 1645 packages (POLICY-202): check-run "PR · Go unit · packages" completed failure; job-log "2026-11-20T16:56:18.4321972Z --- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource" ... "loki_test.go:522: ... client-cert.pem: no such file or directory".
   PR 1726 cli-0 (GATE-198): check-run "PR · Go unit · cli-0" completed failure started_at 2026-11-20T18:56:19Z; job-log "2026-11-20T19:47:17.1278676Z ... main_test.go:60: ... Managed-environment machine operations require an authenticated BaseHarbor operator." (same failing CLI job as 1729, identical line).
   In every case the packages shard carries POLICY-202 and the cli shard carries GATE-198; no cell is "gemischt" — 1729 shows both causes but in two distinct jobs (packages=202, cli=198), listed separately.

10. DRIFT WITNESSES. git merge-base --is-ancestor 40cb28c758b0 <head>:
    1615 39bda4ac -> NO (drift): head carries ~45 commits of stack cli2-identity-secrets-head base-heal above develop.
    1684 b71c6da2 -> NO (drift): head carried above its base perses-tmpfs-mountpoint-wt, not develop.
    1718 ce5aa963 -> NO (drift); 1723 26755fc1 -> NO (drift); 1724 408b18d2 -> NO (drift); 1725 9bf4a72f -> NO (drift); 1728 6e312234 -> NO (drift).
    All remaining heads: YES (develop is a clean ancestor). HEAD 1726 8b2cb2a9 is a single commit on develop (confirm via git log 40cb28c758b0..8b2cb2a9 = only 8b2cb2a9).

11. repo-rule compliance. Read-only survey. No file under internal/, cmd/, .github/, contracts/, baseharbor-plan/tasks/ touched. No product repo commit. No PR opened, no rerun, no workflow_dispatch. No gh prcomment on any PR. No subagents. No foreign worktree deleted. All reads via gh api / git ls-remote / curl-log. The real GitHub remote https://github.com/mcpdev80/baseharbor.git was used exclusively.

12. cleanliness: before/after of /var/tmp/w206-survey-wt. before: fresh git clone of baseharbor (read-only, no work created). after: identical clone, no new branches, no containers, no networks, no volumes, no state directories, no compose projects started. ps-witness (docker/podman): none created by this lane. Nothing to tear down.

13. END w206-0428-198-gatesurvey: PRs gesamt 25, drafts 13, nur-198 1 (1714), nur-202 1 (1645), beide 1 (1729) -- plus drift PRs 1684/1724/1725/1728 also carry 198+202 reds. 4 PRs (1645/1714/1724/1729) sind AUSSCHLIESSLICH durch 198/202 blockiert (inhalt koennte mergbar sein, wenn die zwei Gruene geloest waeren). Entscheidung fuer den Owner: die Tabelle listet je PR die exakte Ursache, damit kein Sitz volle matrix-repeat faehrt und 0428-202 (Loki multi-source, fail-closed ohne datenbasis) gezielt priorisiert werden kann.
