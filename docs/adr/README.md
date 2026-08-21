# Architecture decision records

This directory is the organisation's decision log. It is the only place a boulingua decision is
recorded normatively; a decision that lives in a commit message, an issue thread or a README is not
recorded, and will be re-litigated within the year.

## Format

**MADR.** One decision per file, named `NNNN-kebab-title.md`, four-digit ordinal, starting at `0001`.

Each record carries, in this order:

- an `# ADR NNNN — title` heading, stating the decision, not the topic;
- a metadata block: `**Status:**` with the date, `**Deciders:**`, and `**Related:**` / `**Supersedes:**` / `**Superseded by:**` as applicable;
- `## Context` — the measured position that forced the decision. File paths and counts, not adjectives;
- `## Decision` — what was decided, in the imperative;
- `## Consequences` — including the **cost**, stated plainly. A record with no cost section is an advertisement, not a decision;
- `## Alternatives considered` — each with the reason it was rejected, so it is not proposed again.

`Status` is one of **Proposed**, **Accepted**, **Superseded by ADR NNNN**, or **Rejected**.

## Rules

**Numbers are never reused.** Not after a rejection, not after a supersession, not after a file is
deleted in a branch that never merged. `0007` means what `0007` has always meant.

**Superseded records are kept, never edited away.** When a decision is replaced, the old record's
status becomes `Superseded by ADR NNNN` and the new record names the old one under `Supersedes:`.
Both files stay in the tree. The reasoning that was correct in 2026 is the evidence for why the
change in 2028 was necessary, and deleting it makes the second decision unfalsifiable.

**Cross-links are bidirectional.** If `0019` relates to `0003`, both files say so. A one-way link
rots the first time someone reads the other file.

**Corrections are recorded, not silently applied.** Where a record's context turns out to be wrong,
the correction goes into the record with its date. A decision log that quietly matches reality has
stopped being a log.

## When an ADR is required

An ADR is **required** — the pull request is not merged without its number — for any decision that
changes:

- **a URL**, in any of the three axes a course declares: section-path separator, leaf-slug style, or
  whether the unit ordinal appears in the slug. 821 VG Wort Zählmarken are bound to URLs. A URL
  change destroys registered marks and real statutory income, so no URL moves on anyone's judgement
  alone;
- **a licence** — the MIT/CC BY-SA 4.0 pair, the per-repo legal file set, or the licence acceptable
  for a bundled font or voice model;
- **a VG Wort rule** — qualification, binding, registration, the re-key protocol, the ledger schema,
  or what `url-lock.csv` is generated from;
- **`kit`'s public surface** — anything a course repository imports, calls or is gated against:
  layouts, shortcodes, tokens, the gate battery, the `boulingua.yml` schema, the deploy template.

Everything else is a commit.

