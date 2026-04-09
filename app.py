import ast
import importlib.util
import json
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

SOLUTIONS_DIR = Path(__file__).parent / "solutions"
DIFFICULTIES = ["easy", "medium", "hard"]
TIMEOUT_SECONDS = 5

# Registry: {"easy": [{"id": "001_two_sum", "title": "...", "module": <module>}, ...], ...}
registry: dict[str, list[dict]] = {d: [] for d in DIFFICULTIES}
# Flat lookup: {"001_two_sum": <module>, ...}
lookup: dict[str, object] = {}


def _load_solutions() -> None:
    for difficulty in DIFFICULTIES:
        folder = SOLUTIONS_DIR / difficulty
        if not folder.exists():
            continue
        py_files = sorted(folder.glob("*.py"))
        for path in py_files:
            solution_id = path.stem
            spec = importlib.util.spec_from_file_location(solution_id, path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception:
                continue
            if not all(hasattr(module, attr) for attr in ("TITLE", "PARAMS", "solve")):
                continue
            entry = {"id": solution_id, "title": module.TITLE, "module": module}
            registry[difficulty].append(entry)
            lookup[solution_id] = module


_load_solutions()


def parse_param(value: str, type_str: str):
    type_str = type_str.strip()
    if type_str == "int":
        return int(value)
    if type_str == "float":
        return float(value)
    if type_str == "str":
        return value
    if type_str == "bool":
        return value.lower() == "true"
    if type_str in ("list[int]", "list[str]"):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = ast.literal_eval(value)
        if not isinstance(parsed, list):
            raise ValueError(f"Expected a list, got {type(parsed).__name__}")
        if type_str == "list[int]":
            return [int(x) for x in parsed]
        return [str(x) for x in parsed]
    raise ValueError(f"Unsupported type: {type_str}")


def _run_solve(module, kwargs):
    return module.solve(**kwargs)


@app.route("/")
def index():
    return render_template("index.html", registry=registry)


@app.route("/solution/<solution_id>", methods=["GET", "POST"])
def solution(solution_id):
    module = lookup.get(solution_id)
    if module is None:
        return render_template("error.html", code=404, message="Solution not found."), 404

    result = None
    error = None

    if request.method == "POST":
        try:
            kwargs = {}
            for param in module.PARAMS:
                raw = request.form.get(param["name"], "")
                kwargs[param["name"]] = parse_param(raw, param["type"])

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_run_solve, module, kwargs)
                try:
                    output = future.result(timeout=TIMEOUT_SECONDS)
                    result = repr(output)
                except TimeoutError:
                    error = f"Timed out after {TIMEOUT_SECONDS} seconds."
        except Exception as e:
            error = str(e)

    return render_template(
        "solution.html",
        solution_id=solution_id,
        module=module,
        result=result,
        error=error,
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="Page not found."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, message="Internal server error."), 500


if __name__ == "__main__":
    app.run(debug=True)
