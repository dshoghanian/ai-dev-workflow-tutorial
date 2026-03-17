---
description: "Task list for Sales Analytics Dashboard"
---

# Tasks: Sales Analytics Dashboard

**Input**: Design documents from `/specs/001-analytics-dashboard/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅

**Tests**: Not included — no formal test framework in this project (per constitution).

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- All implementation tasks edit `app.py` sequentially (single-file project)

---

## Phase 1: Setup

**Purpose**: Create the three foundational project files before any feature work begins.

- [x] T001 [P] Create `requirements.txt` at repo root with pinned dependencies: `streamlit>=1.32.0`, `plotly>=5.20.0`, `pandas>=2.2.0`
- [x] T002 [P] Create `app.py` at repo root with `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")` and import statements for `streamlit`, `plotly.express`, and `pandas`
- [x] T003 [P] Confirm `data/sales-data.csv` is present at repo root and contains all 8 required columns (`date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data loading and validation infrastructure that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Implement `load_data()` function in `app.py` decorated with `@st.cache_data` that reads `data/sales-data.csv` via `pd.read_csv()` and returns a DataFrame
- [x] T005 Implement column validation in `app.py`: after `load_data()`, check all 8 required columns are present; if any are missing display `st.error()` with a plain-language message (e.g., "Unable to load dashboard: missing required columns: {list}") and call `st.stop()` to halt rendering

**Checkpoint**: Run `streamlit run app.py` — loads without errors with valid CSV; shows plain error message with missing/malformed CSV.

---

## Phase 3: User Story 1 — View KPI Summary (Priority: P1) 🎯 MVP

**Goal**: Finance manager sees Total Sales and Total Orders as metric cards on load.

**Independent Test**: Load dashboard with `sales-data.csv` — two KPI cards appear above the fold; values match `df['total_amount'].sum()` and `len(df)` calculated directly from CSV.

### Implementation for User Story 1

- [x] T006 [US1] Compute `total_sales = df['total_amount'].sum()` and `total_orders = len(df)` in `app.py`
- [x] T007 [US1] Render two-column KPI row in `app.py` using `st.columns(2)`; display `st.metric("Total Sales", f"${total_sales:,.0f}")` in column 1 and `st.metric("Total Orders", f"{total_orders:,}")` in column 2

**Checkpoint**: KPI cards visible on load with correct values — at this point US1 is fully functional and independently demonstrable.

---

## Phase 4: User Story 2 — Explore Sales Trend Over Time (Priority: P2)

**Goal**: CEO sees a line chart of monthly sales totals across 12 months.

**Independent Test**: Line chart renders with exactly one data point per calendar month, chronological x-axis labels, and tooltip showing exact monthly sales value on hover.

### Implementation for User Story 2

- [x] T008 [US2] In `app.py`, parse `date` column with `pd.to_datetime()`, group by `pd.Grouper(freq='MS')`, aggregate `total_amount` with `.sum()`, reset index, and sort chronologically
- [x] T009 [US2] Render monthly trend line chart in `app.py` using `px.line()` with `title="Sales Trend Over Time"`, x-axis label "Month", y-axis label "Total Sales ($)", and `st.plotly_chart(fig, use_container_width=True)`

**Checkpoint**: Line chart shows 12 monthly data points with correct values and interactive tooltips — US1 and US2 both independently functional.

---

## Phase 5: User Story 3 — Compare Sales by Category (Priority: P3)

**Goal**: Marketing director sees sales ranked by product category as a horizontal bar chart.

**Independent Test**: Chart renders with all 5 categories as horizontal bars sorted highest-to-lowest; hovering shows exact sales value per category.

### Implementation for User Story 3

- [x] T010 [US3] In `app.py`, group transactions by `category`, aggregate `total_amount` with `.sum()`, sort descending by `total_amount`
- [x] T011 [US3] Render horizontal bar chart in `app.py` using `px.bar(..., orientation='h')` with `title="Sales by Category"`, x-axis label "Total Sales ($)", y-axis label "Category", bars sorted highest-to-lowest

**Checkpoint**: 5 horizontal bars sorted correctly with tooltips — US3 independently functional.

---

## Phase 6: User Story 4 — Compare Sales by Region (Priority: P4)

**Goal**: Regional manager sees sales ranked by geographic region as a horizontal bar chart.

**Independent Test**: Chart renders with all 4 regions as horizontal bars sorted highest-to-lowest; hovering shows exact sales value per region.

### Implementation for User Story 4

- [x] T012 [US4] In `app.py`, group transactions by `region`, aggregate `total_amount` with `.sum()`, sort descending by `total_amount`
- [x] T013 [US4] Render horizontal bar chart in `app.py` using `px.bar(..., orientation='h')` with `title="Sales by Region"`, x-axis label "Total Sales ($)", y-axis label "Region", bars sorted highest-to-lowest

**Checkpoint**: 4 horizontal bars sorted correctly with tooltips — all 4 user stories independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Layout refinement and final end-to-end validation.

- [x] T014 Arrange the category and region bar charts side-by-side in `app.py` using `st.columns(2)` to match the dashboard layout in the PRD
- [x] T015 Run the full quickstart.md validation checklist end-to-end: verify all 8 checklist items pass locally (`streamlit run app.py`) and on Streamlit Community Cloud (public URL accessible, values correct, load time ≤5s)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — T001, T002, T003 can all start immediately in parallel
- **Foundational (Phase 2)**: Depends on T002 (app.py exists) — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational complete — no dependency on US2/3/4
- **US2 (Phase 4)**: Depends on Foundational complete — no dependency on US1/3/4
- **US3 (Phase 5)**: Depends on Foundational complete — no dependency on US1/2/4
- **US4 (Phase 6)**: Depends on Foundational complete — no dependency on US1/2/3
- **Polish (Phase 7)**: Depends on all desired user stories complete

### Within Each User Story

- Aggregation task (T006, T008, T010, T012) before render task (T007, T009, T011, T013)
- All tasks within a story edit `app.py` — run sequentially, not in parallel

### Parallel Opportunities

- T001, T002, T003 (Setup) — all touch different files, run together
- US1 through US4 — independent of each other; can be worked in parallel by different developers
  once Foundational phase is complete

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (KPI cards)
4. **STOP and VALIDATE**: KPI values correct, error state works
5. Demo to stakeholders — this is a deployable MVP

### Incremental Delivery

1. Setup + Foundational → runnable app (shows error or blank)
2. + US1 → KPI cards → deploy/demo (**MVP**)
3. + US2 → trend chart → deploy/demo
4. + US3 → category chart → deploy/demo
5. + US4 → region chart → deploy/demo
6. + Polish → final layout + validation → production-ready

---

## Notes

- All implementation tasks edit a single `app.py` — no [P] marker on implementation tasks
- [P] applies only to Setup tasks (different files)
- Each user story phase is independently completable and demonstrable
- Commit after each phase checkpoint
- `@st.cache_data` is applied once in T004; no other caching needed
