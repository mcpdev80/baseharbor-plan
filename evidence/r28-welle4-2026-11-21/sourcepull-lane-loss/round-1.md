# Lane loss record: 0428-216-sourcepull (card 0428-061, `app pull` guided source pull)

Recorded by the coordinator on 2026-11-21, because `worker-cleanup.sh` requires a published lane
evidence path and this lane produced none. This file is the evidence of a **loss**, not of work.

  - lane: `0428-216-sourcepull`, session `12c9bf4f-608a-480d-a447-2d2a62c6fb21`, model channel ornith
  - missions delivered: `coordinator/missions/0428-061-sourcepull.md` (three deliveries: initial, after a
    transcript-echo report, and after a second echo)
  - payload gate: exit 0 for every delivery (`coordinator/scripts/payload-gate.py`)
  - published artefacts measured: `git ls-remote lane-origin 'refs/heads/*0428-061*'` -> 0 lines;
    `git ls-tree -r origin/main -- evidence | grep -c '0428-061\|sourcepull'` -> 0; no PR for the card
  - both END/QUESTION reports the session produced were verbatim echoes of the coordinator's own prompt
    text from the pane view, not a delivery
  - disposition: seat rotated, card 0428-061 stays `planned`, no claim was ever published by this lane
  - known tooling defect that hid this for two reports: `spawn-lane.sh` does not seed
    `workers/todos/<lane>.json` (codeman-coordinator-tooling issue #23), and the lane's todo file was
    unreadable (`Expecting ',' delimiter: line 2 column 1 (char 1004)`) in the 18:5xZ basics-check run

Next action for the coordinator: re-dispatch 0428-061 on a fresh lane when a seat is free; the card has
no dependency on the lost work.
