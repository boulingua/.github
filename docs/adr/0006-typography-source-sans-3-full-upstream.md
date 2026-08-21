# ADR 0006 — Typography: full upstream Source Sans 3, italics shipped, `font-synthesis: none`

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0005 (tokens), ADR 0007 (language islands), ADR 0018 (waves 5–6 deferred)

## Context

Every claim below is measured against the committed files and the upstream releases, not against documentation.

**What ships today is a Latin subset in every repo.** `slidegen/fonts/SourceSans3-{Regular,Light,Semibold,Bold}.ttf` measure **781 codepoints each: 0 Greek, 0 Cyrillic.** The seven `.woff2` files in `pagegen/static/fonts/` are the identical subset, all `latin_latin-ext`. `JetBrainsMono-Regular.ttf` measures 405 codepoints, likewise none.

**What upstream actually contains.** Source Sans 3 **3.052** measures **1,648 codepoints — 228 Latin-Ext, 88 monotonic Greek, all 233 assigned polytonic characters of U+1F00–1FFF, and 156 Cyrillic.** The italic, semibold-italic and bold-italic faces measure the same 1,648 and cover Greek and Cyrillic too. So the problem was never the version — both families are already at their current upstream release — it is that both were fetched with the `latin,latin-ext` ranges only. `v19` and `v24` in the filenames are Google Fonts API revision numbers, not font versions.

**No italic exists anywhere in the org.** Neither `.sty` file sets `ItalicFont`; `fonts.css` declares no italic `@font-face`. Every emphasis span on every live site is a browser-synthesised oblique, and on the print side beamer falls through to Latin Modern Oblique. The exposure: **6,020 emphasis spans in 347 `efl` files, 5,080 in 330 `fle` files, 2,476 in 69 `daf` files — 13,576 spans**, including every learning objective.

**The bundled name table is mangled.** Every Source Sans 3 weight declares nameID 1 = `Source Sans 3 ExtraLight`; every committed worksheet PDF embeds `/BUEMMA+SourceSans3ExtraLight-Regular`. An embedded-font allowlist cannot be written against those names.

**Beamer decks are not set in Source Sans 3 at all.** Both `.sty` files call `\setmainfont`, which sets `\rmfamily`; beamer's document default is `\sffamily`. `daf/static/materials/presentations/unit01_begruessung-und-name.pdf` embeds `LMSans10-Regular`, `LMSans10-Oblique` and `LMSans8-Regular` for body text. All 216 committed decks are typeset in Latin Modern Sans.

**Licensing is incomplete.** Permanent Marker is Apache-2.0 (Font Diner), not OFL, so a single `OFL.txt` is the wrong artefact — and today seven `.woff2` files ship carrying the OFL URL in their own name tables with no licence text anywhere in the repo.

## Decision

**1. Full upstream Source Sans 3 3.052, subset by us, for Latin, Latin-Ext, Greek and Cyrillic.** The bundled 781-codepoint subsets are replaced by subsets `build_fonts.py` produces from the Adobe release, with ranges declared **by codepoint, never by a vendor range name**. Consequence: `gfl`, `rki`, `ufl`, `pfl`, `tfl` and `lle` need **no new typeface at all** — one face across sixteen of eighteen codes.

Two details a naive "add Greek and Cyrillic" fix gets wrong, and both are normative. Polytonic Greek **is covered**, so it does not fail the build; it is an editorial constraint — `gfl` teaches Modern Greek and is monotonic throughout, and polytonic is permitted only inside a `lang="grc"` island for a classical citation. And `ufl` needs the `cyrillic-ext` range even though its letters look like base-block Cyrillic: ґ is U+0490/U+0491 and the common `cyrillic` range stops at U+045F. The glyphs are in the face; a subset built with the base range alone silently drops them.

**2. Italics ship, and synthesis is switched off.** Source Sans 3 Italic, SemiboldItalic and BoldItalic are added. `html { font-synthesis: none; }` is set globally **the moment the real italic lands, and not before**, so a missing face becomes visible rather than faked. This matters most in Cyrillic, where a synthesised oblique is not merely ugly — а, т and д have distinct italic constructions, so the synthesised form is the wrong letterforms.

**3. Arabic script: IBM Plex Sans Arabic 1.005 (OFL 1.1) is the body face for both `afl` and `pfa`.** Verified against the release: full Persian orthographic set (ی ک گ پ چ ژ), both digit sets, and the tashkīl marks including shadda, sukun, fathatan and dagger alef. Noto Naskh Arabic is a scoped second family for fully-vocalised script-stage passages only; Amiri is `pfa`'s classical-reader display face only. Latin runs on those pages are set in Source Sans 3.

