---
id: 2026-10-26-minimal-receipts
type: decision
status: accepted
---

# Minimal receipts — Owner decision, 2026-10-26

Marcel approved the six-field, below-500-byte receipt design and explicitly authorized rewriting the five evidence tasks and beginning PR 1. This decision takes precedence over signature/PKI, archive/manifest, retention/recovery and horizontal publisher/resolver requirements in earlier release/runbook/task text.

Trust boundary: GitHub API authenticates the successful exact run/attempt/job while live. A trusted Owner workflow action verifies again before recording approval. Subsequently protected Planning Git history is the authority; no API revalidation, signatures or archived test contents. A compromised protected writer or complete repository loss is outside this model.

Sequence: PR 1 contract + two scripts + tests/docs; PR 2 one genuine shadow gate with automatic task link and authenticated Owner approval; PR 3 final-check cutover after accepted positive and three negative cases (wrong SHA, dead run, edited receipt). Existing legacy CI qualifies bootstrap and remains unchanged until acceptance. Do not build other gates or reuse machinery in parallel.

Owner approval remains explicit, but no person manually authors evidence or copies run numbers/links. Administrative pilot blockers must be concrete. Owner update 2026-10-29 supersedes the former legacy development fallback: regular feature work waits for verified new CI cutover. Unaccepted product contracts and required coverage remain binding.
