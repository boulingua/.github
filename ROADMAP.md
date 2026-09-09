# boulingua — suite roadmap

**Audited 2026-09-09** against `curriculum` v1.1.0 and the `pagegen` template.
Every number below was measured in the working trees, not carried over from an
earlier plan.

This document sequences the work across all 25 repositories. Each course repo
carries its own `ROADMAP.md` with the detail; this one exists to answer a
different question — *what should be done next, and why that before the rest.*

---

## 1. Where the suite stands

| Repo | Kind | Units | Exams | Materials | Audio | Conformance manifest |
|---|---|---:|---:|---:|---:|---|
| `efl` | course, mature | 180 | 180 | 739 PDF | 400 | **missing** |
| `fle` | course, mature | 156 | 156 | 643 PDF | 1340 | **missing** |
| `daf` | course, mature | 60 | **0** | 379 PDF | 714 | **missing** |
| `nsf`, `nvt` | course, shell only | 0 | 0 | — | — | missing |
| `afl` `cfl` `ele` `gfl` `ils` `jfl` `lle` `pfa` `pfl` `ple` `rki` `tfl` `ufl` | course, scaffold | 0 | 0 | — | — | missing |
| `curriculum` | framework (1170 descriptors) | — | — | — | — | n/a |
| `pagegen` | course template | — | — | — | — | n/a |
| `kit` | shared Hugo module (layouts, shortcodes, CSS) | — | — | — | — | n/a |
| `audiogen` `sheetgen` `slidegen` | generators | — | — | — | — | n/a |
| `website` `ressources` `.github` | hub, resources, org CI | — | — | — | — | n/a |

**18 language courses. Three have content. Fifteen do not.**

## 2. The three things blocking the whole suite

### 2.1 No course can declare conformance — and it is not for want of content

`curriculum` v1.1.0 requires a machine-readable `conformance.yml` naming the
framework, its version, the declared level and the realizations that map to
descriptor IDs. **No repository in the organisation has that file.**

This is the highest-leverage gap in the suite, because the expensive half is
already done: `efl` carries a `curriculum:` block on all 360 unit and exam
pages, `fle` on all 312, `daf` on all 60. The descriptor work exists; the
manifest that makes it auditable does not. Until it lands, `conformance_audit.py
resolve` has nothing to check, `org-audit.yml` cannot gate on coverage, and the
sites cannot honestly claim `core`.

**Do this first, in `efl`, and copy the shape to the other two.** It is days of
work, not weeks, and it converts three courses from *asserted* to *auditable*.

### 2.2 Two of the three mature courses drift from the template

| | `efl` (reference) | `fle` | `daf` |
|---|---|---|---|
| Bundle naming | `unitNN-slug` ✅ | `unitNN_slug` ❌ 312 pages | `unitNN_slug` ❌ 60 pages |
| Forbidden `slug:` in front matter | none ✅ | **all 312 pages** ❌ | none ✅ |
| Exam pages | 180 ✅ | 156 ✅ | **0** ❌ |
| `page_type` discriminator | all ✅ | all ✅ | all ✅ |
| `[taxonomies]` in `hugo.toml` | ❌ | ❌ | ❌ |

`efl` is the reference implementation. Where the three disagree, `efl` wins —
except on `[taxonomies]`, which none of them declares and all of them should.

### 2.3 Fifteen courses have a plan and nothing else

Each carries a detailed, language-specific build plan (115–470 lines) and five
files. The plans are good and are not the bottleneck. What is missing is a
decision about **order**, because building fifteen courses in parallel is not a
plan, it is a wish.

## 3. Sequencing

The order below front-loads the work that makes later work cheaper, and defers
the work that only pays off once.

**Phase A — make the reference honest (weeks 1–2).**
`efl` gets `conformance.yml`, `[taxonomies]`, and a green `conformance_audit.py
resolve` in CI. Nothing else in the suite is worth doing until one course can
prove a conformance claim end to end.

**Phase B — bring the other two mature courses up (weeks 3–6).**
`fle`: rename 312 bundles to hyphen form, drop the forbidden `slug:`, add the
manifest. Both are scriptable; the renaming touches URLs, so it needs redirects.
`daf`: publish the 60 exam pages. The material already exists — 60 exam PDFs and
60 PNGs are committed, and `scripts/pull_exam_pdfs.py` is in the repo. This is a
page-generation task, not an authoring task.

**Phase C — one new course, end to end (weeks 7–12).**
Pick **one** scaffold and finish it to A1, including exams, materials and audio.
The point is not the course; it is to find out what instantiating from `pagegen`
actually costs now that `kit` carries the chrome. Every later course is priced
from this one.

Recommended first: **`ele` (Spanish)** or **`ils` (Italian)** — Latin script, no
script-onboarding stage, large learner base, and abundant openly-licensed source
material. Deliberately *not* `afl`, `rki`, `jfl`, `cfl`, `ufl` or `pfa` first:
each of those needs a script-onboarding stage or RTL support, which is a platform
lift disguised as a course.

**Phase D — scale out (from month 4).**
Order the remaining scaffolds by demand rather than by ease:

1. `rki` (Russian), `tfl` (Turkish), `afl` (Arabic) — the largest heritage and
   newcomer populations in German schools. `afl` also forces the RTL work, which
   is the platform's biggest outstanding technical gap.
2. `pfl` (Polish), `ils`/`ele` (whichever was not the Phase C pilot), `ple`
   (Portuguese), `nvt` (Dutch), `nsf` (Norwegian).
3. `gfl`, `jfl`, `cfl`, `ufl`, `pfa`, `lle`.

## 4. Gaps declared, not hidden

- **No Danish and no Swedish repository exists.** Both were named as wanted. The
  Nordic set is currently Norwegian only.
- **B2/C1 will not be reached for most languages.** Openly-licensed material
  rarely goes that high. Per `curriculum/docs/conformance.md`, the correct move
  is to declare `core` and record the gap, not to lower the framework.
- **`nsf` and `nvt` commit their built `public/` directory.** It should be
  removed from version control before either grows content.
- **No course declares `[taxonomies]`.** Fixing it in `pagegen` first means the
  fifteen scaffolds inherit it rather than repeat the omission.

## 5. How this audit was produced

Structural facts (file counts, bundle and exam counts, front-matter fields,
descriptor-ID occurrences, materials and audio inventories) were measured
directly in the working trees. The eighteen existing planning documents were read
and reconciled against those measurements. Where a document and the working tree
disagreed, **the working tree won** — which is how the July finding "FLE
publishes zero exam pages" was retired: FLE publishes 156.
