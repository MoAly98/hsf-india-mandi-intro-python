# Python for HEP analysis: HSF-India

An introduction to Python, NumPy, classes and Awkward Array for particle physics, in four lessons.
Each lesson is a short lecture followed by a longer project.
Across the projects you rebuild one analysis, the search for H → ZZ → 4 leptons in simulated CMS collisions, with each new tool.

No earlier Python experience is assumed.
The lessons prepare for the later lectures of the school on Awkward Array, HEP analysis and coffea.

## The notebooks

| Lesson | Lecture | Project |
|---|---|---|
| 1. Python | `1a-lecture-python.ipynb` | `1b-project-python.ipynb`: one event at a time, in pure Python |
| 2. NumPy | `2a-lecture-numpy.ipynb` | `2b-project-numpy.ipynb`: the same analysis on whole columns |
| 3. Classes | `3a-lecture-classes.ipynb` | `3b-project-classes.ipynb`: a four-vector class and a coffea-style processor |
| 4. Awkward Array | `4a-lecture-awkward.ipynb` | `4b-project-awkward.ipynb`: every muon in every event |

The lectures are notebooks that also work as slides: click **Toggle Deck** in the notebook toolbar.
Every code cell on a slide can be run live.

Each project is split into parts.
Every part ends with a `check` cell that prints ✅ when your answer is right and a hint when it is not yet right.
If you are stuck for more than five minutes, ask an instructor.

## Run in the browser with Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MoAly98/hsf-india-mand-intro-python/main?urlpath=lab/tree/1a-lecture-python.ipynb)

## Run on your own computer

```shell
git clone https://github.com/MoAly98/hsf-india-mand-intro-python.git
cd hsf-india-mand-intro-python
pixi init --import binder/environment.yml
pixi run jupyter lab
```

## Data

`data/SMHiggsToZZTo4L.parquet` holds 299,973 simulated events in which a Higgs boson decays to four leptons, derived from CMS Open Data.
`tools/make_data.py` makes the two smaller files from it:

- `data/higgs_events.json`: the first 50,000 events as Python lists and dictionaries (project 1)
- `data/higgs_eemumu.npz`: the 30,868 events with exactly two electrons and two muons, as flat arrays (projects 2 and 3)
