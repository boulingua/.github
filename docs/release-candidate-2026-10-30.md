# Coordinated release candidate — updated 2 November 2026

The refinement branches are a coordinated review candidate. Existing public tags,
consumer module pins and production deployments have not been moved. Do not
merge the new reusable workflow into a moving release tag while consumers
still resolve an older kit: its package manifest, build entry point, browser
runner and gate registry must be from the same compatible release.

## Acceptance before publication

| Component | Required evidence | Current limit |
|---|---|---|
| Kit and products | Clean dependency install, regression/build/browser checks, reviewed diffs and package contents | Exact hosted kit, curriculum and product checkpoints are recorded in the remediation log; final follow-up checks remain separately bound to their commits |
| Organisation workflow | Matching kit checkout used both by Hugo and gates; permissions and failure propagation checked | 22 local contract tests pass; read-only immutable candidate workflow prepared; hosted execution pending |
| Curriculum | Schema, resolver, source completeness and coverage checks | 1,199 entries; all 1,170 original entries preserved; 29 restored entries await editorial approval; task mappings remain proposed |
| Established courses | Build/browser/download checks, URL/mark preservation, approved mappings and recording provenance | All three final builds/browser runs pass; 1,188 unit PDFs verified; D6 audio failures, listening validity and substantive teaching deficits remain |
| Development courses | Reviewed lessons and evidence matching the accepted target scope | Eleven first A1 unit/assessment/pronunciation tranches and 33 PDFs prepared; native/teaching review and remaining progression pending; four courses explicitly deferred |
| Archived generators | Preserve history and point to maintained successor | No unarchiving or historical rewrite planned |

## Release order

1. Complete editorial review of the restored framework and select its new
   immutable version. Keep `VERSION` and the approved annotated tag consistent.
   Complete the organisation workflow checks and publish its approved exact tag.
2. Align `kit/templates/deploy.yml` with that actual published org commit using
   the [release-pin procedure](release-pins.md). Review and release the resulting
   kit at a new immutable version. Apply the agreed A21 adoption milestone;
   do not silently change the contract while selecting a version.
3. Prepare and independently verify the exact published foundation manifest.
   The existing historical pins are not the remediated release; retain old tags.
4. Apply that manifest across all consumer callers, locks, module checksums and
   framework declarations with rollback inputs. Re-sync `_materials` and review
   each digest change. The executable procedure controls the exact order.
5. Build each consumer with no unpublished local workspace override. Run the
   full battery using the released framework/org dependencies. Confirm hosted
   results and inspect outgoing commits, identities and package contents.
6. Deploy only consumers whose release criteria are satisfied. Development
   shells must remain visibly in development. Do not suppress D6, promote
   proposed mappings, or equate a published shell with a finished course.

These steps name future version decisions explicitly; no nonexistent tag is
presented as an installable release. The local receipt records exact branch
revisions so review does not depend on a moving branch name.

## Operational boundary and recovery

Sites are static GitHub Pages artifacts; no application database or migration
is introduced. Source, committed materials and lockfiles are the recovery
inputs. Keep the previous approved artifact/dependency set available. For a
bad deployment, rebuild and redeploy that recorded set; do not reset shared
history or move an immutable tag. An actual restore/deployment has not been
performed during this refinement.

The scheduled link workflow now enumerates the public suite inventory, not
only this organisation repository. It reports external outages separately from
blocking local integrity checks. Its future scheduled execution is unobserved.

Link-check flags were checked against the [official lychee CLI reference](https://lychee.cli.rs/guides/cli/). The scheduled job checks HTTP(S) links; built local paths are checked separately by C16.


Current evidence and remaining work are maintained in
[the remediation record](remediation-2026-10-31.md) and the
[teaching-content milestone](education-next-milestone-2026-11-02.md).
Record new hosted results against exact commits; a pass for an earlier checkpoint
does not verify later edits. Historical pins are not the remediated release.
