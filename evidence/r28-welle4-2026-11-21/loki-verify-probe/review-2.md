ROLLE: REVIEW

# CODEX-REVIEW — PR #1734 / Karte 0428-212

**Verdict: APPROVE**

## PLAN

1. Read the mission and record the numbered plan before Git — done.
2. Verify the real GitHub remotes, frozen PR #1734 head/base/refs, ancestry and changed-file set — done.
3. Read card 0428-212, the prior review recipe, round-2 evidence and cleanliness evidence — done.
4. Inspect the Loki tests and confirm assertions use production-reachable verifier paths — done.
5. Classify owner-scope files, ambient-stack chronology and exact-head CI failures — done.
6. Recheck the candidate and write the verdict and any actionable follow-up — done.
7. Publish only this review file to baseharbor-plan main and verify its remote path/commit — done.
8. Complete the end notification under the mission-specific restriction — done.

## Review metadata

Session ID: not exposed by this interface.
Model: GPT-6 Codex; exact serving variant is not exposed.
Backend: not exposed by this interface.
Review time: 2026-11-21 02:30 UTC.

Candidate: mcpdev80/baseharbor PR #1734, head 45d181ab4089da6611d888d249b27318924ef3c4, base develop 40cb28c758b02960356434b630086a341ebe1738.

## Remote, ancestry and immutability

The first Git command was git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v. Output:

```text
lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)
lane-origin https://github.com/mcpdev80/baseharbor.git (push)
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)
upstream https://github.com/mcpdev80/baseharbor.git (fetch)
upstream https://github.com/mcpdev80/baseharbor.git (push)
```

Before review, git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-212-loki-verify-probe refs/pull/1734/head returned:

```text
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
45d181ab4089da6611d888d249b27318924ef3c4 refs/heads/lane-0428-212-loki-verify-probe
45d181ab4089da6611d888d249b27318924ef3c4 refs/pull/1734/head
```

PR API state: head=45d181ab4089da6611d888d249b27318924ef3c4, base.ref=develop, base.sha=40cb28c758b02960356434b630086a341ebe1738, open, draft=false, merged=false. Candidate fetch succeeded; git merge-base --is-ancestor origin/develop origin/pr-1734 exited 0. git diff --name-status origin/develop...origin/pr-1734:

```text
M internal/logs/loki_test.go
```

git log --oneline origin/develop..origin/pr-1734:

```text
45d181a test(logs): assert Loki health-refusal error identity, not bare err != nil
75770bd test(logs): prove passing health verdicts came from a reached probe
430e272 test(logs): assert the fixture server identity carries server-auth before the probe witness
0dc299c test(logs): split Loki datasource health witness into probe-rejection and precondition subtests
```

The four commits are the single fast-forwarded candidate chain described by the lane, not a second PR. The only changed file is the card's allowed internal/logs/loki_test.go. No owner-owned path is changed: internal/observability/registry.go, internal/capability/perses_selection.go, internal/operatorauth/**, internal/identityprovider/**, internal/serviceaccess/**, the #1615 cmd/baha/** stack and .github/** are absent from the diff.

PR refs before and after the read-only review:

```text
PR head before review = 45d181ab4089da6611d888d249b27318924ef3c4
PR head after review = 45d181ab4089da6611d888d249b27318924ef3c4
```

## P1 — Prior review recipe: both refusals now identify their cause

The unselected-manifest test at internal/logs/loki_test.go:346-354 calls logs.VerifyPersesLokiDatasourceHealth and checks the manifest-selection error text. That exact production branch is internal/logs/loki_datasource.go:360-366; an unrelated non-nil error cannot satisfy the new assertion.

The service-access identity test at loki_test.go:474-495 also calls the production verifier. Its selected manifest reaches loki_datasource.go:375-379, then lokiDatasourceHTTPClient:394-401. It requires both the load Loki service access identity prefix and errors.Is(err, os.ErrNotExist); it cannot pass on an arbitrary error.

Both changes satisfy the prior review recipe in review-1.md and the round-2 Fix 1/Fix 2 sections. No code correction remains for these findings.

## P2 — Probe case reaches the production query path; unmaterialized precondition remains separate

TestPersesLokiDatasourceVerifyNeverReportsHealthy at loki_test.go:363-374 invokes the two explicit cases. In assertUnreachableLokiRejectedByProbe:417-445, the test materializes the provider and complete service-access PKI, verifies all five CA/server/client files exist (:423-429), starts a healthy HTTPS test endpoint, closes it, writes that now-unreachable port, and calls logs.VerifyPersesLokiDatasourceHealth (:431-444). It requires the perses Loki datasource query for source error prefix and excludes the identity-load wrapper, ENOENT and missing-file text.

