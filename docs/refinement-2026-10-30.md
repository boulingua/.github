# Suite refinement — 30 October 2026

Status: local engineering candidate implemented; educational and publication criteria remain open. This record supersedes older audit measurements only where fresh evidence is recorded. Architectural decisions remain authoritative. No release readiness is claimed by the existence of this document.

## Scope and acceptance

All 30 repositories are in scope: 26 active repositories and four archived predecessors. The public teaching system serves German school teachers and independent language learners; the reading tools provide a separate alphabet-practice journey. The private assessment repository preserves school examination sources and templates.

A dependable release must build from documented prerequisites, exercise its principal user journeys, preserve existing content and published addresses, report invalid inputs and incomplete checks honestly, maintain source and licence provenance, and provide a reproducible local equivalent of its CI checks. Course conformance requires reviewed evidence; a compilation or a proposed descriptor mapping is not educational approval.

Archived generators remain historical references. Their executable successors are refined in `kit`; this programme does not unarchive repositories or restart obsolete implementations.

## Milestones

| Milestone | Outcome and changes | Dependencies | Completion evidence |
|---|---|---|---|
| 1. Baseline | Inventory, clean isolated worktrees, exact toolchain, builds, existing tests, current hosted CI, repository classifications | None | Commands, revisions, results and environment limitations recorded |
| 2. Foundations | Correct gate execution, useful failure handling, reproducible dependency selection, explicit course/product integration rules | Baseline | Negative controls and clean builds through actual entry points |
| 3. Course consistency | Shared templates, accessible UI, verified downloads and URLs, valid curriculum metadata | Foundations | All affected course builds, published URL comparison, realistic browser journeys |
| 4. Products and expansion | Reading/extension installation and recovery, assessment source validation, honest new-language prerequisites and status | Relevant foundations | Product-specific tests and per-repository first-use records |
| 5. Release handover | Regression review, dependency/security checks, coherent documentation, release order and unresolved requirements | Previous milestones | Evidence-based readiness report, no unexplained failing required checks |

## Initial observations

- GitHub inventory: 29 public repositories and one private repository. All 30 source checkouts were clean and matched their remote default-branch revisions at the start.
- The latest hosted runs for the seven course/hub sites and both newer products succeeded. The organisation's scheduled `kit-drift` run on 26 October failed: it applies the course-only workflow contract to Scriptlibrary and also reports a shared-template override. This needs an explicit product contract, not an unexplained exclusion.
- Source inspection found 180 English, 156 French and 60 German teaching units. English and French each have sibling examination pages; German has none. Norwegian and Dutch have four shell/legal pages each. The other 13 language repositories are scaffolds.
- The courses use `curriculum.yml` as their conformance manifests, although older documentation calls the file `conformance.yml`. These manifests declare work in progress, with proposed descriptor mappings that must not be silently converted into reviewed claims.
- Some READMEs still document Quarto or the retired generators while current workflows use Hugo and `kit`. Historical roadmaps contain measurements and failure states that must be rechecked before implementation.
- Baseline tool availability on this Mac was incomplete. Hugo extended 0.159.2 and Go 1.26.1 are being installed in the isolated refinement tools directory using upstream checksums. Python dependencies are isolated from the user's global environment.

## Preservation and publication

Work is on `refine/2026-10-30` in separate worktrees. Original main worktrees and source material remain available. No source material, published address, counting-mark assignment, archived history, or human review record is removed to obtain a passing check. Remote deployment, merging, moving shared release tags, and submission are separate release actions; this record does not assert that any has occurred.

Authorship for commits is R. Heller, using the existing authenticated account and verified configured identity.

## Implementation evidence (in progress)

- The isolated baseline built all eight existing Hugo sites. The extension's unit tests and package build passed. Scriptlibrary's edition verifier passed for 288 PDFs (36,623 pages). These baseline successes did not establish working browser behaviour.
- Shared failure-path tests now reject missing search indexes, invalid minified shortcode HTML, incomplete exam marking schemes, destructive YAML list replacement, stale LaTeX output, missing glyphs and failed audio synthesis. Human recordings are protected before synthesis starts. Seventeen kit regression tests passed under Python 3.12.16; fourteen framework regression tests passed.
- `kit build` builds Hugo and the configured Pagefind index. The three established courses now have a search page. French interface translations and an effective kit-plus-course translation check were added. Native menu disclosures, skip navigation and keyboard controls are under browser verification.
- The framework resolver validates manifest shape and exact page/descriptor pairs in both directions, checks source levels, refuses proposed mappings in a `met` claim, rounds the 90% threshold upward, and applies an explicit Latin profile under ADR-0013. All five existing course manifests passed the strengthened structural resolution. The generated coverage table was stale and has been recomputed. Native/educational approval of proposed mappings is still outstanding.
- English had 62 nonunique unit basenames across tracks. Its audio manifests now use unique material keys; 304 recording references matched their source transcripts exactly. Thirty-six unmatched passages retain text without claiming an available recording. Legacy manifests and all recording files were preserved. No new voice approval or model provenance was invented.
- The new recording gate exposes missing historical model metadata and absent dated auditions. These are release findings, not successful checks. Voice candidates remain candidates.
- The workflow audit now inspects YAML permissions and failure suppression, handles Git worktrees, and checks course/product contracts. The fresh organisation audit passed across 26 active repositories and 14 workflows. Scriptlibrary's justified home-page override is recorded separately from course conventions.
- A real Chromium extension test passed: injection, editable-region protection, temporary original-text view, dynamic content, lossless restore, and opt-in reload/unregister. Permission-consent UI is not automated. Browser tests now use Playwright's bundled Chromium instead of a Linux-only executable path.
- Real XeLaTeX 2026 compiled representative English, French and German slide decks and worksheets in disposable copies. All six PDFs carried the correct educational author and title; no extracted text block extended beyond its page. Visual review exposed further extraction problems (a vocabulary table header included as a term; vocabulary selected as reading prose); these remain under repair. The committed material corpus has not been regenerated.
- Browser checks exposed project-prefix errors in theme assets and links, menu focus problems, contrast against the actual page background, and minification changing Scriptlibrary source whitespace. Repairs and reruns are in progress. Passing the earlier palette or PDF checks did not cover these failures.

