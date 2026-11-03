# fix-r4 — PR #1333 data-loss regression (t-20261018-r27-delivery-boundary)

Worker lane w7-delivery-r6. Coord f49a3303. Base = head 84634175. Goal: close PR #1333 by fixing the
data-loss regression (review point 1) and the EN/DE doc + caller-conflict contradictions (review point 3).

## PLAN

1. Set up own worktree: fetch work/r27-delivery-boundary, add /tmp/opencode/w7-delivery-r6-wt.
2. Read base 84634175 and review-1333e.md points 1 & 3.
3. Commit 1 — fix retain-order in internal/deployment/deployment_store.go (~199-237):
   - preferences-Retention/replace and authoritative owner/conflict land on the SAME final record that
     is serialized (guardRecord after retention, or retention before the guard-copy);
   - preserve nil-retention (seed nonempty, save nil, reload => identical), replace explicit empty array;
   - invalid input => no change; forged-owner bypass stays denied;
   - set guardRecord.Observed.Conflict to persisted/previous value (caller value discarded, not OR-only);
   - regression tests: nil-retention, explicit empty replacement, invalid input, forged-owner bypass,
     caller-conflict=true with previous=false semantics.
4. Commit 2 — EN/DE docs: scope "refuses actual apply/observation" to record-save extent + deferred
   verweis (existing card names); comments = code.
5. Merge origin/develop; diff grep -E '^(\.github|scripts/|cmd/)' empty; 9-10 files; go test
   ./internal/deployment ./internal/delivery + build/vet; push FF; ls-remote; END to f49a3303.

## repo-rule compliance

- Write set limited to card-authorized store hook + focused regression + EN/DE ADR + comments.
- No new files outside write set; no cmd/baha or CI files; no merge of external changes; max 1 iteration.

## END

Lane w7-delivery-r6: DONE — candidate SHA 4e8e67d877980eda8333c0dd4659e0c0c4eb4457 (PR #1333 head, pushed FF 84634175..4e8e67d8).
