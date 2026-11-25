# Independent review and merge receipt — BaseHarbor PR #1847

Date: 2026-11-25
Card: 0428-078 / `t-20261114-r28-perses-dashboard-identity`
PR: https://github.com/mcpdev80/baseharbor/pull/1847
Reviewed head: `cb2dd0f37da1175968f57d0b7f6f9b533cc4d66a`
Base before merge: `develop` `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`
Canonical owner from fresh Planning `origin/main`: `w165-0428-078-pr1650-basehop`
Candidate `.commit.author.name`: `w165-0428-078-pr1650-basehop` — exact match.
Verdict: **ACCEPTED and MERGED.**

## Contract and diff

The PR changes exactly one file, `scripts/pr-gate-coverage.json`, adding exactly one component row:

```json
{
  "id": "source.internal_metrics_identity_dashboard_witness_go",
  "path": "internal/metrics/identity_dashboard_witness.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

This exactly matches w200's `workers/w200-codex-disposition/1650/decision-block-v2.md` (B/data.capabilities) and `akte.md`. No scripts implementation, product source, workflow, or other file changed. The coverage validator resolves the row's declared surfaces and retains both runtime siblings for `runtime_specific: true`; the Trusted Plan job consumed the trusted-base catalog as intended.

## Exact-head CI and merge gates

Run [45661491401](https://github.com/mcpdev80/baseharbor/actions/runs/45661491401) is a terminal-success `pull_request` run on the reviewed head. API inspection of `/actions/runs/45661491401/jobs?per_page=100` found no failed jobs. `PR · Trusted Plan`, source format, focused Python, executor/policy/planner/receipt validations, and advisory candidate-added checks succeeded. `PR Selected Checks` succeeded in job 139373365631 and the check-run app ID is 15368. Other nonselected native/release jobs were skipped.

The commit parent and pre-merge `develop` tip were both `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`; the PR was open, ready, clean, and mergeable. The active develop required-check ruleset requires `PR Selected Checks` from integration 15368; it passed. No review comments or unresolved review comments existed before this review.

At review time #1842 was not ripe concurrently: its then-current head had one successful pull-request run and a failed dispatch, short of its required two distinct PR runs plus 14 Light gates. I therefore proceeded with #1847; no #1842 action was taken.

## Merge receipt

Normal expected-head squash merge completed. GitHub reports PR state closed/merged, `merged_at` `2026-11-25T17:14:10Z`, and merge SHA `3a2ae6b1139570c98b8924e3b19975c56a289400`. The resulting `develop` tip is that same SHA. The 0428-078 card status was not changed.

PR verdict comment: https://github.com/mcpdev80/baseharbor/pull/1847
