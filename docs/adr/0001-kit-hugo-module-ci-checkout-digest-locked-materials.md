# ADR 0001 — `kit` is a Hugo module, a CI checkout and a digest-locked `_materials/`

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Supersedes:** the copy-to-instantiate model documented in `pagegen/README.md` and in §3 of all fifteen scaffold ROADMAPs

## Context

The org's coupling model is copy-to-instantiate: a new course is created by copying `pagegen`. That model has failed, and it failed silently. The evidence is a census of the checkout, not an impression.

- **Scripts.** Sixteen script basenames exist in more than one of `pagegen`, `efl`, `fle`, `daf`, `website`, `ressources`. **Nine of the sixteen have forked byte-for-byte.** `make_materials.py` and `validate_network_data.py` are each at **three** mutually incompatible versions.
- **Partials.** Ten template partials exist in more than one repo under the same path, and **all ten have diverged.** `layouts/_partials/head/extensions.html` carries **six distinct hashes across six repos** — no two copies are the same file. `header.html` carries five across six; `audio-block.html` four across four.
- **The counting pixel.** One partial, three names: `vgwort/pixel.html` in `pagegen`, `vgwort.html` in `efl`/`fle`/`ressources`, `vgwort-pixel.html` in `daf`.
- **Its manifest.** Four repos, **four incompatible schemas** for one contract:

```
pagegen  qmd_path,md_path,pixel_url
fle      qmd_path,md_path,vgwort_url
efl      qmd_path,article_slug,public_id,pixel_url,source_line
daf      qmd_path,article_slug,pixel_url,pixel_html_verbatim,line_number
```

No consumer can read more than one of them. `pagegen/scripts/verify_all_pixels.py:45` reads a `public_id` column that `pagegen`'s own manifest does not have; `pagegen/scripts/verify-vgwort.sh:35` destructures a different schema again and would read a path as a slug.

- **`static/css/fonts.css`** exists in six copies at three distinct hashes; `scripts/build_materials_latex.py` in four copies that are byte-identical today by luck, not by mechanism.
- **The instantiation instruction is broken at the source.** `pagegen/_materials/`, named in the instantiation step of all fifteen scaffolds, does not exist (`ls: cannot access 'pagegen/_materials'`).

Three consumers need the shared surface, and they need it through three different mechanisms. Hugo can consume a module; a CI job needs scripts on disk before Hugo runs; XeLaTeX can read neither.

## Decision

Create **`boulingua/kit`**, one versioned repo delivered three ways.

| Layer | Mechanism | Why |
|---|---|---|
| Layouts, shortcodes, CSS, i18n, archetypes, `data/accents.yaml` | **Hugo module** (`[[module.imports]]`) | Hugo consumes modules natively. The files stop existing in course repos, so most of the drift surface is removed by construction rather than by policing |
| Generators and the gate scripts | **CI checkout + local `bin/kit`** | A workflow needs scripts on disk before Hugo runs. A module resolved into `~/.cache/hugo_cache/modules/` is not such a path |
| `.sty` files, TTF/OTF fonts, 18 icon PDFs, logo | **Vendored `_materials/` + `kit.lock` digests** | XeLaTeX cannot read a Hugo module. This is the only vendored surface in the org, and it is hash-gated |

`pagegen` is subtree-moved into `kit/` so history survives. `slidegen` and `sheetgen` are absorbed into `kit/latex/` and `kit/fonts/`; `audiogen` into `kit/audio/`. All four are then **archived, not deleted** — their URLs appear in `profile/README.md:77-79` and in every course README.

The resulting invariant, which is the whole decision in one line:

> **A course repo contains content, marks, materials, brand and configuration. It contains no code.**

No `scripts/`, no `_scripts/`, no layouts, no CSS, no shortcodes. `hugo.toml` shrinks from 137 lines to 22.

## Consequences

- The shared surface can no longer fork, because in eighteen repos it no longer exists as a file.
- `kit/example/` — today's `pagegen/content/` — builds on every push with `--panicOnWarning`. The template's own build becomes the platform's first gate, which it has never been: `pagegen/.github/workflows/build-deploy.yml:37` runs `hugo --minify --gc` with no `--panicOnWarning` today.
- `kit` is on the critical path for every gate. Nothing in Phase 2 can be switched blocking before the `bin/kit` verb that runs it exists.
- **Cost:** four repos are archived and §3 of fifteen scaffold ROADMAPs is rewritten. Accepted, because §3 of every scaffold already names a directory that does not exist, so it must be rewritten regardless — and keeping the name `pagegen` would preserve exactly the mental model this decision abolishes.
- **Cost:** the vendored `_materials/` payload is a real duplication across eighteen repos. It is bounded to `.sty`, fonts and 18 icon PDFs, and every byte of it is covered by `kit.lock`, so a one-byte edit fails the next `bin/kit check`.

## Alternatives considered

**Keep the template repo, tighten the instructions.** Rejected. This is the status quo with a stronger promise attached. The census above is what the status quo produced over one year with the instructions already written down: nine forked scripts, ten diverged partials, four schemas for one CSV. A copy has no upstream, so nothing can propagate a fix to it and nothing can detect that it drifted.

**Pure Hugo module, no vendored payload and no CI checkout.** Rejected on two hard limits. XeLaTeX cannot read a Hugo module, so `beamerthemeboulingua.sty` and the fonts must exist as files in the course working tree. And the gate scripts must be on disk before `hugo` is invoked; a module is resolved by Hugo, into a cache path that is not a stable input to a preceding workflow step. A pure-module answer would have re-introduced a second, unversioned copy mechanism for exactly the two payloads that matter most on the revenue and print paths.

**Git submodules for everything.** Rejected. Submodules solve the delivery half but not the versioning half — a course would pin a commit, not a release, and the digest gate on `_materials/` would have nothing to compare against. `kit` ships SemVer tags and `RELEASE/SHA256SUMS`; that is the property a course pins.
