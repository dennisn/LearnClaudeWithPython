# LeetCode Showcase Web App — Design Alternatives

## Context

Build a Python web app (minimal CSS) to showcase LeetCode solutions. The main page lists solutions in a tree grouped by difficulty (Easy / Medium / Hard). Each solution has a dedicated page with a parameter form, a "Run" button, and a results panel.

The project is a blank slate — no existing code, no framework, no solutions yet.

---

## Design A: Flask + Server-Side Rendering + Pico.css

### 1.1 Architecture

- **Framework:** Flask (lightweight, zero boilerplate)
- **Templates:** Jinja2 (built into Flask)
- **CSS:** [Pico.css](https://picocss.com) — a *classless* framework; you write plain semantic HTML and it looks good automatically. Zero custom CSS required.
- **Interaction:** Standard HTML form POST → page reload to show result
- **Solution storage:** Plain Python modules in a `solutions/` directory, auto-discovered at startup

### 1.2 File structure

```text
app.py
solutions/
  easy/
    sol_001_two_sum.py
    ...
  medium/
    ...
  hard/
    ...
templates/
  base.html
  index.html
  solution.html
```

Each solution file exports:

- `TITLE`, `DIFFICULTY`, `PARAMS` (list of {name, type, description})
- A `solve(**kwargs)` function

### 1.3 Page flow

1. `GET /` → renders tree (grouped by difficulty)
2. `GET /solution/<id>` → renders parameter form
3. `POST /solution/<id>` → runs `solve()`, re-renders page with output

### 1.4 Pros

- Dead simple — Flask + Jinja2 is well-documented and predictable
- Pico.css means literally zero custom CSS (drop in one `<link>` tag)
- Full page reloads are easy to debug (no async complexity)
- Easy to add solutions — just drop in a `.py` file
- No JavaScript required

### 1.5 Cons

- Full page reload on every "Run" feels slightly clunky
- No live feedback during long-running solutions (no streaming)
- Harder to extend into an API later

---

## Design B: Flask + HTMX + Simple.css

### 2.1 Architecture

- **Framework:** Flask
- **Templates:** Jinja2
- **CSS:** [Simple.css](https://simplecss.org) — classless, semantic, ~4 KB; + ~5 lines of custom CSS for the tree indentation
- **Interaction:** [HTMX](https://htmx.org) — add `hx-post` / `hx-target` attributes to the form; Flask returns a partial HTML fragment; the result panel updates *without a page reload*, no JavaScript written
- **Solution storage:** Same as Design A

### 2.2 Page flow

1. `GET /` → tree rendered server-side
2. `GET /solution/<id>` → parameter form (HTMX form)
3. Form submit → `POST /solution/<id>/run` → returns `<div>` fragment → HTMX swaps it into the result panel

### 2.3 Pros

- Feels like a modern SPA (no page reload) with *zero JavaScript written*
- HTMX is just HTML attributes — minimal learning curve
- Simple.css + ~5 lines custom CSS stays truly "minimal"
- Clean separation: Flask handles logic, HTMX handles UX
- Easy to add loading spinners, error states via HTMX extensions

### 2.4 Cons

- One extra dependency (HTMX CDN or local file)
- Slightly more template complexity (base layout + partials)
- HTMX is less familiar than plain HTML forms

---

## Design C: Streamlit

### 3.1 Architecture

- **Framework:** [Streamlit](https://streamlit.io) — a pure-Python UI library
- **CSS:** None — Streamlit renders all UI from Python; no HTML or CSS written at all
- **Interaction:** Streamlit's built-in widgets (`st.text_input`, `st.button`, `st.code`, etc.)
- **Solution storage:** Same Python module convention

### 3.2 Page flow

```python
# app.py
solutions = discover_solutions()
selected = st.sidebar.radio("Solutions", solutions_tree)
params = render_param_form(selected)
if st.button("Run"):
    result = selected.solve(**params)
    st.write(result)
```

### 3.3 Pros

- **Zero CSS, zero HTML** — entire UI is Python
- Fastest to prototype (can have something working in ~50 lines)
- Built-in syntax highlighting, dataframe display, charts (useful for algorithm visualisation later)
- Great for non-web developers

### 3.4 Cons

- Looks like a Streamlit app, not a custom website — limited branding control
- Sidebar-based navigation doesn't naturally give each solution its own shareable URL
- Harder to customise layout beyond what Streamlit exposes
- Runs as a single-process app — concurrent users share state (fine for personal use, problematic for public hosting)
- Not a traditional web app; can feel out of place in a portfolio

---

## Comparison Summary

| Criterion              | A: Flask + Pico.css | B: Flask + HTMX  | C: Streamlit |
|------------------------|---------------------|------------------|--------------|
| Custom CSS written     | 0 lines             | ~5 lines         | 0 lines      |
| JavaScript written     | 0 lines             | 0 lines          | 0 lines      |
| UX quality             | Basic               | Good             | Basic        |
| Shareable URLs         | Yes                 | Yes              | Partial      |
| Setup complexity       | Low                 | Low–Medium       | Very Low     |
| Portfolio-worthiness   | High                | High             | Medium       |
| Python-only            | No (HTML templates) | No (HTML + attrs)| Yes          |

---

## Recommendation

**Design B (Flask + HTMX + Simple.css)** offers the best balance: it looks and feels modern, produces shareable URLs, requires almost no CSS, and writes no JavaScript. Design A is the safest fallback if you want to keep things even simpler. Design C is the right pick only if you want to avoid HTML entirely and don't care about URLs.

---

## Chosen Approach

**Design A (Flask + Pico.css)** — selected by user. Zero custom CSS, zero JavaScript, standard HTML form POSTs, and simple page reloads. Prioritises simplicity and learnability over UX polish.
