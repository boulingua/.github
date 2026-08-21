# ADR 0012 — One framework, plus secondary anchors; `bildungsplan-bw` is an anchor, not an alternative

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0011 (the resolver), ADR 0003 (URLs are frozen), ADR 0013 (`core-restricted`), ADR 0019 (`url-lock.csv` from the T.O.M. export)

## Context

`pagegen/docs/front-matter-fields.md:56,61` models the framework field as an enum with two mutually exclusive values: `framework: cefr | bildungsplan-bw`. That models a choice where there is no choice to make. The Bildungsplan is a **state syllabus** — Baden-Württemberg's, with its own code tree, its own Niveau letters and its own Klassenstufen. The boulingua curriculum is a **descriptor catalogue** — 1,170 statements over 79 in-scope scales and seven levels. They are orthogonal axes, and a Gesamtschule course needs both at once: it must satisfy the state syllabus its learners are examined against, and it must be traceable against CEFR descriptors so a learner outside that state can read the course at all.

The measured consequence of the enum: `efl` and `fle` both carry a `bildungsplan:` block and **zero CEFR descriptor IDs**. Across the whole org, no page carries a descriptor ID today. A 1,170-statement framework sits in `curriculum/` that literally nothing consumes.

The knock-on is in the taxonomies. `efl` carries 1,356 tag occurrences across 54 distinct values, of which **816 occurrences are numeric Bildungsplan codes** — `efl/content/track-e/kl09/units/unit01-future-careers/index.md:28-36` lists `reading`/`speaking`/`language_awareness` at `:29-31` and then `3.2.1`, `3.2.3.2`, `3.2.3.3`, `3.2.3.7`, `3.2.3.8` at `:32-36`, producing taxonomy terms such as `/tags/3-2-3-7/`. `fle` (936 occurrences, 13 distinct) and `daf` (299, 22) mirror nothing numeric. A syllabus code that has no home in the schema ends up in `tags:`, and from there it reaches URLs.

## Decision

**One framework, `boulingua-curriculum`, declared as a constant. Zero or more secondary anchors alongside it.**

The enum values `cefr` and `bildungsplan-bw` are removed. `front-matter-fields.md:50-70` is replaced wholesale by:

```yaml
curriculum:
  framework: boulingua-curriculum       # const
  level: B1
  implements:                            # REQUIRED on unit|exam, 3–6 entries
    - B1.INT.conversation.02
    - B1.REC.reading-for-information-and-argument.01
  can_do:                                # optional, bound to an id, course's own wording
    - { id: B1.INT.conversation.02, text: "Ich kann …" }
  bildungsplan:                          # efl/fle only
    plan: bw-2016-englisch
    niveau: E ; klassenstufe: 9 ; track: e
    codes: ["3.2.3.2", "3.2.3.3"]
    topic_codes: ["3.2.1"]               # Orientierungswissen — no CEFR counterpart
```

Rules that follow from it:

- **`implements` is required and non-empty on every unit and exam page.** This single change converts curriculum from prose into enforcement.
- **At least one ID must come from a domain other than the unit's primary skill domain**, evaluated against the eight-domain enum `{REC, PROD, INT, MED, PLUR, LING, SOC, PRAG}`. It forces breadth.
- `cefr_level` → `curriculum.level`; `cefr_can_do` prose → `can_do[]` entries, each bound to a chosen ID. `pruefungs_module` moves to top level — Goethe exam modules are an exam-format concern, not a framework one.
- **`topic_codes` exists because Orientierungswissen has no CEFR counterpart.** A secondary anchor is allowed to carry material the primary framework does not model; that is what makes it an anchor rather than a rival.
- **Bildungsplan codes must not be mirrored into `tags:`.**

`crosswalks/bildungsplan-bw.yml` ships in `curriculum` v1.1.0 and is what makes the anchor machine-resolvable: `conformance_audit.py suggest --level L --domain D` ranks candidate descriptor IDs for a page from its existing `skills_focus` values and `bildungsplan:` codes, and an unresolvable Bildungsplan code is exit 3 — a hard failure, the same class as a dangling descriptor ID.

