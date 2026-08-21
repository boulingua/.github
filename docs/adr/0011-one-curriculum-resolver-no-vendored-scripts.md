# ADR 0011 — One curriculum resolver, upstream; no script is ever vendored into a course repo

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0001 (`_materials/` is the only vendored surface), ADR 0002 (one caller), ADR 0012 (the manifest), ADR 0013 (profiles)

## Context

`boulingua/curriculum` holds a sound framework — 88 scales, 79 in scope, 1,170 statements across seven level files — and exactly one script: `scripts/id-audit.sh`. That script cannot do what eighteen published documents instruct courses to use it for.

**The defect, reproduced on disk.** The bash wrapper hard-codes its own repo root at `id-audit.sh:14-15` (`here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"`) and passes it as the Python's only argument; the Python globs `levels/*.md` at `:50`. There is no `--manifest` flag, no option parsing, and no path by which a caller can point it at a consumer repo. Run from anywhere, against any course, it audits the framework's own 1,170 statements, prints `id-audit: checked 1170 statement(s) across levels/, 79 in-scope scales` followed by `OK`, and exits **0** — regardless of what the course contains.

**The wiring is live and it is wide.** The fifteen scaffolds reference `id-audit.sh` **61 times**, and almost every reference is a milestone acceptance criterion — "`id-audit.sh` green", "passes `id-audit.sh` at that level", "**First flip-worthy state**" — not a passing mention. With `efl/HANDOVER.md:71,73`, `fle/HANDOVER.md:38,70,71` and `daf/HANDOVER.md:42,95,128` that is **69 references across 18 published documents**, every one of which instructs a course to adopt a gate that passes vacuously. `curriculum/docs/verification.md:13` compounds it by ticking *"German A1 example passes conformance at declared level"*, a check nothing performs, and the header comment at `examples/de-a1/conformance.yml:6-7` asserts the same capability.

Separately, two of this programme's predecessor specs proposed vendoring. `spec:pedagogy` copied EQS gate scripts into `<course>/_scripts/eqs/` and added a drift gate to police the copies. `spec:materials` copied generators into course repos via `sync_materials.py`. Eighteen courses × either mechanism is eighteen copies of every script, plus a gate whose whole job is to notice when the copies disagree.

## Decision

**There is one curriculum resolver, it lives upstream in `boulingua/curriculum`, and it is `scripts/conformance_audit.py`.**

It ships in `curriculum` v1.1.0 with the commands `self-audit`, `resolve --manifest FILE --content DIR`, `coverage --emit-yaml --emit-md --check`, `explain ID` and `suggest --level L --domain D`. Its exit codes are the contract: 0 conformant · 1 usage · 2 manifest fails schema · 3 malformed, dangling, deprecated, duplicated or out-of-span ID, or unresolvable Bildungsplan code · 4 front-matter↔manifest drift, or a `coverage --check` diff · 5 declared level not met · 6 version-pin mismatch. Splitting 3, 4 and 5 is deliberate: a ramping course must fail hard on a **wrong** ID while merely being warned about **incomplete** coverage. Conflating them is how the current gate became vacuous.

**`id-audit.sh` is framework-internal.** It audits `curriculum`'s own level files and structurally cannot ingest a consumer's `conformance.yml`. It is replaced by a deprecation wrapper that `exec`s `conformance_audit.py self-audit`, so the phrase in fifteen published ROADMAPs does not dangle while they are being corrected.

**The 69 references are un-wired in P0.7**, and where a reference carried an acceptance criterion it is replaced by the consumer gate:

> **Gate.** The reusable workflow `boulingua/.github/.github/workflows/course-build.yml@v1` runs `python .curriculum/scripts/conformance_audit.py resolve --manifest conformance.yml --content content`. `id-audit.sh` audits the framework's *own* level files and **cannot** validate this repo. Do not wire it here.

`curriculum/docs/verification.md:13` is unchecked until F8's CI actually runs the check. References inside `curriculum` itself (`docs/verification.md:3,6,10`, `docs/conformance.md:29`, `docs/adr/0001:26`, `docs/id-scheme.md:83`, `CHANGELOG.md:34`) are framework-internal and correct; they are left alone.

**Coupling: `curriculum` is a CI-time checkout at a pinned tag.** Never vendored, never a Hugo module, never a git submodule. `hugo --minify --gc` must still succeed with `.curriculum/` absent — conformance is a gate, never a build input.

**No script is ever vendored into a course repo.** Gates and generators come from a `kit` or `curriculum` checkout: `bin/kit` locally, `actions/checkout` in CI. Both vendoring proposals are rejected.

**The only vendored surface in the entire org is `_materials/`** — styles, fonts, brand assets, logo — because XeLaTeX needs files on disk (ADR 0008). It is hash-gated by `_materials/kit.lock`. One rule, no exceptions.

## Consequences

- Gate A16 (`conformance_audit.py resolve`) is the curriculum gate in the battery. It reads its thresholds from the pinned framework and never from a hard-coded number.
- The drift surface is eliminated rather than policed. There is no vendored script for a gate to diff, so the drift gate that `spec:pedagogy` proposed has nothing to do and is not written.
- A course pins `framework_ref`/`framework_sha` and bumps it deliberately. A framework MINOR release that adds descriptors does not retroactively fail a pinned course.
- Eighteen ROADMAPs and HANDOVERs change in one pass, and a defect class that made a milestone criterion meaningless in fifteen repos stops being reachable.
- A course author who wants a local run needs a `curriculum` checkout. `bin/kit` fetches it at the pinned tag, so the local and CI invocations are the same command.
- Anything a course genuinely needs from the framework must be added upstream and released. A course never edits `curriculum`; it files a `framework-gap` issue and continues at its current pin (§9.4).

## Alternatives considered

**Extend `id-audit.sh` with a `--manifest` flag.** Rejected. The consumer gate needs schema validation, ID resolution, front-matter↔manifest drift detection, coverage arithmetic against a pinned framework, and six distinguishable exit codes. That is a new program in Python, not a flag on a bash wrapper that globs `levels/*.md`.

**Vendor the gates into `<course>/_scripts/eqs/` with a drift gate (`spec:pedagogy`).** Rejected. Eighteen copies of every gate script, plus a gate whose only purpose is to notice that the copies disagree. The drift is created by the vendoring; removing the vendoring removes the drift.

**Vendor the generators via `sync_materials.py` (`spec:materials`).** Rejected for the same reason, with the additional cost that a generator copy can silently be a different version from the one that produced the committed artefacts.

**Ship `curriculum` as a Hugo module or a git submodule.** Rejected. A Hugo module makes conformance a build input, so `hugo --minify --gc` would fail when the framework is unavailable — the opposite of the required property. A submodule pins by SHA in a way that makes a deliberate version bump indistinguishable from an accidental one in a diff, and it is a checkout with worse ergonomics than `actions/checkout`.
