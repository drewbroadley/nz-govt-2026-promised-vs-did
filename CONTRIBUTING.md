# Contributing

The point of publishing the data is that people can argue with it. Corrections are welcome.

## Reporting a wrong call

Open an issue with:

1. **The promise id** (each one is shown on the site under its status, and is the `id` column in
   `data/promises.csv`)
2. **What you think the status should be**, and why
3. **A source.** This is the important part. A link to legislation, a Beehive release, a Budget
   document, an agency page or a news report. Without one, there is nothing to act on.

Status calls are judgements, and 70 of them are already flagged as genuinely arguable. If a
promise is marked `contested`, its note sets out both readings. Adding a third reading is useful;
so is showing that one of the two is wrong.

## Reporting a missing promise

Same thing, plus the wording of the commitment and where it was made: which manifesto, which
coalition agreement, which page. Manifesto promises need a citable record. If a party said it
once at a public meeting and it appears nowhere in writing, it is out of scope.

## Reporting a data problem

Broken links, wrong dates, arithmetic that does not add up, a party credited to a term it was not
in government for. `scripts/consolidate.py` catches most structural problems, so if you find one
it slipped through, that is worth knowing about too.

## Adding an outcome indicator

Four are known to be missing: real GDP per head, average hourly earnings, police officer numbers,
public housing stock. If you can find any of them as a consistent published series, the rules are
in [METHODOLOGY.md](METHODOLOGY.md) section 9. In short: one definition, one point in the year,
never estimate a missing value, official source only.

## Making a change yourself

The dataset is assembled from the per-area files in `data/areas/`. Edit those, never
`data/promises.json`, which is generated.

```bash
python3 scripts/consolidate.py    # validate and rebuild the dataset
python3 scripts/build_repo.py     # regenerate data/, sources/ and docs/
```

`consolidate.py` prints a list of problems and should print zero.

## What will not be changed

Scores are about **delivery, not merit**. Arguments that a policy was good, bad, popular or
unpopular do not change a status. "This was delivered but it was a terrible idea" is still
`delivered`. "This was abandoned and abandoning it was the right call" is still `abandoned`.

The site takes no position on whether any policy was desirable, and it will not start.