## Index

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-kit-hugo-module-ci-checkout-digest-locked-materials.md) | `kit` is a Hugo module, a CI checkout and a digest-locked `_materials/` | Accepted 2026-08-21 |
| [0002](0002-one-gate-battery-one-caller-one-config.md) | One gate battery in `boulingua/.github`, one 12-line caller, `boulingua.yml` as the only per-course config | Accepted 2026-08-21 |
| [0003](0003-urls-are-frozen-on-three-axes.md) | URLs are frozen, per site, on three axes | Accepted 2026-08-21 |
| [0004](0004-content-cc-by-sa-4-0-code-mit.md) | Content CC BY-SA 4.0, code MIT, `LICENSE` always means MIT | Accepted 2026-08-21 |
| [0005](0005-design-tokens-one-source-generated-artefacts.md) | Design tokens: one source, generated artefacts, no hand-edited hex anywhere | Accepted 2026-08-21 |
| [0006](0006-typography-source-sans-3-full-upstream.md) | Typography: full upstream Source Sans 3, italics shipped, `font-synthesis: none` | Accepted 2026-08-21 |
| [0007](0007-language-islands-not-page-mirroring.md) | Language islands, not page mirroring | Accepted 2026-08-21 |
| [0008](0008-xelatex-polyglossia-one-tex-engine.md) | XeLaTeX for all 18 courses, polyglossia, one TeX engine | Accepted 2026-08-21 |
| [0009](0009-materials-committed-no-generation-on-the-deploy-path.md) | Materials are committed; nothing generates them on the deploy path | Accepted 2026-08-21 |
| [0010](0010-thumbnails-one-renderer-1000px-forward-only.md) | Thumbnails: one renderer, 1000 px, forward-only | Accepted 2026-08-21 |
| [0011](0011-one-curriculum-resolver-no-vendored-scripts.md) | One curriculum resolver, upstream; no script is ever vendored into a course repo | Accepted 2026-08-21 |
| [0012](0012-one-framework-plus-secondary-anchors.md) | One framework, plus secondary anchors; `bildungsplan-bw` is an anchor, not an alternative | Accepted 2026-08-21 |
| [0013](0013-core-restricted-and-the-classical-reception-profile.md) | `core-restricted` conformance and the `classical-reception` profile for `lle` | Accepted 2026-08-21 |
| [0014](0014-eqs-1-normative-five-step-keys-one-exam-per-unit.md) | EQS-1 is normative: five step keys, localised headings, one exam page per unit | Accepted 2026-08-21 |
| [0015](0015-vg-wort-the-tom-export-is-the-baseline.md) | VG Wort: the T.O.M. export is the baseline; private ledger, `marks.yaml`, `url-lock.csv` | Accepted 2026-08-21 |
| [0016](0016-semver-for-the-kit-calver-for-courses-main-only.md) | SemVer for `kit` and `curriculum`, CalVer for courses, `main` is the only long-lived branch | Accepted 2026-08-21 |
| [0017](0017-topic-competence-area-and-skills-are-three-axes.md) | `topic`, `bildungsplan.competence_areas` and `skills_focus` are three axes, not one | Accepted 2026-08-21 |
| [0018](0018-programme-ii-cfl-jfl-afl-pfa-deferred.md) | Programme II: `cfl`, `jfl`, `afl` and `pfa` defer out of this programme | Accepted 2026-08-21 |
| [0019](0019-tom-reconciliation-before-any-url-work.md) | `url-lock.csv` is generated from a T.O.M. export; no URL work before the diff closes | **Superseded by 0020** 2026-08-21 |
| [0020](0020-tom-reconciliation-deferred-provisional-url-lock.md) | The T.O.M. reconciliation defers to the end; a provisional URL lock holds the line | Accepted 2026-08-21 |

**0019 and 0020 are a pair, and both stay.** 0019 measured the exposure and drew a dependency from
it; 0020 keeps the measurement and narrows the dependency. Read 0019 for *what is wrong* and 0020 for
*when it gets fixed*. Superseded records are never deleted — 0019 is the evidence for why 0020 was
needed, and removing it would make the second decision unfalsifiable.

## Open

**The T.O.M. reconciliation is deferred to the end of the programme** (ADR 0020). The exposure ADR
0019 measured is unchanged: up to 592 of the 821 marks may be registered against Quarto `.html` URLs
that no longer render a pixel, and if so they earn nothing for the programme's duration. That cost is
accepted, not resolved.

What is *not* deferred is prevention. `vgwort/url-lock-provisional.csv` is derived from the built
sitemap crossed with `marks.yaml`, deliberately omits the `registered_url` column so it can never be
mistaken for the reconciled lock, and gate A3 blocks any pull request that moves a locked URL without
declaring it. From the day it lands no *new* divergence can be introduced. The question the export
answers — whether the existing registrations are right — is the only one still open.

**The reconciliation is a release gate, not a wish.** No repository may cut its first CalVer tag under
the completed programme while `url-lock-provisional.csv` is still present in it. The filename is the
reminder.

**A twenty-code hand sample closes the whole question for about two hours of portal work** and is
worth taking the first time T.O.M. is open for any other reason. It is unscheduled by choice.
