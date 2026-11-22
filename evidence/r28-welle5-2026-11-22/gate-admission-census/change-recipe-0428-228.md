# 0428-228 change recipe — admit the operator seam sources to the data-capabilities gates

Owner decision requested: `scripts/**` is Owner scope for lanes (AGENTS write bans), so this recipe is written to be
applied verbatim by the Owner, or by a lane the Owner explicitly authorises for this write set. Nothing here is
executed by a product lane.

## Measured trigger

Candidate PR #1753 head `f29bf6fa303718ee258f4edd40a62dbbecd37f77` (base `develop` `82825e95a6f6083702d0ba5401d97f356085c722`)
changes exactly two files:

- `cmd/baha/ci_integration_operator_enabled.go`
- `cmd/baha/ci_integration_operator_enabled_test.go`

At that run `44982699457` the job `PR · Selected Runtime` is **SKIPPED**, while card 0428-227 acceptance requires the
Docker `data-capabilities` gate to pass on the exact candidate. The reason is a path→gate registration gap, not a
product defect: both mapping tables below were reviewed and neither contains the seam sources.

## Edit 1 — `scripts/pr-gate-plan.py`

The reviewed map ends at the entries shown here (current file, develop `82825e95a6f`):

```
    'cmd/baha/app_footprint_show.go': ('wizard-footprint-command-tests', ()),
    'cmd/baha/app_footprint_show_test.go': ('wizard-footprint-command-tests', ()),
    'cmd/baha/app_machine_adapters.go': ('wizard-machine-adapter-tests', ()),
    'cmd/baha/app_machine_adapters_test.go': ('wizard-machine-adapter-tests', ()),
}
```

Insert, before the closing brace, one entry per seam source file (the three `ci_integration_operator*` sources found by
the H-V32 census, plus the test sources so a test-only change still selects the gate):

```
    'cmd/baha/ci_integration_operator_enabled.go': ('ci-integration-operator-seam-tests',
                                                    ('atomic/docker/data-capabilities',
                                                     'atomic/podman/data-capabilities')),
    'cmd/baha/ci_integration_operator_enabled_test.go': ('ci-integration-operator-seam-tests',
                                                         ('atomic/docker/data-capabilities',
                                                          'atomic/podman/data-capabilities')),
```

Note the shape difference to the neighbours: `app_machine_adapters.go` is mapped to an **empty** gate tuple in this
file and carries its gates only in Edit 2 — so both files must be edited, or the two paths disagree.

## Edit 2 — `scripts/pre-release-runtime-impact.json`

Inside the `"core"` object (current entries at lines 30-31 are the two `app_machine_adapters*` paths):

```
    "cmd/baha/ci_integration_operator_enabled.go": ["atomic/docker/data-capabilities", "atomic/podman/data-capabilities"],
    "cmd/baha/ci_integration_operator_enabled_test.go": ["atomic/docker/data-capabilities", "atomic/podman/data-capabilities"],
```

## Edit 3 — selector tests (hosted, no new CI trigger needed)

- `scripts/test_pr_gate_plan.py` is the owner test for Edit 1. Add one assertion per path that resolving a diff that
  contains only `cmd/baha/ci_integration_operator_enabled.go` (and the `_test.go` variant) yields both
  `atomic/docker/data-capabilities` and `atomic/podman/data-capabilities`. It already references the impact JSON once,
  so extend the same test rather than adding a new file.
- `scripts/test_pre_release_runtime_reuse.py` covers the JSON consumer (`pre-release-runtime-reuse.py` reads the file
  three times); add the pairing assertion that every `"core"` key that names a `cmd/baha/*.go` path also appears in the
  `pr-gate-plan.py` map with the same gate tuple. That single test is what stops the two tables from drifting again —
  the drift is what hid 0428-227.
- Both tests run inside the existing `ci-fast-check` / focused-Python group, so hosted CI executes them without any
  `.github/**` change.

## Sequencing

1. Apply Edits 1-3 on top of `develop` `82825e95a6f` (its own PR, card 0428-228).
2. Merge that PR.
3. Hop PR #1753 onto the new develop and rerun: `PR · Selected Runtime (atomic/docker/data-capabilities, docker,
   data-capabilities)` must then be **executed**, not skipped; card 0428-227 is accepted only on that witness.

Do not accept 0428-227 while the runtime job is skipped: a skipped gate is never evidence.

## Extension measured for PR #1750 (same admission gap, second victim)

Reviewer handoff at exact head `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99` (base develop `82825e95a6f`, PR ready): run
`44982566548` completed/success with `PR Selected Checks` = **success** (job `137087212830`, all six "require …"
steps success), but `PR · Selected Runtime` = **SKIPPED** (job `137086100059`) and `PR · Native` = skipped
(`137086081200`). The verdict is therefore REQUEST CHANGES on admission grounds, not on code: the runtime-consent
behaviour this PR fixes is only observable inside a runtime gate, and no gate was selected.

Cause measured: the candidate changes only test sources -
`cmd/baha/test_operator_context_test.go`, `cmd/baha/application_lifecycle_lock_test.go`,
`cmd/baha/app_init_source_neutral_test.go`, `cmd/baha/app_init_wizard_test.go`, `cmd/baha/repository_up_init_test.go`,
`cmd/baha/runtime_integration_test_support_test.go`, `cmd/baha/app_perses_host_containers_cli_test.go`,
`cmd/baha/app_perses_infra_dashboards_cli_test.go` - and the reviewed path→gate map in `scripts/pr-gate-plan.py`
carries no entry for them, so they fall through to the unmatched default (`scripts/pr-gate-plan.py:1344`).

Same two-file rule as above: add these paths with the gates their behaviour needs -
`atomic/docker/data-capabilities` + `atomic/podman/data-capabilities` for `test_operator_context_test.go` and
`application_lifecycle_lock_test.go`, and `atomic/docker/guided` + `atomic/podman/guided` in addition for the four
init/dashboard test sources - and mirror every entry in `scripts/pre-release-runtime-impact.json` under `"core"`.
The pairing assertion in `scripts/test_pre_release_runtime_reuse.py` then makes the drift impossible for future PRs.

## Handoff state

- Card 0428-228 (this recipe) is `active`, owner = Owner, because `scripts/**` is Owner scope for lanes.
- Card 0428-221 (PR #1750) is set to `wait` with the dependency named, not `blocked`: no decision is missing from the
  Owner beyond applying this recipe.
- Card 0428-227 (PR #1753) stays `review`: content approved, acceptance withheld until this recipe lands and the
  runtime job is executed at the hopped head.
