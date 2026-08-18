#!/usr/bin/env python3
"""Copy pass over the source data files.

Two jobs, both mechanical and both safe to script:

1. MACRONS. The research spec asked agents for ASCII-only text, which stripped the
   macrons off every Maori word in the dataset. In New Zealand English the macron is
   part of the spelling, not an optional flourish, so this puts them back.

2. DASHES. Spaced hyphens standing in for em dashes read as an authorial tic and make
   sentences longer than they need to be. Paired ones become brackets (they are almost
   always appositives); single ones become commas.

Never touches sourceUrl or evidenceUrls, and never changes a number or a claim.
"""
import json, glob, os, re, sys

DATA = "/home/claude/nz-tracker/data"
PROSE = ("promise", "whatHappened", "statusReason", "contestedNote",
         "keyNumber", "sourceDoc", "areaBlurb", "areaLabel", "note", "label")

# Longest first so multi-word names win before their parts.
MACRONS = [
    ("Te Taura Whiri i te Reo Maori", "Te Taura Whiri i te Reo Māori"),
    ("Whai Kainga Whai Oranga", "Whai Kāinga Whai Oranga"),
    ("He Whare Ahuru He Oranga Tangata", "He Whare Āhuru He Oranga Tangata"),
    ("Te Puni Kokiri", "Te Puni Kōkiri"),
    ("Te Pati Maori", "Te Pāti Māori"),
    ("Te Pukenga", "Te Pūkenga"),
    ("Te Uru Rakau", "Te Uru Rākau"),
    ("Kainga Ora", "Kāinga Ora"),
    ("Whanau Ora", "Whānau Ora"),
    ("te reo Maori", "te reo Māori"),
    ("Te Reo Maori", "Te Reo Māori"),
    ("Maori", "Māori"),
    ("Pakeha", "Pākehā"),
    ("whanau", "whānau"),
    ("kainga", "kāinga"),
    ("hapu", "hapū"),
    ("Runanga", "Rūnanga"),
    ("runanga", "rūnanga"),
    ("Maui", "Māui"),
    ("Te Kawanatanga", "Te Kāwanatanga"),
    ("Ngati", "Ngāti"),
    ("Ngai Tahu", "Ngāi Tahu"),
    ("Tamaki Makaurau", "Tāmaki Makaurau"),
    ("Waitakere", "Waitākere"),
    ("Otautahi", "Ōtautahi"),
    ("Papakainga", "Papakāinga"),
    ("papakainga", "papakāinga"),
]

def macronise(s):
    for a, b in MACRONS:
        # already-correct spellings are skipped by the plain-ASCII left side
        s = re.sub(r"\b" + re.escape(a) + r"\b", b, s)
    return s

def dedash(s):
    # paired spaced hyphens acting as brackets: "A - B - C" -> "A (B) C"
    s = re.sub(r"(?<=\w) - ([^-–—()]{3,110}?) - (?=[a-z(])", r" (\1) ", s)
    # a trailing spaced hyphen introducing an aside -> comma
    s = re.sub(r"(?<=\w) - (?=[a-z0-9$])", ", ", s)
    # one introducing a capitalised clause -> full stop, new sentence
    s = re.sub(r"(?<=\w) - (?=[A-Z])", ". ", s)
    # tidy any collisions the above can create
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r"\s+\)", ")", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    return s.strip()

def fix(s):
    return dedash(macronise(s))

changed = 0
samples = []
for path in sorted(glob.glob(f"{DATA}/*.json")):
    if os.path.basename(path).endswith(".merged"):
        continue
    try:
        d = json.load(open(path))
    except Exception as e:
        print("skip", path, e); continue

    def walk(o):
        global changed
        if isinstance(o, dict):
            for k, v in o.items():
                if k in PROSE and isinstance(v, str):
                    nv = fix(v)
                    if nv != v:
                        changed += 1
                        if len(samples) < 12 and len(v) > 60:
                            samples.append((k, v[:150], nv[:150]))
                        o[k] = nv
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)

    walk(d)
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=1)

print(f"fields rewritten: {changed}\n")
for k, a, b in samples:
    print(f"[{k}]\n  before: {a}\n  after : {b}\n")
