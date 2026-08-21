# ADR 0014 — EQS-1 is normative: five step keys, localised headings, one exam page per unit

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0002 (the gate battery), ADR 0012 (one framework), ADR 0017 (three taxonomic axes), ADR 0019 (T.O.M. reconciliation) · ADR 0020 (that reconciliation is deferred to the end; a provisional lock holds the URL space meanwhile)

## Context

EQS-1 is canonical at `curriculum/standards/EQS-1.md`, with `standards/eqs.yml` for thresholds, `standards/step-map.yml` for the heading contract, `assessment/rubrics/rubrics.yml` and `standards/checklists/unit-review.md`. The test it has to pass is that an author writing a Norwegian A1 unit and an author writing a Ukrainian A1 unit, working from EQS-1 alone and never having seen each other's work, produce pages one checker can validate and a reader recognises as the same object.

The shipped corpus makes clear why structure cannot be carried by heading text. Headings are in the content language, and all three are correct:

```
efl : ## Lead-in story  ## 1. Activate  ## 2. Input  ## 3. Practise  ## 4. Produce  ## 5. Reflect
fle : ## Situation de départ  ## 1. Activer  ## 2. Apporter  ## 3. S'entraîner  ## 4. Produire  ## 5. Réfléchir
daf : ## Einstieg  ## Input  ## Üben  ## Anwenden  ## Reflexion
```

A checker written from an English block list rejects every `fle` and every `daf` unit on the day it lands. The divergence is wider than the step names: `efl` writes `## Lead-in story` (×180), `## Exam example` (×180), `## Further reading / listening` (×180), and splits framework alignment across two wordings of its own — `## Bildungsplan alignment` (108) and `## curriculum framework ("Bildungsplan") alignment` (72).

Three further facts are load-bearing. `daf` has no Activate step at all — `## Einstieg` is the lead-in and four steps follow it. `efl`'s `## Exam example` block *is* the exam: measured pairwise across all 180 unit/exam pairs, the in-unit block runs a median 1,502 characters against 1,546 on the sibling page, and in zero of the 180 pairs is the exam page materially larger than the block it duplicates. And answer keys use three mechanisms — `{{< callout collapse="true" >}}` (900 call sites in `efl`), a bare `## Solutions` heading between steps 3 and 4 (156 `fle` units), and `{{< details >}}` (57 uses in `daf`) plus `## Lösungen` (10).

## Decision

**EQS-1 is normative for every course. Structure is carried by keys and front matter, never by the wording of a heading.**

1. **Five canonical step keys: `activate · input · practise · apply · reflect`.** They are English, machine-readable and declared in a front-matter `steps:` block emitted by the archetype. Each `h2` carries its key through the heading anchor `kit`'s render hook emits (`## 2. Apporter` → `id="input"`). **Gate A12 resolves and matches on the key, never on heading text.**
2. **Headings are localised labels, resolved through i18n.** `kit/eqs/step-map.yml` maps each key to one label per content language plus a list of accepted synonyms; the label is the only thing that ever appears on a page. The label set for step 4 is *Produce* / *Produire* / *Anwenden*, unchanged on all 396 shipped units. Synonyms are accepted for one release after a course adopts EQS-1, after which `bin/kit content relabel <code>` rewrites them in one commit per repo.
3. **Legacy anchors are preserved through `anchor-aliases.yaml`.** The render hook emits the canonical `id` plus every historical fragment recorded for that key, as empty anchor targets on the same heading, so `#produce`, `#produire`, `#anwenden` and `#4-produce` keep resolving after the key rename. Anchors are not URLs: no page URL changes and no Zählmarke is affected, and `bin/kit urldiff` proves that before the merge rather than asserting it.
4. **Every unit has exactly one sibling exam page, and the unit's `exam` block is a pointer only** — format, duration, points, skills tested, and a link. The duplicated exam is **transferred**, not deleted.
5. **Answer keys live in `{{< details >}}`.** `kit` ships it as canonical and keeps `collapse="true"` on `{{< callout >}}` as a delegating alias rendering identical markup, so `efl`'s 900 call sites need zero content edits.
6. **Word bands are calibrated to the pedagogy, not to the corpus.** Band I (pre-A1–A2 / Kl. 5–7) body 950–1500 w, exam ≥1900 rendered characters · Band II (B1–B2 / Kl. 8–10) 1000–1800 w, ≥1900 · Band III (C1–C2 / Kl. 11–13) 1500–2800 w, ≥2200. The counting rule — front matter, shortcode calls, fenced blocks and markdown markup stripped — is fixed in `standards/eqs.yml` **before** EQS-1 gates anything, so the argument is about content and not about arithmetic.

