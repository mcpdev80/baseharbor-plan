# ACCEPTED gh-preflight (coordinator verified 2026-10-31)
pre-release.yml + pre-release-runtime-suite.yml: alle runs-on = ubuntu-latest/ubuntu-26.04 (0 self-hosted).
actionlint PASS. Null-Diff = korrekt (nichts zu migrieren). Sie rufen scripts/ci-core-rootless-runtime.sh auf
-> deren GH-hosted-Korrektheit liegt bei Lane gh-ci-core (Shared-Interface), nicht hier. Kein Release/Tag geloest.
