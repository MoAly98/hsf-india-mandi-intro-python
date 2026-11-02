# HSF-India 2026 tutorial: Introduction to Scientific Python

This repository contains everything you need to follow the "[Introduction to Scientific Python](https://indico.cern.ch/event/1724888/contributions/7255053/)" tutorial, presented at the [HSF-India Scientific Computing Workshop](https://indico.cern.ch/event/1724888/) at IIT Mandi on [Monday, November 2, 2026, 2–6 p.m. IST](https://indico.cern.ch/event/1724888/timetable/).

## Option 0: BinderHub (no installation)

Go to the url below to launch a JupyterLab session in your browser, with no GPU, 4 CPUs and 4 GB of memory, using BinderHub:

```
https://binderhub.ssl-hep.org/v2/gh/research-software-collaborations/courses-hsf-india-October2026/binder?gpuModel=&gpuCount=1&cudaMajor=undefined&cudaMinor=undefined&site=nrp&memory=10.0&cpu=4&qos=Guaranteed
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

## Option 2: JupyterLite (no installation)

Go to the url below to launch a JupyterLab session that runs Python entirely in your browser with [Pyodide](https://pyodide.org) and [JupyterLite](https://jupyterlite.readthedocs.io):

```
https://moaly98.github.io/hsf-india-mandi-scientific-python/lab/index.html
```

The notebooks are already there, but packages that Pyodide does not include need a `%pip install` in the notebook first.
This line installs all of them:

```python
%pip install awkward uproot vector "hist[plot]" "mplhep<1.3" particle
```

(`mplhep<1.3` is needed because newer versions require a newer matplotlib than the one Pyodide provides.)

Numba, JAX, pybind11, and `dask.distributed` do not work in the browser, so use another option for lesson 5.

Nothing is saved to the repository: your changes are kept in your browser's storage only.

To build and serve the site on your own computer, make sure you've [installed uv](https://docs.astral.sh/uv/getting-started/installation/) and run:

```shell
uvx nox -s pyodide -- serve
```

## Option 3: run locally with `pixi`

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

## Option 4: run locally with `uv` or a standard Python `venv`

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

Lesson 5 also needs a C and C++ compiler and [Graphviz](https://graphviz.org/download/) installed on your computer, which `pip` cannot install. JAX does not provide wheels for Intel Macs, so it is skipped there.

## Option 5: run locally with `conda`/`mamba`

Make sure you've [installed Miniforge](https://conda-forge.org/download/) on your computer.

Then you can install the environment and start a local JupyterLab session with:

```shell
conda env create -f environment.yml
conda activate hsf-india-mandi-scientific-python
jupyter lab
```

JAX is installed with `pip` inside the environment, because conda-forge has no Windows build of it, and it is skipped on Intel Macs, which it does not provide wheels for.
