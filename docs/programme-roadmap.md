# Programme roadmap — refined

**Status date: 2026-08-30.** Every count in this file was measured on that date against
the checked-out trees and the live GitHub state, not copied forward from
`BOULINGUA-PROGRAMME.md`.

This file **refines** the programme; it does not replace it. Where the two disagree:

- on a **measurement**, this file wins — the programme's figures were taken on
  2026-08-21 and eight days of Phase 3 work has moved most of them;
- on a **decision**, the ADR wins, always. Nothing here reopens ADR-0003, ADR-0016,
  ADR-0018 or ADR-0020;
- on **scope**, the programme wins. This file adds no course, no level and no gate that
  §S2 does not already name.

Work items carry an ID with a stable prefix so a commit, an issue and this file can name
the same thing: **R0** stop-ship, **R1** Phase 3 tail, **R2** wave 1, **R3** waves 2–4,
**R4** the closing phase. Sizes use the programme's scale — **S** ≤1 day, **M** 2–5 days,
**L** 1–3 weeks, **XL** >3 weeks — and author-days are counted separately from engineering
days throughout, because they do not substitute for one another.

---

## 0. Position on 2026-08-30

### 0.1 What is true of the org

| Fact | Value |
|---|---|
| Repositories | 27 (26 + `.github`); `pagegen`, `slidegen`, `sheetgen`, `audiogen` archived |
| Platform | `boulingua/kit` at **v1.17.0**, moving `v1` tag on the same commit |
| Kit pinned by every course | **v1.16.0** — one minor behind the tip |
| Gate battery | 45 IDs in `kit/gates.yml` — **22 live, 12 partial, 11 planned** |
| Gate suppressions org-wide | 0 |
| Registered VG Wort marks | **821** — daf 68, efl 402, fle 351 |
| URL locks | `url-lock-provisional.csv` present in all three — 69 / 403 / 352 data rows |
| Live sites | 5, all returning 200, all serving the build of **2026-08-21** |
| Last green deploy, any repo | **2026-08-21** |
| CI today | **7 of 7 course repos red**, every run since 2026-08-22 |
| Open issues / PRs | 0 |
| Branch protection | **none configured on any repository** |

### 0.2 What is finished

Phases 0, 1 and 2 are complete, and Phase 3 has landed structurally on all five live
repos. Concretely, and verified in the trees rather than in commit subjects:

- **F1–F12** — `kit` exists with the four toolchains subtree-merged and their histories
  intact; `bin/kit` carries its nine verbs (`check design sync urldiff materials audio
  vgwort new menu` plus `bundles`); `design/fonts.yaml` and `design/build_fonts.py` ship
  with `fonts/{core,latin-ext,greek,cyrillic}` built; `latex/` carries the four `.sty`
  files and the two templates; `audio/` carries `voices.yml`, `build_audio.py` and
  `audition.py`; `curriculum` is at **v1.2.0** and all five courses consume it.
- **S1–S6** — the org control plane is live (`CONTRIBUTING`, `SECURITY`, six issue forms,
  20 ADRs, three operations docs, five reusable workflows); `gates.yml` is the single
  definition of the battery and `verify_gate_register.py` joins it to the tree in both
  directions; the palette was re-derived to meet its own published contrast rules; the
  EQS shortcode set is closed and gate A19 checks a repo's own declaration.
- **P3.1–P3.5** — `website`, `daf`, `fle`, `efl` and `ressources` are all on the kit as a
  Hugo module, listed **before** `hugo-coder`, with the marks intact through every move:
  daf 68, efl 402, fle 351, unchanged from the opening census.
- **`fle` is converted** — 312 leaf bundles, URL-neutral, every `slug:` override kept.
- **Voice provenance** — all five shipped voices were replaced with models whose
  MODEL_CARD states training from scratch; `docs/voice-provenance.md` records how each
  replacement was verified; gate D6 refuses a voice that is not `provenance: clean`.
