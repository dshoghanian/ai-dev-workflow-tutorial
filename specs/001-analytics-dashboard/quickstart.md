# Quickstart: Sales Analytics Dashboard

**Feature**: 001-analytics-dashboard
**Date**: 2026-03-16

---

## Prerequisites

- Python 3.11 or higher
- `pip` package manager
- `data/sales-data.csv` present at repo root (see Data section below)

---

## Local Setup

```bash
# 1. Clone the repository and switch to the feature branch
git clone <repo-url>
cd ai-dev-workflow-tutorial
git checkout 001-analytics-dashboard

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`.

---

## Data

The dashboard reads from `data/sales-data.csv` relative to the repo root.
The file must contain these columns (order does not matter):

```
date, order_id, product, category, region, quantity, unit_price, total_amount
```

If the file is missing or a required column is absent, the dashboard displays
a plain-language error message and renders nothing else.

---

## Expected Output

When running with the sample dataset you should see:

| Metric | Expected Value |
|---|---|
| Total Sales | ~$650,000–$700,000 |
| Total Orders | 482 |
| Trend chart | 12 monthly data points |
| Category chart | 5 horizontal bars (Electronics, Audio, Wearables, Smart Home, Accessories) |
| Region chart | 4 horizontal bars (North, South, East, West) |

---

## Deployment to Streamlit Community Cloud

1. Push the branch to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app** → select the repository and branch.
4. Set **Main file path** to `app.py`.
5. Click **Deploy**.

Streamlit Community Cloud installs `requirements.txt` automatically. The
`data/sales-data.csv` file must be committed to the repository (it is not
secret data).

---

## Validation Checklist

Run through these after deployment to confirm the dashboard is complete:

- [ ] Total Sales and Total Orders KPI cards visible on load
- [ ] Sales trend line chart shows 12 monthly data points in chronological order
- [ ] Category bar chart shows all 5 categories sorted highest to lowest
- [ ] Region bar chart shows all 4 regions sorted highest to lowest
- [ ] Hovering on any chart element shows a tooltip with exact value
- [ ] All values match expected calculations from the CSV
- [ ] Dashboard loads within 5 seconds
- [ ] Public URL accessible with no login or installation
