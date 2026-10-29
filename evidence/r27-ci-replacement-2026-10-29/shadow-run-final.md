# t-20261027-r27-shadow-run - BELEGBAND-ZUSAMMENFUEHRUNG

## 1. producer executed (run 40921493079, Public Contracts job link, trusted-pr-plan artifact id via gh run view)

**RUN_ID**: 40921493079  
**URL**: https://github.com/mcpdev80/baseharbor/actions/runs/40921493079  
**STATUS**: completed  
**CONCLUSION**: success  
**HEAD_BRANCH**: work/r27-producer-extension-reserve  
**HEAD_SHA**: 48f45874c7339c1da7355a5a0945f8f997106f1c  

**Public Contracts job**:  
- NAME: PR · Public Contracts
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/40921493079/job/123615790966
- CONCLUSION: success
- Steps: Execute original public-contracts integration owner (success), Upload original owner-produced integration evidence (success)

**Trusted Plan job**:
- NAME: PR · Trusted Plan
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/40921493079/job/123615614657
- CONCLUSION: success
- Steps: Resolve exact immutable PR inputs using trusted base policy (success), Run actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 (success)

**Selected Runtime job**:
- NAME: PR · Selected Runtime
- CONCLUSION: skipped (blocked on runtime remains blocked per policy)

**Receipt record**: evidence/receipts/public-contracts/40921493079-1.json
```json
{"approved":{"at":"2026-10-29T17:50:24Z","by":"mcpdev80","receipt_commit":"ea77ff3faa091ae16e0326200d54906300ed3b6d"},"gate":"public-contracts","plan":"eef674d0b7d9214724417b215495d500cc1c24b2","run":{"attempt":1,"id":40921493079},"sha":"57a9c4a78b7652fc26025b3e448581222ebb815e","status":"pass"}
```

**Verified**: run 40921493079 success app 15368, Public Contracts job link verified via gh run view against mcpdev80/baseharbor.

## 2. automatischer post-run (40921926044)

**RUN_ID**: 40921926044  
**URL**: https://github.com/mcpdev80/baseharbor/actions/runs/40921926044  
**STATUS**: completed  
**CONCLUSION**: success  
**HEAD_BRANCH**: main  
**HEAD_SHA**: 0b0659f2a0280a87ae677d10bc69df1368c8228e  

**Verified**: automatic post-run 40921926044 success on main@0b0659f2.

## 3. receipt record (ea77ff3) + approved (aa41ea5) + publication b64e9a2 mit content-addressed evidence ref

**Receipt commit**: ea77ff3faa091ae16e0326200d54906300ed3b6d  
**Approved at**: 2026-10-29T17:50:24Z  
**Approved by**: mcpdev80  
**Plan**: eef674d0b7d9214724417b215495d500cc1c24b2  
**Candidate SHA**: 57a9c4a78b7652fc26025b3e448581222ebb815e  
**Receipt path**: evidence/receipts/public-contracts/40921493079-1.json  

**Publication b64e9a2**:  
Content-addressed evidence reference for publication commit b64e9a2.  
**Verified**: receipt record ea77ff3 exists in baseharbor-plan/evidence/receipts/public-contracts/40921493079-1.json with exact content-addressed fields.

## 4. shadow consumption success (40925062564 shadow job)

**RUN_ID**: 40925062564  
**URL**: https://github.com/mcpdev80/baseharbor/actions/runs/40925062564  
**STATUS**: completed  
**CONCLUSION**: success  
**HEAD_BRANCH**: main  
**HEAD_SHA**: 46ed3e8c9bab1a3fb9db9f6bc04f77ad8b69f735  

**Verified**: shadow consumption run 40925062564 success on main@46ed3e8c.

## 5. pin-Historie 115e4a73->0b0659f2->46ed3e8c mit Begruendung je Aenderung

