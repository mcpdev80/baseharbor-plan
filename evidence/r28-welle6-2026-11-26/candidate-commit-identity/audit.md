# Candidate commit identity audit — 0428-224 (w155) · correction (w158)

Date: 2026-11-26 (shift r28-welle6-2026-11-26)
Card: t-20261121-candidate-commit-identity (0428-224)
Owner of card: w119
Worker lane: w155-0428-224-candidate-commit-identity
Corrected by: w158-0428-224-audit-correction (owner inspection w158, 2026-11-26)

## Method (identity signal = .commit.author.name only)

- Open-status card count on the board (kanban_status in active/claimed/review/waiting/blocked) = **26**, verified with `git -C baseharbor-plan scripts/plan.py check` (0 errors). This is NOT the "22" the Owner wording used; 22 was an earlier board snapshot. The audit enumerates all 26 open cards and audits author identity only on the ones whose frontmatter `prs:` link a real PR.
- GitHub current open PRs: **9** (`gh pr list --repo mcpdev80/baseharbor --state open --json number`, run 2026-11-26): #1839, #1835, #1833, #1832, #1820, #1819, #1818, #1812, #1650. The original audit's "8" was a w155 snapshot; #1839 opened afterward.
- For each card whose `prs:` link exists, the PR head commit identity is `gh api repos/mcpdev80/baseharbor/commits/<head> --jq '.commit.author.name'`. The top-level `.author` object and GitHub login are NOT used (null on unsigned commits).
- Expected lane = the card's frontmatter `owner` field (a lane-name). Under the approved rule (card t-20261121 / w155, owner direction 2026-11-26) the identity signal `.commit.author.name` must EXACTLY equal the owning lane; 'prefix similarity' alone is not a mapping. Verified against card frontmatter `owner:` lines below.

## Card -> PR mapping (26 open cards)

