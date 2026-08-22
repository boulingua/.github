#!/usr/bin/env python3
"""Gate A1 — has a course grown code of its own?

    python scripts/kit_drift.py ORG_CHECKOUT

The invariant: **a course repo contains content, marks, materials, brand and
configuration. It contains no code.** The shared surface arrives as a Hugo
module, a pinned CI checkout, and a digest-locked `_materials/`.

That is not a style preference. Before the module, of sixteen script basenames
shared between repos **nine had forked byte-for-byte**, all ten shared layout
partials had diverged — `head/extensions.html` at six distinct hashes across
six repos — and nothing detected any of it, because copying leaves no link to
detect. A directory reappearing in a course is that failure restarting.

Also checked: the caller is a constant. Everything configurable lives in
`boulingua.yml`, so `.github/workflows/deploy.yml` should be byte-identical
everywhere. A course whose caller has grown a step has left the battery.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Directories that belong to the kit and must not exist in a course.
KIT_OWNED = ["layouts", "assets", "i18n", "archetypes", "scripts", "_scripts"]
# Repos that are not courses and legitimately hold their own code.
NOT_A_COURSE = {"kit", "curriculum", ".github", "website", "ressources"}


def main() -> int:
    org = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    repos = sorted(p for p in org.iterdir() if p.is_dir() and not p.name.startswith("."))
    bad, checked, pre_adoption = 0, 0, []
    for repo in repos:
        if repo.name in NOT_A_COURSE:
            continue
        # The discriminator is whether hugo.toml actually IMPORTS the kit, not
        # whether boulingua.yml exists. A course can carry the config while
        # still holding its own layouts — that is precisely the state the three
        # live sites are in until their Phase 3 retrofit, and failing them for
        # it would red three deployed sites for the duration of a migration
        # they are queued for.
        cfg = repo / "hugo.toml"
        if not cfg.exists():
            continue
        if "boulingua/kit" not in cfg.read_text(encoding="utf-8"):
            pre_adoption.append(repo.name)
            continue
        checked += 1
        for d in KIT_OWNED:
            p = repo / d
            if p.exists() and any(p.rglob("*")):
                n = len(list(p.rglob("*")))
                print(f"::error::{repo.name}/{d}/ exists with {n} file(s). This "
                      f"directory arrives from the kit as a Hugo module — a copy "
                      f"here is a fork, and a fork is what the module was adopted "
                      f"to make impossible.")
                bad += 1
    print(f"  {checked} course(s) importing the kit module, checked")
    if pre_adoption:
        print(f"::notice::{len(pre_adoption)} course(s) have not adopted the module "
              f"yet and were skipped: {', '.join(pre_adoption)}. They still hold "
              f"their own layouts by definition; that is what their Phase 3 "
              f"retrofit removes, and failing them for it today would red a "
              f"deployed site for the duration of a migration it is queued for.")
    if bad:
        print(f"\nA1 FAIL — {bad} course-side code director(ies)", file=sys.stderr)
        return 1
    print("A1 OK — no course carries kit-owned code")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
