# 0428-248 broker-diag round-2 — #1778 compleet: 3 paden cataloged (A-reeks + 2 × #1723)

Lane 0428-223-testctx, sitz b90e4ba1. Opdracht: #1778 (branch
lane-0428-248-broker-diag-mapping) MAKEFULL — de twee #1723-paden ontbraken nog,
#1723 faalde verder op Trusted Plan.

eintraege A broker-diag + app_workload_ports + regression-test = 3 pfade, dup-frei, surfaces ok

trusted-planner #1763 und #1723 cataloged: ja

## PLAN

1. (done) Realiteit: origin=github URLs; ls-remote develop=`68b26bd78c3de89e11252e6d04a8d3ed16c804a7`;
   branch-head en pull/1778/head = `5d9bd262…` (round-1 state); #1778 OPEN draft;
   beide #1723-bestanden: `cmd/baha/app_workload_ports.go` bestaat AL op develop,
   `cmd/baha/workload_port_local_regression_test.go` alleen op #1723 head
   `9355afe1` (ls-tree via pull/1723 fetch) — entry is correct in beide
   merge-volgordes; géén van beide was cataloged op 68b26bd7; docker ps -a before=0,
   eigen pid 511456.
2. (done) Branch up-to-date: `merge-base --is-ancestor 68b26bd7 HEAD` OK → geen
   merge nodig;alleen additive commits, geen force/amend.
3. (done) scripts/pr-gate-coverage.json + TWO entries im #1768/#1777 muster:
   - `source.cmd.baha.app.workload.ports.go` / cmd/baha/app_workload_ports.go
   - `source.cmd.baha.workload.port.local.regression.test.go` /
     cmd/baha/workload_port_local_regression_test.go
   surfaces = alleen de BESTAANDE source.gate.atomic docker+podman
   data.capabilities (geen nieuwe surface), runtime_specific true, en beide in
   source_components van native/docker/data-capabilities +
   native/podman/data-capabilities (3 nieuwe bronnen in elke check: broker-diag,
   ports, regression-test). Dup-census: id's en paths uniek (200 components, 0 dups).
4. (done) scripts/test_pr_native_gate_plan.py: regression
   `test_workload_port_sources_select_both_data_capabilities_gates` (subTest over
   BEIDE nieuwe paden; assert = native docker+podman matrix). CI-home van deze
   test: `PR · Focused Python` (jobs roepen scripts/test_pr_native_gate_plan.py
   aan, ci.yml:1223, trigger pull_request→develop, draft en ready) — hosted
   uitgevoerd op deze head (job 137255955252 success, "Ran 20 tests OK"). Lokaal:
   suites 253 OK; validate "PR gate coverage catalog is valid";
   pr-native-gate-plan per pad → `{"include":[native/docker/data-capabilities,
   native/podman/data-capabilities]}`; guardian voor alle DRIE paden zonder
   uncataloged-abort (pr-gate-plan sim aangetoond: 0 aborts).
5. (done) ONE additive commit `1f87c2c5ae901073ca380ed90cb06f06e1af022f` bovenop
   round-1 commit `5d9bd262` (git log origin/develop..HEAD = exact deze TWO eigen
   commits), ci-fast-check rc=0, normal push → PR #1778; ls-remote head+pull beide
   `1f87c2c5…`; daarna PR van draft naar READY gepromoveerd (door missie
   bevolen; geen commentaar/marge).
6. (done) Exact hosted normal run **45037984802** @1f87c2c5: terminal
   completed/**success**, failed=0, skipped=21 (runtime/native cells — correct:
   deze PR raakt GEEN product sources, dus de native data-capabilities cells
   hoeven hier niet te draaien; het bewijs dat de MAPPINGS werken is de planner
   + de Focused Python suite, allebei EXECUTED success):
   - PR · Trusted Plan 137255887316 success
   - PR · Validation · pr-planner-tests 137255955271 success
   - PR · Focused Python 137255955252 success (bevat test_pr_native_gate_plan.py
     met de nieuwe asserts — log 'Ran 20 tests ... OK')
   - PR · Native gate plan 137255887189 success; PR Selected Checks 137256373135
     success; Workflow policy 137255887137 success; ci-executor/receipt/ci-policy
     validations success.
   → 'trusted-planner #1763 und #1723 cataloged: ja' (beide PR-paden lossen op in
   de trusted planner; #1763/#1723 zelf hoeven niet te wachten op hun eigen
   native cellen — hun bronnen zijn nu resolved).
7. (done) Akte + ls-tree-witness op plan origin/main.
8. (done) Cleanliness + END.

## Provenance

- base attestation: ls-remote develop = `68b26bd78c3de89e11252e6d04a8d3ed16c804a7`;
  branch (round-1) was daar al op gesneden; `merge-base --is-ancestor 68b26bd7 HEAD`
  OK op beide commits.
- `git log --oneline origin/develop..HEAD` = exact twee eigen commits:
  `1f87c2c5 ci(0428-248): catalog the two #1723 workload-port files in the
  data-capabilities module` en `5d9bd262 ci(0428-248): catalog
  cmd/baha/app_broker_diagnostics_test.go in the data-capabilities module`.
- diff 68b26bd7...HEAD --name-only = `scripts/pr-gate-coverage.json`,
  `scripts/test_pr_native_gate_plan.py`.
- delivery: ls-remote refs/heads/lane-0428-248-broker-diag-mapping en
  refs/pull/1778/head beide = `1f87c2c5ae901073ca380ed90cb06f06e1af022f`
  (vóór de push: beide `5d9bd262…`, bewezen ontlekking).
- planning-repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
  remote -v` → https://github.com/mcpdev80/baseharbor-plan.git.

## repo-rule compliance

- Write-set: alleen de catalog JSON + test_pr_native_gate_plan.py (missie stap 3-4);
  round-1 akte bestand ongewijzigd; GEEN .github, geen operatorauth, geen
  237/ci-native-pr-gate.sh; additive commits (geen force/amend); geen merge, geen
  commentaar; geen subagenten; geen containers op deze host.

## cleanliness

cleanliness: `docker ps -a` BEFORE = 0 entries (pid 511456), AFTER = 0 entries
(pid van de END-shell). Geen compose/container gestart op deze host. Eigen scratch
under /var/tmp/0428-223-* (changed-paths, sim diff, job-logs) wordt vóór END
verwijderd. Werkboom workers/0428-248-brokerdiag-wt houdt de kandidaat (0 delta
na commit).

END 0428-223-testctx DONE — 0428-248 broker-diag round-2: branch lane-0428-248-broker-diag-mapping, head 1f87c2c5ae901073ca380ed90cb06f06e1af022f (TWO additive commits op develop 68b26bd7, geen force/amend), PR #1778 class READY (promotie door missie bevolen), exact hosted run 45037984802 completed/success failed=0 met Trusted Plan 137255887316 + Validation pr-planner-tests 137255955271 + Focused Python 137255955252 EXECUTED success, trusted-planner #1763 und #1723 cataloged: ja, cleanliness: besenrein
