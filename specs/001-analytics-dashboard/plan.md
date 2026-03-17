# Implementation Plan: Sales Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-analytics-dashboard/spec.md`

## Summary

Build a single-page Streamlit dashboard that loads ~1,000 sales transactions
from a CSV file and displays two KPI metric cards (Total Sales, Total Orders),
a monthly sales trend line chart, and two horizontal bar charts (sales by
category and by region). The dashboard validates the CSV on load and shows a
plain-language error if data is missing or malformed. Deployed to Streamlit
Community Cloud as a public URL.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit ≥1.32.0, Plotly ≥5.20.0, Pandas ≥2.2.0
**Storage**: CSV file — `data/sales-data.csv` (repository-resident, relative path)
**Testing**: None — no formal test framework (per constitution and project context)
**Target Platform**: Streamlit Community Cloud (Linux); also runs locally on macOS/Windows
**Project Type**: Single-page web application (dashboard)
**Performance Goals**: Full page load ≤5 seconds; chart render ≤2 seconds after data load
**Constraints**: Single `requirements.txt`; relative paths only; no hardcoded env config;
no Phase 2 features (auth, filtering, export, real-time DB)
**Scale/Scope**: ~1,000 rows, 5 categories, 4 regions, 12 months of data

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|---|---|---|
| I. Simplicity-First | Single `app.py`; no helper modules; `st.metric()` and Plotly Express only | ✅ Pass |
| II. Scope Discipline | No Phase 2 features (auth, filtering, export, DB); only FR-001–FR-010 in scope | ✅ Pass |
| III. Data Integrity | Column validation before render; `st.error()` + `st.stop()` on failure; exact CSV values | ✅ Pass |
| IV. Usability-First | `st.metric()` with plain-language labels; chart titles, axis labels, tooltips on all charts | ✅ Pass |
| V. Deployability | `requirements.txt` at repo root; relative data path; entry point `app.py` at repo root | ✅ Pass |

No violations. Complexity Tracking table not required.

## Project Structure

### Documentation (this feature)

```text
specs/001-analytics-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
app.py                   # Single Streamlit application file
data/
└── sales-data.csv       # Source transaction data
requirements.txt         # Pinned dependencies for Streamlit Community Cloud
```

**Structure Decision**: Single-file layout. `app.py` contains all data loading,
validation, aggregation, and chart rendering in one top-to-bottom readable file.
No `src/`, `tests/`, or module subdirectories — this is a tutorial project where
learner readability is the primary constraint (Principle I).
