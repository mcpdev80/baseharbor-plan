# PR #1812 scope review before acceptance (head 3859d46634899f31530513c63d99310a21ce0d76)

## Facts (remote witnesses)
- Diff files: `.github/workflows/pre-release-runtime-suite.yml` (authorized 0428-249 area: suite order/registry + image refs) AND `scripts/release-requirements.json` (scripts/** = owner scope; NOT named in the card contract).
- JSON change semantics: adds `v0.4.28` while KEEPING `v0.4.27` at many gates (superset).
- Owner decision text: `v0.4.27 entfernen, v0.4.28 fuehren` (remove 0.4.27, carry 0.4.28) - the diff CONTRADICTS the 'remove' half.
- Prior gateplan failure (45504224635): ONLY_GATES vocabulary mismatch remains unresolved.

## Disposition
- No acceptance, no merge until: (a) gate-plan ID issue fixed within the workflow file (zero-code preferred), (b) scripts/release-requirements.json is EITHER brought into line with the owner decision (v0.4.27 removed) under an explicit owner-scope authorization on THIS card, OR moved out into a separate tracked change.
- Scope-deviation documented here BEFORE any acceptance per contamination-first rule.
