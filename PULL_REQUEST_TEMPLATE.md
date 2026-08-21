<!--
boulingua is single-author OER. Pull requests are generally not accepted; errors are filed as
issues. If this PR is one of the rare exceptions, every box below has to be ticked honestly.
An unticked box is not a blocker to be argued with — it is the reason the PR is closed.
Read CONTRIBUTING.md first.
-->

## What this changes

<!-- One paragraph. What, and why now. -->

## Scope

- Repositories touched:
- Issue this closes:
- ADR number, if this decision touches a URL, a licence, a VG Wort rule or `kit`'s public surface:

## Checklist

- [ ] **Gates pass locally.** `bin/kit check` is green on my machine. Nothing here was debugged through CI.
- [ ] **No URL and no slug changed.** No row of `vgwort/url-lock.csv` is touched by this diff.
- [ ] If a URL genuinely had to change: the **re-key protocol** was followed in full — gate A3 failure acknowledged, `aliases:` published, a **new** code drawn, bound and registered, the old code moved to ledger state `retired` with a reason, `url-lock.csv` updated and the old row moved to `url-lock.retired.csv`. An ADR exists if more than one page is affected.
- [ ] **No `slug:` line removed or altered in `fle`.** Those 312 front-matter keys are the URL, not a restatement of the filename.
- [ ] **No leaf-bundle directory renamed in `efl`**, and **no content file renamed in `daf`**. In those two courses the directory name and the filename respectively *are* the URL.
- [ ] **No kit-owned file modified** without a `kit-overrides.yml` entry **and** an ADR.
- [ ] **No private VG Wort identification code in the diff** — not in code, comments, fixtures, test data, screenshots or the commit message. Only the public 32-hex code may appear anywhere in a repository.
- [ ] **No new `continue-on-error` and no `|| true` on a gate.** A gate is blocking, or it is written to warn and says so in its own output. There is no third state.
- [ ] **No workflow writes to `main`.** No `permissions: contents: write`, no `git push`, no commit action outside the Pages deploy job.
- [ ] **No literal version pin.** Go comes from `go-version-file: go.mod`; Hugo is the org-pinned 0.159.2 extended.
- [ ] Licensing understood: this contribution is offered under **MIT** for code and **CC BY-SA 4.0** for content.

## Verification

<!--
Paste the commands you ran and their output — the gate IDs that ran, the build, the artefact checks.
"CI is green" is not a verification; CI has been green while a URL-drift check was suppressed.
-->
