# ADR 0017 — `topic`, `bildungsplan.competence_areas` and `skills_focus` are three axes, not one

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0005 (design tokens), ADR 0012 (one framework plus secondary anchors), ADR 0003 (URLs are frozen), ADR 0019 (T.O.M. reconciliation) · ADR 0020 (that reconciliation is deferred to the end; a provisional lock holds the URL space meanwhile)

## Context

Three repositories ship a file called `data/topics.yml`. They agree on the filename and on nothing else:

```
daf/data/topics.yml : alltag arbeit gesellschaft kultur wissenschaft umwelt kommunikation   (60 pages set one)
efl/data/topics.yml : themen interkulturell text-medien                                     (180 pages set one)
fle/data/topics.yml : sprechen_dialog sprechen_monolog schreiben leseverstehen
                      hoerverstehen sprachmittlung text_medien                              (0 pages set any)
```

Read as one enum with three spellings, this looks like a normalisation task. It is not. The three files hold values from three different dimensions.

`daf`'s seven are **thematic** — what a unit is about — which is what a discovery network needs to colour and cluster by. `efl`'s three are Bildungsplan **competence areas**, documented as such in the header comment of its own `topics.yml`, distributed `themen` 65 · `text-medien` 69 · `interkulturell` 46, and they map into the seven nowhere; `themen` ("topics") in particular maps to nothing at all. `fle`'s seven are **skills**, duplicating `skills_focus`, and no `fle` page sets `topic:`.

The colour side is duplicated the same way. The seven topic hues live in three places that agree by hand — `daf/data/topics.yml`, `pagegen/assets/css/custom.css:614-620` (light) and `:631-637` (dark), plus `daf`'s copy — while `efl` and `fle` declare no `--network-topic-*` tokens at all and carry `color:`/`color_dark:` fields inside their own data files instead. Two mechanisms for one thing. The unknown-topic fallback is the literal `'#888'` at `daf/assets/js/network/main.js:28`, a hard-coded grey outside the token system.

## Decision

**Three axes, named separately, each with one home.**

1. **`topic:` is the thematic axis.** Closed at the seven values `{alltag, arbeit, gesellschaft, kultur, wissenschaft, umwelt, kommunikation}`, required on every unit and every exam page in every course. `data/topics.yml` is **generated** from `tokens.yaml`, and `tokens.css` owns the hues, so the CSS-versus-data-file split ends and the seven values live in one place.
2. **`efl`'s three values move to `bildungsplan.competence_areas`** — a list inside the `bildungsplan:` block that ADR 0012 defines, closed at `{themen, interkulturell, text-medien}`, populated only where a Bildungsplan applies, which today means `efl` and `fle`. It sits inside that block rather than at top level because a competence area is a construct of the state syllabus and has no meaning outside it, exactly as `topic_codes` does.
3. **`fle`'s seven topic values are deleted.** They are skills, and skills live in `skills_focus`, which normalises org-wide to one 8-value English enum: `reading`, `listening`, `speaking_interaction`, `speaking_production`, `writing`, `mediation`, `language_awareness`, `intercultural`.

**Landing rule, and it is binding: the `efl` rename lands in the same commit as the `data/topics.yml` replacement and the network-graph colour lookup.** The graph reads `topic` for node colour, so a split commit renders 180 grey nodes on a live site.

**Assigning a thematic `topic:` to `efl`'s 180 and `fle`'s 156 units is 336 editorial decisions**, roughly a minute each with the unit title in view — about one author-day per course — done inside the front-matter passes that already open every file. **It is not a transform and no script attempts it.** `text-medien → kommunikation` is a guess, not a mapping.

An unregistered `topic` value fails gate A2 at source, before it can reach the renderer, and `'#888'` becomes `var(--boulingua-fg-muted)`.

## Consequences

- **The `efl` reclassification is deferred to P3.7, alongside the unit-body remediation, and is not part of the front-matter migration.** It is per-unit editorial judgement on 180 pages on an axis the pages were never authored against; booking it with the mechanical migration would have hidden about two author-days of judgement inside a rename.
- **`fle` gets its seven thematic values for free**, in the sense that no page sets `topic:` today, so there is no reclassification — only assignment, in the P3.3 pass that opens all 156 unit files anyway.
- **The three axes make cross-course comparison possible for the first time.** With `topic` thematic everywhere, the materials network can put an `efl` unit and a `daf` unit on the same graph and have the adjacency mean something. Under the current arrangement, an edge between a `themen` node and an `alltag` node would be an artefact of two unrelated vocabularies sharing a field name.
- **Where `topic` is registered as a taxonomy it generates term pages, so any reclassification changes the term set.** Those term pages carry no marks — marks sit on units, exams and appendices — but that is **proved by `bin/kit urldiff` against `url-lock.csv` in the same commit, not asserted**, and `url-lock.csv` does not exist until the T.O.M. export closes (ADR 0019). The same constraint governs the removal of `efl`'s 816 numeric Bildungsplan codes from `tags:`.
- `skills_focus` normalisation is cheap in two repos and not in the third. `efl`'s seven values and `daf`'s six are one-to-one lookups. `fle`'s eleven contain a genuine intra-field split (`hör_hörsehverstehen` 18 against `hoerverstehen` 2), three singletons, and non-ASCII in a taxonomy key that reaches URLs; it is the only repo where the migration inspects individual pages.
- The `speaking → speaking_interaction | speaking_production` split cannot be resolved mechanically and is decided per unit from `curriculum.implements[]` — an `INT.*` ID implies interaction, a `PROD.*` ID production — so it lands after that unit's `implements` tranche, never before.
- **`tags:` stops shadowing both axes.** `efl` mirrors its skills and its Bildungsplan codes into `tags:` (1,356 occurrences across 54 values, of which 816 are numeric codes), and `daf` mirrors skills there in German (`hören` appears 121 times in `tags:` and never in `skills_focus`). A hand-maintained shadow of a machine-meaningful field is removed rather than deduplicated.

## Alternatives considered

**One enum, and normalise the three files into it.** Rejected. `themen` maps to nothing in a thematic enum, and forcing it produces a value that is wrong on 65 `efl` pages while looking tidy in a data file.

**Crosswalk `efl`'s three into the seven.** Rejected on the same ground. `text-medien` covers text and media competence across every theme; mapping it to `kommunikation` asserts a relationship between a competence area and a subject that does not hold, and it would then drive node colour on a public graph.

**Keep three per-repo enums and let each course own its own axis.** Rejected. It is the state that produced three colour sources, two colour mechanisms and a hard-coded `'#888'`, and it makes the fifteen scaffolds inherit a choice they have no basis to make.

**Put competence areas at top level as `competence_area:`.** Rejected in favour of nesting under `bildungsplan:`. ADR 0012 already established that the anchor block is where syllabus-specific material lives — that is what makes `bildungsplan-bw` an anchor rather than a rival framework — and a top-level field implies every course has one, which twelve of eighteen never will.

**Drop `topic` and colour the network by CEFR level instead.** Rejected. Level is already carried by `curriculum.level` and is visible in the URL and the page chrome; colouring by it would spend the graph's only strong visual channel on the one attribute a reader already knows.
