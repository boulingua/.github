# ADR 0007 — Language islands, not page mirroring

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0006 (typography), ADR 0008 (XeLaTeX, polyglossia + bidi), ADR 0018 (waves 5–6 deferred)
- **Reverses:** `spec:design-system` §3.1, which put `dir="rtl"` on `<html>` for `afl` and `pfa`

## Context

Two questions are usually treated as one and are not. The first is how a right-to-left course is laid out. The second is how *any* target-language run — French inside a German page, Greek, Cyrillic, Latin with macrons, Arabic — declares what language it is in.

The design spec answered the first by mirroring the whole page for `afl` and `pfa`. That answer does not survive contact with what these courses are. **The metalanguage is German.** Navigation, task instructions, CEFR badges, download buttons and the footer are German and must not mirror. `afl/ROADMAP.md:67-74` and `pfa/ROADMAP.md` both specify LTR chrome with wrapped Arabic runs — and those documents were written by the person who will author the content. Whole-page mirroring also requires an audit of hugo-coder's navbar, table of contents and footer that the design spec itself flags as unaudited risk. And a page declaring `lang="ar"` while its chrome is German makes a screen reader read German in an Arabic voice.

The second question has no answer at all today. There is no mechanism anywhere in the org for marking a target-language run. Every French sentence in `fle` and every English sentence in `efl` currently inherits the page's `lang`, which means a screen reader reads target-language content in the metalanguage's voice, and hyphenation is applied under the wrong language's rules. That is not an RTL problem; it is a defect on the three live Latin-script courses, and it exists now.

`{{< tl >}}` is one of seven shortcodes the educational standard is written against that **exist in no repository and are used zero times in any content**.

## Decision

**The page stays LTR. The target language renders in islands.**

The island is `{{< tl >}}`, and it is the mechanism for *any* target-language run, not an Arabic feature:

```
{{< tl >}}…{{< /tl >}}          →  <span lang="<target>" [dir="rtl"]>…</span>   (inline)
{{< tl block >}}…{{< /tl >}}    →  <div  lang="<target>" [dir="rtl"]>…</div>   (block)
{{< tl lang="grc" >}}…          →  explicit override, for a citation
```

**`lang` is always emitted.** `<target>` comes from `boulingua.yml → target_language`, so it is declared once per course and cannot be typed wrong per page.

**`dir` is emitted only when the course needs it** — `script_tier: arabic` — and omitted otherwise. A `dir` attribute on an LTR run is noise that invites a reader to think direction is being managed per element when it is not.

Supporting rules, all normative:

- `<pre>`, `<code>` and `.highlight` are forced `dir="ltr"` inside any RTL ancestor.
- Latin runs inside RTL prose are wrapped in `<bdi>`.
- CEFR identifiers, unit numbers and dates are always ASCII, `dir="ltr"`, `font-variant-numeric: tabular-nums`. `unit06` must be identical in the URL, in the front matter and on the page — a re-slug destroys registered marks (ADR 0003).
- The vocabulary table carries `lang` **per column**: the target column is `lang="<target>"`, the gloss column `lang="de"`. This is the single most valuable place the attribute lands, and it is why the island is a shortcode contract rather than a CSS class.
- The CSS logical-properties rewrite lands now, ahead of any RTL content: the eleven physical inline properties in `kit/assets/css/custom.css` become `inset-inline-start`, `padding-inline`, `border-inline-start`, `margin-inline-end` and so on. `flex-direction` (13 occurrences) is direction-neutral and allowlisted. This ships as hygiene under a gate rather than as an RTL prerequisite, because the Greek and Cyrillic courses exercise the same layout code and because retro-fitting it under time pressure at wave 5 is how a physical property survives.
- On the print side `\tl{}` is defined in `boulingua-tokens.sty` as the identity for Latin, Greek, Cyrillic and CJK, so the shortcode is a no-op in the four shipped script tiers and does not wait for bidi.

**`{{< tl >}}` ships in `kit v1.0.0`**, used by every course. Only the RTL print half — the `-rtl` templates, the `\LR`-wrapped watermark, the Arabic and Persian reference documents — defers to wave 5, where it is the first work item of the first Arabic course. Nothing in waves 1–4 depends on it.

The gate is an island check: every target-language run carries `lang`, and `dir` where the tier requires it; `<pre>`/`<code>` forced LTR; no physical inline property in a `style` attribute.

## Consequences

- Screen readers switch voice on the run, not on the page, which is the correct behaviour for a language course in any script — including the three Latin-script courses live today.
- Hyphenation and locale-sensitive rendering are correct on `gfl`, `rki`, `ufl`, `tfl` and `lle`, which whole-page mirroring would never have addressed because none of them is RTL.
- The gate is a small, reliable island check instead of a whole-page one, and hugo-coder's chrome needs no audit.
- **Cost, stated plainly:** a full-page Arabic reading passage renders inside an RTL block on an LTR page. The block mirrors correctly; the page scrollbar stays on the left. That is exactly how an Arabic text is presented inside a German textbook, which is what this is.
- **Cost:** authors must wrap target-language runs. It is a real authoring burden on every unit in every course, and it is why the shortcode ships in Phase 1 with an example page and a gate, rather than being introduced when the first Arabic course needs it.
- **Cost:** the shortcode is four artefacts — HTML renderer, LaTeX emitter, accessibility contract, gate — and none of it counts as done until all four exist. The LaTeX emitter is the half that gets forgotten, so it is named in the shortcode register.

## Alternatives considered

**`dir="rtl"` on `<html>` for `afl` and `pfa`.** Rejected, and this ADR reverses it. It mirrors German chrome that must not mirror, mislabels the page language for assistive technology, and requires a theme audit the spec proposing it flagged as unaudited risk. It also solves nothing for the fourteen LTR courses that still need per-run `lang`.

**Two site builds per RTL course — an LTR chrome build and an RTL content build.** Rejected. It doubles the URL space of a course, and every URL in this org is a potential VG Wort binding. Under ADR 0003 that is the most expensive possible way to answer a typographic question.

**A CSS class instead of a shortcode.** Rejected. A class carries no `lang` attribute, and `lang` is the entire point — it is what a screen reader, a hyphenation engine and the font stack all read. A class would style the run correctly and leave it silently mislabelled.

**Emit `dir` unconditionally, including `dir="ltr"` on Latin courses.** Rejected. It suggests direction is being tracked per element in courses where it is not, and it is exactly the kind of always-present attribute that later gets copied into a context where it is wrong.

**Defer `{{< tl >}}` with the Arabic tier.** Rejected. It is the mechanism for any target-language run; deferring it would leave the three live courses and the Greek, Cyrillic and macron courses with no way to declare a language at all.
