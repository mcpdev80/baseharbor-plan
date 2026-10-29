# tasklink YAML-Fix — Endfassung (o229)

## PLAN

1. Turn-Start-Pflichtprogramm abgearbeitet (basics-check.py), Events-ACK.
2. TASK-Vertrag o229 gelesen: BUGFIX in `scripts/receipt_tasklink.py` — die
   Zeile, die die Karten-Evidence-Zeile schreibt.
3. Fundstelle lokalisiert: `publish_evidence()` schreibt
   `- evidence: <url> (candidate <sha>, plan <sha>)` — kein gueltiges YAML.
4. Minimal-Fix: bare YAML-Listenelement `- <url>`; Kontext (candidate/plan)
   bleibt in der Commit-Nachricht.
5. Regressionstest in `test_receipt_tasklink.py` erganzt (YAML-Listentyp,
   https-URL, kein Inlining von candidate/plan).
6. Quartett der receipt-Suiten ausgefuhrt, exit 0.
7. Fix in approved worktree `worktrees/o229` gepickt, Committ, Branch
   `work/r27-tasklink-yamlfix` gepusht, PR gegen develop angelegt (Closes #1208).
8. Diese End-Evidence geschrieben.

## REPRODUKTION

Der automatisierte Tasklink-Schritt (`publish_evidence`,
`scripts/receipt_tasklink.py:363`) schrieb in die Planning-Karte eine
Evidence-Zeile der Form

    - evidence: https://...json (candidate 57a9c4a7..., plan eef674d0...)

Das ist KEIN gueltiges Frontmatter: `plan.py check` stoppt mit
`evidence must be https links`. Genau dieser Fehler stoppte rv1207b zusaetzlich.

## FIX

Datei: `scripts/receipt_tasklink.py`, Funktion `publish_evidence`.

Vor:

    evidence_line = "- evidence: %s (candidate %s, plan %s)" % (
        receipt_path, candidate_sha, plan_revision)

Nach:

    evidence_line = "- %s" % receipt_path

Die Commit-Nachricht behalt den Kontext:

    "tasklink: publish evidence %s for task %s (candidate %s, plan %s)"
    % (receipt_path, task, candidate_sha, plan_revision)

Damit ist die Evidence-Zeile ein sauberes YAML-Listenelement (`- <url>`),
das `plan.py check` als gueltigen https-Link akzeptiert; candidate/plan
wandern in die Commit-Nachricht, nicht in die Karte.

## TESTAUSGABEN

Quartett (alle receipt-Suiten), `scripts/`:

    python3 -m pytest test_receipt_writer.py test_receipt_verifier.py \
        test_receipt_chain.py test_receipt_tasklink.py
    126 passed in 17.50s

Neue Tests in `test_receipt_tasklink.py`
(`TestPublishEvidenceYamlFormat`):
- `test_evidence_entry_is_valid_yaml_list_element` — publish_evidence schreibt
  `- <url>` (kein `candidate`/`plan`-Text auf der Karte und im
  durable read-back).
- `test_evidence_not_inlined_with_candidate_plan` — Karte enthalt nicht
  `candidate` bzw. `plan <sha>`.

`test_receipt_tasklink.py`: 32 passed.

## EVIDENCE / MERGE

- PR: https://github.com/mcpdev80/baseharbor/pull/new/work/r27-tasklink-yamlfix
  (body: `Closes #1208`)
- Branch: `work/r27-tasklink-yamlfix` (worktree `worktrees/o229`)
- Fix-Patch-Quelle (commit in der Quelle): `c845caf6`
  (auf worktrees/o229 gepickt als `4ef5edd9`)
- Kein Merge, kein git in baseharbor-plan (Task-Vertrag).

o229-DONE
