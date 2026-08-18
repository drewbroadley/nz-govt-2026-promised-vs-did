# Data

| File | Rows | What it is |
|---|---:|---|
| `promises.json` | 347 | The full dataset. This is the format the site runs on. |
| `promises.csv` | 347 | The same data as a spreadsheet. Opens in Excel or Sheets. |
| `indicators.json` | 21 | The outcome series, with notes. |
| `indicators.csv` | 187 | One row per series per year. Long format, ready to pivot. |
| `indicator-notes.csv` | 21 | Definition and caveats for each series. |
| `areas/` | 18 files | The per-policy-area files the dataset is assembled from. |

**Edit `areas/`, not the generated files.** Everything else here is rebuilt by
`scripts/consolidate.py` and `scripts/build_repo.py`.

## Fields in promises.csv

| Column | Values |
|---|---|
| `id` | Stable identifier, safe to cite |
| `area` / `areaLabel` | One of 18 policy areas |
| `era` | `labour` (2017-2023) or `national` (2023-2026) |
| `party` | Labour, Greens, NZ First, National, ACT |
| `sourceType` | `manifesto` or `coalition-agreement` |
| `ptype` | `act`, `outcome`, `procedural`, `other` (see METHODOLOGY.md section 5) |
| `status` | `delivered`, `largely`, `partly`, `not-delivered`, `abandoned`, `in-progress`, `superseded` |
| `promise` | What was promised |
| `keyNumber` | Promised versus delivered, where a number applies |
| `statusReason` | One line justifying the status |
| `whatHappened` | What actually occurred, with dates |
| `contested` / `contestedNote` | Whether the call is arguable, and both readings if so |
| `sourceDoc` / `sourceUrl` | Where the promise was made |
| `evidenceUrls` | Evidence of what happened, pipe-separated |
| `coSigned` | Appears in both 2023 coalition agreements |

## Counting

The headline percentage is `kept / (kept + broken + in-progress)`, where kept is
`delivered + largely` and broken is `partly + not-delivered + abandoned`. `superseded` is excluded.
Full reasoning in [METHODOLOGY.md](../METHODOLOGY.md).
