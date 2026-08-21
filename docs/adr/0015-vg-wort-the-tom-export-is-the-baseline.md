# ADR 0015 — VG Wort: the T.O.M. export is the baseline; private ledger, `marks.yaml`, `url-lock.csv`

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0003 (URLs are frozen), ADR 0014 (one exam page per unit), ADR 0016 (release policy), ADR 0019 (`url-lock.csv` is generated from the export)

## Context

The corpus carries **821 Zählmarken**: 402 in `efl` (all in `data/vgwort.yaml`), 351 in `fle` (349 as bare `vgwort_pixel:` strings in front matter, 2 `url:`-keyed in `data/vgwort.yaml`) and 68 in `daf` (`path:`-keyed). Zero codes appear in two repos.

Nothing in the org records where those codes are *registered*. The repos are authoritative for which URL a code **renders on**. Only T.O.M. is authoritative for which URL a code is **registered against**, and those are two different facts that are not known to agree (ADR 0019).

The recording is also thinner than "821 registered" implies:

- **472 marks carry a registration date** — `efl` 402, `daf` 68, `fle` 2. The **349 `fle` front-matter marks carry no `registered_at` anywhere in any repository**; `grep -c registered_at fle/data/vgwort.yaml` returns 2.
- **227 are unverified by any CI gate.** `efl`'s 3 data-only entries (`/about/`, `/about/courses/`, `/acknowledgements/`) are absent from all 399 rows of `efl/vgwort-manifest.csv`, on which `_scripts/verify_all_pixels.py:70,78` prints `WARN` and returns 0. `fle`'s 156 front-matter marks are absent from its 193-row stale manifest. All 68 of `daf`'s are unchecked because `daf/scripts/verify-vgwort.sh:24-27` reads a header-only manifest, prints "manifest is empty — passing trivially" and exits 0.
- **The 399 that are checked are checked more weakly than the word implies.** `efl/_scripts/verify_rendered_pixels.py:23-32` indexes every `.html` in `public/` and asserts each `pixel_url` appears *somewhere* in the build, not on its registered URL. A mark whose page moved but which still renders somewhere passes today.
- **No `private_id` value appears in any repository.** The only occurrence anywhere is the schema comment at `daf/data/vgwort.yaml:13`. That property is currently held by care.

## Decision

**The T.O.M. export is the baseline for every VG Wort operation in this org.** The ledger, the in-repo mark files and the URL lock are all derived from it, in that order, and never from a sitemap.

**Three artefacts, with one writer each.**

1. **The private ledger, `~/vgwort/ledger.csv`** — outside every repository, never in an issue, never in a CI log, backed up with the author's private data. Schema: `public_id, private_id, state, repo, url, registered_url, level, title, drawn_at, assigned_at, registered_at, retired_at, retired_reason`, with `state ∈ {free, assigned, registered, retired}`. `registered_url` is the export column. The ledger is authoritative for which codes exist, which are free, and what URL T.O.M. holds. **`bin/kit vgwort` is the only writer**, so it cannot drift through hand-editing.
2. **`vgwort/marks.yaml` in each course repo** — keyed on the page's current `RelPermalink`, carrying the public code and `registered_at` and nothing private. This replaces the three incompatible shapes in use today: `efl`'s `data/vgwort.yaml`, `fle`'s 349 front-matter strings, and `daf`'s `path:`-keyed entries, which key on the exact source file and therefore break the instant a flat file becomes a leaf bundle.
3. **`vgwort/url-lock.csv`** — schema `url,code,registered_url,first_seen,content_sha`, expected 821 rows across the three repos. **The `url` column is populated from the T.O.M. export, not from the sitemap.** Rows whose registered and rendering URLs disagree are written with the T.O.M. URL and `status: pending-rekey`, and cleared in that repo's Phase 3 branch.

**Six operating stages after the reconciliation.** *Draw* codes in bulk into the ledger as `free`, in blocks sized to a level. *Qualify* — original creative text **and** ≥1,800 rendered characters; never a home page, a materials hub, a taxonomy index, a `/page/N/` pagination URL or a templated legal page. *Bind* atomically through `bin/kit vgwort assign`, which refuses a code already assigned anywhere. *Register* in T.O.M.; only registered marks earn. *Verify* on every push (C1–C3, C5) and weekly (C4 plus reconciliation). *Re-key* under the protocol below.

