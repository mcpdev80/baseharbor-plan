# 0428-206 independent review — round 3

## Verdict: ACCEPT the corrected diagnostic scope

The card's original 89-case denominator is not supported by the available source rows. The round-2 dossier establishes the neutral hosted cohort from run `44850031032` and enumerates its first-level cases from cli-0..3.

Independent checks on the published evidence:

- Parsed the §2.1 Markdown table: 117 rows and 117 distinct test names.
- The dossier's category counts sum to 117: 97 direct gate + 7 gate evidenced by subtests + 9 other causes + 1 other cause evidenced by a subtest + 3 rows with only run markers.
- The three rows without a hosted failure block are explicitly identified as evidence gaps; no cause is invented for them.
- The historical 89 count is explicitly reconciled as an unsupported cohort, rather than silently carried forward.
- This is a read-only diagnosis. No product changes or PRs are required; the separately routed product defects remain with their own cards.

The acceptance text was corrected to match that measured cohort. The result is accepted as a diagnostic inventory, not as a claim that every listed product test is fixed.
