# Coherent foundation and consumer releases

The remediated suite uses the v2 organisation and kit contracts. A successful local build with a
workspace override does not publish its dependencies or establish hosted CI.
Unpromoted `release-pins.json` files explicitly retain a **historical** set.
They are evidence of old dependencies, not closure of the new release criteria.

The historical curriculum `v1.2.0` tag resolves to
`af0b66177c450c6f07a2b7a4f83875d6315fd666`, whose `VERSION` is `1.1.0` and which
does not contain `schema/conformance.schema.json`. Do not relabel or move that
tag. Publish the corrected framework as a new exact version with matching
`VERSION`, reviewed schema and source content.

The v2 kit module is `github.com/boulingua/kit/v2`. Promotion updates both
`go.mod` and the Hugo module import; the major suffix must match the exact
version in the release lock. Existing v1 tags and imports remain historical.
Framework 1.3.0 adds the conformance schema with an aligned `VERSION`.
These foundation releases do not approve course audio or native-language review.

## Contract and local candidate record

Every shared caller supplies the same immutable org commit in `uses`,
`with.org_ref` and its explicit release lock. Kit and curriculum checkout commits
come from that lock. The validator requires exact numeric SemVer declarations,
matching checked-out commits/tags, the actual curriculum `VERSION`, an exact
schema digest and a valid course conformance manifest. Hubs explicitly pin the
framework dependency without claiming course conformance. Missing course
manifests, malformed versions, unknown consumer roles and historical sets fail.

