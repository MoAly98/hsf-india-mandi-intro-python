# Python for HEP analysis: HSF-India

An introduction to Python, NumPy, classes and Awkward Array for particle physics, in four lessons.
Each lesson is a short lecture followed by a longer project.
Across the projects you rebuild one analysis, the search for H → ZZ → 4 leptons in simulated CMS collisions, with each new tool.

No earlier Python experience is assumed.
The lessons prepare for the later lectures of the school on Awkward Array, HEP analysis and coffea.

## The lessons

Each `lesson-*` directory has

- `lecture-slides.ipynb`: what the instructor presents
- `lecture-workbook.ipynb`: what you open to follow along, with room to try things
- `project-*.ipynb`: what you work through after the lecture

| Lesson | Higgs project | Alternative project |
|---|---|---|
| `lesson-1-python` | one event at a time, in pure Python | |
| `lesson-2-numpy` | the same analysis on whole columns | `project-life`: Conway's Game of Life |
| `lesson-3-classes` | a four-vector class that runs the whole analysis | `project-words`: counting words with classes |
| `lesson-4-awkward` | every muon in every event | `project-storms`: 75 years of Atlantic hurricanes |

Lessons 2 to 4 have two projects that teach the same moves. Do the one that appeals to you; the Higgs project continues the analysis.

The slides are notebooks: click **Toggle Deck** in the notebook toolbar to present them.
Every code cell on a slide can be run live.

Each project is split into parts.
Every part ends with a `check` cell that prints ✅ when your answer is right and a hint when it is not yet right.
If you are stuck for more than five minutes, ask an instructor.

## Run in the browser with Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MoAly98/hsf-india-mand-intro-python/main?urlpath=lab/tree/lesson-1-python/lecture-workbook.ipynb)

## Run on your own computer

```shell
git clone https://github.com/MoAly98/hsf-india-mand-intro-python.git
cd hsf-india-mand-intro-python
pixi run jupyter lab
```

## Data

`data/SMHiggsToZZTo4L.parquet` holds 299,973 simulated events in which a Higgs boson decays to four leptons, derived from CMS Open Data.
`tools/make_data.py` makes the two smaller files from it:

- `data/higgs_events.json`: the first 50,000 events as Python lists and dictionaries (project 1)
- `data/higgs_eemumu.npz`: the 30,868 events with exactly two electrons and two muons, as flat arrays (projects 2 and 3)

It also downloads and prepares the data for the alternative projects, from public-domain sources:

- `data/alice_chapters.json`: the chapters of *Alice's Adventures in Wonderland*, from [Project Gutenberg](https://www.gutenberg.org/ebooks/11)
- `data/hurricanes.json`: every Atlantic storm since 1950, from the NOAA [HURDAT2](https://www.nhc.noaa.gov/data/) database
