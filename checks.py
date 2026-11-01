"""Answer checks for the projects.

Use it as `check("1.3", your_answer)`. It prints one line:
✅ when the answer is right, ❌ with a hint when it is not yet right.
"""

import json
import math
import os

import numpy as np

# A short summary of each correct answer. The summaries are not the answers themselves.
EXPECTED = {
    'demo': {"kind": "number", "value": 4.0},
    '1.1': {"kind": "number", "value": 4.0},
    '1.2': {"kind": "dict", "value": {"E": 68.13000395552949, "px": -17.946101605634976, "py": 13.164443907747328, "pz": 64.39193365826549}},
    '1.3': {"kind": "number", "value": 90.28564502441989},
    '1.4': {"kind": "number", "value": 125.23404120293779},
    '1.5': {"kind": "pairs", "value": [[0, 1], [0, 2]]},
    '1.6': {"kind": "values", "count": 4639, "sum": 558818.4380976763},
    '1.7': {"kind": "values", "count": 3867, "sum": 476424.8038089793},
    '2.1': {"kind": "number", "value": 13140.0},
    '2.2': {"kind": "values", "count": 30868, "sum": 1689331.8540297598},
    '2.3': {"kind": "values", "count": 30868, "sum": 1494427.9151199907},
    '2.4': {"kind": "values", "count": 30868, "sum": 27496.0},
    '2.5': {"kind": "values", "count": 27496, "sum": 3318425.5494861603},
    '2.6': {"kind": "values", "count": 23088, "sum": 2850098.370979309},
    '3.1': {"kind": "values", "count": 4, "sum": 16.0},
    '3.2': {"kind": "values", "count": 4, "sum": 21.0},
    '3.3': {"kind": "number", "value": 4.0},
    '3.4': {"kind": "values", "count": 30868, "sum": 1689331.8540297598},
    '3.5': {"kind": "number", "value": 23088.0},
    '3.6': {"kind": "number", "value": 23088.0},
    '3.7': {"kind": "number", "value": 16333.0},
    '4.1': {"kind": "number", "value": 85838.0},
    '4.2': {"kind": "values", "count": 441394, "sum": -48917.36702334864},
    '4.3': {"kind": "values", "count": 196549, "sum": 6667151.841801643},
    '4.4': {"kind": "values", "count": 175780, "sum": 5133633.448475361},
    '4.5': {"kind": "values", "count": 83063, "sum": 4614740.521448255},
    '4.6': {"kind": "values", "count": 224419, "sum": 10977311.885259122},
    '4.7': {"kind": "values", "count": 27496, "sum": 3318425.4526348114},
    'life.1': {"kind": "number", "value": 25.0},
    'life.2': {"kind": "values", "count": 4096, "sum": 200.0},
    'life.3': {"kind": "values", "count": 4096, "sum": 38.0},
    'life.4': {"kind": "values", "count": 4096, "sum": 92.0},
    'words.1': {"kind": "dict", "value": {"alice": 2.0, "rabbit": 1.0}},
    'words.2': {"kind": "dict", "value": {"alice": 3.0, "queen": 4.0, "rabbit": 1.0}},
    'words.3': {"kind": "number", "value": 8.0},
    'words.4': {"kind": "number", "value": 2163.0},
    'words.5': {"kind": "number", "value": 691.0},
    'words.6': {"kind": "number", "value": 8652.0},
    'words.7': {"kind": "number", "value": 56.0},
    'storms.1': {"kind": "number", "value": 279.0},
    'storms.2': {"kind": "values", "count": 33647, "sum": 3066915.704},
    'storms.3': {"kind": "values", "count": 1182, "sum": 77095.0},
    'storms.4': {"kind": "values", "count": 8245, "sum": 703005.0},
    'storms.5': {"kind": "values", "count": 508, "sum": 20981.0},
    'storms.6': {"kind": "number", "value": 882.0},
}

