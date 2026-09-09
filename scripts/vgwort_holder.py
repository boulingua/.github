#!/usr/bin/env python3
"""Every VG Wort Zählmarke in this organisation belongs to one rightsholder.

    vgwort_holder.py ORG_CHECKOUT_DIR

Three ways a mark register goes wrong, and none of them is visible from inside
a single repository — which is why this lives in the org audit and not in the
per-course battery:

  The holder. A Zählmarke is registered to a person. A registry entry naming
  anybody else is either a mistake or somebody else's revenue, and both are
  worth failing over.

  Reuse across repositories. VG Wort issues one Zählmarke per work and does
  not reissue it. The same public_id in two courses means two works claim one
  registration; only one of them can be right, and nothing inside either repo
  can see the collision.

  A second source. When a mark id appears in a repository file that is NOT the
  registry, there are two answers to "which marks does this course use", and
  the one nobody maintains will eventually be the one somebody reads. The
  Quarto-era vgwort-manifest.csv files are exactly this: unreferenced by any
  code, and holding ids the live registry no longer carries.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

PIXEL = re.compile(r"vgwort\.de/na/([0-9a-f]{32})")
# Reading extensions only. A binary is not a second source anybody edits.
TEXT = {".md", ".csv", ".yaml", ".yml", ".toml", ".html", ".js", ".json", ".txt"}


def main() -> int:
    org = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cfg_pfad = Path(__file__).resolve().parent.parent / "vgwort-holder.yml"
    cfg = yaml.safe_load(cfg_pfad.read_text(encoding="utf-8")) if cfg_pfad.exists() else {}
    halter = cfg.get("holder")
    erlaubt = set(cfg.get("also_accepted") or [])
    im_geltungsbereich = set(cfg.get("in_scope") or [])
    if not halter:
        print("::error::vgwort-holder.yml names no holder — the check has no "
              "standard to check against")
        return 1

    bad = 0
    gesehen: dict[str, str] = {}          # public_id -> repo
    geprueft = registrierungen = 0

    for repo in sorted(p.parent for p in org.glob("*/.git")):
        reg_pfad = repo / "data" / "vgwort.yaml"
        if not reg_pfad.exists():
            continue
        if im_geltungsbereich and repo.name not in im_geltungsbereich:
            print(f"  {repo.name}: holds a registry but is outside in_scope — skipped")
            continue
        geprueft += 1
        eintraege = yaml.safe_load(reg_pfad.read_text(encoding="utf-8")) or []
        bekannt = set()
        for e in eintraege:
            registrierungen += 1
            pid, url = e.get("public_id"), e.get("url")
            autor = e.get("author")
            bekannt.add(pid)
            if autor != halter and autor not in erlaubt:
                print(f"::error::{repo.name}{url}: registered to {autor!r}, not to "
                      f"{halter!r}. A Zählmarke belongs to a person; a registry "
                      f"entry naming somebody else is not this course's to claim.")
                bad += 1
            if pid in gesehen and gesehen[pid] != repo.name:
                print(f"::error::{repo.name}{url}: public_id {pid} is already "
                      f"registered in {gesehen[pid]}. VG Wort issues one mark per "
                      f"work and does not reissue it, so two works cannot share one.")
                bad += 1
            gesehen[pid] = repo.name

        # Zweite Quelle: Marken-IDs ausserhalb der Registratur
        fremd: dict[str, set[str]] = {}
        for f in repo.rglob("*"):
            # public/ und resources/ sind Hugo-Bauausgabe, kein zweiter Ort, an
            # dem jemand eine Marke pflegt. Sie enthalten die Pixel notwendig -
            # sie zu melden hiesse, das Rendern selbst zu beanstanden.
            # RELATIV zum Repo pruefen: der Org-Checkout kann selbst in einem
            # Verzeichnis namens "public" liegen, und ein Abgleich gegen den
            # absoluten Pfad haette dann jede Datei ausgeschlossen und still
            # "OK" gemeldet.
            if set(f.relative_to(repo).parts) & {".git", "public", "resources",
                                                 "node_modules"}:
                continue
            if not f.is_file() or f.suffix not in TEXT:
                continue
            if f.name in {"vgwort.yaml", "withdrawn.csv"}:
                continue
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            unbekannt = {p for p in PIXEL.findall(t) if p not in bekannt}
            if unbekannt:
                fremd.setdefault(str(f.relative_to(repo)), set()).update(unbekannt)
        for datei, ids in sorted(fremd.items()):
            print(f"::error::{repo.name}/{datei}: holds {len(ids)} mark id(s) that "
                  f"the registry does not carry. Two sources of truth for which "
                  f"marks this course uses; delete the file or fold it into "
                  f"data/vgwort.yaml.")
            bad += 1

    print(f"  {geprueft} course registr(ies) checked, {registrierungen} "
          f"registration(s), holder {halter!r}")
    if bad:
        print(f"\nvgwort-holder FAIL — {bad} finding(s)", file=sys.stderr)
        return 1
    print("vgwort-holder OK — every mark is held by the declared rightsholder, "
          "no id is reused across courses, and the registry is the only source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
