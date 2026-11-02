# Release remediation — 31 October 2026

The suite re-audit is being implemented against the existing isolated candidate
branches. The release objective remains usable, reviewed teaching content and
reproducible products. A successful scaffold build or metadata migration does not
close that objective.

## Current continuation — 2 November 2026

The suite is **not ready for a full-course release**. The repairable engineering and source issues have been substantially reduced, but the content deficits and genuine review criteria below remain open. The historical checkpoint below is retained to distinguish earlier evidence from current observations.

- All **156 FLE standalone assessments** are now reconciled with preserved originals, source-specific decisions and current unit/exam hashes. Scoring validation passes 77 retained grade-scaled papers and 79 explicitly declared points-only papers. Old grade conversions are archived where revised outcomes make them unsuitable; native, pedagogical and assessment-policy review remains pending.
- The core source inventory still records **302 short teaching units, 227 short assessment pages and 188 missing assessment durations**, affecting 380 distinct units across the overlapping conditions. Twelve null point fields belong to explicitly declared EFL Klasse 13 rehearsals; they require an assessment-contract scope decision, not invented totals. The [quantitative milestone](education-next-milestone-2026-11-02.md) identifies each course/level cohort and the [machine-readable inventory](education-next-milestone-2026-11-02.json) records individual paths. Fresh strict EQS checks against the final 2 November public builds reproduce those counts; unit, exam and rendered HTML hashes are recorded. Duration fields are not classroom evidence.
- A fresh EFL assessment inventory identifies **145 learner-visible listening transcripts** and **five incomplete standalone listening stimuli** among 150 papers with listening instructions. A source-preserving first-unit/assessment draft is staged separately and has received independent static source review. Its 1,216 learner words and 3,184 source learner assessment characters meet the draft budgets; A13 arithmetic passes. Native/pedagogical review, timed trials and rendered draft checks remain pending, and no live promotion is claimed. Wholesale transcript hiding is unsafe where a later reading task needs the same passage. Full-course listening validity is an open release blocker.
- Framework population is **1,199 entries** (1,170 preserved plus 29 restored); canonical ID/schema checks pass. The five source-qualifier corrections and independent comparison are recorded. Editorial approval of restored text and task-level approval of course mappings remain pending; no mapping has been mass-promoted to asserted coverage.
- Each of the **eleven Programme I courses** now has a substantive first A1 unit, standalone assessment, pronunciation draft and pending review ledger. Their 33 PDFs and 33 thumbnails have local publication receipts. NSF/NVT source-reference additions and their affected materials have now been refreshed. The combined 153 final supplementary PDFs (120 DaF assessment copies plus 33 Programme I files) comprise 405 checked pages. These first tranches do not establish complete A1 coverage or M2 approval. CFL, JFL, AFL and PFA remain deferred under the accepted re-entry contract.
- Audio production has completed **1,064 candidate clips for all 396 core units**: EFL 350, FLE 506, DaF 208; total duration about 9.72 hours. Fresh 2 November checks bind exact transcript, model, configuration, cache and final published source inputs, including teacher-link metadata revisions, and fully decode each mono Opus file. The review queue contains **1,064 pending records and no invented reviewers**. Browser evidence checks all players and one muted playback sample per course, not pronunciation or native approval. No candidate audio publication is claimed.
- The private French assessment derivative now supplies a clearly fictional teacher listening dialogue, matching keys for ten true/false items and six blanks, and source-specific translation keys: two active prompts in the dated paper, five in the template. Four final PDFs preserve the learner text except the derivative header and keep original point allocations; the final audio-v2 reading candidate decodes successfully at 122.13 seconds. The exact current derivative evidence is `school-language-assessment/derivatives/french-listening-2026-10-31/provenance-verification-2026-11-02.json`; the earlier 125.92-second candidate is superseded. Historical sources remain unchanged. Timing, grading policy, intended-use rights and native/pedagogical approval remain pending.
- **Core classroom-material publication is complete locally:** all 396 units have 1,188 verified PDFs and 1,188 matching thumbnails installed through the guarded publication plan (2,778 writes). Source/answer preservation, escaping, symbol, link, overflow and thumbnail checks passed; representative visual review covered 40 documents and 54 pages across 13 bands. The three course receipts are `docs/material-build-2026-10-31.json`, with actual completion dated 2 November. An independent byte check matches all 396 published unit hashes and all 2,376 PDF/PNG hashes to those receipts. Only the teacher-download metadata changed; a separate receipt records subsequent whitespace-only cleanup in that fragment. Teaching counts are unchanged. All 792 active core review-page identities have now been rebound to current hashes with exact old source/ledger archives; pending review states and mapping evidence are preserved. Final core strict builds and browser checks pass; each configured battery fails only D6 (EFL 611, FLE 1,342 and DaF 716 historical-audio findings). All three source/material/archive checkpoints are committed under the verified Git identity. One empty Sources continuation slide in DaF B1 unit 6 is cosmetic; the citations are present on preceding slides.
- The 26-repository inclusion audit found no remaining authored preservation evidence hidden by ignore rules. Narrow exceptions expose EFL/DaF/FLE archives and review records, and the three resource JSON files. These archives and receipts are now retained in the three committed core checkpoints; byte-preserved historical whitespace was kept deliberately. Current authored files pass whitespace checks.
- Hosted Scriptbridge and Scriptlibrary checks succeeded for their recorded immutable product commits. Kit passed 148 local tests and nine clean checks, then its hosted platform run succeeded for commit `85c338fd` ([run 41473214190](https://github.com/boulingua/kit/actions/runs/41473214190)). Curriculum passed 22 tests, self-audit and coverage checks, then its hosted run succeeded for commit `dd10b463` ([run 41474653600](https://github.com/boulingua/curriculum/actions/runs/41474653600)). All 17 noncore course/hub strict builds and configured gate batteries passed locally, and their review branches are pushed and verified. The stronger final browser pass covers 83 pages, whole-page light/dark mode, download hover states and pronunciation pages, with zero accessibility findings, script errors or failed requests. A subsequent additional WCAG 2.1 A tag check is tracked separately. These results do not establish native approval or full-course content coverage. The org candidate contract now passes 22 tests, validates the registered website/hub identity, and records optional draft-build scope. Compatible foundation releases, consumer pins, full coordinated candidate CI and production deployment remain open.

The external evidence root is `.refinement/20261030/`: `reaudit/education-source-refresh-2026-11-02.json`, `reaudit/checkpoint-refresh-2026-11-02.json`, `reaudit/release-evidence-refresh-2026-11-02.json`, `remediation/audio-candidates/final-corpus-receipt.json`, `reaudit/assessment-derivative-final-checks.json`, and `remediation/education-next-milestone/efl-listening-inventory.json`. Repository archives and ledgers preserve the source-level decisions; external staging is not a public release.

## Implementation sequence

1. Repair actual source loss, unsafe student export, standalone CI and analytics
   disagreement. Validate the original adverse examples and independent review.
2. Restore the missing framework scales and complete the canonical teaching
   contract. Preserve descriptor IDs, original lessons, examinations and URLs.
3. Migrate keyed steps, actual exam links and collapsible keys; reconcile teaching
   content against the contract. Author Programme I review tranches, with native
   and pedagogical review recorded separately from drafting.
4. Regenerate classroom files in a separate staging tree, verify actual content,
   inspect rendered samples and publish only with unchanged source hashes. Keep
   original material backups and truthful audio provenance.
5. Prepare compatible immutable foundation versions and consumer pins, run clean
   installation and hosted checks, then release only accepted components.

## Historical implementation evidence — 31 October checkpoint

- Source-based material extraction preserves multiple passages and answer tables,
  complete production tasks and distinct learner/teacher copies. Actual adverse
  lessons have been compiled and text/visual checks completed. Full-corpus staging
  is in progress; this is not a claim that every final download has been replaced.
- Audio parsing preserves formatted speaker turns. Human-recording evidence now
  requires source/permission records and dated review tied to audio/transcript
  hashes. Candidate synthetic audio remains candidate until actual review.
- Kit path tests have self-contained provenance-linked fixtures, plus explicit
  real-course integration mode. Primary material CLI supports safe staging.
- Framework population now includes the missing scales with 29 additive entries;
  all 1,170 original entries remain unchanged. Source comparison, schema and
  coverage checks are distinct from outstanding editorial approval.
- Canonical EQS files, ordered headings and legacy aliases are implemented. All
  396 existing units have a sibling exam, including 60 transferred DaF drafts.
  At this checkpoint the first twelve divergent FLE assessments had received
  substantive repair; the 2 November continuation below supersedes that count.
- A12 now measures actual keyed/rendered structure, exam pointers, preserved
  fragments and canonical content budgets. It reports existing-course deficits
  under the recorded adoption ramp; new courses must meet the contract.
- C9 checks explicit script/domain settings against rendered scripts and actual
  localized notices. Implicit third-party fallback has been removed; existing
  active sites use their stated self-hosted endpoint. Inactive notices agree with
  inactive configuration. Hub completion and licence claims have been corrected.
- Scriptlibrary preserves the last practice alphabet across original-view reloads.
  All 288 PDFs, 36,623 pages and 166,912 ordered narrative paragraphs passed the
  strengthened source/transform checks. Its complete browser matrix passed.
- Scriptbridge packages are deterministic and synchronized byte-for-byte with the
  library copy. Native Chrome permission acceptance remains unobserved because
  the browser access host is unavailable.
- Private assessment derivatives enforce selected answer mode and record actual
  inputs and toolchain. All ten review PDFs were rebuilt and checked. Their
  timing/scoring policy, then-missing French listening stimuli, content corrections
  and intended-use rights were explicit release criteria; see the later derivative below.

## Release boundaries

Task mappings remain proposed until genuine task-level judgment is recorded.
Restored framework text, new lessons, assessment drafts and voice auditions do
not receive invented approvals. Full curricular coverage still needs reviewed
task evidence and substantive missing teaching content. Current content-budget
measurements are recorded rather than weakened.

Programme I covers eleven new courses. The four Programme II courses retain
their accepted re-entry requirements. Text-first delivery is allowed where
documented and pedagogically coherent; it does not retrospectively approve old
audio. Private assessment decisions do not block independent reading products.

No release tag or production deployment is asserted by this progress record.
The final handover must distinguish local checks, hosted results, actual review
records and observed deployed behavior, with exact revisions and artifacts.


## Explicit release dependencies — 31 October 2026

The shared workflow caller now names the same immutable org commit in `uses` and
`org_ref`; `release-pins.json` records the actual historical kit/framework pins.
These historical pins are explicitly not the remediated release. The new org
workflow rejects absent/malformed versions, mismatched source commits and schema
bytes, and nonconforming course manifests; hubs pin dependencies without claiming
course conformance. The coordinated updater prepares exact published foundation
sets, updates consumers/checksums together and retains rollback inputs. Separate
read-only candidate CI can validate immutable pre-release commits without release
tags or deployment rights. Hosted execution and new foundation publication remain
unobserved. See the org `docs/release-pins.md`.

Nineteen organisation tests pass (11 release/rollback,4 candidate,4 workflow).
Real negative probes rejected an unpublished exact tag and an uncommitted
candidate before producing output. The snapshot command records all3 foundation
working trees and20 consumer declarations; its current external receipt is a
local candidate, not a published Git identity.
