# Open PR sweep continuation — 2026-11-19

This is a point-in-time coordination record for the Maintainer-directed continuation of the open-PR sweep. It does not accept or close any product task. Product PR state and Codeman lane ownership must be rechecked before each action.

## GitHub snapshot

A fresh GitHub open-PR search at 2026-11-19 21:47 UTC returned 28 open PRs: #1704, #1702, #1697, #1695, #1693, #1690, #1684, #1665, #1650, #1645, #1627, #1625, #1623, #1620, #1615, #1614, #1606, #1597, #1596, #1595, #1594, #1591, #1588, #1587, #1585, #1582, #1580, and #1578.

Previously completed in this sweep: #1589 merged (`ab77e29d7c1cf981777e1069e51dfff82ffcf654`, exact run `44617085771` passed); #1705 merged (`28fb427f057499efca705c1b7459e7653bd532a8`, exact run `44619193702` passed); #1649 closed without merge as superseded by stronger current-develop coverage. See `../pr-inventory/follow-up-1649.md` for its evidence.

## Codeman ownership snapshot

Read-only host observation at 21:47:37 UTC: coordinator `9142ab1f` busy; pool 5/5, no free seats. #1693 / 0428-123 (`129c8528`) at `93eea495`, run `44621626037` in progress; #1704 / 0428-073 (`349c97ee`) at `f5dcf128`, run `44621875256` in progress; #1702 / 0428-142 (`453b8792`) at `6740299f`, exact run `44621032956` succeeded and worker is in closeout; #1684 / 0428-083 (`e01fcb6d`) remains active. The new 0428-151 worker (`ba3ab78a`) is fixing the reproduced retention path in `internal/application/provider_registry.go:278` and its tests; no PR exists yet. 0428-152 waits on #1702 due shared `cmd/baha/app_status_collect.go`. The #119 lane is reported to own `internal/application/provider_consent_authority.go`; its current worker pane could not be identified. No Codeman state was changed.

## Independent draft audits

Read-only audits compared PRs, current `develop` (`28fb427f`), canonical plan main, dependencies, and exact-head runs. Findings do not constitute task acceptance.

- #1588, #1587, #1585, #1582, #1580, and #1578 each contain unique changes absent from `develop`; none is a safe duplicate/superseded closure. The first four retain explicit wait/frost or owner/release dispositions; #1578 is an upstream CLI2 prerequisite and #1580 depends on it. Their old successful exact-head CI runs predate current `develop` and require refreshed checks after any approved hop. The #1587 physical smoke remains outstanding.
- #1591, #1594, #1595, #1596, and #1597 also contain unique implementation required by active dependency chains. #1594 and #1596 have plan cross-link gaps and bases behind current #1591; #1597 is still `wait`, stale, and needs scope reconciliation. No task was safe to close as duplicate or superseded.
- #1695 overlaps active metrics work and remains sequenced behind 0428-121; its earlier review found two CLI-output issues and its exact CI is stale. Do not edit alongside #1693.
- #1690 remains blocked on its exact-head Docker lifecycle witness. #1606 is not a duplicate of #1650; it has unique dashboard files. Both remain within the coordinator-owned/blocked 0428-078 area.

All unmerged PRs remain open pending their owners, dependency resolution, fresh exact-head evidence, or an explicit disposition. This record does not authorize merging frozen drafts, changing their task scope, or modifying Codeman lanes.
