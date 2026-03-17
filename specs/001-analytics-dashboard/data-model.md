# Data Model: Sales Analytics Dashboard

**Feature**: 001-analytics-dashboard
**Date**: 2026-03-16

---

## Source Entity: Transaction

The raw unit of data loaded from `data/sales-data.csv`. Each row represents
one sales transaction.

| Field | Type | Description | Validation |
|---|---|---|---|
| date | date | Transaction date | MUST be parseable by `pd.to_datetime()` |
| order_id | string | Unique order identifier | MUST be present (used for order count) |
| product | string | Product name | Informational; not used in Phase 1 aggregations |
| category | string | Product category | MUST be non-null; derived from data (not hard-coded) |
| region | string | Geographic region | MUST be non-null; derived from data (not hard-coded) |
| quantity | integer | Units sold | Informational; not used in Phase 1 aggregations |
| unit_price | decimal | Price per unit | Informational; not used in Phase 1 aggregations |
| total_amount | decimal | Total transaction value | MUST be numeric; used in all aggregations |

**Validation rule**: All eight columns MUST be present before any derived
entity is computed. Missing columns produce an error state; no partial
rendering occurs.

---

## Derived Entity: KPI Summary

Computed once from the full Transaction dataset. Displayed as metric cards.

| Field | Derivation | Format |
|---|---|---|
| total_sales | `sum(total_amount)` across all rows | `$X,XXX,XXX` (currency, comma-separated) |
| total_orders | `count(order_id)` across all rows | Integer with comma separators |

---

## Derived Entity: Monthly Sales Series

Transactions aggregated by calendar month. Used for the trend line chart.

| Field | Derivation |
|---|---|
| month | First day of each calendar month (from `date` column) |
| monthly_sales | `sum(total_amount)` for all transactions in that month |

**Ordering**: Chronological (ascending by month).
**Expected rows**: 12 (one per month of data).

---

## Derived Entity: Category Breakdown

Transactions aggregated by product category. Used for the category bar chart.

| Field | Derivation |
|---|---|
| category | Distinct values from `category` column |
| category_sales | `sum(total_amount)` for all transactions in that category |

**Ordering**: Descending by `category_sales` (highest first).
**Expected rows**: 5 (Electronics, Accessories, Audio, Wearables, Smart Home).

---

## Derived Entity: Regional Breakdown

Transactions aggregated by geographic region. Used for the region bar chart.

| Field | Derivation |
|---|---|
| region | Distinct values from `region` column |
| region_sales | `sum(total_amount)` for all transactions in that region |

**Ordering**: Descending by `region_sales` (highest first).
**Expected rows**: 4 (North, South, East, West).

---

## Data Flow

```
data/sales-data.csv
       │
       ▼
  [Load & Validate]          ← @st.cache_data; column check; st.error + st.stop on failure
       │
       ├──► KPI Summary      ← sum(total_amount), count(order_id)
       │
       ├──► Monthly Series   ← groupby month → sum(total_amount) → sort asc
       │
       ├──► Category Breakdown ← groupby category → sum(total_amount) → sort desc
       │
       └──► Regional Breakdown ← groupby region → sum(total_amount) → sort desc
```
