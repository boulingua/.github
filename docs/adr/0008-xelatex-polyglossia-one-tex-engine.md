# ADR 0008 — XeLaTeX for all 18 courses, polyglossia, one TeX engine

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0001 (`kit/latex/`), ADR 0006 (typography), ADR 0007 (RTL islands), ADR 0009 (materials committed), ADR 0018 (waves 5 and 6 deferred)

## Context

Every print artefact this org ships today is XeLaTeX output. `build_materials_latex.py:305-309` shells `xelatex` directly, and both style files already load fontspec — `slidegen/beamerthemeboulingua.sty:7` and `sheetgen/boulingua-sheet.sty:7`. Font selection is by path (`\setmainfont{SourceSans3}[Path=fonts/, Extension=.ttf, …]`, `slidegen:50-51`, `sheetgen:69-71`), which is a fontspec construction. There is no pdfLaTeX artefact anywhere in the org.

There is one exception, and it is the reason this decision has to be written down rather than assumed: `daf`'s 60 exam download PDFs are pandoc/LuaHBTeX output under TeX Live 2026, embedding Latin Modern Roman and FontAwesome 5. They are a serif document set inside a sans design language, produced by a toolchain no other artefact in the org uses.

The eighteen courses span seven script tiers. Four are paid for in this programme — `core`, `latin-ext`, `greek`, `cyrillic` — and three are declared in `kit/design/fonts.yaml` with `status: deferred` and no committed binaries: `arabic`, `hanzi-sc`, `kana-kanji` (F3). The deferred three are the ones that decide the engine question, because they are the ones that need bidi and CJK.

Two multilingual packages are candidates: babel and polyglossia. Under XeTeX, babel's Arabic support routes through `bidi` regardless, so choosing babel adds a layer, subtracts nothing, and carries a longer list of beamer incompatibilities.

## Decision

**XeLaTeX is the only TeX engine in this org, for all eighteen courses, on both the deck and the worksheet path.**

Multilingual switching is **polyglossia**, not babel. `\setdefaultlanguage{german}` with `\setotherlanguage{…}` per target language. Two macros carry it into the templates:

- `\blgsetlang{<code>}` keeps its one-argument signature (already emitted as `\blgsetlang{@@LANG@@}` by `build_materials_latex.py:285,294`) and selects accent and hover colours, `\blglangmark` → `brand/icons/<code>.pdf`, script and font tier, and direction.
- `\blgsetui{<polyglossia-lang>}` sets the **instruction** language, defaulting to `german`. Every page in every course is German instructions around target-language content, and the print side had no way to say so.

**The package load order is normative:**

```
fontspec → xcolor → boulingua-tokens → geometry → [others] → xeCJK (cfl, jfl) → hyperref → polyglossia
```

Violating it silently breaks bidi or CJK rather than failing. `sheetgen/boulingua-sheet.sty` today loads fontspec at `:7`, xcolor at `:8`, geometry at `:9` and hyperref **last** at `:21` — correct up to the last step; `boulingua-tokens` inserts between `:8` and `:9` (F2) and hyperref moves ahead of the new polyglossia line. `slidegen` inherits hyperref from beamer and takes polyglossia after `\usetheme`.

**The bidi and xeCJK slots in that order are reserved and unfilled.** The polyglossia line, the `\setotherlanguage{arabic|persian}` calls, `kit/latex/{slides,worksheet}-template-rtl.tex`, the `\LR`-wrapped watermark, the Arabic and Persian reference documents and gate D5's RTL half are deferred to wave 5 (F4b); the `-cjk` template and the `xeCJK` slot defer to wave 6 on the same terms. Both waves are deferred out of this programme by ADR 0018. The slot is declared now so that no `.sty` is written into a shape that has to be reordered later.

**`daf`'s 60 pandoc/LuaHBTeX exam PDFs are regenerated through `kit/latex/`** as part of P3.2's exam work. After that commit, no LuaTeX artefact exists in the org.

## Consequences

- One `Makefile`, one CI apt list, one set of rendering behaviours for one `.sty` pair. `kit/Containerfile` pins TeX Live 2026 / xdvipdfmx 20260317 and nothing else needs a second pin.
- Reproducibility is achievable. XeLaTeX writes a wall-clock timestamp and a random file identifier into every output, so `bin/kit materials` exports `SOURCE_DATE_EPOCH` and `FORCE_SOURCE_DATE=1` — which makes `xdvipdfmx` stamp a fixed `/CreationDate` — and normalises the PDF `/ID` before comparison. Without both, F5's twice-in-a-row acceptance criterion is unsatisfiable.
- **XeLaTeX prints "Missing character" and exits 0.** `xelatex()` at `build_materials_latex.py:305-309` only checks that a file exists, so it currently ships tofu as a success. Gate D5 therefore has two halves: a pre-flight cmap check against the family `\tl{}` will select, hard-exiting with codepoint, character, unit and font; and a post-flight PyMuPDF pass over every produced PDF scanning `page.get_text("rawdict")` for glyph id 0 and U+FFFD.
- `\DocumentMetadata{lang=<bcp47>, pdfstandard=ua-2}` for tagged PDFs is available on this engine, which §9.5's print accessibility floor requires.
- Anything that only LuaTeX can do is unavailable, permanently. Nothing currently planned needs it.
- If `jfl`'s furigana proves inadequate under the `ruby` package when wave 6 reopens, `jfl` print degrades to a documented parenthetical reading. It does not get a second engine.

## Alternatives considered

**LuaLaTeX.** Rejected. `bidi` is XeTeX-only, and `afl` and `pfa` own the RTL layer for the org. Adopting LuaLaTeX for some courses and XeLaTeX for the RTL ones means two Makefiles, two CI apt lists and two rendering behaviours for one `.sty` — the same `.sty` that gate D4 checks for print parity down to a ΔE2000 ≤ 2.0 accent-rule sample. Two rendering behaviours make that gate meaningless.

**babel under XeTeX.** Rejected. It reaches `bidi` anyway, so it buys a compatibility layer and no capability, and its beamer incompatibility list is longer than polyglossia's on the deck path where `slidegen` lives.

**pdfLaTeX.** Rejected outright. No OpenType, no fontspec, no `\setmainfont` by path; the whole type system (ADR 0006) is unbuildable on it.

**Keeping pandoc/LuaHBTeX for `daf`'s exam downloads.** Rejected. It is a third toolchain serving 60 files, it produces a serif document inside a sans design language, and its output cannot satisfy gates D2, D4 or D5 without duplicating all three for one artefact class.
