# Round 0 — Secure Export (t-20261018-r27-secure-export), Lane w204

State: BLOCKED (scope decision required from Owner)

## Base attestation
- develop HEAD (base I cut from): `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
- `git ls-remote origin develop` == `3d8fc207deabc2840bcfd888f46d2394cc5a7d36` (confirmed)
- `git ls-remote origin work/r27-secure-export` == EMPTY (branch does not exist)
- Local product repo was on branch `work/r27-registry-access` (head `c2ada69c`), NOT the task branch.
- develop IS an ancestor of the local HEAD (`git merge-base --is-ancestor origin/develop HEAD` rc=0).

## Findings (all verified against origin/develop)
- Predecessor t-20261018-r27-profile-codec (#1363) reports a "connection/profile codec/store" (store.go), but NO such module exists on develop. Instead `internal/application/store.go` was built — that path belongs to t-20261018-r27-public-surfaces, not this slice.
- Predecessor t-20261018-r27-protected-credentials (#1385) reports an OpenBao managed-credential path (`SetManagedCredentialIfAbsent`) plus `internal/credential/broker.go` and `FilePreparedMaterialStore`. On develop:
  - `internal/credential/broker.go` = rotation/managed-credential API: `Broker.Resolve(ctx, ref, scope)`, `NoopBroker`. NOT a local credential export API.
  - `internal/credential/prepared_material.go` = `PreparedMaterialStore` (Load/Save/Clear) keyed by rotation keys. NOT a local credential export API.
  - Neither is consumed by any production code on develop (no non-test callers found).
- `internal/applicationbackup/archive.go` + `archive_test.go` exist on develop — but this is the generic BACKUP archive (`Build`/`Open` over `PayloadEntry{Name,Data}`), owned by the backup-restore feature (core-315 / podman-backup-guided-runtime), NOT the local secure-profile export this task needs. The mission says reuse `crypto.go` only via existing API, not to migrate crypto.
- No eligible local credential catalog, no local credential export path exists on develop.

## Conclusion
The interfaces the task assumes (profile-codec connection/store, protected-credentials local export authority) are either not delivered on develop or are a different API (rotation/managed-credentials). The bounded write-set (secure-profile archive adapter) and the reuse target (crypto.go) are also ambiguous vs the existing backup archive module. This is a scope decision for the Owner — cannot proceed without it.

## END
END_BLOCKED w204-secure-export: BLOCKED — scope decision: predecessor interfaces (profile-codec connection/store, protected-credentials local export authority) not delivered on develop (develop=3d8fc207, secure-export branch absent), local repo on wrong branch, stray untracked coordinator/ in product repo. Need Owner call.
