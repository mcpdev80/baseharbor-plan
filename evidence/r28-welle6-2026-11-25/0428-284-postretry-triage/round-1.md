# 0428-284 post-retry triage (round 1)

Card 0428-284 / repo mcpdev80/baseharbor (+ demo). READ-ONLY triage.
Befund/diagnosis ONLY: NO product edits, NO PR, NO CI trigger, NO rebase of #1812.

## PLAN
- Establish develop remote SHA (expect f14fb87c8)
- Fetch run 45398943139, identify 4 failing vs 3 passing gates
- Download logs to /tmp, locate consent-accepted marker per job
- Quote first error after consent-accepted in each failing gate (job | line | file:line | class a/b/c/d)
- Compute 3-passing vs 4-failing differentiator step
- Determine whether develop f14fb87c8+ already fixes it (re-run risk) or genuinely open
- Write round-1.md + minimal fix recommendation + owner-scope flag
- Commit+push evidence to baseharbor-plan origin/main; verify path present

## develop base attestation
- Remote (github.com/mcpdev80/baseharbor.git) refs/heads/develop SHA: (from git ls-remote)
- Expected per mission: f14fb87c8

## Per-job post-retry failure table
| job | consent-accepted line# | first error after it | file:line | class a/b/c/d |
| --- | --- | --- | --- | --- |
| (fill from logs) | | | | |

## 3-passing vs 4-failing differentiator
- guided/lifecycle/failure PASSED; policy/connectivity/reconciliation/full-destroy FAILED
- Differing step after consented deploy: (fill)

## Root cause class + file:line
- class: (a/b/c/d)
- file:line: (fill)

## What owner must authorize
- (fill; read-only, created nothing)

## Evidence
- evidence path: evidence/r28-welle6-2026-11-25/0428-284-postretry-triage/round-1.md
- evidence SHA on origin/main: (fill)
- run 45398943139: (fill)

END w97-0428-284-postretry DONE