This is the production HTTP query path, not a test-only shortcut: VerifyPersesLokiDatasourceHealth calls persesLokiDatasourceQuery at loki_datasource.go:375-381; that wraps the query error at :323-330; httpClientQueryProbe delegates to queryStream at :159-166; internal/logs/query.go:279-295 constructs and sends the Loki query_range HTTP request. The closed listener makes the query fail after the client identity has loaded. The service-access fixture writes the client cert and key at loki_test.go:555-650.

The separate unmaterialized case at loki_test.go:451-467 verifies the PKI is absent before calling the same production verifier, then requires the identity-load prefix, os.ErrNotExist, and the PKI path. The precondition remains a named subtest.

The remaining service-access-related error assertions from the prior review are now type/content-bound. The changed health assertions inspected use VerifyPersesLokiDatasourceHealth or its returned error; successful multi-source tests additionally require recorded requests at :684-690 and :760-765. No unreachable production AST was found.

## Earlier red/green evidence

The prior round-1 evidence records the false-green baseline and reproduced missing-client-cert.pem failure in its “Before (verbatim failure evidence)” section, followed by passing explicit probe/precondition subtests in “After (verbatim passing evidence)” and exact-head packages CI. The round-2 akte records that the two old err != nil checks were green before assertion strengthening and includes the new content-bound tests passing in “Local proof”.

The round-2 akte has no separate heading named “WAS DAMIT NICHT BEWIESEN IST”. The boundary is stated in test comments: these tests prove the health verifier's HTTP probe and service-access error path using an isolated local TLS server; they do not claim a live external Loki deployment. This aligns with the card's unreachable-endpoint test contract and is not a blocker.

## P3 — Cleanliness and ambient-stack chronology

The lane's cleanliness section says it started no Docker/Podman project and left the shared bh-docker-dev-shared-* stack untouched. It separately records removing nine empty internal/application/*/runtime/runtime.env test-runtime directories belonging to another session before its commit. That filesystem cleanup is distinct from the ambient container stack and is disclosed.

Per the owner-supplied mission context, a separate hop-lane later removed the ambient bh-docker-dev-shared-* stack on the owner's host at about 03:0xZ under the owner's instruction. I do not attribute that removal to w235. Host container counts after that separate removal are not comparable with earlier counts; this review did not query Docker or start a container. The round-2 evidence is a report of the lane's own actions at its time, not a claim that no later external cleanup occurred.

## P4 — Required CI and inherited red state

Run 44853938826 is pull_request, completed/failure at the exact head 45d181ab4089da6611d888d249b27318924ef3c4. The required card path PR · Go unit · packages completed success; its log says PASS all non-CLI Go package tests. PR · Go unit · owner, go-build and go-vet also succeeded. The required aggregate PR Selected Checks is failure because PR · Go unit · cli-0..3 are failure.

A CLI failure log has the inherited operator-auth line, for example main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator. These are cmd/baha failures outside the only changed file and match 0428-204/0428-215. Thus the red CLI shards are not content of this card. The card's internal/logs packages shard is green and executed; the aggregate itself remains red and cannot be reported as a pass. No rerun or workflow action was performed.

## Verdict and follow-up

**APPROVE** — content and the card-required internal/logs CI shard satisfy the reviewed acceptance. No code correction recipe remains for this card. The inherited CLI gate remains a separate state for its owning cards before any merge.

## Planning repository witness and publication

Planning remote witness from the isolated plan clone:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The plan clone was fetched and git log --oneline origin/main -5 showed:

```text
ee67d7b review: begin PR 1734 card 0428-212
454dfb6 kanban: t-20261121-loki-verify-probe -> review
bad8cff kanban: t-20261120-cli-operator-entrypoints -> review
22c031f kanban: t-20261121-loki-verify-probe -> review
557d6b9 plan: record PR 1615 recovery gate pass
```

After fetching origin main, the exact ls-tree path witness was:

```text
evidence/r28-welle4-2026-11-21/loki-verify-probe/review-2.md
```

The review was published as a single-file commit via the GitHub Contents API because the local plan clone could not create new worktree files under the session disk quota. This publication exception is recorded; no shared checkout, product repository, PR, workflow or other Planning file was written. Mission-specific instruction prohibits posting to another Codeman session; no codeman agent post was sent.

## END

END DONE codex-rev-cli2b: APPROVE for PR #1734 content at unchanged candidate 45d181ab4089da6611d888d249b27318924ef3c4; inherited PR Selected Checks remains red.
