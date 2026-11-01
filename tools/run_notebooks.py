"""Run every lecture and every solution, and fail if anything goes wrong.

Run from the repository root:

    python tools/run_notebooks.py

A notebook fails if a cell raises an error that is not tagged "raises-exception",
or if a check in a solution does not print ✅.
"""

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
notebooks = (
    sorted(ROOT.glob("lesson-*/lecture-slides.ipynb"))
    + sorted(ROOT.glob("lesson-*/lecture-workbook.ipynb"))
    + sorted(ROOT.glob("lesson-*/solutions-*.ipynb"))
)

failures = []
for path in notebooks:
    nb = nbformat.read(path, as_version=4)
    NotebookClient(
        nb, timeout=900, kernel_name="python3", allow_errors=True,
        resources={"metadata": {"path": str(path.parent)}},
    ).execute()
    problems = []
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        expected_error = "raises-exception" in cell.metadata.get("tags", [])
        for output in cell.outputs:
            if output.output_type == "error" and not expected_error:
                problems.append(f"{output.ename}: {output.evalue[:200]}")
            if output.output_type == "stream" and ("❌" in output.text or "⬜" in output.text):
                problems.append(output.text.strip())
    status = "ok" if not problems else "FAILED"
    print(f"{status:7} {path.relative_to(ROOT)}")
    for problem in problems:
        print("        ", problem)
    if problems:
        failures.append(path)

sys.exit(1 if failures else 0)
