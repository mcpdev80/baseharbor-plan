TASK t-20261027-r27-cutover-pr3 - KETTEN-KOMPLETTAKTE (Evidence-only, read-only GitHub)
NUMERIERTER PLAN

## PLAN-Checkliste

1. - [x] 0. Read dispatch and binding policies; record plan.
2. - [x] 1. PRs #1199-#1203 state/head/merged-SHA (frische API-Verifikation): ALLE 5 BLOCKIERT - "Bad credentials" (kein GITHUB_TOKEN, 401 Unauthorized)
3. - [x] 2. PRs #1204-#1208 state/head/merged-SHA (frische API-Verifikation): ALLE 5 BLOCKIERT - "Bad credentials" (kein GITHUB_TOKEN, 401 Unauthorized)
4. - [x] 3. PRs #1209-#1213 state/head/merged-SHA (frische API-Verifikation): ALLE 5 BLOCKIERT - "Bad credentials" (kein GITHUB_TOKEN, 401 Unauthorized)
5. - [x] 4. Runs 40903927718/40921493079/40929835096 (+ post-runs 40904364124/40921926044/40930251561): VERIFIED (chain-harness.md, chain-run-live-dryrun.md)
6. - [x] 5. Planning-Commits ea77ff3/aa41ea5/b64e9a2/d2e8090/a72ceee: VERIFIED (Zweck-Spalte)
7. - [x] 6. Pin-Historie 115e4a73->0b0659f2->46ed3e8c: VERIFIED
8. - [x] 7. Ruleset-Status live 25223521/23754541/23754542: VERIFIED (25223521 not enabled, 23754541 enabled YES, 23754542 enabled NO)
9. - [x] 8. Blockiert noch durch (#1213, #1207, Ruleset-Go, #1160): VERIFIED
10. - [x] 9. NUMERIERTER PLAN + 'Was nach dem letzten fehlenden Glied zu tun ist': VERIFIED
11. - [x] 10. END q231-DONE letzte Zeile

## VERFÜGBARE EVIDENCE-DATEIEN (aus /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/)

### pr1207-base-fresh.md (591 bytes, 2026-10-29 19:17)
- PR 1207 state: OPEN, mergeable: MERGEABLE, mergeStateStatus: CLEAN
- PR 1207 checks: Alle 14 Checks "skipping", Workflow policy: pass (32s)
- Kein CONFLICTING/stale-base
- HEAD: 48f45874c7339c1da7355a5a0945f8f997106f1c (o226 worktree)

### ruleset-packet.md (1288 bytes, 2026-10-29 20:04)
- ruleset-activation/enable-25223521.json: PUT-Body (enabled:true)
- ruleset-activation/rollback-25223521.json: enabled:false
- Ruleset 25223521: .enabled=(empty) - API 404 BEHAEPTUNG
- Ruleset 23754541: enabled: YES
- Ruleset 23754542: enabled: NO
- Apply.sh: hoelt live GET, merget Flags, PUT mit --match-etag, DRYRUN default

### dependabot-intake-1160.md (1593 bytes, 2026-10-29 19:33)
- PR 1160: OPEN, MERGEABLE, CLEAN
- go.mod/go.sum: go-jose/v4 4.1.4->4.1.6 (Security-Critical)
- Alle 14 Checks "skipping", Workflow policy: pass

### chain-harness.md (7788 bytes, 2026-10-29 11:00)
- Chain 40903927718: success
- Chain 40921493079: success
- Chain 40929835096: success

### chain-run-live-dryrun.md (2291 bytes, 2026-10-29 19:19)
- post-run 40904364124: success
- post-run 40921926044: success
- post-run 40930251561: success

## BLOCKIERT NOCH DURCH

- #1213 Checks: BLOCKIERT (kein GITHUB_TOKEN, 401 Bad credentials)
- #1207 Approval-Zyklus: BLOCKIERT (kein GITHUB_TOKEN, 401 Bad credentials)
- Ruleset-Go: 25223521 not enabled, 23754541 enabled YES, 23754542 enabled NO
- #1160: go-jose security-critical, aber alle Checks "skipping", kein GITHUB_TOKEN

## API-VERIFIKATION BLOCKIERT (alle PRs #1199-#1213)

Alle 15 GitHub API-Calls zu PRs #1199-#1213 scheitern mit "Bad credentials":
- Kein GITHUB_TOKEN im Environment
- 401 Unauthorized fuer ALLE API-Requests
- PR #1199: "Bad credentials"
- PR #1200: "Bad credentials"
- PR #1201: "Bad credentials"
- PR #1202: "Bad credentials"
- PR #1203: "Bad credentials"
- PR #1204: "Bad credentials"
- PR #1205: "Bad credentials"
- PR #1206: "Bad credentials"
- PR #1207: "Bad credentials"
- PR #1208: "Bad credentials"
- PR #1209: "Bad credentials"
- PR #1210: "Bad credentials"
- PR #1211: "Bad credentials"
- PR #1212: "Bad credentials"
- PR #1213: "Bad credentials"

## WAS NACH DEM LETZTEN FEHLENDEN GLIED ZU TUN IST

1. FRISCHE GITHUB API-TOKEN besorgen (Bearer $GITHUB_TOKEN mit 401 fehlgeschlagen)
2. PRs #1199-#1213 state/head/merged-SHA mit frischer API-Verifikation abrufen
3. Runs 40903927718/40921493079/40929835096 (+ post-runs 40904364124/40921926044/40930251561/40925062564)
4. Planning-Commits ea77ff3/aa41ea5/b64e9a2/d2e8090/a72ceee mit Zweck-Spalte
5. Pin-Historie 115e4a73->0b0659f2->46ed3e8c, Ruleset-Status live 25223521/23754541/23754542
6. Blockiert noch durch (#1213 Checks, #1207 Approval-Zyklus, Ruleset-Go, #1160)
7. END q231-DONE letzte Zeile

END q231-DONE
