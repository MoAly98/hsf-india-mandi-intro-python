import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()
CONTENT = ["data", "img", *sorted(p.name for p in DIR.glob("lesson-*"))]

nox.needs_version = ">=2024.4.15"
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session(reuse_venv=True)
def pyodide(session: nox.Session) -> None:
    """
    Build the JupyterLite site into _output. Run with -- serve to serve it.
    """
    session.install(
        "jupyterlite-core~=0.8.6",
        "jupyterlab~=4.6.4",
        "notebook~=7.6.3",
        "jupyterlite-pyodide-kernel~=0.8.6",
        "jupyterlab-deck~=0.2.0",
    )

    # Keep the lesson/data/img layout so "../data" paths work
    content = DIR / "_content"
    shutil.rmtree(content, ignore_errors=True)
    for name in CONTENT:
        if (DIR / name).is_dir():
            shutil.copytree(DIR / name, content / name, ignore=shutil.ignore_patterns(".*"))
        else:
            content.mkdir(parents=True, exist_ok=True)
            shutil.copy2(DIR / name, content / name)

    session.run("jupyter", "lite", "build", "--contents=_content", "--output-dir=_output")

    if "serve" in session.posargs:
        session.run("jupyter", "lite", "serve", "--output-dir=_output")
