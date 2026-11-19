# Independent read-only review — PR #1623 / 0428-063

Reviewed 2026-11-19.

- Live PR is open and Draft at head `8014d71eaac422ed44c8fcf2c28a784c0cb0a044`, based on `cli2-identity-secrets-head` `f93564a0d707983bfe6a8b59375c1c1c914d7827`.
- Exact head has no workflow runs/checks; branch is based on an open stack entry and is substantially diverged from current `develop` `558dc42d0c8c9d798fcdf5938be2ea14e432b754`. Rebase and exact-head checks remain required.

## Findings

1. `app logs -c NAME` parses the component selector but the execution path uses only `options.service`; the selected components do not filter the logs request. With multiple services, noninteractive selection can remain ambiguous. Existing tests cover parsing, not command behavior.
2. `app exec --cmd "echo hi > /tmp/x"` passes the whole string as one executable argument to Compose; Compose does not shell-parse it, so shell syntax is not executed. Either define and implement an explicit shell command contract or document and validate an executable-only argv contract.
3. The PR says child exit status is preserved, but `preserveWorkloadExitStatus` wraps it as a presented error; `cli.ExitCode` maps that non-usage error to exit code 1. Tests check the rendered `7`, not the process exit status.

No PR/product files, comments, claims, or merge state were changed by this review.
