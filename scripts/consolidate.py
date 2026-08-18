#!/usr/bin/env python3
"""Consolidate per-area JSON into one validated dataset."""
import json, glob, os, re, sys, unicodedata
from collections import Counter, defaultdict

DATA = "/home/claude/nz-tracker/data"
OUT = "/home/claude/nz-tracker/dataset.json"

VALID_STATUS = {"delivered", "largely", "partly", "not-delivered",
                "abandoned", "in-progress", "superseded"}
VALID_PARTY = {"Labour", "Greens", "NZ First", "National", "ACT"}
VALID_ERA = {"labour", "national"}
VALID_SRC = {"manifesto", "coalition-agreement"}

AREA_ORDER = [
    "housing", "cost-of-living", "economy", "health", "education", "law-order",
    "climate", "environment", "transport", "energy", "welfare", "treaty",
    "immigration", "rma", "primary", "water", "public-service", "foreign",
]

problems = []
areas = []
seen_ids = {}
promises = []

for path in sorted(glob.glob(f"{DATA}/*.json")):
    base = os.path.basename(path)
    if base.startswith("_") or base.startswith("stats"):
        continue
    try:
        d = json.load(open(path))
    except Exception as e:
        problems.append(f"{base}: FAILED TO PARSE — {e}")
        continue

    key = d.get("areaKey") or base[:-5]
    label = d.get("areaLabel") or key.title()
    blurb = (d.get("areaBlurb") or "").strip()
    plist = d.get("promises", [])
    if not plist:
        problems.append(f"{base}: no promises")
        continue

    areas.append({"key": key, "label": label, "blurb": blurb})

    for p in plist:
        pid = p.get("id", "")
        if not pid:
            problems.append(f"{key}: promise with no id — dropped")
            continue
        if pid in seen_ids:
            problems.append(f"duplicate id '{pid}' ({key} vs {seen_ids[pid]}) — suffixed")
            n = 2
            while f"{pid}-{n}" in seen_ids:
                n += 1
            pid = f"{pid}-{n}"
        seen_ids[pid] = key

        status = p.get("status", "")
        party = p.get("party", "")
        era = p.get("era", "")
        stype = p.get("sourceType", "")

        if status not in VALID_STATUS:
            problems.append(f"{pid}: bad status '{status}' — dropped"); continue
        if party not in VALID_PARTY:
            problems.append(f"{pid}: bad party '{party}' — dropped"); continue
        if era not in VALID_ERA:
            problems.append(f"{pid}: bad era '{era}' — dropped"); continue
        if stype not in VALID_SRC:
            problems.append(f"{pid}: bad sourceType '{stype}' — defaulted to manifesto")
            stype = "manifesto"

        # sanity: NZ First is the only party legitimately in both eras
        era_parties = {"labour": {"Labour", "Greens", "NZ First"},
                       "national": {"National", "ACT", "NZ First"}}
        if party not in era_parties[era]:
            problems.append(f"{pid}: {party} not in government during '{era}' era — dropped")
            continue

        src = (p.get("sourceUrl") or "").strip()
        ev = [u.strip() for u in p.get("evidenceUrls", []) if u and u.strip().startswith("http")]
        if not src.startswith("http"):
            problems.append(f"{pid}: no valid sourceUrl — dropped"); continue
        if not ev:
            problems.append(f"{pid}: no evidenceUrls")

        def clean(s):
            s = (s or "").strip()
            s = unicodedata.normalize("NFC", s)
            s = s.replace("→", "->").replace("—", ", ")  # never re-introduce a spaced-hyphen dash
            s = s.replace("‘", "'").replace("’", "'")
            s = s.replace("“", '"').replace("”", '"')
            return re.sub(r"\s+", " ", s)

        contested = bool(p.get("contested"))
        note = clean(p.get("contestedNote"))
        if contested and not note:
            note = "The status of this commitment is open to interpretation."
        if not contested:
            note = ""

        promises.append({
            "id": pid,
            "area": key,
            "areaLabel": label,
            "era": era,
            "party": party,
            "sourceType": stype,
            "sourceDoc": clean(p.get("sourceDoc")),
            "sourceUrl": src,
            "promise": clean(p.get("promise")),
            "whatHappened": clean(p.get("whatHappened")),
            "status": status,
            "statusReason": clean(p.get("statusReason")),
            "keyNumber": clean(p.get("keyNumber")),
            "evidenceUrls": ev[:4],
            "contested": contested,
            "contestedNote": note,
        })