- **Phase 4 has started** — `nsf` and `nvt` completed Stage 1 (instantiated by `kit new`,
  not copied) and Stage 4 (course plan, conformance M0) on 2026-08-26.

### 0.3 What is provably not done

Measured, not inferred:

| | daf | efl | fle | nsf | nvt |
|---|---|---|---|---|---|
| Unit pages (`page_type: unit`) | 60 | 180 | 156 | 0 | 0 |
| Exam pages (`page_type: exam`) | **0** | 180 | 156 | 0 | 0 |
| Descriptor claims `asserted` | **0** of 60 | **0** of 360 | **0** of 312 | — | — |
| Marks in `data/vgwort.yaml` | 68 | 402 | **2** (349 still in front matter) | 0 | 0 |
| Audio segments withheld | 355 of 357 | 182 of 193 | 663 of 670 | — | — |
| `kit check` blocking failures | 0 | **36** (A18/C6) | **96** (A18/C6) | 0 | 0 |
| GitHub Pages enabled | yes | yes | yes | **no** | **no** |

---

## 1. R0 — stop-ship

Six items. Nothing downstream is worth starting while any of the first three stand,
because none of it can be shown to work.

### R0.1 — The gate register resolves the org from the kit's parent, so CI cannot run the battery — **S**

`kit/scripts/verify_gate_register.py:66` defaults `org` to `KIT.parent`, and `:61`
resolves a non-kit owner as `org / owner`. Locally the kit sits at
`~/Documents/GitHub/boulingua/public/kit`, so `org` is the checkout root, `.github/` and
`curriculum/` are siblings, and the join succeeds. In CI the reusable workflow checks the
kit out **inside the course** at `.kit` (`course-build.yml:56`) and curriculum at
`.curriculum` (`:63`), and never checks out `.github` at all. So `org` becomes the course
root and the verifier looks for:

```
gates.yml[A1]:  <course>/.github/scripts/kit_drift.py          → the course's own workflow dir
gates.yml[A16]: <course>/curriculum/scripts/conformance_audit.py → checkout is at .curriculum
```

Both are absent, the verifier prints `gates.yml is inconsistent with the tree — battery
not run` and exits 1 **before any gate executes**.

This is the org's signature defect one level up: not a gate that cannot fail, but a
*register* that fails in a way that stops every gate from running. It is fail-closed,
which is the right direction, but the effect since 2026-08-26 is that **no gate has
examined any site in the org**, and since 2026-08-22 **nothing has deployed**. The live
sites are nine days stale: none of the module reordering, the i18n work, the `page_type`
migration, the palette repair or the shortcode closure is public.

**Fix.** Give the register an explicit checkout map instead of a derived one. The workflow
knows where it put each repo; pass it. Add `--owner-root .github=<path>` /
`--owner-root curriculum=<path>` (or a single `--checkouts` mapping), have
`course-build.yml` check out `boulingua/.github` at `.github-org` and pass all three, and
make an unmapped owner a hard error rather than a path guess.

**Exit test.** A run of the register inside a fresh CI-shaped checkout — kit at `.kit`,
curriculum at `.curriculum`, no sibling directories — reports OK; and a run with a
deliberately wrong mapping fails. Both cases go in `test_battery_drift.py`, because a
register that has been wrong in CI for four days while passing locally is exactly the
thing that needs a test standing in the CI shape.

### R0.2 — `nsf` and `nvt` have no GitHub Pages site, so Stage 1's gate never actually passed — **S**

`gh api repos/boulingua/{nsf,nvt}/pages` returns 404. `actions/configure-pages@v5` fails
at step 10, and `Build site`, `kit check` and `Upload artifact` are all skipped. Every run
either repo has ever had — three each — has failed at the same step.

Stage 1's gate is *"`bin/kit check` green on an empty course; the repo builds and deploys
with zero units."* Neither half has ever been demonstrated for wave 1. Locally both are
clean, which is why it was not noticed.

**Fix.** Enable Pages with `build_type: workflow` on both, then re-run. Add the Pages
check to Stage 0 or Stage 1 of the runbook so the next nine courses do not each discover
it: `gh api repos/boulingua/<code>/pages` returning 200 is a one-line precondition.

