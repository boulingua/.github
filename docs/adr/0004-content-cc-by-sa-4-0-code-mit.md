# ADR 0004 — Content CC BY-SA 4.0, code MIT, `LICENSE` always means MIT

- **Status:** Accepted, 2026-08-21
- **Deciders:** S. Le Boulanger
- **Related:** ADR 0001 (`kit` ships the canonical legal file set)

## Context

The org states its licensing in six places and they do not agree. The conflict is five-way in kind:

1. `profile/README.md:104-105` — the public promise: **code MIT, content CC BY-SA 4.0**.
2. `efl|fle|daf/LICENSE` — a **content** licence, opening *"© 2026 S. Le Boulanger. Prose licensed under CC BY 4.0."*, with the code licence displaced into `LICENSE-CODE.md`. So in the three repos that matter most, the file named `LICENSE` does not mean what it means anywhere else in the org, and the content grant is **CC BY**, not **CC BY-SA**.
3. `pagegen` — `LICENSE` = MIT plus `LICENSE-CONTENT.md`.
4. `website` and `ressources` — `LICENSE` = MIT plus `LICENSE-content`, a third filename differing only in case and hyphenation; `website`'s is dated `Copyright (c) 2025` against 2026 everywhere else.
5. `curriculum`, `slidegen`, `sheetgen`, `audiogen` and all fifteen scaffolds — plain MIT and no content licence at all. `curriculum/NOTICE.md:38-39` explicitly licenses its 1,170 can-do statements under the repo `LICENSE`, i.e. MIT: a code licence applied to prose.

The sixth statement is the useful one: `pagegen/layouts/_partials/footer.html:10` renders `MIT / CC-BY-SA 4.0` on every page built from the template, contradicting `pagegen`'s own files and independently confirming the target pair.

The copyright holder is split too: `S. Le Boulanger` in `efl`, `fle`, `daf`, `ressources`; `boulingua` in the other eleven-plus repos.

One page also makes a licensing claim that is false in the author's favour. `daf/content/literatur.md:34` states publicly: *"Die Deskriptoren unter `cefr_can_do:` im Front Matter einer Einheit stammen **verbatim** aus dem GER-Begleitband 2020."* Spot-checked against the actual values, these are the author's own formulations. The sentence contradicts `curriculum/NOTICE.md`, and relicensing that page CC BY-SA 4.0 while it stands would purport to sublicense text the page itself attributes to the Council of Europe.

## Decision

**Code MIT. Content CC BY-SA 4.0. `LICENSE` always means MIT, in every repo, no exceptions.**

Reasons, in order:

- It is what the org has already publicly promised, in two independent places.
- **ShareAlike is the mission.** `ressources` runs a CI gate literally named "Block commercial sources". Licensing the corpus CC BY — which permits proprietary enclosure of derivatives — contradicts the gate the author wrote.
- VG Wort's §§ 54 ff. UrhG remuneration right is licence-neutral, so the choice costs nothing on the revenue side.

File naming, binding everywhere: `LICENSE` = MIT; `LICENSE-CONTENT.md` = full CC BY-SA 4.0 with a scope paragraph naming which paths are content; `NOTICE.md` for third-party attributions; `REUSE.toml`; `CITATION.cff`. `LICENSE-CODE.md` and `LICENSE-content` are retired names.

**The change is prospective, not retroactive.** `efl`, `fle` and `daf` move to a *more* restrictive licence. Every version already published under CC BY 4.0 stays perpetually available under CC BY 4.0 to anyone who obtained it. That grant is irrevocable and cannot be withdrawn, and this ADR does not pretend otherwise. Each of the three therefore carries **`LICENSE-HISTORY.md`**, naming the change date, the commit SHA and the last CC BY 4.0 tag.

Scope executed now: `efl`, `fle`, `daf` only — the three repos actively publishing a contradiction, and the only three with a history to preserve. In the same commit as `daf`'s licence change, `daf/content/literatur.md:34` is corrected to: *"Die Formulierungen unter `cefr_can_do:` sind eigene, am GER-Begleitband 2020 orientierte Umsetzungen; die Zuordnung zu den offiziellen Deskriptoren erfolgt über `curriculum.implements`."*

Rollout across the remaining 23 repos — including the deletion of `website|ressources/LICENSE-content`, the `boulingua` → `S. Le Boulanger` copyright normalisation, and moving `curriculum`'s 1,170 statements from MIT to CC BY-SA 4.0 — is carried by the canonical set in `kit/templates/legal/` and enforced by the org licence gate. `bin/kit new` writes the full set at course creation, so no new course inherits this problem.

## Consequences

- One question — "which licence?" — has one answer, and the file that answers it has one name.
- Inbound equals outbound: a contribution is offered under the same pair, stated in `CONTRIBUTING.md`.
- The licence gate blocks a repo missing any file in the set, and blocks a repo shipping a `.woff2` or `.ttf` with no row in the font attribution file.
- **Cost:** downstream reusers of `efl`, `fle` or `daf` content who relied on CC BY's permission to relicense derivatives must, for versions published after the change date, share alike instead. This is a real restriction on real people and it is why `LICENSE-HISTORY.md` exists rather than a silent file swap.
- **Cost:** 23 repos acquire five legal files each. Done by hand now it would be done twice, so it waits for the template plus the gate.

## Alternatives considered

**Keep CC BY 4.0 for content.** Rejected. It permits proprietary enclosure of derivative teaching material, which is the outcome the org's own commercial-source gate exists to prevent, and it contradicts the public promise on the front page.

**Relicense retroactively.** Not available. The CC BY 4.0 grant already made is irrevocable for anyone who obtained a copy under it. An ADR claiming otherwise would be wrong, so the ADR states the limit instead.

**Keep `LICENSE` as the content licence in `efl`/`fle`/`daf` and normalise the org onto that.** Rejected. `LICENSE` is what every tool, forge and scanner reads as the software licence, and eleven repos plus the template already use it that way. Inverting the convention org-wide to match three repos maximises the change and keeps the surprise.

**One combined `LICENSE` file stating both grants.** Rejected. Automated licence detection reads one identifier from that path; a dual-statement file resolves to "other" and the machine-readable promise disappears. Two files, two names, one meaning each.
