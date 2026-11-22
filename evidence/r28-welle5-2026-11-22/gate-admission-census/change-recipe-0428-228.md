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