**Gate A3 keys on `RelPermalink`, never on a slug field.** `efl` carries four distinct slug namespaces on one page — `unit_slug`, the material slug inside `presentation.file`, the bundle directory name which *is* the URL, and an `aliases:` entry. A gate specified as "a marked page's `material_slug` changed" protects nothing at all on the largest live course.

**The re-key protocol, mandatory and never abbreviated.** (1) A3 fails the PR. (2) Decide: revert the slug — the default, and free — or proceed. (3) If proceeding, publish a Hugo `aliases:` entry; **the alias preserves the reader's link, not the income**. (4) Draw a **new** code for the new URL, bind, register. (5) The old code moves to ledger state `retired` with a reason; never reused, never deleted. (6) `url-lock.csv` gains a row and the old row moves to `url-lock.retired.csv`. (7) An ADR if more than one page is affected.

**A mark and its URL move in the same commit, or neither moves.** There is no intermediate state in which a page has been renamed and its mark has not followed, and no PR may land one half of a re-key.

**Weekly reconciliation** reports: registered in the ledger but absent from any `marks.yaml` (an orphaned mark, earning nothing); present in a repo but `free` or absent in the ledger (an unrecorded registration, the state that produces accidental reuse); `assigned` for more than 30 days with no `registered_at` (forgotten in T.O.M.); `registered_url` diverging from today's `RelPermalink`; any code in two repos (a hard error — zero today, and it stays zero); and the four counts that must agree: repo marks, `url-lock.csv` rows, C2-verified, T.O.M.-registered.

## Consequences

- **Today the report reads: 821 marks in the repos · 472 with an in-repo registration date · 227 unverified by any CI gate · 0 duplicates · T.O.M. agreement unknown.** After Phase 3 it must read: 821 registered, 821 verified on their registered URL, 0 duplicates, ledger agrees, T.O.M. agrees.
- **`fle` cannot make C1 blocking until the export lands.** C1 requires `registered_at` on every entry, and 349 of `fle`'s dates exist in no repository. P3.3's migration lands all 349 with `registered_at: unknown-pre-programme` and the export backfills them; that backfill is the release gate on C1 for `fle`. This is a hard dependency of P3.3 on ADR 0019.
- **C2's "the pixel renders on exactly one page, and it is the registered one" is a genuine tightening** over what `efl` checks today, and should be described as one rather than as a port.
- **C3 must not be written as "no mark on a section index".** 28 marked pages — 15 in `efl`, 13 in `fle` — *are* Hugo section landings carrying 2,862–4,550 characters of original editorial prose above a generated list. The rule is: no mark on a page whose original prose, excluding layout-generated lists, download blocks and audio sections, is below the Mindestumfang. Written the obvious way, C3 would orphan 28 live marks on the day it lands.
- Under-floor marked pages are either completed past 1,800 characters or their mark is retired through the protocol. Decided for `fle`: complete the 13 `uebersicht.md` per-Klassenstufe overviews (166–167 characters today), retire the 5 `annexes/*` marks (275–469 characters; a glossary stub is not a work and padding it is exactly what the standard forbids).
- The no-private-code rule ratifies practice rather than changing it, and moves it from care to a PR-checklist gate. The `vgwort-mark` issue form is restricted and its body warns in bold never to paste a private identification code into an issue.

## Alternatives considered

**Take the sitemap crossed with `marks.yaml` as the baseline.** Rejected, and the rejection is its own record — ADR 0019. The sitemap says where a pixel renders; only the export says where a code earns.

**Keep marks in front matter, as `fle` does.** Rejected. 349 marks spread across 349 files cannot be counted, diffed or reconciled as a set, and a mark whose only home is the page it sits on disappears with the page. The front-matter key stays in place for one release during P3.3 so both paths yield the same URL and C2 stays green through the overlap.

**Keep the ledger in a private repository rather than outside every repository.** Rejected. A private repository is one visibility setting away from being public, and CI logs, forks and issue attachments all reach into repositories. The private identification codes are the one asset in the org that cannot be regenerated.

**Treat a Hugo alias as preserving income.** Rejected on the mechanism: Hugo's alias output is a `<meta http-equiv=refresh>` stub carrying no pixel, and `efl/_scripts/verify_rendered_pixels.py:28-30` skips exactly those pages by design.

**Delete retired codes from the ledger.** Rejected. A retired code must remain visible forever so it is never redrawn, and so a later question about a URL that used to earn has an answer.
