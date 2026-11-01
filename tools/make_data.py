"""Make the small input files for the projects.

Run from the repository root:

    python tools/make_data.py

From data/SMHiggsToZZTo4L.parquet (in the repository):

data/higgs_events.json     the first 50,000 events as plain Python lists and dictionaries
data/higgs_eemumu.npz      every event with exactly two electrons and two muons, as flat arrays

Downloaded if not already in data/ (both sources are public domain):

data/alice_chapters.json   the 12 chapters of Alice's Adventures in Wonderland, from Project Gutenberg
data/hurricanes.json       every Atlantic storm since 1950, from the NOAA HURDAT2 database
"""

import json
import re
import urllib.request
from pathlib import Path

import awkward as ak
import numpy as np

ALICE_URL = "https://www.gutenberg.org/files/11/11-0.txt"
HURDAT_URL = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2025-092326.txt"

FIELDS = ["pt", "eta", "phi", "mass", "charge"]
events = ak.from_parquet("data/SMHiggsToZZTo4L.parquet")


def lepton(record):
    return {k: (int(record[k]) if k == "charge" else round(float(record[k]), 4)) for k in FIELDS}


# project 1: lists of dictionaries
small = events[:50_000]
electrons = ak.to_list(small.electron[FIELDS])
muons = ak.to_list(small.muon[FIELDS])
runs = ak.to_list(small.run)
numbers = ak.to_list(small.event)
out = []
for run, number, es, ms in zip(runs, numbers, electrons, muons):
    out.append({
        "run": run,
        "event": number,
        "electron": [lepton(e) for e in es],
        "muon": [lepton(m) for m in ms],
    })
with open("data/higgs_events.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))

# projects 2 and 3: one flat array per lepton and per field
selected = events[(ak.num(events.electron) == 2) & (ak.num(events.muon) == 2)]
arrays = {}
for name, collection, index in [("e1", "electron", 0), ("e2", "electron", 1), ("mu1", "muon", 0), ("mu2", "muon", 1)]:
    for field in FIELDS:
        arrays[f"{name}_{field}"] = ak.to_numpy(selected[collection][field][:, index])
np.savez_compressed("data/higgs_eemumu.npz", **arrays)
print(len(out), "events in JSON,", len(selected), "events in npz")


def fetch(url, path):
    if not path.exists():
        with urllib.request.urlopen(url) as response:
            path.write_bytes(response.read())
    return path.read_text(encoding="utf-8")


# lesson 3 alternative project: the chapters of Alice's Adventures in Wonderland
raw = fetch(ALICE_URL, Path("data/alice_raw.txt"))
body = raw.split("*** START OF THE PROJECT GUTENBERG EBOOK 11 ***")[1]
body = body.split("*** END OF THE PROJECT GUTENBERG EBOOK 11 ***")[0]
# Chapter headings start at the left margin; the table of contents is indented.
pieces = re.split(r"^CHAPTER [IVX]+\.\n", body, flags=re.MULTILINE)[1:]
chapters = []
for piece in pieces:
    lines = piece.strip().split("\n")
    chapters.append({"title": lines[0].strip(), "text": "\n".join(lines[1:]).strip()})
with open("data/alice_chapters.json", "w") as f:
    json.dump(chapters, f, separators=(",", ":"), ensure_ascii=False)
print(len(chapters), "chapters in alice_chapters.json")

# lesson 4 alternative project: Atlantic storm tracks since 1950
raw = fetch(HURDAT_URL, Path("data/hurdat2_raw.txt"))
storms = []
for line in raw.strip().split("\n"):
    parts = [p.strip() for p in line.split(",")]
    if parts[0].startswith("AL"):  # header: basin+number+year, name, number of track points
        year = int(parts[0][4:8])
        storm = {"name": parts[1].title(), "year": year, "track": []}
        if year >= 1950:
            storms.append(storm)
    else:  # track point: date, time, record id, status, lat, lon, wind, pressure, ...
        storm["track"].append({
            "lat": round(float(parts[4][:-1]) * (1 if parts[4][-1] == "N" else -1), 1),
            "lon": round(float(parts[5][:-1]) * (1 if parts[5][-1] == "E" else -1), 1),
            "wind": int(parts[6]),
            "pressure": None if parts[7] == "-999" else int(parts[7]),
        })
with open("data/hurricanes.json", "w") as f:
    json.dump(storms, f, separators=(",", ":"))
print(len(storms), "storms in hurricanes.json")
