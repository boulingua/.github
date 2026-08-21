# Beiträge zu boulingua · Contributing to boulingua

Diese Datei gilt für alle 26 Repositories der Organisation.
This file applies to all 26 repositories in the organisation.

---

# Deutsch

## Was boulingua ist

boulingua veröffentlicht freie, GER-orientierte Sprachkurse für die deutsche Gesamtschule und für Selbstlernende. Achtzehn Kurse sind geplant, drei sind live: `efl` (Englisch, 180 Einheiten + 180 Prüfungen), `fle` (Französisch, 156 + 156) und `daf` (Deutsch, 60 Einheiten, GER A1–C1). Dazu kommen `website` (Dach-Hub), `ressources` (Katalog offener Quellen), `curriculum` (das Deskriptor-Rahmenwerk) und die Werkzeug-Repositories.

**boulingua ist ein Ein-Autoren-Projekt.** Die Inhalte stammen von S. Le Boulanger; gepusht wird von R. Heller. Das ist keine Formalie: die pädagogische Kohärenz über achtzehn Sprachen hinweg ist genau das, was ein einzelner Autor leisten kann und ein verteiltes Team nicht.

**Pull Requests werden daher in der Regel nicht angenommen.** Fehler bitte als Issue melden — Tippfehler, sachliche Fehler, kaputte Links, fehlende Downloads, Barrierefreiheitsprobleme, alles. Ein Issue ist hier der schnellere Weg, nicht der langsamere.

## Die eine absolute Regel

> **Öffne niemals einen Pull Request, der eine URL oder einen Slug ändert.**

Der Grund ist finanziell, nicht ästhetisch.

Jede längere Seite dieser Kurse trägt eine VG-Wort-Zählmarke. Zählmarken sind die gesetzliche Vergütung des Autors. In den drei Live-Repositories existieren **821 eindeutige 32-stellige Zählmarken** — 402 in `efl`, 351 in `fle`, 68 in `daf`, ohne eine einzige Dublette.

Eine Zählmarke ist an eine **URL** gebunden. Ändert sich die URL, ist das für die VG Wort ein neues Werk: die registrierte Marke zählt nicht mehr, und das Einkommen dazu ist weg. Ein Hugo-`aliases:`-Eintrag rettet das nicht. Hugos eingebaute Alias-Ausgabe ist eine reine `<meta http-equiv=refresh>`-Seite ohne Zählpixel — sie bewahrt den Link des Lesers, aber nicht die Vergütung.

### Die konkrete Falle: `slug:` in `fle`

**312 von 358 Inhaltsdateien in `fle` tragen eine `slug:`-Zeile im Front Matter.** Diese Zeilen sehen aus, als würden sie nur den Dateinamen wiederholen. Das tun sie nicht — **sie sind die URL.**

```
Datei : fle/content/track_gm_kl06/units/unit01_salutations-et-prenoms.md
Front Matter : slug: "salutations-et-prenoms"
gerenderte URL : /track_gm_kl06/units/salutations-et-prenoms/
```

Der Unterstrich steckt nur im Sektionspfad. Der Blattname ist mit Bindestrichen geschrieben, und das `unitNN`-Präfix erreicht die URL überhaupt nie. Wer eine dieser 312 Zeilen als Redundanz entfernt, ändert die URL, verwaist die Zählmarke — und der Diff sieht dabei aus wie Aufräumen.

Dieselbe Regel in der anderen Richtung: in `efl` **ist** der Ordnername des Leaf Bundles die URL, in `daf` **ist** der Dateiname die URL. Datei- und Ordnernamen werden in Inhaltsverzeichnissen dieser Repositories nicht umbenannt.

### Derzeit blockiert

Der Abgleich mit T.O.M. steht aus, und bis er abgeschlossen ist, bewegt sich am URL-Raum gar nichts. 399 der 402 `efl`-Marken tragen `registered_at: '2026-04-30'` — sechs Tage **vor** der Quarto→Hugo-Migration vom 2026-05-06 — und die Manifeste von `efl` und `fle` sind weiterhin auf den Quarto-Pfad `qmd_path` geschlüsselt. `efl` trägt `aliases:` auf 405 Seiten, `fle` auf 202, `daf` auf 80. Bis zu **592 Marken** könnten also auf URLs registriert sein, die heute kein Pixel mehr ausliefern. Nur das T.O.M.-Konto des Autors kann das klären. **Solange dieser Abgleich offen ist, darf kein Schritt ausgeführt werden, der eine URL ändert.**

## Kein Workflow in dieser Organisation schreibt nach `main`

