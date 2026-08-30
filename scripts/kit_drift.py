#!/usr/bin/env python3
"""Gate A1 — has a course grown code of its own?

    python scripts/kit_drift.py REPO          # one course — the battery's shape
    python scripts/kit_drift.py ORG_CHECKOUT  # every course — org-audit's shape

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

**This took one argument and it was the wrong one.** `kit check` hands every
gate the repo under test; this script read it as an org checkout and iterated
its subdirectories, so `content/`, `static/` and `data/` were the "repos", none
of them imported the kit, and it printed *0 course(s) importing the kit module,
checked · A1 OK*. Green, on every course, having examined nothing. The drift
gate had the drift defect, and it was invisible for as long as the gate register
was aborting before the battery ran at all.

So: one repo is checked as one repo, an org checkout is still iterated, and
**checking nothing is no longer a way to pass**. The kit is located from
`$BLG_KIT` when `kit check` sets it — in CI the kit is at `.kit` inside the
course, not beside it — and from a sibling otherwise.
"""
from __future__ import annotations

import sys
import re
from pathlib import Path

# Directories that belong to the kit and must not exist in a course.
KIT_OWNED = ["layouts", "assets", "i18n", "archetypes", "scripts", "_scripts"]
# Repos that are not courses and legitimately hold their own code.
NOT_A_COURSE = {"kit", "curriculum", ".github", "website", "ressources"}


def is_repo(p: Path) -> bool:
    """A repository, as opposed to an org checkout holding several. Recognised
    by boulingua.yml or hugo.toml — the two files a course always has and a
    checkout root never does."""
    return (p / "boulingua.yml").exists() or (p / "hugo.toml").exists()


