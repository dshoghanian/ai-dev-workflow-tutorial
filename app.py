import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]

@st.cache_data
def load_data():
    return pd.read_csv("data/sales-data.csv")

df = load_data()

missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
if missing:
    st.error(f"Unable to load dashboard: missing required columns: {missing}")
    st.stop()

st.title("ShopSmart Sales Dashboard")

# KPI Summary
total_sales = df["total_amount"].sum()
total_orders = len(df)

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")

# Sales Trend Over Time
df["date"] = pd.to_datetime(df["date"])
monthly = (
    df.groupby(pd.Grouper(key="date", freq="MS"))["total_amount"]
    .sum()
    .reset_index()
    .sort_values("date")
)
fig_trend = px.line(
    monthly,
    x="date",
    y="total_amount",
    title="Sales Trend Over Time",
    labels={"date": "Month", "total_amount": "Total Sales ($)"},
)
st.plotly_chart(fig_trend, use_container_width=True)

# Sales by Category and Region (side-by-side)
col_cat, col_reg = st.columns(2)

category_sales = (
    df.groupby("category")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("total_amount", ascending=True)
)
fig_category = px.bar(
    category_sales,
    x="total_amount",
    y="category",
    orientation="h",
    title="Sales by Category",
    labels={"total_amount": "Total Sales ($)", "category": "Category"},
)
col_cat.plotly_chart(fig_category, use_container_width=True)

region_sales = (
    df.groupby("region")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("total_amount", ascending=True)
)
fig_region = px.bar(
    region_sales,
    x="total_amount",
    y="region",
    orientation="h",
    title="Sales by Region",
    labels={"total_amount": "Total Sales ($)", "region": "Region"},
)
col_reg.plotly_chart(fig_region, use_container_width=True)
