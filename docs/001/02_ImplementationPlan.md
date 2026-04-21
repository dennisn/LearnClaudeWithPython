# LeetCode Showcase — Implementation Plan (Design A: Flask + Pico.css)

## Context

Build a Python web app to showcase personal LeetCode solutions. Main page lists all solutions in a tree grouped by difficulty (Easy / Medium / Hard). Each solution has its own page with a parameter form, a "Run" button, and a results panel.

**Chosen stack:** Flask + Jinja2 + Pico.css (classless CSS via CDN — zero custom CSS, zero JavaScript).

---

## Final File Structure

```text
app.py                        ← Flask app, routes, solution loader
requirements.txt
solutions/
  easy/
    sol_001_two_sum.py
  medium/
  hard/
templates/
  base.html                   ← Pico.css CDN link, nav, shared layout
  index.html                  ← difficulty tree (main page)
  solution.html               ← parameter form + results panel
  error.html                  ← friendly error page
```

---

## Step 1 — Dependencies (`requirements.txt`)

```text
flask>=3.0
```

Pico.css is loaded from CDN in `base.html` — no pip package needed.

---

## Step 2 — Solution File Convention

Each file in `solutions/<difficulty>/<id>_<slug>.py` must export:

```python
TITLE = "Two Sum"
DESCRIPTION = "Given an array nums and an integer target, return indices of the two numbers that add up to target."
PARAMS = [
    {"name": "nums",   "type": "list[int]", "description": "Input array e.g. [2,7,11,15]"},
    {"name": "target", "type": "int",       "description": "Target sum e.g. 9"},
]

def solve(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
```

**Supported param types** (parsed from the form string input):

| `type` value | Parsed as |
|---|---|
| `int` | `int(value)` |
| `float` | `float(value)` |
| `str` | raw string |
| `list[int]` | `json.loads(value)` → validated as list of ints |
| `list[str]` | `json.loads(value)` → validated as list of strings |
| `bool` | `value.lower() == "true"` |

---

## Step 3 — Solution Loader (`app.py`)

At startup, scan `solutions/` and build an in-memory registry:

```python
# Pseudocode — implemented in app.py
registry = {
    "easy":   [{"id": "sol_001_two_sum", "title": "Two Sum", "module": <module>}, ...],
    "medium": [...],
    "hard":   [...],
}
```

Key behaviours:
- Use `importlib.util.spec_from_file_location` to dynamically import each `.py` file
- Skip files that are missing `TITLE`, `PARAMS`, or `solve`
- Sort by filename (numeric prefix ensures order)
- Build a flat lookup `{id: module}` for O(1) route access

---

## Step 4 — Routes (`app.py`)

| Method | Path | Action |
|---|---|---|
| `GET` | `/` | Render `index.html` with the full registry |
| `GET` | `/solution/<id>` | Render `solution.html` (form only, no result) |
| `POST` | `/solution/<id>` | Parse form, call `solve()`, re-render `solution.html` with result |

**POST logic:**
1. Look up module by `id` — 404 if not found
2. For each param in `module.PARAMS`, read `request.form[name]` and parse by `type`
3. Call `module.solve(**parsed_kwargs)`
4. Pass `result=repr(output)` back to the template
5. On any parse or runtime error, pass `error=str(e)` instead

---

## Step 5 — Templates

### `base.html`
- `<link>` to Pico.css CDN
- `<nav>` with site title linking back to `/`
- `{% block content %}` for child pages
- Semantic `<main>`, `<header>`, `<footer>`

### `index.html` (extends base)
- `<details open>` / `<summary>` for each difficulty group (Easy / Medium / Hard) — native HTML accordion, no JS
- Each solution is an `<a href="/solution/<id>">` list item

```text
Easy ▾
  • Two Sum
  • Valid Parentheses
Medium ▾
  • Add Two Numbers
Hard ▾
  (none yet)
```

### `solution.html` (extends base)
- Problem title + description
- `<form method="POST">` with one `<input type="text">` per param (label = name, placeholder = description)
- `<button type="submit">Run</button>`
- Result panel: shown only if `result` or `error` is set
  - Success: `<pre>{{ result }}</pre>`
  - Error: `<mark>{{ error }}</mark>` (Pico styles `<mark>` as a highlighted callout)
- Back link to `/`

### `error.html` (extends base)
- Generic 404 / 500 page using Pico's `<article>` card component

---

## Step 6 — Input Parsing & Safety

- Parse all inputs in a `parse_param(value, type_str)` helper in `app.py`
- Use `ast.literal_eval` as fallback for list types (safer than raw `eval`)
- Wrap `solve()` call in `try/except Exception` — never let a bad solution crash the server
- Cap execution time: wrap `solve()` with `concurrent.futures` and a 5-second timeout (cross-platform)

---

## Step 7 — Running the App

```bash
pip install -r requirements.txt
python app.py          # → http://localhost:5000
```

`app.py` ends with:
```python
if __name__ == "__main__":
    app.run(debug=True)
```

---

## Verification Checklist

1. `pip install -r requirements.txt && python app.py` — server starts with no errors
2. `GET /` — tree shows Easy / Medium / Hard groups; each group is collapsible
3. Click "Two Sum" → `GET /solution/sol_001_two_sum` — form shows `nums` and `target` inputs
4. Enter `[2,7,11,15]` and `9` → click Run → result shows `[0, 1]`
5. Enter `notvalid` for `nums` → result shows a clear error message (no 500)
6. Add `solutions/easy/002_valid_parentheses.py` → restart → appears in tree
7. Visit `/solution/doesnotexist` → friendly 404 page

---

## Implementation Order

1. `requirements.txt`
2. `solutions/easy/sol_001_two_sum.py` (sample solution to test with)
3. `app.py` — loader + all routes
4. `templates/base.html`
5. `templates/index.html`
6. `templates/solution.html`
7. `templates/error.html`
