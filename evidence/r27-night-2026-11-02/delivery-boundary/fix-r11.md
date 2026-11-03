# Fix r11 — retention fail-closed (w15-delivery-retention)

## Context
PR #1333 base `870031253b963793e3ae1463ad82e8342b84ef70` on `work/r27-delivery-boundary`.
Review-1333k.md finding 2 (and review-rezept 1+2): the retention block in
`internal/deployment/deployment_store.go` swallows any loader error of a previous
record, allowing silent Preferences loss + a skipped identity check.

## Work plan
1. Code fix: fail-closed when a previous record exists but the full loader rejects it.
2. B1: EN Consequences line swap (ADR 0022 EN).
3. B2: DE new sub-bullet after `Selection.Normalize` line (ADR 0022 DE).
4. B3: EN Trade-offs line swap.
5. B4: DE Nachteile line swap.
6. Ansende: merge origin/develop, write-set grep, tests, push.

## Implementation

### Code (PART A) — internal/deployment/deployment_store.go
Retention block now distinguishes "no previous file" from "previous exists but
unreadable":

    if record.DesiredProviderPreferences == nil {
        previous, loadErr := loadDeploymentRecordFile(...)
        if loadErr == nil {
            if previous.Identity.ApplicationID != record.Identity.ApplicationID || previous.Identity.Environment != record.Identity.Environment {
                return errors.New("cannot retain preferences from a different deployment owner")
            }
            record.DesiredProviderPreferences = previous.DesiredProviderPreferences
        } else if errors.Is(loadErr, os.ErrNotExist) {
            // no previous record -> first save, allow nil preferences
        } else {
            // previous exists but full loader rejects it (invalid selection/remote-project)
            return fmt.Errorf("cannot retain preferences: previous record unreadable: %w", loadErr)
        }
    }

- `previousExists` logic unchanged (raw file existence via os.ErrNotExist).
- Identity comparison (ApplicationID/Environment) preserved.

### Docs (PART B) — exact replacement texts
- B1 EN Consequences line replaced with fail-closed wording (ADR 0022 EN).
- B2 DE new sub-bullet added after `Selection.Normalize` line (ADR 0022 DE).
- B3 EN Trade-offs: "at observation time" -> "at record-save time".
- B4 DE Nachteile: "Beobachtungszeitpunkt" -> "Speichern des Datensatzes".

## repo-rule compliance
- Only the authorized replacement texts applied; wording left verbatim otherwise.
- Write-set limited to: internal/deployment/deployment_store.go + 2 doc files.

## Tests
TMPDIR=/tmp go test ./internal/deployment ./internal/delivery + go build ./... + go vet

## Ansende
- run w15-mergeblock.sh: git fetch (develop=9a57107f, branch=8c46bb18) + git merge origin/develop
- Merge commit 20f93e9a (parents: 8c46bb18 + 9a57107f); conflict markers: NONE (clean auto-merge)
- build via -buildvcs=false (VCS stamping fails on detached-HEAD worktree, non-fatal); go vet PASS; go test PASS
- push origin HEAD:work/r27-delivery-boundary → 8c46bb18..20f93e9a
- ls-remote work/r27-delivery-boundary == 20f93e9a (== head)
- is-ancestor 9a57107f HEAD => ANCESTOR_RC=0
- my fix content (code + B1/B2/B3/B4 + 2 tests) verified present in merge HEAD

## END
END_DONE w15-delivery-retention: head=8c46bb18f9b74c9e1098f1d854e6d6cbf66eee6a retention-failclosed=4tests
