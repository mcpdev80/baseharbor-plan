# Candidate commit identity audit — 0428-224 (w155)

Date: 2026-11-26 (shift r28-welle6-2026-11-26)
Card: t-20261121-candidate-commit-identity (0428-224)
Owner of card: w119
Worker lane: w155-0428-224-candidate-commit-identity

## Method (identity signal = .commit.author.name only)

- Open-status card count on the board (kanban_status in active/claimed/review/waiting/blocked) = **26**, verified with `git -C baseharbor-plan scripts/plan.py check` (0 errors). This is NOT the "22" the Owner wording used; 22 was an earlier board snapshot. The audit enumerates all 26 open cards and audits author identity only on the ones whose frontmatter `prs:` link a real PR.
- GitHub current open PRs: **8** (verified `gh pr list --repo mcpdev80/baseharbor --state open`). Owner wording "8" is correct.
- For each card whose `prs:` link exists, the PR head commit identity is `gh api repos/mcpdev80/baseharbor/commits/<head> --jq '.commit.author.name'`. The top-level `.author` object and GitHub login are NOT used (null on unsigned commits).
- Expected lane = the card's frontmatter `owner` field (a lane-name). The headRef lane of each PR is recorded; the identity signal is the commit author string, which is compared against the owning lane's identity pattern.

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
| 0428-287 | active | w105-0428-279-audit | #1835 (open) | open |
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

Summary of the 26 open cards:
- 11 cards have a PR link (map to a candidate).
- Of those 11, **6 map to an OPEN PR** (#1650, #1818, #1833, #1835, #1819, #1820 from 0428-078/#1; plus #1832, #1834-closed, #1837-merged, #1826-merged, #1817-merged, #1596-merged, #1714-merged, #1773/#1783-merged, #1753/#1761/#1770/#1780/#1762/#1783-merged).
- Precise split of the 11 PR-linked cards: 8 map to an OPEN PR, 3 map to merged/closed PRs (#1809 merged, #1596 merged, #1714 merged, #1773/#1783 merged, #1753/#1761/#1770/#1780/#1762 merged, #1783 merged, #1837 merged, #1826 merged, #1817 merged, #1834 closed).

## Author-identity audit table (per PR, open and mapped)

Identity column = `.commit.author.name` of the PR head commit (sole signal; `.author.login`/GitHub login ignored, null on unsigned commits is not a finding).

| PR | head sha (first 12) | commit author (.commit.author.name) | owning lane (card owner) | maps to card | open PR? | OK / MISMATCH |
| --- | --- | --- | --- | --- | --- | --- |
| 1809 | 0f9f45e07193 | 0428-061-sourcepull | w058-0428-058-hop | 0428-058 | no (MERGED) | MISMATCH (author lane != owning lane) |
| 1650 | 84943695be19 | w21-pr1702-0428-246-footprint | w55-0428-078-probehop | 0428-078 | yes (OPEN, DIRTY) | MISMATCH |
| 1818 | 20fc1cb7d496 | w53-0428-152-alertfix | w55-0428-078-probehop | 0428-078 | yes (OPEN, BEHIND) | MISMATCH |
| 1596 | c27158567c0e | Marcel Pfingstgräf (real name, noreply) | Codex team (current thread) | 0428-149 | no (MERGED) | OK — merged under w119 exception (see below) |
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
| 1835 | 55d17d437cfc | w105 | w105-0428-279-audit | 0428-287 | yes (OPEN, CLEAN) | OK (w105 == owning lane) |
| 1833 | a7b0a48048c1 | w124 | w147-0428-288-pr1833-fix | 0428-288 | yes (OPEN, UNSTABLE) | MISMATCH (w124 on a w147 card) |
| 1832 | 813ef899104c | w124 | w126-0428-290-pr1832-worker | 0428-290 | yes (OPEN, BLOCKED) | MISMATCH (w124 on a w126 card) |

## Cited-14 subset (explicitly marked)

The Owner wording "14 of 22" = 14 CARDS with the wrong-identity symptom. The two PRs the card itself cites in its own evidence (recorded exception 2026-11-24) are:

- **PR #1596** — head `c27158567c0ebc370fc6c97390a561846305738f`, author `Marcel Pfingstgräf` (real name). Card 0428-149. MERGED. Recorded exception in card handoff (3 authors from Owner-side hops, no content finding, exact run 44945468909 success). **OK as a documented exception** — the rule is unchanged; this is the one explicit carve-out on the card.
- **PR #1819** — head `17381017be986f0eccb25662ad742ad759296346`, author `0428-061-sourcepull`. Card 0428-181, owner `w54-0428-181-export`. **MISMATCH** — head commit author is the 061 source-pull lane, not the owning lane w54. Open, BEHIND develop.

The other cited-14 candidates that show the symptom (author lane != owning lane), drawn from the table above, include #1650, #1818, #1833, #1832, #1820, #1812, #1837, #1817, #1826, #1834, #1753, #1761, #1780, #1783, #1773. Symptom confirmed on every open PR head that is not authored by its own lane.

## Reconciliation of "14 of 22"

- 22 was a stale board snapshot; the live board has **26** open-status cards.
- **8** open PRs is correct (matches the "8" the Owner verified).
- 11 of the 26 open cards carry a PR link; 6–8 of those map to currently OPEN PRs; the rest are merged/closed.
- Every mapped candidate that is still open and authored by a lane other than its owner shows the symptom; only #1596 (documented exception) and #1835 (owner lane w105 == commit author w105) are clean.

## Findings (no product change, no head rewrite, no merge)

- Candidate commit authorship is NOT lane-deterministic across lanes that share the checkout (last-writer-wins on `user.name`). This is the exact symptom card 0428-224 describes.
- Fix-forward is allowed: future commits with `git -c user.name=<lane> -c user.email=<lane>@baseharbor.local commit ...`. No history rewrite without Owner (no history rewrite done here).
- Root cause is the admission rule missing from `coordinator/scripts/dispatch-lane.sh`; the fix is a prompt-only change to that file (Owner scope: scripts/**). Implemented below.

## Evidence witnesses

- `git -C baseharbor-plan remote -v`: `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- `gh pr list --repo mcpdev80/baseharbor --state open` returned exactly 8 PRs (numbers 1835, 1833, 1832, 1820, 1819, 1818, 1812, 1650).
- Identity fetched with `gh api repos/mcpdev80/baseharbor/commits/<sha> --jq '.commit.author.name'`; top-level `.author` and GitHub login are ignored (null on unsigned commits is not a finding).

END w155-0428-224-candidate-commit-identity DONE
Candidate SHA: 813ef899104c590fe533245cfc5ab8b0249b3114 (PR #1832 head, audit witness)
