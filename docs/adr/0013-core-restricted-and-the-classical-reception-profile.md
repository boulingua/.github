# ADR 0013 — `core-restricted` conformance and the `classical-reception` profile for `lle`

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0011 (the resolver), ADR 0012 (one framework), ADR 0006 (the `latin-macron` fallback)

## Context

Conformance targets in this org are computed, not asserted. A `(level, scale)` **cell** is a pair from the 79 `in_scope: true` scales in `curriculum/schema/scale-registry.yml` and the seven level files; a cell is **populated** when its section carries a `yaml` block with at least one `status: active` statement, and `no-official-descriptor` when it carries the marker line instead. Every cell is one or the other. At `curriculum` HEAD on 2026-08-21 that gives 441 populated cells of 553, and the declared targets `core` (A1–B1) = **206** cells, `full` (A1–C1) = **356**, `complete` (A1–C2) = **412**. A course declaring level *L* covers ≥90 % of *L*'s populated cells and declares 100 % of the remainder in `gaps[]`.

That arithmetic assumes a living language. `lle` (Latin) is the one course in the eighteen where it does not hold. Its audience is Latinum candidates and adult readers; its span is L0 plus A1r–B2r, where the `r` is reception. There is no speech community to interact with, so the spoken-interaction scales and the spoken half of production have no realisable content — not because the course is incomplete, but because the language's use case does not contain them. Forcing `lle` to declare `core` would either make it permanently non-conformant against scales it can never meet, or push it to write `gaps[]` entries with no honest `scheduled:` date, which corrupts the gap mechanism for every other course.

The current scaffold already reached for this and had no legal way to say it: `lle/ROADMAP.md:77` writes `declared_conformance: core (reception)` — a freeform string the schema does not accept and the resolver cannot parse.

The audio side is settled on verified ground: upstream Piper ships **no `la` voice**, so `lle` is transcript-only and its README carries the reworded promise (*"native-voice audio where an openly-licensed voice exists; transcripts always"*) rather than an unqualified one.

## Decision

**`core-restricted` is a legal value of `declared_conformance`, and it is legal only in combination with a declared `profile:`.**

**`lle` declares `declared_conformance: core-restricted` with `profile: classical-reception`.** `lle/ROADMAP.md:77`'s illegal `core (reception)` is corrected to those two fields in P0.7.

**`profiles/classical-reception.yml` ships in `curriculum` v1.1.0** (F8). The profile file — not this ADR, and not the course — enumerates the scales it places out of scope: the spoken-interaction scales and the spoken half of production, the ones a language with no living speech community cannot realise. The resolver reads that list and **recomputes the denominator** from the pinned framework by the same cell rule as every other target. No count is written into a course, a ROADMAP or this record, because a count written in prose is a count a gate will eventually disagree with.

**A profile narrows the universe; it never lowers the bar.** Within the restricted denominator, `lle` meets the same ≥90 % threshold as every other course, and it meets reception, mediation, language-awareness, sociolinguistic and pragmatic scales in full. `core-restricted` is a smaller set of cells covered to the same standard, not the same set covered less well.

**`out_of_scope[]` is legal only with a declared profile, and only for language-intrinsic exclusions.** Author capacity is a **gap**, never an exclusion. A course that is behind writes `gaps[]` with a specific reason and a `scheduled:` date; a course that structurally cannot cover a cell declares a profile. Those are different claims and the schema keeps them apart.

**`lle` is the only course in this programme that may use either.** Every living language declares `core` or `full`. Any further profile, and any further use of `core-restricted`, requires its own ADR.

## Consequences

- `lle` becomes the resolver's hardest test, and deliberately so: it is the only course exercising a declared profile, a restricted denominator and a recomputed target. It is scheduled in wave 3, behind `pfl` and `tfl`, on Latin script with no new font tier beyond the macron fallback — so the profile machinery is proved on the cheapest possible course rather than on one that is also paying for a script.
- The profile must exist before `lle` opens. It ships with `curriculum` v1.1.0 in F8, which is Phase 1, and wave 3 is Phase 5. There is no sequencing risk.
- `lle`'s excluded scales are published, not hidden. `gaps.yml` and the profile's exclusion list render on the course's public **Framework** page: a reader of a Latin course is told in the course's own pages that it does not teach spoken interaction and why. That is a feature of an honest OER.
- `lle` ships **35–36 units and 35–36 exams** at `core-restricted`, against a 45–48-unit plan. Stage IV (B2r) sits outside `core-restricted` and is not priced.
- Audio is transcript-only for the whole course, with `status: none` as a first-class state: `build_audio.py` exits 0 with a message and the layout still renders the transcript section. Gate D6 does not require an `auditions/lle.md` verdict where no voice exists. `lle/ROADMAP.md`'s option of approximating with an Italian or Spanish voice is **closed as rejected** — a neighbouring language's voice is never a fallback, org-wide.
- `lle`'s `must_render` set (`ā ē ī ō ū ȳ Ā Ȳ`) still exists and is still gated, because F3's `latin-ext` reference document consumes it. ȳ (U+0233) and Ȳ (U+0232) are absent from the full upstream Source Sans 3, so `lle` ships the `latin-macron` Noto Sans fallback under ADR 0006. The conformance profile changes nothing about that.
- The schema gains a value that can be misused. It is constrained three ways: `core-restricted` without `profile:` fails validation (exit 2); a profile the framework does not ship is unresolvable; and any new profile needs an ADR. Lowering the framework itself to make a course pass — removing a scale from `scale-registry.yml`, or flipping `in_scope` — is prohibited outright and would require an ADR plus a MAJOR release.

## Alternatives considered

**`lle` declares `core` and lists the spoken scales in `gaps[]`.** Rejected. `gaps[]` entries carry a `scheduled:` date, and there is no date on which Latin acquires a speech community. It would put a permanent falsehood into the one mechanism the org relies on to be honest about what is not yet written, and it would make `lle` show a growing gap list forever for reasons that have nothing to do with the author.

**`lle` declares no conformance at all.** Rejected. Latin's reception, mediation and language-awareness work is exactly the work the framework describes well, and `lle` should be held to it. Opting out of the framework to avoid four scales discards the traceability for the seventy-five it does meet.

**A separate Latin framework.** Rejected. A second descriptor catalogue means a second coverage computation, a second set of IDs, a second crosswalk and a second thing to maintain, for one course — and it would break the property ADR 0012 buys, that every page in every course resolves against one catalogue.

**Keep `core (reception)` as a freeform string.** Rejected. It is not in the schema, `conformance_audit.py` cannot parse it, and it fails at exit 2. A conformance claim that no gate can evaluate is prose, not a declaration.

**Make `partial` a conformance level and give it to `lle`.** Rejected. `partial` is not a level — it conflates "smaller universe, same standard" with "same universe, not finished yet", which are precisely the two claims that have to stay distinguishable. `examples/de-a1/conformance.yml`'s `declared_conformance: partial` becomes `core` plus `in-progress` for the same reason.
