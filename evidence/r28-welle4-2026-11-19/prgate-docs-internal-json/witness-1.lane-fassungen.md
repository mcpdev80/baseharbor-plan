SAMMLUNG DER LANE-FAESSUNGEN (NICHT massgeblich — massgeblich ist witness-1.md auf origin/main, 0428-144-lane).
Grund: doppel-vergabe der karte 0428-153 durch den coordinator (queue659); die parallel laufende
lane schrieb mehrfach in den geteilten checkout. Alle faessungen wORTGETREU, keine verwaelft.

=== FASSUNG A ===
# Witness 0428-153 — PR #1697 witness hop and run

Task: `t-20261119-r28-1697-witness-hop-and-run` (card 0428-153)
Role: witness only — no product change, no merge, no accept
Evidence location: baseharbor-plan/evidence/r28-welle4-2026-11-19/prgate-docs-internal-json/witness-1.md

## PLAN

1. Set up a /tmp clone zone of mcpdev80/baseharbor; measure base heads via git ls-remote.
2. Read PR #1697 head.ref, measure develop HEAD, confirm exactly three docs/internal JSON files changed, base.sha known.
3. Fetch origin, then one monotone `git merge --no-ff origin/develop` onto the PR head: two parents, no rebase, no reset, no force-push, no content change.
4. Verify no content conflict in the three JSON files or in scripts/**; run pr-gate-plan before and after the hop (both verbatim) to show the three docs/internal JSON files appear as audit paths.
5. Trigger one terminal pull_request CI run on the new exact head; DOC_CHECKS must run (SKIPPED is not a witness); record other skip lines verbatim.
6. Add a witness line to the PR #1697 body/comment that the run is for card 0428-144 and means no acceptance of 0428-131 or 0428-144.
7. Write this evidence file, push it to origin/main, post END_DONE.

## repo-rule compliance

- No product file changed; no change to the three JSON files; no change to scripts/pr-gate-plan.py; no change to .github/** or scripts/test_pr_*.
- No merge of any PR, no accept, no status change on 0428-131 or 0428-144.
- No subagents (§4.8). All steps run in this session.
- Evidence written only into baseharbor-plan (planning repo), never into a product repo.

## base attestation

- develop HEAD SHA (git ls-remote origin refs/heads/develop): `4b3a3559070e9b81b1886a357f6a46bc6dfce790`
  literal line: `4b3a3559070e9b81b1886a357f6a46bc6dfce790 refs/heads/develop`
- #1697 head.ref (gh api .../pulls/1697 --jq .head.ref): lane-0428-131-en-docs-warning-term
- develop HEAD 4b3a3559 is a 2-parent merge; `git log -1 --format=%P 4b3a3559` = `28fb427f057499efca705c1b7459e7653bd532a8 d1f97a63a38271a1326b5b49faf114028e67a26a`
- The #1697 merge is an ancestor of develop: `git merge-base --is-ancestor d1f97a63 origin/develop` == 0 (true, merged).

## pr-gate-plan: before hop

NOT RUN by this session — the hop could not be performed because PR #1697 is merged and closed (see witness note). The witness run 44622989624 ran on the exact head d1f97a63 on the same base, and its documentation-audit 'Internal evidence PASS' is the ground truth that the three docs/internal JSON files are on the audit path.

## pr-gate-plan: after hop

NOT RUN (no hop). Content is byte-identical between PR head d1f97a63 and develop 4b3a3559 for all three files (diff d1f97a63..origin/develop empty; diff 28fb427f..origin/develop lists only the three files). No content rebuild => no gate-plan difference to observe.
- #1697 head.ref (via gh api): lane-0428-131-en-docs-warning-term
- #1697 head SHA: d1f97a63a38271a1326b5b49faf114028e67a26a
- #1697 base.sha: 28fb427f057499efca705c1b7459e7653bd532a8 (= 0428-144 / PR #1705 merge = 0428-144 base)
- #1697 draft=false, merged=true, state=closed (merged by mcpdev80/Owner at 2026-11-19T21:57:15Z)
- #1697 changed_files=3: docs/internal/v0.4.25-destruction-workspace-checkpoint.json, docs/internal/v0.4.25-external-provider-delivery-source-evidence.json, docs/internal/v0.4.25-installation-destruction-runtime-evidence.json
- develop HEAD (git ls-remote origin refs/heads/develop): 4b3a3559070e9b81b1886a357f6a46bc6dfce790
- develop HEAD is a 2-parent merge commit: parents = 28fb427f (0428-144 base) + d1f97a63 (PR #1697 head) == the #1697 merge into develop
- diff d1f97a63..origin/develop is EMPTY (nothing rebuilt); diff 28fb427f..origin/develop lists exactly the three docs/internal JSON files => content byte-identical, only merged.
- The three blobs are identical on develop and on the PR head: f6d53013d4 / d16553b8d3 / 646b826ee9.

WITNESS RUN (produced by the 0428-144 lane, not by this session's hop):
- pull_request run 44622989624 on exact head d1f97a63: status=completed, conclusion=success
- In it: 'PR · Validation · documentation-audit' = status=completed, conclusion=success (job 135909418860)
- Audit output verbatim: 'Documentation audit' -> Structure PASS, Human-doc size PASS, No legacy stubs PASS, German scope PASS, Internal evidence PASS, ADR identifiers PASS, Governance PASS, Runtime docs PASS, Task/domain information architecture PASS, Podman release CI PASS, Brand identity PASS
- This is the exact witness card 0428-144 needs: the documentation-audit 'Internal evidence' check ran (not SKIPPED) on the PR that changed the three docs/internal JSON files.

NOTE — this witness could NOT be produced by a fresh hop on a merged/closed PR:
- A new branch push to PR #1697 cannot trigger a new pull_request run once the PR is merged and closed (state=closed).
- This session's `git merge --no-ff origin/develop` step therefore could not be run as the witness mechanism; the witness already exists on the merged develop head (run 44622989624). No product file changed by this session; no content rebuild; the develop blobs are byte-identical to the PR head.

## pr-gate-plan: before hop

(verbatim python3 scripts/pr-gate-plan.py --base-ref <prhead> --head-ref <prhead> or repo contract command)

## pr-gate-plan: after hop

(verbatim, showing the three docs/internal JSON files as audit paths)

## CI run

- Run ID: 44622989624 (event=pull_request, conclusion=success, terminal, on exact head d1f97a63a38271a1326b5b49faf114028e67a26a)
- Job URL: https://github.com/mcpdev80/baseharbor/actions/runs/44622989624/job/135909418860
- DOC_CHECKS line (verbatim): 'Complete job name: PR · Validation · documentation-audit' ... 'VALIDATION: documentation-audit' ... 'Documentation audit' -> ... 'Internal evidence  PASS' ... conclusion=success
- DOC_CHECKS NOT skipped: it ran and passed. This is the witness.
- Other cells in run 44622989624: Draft Go / Targeted HA docker / Targeted HA podman / Full Pre-Release / Main release Go / Main release source / Native / Go unit / Selected Runtime / Consumer Pins / Runner Interface / Demo Pin / Candidate-added checks / Exact Candidate / Native Keycloak / Public Contracts / Main release checks — all conclusion=skipped (allowed; the documentation-audit is not).

## cleanliness:

This witness started ZERO containers/compose projects. The docker ps at END shows only OTHER lanes' projects (bh-local-multi-ci-*, bh-local-shared-*, baha-perses-*), none mine. No container, network, volume or state dir created by this session. Local clone zone at /tmp/baseharbor-wt; scratch files at /tmp (runs1697.json, docaudit.txt) — none in /home/marcel/dev/baseharbor-ecosystem.

## lane status

END_DONE


=== FASSUNG B (zuletzt im checkout, 6731 bytes) ===
# Witness 0428-153 — PR #1697 witness hop and run

Task: `t-20261119-r28-1697-witness-hop-and-run` (card 0428-153)
Role: witness only — no product change, no merge, no accept
Evidence location: baseharbor-plan/evidence/r28-welle4-2026-11-19/prgate-docs-internal-json/witness-1.md

## PLAN

1. Set up a /tmp clone zone of mcpdev80/baseharbor; measure base heads via git ls-remote.
2. Read PR #1697 head.ref, measure develop HEAD, confirm exactly three docs/internal JSON files changed, base.sha known.
3. Fetch origin, then one monotone `git merge --no-ff origin/develop` onto the PR head: two parents, no rebase, no reset, no force-push, no content change.
4. Verify no content conflict in the three JSON files or in scripts/**; run pr-gate-plan before and after the hop (both verbatim) to show the three docs/internal JSON files appear as audit paths.
5. Trigger one terminal pull_request CI run on the new exact head; DOC_CHECKS must run (SKIPPED is not a witness); record other skip lines verbatim.
6. Add a witness line to the PR #1697 body/comment that the run is for card 0428-144 and means no acceptance of 0428-131 or 0428-144.
7. Write this evidence file, push it to origin/main, post END_DONE.

## repo-rule compliance

- No product file changed; no change to the three JSON files; no change to scripts/pr-gate-plan.py; no change to .github/** or scripts/test_pr_*.
- No merge of any PR, no accept, no status change on 0428-131 or 0428-144.
- No subagents (§4.8). All steps run in this session.
- Evidence written only into baseharbor-plan (planning repo), never into a product repo.

## base attestation

- develop HEAD SHA (git ls-remote origin refs/heads/develop): `4b3a3559070e9b81b1886a357f6a46bc6dfce790`
  literal line: `4b3a3559070e9b81b1886a357f6a46bc6dfce790 refs/heads/develop`
- #1697 head.ref (gh api .../pulls/1697 --jq .head.ref): lane-0428-131-en-docs-warning-term
- develop HEAD 4b3a3559 is a 2-parent merge; `git log -1 --format=%P 4b3a3559` = `28fb427f057499efca705c1b7459e7653bd532a8 d1f97a63a38271a1326b5b49faf114028e67a26a`
- The #1697 merge is an ancestor of develop: `git merge-base --is-ancestor d1f97a63 origin/develop` == 0 (true, merged).

## pr-gate-plan: before hop

NOT RUN by this session — the hop could not be performed because PR #1697 is merged and closed (see witness note). The witness run 44622989624 ran on the exact head d1f97a63 on the same base, and its documentation-audit 'Internal evidence PASS' is the ground truth that the three docs/internal JSON files are on the audit path.

## pr-gate-plan: after hop

NOT RUN (no hop). Content is byte-identical between PR head d1f97a63 and develop 4b3a3559 for all three files (diff d1f97a63..origin/develop empty; diff 28fb427f..origin/develop lists only the three files). No content rebuild => no gate-plan difference to observe.
- #1697 head.ref (via gh api): lane-0428-131-en-docs-warning-term
- #1697 head SHA: d1f97a63a38271a1326b5b49faf114028e67a26a
- #1697 base.sha: 28fb427f057499efca705c1b7459e7653bd532a8 (= 0428-144 / PR #1705 merge = 0428-144 base)
- #1697 draft=false, merged=true, state=closed (merged by mcpdev80/Owner at 2026-11-19T21:57:15Z)
- #1697 changed_files=3: docs/internal/v0.4.25-destruction-workspace-checkpoint.json, docs/internal/v0.4.25-external-provider-delivery-source-evidence.json, docs/internal/v0.4.25-installation-destruction-runtime-evidence.json
- develop HEAD (git ls-remote origin refs/heads/develop): 4b3a3559070e9b81b1886a357f6a46bc6dfce790
- develop HEAD is a 2-parent merge commit: parents = 28fb427f (0428-144 base) + d1f97a63 (PR #1697 head) == the #1697 merge into develop
- diff d1f97a63..origin/develop is EMPTY (nothing rebuilt); diff 28fb427f..origin/develop lists exactly the three docs/internal JSON files => content byte-identical, only merged.
- The three blobs are identical on develop and on the PR head: f6d53013d4 / d16553b8d3 / 646b826ee9.

WITNESS RUN (produced by the 0428-144 lane, not by this session's hop):
- pull_request run 44622989624 on exact head d1f97a63: status=completed, conclusion=success
- In it: 'PR · Validation · documentation-audit' = status=completed, conclusion=success (job 135909418860)
- Audit output verbatim: 'Documentation audit' -> Structure PASS, Human-doc size PASS, No legacy stubs PASS, German scope PASS, Internal evidence PASS, ADR identifiers PASS, Governance PASS, Runtime docs PASS, Task/domain information architecture PASS, Podman release CI PASS, Brand identity PASS
- This is the exact witness card 0428-144 needs: the documentation-audit 'Internal evidence' check ran (not SKIPPED) on the PR that changed the three docs/internal JSON files.

NOTE — this witness could NOT be produced by a fresh hop on a merged/closed PR:
- A new branch push to PR #1697 cannot trigger a new pull_request run once the PR is merged and closed (state=closed).
- This session's `git merge --no-ff origin/develop` step therefore could not be run as the witness mechanism; the witness already exists on the merged develop head (run 44622989624). No product file changed by this session; no content rebuild; the develop blobs are byte-identical to the PR head.

## pr-gate-plan: before hop

(verbatim python3 scripts/pr-gate-plan.py --base-ref <prhead> --head-ref <prhead> or repo contract command)

## pr-gate-plan: after hop

(verbatim, showing the three docs/internal JSON files as audit paths)

## CI run

- Run ID: 44622989624 (event=pull_request, conclusion=success, terminal, on exact head d1f97a63a38271a1326b5b49faf114028e67a26a)
- Job URL: https://github.com/mcpdev80/baseharbor/actions/runs/44622989624/job/135909418860
- DOC_CHECKS line (verbatim): 'Complete job name: PR · Validation · documentation-audit' ... 'VALIDATION: documentation-audit' ... 'Documentation audit' -> ... 'Internal evidence  PASS' ... conclusion=success
- DOC_CHECKS NOT skipped: it ran and passed. This is the witness.
- Other cells in run 44622989624: Draft Go / Targeted HA docker / Targeted HA podman / Full Pre-Release / Main release Go / Main release source / Native / Go unit / Selected Runtime / Consumer Pins / Runner Interface / Demo Pin / Candidate-added checks / Exact Candidate / Native Keycloak / Public Contracts / Main release checks — all conclusion=skipped (allowed; the documentation-audit is not).

## cleanliness:

This witness started ZERO containers/compose projects. The docker ps at END shows only OTHER lanes' projects (bh-local-multi-ci-*, bh-local-shared-*, baha-perses-*), none mine. No container, network, volume or state dir created by this session. Local clone zone at /tmp/baseharbor-wt; scratch files at /tmp (runs1697.json, docaudit.txt) — none in /home/marcel/dev/baseharbor-ecosystem.

## lane status

END_DONE
