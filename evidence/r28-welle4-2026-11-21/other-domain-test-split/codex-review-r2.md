# 0428-206 independent review — round 2

## Verdict: REJECT the round-1 classification as incomplete

The round-1 evidence cannot meet the acceptance requirement that all 89 other-domain failures appear exactly once.

### Direct arithmetic defects

- The twelve group counts printed in round 1 are `9+5+3+3+2+2+2+1+1+1+1+8`, which sum to **38**, not 89.
- Group 12 is labelled 8, but its listed subgroups are `3+2+2+2`, which sum to **9**.
- The round-1 inventory only enumerates 13 selected failures in its §1; it does not include the full `other` cohort. The referenced `/tmp/w217-classified.tsv` and `/tmp/w217-run1.txt` are absent on this machine, so the original 89-row classification cannot be audited from those files.
- Group 8's production-file attribution was later corrected by the dedicated App Edit investigation: the refusal is raised by `cmd/baha/core_network_binding.go`, not `application_provider_impact.go`. That correction does not restore the missing rows.

### Independent exact-base reproduction

- Product repository: `mcpdev80/baseharbor`; detached worktree `/tmp/baseharbor-w206-review` at exact develop SHA `40cb28c758b02960356434b630086a341ebe1738`.
- Command: `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true go test -json ./cmd/baha -count=1`.
- Result: package FAILURE after 179.442s. The complete machine-readable stream was captured at `/tmp/w206-rerun.json` for this review session.
- The JSON stream contains 203 distinct failing top-level test names. This is not directly interchangeable with the old dossier's “181 First-Level” count: the old raw output is unavailable, and this rerun includes environment-sensitive failures (for example, the App Edit lifecycle test fails its host-memory headroom preflight). I therefore do not claim that the new run confirms the old cohort or that these 203 are the 89 target cases.
- Initial invocation without prompt suppression stalled at a test's `git credential fill` against `https://example.invalid` and was interrupted; the second run disabled Git prompts and completed. Existing Docker containers were pre-existing and no container was created by this classification run.

## Required correction before acceptance

Rebuild the exact first-level failure inventory from the captured `go test -json` stream (or a fresh equivalent controlled run), state the classification algorithm for `runWithIO`, MCP, direct subcommand/domain calls, and map every target failure exactly once to its first failing production file with the required rubric and witness. Reconcile the original 89/181 counts against the new run rather than assuming they match. Preserve separate already-created consequences 0428-207 and 0428-210; do not create duplicates.

Until that full row-level reconciliation is complete, 0428-206 is not accepted. The card is returned to active work under the current wait-sweep owner.