## Consequences

- **This is the largest single authoring cost in the programme, and it is booked honestly.** `daf` has `cefr_can_do` on 61 pages and `cefr_level` on 60, so for `daf` this is a rename plus 200–300 strings of authoring. `efl` (360 pages) and `fle` (312) have **no field to rename** — they carry `niveau: E` + `klassenstufe: 9` and a `bildungsplan:` block — so roughly **672 pages each need 3–6 IDs chosen by hand**. At 10 minutes a page that is about **14 author-weeks**, and it cannot be automated, because the entire value of `implements` is that a human asserted the mapping.
- Three mechanisms keep that from blocking every deploy the day the schema lands. **(1)** The gate ramps with the milestone: at M0 a missing `curriculum:` block is a `::warning::`, at M1 it is required on any page the PR touches, at M2 it is required repo-wide, with the milestone read from `boulingua.yml` so the ramp is a declared state rather than a per-PR judgement. **(2)** The backfill is a per-level tranche, one `klassenstufe` per commit, each tranche moving that level to M1; a tranche that is not done does not block one that is. **(3)** `suggest` does the ranking, which is what makes 10 minutes a page realistic rather than 30.
- `skills_focus` normalises to one 8-value English enum — `reading`, `listening`, `speaking_interaction`, `speaking_production`, `writing`, `mediation`, `language_awareness`, `intercultural` — replacing today's 7, 11 and 6 values in `efl`, `fle` and `daf`. `efl`'s seven and `daf`'s six are clean one-to-one lookups. `fle`'s eleven contain a genuine intra-field split (`hör_hörsehverstehen` 18 against `hoerverstehen` 2) and three singletons, and it also puts non-ASCII in a taxonomy key that reaches URLs; it is the only repo where the migration must inspect individual pages.
- **`speaking` → interaction or production cannot be resolved mechanically.** It is decided per unit from `implements` — an `INT.*` ID implies interaction, a `PROD.*` ID production — so it lands **after** that unit's `implements` tranche, never before. It is the one place where descriptor IDs drive the migration instead of following it.
- Removing the 816 numeric codes from `efl`'s `tags:` changes 180 pages and deletes roughly 40 taxonomy terms. Those term pages carry no marks — marks sit on units, exams and appendices — so the deletion is URL-safe, but that is **proved by `bin/kit urldiff` against `url-lock.csv` in the same commit, not asserted.**
- **Blocked until the T.O.M. export closes.** `url-lock.csv` cannot be generated until the T.O.M. export exists (ADR 0019), and no URL may move before it. The tag-term deletion therefore waits on P0.0 even though the analysis says it is safe.
- Migration is a `ruamel.yaml` round-trip, never a regex pass. `efl`'s files interleave `aliases:` between `skills_focus` and `presentation:`; a `sed` pass would silently corrupt front matter. Every migration script writes to a temp file and re-parses before replacing.

## Alternatives considered

**Keep `framework: cefr | bildungsplan-bw` as an enum.** Rejected. It is the reason `efl` and `fle` carry zero descriptor IDs. Forcing a course to pick one axis makes the other unrepresentable, and both are real.

**Make `bildungsplan-bw` a second framework, with parallel `implements` blocks.** Rejected. Two frameworks means two coverage computations, two conformance targets and two things a course can be conformant to, and the resolver would have to reconcile them. The Bildungsplan publishes a syllabus, not a descriptor scale set; there is nothing to compute coverage against.

**Drop `bildungsplan:` entirely and keep only descriptor IDs.** Rejected. `efl` and `fle` serve Baden-Württemberg Gesamtschulen and are examined against that syllabus. Removing the codes makes the courses less usable to their primary audience to buy schema tidiness.

**Leave Bildungsplan codes in `tags:` as today.** Rejected. It produces taxonomy terms like `/tags/3-2-3-7/`, which are neither a topic nor a competence and are not something a learner would ever browse; and it puts a syllabus identifier into a URL-generating field, which under ADR 0003's freeze is a liability rather than a mistake that can simply be corrected.
