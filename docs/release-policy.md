# Release policy

Two schemes, because the repositories are two kinds of thing.

## `kit`, `curriculum`, `.github` — SemVer, with moving majors

| | |
|---|---|
| **MAJOR** | a change that requires courses to edit something |
| **MINOR** | additive; a course can ignore it until it wants it |
| **PATCH** | a fix that changes no interface |

Courses pin `@v1`. The moving tags `v1` and `v1.2` are maintained so a course
gets fixes without a commit, and `org-audit` reports how far behind each course
is rather than updating anything on its own.

Descriptor ids in `curriculum` are **additive and never renumbered** — a
withdrawn statement becomes `status: deprecated`. That is what makes a MINOR
release safe: nothing a course already claims can stop resolving.

## Courses — CalVer, `vYYYY.MM`

Cut when a level or track is content-complete, not on a calendar. Release notes
name the units added, the marks registered, and the `kit` and `curriculum`
versions in force.

**A course may not cut a tag while:**

- a coverage gate is warning on that level,
- any unit sits at `native_check: pending`, or
- `vgwort/url-lock-provisional.csv` is still present.

That last one is the release gate on the T.O.M. reconciliation (ADR-0020). The
provisional lock records where a mark *renders*, not where it *earns*; a course
that tags while it is still in place is claiming a completeness nobody has
checked. The filename is the reminder.

Every tag is annotated. A release is a signed statement about a corpus of
teaching material, not a convenience marker.

## Today

`daf v1.0.0` and `v0.1.0` · `efl v0.1.0` · `fle v0.1.0` · `ressources v0.1.0` ·
`kit v1.0.0` · `curriculum` at 1.1.0 unreleased. `daf` is the only course its
author has ever considered finished enough for a 1.0, and that is retained and
aliased rather than renumbered.
