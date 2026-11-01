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
    '4.1': {"kind": "number", "value": 85838.0},
    '4.2': {"kind": "values", "count": 441394, "sum": -48917.36702334864},
    '4.3': {"kind": "values", "count": 196549, "sum": 6667151.841801643},
    '4.4': {"kind": "values", "count": 175780, "sum": 5133633.448475361},
    '4.5': {"kind": "values", "count": 83063, "sum": 4614740.521448255},
    '4.6': {"kind": "values", "count": 224419, "sum": 10977311.885259122},
    '4.7': {"kind": "values", "count": 27496, "sum": 3318425.4526348114},
    'storms.1': {"kind": "number", "value": 279.0},
    'storms.2': {"kind": "values", "count": 33647, "sum": 3066915.704},
    'storms.3': {"kind": "values", "count": 1182, "sum": 77095.0},
    'storms.4': {"kind": "values", "count": 8245, "sum": 703005.0},
    'storms.5': {"kind": "values", "count": 508, "sum": 20981.0},
    'storms.6': {"kind": "number", "value": 882.0},
}

HINTS = {
    "4.1": "ak.num(events.muon) == 2 is a mask with one value per event. ak.sum counts its True values.",
    "4.2": "events.muon.pt * np.sinh(events.muon.eta)",
    "4.3": "ak.max(events.muon.pt, axis=1)",
    "4.4": "Index muons with the flat mask ak.num(muons) == 2.",
    "4.5": "Add mu1 and mu2, then index with mu1.charge != mu2.charge.",
    "4.6": "The same as Part 5: add mu1 and mu2, then index with mu1.charge != mu2.charge.",
    "4.7": "Take the two electrons and two muons with [:, 0] and [:, 1], require opposite charges in both pairs, and take the mass of the sum of all four.",
    "storms.1": "ak.num(storms.track) counts the points of every storm. ak.sum counts the True values of the >= 40 mask.",
    "storms.2": "storms.track.wind * 1.852",
    "storms.3": "ak.max(storms.track.wind, axis=1)",
    "storms.4": "Index storms.track with the jagged mask storms.track.wind >= 64.",
    "storms.5": "Index storms with the flat mask peak_wind >= 64.",
    "storms.6": "lowest = ak.min(hurricanes.track.pressure, axis=1), then record_low = ak.min(lowest).",
}

# For these parts the check is given the whole collection and looks at one property.
ATTRIBUTE = {"4.4": "pt", "4.5": "mass", "4.6": "mass"}

NOTES = {
    "4.7": "The same events as project 2, with no fixed number of leptons needed in the array.",
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
