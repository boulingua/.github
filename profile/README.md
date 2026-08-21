<p align="center">
  <img src="https://boulingua.github.io/website/images/avatar.png" alt="boulingua" width="160" />
</p>

<h1 align="center">boulingua</h1>

<p align="center"><strong>Multilingual Teaching Platform — EFL · FLE · DaF · Ressourcen</strong></p>

Boulingua is a free, openly licensed multilingual teaching platform created by S. Le Boulanger. It is built for language teachers and learners working in the German school system — specifically *Gesamtschule* — and for international learners of German following the Common European Framework of Reference (CEFR).

The platform consists of **four sister sites** sharing a single design system, plus an umbrella landing page. Three of the sister sites deliver curriculum-aligned teaching units for English, French, and German as a foreign language. The fourth is a curated hub of free, openly licensed teaching resources.

🌐 **Website:** https://boulingua.github.io/website/

---

## Platforms

### 🇬🇧 EFL — English as a Foreign Language

A complete English-as-a-foreign-language curriculum spanning **Klassen 5–13**. Around **180 units** cover listening, reading, writing, speaking, grammar, and vocabulary. Every unit is curriculum-aligned (Bildungsplan BW) and includes *Niveau-Differenzierung* at the G, M, and E levels.

For teachers and learners at Gesamtschule.

→ **Site:** https://boulingua.github.io/efl/  
→ **Repo:** https://github.com/boulingua/efl

### 🇫🇷 FLE — Français Langue Étrangère

A French-as-a-foreign-language curriculum spanning **Klassen 6–13**. Around **156 units** cover *compréhension orale et écrite, production orale et écrite, grammaire,* and *vocabulaire.* Curriculum-aligned with *Niveau-Differenzierung* at the G, M, and E levels.

For teachers and learners at Gesamtschule.

→ **Site:** https://boulingua.github.io/fle/  
→ **Repo:** https://github.com/boulingua/fle

### 🇩🇪 DaF — Deutsch als Fremdsprache

A German-as-a-foreign-language curriculum for international learners, covering **CEFR levels A1–C1**. Around **60 units** follow the four-skill structure of standard examination formats: *Lesen, Hören, Schreiben, Sprechen.* Units are organised by CEFR level rather than by school year.

For learners and teachers preparing for CEFR-based examinations.

→ **Site:** https://boulingua.github.io/daf/  
→ **Repo:** https://github.com/boulingua/daf

### 📚 Ressourcen-Hub — Curated Teaching Resources

A curated collection of **free, openly licensed teaching resources** for English, French, and German. Materials come from institutional and public sources only — British Council, Goethe-Institut, Deutsche Welle, and similar organisations. **No commercial publishers** are included.

Resources are tagged by language, level, skill, and licence type so teachers can quickly find what they need.

For teachers of English, French, and German across all levels.

→ **Site:** https://boulingua.github.io/ressources/  
→ **Repo:** https://github.com/boulingua/ressources

---

## Umbrella Website

The landing page that ties everything together — about, philosophy, references, contact, and legal pages.

→ **Site:** https://boulingua.github.io/website/  
→ **Repo:** https://github.com/boulingua/website

---

## Repositories at a glance

| Repo | Stack | Purpose |
|------|-------|---------|
| [`website`](https://github.com/boulingua/website) | Hugo (Coder theme) | Umbrella landing page + interactive language-reach map |
| [`efl`](https://github.com/boulingua/efl) | Hugo | English curriculum, Klassen 5–13 |
| [`fle`](https://github.com/boulingua/fle) | Hugo | French curriculum, Klassen 6–13 |
| [`daf`](https://github.com/boulingua/daf) | Hugo | German curriculum, CEFR A1–C1 |
| [`ressources`](https://github.com/boulingua/ressources) | Hugo | Curated open-license resources hub |
| [`kit`](https://github.com/boulingua/kit) | Hugo module · LaTeX · Python | The platform every course imports: shared layouts and assets, branded slide-deck and worksheet templates, native-voice audio pipeline, build and gate scripts |

The four content sites are deployed via **GitHub Pages**. A course repo holds
content, marks, materials, brand and configuration — no code: the shared surface
arrives from `kit` as a Hugo module, a pinned CI checkout, and a digest-locked
`_materials/` tree. The earlier toolchain repos — `pagegen`, `slidegen`,
`sheetgen` and `audiogen` — are **archived**; their histories are preserved
inside `kit`.

Additional single-letter repos (`afl`, `cfl`, `gfl`, …) are **scaffolds for
future languages** — the platform is architected to extend beyond its first
three languages, as shown on the [interactive world map](https://boulingua.github.io/website/platforms/).

---

## Design philosophy

All sister sites share an **identical design system** — same navigation, same typography (Source Sans 3 + JetBrains Mono), same visual rhythm in light and dark mode. A teacher or student moving between languages encounters the same interface every time. Consistency is a feature, not an accident.

Within that shared frame, **each language carries its own signature accent colour** — chosen to be distinct, accessible, and, by rule, *not* a colour found in the language's national flag — together with a matching pentagon icon. The colour is applied consistently across the site, the READMEs, and the printed materials, so each language stays recognisable at a glance. The full palette and the reasoning behind it are documented on the [design & colours page](https://boulingua.github.io/website/design/).

Every teaching unit ships in **multiple formats**: an HTML page for browser study, a printable slide deck and worksheet (both generated from the branded LaTeX templates in [`kit`](https://github.com/boulingua/kit)), and native-voice audio. PDFs carry attribution watermarks; CI gates block deployment for missing copyright metadata, unfilled Impressum placeholders, or commercial sources in the Ressourcen-Hub.

---

## License

Dual-licensed across all repositories:

- **Code** — [MIT License](https://opensource.org/licenses/MIT)
- **Content** (teaching units, resources, written materials) — [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

Anyone can use, share, and adapt the materials with attribution.

---

## Contact

Maintained by **S. Le Boulanger** — see https://boulingua.github.io/website/contact/ and https://boulingua.github.io/website/impressum/.
