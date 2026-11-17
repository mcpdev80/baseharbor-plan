# Scan 1 — docs/de already keep a single warning label (already-compliant)

- Card: `t-20261117-hunt-signals-107` / `0428-107` · docs/de keeps Warnung/Fehler/Hinweis labels (low)
- Type: docs-only label-language audit (no product change)
- SHA base: `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458` (origin develop)
- Repo: `https://github.com/mcpdev80/baseharbor.git`
- Write-set claimed by card: `docs/` ONLY. Outcome: NO edit, NO PR (already-compliant).

## Formulierung vs. Ist-Beweis

The card text (and hunt source `befund-1.md`) describe **Go CLI `Achtung:` strings**
rendered by `fmt.Fprintln`/`fmt.Fprintf` on destructive/consent-gated paths. That
is a consumer-visible CLI-surface finding, handled by the separate card **106**. The
docs-de label contract (`docs/` only) was checked independently against the current
`develop` tree and is already consistent. No stale claim is carried over from the CLI
view; the CLI portion is out of scope for this lane.

## Sweep (witness)

Pattern over `docs/` (both `de` and `en` trees):
`Warnung | Vorsicht | Fehlerhinweis | Hinweis: | Warning: | Note:`

```
$ grep -rnc -E 'Warnung|Vorsicht|Fehlerhinweis|Hinweis:|Warning:|Note:' docs/ | grep -v ':0$'
docs/de/releases/v0.4.9.md:1
docs/de/releases/v0.4.15.1.md:1
```

Exactly two matches, both in intentional German release notes:
- `docs/de/releases/v0.4.9.md:26` — release note prose ("keine Warnung kann eine Leugnungspolitik stillschweigend umgehen")
- `docs/de/releases/v0.4.15.1.md:31` — release note prose ("meldet Warnungen, anstatt die vollständige Liste zu versagen")

Neither is a label marker; both are prose inside German release-engineering pages.
No `Warnung`/`Vorsicht`/`Fehlerhinweis`/`Hinweis:`/`Warning:`/`Note:` label marker
exists anywhere else in `docs/`.

### Warning-label sites (the only label marker used)

```
$ grep -rn -E '\*\*Achtung\*\*' docs/ | wc -l
21
```

All 21 occurrences use the single invariant token `**Achtung**` — the same token the
English docs use on the paired pages. Representative sites (DE + EN):

```
docs/de/spec/capability-first-v0425.md:216   **Achtung** (DE)
docs/spec/capability-first-v0425.md:202      **Achtung** (EN, paired)
docs/de/cli/targets.md:42,119               **Achtung** (DE)
docs/cli/targets.md:49,125                  **Achtung** (EN, paired)
docs/de/how-to/external-providers.md:60     **Achtung** (DE)
docs/how-to/external-providers.md:66        **Achtung** (EN, paired)
docs/de/how-to/machine-operations.md:6      **Achtung** (DE)
docs/how-to/machine-operations.md:5         **Achtung** (EN, paired)
docs/de/releases/v0.4.25.md:32              **Achtung** (DE)
docs/releases/v0.4.25.md:29                 **Achtung** (EN, paired)
docs/de/spec/runtime-explorer-v1.md:147     **Achtung** (DE)
docs/spec/runtime-explorer-v1.md:145        **Achtung** (EN, paired)
```

No `**Warnung**` / `**Vorsicht**` / `**Hinweis**` / `**Notiz**` / `**Tipp**` bold
label marker exists in `docs/de/`. No English `**Warning**`/`**Note**`/`**Tip**`/
`**Caution**` label marker exists in the human-facing `docs/` pages either. The
German docs already render the one consistent warning label the contract requires.

## Doc integrity (authoritative validators for this path)

```
$ python3 scripts/check_de_translation_integrity.py
DE technical integrity: PASS (168 paired pages)

$ python3 scripts/check_docs_locale_parity.py
EN/DE page coverage OK: 168 matched Markdown pages
```

`mkdocs build` itself exited on a host disk-quota error (`[Errno 122] Disk quota
exceeded` on write to the output dir) — a local environment limit, not a docs fault.
The two repo-specific doc gates above are the passing evidence for this path.

## Ergebnis: already-compliant

- The German docs already keep a single consistent warning label (`**Achtung**`)
  matching the English paired pages; no `Warnung`/`Vorsicht`/`Hinweis` label
  variant exists in the human-facing docs.
- The only remaining `Achtung:` token is the **Go CLI** surface, which is the
  separate card 106, not this docs-de lane.
- No doc edit, no branch, no PR. Write-set `docs/` untouched.

## EVIDENCE ON origin/main (before END)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree origin/main --name-only -r -- evidence/r28-welle3-2026-11-16/hunt-signals-107/
```

(to be filled with the exact `ls-tree` output after this file is committed to planning origin/main)

## END STATUS

END_DONE to coordinator d4212c96-16b8-4fe3-a6ef-587d20c0e0d0. No product edits,
no branch cut, no PR. No containers/compose started (cleanliness: none; ambient-core
`bh-local-shared-*` stacks foreign, left untouched).
