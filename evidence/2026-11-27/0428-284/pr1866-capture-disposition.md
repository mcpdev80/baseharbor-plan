# PR #1866 capture-path disposition

Date: 2026-11-27  
Role: CODEX REVIEW / scope adjudication  
Card: 0428-284 (existing owner-authorized Demo consent test-harness scope)  
Core candidate: `mcpdev80/baseharbor#1866`, head `3702c09502203e82633d664690eac9484a370df9`  
Evidence run: [Actions run 45916731635](https://github.com/mcpdev80/baseharbor/actions/runs/45916731635), `pull_request`, attempt 1, completed `failure` on that exact head.

## Decision

**Approved scope: one minimal capture-path correction in `mcpdev80/baseharbor-demo/tests/guided/drive.py` only.** The evidence supports a test-harness PTY/transcript capture defect: both selected native runtime jobs emitted the candidate digest and the documented retry hint in their Hosted logs, but the harness reported an empty first transcript and stopped before its explicit retry. This is not evidence that the digest parser or retry is absent. The log evidence does not isolate a lower-level PTY mechanism, so the implementation must correct the observed capture boundary without claiming an unproven cause.

The correction must preserve fail-closed consent behavior. It may allow the existing second `up --confirm-candidate <exact captured digest>` only after the documented prompt and digest are present in the captured first transcript and no foreign error signature is present. Missing, incomplete, or ambiguous capture remains an abort. No automatic confirmation or consent bypass is authorized.

## Exact evidence

- Run `45916731635` is on Core head `3702c09502203e82633d664690eac9484a370df9` (API: `event=pull_request`, `run_attempt=1`, terminal `failure`). The two failing jobs are `140238551139` (Docker data-capabilities, failed step `Run runtime gate`) and `140238551015` (Podman data-capabilities, failed step `Run runtime gate`). `PR Selected Checks` job `140242097317` is downstream and also failed.
- Docker job `140238551139` log prints `confirm-hash fb0c632a4bae7ad2ab6557e5b7805e7130df26e7f310405a99651d7a0b5dd20e` and `Re-run with --confirm-candidate <same digest> ...` immediately before the abort. The reported result is `hash=False, prompt=False, hash_chars=0, transcript_chars=0, confirm_literal=False`; no second `up` was run.
- Podman job `140238551015` log likewise prints `confirm-hash 984ca9f460682613e192dcdec80edad3110528d56597227c23cbad3407f77289` and its exact retry hint immediately before the same zero-capture abort; no second `up` was run.
- The Docker and Podman job logs both identify the checked-out demo reference as `1a3c055cc0eef3f961722f12d843e33f6c1ca43e`. Inspection of `tests/guided/drive.py` at that commit and demo develop `58ac70679efe5f7e95bd47d602841704fb9ffa67` confirms the parser and explicit retry already exist and the file is byte-identical between those two revisions for the reviewed path.
- At the pinned file, `run_tty` requests a capture at lines 261-267, reads the PTY at 303-319, and drains final PTY bytes at 364-380. `run_guided_consent_flow` invokes it with `capture=True` and parses `first_buffer` at 563-571. It refuses the retry when the captured prompt/hash are absent or a foreign signature exists at 588-606; the explicit retry is constructed only at 621-648.

## Scope boundary and acceptance evidence for the correction

Allowed write-set: `baseharbor-demo/tests/guided/drive.py` only. A focused regression must exercise the actual capture path and establish that the first captured transcript contains the emitted documented digest and retry hint, that the retry receives that exact digest only when the existing fail-closed conditions pass, and that absent/partial capture or any foreign error still aborts without retry.

Not authorized: changes to Core/product code, product consent/auth semantics, any `.github/**` workflow or trigger, demo pin changes or reverts, parser/retry redesign, automatic `--yes`/auto-consent, or stopping solely because a text search/grep fails to find the output. This is a scope adjudication, not implementation or run qualification; run `45916731635` remains a failure record.
