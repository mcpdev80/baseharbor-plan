# 0428-142 r2 — real `unreachable` backend-witness emission

Korrekturrunde nach CODEX-REVIEW (note-142-fix.txt / review-1.md). PR #1702, head `6740299f91c040af7b1357d63be898eac57669f5`, base develop.

## PLAN

- Befund 1 (content): the backend-witness still derives every state from manifest flags; `unreachable` is declared (`app_status_result.go:64-65`) but never emitted. Derive per-backend state from a REAL resolved backend signal so `unreachable` is a genuine state, tested against a manifest that declares a signal but resolves unreachable.
- Befund 2 (records): locate the false `validate ...` claim in the akte, correct it with a witnessed source.
- Befund 3 (knowledge, not a bug): after merging #1702 to develop 40cb28c the four CLI shards stay red (0428-204). Do NOT touch cmd/baha/main.go, internal/operatorauth/**, or tests that 0428-204 occupies.

### Steps

- Fix witness test helper to add configureTestTarget(t) env setup so the witness path resolves (baseline repro).
- Implement unreachable emission: change persesBackendSignalWitnessFromManifest signature to (m, resolvedHostSignalStatus, PersesBackendSignalWitness), wire both call sites.
- Add a test asserting unreachable against a declared-but-unresolved manifest (not against a flag).
- Correct the false validate claim in the akte with a witnessed source.
- Gate: go test cmd/baha (Status|Witness|Perses) before/after + go test internal/metrics, go vet, go build.
- One PR push on lane-0428-142-statuswitness, watch hosted run to terminal, record run-id + conclusion.
- Publish evidence to baseharbor-plan origin/main, clean host, post END to coordinator.

## Repo-rule compliance

- Write-set: exactly the PR witness files (cmd/baha/app_status_result.go, cmd/baha/perses_lifecycle.go, cmd/baha/app_status_result_test.go, and the per-backend witness input from internal/metrics which is already in the PR). No new files beyond the PR's existing ones.
- No changes to cmd/baha/main.go, internal/operatorauth/**, internal/capability/perses.go, internal/serviceaccess/**, .github/**, scripts/**.
- No subagents; every step runs in this session.

## Cleanliness

- (to be filled at END with a ps-witness)

## END

- (to be filled: END_DONE|END_BLOCKED w222-0428-142-witness + candidate SHA)
