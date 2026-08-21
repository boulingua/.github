# ADR 0003 — URLs are frozen, per site, on three axes

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0002 (`boulingua.yml`), ADR 0015 (VG Wort ledger), ADR 0019 (`url-lock.csv` from the T.O.M. export) · ADR 0020 (that reconciliation is deferred to the end; a provisional lock holds the URL space meanwhile)

## Context

821 unique 32-hex VG Wort Zählmarken exist in the three live repos — `efl` 402, `fle` 351, `daf` 68, with zero duplicates across repos. A Zählmarke is bound to a URL. A URL change is a **new work** to VG Wort: it destroys the registered mark and the statutory income attached to it. A Hugo `aliases:` entry preserves the reader's link but not the income — an alias page is a `<meta http-equiv=refresh>` document on which the pixel never fires, and `efl/_scripts/verify_rendered_pixels.py:28-30` skips exactly those pages.

The shorthand "`daf` and `fle` keep underscores, `efl` keeps hyphens" is false, and honouring it in a generator would cost real money. Measured on the checkout:

| | section path | leaf slug | unit ordinal in URL | derived from | live example |
|---|---|---|---|---|---|
| `efl` | hyphen (`/track-e/kl09/units/`) | hyphen | **yes** (`unit06-`) | leaf-bundle directory name; **0 of 360 `slug:` overrides** | `/track-e/kl09/units/unit06-interview-and-portrait/` |
| `fle` | **underscore** (`/track_gm_kl06/units/`) | **hyphen** | **no** | front-matter `slug:` override on **312 of 358** files, **none of which contains an underscore** | `/track_gm_kl06/units/salutations-et-prenoms/` |
| `daf` | underscore (`/kurs_a1/units/`) | underscore | yes (`unit01_`) | flat filename stem; **0 of 60 `slug:` overrides** | `/kurs_a1/units/unit01_begruessung-und-name/` |

`fle/content/track_gm_kl06/units/unit01_salutations-et-prenoms.md` declares `slug: "salutations-et-prenoms"` and renders at `/track_gm_kl06/units/salutations-et-prenoms/`. The underscore is in the **section path only**; the leaf is hyphenated and the `unitNN` ordinal never reaches the URL at all.

**The freeze is also currently defending an unverified baseline, and that is blocking.** All three sites migrated from Quarto to Hugo on 2026-05-06. `efl` carries `aliases:` on 405 pages, `fle` on 202, `daf` on 80. But **399 of `efl`'s 402 marks carry `registered_at: '2026-04-30'`** — six days *before* the migration — and each still records its Quarto source in a `qmd_path:` field; `fle`'s pre-migration manifest holds 193 rows keyed on `qmd_path`, carried into Hugo verbatim. So **up to 592 of the 821 marks may be registered in T.O.M. against URLs that no longer render a pixel.** The repos cannot settle this. Only the author's T.O.M. account can. **This is open.** Until the export exists and the diff closes, nothing that changes a URL may proceed, and `url-lock.csv` cannot be generated, because a lock file built from the wrong baseline would teach the gate to defend URLs no registration points at — forever, with perfect fidelity.

## Decision

**1. URLs are frozen per site, permanently.** Not the slug style — the rendered URL.

**2. The convention is declared on three axes, never one**, in `boulingua.yml`:

```yaml
slug:                           # FROZEN
  section_separator: underscore   # underscore | hyphen
  leaf_source: frontmatter        # frontmatter | dirname | filestem
  leaf_style: hyphen              # underscore | hyphen
  unit_number_in_slug: false
```

A single `slug_style: underscore` for `fle` is **wrong and destructive**: any generator honouring it emits `/track_gm_kl06/units/unit01_salutations-et-prenoms/` and orphans 349 registered marks in one commit.

**3. `fle`'s front-matter `slug:` overrides are load-bearing and permanent.** They are not redundant, they are not tidy-up-able, and deleting one changes a URL and kills a mark. Any conversion of `fle` content carries all 312 through verbatim.

**4. Leaf bundles are adopted org-wide *because* they are URL-neutral under all three shapes.** `content/kurs_a1/units/unit01_x.md` and `content/kurs_a1/units/unit01_x/index.md` render at the identical URL, and Hugo's `slug` replaces a bundle directory name exactly as it replaces a filename — which is why the conversion is URL-neutral for `fle` too. This closes the diverging-content-model defect without touching a single URL or a single mark.

**5. The gate keys on `RelPermalink` and on nothing else.** `efl` carries four independent slug namespaces on one page — `unit_slug`, the material slug inside `presentation.file`, the bundle directory that *is* the URL, and an `aliases:` entry. Changing `material_slug` renames a PDF and orphans nothing; changing the bundle directory orphans the mark and leaves `material_slug` untouched. A gate specified against `material_slug` protects nothing on the largest live course.

**6. New courses use hyphen / hyphen / `unit_number_in_slug: true`.** All fifteen scaffolds carry zero marks, so they adopt the final convention for free.

**7. Every URL-affecting step is one commit** — file move, front-matter change, mark re-key and materials rename together, gated on the *built* site before the deploy job. Split them and marks go dark between deploys.

## Consequences

- The org's URL space will never look uniform, and that is the accepted outcome. Consistency here is worth less than 821 registered marks.
- `bin/kit urldiff` builds the site twice and diffs `RelPermalink` sets against `url-lock.csv`. Every migration step runs it; no step claims URL-neutrality without it.
- The gate blocks PRs made by this programme, which is the point.
- **Cost:** three live courses keep three shapes forever, and every generator, gate and document that touches a URL must ask which of the three axes it means before it can be costed. Any future proposal to "unify the slugs" is not admissible until it names the axis.
- **Cost, currently unpaid:** `url-lock.csv` and the gate behind it are blocked on the T.O.M. export. The freeze holds by convention until that lands, and by machine afterwards.

## Alternatives considered

**Unify all three courses on one URL shape.** Rejected. It changes 753 URLs and puts every mark on them through the re-key protocol — draw a new code, bind, register, retire the old one — with the alias preserving only the reader's link. The programme's largest revenue exposure would be created deliberately, to buy tidiness.

**Declare one axis (`slug_style`) and derive the rest.** Rejected as actively destructive, and named here so it is not proposed again. It is the single most expensive wrong assumption available: applied to `fle` it is a 349-mark extinction event, and the resulting diff would look like a cleanup.

**Rely on `aliases:` and change URLs freely.** Rejected on measured behaviour, not on principle. Hugo's built-in alias output is a bare meta-refresh stub carrying no pixel; it converts a paid page into an unpaid redirect. This is the same mechanism that leaves the 2026-05-06 migration unreconciled today.

**Delete `fle`'s 312 `slug:` overrides during the leaf-bundle conversion.** Rejected. This is the specific mistake an implementer who does not know the above will make, because 312 front-matter keys that appear to restate the filename look like noise. They are the URL.
