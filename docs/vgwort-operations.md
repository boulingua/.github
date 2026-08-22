# VG Wort operations

821 registered Zählmarken across the three live courses — `efl` 402, `fle` 351,
`daf` 68. They are the author's statutory remuneration under §§ 54 ff. UrhG,
and they are **keyed to URLs**. That single fact is why this document exists and
why URL stability outranks consistency and tidiness everywhere in this
organisation.

## The rule

**A mark and its URL move in the same commit, or neither moves.**

Gate A3 enforces it. `bin/kit urldiff` runs before every merge and compares the
built `RelPermalink` set against the lock; a moved URL fails unless the change
declares it.

## The lock is provisional, and the filename says so

`vgwort/url-lock-provisional.csv` is derived from the built sitemap. It records
where a mark **renders**. It deliberately has no `registered_url` column,
because only a T.O.M. export can fill that, and a lock that guessed would teach
the gate to defend a fact nobody checked.

So gate A3 runs in **neutrality mode**: it proves a change moved nothing. It
cannot prove the URLs it defends are the registered ones.

## The open exposure

All three sites migrated Quarto → Hugo on **2026-05-06**. But **399 of `efl`'s
402 marks are dated `2026-04-30`** — six days earlier — and every `efl` manifest
row still records a Quarto `qmd_path`. `efl` carries `aliases:` on 405 pages,
`fle` on 202, `daf` on 80, and Hugo's alias output is a bare meta-refresh stub
carrying **no pixel**.

So up to **592 of the 821 marks may be registered against URLs that no longer
render one**, and would have been earning nothing since May. The repositories
cannot settle this. Only T.O.M. can.

Deferred to the closing phase (ADR-0020). What is *not* deferred is prevention:
from the day the provisional lock landed, no new divergence can be introduced.

**A twenty-code hand sample closes the question in about two hours** and is
worth taking the first time the portal is open for anything else. Spread them
across the three repos and across both `registered_at` dates.

## Codes

The **public** code — 32 hex, in the pixel URL — may appear in a repo, an issue
and a build log. The **private** identification code may appear in none of
them, ever. It lives only in the ledger outside every repository.

If a private code is committed: report it as a security advisory rather than an
issue, because an issue is public and would republish it. The mark is retired
and re-drawn.

## Never marked

Navigation surfaces, the materials hub, tag and category indexes, paginated
continuations, and the three templated legal pages — Impressum, Datenschutz and
Haftungsausschluss are not the author's creative Sprachwerke. Minimum 1,800
rendered characters, exactly one mark per work, on exactly one URL.
