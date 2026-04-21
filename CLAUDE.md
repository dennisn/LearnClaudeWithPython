# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
pip install -r requirements.txt
python app.py   # → http://localhost:5000
```

Flask runs in debug mode by default (`debug=True`), so the server auto-reloads on file changes. No build step required.

## Architecture

### Solution Discovery (app.py)

At startup, `app.py` scans `solutions/<difficulty>/*.py` and builds two data structures:

- **`registry`** — `dict[difficulty → list[{id, title, module}]]` used by the index page to render the tree
- **`lookup`** — `dict[id → module]` used by the solution route for O(1) access

Solutions are loaded via `importlib.util.spec_from_file_location`. Files missing `TITLE`, `PARAMS`, or `solve` are silently skipped. Sorted by filename, so `sol_`-prefixed names (`sol_001_`, `sol_002_`) control display order.

### Adding a Solution

Drop a `.py` file into `solutions/easy/`, `solutions/medium/`, or `solutions/hard/`. It must export:

```python
TITLE = "Two Sum"
DESCRIPTION = "..."
PARAMS = [
    {"name": "nums",   "type": "list[int]", "description": "e.g. [2,7,11,15]"},
    {"name": "target", "type": "int",       "description": "e.g. 9"},
]

def solve(nums: list[int], target: int):
    ...
```

Supported `type` values: `int`, `float`, `str`, `bool`, `list[int]`, `list[str]`.

### Input Parsing & Safety

`parse_param(value, type_str)` in `app.py` converts raw form strings to Python types. List types try `json.loads` first, then fall back to `ast.literal_eval`. The `solve()` call runs inside a `ThreadPoolExecutor` with a 5-second timeout to prevent the server from hanging on infinite loops.

### Templates

All templates extend `templates/base.html`, which loads Pico.css from CDN (classless — no custom CSS anywhere). Key template variables:

- `index.html`: receives `registry` dict
- `solution.html`: receives `module`, `result` (repr string or None), `error` (str or None)
- `error.html`: receives `code` (int) and `message` (str)

## Project Docs

Design alternatives and implementation rationale are in `docs/001/`. The `learning/` directory documents the Claude Code workflow used to build this project.

## Git Workflow Rules

- ALWAYS create a new feature branch before making any file modifications
- Use the naming convention `feature/[yyyyMMdd]_[DescriptionInCamelCase]`
- Check out the branch immediately after creation.
- Once implementation finished, create pull-request for review & merge.