Das ist eine Regel, kein Ist-Zustand. Am 2026-08-21 wurde `fle/.github/workflows/regen-materials.yml` gelöscht: ein `workflow_dispatch` mit `contents: write`, der `git push origin HEAD:main` ausführte und dabei 156 fertig gesetzte, gebrandete Arbeitsblatt-PDFs durch Platzhalter hätte ersetzen können — unbeaufsichtigt, direkt auf `main`.

`org-audit.yml` prüft das seitdem maschinell und schlägt bei jedem `permissions: contents: write` außerhalb des Pages-Deploy-Jobs fehl. Ein Pull Request, der einen schreibenden Workflow einführt, wird abgelehnt.

## Lokale Einrichtung

Nichts wird über CI debuggt. Die Prüfungen laufen lokal, bevor irgendetwas gepusht wird.

| Werkzeug | Version | Wofür |
|---|---|---|
| Hugo | **≥ 0.159.2, extended** | Alle Kurs-Sites. `extended` ist Pflicht (SCSS). |
| Go | **≥ 1.26.1** | Hugo Modules lösen das Theme darüber auf. |
| Python | **3.11+** | Gate-Skripte und Generatoren. |
| TeX Live mit **XeLaTeX** | aktuell | Foliensätze und Arbeitsblätter. `polyglossia` + `bidi`; kein LuaLaTeX. |
| Piper | ≥ 1.5.0 | Audio. |
| Node | LTS | Nur `daf` und `efl` — siehe unten. |

**Die Go-Version wird nie als Literal geschrieben.** Sie steht in `go.mod` und wird von dort gelesen: in Workflows `actions/setup-go` mit `go-version-file: go.mod`, lokal ebenso aus `go.mod`. Ein fest eingetragener `go-version: '1.22'` neben einem `go.mod` mit `1.26.1` ist genau der Drift, den diese Regel abschafft; in allen 8 Workflows der sechs Hugo-Repositories steht seit dem 2026-08-21 kein einziger Literal-Pin mehr.

**`npm ci` nur dort, wo eine `package.json` liegt** — das sind `daf` und `efl`. Beide brauchen `cytoscape` und `cytoscape-fcose` für das Materials-Network-Bundle (`daf` cytoscape 3.30.2, `efl` 3.30.4, beide `cytoscape-fcose` 2.2.0). Kein anderes Repository hat eine `package.json`, und keines bekommt eine, nur um ein Skript auszuführen.

Danach lokal prüfen:

```
bin/kit check
```

Das ist derselbe Einstiegspunkt, den der wiederverwendbare Workflow in CI mit `--ci` aufruft. Was lokal grün ist, ist in CI grün.

## Lizenz: eingehend = ausgehend

- **Code:** MIT.
- **Inhalte** (Unterrichtseinheiten, Materialien, Texte): **CC BY-SA 4.0**.

Wer etwas beiträgt — Issue-Text, Korrekturvorschlag, Patch — stellt es unter genau diese Lizenzen. `LICENSE` bedeutet in jedem Repository dieser Organisation MIT; die Inhaltslizenz steht in `LICENSE-CONTENT.md`.

## Einsatz von LLM-Werkzeugen

Diese Erklärung stammt aus `pagegen/README.md` und gilt ab sofort für die gesamte Organisation, im Wortlaut:

> **Use of LLM tools**
>
> This project uses large language model (LLM) tools to assist with drafting,
> refactoring and review. All content is authored and reviewed by S. Le Boulanger;
> quoted material is limited to public-domain or openly-licensed sources.

## Was gemeldet werden soll, und wo

Sechs Formulare unter *Issues → New issue*:

| Formular | Wofür |
|---|---|
| `Unit defect` | Fehler in einer Einheit oder Prüfungsseite |
| `VG Wort mark` | Zählmarken-Probleme — **eingeschränkt**, siehe Warnung im Formular |
| `Platform drift` | Abweichung vom `kit`-Stand, Workflow-Regeln, Versions-Pins |
| `New language` | Vorschlag für einen neunzehnten Kurs |
| `Materials defect` | PDF, Thumbnail, Audio, Transkript |
| `Framework gap` | Lücke im Deskriptor-Rahmenwerk `curriculum` |

Leere Issues sind deaktiviert. Ein Formular ohne die geforderten Felder kann nicht bearbeitet werden.

## Checkliste, falls doch ein Pull Request nötig ist

Ein PR wird nur betrachtet, wenn alle acht Punkte zutreffen:

