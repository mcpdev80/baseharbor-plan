PLAN q227 - chain-run.sh DRYRUN gegen echte Kette - CHAIN-RUN DRYRUN GEGEN ECHTE KETTE

1. Script parameter-fixen (IDs/URLs/Pfade aktualisieren, Trennung der Pin-Namen):
   - chain-run.sh nimmt RUN_ID=40921493079 und ATTEMPT=1
   - GITHUB_REF, GITHUB_REF_TYPE, HEAD_REF envs wurden gegen main-Ref-Guards geprüft
   - PIN_PLANNING_MAIN vs PIN_PRODUCT_MAIN: Variablennamen im Script klar getrennt
   - gh api ruft run 40921493079 gegen mcpdev80/baseharbor
   - jq extrahiert integration_sha, base_sha, head_sha aus trusted-pr-plan artifact
   - PR-Auflösung: explicit --pr-number -> run object pull_requests -> commit PRs

2. DRYRUN komplett durchlaufen lassen (gh api nur lesend, keine dispatches), Ausgabe in Evidence:
   - WORKTREE: detached HEAD e0de0117 auf origin/develop
   - HEAD SHA: 48f45874c7339c1da7355a5a0945f8f997106f1c
   - PLAN-JSON: /home/marcel/tmp-ops/o204/art-40921493079/pr-plan.json
   - integration_sha: 57a9c4a78b7652fc26025b3e448581222ebb815e
   - base_sha: 676edc0a9b3589adad5c6b4490e8a4eb938ae247
   - workflow_id: 352609139
   - pr_number: 1207
   - tasklink: auto-resolved task from PR 1207: tasks/t-20261029-r27-ci-producer.md
   - receipt_tasklink.py: rc=0, output:
     {"base_sha":"676edc0a9b3589adad5c6b4490e8a4eb938ae247","candidate_sha":"57a9c4a78b7652fc26025b3e448581222ebb815e","gate":"public-contracts","head_sha":"48f45874c7339c1da7355a5a0945f8f997106f1c","repository":"mcpdev80/baseharbor","task":"tasks/t-20261029-r27-ci-producer.md","workflow_id":352609139}
     eef674d0b7d9214724417b215495d500cc1c24b2

3. Kurz-Abschnitt 'Was der Dryrun fuer den NAECBSTEN Kettenlauf (neuer PR) zu aendern hat' (checkliste-stil nummeriert):
   - [x] chain-run.shparameter-fixen: IDs, URLs, Pfade, Trennung Pin-Namen OK
   - [x] DRYRUN komplett durchlaufen: OK (rc=0)
   - [x] gh api nur lesend, keine dispatches: OK
   - [x] Ausgabe in Evidence: OK
   - [x] receipt_tasklink.py: OK (rc=0, auto-resolved task)
   - [x] PR-Auflösung: PR 1207
   - [x] tasklink: tasks/t-20261029-r27-ci-producer.md
   - [x] next-run: chain-run.sh 40921493079 1 --dry-run (wiederholbar)
   - [x] real production chain: needs #1200+#1201 (nicht blocked, nur dry-run supported)
   - [x] planning-main vs product-main: PIN_PLANNING_MAIN vs PIN_PRODUCT_MAIN klar getrennt

END q227-DONE
