# ADR 0016 — SemVer for `kit` and `curriculum`, CalVer for courses, `main` is the only long-lived branch

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0001 (`kit` is a Hugo module), ADR 0002 (the shared gate battery), ADR 0009 (materials committed), ADR 0015 (VG Wort operations)

## Context

The org has 26 repositories and, today, five tags in total. Verified: `efl v0.1.0`, `fle v0.1.0`, `daf v0.1.0` and `v1.0.0`, `ressources v0.1.0`. `website`, `curriculum`, `pagegen`, `slidegen`, `sheetgen` and `audiogen` carry **no tags at all**.

That matters in two directions. Courses will consume `kit` and `curriculum` as pinned dependencies, so those two need a version scheme that says whether an upgrade requires course edits. And the three live courses are about to be retrofitted, so each needs a rollback point that actually corresponds to a deployable site. `daf` has one: `v1.0.0` predates the retrofit. `efl` does not — its only tag, `v0.1.0`, was cut before the Quarto→Hugo migration of 2026-05-06, and a site that has since changed content model, URL scheme and build system cannot be rolled back to it.

Branch state is verified and inconsistent with any policy at all. `fle` carries six `phase4/*` branches holding **151 unique commits** — `phase4/kl08e` contains the other five as ancestors, so the union is 151, not the 416 a naive sum gives — with **no common ancestor with `main`** (`git merge-base` is empty for every one), tips dated 2026-04-29 to 2026-05-04. `efl` carries `migration/hugo-coder` with **0** commits not already on `main`. `ressources` carries `add-prompt-docs` with 4.

## Decision

**`kit`, `curriculum` and `boulingua/.github` use SemVer. Courses use CalVer. `main` is the only long-lived branch anywhere in the org.**

**SemVer, for the shared repositories.** MAJOR = a change that requires course edits. MINOR = additive. PATCH = fixes. Moving tags `v1` and `v1.2` are maintained so courses can pin `@v1` and receive compatible changes without a bump per course; `org-audit.yml` reports how far behind each course is against the exact tag.

**CalVer `vYYYY.MM`, for the courses.** A course tag is cut when a level or a track is content-complete — not on a calendar, and not on a deploy. Release notes name the units added, the marks registered, and the `kit` and `curriculum` versions in force.

**Every tag is annotated.** A release is a signed statement about the corpus, so it carries a message rather than being a bare pointer.

**Rollback tags are part of the policy, not an afterthought.** Before a retrofit branch touches anything destructive, the repository is tagged and the tag names the pinned toolchain and the `kit`/`curriculum` pins in force:

- `efl` is tagged `v2026.08-preflip` at the end of its content migration, **before a single `.gitignore` line is deleted** in the materials-commit flip.
- `fle` is tagged before its mark migration moves 349 front-matter marks into `vgwort/marks.yaml`.
- `ressources` is tagged before its retrofit.

`daf v1.0.0` is retained and additionally aliased `v2026.07`, so the CalVer series is continuous without rewriting a tag anyone may already have fetched. Every other repository receives its first tag at the end of Phase 3, so "green under the shared battery" has a name.

**Branch policy.** `main` is protected, with linear history, no force-push, and one required check — the `course` job from the shared battery. **No workflow in this org writes to `main`.** Work branches are `fix/…`, `feat/…` or `content/…`, deleted on merge, and none older than 90 days.

**Cleanup preserves everything.** A branch that carries commits `main` does not have is tagged `archive/<repo>-<branch>` and pushed before deletion. `fle`'s six `phase4/*` branches are archived that way — all six tips tagged, not just `phase4/kl08e`, because the tag names are the only record of which tranche each belonged to and that is the part `main` cannot reconstruct. `efl`'s `migration/hugo-coder` is deleted outright: an archive tag would preserve nothing `main` does not already contain. `ressources/add-prompt-docs` is archived and deleted.

## Consequences

- The `fle` archive is safe on the evidence: **zero `vgwort` occurrences under `content/` on any of the six branches**, so no registered mark lives only there. A tag costs about 40 bytes and keeps all 151 commits reachable permanently — the same principle that governs marks under ADR 0015, that nothing which took work to produce disappears because it was tidied.
- **The materials-commit flip gets an explicit abort criterion**, which it previously lacked. Generation, `.gitignore` deletion and `git add` are one commit precisely so that reverting one SHA restores the previous state; deleting the CI generator is a second commit that is never pushed until the download and PDF gates are green on the first. The flip is aborted and the branch discarded rather than fixed forward if any produced PDF carries a `.notdef` or U+FFFD, if any is missing `/Author` or `/Title`, or if a local `bin/kit materials` run is not byte-stable across two consecutive invocations. Aborting costs one local generation run; landing a bad batch costs a ~20 MB revert plus a second ~20 MB commit in a repository whose history is otherwise text.
- **If the materials commit lands and the batch is bad, the deployed site is unaffected**, because the CI generator has not yet been removed and is still authoritative. That ordering is the reason the two commits may not be exchanged.
- A course pinning `@v1` picks up compatible `kit` changes without action. A MAJOR bump appears in `org-audit`'s weekly issue as work, not as drift, and the course adopts it on its own schedule.
- CalVer tells a teacher what they are looking at. `efl v2026.09` is a statement about when the corpus was current; `efl v3.2.1` would be a statement about an API that a course does not have.

## Alternatives considered

**SemVer for courses too.** Rejected. A course has no public API, so MAJOR/MINOR/PATCH has nothing to measure. The only question a reader asks of a course release is how recent it is, which is exactly what CalVer answers.

**CalVer for `kit` and `curriculum`.** Rejected. Courses pin them, and a pin needs to encode compatibility. `kit v2026.09` does not tell a course whether upgrading requires editing 360 pages; `kit v2.0.0` does.

**A `develop` branch, or release branches per course.** Rejected. This is a single-author org with one deploy target per repository. A second long-lived branch buys a staging concept nobody uses and costs a merge topology that a solo author maintains by hand.

**Tag only on deploy.** Rejected. Deploys happen on every content push. A tag that fires on every push is a log, not a release, and the release notes — units added, marks registered, dependency versions — only make sense at a content-complete boundary.

**Delete the stale branches outright.** Rejected for `fle` and `ressources`. 151 commits with no ancestor in `main` are unrecoverable once the branch pointer is gone, and the cost of keeping them is a tag.

**Keep a `continue-on-error` escape on the required check while the retrofit runs.** Rejected. There are already nine suppressed checks across four repositories, three of them on the revenue path; adding a tenth to make a branch policy comfortable is how a battery becomes advisory.