- [ ] Alle Gates laufen lokal grün (`bin/kit check`).
- [ ] **Keine URL und kein Slug geändert.** Keine Zeile in `vgwort/url-lock.csv` berührt. Falls doch: das Re-Key-Protokoll ist vollständig durchlaufen und `url-lock.csv` sowie `url-lock.retired.csv` sind aktualisiert.
- [ ] Keine `slug:`-Zeile in `fle` entfernt oder geändert, kein Leaf-Bundle-Ordner in `efl` umbenannt, keine Inhaltsdatei in `daf` umbenannt.
- [ ] Keine `kit`-eigene Datei geändert ohne Eintrag in `kit-overrides.yml` **und** ohne ADR.
- [ ] **Kein privater VG-Wort-Identifikationscode im Diff** — weder in Code, Kommentar, Testdatei noch Commit-Message.
- [ ] **Kein neues `continue-on-error` und kein `|| true` auf einem Gate.**
- [ ] Kein Workflow schreibt nach `main`; kein `contents: write` außerhalb des Pages-Deploy-Jobs.
- [ ] Bei einer Entscheidung, die eine URL, eine Lizenz, eine VG-Wort-Regel oder die öffentliche Oberfläche von `kit` berührt: die ADR-Nummer ist genannt.

Zum vorletzten Punkt, weil er sonst wie Pedanterie aussieht: die Organisation trug **neun** solcher Unterdrückungen in vier Repositories. Eine davon, `efl/.github/workflows/hugo.yml:128`, hat `verify_url_parity.py` stillgelegt — die URL-Drift-Prüfung, ausgerechnet im Repository mit 402 Zählmarken. Ein Gate ist blockierend, oder es ist als Warnung geschrieben und sagt das in seiner eigenen Ausgabe. Ein drittes gibt es nicht.

---

# English

## What boulingua is

boulingua publishes free, CEFR-aligned language courses for the German *Gesamtschule* and for independent learners. Eighteen courses are planned; three are live: `efl` (English, 180 units + 180 exams), `fle` (French, 156 + 156) and `daf` (German, 60 units, CEFR A1–C1), alongside `website` (the umbrella hub), `ressources` (the open-resource catalogue), `curriculum` (the descriptor framework) and the tooling repositories.

**boulingua is single-author OER.** Content is authored by S. Le Boulanger and pushed by R. Heller. That is not a formality: pedagogical coherence across eighteen languages is something one author can hold and a distributed team cannot.

**Pull requests are therefore generally not accepted.** File an issue instead — typos, factual errors, dead links, missing downloads, accessibility problems, all of it. An issue is the faster route here, not the slower one.

## The one absolute rule

> **Never open a pull request that changes a URL or a slug.**

The reason is money, not tidiness.

Every substantial page in these courses carries a VG Wort *Zählmarke* — a counting mark. Zählmarken are the author's statutory remuneration under German copyright law. **821 unique 32-hex marks** exist across the three live repositories: 402 in `efl`, 351 in `fle`, 68 in `daf`, with zero duplicates.

A mark is bound to a **URL**. Change the URL and VG Wort sees a new work: the registered mark stops earning, permanently. A Hugo `aliases:` entry does not rescue it. Hugo's built-in alias output is a bare `<meta http-equiv=refresh>` stub that carries no pixel — it preserves the reader's link, not the income.

### The specific trap: `slug:` in `fle`

**312 of `fle`'s 358 content files carry a `slug:` line in front matter.** Those lines look like they restate the filename. They do not — **they are the URL.**

```
file          : fle/content/track_gm_kl06/units/unit01_salutations-et-prenoms.md
front matter  : slug: "salutations-et-prenoms"
rendered URL  : /track_gm_kl06/units/salutations-et-prenoms/
```

The underscore is in the section path only. The leaf is hyphenated, and the `unitNN` ordinal never reaches the URL at all. Removing one of those 312 lines as redundant changes the URL and orphans the mark — and the diff looks like housekeeping while it does so.

The same rule in the other direction: in `efl` the leaf-bundle **directory name is the URL**; in `daf` the **filename is the URL**. Files and directories under `content/` in these repositories are not renamed.

### Currently blocked

The T.O.M. reconciliation is outstanding, and until it closes nothing in the URL space moves. 399 of `efl`'s 402 marks carry `registered_at: '2026-04-30'` — six days **before** the Quarto→Hugo migration of 2026-05-06 — and the `efl` and `fle` manifests are still keyed on the Quarto `qmd_path`. `efl` carries `aliases:` on 405 pages, `fle` on 202, `daf` on 80. So up to **592 marks** may be registered against URLs that no longer render a pixel. Only the author's T.O.M. account can settle it. **Until that diff is empty, no step that changes a URL may proceed.**

