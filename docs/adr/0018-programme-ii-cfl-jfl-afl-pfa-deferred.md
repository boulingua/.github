# ADR 0018 — Programme II: `cfl`, `jfl`, `afl` and `pfa` defer out of this programme

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0006 (typography), ADR 0007 (RTL islands), ADR 0008 (XeLaTeX, polyglossia + bidi), ADR 0013 (`core-restricted`), ADR 0016 (release policy)

## Context

The build-out is ordered in six waves. Waves 1–4 are eleven new courses — `nsf` `nvt` · `ele` `ils` `ple` · `pfl` `tfl` `lle` · `gfl` `ufl` `rki` — all Latin, Greek or Cyrillic, all served by one type family once the full upstream Source Sans 3 lands. Waves 5 and 6 are `cfl` Chinese, `jfl` Japanese, `afl` Arabic and `pfa` Persian, and they require a different class of enablement: a content-derived CJK subsetter and its two-tier fallback, `xeCJK` and the CJK print tier, the `{{< furi >}}` ruby layer in two renderers, the whole of the RTL work (polyglossia + bidi, the `{{< tl >}}` island layer, gate C12, the Arabic subset feature-list guard in `build_fonts.py`), and procurement of IBM Plex Sans Arabic, Noto Naskh, Amiri, Noto Sans SC and Noto Sans JP.

Rated on this programme's own scale those items are **L / L / L / M** — roughly ten engineering weeks. Nothing in waves 1–4 consumes any of it, and none of it produces a single reader-visible page until an author writes the first Chinese or Arabic unit.

That author cannot start unassisted. The standard forbids shipping a unit in a language the author is not native in without a **named, dated native checker** recorded before the work begins. These four are precisely the languages where German-L1 overlap makes a checker hardest to find — which puts the programme's largest unresolved dependency at the far end of its longest engineering queue. Sequencing them last does not reduce that. Removing them from the path does.

There is also a hard blocker on `pfa` today: `acc-pfa` is absent from both `.sty` files and `brand/icons/` holds **17 PDFs, not 18**, so `\blgsetlang{pfa}` fails at `\includegraphics`.

## Decision

**This programme ships waves 1–4. `cfl`, `jfl`, `afl` and `pfa` are removed from its critical path, its schedule and its acceptance criteria, and re-open as a successor programme, *Boulingua Non-Latin II*.**

**Their design decisions stand. Only their enablement is unscheduled.** The typography rows for all four, the RTL-island reversal and the single-TeX-engine decision are recorded now (ADR 0006, ADR 0007, ADR 0008) because they are cheap to write down and expensive to re-litigate, and because the typography continuity argument only holds if it is stated across all eighteen.

**Re-entry is gated per language, and every language needs both conditions closed before any engineering is spent on it:**

| Code | Named native checker | Voice decision, closed | What that language then pays for |
|---|---|---|---|
| `cfl` | required, recorded in the `new-language` issue form | `auditions/cfl.md` committed | content-derived Noto Sans SC subsetting + `xeCJK` (L); strictly LTR, no ruby |
| `jfl` | required | `auditions/jfl.md` committed; `ja_JP` is unresolved and `status: none` is an acceptable close | the `{{< furi >}}` ruby layer in HTML and XeLaTeX (M); inherits all of `cfl`'s subsetting |
| `afl` | required | `auditions/afl.md` committed | bidi itself (L) — polyglossia, `\setotherlanguage{arabic}`, IBM Plex Sans Arabic |
| `pfa` | required | `auditions/pfa.md` committed | Persian orthography, Eastern digits, the ezāfe policy; inherits `afl`'s bidi |

A voice decision is closed by a committed `auditions/<code>.md` verdict from `bin/kit audio audition <code>`, and **`status: none` is a first-class close**, not a failure — a text-first course is shippable, and audio never blocks content. No voice ID may be written into a ROADMAP, a `get_voices.sh` URL or a README promise before that verdict exists.

