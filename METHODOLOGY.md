# Methodology

A scorecard is only as good as its rules. These are the rules, including where they are weak.

---

## 1. Scope

Two governments, five parties.

| Era key | Period | Parties |
|---|---|---|
| `labour` | Oct 2017 to Nov 2023 | **Labour** (led the government across both terms), **NZ First** (coalition partner 2017 to 2020), **Greens** (confidence and supply 2017 to 2020, cooperation agreement 2020 to 2023) |
| `national` | Nov 2023 to present | **National** (leads the government), **ACT** (coalition partner), **NZ First** (coalition partner) |

Labour's term is judged against the state of things at the October 2023 handover. The current term
is judged as at August 2026, and is not finished.

NZ First appears in both eras. It is the only party that does.

---

## 2. What counts as a promise

Two kinds, tagged separately throughout and filterable on the site.

**Manifesto** promises are what a party told voters at the election: the 2017 and 2020 Labour,
Green and NZ First manifestos, and the 2023 National, ACT and NZ First manifestos, together with
major campaign announcements and published fiscal plans.

**Coalition agreement** commitments are what a party actually signed up to in government:

- Labour and NZ First coalition agreement, 2017
- Labour and Greens confidence and supply agreement, 2017
- Labour and Greens cooperation agreement, 2020
- National and ACT coalition agreement, 2023
- National and NZ First coalition agreement, 2023

Speeches from the Throne, published quarterly action plans and 100-day plans were also accepted.

Where a party's own manifesto policy was traded away in coalition talks, **both** are recorded and
the manifesto one is marked `superseded`. That gap is part of the story.

Specific, checkable promises were preferred over aspirations. A promise with a number in it is
worth more than three without one.

---

## 3. The seven outcomes

| Status | Meaning |
|---|---|
| `delivered` | Done, broadly as promised, within the term |
| `largely` | Done, but scaled back, late, or with real caveats |
| `partly` | Real progress, but well short of what was promised |
| `not-delivered` | Promised, and it did not happen, whether or not it was attempted |
| `abandoned` | Dropped, cancelled or reversed by the party that promised it |
| `in-progress` | Still live and moving at the end of the period |
| `superseded` | Traded away in coalition talks before the party got to govern |

---

## 4. How the score is calculated

```
kept%  =  kept / (kept + broken + in-progress)

kept    = delivered + largely
broken  = partly + not-delivered + abandoned
```

`superseded` promises are excluded entirely, because the party never got the chance to attempt
them.

**`in-progress` counts in the denominator but not as a success.** This is the single most
consequential rule on the site, and it needs explaining.

Every in-progress promise in the dataset belongs to the current term, because the other
government's term ended in 2023 and its unfinished business resolved one way or the other. If
unfinished promises were excluded from the score, the current government would get an exemption
its predecessor could not use, and the exemption alone would move its score by roughly nine
points. So unfinished promises count against the score, exactly as Labour's incomplete long-term
targets did when it left office.

Where a commitment described as under way is, by the record's own account, moving *away* from its
target, it is scored `partly` rather than left open. Examples: Jobseeker numbers rising against a
pledge to cut them by 50,000; material hardship rising against a pledge to reduce it.

**Small samples.** A percentage is not shown at all where fewer than 6 promises are scored, and is
visibly marked where fewer than 10 are. The stacked bar still shows the raw counts, which is the
honest thing to show at that sample size.

---

## 5. The like-for-like adjustment

Promises are classified into four kinds:

| Kind | Description | Kept |
|---|---|---:|
| `act` | Do a thing: pass, repeal, abolish, establish. Inside a government's control. | 70% |
| `outcome` | Hit a number: a target for something out in the world. | 36% |
| `procedural` | Look into it: review, explore, investigate, consult. | 71% |
| `other` | Does not fall cleanly into the other three. | 49% |

Those rates hold across every party. A party that campaigned mostly on one kind will score
differently for reasons that have nothing to do with competence.

The like-for-like column is a direct standardisation: each party's kept rate is computed within
each kind, then reweighted to the dataset-wide mix. A stratum with fewer than 4 scored promises is
dropped and the remaining weights renormalised; if more than 45% of the weight is unestimable the
figure is suppressed.

---

## 6. Things that can skew a scorecard like this

Three effects were tested for.

**Unfinished promises can only help one side.** Handled by counting them in the denominator, as
described above.

**The kind of promise matters more than the party.** Handled by the like-for-like column.

