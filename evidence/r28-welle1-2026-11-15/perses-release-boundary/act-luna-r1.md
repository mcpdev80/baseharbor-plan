# CODEX-REVIEW — PR #1577

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-release-boundary`  
**Candidate:** `5e8d138cd659cbd7a72fde4713b3b1389b95dcdb`  
**Exact-head CI:** run `43794816481`, COMPLETED SUCCESS, exact SHA; docs-only source/routing gates passed.  
**Scope:** SHA-exact docs diff against develop `14d8f17d1aa61496db9ed4d57bd4c22eda34ae95`; 12 files, docs-only; `git diff --check` clean. Current r6 prose names the states and points to the normative spec; the earlier r5 exact-copy concern was superseded by the r6 scope documented in lane evidence.

## Verdict: REQUEST CHANGES

The six mirrored release/reference/how-to passages say state may be `not_configured`, `configured_unverified`, or `verified` “depending on selected, pinned and reachable.” That paraphrase omits the spec’s required real health probe for `verified` and can imply reachability alone is sufficient. The card is intended to keep release prose non-normative and defer state semantics to the spec.

## Recipe

- **Files/change:** English/German release notes, reference, and how-to mirrors changed by this PR; reduce the sentence to state-name mention plus the pointer to `docs/spec/management-access-v1.md`, or explicitly include the real health-probe condition consistently with the spec. Avoid introducing a competing shorthand definition.
- **Tests:** docs consistency/search check across all six mirrors, `git diff --check`, and exact-head docs CI.
- **Stop:** stop if a wording change would redefine state semantics differently from the normative spec; update the spec first under its owning contract.

Read-only review; no merge performed.
