# gh-ci-core SCOPE ACCEPTED (2026-11-01): CI files (ci.yml, nextjs e2e, ci-core-rootless-runtime.sh system-daemon,
doctor test) green. PR #1239 validate red ONLY due to product endpoint gap internal/runtime/docker_engine.go:105
(hardcoded rootless, no system-context resolution) -> handed to docker-endpoint-context lane. Do-not-merge while
gate red (owner rule 7). Empirical: rootless impossible on ubuntu-latest (userns blocked); must use system context.
