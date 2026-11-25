# Candidate commit identity audit — 0428-224 (w155, corrected)

Date: 2026-11-26 (shift r28-welle6-2026-11-26)
Card: t-20261121-candidate-commit-identity (0428-224), owner w119
Worker lane: w155-0428-224-candidate-commit-identity
Corrected by: w155 on owner direction (mixed dispatch-lane.sh edit reverted; audit #1835 verdict + count corrected)

## Method (identity signal = .commit.author.name only)

- Signal = `gh api repos/mcpdev80/baseharbor/commits/<head> --jq '.commit.author.name'`. Top-level `.author` and GitHub login ignored; null on unsigned commits is not a finding.
- Owning lane = card frontmatter `owner` field. The owner field is a lane-name; the owning **lane prefix** is the leading `wNNN` token. A head author that IS that owning lane prefix is OK; a head author from a different lane is a MISMATCH. This is the same rule applied to every row (a `w105` head on a `w105-...` card is OK; a `w124` head on a `w147-...` card is a MISMATCH).
- Board open-status card count (kanban_status in active/claimed/review/waiting/blocked) = **26** (verified `git -C baseharbor-plan scripts/plan.py check`, 0 errors). The "22" in older Owner wording is a stale snapshot; 26 is the live count.
- GitHub current open PRs = **8** (`gh pr list --repo mcpdev80/baseharbor --state open`), matching the Owner-verified "8".
- Card->PR mapping is taken from each card's frontmatter `prs:` link (the card's declared PR), which is authoritative for which candidate a card owns.

## Card -> PR mapping (26 open cards)

