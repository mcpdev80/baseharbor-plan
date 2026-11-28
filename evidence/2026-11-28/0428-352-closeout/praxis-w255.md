# 0428-352 Praxis-Retest / Disposition — w255

Date: 2026-11-28
Role: read-only review; no cleanup/session mutation performed.

## Disposition

Keep the current implementation in CHANGES under the existing card 0428-352. Do not create a new card and do not treat the r9 PASS as sufficient acceptance: the real shared-directory scenario reported by the owner still fails closed before a durable mapping can be written, and its PARTIAL text overstates what was persisted. Repair this in the existing card's write-set, then re-review before any cleanup run.

## Bound evidence

Read-only `codeman agent list --json`, filtered to the two exact lane names, returned:

- `w401-0428-292-consentfix`: id and claudeSessionId both `2cd2e2d6-9a4d-4e87-ad3a-63559e9ac48c`; status `idle`; parentSessionId `e6ca7696-b1f8-492d-b226-876b16925fc5`; shared workingDir `/home/marcel/dev/baseharbor-ecosystem/workers/.models/flash`.
- `w402-0428-315-constfix`: id and claudeSessionId both `e0ed81d0-fac2-4f3d-aae3-0009e872f466`; status `idle`; same parentSessionId and workingDir.

Read-only watcher-state inspection shows both exact ids registered as workers with the Coordinator id and terminal acknowledgement. Read-only OpenCode DB query against those two exact session ids returned `db_rows []`. Read-only `scripts/.release-pending.json` lookup returned no entries for either id.

These witnesses establish two individually named live Codeman agents, a shared directory, no exact OpenCode DB row for either corresponding session id, and no persisted pending-release record for either agent. They do not authorize deleting either Codeman agent or altering pool state.

## Findings and recipe

1. Resolve identity by exact lane name and trusted parent before directory matching.

   `release-lane.py:147-155` currently treats two children with the shared working directory as ambiguous, even though `agents()` has a unique exact lane name and trusted `parentSessionId` for each. Change the resolver to accept the selected lane identity (or exact name plus coordinator id), select exactly one agent where `name == lane_name` and `parentSessionId == coordinator_id`, and take its exact `claudeSessionId` as the OpenCode id. Require exactly one match; zero or multiple exact-name/parent matches fail closed. Directory may be checked as context, but must not be the identity key. Keep registry resolution as another exact source only when its lane id/name association is unique.

2. Make PARTIAL persistence truthful and resumable.

   In `release-lane.py:349-361`, the ambiguous and unresolved returns at lines 351-354 occur before the pending write at lines 356-360. Therefore those branches cannot claim that a durable exact reference was retained unless a prior pending entry exists. Once exact-name resolution yields an OpenCode id, atomically persist the full exact record before PARTIAL or destructive work. When identity cannot be resolved, either atomically persist an explicit retry ticket with `opencode_id: null` and an ambiguity reason, or do not claim persistence; the message must say `no exact OpenCode id resolved; no exact session reference persisted; reservation/session retained` (or accurately describe a persisted retry ticket). An unresolved retry ticket is not an exact OpenCode reference. Preserve the reservation until the OpenCode session is proven gone and Codeman removal succeeds.

3. Release the two current zombies only after the resolver fix is deployed and reviewed.

   For each lane, `worker-cleanup.sh` already selects a unique exact name in `codeman agent list --json` and passes its id to `release-lane.py`. The verified agent record supplies the trusted parent and exact `claudeSessionId`. After the name-based resolver uses that exact OpenCode id, the already observed absence of `session_v2.id` for that id is the gone witness. `release-lane.py` can then persist the exact mapping, remove the Codeman agent by its Codeman id, observe that the exact OpenCode DB row is absent (so no OpenCode delete is needed), write the release receipt, and release the reservation. Verify the final seat with `pool-reconcile.py status` and confirm the exact Codeman name is absent from `agent list`.

   If the name/parent match ceases to be unique, or the exact OpenCode id cannot be established, HOLD: do not infer gone from the shared directory, do not remove the Codeman entry, and do not free the reservation. Re-capture the bounded agent-list and exact-id DB witnesses before retrying.

## Source locations

- `scripts/release-lane.py:147-155`: shared-directory lineage matching and ambiguous-lineage exception.
- `scripts/release-lane.py:349-361`: PARTIAL returns precede the pending write.
- `scripts/release-lane.py:382-405`: exact pending write before destructive actions, OpenCode exact-id existence/deletion check, pending clear after gone verification, then pool release.
- `scripts/worker-cleanup.sh:76-85`: exact-name Codeman lookup and release-lane invocation.

END_BLOCKED w255-0428-251-demo170codex: 0428-352 praxis retest finds name-resolvable shared-dir failure and false durable-reference PARTIAL; current exact OpenCode DB rows are absent for w401/w402; no cleanup mutation performed.
