#!/usr/bin/env python3
"""Apply audit corrections to dataset.json.

Three things happen here, all of them responses to findings in AUDIT.md:

1. Status fixes. 18 promises whose OWN whatHappened text contradicts their status,
   almost all of them `in-progress` items the dataset itself records as stalled or
   moving away from target. Applied from audit-fixes.json.

2. Promise-type classification. Every promise is tagged as a discrete act (pass,
   repeal, establish, abolish — inside a government's control) or an outcome
   aspiration (reduce X to Y, ensure everyone has Z — dependent on the world).
   Discrete acts score far higher than outcome aspirations regardless of party, so
   a party's mix of the two distorts its raw score. Tagging lets the site show a
   like-for-like adjusted figure.

3. Co-signature flag. Commitments in a coalition agreement are signed by two
   parties but attributed to one. Flagging them lets the site disclose it.
"""
import json, re, sys
from collections import Counter, defaultdict

DS = "/home/claude/nz-tracker/dataset.json"
d = json.load(open(DS))
P = d["promises"]
by_id = {p["id"]: p for p in P}

# ---------- 1. status fixes ----------
fixes = json.load(open("/home/claude/nz-tracker/audit-fixes.json"))["fixes"]
applied, skipped = [], []
for f in fixes:
    p = by_id.get(f["id"])
    if not p:
        skipped.append((f["id"], "not found")); continue
    if p["status"] != f["currentStatus"]:
        skipped.append((f["id"], f"status is {p['status']}, expected {f['currentStatus']}")); continue
    p["statusWas"] = p["status"]
    p["status"] = f["proposedStatus"]
    p["auditNote"] = f["reason"]
    applied.append((f["id"], f["currentStatus"], f["proposedStatus"], f["confidence"]))

# ---------- 2. promise type ----------
# Discrete act: the government does a thing. Wholly within its control.
ACT_RE = re.compile(r"\b(pass|passed|repeal|repealed|abolish|abolished|disestablish|establish|"
                    r"introduce|legislate|enact|scrap|cancel|ban|create|set up|restore|reinstate|"
                    r"amend|replace|remove|reverse|stop|end|require|extend|fund|commission|"
                    r"appoint|launch|sign|ratify|purchase|buy|build|deliver)\b", re.I)
# Outcome aspiration: a state of the world the government hopes to bring about.
OUT_RE = re.compile(r"\b(reduce|cut|lift|raise|lower|halve|double|improve|increase|decrease|"
                    r"ensure|achieve|eliminate|end (?:child |homeless)|so that|"
                    r"access to|standard of living|by \d{4}|per cent|percent|%)\b", re.I)
# Procedural soft commitment: review, explore, investigate. Easy to satisfy.
SOFT_RE = re.compile(r"\b(review|explore|investigate|consider|consult|examine|assess|"
                     r"work towards|work with|look at|scope|inquiry into|monitor)\b", re.I)

def classify(p):
    t = p["promise"]
    has_num = bool(re.search(r"\d", t))
    soft = bool(SOFT_RE.search(t))
    out = bool(OUT_RE.search(t))
    act = bool(ACT_RE.search(t))
    # An outcome aspiration is a target for a state of the world, usually numeric.
    if out and (has_num or not act):
        return "outcome"
    if soft and not act:
        return "procedural"
    if act:
        return "act"
    return "other"

for p in P:
    p["ptype"] = classify(p)

# ---------- 3. co-signed coalition commitments ----------
COSIGN_RE = re.compile(r"both (agreement|coalition)|appears in both|national[-–—]act and national[-–—]nz",
                       re.I)
for p in P:
    p["coSigned"] = bool(p["sourceType"] == "coalition-agreement" and
                         (COSIGN_RE.search(p.get("sourceDoc","")) or COSIGN_RE.search(p.get("whatHappened",""))))

# ---------- report ----------
print(f"STATUS FIXES APPLIED: {len(applied)}  (skipped {len(skipped)})")
for i, a, b, c in applied:
    print(f"  [{c:6}] {i:52} {a:14} -> {b}")
for i, why in skipped:
    print(f"  SKIP {i}: {why}")

print("\nPROMISE TYPE MIX (share of each party's set)")
KEPT = {"delivered","largely"}
BROKEN = {"partly","not-delivered","abandoned"}
def kpct(items):
    k = sum(1 for x in items if x["status"] in KEPT)
    b = sum(1 for x in items if x["status"] in BROKEN)
    ip = sum(1 for x in items if x["status"] == "in-progress")
    den = k + b + ip
    return (round(100*k/den) if den else None), den

groups = {}
for era in ("labour","national"):
    for pt in ("Labour","Greens","NZ First","National","ACT"):
        sel = [x for x in P if x["era"]==era and x["party"]==pt]
        if sel: groups[f"{pt} ({era})"] = sel

types = ["act","outcome","procedural","other"]
hdr = f"{'group':24} {'n':>4} " + " ".join(f"{t:>10}" for t in types) + f" {'strict%':>8}"
print(hdr); print("-"*len(hdr))
for g, sel in groups.items():
    c = Counter(x["ptype"] for x in sel)
    pct, den = kpct(sel)
    print(f"{g:24} {len(sel):4} " + " ".join(f"{round(100*c[t]/len(sel)):9}%" for t in types)
          + f" {(str(pct)+'%' if pct is not None else '-'):>8}")

print("\nDATASET-WIDE kept% BY PROMISE TYPE")
for t in types:
    sel = [x for x in P if x["ptype"]==t]
    pct, den = kpct(sel)
    print(f"  {t:11} n={len(sel):4}  scored={den:4}  kept={pct}%")

print("\nIN-PROGRESS REMAINING BY ERA:", Counter(x["era"] for x in P if x["status"]=="in-progress"))
print("CO-SIGNED COALITION COMMITMENTS:", sum(1 for x in P if x["coSigned"]))

d.pop("scores", None)
d["auditApplied"] = {"statusFixes": len(applied), "date": "2026-08-18"}
json.dump(d, open(DS,"w"), ensure_ascii=False, separators=(",",":"))
print("\nwritten", DS)
