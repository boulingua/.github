# Suite repair and harmonisation — the programme

**Opened 2026-08-31.** This roadmap is the output of two exhaustive audits run over all 27
repositories on the night of 2026-08-30/31: a sixteen-dimension defect audit (45 agents, every
finding adversarially verified by two independent lenses) and a harmonisation design study
(17 agents, four competing proposals scored by four judges). It sits beside
`programme-roadmap.md`, which tracks the *content* programme; this one tracks the *platform*.

Where the two disagree on a measurement, this file wins — it was measured later and by execution.
Where either disagrees with an ADR on a decision, the ADR wins.

## What the audits actually found

**145 verified defects. 37 blocking.** Ninety-six of them are in `kit`, which is the correct
place for them to be and the reason the platform exists: one repository absorbs what would
otherwise be eighteen.

| Workstream | | blocking | major | minor | total |
|---|---|---|---|---|---|
| **S** | Stop-ship / data corruption | 1 | 0 | 1 | 2 |
| **G** | Gates that examine nothing | 21 | 20 | 5 | 46 |
| **M** | VG Wort money integrity | 4 | 13 | 3 | 20 |
| **O** | CI, supply chain, org plane | 2 | 2 | 0 | 4 |
| **U** | curriculum | 1 | 3 | 3 | 7 |
| **C** | Config drift across repos | 0 | 6 | 6 | 12 |
| **H** | Harmonisation & accessibility | 1 | 2 | 1 | 4 |
| **P** | Documentation that is false | 2 | 8 | 13 | 23 |
| **K** | Kit correctness & dead code | 5 | 7 | 15 | 27 |
| | **TOTAL** | **37** | **61** | **47** | **145** |

### The one sentence that explains most of them

**A gate here does not fail wrongly. It passes having examined nothing, and the symptom is a
confident zero.** Forty-six findings are that shape. The five found on 2026-08-30 (C1, C4, A1,
A13, A3) were not the population; they were the sample that made the population visible. A7 and A8
root themselves at `__file__` and have never read a course stylesheet, while 114 colour literals
and 23 physical inline properties sit unmeasured in the four course CSS files they were written to
police. A10 only ever examines the kit, and nothing runs the battery against the kit. A16 has no
invocation site anywhere in the organisation. A12/A14/C12 cannot match the HTML that CI builds,
because every contract regex requires quoted class attributes that `hugo --minify` strips.

The second-order lesson is the one worth keeping: **an outer fault hides an inner one.** None of
this was visible while the gate register aborted before the battery ran. Every gate that was green
during that window was green without evidence, and the audit is what converted that suspicion into
a list.

### Two defects were shipped by the repair itself

Both are already fixed, and both are recorded here because they are the strongest available
argument for the harness in **G1**.

- **560 of the 1,220 clips regenerated on 2026-08-30 were built from the wrong text.**
  `build_audio.py` emits two strings per vocabulary segment — `' · '.join(terms)` to display and
  `'.\n'.join(terms) + '.'` to speak — and the manifest stored only the first. The full stops are
  the drill: they are what puts a pause between one vocabulary item and the next. Measured on efl
  unit01 Vocabulary 1: 7.52 s with zero internal pauses against 10.03 s with two.
- **`build_audio.py` republished the previous clip under the next clip's filename** whenever piper
  failed, and wrote the hash sidecar so it was never retried. Reproduced with a stub failing on
  call 2: two byte-identical `.ogg` files, the manifest carrying the second clip's transcript
  beside the first clip's audio, exit 0, `3 clips synthesized`.

Neither would have been caught by anything the organisation owns. That is the finding.

---

## The order of work

Nine workstreams. The dependency spine is short and the rest is wide:

```
  S ─ stop-ship, now
  │
  G1 ─ the harness ──┬─ G2..G6  gates, in parallel
                     ├─ M       money integrity
                     ├─ O       CI and the org plane
                     ├─ U       curriculum
                     └─ H1..H14 harmonisation
                                    │
  C, P, K ─ independent throughout  └─ H12 move v1, once every adoption PR has merged
```

**G1 is the blocking prerequisite for everything.** Not because the other work depends on its
code, but because without it no other workstream can prove it did not break something. That is not
a theoretical worry: deleting `daf/layouts/materials/list.html` silently removes five fingerprinted
JS bundles from the published tree with **exit code 0, 145/145 pages, no Hugo warning even under
`--panicOnWarning`, and `kit urldiff` reporting `A3 OK — 68 locked marks`**. Nothing the
organisation owns today can see that, and eleven of the fourteen harmonisation steps delete a
template.