From a directory containing the sibling checkouts `.github`, `kit`,
`curriculum` and consumers, with Python3.12, Git, Go (at the kit's declared floor),
PyYAML6.0.3 and jsonschema4.26.0 installed:

```sh
python .github/scripts/update_release_pins.py snapshot . \
  --output ../release-candidate-inputs.json
python -m unittest discover -s .github/tests -v
python kit/scripts/test_battery_drift.py
```

The snapshot hashes the actual foundation working-tree files and consumer pin
surfaces. Regenerate it after further source edits. It explicitly records local
candidate status and does not manufacture an immutable commit or approved tag.
Run each consumer's normal build/battery with the candidate kit workspace and
explicit curriculum/org owner roots; retain failures instead of presenting old
published modules as validation of new code.

## Hosted candidate validation before release tags

`candidate-check.yml` is a separate workflow with only `contents: read`, no
deployment job/environment, and no Pages/token-write permission. It accepts
exact course, kit and curriculum commits; the organisation input is the exact
executing workflow commit. It uses the real candidate framework schema and a
Hugo workspace pointing at the checked-out candidate kit, then runs the normal
build and entire gate battery. It does not require release tags or promote the
historical production locks. Any outstanding D6/content gate still fails.
The optional `include_drafts` boolean is recorded in the input and source
receipts and defaults to false. Select it for unpublished teaching tranches
whose actual lessons must be reviewed; this adds `--drafts` to the build and
does not grant deployment. Pronunciation pages participate in the browser checks.

After reviewed candidate commits have been pushed under existing authorization,
prepare remotely available immutable inputs:

```sh
python .github/scripts/update_release_pins.py candidate-inputs . --course efl \
  --output .github/.github/candidate-run.json
```

For a Programme I draft tranche, use the same command with its course code and
`--drafts`. Prepare the file in an isolated candidate-CI worktree after the
reviewed foundation and course trees are clean and remotely available.

Commit that small input file on the organisation's `candidate-ci/REVIEW_NAME`
branch. A subsequently authorized push triggers the read-only candidate workflow
even before the workflow is registered on the default branch. There is no
self-referential org hash in the file: GitHub supplies the actual workflow SHA
to the resolved evidence manifest. The checker verifies all four real checkouts,
clean source state, consumer identity and actual framework version/schema.

Once manual dispatch is available, the same workflow accepts `course`,
`course_commit`, `kit_commit`, `curriculum_commit` and `include_drafts` inputs against the chosen
candidate workflow branch. Repeat for each applicable consumer. Download its
candidate inputs, source receipt and build artifact; record the actual hosted
run URL and full gate result. The completed review campaign is recorded in
[the 2 November verification](release-readiness-2026-11-02.md); it does not
publish the historical production locks or create new release tags.

The permissions and workflow context follow GitHub's
[workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
and [workflow context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
contracts. The production workflow below remains strict about published pins.

## Publish and promote the approved set

Select new release versions from the final reviewed changes. The uppercase tag
arguments below are placeholders for those **approved, already published** exact
SemVer tags; they are not claims that a tag currently exists.

1. Finish and approve the framework and organisation workflow. Verify sole Git
   identity, inspect outgoing commits, then publish their new annotated exact
   tags only under the existing publication authorization. Retain old tags.
2. Align the candidate kit caller with the actual published org commit before
   publishing the kit:

   ```sh
   python .github/scripts/update_release_pins.py align-caller kit \
     --org-ref APPROVED_ORG_TAG
   python .github/scripts/update_release_pins.py align-caller kit \
     --org-ref APPROVED_ORG_TAG --write
   ```

   Review/test that kit revision and publish its approved exact annotated tag.
3. Prepare the exact set and inspect the proposed consumer changes:

   ```sh
   python .github/scripts/update_release_pins.py prepare \
     --org-ref APPROVED_ORG_TAG --kit-ref APPROVED_KIT_TAG \
     --curriculum-ref APPROVED_CURRICULUM_TAG --output ../published-foundations.json
   python .github/scripts/update_release_pins.py apply . \
     ../published-foundations.json --receipt ../consumer-pin-plan.json
   python .github/scripts/update_release_pins.py apply . \
     ../published-foundations.json --write --receipt ../consumer-pin-apply.json
   ```

`prepare` reads the published trees, checks their identities/contracts, and gets
Go module checksums whose reported origin matches the published kit commit.
`apply` revalidates the complete published set before any writes. It updates all
20 shared caller/lock sets and framework declarations, all21 kit module
consumers and their Go sums, and the kit caller template. It preserves unrelated
Go sums and course content, and saves exact rollback inputs before changing
files. It creates no commits/tags and pushes/deploys nothing. Re-sync the kit's
vendored `_materials` surface through `kit sync`, inspecting changes separately;
that preservation-aware operation must not be replaced by writing new hashes
over unexplained local differences.

The kit cannot embed its own future commit hash in its published source. New
courses therefore use the separately prepared manifest:

```sh
python kit/scripts/new_course.py COURSE_CODE --into ../new-course \
  --release-manifest ../published-foundations.json
```

Omitting that flag intentionally uses the retained historical development
baseline. Such a scaffold is not a published release. The shared caller remains
byte-identical; every release-lock identity comes from the prepared manifest.

## Hosted verification and recovery

Build consumers without a local unpublished workspace override and run the full
battery against the recorded released foundations. Open the coordinated
consumer changes for review. Pull-request runs publish nothing. Capture actual
hosted run URLs/results and inspect the built artifacts; a prepared workflow is
not an observed hosted pass. Main updates currently deploy on success, so merge
only consumers whose educational, source-rights, audio, URL and remaining
release criteria are satisfied under existing authorization.

For local pin rollback, dry-run first. The tool refuses to overwrite any later
author edit and verifies every backup digest before restoring anything:

```sh
python .github/scripts/update_release_pins.py rollback . ../consumer-pin-apply.json
python .github/scripts/update_release_pins.py rollback . ../consumer-pin-apply.json --write
```

This restores local files only. An actual deployment rollback requires a reviewed
revert/rebuild of the last approved recorded dependency/artifact set, with a
fresh hosted run and observed deployment. Do not reset shared history or move
an immutable tag. Candidate CI has run against exact review commits. No new foundation release
or deployment rollback has been performed during this preparation.