### R0.3 — `efl` and `fle` are genuinely red, and R0.1 is currently hiding it — **M**

With the battery running locally, `kit check` fails A18/C6 on both:

- **`efl` — 36 problems** across 42 marked non-unit pages: 8 `_index.md` section pages
  carrying a mark (`about/`, `about/courses/`, `track-e/kl05`–`kl11`), and 12 pages under
  the 1,800-character Mindestumfang while holding one — the seven `schedule/index.md`
  pages at 1,192–1,259 characters, `acknowledgements/` at 1,587,
  `appendices/teaching-workflow/` at 1,575, `appendices/skills-decision-tree/` at 809,
  `about/courses/` at 401.
- **`fle` — 96 problems** across 39 marked non-unit pages: the same two classes plus a
  third that is worse — **22 pages carry a mark and say the content is still to come**
  (`annexes/competences.md`, `erreurs_typiques.md`, `glossaire.md`, `grille_evaluation.md`,
  `strategies.md` and the rest, ~215 bytes each, *"Cette annexe sera remplie après
  l'écriture des 156 unités"*) — and **no author in front matter** on the marked pages,
  which is C8's territory arriving through C6.

`daf` is the comparison that makes the placeholder count a finding rather than a
convention: 18 placeholder pages, zero marks on them.

**These are author decisions, not engineering ones**, and the roadmap must not pretend
otherwise. For each of the 22: withdraw the mark, or write the page. For each under-floor
page: write it up over 1,800 rendered characters, or withdraw. Both cost something and the
programme says so. `docs/marked-placeholders.md` in the kit holds the list.

**Sequencing note.** Do this *after* R0.1, not before. Fixing the register turns two
already-red repos from "not examined" into "failing", and it is better to know that from a
green pipeline than to discover it on the commit that was meant to turn the pipeline green.

### R0.4 — Gate C4 audits the kit while standing in a course, and has never examined a site — **S**

`kit/scripts/verify_vgwort_coverage.py:24-26`:

```python
ROOT   = Path(__file__).resolve().parents[1]   # the kit, always
PUBLIC = ROOT / "public"
DATA   = ROOT / "data" / "vgwort.yaml"
```

The script reads no `sys.argv` at all, while `bin/kit check` passes the repo as
`argv[1]` (`bin/kit:114`). So C4 opens `kit/data/vgwort.yaml`, does not find it, prints
*"data/vgwort.yaml missing — VG Wort partial will render nothing"* and returns 1 — on
**every** repo, including the three where that file exists and holds 821 entries between
them. Its severity is `warn`, so the wrong answer has never blocked anything and the
message has been on screen since the gate was promoted.

C4 is the only gate that finds long-form pages which have crossed the Mindestumfang and
have no mark — that is, the only gate pointed at **revenue not yet claimed**. It has never
run.

Its skip list is a second, smaller instance of the same fault: `SKIP_PREFIXES` at `:30`
carries `/track-e/` and `/track-gm/`, which are efl's section paths, in a script that runs
on all five.

**Fix.** Take the repo from `argv[1]` like every sibling script; derive `PUBLIC` and `DATA`
from it; move the skip list into `boulingua.yml` per course, or key it off `page_type:
section` which now exists everywhere. **Then run it on all five and expect findings** — it
has a year of unexamined pages behind it.

**Exit test.** C4 run against `kit` itself reports n/a rather than failing; run against
`daf` reports a number; and a page seeded over 1,800 characters with no mark makes it warn.
(`verify_legal_placeholders.py:26` has the same `parents[1]` line but reads `sys.argv[1]`
at `:31`, so A5/C7 are correct — it is worth leaving a comment there saying why, since the
two files now look identical at the top and only one of them is right.)

### R0.5 — The audition gate downloads the encumbered model the provenance work removed — **S**

`kit/audio/audition.py:118` fetches `row["url"]` and refuses to construct one from the key
— *"never construct one from the key"* — while `kit/scripts/regen_audio.py:49` generates
from `row["piper_key"]`. For the five replaced voices those two fields now name different
models:

| Course | `piper_key` (generation) | `url` / `md5` (audition) |
|---|---|---|
| efl | `en_GB-cori-medium` | `en_GB-alba-medium` |
| fle | `fr_FR-mls-medium` | `fr_FR-siwis-medium` |
| daf | `de_DE-mls-medium` | `de_DE-thorsten-medium` |
| nsf | `no_NO-nvcc-medium` | `no_NO-talesyntese-medium` |
| nvt | `nl_NL-mls-medium` | `nl_NL-ronnie-medium` |

Nothing ships from `url` today, so this is not a licence breach in the published sites.
It is worse in one specific way: **Stage 3's audition — the gate whose whole point is that
a human listened — would have the author listen to the model that was removed.** A verdict
recorded that way is a false verdict, and `auditions/` holds only `TEMPLATE.md`, so no
verdict has been recorded yet and none is contaminated. This has to be fixed before the
first audition, which is wave 1's next stage.

**Fix.** Update `url`, `md5` and `sample_rate` on the five rows to the model
`piper_key` names, and add a register check — `url` basename must equal `piper_key` — to
`verify_voices.py` so the two cannot diverge again. Note `ple`'s row is a false positive
in the same check: `pt_PT-tugão-medium` is percent-encoded in the URL, and the ASCII form
404s, so compare after decoding.

### R0.6 — Uncommitted regenerated audio in three repos, and one truncated file — **S**

Working trees at the time of writing: `daf` 6 changes, `efl` 16, `fle` 9 — the manifests
and `.ogg` files for the 20 segments that were regenerated before the run stopped — plus
`daf/static/materials/audio/unit01_arbeitssuche-und-stellenanzeige/dialogue3.ogg.part`,
a truncated download.

Delete the `.part`, verify the 20 regenerated files play, and commit them as their own
commit before the next batch, so the regeneration has a resumable floor. The atomic-write
change of 2026-08-26 means the next interruption will not leave a partial `.ogg`, but it
did not clean up this one.

---

## 2. R1 — the Phase 3 tail

Phase 3 is structurally complete and substantively is not. These are the items that stand
between "the live repos are on the platform" and "the live repos meet the standard the
platform enforces".

### R1.1 — Regenerate 1,200 withheld audio segments — **M engineering, days of machine time**

| Course | Segments | Withheld | Live |
|---|---|---|---|
| daf | 357 | 355 | 2 |
| efl | 193 | 182 | 11 |
| fle | 670 | 663 | 7 |
| **Total** | **1,220** | **1,200** | **20** |

Every withheld segment is a player the reader does not get. The transcript-only switch is
reversible by design and the sites are correct as they stand — they are simply, at the
moment, three text courses.

Run `regen_audio.py` per course with the fetched clean models, in level-sized batches,
committing each batch. Do **not** start before R0.5, or the audition that is supposed to
approve these voices will have listened to the wrong ones.

**Exit test.** `withheld == 0` in all 60 + 107 + 156 manifests; D6 green; every `.ogg`
opens; no `.part` in the tree.

### R1.2 — `fle`: 349 front-matter marks → `data/vgwort.yaml` — **S**

`fle/data/vgwort.yaml` holds 2 entries; 349 marks are still `vgwort_pixel:` in page front
matter, carried by the kit partial's back-compat path. It works, and it is the last place
in the org where the registry is not a registry.

This is a **re-key event on 349 marks**, so it obeys §12.5 and the rule the flat→bundle
conversion established: the entry is keyed by `url:`, the URL is read from the built site,
and `kit vgwort` refuses the move unless both the URL set and the pixel set survive it.
Run `kit urldiff` before and after; the diff must be empty.

### R1.3 — Dispose of the 118 A18/C6 findings — **author work, ~2 weeks**

See R0.3 for the breakdown. Three decisions, each per page:

1. **22 `fle` placeholder annexes** — write, or withdraw the mark. Writing them is roughly
   22 × 1,800+ characters of appendix prose the course wants anyway.
2. **~20 marked pages under the Mindestumfang** — extend past the floor, or withdraw.
   The seven `efl` schedule pages at ~1,200 characters are the cheapest: ~600 characters
   each of genuine orientation prose.
3. **~11 `_index.md` section pages carrying a mark** — these are navigation surfaces and
   C3 already says a section page is not a Sprachwerk. Withdraw, and record the codes in
   `vgwort-operations.md` so they can be re-used on a page that qualifies.
4. **`fle` marked pages with no `author:`** — mechanical; one front-matter field.

### R1.4 — `daf`: author 60 exam pages — **~30 author-days**

`daf` has 60 units and **0** exam pages, so gate A13 reports *n/a* on the only repo where
one exam per unit is not merely unmet but structurally absent. EQS-3.1a makes the sibling
exam mandatory. This is also up to 60 fresh T.O.M. registrations once the pages clear the
floor — the largest single block of new marks in the programme.

### R1.5 — Confirm the descriptor claims — **~19 author-days**

`asserted: 0` in all three manifests. 732 proposed claims (daf 60, efl 360, fle 312) are
machine rankings whose *structure* is verified — each ID resolves at the page's own level,
no two share a scale, breadth holds — and whose *judgement* is not. Every course stays
`conformance_status: in-progress` while one `implements_basis: proposed` remains, so none
of the three can reach M2, and M2 on waves 1–4 is an entry condition for Programme II.

At ~10 claims an hour of careful reading, 732 claims is ~19 author-days. It is
tranche-able by level, which is how it should be scheduled: confirm A1 across all three
courses first, so the pattern is set before the volume.

### R1.6 — Bump the five live repos to `kit v1.17.0` — **S**

Every course pins v1.16.0; the kit is at v1.17.0, which is the release carrying the four
money gates (C3, C5, A18, C6) and the atomic audio writes. Bump after R0.1, because the
bump commit is the one that should first go green.

### R1.7 — Enforce the branch policy that is already written — **S**

`docs/branch-policy.md` states main is *"Protected, linear history, no force-push"* with
the `course` job as the required check. **No repository in the org has branch protection
configured** — the API returns 404 on all of them. The policy is a document describing a
setting nobody made.

Configure it, on all 27, once CI is green — requiring a check that currently fails would
lock the org out of its own repositories. Also finish the branch cleanup the policy names:
`fle`'s six orphaned `phase4/*` branches, `efl`'s `migration/hugo-coder`, `ressources`'
`add-prompt-docs`.

### R1.8 — Close the 12 partial and 11 planned gates — **M, continuous**

22 of 45 gate IDs are `live`. Each `partial` carries a `gap:` naming what it does not do,
which is the honest form and also a queue. Two are worth pulling forward because a wave-1
course will hit them first: **A1**'s hugo.toml key allowlist and `deploy.yml` equality
check (a scaffolded course is exactly where drift starts), and **A2**'s curriculum-block
milestone, which is what turns R1.5 from a judgement call into a measurement.

---

## 3. R2 — Phase 4, wave 1 (`nsf`, `nvt`)

Both courses are through Stage 1 and Stage 4. Stages 0, 2 and 3 are either done or n/a;
what remains is the authoring loop and the release machinery, run for the first time.

| Stage | State | Work |
|---|---|---|
| 0 Register the language | done | accents, icons, `voices.yml` row, worldmap pin |
| 1 Create the repo | done, **gate never passed** | R0.2 — Pages, then a green run |
| 2 Script/font enablement | n/a | both `script_tier: core` |
| 3 Voice audition | **next**, blocked on R0.5 | fetch, listen, commit `auditions/{nsf,nvt}.md`; `candidate` → `ready` or `none` |
| 4 Course plan, M0 | done | `curriculum.yml` present, conformance M0 |
| 5 Onboarding stage | `nsf` only, small | *Uttale* as 2–3 editorial pages, not a unit sequence |
| 6 Unit loop | **the bulk** | nsf 39–41 units + exams; nvt 36 `core` + exams |
| 7 Materials | per level | decks + worksheets, committed, `/Title` and `/Author` set |
| 8 Audio | per level | on the auditioned voice, or transcript-only |
| 9 Marks | per level | T.O.M. registration; ~80 marks nsf, ~72 nvt |
| 10 Level release | per level | coverage artefacts, conformance stage, CalVer tag |
| 11 Publish to the hub | at A1 | `worldmap.yaml` `upcoming` → `active`; `published: true` |

**Wave 1 completes** when both have shipped Level-0 (nsf) and their A1 tranche under the
full battery with a CalVer tag — not when they are content-complete. **~152 author-days**
for the two `core` scopes; the A1 tranche that closes the wave is roughly a quarter of it.

**What wave 1 is actually for** is the runbook. Three things should come out of it as kit
changes rather than as course changes: the Pages precondition (R0.2), the first real
audition verdict, and `nsf`'s transcript-under-every-player accessibility rule, which the
programme already marks for promotion org-wide.

---

## 4. R3 — waves 2, 3 and 4

Nine courses, all Latin, Greek or Cyrillic, all served by one type family. Entry
conditions and marginal costs are unchanged from §8 of the programme; the wave order rests
on properties of the repos, not preference, and does not depend on any voice ID.

| Wave | Courses | `core` units + exams | Author-days | Engineering |
|---|---|---|---|---|
| 2 | `ele` 41, `ils` 39, `ple` 37–39 | ~117 + same | ~236 | zero enablement |
| 3 | `pfl` 39, `tfl` 32–39, `lle` 35–36 | ~110 + same | ~222 | `tfl` casing layer (S); `lle` macron face check (S) |
| 4 | `gfl` 42–44, `ufl` 54, `rki` 37 | ~135 + same | ~268 | `gfl` Greek verification (S); `ufl` Cyrillic tier (M); `rki` inherits |

Decisions already taken, recorded so they are not re-litigated in the wave: German chrome
for all fifteen scaffolds; one exam per unit universal, which amends `nsf`, `pfl`, `tfl`
and `rki`'s ROADMAP counts upward and is why §11's `N + N` column supersedes each
ROADMAP's §4; `pfl`'s section paths corrected before its first published URL; `tfl` and
`lle` transcript-only, because no licence-clean voice exists for either.

**Wave 4 carries the one real engineering block left in the programme**: `ufl` owns the
Cyrillic tier and `gfl` the Greek, and each needs its `must_render` set declared as a
schema'd `fonts.yaml` column plus a reference deck and worksheet in the target script
(`kit/latex/{slides,worksheet}-template-<code>.tex`, absent today). Ukrainian before
Russian, because ґ і ї є plus U+02BC/U+2019 is a strict superset of ё plus U+0301.

---

## 5. R4 — the closing phase (T.O.M. reconciliation)

Deferred to the end by ADR-0020 and unchanged. Entry condition: every course
content-complete to its declared level, every repo green under the full battery, and
`url-lock-provisional.csv` still present in `efl`, `fle` and `daf` — which it is, in all
three, which is the marker that this phase has not run.

| Step | Action |
|---|---|
| 15.1 | Export the registered URL for all 821 codes from T.O.M. to `~/vgwort/tom-export-<date>.csv`, outside every repository. If there is no bulk export, hand-sample twenty codes across both `registered_at` dates |
| 15.2 | Build all three sites; diff the export against each `sitemap.xml` → `vgwort/tom-diff.csv` |
| 15.3 | Dispose of every `alias-only` row: edit the T.O.M. record where VG Wort permits it, otherwise the §12.5 re-key protocol |
| 15.4 | Backfill `fle`'s 349 missing `registered_at` dates; make C1 blocking org-wide |
| 15.5 | Replace `url-lock-provisional.csv` with `url-lock.csv`, `registered_url` populated; switch A3 from neutrality to correctness |
| 15.6 | Record the finding against ADR-0015 — including "everything was already correct", which is two lines and still worth having |

**The open question this settles** remains open: 399 of `efl`'s 402 marks are dated
2026-04-30, six days before the Quarto→Hugo migration, and the manifests were keyed on
Quarto `qmd_path`. If T.O.M. still holds the old `.html` URLs, those pages serve alias
stubs carrying no pixel and have earned nothing since 2026-05-06. **A twenty-code hand
sample answers it in an afternoon and does not require the phase.** The deferral was a
decision about *repair*, not about *knowing*; taking the sample early costs nothing and
bounds the loss.

No repository may cut its first CalVer tag under the completed programme while
`url-lock-provisional.csv` still exists in it.

---

## 6. Deferred — Programme II

`cfl`, `jfl`, `afl`, `pfa` — ADR-0018. Four scaffolds sit at Stage 1 for the duration,
carrying no marks, so nothing is at risk. Re-entry needs all three of: a **named native
checker** recorded in the `new-language` issue form before any engineering; waves 1–4 at
**M2 or better** on all eleven courses; and the deferred enablement re-scoped as its own
foundations phase.

What still ships in this programme regardless: `pfa`'s generated brand assets and the
`acc-pfa` pair, so A11's `icon count ≠ 18` is not a permanent known failure; `{{< tl >}}`,
because `gfl`, `ufl`, `rki` and `lle` need it under C12; all four rows in `accents.yaml`,
`worldmap.yaml` at `upcoming`, and §11.

---

## 7. Arithmetic

| | Engineering | Author |
|---|---|---|
| R0 stop-ship | ~4 days | — |
| R1 Phase 3 tail | ~2 weeks | ~68 days (R1.3 ~10, R1.4 ~30, R1.5 ~19, rest ~9) |
| R2 wave 1 | ~1 week | ~152 days |
| R3 waves 2–4 | ~4 weeks | ~726 days |
| R4 closing phase | ~1 week | — |
| **Total** | **~9 weeks** | **~946 days** |

Plus the ~157 author-days of `efl` and `fle` retrofit content the programme prices in
§11.1 and this file does not re-count: ID assignment, `topic` reclassification, the 132
`efl` units under the Band I floor, the 309 `fle` answer-key relocations, the 143 `fle`
under-floor exam pages.

**~1,100 author-days stands.** At the ~100 productive days a year a working teacher can
sustain, that is a decade; at 200, five and a half years. Engineering is ~9 weeks and is
almost entirely front-loaded. Nothing in the last eight days has changed that shape, and
the shape is not a problem to be solved — it is the reason the platform had to be built
first, and the reason the wave-completion rule counts an A1 tranche rather than a finished
course.

---

## 8. Order of work

1. **R0.1** — the register. Everything else is unobservable until CI runs.
2. **R0.2** — Pages on `nsf`/`nvt`; wave 1's Stage 1 gate has never passed.
3. **R1.6** — bump to `kit v1.17.0` and take the first green run in nine days.
4. **R0.6, R0.5, R0.4** — commit the stranded audio, repair the audition URLs, give C4 the
   repo. Three small fixes, and C4 will produce findings.
5. **R0.3 / R1.3** — dispose of the 118 A18/C6 findings. Author decisions; the 22 `fle`
   placeholder marks are the ones with a deadline, because a registration asserting a work
   that does not exist is the one defect here that is not merely untidy.
6. **R1.1** — regenerate the 1,200 audio segments, in batches, committing each.
7. **R1.2** — `fle`'s 349 marks into the registry, with a `urldiff` on both sides.
8. **R4.15.1 (early)** — the twenty-code T.O.M. hand sample. Out of order deliberately:
   it is an afternoon, and it bounds a loss that is accruing monthly.
9. **R2** — wave 1's audition and unit loop; **R1.4/R1.5** run in parallel as author work.
10. **R1.7** — branch protection, once green.
11. **R3**, then **R4**.
