# w366-0428-284-democonsent — recon, END_BLOCKED

- Lane: w366-0428-284-democonsent (session e6ca7696-b1f8-492d-b226-876b16925fc5)
- Card: 0428-284 (t-20261125-0428-284-1812-postretry-gate-failure) — repo baseharbor-demo
- Status: BLOCKED — scope conflict, no claim / no branch / no PR opened
- Date: 2026-11-28

## What I was asked to do

Mission w366-0428-284-democonsent: add a parser for the nested refusal/consent structure in `tests/guided/drive.py` plus an explicit retry with the extracted digest. Claim 0428-284 first (follow-up demo-test-driver, owner-authorized separate demo PR), then a fresh branch from demo `develop`, change + a CI-covered test, prechecks only, normal push, PR against develop, Hosted CI, END with a pair.

## Recon findings (read-only, nothing changed)

- baseharbor-demo remote is https://github.com/mcpdev80/baseharbor-demo.git (verified via `git remote -v`); develop tip = `58ac70679efe5f7e95bd47d602841704fb9ffa67`.
- Governing card 0428-284 (`t-20261125-0428-284-1812-postretry-gate-failure`, state active, owner w198-0428-284-demo-parser) is itself awaiting Codex/Owner reactivation; w267 akte runs in parallel.
- `tests/guided/drive.py` at both the develop tip AND the pin commit already contains the digest parser AND the retry-with-digest path. The mission's premise ("digest not captured, hash=False/prompt=False, kein zweiter up") is contradicted by the code:
  - `capture_confirm_hash` (line 80-92) extracts the 64-hex digest.
  - `run_guided_consent_flow` (line 530-665) re-runs `up --confirm-candidate <digest>` as a second `up` on a documented abort.

## Read-only witnesses

Witness (1) — demo develop tip `58ac706:tests/guided/drive.py`, confirm-candidate parser+retry present:
```
$ git show 58ac706:tests/guided/drive.py | grep -n "confirm-candidate" -A3 -B3
36:def binary_supports_confirm_candidate(argv):
37:    """Feature detection: does the Core 'up' binary expose --confirm-candidate?
...
60:            [*argv, "up", "--confirm-candidate"],
75:        and "--confirm-candidate requires DIGEST" in output
76:        and "unknown option --confirm-candidate" not in output
80:def capture_confirm_hash(text):
83:    Core prints 'Re-run with --confirm-candidate <digest> to acknowledge this
89:        r"Re-runwith--confirm-candidate([0-9a-f]{64})",
107:    match = re.search(r"Candidate:--confirm-candidate([0-9a-f]{64})", normalized)
141:    "(--confirm-candidate); refusing to record deployment state: "
143:    "(--confirm-candidate); refusing to record deployment state"
190:CANDIDATE_ABORT_ERROR = "Re-run with --confirm-candidate"
```
Result: parser + retry VORHANDEN auf demo develop (58ac706).

Witness (2) — pin commit `1a3c055cc0eef3f961722f12d843e33f6c1ca43e:tests/guided/drive.py`, confirm-candidate parser present:
```
$ git show 1a3c055...:tests/guided/drive.py | grep -n "confirm-candidate" -A3 -B3
36:def binary_supports_confirm_candidate(argv):
...
60:            [*argv, "up", "--confirm-candidate"],
75:        and "--confirm-candidate requires DIGEST" in output
80:def capture_confirm_hash(text):
83:    Core prints 'Re-run with --confirm-candidate <digest> to acknowledge this
89:        r"Re-runwith--confirm-candidate([0-9a-f]{64})",
107:    match = re.search(r"Candidate:--confirm-candidate([0-9a-f]{64})", normalized)
```
Result: der PIN-Commit 1a3c055 HAT den Parser bereits (nicht aelter als der Parser).

## Scope conflict

- No code change is needed for "capture digest + retry" — it exists on both the pin commit and develop. A new demo PR would duplicate existing, working behavior.
- The governing card 0428-284 needs Codex/Owner reactivation (w267 running). This mission's premise (digest missing) conflicts with the current code and with the card's own disposition.
- I received two directly contradicting answers mid-recon ("proceed with claim + fix" vs "stop without claim, deliver END_BLOCKED"). I did NOT act on an ambiguous instruction.

## Decision

STOP without claim / branch / PR. Delivered END_BLOCKED with the two read-only witnesses above. No product/delta change; no CI triggered; no runner/infrastructure touched.

## Cleanliness

- No container / compose project started.
- No worktree created under baseharbor (product) or baseharbor-plan beyond evidence.
- git status of baseharbor-demo: clean (read-only `git show` only).

## END line

END_BLOCKED w366-0428-284-democonsent: scope conflict — digest parser + retry already present on pin commit 1a3c055 and demo develop 58ac706; card 0428-284 needs Codex/Owner reactivation (w267 running); contradicting answers. No claim/branch/PR. Read-only witnesses captured.
