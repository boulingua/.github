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

**0019 is reserved.** Records 0003 and 0012 already cite it for the rule that `vgwort/url-lock.csv`
is generated from a T.O.M. export and never from a sitemap crossed with `marks.yaml`. ADR 0015
carries that rule today; 0019 stays reserved rather than reassigned, because the ordinal is already
in the tree and a reused number is worse than an unused one.

## Open

**ADR 0003 and ADR 0015 are blocked on the T.O.M. export.** The repositories know which URL a code
*renders* on; only T.O.M. knows which URL a code is *registered* against, and there is direct
evidence the two have diverged. 399 of `efl`'s 402 marks carry `registered_at: '2026-04-30'`, six
days before the Quarto→Hugo migration of 2026-05-06; `efl` and `fle` manifests remain keyed on the
Quarto `qmd_path`; `aliases:` sit on 405 `efl` pages, 202 `fle` and 80 `daf`, and Hugo's built-in
alias output is a bare meta-refresh stub carrying no pixel. Up to 592 of the 821 marks may therefore
be registered against URLs that no longer render one. `url-lock.csv` cannot be generated until the
export exists, because a lock file built from the wrong baseline would teach the gate to defend the
wrong URLs forever, with perfect fidelity. **Nothing that changes a URL proceeds until that diff
closes.**