**4. CJK: Noto Sans SC for `cfl`, Noto Sans JP (plus Noto Serif JP for reading passages) for `jfl`**, subset from `notofonts/noto-cjk` rather than the Google Fonts repackaging, because the subsetting is ours.

**Rows 3 and 4 are recorded decisions that are not procured in this programme.** The `arabic`, `hanzi-sc` and `kana-kanji` tiers are declared in `fonts.yaml` with `status: deferred`, carry no committed binaries, and `bin/kit sync` refuses to instantiate a course whose `script_tier` names a deferred tier. They are paid for at the opening of wave 5 (ADR 0018). The mechanism is built now because it is the same code and the same manifest either way.

**5. The optical-matching contract, because "closest match" is an assertion and an assertion is not a design system.** Every non-Latin family in `fonts.yaml` carries a measured `x_height_ratio` against Source Sans 3 at the same nominal size, committed beside the family with the tool and date that produced it. One number generates both the `size-adjust`/`ascent-override`/`descent-override` in the `@font-face` block and the `Scale=` factor in the `\newfontfamily` declaration, so web and print cannot drift. **A family whose ratio has not been measured fails the build** — it does not fall back to 100 %, because 100 % is exactly the value that produces the second design this contract exists to prevent.

**6. OpenType features are a floor plus a no-drop rule, not a fixed list.** Required floor `ccmp locl calt liga` (GSUB) and `kern mark mkmk` (GPOS), with `init medi fina rlig` additionally for the Arabic tier; the produced subset's feature list must equal the source face's intersected with floor-plus-used, and `build_fonts.py` fails naming the dropped tag. A hardcoded list would have rejected the very face this ADR selects: `isol` is the unsubstituted default form and appears in no well-built Arabic sans's GSUB, and `curs` is absent from IBM Plex Sans Arabic entirely.

**7. Delivery.** Exactly one `<link rel=preload as=font>` in `<head>` — the body regular upright — and it is emitted **after** the VG Wort pixel preload. Mono, italic and every fallback load via `font-display: swap` with no preload. No external font host, ever.

**8. Ancillary fixes that fall out of this and are not optional.** `\setsansfont` beside `\setmainfont` in both `.sty` files, with `\renewcommand{\familydefault}{\sfdefault}` on the worksheet side, so decks stop being Latin Modern. `lle` gains a `latin-macron` fallback family — Noto Sans 2.015, restricted by `unicode-range` to the Latin-Ext gaps — because ȳ (U+0233) and Ȳ (U+0232) are absent from the **full** upstream Source Sans 3, not merely from the bundled subset. `kit/design/fonts/LICENSES/` holds `OFL-1.1.txt` and `Apache-2.0.txt`, and `ATTRIBUTION.md` carries one row per family with version, upstream release tag, licence file and the exact subsetting command.

## Consequences

- One typeface carries fourteen of eighteen courses, and the two script families that genuinely appear beside it are held to a measured metric rather than to a judgement.
- 13,576 emphasis spans render in a drawn italic for the first time, in three scripts.
- A live OFL §5 compliance gap closes.
- **Cost:** the four bundled Latin subsets and seven `.woff2` files are re-fetched and rebuilt; the re-fetch is a precondition for the embedded-font allowlist, not a nicety. Every committed PDF re-renders at its next regeneration and picks up both the corrected family names and the real italic.
- **Cost:** `code`, `pre`, `kbd` and `samp` in the four deferred codes fall through to the primary face at `0.94em`, because JetBrains Mono has no Arabic or Han. Declared in the stack, not left to chance.
- **Cost:** waves 5 and 6 cannot start until their tier payload is procured. That is stated as a refusal in `bin/kit sync` rather than discovered as tofu in a classroom.

## Alternatives considered

**Add a Noto tier per script.** Rejected. It replaces one face with four and makes the reader perceive a different design at every script boundary, when the face already in use covers Greek, Cyrillic and polytonic at 1,648 codepoints. The measured coverage table is what settled this.

**Noto Naskh Arabic, Amiri or Vazirmatn as the Arabic body face.** Rejected as the body face. One design language across eighteen courses is the governing requirement and a Naskh serif does not deliver it beside a humanist Latin sans; Vazirmatn carries Persian letterforms into an Arabic course; Noto Sans Arabic is geometrically flatter than the Latin it must sit beside. Naskh is retained where it is genuinely better — fully-vocalised script-stage passages — and scoped there.

**Keep browser-synthesised obliques.** Rejected. It is invisible on Latin and wrong on Cyrillic, and `font-synthesis: none` without a real italic would simply delete emphasis from 13,576 spans. The two ship together, in that order.

**Ship the deferred tiers now, unmeasured, at 100 % scale.** Rejected. That is the failure this ADR's clause 5 names explicitly.
