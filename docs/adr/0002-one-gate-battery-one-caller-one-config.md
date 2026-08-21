# ADR 0002 — One gate battery in `boulingua/.github`, one 12-line caller, `boulingua.yml` as the only per-course config

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0001 (`kit`), ADR 0003 (URL freeze)

## Context

Every repo carries its own CI, and each one is a different opinion about what a build is. `daf` runs 22 named steps including Pagefind, a JS bundle budget, pa11y and a PDF `/Author` gate. `website` runs **one** real check — a placeholder grep at `deploy.yml:48`. `efl` runs the URL-drift check `_scripts/verify_url_parity.py` at `hugo.yml:128` with `continue-on-error: true`, on the repo carrying 402 registered marks. Nothing is shared, so nothing improves in more than one place at a time.

Two failure modes follow, and both are live.

**Gates that cannot fail.** Nine gate-step suppressions exist across four repos. Three of them sit on the revenue path. `pagegen/.github/workflows/build-deploy.yml:41` runs `scripts/verify_vgwort_coverage.py || true`, which ships the habit into every course instantiated from the template. `daf/vgwort-manifest.csv` is a header-only file and `daf/scripts/verify-vgwort.sh:22-26` prints `verify-vgwort: manifest is empty — passing trivially` and exits 0 — so all 68 of `daf`'s registered marks have been verified by nothing since migration, while the build printed the word "passing". A gate that cannot fail is worse than no gate, because it is quoted as evidence.

**Gates that write.** `fle/.github/workflows/regen-materials.yml:17,55` combined `contents: write` with `git push origin HEAD:main` on a `workflow_dispatch`, running a generator the sibling workflow itself declares retired — one manual trigger away from overwriting 156 branded worksheet PDFs with placeholders and pushing the damage to `main` unattended. It was deleted in Phase 0 on 2026-08-21.

Phase 0 also proved the shape of the remaining work: moving all six Hugo repos off the deprecated `.Site.Data` to `hugo.Data`, and moving all eight workflows onto `actions/setup-go` with `go-version-file: go.mod`, were eight separate edits to eight separate files for one decision each.

Four specifications each proposed their own reusable workflow. Eighteen courses × five `uses:` blocks is 90 call sites to keep in sync.

## Decision

**One battery, one caller, one config.**

1. `boulingua/.github/.github/workflows/` holds `course-build.yml` (`workflow_call`), `link-check.yml`, `kit-drift.yml`, `materials-latex.yml` (opt-in, local-only escape hatch) and `org-audit.yml` (scheduled). Tagged `v1`.

2. Every repo's `build-deploy.yml` is this, byte-identical in all eighteen:

```yaml
name: build-deploy
on: { push: { branches: [main] }, pull_request: , workflow_dispatch: }
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: false }
jobs:
  course:
    uses: boulingua/.github/.github/workflows/course-build.yml@v1
    secrets: inherit
```

**There is no `with:` block.** Everything configurable lives in `boulingua.yml`, read by the reusable workflow itself. That is what makes the caller a constant, and therefore drift-gatable against `kit/templates/deploy.yml`.

3. `boulingua.yml` is the **only** per-course config file, absorbing what the specs split across `materials-profile.yml`, `gates:` flags and `hugo.toml` params: `code`, `kind`, `content_model`, the three frozen `slug:` axes (ADR 0003), `script_tier`, `target_language`, `chrome_language`, `band_default`, `milestone`, `gates:`, `vgwort:`.

4. **`course-build.yml` does not re-implement the battery.** It checks out `kit` and `curriculum` at pinned tags and runs `bin/kit check --ci` — the same entry point an author runs locally.

5. **A gate is blocking or it is written to warn.** `continue-on-error` and `|| true` are prohibited org-wide. A warn gate prints `::warning::`, exits 0, and says so in its own output.

6. **No workflow in this org writes to `main`.** `org-audit.yml` greps every repo's workflows for `contents: write`, `git push`, `peter-evans/create-pull-request` and `stefanzweifel/git-auto-commit-action`, and fails the audit on any hit.

## Consequences

- "If it passes locally it passes in CI" becomes true rather than aspirational, because CI runs exactly `bin/kit check`. The property is tested: a drift test in `kit` CI asserts no gate is reachable from one entry point and not the other.
- A gate improvement lands once and reaches eighteen repos. `daf`'s four best gates are promoted upstream rather than `daf` being downgraded to a leaner template; `daf/.github/workflows/hugo.yml` shrinks to the 12-line caller with no gate logic left in it.
- The Phase 0 deletion of `regen-materials.yml` becomes a defect class that cannot recur, instead of a one-off fix.
- **Cost:** `kit`'s CLI is now on the critical path for every gate in the org. No gate can be switched blocking before its verb exists and has its own acceptance test.
- **Cost:** a bug in `course-build.yml@v1` is eighteen red repos at once. Mitigated by tag discipline — `v1` is a moving tag advanced only after the change is green on `kit/example` and on `daf` — and by the fact that eighteen identical red builds are diagnosable, where eighteen different ones are not.
- **Cost:** the escape hatch is deliberately narrow. `materials-latex.yml` is opt-in and local-only; a course needing something the battery does not offer files it as a gate register defect, not as a local script.

## Alternatives considered

**Per-repo workflows with a shared checklist.** Rejected. That is the status quo. The checklist exists today in prose and produced a nine-suppression census, one repo with 22 gates and another with one.

**Composite actions instead of a reusable workflow.** Rejected. A composite action still requires each repo to write and maintain the job scaffolding — runner, permissions, concurrency, checkout order — which is precisely the surface that drifted. The reusable workflow moves the whole job body upstream and leaves twelve lines that a byte-comparison can police.

**Several reusable workflows, one per concern (design, EQS, materials, curriculum).** Rejected, and this is the resolution of four competing specs. Five `uses:` blocks in eighteen repos is 90 call sites; `course-build.yml` sequences the four stages internally instead. Its dependency footprint stays `pip install pyyaml pypdf pymupdf fonttools` plus Hugo and Go — no TeX Live, no LibreOffice, no Piper on the deploy path.

**Keep configuration in `with:` inputs.** Rejected. Inputs make the caller vary per repo, which removes the one property that makes drift detectable at all.
