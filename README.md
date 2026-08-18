# Promised vs Performed

**A delivery record of New Zealand's last two governments, ahead of the 7 November 2026 general election.**

[**View the site**](https://drewbroadley.github.io/nz-govt-2026-promised-vs-did/) &middot;
[Browse the data](data/) &middot;
[Browse the sources](sources/) &middot;
[Read the method](METHODOLOGY.md)

347 election and coalition promises from five parties, each scored on whether it was delivered,
with a link to the promise and a link to the evidence of what happened. Plus 21 official
statistical series covering the same period.

It scores **delivery, not merit**. A promise kept is scored the same whether the policy worked or
was a disaster, and a promise broken the same whether dropping it was cowardice or good sense.

---

## What it found

| Government | Promises | Judgeable | Kept |
|---|---:|---:|---:|
| Labour-led, Oct 2017 to Nov 2023 | 152 | 146 | **55%** |
| National-led, Nov 2023 to present | 195 | 187 | **58%** |

Three points apart, on 347 promises, is a tie. The interesting differences are elsewhere:

- **National promised nearly three times as fast** (71 a year against 25) and its promises were
  easier. 65% of them come from signed coalition agreements, written after the election by people
  who already knew what was deliverable, against 43% of Labour's. Coalition-agreement commitments
  are kept 61% of the time across this dataset; manifesto pledges 51%.
- **The kind of promise matters more than the party.** Promises to *do a thing*, like passing a
  law, are kept 70% of the time by anyone. Promises to *hit a number* are kept 36% of the time by
  anyone. The site's like-for-like column reweights every party to the same mix.
- **They kept different promises, not more of them.** Labour delivered on trade, housing rules and
  climate law, and failed on transport and health. National has delivered on law and order and
  energy, and undershot most on cost of living and tax.

By party, within its own term:

| Party | Term | Promises | Kept |
|---|---|---:|---:|
| Labour | Labour-led | 87 | 62% |
| NZ First | Labour-led | 32 | 64% |
| Greens | Labour-led | 33 | 28% |
| National | National-led | 99 | 62% |
| ACT | National-led | 35 | 62% |
| NZ First | National-led | 61 | 48% |

NZ First is the only party to have governed in both terms, which makes it the closest thing to a
controlled experiment in the dataset.

**Treat the Greens' figure with caution.** It rests on 33 promises, 42% of them targets for things
outside the party's control, and five of them in portfolios the Greens never held in Cabinet.

---

## Repository layout

```
data/
  promises.json          all 347 promises, the format the site runs on
  promises.csv           the same data as a spreadsheet
  indicators.json        the 21 outcome series
  indicators.csv         one row per series per year
  indicator-notes.csv    definitions and caveats for each series
  areas/                 the per-policy-area source files the dataset is built from
sources/
  README.md              index, and where the citations come from
  by-policy-area.md      every promise with its links, grouped by subject
  all-sources.md         every distinct URL, grouped by domain
  indicators.md          each statistical series, its definition and its caveats
scripts/
  consolidate.py         builds data/areas/*.json into one validated dataset
  refine.py              applies status corrections and classifies promise types
  copyfix.py             macron and punctuation pass over the source files
  build_repo.py          assembles this repository
  template.html          the site template, before the data is injected
docs/
  index.html             the published site, self-contained in one file
  data/  sources/        copies, so the site's own links resolve
```

`data/` and `sources/` appear twice on purpose. The copies at the repository root are what you
read on GitHub. The copies under `docs/` are what the published site links to. **Only edit the
root copies**; running `scripts/build_repo.py` refreshes both.

---

## Publishing it

The site is a single self-contained HTML file with no build step, no dependencies and no external
requests. To publish with GitHub Pages:

1. **Settings → Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main`, folder **`/docs`**

It will appear at `https://<your-username>.github.io/<repo-name>/`.

If you fork this or rename the repository, update the two URLs at the top of
`scripts/build_repo.py` and the repository links in `scripts/template.html`, then rebuild.

---

## Rebuilding from source

Python 3.9 or later, no third-party packages.

```bash
python3 scripts/consolidate.py     # data/areas/*.json  ->  dataset.json
python3 scripts/refine.py          # status corrections + promise-type classification
python3 scripts/build_repo.py      # regenerates data/, sources/ and docs/
```

`consolidate.py` validates as it goes: it rejects unknown statuses and parties, catches a party
credited to a term it was not in government for, requires a working source URL on every promise,
and reports duplicate ids. It exits with a list of problems, and should print zero.

---

## How promises are scored

Seven outcomes, applied identically to both terms:

| Status | Meaning | Count |
|---|---|---:|
| Delivered | Done, broadly as promised, within the term | 138 |
| Largely delivered | Done, but scaled back, late, or with real caveats | 50 |
| Partly delivered | Real progress, but well short of what was promised | 89 |
| Not delivered | Promised, and it did not happen | 38 |
| Abandoned | Dropped, cancelled or reversed by the party that promised it | 7 |
| In progress | Still live at the end of the period | 11 |
| Superseded | Traded away in coalition talks before the party got to govern | 14 |

The headline percentage is **kept ÷ (kept + broken + in progress)**, where kept means delivered or
largely delivered. An unfinished promise counts in the denominator but not as a success.

That rule matters more than it looks. Every in-progress promise belongs to the current term,
because the other government's ended in 2023. Excluding them would hand the current government an
exemption its predecessor could not use.

Full detail, including the known weaknesses, is in [METHODOLOGY.md](METHODOLOGY.md).

---

## Reusing it

Released under [CC0 1.0](LICENSE): a public domain dedication. You can copy, adapt and republish
any of it, commercially or otherwise, with no permission and no attribution required.

Attribution is not required, but it is appreciated, and it helps readers trace a number back to
its source:

> Broadley, D. (2026). *Promised vs Performed: a delivery record of New Zealand's last two
> governments.* https://drewbroadley.github.io/nz-govt-2026-promised-vs-did/

---

## Corrections

Every status call is a judgement, and 70 of them are flagged as genuinely arguable. If you think
one is wrong, [open an issue](https://github.com/drewbroadley/nz-govt-2026-promised-vs-did/issues) with a
source, or email drew@broadley.org.nz. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

Compiled by **Drew Broadley** &middot; drew@broadley.org.nz

The research, data collection and writing were done with AI assistance. Every promise carries links
to the promise and to the evidence, so any entry can be checked independently. This is one round of
research, not a peer-reviewed audit. Treat it as a starting point with its sources attached, not a
final verdict.
