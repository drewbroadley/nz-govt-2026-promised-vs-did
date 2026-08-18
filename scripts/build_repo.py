#!/usr/bin/env python3
"""Assemble the publishable repository.

Layout:
  README.md  METHODOLOGY.md  CONTRIBUTING.md  CHANGELOG.md
  data/      canonical dataset (JSON + CSV) and the per-area source files
  sources/   every citation as browsable markdown
  scripts/   the build pipeline
  docs/      what GitHub Pages serves: index.html plus copies of data/ and sources/
             so the site's own links resolve

data/ and sources/ are duplicated into docs/ on purpose. The repo root copies are
what people read on GitHub; the docs/ copies are what the published site links to.
Only ever edit the root copies. Running this script refreshes both.
"""
import json, csv, os, shutil, re, collections, io

ROOT = "/home/claude/nz-tracker"
OUT  = f"{ROOT}/repo"
REPO_URL = "https://github.com/drewbroadley/nz-govt-2026-promised-vs-did"   # <- change in one place
SITE_URL = "https://drewbroadley.github.io/nz-govt-2026-promised-vs-did/"

ds = json.load(open(f"{ROOT}/dataset.json"))
P, AREAS, INDS = ds["promises"], ds["areas"], ds["stats"]["indicators"]
AREA_LABEL = {a["key"]: a["label"] for a in AREAS}

for d in ("data/areas", "sources", "scripts", "docs"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)

# ---------------------------------------------------------------- data
json.dump({"generated": ds["generated"], "areas": AREAS, "promises": P},
          open(f"{OUT}/data/promises.json", "w"), ensure_ascii=False, indent=1)
json.dump({"generated": ds["generated"], "indicators": INDS},
          open(f"{OUT}/data/indicators.json", "w"), ensure_ascii=False, indent=1)

COLS = ["id","area","areaLabel","era","party","sourceType","ptype","status","promise",
        "keyNumber","statusReason","whatHappened","contested","contestedNote",
        "sourceDoc","sourceUrl","evidenceUrls","coSigned"]
