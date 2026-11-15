# PR #1577 Review R5 — Perses exact-spec wording

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1577 head/base refs, candidate ancestry/log, metadata, and exact-head run 43677962027.
2. Compare diff 2c4ccc31..fe6c795c against the exact approved #1575 spec sentence in all four release/reference paragraphs and both how-to not_configured definitions.
3. Scan Perses documentation for verified claims lacking the health-path clause and check only substantive spec/code contradictions beyond the r4 recipe.
4. Write APPROVE or REJECT with exact remote/run witnesses, validate, publish evidence on origin/main, verify remote, and post END.

## Candidate and provenance

PR #1577 is OPEN and DRAFT, base `develop`, branch `0428-092-perses-boundary`, exact head `fe6c795cea2e94f1c2772f3b9737e231d244ff1d`. Direct product remote witness (`git ls-remote https://github.com/mcpdev80/baseharbor.git`):

```text
fe6c795cea2e94f1c2772f3b9737e231d244ff1d	refs/heads/0428-092-perses-boundary
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/pull/1575/head
fe6c795cea2e94f1c2772f3b9737e231d244ff1d	refs/pull/1577/head
```

`gh pr view 1577 --repo mcpdev80/baseharbor --json number,state,isDraft,baseRefName,headRefName,headRefOid,url`:

```json
{"baseRefName":"develop","headRefName":"0428-092-perses-boundary","headRefOid":"fe6c795cea2e94f1c2772f3b9737e231d244ff1d","isDraft":true,"number":1577,"state":"OPEN","url":"https://github.com/mcpdev80/baseharbor/pull/1577"}
```

The exact fetched base `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` is an ancestor of the reviewed head (`git merge-base --is-ancestor` succeeded). The base-to-head log from r4 `2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd` contains only the candidate's own commit:

```text
fe6c795cea2e94f1c2772f3b9737e231d244ff1d docs(0428-077): r4 spec-copy verified-health-probe + unavailable-pin coverage (EN/DE)
```

`git diff --check 2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd..fe6c795cea2e94f1c2772f3b9737e231d244ff1d` passed. The diff changes six EN/DE release, reference, and how-to documents (six insertions and six deletions).

## Exact-head CI witness

`gh run view 43677962027 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName`:

```json
{"conclusion":"success","databaseId":43677962027,"event":"pull_request","headSha":"fe6c795cea2e94f1c2772f3b9737e231d244ff1d","status":"completed","workflowName":"CI · Source & Quality"}
```

This is the completed `pull_request` run on the exact reviewed head. No workflow rerun or dispatch was initiated.

## Review findings and verdict

Verdict: REJECT at `fe6c795cea2e94f1c2772f3b9737e231d244ff1d`. One narrowly scoped r5 acceptance criterion remains unmet: the mission explicitly asks that the approved spec sentence be copied word-for-word into all four release/reference paragraphs. The approved source at `docs/spec/management-access-v1.md:63-64` on PR #1575 head `af308e66d38ad1204345bbe83d066dd7548ea6e6` is:

```text
`verified`: only when a real Perses health probe observes the surface. Pin validation alone MUST NOT emit this state.
```

The four target passages do state the health-path condition, but do not reproduce that exact sentence. EN release `docs/releases/v0.4.28.md:15` and EN reference `docs/reference/releases.md:31` use an em dash after `verified` where the spec uses a colon. DE release `docs/de/releases/v0.4.28.md:13` and DE reference `docs/de/reference/releases.md:30` translate the sentence rather than copying it verbatim. This is the requested exact-wording check, not an added formatting preference. The semantic safety rule itself is present in all four passages.

The remaining r4 recipe checks pass: `docs/how-to/observability.md:32` and `docs/de/how-to/observability.md:28` classify an unselected Perses surface or invalid/unavailable pin as `not_configured`; each also describes the configured-unverified state and requires actual Perses health observation before verified. The scan `rg -n -i 'perses.*(unsupported|not supported)|(unsupported|not supported).*perses' docs` returned no Perses unsupported/not-supported state references. The only separate `docs/development/pre-release-readiness.md:7-18` Perses mention says the optional surface is outside the required Core bundle and that no release proof may claim an instance implemented or provisioned; it contains no `verified` assertion and does not contradict the three-state spec. No additional substantive documentation/spec contradiction was found in scope.

## Planning repository witness

The required planning root was verified before this evidence commit with `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel`:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

This evidence is stored only in the actual `baseharbor-plan` repository. Review was read-only against a fresh product clone; no product files, `.github/**` files, workflows, PR state, tests, containers, or VMs were changed or run. No merge was performed; the frost hold remains in effect.

END mission-rev1577-r5.md DONE — REJECT #1577 at `fe6c795cea2e94f1c2772f3b9737e231d244ff1d`; the four release/reference passages still do not copy the approved verified sentence word-for-word.

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully: 536 tasks, 7 epics, 13 releases, 22 decisions; 0 errors and 12 dependency warnings. `git diff --check` passed. The evidence contains no Markdown checkbox lines.

Planning origin/main witness immediately before evidence push (`git ls-remote origin refs/heads/main`):

```text
6566739cf8a1cc9d5e656628bd64b31b90570971	refs/heads/main
```
