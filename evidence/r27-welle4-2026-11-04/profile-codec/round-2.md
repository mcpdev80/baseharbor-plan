## PLAN — w113-codec-r2 (t-20261018-r27-profile-codec round 2)

- Read mission + review-1363a fully; confirm candidate head 0eb8f231, base develop bb9bc0ef, PR #1363 draft
- Recipe 1: store.go bind every imported/exported record to canonical version + normative schema + installation/recipient/scope/trust as store input; reject before side effects; reject credential-bearing URLs / secret material in all serialized fields incl recipient/dest path
- Recipe 2: decode with unknown-field rejection (incl nested) OR lossless documented forward-compat; adversarial tests with real secret canary + unknown future field; assert no secret in export bytes
- Recipe 3: canonical container format + real import->export round-trip; pin field/record ordering in regression; golden follows canonical representation
- Recipe 4: transactional atomic write; partial-write leaves nothing behind; conflict-replace verifies previous record actually replaced (not just Replaced==1)
- Recipe 5: update docs/spec/credential-access-v1.md AND docs/de/spec/credential-access-v1.md so payload/envelope semantics + outer container schema match the implemented model exactly
- Recheck all seven probes (secret, unknown-field, bad-version, wrong-installation/recipient/scope, canonical round-trip, partial-write, conflict-replace) + package tests, build, vet, gofmt
- Local commit isolated branch; prepare exact-SHA handoff; keep draft; report gates as STATE not green without observed terminal run

END at f49a3303 pending.