### Branch protection changes the sequencing

Configured on all 27 repos on 2026-08-30. `kit`, `.github`, `curriculum` and the 13 scaffolds
accept direct pushes; **daf, efl, fle, nsf, nvt, website and ressources require a PR with the
`course` check green**. Every course-side step below is therefore a PR, and the seven adoption PRs
in H7–H11 must all merge before H12 moves the `v1` tag.

### The `v1` trap, which no proposal saw until it was measured

`course-build.yml` defaults `kit_ref: v1` — a **moving** tag — so CI gate scripts come from `v1`
while layouts come from the exact `go.mod` pin. Moving `v1` therefore changes CI for seven
branch-protected repositories simultaneously. New gates ship `status: planned`, `v1` moves only
after every adoption PR has merged, and gates become blocking one release later.

### The module-cache trap, which invalidated a judge's finding and six experiments

A course pins `github.com/boulingua/kit v1.21.0`, so Hugo serves the kit from
`~/.cache/hugo_cache/modules/…` and **every local kit edit is invisible**. A judge disqualified the
winning proposal on evidence produced this way, and the plan's author fell into it first. Before
trusting any kit change:

```
cd <course> && hugo config mounts | grep -A6 '"path": "github.com/boulingua/kit"' | grep '"dir"'
# must print your working copy, never a path under ~/.cache/hugo_cache
# to make it so:  printf '\nreplace github.com/boulingua/kit => ../kit\n' >> go.mod   (scratch only)
```

---

## S — stop-ship

Done during the audit; recorded for the trail.

| | file | finding |
|---|---|---|
| BLO | `kit/scripts/split_speaking.py:37` | split_speaking.py's replace_block cannot see indented YAML list items — running it on efl silently corrupts skills_focus on all 71 target pages |

`regen_audio.py` now prefers a stored `tts` key, reconstructs it by inverting `build_audio.py`'s
own join where absent, and routes everything through `normalise()` — which had also never run, so
the U+0301 stripping for ru/uk, bidi controls for ar/fa, ano-teleia for el and NFC for tr were all
bypassed on what is now the tool of record. `build_audio.py` checks its subprocess return codes,
uses one temp file per segment, and writes neither hash nor manifest entry unless the encode
verified. **`S2` — `split_speaking.py`'s `replace_block` cannot see indented YAML list items and
silently corrupts `skills` on efl — is NOT yet fixed and must not be run.**

---

## G — the gates must be able to see

Forty-six findings. **G1 first, alone.**

### G1 — the harness (L, blocks everything)

Three new checks, because the failure mode this programme most needs to detect is one nothing
currently reports:

- `verify_url_set.py` — full published-file-set diff. REMOVED or MOVED fails; ADDED passes with a
  declared count. Stronger than A3, which defends 789 of 2,076 pages, and stronger than any
  HTML-only comparison.
- `pixelmap.py` — deterministic full-page screenshot manifest, two viewports × two colour schemes,
  fonts settled, the nondeterministic Cytoscape mount excluded and covered by C15 instead.
- `verify_template_paths.py` (**A20**) — a course may hold no template whose first path segment is
  a content section, and `boulingua.yml` may contain no `url_shape`-shaped key. This is the
  `url_shape` question answered as an assertion rather than an abstraction.

**Exit test — the negative control is the point.** `mv daf/layouts/materials/list.html /tmp` must
produce `A3 OK` from `kit urldiff` and a **non-zero** exit from `verify_url_set.py` listing exactly
five `- /js/network/*.js` removals.

### G2–G6 — the gates themselves (parallel once G1 lands)