Two programme-level conditions apply on top: waves 1–4 at conformance M2 or better on all eleven courses, so the runbook is proven across three script tiers before a fourth is attempted; and the deferred enablement re-scoped as its own foundations phase, with `bin/kit` and the gate battery already load-bearing rather than newly written.

**What is not deferred, because waves 1–4 need it anyway:**

- **`pfa`'s missing assets still ship.** `brand/icons/pfa.pdf`, `website/static/icons/pfa.svg` and the `acc-pfa`/`acch-pfa` colour pair are generated in this programme. The org registry is complete at 18 or gate A11's `icon count ≠ 18` check is a permanent known failure, and a permanent known failure is how a battery becomes advisory.
- **`{{< tl >}}` ships in `kit v1.0.0`.** It is the mechanism for any target-language run, not an Arabic feature: `gfl`, `ufl` and `rki` need it for `lang`/`dir` correctness under gate C12, and `lle` needs it for `\textlatin` discipline. Only `{{< furi >}}` defers, with `jfl`.
- The CSS logical-properties rewrite lands as hygiene under gate A8; `fonts.yaml`, `build_fonts.py` and the `script_tier` mechanism ship in F3 for Greek and Cyrillic; the two-language print API ships in F5a.
- All four rows stay in `data/accents.yaml`, in the typography matrix and in the per-language dossier. **`worldmap.yaml` keeps all four pins at `status: upcoming`** — announced as planned, not as coming — and no README in any of the four promises a date.

**Chrome language, decided here so it is not re-opened:** German, for all fifteen scaffolds, including `afl` and `pfa` when they return. That closes the English-versus-German question left open at `afl/ROADMAP.md:296-298` and means one i18n file rather than fifteen.

## Consequences

- **The programme drops from roughly 1,425 author-days to roughly 1,100** — about **322 author-days** removed — and about **ten engineering weeks** leave the critical path. At 200 productive authoring days a year the remainder is 5.5 years; at the ~100 days a working teacher can sustain alongside a teaching load it is a decade. That shape is stated out loud rather than discovered in month seven.
- **Four scaffold repositories sit at Stage 1 — empty, building, deploying, zero units — for the duration.** They carry no marks, so nothing is at risk and no reader sees a broken promise.
- Each of `afl/ROADMAP.md`, `cfl/ROADMAP.md`, `jfl/ROADMAP.md` and `pfa/ROADMAP.md` gains a dated note at the head of §1 recording the deferral and its entry conditions, so nobody re-derives the decision from the wave table alone and reaches the opposite answer.
- The successor programme inherits a proven runbook, a working `bin/kit`, a load-bearing gate battery and eleven courses of evidence about where the runbook is wrong. That is worth more than a ten-week head start on font tooling.
- The one dependency the programme cannot satisfy from its own resources — native checkers for languages the author does not speak — is removed from the critical path of the eleven courses where German-L1 overlap makes checkers findable, rather than being carried as an open risk across the whole plan.

## Alternatives considered

**Keep waves 5 and 6 and sequence them last.** Rejected. Sequencing leaves the checker dependency standing at the end of the longest engineering queue, where it blocks the most accumulated investment and where discovering it is unsatisfiable is most expensive. The risk is not reduced by ordering; it is reduced by removal.

**Build the enablement now and author later.** Rejected. Ten engineering weeks of subsetting, `xeCJK`, ruby and bidi produce nothing a reader can see until the first Chinese or Arabic unit exists, and unused tooling rots against the platform it targets.

**Drop the four languages entirely.** Rejected. The typography, RTL and TeX-engine decisions are already made and cost nothing to hold; deleting the rows means re-deriving them later at full price, and the continuity argument for the type system needs all eighteen stated at once.

**Ship a Chinese or Arabic course without a native checker, and correct it on reader reports.** Rejected. It inverts the responsibility of a course that presents itself as an educational resource, and there is no cheap correction path once material is in classroom use.

**Set the chrome language of each course to its target language.** Rejected — Greek-medium chrome for absolute-beginner German pupils is what `gfl/ROADMAP.md:56,85` currently proposes, without weighing it. The audience is the German Gesamtschule; the chrome is German and the content is the target language.
