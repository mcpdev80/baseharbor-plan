## PLAN
- Step 0: Setup — initialize evidence, read mission, verify worktree/branch
- Step 1: Change `runs-on: [self-hosted,...]` to `ubuntu-latest` in all 5 workflow files
- Step 2: Remove rootless-specific setup steps from workflow files (dockerd-rootless-setuptool, sysctl), use system docker
- Step 3: actionlint + YAML check on all 5 files
- Step 4: workflow_dispatch test on branch (GH-hosted), observe run
- Step 5: Codex post with END result

## Evidence
- Candidate SHA: 878a21247996244d55769b3a1a3c7fdb47d53147
- runs-on changes per file:
  - runtime-broker.yml: lines 27, 233: `[self-hosted, Linux, X64, baseharbor, docker]` → `ubuntu-latest`
  - runtime-s3-acceptance.yml: line 15: `[self-hosted, Linux, X64, baseharbor, docker]` → `ubuntu-latest`
  - docker-runtime-acceptance.yml: already ubuntu-latest/ubuntu-24.04, no change
  - targeted-integration.yml: already ubuntu-latest/ubuntu-26.04, no change
  - targeted-demo-acceptance.yml: already ubuntu-latest, no change
- Rootless setup steps IN workflow files: none found (rootless setup is only in scripts/ci-core-rootless-runtime.sh)
- actionlint: PASSED 0 errors
- YAML validation: PASSED all 5 files
- grep check `runs-on:.*self-hosted` in runtime-broker.yml + runtime-s3-acceptance.yml: 0 matches (exit 1)
- Git commit: `ci(gh-dispatch2): run broker + s3 acceptance on GitHub-hosted (100% GH-hosted, owner rule)`
- Pushed to: `origin/work/gh-dispatch2`
- PR: #1243 https://github.com/mcpdev80/baseharbor/pull/1243 (state: OPEN, base: develop)
- Diff: exactly 3 lines changed, only runs-on values, no scripts/internal touched
