# Plan: Rename Solutions with `sol_` Prefix + Add Unit Tests

## Context
Solution filenames like `001_two_sum.py` start with a digit, making them invalid Python identifiers. This prevents clean imports in test files. The fix is to rename files with a `sol_` prefix (e.g. `sol_001_two_sum.py`), then add unit tests that import `solve` directly.

---

## Part 1: Rename Solution Files

### 1a. Rename the file
`git mv solutions/easy/001_two_sum.py solutions/easy/sol_001_two_sum.py`

No changes needed inside the file — contents are unchanged. `app.py` uses `path.stem` which automatically picks up the new name `sol_001_two_sum` as the solution ID.

**Side effect on routes:** URL changes from `/solution/001_two_sum` → `/solution/sol_001_two_sum`. This is fine — no hardcoded URLs anywhere.

### 1b. Update CLAUDE.md
**File:** `CLAUDE.md` line referencing numeric prefixes:
> "Sorted by filename, so numeric prefixes (`001_`, `002_`) control display order."

Change to:
> "Sorted by filename, so `sol_`-prefixed names (`sol_001_`, `sol_002_`) control display order."

### 1c. Update documentation references (docs only — no logic changes)
These are informational updates to keep docs accurate:

| File | References to update |
|---|---|
| `docs/001/02_ImplementationPlan.md` | 4 occurrences of `001_two_sum` → `sol_001_two_sum` |
| `docs/001/01_InitialPlan.md` | 3 occurrences of `001_two_sum` → `sol_001_two_sum`; also `002_add_two_numbers` → `sol_002_add_two_numbers` |
| `docs/000/01_InitialPlan.md` | 1 occurrence of `001_two_sum` → `sol_001_two_sum` |

---

## Part 2: Add Unit Tests

### 2a. Add pytest to requirements.txt
Append `pytest` to `requirements.txt`.

### 2b. Create test files mirroring solutions structure
```text
tests/
  __init__.py          (empty)
  easy/
    __init__.py        (empty)
    test_sol_001_two_sum.py
```

### 2c. Test file implementation
Since `sol_001_two_sum` is now a valid Python identifier, import directly:
```python
from solutions.easy.sol_001_two_sum import solve
```

**Test cases:**

| Scenario | `nums` | `target` | Expected |
|---|---|---|---|
| Basic example | `[2,7,11,15]` | `9` | `[0,1]` |
| Answer at end | `[3,2,4]` | `6` | `[1,2]` |
| Duplicate values | `[3,3]` | `6` | `[0,1]` |
| Negative numbers | `[-1,-2,-3,-4,-5]` | `-8` | `[2,4]` |
| Single pair | `[1,9]` | `10` | `[0,1]` |

---

## Critical Files

| File | Action |
|---|---|
| `solutions/easy/001_two_sum.py` | `git mv` → `sol_001_two_sum.py` |
| `CLAUDE.md` | Update prefix description |
| `docs/001/02_ImplementationPlan.md` | Update 4 filename references |
| `docs/001/01_InitialPlan.md` | Update 3 filename references |
| `docs/000/01_InitialPlan.md` | Update 1 filename reference |
| `requirements.txt` | Add `pytest` |
| `tests/__init__.py` | Create (empty) |
| `tests/easy/__init__.py` | Create (empty) |
| `tests/easy/test_sol_001_two_sum.py` | Create with 5 test cases |

## No Changes Needed
- `app.py` — `path.stem` and `spec_from_file_location` work unchanged
- `templates/` — all dynamic, no hardcoded IDs

## Verification
```bash
pip install -r requirements.txt
python app.py           # check /solution/sol_001_two_sum loads correctly
pytest tests/ -v        # all 5 tests should pass
```
