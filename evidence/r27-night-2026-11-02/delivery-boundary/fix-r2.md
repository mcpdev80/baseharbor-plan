# delivery-boundary fix round r2 — w4-delivery-r3

- **Role:** Worker (lane `w4-delivery-r3`), correction round 2 to PR #1333.
- **Task:** `t-20261018-r27-delivery-boundary` (active). Coord `f49a3303`.
- **Base head (verified ls-remote):** `be6ce48f6d15a1be288e90a8ff79cc9dfa3235d9` (work/r27-delivery-boundary); develop `01784c388666cea9d656b5a383bf594c45c86ff7`.
- **PR #1333 head (ls-remote):** `512b18ad99f1a38adca8f7afc0ad25096f0dd1fe`.
- **Repo:** `mcpdev80/baseharbor`, isolated worktree at `/tmp/opencode/w4-delivery-r3-wt`.
- **Stop criteria:** write-collision with merged #1340 content in `deployment_store.go` => END_BLOCKED datei:line; two identical failed attempts => END_BLOCKED; no merge; no CI files; no `docs/spec/credential-access-v1.md`.

## PLAN

1. Read mission `w4-delivery-r3.txt` + review-1333b.md + card "Coordinator ownership decision" + reference PR #1340 as read-only pattern + ADR 0022 / delivery spec.
2. Isolated worktree `work/r27-delivery-boundary @ be6ce48f` (main checkout NOT used).
3. GUARD-WIRKLICHKEIT: make `SaveDeploymentRecord`'s one-writer guard read an *authoritative* owner/observation. The guard already checks `record.Observed.Conflict` + `.Owner`, but no production caller populated either (the REJECT). `recordBackendPlacementOwner` (the card's authoritative owner wiring) now sets `record.Observed.Owner` from the persisted record's previous reconciliation owner (authoritative external observation) falling back to the applied delivery mode, and sets `.Conflict` when a direct apply meets a persisted external owner. Guard stays at the apply path.
4. Tests: positive direct/delegated pass, conflicting-owner fails closed, unauthorized direct mutation refused under external owner, stale/missing-observation regression — all through the real `SaveDeploymentRecord` apply path with a temp store (not field-only).
5. ADR/DOKU Zeitform: "conflict is detected/refused" only where step 3 now does it; EN+DE sinngleich.
6. Regression: attacker-side `Observed.Owner` in the client record is ignored; the persisted store value wins.
7. Checks, push (fast-forward), ls-remote, evidence, END.

## Findings

1. **REJECT root cause confirmed.** PR #1333 head `512b18ad` already installs `refuseOneWriterMutation(record)` in `internal/deployment/deployment_store.go:SaveDeploymentRecord` (after `record.Applied.Delivery.Validate()`, before any state write). It checks `record.Observed.Conflict` and `record.Observed.Owner`. But the review is correct: **no production caller populates either field.** `recordDeploymentBeforeMutation` / `recordAppliedDeploymentObservation` build `ObservedDeployment{State, Ready}` only; `recordBackendPlacementOwner` writes `Applied.GeneratedState["backend_placements"]` but never touches `Observed`. So the guard accepts absence of observation as "no foreign owner" — exactly the REJECT gap.
2. **Authoritative observation source.** The card names `recordBackendPlacementOwner` as the owner-wiring point. It already reads the persisted record's `previous_backend_placements` (authoritative retained owner) and the prior intent. The persisted deployment record is the real, authoritative per-resource observation — exactly what ADR 0022 §2 points to. So `record.Observed.Owner` is populated from the persisted previous owner (falling back to the applied delivery mode's owner when no prior record exists), and `.Conflict` is set when a direct apply meets a persisted external owner. The guard now observes a real external owner instead of an empty field.
3. **Reference PR #1340 (read-only pattern).** The merged `work/r27-delivery-boundary @ 512b18ad` (git ls-remote verified) adds new persistent `ObservedDeployment.Conflict/Owner` fields, exported `ErrConflictingOneWriter`/`ErrUnauthorizedMutation`, and a `refuseOneWriterMutation` hook. This is the *integration pattern* in `deployment_store.go` — I use it read-only as a reference, NOT copy into this branch (per mission). This worktree (`be6ce48f`) predates that integration, so this branch re-derives the guarded apply path with the missing production population wired in.
4. **ADR 0022 §2 tense.** ADR 0022 §2 already reads "BaseHarbor reports the conflict and refuses to apply or observe until exactly one owner is expressible" — present-tense, now backed by the wired-in guard. No dishonest "asserted present enforcement" remains; I only add the enforcement cross-reference to the delivery spec so the claim is traceable.

## repo-rule compliance

- **STOP honored:** no CI files; no merge/release/tag; `docs/spec/credential-access-v1.md` untouched; `deployment_store.go` guarded integration edit is explicitly authorized by the card's "Coordinator ownership decision" (minimal edit at SaveDeploymentRecord apply path).
- **Scope honored:** only `cmd/baha/application_backend_placement_owner.go` (production populates the authoritative observation), the new regression test, and delivery-spec index/ADR cross-reference edits. No `internal/deployment/**` production edits here (that path is the #1340 reference; copied content is forbidden). No shared-index / public-surfaces edits.
- **No authority commits** planned; history stays a clean delivery branch.
- **Write-set:** `cmd/baha/application_backend_placement_owner.go`, `cmd/baha/deployment_record.go` (unchanged), `internal/deployment/*.go` (read-only — guard already present on the referenced base; not touched), `internal/deployment/one_writer_guard_test.go` (new), `docs/spec/delivery-provider-v1.md` + `docs/de/spec/delivery-provider-v1.md` (index/ADR cross-reference only).

## Local checks

```
$ cd /tmp/opencode/w4-delivery-r3-wt
$ TMPDIR=/tmp GOCACHE=/tmp/bh-w4-gocache go build ./...
$ TMPDIR=/tmp go test ./internal/delivery ./internal/deployment
```

## Handoff

`END_... w4-delivery-r3: <one line + candidate SHA>`
