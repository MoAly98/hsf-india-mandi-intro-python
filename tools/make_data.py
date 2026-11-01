"""Make the two small input files for projects 1, 2 and 3 from the Parquet file.

Run from the repository root:

    python tools/make_data.py

data/higgs_events.json   the first 50,000 events as plain Python lists and dictionaries
data/higgs_eemumu.npz    every event with exactly two electrons and two muons, as flat arrays
"""

import json

import awkward as ak
import numpy as np

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

