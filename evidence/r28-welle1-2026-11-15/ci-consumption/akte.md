# 0427-020 — Deferred CI consumption examples for accepted product APIs (developer integration docs)

Karte: `t-20261018-r27-ci-consumption` (0427-020, release v0.4.28) · Lane: mission-020-consumption (ornith-laptop) · Model: worker-ornith1.5-laptop · PR: (draft, base develop, created in final step)

## END line

`END_DONE` — task complete: EN/DE CI consumption guide + GitHub Actions/GitLab CI examples (docs only), PR #1589 (draft, base develop 0e9ccb582), CI 43738441977 success (6/21/0).

## PLAN

1. Pull baseharbor-plan, read card fully (product-outcome + three-slot ownership + explicit scope-transfer sections), claim via `plan.py claim` + commit + push VOR any change, then `plan.py show` as witness.
2. Reality check: `develop ls-remote`; cut worktree from develop.
3. Map the accepted product API surface on develop (verified against live `baha` binary + docs) — no invented APIs; file:line witnesses.
4. Write consumption examples under `docs/` (EN + DE where a pattern exists) for the cards' accepted APIs; no `.github/**`, no workflow, no product-code change.
5. Draft PR base develop (one PR per card).
6. Watch CI docs-gates to terminal; publish akte to origin/main; END post.

## Planning repository identity witness (wrong-zone check)

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

## Base attestation and provenance

- Base SHA the branch is cut from: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (origin/develop, exact fetch).
- Ancestor test: `git merge-base --is-ancestor 0e9ccb582... <candidate HEAD>` = YES.
- `git log 0e9ccb582..HEAD` lists ONLY my own commits (no foreign commit carried on top).
- claim published before any change: planning commit `591285722dcf1550b14a20dd204fedf48cf25d37` (origin/main witness: `e2d968fa..59128572`).

## Reality witnesses (remote truth)

```
git ls-remote https://github.com/mcpdev80/baseharbor.git develop main
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```

## Result

- EN consumption guide `docs/how-to/ci-consumption.md` (+ DE `docs/de/how-to/ci-consumption.md`): pin release image (immutable digest), `--control-plane-only` Core operator path, deterministic app lifecycle (`--no-input`, `--yes`), JSON/exit-code/timeout behavior, secrets out of examples, no live triggers, preserved native delivery/stage boundary and supported providers. No invented APIs.
- GH Actions example `docs/example/github-actions/` (README.md + `consume.yml`) + DE counterpart; GitLab CI example `docs/example/gitlab-ci/` (README.md + `pipeline.yml`) + DE counterpart. Both document the accepted `baha` surface only; no BaseHarbor change, no secrets, no auto trigger.
- Registered in EN nav (`mkdocs.yml`) and DE nav (`mkdocs.de.yml`) under Automation / Agents.
- Verified against live `baha` binary on develop: global flags `--no-input/--plain/--no-color/-q/--quiet/-o json/--output json/--json/-v/--verbose`; core workflow `init/up/down/status/plan/destroy/update/version`; `app inspect/plan/preflight/apply/env/creds/logs/status`; releases pin `ghcr.io/mcpdev80/baseharbor-runtime:X.Y.Z` (docs/reference/releases.md).
- Scope: docs only. No `.github/**`, no workflow change, no product-code change. Base SHA the branch is cut from: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (develop).

## repo-rule compliance

- documentation-audit.sh PASS; mkdocs build --strict (EN + DE) passes; go build ./... OK.
- No `.github/**` touched, no workflow change, no product-code change (Owner scope preserved).
- No `.evidence/` directory in product repo; evidence lives only in baseharbor-plan.
- No docker/podman compose project started (CI docs task, no runtime gate needed).

## Verification runs

- `scripts/documentation-audit.sh`: PASS (EN/DE 170 paired pages, DE integrity 170, German nav 44, German rendered links 19975, brand identity).
- `mkdocs build --strict` (EN + DE): built OK after fixing two relative links to `../reference/releases.md` and `../cli/core.md`.
- GitHub CI run **43738441977** (PR #1589, pull_request): completed, **6 success / 21 skipped / 0 failed**. Docs/validation path succeeded; heavyweight native/release gates skipped for a draft docs PR. No failed job.
- Both YAML fixtures parse (yaml.safe_load OK on `consume.yml` and `pipeline.yml`).