HINTS = {
    "demo": "2 + 2 is 4.",
    "1.1": "Add the length of the electron list and the length of the muon list.",
    "1.2": "Check each formula: pz uses math.sinh of eta, and E needs the mass squared inside the square root.",
    "1.3": "add() must add all four components. mass() is the square root of E**2 minus the three momentum components squared.",
    "1.4": "Build each muon with four_momentum, add the two muons, then add z_ee and z_mumu.",
    "1.5": 'Compare muons[i]["charge"] with muons[j]["charge"].',
    "1.6": "Use != to compare the two charges in each pair, and append mass(add(z_ee, z_mumu)).",
    "1.7": "Compute z_small and z_big with min() and max(), then test 12 < z_small < 120 and 40 < z_big < 120.",
    "2.1": "Make one mask per electron, combine them with &, then call .sum().",
    "2.2": "Copy the three functions from project 1 and replace math. with np. everywhere.",
    "2.3": "z_mumu = add(four_momentum(mu1), four_momentum(mu2))",
    "2.4": 'Compare e1["charge"] with e2["charge"], and mu1["charge"] with mu2["charge"]. Join the two with &.',
    "2.5": "higgs = add(z_ee, z_mumu). Then take mass(higgs) and index it with opposite.",
    "2.6": "Use np.minimum and np.maximum of mass(z_ee) and mass(z_mumu). Join four comparisons with &.",
    "3.1": "Store each argument on self, for example self.px = px. Then run the class cell again.",
    "3.2": "__add__ returns FourVector(self.E + other.E, self.px + other.px, ...). Run the class cell again.",
    "3.3": "mass returns np.sqrt(self.E**2 - self.px**2 - self.py**2 - self.pz**2). Run the class cell again.",
    "3.4": "Use the same formulas as project 2, with np.sin, np.sinh and np.sqrt.",
    "3.5": 'opposite compares the charges of both pairs, z_mumu adds the two muon vectors, and the histogram gets (z_ee + z_mumu).mass[selected].',
    "3.6": "total = {key: total[key] + output[key] for key in total}",
    "3.7": "Inside the new class: def __init__(self): super().__init__(z_small=(20, 120), z_big=(60, 120))",
    "4.1": "ak.num(events.muon) == 2 is a mask with one value per event. ak.sum counts its True values.",
    "4.2": "events.muon.pt * np.sinh(events.muon.eta)",
    "4.3": "ak.max(events.muon.pt, axis=1)",
    "4.4": "Index muons with the flat mask ak.num(muons) == 2.",
    "4.5": "Add mu1 and mu2, then index with mu1.charge != mu2.charge.",
    "4.6": "The same as Part 5: add mu1 and mu2, then index with mu1.charge != mu2.charge.",
    "4.7": "Take the two electrons and two muons with [:, 0] and [:, 1], require opposite charges in both pairs, and take the mass of the sum of all four.",
    "life.1": "world.sum() adds every 0 and 1 in the grid.",
    "life.2": "Loop dy and dx over (-1, 0, 1), skip (0, 0), and add np.roll(np.roll(world, dy, axis=0), dx, axis=1) each time.",
    "life.3": "survive = (world == 1) & ((neighbours == 2) | (neighbours == 3)), born = (world == 0) & (neighbours == 3). Return (survive | born).astype(np.int32).",
    "life.4": "world = step_numpy(world), one hundred times, inside for _ in range(100).",
    "words.1": "Store the argument: self.counts = counts. Then run the class cell again.",
    "words.2": "Copy self.counts with dict(), add the other counts with merged.get(word, 0) + count, and return Tally(merged). Run the class cell again.",
    "words.3": "Return sum(self.counts.values()). Run the class cell again.",
    "words.4": "Loop over words(text) and count with counts.get(word, 0) + 1. Return Tally(counts).",
    "words.5": 'Start from tally(text), keep the words with len(word) >= self.min_length, and return {"words": Tally(kept), "chapters": 1}.',
    "words.6": "total = {key: total[key] + output[key] for key in total}",
    "words.7": "Inside the new class: def __init__(self): super().__init__(min_length=9)",
    "storms.1": "ak.num(storms.track) counts the points of every storm. ak.sum counts the True values of the >= 40 mask.",
    "storms.2": "storms.track.wind * 1.852",
    "storms.3": "ak.max(storms.track.wind, axis=1)",
    "storms.4": "Index storms.track with the jagged mask storms.track.wind >= 64.",
    "storms.5": "Index storms with the flat mask peak_wind >= 64.",
    "storms.6": "lowest = ak.min(hurricanes.track.pressure, axis=1), then record_low = ak.min(lowest).",
}

# For these parts the check is given the whole collection and looks at one property.
ATTRIBUTE = {"4.4": "pt", "4.5": "mass", "4.6": "mass", "words.1": "counts", "words.2": "counts"}

