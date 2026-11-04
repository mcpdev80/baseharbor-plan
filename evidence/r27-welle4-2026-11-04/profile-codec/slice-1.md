# Slice 1 — w88 / r27-profile-codec

Worker lane w88, task `t-20261018-r27-profile-codec` (owner: coord-welle4, lane w88).
Coordination session: f49a3303-e8bb-491b-9e2c-b629783c4e5f.

## PLAN checklist (bullets, no checkboxes)

- Read mission `coordinator/missions/w88-profile-codec.txt` and card `tasks/t-20261018-r27-profile-codec.md` + predecessor `t-20261018-r27-profile-contract` (accepted, PR #1324).
- Confirm base: `baseharbor` repo at `3d08ef72` (develop HEAD); profile-contract `9a57107f` already merged into develop and reachable from my branch.
- Fix the product surface: `contracts/managementaccess/v1` defines `ManagementAccessProfile` (3 kinds) and the fail-closed import boundary. Built on it.
- Build a bounded codec + store package: `contracts/managementaccess/v1/store.go` (export excludes secrets, import validates version/trust/installation/scope before writing, transactional import, explicit conflict handling, local path remap destination-local).
- Golden fixture + positive/negative component tests: wrong version/trust => no write; export carries no secret; conflict => explicit decision, no silent overwrite; round-trip/tamper/partial-write/secret-exclusion/wrong-installation.
- Ran smallest matching gates: `go build ./...`, `go vet ./...`, `gofmt -l`, focused package tests — all green. No CLI registration. No push to develop.
- Documented repo-rule compliance under ## repo-rule compliance.
- Local commits on branch `work/w88-profile-codec-isolated`; preparing handoff to coord f49a3303.

## Repo-rule compliance

- Write-set: `contracts/managementaccess/v1/store.go` + `store_test.go` + `store_testseams_test.go` + `store.golden.json` only. No CLI registration, no shared indexes/registrations, no edit of another slice's files, no use of another slice's draft branch.
- Contract precedence: the accepted `management-access/v1` wire record (kind enum, version marker `baseharbor.management-access/v1`, `import.failClosedImport`, storage/sensitivity, `export` AES-256-GCM/12-byte nonce) is the authority the codec encodes/decodes. No new interface paths invented.
- Secret exclusion by default on export; version/trust/installation/scope checked before any write; transactional import; explicit conflict resolution (no silent overwrite); local path remap is destination-local.
- Note: this workspace is a shared git repo across lanes; the working tree is periodically reset by other lanes. Work is committed incrementally to an isolated branch `work/w88-profile-codec-isolated` to survive resets.

## Handoff / END line

- END an f49a3303: `END_DONE w88-profile-codec: head=<sha10> pr=<n> tests=<pakete> rotfirst=belegt lsremote=<sha10> | <Satz>`

## END_DONE

w88-profile-codec: head=73a75b5e8c pr=0 (local branch, DRAFT, no develop push) tests=contracts/managementaccess/v1 (all green) rotfirst=belegt (wrong version/trust => no write, export no secret, conflict => reject, round-trip/tamper/partial-write verified) | bounded profile codec + store on accepted management-access/v1: export carries no secrets, import validates version/trust/scope before any write, transactional import with explicit conflict handling, local path remap destination-local; no CLI registration; all gates green; committed to isolated branch work/w88-profile-codec-isolated awaiting coord PR guidance.
