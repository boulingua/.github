# Security

boulingua publishes static teaching sites. There is no server, no database, no
user account and no form that accepts input — the attack surface is small by
construction, and it is kept that way deliberately.

## Reporting

Open a [security advisory](https://github.com/boulingua/.github/security/advisories/new)
rather than a public issue. If that is unavailable to you, use the contact
address on <https://boulingua.github.io/website/impressum/>.

Expect an acknowledgement within a week. This is a single-author project, so
please do not expect a same-day response.

## What is in scope

- Anything that would let a third party change what a learner is served.
- A dependency in the build path with a known advisory.
- **A private VG Wort identification code committed to a repository.** These
  are not credentials in the usual sense, but they are the author's statutory
  remuneration and they must never appear in a repo, an issue, a CI log or a
  screenshot. If you find one, report it here rather than opening an issue —
  an issue is public and would republish it. The mark is then retired and
  re-drawn.

## What is not

- Broken links to third-party sites. Reported weekly by the advisory job.
- The absence of a Content Security Policy on GitHub Pages, which does not let
  us set response headers.
- Anything requiring push access to the org, which is the author alone.

## Supply chain

Course repos contain no code. Layouts, scripts and gates arrive from `kit` at a
pinned tag, the curriculum framework likewise, and the only vendored files —
LaTeX styles, fonts and brand marks in `_materials/` — are digest-locked in
`kit.lock` and checked on every build. Fonts are cut from upstream releases we
fetch and record by checksum, and no workflow in this organisation has write
access to any repository.
