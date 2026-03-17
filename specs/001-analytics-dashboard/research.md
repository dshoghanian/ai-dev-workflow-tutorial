# Research: Sales Analytics Dashboard

**Feature**: 001-analytics-dashboard
**Date**: 2026-03-16
**Phase**: 0 — Outline & Research

---

## Decision 1: Code Structure

**Decision**: Single `app.py` file containing all UI, data loading, and chart logic.

**Rationale**: The constitution (Principle I — Simplicity-First) requires code
readable by a Python learner with no prior framework experience. A single file
allows top-to-bottom reading without navigating modules. No logic is complex
enough to justify separation — each chart is a ~5-line Plotly Express call.

**Alternatives considered**:
- `app.py` + `data.py`: Rejected — data loading is a single `pd.read_csv()` call;
  extracting it to a module adds indirection for no learner benefit.
- `app.py` + `data.py` + `charts.py`: Rejected — same reasoning; each chart
  function would be used exactly once (YAGNI violation per Principle I).

---

## Decision 2: KPI Card Component

**Decision**: Streamlit's built-in `st.metric()` component.

**Rationale**: Zero custom code, professional appearance, supports the label/
value structure required by FR-001 and FR-002. Suitable for executive
presentation (NFR-2) without any CSS.

**Alternatives considered**:
- `st.markdown()` with HTML/CSS: Rejected — violates Simplicity-First; adds
  maintenance burden with no material UX improvement over `st.metric()`.
- `st.write()` with bold text: Rejected — insufficient visual weight for
  executive-facing KPI cards (fails NFR-2).

---

## Decision 3: Data Caching

**Decision**: `@st.cache_data` decorator on the CSV loading function.

**Rationale**: Streamlit reruns the entire script on any interaction. Without
caching, the CSV is re-read on every user action. `@st.cache_data` is a single
decorator line and teaches a real-world Streamlit pattern. Performance impact
is negligible at 1,000 rows but the pattern is important for learners to see.

**Alternatives considered**:
- No caching: Rejected — while functionally acceptable at 1,000 rows, omitting
  caching would teach bad habits and would degrade performance at larger scale.

---

## Decision 4: Chart Library

**Decision**: Plotly Express (via the `plotly` package).

**Rationale**: Fixed by the constitution's Technology Stack section. Plotly
Express provides interactive tooltips, professional appearance, and requires
minimal code (typically one function call per chart).

**Key Plotly Express calls**:
- Line chart: `px.line(df, x='month', y='total_amount')`
- Horizontal bar: `px.bar(df, x='total_amount', y='category', orientation='h')`

---

## Decision 5: Monthly Aggregation

**Decision**: Parse `date` column with `pd.to_datetime()`, then group by
`pd.Grouper(freq='MS')` (month start) to produce one row per calendar month.

**Rationale**: `pd.Grouper(freq='MS')` is the idiomatic Pandas approach for
calendar-month aggregation. It handles uneven month lengths and produces clean
month-start labels suitable for the x-axis.

**Alternatives considered**:
- `dt.to_period('M')`: Works but requires converting back to timestamp for
  Plotly — unnecessary extra step.
- Manual string truncation on date: Rejected — fragile, non-idiomatic.

---

## Decision 6: Data Validation Strategy

**Decision**: Validate required columns immediately after CSV load, before any
aggregation or rendering. Raise a caught exception that surfaces as
`st.error()` with a plain-language message; use `st.stop()` to halt rendering.

**Required columns**: `date`, `order_id`, `product`, `category`, `region`,
`quantity`, `unit_price`, `total_amount`.

**Rationale**: Aligns with constitution Principle III (Data Integrity) and
FR-008/FR-009. `st.stop()` is the Streamlit-idiomatic way to halt page
rendering after displaying an error.

---

## Decision 7: Deployment Configuration

**Decision**: Single `requirements.txt` at repo root with pinned versions.
Data file at `data/sales-data.csv` relative to repo root. Entry point: `app.py`
at repo root.

**Rationale**: Streamlit Community Cloud expects `requirements.txt` at repo
root and runs `streamlit run app.py` by default. Relative path `data/sales-data.csv`
works identically locally and on the cloud (constitution Principle V).

**Pinned versions** (latest stable as of 2026-03-16):
- `streamlit>=1.32.0`
- `plotly>=5.20.0`
- `pandas>=2.2.0`
