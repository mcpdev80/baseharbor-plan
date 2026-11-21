# 0428-143 / PR #1729 — exact-head closeout

- Exact PR head: `f979d7664faa782bd31043ee92bf9988dd1341a7`.
- Exact hosted run: [44891055506](https://github.com/mcpdev80/baseharbor/actions/runs/44891055506), SUCCESS.
- Regression: `internal/metrics.TestVerifyApplicationSourceVerificationNoneIsSkipped`.
- Mapped gate: `PR · Go unit · packages`, job `136806771816`, SUCCESS; auto-discovered package test route.
- Aggregate `PR Selected Checks`, job `136808161539`, SUCCESS; all required checks passed.
- PR #1729 merged normally at 2026-11-21T09:51:51Z as `53f16a81f23a366fff8305dfd7743e34ac3ef943`.
- The verifier now applies the `Verification=none` rule consistently to application-class sources. The stacked stale-target follow-up #1730 remains open and has been retargeted to `develop` for separate exact-head validation.