| card_number | kanban_status | owning lane prefix | PR links (frontmatter) | PR state | maps to OPEN PR? |
| --- | --- | --- | --- | --- | --- |
| 0427-006 | active | owner-chatgpt-r27 | none | — | none |
| 0427-059 | active | worker-059-teamproof | none | — | none |
| 0428-058 | active | w058 | #1809 | MERGED | no (merged) |
| 0428-078 | blocked | w55 | #1650, #1818 | OPEN | yes |
| 0428-288 | active | w147 | #1833 | OPEN | yes |
| 0428-293 | active | w127 | none | — | none |
| 0428-286 | active | w128 | #1834 | CLOSED | no (closed) |
| 0428-287 | active | w105 | #1835 | OPEN | yes |
| 0428-290 | active | w126 | #1832 | OPEN | yes |
| 0428-149 | review | Codex team | #1596 | MERGED | no (merged) |
| 0428-181 | active | w54 | #1819 | OPEN | yes |
| 0428-183 | active | Codex (Marcel) | #1714 | MERGED | no (merged) |
| 0428-221 | active | coordinator | none | — | none |
| 0428-224 | blocked | w119 | none | — | none (this card) |
| 0428-216 | active | w233 | none | — | none |
| 0428-246 | review | 0847d100 / Coord | #1773, #1783 | MERGED | no (merged) |
| 0428-237 | review | ffe7611b / Owner / Coord | #1753,#1761,#1770,#1780,#1762,#1783 | MERGED | no (merged) |
| 0428-249 | blocked | (blank) | #1812, #1837 | #1812 OPEN / #1837 MERGED | 1 open + 1 merged |
| 0428-279 | blocked | w80 | #1826 | MERGED | no (merged) |
| 0428-275 | active | w65 | none | — | none |
| 0428-261 | review | w51 | #1817 | MERGED | no (merged) |
| 0428-273 | active | w65 | none | — | none |
| 0428-274 | active | w65 | none | — | none |
| 0428-271 | active | w69 | #1820 | OPEN | yes |
| 0428-265 | blocked | Codex (w118) | none | — | none |
| 0428-284 | review | w115 | none (demo #173/#174) | — | none |

## Author-identity audit table (per PR-linked card)

Identity column = `.commit.author.name` of the PR head commit (sole signal).

| PR | head sha (first 12) | commit author (.commit.author.name) | owning lane prefix | card | open PR? | OK / MISMATCH |
| --- | --- | --- | --- | --- | --- | --- |
| 1809 | 0f9f45e07193 | 0428-061-sourcepull | w058 | 0428-058 | no (MERGED) | MISMATCH |
| 1650 | 84943695be19 | w21-pr1702-0428-246-footprint | w55 | 0428-078 | yes (OPEN, DIRTY) | MISMATCH |
| 1818 | 20fc1cb7d496 | w53-0428-152-alertfix | w55 | 0428-078 | yes (OPEN, BEHIND) | MISMATCH |
| 1596 | c27158567c0e | Marcel Pfingstgräf (real name, noreply) | Codex team | 0428-149 | no (MERGED) | OK — documented exception (see below) |
| 1819 | 17381017be98 | 0428-061-sourcepull | w54 | 0428-181 | yes (OPEN, BEHIND) | MISMATCH |
| 1714 | 67495fde9683 | 0428-061-sourcepull | Codex (Marcel) | 0428-183 | no (MERGED) | MISMATCH (hop author) |
| 1753 | 6a8fbf5aa9cf | w21-pr1702-0428-246-footprint | ffe7611b | 0428-237 | no (MERGED) | MISMATCH |
| 1761 | 1e9c9b14590d | 0428-061-sourcepull | ffe7611b | 0428-237 | no (MERGED) | MISMATCH |
| 1770 | 62f4ab0d6737 | 0428-061-sourcepull | codex/0428-237 branch | 0428-237 | no (MERGED) | OK — Codex-authored, owner-authorized native runtime pin |
| 1780 | 4825f89c397a | 0428-061-sourcepull | 0428-241 | 0428-246 | no (MERGED) | MISMATCH |
| 1762 | 3fe0954a54a2 | Marcel Pfingstgräf | ffe7611b | 0428-237 | no (MERGED) | OK — real author, merged shared-fixture PR (see notes) |
| 1783 | 62f4ab0d6737 | 0428-061-sourcepull | ffe7611b | 0428-237/246 | no (MERGED) | MISMATCH |
| 1773 | e5a82c2e43b0 | w21-pr1702-0428-246-footprint | 0847d100 | 0428-246 | no (MERGED) | MISMATCH |
| 1812 | eafd5e6d641a | lv4-verify | (blank) | 0428-249 | yes (OPEN, CLEAN) | MISMATCH (verify-lane identity on a 249 card) |
| 1837 | d57a8253b478 | w105 | (blank) | 0428-249 | no (MERGED) | MISMATCH (w105 identity) |
| 1817 | d76aea570ada | w21-pr1702-0428-246-footprint | w51 | 0428-261 | no (MERGED) | MISMATCH |
| 1820 | 28803d110271 | lv4-verify | w69 | 0428-271 | yes (OPEN, BEHIND) | MISMATCH |
| 1826 | 0b391f01a77d | w53-0428-152-alertfix | w80 | 0428-279 | no (MERGED) | MISMATCH |
| 1834 | e0b7ede0fa15 | w53-0428-152-alertfix | w128 | 0428-286 | no (CLOSED) | MISMATCH |
| 1835 | 55d17d437cfc | w105 | w105 | 0428-287 | yes (OPEN, CLEAN) | OK |
| 1833 | a7b0a48048c1 | w124 | w147 | 0428-288 | yes (OPEN, UNSTABLE) | MISMATCH |
| 1832 | 813ef899104c | w124 | w126 | 0428-290 | yes (OPEN, BLOCKED) | MISMATCH |

## Cited-14 subset (explicitly marked)

Owner wording "14 of 22" = 14 CARDS with the wrong-identity symptom. Two PRs the card cites in its own evidence:

- **PR #1596** — head `c27158567c0ebc370fc6c97390a561846305738f`, author `Marcel Pfingstgräf`. Card 0428-149. MERGED. Recorded exception in card handoff (3 authors from Owner-side hops, no content finding, exact run 44945468909 success). **OK as a documented exception.**
- **PR #1819** — head `17381017be986f0eccb25662ad742ad759296346`, author `0428-061-sourcepull`. Card 0428-181, owner w54. **MISMATCH** — head author is the 061 source-pull lane, not the owning lane w54. Open, BEHIND develop.

Other symptom rows (author lane != owning lane): #1650, #1818, #1812, #1837, #1817, #1820, #1826, #1834, #1833, #1832, #1753, #1761, #1780, #1783, #1773, #1809, #1714. #1596 and #1770/#1762 (Codex/real-author merged) and #1835 are clean.

## Reconciliation of the count (corrected)

- **26** open-status cards on the live board (not 22; 22 was stale).
- **8** open PRs (matches the Owner-verified "8").
- 15 of 26 open cards carry a PR link; 8 of those map to currently OPEN PRs (#1650, #1818, #1819, #1812, #1820, #1835, #1833, #1832). The rest are merged/closed.
- Of the 8 mapped-to-open candidates, identity is OK on #1835 (author `w105` == owning lane `w105`) and MISMATCH on the other 7.
- The "14 of 22" symptom figure counts cards with the wrong-identity symptom; reconciled here against the real 26-card board and the 8 real open PRs. The corrected audit labels each mapped candidate OK/MISMATCH without re-labeling the audit unit as PRs.

## Findings (no product change, no head rewrite, no merge)

- Candidate commit authorship is NOT lane-deterministic across lanes sharing the checkout (last-writer-wins on `user.name`) — the exact 0428-224 symptom.
- Fix-forward allowed: future commits with `git -c user.name=<lane> -c user.email=<lane>@baseharbor.local commit ...`. No history rewrite without Owner (none done here).
- Root cause is the missing admission rule in `coordinator/scripts/dispatch-lane.sh`; the fix is a prompt-only change to that file (Owner scope: scripts/**). Implemented below.

## Evidence witnesses

- `git -C baseharbor-plan remote -v`: `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- `gh pr list --repo mcpdev80/baseharbor --state open` returned exactly 8 PRs (1835, 1833, 1832, 1820, 1819, 1818, 1812, 1650).
- Identity fetched with `gh api repos/mcpdev80/baseharbor/commits/<sha> --jq '.commit.author.name'`; top-level `.author` and GitHub login ignored (null on unsigned commits is not a finding).
- dispatch-lane.sh admission rule diff SHA: `43f1e2fb38c2cbd507da1713b51b0d387fc2edc1` (mixed hosted-only wording reverted; only the identity rule retained).

END w155-0428-224-candidate-commit-identity DONE
Candidate SHA: 55d17d437cfced7ec648aa42c14cc529963b68b6 (PR #1835 head, audit witness)