The supported verification environment is Hugo extended 0.159.2, Go 1.26.1,
Python 3.12.16 and Node 22.23.4. Upstream checksums were verified for the local
tool installs. Initial baselines used Python 3.15 and Node 26; subsequent release
checks use the supported versions. No GitHub publication has occurred.

## Current evidence and remaining release work

The following supersedes the earlier in-progress measurements above.

- Twenty existing/new course and hub sites build locally, and Scriptlibrary
  builds separately. All fifteen development courses, the website and the
  resource catalogue pass the complete local kit battery. The three established
  courses fail D6 because historical audio lacks adequate provenance and dated
  approval. Their other blocking engineering checks pass after the final
  template/override repair. The English C1 and resource-catalogue C4 registration warnings remain recorded.
- Forty kit regressions, fifteen curriculum regressions and four workflow
  regressions passed. The organisation audit examined 26 active repositories
  and 29 workflows with zero findings. Local browser checks exercise search,
  downloads, filtering, lazy graphs, mobile menus, no-JavaScript content and
  representative WCAG 2.1 AA checks; this is not a full manual accessibility
  review or an observation of hosted CI.
- EFL, FLE and DaF use section-neutral template selection without renaming
  published URLs. Shared material sync passed for all eighteen courses.
  The material parser handled all 396 units. Six representative regenerated
  PDFs were compiled and visually reviewed; fixes retain tasks, criteria,
  differentiation, numbering and lesson-only keys. The 852 committed course
  PDFs were preserved rather than silently replaced by an unreviewed corpus.
- Fourteen candidate voices produced 42 locally validated WAV previews with
  model/config/card digests and speaker records. A real disposable unit produced
  two Opus clips; a repeat synthesised none. Pronunciation approval is pending.
  Existing recordings were preserved; new previews do not establish their
  historical provenance.
- Scriptbridge passed clean installation, unit checks, packaging and real
  Chromium injection/restore/preference journeys. Scriptlibrary passed all 288
  book/profile browser combinations and verified 288 PDFs / 36,623 pages in a
  fresh environment using its exact pinned dependencies. Source text and PDF
  bytes were retained; HTML minification no longer collapses reading text.
- The private archival assessment work produced ten clearly labelled review
  PDFs in student/teacher modes while preserving all original sources. Layout
  checks passed; educational, rights and scoring decisions remain private
  repository findings and are not grounds for public distribution.

| Remaining item | Classification and impact | Completion criterion |
|---|---|---|
| Two missing framework scales | Confirmed high-severity source omission | Independently reviewed additive statements; source/coverage/self-audit pass |
| Historical course audio | Confirmed release blocker, D6 | Verified original provenance or approved replacement recordings and receipts |
| Proposed course mappings | Unreviewed educational claims | Qualified review of actual lessons/assessments and descriptor pairs |
| Fifteen developing courses | Intended teaching content not yet authored | Accepted ADR scope, named reviewers, reviewed lessons/materials/audio and conformance evidence |
| Full print regeneration | Representative pipeline verified only | Course-by-course content/layout review of actual regenerated corpus before replacement |
| Hosted CI and deployment | Not performed | Compatible immutable dependencies, observed required CI, authorised publication |
| Registered counting URLs | External account evidence remains distinct from local URL preservation | Reconcile authoritative registration export without changing existing addresses |

The runnable first-use paths are in each repository README; a local review
workspace also holds logs, screenshots, PDF checks and a revision receipt.
[Release order and recovery](release-candidate-2026-10-30.md) explicitly prevent
mixing the new workflow with old dependency pins. This suite is materially
improved and locally reviewable; it is **not** fully authored, approved or
released. Remaining learning content and reviews are acceptance work, not
optional cosmetic follow-ups.
