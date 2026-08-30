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

## Released codes

Thirty-two marks were withdrawn on 2026-08-30 from `_index.md` section landing
pages. A section page is a navigation surface, not the author's Sprachwerk: gate
C3 fails a mark found on one from the rendered side and A18/C6 from the source,
and this is the disposal that reconciles the repos with both.

**These codes are not spent.** A withdrawn mark has never been claimed against a
work, so each may be re-registered on a page that qualifies — over 1,800
rendered characters, one work, one URL. They are listed so that happens instead
of a fresh draw.

The pages themselves are unchanged and still published. What they no longer do
is carry a pixel.

| course | URL | public code |
|---|---|---|
| `efl` | `/track-e/kl05/` | `00a66596a63a42f1beb56220bfd8d67a` |
| `efl` | `/track-e/kl06/` | `0222dd1db3254a26801c796f9ea0644b` |
| `efl` | `/track-e/kl07/` | `03eeb7fba1ae4497b51a4c1c9d52d94a` |
| `efl` | `/track-e/kl08/` | `059d98000d514fee9edd2dae2a26c2a8` |
| `efl` | `/track-e/kl09/` | `076ec137517948178f15bad235ef084f` |
| `efl` | `/track-e/kl10/` | `08fb07458c0943d799d95537a9f13f42` |
| `efl` | `/track-e/kl11/` | `0ad7c8fc2dde46aaacd8927bb0527e09` |
| `efl` | `/track-e/kl12/` | `0c9ed18d52c648e589dda7289acd2c69` |
| `efl` | `/track-e/kl13/` | `0e40eeac17cd41b3aa6afa478e303cc3` |
| `efl` | `/track-gm/kl05/` | `1043529b55504b30b531a3f44f1f483f` |
| `efl` | `/track-gm/kl06/` | `11f6978acfd3425db61ef13b4fd01ded` |
| `efl` | `/track-gm/kl07/` | `13ef6e89272f4d7c95b1b3b8e8ee8534` |
| `efl` | `/track-gm/kl08/` | `15e07ad41861429bb58f66ee88b751f9` |
| `efl` | `/track-gm/kl09/` | `17a7d36f3cfb4effacf605e8acf14ec7` |
| `efl` | `/track-gm/kl10/` | `1952725598d84ee09878d25ca51f1701` |
| `efl` | `/about/` | `1bfa32f4f472497c9d00e33805d27b97` |
| `efl` | `/about/courses/` | `1c1dd2ace2e54ab6aee391722b8897d1` |
| `fle` | `/filiere-e/` | `1c920712b1ac4286bba3826a4c410537` |
| `fle` | `/filiere-gm/` | `1ca3800adb624d47809df648bd176f6b` |
| `fle` | `/track_e_kl06/` | `1bc684db552e471aac7223b955bb6d11` |
| `fle` | `/track_e_kl07/` | `1d5ad4f111e2453aa8da00cf4da53d0e` |
| `fle` | `/track_e_kl08/` | `1ef4d7f41e8848e3ad6ef10309cc1627` |
| `fle` | `/track_e_kl09/` | `208c48dfb1604b9fb07d003188ad75c0` |
| `fle` | `/track_e_kl10/` | `22785e759724430483fb09ae3909f5e9` |
| `fle` | `/track_e_kl11/` | `23b158a72df54f0684c5b2380c43a8e9` |
| `fle` | `/track_e_kl12/` | `258d4552a089402a956ec9e3a040a6d0` |
| `fle` | `/track_e_kl13/` | `26fddee2be7b4ffba26dc95ea73c7714` |
| `fle` | `/track_gm_kl06/` | `28b4d1dde71e4d269a4f381c8679b5d9` |
| `fle` | `/track_gm_kl07/` | `2ac3fac658604d0bbc8c6cb181b632ca` |
| `fle` | `/track_gm_kl08/` | `2c32ca894703496f94a3878cc3693c9f` |
| `fle` | `/track_gm_kl09/` | `2d8b1da63eb649a596b3e957c4755318` |
| `fle` | `/track_gm_kl10/` | `2f051bac8e144f4eb4a4ed63de6b70ad` |

## Never marked

Navigation surfaces, the materials hub, tag and category indexes, paginated
continuations, and the three templated legal pages — Impressum, Datenschutz and
Haftungsausschluss are not the author's creative Sprachwerke. Minimum 1,800
rendered characters, exactly one mark per work, on exactly one URL.
