# Coordinated release candidate — 30 October 2026

The refinement branches are a matching local candidate. Existing public tags,
consumer module pins and production deployments have not been moved. Do not
merge the new reusable workflow into a moving release tag while consumers
still resolve an older kit: its package manifest, build entry point, browser
runner and gate registry must be from the same compatible release.

## Acceptance before publication

| Component | Required evidence | Current limit |
|---|---|---|
| Kit and products | Clean dependency install, regression/build/browser checks, reviewed diffs and package contents | Locally exercised; hosted candidate CI unobserved |
| Organisation workflow | Matching kit checkout used both by Hugo and gates; permissions and failure propagation checked | Local YAML/contract audit passed; no hosted run |
| Curriculum | Schema, resolver, source completeness and coverage checks | Two confirmed source omissions; self-audit must fail |
| Established courses | Build/browser/download checks, URL/mark preservation, approved mappings and recording provenance | Audio D6 failures and educational review remain |
| Development courses | Buildable honest shell, followed by reviewed lessons and evidence matching target scope | Shell checks passed; no authored teaching release |
| Archived generators | Preserve history and point to maintained successor | No unarchiving or historical rewrite planned |

## Release order

1. Resolve the framework omissions with reviewed additive statements; verify
   source ordinals, levels, crosswalk, coverage and the resolver. Decide its new
   immutable version and update `VERSION` consistently with the release tag.
2. Review and release the kit's tested code at a new immutable version. Decide
   whether the A21 adoption milestone is included; if using v1.23.0, make the
   template declaration requirement blocking as specified by that milestone.
3. Publish the organisation workflow as an immutable **new major workflow
   tag**, for example `v2`. Set its `org_ref` default to that same released
   revision. Keep the existing `v1` release available to old consumers.
4. In one coordinated consumer change, update the kit version in `go.mod` and
   `go.sum`, `curriculum.yml`/framework version where applicable, the shared
   `kit/templates/deploy.yml` caller and all course/hub callers to the new
   workflow tag. Re-sync `_materials` and review each digest change.
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
