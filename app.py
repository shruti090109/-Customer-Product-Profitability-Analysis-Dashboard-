import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- Page Config ----------------
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

st.title("📊 Customer, Product & Profitability Analysis Dashboard")
st.markdown("---")

# ---------------- Load Data ----------------
df = pd.read_csv("cleaned_data.csv")
# ---------------- Sidebar ----------------
st.sidebar.header("Filters")

market = st.sidebar.multiselect(
    "Select Market",
    options=df["Market"].unique(),
    default=df["Market"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category Name"].unique(),
    default=df["Category Name"].unique()
)

df = df[(df["Market"].isin(market)) &
        (df["Category Name"].isin(category))]

# ---------------- KPIs ----------------
total_sales = df["Sales"].sum()
total_profit = df["Order Profit Per Order"].sum()
profit_margin = (total_profit / total_sales) * 100
total_customers = df["Customer Id"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Profit Margin", f"{profit_margin:.2f}%")
c4.metric("Customers", total_customers)

st.markdown("---")

# ---------------- Top Products ----------------
top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Product Name",
    y="Sales",
    title="Top 10 Products by Sales"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Top Customers ----------------
top_customers = (
    df.groupby("Customer Id")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_customers,
    x="Customer Id",
    y="Sales",
    title="Top 10 Customers by Sales"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Category Pie Chart ----------------
category_sales = (
    df.groupby("Category Name")["Sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    category_sales,
    names="Category Name",
    values="Sales",
    title="Category-wise Sales"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Market Profit ----------------
market_profit = (
    df.groupby("Market")["Order Profit Per Order"]
    .sum()
    .reset_index()
)

fig = px.bar(
    market_profit,
    x="Market",
    y="Order Profit Per Order",
    title="Market-wise Profit"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Region Sales ----------------
region_sales = (
    df.groupby("Order Region")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    region_sales,
    x="Order Region",
    y="Sales",
    title="Region-wise Sales"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Discount vs Profit ----------------
fig = px.scatter(
    df,
    x="Order Item Discount Rate",
    y="Order Profit Per Order",
    title="Discount vs Profit"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.success("Dashboard Created Successfully ✅")




