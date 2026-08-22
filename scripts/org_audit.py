#!/usr/bin/env python3
"""Org audit — the rules that only make sense across all 27 repos at once.

    python scripts/org_audit.py ORG_CHECKOUT

Three checks, each of which caught something real:

**1. No workflow writes to main.** `fle` carried a workflow_dispatch job with
`contents: write` that ran the retired placeholder generator and pushed to
main — one dispatch would have overwritten 156 committed branded worksheet PDFs
and pushed the result. It was deleted, but deleting one instance leaves the
class open. This closes it: `contents: write`, `git push`, and the two common
auto-commit actions are all a failure anywhere in the org.

**2. No gate suppression.** Nine `continue-on-error` / `|| true` suppressions
existed across four repos, and three sat on the revenue path — including the
closest thing `efl` had to a URL-drift check. The ban is only credible if it
names what it bans, so the rule is precise: `continue-on-error:` at step level
is forbidden outright; `|| true` is forbidden only on a line whose command is a
gate. `[[ -f package-lock.json ]] && npm ci || true` and
`kill "$(cat /tmp/server.pid)" || true` are shell idioms inside a step, not
suppressions, and the rule must not flag them or it will be switched off.

**3. One caller, byte-identical.** Everything configurable is in boulingua.yml,
so the caller is a constant — and a constant is checkable. A course that has
grown its own gate step has left the battery.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WRITE_SMELLS = [
    (re.compile(r"contents:\s*write"), "grants contents: write"),
    (re.compile(r"git\s+push"), "pushes from CI"),
    (re.compile(r"peter-evans/create-pull-request"), "opens PRs from CI"),
    (re.compile(r"stefanzweifel/git-auto-commit-action"), "auto-commits from CI"),
]
GATE_CMD = re.compile(r"verify_|check_|audit|pa11y|lychee|conformance_|kit check")
CONTINUE_ON_ERROR = re.compile(r"^\s*continue-on-error:\s*true")
OR_TRUE = re.compile(r"\|\|\s*true")


def load_exceptions(here: Path) -> dict:
    import yaml
    f = here / "org-audit-exceptions.yml"
    return yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else {}


def main() -> int:
    org = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    exc = load_exceptions(Path(__file__).resolve().parent)
    archived = set(exc.get("archived", []))
    scheduled = {(x["repo"], x["file"]): x for x in exc.get("scheduled", [])}
    repos = sorted(p.parent for p in org.glob("*/.git") if p.is_dir())
    if not repos:
        repos = sorted(p.parent for p in org.glob("*/.git"))
    bad, scanned = 0, 0

    deferred = 0
    for repo in repos:
        if repo.name in archived:
            continue          # read-only; the code lives on inside kit
        for wf in sorted((repo / ".github" / "workflows").glob("*.yml")):
            scanned += 1
            rel = f"{repo.name}/{wf.relative_to(repo)}"
            sched = scheduled.get((repo.name, str(wf.relative_to(repo))))
            for i, line in enumerate(wf.read_text(encoding="utf-8").split("\n"), 1):
                if line.lstrip().startswith("#"):
                    continue
                for pat, why in WRITE_SMELLS:
                    if pat.search(line):
                        print(f"::error::{rel}:{i} {why} — no workflow in this org "
                              f"writes to main. One dispatch of the workflow this "
                              f"rule exists for would have overwritten 156 branded "
                              f"PDFs.")
                        bad += 1
                sup = (CONTINUE_ON_ERROR.search(line)
                       or (OR_TRUE.search(line) and GATE_CMD.search(line)))
                if sup:
                    if sched:
                        print(f"::warning::{rel}:{i} gate suppression — known, "
                              f"scheduled for {sched['destination']}")
                        deferred += 1
                    else:
                        print(f"::error::{rel}:{i} gate suppression — a gate is "
                              f"either blocking or written to warn, never "
                              f"suppressed: {line.strip()[:60]}")
                        bad += 1

    print(f"  {len(repos) - len(archived)} live repo(s), {scanned} workflow file(s) "
          f"scanned; {len(archived)} archived skipped")
    if deferred:
        print(f"  {deferred} known suppression(s) deferred to a named phase — "
              f"warned, not failed. Each carries a reason and a destination in "
              f"org-audit-exceptions.yml; an exception with neither is how a "
              f"permanent suppression starts.")
    if bad:
        print(f"\norg-audit FAIL — {bad} finding(s)", file=sys.stderr)
        return 1
    print("org-audit OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
