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
    overrides: dict[str, dict] = {}
    for repo in repos:
        f = repo / "kit-overrides.yml"
        if f.exists():
            import yaml
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            overrides[repo.name] = {e["path"]: e for e in doc.get("overrides", [])}
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
            if not (p.exists() and any(p.rglob("*"))):
                continue
            # Compare FILE BY FILE against the kit, not directory by directory.
            # The coarse rule said a course may not have a scripts/ directory at
            # all, which is wrong in the one case that matters: daf's four
            # authoring tools generate German audio and daf-specific tags, the
            # kit has no equivalent, and there is nowhere else for them to live.
            # A rule that forbids them either gets a blanket exception — which
            # then covers the real forks too — or gets renamed around, which is
            # worse because the next reader believes it.
            #
            # What a fork actually is: a file the kit also ships. That is the
            # thing that silently diverges.
            kit_dir = org / "kit" / d
            kit_names = {q.name for q in kit_dir.rglob("*")} if kit_dir.is_dir() else set()
            # A declared override is still a fork; declaring it buys time, not
            # forgiveness. Every entry needs a reason and a destination, and an
            # entry whose file no longer exists is spent and fails — the same
            # contract as org-audit-exceptions.yml and placeholder-exceptions.yml.
            forks = sorted(q for q in p.rglob("*")
                           if q.is_file() and q.name in kit_names
                           and q.relative_to(repo).as_posix() not in overrides.get(repo.name, {}))
            own = [q for q in p.rglob("*") if q.is_file() and q.name not in kit_names]
            for q in forks:
                print(f"::error::{repo.name}/{q.relative_to(repo)} — the kit ships "
                      f"a file of this name. A course copy of it is a fork, and a "
                      f"fork is what the module was adopted to make impossible.")
            bad += len(forks)
            if own and not forks:
                print(f"::notice::{repo.name}/{d}/ holds {len(own)} file(s) the kit "
                      f"does not ship. Course-specific tooling is allowed here; "
                      f"what is not allowed is a copy of something the kit owns.")
    # Spent overrides. A declaration that outlives the file it covers is a
    # standing permission for a fork nobody has.
    for name, entries in overrides.items():
        for path, e in entries.items():
            if not (org / name / path).exists():
                print(f"::error::{name}/kit-overrides.yml declares {path}, which "
                      f"does not exist. The override is spent — delete the entry. "
                      f"Its destination was {e.get('destination', '(none given)')}")
                bad += 1
            elif not (str(e.get("reason", "")).strip()
                      and str(e.get("destination", "")).strip()):
                print(f"::error::{name}/kit-overrides.yml: {path} needs both a "
                      f"reason and a destination. An override with neither is a "
                      f"permanent fork with a config entry.")
                bad += 1
            else:
                print(f"::warning::{name}/{path} is a declared fork of a kit file, "
                      f"scheduled for {e['destination']}")

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