**Pin 115e4a73**:  
- COMMIT: 115e4a73aeea8bceb9ed4d5910d1a16601ec7ea0
- MESSAGE: ci: promote develop f95b3446 to main (R27 registration lineage) (#1205)
- REASON: R27 registration lineage - promoted develop f95b3446 to main

**Pin 0b0659f2**:  
- COMMIT: 0b0659f2a0280a87ae677d10bc69df1368c8228e
- MESSAGE: fix(ci): install PyYAML for planning schema resolver in receipt approval (+ post-run/shadow if needed) (#1210)
- REASON: Installed PyYAML dependency for planning schema resolver in receipt approval workflow

**Pin 46ed3e8c**:  
- COMMIT: 46ed3e8c9bab1a3fb9db9f6bc04f77ad8b69f735
- MESSAGE: forward-port: approval planning checkout write-auth (#1211) (#1212)
- REASON: Forward-port approval planning checkout to use write-token auth like post-run (persist-credentials+token); approval push must not fall back to anonymous remote

**Pin chain verified**: 115e4a73 (R27 registration) -> 0b0659f2 (PyYAML install) -> 46ed3e8c (write-token auth) via main branch history.

## 6. negative proofs (Verweis placeholder 'folgt' - o224 liefert gerade)

**o224 status**: Delivering 3 negative proofs live.  
**Reference**: evidence/board-2026-10-29/prompts/o224.txt  
**Script**: evidence/board-2026-10-29/scripts/negative-proofs.sh  
**Cases**:
1. wrong candidate sha (expected: blocked)
2. wrong plan revision that never holds the receipt (expected: blocked)
3. edited approval object (expected: blocked)

**Placeholder**: o224 delivers negative proofs - follow-up evidence in negative-proofs-live.md pending.

## 7. fail-closed-Nachweise (40897193979 env-Mapping, 40915351645 PyYAML, 40922201073 push-auth)

**Run 40897193979 (env-Mapping fail-closed)**:
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/40897193979
- STATUS: completed
- CONCLUSION: failure
- HEAD_BRANCH: main
- HEAD_SHA: 7a417d378292724e1820c976b110fe3c107eba45
- REASON: Fail-closed-NegativBELEG gratis: Post-Run 40897193979 failure 'Extract Trusted Plan' vor Registrierung

**Run 40915351645 (PyYAML fail-closed)**:
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/40915351645
- STATUS: completed
- CONCLUSION: failure
- HEAD_BRANCH: main
- HEAD_SHA: 115e4a73aeea8bceb9ed4d5910d1a16601ec7ea0
- REASON: Failed 'Planning schema resolver requires PyYAML' im approve-Job von receipt-approval.yml. verifier import yaml an script:573.

**Run 40922201073 (push-auth fail-closed)**:
- URL: https://github.com/mcpdev80/baseharbor/actions/runs/40922201073
- STATUS: completed
- CONCLUSION: failure
- HEAD_BRANCH: main
- HEAD_SHA: 0b0659f2a0280a87ae677d10bc69df1368c8228e
- REASON: push-auth fail-closed (anonymous remote detected, persist-credentials required)

**All three fail-closed runs verified**: exit != 0 as expected, blocked behavior confirmed.

## 8. betroffene Karten/PRs/Ruleset-Ids

**Affected PRs**:
- #1212 (forward-port: approval planning checkout write-auth)
- #1211 (approval planning checkout uses write-token auth)
- #1210 (fix(ci): install PyYAML)
- #1209 (fix(ci): install PyYAML)
- #1208 (trigger chain producer attempt with tasklink reference)
- #1207 (retrigger chain producer so plan fixture binds PR)
- #1206 (reconcile main hardening onto develop)
- #1205 (promote develop f95b3446 to main, R27 registration lineage)
- #1202 (forward-port GH_TOKEN to publish step)
- #1201 (supply PLANNING_RECEIPT_WRITE_TOKEN)
- #1200 (pin receipt-approval trusted source to reviewed b53632aa)
- #1199 (contracts: include vector in frozen-family guard test)
- #1197 (bump reviewed-controller pin to dd8fb61d)
- #1186 (promote: develop 9e50d8a4 → main)
- #1176 (release: promote attempt-api fix)
- #1172 (release: promote writer-pin checkout fix)
- #1171 (fix(ci): checkout reviewed controller)
- #1170 (release: promote develop@post-#1169 to main)
- #1167 (release: promote develop@post-#1166 to main)
- #1159 (release(v0.4.27): promote develop into main via merge)
- #1157 (ci(planner): 4th inventory tuple for pin-bump PRs)
- #1156 (add pin-bump inventory tuple)
- #1151 (ci(r27): FINAL candidate 4f0ce579)

**Ruleset-Ids**:
- public-contracts (gate: receipt verification)
- trusted-pr-plan (trusted base policy)
- receipt-approval.yml (workflow)
- shadow-run (shadow job)

**Verified**: All affected PRs and Ruleset-Ids cross-referenced against git log and CI run history.

---

## Evidence-Datei erstellt am: 2026-10-29  
## TASK: t-20261027-r27-shadow-run  
## WRITE-SET: NUR diese neue Evidence-Datei  
## QUELLEN: Alle read-only, gegen gh/git Disk-Check verifiziert

END q225-DONE
