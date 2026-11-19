# Independent read-only review — PR #1690 / 0428-119

Reviewed 2026-11-19.

- Head: `184eefde9b84ff7d6bfb3dc0017989a2143ddede`
- Base at review: `1019190d8dc0ecac7693f3461153e76be0e2cb8a`; current `develop` had advanced to `558dc42d0c8c9d798fcdf5938be2ea14e432b754`.
- Exact-head run `44563139929` passed unit/build/vet and the required aggregate, but Docker lifecycle, Podman, and coreless runtime gates were skipped. PR is behind current develop.
- No repository edit, PR comment, or merge was performed by this review.

## Finding

**Consent equivalence ignores registry contents.** `ConsentAuthority.Equivalent` calls `equalRegistry`, but `equalRegistry` (`provider_consent_authority.go:432-440`) compares only `len(Instances)` and `len(Bindings)`. Same-cardinality provider, binding, or ownership mutations can therefore be considered equivalent, despite `BuildConsentAuthority` storing the registry contents. Compare canonicalized values or a deterministic digest and add tests that mutate registry entries without changing cardinality. Related incomplete comparisons observed: `Released` is not compared; `Ancillary` is compared by length only; Consumers/Activity map lengths are not checked; `equivalentImpact` omits `After`.

The card already records that runtime acceptance is blocked because the exact-head Docker lifecycle gate was skipped pending the approved ORAS/CI owner route. This review adds a code-correctness blocker; neither skipped runtime evidence nor stale-base CI supports a merge.
