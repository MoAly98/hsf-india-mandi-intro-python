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
| `lesson-4-awkward` | every combination of leptons in every event | `project-1-taxi`: path lengths of Chicago taxi trips |

Lessons 2 to 4 have two projects that teach the same moves. Do the one that appeals to you; the Higgs project continues the analysis.

The slides are notebooks: click **Toggle Deck** in the notebook toolbar to present them.
Every code cell on a slide can be run live.

Each project is split into parts.
Every part ends with a `check` cell that prints ✅ when your answer is right and a hint when it is not yet right.
If you are stuck for more than five minutes, ask an instructor.

## Option 0: BinderHub (no installation)

Go to the url below to launch a JupyterLab session in your browser, with no GPU, 4 CPUs and 4 GB of memory, using BinderHub:

```
https://binderhub.ssl-hep.org/v2/gh/research-software-collaborations/courses-hsf-india-October2026/binder?gpuModel=&gpuCount=0&cudaMajor=undefined&cudaMinor=undefined&site=nrp&memory=4.0&cpu=4&qos=Guaranteed
```

<p align="center"><img src="https://github.com/jpivarski-talks/2024-05-22-hsf-india-tutorial-delhi/assets/1852447/9f57768b-7d3d-4b74-8364-c066fe352c39" width="75%"></p>

This session comes with all dependencies pre-installed, but not with the notebooks.
To get them, bring up a terminal by pressing the "Terminal" button:

<p align="center"><img src="https://github.com/jpivarski-talks/2024-05-22-hsf-india-tutorial-delhi/assets/1852447/9efd21b4-1cd7-45b7-80d0-a20bb0c36ac4" width="75%"></p>

Then clone this repository in that terminal with:

```shell
git clone https://github.com/MoAly98/hsf-india-mandi-scientific-python.git
```

<p align="center"><img src="https://github.com/jpivarski-talks/2024-05-22-hsf-india-tutorial-delhi/assets/1852447/89b5625b-c1db-44f7-8ce7-774ed592580e" width="75%"></p>

Now there is a `hsf-india-mandi-scientific-python` directory in the file browser that you can double-click to open the notebooks.

<p align="center"><img src="https://github.com/jpivarski-talks/2024-05-22-hsf-india-tutorial-delhi/assets/1852447/32497618-3df3-4718-b643-fa38d05d56fb" width="75%"></p>

<p align="center"><img src="https://github.com/jpivarski-talks/2024-05-22-hsf-india-tutorial-delhi/assets/1852447/9d8df96b-a463-4702-9e40-c003dc5f8694" width="75%"></p>

## Option 1: MyBinder (no installation)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MoAly98/hsf-india-mandi-scientific-python/main?urlpath=lab/tree/lesson-1-python/lecture-workbook.ipynb)

Click on the Binder badge above or go to the url below to launch a JupyterLab session in your browser with the notebooks and all dependencies pre-installed using MyBinder:

```
https://mybinder.org/v2/gh/MoAly98/hsf-india-mandi-scientific-python/main?urlpath=lab/tree/lesson-1-python/lecture-workbook.ipynb
```

## Option 2: run locally with `pixi`

First, clone this repository.

```shell
git clone https://github.com/MoAly98/hsf-india-mandi-scientific-python.git
cd hsf-india-mandi-scientific-python
```

Make sure you've [installed pixi](https://pixi.sh/latest/installation/) on your computer.

Then you can install the environment and start a local JupyterLab session with:

```shell
pixi run start
```

## Option 3: run locally with `uv` or a standard Python `venv`

Make sure you've [installed uv](https://docs.astral.sh/uv/getting-started/installation/) on your computer.

Then you can install the environment and start a local JupyterLab session with uv:

```shell
uv venv --python=3.14
source .venv/bin/activate
uv pip install -r requirements.txt
jupyter lab
```

or with a standard Python `venv`:

```shell
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Option 4: run locally with `conda`/`mamba`

Make sure you've [installed Miniforge](https://conda-forge.org/download/) on your computer.

Then you can install the environment and start a local JupyterLab session with:

```shell
conda env create -f environment.yml
conda activate hsf-india-mandi-scientific-python
jupyter lab
```

## Data

`data/SMHiggsToZZTo4L.parquet` holds 299,973 simulated events in which a Higgs boson decays to four leptons, derived from CMS Open Data.
`tools/make_data.py` makes the two smaller files from it:

- `data/higgs_events.json`: the first 50,000 events as Python lists and dictionaries (project 1)
- `data/higgs_eemumu.npz`: the 30,868 events with exactly two electrons and two muons, as flat arrays (projects 2 and 3)

It also downloads and prepares the data for the word-count project, from a public-domain source:

- `data/alice_chapters.json`: the chapters of *Alice's Adventures in Wonderland*, from [Project Gutenberg](https://www.gutenberg.org/ebooks/11)