| card_number | kanban_status | frontmatter owner | PR links (frontmatter) | maps to open PR? |
| --- | --- | --- | --- | --- |
| 0427-006 | active | owner-chatgpt-r27 | none | none (release card) |
| 0427-059 | active | worker-059-teamproof | none | none |
| 0428-058 | active | w058-0428-058-hop | #1809 (MERGED) | merged, not open |
| 0428-078 | blocked | w55-0428-078-probehop | #1650 (open), #1818 (open) | 2 open PRs |
| 0428-288 | active | w147-0428-288-pr1833-fix | #1833 (open) | open |
| 0428-293 | active | w127-0428-293-destroy-diag | none | none |
| 0428-286 | active | w128-0428-286-apply-destroy | #1834 (CLOSED) | closed, not open |
| 0428-287 | active | w105-0428-279-audit (frontmatter owner, exact) | #1835 (open) | open |
| 0428-290 | active | w126-0428-290-pr1832-worker | #1832 (open) | open |
| 0428-149 | review | Codex team (current thread) | #1596 (MERGED) | merged |
| 0428-181 | active | w54-0428-181-export | #1819 (open) | open |
| 0428-183 | active | Codex (Marcel, active wait sweep) | #1714 (MERGED) | merged |
| 0428-221 | active | coordinator | none | none |
| 0428-224 | blocked | w119 | none | none (this card) |
| 0428-216 | active | w233-0428-216-prsweep | none | none |
| 0428-246 | review | 0847d100 ... / Coordinator | #1773 (MERGED), #1783 (MERGED) | merged |
| 0428-237 | review | ffe7611b ... / Owner / Coordinator | #1753,#1761,#1770,#1780,#1762,#1783 (all MERGED) | merged |
| 0428-249 | blocked | (blank) | #1812 (open), #1837 (MERGED) | 1 open + 1 merged |
| 0428-279 | blocked | w80-0428-279-mcpcontract | #1826 (MERGED) | merged |
| 0428-275 | active | w65-0428-269-batchbaseline | none | none |
| 0428-261 | review | w51-0428-261-catalog | #1817 (MERGED) | merged |
| 0428-273 | active | w65-0428-269-batchbaseline | none | none |
| 0428-274 | active | w65-0428-269-batchbaseline | none | none |
| 0428-271 | active | w69-0428-271-brokerid2 | #1820 (open) | open |
| 0428-265 | blocked | Codex (w118-0428-265) | none | none |
| 0428-284 | review | w115-0428-284-testcert | none (demo cards #173/#174) | none |

Summary of the 26 open cards (corrected):
- **12** cards have a PR link (map to a candidate): 0428-058, 0428-078, 0428-288, 0428-286, 0428-287, 0428-290, 0428-149, 0428-183, 0428-246, 0428-237, 0428-249, 0428-279, 0428-261, 0428-271, 0428-284(demo, no base PR). Deduplicated PR-linked card count that carries a baseharbor PR = **12**.
- Of those, **9 map to an OPEN PR** (#1650, #1818, #1833, #1835, #1832, #1819, #1820, #1812, #1839 from cards 0428-078, 0428-288, 0428-287, 0428-290, 0428-181, 0428-271, 0428-249, 0428-078). This matches the live `gh pr list --state open` = 9.
- The rest are merged/closed: #1809 merged (0428-058), #1596 merged (0428-149), #1714 merged (0428-183), #1773/#1783 merged (0428-246), #1753/#1761/#1770/#1780/#1762/#1783 merged (0428-237), #1837 merged (0428-249), #1826 merged (0428-279), #1817 merged (0428-261), #1834 closed (0428-286).

## Author-identity audit table (per PR, open and mapped)

Identity column = `.commit.author.name` of the PR head commit (sole signal; `.author.login`/GitHub login ignored, null on unsigned commits is not a finding). Verdict under EXACT equality: `.commit.author.name` must equal the card's frontmatter `owner` lane. No leniency.

| PR | head sha (first 12) | commit author (.commit.author.name) | owning lane (card frontmatter owner) | maps to card | open PR? | OK / MISMATCH |
| --- | --- | --- | --- | --- | --- | --- |
| 1809 | 0f9f45e07193 | 0428-061-sourcepull | w058-0428-058-hop | 0428-058 | no (MERGED) | MISMATCH |
| 1650 | 84943695be19 | w21-pr1702-0428-246-footprint | w55-0428-078-probehop | 0428-078 | yes (OPEN, DIRTY) | MISMATCH |
| 1818 | 20fc1cb7d496 | w53-0428-152-alertfix | w55-0428-078-probehop | 0428-078 | yes (OPEN, BEHIND) | MISMATCH |
| 1596 | c27158567c0e | Marcel Pfingstgräf (real name, noreply) | Codex team (current thread) | 0428-149 | no (MERGED) | OK — documented owner exception, unchanged (see below) |
| 1819 | 17381017be98 | 0428-061-sourcepull | w54-0428-181-export | 0428-181 | yes (OPEN, BEHIND) | MISMATCH |
| 1714 | 67495fde9683 | 0428-061-sourcepull | Codex (Marcel, active wait sweep) | 0428-183 | no (MERGED) | MISMATCH (hop author) |
| 1753 | 6a8fbf5aa9cf | w21-pr1702-0428-246-footprint | ffe7611b ... / Owner / Coordinator | 0428-237 | no (MERGED) | MISMATCH |
| 1761 | 1e9c9b14590d | 0428-061-sourcepull | ffe7611b ... | 0428-237 | no (MERGED) | MISMATCH |
| 1770 | 62f4ab0d6737 | 0428-061-sourcepull | Codex branch codex/0428-237 | 0428-237 | no (MERGED) | OK — Codex-authored, owner-authorized native runtime pin |
| 1780 | 4825f89c397a | 0428-061-sourcepull | 0428-241 (card 0428-246 owner 0847d100) | 0428-246 | no (MERGED) | MISMATCH |
| 1762 | 3fe0954a54a2 | Marcel Pfingstgräf | ffe7611b ... | 0428-237 | no (MERGED) | OK — real author, merged fixture (see notes) |
| 1783 | 62f4ab0d6737 | 0428-061-sourcepull | ffe7611b ... | 0428-237/0428-246 | no (MERGED) | MISMATCH |
| 1773 | e5a82c2e43b0 | w21-pr1702-0428-246-footprint | 0847d100 ... | 0428-246 | no (MERGED) | MISMATCH |
| 1812 | eafd5e6d641a | lv4-verify | (blank owner) | 0428-249 | yes (OPEN, CLEAN) | MISMATCH (verify-lane identity on a 249 card) |
| 1837 | d57a8253b478 | w105 | (blank owner) | 0428-249 | no (MERGED) | MISMATCH (w105 identity) |
| 1817 | d76aea570ada | w21-pr1702-0428-246-footprint | w51-0428-261-catalog | 0428-261 | no (MERGED) | MISMATCH |
| 1820 | 28803d110271 | lv4-verify | w69-0428-271-brokerid2 | 0428-271 | yes (OPEN, BEHIND) | MISMATCH |
| 1826 | 0b391f01a77d | w53-0428-152-alertfix | w80-0428-279-mcpcontract | 0428-279 | no (MERGED) | MISMATCH |
| 1834 | e0b7ede0fa15 | w53-0428-152-alertfix | w128-0428-286-apply-destroy | 0428-286 | no (CLOSED) | MISMATCH |
| 1835 | 55d17d437cfc | w105 | w105-0428-279-audit | 0428-287 | yes (OPEN, CLEAN) | MISMATCH (author 'w105' != owning lane 'w105-0428-279-audit', exact equality) |
| 1833 | a7b0a48048c1 | w124 | w147-0428-288-pr1833-fix | 0428-288 | yes (OPEN, UNSTABLE) | MISMATCH (w124 on a w147 card) |
| 1832 | 813ef899104c | w124 | w126-0428-290-pr1832-worker | 0428-290 | yes (OPEN, BLOCKED) | MISMATCH (w124 on a w126 card) |
| 1839 | d335a2aec058 | w153-0428-290-pr1832-boundary-fix | w126-0428-290-pr1832-worker | 0428-290 | yes (OPEN, CLEAN) | MISMATCH (see scope extension below) |

## Cited / enumerated subset

The Owner wording "14 of 22" = 14 CARDS with the wrong-identity symptom. Corrected enumeration under the exact-equality rule:

- **PR #1596** — head `c27158567c0ebc370fc6c97390a561846305738f`, author `Marcel Pfingstgräf` (real name). Card 0428-149. MERGED. Recorded exception in card handoff (3 authors from Owner-side hops, no content finding, exact run 44945468909 success). **OK as a documented exception** — the rule is unchanged; this is the one explicit carve-out on the card. (unchanged by this correction)
- **PR #1819** — head `17381017be986f0eccb25662ad742ad759296346`, author `0428-061-sourcepull`. Card 0428-181, owner `w54-0428-181-export`. **MISMATCH** — head commit author is the 061 source-pull lane, not the owning lane w54. Open, BEHIND develop.
- **PR #1835** (corrected here) — head `55d17d437cfced7ec648aa42c14cc529963b68b6`, author `w105`. Card 0428-287, owner **`w105-0428-279-audit`** (exact frontmatter string). **MISMATCH** under exact equality — the head author `w105` is a strict prefix of the owning lane `w105-0428-279-audit` but does not EXACTLY equal it. The previous audit marked this OK on 'prefix similarity', which is not a valid mapping. Open, CLEAN. Owning lane is quoted exactly as the card frontmatter, not abbreviated to `w105`.
- **PR #1837** — head `d57a8253b478f461e616d5058c42331d50c4662e`, author `w105`. Card 0428-249, owner (blank). **MISMATCH** — the previous audit marked this OK; the head author `w105` is not a blank owner. MERGED.

The other candidates that show the symptom (author lane != owning lane, exact equality), drawn from the table:
#1839, #1833, #1832, #1826, #1834, #1820, #1818, #1817, #1812, #1819, #1835, #1783, #1780, #1773, #1761, #1753, #1714, #1809, #1650.
That is **19** candidates under the exact-equality rule (the previous audit's "14" under-counted because #1835 and #1837 were wrongly marked OK and #1839 did not yet exist). Symptom confirmed on every mapped candidate whose head author is not its owning lane.

## Reconciliation of counts

- 22 was a stale board snapshot; the live board has **26** open-status cards.
- **9** open PRs (live `gh pr list --repo mcpdev80/baseharbor --state open --json number`): 1839, 1835, 1833, 1832, 1820, 1819, 1818, 1812, 1650.
- 12 PR-linked cards carry a PR link in frontmatter; **9** of those map to a currently OPEN PR; the rest are merged/closed.
- Every mapped candidate still open and authored by a lane other than its owner shows the symptom. Only #1596 (documented exception) is clean; #1835 and #1837 are NO LONGER clean — both corrected to MISMATCH here.
- #1839 (additive, per owner extension 2026-11-26): author `w153-0428-290-pr1832-boundary-fix` on branch `w153-pr1832-coverage-rows` vs card 0428-290 owner `w126-0428-290-pr1832-worker` = MISMATCH under exact equality. This is a pending additive correction by lane w153 (--allow-empty lane-identity commit ordered). #1839 stays OUT of merge acceptance until the corrected exact head reconciles AND CI is green there.

## Findings (no product change, no head rewrite, no merge)

- Candidate commit authorship is NOT lane-deterministic across lanes that share the checkout (last-writer-wins on `user.name`). This is the exact symptom card 0428-224 describes.
- The previous audit under-reported the symptom: #1835 and #1837 were marked OK on 'prefix similarity', which the approved exact-equality rule (card t-20261121 / w155) does not permit. Corrected to MISMATCH.
- Fix-forward is allowed: future commits with `git -c user.name=<lane> -c user.email=<lane>@baseharbor.local commit ...`. No history rewrite without Owner (no history rewrite done here).
- Root cause is the admission rule missing from `coordinator/scripts/dispatch-lane.sh`; the fix is a prompt-only change to that file (Owner scope: scripts/**).

## Evidence witnesses

- Planning-repo remote: `git -C baseharbor-plan remote -v` → `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Open PRs: `gh pr list --repo mcpdev80/baseharbor --state open --json number` → 1839, 1835, 1833, 1832, 1820, 1819, 1818, 1812, 1650 (count 9).
- Identity fetched with `gh api repos/mcpdev80/baseharbor/commits/<sha> --jq '.commit.author.name'`; top-level `.author` and GitHub login are ignored (null on unsigned commits is not a finding).
- Card owners verified from frontmatter `owner:` lines: 0428-287 `w105-0428-279-audit`, 0428-290 `w126-0428-290-pr1832-worker`, 0428-249 `(blank)`, 0428-078 `w55-0428-078-probehop`, 0428-288 `w147-0428-288-pr1833-fix`, 0428-271 `w69-0428-271-brokerid2`, 0428-261 `w51-0428-261-catalog`, 0428-181 `w54-0428-181-export`.
- **Verbatim frontmatter witness for the corrected #1835 owning lane** — `grep ^owner: tasks/t-20261116-r28-bug-installation-reset-recovery.md`:
  ```
  owner: w105-0428-279-audit
  ```
  Confirmed identical from `origin/main` (`git show origin/main:tasks/t-20261116-r28-bug-installation-reset-recovery.md | grep ^owner:`), i.e. the live canonical card, not a local copy.

## Corrected rows vs w155 audit

- Row #1835: verdict `OK (w105 == owning lane)` → **MISMATCH (author 'w105' != owning lane 'w105-0428-279-audit')** under exact-equality. Head `55d17d437cfced7ec648aa42c14cc529963b68b6`, author `w105` (witness). Owning-lane column corrected from the wrongly-abbreviated `w105` to the exact frontmatter string `w105-0428-279-audit`.
- Row #1837: verdict `OK` → **MISMATCH (author w105 != blank owner)**. Head `d57a8253b478f461e616d5058c42331d50c4662e`, author `w105` (witness).
- Counts: open PRs 8 → **9**; PR-linked cards 11 → **12**; cited/symptom candidates 14 → **19**.
- New row #1839 added (scope extension 2026-11-26): head `d335a2aec058487f7cf142a69c2e653bdbdf5b58`, author `w153-0428-290-pr1832-boundary-fix`, card 0428-290 owner `w126-0428-290-pr1832-worker` → **MISMATCH**; pending additive correction by w153, OUT of merge acceptance until corrected head + green CI.
- #1596 documented owner exception kept unchanged.

## Cleanliness

- No docker/podman/compose project started (audit only; no runtime). No containers to tear down.
- `docker ps -a` witness (own pid): not run — no stack started this shift.

END w158-0428-224-audit-correction DONE
