# 0427-191 — create-only `baha app new` documentation

## Verified behavior

Source commit: BaseHarbor `develop` `40cb28c758b02960356434b630086a341ebe1738`.

`cmd/baha/app_new.go:32` describes `app new` as creating an ecosystem-native source repository and `baseharbor.yaml`. The create-only result prints `Next: baha app init --quick` and `Next: baha up` (`app_new.go:137-143`). The interactive mode defaults to `create-only` (`app_new_wizard.go:289-300`). The command index defines `baha app list` as listing registered deployments for the effective Target.

## Current-source smoke

Built `baha` from develop and ran:

```text
baha app new appalpha --directory <existing-parent> --stack go --sql --cache --no-input
```

Result: exit 0; generated project files and printed the documented init/up steps. With a fresh `BASEHARBOR_STATE_DIR`, the state root did not exist after create-only generation.

`baha app list` from the generated project then returned exit 2 with `Managed-environment machine operations require an authenticated BaseHarbor operator.` This is the current #1594 policy. Therefore the docs state that no deployment appears in the registered-deployment list until initialization/application, and do not promise an unauthenticated empty-list response.

## Documentation change and local checks

PR #1744 / exact head `1dcf8d29f02d3cab37653edbe0bda0bfccd6d831` adds the create-only registration explanation and next steps to both `docs/cli/applications.md` and `docs/de/cli/applications.md`.

- `bash scripts/documentation-audit.sh`: PASS (including EN/DE integrity, technical boundaries, workflow coverage).
- `python3 scripts/check_docs_locale_parity.py`: PASS, 171 matched pages.
- `mkdocs build --strict --config-file mkdocs.yml`: PASS.
- `mkdocs build --strict --config-file mkdocs.de.yml`: PASS.
- `git diff --check`: PASS.

The strict builds used the pinned `requirements-docs.txt` in a temporary venv. These changes are on develop through PR #1744; they are not part of the already published v0.4.27 tag.

## Hosted gate

Exact PR run [44879306761](https://github.com/mcpdev80/baseharbor/actions/runs/44879306761) was in progress at evidence publication. Record final job conclusions here before merge/acceptance. Do not close this card until PR #1744 is merged and the exact required checks are acceptable.

## Closeout

PR #1744 was merged after exact hosted run 44879306761 completed all selected jobs successfully. The run passed `PR · Source format`, `PR · Trusted Plan`, `Workflow policy`, `PR · Focused Python`, `PR · Validation · mkdocs-en-strict`, `PR · Validation · mkdocs-de-strict`, `PR · Validation · documentation-audit`, and `PR · Validation · pages-candidate-build`; no job failed or remained in progress. Release/native/Go test jobs were skipped by the docs-only impact selection.

GitHub confirms PR #1744 is CLOSED/MERGED at merge commit `d2d4ded3dedbb6ef7efdd9dc6ba3c114c5e3a163` for exact head `1dcf8d29f02d3cab37653edbe0bda0bfccd6d831`. This resolves the documentation card on current develop. The published v0.4.27 tag was not changed; the documentation clarification is in the subsequent develop history.