| | file | finding |
|---|---|---|
| BLO | `kit/bin/kit:387` | `kit materials REPO --thumbs` throws the REPO away and renders thumbnails into the kit |
| BLO | `kit/bin/kit:136` | `kit check` cannot tell "the course opted out" from "nobody said anything", and the exempt-from-CI class is the one it picks |
| BLO | `kit/scripts/verify_pixel_delivery.py:67` | A mark on an `_index.md` section landing page passes every rendered-side gate — the 2026-08-30 withdrawal of 32 codes has no automated guard against recurrence |
| BLO | `kit/scripts/verify_logical_css.py:38,51` | A8 ignores its argument entirely: it derives its root from __file__ and has never examined a course stylesheet |
| BLO | `kit/scripts/verify_tokens.py:40,99-102` | A7 has the same __file__ root: 114 colour literals live in course CSS while it reports "one source for every colour" per repo |
| BLO | `kit/scripts/verify_contrast.py:68-72` | A10 has never examined anything: only the kit holds design/tokens.yaml, and nothing runs the battery against the kit |
| BLO | `kit/scripts/verify_assessment.py:77-80,126-128,140-145` | A13: one well-formed exam page is enough to turn 156 markless papers from a FAIL into "A13 OK — 1 exam(s)" |
| BLO | `kit/scripts/verify_eqs.py:50` | C12/A12/A14 cannot match the HTML that CI builds: every contract regex requires quoted class attributes that hugo --minify strips |
| BLO | `kit/scripts/verify_js_budget.py:34` | C15 budgets only public/js/network/*.js, so fle's 204 KB gz of eagerly-loaded cytoscape is invisible and the gate reports 5,619 B |
| BLO | `kit/scripts/verify_page_contract.py:94` | C6 joins locked marks to source files by file path, ignoring front-matter slug:, so 312 of fle's 336 marked pages are never examined |
| BLO | `kit/scripts/verify_voices.py:70` | D6 examines nothing in the battery: verify_voices.py is handed the course, voices.yml lives in the kit, and the kit has no CI at all |
| BLO | `kit/scripts/verify_pdf_metadata.py:89` | D2's anti-vacuous-pass guard is dead on efl and fle: deleting all 672 committed PDFs still returns 0 |
| BLO | `kit/scripts/verify_pagefind.py:23` | B3 passes with no search index at all on daf and fle, both of which declare gates.pagefind: true, and nothing in the org ever builds one |
| BLO | `.github/.github/workflows/course-build.yml:161` | E1 is status: live with no automated enforcement — removing the main-only guard so every pull request deploys to production Pages passes org_audit and the register untouched |
| BLO | `kit/gates.yml:292` | Gate A16 (conformance resolution) has no invocation site anywhere in the organisation |
| BLO | `.github/workflows/course-build.yml:131` | Gate A16 (conformance resolution) is declared live and runs nowhere — course-build.yml never invokes it, and the register only checks that the `runs:` field is a non-empty sentence |
| BLO | `scripts/org_audit.py:66` | org_audit.py globs only `*.yml`, so the org-wide ban on `contents: write` / `git push` / gate suppression is defeated by naming a workflow `.yaml` |
| BLO | `.github/workflows/kit-drift.yml:24` | kit-drift.yml's `git clone --depth 1` strips kit's semver tags, so the module-version drift check silently never runs — a course seventeen minors behind passes |
| BLO | `kit/scripts/verify_pdf_metadata.py:89` | Gate D2's anti-vacuity guard is disarmed on efl and fle — the two courses holding 672 of the org's 852 committed PDFs |
| BLO | `kit/scripts/verify_page_contract.py:96` | A18/C6 re-derives page URLs from the file path and ignores `slug:`, so it examines 24 of fle's 336 marked pages and prints "0 marked unit/exam page(s)" |
| BLO | `kit/scripts/verify_voices.py:70` | D6, the only audio gate in the battery, is handed the course repo and returns 0 having examined nothing — on all 26 non-kit repos |
| MAJ | `kit/scripts/render_thumbs.py:29` | render_thumbs.py roots itself at the kit, so `kit materials REPO --thumbs` renders nothing and exits 0; when it does find a PDF it dies on an undefined counter |
| MAJ | `kit/scripts/verify_page_contract.py:94` | A18/C6 re-derives the page URL from the file path instead of blg_paths.url_key, so 312 of fle's 336 marked pages are never examined — and it prints "0 marked unit/exam page(s)" |
| MAJ | `.github/scripts/kit_drift.py:43,124-125` | A1's NOT_A_COURSE skip-list exempts website and ressources, which between them hold five diverged forks of kit files |
| MAJ | `kit/scripts/verify_i18n_chrome.py:44-55` | A9 run per course examines only the course's own layouts, never the 26 kit layouts it actually renders — "0 key(s) used" on efl, fle and website |
| MAJ | `kit/scripts/verify_inclusion.py:47` | A15's speaker-consistency half is inert on two of the three live courses: 1 speaker appearance found across fle's 156 units, 0 across efl's 180 |
| MAJ | `kit/scripts/verify_eqs.py:103-121` | A12/A14/C12 has never examined a page anywhere in the organisation, and its own warning is invisible in the battery |
| MAJ | `kit/gates.yml:358` | All 11 planned gates are booked to phases the roadmap declares finished, and the register verifier reports otherwise while checking only that the string is non-empty |
| MAJ | `curriculum/scripts/conformance_audit.py:211` | The three structural properties every course manifest asserts as "verified" are checked by nothing |
| MAJ | `curriculum/scripts/conformance_audit.py:245` | resolve --content at a path that does not exist silently skips the only content-side check and prints "resolve OK" |
| MAJ | `kit/scripts/verify_pagefind.py:23-25` | daf and fle declare `gates.pagefind: true` and render a search box, no index exists or is ever built, and gate B3 returns 0 saying "this course ships no search index" |
| MAJ | `scripts/org_audit.py:109` | org_audit.py passes on an empty org checkout and reports a negative live-repo count — nothing distinguishes "clean" from "cloned nothing" |
| MAJ | `kit/scripts/verify_pdf_metadata.py:61` | D2 never inspects /Subject, /Keywords or /Creator: REPORTED_FIELDS is declared and never read, and gates.yml's "All five fields are checked now" is false — 792 of 852 PDFs have no /Subject and no /Keywords |
| MAJ | `kit/scripts/render_thumbs.py:29` | render_thumbs.py — "the one thumbnail renderer" — cannot target any course, crashes on the first PDF if it ever could, and exits 0 having rendered nothing |
| MAJ | `kit/scripts/verify_downloads.py:112` | D1's exam-PDF check is keyed on `cefr_level`, a field only daf uses — a one-field rename silences 60 missing PDFs, and the branch has never executed on efl or fle |
| MAJ | `kit/scripts/test_blg_paths.py:31` | kit's own path-contract self-test skips two of three fixtures on stale paths and fails the third, because efl no longer carries `unit_slug` |
| MAJ | `kit/scripts/verify_voices.py:126` | verify_voices.py's provenance-note requirement is bypassed by `base_model: null` — exactly the case its own comment says is not evidence |
| MAJ | `kit/scripts/verify_voices.py:169` | D6's audition half examines nothing: zero rows are `status: ready`, `auditions/` holds only TEMPLATE.md, and the gate still prints "every ready voice auditioned by a named listener" |
| MAJ | `.github/docs/adr/0004-content-cc-by-sa-4-0-code-mit.md:45 (and :33, :39)` | ADR-0004 says 'the licence gate blocks a repo missing any file in the set'; A4 checks two of the five, and REUSE.toml exists in zero repos while every build is green |
| MAJ | `kit/scripts/verify_fonts.py:10 (check implemented at :107-121); kit/design/fonts.yaml:147,165,181` | verify_fonts.py's docstring claims it verifies that every licence file a family points at exists and is non-empty; it never opens the path, and all three shipped families point at a file that does not exist |
| MAJ | `kit/scripts/verify_i18n_chrome.py:53 (and :81)` | Gate A9 reports "0 key(s) used ... all translated" for fle — it scans the repo's own layouts/ (which call i18n zero times) and keys its language axis off which yaml files exist, never off the site's language |

---

## M — VG Wort money integrity

789 registered marks. Twenty findings, four blocking.

| | file | finding |
|---|---|---|
| BLO | `kit/scripts/verify_page_contract.py:98` | 282 registered marks sit on pages under VG Wort's 1,800-character Mindestumfang, and no gate in the battery can reach them |
| BLO | `kit/scripts/verify_page_contract.py:94-96` | A18 derives page URLs from file paths and ignores `slug:`, so 312 of fle's 336 locked marks match no page and it prints "0 marked unit/exam page(s)" |
| BLO | `kit/scripts/verify_page_contract.py:72` | C6's lock path is hardcoded, so boulingua.yml's vgwort.url_lock is inert and pointing it anywhere turns 41 blocking errors into 'n/a — this repo registers no marks' |
| BLO | `nsf/boulingua.yml:58, nvt/boulingua.yml:58, kit/templates/boulingua.yml:58` | nsf, nvt and the kit's own scaffold template still declare `registry: vgwort/marks.yaml` — a mark filed there renders no pixel and the whole battery reports "registers no Zählmarken" |
| MAJ | `kit/scripts/verify_rendered_pixels.py:108` | One public code registered against two works renders on both pages and the whole battery passes, whenever the code is not already in the lock |
| MAJ | `kit/scripts/verify_page_contract.py:72` | A18/C6 keys the marked-page set off the URL lock rather than data/vgwort.yaml, so a newly registered mark is unchecked until someone regenerates the lock by hand |
| MAJ | `kit/scripts/vgwort_audit.py:99` | C1 and C4 answer the same coverage question with 0 and 96: C1 measures source markdown, so 96 ressources pages whose source body is zero characters and which render 2,636-24,820 are invisible to it |
| MAJ | `kit/scripts/verify_page_contract.py:55` | C6 'rendered length floor' measures the source markdown, and two of efl's eighteen current blocking failures are pages that clear the Mindestumfang when measured the way C4 measures it |
| MAJ | `kit/scripts/verify_pixel_delivery.py:98` | C5's display:none-ancestor detector is a 400-character look-back with a 'visibility' escape hatch; both are trivially slipped and the pixel then never fetches |
| MAJ | `kit/scripts/verify_rendered_pixels.py:45` | `vgwort.url_lock` is declared in six config files and read by no code; C2 hardcodes the filename, and moving the lock to where the config says breaks the gate |
| MAJ | `kit/audio/voices.yml:294` | voices.yml's `second_voice` names six models the org's own provenance doc classifies as NonCommercial-tainted — and no line of code anywhere reads the field |
| MAJ | `efl/static/materials/audio/unit01-hello-world/texte2.ogg` | Seven efl .ogg missed the regeneration, are still in the old Opus codec, and ship in git and in the built site — and D1, the "no orphans" gate, contains no audio check at all |
| MAJ | `kit/docs/marked-placeholders.md:3, :81, :83` | kit/docs/marked-placeholders.md lists a truncation notice as a table row and counts it: '58 pages' is 41 pages, and one of the 59 rows is not a page |
| MAJ | `.github/CONTRIBUTING.md:114 and :232; .github/PULL_REQUEST_TEMPLATE.md:21-22` | CONTRIBUTING.md and the PR template gate every contributor on vgwort/url-lock.csv and url-lock.retired.csv; neither file exists in any repository |
| MAJ | `kit/docs/vgwort-standard.md:3-6` | kit/docs/vgwort-standard.md — the binding VG Wort standard — still says the reference implementation lives in pagegen and is copied verbatim into each course |
| MAJ | `kit/layouts/_partials/vgwort/url.html:27-38 (specifically :30 $fp from .File.Path, :34 the match)` | A `path:`-keyed vgwort entry emits the SAME Zählmarke on every language version of a page, and a `url:` key written as documented never matches on a multilingual site |
| MAJ | `kit/layouts/_partials/head/extensions.html:11-22 (the claim); hugo-coder layouts/_partials/head/theme-styles.html:1-3 (the cause, un-overridden by the kit)` | Three FontAwesome preloads sit ahead of the VG Wort pixel preload and all three 404 on a project-path site — the head/extensions comment asserting the pixel is "FIRST in the connection queue" is false in the built output |

**The largest single item is not a bug but a measurement**: 282 registered marks sit on pages under
VG Wort's 1,800-character Mindestumfang, and no gate in the battery can reach them, because C6
measures source markdown while the floor is defined on rendered prose. That is a disposal decision
per page — write or withdraw — of the same kind as the 58 already listed in
`kit/docs/marked-placeholders.md`, and roughly five times the size.

**Still open and still the highest-value hour in the programme:** the twenty-code T.O.M. hand
sample. 384 of efl's 385 marks are dated six days before the Quarto→Hugo migration and were keyed
on `qmd_path`; all 336 of fle's carry no registration date in any repository. Nothing in the repos
can prove those marks are registered against the URLs they now render on. It needs portal
credentials, so it is the author's, not the platform's.

---

## O — CI, supply chain and the org plane

| | file | finding |
|---|---|---|
| BLO | `kit/gates.yml:100` | A3, the blocking VG Wort URL-lock gate, is invoked by nothing — and `kit check` drops it without even a SKIP line |
| BLO | `.github/scripts/kit_drift.py:69-75,102-122` | A1's kit-module version check is dead in CI: actions/checkout of `.kit` at ref v1 leaves no semver tags, so `latest` is None and every comparison is skipped |
| MAJ | `scripts/org_audit.py:34` | org_audit's write-smell patterns miss `permissions: write-all` and every auto-commit action outside the two hardcoded names |
| MAJ | `kit/README.md:35-36; .github/docs/adr/0001-...md:51; .github/docs/adr/0002-...md:52` | Three documents call kit/example's --panicOnWarning build 'the platform's first gate' and cite a 'drift test in kit CI'; the kit repository has no CI of any kind |

---

## U — curriculum

| | file | finding |
|---|---|---|
| BLO | `curriculum/VERSION:1` | Tag v1.2.0 ships VERSION=1.1.0, so resolve aborts at exit 6 before examining a single descriptor id |
| MAJ | `curriculum/scripts/conformance_audit.py:54` | preA1 is unreachable: `complete` is documented as Pre-A1–C2 but SPANS excludes preA1, so every preA1 id is a hard exit 3 |
| MAJ | `curriculum/coverage.yml:17` | coverage.yml is stale at HEAD (complete: 441 vs 412, plus an obsolete `partial` span) and `coverage --check` is wired nowhere |
| MAJ | `curriculum/examples/de-a1/conformance.yml:15` | The repo's shipped conformance example fails the repo's own resolver, while verification.md ticks it as passing "which CI runs" |

---

## C — configuration drift

| | file | finding |
|---|---|---|
| MAJ | `kit/gates.yml:101,293` | A3 and A16 both carry a `runs:` claim in gates.yml that nothing honours — neither gate is invoked by any workflow |
| MAJ | `kit/assets/css/custom.css:17` | nsf and nvt download 40 webfonts, preload one, and render every page in the system font: the kit's generated fonts.css names families the kit's own custom.css never asks for |
| MAJ | `daf/static/css/fonts.css:1 (also efl/, fle/, website/, ressources/static/css/fonts.css)` | Five of seven sites shadow the kit's generated fonts.css with a hand-copied pre-tier one, so `script_tier: core` is unmet by 527 of its 759 declared codepoints — including U+2192, which renders on 509 pages |
| MAJ | `nsf/.gitignore (absent), nvt/.gitignore (absent)` | nsf and nvt have no .gitignore and have committed their built site: 70 of 92 tracked files are public/, plus resources/_gen and .hugo_build.lock |
| MAJ | `.github/workflows/course-build.yml:28` | course-build.yml pins curriculum at v1.1.0 while every course manifest pins framework 1.2.0 — A16 would hard-fail exit 6 in CI and pass locally |
| MAJ | `kit/assets/css/custom.css:280-284 (63 var() uses with no fallback); contract stated at kit/hugo.defaults.toml:55; violated by daf/hugo.toml:42` | daf loads the kit's custom.css without tokens.css, so 163 of its 247 callouts lose their type colour — the only cue distinguishing tip from warning |

---

## H — harmonisation: one design language, eleven forks deleted, zero URLs moved

The design study's conclusion, after four competing proposals and four judges:

> Eleven of the twenty course-local layouts exist for one mechanical reason: **Hugo selects a
> template by SECTION NAME, and a section name is a frozen URL.** `layouts/materials/materials-list.html`
> and `layouts/materiel/materials-list.html` are the same 92-line file twice because *materials* and
> *materiel* are different words, not because the courses need different templates.

Select by a front-matter `layout:` key at a section-neutral kit path and the forks collapse — with
no `url_shape` invented, which is the abstraction daf's `kit-overrides.yml` asks for and which the
judges agreed would have re-created ADR-0003's rejected alternative in YAML.

**Measured, with the kit resolving locally:** course-local layouts 20 → 9; kit 26 → 31; daf 2 → 1,
efl 4 → 2, fle 4 → 1, website 6 → 1, ressources 4 → 4, nsf/nvt 0 → 0. File sets: efl 1917 → 1917
diff empty; daf 1112 → 1113 (one added stylesheet, nothing removed); fle 2055 → 2053 (two removed,
both belonging to a dead network shell whose graph has never existed); website 97 → 97. **`kit
urldiff`: A3 OK on all 789 marks.**

| id | size | repo | title | depends on |
|---|---|---|---|---|
| H1 | L | kit + .github | Harness first — the gates cannot see the only failure this migration has | — |
| H2 | M | kit | Chrome i18n that scales to fifteen courses, not one more language | H1 |
| H3 | L | kit | Materials templates in the kit, selected by layout, never by section name | H1, H2 |
| H4 | M | kit | The three partials the kit has never shipped | H1, H2 |
| H5 | S | kit | The two-line font fix that repairs typography on every future course | H1 |
| H6 | S | kit | Cut v1.22.0 and prove all seven consumers green **locally** first | H3, H4, H5 |
| H7 | M | daf | adoption — two layouts to one | H6 |
| H8 | M | efl | adoption — four to two, and 416 lines of dead Quarto SCSS | H6 |
| H9 | M | fle | adoption — four to one, and the empty-`<h2>` bug closed | H6 |
| H10 | M | website | adoption — six to one, un-shadowing the kit stylesheet | H6 |
| H11 | S | ressources, nsf, nvt | pin bump and declaration only | H6 |
| H12 | S | kit | **Move the `v1` tag** — the one action that changes every repo's CI at once | H7–H11 all merged |
| H13 | M | kit + 7 PRs | v1.23.0 — delete the shim, make the new gates blocking | H12 |
| H14 | S | fle | Retire the orphaned network assets | H9 |

H2 is not optional and not cosmetic: the kit ships `de.yaml` and `en.yaml` only, so **fle renders
856 empty `aria-label`s, 156 empty `<h2>`s and 312 links with no accessible name**, and ten queued
roadmaps set `defaultContentLanguage` to es/it/nl/ru/nb/el/tr/uk. Hugo merges i18n key by key
across modules, so a kit `fr.yaml` plus a one-key course override gives the right answer on both.

### What harmonisation explicitly does not touch

Every URL, on all three axes. The three courses' section vocabularies, separators, ordinals, 312
`slug:` overrides, French and German section words, and all 828 aliases stay exactly as they are.
Also left alone, each for a reason recorded in the study: `[taxonomies]`, the raw furniture HTML
(A19's note records that converting daf's 65 card blocks would drop 60 headings out of five
landing-page outlines), each course's topic vocabulary, the per-course accent, efl's
Baden-Württemberg `bildungsplan:` block, the three unit heading spines, and website's worldmap.

| | file | finding |
|---|---|---|
| BLO | `kit/i18n/ (only de.yaml, en.yaml) — emitters: kit/layouts/_partials/header.html:13,47; kit/layouts/_partials/page.html:22; kit/layouts/_partials/material-links.html:8,9,10,15,16,17` | kit ships no i18n/fr.yaml, so every un-defaulted i18n call renders empty on fle: 856 empty aria-labels, 156 empty <h2>, 312 links with no accessible name |
| MAJ | `kit/layouts/_partials/header.html:51,66 (emitters) vs kit/assets/css/custom.css:996 (the only definition)` | ressources renders the kit header's screen-reader-only text as visible page furniture — `.visually-hidden` exists only in the kit's custom.css, which ressources does not load |
| MAJ | `kit/i18n/ (de.yaml, en.yaml only); consumed at kit/layouts/_partials/header.html:13,47` | ressources' French pages announce their chrome in German: no kit fr.yaml, so Hugo falls back to the default content language (de) |

---

## P — documentation that is false

Twenty-three findings. Not cosmetic: three of the live courses publish a licence statement that
ADR-0004 superseded, and `kit/audio/NOTICE.md` — the organisation's voice-attribution registry —
still credits two NonCommercial-derived voices that were withdrawn.

| | file | finding |
|---|---|---|
| BLO | `efl/README.md:61-62, fle/README.md:52-53, daf/README.md:73-79,122` | efl, fle and daf READMEs still publish the pre-ADR-0004 licence statement: content CC BY 4.0, LICENSE as the content file, LICENSE-CODE.md as MIT |
| BLO | `kit/audio/NOTICE.md:17-19` | kit/audio/NOTICE.md — the org's voice-attribution registry — credits two withdrawn NonCommercial-derived voices and omits the two courses that actually owe CC BY 4.0 attribution |
| MAJ | `kit/scripts/verify_fonts.py:43-49` | A4 checks 7 fonts and the deployed site ships 46: six Font Awesome faces reach every course site with no attribution row and no NOTICE.md entry |
| MAJ | `kit/scripts/verify_pdf_metadata.py:61` | D2 enforces only /Author although every one of the 852 shipped PDFs would pass --strict today, and REPORTED_FIELDS is dead code so three fields are neither enforced nor reported |
| MAJ | `daf/hugo.toml:25` | Nothing compares hugo.toml `[params].code` with boulingua.yml `code`; daf/hugo.toml:25 says gate A11 does, and A11 is `status: planned, scripts: [], battery: false` |
| MAJ | `kit/audio/voices.yml:671` | nsf's provenance_note is the BLOCKED voice's note, contradicting its own `provenance: clean`, its piper_key and the model card |
| MAJ | `.github/docs/adr/0014-eqs-1-normative-five-step-keys-one-exam-per-unit.md:9,28,29,32,46` | ADR-0014 declares EQS-1 normative and names five canonical files in curriculum; curriculum/standards/ does not exist and none of the five files do |
| MAJ | `kit/README.md:34, :38, :40, :49-55` | kit/README.md's Layout and 'Arriving later' sections are stale on four counts, including an 'Arriving later' list in which every item has already arrived |
| MAJ | `.github/docs/adr/0008-xelatex-polyglossia-one-tex-engine.md:40; .github/docs/adr/0009-materials-committed-no-generation-on-the-deploy-path.md:26` | ADR-0008 and ADR-0009 pin the toolchain to kit/Containerfile, which does not exist anywhere in the org |
| MAJ | `.github/profile/README.md:79-81; .github/SECURITY.md:36` | profile/README.md and SECURITY.md tell the public that course repos contain no code; four live repos carry 27 Python scripts, 4 shell scripts and 13 layout templates |

---

## K — kit correctness and dead code

| | file | finding |
|---|---|---|
| BLO | `kit/scripts/verify_legal_placeholders.py:150` | C7 'rendered placeholders' inspects only the nine legal slugs — an unfilled ⟨…⟩ and a literal TODO shipped on 12 built ressources pages with both A5 and C7 green |
| BLO | `kit/scripts/verify_js_budget.py:34` | C15's measurement window is one directory name, so 203,790 B gz of eagerly-deferred Cytoscape on fle is unbudgeted, and efl and ressources are budgeted at zero |
| BLO | `kit/scripts/regen_audio.py:110` | regen_audio.py re-synthesised the DISPLAY transcript instead of the TTS text — all 560 vocabulary clips lost the pauses between terms |
| BLO | `kit/audio/build_audio.py:201` | build_audio.py: a failed piper call silently republishes the PREVIOUS clip's audio under the next clip's filename, and writes its hash so it is never retried |
| BLO | `kit/layouts/materials/list.html:21,27,28` | kit/layouts/materials/list.html emits root-absolute hrefs — relURL does not prefix a leading-slash path — so all 362 links on efl's three materials pages 404 |
| MAJ | `kit/scripts/render_thumbs.py:66` | render_thumbs.py can never succeed: `n` and `n_pdf` are never initialised, and a bare `except Exception` reports the crash as a per-PDF render failure |
| MAJ | `kit/scripts/render_thumbs.py:29` | render_thumbs.py — D3's 'one renderer' — resolves its repo from __file__, crashes with UnboundLocalError on the first PDF it finds, and exits 0 when it finds none |
| MAJ | `kit/scripts/verify_voices.py:116` | D6's provenance check fires only on `provenance: blocked` — omitting the key lets an en_US-lessac-medium fine-tune through, while declaring `provenance: clean` honestly fails |
| MAJ | `.github/workflows/link-check.yml:17` | link-check.yml never checks out a course — the weekly "external link rot" job scans only the 46-file .github repo |
| MAJ | `kit/latex/boulingua-sheet.sty:97` | Every one of the 336 English and French worksheet PDFs prints the German word "Lösungen" over its answer key: \blgsetui has no caller and the package defaults to german |
| MAJ | `kit/bin/kit:395` | `kit audio build` crashes with IndexError — the documented entry point for the whole audio pipeline has never worked |
| MAJ | `kit/layouts/_partials/vgwort/url.html:22` | The `.Paginator` probe in the <head> pre-initialises the default pager, so a course template's `.Paginate` silently ignores both its filtered page set and its page size |

---

## Verification

No workstream is done on a judgement. Every step is bracketed by six commands, and a course-side
step repeats all six in its PR body:

| | invariant | command |
|---|---|---|
| I0 | the kit under test is the kit you edited | `hugo config mounts \| grep -A6 boulingua/kit` |
| I1 | no published file removed or moved | `kit urlset --diff <base> <now>` |
| I2 | every Zählmarke still on its URL | `kit urldiff <repo>` |
| I3 | the rendered pixels changed only where intended | `kit pixeldiff <base> <now>` |
| I4 | battery green, build warning-clean | `hugo --panicOnWarning …` then `kit check <repo>` |
| I5 | the tree holds nothing but the change | `git status --porcelain` |

Baselines come from a worktree at the merge base, never from a committed file.

---

## What this programme is not

It does not touch content. The ~1,100 author-days in `programme-roadmap.md` are unchanged by any of
it, and none of the 145 findings is a reason to write a different course. What it changes is
whether the organisation can tell, mechanically, that a course is correct — which is the thing that
was quietly untrue while thirty-seven blocking gates reported green.