def main() -> int:
    import os
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    single = is_repo(target)
    org = target.parent if single else target
    repos = [target] if single else sorted(
        p for p in org.iterdir() if p.is_dir() and not p.name.startswith("."))
    # In CI the kit is checked out INSIDE the course at .kit, so `org / "kit"`
    # is a directory that does not exist and every fork comparison silently
    # compares against an empty set.
    kit_root = Path(os.environ["BLG_KIT"]).resolve() if os.environ.get("BLG_KIT") \
        else org / "kit"
    bad, checked, pre_adoption = 0, 0, []
    # The kit's own newest tag, read from the checkout rather than from a
    # constant — a hardcoded "current version" in a gate is stale by definition.
    latest = None
    if kit_root.is_dir():
        import subprocess
        r = subprocess.run(["git", "tag", "-l", "v*.*.*"], cwd=kit_root,
                           capture_output=True, text=True)
        vs = [tuple(int(x) for x in t[1:].split("."))
              for t in r.stdout.split() if re.fullmatch(r"v\d+\.\d+\.\d+", t)]
        latest = max(vs) if vs else None
    overrides: dict[str, dict] = {}
    for repo in repos:
        f = repo / "kit-overrides.yml"
        if f.exists():
            import yaml
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            overrides[repo.name] = {e["path"]: e for e in doc.get("overrides", [])}
    for repo in repos:
        # The MODULE VERSION check applies to every repo that imports the kit,
        # not only to the ones whose layouts it owns. website and ressources are
        # NOT_A_COURSE for the layouts rule and were skipped entirely — which is
        # how website sat on v1.4.2 while ressources ran v1.7.0 with nothing
        # reporting it.
        cfgp = repo / "hugo.toml"
        if cfgp.exists() and "boulingua/kit" in cfgp.read_text(encoding="utf-8"):
            # The pinned MODULE version, which is a second kind of drift and the
            # one the module itself was supposed to end. `v1` moves, but go.mod
            # pins an exact version, so five courses adopting the kit over five
            # days ended up rendering from five different releases — website on
            # v1.4.2 while ressources was on v1.7.0. Nothing looked wrong: each
            # site built cleanly against a kit that was internally consistent, just
            # not the same one as its siblings.
            #
            # One minor behind is tolerated, because a course should not fail for
            # being a day late. Two is drift.
            gomod = repo / "go.mod"
            if gomod.exists() and latest:
                m = re.search(r"boulingua/kit v(\d+)\.(\d+)\.(\d+)",
                              gomod.read_text(encoding="utf-8"))
                if m:
                    have = tuple(int(x) for x in m.groups())
                    if have[0] != latest[0]:
                        print(f"::error::{repo.name} pins kit v{'.'.join(map(str, have))} "
                              f"against a current major of v{latest[0]} — a major means "
                              f"the course has an edit to make, so this cannot be a "
                              f"silent lag")
                        bad += 1
                    elif latest[1] - have[1] > 1:
                        print(f"::error::{repo.name} pins kit v{'.'.join(map(str, have))}, "
                              f"{latest[1] - have[1]} minors behind v{'.'.join(map(str, latest))}. "
                              f"Courses rendering from different kit releases is the drift "
                              f"the module exists to end.")
                        bad += 1
                    elif have != latest:
                        print(f"::notice::{repo.name} pins kit "
                              f"v{'.'.join(map(str, have))}, current is "
                              f"v{'.'.join(map(str, latest))}")

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

        # THE CALLER IS A CONSTANT. The docstring has claimed this since the
        # reusable workflow landed and nothing enforced it. `kit check --ci` is
        # the whole job body, so a caller that has grown a step has grown a gate
        # nobody can run locally — which is how all nine of this org's
        # continue-on-error suppressions started.
        tmpl = kit_root / "templates" / "deploy.yml"
        wfdir = repo / ".github" / "workflows"
        if tmpl.exists() and wfdir.is_dir():
            caller = wfdir / "deploy.yml"
            if not caller.exists():
                print(f"::error::{repo.name} has no .github/workflows/deploy.yml. "
                      f"It calls the reusable workflow or it is not in the "
                      f"battery; there is no third state.")
                bad += 1
            elif caller.read_bytes() != tmpl.read_bytes():
                print(f"::error::{repo.name}/.github/workflows/deploy.yml differs "
                      f"from kit/templates/deploy.yml. The caller is a constant so "
                      f"that it is drift-gatable; an edit here moves a gate out of "
                      f"`kit check`, where it can be run before pushing, and into "
                      f"a file that can only be run by pushing.")
                bad += 1
            extra = sorted(q.name for q in wfdir.glob("*.y*ml")
                           if q.name != "deploy.yml")
            if extra:
                print(f"::error::{repo.name} carries workflow(s) beside the "
                      f"caller: {', '.join(extra)}. A course runs the battery and "
                      f"nothing else — anything additional is CI a contributor "
                      f"cannot reproduce.")
                bad += len(extra)

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
            # Compare RELATIVE PATHS, not basenames. Matching on the file name
            # alone made fle/layouts/materiel/list.html a "fork" of the kit's
            # layouts/materials/list.html — two different templates that share
            # four letters. A fork is the same file at the same path; anything
            # else is a coincidence of naming, and list.html is about the most
            # likely name to collide by accident in a Hugo project.
            kit_dir = kit_root / d
            kit_names = ({q.relative_to(kit_dir).as_posix() for q in kit_dir.rglob("*")
                          if q.is_file()} if kit_dir.is_dir() else set())
            # A declared override is still a fork; declaring it buys time, not
            # forgiveness. Every entry needs a reason and a destination, and an
            # entry whose file no longer exists is spent and fails — the same
            # contract as org-audit-exceptions.yml and placeholder-exceptions.yml.
            forks = sorted(q for q in p.rglob("*")
                           if q.is_file() and q.relative_to(p).as_posix() in kit_names
                           and q.relative_to(repo).as_posix() not in overrides.get(repo.name, {}))
            own = [q for q in p.rglob("*")
                   if q.is_file() and q.relative_to(p).as_posix() not in kit_names]
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
    by_name = {r.name: r for r in repos}
    for name, entries in overrides.items():
        for path, e in entries.items():
            if not (by_name.get(name, org / name) / path).exists():
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
    # Checking nothing is not passing. In single-repo mode a zero here means
    # the gate was pointed at something it does not understand, which is
    # exactly how it ran green on all five courses.
    if single and not checked and target.name not in NOT_A_COURSE \
            and target.name not in pre_adoption:
        print(f"::error::A1 examined no repository. {target} was given as a "
              f"course but does not import the kit module and is not on the "
              f"pre-adoption list — so nothing was compared and this is not a "
              f"pass.", file=sys.stderr)
        return 1
    if single and not checked:
        why = ("is not a course" if target.name in NOT_A_COURSE
               else "has not adopted the kit module yet")
        print(f"A1 n/a — {target.name} {why}.")
        return 1 if bad else 0
    if not single and not checked:
        print(f"::error::A1 iterated {len(repos)} director(ies) under {org} and "
              f"found no course importing the kit. That is not an org checkout.",
              file=sys.stderr)
        return 1
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