NOTES = {
    "1.3": "This electron pair has a mass close to the Z mass, 91 GeV.",
    "1.4": "125 GeV is less than two full Z masses, so one Z is lighter than 91 GeV.",
    "1.6": "Now plot the masses below.",
    "2.4": "About 89% of the events pass.",
    "3.4": "The same masses as project 2, now from your own class.",
    "3.6": "Ten chunks give the same answer as all events at once.",
    "4.7": "The same events as project 2, with no fixed number of leptons needed in the array.",
    "life.4": "The puffer is flying left, leaving smoke behind.",
    "storms.6": "That is Hurricane Wilma, 2005: the deepest Atlantic low on record.",
}


def _flat_values(answer):
    """Turn a list, NumPy array or Awkward Array into one flat NumPy array of numbers."""
    try:
        import awkward as ak

        if isinstance(answer, ak.Array):
            answer = ak.flatten(ak.drop_none(answer), axis=None)
            return np.asarray(ak.to_numpy(answer), dtype=float)
    except ImportError:
        pass
    return np.asarray(answer, dtype=float).ravel()


def _has_ellipsis(answer):
    if answer is Ellipsis:
        return True
    if isinstance(answer, dict):
        return any(_has_ellipsis(v) for v in answer.values())
    if isinstance(answer, (list, tuple)):
        return any(_has_ellipsis(v) for v in answer)
    return False


def _summary(answer):
    if hasattr(answer, "axes") and hasattr(answer, "values"):  # a hist histogram
        answer = answer.values()
    if isinstance(answer, dict):
        return {"kind": "dict", "value": {k: float(answer[k]) for k in sorted(answer)}}
    if isinstance(answer, (bool, int, float, np.bool_, np.integer, np.floating)):
        return {"kind": "number", "value": float(answer)}
    if isinstance(answer, list) and answer and all(isinstance(a, tuple) for a in answer):
        return {"kind": "pairs", "value": sorted([int(i), int(j)] for i, j in answer)}
    values = _flat_values(answer)
    return {"kind": "values", "count": int(values.size), "sum": float(np.nansum(values))}


def _close(a, b, rel=1e-3):
    return math.isclose(a, b, rel_tol=rel, abs_tol=1e-6)


def _same(got, want):
    if got["kind"] != want["kind"]:
        return False, None
    if want["kind"] == "number":
        return _close(got["value"], want["value"]), None
    if want["kind"] == "dict":
        if sorted(got["value"]) != sorted(want["value"]):
            return False, "The dictionary should have the keys " + ", ".join(sorted(want["value"])) + "."
        return all(_close(got["value"][k], want["value"][k]) for k in want["value"]), None
    if want["kind"] == "pairs":
        return got["value"] == want["value"], None
    if got["count"] != want["count"]:
        return False, f"You have {got['count']:,} values. The answer has {want['count']:,}."
    return _close(got["sum"], want["sum"]), None


def check(part, answer):
    if part in ATTRIBUTE and answer is not Ellipsis and answer is not None:
        try:
            answer = getattr(answer, ATTRIBUTE[part])
        except AttributeError:
            print(f"❌ Part {part}: not yet. Hint: " + HINTS.get(part, ""))
            return
    if part in ("3.1", "3.2") and answer is not Ellipsis and answer is not None:
        try:
            answer = [answer.E, answer.px, answer.py, answer.pz]
        except AttributeError:
            print(f"❌ Part {part}: not yet. Hint: " + HINTS.get(part, ""))
            return
    record = os.environ.get("CHECKS_RECORD")
    if record:
        with open(record, "a") as f:
            f.write(json.dumps({"part": part, "summary": _summary(answer)}) + "\n")
    if _has_ellipsis(answer) or answer is None:
        print(f"⬜ Part {part}: replace every ... with your code, then run the cell again.")
        return
    want = EXPECTED.get(part)
    if want is None:
        print(f"Part {part}: no answer is stored for this part.")
        return
    try:
        ok, why = _same(_summary(answer), want)
    except (TypeError, ValueError):
        ok, why = False, None
    if ok:
        note = NOTES.get(part)
        print(f"✅ Part {part}: correct." + (f" {note}" if note else ""))
    else:
        print(f"❌ Part {part}: not yet. " + (why + " " if why else "") + "Hint: " + HINTS.get(part, ""))