# order areas
order = {k: i for i, k in enumerate(AREA_ORDER)}
areas.sort(key=lambda a: (order.get(a["key"], 99), a["label"]))

# stats
stats = {"indicators": []}
sp = f"{DATA}/_stats.json"
if os.path.exists(sp):
    try:
        stats = json.load(open(sp))
    except Exception as e:
        problems.append(f"_stats.json failed to parse — {e}")

# ---- scoring ----
# A "kept" score counts delivered fully + largely as kept. in-progress and superseded
# are excluded from the denominator: neither is a completed promise you can fairly score.
KEPT = {"delivered", "largely"}
BROKEN = {"partly", "not-delivered", "abandoned"}

def score(items):
    c = Counter(p["status"] for p in items)
    kept = sum(c[s] for s in KEPT)
    broken = sum(c[s] for s in BROKEN)
    denom = kept + broken
    return {
        "total": len(items),
        "counts": {s: c.get(s, 0) for s in VALID_STATUS},
        "kept": kept,
        "broken": broken,
        "scored": denom,
        "keptPct": round(100 * kept / denom) if denom else None,
    }

by_era = {e: score([p for p in promises if p["era"] == e]) for e in VALID_ERA}
by_party = {}
for e in VALID_ERA:
    for pt in VALID_PARTY:
        sel = [p for p in promises if p["era"] == e and p["party"] == pt]
        if sel:
            by_party[f"{e}|{pt}"] = score(sel)
by_area = {}
for a in areas:
    for e in VALID_ERA:
        sel = [p for p in promises if p["area"] == a["key"] and p["era"] == e]
        if sel:
            by_area[f"{a['key']}|{e}"] = score(sel)
by_srctype = {}
for e in VALID_ERA:
    for st in VALID_SRC:
        sel = [p for p in promises if p["era"] == e and p["sourceType"] == st]
        if sel:
            by_srctype[f"{e}|{st}"] = score(sel)

out = {
    "generated": "2026-08-18",
    "areas": areas,
    "promises": promises,
    "stats": stats,
    "scores": {"byEra": by_era, "byParty": by_party, "byArea": by_area,
               "bySourceType": by_srctype},
}
json.dump(out, open(OUT, "w"), indent=None, separators=(",", ":"), ensure_ascii=False)

# ---- report ----
print(f"Areas: {len(areas)}   Promises: {len(promises)}")
print(f"Dataset: {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB)\n")
print("BY ERA")
for e in ("labour", "national"):
    s = by_era[e]
    print(f"  {e:9} total={s['total']:3}  kept={s['kept']:3} broken={s['broken']:3} "
          f"scored={s['scored']:3}  kept%={s['keptPct']}")
print("\nBY PARTY / ERA")
for k, s in sorted(by_party.items()):
    print(f"  {k:22} total={s['total']:3} kept%={s['keptPct']}")
print("\nSTATUS DISTRIBUTION")
for st, n in Counter(p["status"] for p in promises).most_common():
    print(f"  {st:15} {n:3}")
print("\nSOURCE TYPE")
for st, n in Counter(p["sourceType"] for p in promises).most_common():
    print(f"  {st:20} {n:3}")
print(f"\nContested: {sum(1 for p in promises if p['contested'])}")
print(f"Stats indicators: {len(stats.get('indicators', []))}")
print(f"\nPROBLEMS ({len(problems)}):")
for x in problems:
    print("  -", x)