## Consequences

- **The bands collide with `efl`, and the collision is booked rather than waived.** Measured on the 180 shipped unit bodies under the fixed counting rule: **74 fall below the Band I 950-word floor today** (minimum 688, median 972), concentrated in Kl. 5 (17/24), Kl. 6 (21/24), Kl. 8 (13/24) and Kl. 9 (12/24). The de-duplication EQS-1 mandates removes a median 250 words per unit, after which **132 of 180 fall below 950**. `fle` (minimum 1,181) and `daf` (minimum 1,062) pass comfortably, which is how the bands came to be calibrated against them.
- **Therefore C6 and A12 run `warn` on `efl` until its retrofit closes, and blocking everywhere else from day one.** The remediation is booked as P3.6 — 132 units needing 150–350 words of genuine content each, roughly half an author-day apiece, ~65 author-days — scheduled after wave 1 has proven the factory runbook, because the runbook produces the pattern these units are missing. The count is reported month over month in the weekly `org-audit` issue; a count that stops falling is a risk materialising, not a schedule slip.
- **The exam transfer clears 264 of the 268 under-floor exam pages**: `efl` from 129 of 180 under 1,800 rendered characters to 0, `fle` from 139 of 156 to 4. It is the largest identified monetary item in the programme and it is retired by moving text that already exists to the page it was always about. It is a content edit on two pages that both already exist, both keep their URLs and both keep their marks, and it runs before the `efl` materials-commit flip because it changes the LaTeX input for 336 worksheets.
- **A page is never padded to reach the floor; it is completed to reach it.** The four surviving `fle` exam pages are completed individually.
- `daf` authors an Activate step in 60 units (≈15 author-days) and 60 new exam pages. Adding an exam page creates a *new* URL rather than moving one, so it is not gated by ADR 0019 — but up to 60 fresh codes must be drawn from T.O.M., which is an external dependency with a lead time, and each new exam is assessed individually against the 1,800-character floor.
- `fle`'s 309 `## Solutions` relocations and `efl`'s answer-key retrofit are gated on `kit` shipping `{{< details >}}`; neither repo ships it and both use it zero times today. Until the shortcode set exists, A12's clauses that depend on a shortcode run `warn`, flipping to blocking in the release that tags `kit v1.0.0` — never before, so no course is ever blocked on a template that does not exist.
- `efl` gains `teacher_notes` free: it is a relabel of the hand-written `## Downloads` under which all 180 units keep their teacher prose. The hand-written `## Downloads` is itself a defect — the layout emits that heading.

## Alternatives considered

**Keep `produce` as the canonical key.** The objection was that renaming touches 396 shipped units in three languages and breaks every external deep link into a step. `anchor-aliases.yaml` answers the second at the cost of one generated file, and the first shrinks to a front-matter key nobody types once headings are localised labels — the visible headings do not change at all. `apply` is adopted because it names what step 4 normatively requires: a task with a non-linguistic outcome, never a gap-fill, transformation or translation drill.

**Match on heading text against an English block list.** Rejected. It rejects every `fle` and every `daf` unit on day one, and it is the reason the step-map exists.

**Rename roughly 1,100 headings to one canonical English wording.** Rejected. That is a migration, not a standard, and it makes the standard unusable for the fifteen languages that have not been written yet.

**Leave the exam inside the unit and let the sibling page stay a stub.** Rejected. 268 exam pages carry registered marks that can never count, and the pedagogy is worse in the same direction: assessment trapped in a unit cannot be printed, embargoed or version-controlled separately.

**Lower the Band I floor so the shipped corpus passes.** Rejected. The floor is a pedagogical claim; moving it to make a corpus conform is the same category of error as removing a scale from `scale-registry.yml` to make a course conform.

**Keep three answer-key mechanisms and check all three.** Rejected. One mechanism with one delegating alias costs `efl` nothing and gives print a single `data-role="key"` rule to exclude keys from the learner PDF and include them in the teacher PDF.
