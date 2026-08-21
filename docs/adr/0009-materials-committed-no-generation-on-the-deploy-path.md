# ADR 0009 — Materials are committed; nothing generates them on the deploy path

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0001 (digest-locked `_materials/`), ADR 0002 (the gate battery), ADR 0008 (XeLaTeX), ADR 0010 (thumbnails)

## Context

Two of the three live sites commit their generated materials and one does not. `fle` carries 312 committed PDFs and `daf` 180. `efl` carries zero: `efl/.gitignore:20-22` ignores `/static/downloads/`, `/static/materials/presentations/` and `/static/materials/worksheets/`, and all three directories are empty on disk. `efl` regenerates its 180 decks and 180 worksheets inside the deploy workflow — TeX Live is installed at `efl/.github/workflows/hugo.yml:58-68` and the generator runs at `:75-80`, before `hugo --minify` at `:103`.

That model has failed quietly four ways, all verified:

- **Determinism.** A TeX Live point release silently reflows 360 documents between two deploys with no content change and no review.
- **Blast radius.** `xelatex()` at `build_materials_latex.py:305-309` discards the subprocess return code and returns `(file_exists, result)`; `process()` at `:363-375` records the failure into a dict; `main()` at `:383-404` prints `[PARTIAL]` and never exits non-zero. A broken unit today produces no PDF, no error exit, and a deploy pointing at a missing file.
- **Attribution.** `daf/scripts/verify_pdf_metadata.py:29` walks `static/**/*.pdf` and `:30-32` returns 0 with `no PDFs found` when the glob is empty. On `efl`, where the PDFs are git-ignored, that gate passes **vacuously** — a legal-adjacent invariant reports success when the build step it depends on has not run.
- **Reviewability.** `git diff --stat static/materials/` is the change log for what learners receive. On `efl` there is no such log.

The write-back variant of the same model was worse and has already been removed. `fle/.github/workflows/regen-materials.yml` held `contents: write` at `:16-17`, `workflow_dispatch` at `:13-14`, ran the retired placeholder generator `_scripts/make_materials.py` at `:38`, then `git add static/materials/` at `:44` and `git push origin HEAD:main` at `:55`. `make_materials.py:257` writes `WORK_DIR / f"{slug}.pdf"` — the exact path of the 156 committed branded worksheets — `:256` writes placeholder `.pptx` beside the 156 branded presentation PDFs, and `:258-263` overwrite all 312 committed thumbnails. The front-matter rewrite at `:279-290` was not staged, so the pushed state would have been placeholder artefacts under front matter still claiming they were branded. **The file was deleted in Phase 0 on 2026-08-21.**

## Decision

**All generated artefacts are committed, in every repo: PDFs, thumbnails, `.ogg` audio, and their manifests.**

**No CI job on the deploy path may run XeLaTeX, LibreOffice or Piper. CI verifies; it does not generate.**

The reusable workflow `course-build.yml` has a fixed dependency footprint — `pip install pyyaml pypdf pymupdf fonttools`, plus Hugo and Go. No TeX Live, no LibreOffice, no Piper. Generation happens locally through `bin/kit materials <code>` and `bin/kit audio <code>` against the pinned toolchain in `kit/Containerfile` (TeX Live 2026 / xdvipdfmx 20260317, Python 3.11, PyMuPDF 1.24.x, pypdf 4.x, oxipng 9.x, piper-tts ≥1.5.0, ffmpeg 6.x), and the output is committed and reviewed like any other change.

**No workflow in this org writes to `main`.** That rule is stated in `CONTRIBUTING.md` and is checked by the PR template.

**`efl` migrates in P3.4b, sequenced after its content migration, not before it.** The order is not negotiable:

1. Generate locally with the pinned toolchain — 180 decks, 180 worksheets, 360 thumbnails.
2. Delete `efl/.gitignore:20-22`.
3. `git add` and commit all of it in **one** changeset naming the toolchain versions.
4. **Only then** delete the TeX Live install at `hugo.yml:58-68` and the generation step at `:75-80`.

Reversing 3 and 4 deploys a site with 360 dead download links. Steps 1–3 are a single commit precisely so that reverting one SHA restores the previous state, and step 4 is a second commit that is never pushed before D1–D5 are green on the first. **Abort criterion:** if D1–D5 fail on the generated batch, the branch is abandoned and not partially merged. `efl`'s only tag is `v0.1.0`, from before the Hugo migration and useless as a rollback point, so `efl` is tagged `v2026.xx` at the end of P3.4a and that tag is the rollback target.

The same commit deletes the `libreoffice-impress` install at `daf/.github/workflows/hugo.yml:50-53`, along with the LibreOffice branch of `render_thumbs.py` (`:40-51`, `:66-87`, `:91-97`, `:123-138`) — see ADR 0010.

## Consequences

- `efl` adds roughly 20 MB to git history once, post-oxipng, and buys back about 4 minutes of TeX Live install plus about 6 minutes of 360 double-pass XeLaTeX runs from **every** deploy.
- Gates D1–D5 become meaningful on `efl` for the first time. `verify_pdf_metadata.py`'s empty-glob pass and gate D2's `/Creator` clause both stop being vacuous the moment the PDFs exist in the tree.
- Gate D2's `/Creator contains boulingua` clause fails on 100 % of today's PDFs, because none of the three current toolchains writes it. D2 therefore lands **with** the first regeneration, not before it, and `bin/kit materials --verify-only` reports the pre-migration state as a count rather than a failure until then.
- A deploy can no longer produce an artefact nobody reviewed. Whatever a learner downloads is in the diff of some commit.
- Regenerating materials becomes an explicit author action with a review step. That is the cost, and it is the point.
- Deploy workflows lose their apt install steps entirely, which is most of their runtime.

## Alternatives considered

**Generate on the deploy path, as `efl` does today.** Rejected on all four grounds above. The determinism argument alone is decisive: 360 documents reflowing on a TeX Live point release, with no content change and no reviewer, is not a publishing pipeline.

**Generate in CI and push the result back to `main`, as `fle/.github/workflows/regen-materials.yml` did.** Rejected, and the file is deleted. It gave one `workflow_dispatch` click the power to overwrite 156 branded worksheets and 312 thumbnails with placeholders and deploy the result automatically, with no reviewer and no revert prompt.

**Host artefacts outside the repo — a release asset store or an object bucket.** Rejected. It moves the download URLs off the course domain, and every unit page's download link is a URL under the VG Wort freeze (ADR 0003, ADR 0015). It also removes the `git diff --stat` change log, which is the property that makes the commit model worth its bytes.

**Commit in `fle` and `daf`, keep `efl` generating.** Rejected. One org, one rule; a per-repo exception is how the current three-way divergence happened, and the exception repo is the one where a legal-adjacent gate passes vacuously.