## No workflow in this org writes to `main`

This is a rule, not a description. On 2026-08-21 `fle/.github/workflows/regen-materials.yml` was deleted: a `workflow_dispatch` with `contents: write` running `git push origin HEAD:main`, capable of overwriting 156 finished branded worksheet PDFs with placeholders and pushing the damage to `main` unattended.

`org-audit.yml` now asserts this mechanically and fails on any `permissions: contents: write` outside the Pages deploy job. A pull request introducing a writing workflow is refused.

## Local setup

Nothing is debugged through CI. The gates run locally before anything is pushed.

| Tool | Version | For |
|---|---|---|
| Hugo | **≥ 0.159.2, extended** | Every course site. `extended` is required (SCSS). |
| Go | **≥ 1.26.1** | Hugo Modules resolve the theme through it. |
| Python | **3.11+** | Gate scripts and generators. |
| TeX Live with **XeLaTeX** | current | Slide decks and worksheets. `polyglossia` + `bidi`; no LuaLaTeX. |
| Piper | ≥ 1.5.0 | Audio. |
| Node | LTS | `daf` and `efl` only — see below. |

**Never write the Go version as a literal.** It lives in `go.mod` and is read from there: `actions/setup-go` with `go-version-file: go.mod` in workflows, and from `go.mod` locally. A pinned `go-version: '1.22'` sitting next to a `go.mod` declaring `1.26.1` is exactly the drift this rule removes; since 2026-08-21 all 8 workflows across the six Hugo repositories carry zero literal version pins.

**`npm ci` only where a `package.json` exists** — that is `daf` and `efl`. Both need `cytoscape` and `cytoscape-fcose` for the Materials Network bundle (`daf` cytoscape 3.30.2, `efl` 3.30.4, both `cytoscape-fcose` 2.2.0). No other repository has a `package.json`, and none acquires one just to run a script.

Then check locally:

```
bin/kit check
```

This is the same entry point the reusable workflow invokes in CI with `--ci`. What passes locally passes in CI.

## Inbound = outbound licensing

- **Code:** MIT.
- **Content** (teaching units, materials, prose): **CC BY-SA 4.0**.

Anything you contribute — issue text, a suggested correction, a patch — is offered under exactly those terms. `LICENSE` means MIT in every repository in this organisation; the content licence lives in `LICENSE-CONTENT.md`.

## Use of LLM tools

This statement originates in `pagegen/README.md` and is org policy from now on, in its own words:

> **Use of LLM tools**
>
> This project uses large language model (LLM) tools to assist with drafting,
> refactoring and review. All content is authored and reviewed by S. Le Boulanger;
> quoted material is limited to public-domain or openly-licensed sources.

## What to report, and where

Six forms under *Issues → New issue*:

| Form | For |
|---|---|
| `Unit defect` | An error in a unit or exam page |
| `VG Wort mark` | Counting-mark problems — **restricted**, read the warning in the form |
| `Platform drift` | Divergence from `kit`, workflow rules, version pins |
| `New language` | A proposal for a nineteenth course |
| `Materials defect` | PDFs, thumbnails, audio, transcripts |
| `Framework gap` | A gap in the `curriculum` descriptor framework |

Blank issues are disabled. A form submitted without its required fields cannot be acted on.

## Pull request checklist, if one is genuinely needed

A PR is looked at only when all eight hold:

- [ ] Every gate passes locally (`bin/kit check`).
- [ ] **No URL and no slug changed.** No row of `vgwort/url-lock.csv` touched. If one had to change: the re-key protocol was followed in full and both `url-lock.csv` and `url-lock.retired.csv` are updated.
- [ ] No `slug:` line in `fle` removed or altered; no `efl` leaf-bundle directory renamed; no `daf` content file renamed.
- [ ] No kit-owned file modified without a `kit-overrides.yml` entry **and** an ADR.
- [ ] **No private VG Wort identification code anywhere in the diff** — not in code, comments, fixtures or the commit message.
- [ ] **No new `continue-on-error` and no `|| true` on a gate.**
- [ ] No workflow writes to `main`; no `contents: write` outside the Pages deploy job.
- [ ] For any decision touching a URL, a licence, a VG Wort rule or `kit`'s public surface: the ADR number is named.

On the sixth item, because it otherwise reads as pedantry: the org carried **nine** such suppressions across four repositories. One of them, `efl/.github/workflows/hugo.yml:128`, silenced `verify_url_parity.py` — the URL-drift check, on the repository holding 402 marks. A gate is blocking, or it is written to warn and says so in its own output. There is no third state.
