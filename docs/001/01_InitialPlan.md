# LeetCode Showcase Web App — Design Alternatives

## Context

Build a Python web application (minimal CSS) to showcase personal LeetCode solutions.
- **Main page:** tree listing all solutions grouped by difficulty (Easy / Medium / Hard)
- **Solution page:** form to enter parameters, "Run" button, results panel
- Starting from a blank repository — no existing code, no solutions yet

---

## Design A: Flask + Pico.css (Pure Server-Side)

### Architecture
- **Framework:** Flask
- **Templates:** Jinja2 (built into Flask)
- **CSS:** [Pico.css](https://picocss.com) — classless; drop one `<link>` tag, get styled semantic HTML. Zero custom CSS.
- **Interaction:** Standard HTML `<form>` POST → full page reload to show result
- **Solution discovery:** Auto-scan `solutions/easy/`, `solutions/medium/`, `solutions/hard/` at startup

### File Structure

```text
app.py
solutions/
  easy/sol_001_two_sum.py
  medium/sol_002_add_two_numbers.py
  hard/
templates/
  base.html
  index.html
  solution.html
requirements.txt
```

### Page Flow
1. `GET /` → render difficulty tree
2. `GET /solution/<id>` → render parameter form
3. `POST /solution/<id>` → run `solve()`, re-render page with output

### Pros
- Fewest moving parts — Flask + Jinja2 is extremely well documented
- Zero custom CSS (Pico.css handles everything via semantic HTML)
- Zero JavaScript
- Full page reloads are trivially debuggable
- Adding a solution = dropping one `.py` file

### Cons
- Full page reload on every "Run" click feels dated
- No live feedback during long-running solutions (no spinner, no streaming)
- Harder to evolve into a REST API later

---

## Design B: Flask + HTMX + Simple.css (Dynamic Partials, No JS Written)

### Architecture
- **Framework:** Flask
- **Templates:** Jinja2
- **CSS:** [Simple.css](https://simplecss.org) (~4 KB classless) + ~5 lines of custom CSS for tree indentation
- **Interaction:** [HTMX](https://htmx.org) — `hx-post` / `hx-target` attributes on the form; Flask returns an HTML fragment; HTMX swaps it into the results `<div>` without a page reload. No JavaScript written.
- **Solution discovery:** Same as Design A

### File Structure

```text
app.py
solutions/
  easy/sol_001_two_sum.py
  ...
templates/
  base.html
  index.html
  solution.html
  _result.html        ← partial returned by POST /solution/<id>/run
requirements.txt
```

### Page Flow
1. `GET /` → full tree page
2. `GET /solution/<id>` → full solution page (form + empty result panel)
3. Form submit → `POST /solution/<id>/run` → returns `<div>` fragment → HTMX swaps result panel in-place

### Pros
- Feels like a modern SPA (no page reload) with **zero JavaScript written**
- HTMX is just HTML attributes — minimal new concepts
- Simple.css + 5 lines of custom CSS stays "minimal"
- Easy to add a loading indicator (`hx-indicator`) without any JS
- Clean shareable URLs per solution

### Cons
- Two extra CDN dependencies (HTMX + Simple.css)
- Slightly more template complexity (base + partials)
- HTMX requires a mental model shift for those unfamiliar with it

---

## Design C: FastAPI + Jinja2 + MVP.css (API-First)

### Architecture
- **Framework:** [FastAPI](https://fastapi.tiangolo.com) — async, auto-generates OpenAPI/Swagger docs at `/docs`
- **Templates:** Jinja2 (`Jinja2Templates` from `fastapi.templating`)
- **CSS:** [MVP.css](https://andybrewer.github.io/mvp/) — classless, ~8 KB; styled HTML with no classes
- **Interaction:** HTML forms for the web UI; JSON API endpoints callable independently (via `/docs` or `curl`)
- **Solution discovery:** Same as Design A

### File Structure

```text
main.py
solutions/
  easy/sol_001_two_sum.py
  ...
templates/
  base.html
  index.html
  solution.html
requirements.txt
```

### Page Flow
1. `GET /` → tree page (HTML)
2. `GET /solution/{id}` → solution page (HTML)
3. `POST /solution/{id}/run` → accepts form data or JSON → returns HTML or JSON depending on `Accept` header
4. `GET /docs` → free interactive Swagger UI for all endpoints

### Pros
- Auto-generated API docs at `/docs` — impressive for a portfolio piece
- Async support: long-running solutions won't block other requests
- Built-in request validation via Pydantic (type errors surfaced cleanly)
- Easy to add a frontend later — the JSON API is already there
- MVP.css gives a clean, minimal look with zero custom CSS

### Cons
- More complex than Flask for a simple showcase app
- FastAPI + Pydantic + async has a steeper learning curve
- Async benefits are mostly irrelevant for personal single-user use
- Slightly more boilerplate for Jinja2 integration vs Flask

---

## Comparison Summary

| Criterion              | A: Flask + Pico.css | B: Flask + HTMX  | C: FastAPI + MVP.css |
|------------------------|---------------------|------------------|----------------------|
| Custom CSS written     | 0 lines             | ~5 lines         | 0 lines              |
| JavaScript written     | 0 lines             | 0 lines          | 0 lines              |
| UX on "Run"            | Full page reload    | In-place swap    | Full page reload     |
| Shareable URLs         | Yes                 | Yes              | Yes                  |
| Setup complexity       | Low                 | Low–Medium       | Medium               |
| Portfolio-worthiness   | High                | High             | Very High            |
| Built-in API docs      | No                  | No               | Yes (`/docs`)        |
| Learning curve         | Low                 | Low–Medium       | Medium–High          |

---

## Chosen Design

**Design A (Flask + Pico.css)** — selected for its simplicity and low learning curve. Zero custom CSS, zero JavaScript, standard HTML form POSTs, and straightforward page reloads. Prioritises clarity and learnability over UX polish.