**Coalition commitments are co-signed but recorded against one party.** All 19 broken
signed-agreement commitments sit with ACT or NZ First, while National's own agreement list shows
no outright failure. That is a bias by role rather than by politics, and it flatters whichever
party leads a government. **This one is not corrected for**, because reattributing co-signed
commitments would require a judgement about who owned each one that the agreements do not
support. Read partner scores with it in mind. Commitments that appear in both 2023 agreements are
tagged `coSigned` in the data.

The risk in a scorecard like this is rarely loaded language. It is almost always the counting
rules.

---

## 7. The comparison is not symmetrical

- Labour governed for **six years and one month**. The current government has governed for **two
  years and nine months** and its term is not over.
- Labour's term included **Covid-19**, which took over the agenda from 2020 to 2022 and killed off
  promises unrelated to it. This cuts both ways: Covid is a real reason many promises were not
  kept, and it is also true that Labour won a larger majority in 2020, mid-pandemic, on a fresh set
  of promises it also underdelivered.
- Labour held a **single-party majority from 2020**. The current government needs two partners to
  agree.
- **65%** of the current government's promises come from post-election coalition agreements,
  against **43%** of Labour's, and that source type is kept 10 points more often.

The fairest comparisons on the site are the like-for-like column and the area-by-area table, both
of which hold something constant.

---

## 8. Treaty and Māori policy

This is the most contested material in the dataset and it was handled with extra care.

- Policies are described by what the law actually did, in the parties' own neutral terms.
- Where the *significance* of a change is disputed, and it often is, both readings are set out in
  the promise's `contestedNote` and the site does not pick one.
- Delivery is scored on whether the stated commitment happened. That is a narrower question than
  whether it was right, and the site does not attempt the second one.

The area carries 17 promises from the Labour years and 13 from the current term. It remains the
hardest area to score fairly and the one to read most sceptically.

---

## 9. Outcome indicators

21 official statistical series are plotted alongside the promises. Rules:

1. **One consistent definition per series.** Never splice two different measures into one line.
   Where a definition changed, the break is stated in the note.
2. **One consistent point in the year**, stated in the note. Where the final point is a different
   period because it is the latest available, the note says so.
3. **Never estimate, interpolate or infer.** A missing year is omitted. A gap is honest; a made-up
   number is not.
4. **Official sources only** for the numbers.

Worked example of why rule 1 matters: the Ministry for the Environment revises its entire
greenhouse gas back series each year. Comparing a figure from the 2024 inventory against one from
the 2026 inventory can show emissions *rising* over a period in which, within any single vintage,
they fell. Both emissions series here come from one vintage.

No causal claim is made. A government inherits far more than it causes, and most of these series
were already moving before it took office. Inflation and interest rates in particular were driven
by a global cycle that hit every comparable country. Read the per-term changes as *what happened
while they were there*, which is a different claim from *what they did*.

Definitions and caveats for every series: [`sources/indicators.md`](sources/indicators.md).

---

## 10. Known weaknesses

- **Several 2017 and 2020 manifesto PDFs are no longer hosted anywhere reachable.** Those promises
  cite the strongest available record of the commitment rather than the manifesto itself.
- **The Greens' figure is the least trustworthy on the site.** It rests on 33 promises, 42% of them
  targets for things outside the party's control, and five of them pledges in portfolios the Greens
  never held in Cabinet. Several cooperation agreement clauses have nothing measurable in them and
  are still counted. Use the like-for-like column, and treat even that with caution.
- **70 promises are flagged `contested`**, meaning the status call is genuinely arguable. Both
  readings are given. Disagree with them and the numbers move.
- **Promise counts differ by party**, so a percentage drawn from a small sample is less reliable
  than one drawn from a large sample. Counts are shown everywhere for that reason.
- **Four outcome measures are missing**: real GDP per head, average hourly earnings, police officer
  numbers and public housing stock. Stats NZ has retired the tables that held the first two. Police
  report staff numbers only inside annual report PDFs. The housing dashboard moved when the
  Ministry of Housing and Urban Development became part of the Ministry for Cities, Environment,
  Regions and Transport on 1 July 2026.
- **This is one round of research, not a peer-reviewed audit.** Treat it as a starting point with
  its sources attached, not a final verdict.

---

## 11. Sources

Primary sources were used wherever possible: the signed coalition agreements, `legislation.govt.nz`
for what actually passed, Beehive releases, Treasury Budget documents and departmental data. New
Zealand news outlets, including RNZ, the NZ Herald, The Post, Newsroom, The Spinoff and
BusinessDesk, were used to check them.

Every promise carries at least one link to the promise and at least one to the evidence of what
happened. 573 distinct source links in total, across 109 domains.

Where a source could not be found at all, the promise was dropped rather than guessed at.
