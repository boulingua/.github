# Release readiness — 2 November 2026

The complete teaching suite is not ready for release. The engineering candidate
is verified and available on `refine/2026-10-30` in all 26 active repositories;
the four archived predecessors remain preserved. Substantial teaching work and
genuine review remain. No main merge, release tag or deployment was performed.

## Observed verification

- Kit: 163 tests and all nine fresh-source platform commands pass, with
  [hosted success at 3642629](https://github.com/boulingua/kit/actions/runs/41482197367).
- Organisation: 35 tests pass in a standalone source copy and in each final
  hosted consumer run. Runtime identity follows declared modules, site roles,
  origins and publication paths. Explicit overrides and exact temporary copies
  do not waive fork or counting-mark protection.
- Curriculum: 22 tests, source self-audit and coverage checks pass at
  [dd10b463](https://github.com/boulingua/curriculum/actions/runs/41474653600).
  The 29 restored entries and course mappings still need real editorial review.
- All 20 shared consumers build in clean hosted checkouts. Their 98 representative
  browser pages pass WCAG 2/2.1 A/AA automation, light/dark, downloads, keyboard,
  mobile and available pronunciation journeys. Seventeen batteries pass; the
  three core batteries fail only D6. These are representative checks, not an
  accessibility certification or approval of the teaching content.
- Scriptbridge passes [e376f267](https://github.com/boulingua/scriptbridge/actions/runs/41478341267).
  Native Chrome permission/popup acceptance and deliberate distribution remain.
- Scriptlibrary passes [21acdef7](https://github.com/boulingua/scriptlibrary/actions/runs/41480154465):
  288 PDFs, 36,623 pages, 166,912 ordered narrative paragraphs and 288 reader
  combinations. Deployment was skipped. The later `cb068398` change is documentation
  only; original source/PDF/package bytes are unchanged. Its npm audit found zero
  known vulnerabilities in the current lock.

The [machine-readable record](release-verification-2026-11-02.json) binds the
exact course, foundation and workflow revisions. Candidate CI uses the matching
workspace explicitly; it does not claim a newly published foundation release.
Initial resources/website failures are retained in the local evidence and were
closed by the identity repair before the final runs below.

| Consumer | Source commit | Complete battery | Build scope | Hosted evidence |
|---|---|---|---|---|
| afl | c1e0f826 | Pass | Normal build | [run 41482706235](https://github.com/boulingua/.github/actions/runs/41482706235) |
| cfl | ebd1a7f7 | Pass | Normal build | [run 41482750446](https://github.com/boulingua/.github/actions/runs/41482750446) |
| daf | 8cb304da | Blocked: D6 historical audio | Normal build | [run 41482525773](https://github.com/boulingua/.github/actions/runs/41482525773) |
| efl | 70ba0ff1 | Blocked: D6 historical audio | Normal build | [run 41482469316](https://github.com/boulingua/.github/actions/runs/41482469316) |
| ele | 123677d3 | Pass | Drafts included | [run 41482574249](https://github.com/boulingua/.github/actions/runs/41482574249) |
| fle | 0d505b65 | Blocked: D6 historical audio | Normal build | [run 41482498651](https://github.com/boulingua/.github/actions/runs/41482498651) |
| gfl | 5ecac11b | Pass | Drafts included | [run 41482664935](https://github.com/boulingua/.github/actions/runs/41482664935) |
| ils | ed3d4bde | Pass | Drafts included | [run 41482590409](https://github.com/boulingua/.github/actions/runs/41482590409) |
| jfl | 39cea801 | Pass | Normal build | [run 41482737027](https://github.com/boulingua/.github/actions/runs/41482737027) |
| lle | 05c0023b | Pass | Drafts included | [run 41482651780](https://github.com/boulingua/.github/actions/runs/41482651780) |
| nsf | 72e569ad | Pass | Drafts included | [run 41482541566](https://github.com/boulingua/.github/actions/runs/41482541566) |
| nvt | d4a77d12 | Pass | Drafts included | [run 41482557180](https://github.com/boulingua/.github/actions/runs/41482557180) |
| pfa | f59c0172 | Pass | Normal build | [run 41482719865](https://github.com/boulingua/.github/actions/runs/41482719865) |
| pfl | e2bb822f | Pass | Drafts included | [run 41482620489](https://github.com/boulingua/.github/actions/runs/41482620489) |
| ple | 2c6c62ed | Pass | Drafts included | [run 41482605620](https://github.com/boulingua/.github/actions/runs/41482605620) |
| ressources | 3b5fc72f | Pass | Normal build | [run 41482432792](https://github.com/boulingua/.github/actions/runs/41482432792) |
| rki | 450be44c | Pass | Drafts included | [run 41482691409](https://github.com/boulingua/.github/actions/runs/41482691409) |
| tfl | 2f11b789 | Pass | Drafts included | [run 41482636365](https://github.com/boulingua/.github/actions/runs/41482636365) |
| ufl | 4eb2f43f | Pass | Drafts included | [run 41482678165](https://github.com/boulingua/.github/actions/runs/41482678165) |
| website | dc64fb0c | Pass | Normal build | [run 41482445137](https://github.com/boulingua/.github/actions/runs/41482445137) |

## Materials and remaining teaching work

All 396 core units now have 1,188 checked PDFs (9,420 pages) and matching thumbnails.
The 153 supplementary PDFs comprise 120 DaF assessment copies and 33 Programme I
classroom files (405 pages). Source/archive receipts and committed artifact bytes
were verified. The separate Hello World pilot adds five review PDFs / 29 pages;
it remains outside the live course. Minor documented pagination issues remain.

All 1,064 separately staged voice clips pass input/provenance and full decode
checks, but every listening-review record remains pending. They have not replaced
the historical production recordings. The private French derivative supplies four
PDFs / 35 pages and a 122.13-second listening candidate, with eight local tests;
native review, timing/grading policy and intended-use rights remain open.

Fresh strict rendered EQS checks still find 302 short units, 227 short assessments
and 188 missing durations, affecting 380 distinct units. Twelve null maxima belong
to intentional rehearsals needing an accepted assessment-scope decision. EFL also
has 145 learner-visible listening scripts and five incomplete standalone stimuli.
These require source-specific repairs, not merely signatures or additional prose.
See the [authoring milestone](education-next-milestone-2026-11-02.md).

Task mappings remain proposed and full reviewed coverage is unachieved. Eleven
Programme I courses have first A1/pronunciation/assessment tranches, not complete
A1 curricula. Four Programme II courses remain deferred under their re-entry
conditions. The unchanged D6 failures are EFL 611, FLE 1,342 and DaF 716 findings.

## First use and next release action

The retained local workspace is `.refinement/20261030` under the Boulingua root.
It supplies Python 3.12, Node 22, Hugo extended 0.159.2 and Go 1.26.1. From that
workspace, `./preview.sh 8765` serves the checked core sites at `/efl/`, `/fle/`
and `/daf/`. Its first-use path was tested. To review the voice corpus:

```sh
tools/py312env/bin/python -m http.server 8774 --bind 127.0.0.1 \
  --directory remediation/audio-candidates
```

Open `http://127.0.0.1:8774/`. The local `reaudit/RELEASE_READINESS_2026-11-02.md`
links the pilot PDFs, source/evidence packets, exact rebuild commands and each
repository's README. The per-repository READMEs provide installation prerequisites
and candidate build commands; use the matching revisions recorded above.

Review the bounded lesson pilot, actual timing and assessment scope with a
qualified teacher/native reviewer, and conduct the three course-voice auditions.
Continue substantive authoring in the identified cohorts. Regenerate/review the
affected PDFs and clips after accepted source changes, preserving previous bytes.
Only then prepare the accepted scope's compatible immutable foundations and
consumer pins through [the release procedure](release-pins.md), verify the
published dependency set, and perform the authorised release/live smoke checks.
No approval or deployment is inferred from this record.