with open(f"{OUT}/data/promises.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS)
    for p in P:
        w.writerow([" | ".join(p.get(c,[])) if c=="evidenceUrls" else p.get(c,"") for c in COLS])

with open(f"{OUT}/data/indicators.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["key","label","unit","format","higherIsBetter","source","sourceUrl","year","value"])
    for i in INDS:
        for pt in sorted(i["series"], key=lambda x: x["year"]):
            w.writerow([i["key"],i["label"],i.get("unit",""),i.get("format",""),
                        i.get("higherIsBetter",""),i.get("source",""),i.get("sourceUrl",""),
                        pt["year"],pt["value"]])

with open(f"{OUT}/data/indicator-notes.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["key","label","source","sourceUrl","note"])
    for i in INDS: w.writerow([i["key"],i["label"],i.get("source",""),i.get("sourceUrl",""),i.get("note","")])

for src in sorted(os.listdir(f"{ROOT}/data")):
    if src.endswith(".json") and not src.endswith(".merged"):
        shutil.copy(f"{ROOT}/data/{src}", f"{OUT}/data/areas/{src}")

# ---------------------------------------------------------------- sources
def host(u):
    m = re.match(r"https?://([^/]+)", u or "")
    return m.group(1).replace("www.","") if m else "?"

cites = collections.defaultdict(list)     # url -> [promise ids]
for p in P:
    cites[p["sourceUrl"]].append((p["id"], "promise"))
    for u in p.get("evidenceUrls", []): cites[u].append((p["id"], "evidence"))
for i in INDS:
    if i.get("sourceUrl"): cites[i["sourceUrl"]].append((i["key"], "indicator"))

domains = collections.Counter(host(u) for u in cites)

with open(f"{OUT}/sources/README.md","w",encoding="utf-8") as f:
    f.write(f"""# Sources

Every claim on the site is linked to something you can open. This folder lists all of them.

| File | What it holds |
|---|---|
| [`by-policy-area.md`](by-policy-area.md) | Every promise, grouped by policy area, with its links |
| [`all-sources.md`](all-sources.md) | Every distinct URL, with the promises that cite it |
| [`indicators.md`](indicators.md) | The {len(INDS)} outcome series, with definitions and caveats |

**{len(cites)}** distinct URLs support **{len(P)}** promises and **{len(INDS)}** statistical series.

Each promise carries at least one link to the promise itself (a manifesto, a signed coalition
agreement, or the strongest available record of the commitment) and at least one to the evidence
of what happened.

## Where the sources come from

| Domain | Citations |
|---|---|
""")
    for d, n in domains.most_common(28): f.write(f"| `{d}` | {n} |\n")
    if len(domains) > 28: f.write(f"| _{len(domains)-28} others_ | |\n")
    f.write("""
Primary sources were preferred: the signed coalition agreements, `legislation.govt.nz` for what
actually passed, Beehive releases, Treasury Budget documents and departmental data. New Zealand
news outlets were used to check them.

## Known gaps

Several 2017 and 2020 manifesto PDFs are no longer hosted anywhere reachable. Those promises cite
the strongest available record of the commitment rather than the manifesto itself. Where a source
could not be found at all, the promise was dropped rather than guessed at.
""")

STATUS_LABEL = {"delivered":"Delivered","largely":"Largely delivered","partly":"Partly delivered",
                "not-delivered":"Not delivered","abandoned":"Abandoned","in-progress":"In progress",
                "superseded":"Superseded"}

with open(f"{OUT}/sources/by-policy-area.md","w",encoding="utf-8") as f:
    f.write("# Sources by policy area\n\nEvery promise, with the link to the promise and the links to the evidence.\n\n")
    f.write("## Contents\n\n")
    for a in AREAS:
        n = sum(1 for p in P if p["area"]==a["key"])
        f.write(f"- [{a['label']}](#{re.sub(r'[^a-z0-9]+','-',a['label'].lower()).strip('-')}) ({n})\n")
    for a in AREAS:
        sel = [p for p in P if p["area"]==a["key"]]
        f.write(f"\n---\n\n## {a['label']}\n\n")
        if a.get("blurb"): f.write(f"_{a['blurb']}_\n\n")
        for p in sorted(sel, key=lambda x:(x["era"], x["party"])):
            era = "Labour 2017-2023" if p["era"]=="labour" else "National 2023-2026"
            f.write(f"### {p['promise']}\n\n")
            f.write(f"**{p['party']}** &middot; {era} &middot; **{STATUS_LABEL[p['status']]}**")
            if p.get("contested"): f.write(" &middot; _contested call_")
            f.write(f"  \n`{p['id']}`\n\n")
            if p.get("keyNumber"): f.write(f"> {p['keyNumber']}\n\n")
            f.write(f"{p['statusReason']}\n\n")
            f.write(f"- Promise ({p['sourceType'].replace('-',' ')}): [{host(p['sourceUrl'])}]({p['sourceUrl']})")
            if p.get("sourceDoc"): f.write(f" - {p['sourceDoc']}")
            f.write("\n")
            for u in p.get("evidenceUrls", []): f.write(f"- Evidence: [{host(u)}]({u})\n")
            f.write("\n")

with open(f"{OUT}/sources/all-sources.md","w",encoding="utf-8") as f:
    f.write(f"# All sources\n\nEvery distinct URL cited, grouped by domain, with the entries that cite it.\n\n")
    by_dom = collections.defaultdict(list)
    for u in cites: by_dom[host(u)].append(u)
    for dom in sorted(by_dom, key=lambda d: (-len(by_dom[d]), d)):
        f.write(f"\n## {dom} ({len(by_dom[dom])})\n\n")
        for u in sorted(by_dom[dom]):
            ids = ", ".join(f"`{i}`" for i,_ in sorted(set(cites[u]))[:8])
            more = "" if len(set(cites[u]))<=8 else f" _+{len(set(cites[u]))-8} more_"
            f.write(f"- <{u}>  \n  {ids}{more}\n")

with open(f"{OUT}/sources/indicators.md","w",encoding="utf-8") as f:
    f.write("# Outcome indicators\n\nOfficial statistical series plotted on the site. "
            "Each note states the exact definition, the point in the year used, and any break in comparability.\n\n")
    for i in INDS:
        yrs = sorted(x["year"] for x in i["series"])
        f.write(f"## {i['label']}\n\n")
        f.write(f"- **Key** `{i['key']}`\n- **Unit** {i.get('unit','')}\n- **Source** {i.get('source','')} - <{i.get('sourceUrl','')}>\n")
        f.write(f"- **Covers** {yrs[0]} to {yrs[-1]} ({len(yrs)} points)\n")
        hib = i.get("higherIsBetter")
        f.write(f"- **Direction** {'higher is better' if hib is True else 'lower is better' if hib is False else 'neither direction is inherently better'}\n\n")
        f.write(f"{i.get('note','')}\n\n| Year | Value |\n|---|---|\n")
        for pt in sorted(i["series"], key=lambda x:x["year"]): f.write(f"| {pt['year']} | {pt['value']} |\n")
        f.write("\n")

# ---------------------------------------------------------------- scripts
for s in ("consolidate.py","refine.py","copyfix.py"):
    if os.path.exists(f"{ROOT}/{s}"): shutil.copy(f"{ROOT}/{s}", f"{OUT}/scripts/{s}")
shutil.copy(f"{ROOT}/build_repo.py", f"{OUT}/scripts/build_repo.py")
shutil.copy(f"{ROOT}/template.html", f"{OUT}/scripts/template.html")

# ---------------------------------------------------------------- docs
shutil.copy(f"{ROOT}/index.html", f"{OUT}/docs/index.html")
os.makedirs(f"{OUT}/docs/img", exist_ok=True)
for im in ("og-image.png", "og-square.png"):
    if os.path.exists(f"{ROOT}/{im}"): shutil.copy(f"{ROOT}/{im}", f"{OUT}/docs/img/{im}")
open(f"{OUT}/docs/.nojekyll","w").close()      # stop Pages running Jekyll over it
for sub in ("data","sources"):
    dst = f"{OUT}/docs/{sub}"
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(f"{OUT}/{sub}", dst)

print("data files:", len(os.listdir(f'{OUT}/data')) + len(os.listdir(f'{OUT}/data/areas')))
print("distinct source URLs:", len(cites))
print("domains:", len(domains))
